"""Memory benchmark (sponsor: past.dev): past.dev vs markdown vs RAG on the lab's own facts.

  1. QA set auto-built from the facts by an LLM: one question per fact (answer contained in that fact) plus a
     few cross-fact questions (answer needs two or more facts, incl. "latest value" questions).
  2. Three memory systems answer every question from ONLY what their lookup returned:
       past.dev  facts ingested under a dedicated identity `ltd-bench-<ts>` (POST /api/v1/ingest/batch, polled
                 until completed), looked up with POST /api/v1/recall (limit k, restricted to this run's
                 occurrence window so other project memory cannot leak in)
       markdown  every fact in one markdown document, always the whole file in context
       rag       OpenAI text-embedding-3-small over the same facts, cosine top-k
  3. Answers by gpt-5.4-mini, graded by a strict LLM judge (gpt-5.4-mini, exact rubric).
  4. accuracy, mean lookup latency (ms), cost in USD (token counts x public list prices; past.dev credits
     counted at $0, the credits spent are reported separately).

Public interface (wired to HTTP by the backend, do not change):
    run(facts) -> dict            # blocking, returns the benchmark (shape of memory.benchmark in SPEC + extras)
    start_async(facts) -> bool    # background thread (False = one is already running; ValueError if < 3 facts)
    latest() -> dict | None       # last completed benchmark from data/memory_benchmark.json (+ running/last_error)

At most MAX_INDEX_FACTS (most recent) facts are indexed by all three systems, and at most MAX_QUESTION_FACTS of
them get a single-fact question, so a click on "Run benchmark" stays a few minutes long however big memory grows.

A fact is {"text": str, "id"?: str, "agent"?: str, "problem"?: str, "time"?: iso str}.
CLI:  python3 -m ltd.memory_bench ltd/tests_labs/sample_facts.json
"""
from __future__ import annotations

import concurrent.futures as cf
import datetime as dt
import json
import os
import sys
import threading
import time
import traceback

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.environ.get("LTD_BENCH_PATH", os.path.join(ROOT, "data", "memory_benchmark.json"))
PAST_BASE = os.environ.get("LTD_PAST_BASE", "https://app.past.dev/api/v1")

try:
    from ltd import config as _cfg  # type: ignore
    FAST_MODEL = getattr(_cfg, "FAST_MODEL", "gpt-5.4-mini")
    EMBED_MODEL = getattr(_cfg, "EMBED_MODEL", "text-embedding-3-small")
except Exception:  # pragma: no cover
    FAST_MODEL, EMBED_MODEL = "gpt-5.4-mini", "text-embedding-3-small"
ANSWER_MODEL = FAST_MODEL
JUDGE_MODEL = FAST_MODEL
QA_MODEL = "gpt-5.5"           # writes the questions; its cost is benchmark overhead, not charged to a system
TOP_K = 5
INGEST_TIMEOUT_S = 600
MAX_INDEX_FACTS = 100      # most recent facts every system indexes (keeps the past.dev ingest + run < ~5 min)
MAX_QUESTION_FACTS = 30    # facts that get a 'single' question (spread over time); cross questions come on top

# Public list prices, USD per 1M tokens (standard tier, platform.openai.com/docs/pricing, read 2026-11-15).
PRICES = {
    "gpt-5.4-mini": {"input": 0.75, "cached_input": 0.075, "output": 4.50},
    "text-embedding-3-small": {"input": 0.02, "output": 0.0},
}

_run_lock = threading.Lock()
_running = False
_run_info: dict = {}       # {started_at, n_facts} of the run in progress, {last_error, failed_at} of the last failure


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _iso(t: dt.datetime) -> str:
    return t.astimezone(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _envload():
    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)
    import envload  # secrets only via envload, never printed
    envload.load()


