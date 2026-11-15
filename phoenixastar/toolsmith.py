"""Toolsmith: the lab commissions NEW search strategies from Devin (Cognition) and only adopts what passes the verifier.

Flow (every step is a ledger decision when called from the loop):
  1. request(problem, goal)    -> opens a Devin session (POST https://api.devin.ai/v1/sessions) with a precise spec:
                                  problem statement, the official verifier source, the record, the CLI/log/FOUND
                                  conventions every strategy on the GPU box follows, and a structured-output schema
                                  {"filename", "code", "params", "notes"}.
  2. poll()                    -> GET /v1/session/{id}; when Devin reports structured output, the code is saved under
                                  search/devin/<filename>, smoke-tested locally (time-limited subprocess), and its
                                  printed solution is scored by the OFFICIAL verifier.
  3. adopt                     -> if the smoke test produced a valid solution, the strategy is appended to
                                  search/TEMPLATES.json (resource cpu) so the planner can launch it on the box.
State persists in data/toolsmith.json. Never prints or stores the API key.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import envload  # noqa: E402

API = "https://api.devin.ai/v1"
STATE = os.path.join(ROOT, "data", "toolsmith.json")
OUTDIR = os.path.join(ROOT, "search", "devin")
_lock = threading.Lock()

SCHEMA = {
    "type": "object",
    "properties": {
        "filename": {"type": "string", "description": "snake_case python filename, e.g. snake_devin.py"},
        "code": {"type": "string", "description": "the complete, self-contained python 3.10 program"},
        "params": {"type": "object", "description": "CLI params: {name: {type: int|float|enum, min, max, values, default}}"},
        "notes": {"type": "string", "description": "method summary and what you tested"},
    },
    "required": ["filename", "code", "params", "notes"],
}


def _now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def _req(method, path, body=None, timeout=60):
    envload.load()
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(API + path, data=data, method=method,
                               headers={"Authorization": "Bearer " + os.environ["DEVIN_API_KEY"],
                                        "Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=timeout) as resp:
        return json.loads(resp.read() or b"{}")


def _load():
    try:
        return json.load(open(STATE))
    except (OSError, ValueError):
        return {"sessions": []}


def _save(s):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    tmp = STATE + ".tmp"
    json.dump(s, open(tmp, "w"), indent=1)
    os.replace(tmp, STATE)


def spec_prompt(problem: str, goal: str) -> str:
    pdir = os.path.join(ROOT, "problems", problem)
    desc = open(os.path.join(pdir, "description.md")).read()[:6000]
    verifier = open(os.path.join(pdir, "verifier.py")).read()
    meta = json.load(open(os.path.join(pdir, "meta.json")))
    return f"""You are the toolsmith for an autonomous math-discovery lab. Write ONE new search program.

PROBLEM: {meta.get('title')} (slug {problem}, {meta.get('scoring')} the score; minImprovement {meta.get('minImprovement')}).
GOAL FROM THE LAB'S PLANNER: {goal}

Problem statement:
{desc}

The OFFICIAL verifier (exact; your output must pass it):
```python
{verifier}
```
Solution schema: {json.dumps(meta.get('solutionSchema'))}

