"""Critic: (a) re-verifies every FOUND_* / best_* artifact with the OFFICIAL verifier (never trusts the search);
(b) scores past predictions once their horizon has passed and writes the lesson to memory."""
import json
import threading
import time

from . import artifacts, config, events, ledger

_q, _qlock, _run_lock = [], threading.Lock(), threading.Lock()


def _slug_for_path(path):
    fams = dict(config.FAMILY_TO_PROBLEM)
    try:
        from . import monitor
        fams.update((monitor.current().get("snap") or {}).get("families") or {})
    except Exception:  # noqa: BLE001
        pass
    parts = path.split("/runs/", 1)[-1].split("/")
    return fams.get(parts[0]) if parts else None


def _key(path, candidate, mtime):
    return f"{path}@{int(mtime or 0)}" if candidate else path


def queue_found(path, candidate=False, mtime=None):
    """FOUND files are verified once; best_* candidate files again whenever they change (at most every 10 min)."""
    key = _key(path, candidate, mtime)
    if ledger.q("SELECT 1 FROM verified_paths WHERE path=?", (key,)):
        return
    if candidate:
        last = ledger.q("SELECT time FROM verified_paths WHERE path LIKE ? ORDER BY time DESC LIMIT 1", (path + "@%",))
        if last and time.time() - (ledger.parse_iso(last[0]["time"]) or 0) < 600:
            return
    with _qlock:
        if key not in [k for k, _, _ in _q]:
            _q.append((key, path, candidate))


def process_queue(cycle=None, budget_s=240):
    """Verify queued files (blocking, bounded by budget_s). Returns list of result dicts."""
    out = []
    if not _run_lock.acquire(blocking=False):
        return out
    try:
        t0 = time.time()
        while time.time() - t0 < budget_s:
            with _qlock:
                if not _q:
                    break
                key, path, candidate = _q.pop(0)
            if ledger.q("SELECT 1 FROM verified_paths WHERE path=?", (key,)):
                continue
            out.append(_verify_file(path, candidate, cycle, key))
    finally:
        _run_lock.release()
    return out


def _verify_file(path, candidate, cycle, key=None):
    from . import box, memory
    slug = _slug_for_path(path)
    if not slug:
        ledger.x("INSERT OR REPLACE INTO verified_paths VALUES(?,?,?,?,?,?)", (key or path, None, ledger.now(), 0, None, "unknown family"))
        return {"path": path, "ok": False, "error": "unknown family"}
    try:
        if path.startswith("modal:"):     # FOUND file on the Modal fleet's Volume
            from . import fleet
            d = json.loads(fleet.fetch(path))
        else:
            d = json.loads(box.fetch(path))
        sol = d.get("solution", d)
    except Exception as e:  # noqa: BLE001
        return {"path": path, "ok": False, "error": f"fetch failed: {e}"}
    r = artifacts.verify(slug, sol)
    ledger.x("INSERT OR REPLACE INTO verified_paths VALUES(?,?,?,?,?,?)",
             (key or path, slug, ledger.now(), int(bool(r["ok"])), r.get("score"), r.get("error")))
    P = config.PROBLEMS[slug]
    claimed = d.get("score", d.get("log10", d.get("points_count")))
    if not r["ok"]:
        did = ledger.add_decision(cycle, "critic", "reject", slug, {"path": path, "claimed": claimed},
                                  f"Official verifier REJECTED {path}: {r['error']}. The search's own claim is not trusted.",
                                  outcome={"observed": None, "verdict": "n/a", "note": r["error"]})
        events.publish("decision", ledger.get_decision(did))
        return {"path": path, **r}
    beats = config.beats_record(slug, r["score"])
    if candidate and not beats:
        same_as_record = P["record"] is not None and abs(r["score"] - P["record"]) < 1e-12
        prev = ledger.kv_get(f"cand_score:{path}")
        ledger.kv_set(f"cand_score:{path}", r["score"])
        best = ledger.get_best(slug)
        better = (not same_as_record) and (best is None or best.get("score") is None or (
            r["score"] > best["score"] if P["scoring"] == "maximize" else r["score"] < best["score"]))
        if better:
            ledger.set_best(slug, r["score"], True, sol, None, path, False)
            _set_ours_artifact(slug, sol, r["score"], path)
        if prev != r["score"]:
            did = ledger.add_decision(
                cycle, "critic", "verified", slug, {"path": path, "score": r["score"], "record": P["record"], "candidate": True},
                f"Official verifier scored the search's current best file {path.rsplit('/', 1)[-1]} at {r['score']} "
                f"({'equals the record it started from' if same_as_record else 'valid, below the record'}; record "
                f"{P['record']} by {P['holder']}).", outcome={"observed": r["score"], "verdict": "n/a", "note": "candidate"})
            events.publish("decision", ledger.get_decision(did))
        return {"path": path, **r, "beats_record": False}
    best = ledger.get_best(slug)
    better = best is None or best.get("score") is None or (
        r["score"] > best["score"] if P["scoring"] == "maximize" else r["score"] < best["score"])
    sid = None
    stem = path.rsplit("/", 1)[-1].replace("FOUND_", "").rsplit(".", 1)[0]
    for s in ledger.strategies(problem=slug):
        if s.get("log") and stem.split("_")[0] in s["log"] and f"s{s['params'].get('seed')}" in stem:
            sid = s["id"]
    if better:
        ledger.set_best(slug, r["score"], True, sol, sid, path, beats)
        _set_ours_artifact(slug, sol, r["score"], path)
    verdict = "RECORD" if beats else "valid, not a record"
    did = ledger.add_decision(
        cycle, "critic", "record" if beats else "verified", slug,
        {"path": path, "score": r["score"], "record": P["record"], "min_improvement": P["min_improvement"], "claimed": claimed},
        f"Official verifier ({slug}/verifier.py) scored {path.rsplit('/', 1)[-1]} at {r['score']} in {r['seconds']}s: {verdict} "
        f"(leaderboard top {P['record']} by {P['holder']}, minImprovement {P['min_improvement']}).",
        outcome={"observed": r["score"], "verdict": "confirmed" if beats else "n/a", "note": verdict})
    events.publish("decision", ledger.get_decision(did))
    fid = memory.write("critic", slug, f"Verified {path.rsplit('/', 1)[-1]} with the official verifier: score {r['score']} "
                       f"({verdict}; record {P['record']}).", ["verification"])
    ledger.update_decision(did, memory_writes=[fid])
    if beats:
        events.publish("record", {"slug": slug, "score": r["score"], "verified": True})
        events.log(f"NEW RECORD on {slug}: {r['score']} (verified)", "record")
    return {"path": path, **r, "beats_record": beats}