def _cost(model: str, inp: int, out: int = 0, cached: int = 0) -> float:
    p = PRICES.get(model)
    if not p:
        return 0.0
    return ((inp - cached) * p["input"] + cached * p.get("cached_input", p["input"]) + out * p["output"]) / 1e6


def _norm_facts(facts: list[dict]) -> list[dict]:
    out, seen = [], set()
    for i, f in enumerate(facts):
        if isinstance(f, str):
            f = {"text": f}
        text = str(f.get("text") or f.get("content") or "").strip()
        if not text:
            continue
        fid = str(f.get("id") or f"f{i + 1}").replace("/", "_")
        if fid in seen:  # past.dev refuses a batch with a repeated source id
            fid = f"{fid}-{i + 1}"
        seen.add(fid)
        out.append({"id": fid, "agent": f.get("agent") or "unknown", "problem": f.get("problem"),
                    "text": text, "time": f.get("time")})
    # stable chronological order (facts without a time keep their input position)
    out.sort(key=lambda f: (f["time"] or "", ))
    if len(out) > MAX_INDEX_FACTS:
        out = out[-MAX_INDEX_FACTS:]
    return out


def _question_facts(facts: list[dict]) -> list[dict]:
    """At most MAX_QUESTION_FACTS facts, evenly spread over the (chronological) list."""
    if len(facts) <= MAX_QUESTION_FACTS:
        return facts
    step = len(facts) / MAX_QUESTION_FACTS
    return [facts[int(i * step)] for i in range(MAX_QUESTION_FACTS)]


# --------------------------------------------------------------------------------------------- OpenAI helpers
def _client():
    _envload()
    from openai import OpenAI
    return OpenAI(timeout=120.0, max_retries=3)


def _json_call(client, model: str, instructions: str, prompt: str, schema: dict, name: str,
               effort: str = "low") -> tuple[dict, dict]:
    r = client.responses.create(model=model, instructions=instructions, input=prompt, reasoning={"effort": effort},
                                text={"format": {"type": "json_schema", "name": name, "strict": True,
                                                 "schema": schema}})
    u = r.usage
    cached = 0
    try:
        cached = int(u.input_tokens_details.cached_tokens or 0)
    except Exception:
        pass
    usage = {"input": int(u.input_tokens), "output": int(u.output_tokens), "cached": cached}
    return json.loads(r.output_text), usage


def build_qa(client, facts: list[dict]) -> tuple[list[dict], dict]:
    """One 'single' question for each of (at most MAX_QUESTION_FACTS of) the facts + a few cross-fact questions.
    The writer sees every indexed fact, so cross questions and 'latest value' questions stay correct."""
    asked = _question_facts(facts)
    asked_ids = {f["id"] for f in asked}
    listing = "\n".join(f"[{f['id']}]{'*' if f['id'] in asked_ids and len(asked) < len(facts) else ''} "
                        f"({f['agent']}, {f['problem'] or 'general'}, {f['time'] or 'n/a'}) {f['text']}"
                        for f in facts)
    n_cross = max(3, min(6, len(asked) // 5))
    schema = {"type": "object", "additionalProperties": False, "required": ["questions"], "properties": {
        "questions": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["question", "answer", "fact_ids", "kind"],
            "properties": {"question": {"type": "string"}, "answer": {"type": "string"},
                           "fact_ids": {"type": "array", "items": {"type": "string"}},
                           "kind": {"type": "string", "enum": ["single", "cross"]}}}}}}
    instr = ("You build a QA benchmark for an agent memory system. Questions must be answerable ONLY from the "
             "facts, must be specific (names, numbers, settings, outcomes), must not quote the fact verbatim, and "
             "the expected answer must be short and unambiguous.")
    which = ("per fact marked with *" if len(asked) < len(facts) else "per fact")
    prompt = (f"Facts (id in brackets, chronological):\n{listing}\n\nWrite exactly one 'single' question {which} "
              f"(fact_ids = [that id]; its answer is contained in that fact) and then {n_cross} 'cross' questions "
              "whose answer needs two or more facts (e.g. comparisons, the latest value after an update, which "
              "strategy is closer to its record). Return them all.")
    out, usage = _json_call(client, QA_MODEL, instr, prompt, schema, "qa_set", effort="low")
    ids = {f["id"] for f in facts}
    qs = []
    for q in out.get("questions", []):
        fids = [x for x in q.get("fact_ids", []) if x in ids]
        if q.get("question") and q.get("answer") and fids:
            qs.append({"question": q["question"], "answer": q["answer"], "fact_ids": fids,
                       "kind": q.get("kind", "single")})
    return qs, usage


