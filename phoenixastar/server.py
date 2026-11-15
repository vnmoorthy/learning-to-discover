"""FastAPI server: the API of SPEC section 4, SSE events, the built frontend (web/dist) and /gallery.

python3 -m phoenixastar.server   ->  http://127.0.0.1:8787
Env: PHOENIX_LOOP_AUTOSTART=0 starts with the loop paused; PHOENIX_TEST_MODE=1 gives launches test- ids and dry-runs stops.
"""
import asyncio
import json
import mimetypes
import os
import re
import threading
import time

from fastapi import Body, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, Response, StreamingResponse
from sse_starlette.sse import EventSourceResponse

from . import artifacts, box, config, events, ledger, loop as loopmod, memory, monitor, planner, strategies, views

app = FastAPI(title="Phoenixastar", version="1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
                   allow_methods=["*"], allow_headers=["*"])
_started = {"v": False}


def _poller():
    ok, msg = box.sync_code(force=True)
    events.log(f"code sync to box: {msg}", "info" if ok else "warn")
    last_art = 0.0
    while True:
        t0 = time.time()
        try:
            want_art = time.time() - last_art > config.ARTIFACT_POLL_S
            if monitor.poll(loopmod.get().cycle, artifacts=want_art) is not None and want_art:
                last_art = time.time()
                from . import critic
                critic.process_queue(loopmod.get().cycle, budget_s=120)
        except Exception as e:  # noqa: BLE001
            events.log(f"poller error: {e}", "warn")
        time.sleep(max(2.0, config.TELEMETRY_POLL_S - (time.time() - t0)))


def _instance_lock():
    """One autonomous loop per database: a second server on the same DB (another port, a stray terminal) would
    otherwise double every kill and launch on the box. Returns True when this process owns the loop."""
    import fcntl
    try:
        fh = open(config.DB_PATH + ".loop.lock", "a+")
        fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        return False
    fh.seek(0); fh.truncate(); fh.write(f"{os.getpid()} port {config.PORT}\n"); fh.flush()
    _started["lock"] = fh          # keep the handle (and the lock) for the life of the process
    return True


@app.on_event("startup")
def _startup():
    if _started["v"]:
        return
    _started["v"] = True
    ledger.conn()
    artifacts.ensure_defaults()
    monitor.restore_from_db()
    lp = loopmod.get()
    if not _instance_lock():
        # read-only instance: serves the API from the DB, never polls/reconciles, launches, stops or runs cycles
        lp.lock_out("another phoenixastar.server already runs the loop on this database (this instance is read-only)")
    else:
        threading.Thread(target=_poller, name="ltd-telemetry", daemon=True).start()
    lp.start()
    events.log(f"server up; loop {lp.status}, interval {config.LOOP_INTERVAL_S}s, test_mode={loopmod.TEST_MODE}"
               + (f"; LOOP DISABLED: {lp.locked_out}" if lp.locked_out else ""), "warn" if lp.locked_out else "info")


# ------------------------------------------------------------------ read API
@app.get("/api/state")
def get_state():
    return views.state(loopmod.get().view())


@app.get("/api/problems/{slug}")
def get_problem(slug: str):
    d = views.problem_detail(slug)
    if d is None:
        return JSONResponse({"error": f"unknown problem {slug}"}, status_code=404)
    return d


@app.get("/api/decisions")
def get_decisions(problem: str | None = None, agent: str | None = None, limit: int = 100, before: int | None = None):
    return ledger.decisions(problem, agent, max(1, min(limit, 1000)), before)


@app.get("/api/memory")
def get_memory():
    return views.memory_view()


@app.get("/api/literature")
def get_literature(problem: str | None = None):
    return views.literature(problem)


@app.get("/api/learning")
def get_learning():
    return views.learning()


@app.get("/api/sandboxes")
def get_sandboxes(limit: int = 100):
    return views.sandboxes(limit)


@app.get("/api/gallery")
def get_gallery():
    return views.gallery()


@app.get("/api/physics")
def get_physics():
    return views.physics()


@app.get("/api/events")
async def sse(request: Request):
    qu = events.subscribe()

    async def gen():
        try:
            lp = loopmod.get()
            yield {"event": "phase", "data": json.dumps({"phase": lp.phase, "cycle": lp.cycle})}
            yield {"event": "telemetry", "data": json.dumps(monitor.telemetry_event(), default=str)}
            while True:
                if await request.is_disconnected():
                    break
                try:
                    ev, data = await asyncio.wait_for(qu.get(), timeout=15)
                except asyncio.TimeoutError:
                    continue
                yield {"event": ev, "data": json.dumps(data, default=str)}
        finally:
            events.unsubscribe(qu)

    return EventSourceResponse(gen(), ping=15)