def _nothree_origin(path):
    """{sym, round} of a no-three FOUND file: SAT runs write FOUND_<sym>_s<seed>_<n>.json (round from that run's
    log), the GPU min-conflicts runs FOUND_s<seed>_<n>_<time>.json."""
    import re
    name = path.rsplit("/", 1)[-1]
    m = re.match(r"FOUND_(.+)_s(\d+)_(\d+)\.json$", name)
    if m and not name.startswith("FOUND_s"):
        sym, seed = m.group(1), m.group(2)
        rnd = None
        try:
            from . import monitor
            for lp, li in ((monitor.current().get("snap") or {}).get("logs") or {}).items():
                if lp.endswith(f"/{sym}_s{seed}.log") and li.get("round") is not None:
                    rnd = int(li["round"])
        except Exception:  # noqa: BLE001
            pass
        return {"sym": sym, "round": rnd if rnd is not None else 0, "seed": int(seed)}
    m = re.match(r"FOUND_s(\d+)_", name)
    return {"sym": "gpu min-conflicts (no symmetry)", "round": 0, "seed": int(m.group(1)) if m else None}


def _set_ours_artifact(slug, sol, score, path):
    kind = config.PROBLEMS[slug]["artifact_kind"]
    if slug == "no-three-in-line-75":
        a = {"kind": "grid", "n": 75, "points": sol["points"], "violated_lines": [], "count": len(sol["points"])}
        a.update(_nothree_origin(path))
    elif slug == "spencer-discrepancy":
        m = sol["matrix"]
        # official score = discrepancy / sqrt(n), so the discrepancy every sign vector reaches is score * sqrt(n)
        a = {"kind": "sign_matrix", "n": len(m), "D": int(round(score * len(m) ** 0.5)), "matrix": m, "bad_vectors": 0,
             "total_vectors": 2 ** (len(m) - 1)}
    elif slug == "hadamard-det-51":
        a = {"kind": "sign_matrix", "n": len(sol["matrix"]), "matrix": sol["matrix"], "log10_det": score}
    elif slug == "sidon-45-set":
        el = sorted(sol["elements"])
        a = {"kind": "integer_set", "elements": el, "h": round(score * len(el)), "score": score}
    elif slug == "two-deletion-code-16":
        a = {"kind": "code", "words": sol["words"], "count": len(sol["words"])}
    else:
        a = {"kind": kind or "solution", "solution": sol}
    a["file"] = path
    ledger.set_artifact(slug, a["kind"], a, "ours", f"our verified construction (score {score})")