def answer(client, question: str, context: str) -> tuple[str, dict]:
    instr = ("Answer the question using ONLY the memory context below. If the context does not contain the "
             "answer, reply exactly 'unknown'. Be concise: one sentence, include exact numbers and names.")
    prompt = f"Memory context:\n{context if context.strip() else '(empty)'}\n\nQuestion: {question}"
    r = client.responses.create(model=ANSWER_MODEL, instructions=instr, input=prompt, reasoning={"effort": "low"})
    u = r.usage
    cached = 0
    try:
        cached = int(u.input_tokens_details.cached_tokens or 0)
    except Exception:
        pass
    return r.output_text.strip(), {"input": int(u.input_tokens), "output": int(u.output_tokens), "cached": cached}


def judge(client, q: dict, facts_by_id: dict, candidate: str) -> dict:
    schema = {"type": "object", "additionalProperties": False, "required": ["correct", "reason"],
              "properties": {"correct": {"type": "boolean"}, "reason": {"type": "string"}}}
    instr = ("You are a strict grader. Mark CORRECT only if the candidate answer states the expected answer's key "
             "facts: every number, name and setting must match exactly (equivalent formatting such as 4/7 vs "
             "0.5714 is fine). Mark INCORRECT if it is 'unknown', vague, hedged between options, missing a "
             "required part, or contradicts the expected answer or the source facts.")
    src = "\n".join(f"- {facts_by_id[i]['text']}" for i in q["fact_ids"] if i in facts_by_id)
    prompt = (f"Question: {q['question']}\nExpected answer: {q['answer']}\nSource facts:\n{src}\n\n"
              f"Candidate answer: {candidate}")
    out, usage = _json_call(client, JUDGE_MODEL, instr, prompt, schema, "grade", effort="low")
    return {"correct": bool(out.get("correct")), "reason": out.get("reason", ""), "usage": usage}


# --------------------------------------------------------------------------------------------- memory systems
class Markdown:
    name = "markdown"

    def __init__(self, facts):
        lines = ["# Lab memory (all facts)", ""]
        for f in facts:
            lines.append(f"- [{f['time'] or 'n/a'}] **{f['agent']}** ({f['problem'] or 'general'}): {f['text']}")
        self.doc = "\n".join(lines)
        self.cost_usd = 0.0
        self.setup = {}

    def lookup(self, query):
        return self.doc


class Rag:
    name = "rag"

    def __init__(self, client, facts, k=TOP_K):
        import numpy as np
        self.np, self.client, self.facts, self.k = np, client, facts, k
        t = time.time()
        r = client.embeddings.create(model=EMBED_MODEL, input=[self._fmt(f) for f in facts])
        self.mat = np.array([d.embedding for d in r.data], dtype=np.float32)
        self.mat /= np.linalg.norm(self.mat, axis=1, keepdims=True) + 1e-9
        self.embed_tokens = int(r.usage.total_tokens)
        self.cost_usd = _cost(EMBED_MODEL, self.embed_tokens)
        self.setup = {"index_tokens": self.embed_tokens, "index_seconds": round(time.time() - t, 2), "k": k}
        self.lock = threading.Lock()

    @staticmethod
    def _fmt(f):
        return f"[{f['time'] or 'n/a'}] {f['agent']} ({f['problem'] or 'general'}): {f['text']}"

    def lookup(self, query):
        np = self.np
        r = self.client.embeddings.create(model=EMBED_MODEL, input=[query])
        v = np.array(r.data[0].embedding, dtype=np.float32)
        v /= np.linalg.norm(v) + 1e-9
        with self.lock:
            self.cost_usd += _cost(EMBED_MODEL, int(r.usage.total_tokens))
        top = np.argsort(-(self.mat @ v))[: self.k]
        return "\n".join(f"- {self._fmt(self.facts[i])}" for i in top)


