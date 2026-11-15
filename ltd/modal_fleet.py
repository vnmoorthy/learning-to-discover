"""Modal fleet: the lab's elastic compute. Every search strategy runs as a Modal container (A100 or CPU),
logs to the shared Modal Volume `ltd-runs`, and is launched / cancelled by the planner.

  modal deploy ltd/modal_fleet.py           # once (and after search code changes)
  python3 -m ltd.modal_fleet launch nothree_gpu '{"seed":1}'
  python3 -m ltd.modal_fleet telemetry
  python3 -m ltd.modal_fleet cancel <call_id>

Containers get no secrets: the strategies only need numpy/torch/numba/pysat and the problem files.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time

import modal

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_NAME = "ltd-fleet"
app = modal.App(APP_NAME)
vol = modal.Volume.from_name("ltd-runs", create_if_missing=True)


def _with_code(img: modal.Image) -> modal.Image:
    return (img.add_local_dir(os.path.join(ROOT, "search"), "/root/ltd/search")
               .add_local_dir(os.path.join(ROOT, "problems"), "/root/ltd/problems")
               .add_local_file(os.path.join(ROOT, "scripts", "telemetry.py"), "/root/ltd/scripts/telemetry.py"))


cpu_image = _with_code(modal.Image.debian_slim(python_version="3.11").pip_install("numpy", "numba", "python-sat", "sympy"))


def _prepare():
    os.makedirs("/root/ltd", exist_ok=True)
    if not os.path.exists("/root/ltd/runs"):
        os.symlink("/runs", "/root/ltd/runs")
    os.chdir("/root/ltd")


def _run(sid: str, script: str, args: list[str], family: str, seconds: float) -> dict:
    _prepare()
    os.makedirs(f"/runs/{family}", exist_ok=True)
    logp = f"/runs/{family}/{sid}.log"
    log = open(logp, "a", buffering=1)
    env = {**os.environ, "LTD_STRATEGY_ID": sid, "PYTHONUNBUFFERED": "1"}
    t0 = time.time()
    p = subprocess.Popen([sys.executable, "-u", "-B", script] + args, stdout=log, stderr=subprocess.STDOUT, env=env)
    stop = threading.Event()

    def committer():
        while not stop.wait(20):
            try:
                log.flush(); vol.commit()
            except Exception:  # noqa: BLE001
                pass
    th = threading.Thread(target=committer, daemon=True); th.start()
    try:
        while p.poll() is None:
            if time.time() - t0 > seconds:
                p.terminate(); break
            time.sleep(5)
    finally:
        stop.set(); log.flush(); vol.commit()
    return {"id": sid, "returncode": p.returncode, "seconds": round(time.time() - t0, 1), "log": logp}


@app.function(image=cpu_image, volumes={"/runs": vol}, cpu=1.0, memory=4096, timeout=24 * 3600)
def run_cpu(sid: str, script: str, args: list[str], family: str, seconds: float = 6 * 3600) -> dict:
    return _run(sid, script, args, family, seconds)


# GPU containers need a payment method on the Modal account (Starter plan). GPU strategies run on the Lambda box.
GPU_AVAILABLE = False


@app.function(image=cpu_image, volumes={"/runs": vol}, timeout=300)
def telemetry() -> dict:
    """Parse every log and the freshest artifacts on the Volume (same parser as the box telemetry)."""
    _prepare()
    vol.reload()
    sys.path.insert(0, "/root/ltd/scripts")
    import glob
    import telemetry as T  # noqa: N812
    out = {"time": time.time(), "logs": {}, "found": [], "latest": {}}
    for path in glob.glob("/runs/*/*.log"):
        fam = path.split("/")[2]
        try:
            out["logs"][path] = T.parse_log(path, fam)
        except Exception as e:  # noqa: BLE001
            out["logs"][path] = {"family": fam, "error": str(e)[:200]}
    out["found"] = sorted(glob.glob("/runs/*/FOUND*"))
    for path in glob.glob("/runs/*/latest_*.json"):
        try:
            out["latest"][path] = json.load(open(path))
        except Exception:  # noqa: BLE001
            pass
    return out


# ---------------------------------------------------------------- client side (runs on the Mac) ----
def _templates():
    return json.load(open(os.path.join(ROOT, "search", "TEMPLATES.json")))


def build_args(template: str, params: dict) -> tuple[str, list[str], str, str]:
    t = _templates()[template]
    spec = t.get("params", {})
    args = []
    for k, v in params.items():
        if k not in spec:
            raise ValueError(f"unknown param {k} for {template}")
        s = spec[k]
        if s["type"] == "enum" and v not in s["values"]:
            raise ValueError(f"{k} must be one of {s['values']}")
        if s["type"] in ("int", "float"):
            v = int(v) if s["type"] == "int" else float(v)
            if ("min" in s and v < s["min"]) or ("max" in s and v > s["max"]):
                raise ValueError(f"{k}={v} outside [{s.get('min')}, {s.get('max')}]")
        args += [f"--{k}", str(v)]
    family = t["out"].split("/")[1] if t.get("out", "").startswith("runs/") else template
    args += ["--out", f"runs/{family}"]
    return t["script"], args, family, t["resource"]


def launch(template: str, params: dict, sid: str | None = None, seconds: float = 6 * 3600) -> dict:
    script, args, family, resource = build_args(template, params)
    sid = sid or f"{template}-{int(time.time())}-{params.get('seed', 0)}"
    if resource == "gpu" and not GPU_AVAILABLE:
        raise RuntimeError("GPU strategies run on the Lambda box (Modal GPUs need a payment method on this account)")
    fn = modal.Function.from_name(APP_NAME, "run_cpu")
    call = fn.spawn(sid, script, args, family, seconds)
    return {"id": sid, "call_id": call.object_id, "template": template, "params": params, "resource": resource,
            "family": family, "where": "modal", "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}


def cancel(call_id: str) -> bool:
    modal.FunctionCall.from_id(call_id).cancel()
    return True


def fleet_telemetry() -> dict:
    return modal.Function.from_name(APP_NAME, "telemetry").remote()


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "telemetry"
    if cmd == "launch":
        print(json.dumps(launch(sys.argv[2], json.loads(sys.argv[3]) if len(sys.argv) > 3 else {},
                                seconds=float(sys.argv[4]) if len(sys.argv) > 4 else 6 * 3600)))
    elif cmd == "cancel":
        print(cancel(sys.argv[2]))
    else:
        t = fleet_telemetry()
        print(json.dumps({"logs": {k: {kk: vv for kk, vv in v.items() if kk in ("family", "last_line", "t", "best_violated", "values")} for k, v in t["logs"].items()},
                          "found": t["found"]}, indent=1)[:6000])
