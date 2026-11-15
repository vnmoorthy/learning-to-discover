"""Modal agent sandboxes (sponsor: Modal).

An OpenAI model writes n diverse, self-contained Python search programs for a cheap problem; all n run in
parallel in isolated `modal.Sandbox`es (no network, no secrets); the last stdout line of each is parsed as a
solution and verified LOCALLY with the official verifier (`problems/<slug>/verifier.py`, in a subprocess with a
timeout). Every run is appended to `data/sandboxes.jsonl`.

Public interface (wired to HTTP by the backend, do not change):
    run_batch(problem, n, context='') -> list[dict]   # blocking
    start_batch_async(problem, n, context='') -> None # background thread (raises if too many batches run)
    list_runs(limit=100) -> list[dict]                # newest first

Every program is logged as a decision (agent "sandbox", action "sandbox_run") through `phoenixastar.ledger` and its id is
stored as the run's `decision_id`. Set PHOENIX_LABS_LEDGER=0 to skip the ledger (tests, offline runs).

CLI test:  python3 -m phoenixastar.sandboxes sidon-45-set 8
           python3 -m phoenixastar.sandboxes --backfill   # log decisions for stored runs that have none yet
"""
from __future__ import annotations

import concurrent.futures as cf
import datetime as dt
import fcntl
import json
import os
import re
import subprocess
import sys
import threading
import time
import traceback

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROBLEMS_DIR = os.path.join(ROOT, "problems")
DATA_DIR = os.path.join(ROOT, "data")
RUNS_PATH = os.environ.get("PHOENIX_SANDBOX_RUNS", os.path.join(DATA_DIR, "sandboxes.jsonl"))

SUPPORTED = ("sidon-45-set", "spencer-discrepancy", "ring-loading-15")
MAX_N = 32
PROGRAM_BUDGET_S = 100      # what the programs are told
KILL_AFTER_S = 110          # hard kill inside the sandbox (coreutils timeout)
SANDBOX_TIMEOUT_S = 150     # Modal sandbox lifetime
VERIFY_TIMEOUT_S = 180      # local official-verifier subprocess
APP_NAME = "phoenixastar-sandboxes"
MAX_ACTIVE_BATCHES = 2      # guards the OpenAI + Modal bill against repeated clicks / proposer bursts
MAX_CODE_CHARS = 100_000    # the program goes through argv (Linux caps one argument at 128 KiB)

try:  # model names come from the shared config when the backend has written it
    from phoenixastar import config as _cfg  # type: ignore
    PROPOSER_MODEL = getattr(_cfg, "PROPOSER_MODEL", "gpt-6-astra")
except Exception:  # pragma: no cover - config not present yet
    PROPOSER_MODEL = "gpt-6-astra"
FALLBACK_MODEL = "gpt-5.5"

_lock = threading.Lock()          # file + id allocation
_active_lock = threading.Lock()
_active: dict[str, dict] = {}     # batch_id -> {problem, n, started, done}
_batch_seq = 0


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _envload() -> None:
    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)
    import envload  # noqa: WPS433  (secrets only via envload, never printed)
    envload.load()


_SECRET_RE = re.compile(r"(sk-[A-Za-z0-9_\-*]{6,}|Bearer\s+[A-Za-z0-9._\-]+|(?:api[_-]?key|token)[\"']?\s*[:=]\s*[\"']?[A-Za-z0-9._\-]{8,})",
                        re.IGNORECASE)


def _scrub(text) -> str:
    """Strip anything key-like and local home paths from text that is stored / shown in the (public) UI."""
    if not text:
        return text or ""
    text = _SECRET_RE.sub("[redacted]", str(text))
    text = text.replace(ROOT, "ROOT")
    home = os.path.expanduser("~")
    return text.replace(home, "~") if home and home != "/" else text


# ----------------------------------------------------------------------------------------------- ledger glue
def _ledger_on() -> bool:
    return os.environ.get("PHOENIX_LABS_LEDGER", "1") != "0"


