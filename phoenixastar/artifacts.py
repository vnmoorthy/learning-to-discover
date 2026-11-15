"""Artifacts for the UI (one per problem) built from files pulled off the box, or the public record when we have nothing better.

Every artifact says where it came from: source = "ours" (verified), "candidate" (current search state, not a valid
solution yet), or "record" (the leaderboard holder's construction, shown for reference).
"""
import hashlib
import json
import subprocess
import sys
import threading
import time

from . import config, events, ledger

_verify_lock = threading.Lock()


def verify(slug, solution, timeout=None):
    """Run the official verifier in a subprocess. Returns {ok, score, error, seconds}."""
    timeout = timeout or (600 if slug in ("hadamard-det-51", "spencer-discrepancy", "two-deletion-code-16") else 180)
    t0 = time.time()
    try:
        p = subprocess.run([sys.executable, "-m", "phoenixastar.verify_worker", slug], input=json.dumps(solution),
                           capture_output=True, text=True, timeout=timeout, cwd=config.ROOT)
    except subprocess.TimeoutExpired:
        return {"ok": False, "score": None, "error": f"verifier timeout after {timeout}s", "seconds": round(time.time() - t0, 2)}
    try:
        res = json.loads(p.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return {"ok": False, "score": None, "error": f"verifier crashed: {p.stderr.strip()[-300:]}",
                "seconds": round(time.time() - t0, 2)}
    res["seconds"] = round(time.time() - t0, 2)
    return res


def masks_to_matrix(rows, n):
    return [[-1 if (r >> j) & 1 else 1 for j in range(n)] for r in rows]


def record_solution(slug):
    lb = config.load_leaderboard(slug)
    if not lb:
        return None, None
    d = lb[0].get("data")
    if isinstance(d, str):
        try:
            d = json.loads(d)
        except ValueError:
            return None, None
    return d, lb[0]


def record_artifact(slug):
    sol, row = record_solution(slug)
    if not sol:
        return None
    holder = row.get("agentName")
    score = float(row["score"])
    if slug == "hadamard-det-51":
        return {"kind": "sign_matrix", "n": len(sol["matrix"]), "matrix": sol["matrix"], "log10_det": score,
                "source": "record", "label": f"record matrix by {holder} (not ours)"}
    if slug == "sidon-45-set":
        el = sorted(int(v) for v in sol["elements"])
        h = round(score * len(el))
        return {"kind": "integer_set", "elements": el, "h": h, "score": score, "source": "record",
                "label": f"record set by {holder} (not ours)"}
    if slug == "two-deletion-code-16":
        return {"kind": "code", "words": sol["words"], "count": len(sol["words"]), "source": "record",
                "label": f"record code by {holder} (not ours)"}
    if slug == "spencer-discrepancy":
        m = sol["matrix"]
        return {"kind": "sign_matrix", "n": len(m), "D": int(round(score * len(m) ** 0.5)), "matrix": m, "bad_vectors": 0,
                "total_vectors": 2 ** (len(m) - 1),
                "source": "record", "label": f"record matrix by {holder} (not ours)"}
    if slug == "no-three-in-line-75":
        return {"kind": "grid", "n": 75, "points": sol["points"], "violated_lines": [], "count": len(sol["points"]),
                "sym": "record", "round": 0, "source": "record", "label": f"record configuration by {holder} (not ours)"}
    return None


def ensure_defaults():
    """Make sure every attacked problem has some artifact (record reference) before the first box pull."""
    for slug in ("hadamard-det-51", "sidon-45-set", "two-deletion-code-16"):
        a = ledger.get_artifact(slug)
        if a is None:
            ra = record_artifact(slug)
            if ra:
                ledger.set_artifact(slug, ra["kind"], ra, "record", ra["label"])


def _h(obj):
    return hashlib.sha1(json.dumps(obj, sort_keys=True).encode()).hexdigest()[:16]


def ingest(arts, snap):
    """Update artifacts from a telemetry --artifacts payload; queue verification of new found / candidate files."""
    nb = arts.get("nothree_best")
    if nb and nb.get("points"):
        best = ledger.get_best("no-three-in-line-75")
        if not (best and best.get("verified")):
            ledger.set_artifact("no-three-in-line-75", "grid",
                                {"kind": "grid", "n": 75, "points": nb["points"], "violated_lines": nb.get("violated_lines", []),
                                 "count": nb.get("count", len(nb["points"])), "sym": nb.get("sym"), "round": nb.get("round"),
                                 "seed": nb.get("seed"), "file": nb.get("file")},
                                "candidate", f"current SAT model with fewest violated lines ({nb.get('violated')}), not yet valid")
    sp = arts.get("spencer_best") or []
    if sp:
        best = ledger.get_best("spencer-discrepancy")
        if not (best and best.get("beats_record")):
            c = min(sp, key=lambda s: s["bad"] / 2 ** (s["n"] - 1))
            mat = masks_to_matrix(c["rows"], c["n"])
            ledger.set_artifact("spencer-discrepancy", "sign_matrix",
                                {"kind": "sign_matrix", "n": c["n"], "D": c["D"], "matrix": mat, "bad_vectors": c["bad"],
                                 "total_vectors": 2 ** (c["n"] - 1), "seed": c["seed"], "file": c["file"]},
                                "candidate", f"best tabu matrix for n={c['n']} D={c['D']}: {c['bad']} sign vectors still below D")
        # queue official scoring of our best spencer matrices (a valid construction; score = disc/sqrt(n))
        cands = []
        for c in sp:
            mat = masks_to_matrix(c["rows"], c["n"])
            cands.append({"solution": {"matrix": mat}, "label": f"n={c['n']} D={c['D']} seed={c['seed']}", "file": c["file"]})
        threading.Thread(target=_score_candidates, args=("spencer-discrepancy", cands), daemon=True).start()
    from . import critic
    found = arts.get("found") or {}
    for path in found:
        critic.queue_found(path)
    for fam, files in (arts.get("best_files") or {}).items():
        items = files.items() if isinstance(files, dict) else [(f, 0) for f in files]
        for path, mt in sorted(items, key=lambda kv: -kv[1])[:4]:
            critic.queue_found(path, candidate=True, mtime=mt)


def _score_candidates(slug, cands):
    """Score valid-but-not-record constructions with the official verifier; keep our best as `ours`."""
    if not _verify_lock.acquire(blocking=False):
        return
    try:
        done = ledger.kv_get(f"scored_{slug}", {}) or {}
        for c in cands:
            h = _h(c["solution"])
            if h in done:
                continue
            r = verify(slug, c["solution"])
            done[h] = r.get("score")
            ledger.kv_set(f"scored_{slug}", done)
            if not r["ok"]:
                continue
            best = ledger.get_best(slug)
            P = config.PROBLEMS[slug]
            better = best is None or best.get("score") is None or (
                r["score"] > best["score"] if P["scoring"] == "maximize" else r["score"] < best["score"])
            if better:
                beats = config.beats_record(slug, r["score"])
                ledger.set_best(slug, r["score"], True, c["solution"], None, c.get("file"), beats)
                events.log(f"{slug}: official verifier scores our best construction ({c['label']}) at {r['score']:.6f}")
                did = ledger.add_decision(
                    ledger.max_cycle(), "critic", "record" if beats else "verified", slug,
                    {"path": c.get("file"), "score": r["score"], "record": P["record"], "label": c["label"]},
                    f"Official verifier ({slug}/verifier.py) scored our best search matrix ({c['label']}) at "
                    f"{r['score']:.6f}: {'RECORD' if beats else 'valid, below the record'} (leaderboard top "
                    f"{P['record']} by {P['holder']}).",
                    outcome={"observed": r["score"], "verdict": "confirmed" if beats else "n/a",
                             "note": "RECORD" if beats else "our best valid construction"})
                events.publish("decision", ledger.get_decision(did))
                if beats:
                    events.publish("record", {"slug": slug, "score": r["score"], "verified": True})
    finally:
        _verify_lock.release()