class PastDev:
    name = "past.dev"

    def __init__(self, facts, k=TOP_K):
        import httpx
        _envload()
        self.http = httpx.Client(timeout=60.0, headers={"Authorization": "Bearer " + os.environ["PAST_API_KEY"],
                                                       "Content-Type": "application/json"})
        self.k = k
        self.facts = facts
        self.by_id = {f["id"]: f for f in facts}
        stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S")
        self.identity = f"ltd-bench-{stamp}"
        # A private occurrence window per run (facts keep their order, 10 s apart) so that recall cannot
        # return other project memory, e.g. the live lab's own facts under identity ltd-lab.
        # one private 20-minute slot per benchmark second (repeats after ~7.5 days; slots end before 2026), so
        # two runs started in the same minute (server button + CLI) cannot read each other's items either
        slot = int(time.time()) % 650_000
        base = dt.datetime(2001, 1, 1, tzinfo=dt.timezone.utc) + dt.timedelta(seconds=1200 * slot)
        self.t_from = base - dt.timedelta(seconds=1)
        self.t_to = base + dt.timedelta(seconds=10 * len(facts) + 1)
        self.items = [{"id": f"{self.identity}-{f['id']}", "content": f["text"],
                       "label": f"{f['agent']} / {f['problem'] or 'general'}",
                       "timestamp": _iso(base + dt.timedelta(seconds=10 * i)), "identity": self.identity,
                       "metadata": {"bench": self.identity, "fact_id": f["id"], "agent": f["agent"],
                                    "problem": f["problem"], "original_time": f["time"]}}
                      for i, f in enumerate(facts)]
        self.src_to_fact = {it["id"]: it["metadata"]["fact_id"] for it in self.items}
        self.cost_usd = 0.0
        self.setup = {"identity": self.identity}

    def _usage_credits(self):
        try:
            r = self.http.get(PAST_BASE + "/usage")
            return float(r.json()["project"]["credits"])
        except Exception:
            return None

    def ingest(self):
        c0 = self._usage_credits()
        t = time.time()
        r = self.http.post(PAST_BASE + "/ingest/batch", json={"idempotencyKey": self.identity, "items": self.items})
        r.raise_for_status()
        ing = r.json()
        iid = ing["ingestionId"]
        status = ing.get("status")
        delay = 2.0
        while status != "completed" and time.time() - t < INGEST_TIMEOUT_S:
            time.sleep(delay)
            if time.time() - t > 60:
                delay = 10.0
            g = self.http.get(f"{PAST_BASE}/ingest/{iid}")
            if g.status_code == 200:
                status = g.json().get("status")
                if status == "failed":
                    break
        self.setup.update(ingestion_id=iid, ingest_status=status, ingest_wait_s=round(time.time() - t, 1),
                          credits_before=c0)
        return status == "completed"

    def lookup(self, query):
        body = {"query": query, "identity": self.identity, "limit": self.k, "level": "low",
                "occurredFrom": _iso(self.t_from), "occurredTo": _iso(self.t_to)}
        r = None
        for attempt in range(4):
            r = self.http.post(PAST_BASE + "/recall", json=body)
            if r.status_code == 429 or r.status_code >= 500:
                time.sleep(2 + 3 * attempt)
                continue
            break
        r.raise_for_status()
        parts = []
        for res in r.json().get("results", []):
            lines = [f"## memory #{res.get('rank')}", res.get("content", "").strip()]
            for s in res.get("sources", []):
                fid = self.src_to_fact.get(s.get("sourceId"))
                f = self.by_id.get(fid) if fid else None
                when = (f or {}).get("time") or "n/a"
                for ex in s.get("excerpts", [])[:3]:
                    lines.append(f"  source [{when}] {s.get('label', '')}: {ex.strip()}")
            parts.append("\n".join(x for x in lines if x))
        return "\n\n".join(parts)

    def finish(self):
        c1 = self._usage_credits()
        c0 = self.setup.get("credits_before")
        self.setup["credits_spent"] = round(c1 - c0, 2) if (c0 is not None and c1 is not None) else None
        self.setup.pop("credits_before", None)