def _log_decision(rec: dict, info: dict) -> int | None:
    """Log one finished program as a decision (SPEC: 'log every program + score as decisions'). Best-effort:
    returns the decision id, or None when the ledger is off/unavailable. Never raises."""
    if not _ledger_on():
        return None
    try:
        from phoenixastar import ledger  # type: ignore
        rec_score = (info.get("record") or {}).get("score")
        score = rec.get("score")
        if score is None:
            result = f"{rec['status']}: {rec.get('error') or 'no valid solution'}"
        elif rec.get("beats_record"):
            result = f"official verifier score {score} BEATS the record {rec_score}"
        elif rec.get("same_as_record"):
            result = f"official verifier score {score}: it printed the record solution itself"
        else:
            result = f"official verifier score {score} (record {rec_score}, {info['scoring']})"
        did = ledger.add_decision(
            ledger.max_cycle(), "sandbox", "sandbox_run", rec["problem"],
            {"run_id": rec["id"], "batch": rec.get("batch"), "approach": rec.get("approach"), "status": rec["status"],
             "score": score, "seconds": rec.get("seconds"), "beats_record": bool(rec.get("beats_record")),
             "same_as_record": rec.get("same_as_record")},
            _scrub(f"Modal sandbox program #{rec['id']} ({rec.get('approach') or 'approach'}): {rec.get('idea') or ''} "
                   f"Result: {result}.")[:1500],
            outcome={"observed": score, "verdict": "n/a", "note": rec["status"]},
            model=rec.get("model"), tokens=rec.get("gen_tokens"),
            latency_ms=int(1000 * float(rec.get("wall_seconds") or rec.get("seconds") or 0)))
        if rec.get("time"):
            try:
                ledger.update_decision(did, time=rec["time"])
            except Exception:
                pass
        try:
            from phoenixastar import events  # type: ignore
            events.publish("decision", ledger.get_decision(did))
            if rec.get("beats_record"):
                best = ledger.get_best(rec["problem"])
                better = best is None or best.get("score") is None or (
                    score > best["score"] if info["maximize"] else score < best["score"])
                if better:
                    ledger.set_best(rec["problem"], score, True, rec.get("solution"), f"sandbox-{rec['id']}",
                                    f"modal-sandbox:{rec['id']}", True)
                events.publish("record", {"slug": rec["problem"], "score": score, "verified": True})
                events.log(f"NEW RECORD on {rec['problem']} from Modal sandbox #{rec['id']}: {score} "
                           "(official verifier)", "record")
        except Exception:
            pass
        return int(did)
    except Exception:
        return None


def backfill_decisions() -> int:
    """Log a decision for every stored run whose decision_id is still empty (runs made before decisions were
    logged). Keeps each run's original time. Returns how many runs were backfilled."""
    if not _ledger_on():
        return 0
    todo = [r for r in _read_all() if r.get("decision_id") is None]
    done = 0
    infos: dict = {}
    for r in sorted(todo, key=lambda r: int(r.get("id", 0))):
        try:
            info = infos.setdefault(r["problem"], problem_info(r["problem"]))
        except Exception:
            continue
        if r.get("solution") and r.get("same_as_record") is None:
            r["same_as_record"] = _same(r["solution"], (info.get("record") or {}).get("solution"))
        did = _log_decision(r, info)
        if did is None:
            break
        annotate(r["id"], decision_id=did, same_as_record=r.get("same_as_record"))
        done += 1
    return done


# ----------------------------------------------------------------------------------------------- problem info
def problem_info(slug: str) -> dict:
    if slug not in SUPPORTED:
        raise ValueError(f"unsupported sandbox problem {slug!r}; supported: {', '.join(SUPPORTED)}")
    pdir = os.path.join(PROBLEMS_DIR, slug)
    meta = json.load(open(os.path.join(pdir, "meta.json")))
    best = json.load(open(os.path.join(pdir, "best_solutions.json")))
    maximize = meta.get("scoring") == "maximize"
    best = sorted(best, key=lambda b: b["score"], reverse=maximize)
    top = best[0] if best else None
    return {
        "slug": slug,
        "title": meta.get("title", slug),
        "scoring": meta.get("scoring"),
        "maximize": maximize,
        "min_improvement": float(meta.get("minImprovement") or 0.0),
        "schema": meta.get("solutionSchema", {}),
        "description": open(os.path.join(pdir, "description.md")).read(),
        "verifier_src": open(os.path.join(pdir, "verifier.py")).read(),
        "record": ({"score": top["score"], "holder": top.get("agentName"), "solution": top.get("data")}
                   if top else None),
        "leaderboard": [{"agent": b.get("agentName"), "score": b["score"]} for b in best[:5]],
    }


