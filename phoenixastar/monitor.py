"""Live view of the box: polls telemetry, adopts/reconciles strategies, derives per-problem metrics and staleness.

The latest snapshot lives in memory (and the DB, so a restart or the static snapshot still has it).
"""
import json
import re
import threading
import time

from . import config, events, ledger, strategies

_lock = threading.RLock()
_update_lock = threading.Lock()   # reconcile + metrics from one snapshot at a time (poller, loop and API threads all poll)
_cur = {"snap": None, "t": 0.0, "procs": [], "foreign": [], "metrics": {}, "classes": {}, "error": None,
        "artifact_t": 0.0}
VANISH_GRACE_S = 90               # a strategy launched this recently is not declared exited from one missing snapshot

# Families whose logs print a line only when their best improves: log mtime = time of the last improvement.
# Every other generic family (twodel_ils, sidon_sa, ...) prints periodic status lines, so its staleness is tracked
# here from the value itself: since = when this log's best value last changed (persisted, survives restarts).
PRINTS_ON_IMPROVEMENT = {"spencer", "hadamard", "nothree_gpu"}
_best_seen = {"loaded": False, "d": {}}   # log path -> [best value, since_ts]


# metrics reported by secondary search families: [(log key, lower_is_better)]
SECONDARY_METRICS = {"nothree_gpu": [("best_triples", True), ("best_after_deletion", True)]}


def _is_test_foreign(p, sid_env):
    argv = " ".join(p.get("argv") or [])
    if sid_env and sid_env.startswith("test-"):
        return ledger.get_strategy(sid_env) is None   # someone else's test run
    return "_test" in argv or "/test" in argv or "runs/test" in argv


def _metric_of(family, li):
    if not li:
        return None
    if family == "spencer":
        return li.get("best_bad")
    if family == "hadamard":
        return li.get("best_log10")
    if family == "nothree":
        return li.get("best_violated")
    vals = li.get("values") or {}
    if family == "sidon":
        m = re.search(r"best=(\d+)/(\d+)=([\d.]+)", li.get("last_line") or "")
        if m:
            return float(m.group(3))
    if family == "threebody":     # count only families that are NEW relative to the catalog (not rediscoveries)
        return vals.get("new", vals.get("best"))
    if family == "nothree_gpu":   # GPU min-conflicts: collinear triples left (0 = 150 points)
        return vals.get("best_triples")
    for k in ("best", "best_score", "score", "best_size", "size", "best_length", "count"):
        if k in vals:
            return vals[k]
    js = li.get("json") or {}
    for k in ("best", "score", "size", "count"):
        if isinstance(js.get(k), (int, float)):
            return js[k]
    return None


def _track_best(path, family, li, now):
    """For periodic-status families: when did this log's best value last change? Returns since_ts or None."""
    if not path or not li or family in PRINTS_ON_IMPROVEMENT or family == "nothree":
        return None
    v = _metric_of(family, li)
    if v is None:
        return None
    if not _best_seen["loaded"]:
        _best_seen["d"] = ledger.kv_get("best_seen", {}) or {}
        _best_seen["loaded"] = True
    rec = _best_seen["d"].get(path)
    if rec is None:
        # first sight: a finished run's log stopped changing at its mtime; for a live run we only know "since now"
        first = now if li.get("alive", True) else min(now, li.get("mtime", now))
        _best_seen["d"][path] = rec = [v, first]
    elif rec[0] != v:                       # a best only changes when it improves
        _best_seen["d"][path] = rec = [v, now]
    return rec[1]


def _improve_age_s(family, li, etime_s, now, path=None):
    """Seconds since this run last improved its own best (from log timing), or None."""
    if not li:
        return None
    if family in PRINTS_ON_IMPROVEMENT:
        return max(0.0, now - li.get("mtime", now))       # these logs only print on improvement
    if family == "nothree" and li.get("best_t") is not None:
        start = (now - etime_s) if etime_s is not None else (li.get("mtime", now) - (li.get("t") or 0))
        return max(0.0, now - (start + li["best_t"]))
    since = _track_best(path, family, li, now)
    if since is not None:
        return max(0.0, now - since)
    return max(0.0, now - li.get("mtime", now))


def _history_age_s(slug, metric, value, now):
    """Seconds the problem-level metric has been at `value`, from the stored history (spans restarts), or None."""
    h = ledger.metric_history(slug, metric, limit=2000)
    if not h or value is None or h[-1][1] != value:
        return None
    since = h[-1][0]
    for t, v in reversed(h):
        if v != value:
            break
        since = t
    ts = ledger.parse_iso(since)
    return max(0.0, now - ts) if ts else None