# ---------------- predictions ----------------
def observe(metric, metrics, problem=None):
    """Observed value of a prediction metric name: '<metric>' or '<metric>@<sub>' (e.g. min_violated_lines@rot180-150)."""
    base, _, sub = metric.partition("@")
    cands = [problem] if problem else []
    cands += [s for s in metrics if s not in cands]
    for slug in cands:
        m = metrics.get(slug) or {}
        if metric in (m.get("extra") or {}):
            return m["extra"][metric]
        if m.get("name") != base:
            continue
        if sub:
            return (m.get("sub") or {}).get(sub)
        return m.get("value")
    return None


def _history_value_at(slug, metric, at):
    """The stored value of a metric ('<name>' or '<name>@<sub>') at or just before time `at`, or None."""
    r = ledger.q("SELECT value FROM telemetry WHERE kind='metric' AND problem=? AND metric=? AND time<=? "
                 "ORDER BY id DESC LIMIT 1", (slug, metric, at))
    if r:
        return r[0]["value"]
    # no sample before the decision (e.g. the first runs of a problem): the first sample within 15 min after it
    t = ledger.parse_iso(at)
    if t is None:
        return None
    r = ledger.q("SELECT value FROM telemetry WHERE kind='metric' AND problem=? AND metric=? AND time>? AND time<=? "
                 "ORDER BY id LIMIT 1", (slug, metric, at, ledger.iso(t + 900)))
    return r[0]["value"] if r else None


def score_predictions(cycle, metrics):
    """Resolve every pending prediction whose horizon has passed. Returns the resolved decisions."""
    from . import memory
    rows = ledger.q("SELECT * FROM decisions WHERE prediction IS NOT NULL AND outcome LIKE '%\"pending\"%' ORDER BY id")
    out = []
    now = time.time()
    for r in rows:
        try:
            pred = ledger.uj(r["prediction"]) or {}
            t = ledger.parse_iso(r["time"]) or now
            if now < t + 60 * float(pred.get("horizon_min") or 30):
                continue
            slug = r["problem"]
            obs = observe(str(pred.get("metric", "")), metrics, slug)
            exp = float(pred.get("expected"))
        except (TypeError, ValueError) as e:     # a malformed prediction must not fail the whole cycle
            ledger.update_decision(r["id"], outcome={"observed": None, "verdict": "n/a", "note": f"unscorable prediction: {e}"[:200]})
            continue
        p = ledger.uj(r["params"], {}) or {}
        base = p.get("baseline")
        if not isinstance(base, (int, float)):
            base = _history_value_at(slug, str(pred.get("metric", "")), r["time"])
        ms = metrics.get(slug) or {}
        lib = (ms.get("extra_lower_is_better") or {}).get(str(pred.get("metric")), ms.get("lower_is_better", True))
        if not isinstance(obs, (int, float)):
            outcome = {"observed": None, "verdict": "n/a", "note": f"metric {pred.get('metric')!r} not observable"}
        elif isinstance(base, (int, float)) and not (exp < base - 1e-9 if lib else exp > base + 1e-9):
            # every live metric is a running best (it can never get worse), so "stays at <= its value now" cannot
            # fail: such a prediction carries no information and is not counted as confirmed
            outcome = {"observed": obs, "verdict": "n/a",
                       "note": f"trivial: predicted no improvement over {base} (a running best cannot get worse); not scored"}
        else:
            ok = obs <= exp + 1e-9 if lib else obs >= exp - 1e-9
            outcome = {"observed": obs, "verdict": "confirmed" if ok else "refuted",
                       "note": f"expected {'<=' if lib else '>='} {exp} (from {base}) after {pred.get('horizon_min')} min, "
                               f"observed {obs}"}
        ledger.update_decision(r["id"], outcome=outcome)
        if outcome["verdict"] in ("confirmed", "refuted"):
            p = ledger.uj(r["params"], {}) or {}
            lesson = (f"Prediction of decision #{r['id']} ({r['action']} {p.get('template') or ''} "
                      f"{json.dumps(p.get('params') or {}, sort_keys=True)[:120]}) on {slug}: {pred.get('metric')} "
                      f"{'<=' if lib else '>='} {pred.get('expected')} within "
                      f"{pred.get('horizon_min')} min was {outcome['verdict'].upper()} (observed {obs}).")
            fid = memory.write("critic", slug, lesson, ["lesson", outcome["verdict"]])
            did = ledger.add_decision(cycle, "critic", "score_prediction", slug,
                                      {"decision_id": r["id"], "metric": pred.get("metric"), "expected": pred.get("expected")},
                                      lesson, outcome=outcome, memory_writes=[fid])
            events.publish("decision", ledger.get_decision(did))
        out.append({"id": r["id"], **outcome})
    return out