# ------------------------------------------------------------------ loop control
@app.post("/api/loop/pause")
def loop_pause():
    loopmod.get().pause()
    return {"ok": True, "loop": loopmod.get().view()}


@app.post("/api/loop/resume")
def loop_resume():
    lp = loopmod.get()
    lp.resume()
    return {"ok": not lp.locked_out, "loop": lp.view(), **({"error": lp.locked_out} if lp.locked_out else {})}


@app.post("/api/loop/run-now")
def loop_run_now():
    lp = loopmod.get()
    lp.run_now()
    return {"ok": not lp.locked_out, "loop": lp.view(), **({"error": lp.locked_out} if lp.locked_out else {})}


# ------------------------------------------------------------------ actions
def _solution_from_artifact(slug, a):
    if not a:
        return None
    k = a.get("kind")
    if k == "grid":
        return {"points": a["points"]}
    if k == "sign_matrix":
        return {"matrix": a["matrix"]}
    if k == "integer_set":
        return {"elements": a["elements"]}
    if k == "code":
        return {"words": a["words"]}
    return a.get("solution")


@app.post("/api/problems/{slug}/verify")
def verify(slug: str):
    if slug not in config.PROBLEMS:
        return {"ok": False, "score": None, "beats_record": False, "error": f"unknown problem {slug}", "seconds": 0.0}
    best = ledger.get_best(slug)
    if best and best.get("solution"):
        sol, source = best["solution"], "ours"
    else:
        art = ledger.get_artifact(slug)
        sol, source = _solution_from_artifact(slug, art), (art or {}).get("source", "none")
    if not sol:
        return {"ok": False, "score": None, "beats_record": False, "error": "no solution to verify yet", "seconds": 0.0,
                "source": None}
    r = artifacts.verify(slug, sol)
    beats = bool(r["ok"] and source == "ours" and config.beats_record(slug, r["score"]))
    did = ledger.add_decision(loopmod.get().cycle, "critic", "verify", slug, {"source": source, "score": r.get("score")},
                              f"On-demand official verification of our current {source} solution: "
                              f"{'score ' + str(r['score']) if r['ok'] else 'invalid: ' + str(r['error'])}"
                              f"{' (this is the record holder' + chr(39) + 's construction, not ours)' if source == 'record' else ''}.",
                              outcome={"observed": r.get("score"), "verdict": "n/a", "note": source})
    events.publish("decision", ledger.get_decision(did))
    return {"ok": bool(r["ok"]), "score": r.get("score"), "beats_record": beats, "error": r.get("error"),
            "seconds": r.get("seconds", 0.0), "source": source}


_launch_lock = threading.Lock()


@app.post("/api/strategies")
def launch_strategy(body: dict = Body(...)):
    # one manual launch at a time: two quick clicks must not both pick the same "free" GPU or seed
    if not _launch_lock.acquire(timeout=90):
        return {"ok": False, "id": None, "error": "another launch is in progress; try again"}
    try:
        return _launch_strategy(body)
    except Exception as e:  # noqa: BLE001 - never a 500 for the UI form
        return {"ok": False, "id": None, "error": f"{type(e).__name__}: {str(e)[:300]}"}
    finally:
        _launch_lock.release()