Conventions every strategy follows (mandatory):
- Python 3.10, standard library + numpy (+ numba if helpful). Single process, single thread. No network.
- CLI with argparse: --seed (int), --seconds (float, wall-clock budget), --out (directory, default runs/devin), plus your own tuning params.
- Seed from the public best solution if useful: it is passed as a JSON file via --init (optional arg) containing {{"data": <solution dict>}}.
- On every improvement print one line: [<name> s<seed>] t=<seconds>s best=<score>   (score as the verifier computes it)
- Write <out>/best_s<seed>.json = {{"score": <score>, "solution": <solution dict>}} on every improvement.
- If the score beats the record by more than minImprovement, also write <out>/FOUND_s<seed>.json with the same content.
- As the LAST line of stdout before exiting, print the best solution dict as compact JSON (exactly what the verifier's evaluate() takes).
- Must respect --seconds and exit cleanly. Test it yourself against the verifier above for at least 60 seconds.

Return your result as structured output with this JSON schema: {json.dumps(SCHEMA)}
"""


def request(problem: str, goal: str, title: str | None = None) -> dict:
    body = {"prompt": spec_prompt(problem, goal), "idempotent": False,
            "title": title or f"LTD toolsmith: {problem}"}
    out = _req("POST", "/sessions", body)
    rec = {"session_id": out.get("session_id"), "url": out.get("url"), "problem": problem, "goal": goal,
           "status": "working", "created": _now(), "updated": _now(), "filename": None, "smoke": None, "adopted": False}
    with _lock:
        s = _load(); s["sessions"].insert(0, rec); _save(s)
    return rec


def _extract(sess: dict) -> dict | None:
    so = sess.get("structured_output")
    if isinstance(so, str):
        try:
            so = json.loads(so)
        except ValueError:
            so = None
    if isinstance(so, dict) and so.get("code"):
        return so
    # fallback: the last message containing a python code block
    for m in reversed(sess.get("messages") or []):
        txt = m.get("message") or ""
        blk = re.findall(r"```python\n(.*?)```", txt, re.S)
        if blk:
            return {"filename": "devin_strategy.py", "code": blk[-1], "params": {}, "notes": "extracted from message"}
    return None


def run_in_modal(code: str, args: list[str], files: dict[str, str], seconds: int) -> tuple[int, str, str]:
    """Run untrusted (AI-written) code in a Modal sandbox: no network, no secrets, hard timeout."""
    import base64
    import modal
    app = modal.App.lookup("phoenixastar-sandboxes", create_if_missing=True)
    image = modal.Image.debian_slim(python_version="3.11").pip_install("numpy", "numba")
    setup = [f"echo {base64.b64encode(code.encode()).decode()} | base64 -d > /tmp/prog.py"]
    for name, content in files.items():
        setup.append(f"echo {base64.b64encode(content.encode()).decode()} | base64 -d > /tmp/{name}")
    cmd = " && ".join(setup + ["mkdir -p /tmp/out", "cd /tmp && python /tmp/prog.py " + " ".join(args)])
    sb = modal.Sandbox.create("bash", "-c", cmd, app=app, image=image, timeout=seconds + 120, block_network=True, cpu=2.0)
    sb.wait(raise_on_termination=False)
    return sb.returncode, sb.stdout.read(), sb.stderr.read()


def smoke_test(problem: str, path: str, seconds: int = 60) -> dict:
    """Run the program in a Modal sandbox with a short budget, verify its last stdout line with the official verifier (locally)."""
    pdir = os.path.join(ROOT, "problems", problem)
    best = json.load(open(os.path.join(pdir, "best_solutions.json")))
    best = best if isinstance(best, list) else best.get("solutions", best)
    t0 = time.time()
    try:
        rc, out, err = run_in_modal(open(path).read(),
                                    ["--seed", "0", "--seconds", str(seconds), "--out", "/tmp/out", "--init", "/tmp/init.json"],
                                    {"init.json": json.dumps({"data": best[0]["data"]})}, seconds)
        last = [l for l in out.strip().splitlines() if l.strip().startswith("{")]
        if not last:
            return {"ok": False, "where": "modal", "error": f"no JSON solution on stdout (rc={rc}): {err[-400:]}", "seconds": round(time.time() - t0, 1)}
        sol = json.loads(last[-1])
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "where": "modal", "error": f"{type(e).__name__}: {e}"[:400], "seconds": round(time.time() - t0, 1)}
    v = subprocess.run([sys.executable, "-I", "-B", "-c",
                        "import json,sys,importlib.util;spec=importlib.util.spec_from_file_location('v',sys.argv[1]);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);print(json.dumps(m.evaluate(json.load(open(sys.argv[2])))))",
                        os.path.join(pdir, "verifier.py"), _dump(sol)], capture_output=True, text=True, timeout=600)
    if v.returncode != 0:
        msg = v.stderr.strip().splitlines()[-1][:300] if v.stderr.strip() else "verifier error"
        return {"ok": False, "where": "modal", "error": "verifier rejected: " + msg, "seconds": round(time.time() - t0, 1)}
    return {"ok": True, "where": "modal", "score": float(json.loads(v.stdout.strip())), "seconds": round(time.time() - t0, 1)}


def _dump(sol) -> str:
    p = os.path.join(ROOT, "data", "toolsmith_candidate.json")
    json.dump(sol, open(p, "w"))
    return p


def _adopt(rec: dict, so: dict, path: str):
    tp = os.path.join(ROOT, "search", "TEMPLATES.json")
    t = json.load(open(tp))
    name = "devin_" + os.path.splitext(os.path.basename(path))[0].replace("-", "_")
    params = {"seed": {"type": "int", "min": 0, "max": 100000, "default": 0},
              "seconds": {"type": "float", "min": 60, "max": 36000, "default": 21600}}
    for k, v in (so.get("params") or {}).items():
        if isinstance(v, dict) and k not in params and v.get("type") in ("int", "float", "enum"):
            params[k] = v
    fam = "devin_" + rec["problem"].replace("-", "_")
    t[name] = {"problem": rec["problem"], "script": os.path.relpath(path, ROOT), "resource": "cpu", "params": params,
               "out": f"runs/{fam}", "log": f"runs/{fam}/{{id}}.log", "made_by": "Devin (toolsmith)",
               "devin_session": rec.get("url"), "notes": (so.get("notes") or "")[:500]}
    json.dump(t, open(tp, "w"), indent=1)
    return name


def poll() -> list[dict]:
    """Advance every open session; returns the session records (newest first)."""
    with _lock:
        s = _load()
    changed = False
    for rec in s["sessions"]:
        if rec.get("status") in ("adopted", "rejected", "failed", "expired"):
            continue
        try:
            sess = _req("GET", f"/session/{rec['session_id']}")
        except urllib.error.HTTPError as e:
            rec["status"] = f"error {e.code}"; changed = True; continue
        except Exception:  # noqa: BLE001
            continue
        st = sess.get("status_enum") or sess.get("status") or "working"
        rec["devin_status"] = st; rec["updated"] = _now(); changed = True
        so = _extract(sess)
        if so and rec.get("filename") is None:
            os.makedirs(OUTDIR, exist_ok=True)
            fn = re.sub(r"[^a-z0-9_]", "_", (so.get("filename") or "devin_strategy.py").lower().removesuffix(".py")) + ".py"
            path = os.path.join(OUTDIR, fn)
            open(path, "w").write(so["code"])
            rec["filename"] = os.path.relpath(path, ROOT); rec["notes"] = (so.get("notes") or "")[:1000]
            rec["status"] = "testing"
            res = smoke_test(rec["problem"], path)
            rec["smoke"] = res
            if res.get("ok"):
                rec["template"] = _adopt(rec, so, path); rec["status"] = "adopted"; rec["adopted"] = True
            else:
                rec["status"] = "rejected"
        elif st in ("expired",):
            rec["status"] = "expired"
        elif st in ("blocked", "finished") and not so:
            rec["status"] = "waiting-output"
    if changed:
        with _lock:
            _save(s)
    return s["sessions"]


def sessions() -> list[dict]:
    return _load()["sessions"]


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["request", "poll", "list"])
    ap.add_argument("--problem", default="snake-in-the-box-13")
    ap.add_argument("--goal", default="Beat the record by extending or repairing the best known snake (local surgery: cut a segment and regrow it longer with pruned DFS / beam search).")
    a = ap.parse_args()
    if a.cmd == "request":
        r = request(a.problem, a.goal); print(json.dumps({k: r[k] for k in ("session_id", "url", "status")}))
    elif a.cmd == "poll":
        for r in poll(): print(json.dumps({k: r.get(k) for k in ("session_id", "problem", "status", "devin_status", "filename", "smoke", "template")}))
    else:
        for r in sessions(): print(json.dumps({k: r.get(k) for k in ("session_id", "problem", "status", "url")}))