def beats_record(info: dict, score: float | None) -> bool:
    if score is None or not info.get("record"):
        return False
    rec = info["record"]["score"]
    eps = info["min_improvement"]
    return score > rec + eps if info["maximize"] else score < rec - eps


# Per-problem hints so the generated programs are fast and target the right regime.
_HINTS = {
    "sidon-45-set": (
        "Score = h(A)/|A| where h(A) is the size of the largest Sidon subset; LOWER is better. "
        "The record 4/7 uses 14 points with h=8. Beating it needs e.g. |A|=15 with h<=8, |A|=16 or 17 with h<=9, "
        "|A|=18 with h<=10, or |A|=12 with h<=6 (all strictly below 4/7). A (4,5)-set means every 4 points have "
        "at least 5 distinct pairwise differences, i.e. at most one coincidence among the 6 differences. "
        "Computing h exactly needs a branch-and-bound / bitmask search over subsets (n<=18 is small: a "
        "numba or bitmask max-'independent set' over the 4-term relations a+b=c+d (with a=b allowed, i.e. "
        "3-term APs) is fast). Return the best VALID set found even if it does not beat the record. Keep "
        "|elements| between 4 and 18 and |x| <= 1e9."
    ),
    "spencer-discrepancy": (
        "Score = disc(A)/sqrt(n), HIGHER is better, n<=20. Record 7/sqrt(17)~1.6977. Evaluating disc exactly "
        "needs all 2^n sign vectors: use numpy bit tricks or numba; for n<=20 that is ~1e6 vectors * n rows. "
        "Return an n x n list of lists of Python ints -1/1 (not numpy types). n<=18 keeps verification fast."
    ),
    "ring-loading-15": (
        "Score = min over 2^15 adversary choices of max prefix imbalance; HIGHER is better. Record 1.125. "
        "Values must be STRINGS: non-negative decimals like '0.4375' or fractions like '7/16' with u+v<=1 "
        "exactly. Prefer dyadic fractions (denominator a power of 2, <= 2^20) so the exact verifier agrees "
        "with your float search. Exactly 15 pairs."
    ),
}

_DEFAULT_APPROACHES = [
    "simulated annealing with incremental score updates",
    "tabu search with a short-term memory of recent moves",
    "greedy randomized construction + local improvement (GRASP)",
    "genetic algorithm with crossover of good solutions",
    "algebraic / structured seed (e.g. from known constructions) then local perturbation",
    "large neighbourhood search: destroy-and-repair of a few coordinates",
    "random restarts hill climbing with numba-accelerated evaluation",
    "perturbation of the current record solution (iterated local search)",
]


def _system_prompt() -> str:
    return (
        "You are a research engineer in an autonomous mathematics lab. You write complete, self-contained "
        "Python 3.12 programs that SEARCH for constructions for an open optimization problem. Hard rules: "
        "only numpy, numba and the standard library are available; there is no network and no filesystem "
        "input; the program must stop by itself within the given wall-clock budget (check time.time()); it "
        "must print exactly one JSON object (the solution dict accepted by the verifier) as the LAST line "
        "of stdout, using json.dumps on plain Python types (int/str/list, never numpy scalars). It may print "
        "short progress lines before that. Re-implement the verifier's checks inside the program and only "
        "print a candidate that passes them. Prefer correctness over cleverness: a valid weaker solution "
        "is better than an invalid one. Never print the current record solution unchanged: print the best "
        "construction your search found that DIFFERS from it (it may score worse; seeding from it is allowed)."
    )