def _launch_strategy(body):
    if loopmod.get().locked_out:
        return {"ok": False, "id": None, "error": loopmod.get().locked_out}
    slug, tpl, raw = body.get("problem"), body.get("template"), body.get("params")
    if raw is not None and not isinstance(raw, dict):
        return {"ok": False, "id": None, "error": "params must be a JSON object"}
    params = dict(raw or {})
    try:
        t = strategies.get(tpl)
        if t.get("problem") != slug:
            raise ValueError(f"template {tpl} is for {t.get('problem')}, not {slug}")
        if "seed" in (t.get("params") or {}) and ("seed" not in params or params["seed"] in planner.used_seeds(tpl)):
            params["seed"] = planner.fresh_seed(tpl, set())
        params = strategies.validate(tpl, params)
    except ValueError as e:
        return {"ok": False, "id": None, "error": str(e)}
    test = bool(body.get("test")) or loopmod.TEST_MODE     # test mode: every manual launch is a test- run too
    want = body.get("id")
    if want is not None and not re.fullmatch(r"[A-Za-z0-9_.-]{1,70}", str(want)):
        return {"ok": False, "id": None, "error": "bad id"}
    if want and test and not str(want).startswith("test-"):
        want = f"test-{want}"[:70]
    sid = want if want and not ledger.get_strategy(want) else planner.make_id(tpl, params, test=test)
    bud = monitor.budget()
    gpu = None
    if t.get("resource") == "gpu":
        gpu = body.get("gpu")
        if gpu is None:
            if not bud["free_gpus"]:
                return {"ok": False, "id": None, "error": f"no free GPU (all {bud['gpus_total']} busy); stop a GPU strategy first"}
            gpu = bud["free_gpus"][0]
        elif isinstance(gpu, bool) or not isinstance(gpu, int) or not 0 <= gpu < bud["gpus_total"]:
            return {"ok": False, "id": None, "error": f"gpu must be an integer 0..{bud['gpus_total'] - 1}"}
        elif gpu not in bud["free_gpus"] and not body.get("force"):
            return {"ok": False, "id": None, "error": f"GPU {gpu} is busy; pick a free one ({bud['free_gpus']}) or pass force"}
    if bud["cores_used"] >= config.CPU_TOTAL - 2 and not body.get("force"):
        return {"ok": False, "id": None, "error": f"box full: {bud['cores_used']} processes on {config.CPU_TOTAL} cores"}
    r = box.launch(sid, tpl, params, gpu=gpu)
    if not r["ok"]:
        return {"ok": False, "id": None, "error": r["error"]}
    ledger.upsert_strategy({"id": sid, "problem": slug, "template": tpl, "params": r["params"],
                            "resource": t.get("resource", "cpu"), "gpu": gpu, "pid": r["pid"], "started_at": ledger.now(),
                            "status": "running", "adopted": 0, "log": f"/home/ubuntu/ltd/{r['log']}",
                            "test": int(sid.startswith("test-"))})
    did = ledger.add_decision(loopmod.get().cycle, "executor", "launch", slug,
                              {"template": tpl, "params": r["params"], "strategy_ids": [sid], "gpus": [gpu] if gpu is not None else [],
                               "manual": True},
                              f"Manual launch from the UI/API: {sid} (pid {r['pid']}{', GPU ' + str(gpu) if gpu is not None else ''}).")
    events.publish("decision", ledger.get_decision(did))
    threading.Thread(target=monitor.poll, daemon=True).start()
    return {"ok": True, "id": sid, "error": None}


@app.delete("/api/strategies/{sid}")
def stop_strategy(sid: str):
    rec = ledger.get_strategy(sid)
    if not rec:
        return {"ok": False, "error": f"unknown strategy {sid}"}
    if rec.get("status") != "running":
        return {"ok": False, "error": f"strategy {sid} is {rec.get('status')}"}
    if loopmod.get().locked_out:
        return {"ok": False, "error": loopmod.get().locked_out}
    if loopmod.TEST_MODE and not sid.startswith("test-"):
        return {"ok": False, "error": f"test mode: only test- strategies can be stopped ({sid} is a real run)"}
    r = box.stop(sid, rec)
    if r["ok"]:
        ledger.upsert_strategy({"id": sid, "status": "stopped", "stopped_at": ledger.now(), "stop_reason": "manual stop"})
        did = ledger.add_decision(loopmod.get().cycle, "executor", "stop", rec["problem"], {"strategy_ids": [sid], "manual": True},
                                  f"Manual stop from the UI/API: {sid} (pid {rec.get('pid')}).")
        events.publish("decision", ledger.get_decision(did))
        threading.Thread(target=monitor.poll, daemon=True).start()
    return {"ok": bool(r["ok"]), "error": r.get("error")}


@app.post("/api/learning/start")
def learning_start(body: dict = Body(default={})):
    try:
        steps = int((body or {}).get("steps", 30))
    except (TypeError, ValueError):
        return {"ok": False, "error": "steps must be an integer"}
    try:
        from . import learning as lr
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": f"phoenixastar.learning unavailable: {type(e).__name__}: {e}"}
    try:
        ok = bool(lr.start(steps=steps))
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": f"could not start training: {type(e).__name__}: {str(e)[:300]}"}
    return {"ok": ok, "error": None if ok else "a training run is already in progress"}


