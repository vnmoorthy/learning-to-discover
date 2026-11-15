"""SQLite event store (ROOT/data/phoenixastar.sqlite). One connection guarded by a lock; every agent action is a decision row."""
import datetime as _dt
import json
import os
import sqlite3
import threading

from . import config

_lock = threading.RLock()
_conn = None

SCHEMA = """
CREATE TABLE IF NOT EXISTS decisions (
  id INTEGER PRIMARY KEY AUTOINCREMENT, cycle INTEGER, time TEXT, agent TEXT, problem TEXT, action TEXT,
  params TEXT, rationale TEXT, prediction TEXT, outcome TEXT, sources TEXT, memory_reads TEXT, memory_writes TEXT,
  model TEXT, tokens INTEGER, latency_ms INTEGER);
CREATE INDEX IF NOT EXISTS dec_problem ON decisions(problem);
CREATE INDEX IF NOT EXISTS dec_agent ON decisions(agent);
CREATE TABLE IF NOT EXISTS telemetry (
  id INTEGER PRIMARY KEY AUTOINCREMENT, time TEXT, cycle INTEGER, kind TEXT, problem TEXT, metric TEXT, value REAL, data TEXT);
CREATE INDEX IF NOT EXISTS tel_kind ON telemetry(kind, problem, metric);
CREATE TABLE IF NOT EXISTS facts (
  id TEXT PRIMARY KEY, time TEXT, agent TEXT, problem TEXT, text TEXT, tags TEXT, read_by TEXT,
  remote TEXT, embedding TEXT);
CREATE TABLE IF NOT EXISTS fact_reads (fact_id TEXT, reader TEXT, time TEXT, via TEXT, decision_id INTEGER);
CREATE TABLE IF NOT EXISTS literature (
  id INTEGER PRIMARY KEY AUTOINCREMENT, problem TEXT, query TEXT, title TEXT, url TEXT, published TEXT,
  highlight TEXT, time TEXT, cited_by TEXT);
CREATE TABLE IF NOT EXISTS lit_queries (query TEXT PRIMARY KEY, problem TEXT, time TEXT, ids TEXT);
CREATE TABLE IF NOT EXISTS artifacts (
  problem TEXT PRIMARY KEY, time TEXT, kind TEXT, source TEXT, label TEXT, data TEXT);
CREATE TABLE IF NOT EXISTS bests (
  problem TEXT PRIMARY KEY, score REAL, verified INTEGER, time TEXT, strategy_id TEXT, solution TEXT,
  path TEXT, beats_record INTEGER);
CREATE TABLE IF NOT EXISTS verified_paths (path TEXT PRIMARY KEY, problem TEXT, time TEXT, ok INTEGER, score REAL, error TEXT);
CREATE TABLE IF NOT EXISTS strategies (
  id TEXT PRIMARY KEY, problem TEXT, template TEXT, params TEXT, resource TEXT, gpu INTEGER, pid INTEGER,
  started_at TEXT, stopped_at TEXT, status TEXT, adopted INTEGER, cmdline TEXT, log TEXT, metric_value REAL,
  stop_reason TEXT, decision_id INTEGER, test INTEGER DEFAULT 0);
CREATE TABLE IF NOT EXISTS learning (key TEXT PRIMARY KEY, time TEXT, data TEXT);
CREATE TABLE IF NOT EXISTS kv (key TEXT PRIMARY KEY, value TEXT);
"""


def now():
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def iso(ts):
    return _dt.datetime.fromtimestamp(float(ts), _dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(s):
    if not s:
        return None
    try:
        return _dt.datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=_dt.timezone.utc).timestamp()
    except ValueError:
        return None


def conn():
    global _conn
    with _lock:
        if _conn is None:
            os.makedirs(config.DATA, exist_ok=True)
            _conn = sqlite3.connect(config.DB_PATH, check_same_thread=False, timeout=30)
            _conn.row_factory = sqlite3.Row
            _conn.execute("PRAGMA journal_mode=WAL")
            _conn.executescript(SCHEMA)
            _conn.commit()
        return _conn


def q(sql, args=()):
    with _lock:
        return [dict(r) for r in conn().execute(sql, args).fetchall()]


def x(sql, args=()):
    with _lock:
        c = conn().execute(sql, args)
        conn().commit()
        return c.lastrowid


def j(v):
    return json.dumps(v) if v is not None else None


def uj(s, default=None):
    if s is None:
        return default
    try:
        return json.loads(s)
    except (TypeError, ValueError):
        return default


