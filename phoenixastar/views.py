"""API response builders (shared by the live server and the static snapshot). Shapes follow SPEC section 4."""
import json
import os

from . import config, ledger, memory, monitor, planner, strategies


def _ours(slug):
    b = ledger.get_best(slug)
    if not b or b.get("score") is None:
        return None
    return {"score": b["score"], "verified": bool(b["verified"]), "at": b["time"], "strategy_id": b.get("strategy_id")}


def problem_summary(slug, an=None):
    an = an or planner.analyze()
    P = config.PROBLEMS[slug]
    a = an["problems"][slug]
    ours = _ours(slug)
    procs = [p for p in an["procs"] if p["problem"] == slug]
    foreign = [p for p in an["foreign"] if p["problem"] == slug]
    strat = []
    for p in sorted(procs, key=lambda p: p.get("started_at") or ""):
        rec = ledger.get_strategy(p["id"]) or {}
        strat.append({"id": p["id"], "template": p["template"], "params": p["params"], "resource": p["resource"],
                      "started_at": rec.get("started_at") or p.get("started_at"), "adopted": bool(p.get("adopted")),
                      "metric_value": p.get("metric_value"), "gpu": p.get("gpu"), "pid": p.get("pid"),
                      "improve_age_min": round(p["improve_age_s"] / 60, 1) if p.get("improve_age_s") is not None else None})
    try:
        from . import fleet
        modal_runs = fleet.runs(slug)
    except Exception:  # noqa: BLE001
        modal_runs = []
    for r in modal_runs:
        strat.append({k: r.get(k) for k in ("id", "template", "params", "resource", "started_at", "adopted", "metric_value",
                                              "gpu", "pid")} | {"where": "modal", "improve_age_min": None})
    out = {"slug": slug, "title": P["title"], "scoring": P["scoring"],
           "record": {"score": P["record"], "holder": P["holder"]},
           "ours": ours, "beats_record": bool(ours and ours["verified"] and config.beats_record(slug, ours["score"])),
           "metric": {"name": a["metric"], "value": a["value"], "target": a["target"], "lower_is_better": a["lower_is_better"]},
           "status": a["status"],
           "compute": {"gpus": a["gpus"], "cpu_procs": len(procs) + len(foreign), "share": a["share"],
                       "modal_containers": len(modal_runs)},
           "strategies": strat,
           # extras (not in the minimal contract, safe to ignore)
           "metric_detail": {"by_target": a["sub"], "secondary": a.get("extra") or {},
                             "best_age_min": a["best_age_min"] and round(a["best_age_min"], 1),
                             "rate_1h": a["rate_1h"], "priority": a["priority"]},
           "active": P["active"]}
    if slug == "no-three-in-line-75":
        out["classes"] = sorted(an["classes"].values(), key=lambda c: c["sym"])
    if slug in planner.KNOWN_NEGATIVE:
        out["known_negative"] = planner.KNOWN_NEGATIVE[slug]
    if foreign:
        out["foreign_procs"] = len(foreign)
    return out


def state(loop_view):
    an = planner.analyze()
    probs = [problem_summary(s, an) for s, P in config.PROBLEMS.items()]
    probs.sort(key=lambda p: (not p["active"], p["slug"] not in config.ACTIVE, config.ACTIVE.index(p["slug"]) if p["slug"] in config.ACTIVE else 99))
    return {"now": ledger.now(), "loop": loop_view, "compute": monitor.compute(), "problems": probs, "totals": totals()}


def totals():
    one = lambda sql: (ledger.q(sql) or [{"c": 0}])[0]["c"] or 0  # noqa: E731
    sandboxes = 0
    try:
        from . import sandboxes as sb
        sandboxes = len(sb.list_runs(limit=100000))
    except Exception:  # noqa: BLE001
        pass
    return {"decisions": one("SELECT COUNT(*) c FROM decisions"),
            "cycles": one("SELECT MAX(cycle) c FROM decisions"),
            "experiments_run": one("SELECT COUNT(*) c FROM strategies WHERE test=0"),
            "sandboxes_run": sandboxes,
            "facts": one("SELECT COUNT(*) c FROM facts"),
            "sources": one("SELECT COUNT(*) c FROM literature"),
            "records": one("SELECT COUNT(*) c FROM bests WHERE beats_record=1 AND verified=1")}