def _problem_block(info: dict, context: str) -> str:
    rec = info["record"]
    parts = [
        f"# Problem: {info['title']} (slug {info['slug']}), scoring: {info['scoring']}",
        "## Description", info["description"].strip(),
        "## Official verifier (exact; your output is checked with this)", "```python",
        info["verifier_src"].strip(), "```",
        "## Solution schema", json.dumps(info["schema"]),
        "## Current record", json.dumps({"score": rec["score"], "holder": rec["holder"],
                                          "solution": rec["solution"]}) if rec else "none",
        "## Leaderboard top", json.dumps(info["leaderboard"]),
        "## Practical notes", _HINTS.get(info["slug"], ""),
    ]
    if context:
        parts += ["## Lab context (memory, lessons, recent results)", context.strip()[:6000]]
    return "\n".join(parts)


def _openai():
    _envload()
    from openai import OpenAI
    return OpenAI(timeout=240.0, max_retries=2)


def _respond(client, prompt: str, schema: dict, name: str, effort: str) -> tuple[dict, str, int]:
    last = None
    for model in (PROPOSER_MODEL, FALLBACK_MODEL):
        try:
            r = client.responses.create(
                model=model,
                instructions=_system_prompt(),
                input=prompt,
                reasoning={"effort": effort},
                text={"format": {"type": "json_schema", "name": name, "strict": True, "schema": schema}},
            )
            tokens = int(getattr(r.usage, "total_tokens", 0) or 0) if getattr(r, "usage", None) else 0
            return json.loads(r.output_text), model, tokens
        except Exception as e:  # try the fallback model
            last = e
    raise RuntimeError(f"OpenAI call failed: {last}")


def plan_approaches(client, info: dict, n: int, context: str) -> list[dict]:
    schema = {
        "type": "object", "additionalProperties": False, "required": ["approaches"],
        "properties": {"approaches": {"type": "array", "items": {
            "type": "object", "additionalProperties": False, "required": ["name", "idea"],
            "properties": {"name": {"type": "string"}, "idea": {"type": "string"}}}}},
    }
    prompt = (_problem_block(info, context) + f"\n\n## Task\nPropose exactly {n} MUTUALLY DIVERSE search "
              "approaches (different algorithms, representations, sizes |A| or n, seeds/initialisations), each "
              "implementable as a single <=100 s CPU program. One sentence each for 'idea'.")
    try:
        out, _, _ = _respond(client, prompt, schema, "approaches", "low")
        apps = [a for a in out.get("approaches", []) if a.get("idea")]
    except Exception:
        apps = []
    while len(apps) < n:  # pad deterministically if the model returned fewer
        k = len(apps)
        apps.append({"name": f"default-{k}", "idea": _DEFAULT_APPROACHES[k % len(_DEFAULT_APPROACHES)]})
    return apps[:n]


def write_program(client, info: dict, approach: dict, idx: int, n: int, context: str) -> dict:
    schema = {
        "type": "object", "additionalProperties": False, "required": ["idea", "code"],
        "properties": {"idea": {"type": "string"}, "code": {"type": "string"}},
    }
    prompt = (_problem_block(info, context) +
              f"\n\n## Task\nWrite program {idx + 1} of {n}. Approach: {approach['name']}: {approach['idea']}\n"
              f"Use random seed {1000 + idx}. Wall-clock budget: stop searching after {PROGRAM_BUDGET_S - 20} s "
              f"and print the final answer well before {PROGRAM_BUDGET_S} s (numba compile time counts). "
              "Return JSON with 'idea' (one sentence) and 'code' (the full program source).")
    out, model, tokens = _respond(client, prompt, schema, "program", "medium")
    code = out.get("code", "")
    if code.startswith("```"):
        code = code.strip("`")
        code = code.split("\n", 1)[1] if "\n" in code else code
    return {"idea": out.get("idea", approach["idea"]), "code": code, "model": model, "tokens": tokens}


# ------------------------------------------------------------------------------------------------ execution
_modal_cache: dict = {}


def _modal_handles():
    import modal
    if "app" not in _modal_cache:
        _modal_cache["app"] = modal.App.lookup(APP_NAME, create_if_missing=True)
        _modal_cache["image"] = modal.Image.debian_slim().pip_install("numpy", "numba", "scipy", "sympy")
    return modal, _modal_cache["app"], _modal_cache["image"]


