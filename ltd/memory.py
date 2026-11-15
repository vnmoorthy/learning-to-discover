"""Multi-agent memory (past.dev) + two baselines for the benchmark: an append-only markdown file and a small RAG.

Agents: planner, proposer, critic, literature, and one agent:<slug> per problem. All agents share one past.dev
identity ("ltd-lab"), so each reads what the others wrote; the writer agent travels in metadata. Every read is
recorded (fact_reads + facts.read_by), which is what the Memory page draws as agent -> agent links.
"""
import json
import math
import os
import queue
import threading
import time
import uuid

from . import config, events, ledger

PAST_URL = "https://app.past.dev/api/v1"
IDENTITY = os.environ.get("LTD_PAST_IDENTITY", "ltd-lab")
_q = queue.Queue()
_worker = {"t": None}
_md_lock = threading.Lock()
_status = {"ingested": 0, "failed": 0, "last_error": None, "recalls": 0, "recall_errors": 0}


def _env():
    import sys
    if config.ROOT not in sys.path:
        sys.path.insert(0, config.ROOT)
    import envload
    envload.load()


def _headers():
    _env()
    return {"Authorization": "Bearer " + os.environ.get("PAST_API_KEY", "")}


def _ensure_worker():
    if _worker["t"] is None or not _worker["t"].is_alive():
        _worker["t"] = threading.Thread(target=_work, name="memory-ingest", daemon=True)
        _worker["t"].start()


def _work():
    import httpx
    while True:
        fid = _q.get()
        r = ledger.q("SELECT * FROM facts WHERE id=?", (fid,))
        if not r:
            continue
        f = r[0]
        body = {"id": f["id"], "content": f["text"], "label": f["agent"], "timestamp": f["time"], "identity": IDENTITY,
                "metadata": {"agent": f["agent"], "problem": f["problem"] or "", "lab": IDENTITY,
                             "tags": ",".join(ledger.uj(f["tags"], []) or [])}}
        status = "failed"
        for attempt in range(3):
            try:
                resp = httpx.post(f"{PAST_URL}/ingest", headers=_headers(), json=body, timeout=30)
                if resp.status_code < 300:
                    status = "ingested"
                    _status["ingested"] += 1
                    break
                _status["last_error"] = f"ingest HTTP {resp.status_code}"
            except Exception as e:  # noqa: BLE001
                _status["last_error"] = f"ingest {type(e).__name__}"
            time.sleep(2 * (attempt + 1))
        if status == "failed":
            _status["failed"] += 1
        emb = None
        try:
            emb = embed([f["text"]])[0]
        except Exception as e:  # noqa: BLE001
            _status["last_error"] = f"embed {type(e).__name__}"
        ledger.x("UPDATE facts SET remote=?, embedding=COALESCE(?, embedding) WHERE id=?",
                 (status, json.dumps([round(v, 5) for v in emb]) if emb else None, fid))


def write(agent, problem, text, tags=None):
    """Store a fact: local row + markdown baseline now, past.dev ingest + embedding in the background."""
    fid = "f-" + uuid.uuid4().hex[:10]
    t = ledger.now()
    ledger.x("INSERT INTO facts(id,time,agent,problem,text,tags,read_by,remote) VALUES(?,?,?,?,?,?,?,?)",
             (fid, t, agent, problem, text, json.dumps(tags or []), "[]", "queued"))
    with _md_lock:
        os.makedirs(config.DATA, exist_ok=True)
        with open(config.MEMORY_MD, "a") as fh:
            fh.write(f"- [{t}] ({fid}) **{agent}**{' on ' + problem if problem else ''}: {text}\n")
    _ensure_worker()
    _q.put(fid)
    events.publish("log", {"level": "memory", "msg": f"{agent} wrote {fid}: {text[:140]}"})
    return fid


def mark_read(fact_ids, reader, via="past.dev", decision_id=None):
    t = ledger.now()
    for fid in fact_ids:
        r = ledger.q("SELECT read_by FROM facts WHERE id=?", (fid,))
        if not r:
            continue
        rb = ledger.uj(r[0]["read_by"], []) or []
        if reader not in rb:
            rb.append(reader)
            ledger.x("UPDATE facts SET read_by=? WHERE id=?", (json.dumps(rb), fid))
        ledger.x("INSERT INTO fact_reads(fact_id,reader,time,via,decision_id) VALUES(?,?,?,?,?)", (fid, reader, t, via, decision_id))


def _fact(fid):
    r = ledger.q("SELECT id,agent,problem,text,time FROM facts WHERE id=?", (fid,))
    return r[0] if r else None