def problem_detail(slug):
    if slug not in config.PROBLEMS:
        return None
    out = problem_summary(slug)
    try:
        out["description_md"] = open(os.path.join(config.PROBLEMS_DIR, slug, "description.md")).read()
    except OSError:
        out["description_md"] = ""
    out["leaderboard"] = [{"rank": i + 1, "agent": r.get("agentName"), "score": float(r["score"])}
                          for i, r in enumerate(config.load_leaderboard(slug))]
    out["metric_history"] = ledger.metric_history(slug, config.PROBLEMS[slug]["metric"])
    out["artifact"] = ledger.get_artifact(slug)
    out["templates"] = [{"name": n, "resource": t.get("resource", "cpu"), "params": strategies.public_params(t)}
                        for n, t in sorted(strategies.for_problem(slug).items())]
    return out


def literature(problem=None):
    return ledger.literature(problem)


def learning():
    try:
        from . import learning as lr  # owned by another builder
        st = lr.status()
        if isinstance(st, dict):
            return st
    except Exception as e:  # noqa: BLE001
        err = f"phoenixastar.learning unavailable: {type(e).__name__}: {e}"
    else:
        err = "phoenixastar.learning.status() returned no data"
    saved = ledger.learning_get("learning_status")
    if saved:
        return saved
    return {"status": "idle", "base_model": "Qwen/Qwen3-8B", "problem": "sidon-45-set", "steps": [], "eval": None,
            "best": None, "error": err}


def sandboxes(limit=100):
    try:
        from . import sandboxes as sb  # owned by another builder
        return sb.list_runs(limit=limit)
    except Exception:  # noqa: BLE001
        return []


def gallery():
    path = os.path.join(config.GALLERY_DIR, "gallery.json")
    try:
        items = json.load(open(path))
        if isinstance(items, list):
            return items
    except (OSError, ValueError):
        pass
    out = []
    if os.path.isdir(config.GALLERY_DIR):
        for f in sorted(os.listdir(config.GALLERY_DIR)):
            ext = f.rsplit(".", 1)[-1].lower()
            if ext in ("png", "jpg", "jpeg", "webp", "gif", "mp4", "webm", "mov"):
                out.append({"title": f.rsplit(".", 1)[0].replace("_", " ").replace("-", " "), "src": f"/gallery/{f}",
                            "kind": "video" if ext in ("mp4", "webm", "mov") else "image", "made_with": "", "caption": ""})
    return out


def memory_view():
    return memory.api_view()


def physics():
    """The lab's science domains beyond EinsteinArena: three-body periodic orbits and EVENT HORIZON."""
    out = {"threebody": None, "event_horizon": None}
    slug = "three-body-periodic-orbits"
    meta = config.load_meta(slug)
    b = ledger.get_best(slug) or {}
    orbits = ((b.get("solution") or {}).get("orbits")) or []
    try:
        cat = json.load(open(os.path.join(config.PROBLEMS_DIR, slug, "catalog.json")))
        n_cat = len(cat.get("orbits") or cat.get("entries") or []) if isinstance(cat, dict) else len(cat)
        not_checked = cat.get("not_included") if isinstance(cat, dict) else None
    except (OSError, ValueError):
        n_cat, not_checked = 2060, None
    out["threebody"] = {"title": meta.get("title"), "score": b.get("score"), "verified": bool(b.get("verified")),
                        "time": b.get("time"), "orbits": orbits, "catalog_entries": n_cat or 2060,
                        "not_checked": not_checked, "image": "/gallery/threebody_candidates.png",
                        "verification": meta.get("verification"), "novelty": meta.get("novelty"),
                        "caveats": meta.get("caveats")}
    p = os.path.join(config.ROOT, "domains", "event-horizon", "results", "dashboard.json")
    try:
        eh = json.load(open(p))
        for f in eh.get("figures") or []:
            f["src"] = "/gallery/event-horizon/" + os.path.basename(f.get("path") or "")
        out["event_horizon"] = eh
    except (OSError, ValueError):
        out["event_horizon"] = None
    return out