# ---------- kv ----------
def kv_get(key, default=None):
    r = q("SELECT value FROM kv WHERE key=?", (key,))
    return uj(r[0]["value"], default) if r else default


def kv_set(key, value):
    x("INSERT INTO kv(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, j(value)))


# ---------- decisions ----------
def add_decision(cycle, agent, action, problem=None, params=None, rationale="", prediction=None, outcome=None,
                 sources=None, memory_reads=None, memory_writes=None, model=None, tokens=None, latency_ms=None,
                 link_sources=True):
    if prediction is not None and outcome is None:
        outcome = {"observed": None, "verdict": "pending", "note": ""}
    if cycle is None:       # API contract: cycle is always an int (background polls/verifications get the current one)
        cycle = max_cycle()
    did = x("""INSERT INTO decisions(cycle,time,agent,problem,action,params,rationale,prediction,outcome,sources,
               memory_reads,memory_writes,model,tokens,latency_ms) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (cycle, now(), agent, problem, action, j(params or {}), rationale or "", j(prediction), j(outcome),
             j(sources or []), j(memory_reads or []), j(memory_writes or []), model, tokens, latency_ms))
    if link_sources:
        for lid in sources or []:
            cite_literature(lid, did)
    return did


def update_decision(did, **kw):
    sets, args = [], []
    for k, v in kw.items():
        sets.append(f"{k}=?")
        args.append(j(v) if k in ("params", "prediction", "outcome", "sources", "memory_reads", "memory_writes") else v)
    if sets:
        x(f"UPDATE decisions SET {','.join(sets)} WHERE id=?", (*args, did))


def decision_row(r):
    src_ids = uj(r["sources"], []) or []
    sources = []
    if src_ids:
        rows = q(f"SELECT id,title,url,published FROM literature WHERE id IN ({','.join('?' * len(src_ids))})", src_ids)
        sources = [{"id": s["id"], "title": s["title"], "url": s["url"], "published": s["published"]} for s in rows]
    return {"id": r["id"], "cycle": r["cycle"], "time": r["time"], "agent": r["agent"], "problem": r["problem"],
            "action": r["action"], "params": uj(r["params"], {}) or {}, "rationale": r["rationale"] or "",
            "prediction": uj(r["prediction"]), "outcome": uj(r["outcome"]), "sources": sources,
            "memory_reads": uj(r["memory_reads"], []) or [], "memory_writes": uj(r["memory_writes"], []) or [],
            "model": r["model"], "tokens": r["tokens"], "latency_ms": r["latency_ms"]}


def get_decision(did):
    r = q("SELECT * FROM decisions WHERE id=?", (did,))
    return decision_row(r[0]) if r else None


def decisions(problem=None, agent=None, limit=100, before=None):
    w, a = [], []
    if problem:
        w.append("problem=?"); a.append(problem)
    if agent:
        w.append("agent=?"); a.append(agent)
    if before:
        w.append("id<?"); a.append(int(before))
    sql = "SELECT * FROM decisions" + (" WHERE " + " AND ".join(w) if w else "") + " ORDER BY id DESC LIMIT ?"
    return [decision_row(r) for r in q(sql, (*a, int(limit)))]


def max_cycle():
    r = q("SELECT MAX(cycle) AS c FROM decisions")
    return int(r[0]["c"] or 0) if r else 0


# ---------- telemetry / metric history ----------
def add_metric(problem, metric, value, cycle=None, t=None, data=None):
    x("INSERT INTO telemetry(time,cycle,kind,problem,metric,value,data) VALUES(?,?,?,?,?,?,?)",
      (t or now(), cycle, "metric", problem, metric, value, j(data)))


def add_snapshot(snap, cycle=None):
    x("INSERT INTO telemetry(time,cycle,kind,data) VALUES(?,?,?,?)", (now(), cycle, "snapshot", j(snap)))
    # keep the table small: only the last 400 raw snapshots
    x("DELETE FROM telemetry WHERE kind='snapshot' AND id NOT IN (SELECT id FROM telemetry WHERE kind='snapshot' ORDER BY id DESC LIMIT 400)")


def last_snapshot():
    r = q("SELECT time,data FROM telemetry WHERE kind='snapshot' ORDER BY id DESC LIMIT 1")
    return (uj(r[0]["data"]), r[0]["time"]) if r else (None, None)


def metric_history(problem, metric, limit=2000):
    rows = q("SELECT time,value FROM telemetry WHERE kind='metric' AND problem=? AND metric=? AND value IS NOT NULL "
             "ORDER BY id DESC LIMIT ?", (problem, metric, limit))
    return [[r["time"], r["value"]] for r in reversed(rows)]


# ---------- strategies ----------
def upsert_strategy(s):
    cols = ["id", "problem", "template", "params", "resource", "gpu", "pid", "started_at", "stopped_at", "status",
            "adopted", "cmdline", "log", "metric_value", "stop_reason", "decision_id", "test"]
    vals = [j(s.get(c)) if c == "params" else s.get(c) for c in cols]
    upd = ",".join(f"{c}=COALESCE(excluded.{c},{c})" for c in cols[1:])
    x(f"INSERT INTO strategies({','.join(cols)}) VALUES({','.join('?' * len(cols))}) ON CONFLICT(id) DO UPDATE SET {upd}", vals)


def strategy_row(r):
    d = dict(r)
    d["params"] = uj(d.get("params"), {}) or {}
    d["adopted"] = bool(d.get("adopted"))
    d["test"] = bool(d.get("test"))
    return d


def strategies(status=None, problem=None):
    w, a = [], []
    if status:
        w.append("status=?"); a.append(status)
    if problem:
        w.append("problem=?"); a.append(problem)
    sql = "SELECT * FROM strategies" + (" WHERE " + " AND ".join(w) if w else "") + " ORDER BY started_at"
    return [strategy_row(r) for r in q(sql, a)]


def get_strategy(sid):
    r = q("SELECT * FROM strategies WHERE id=?", (sid,))
    return strategy_row(r[0]) if r else None


# ---------- literature ----------
def cite_literature(lid, did):
    r = q("SELECT cited_by FROM literature WHERE id=?", (lid,))
    if not r:
        return
    c = uj(r[0]["cited_by"], []) or []
    if did not in c:
        c.append(did)
        x("UPDATE literature SET cited_by=? WHERE id=?", (j(c), lid))


def literature(problem=None):
    rows = q("SELECT * FROM literature" + (" WHERE problem=?" if problem else "") + " ORDER BY id DESC",
             (problem,) if problem else ())
    return [{"id": r["id"], "problem": r["problem"], "query": r["query"], "title": r["title"], "url": r["url"],
             "published": r["published"], "highlight": r["highlight"] or "", "cited_by": uj(r["cited_by"], []) or []}
            for r in rows]


# ---------- learning ----------
def learning_set(key, data):
    x("INSERT INTO learning(key,time,data) VALUES(?,?,?) ON CONFLICT(key) DO UPDATE SET time=excluded.time, data=excluded.data",
      (key, now(), j(data)))


def learning_get(key):
    r = q("SELECT data FROM learning WHERE key=?", (key,))
    return uj(r[0]["data"]) if r else None


# ---------- artifacts / bests ----------
def set_artifact(problem, kind, data, source, label=""):
    x("INSERT INTO artifacts(problem,time,kind,source,label,data) VALUES(?,?,?,?,?,?) ON CONFLICT(problem) DO UPDATE SET "
      "time=excluded.time,kind=excluded.kind,source=excluded.source,label=excluded.label,data=excluded.data",
      (problem, now(), kind, source, label, j(data)))


def get_artifact(problem):
    r = q("SELECT * FROM artifacts WHERE problem=?", (problem,))
    if not r:
        return None
    d = uj(r[0]["data"]) or {}
    d.setdefault("source", r[0]["source"])
    if r[0]["label"]:
        d.setdefault("label", r[0]["label"])
    return d


def set_best(problem, score, verified, solution, strategy_id=None, path=None, beats=False):
    x("INSERT INTO bests(problem,score,verified,time,strategy_id,solution,path,beats_record) VALUES(?,?,?,?,?,?,?,?) "
      "ON CONFLICT(problem) DO UPDATE SET score=excluded.score,verified=excluded.verified,time=excluded.time,"
      "strategy_id=excluded.strategy_id,solution=excluded.solution,path=excluded.path,beats_record=excluded.beats_record",
      (problem, score, int(bool(verified)), now(), strategy_id, j(solution), path, int(bool(beats))))


def get_best(problem):
    r = q("SELECT * FROM bests WHERE problem=?", (problem,))
    if not r:
        return None
    d = dict(r[0])
    d["solution"] = uj(d["solution"])
    d["verified"] = bool(d["verified"])
    d["beats_record"] = bool(d["beats_record"])
    return d