def run_in_sandbox(code: str) -> dict:
    """Run one program in a fresh Modal sandbox. Returns {rc, stdout, stderr, seconds, killed}."""
    if len(code) > MAX_CODE_CHARS:
        raise ValueError(f"program is {len(code)} chars; the limit is {MAX_CODE_CHARS}")
    modal, app, image = _modal_handles()
    t0 = time.time()
    sb = modal.Sandbox.create(app=app, image=image, timeout=SANDBOX_TIMEOUT_S, block_network=True,
                              cpu=2.0, memory=2048)
    try:
        p = sb.exec("timeout", "-s", "KILL", str(KILL_AFTER_S), "python", "-c", code)
        p.wait()
        out = p.stdout.read() or ""
        err = p.stderr.read() or ""
        rc = p.returncode
    finally:
        try:
            sb.terminate()
        except Exception:
            pass
    secs = time.time() - t0
    killed = rc in (124, 137, -9) or (rc != 0 and secs >= KILL_AFTER_S)
    return {"rc": rc, "stdout": out, "stderr": err, "seconds": secs, "killed": killed}


_VERIFY_RUNNER = r"""
import json, sys, time
sys.path.insert(0, sys.argv[1])
import verifier
sol = json.loads(sys.stdin.read())
t = time.time()
try:
    s = verifier.evaluate(sol)
    print(json.dumps({"ok": True, "score": float(s), "seconds": time.time() - t}))
except Exception as e:
    print(json.dumps({"ok": False, "error": f"{type(e).__name__}: {e}"[:500], "seconds": time.time() - t}))
"""


def verify(slug: str, solution: dict, timeout: float = VERIFY_TIMEOUT_S) -> dict:
    """Official verifier in an isolated subprocess. Returns {ok, score|None, error|None}."""
    pdir = os.path.join(PROBLEMS_DIR, slug)
    try:
        cp = subprocess.run([sys.executable, "-I", "-c", _VERIFY_RUNNER, pdir], input=json.dumps(solution),
                            capture_output=True, text=True, timeout=timeout, cwd=pdir)
        line = (cp.stdout.strip().splitlines() or [""])[-1]
        res = json.loads(line) if line else {"ok": False, "error": (cp.stderr or "no output")[-500:]}
    except subprocess.TimeoutExpired:
        res = {"ok": False, "error": f"verifier timeout after {timeout}s"}
    except Exception as e:
        res = {"ok": False, "error": f"{type(e).__name__}: {e}"}
    res.setdefault("score", None)
    res.setdefault("error", None)
    return res


def _same(a: dict | None, b: dict | None) -> bool:
    """True when a solution is just the incumbent record (order-insensitive for integer sets)."""
    if not a or not b:
        return False
    if "elements" in a and "elements" in b:
        try:
            return sorted(a["elements"]) == sorted(b["elements"])
        except Exception:
            return False
    return a == b


def _parse_solution(stdout: str, strict_last: bool) -> tuple[dict | None, str | None]:
    lines = [ln.strip() for ln in stdout.splitlines() if ln.strip()]
    if not lines:
        return None, "no stdout"
    candidates = lines[-1:] if strict_last else list(reversed(lines))
    for ln in candidates:
        try:
            obj = json.loads(ln)
        except Exception:
            continue
        if isinstance(obj, dict):
            return obj, None
    return None, "last stdout line is not a JSON object"


# ------------------------------------------------------------------------------------------------ persistence
# One JSON object per line. The server and a CLI run may write at the same time, so every write holds an
# exclusive flock on the file itself and run ids are assigned at append time (max id in the file + 1).
def _parse_lines(lines) -> list[dict]:
    out = []
    for ln in lines:
        ln = ln.strip()
        if ln:
            try:
                out.append(json.loads(ln))
            except Exception:
                pass
    return out


def _append(rec: dict, info: dict | None = None) -> dict:
    """Assign the next id, log the decision (when `info` is given) and append the record."""
    os.makedirs(os.path.dirname(RUNS_PATH) or ".", exist_ok=True)
    with _lock:
        with open(RUNS_PATH, "a+") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                f.seek(0)
                mx = max([int(r.get("id", 0) or 0) for r in _parse_lines(f)] + [0])
                rec["id"] = mx + 1
                if info is not None:
                    rec["decision_id"] = _log_decision(rec, info)
                f.seek(0, os.SEEK_END)
                f.write(json.dumps(rec) + "\n")
                f.flush()
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)
    return rec