@app.post("/api/memory/benchmark")
def memory_benchmark():
    try:
        from . import memory_bench
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": f"phoenixastar.memory_bench unavailable: {type(e).__name__}: {e}"}
    try:
        ok = memory_bench.start_async(memory.all_facts())
    except Exception as e:  # noqa: BLE001 - e.g. too few facts yet
        return {"ok": False, "error": f"could not start the benchmark: {str(e)[:300]}"}
    # start_async returns False (no-op) while a benchmark is already running
    return {"ok": ok is not False, "error": None if ok is not False else "a benchmark is already running"}


@app.post("/api/sandboxes/run")
def sandboxes_run(body: dict = Body(...)):
    slug = body.get("problem")
    try:
        n = max(1, min(int(body.get("n") or 4), 32))
    except (TypeError, ValueError):
        return {"ok": False, "error": "n must be an integer"}
    if slug not in config.PROBLEMS:
        return {"ok": False, "error": f"unknown problem {slug}"}
    try:
        from . import sandboxes
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": f"phoenixastar.sandboxes unavailable: {type(e).__name__}: {e}"}
    try:
        a = planner.analyze()["problems"][slug]
        ctx = f"{config.PROBLEMS[slug]['title']}: record {config.PROBLEMS[slug]['record']}; live {a['metric']}={a['value']}"
        sandboxes.start_batch_async(slug, n, context=ctx)
    except Exception as e:  # noqa: BLE001 - unsupported problem, too many batches running, ...
        return {"ok": False, "error": f"{type(e).__name__}: {str(e)[:300]}"}
    did = ledger.add_decision(loopmod.get().cycle, "sandbox", "start_batch", slug, {"n": n, "manual": True},
                              f"Manual request: {n} Modal sandbox programs for {slug}.")
    events.publish("decision", ledger.get_decision(did))
    return {"ok": True}


@app.get("/api/health")
def health():
    return {"ok": True, "box": box.status(), "memory": memory.status(), "loop": loopmod.get().view(),
            "templates": sorted(strategies.templates())}


# ------------------------------------------------------------------ static files
def _ranged_file(request, f):
    """FileResponse with HTTP Range support (Safari will not play an mp4 <video> without 206 responses)."""
    size = os.path.getsize(f)
    m = re.fullmatch(r"bytes=(\d*)-(\d*)", (request.headers.get("range") or "").strip())
    if not m or not (m.group(1) or m.group(2)):
        return FileResponse(f, headers={"Accept-Ranges": "bytes"})
    if m.group(1):
        start, end = int(m.group(1)), (int(m.group(2)) if m.group(2) else size - 1)
    else:                                   # suffix range: the last N bytes
        start, end = max(0, size - int(m.group(2))), size - 1
    end = min(end, size - 1)
    if start > end:
        return Response(status_code=416, headers={"Content-Range": f"bytes */{size}"})

    def body():
        with open(f, "rb") as fh:
            fh.seek(start)
            left = end - start + 1
            while left > 0:
                chunk = fh.read(min(1 << 20, left))
                if not chunk:
                    break
                left -= len(chunk)
                yield chunk
    return StreamingResponse(body(), status_code=206, media_type=mimetypes.guess_type(f)[0] or "application/octet-stream",
                             headers={"Content-Range": f"bytes {start}-{end}/{size}", "Accept-Ranges": "bytes",
                                      "Content-Length": str(end - start + 1)})


@app.get("/{path:path}", include_in_schema=False)
def spa(path: str, request: Request):
    if path.startswith("api/"):
        return JSONResponse({"error": "not found"}, status_code=404)
    if path.startswith("gallery/") and path.strip("/") != "gallery":
        f = os.path.realpath(os.path.join(config.GALLERY_DIR, path[len("gallery/"):]))
        if f.startswith(os.path.realpath(config.GALLERY_DIR) + os.sep) and os.path.isfile(f):
            return _ranged_file(request, f)
        return JSONResponse({"error": "not found"}, status_code=404)
    dist = os.path.realpath(config.WEB_DIST)
    f = os.path.realpath(os.path.join(dist, path))
    if path and f.startswith(dist + os.sep) and os.path.isfile(f):
        return FileResponse(f)
    idx = os.path.join(dist, "index.html")
    if os.path.isfile(idx):
        return FileResponse(idx)
    return JSONResponse({"error": "frontend not built (run npm run build in web/)", "api": "/api/state"}, status_code=404)


def main():
    import uvicorn
    uvicorn.run(app, host=config.HOST, port=config.PORT, log_level="warning")


if __name__ == "__main__":
    main()