def reconcile(snap, cycle=None):
    """Adopt new processes, update running ones, mark vanished ones exited. Returns (procs, foreign)."""
    now = snap.get("time") or time.time()
    procs, foreign, seen, new_adopted = [], [], set(), {}
    for p in snap.get("procs", []):
        name, params, extra = strategies.parse_cmdline(p.get("argv") or [])
        if not name:
            continue
        t = strategies.get(name)
        sid_env = p.get("strategy_id")
        li = p.get("log_info") or {}
        fam = p.get("family") or ""
        rec = {"pid": p["pid"], "template": name, "params": params, "problem": t.get("problem"),
               "resource": t.get("resource", "cpu"), "gpu": (p.get("gpus") or [None])[0], "log": p.get("log"),
               "cmdline": " ".join(p.get("argv") or []), "etime_s": p.get("etime_s"),
               "metric_value": _metric_of(fam, li), "family": fam, "log_info": li,
               "improve_age_s": _improve_age_s(fam, li, p.get("etime_s"), now, p.get("log"))}
        if _is_test_foreign(p, sid_env):
            rec["id"] = f"foreign-{p['pid']}"
            foreign.append(rec)
            continue
        if sid_env:
            sid, adopted = sid_env, False
        else:
            sid, adopted = f"adopt-{name}-{p['pid']}", True
        rec["id"] = sid
        rec["adopted"] = adopted
        old = ledger.get_strategy(sid)
        started = old["started_at"] if old and old.get("started_at") else ledger.iso(now - (p.get("etime_s") or 0))
        ledger.upsert_strategy({"id": sid, "problem": rec["problem"], "template": name, "params": params,
                                "resource": rec["resource"], "gpu": rec["gpu"], "pid": p["pid"], "started_at": started,
                                "status": "running", "adopted": int(adopted), "cmdline": rec["cmdline"],
                                "log": rec["log"], "metric_value": rec["metric_value"],
                                "test": int(sid.startswith("test-"))})
        if old is None and adopted:
            new_adopted.setdefault((rec["problem"], name), []).append(rec)
        rec["started_at"] = started
        seen.add(sid)
        procs.append(rec)
    for (slug, name), recs in new_adopted.items():
        groups = {}
        for r in recs:
            k = json.dumps({a: b for a, b in r["params"].items() if a != "seed"}, sort_keys=True)
            groups.setdefault(k, []).append(r)
        desc = "; ".join(f"{len(g)}x {k}" for k, g in groups.items())
        gp = sorted({r["gpu"] for r in recs if r["gpu"] is not None})
        did = ledger.add_decision(cycle, "executor", "adopt", slug,
                                  {"template": name, "count": len(recs), "strategy_ids": [r["id"] for r in recs],
                                   "pids": [r["pid"] for r in recs], "gpus": gp},
                                  f"Adopted {len(recs)} already-running {name} processes found on the box (not restarted): "
                                  f"{desc[:600]}. Params parsed from each command line"
                                  f"{', GPUs ' + str(gp) + ' from CUDA_VISIBLE_DEVICES / nvidia-smi' if gp else ''}.")
        events.publish("decision", ledger.get_decision(did))
    # vanished strategies
    logs = snap.get("logs", {})
    for s in ledger.strategies(status="running"):
        if s["id"] in seen or str(s["id"]).startswith("modal-"):
            continue
        st = ledger.parse_iso(s.get("started_at"))
        if not s.get("adopted") and st and time.time() - st < VANISH_GRACE_S:
            continue    # just launched: this snapshot may predate it (the launch itself confirmed the pid alive)
        li = logs.get(s.get("log") or "", {}) if s.get("log") else {}
        if not li and s.get("log"):
            li = logs.get(f"/home/ubuntu/ltd/{s['log']}", {}) or {}
        # "UNSAT" means a proof only for the SAT no-three runs (twodel_lns, e.g., logs UNSAT for each closed neighbourhood)
        reason = "UNSAT" if li.get("unsat") and li.get("family") == "nothree" else ("FOUND" if li.get("found") else "exited")
        ledger.upsert_strategy({"id": s["id"], "status": "exited" if reason == "exited" else reason.lower(),
                                "stopped_at": ledger.now(), "stop_reason": reason})
        last = (li.get("last_line") or "")[-200:]
        ledger.add_decision(cycle, "executor", "exited", s["problem"], {"strategy_id": s["id"], "reason": reason},
                            f"Process {s['id']} (pid {s.get('pid')}) is no longer running; log says: {last or 'n/a'}")
    return procs, foreign