def _read_all() -> list[dict]:
    if not os.path.exists(RUNS_PATH):
        return []
    with open(RUNS_PATH) as f:
        fcntl.flock(f, fcntl.LOCK_SH)
        try:
            return _parse_lines(f)
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def list_runs(limit: int = 100) -> list[dict]:
    runs = sorted(_read_all(), key=lambda r: int(r.get("id", 0)), reverse=True)
    return runs[: max(0, int(limit))]


def active_batches() -> list[dict]:
    """Batches currently running in this process: [{batch, problem, n, started, done}]."""
    with _active_lock:
        return [dict(v, batch=k) for k, v in _active.items()]


def annotate(run_id: int, **fields) -> bool:
    """Set extra fields on a stored run (e.g. decision_id). Rewrites the file in place under the file lock."""
    if not os.path.exists(RUNS_PATH):
        return False
    with _lock:
        with open(RUNS_PATH, "r+") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                runs = _parse_lines(f)
                hit = False
                for r in runs:
                    if int(r.get("id", -1)) == int(run_id):
                        r.update(fields)
                        hit = True
                if hit:
                    f.seek(0)
                    f.write("".join(json.dumps(r) + "\n" for r in runs))
                    f.truncate()
                    f.flush()
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)
    return hit


# ------------------------------------------------------------------------------------------------ batch driver
def _one(client, info: dict, approach: dict, idx: int, n: int, context: str, batch: str) -> dict:
    slug = info["slug"]
    rec = {"id": None, "problem": slug, "time": _now(), "code": "", "status": "error", "score": None,
           "seconds": 0.0, "decision_id": None, "batch": batch, "idea": approach.get("idea", ""),
           "approach": approach.get("name", ""), "model": None, "error": None, "solution": None,
           "beats_record": False, "stdout_tail": "", "stderr_tail": ""}
    t0 = time.time()
    try:
        prog = write_program(client, info, approach, idx, n, context)
        rec.update(code=prog["code"], idea=prog["idea"], model=prog["model"], gen_tokens=prog["tokens"],
                   gen_seconds=round(time.time() - t0, 1))
        if not prog["code"].strip():
            raise RuntimeError("model returned empty code")
        run = run_in_sandbox(prog["code"])
        rec["seconds"] = round(run["seconds"], 2)
        rec["stdout_tail"] = run["stdout"][-2000:]
        rec["stderr_tail"] = run["stderr"][-1500:]
        rec["returncode"] = run["rc"]
        sol, perr = _parse_solution(run["stdout"], strict_last=not run["killed"])
        if run["killed"]:
            rec["status"] = "timeout"
            rec["error"] = f"killed after {KILL_AFTER_S}s"
        elif run["rc"] != 0 and sol is None:
            rec["status"] = "error"
            rec["error"] = (run["stderr"].strip().splitlines() or [f"exit code {run['rc']}"])[-1][:500]
        elif sol is None:
            rec["status"] = "invalid"
            rec["error"] = perr
        if sol is not None:
            v = verify(slug, sol)
            if v["ok"]:
                rec["score"] = v["score"]
                rec["solution"] = sol
                rec["beats_record"] = beats_record(info, v["score"])
                rec["same_as_record"] = _same(sol, (info.get("record") or {}).get("solution"))
                if not run["killed"]:
                    rec["status"] = "ok"
            elif not run["killed"]:
                rec["status"] = "invalid"
                rec["error"] = v["error"]
    except Exception as e:
        rec["status"] = "error"
        rec["error"] = f"{type(e).__name__}: {e}"[:800]
        rec["traceback"] = traceback.format_exc()[-1500:]
    rec["time"] = _now()
    rec["wall_seconds"] = round(time.time() - t0, 1)
    for k in ("error", "traceback", "stdout_tail", "stderr_tail"):
        if rec.get(k):
            rec[k] = _scrub(rec[k])
    _append(rec, info)  # assigns rec["id"] and rec["decision_id"]
    with _active_lock:
        if batch in _active:
            _active[batch]["done"] += 1
    return rec