def recall_past(query, k=5):
    """Raw past.dev recall over the shared identity. Returns ([{id, agent, problem, text, time}], latency_ms)."""
    import httpx
    t0 = time.time()
    resp = httpx.post(f"{PAST_URL}/recall", headers=_headers(),
                      json={"query": query, "identity": IDENTITY, "level": "high", "limit": max(15, 3 * int(k))}, timeout=45)
    resp.raise_for_status()
    out, seen = [], set()
    for res in resp.json().get("results", []):
        srcs = res.get("sources") or []
        sid = srcs[0].get("sourceId") if srcs else None
        # Only facts this lab wrote (they all exist locally). The past.dev project also holds other identities'
        # items (e.g. the memory benchmark's QA corpus); those must never be read back as lab memory.
        local = _fact(sid) if sid else None
        if local and sid not in seen:
            seen.add(sid)
            f = dict(local)
            if res.get("content") and res["content"] != f["text"]:
                f["recalled"] = res["content"][:300]     # past.dev's derived memory for this source
            out.append(f)
    return out[:k], int((time.time() - t0) * 1000)


def recall(reader, query, k=5, problem=None, decision_id=None, include_recent_others=3):
    """What `reader` gets back for `query`: past.dev recall (shared space) + the latest facts other agents wrote on this
    problem (so a fresh fact still being indexed is not missed). Every returned fact is marked as read by `reader`."""
    facts, via = [], {}
    try:
        res, _ = recall_past(query, k)
        _status["recalls"] += 1
        for f in res:
            if f["id"] not in via:
                facts.append(f); via[f["id"]] = "past.dev"
    except Exception as e:  # noqa: BLE001
        _status["recall_errors"] += 1
        _status["last_error"] = f"recall {type(e).__name__}: {str(e)[:120]}"
    if include_recent_others:
        sql = "SELECT id,agent,problem,text,time FROM facts WHERE agent<>?" + \
              (" AND (problem=? OR problem IS NULL)" if problem else "") + " ORDER BY time DESC LIMIT ?"
        args = (reader, problem, include_recent_others) if problem else (reader, include_recent_others)
        for f in ledger.q(sql, args):
            if f["id"] not in via:
                facts.append(f); via[f["id"]] = "recent"
    mark_read([f["id"] for f in facts if _fact(f["id"])], reader, "past.dev", decision_id)
    for f in facts:
        f["via"] = via.get(f["id"])
    return facts


# ---------------- baselines ----------------
def markdown_text():
    try:
        return open(config.MEMORY_MD).read()
    except OSError:
        return ""


def embed(texts):
    _env()
    from openai import OpenAI
    r = OpenAI().embeddings.create(model=config.EMBED_MODEL, input=texts)
    return [d.embedding for d in r.data]


def rag_recall(query, k=5):
    """Cosine top-k over fact embeddings (text-embedding-3-small). Facts missing an embedding are embedded now."""
    rows = ledger.q("SELECT id,agent,problem,text,time,embedding FROM facts")
    missing = [r for r in rows if not r["embedding"]]
    for i in range(0, len(missing), 64):
        chunk = missing[i:i + 64]
        embs = embed([r["text"] for r in chunk])
        for r, e in zip(chunk, embs):
            r["embedding"] = json.dumps([round(v, 5) for v in e])
            ledger.x("UPDATE facts SET embedding=? WHERE id=?", (r["embedding"], r["id"]))
    qv = embed([query])[0]
    qn = math.sqrt(sum(v * v for v in qv)) or 1.0
    scored = []
    for r in rows:
        v = json.loads(r["embedding"])
        dot = sum(a * b for a, b in zip(qv, v))
        n = math.sqrt(sum(b * b for b in v)) or 1.0
        scored.append((dot / (qn * n), r))
    scored.sort(key=lambda z: -z[0])
    return [{k2: r[k2] for k2 in ("id", "agent", "problem", "text", "time")} | {"sim": round(s, 4)} for s, r in scored[:k]]


# ---------------- API views ----------------
def all_facts():
    return ledger.q("SELECT id,agent,problem,text,time FROM facts ORDER BY time")


def status():
    return dict(_status, identity=IDENTITY, queued=_q.qsize())


def api_view(limit=500):
    rows = ledger.q("SELECT id,agent,problem,text,time,read_by FROM facts ORDER BY time DESC LIMIT ?", (limit,))
    facts = [{"id": r["id"], "agent": r["agent"], "problem": r["problem"], "text": r["text"], "time": r["time"],
              "read_by": ledger.uj(r["read_by"], []) or []} for r in rows]
    agents = {"planner", "proposer", "critic"} | {f"agent:{s}" for s, p in config.PROBLEMS.items() if p["active"]}
    for f in facts:
        agents.add(f["agent"]); agents.update(f["read_by"])
    links = {}
    for r in ledger.q("SELECT fr.fact_id, fr.reader, f.agent FROM fact_reads fr JOIN facts f ON f.id=fr.fact_id"):
        if r["agent"] != r["reader"]:
            links[(r["agent"], r["reader"], r["fact_id"])] = 1
    bench = None
    try:
        from . import memory_bench  # owned by another builder
        bench = memory_bench.latest()
    except Exception:  # noqa: BLE001
        bench = None
    if not bench:
        bench = ledger.learning_get("memory_benchmark")
    return {"facts": facts, "agents": sorted(agents),
            "links": [{"from_agent": a, "to_agent": b, "fact_id": f} for (a, b, f) in links],
            "benchmark": bench}