def _problem_metrics(snap, procs):
    """{slug: {value, lower_is_better, name, sub:{key: value}, since_ts, runs}} plus nothree class table."""
    now = snap.get("time") or time.time()
    logs = snap.get("logs", {})
    fam2slug = dict(config.FAMILY_TO_PROBLEM)
    fam2slug.update(snap.get("families") or {})
    out, classes = {}, {}
    alive = {p["log"]: p for p in procs if p.get("log")}
    for slug, P in config.PROBLEMS.items():
        out[slug] = {"name": P["metric"], "lower_is_better": P["lower_is_better"], "value": None, "sub": {},
                     "best_age_s": None}
    for path, li in logs.items():
        fam = li.get("family")
        slug = fam2slug.get(fam)
        if not slug or slug not in out:
            continue
        v = _metric_of(fam, li)
        m = out[slug]
        p = alive.get(path)
        age = _improve_age_s(fam, li, p["etime_s"] if p else None, now, path)
        if fam == "nothree" and li.get("sym"):
            c = classes.setdefault(li["sym"], {"sym": li["sym"], "procs": 0, "logs": 0, "unsat": 0, "found": 0,
                                               "best_violated": None, "best_age_s": None, "current_min": None,
                                               "current_median": None, "rounds_median": None, "lines_median": None,
                                               "_cur": [], "_rounds": [], "_lines": [], "rounds_last_15min": 0,
                                               "no_round_yet": 0})
            c["logs"] += 1
            c["procs"] += int(p is not None)
            c["unsat"] += int(bool(li.get("unsat")))
            c["found"] += int(bool(li.get("found")))
            if p is not None and v is None:
                c["no_round_yet"] += 1
            if li.get("violated") is not None and p is not None:
                c["_cur"].append(li["violated"]); c["_rounds"].append(li.get("round") or 0); c["_lines"].append(li.get("lines") or 0)
            if v is not None:
                if c["best_violated"] is None or v < c["best_violated"]:
                    c["best_violated"], c["best_age_s"] = v, age
                elif v == c["best_violated"] and age is not None and (c["best_age_s"] is None or age > c["best_age_s"]):
                    c["best_age_s"] = age
            if p is not None and li.get("recent") and li.get("t") is not None:
                start = now - (p["etime_s"] or 0)
                c["rounds_last_15min"] += sum(1 for r in li["recent"] if start + r[2] > now - 900)
        if v is None:
            continue
        if fam != config.PROBLEMS[slug]["family"] and fam in SECONDARY_METRICS:
            # a secondary search family for this problem (e.g. nothree_gpu counts collinear triples, not violated
            # lines): reported under metric["extra"], never mixed into the main metric
            vals = dict(li.get("values") or {})
            for name, lib in SECONDARY_METRICS.get(fam, [("best", m["lower_is_better"])]):
                if name in vals:
                    k = f"{fam}.{name}"
                    ex = m.setdefault("extra", {})
                    if ex.get(k) is None or (vals[name] < ex[k] if lib else vals[name] > ex[k]):
                        ex[k] = vals[name]
                    m.setdefault("extra_lower_is_better", {})[k] = lib
            continue
        better = (m["value"] is None or (v < m["value"] if m["lower_is_better"] else v > m["value"]))
        if better:
            m["value"], m["best_age_s"] = v, age
        elif v == m["value"] and age is not None and (m["best_age_s"] is None or age > m["best_age_s"]):
            m["best_age_s"] = age   # the best was first reached by the oldest run that holds it
        key = None
        if fam == "spencer" and "n" in li:
            key = f"n{li['n']}D{li['D']}"
        elif fam == "nothree" and li.get("sym"):
            key = li["sym"]
        if key:
            sv = m["sub"].get(key)
            if sv is None or (v < sv if m["lower_is_better"] else v > sv):
                m["sub"][key] = v
    for c in classes.values():
        cur, rr, ln = sorted(c.pop("_cur")), sorted(c.pop("_rounds")), sorted(c.pop("_lines"))
        c["current_min"] = cur[0] if cur else None
        c["current_median"] = cur[len(cur) // 2] if cur else None
        c["rounds_median"] = rr[len(rr) // 2] if rr else None
        c["lines_median"] = ln[len(ln) // 2] if ln else None
    if "no-three-in-line-75" in out:
        out["no-three-in-line-75"]["unsat_classes"] = sorted(k for k, c in classes.items() if c["unsat"])
    # periodic-status families: the problem's best is at least as old as its unchanged run in the stored history
    for slug, m in out.items():
        if config.PROBLEMS[slug]["family"] in PRINTS_ON_IMPROVEMENT or slug == "no-three-in-line-75" or m["value"] is None:
            continue
        ha = _history_age_s(slug, m["name"], m["value"], now)
        if ha is not None and (m["best_age_s"] is None or ha > m["best_age_s"]):
            m["best_age_s"] = ha
    # verified bests override for problems where the metric is the score itself
    for slug in ("sidon-45-set", "two-deletion-code-16"):
        b = ledger.get_best(slug)
        if b and b.get("verified") and b.get("score") is not None and slug in out:
            m = out[slug]
            if m["value"] is None or (b["score"] < m["value"] if m["lower_is_better"] else b["score"] > m["value"]):
                m["value"] = b["score"]
    return out, classes


def update(snap, cycle=None, store=True):
    try:
        from . import fleet
        fleet.refresh()
        flogs = fleet.logs()
        if flogs:
            snap = dict(snap); snap["logs"] = {**(snap.get("logs") or {}), **flogs}
    except Exception as e:  # noqa: BLE001 - the fleet is optional; the box alone still works
        events.log(f"modal fleet telemetry failed: {e}", "warn")
    with _update_lock:
        with _lock:
            last_t = (_cur.get("snap") or {}).get("time") if _cur.get("t") else None
            if last_t and snap.get("time") and snap["time"] < last_t:
                return list(_cur["procs"])    # an older snapshot that finished after a newer one: ignore it
        procs, foreign = reconcile(snap, cycle)
        metrics, classes = _problem_metrics(snap, procs)
        with _lock:
            _cur.update(snap=snap, t=time.time(), procs=procs, foreign=foreign, metrics=metrics, classes=classes, error=None)
        if _best_seen["loaded"]:
            live = set(snap.get("logs") or {})
            _best_seen["d"] = {k: v for k, v in _best_seen["d"].items() if k in live}
            ledger.kv_set("best_seen", _best_seen["d"])
        _store(snap, procs, foreign, metrics, classes, cycle, store)
    events.publish("telemetry", telemetry_event())
    return procs


def _store(snap, procs, foreign, metrics, classes, cycle, store):
    if store:
        slim = {k: v for k, v in snap.items() if k not in ("logs", "procs", "artifacts")}
        slim["procs_slim"] = [{k: p.get(k) for k in ("id", "pid", "template", "problem", "gpu", "metric_value",
                                                       "improve_age_s", "adopted", "resource", "params", "started_at",
                                                       "etime_s", "log")} for p in procs]
        slim["foreign_slim"] = [{k: p.get(k) for k in ("id", "pid", "template", "problem", "gpu", "resource", "params")}
                                for p in foreign]
        slim["metrics"] = metrics
        slim["classes"] = classes
        ledger.add_snapshot(slim, cycle)
        last = ledger.kv_get("last_metric_store", 0) or 0
        if time.time() - last > 55:
            for slug, m in metrics.items():
                if m["value"] is not None:
                    ledger.add_metric(slug, m["name"], m["value"], cycle)
                for k, v in (m.get("sub") or {}).items():
                    ledger.add_metric(slug, f"{m['name']}@{k}", v, cycle)
                for k, v in (m.get("extra") or {}).items():     # secondary metrics (e.g. nothree_gpu.best_triples)
                    if isinstance(v, (int, float)):
                        ledger.add_metric(slug, k, v, cycle)
            ledger.kv_set("last_metric_store", time.time())


def current():
    with _lock:
        return dict(_cur)


def restore_from_db():
    """At startup, show the last stored snapshot until the first live poll lands."""
    snap, t = ledger.last_snapshot()
    if snap:
        procs = []
        for p in snap.get("procs_slim", []):
            rec = ledger.get_strategy(p["id"]) or {}
            q = {"params": rec.get("params") or {}, "started_at": rec.get("started_at"), "resource": rec.get("resource", "cpu"),
                 "adopted": bool(rec.get("adopted")), "log": rec.get("log")}
            q.update({k: v for k, v in p.items() if v is not None})
            q["log_info"] = None
            procs.append(q)
        with _lock:
            _cur.update(snap=snap, metrics=snap.get("metrics", {}), classes=snap.get("classes", {}), procs=procs,
                        foreign=[dict(p, params=p.get("params") or {}) for p in snap.get("foreign_slim", [])], t=0.0)


def poll(cycle=None, artifacts=False):
    from . import box
    try:
        snap = box.telemetry(artifacts=artifacts)
    except Exception as e:  # noqa: BLE001 - the box may be offline; never crash callers
        with _lock:
            _cur["error"] = str(e)
        events.log(f"telemetry failed: {e}", "warn")
        events.publish("telemetry", telemetry_event())
        return None
    update(snap, cycle)
    if artifacts and snap.get("artifacts"):
        from . import artifacts as art
        try:
            art.ingest(snap["artifacts"], snap)
        except Exception as e:  # noqa: BLE001
            events.log(f"artifact ingest failed: {e}", "warn")
        with _lock:
            _cur["artifact_t"] = time.time()
    return snap


def compute():
    """state.compute in the API shape."""
    from . import box
    cur = current()
    snap = cur["snap"] or {}
    allp = list(cur["procs"]) + list(cur["foreign"])
    by_gpu = {}
    for p in allp:
        if p.get("gpu") is not None:
            by_gpu.setdefault(int(p["gpu"]), []).append(p)
    gpus = []
    for g in snap.get("gpus", []):
        owners = sorted(by_gpu.get(g["idx"], []), key=lambda p: p.get("etime_s") or 0)  # newest first
        prim = owners[0] if owners else None
        gpus.append({"idx": g["idx"], "util": g.get("util", 0), "mem_mb": g.get("mem", 0),
                     "problem": prim["problem"] if prim else None, "strategy_id": prim["id"] if prim else None,
                     "strategy_ids": [p["id"] for p in owners], "problems": sorted({p["problem"] for p in owners})})
    cpu_procs = {}
    for p in allp:
        cpu_procs[p["problem"]] = cpu_procs.get(p["problem"], 0) + 1
    fresh = cur["t"] and time.time() - cur["t"] < max(3 * config.TELEMETRY_POLL_S, 120)
    return {"gpus": gpus, "cpus": snap.get("cpus", config.CPU_TOTAL), "load1": round(float(snap.get("load1") or 0), 2),
            "cpu_procs": cpu_procs, "box": "online" if (fresh and box.online() is not False and not cur["error"]) else "offline",
            "other_busy": snap.get("other_busy", 0), "telemetry_at": ledger.iso(snap["time"]) if snap.get("time") else None,
            "modal": _fleet_summary()}


def _fleet_summary():
    try:
        from . import fleet
        return fleet.summary()
    except Exception as e:  # noqa: BLE001
        return {"containers": 0, "by_problem": {}, "error": str(e)[:200]}


def budget():
    """Free capacity: GPUs nobody owns and cores below the CPU target."""
    cur = current()
    snap = cur["snap"] or {}
    allp = list(cur["procs"]) + list(cur["foreign"])
    owned = {int(p["gpu"]) for p in allp if p.get("gpu") is not None}
    for g in snap.get("gpus", []):
        if g.get("pids"):
            owned.add(g["idx"])
    idx = [g["idx"] for g in snap.get("gpus", [])] or list(range(config.GPU_COUNT))
    # no GPU table (no snapshot yet, or nvidia-smi failed on the box): occupancy unknown, so nothing counts as free
    free_gpus = [i for i in idx if i not in owned and i not in config.RESERVED_GPUS] if snap.get("gpus") else []
    used = len(allp) + int(snap.get("other_busy") or 0)
    # safety floor: if the process table ever comes back short (or something we do not parse is busy), the load
    # average still shows the cores are taken, so refill can never pile dozens of extra processes onto a full box
    if snap.get("load1") is not None:
        used = max(used, int(float(snap["load1"])) - 6)
    return {"free_gpus": free_gpus, "gpus_total": len(idx), "cores_used": used,
            "free_cores": max(0, config.CPU_TARGET - used), "cpu_target": config.CPU_TARGET,
            "load1": snap.get("load1")}


def telemetry_event():
    cur = current()
    return {**compute(), "metrics": {s: m.get("value") for s, m in (cur["metrics"] or {}).items()}}