def _register(problem: str, n: int) -> str:
    """Reserve a batch slot; raises RuntimeError when MAX_ACTIVE_BATCHES are already running in this process."""
    with _active_lock:
        if len(_active) >= MAX_ACTIVE_BATCHES:
            busy = ", ".join(f"{v['problem']} ({v['done']}/{v['n']} done)" for v in _active.values())
            raise RuntimeError(f"{len(_active)} sandbox batches are already running ({busy}); try again when one "
                               "finishes")
        global _batch_seq
        _batch_seq += 1   # ms + pid alone collide when the planner starts two batches back to back
        batch = f"sb-{int(time.time() * 1000)}-{os.getpid() % 1000}-{_batch_seq}"
        _active[batch] = {"problem": problem, "n": n, "started": _now(), "done": 0}
    return batch


_backfilled = False


def run_batch(problem: str, n: int, context: str = "", _batch: str | None = None) -> list[dict]:
    """Write n diverse programs with an OpenAI model, run them in parallel Modal sandboxes, verify locally."""
    global _backfilled
    info = problem_info(problem)
    n = max(1, min(int(n), MAX_N))
    batch = _batch or _register(problem, n)
    try:
        if not _backfilled:  # runs stored before per-program decisions existed get theirs once per process
            _backfilled = True
            try:
                backfill_decisions()
            except Exception:
                pass
        try:
            client = _openai()
            _modal_handles()  # resolve app/image once before fanning out
        except Exception as e:  # setup failed: record it visibly instead of dying in a background thread
            err = _scrub(f"setup failed: {type(e).__name__}: {e}")[:800]
            out = []
            for _ in range(n):
                rec = {"id": None, "problem": problem, "time": _now(), "code": "", "status": "error", "score": None,
                       "seconds": 0.0, "decision_id": None, "batch": batch, "idea": "", "approach": "", "model": None,
                       "error": err, "solution": None, "beats_record": False, "stdout_tail": "", "stderr_tail": ""}
                out.append(_append(rec, info))
            return out
        approaches = plan_approaches(client, info, n, context)
        with cf.ThreadPoolExecutor(max_workers=min(n, 16)) as ex:
            futs = [ex.submit(_one, client, info, approaches[i], i, n, context, batch) for i in range(n)]
            results = [f.result() for f in futs]
        return sorted(results, key=lambda r: r["id"])
    finally:
        with _active_lock:
            _active.pop(batch, None)


def start_batch_async(problem: str, n: int, context: str = "", callback=None) -> None:
    """Run `run_batch` in a daemon thread. Optional callback(results) is called when it finishes.
    Raises ValueError for an unsupported problem and RuntimeError when too many batches are running."""
    problem_info(problem)  # validate eagerly so the caller gets an error for a bad slug
    n = max(1, min(int(n), MAX_N))
    batch = _register(problem, n)  # synchronously, so two quick clicks cannot both slip past the limit

    def _bg():
        try:
            res = run_batch(problem, n, context, _batch=batch)
            if callback is not None:
                callback(res)
        except Exception:
            traceback.print_exc()
        finally:
            with _active_lock:
                _active.pop(batch, None)

    try:
        threading.Thread(target=_bg, name=f"sandboxes-{problem}", daemon=True).start()
    except Exception:
        with _active_lock:
            _active.pop(batch, None)
        raise


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--backfill":
        print(json.dumps({"backfilled": backfill_decisions()}))
        sys.exit(0)
    slug = sys.argv[1] if len(sys.argv) > 1 else "sidon-45-set"
    k = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    t = time.time()
    res = run_batch(slug, k)
    for r in res:
        print(json.dumps({x: r.get(x) for x in ("id", "status", "score", "seconds", "approach", "error",
                                                 "beats_record")}))
    ok = [r["score"] for r in res if r["score"] is not None]
    print(f"batch done in {time.time() - t:.0f}s: {len(ok)}/{len(res)} scored; best={min(ok) if ok and slug == 'sidon-45-set' else (max(ok) if ok else None)}")
