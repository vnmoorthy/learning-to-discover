"""Modal fleet bookkeeping: the lab's elastic CPU capacity next to the GPU box.

Runs launched on Modal (by the planner, or bootstrapped from data/modal_fleet_launched.json) are ledger strategies with
ids "modal-<sid>". Their logs live on the Modal Volume `phoenixastar-runs`; a background refresh pulls the parsed logs every
MODAL_POLL_S via the deployed `telemetry` function and checks each FunctionCall for completion.
"""
from __future__ import annotations

import json
import os
import threading
import time

from . import config, events, ledger, strategies

MODAL_POLL_S = int(os.environ.get("PHOENIX_MODAL_POLL", "120"))
MODAL_MAX = int(os.environ.get("PHOENIX_MODAL_MAX", "140"))          # max concurrent planner-managed containers
LAUNCHED = os.path.join(config.DATA, "modal_fleet_launched.json")
_lock = threading.Lock()
_cache = {"t": 0.0, "logs": {}, "found": [], "error": None, "refreshing": False, "done": {}}


def _sid_of(log_path: str) -> str:
    return os.path.basename(log_path)[:-4]


def bootstrap():
    """Register runs launched from the CLI before the loop managed the fleet (idempotent)."""
    try:
        rows = json.load(open(LAUNCHED))
    except (OSError, ValueError):
        return 0
    n = 0
    for r in rows:
        sid = "modal-" + r["id"]
        if ledger.get_strategy(sid):
            continue
        try:
            t = strategies.get(r["template"])
        except ValueError:
            continue
        ledger.upsert_strategy({"id": sid, "problem": t.get("problem"), "template": r["template"], "params": r["params"],
                                "resource": "modal", "gpu": None, "pid": None, "started_at": r.get("started_at") or ledger.now(),
                                "status": "running", "adopted": 0, "cmdline": f"modal call {r.get('call_id')}",
                                "log": f"modal:/runs/{r.get('family')}/{r['id']}.log", "test": 0})
        ledger.kv_set(f"modal_call:{sid}", r.get("call_id"))
        n += 1
    return n


def _refresh():
    try:
        from . import modal_fleet
        t = modal_fleet.fleet_telemetry()
        logs = {f"modal:{p}": li for p, li in (t.get("logs") or {}).items()}
        done = {}
        import modal
        for s in ledger.strategies(status="running"):
            if not str(s["id"]).startswith("modal-"):
                continue
            cid = ledger.kv_get(f"modal_call:{s['id']}")
            if not cid:
                continue
            try:
                modal.FunctionCall.from_id(cid).get(timeout=0)
                done[s["id"]] = "finished"
            except TimeoutError:
                pass
            except Exception as e:  # noqa: BLE001 - cancelled / failed calls
                done[s["id"]] = type(e).__name__
        with _lock:
            _cache.update({"t": time.time(), "logs": logs, "found": t.get("found") or [], "error": None, "done": done})
        try:
            from . import critic
            for fp in t.get("found") or []:
                critic.queue_found("modal:" + fp)      # verified by the official verifier, like box FOUND files
        except Exception as e:  # noqa: BLE001
            events.log(f"queueing modal FOUND files failed: {e}", "warn")
        for sid, why in done.items():
            ledger.upsert_strategy({"id": sid, "status": "exited", "stopped_at": ledger.now(), "stop_reason": f"modal call {why}"})
    except Exception as e:  # noqa: BLE001
        with _lock:
            _cache["error"] = f"{type(e).__name__}: {str(e)[:200]}"
    finally:
        with _lock:
            _cache["refreshing"] = False


def refresh(block=False):
    """Kick a background refresh if the cache is older than MODAL_POLL_S (never blocks the loop unless asked)."""
    with _lock:
        stale = time.time() - _cache["t"] > MODAL_POLL_S
        if not stale or _cache["refreshing"]:
            return
        _cache["refreshing"] = True
    if block:
        _refresh()
    else:
        threading.Thread(target=_refresh, daemon=True).start()


def fetch(path: str, max_bytes: int = 5_000_000) -> str:
    """Read a file from the fleet Volume; path like 'modal:/runs/<family>/<file>'."""
    import modal
    rel = path.removeprefix("modal:").removeprefix("/runs/").lstrip("/")
    if ".." in rel:
        raise ValueError("refusing path")
    vol = modal.Volume.from_name("phoenixastar-runs")
    buf = b""
    for chunk in vol.read_file(rel):
        buf += chunk
        if len(buf) > max_bytes:
            break
    return buf.decode(errors="ignore")


def logs() -> dict:
    with _lock:
        return dict(_cache["logs"])


def runs(problem: str | None = None, status: str = "running") -> list[dict]:
    from .monitor import _metric_of
    lg = logs()
    out = []
    for s in ledger.strategies(status=status):
        if not str(s["id"]).startswith("modal-") or (problem and s["problem"] != problem):
            continue
        li = lg.get(s.get("log") or "", {})
        out.append({"id": s["id"], "template": s["template"], "params": s["params"], "resource": "modal", "where": "modal",
                    "started_at": s.get("started_at"), "adopted": False, "gpu": None, "pid": None,
                    "metric_value": _metric_of(li.get("family") or "", li) if li else None,
                    "last_line": (li.get("last_line") or "")[-160:] if li else None})
    return out


def summary() -> dict:
    rs = runs()
    by = {}
    for r in rs:
        by[r["problem"] if "problem" in r else None] = 0
    by = {}
    for s in ledger.strategies(status="running"):
        if str(s["id"]).startswith("modal-"):
            by[s["problem"]] = by.get(s["problem"], 0) + 1
    with _lock:
        age = time.time() - _cache["t"] if _cache["t"] else None
        err = _cache["error"]
    return {"containers": sum(by.values()), "by_problem": by, "max": MODAL_MAX, "cpu_only": True,
            "telemetry_age_s": round(age, 1) if age is not None else None, "error": err,
            "note": "Modal CPU containers (GPU containers need a payment method on this Modal account)"}


def free_slots() -> int:
    return max(0, MODAL_MAX - summary()["containers"])


def launch(items: list[dict]) -> dict:
    """items: [{id, template, params}] -> {id: {ok, error, call_id, log}}."""
    from . import modal_fleet
    res = {}
    for it in items:
        try:
            r = modal_fleet.launch(it["template"], dict(it["params"]), sid=it["id"].removeprefix("modal-"), seconds=6 * 3600)
            sid = "modal-" + r["id"]
            ledger.kv_set(f"modal_call:{sid}", r["call_id"])
            res[it["id"]] = {"ok": True, "call_id": r["call_id"], "log": f"modal:/runs/{r['family']}/{r['id']}.log",
                             "params": it["params"]}
        except Exception as e:  # noqa: BLE001
            res[it["id"]] = {"ok": False, "error": f"{type(e).__name__}: {str(e)[:200]}"}
    return res


def stop(ids: list[str]) -> dict:
    from . import modal_fleet
    res = {}
    for sid in ids:
        cid = ledger.kv_get(f"modal_call:{sid}")
        if not cid:
            res[sid] = {"ok": False, "error": "no modal call id recorded"}; continue
        try:
            modal_fleet.cancel(cid)
            ledger.upsert_strategy({"id": sid, "status": "stopped", "stopped_at": ledger.now()})
            res[sid] = {"ok": True}
        except Exception as e:  # noqa: BLE001
            res[sid] = {"ok": False, "error": f"{type(e).__name__}: {str(e)[:200]}"}
    return res