# --------------------------------------------------------------------------------------------- driver
def run(facts: list[dict], label: str | None = None) -> dict:
    t_start = time.time()
    n_available = len(facts)
    facts = _norm_facts(facts)
    if len(facts) < 3:
        raise ValueError("need at least 3 facts to benchmark")
    client = _client()
    facts_by_id = {f["id"]: f for f in facts}

    # past.dev ingestion runs while the QA set is written and the RAG index is built
    past = PastDev(facts)
    with cf.ThreadPoolExecutor(max_workers=2) as ex:
        ingest_f = ex.submit(past.ingest)
        qa_f = ex.submit(build_qa, client, facts)
        rag = Rag(client, facts)
        md = Markdown(facts)
        questions, qa_usage = qa_f.result()
        ingest_ok = ingest_f.result()
    if not questions:
        raise RuntimeError("the QA writer returned no usable questions; the previous benchmark is kept")
    systems = [past, md, rag]

    # lookups: sequential per system so latency is not inflated by our own parallel load
    contexts: dict[str, list] = {}
    for s in systems:
        rows = []
        for q in questions:
            t = time.perf_counter()
            try:
                ctx, err = s.lookup(q["question"]), None
            except Exception as e:
                ctx, err = "", _scrub(f"{type(e).__name__}: {e}")[:300]
            rows.append({"context": ctx, "latency_ms": (time.perf_counter() - t) * 1000.0, "error": err})
        contexts[s.name] = rows
    if hasattr(past, "finish"):
        past.finish()

    # answers + strict judging in parallel
    zero = {"input": 0, "output": 0, "cached": 0}

    def work(si, qi):
        # one failed call (after the client's own retries) must not sink the whole benchmark: it is scored
        # as incorrect and its error is kept in the per-question record
        s = systems[si]
        row = contexts[s.name][qi]
        try:
            ans, use = answer(client, questions[qi]["question"], row["context"])
        except Exception as e:
            return si, qi, "", zero, {"correct": False, "reason": _scrub(f"answer call failed: {type(e).__name__}: {e}")[:300],
                                      "usage": zero, "error": True}
        try:
            g = judge(client, questions[qi], facts_by_id, ans)
        except Exception as e:
            g = {"correct": False, "reason": _scrub(f"judge call failed: {type(e).__name__}: {e}")[:300], "usage": zero,
                 "error": True}
        return si, qi, ans, use, g

    results = {(si, qi): None for si in range(len(systems)) for qi in range(len(questions))}
    with cf.ThreadPoolExecutor(max_workers=12) as ex:
        for si, qi, ans, use, g in ex.map(lambda a: work(*a), list(results)):
            results[(si, qi)] = (ans, use, g)

    out_systems, judge_tokens = [], {"input": 0, "output": 0}
    for si, s in enumerate(systems):
        n = len(questions)
        correct = sum(1 for qi in range(n) if results[(si, qi)][2]["correct"])
        ans_cost = sum(_cost(ANSWER_MODEL, u["input"], u["output"], u["cached"])
                       for qi in range(n) for u in [results[(si, qi)][1]])
        ctx_tokens = [results[(si, qi)][1]["input"] for qi in range(n)]
        lat = [contexts[s.name][qi]["latency_ms"] for qi in range(n)]
        by_kind = {}
        for kind in ("single", "cross"):
            idx = [qi for qi in range(n) if questions[qi]["kind"] == kind]
            if idx:
                by_kind[kind] = round(sum(results[(si, qi)][2]["correct"] for qi in idx) / len(idx), 4)
        total_cost = ans_cost + s.cost_usd
        out_systems.append({
            "name": s.name, "accuracy": round(correct / n, 4) if n else 0.0,
            "latency_ms": round(sum(lat) / n, 1) if n else 0.0, "cost_usd": round(total_cost, 6), "n": n,
            "correct": correct, "accuracy_by_kind": by_kind,
            "latency_p50_ms": round(sorted(lat)[n // 2], 1) if n else 0.0,
            "cost_per_question_usd": round(total_cost / n, 7) if n else 0.0,
            "context_tokens_mean": round(sum(ctx_tokens) / n, 1) if n else 0.0,
            "lookup_errors": sum(1 for r in contexts[s.name] if r["error"]),
            "call_errors": sum(1 for qi in range(n) if results[(si, qi)][2].get("error")),
            "setup": s.setup,
        })
    for (si, qi), (ans, use, g) in results.items():
        judge_tokens["input"] += g["usage"]["input"]
        judge_tokens["output"] += g["usage"]["output"]

    qrows = []
    for qi, q in enumerate(questions):
        qrows.append({**q, "answers": {systems[si].name: {
            "answer": results[(si, qi)][0], "correct": results[(si, qi)][2]["correct"],
            "reason": results[(si, qi)][2]["reason"], "latency_ms": round(contexts[systems[si].name][qi]["latency_ms"], 1),
            "context_chars": len(contexts[systems[si].name][qi]["context"]),
            "lookup_error": contexts[systems[si].name][qi]["error"]} for si in range(len(systems))}})

    bench = {
        "systems": out_systems, "time": _now(), "status": "done",
        "n_facts": len(facts), "n_facts_available": n_available, "n_questions": len(questions),
        "caps": {"max_index_facts": MAX_INDEX_FACTS, "max_question_facts": MAX_QUESTION_FACTS},
        "facts_source": label or "lab memory facts",
        "identity": past.identity, "past_ingest_completed": ingest_ok,
        "models": {"answer": ANSWER_MODEL, "judge": JUDGE_MODEL, "qa_writer": QA_MODEL, "embed": EMBED_MODEL},
        "top_k": TOP_K, "prices_usd_per_1m": PRICES,
        "cost_note": "cost = answer-model tokens x list price (+ embedding tokens for RAG); past.dev credits at $0 "
                     "(credits spent reported in setup); judge and QA-writer tokens are benchmark overhead",
        "overhead_tokens": {"judge": judge_tokens, "qa_writer": qa_usage},
        "seconds": round(time.time() - t_start, 1),
        "questions": qrows,
    }
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    tmp = f"{OUT_PATH}.{os.getpid()}.tmp"
    with open(tmp, "w") as f:
        json.dump(bench, f, indent=1)
    os.replace(tmp, OUT_PATH)
    _to_ledger(bench)
    return bench


def _scrub(text: str) -> str:
    import re
    text = re.sub(r"(sk-[A-Za-z0-9_\-*]{6,}|Bearer\s+[A-Za-z0-9._\-]+)", "[redacted]", text or "")
    home = os.path.expanduser("~")
    text = text.replace(ROOT, "ROOT")
    return text.replace(home, "~") if home and home != "/" else text


def _to_ledger(bench: dict):
    """SPEC: results also go to the ledger (`learning` table, key memory_benchmark) + one decision. Best-effort."""
    if os.environ.get("LTD_LABS_LEDGER", "1") == "0":
        return
    try:
        from ltd import ledger  # type: ignore
        ledger.learning_set("memory_benchmark", bench)
        line = "; ".join(f"{s['name']} {s['accuracy']:.0%} correct, {s['latency_ms']:.0f} ms lookup, ${s['cost_usd']:.4f}"
                         for s in bench["systems"])
        did = ledger.add_decision(
            ledger.max_cycle(), "memory", "benchmark", None,
            {"n_facts": bench["n_facts"], "n_questions": bench["n_questions"], "identity": bench["identity"],
             "systems": [{k: s[k] for k in ("name", "accuracy", "latency_ms", "cost_usd", "n")} for s in bench["systems"]]},
            f"Memory benchmark on {bench['n_facts']} facts ({bench['facts_source']}), {bench['n_questions']} questions "
            f"graded by {bench['models']['judge']}: {line}.",
            outcome={"observed": None, "verdict": "n/a", "note": "benchmark"}, model=bench["models"]["answer"])
        try:
            from ltd import events  # type: ignore
            events.publish("decision", ledger.get_decision(did))
        except Exception:
            pass
    except Exception:
        pass


def latest() -> dict | None:
    """Last completed benchmark, plus `running` (a new one is in progress in this process) and, if the last
    attempt failed, `last_error`. None when no benchmark has ever completed."""
    if not os.path.exists(OUT_PATH):
        return None
    try:
        b = json.load(open(OUT_PATH))
    except Exception:
        return None
    b["running"] = _running
    if _running and _run_info.get("started_at"):
        b["running_since"] = _run_info["started_at"]
    if _run_info.get("last_error"):
        b["last_error"] = _run_info["last_error"]
        b["last_error_at"] = _run_info.get("failed_at")
    return b


def running() -> bool:
    return _running


def start_async(facts: list[dict], label: str | None = None, callback=None) -> bool:
    """Run `run` in a daemon thread. Returns False (no-op) while one is running. Raises ValueError right away
    when there are too few facts, so the caller can report it. Optional callback(result) on success."""
    global _running
    facts = list(facts)
    if len(_norm_facts(facts)) < 3:
        raise ValueError(f"need at least 3 non-empty facts to benchmark (have {len(_norm_facts(facts))})")
    with _run_lock:
        if _running:
            return False
        _running = True
        _run_info.update(started_at=_now(), n_facts=len(facts))

    def _bg():
        global _running
        try:
            res = run(facts, label)
            _run_info.pop("last_error", None)
            if callback is not None:
                callback(res)
        except Exception as e:
            _run_info.update(last_error=_scrub(f"{type(e).__name__}: {e}")[:500], failed_at=_now())
            traceback.print_exc()
        finally:
            _running = False

    try:
        threading.Thread(target=_bg, name="ltd-memory-bench", daemon=True).start()
    except Exception:
        _running = False
        raise
    return True


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "ltd", "tests_labs", "sample_facts.json")
    data = json.load(open(path))
    lab = data.get("label") if isinstance(data, dict) else None
    fs = data["facts"] if isinstance(data, dict) else data
    b = run(fs, label=lab or os.path.basename(path))
    print(f"{'system':10s} {'acc':>6s} {'single':>7s} {'cross':>6s} {'lat_ms':>8s} {'cost_usd':>10s} {'ctx_tok':>8s} n")
    for s in b["systems"]:
        print(f"{s['name']:10s} {s['accuracy']:6.3f} {s['accuracy_by_kind'].get('single', 0):7.3f} "
              f"{s['accuracy_by_kind'].get('cross', 0):6.3f} {s['latency_ms']:8.1f} {s['cost_usd']:10.6f} "
              f"{s['context_tokens_mean']:8.0f} {s['n']}")
    print(json.dumps({k: b[k] for k in ("n_facts", "n_questions", "identity", "past_ingest_completed", "seconds")}))
    print(json.dumps([s["setup"] for s in b["systems"]]))
