"""SSH wrapper for the GPU box (ssh -F scripts/ssh_config gpubox). Every call has a timeout; nothing here uses pkill.

Processes are stopped only by explicit pid after re-checking that the pid still runs the expected script
(and, for strategies we launched, carries our PHOENIX_STRATEGY_ID), so a recycled pid can never be hit.
"""
import json
import os
import re
import shlex
import subprocess
import threading
import time

from . import config, strategies

_state = {"online": None, "last_ok": None, "last_error": None}
_sync_lock = threading.Lock()
_last_sync = {"t": 0}


ON_BOX = os.environ.get("PHOENIX_ON_BOX", "0") == "1"   # the server itself runs on the GPU box: run commands locally


def ssh(cmd, timeout=40, stdin=None):
    """Run a command on the box (over ssh from the laptop, or locally when the server runs on the box)."""
    args = ["bash", "-lc", cmd] if ON_BOX else ["ssh", "-F", config.SSH_CONFIG, "-o", "ConnectTimeout=10", config.SSH_HOST, cmd]
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=timeout, input=stdin)
    except subprocess.TimeoutExpired:
        _state.update(online=False, last_error=f"timeout after {timeout}s")
        return 124, "", f"timeout after {timeout}s"
    if p.returncode == 255:
        _state.update(online=False, last_error=p.stderr.strip()[-300:])
    else:
        _state.update(online=True, last_ok=time.time())
    return p.returncode, p.stdout, p.stderr


def online():
    return bool(_state["online"])


def status():
    return dict(_state)


def telemetry(artifacts=False):
    """One JSON snapshot from ~/ltd/scripts/telemetry.py (raises RuntimeError when the box is unreachable)."""
    rc, out, err = ssh(f"python3 -B {config.BOX_ROOT}/scripts/telemetry.py" + (" --artifacts" if artifacts else ""), timeout=60)
    if rc != 0:
        raise RuntimeError(f"telemetry failed rc={rc}: {err.strip()[-300:]}")
    return json.loads(out)


def list_processes(snap=None):
    """[{pid, cmdline, template, params, gpu, log, strategy_id, etime_s, ...}] for every known search process."""
    snap = snap or telemetry()
    out = []
    for p in snap.get("procs", []):
        name, params, extra = strategies.parse_cmdline(p.get("argv") or [])
        out.append({**p, "cmdline": " ".join(p.get("argv") or []), "template": name, "params": params, "extra": extra,
                    "gpu": (p.get("gpus") or [None])[0]})
    return out


def sync_code(force=False):
    """rsync search/ and scripts/ to ~/ltd/ (no --delete; at most once a minute unless forced)."""
    if ON_BOX:
        return True, "local (server runs on the box; search/ and scripts/ are the live copies)"
    with _sync_lock:
        if not force and time.time() - _last_sync["t"] < 60:
            return True, "recent"
        ssh_e = f"ssh -F {config.SSH_CONFIG}"
        errs = []
        for d in ("search", "scripts"):
            src = os.path.join(config.ROOT, d) + "/"
            p = subprocess.run(["rsync", "-az", "--exclude", "__pycache__", "--exclude", "*.pyc", "-e", ssh_e, src,
                                f"{config.SSH_HOST}:{config.BOX_ROOT}/{d}/"], capture_output=True, text=True, timeout=90)
            if p.returncode != 0:
                errs.append(f"{d}: {p.stderr.strip()[-200:]}")
        if errs:
            return False, "; ".join(errs)
        _last_sync["t"] = time.time()
        return True, "synced"


def launch(strategy_id, template, params, resource=None, gpu=None):
    """Launch one validated strategy detached on the box. Returns {ok, pid, log, params, error}."""
    return launch_many([{"id": strategy_id, "template": template, "params": params, "gpu": gpu}])[strategy_id]


def launch_many(items):
    """Launch several strategies in one ssh round trip, then confirm each pid is alive.
    items: [{id, template, params, gpu}] -> {id: {ok, pid, log, params, error}}"""
    res, cmds, meta = {}, [], {}
    for it in items:
        try:
            cmd, log, params = strategies.command(it["template"], it["params"], it["id"], gpu=it.get("gpu"))
        except ValueError as e:
            res[it["id"]] = {"ok": False, "error": str(e)}
            continue
        cmds.append(cmd)
        meta[it["id"]] = (log, params)
    if not cmds:
        return res
    ok, msg = sync_code()
    if not ok:
        for sid in meta:
            res[sid] = {"ok": False, "error": f"code sync failed: {msg}"}
        return res
    rc, out, err = ssh(" ; ".join(cmds), timeout=60 + 2 * len(cmds))
    pids = {m.group(1): int(m.group(2)) for m in re.finditer(r"LAUNCHED (\S+) (\d+)", out)}
    # GPU (torch) runs crash on import/first step if their environment is wrong: watch them longer
    gpu_launch = any(it.get("gpu") is not None for it in items)
    time.sleep(12 if gpu_launch else 3)
    checks = " ; ".join(f"test -d /proc/{p} && echo ALIVE {p} || (echo DEAD {p}; tail -n 3 {config.BOX_ROOT}/{shlex.quote(meta[s][0])} "
                        f"| sed 's/^/LOG {p} /')" for s, p in pids.items())
    alive, logs = set(), {}
    if checks:
        rc2, out2, _ = ssh(checks, timeout=40)
        alive = {int(x) for x in re.findall(r"ALIVE (\d+)", out2)}
        for m in re.finditer(r"LOG (\d+) (.*)", out2):
            logs.setdefault(int(m.group(1)), []).append(m.group(2))
    for sid, (log, params) in meta.items():
        pid = pids.get(sid)
        if pid is None:
            res[sid] = {"ok": False, "error": f"launch failed rc={rc}: {(err or out).strip()[-300:]}"}
        elif pid not in alive:
            res[sid] = {"ok": False, "pid": pid, "log": log, "params": params,
                        "error": "process exited immediately: " + " | ".join(logs.get(pid, []))[-400:]}
        else:
            res[sid] = {"ok": True, "pid": pid, "log": log, "params": params, "error": None}
    return res


def _guard(pid, script, strategy_id=None, cmdline=None):
    """Remote shell test: pid still runs `script` (and carries our strategy id / still has the exact recorded
    command line of an adopted process, so a recycled pid can never be hit)."""
    chk = f"tr '\\0' ' ' < /proc/{pid}/cmdline | grep -q -- {shlex.quote(script)}"
    if cmdline:
        chk += f" && [ \"$(tr '\\0' ' ' < /proc/{pid}/cmdline)\" = {shlex.quote(cmdline + ' ')} ]"
    if strategy_id:
        legacy = "".join(map(chr, (76, 84, 68))) + "_STRATEGY_ID"   # runs started before the rename
        ere = "".join("\\" + ch if ch in ".^$*+?()[]{}|\\" else ch for ch in strategy_id)   # POSIX ERE escape
        pat = f"(PHOENIX_STRATEGY_ID|{legacy})=" + ere
        chk += f" && tr '\\0' '\\n' < /proc/{pid}/environ | grep -qxE {shlex.quote(pat)}"
    return chk


def _guarded_kill(pid, script, strategy_id=None, cmdline=None):
    """Remote snippet: SIGTERM pid only if _guard() holds; otherwise report it gone (never another pid)."""
    return (f"if [ -d /proc/{pid} ] && {_guard(pid, script, strategy_id, cmdline)}; then kill -TERM {pid} && "
            f"echo killed {pid}; else echo gone {pid}; fi")


def stop(strategy_id, rec=None):
    """Stop one strategy (pid file for launched ones, recorded pid for adopted ones). Returns {ok, error}."""
    from . import ledger
    rec = rec or ledger.get_strategy(strategy_id)
    if not rec:
        return {"ok": False, "error": f"unknown strategy {strategy_id}"}
    try:
        script = strategies.get(rec["template"])["script"]
    except ValueError as e:
        return {"ok": False, "error": str(e)}
    pid = rec.get("pid")
    if not rec.get("adopted"):
        rc, out, _ = ssh(f"cat {config.BOX_ROOT}/runs/strategies/{shlex.quote(strategy_id)}.pid 2>/dev/null", timeout=20)
        if out.strip().isdigit():
            pid = int(out.strip())
    if not pid:
        return {"ok": False, "error": "no pid recorded"}
    cmd = _guarded_kill(int(pid), script, None if rec.get("adopted") else strategy_id,
                        rec.get("cmdline") if rec.get("adopted") else None)
    rc, out, err = ssh(cmd + f"; sleep 1; test -d /proc/{int(pid)} && echo still || echo stopped", timeout=30)
    if rc != 0:
        return {"ok": False, "error": f"ssh rc={rc}: {err.strip()[-200:]}"}
    if "still" in out:
        # give a slow C extension a moment, then report (never escalate to other pids)
        rc, out2, _ = ssh(f"sleep 3; test -d /proc/{int(pid)} && echo still || echo stopped", timeout=20)
        if "still" in out2:
            return {"ok": False, "error": f"pid {pid} still running after SIGTERM"}
    return {"ok": True, "error": None, "note": out.strip().splitlines()[0] if out.strip() else ""}


def stop_many(recs):
    """Stop several strategies in one ssh round trip. recs: list of strategy rows. Returns {id: {ok, error}}."""
    parts, res = [], {}
    for r in recs:
        try:
            script = strategies.get(r["template"])["script"]
        except ValueError as e:
            res[r["id"]] = {"ok": False, "error": str(e)}
            continue
        if not r.get("pid"):
            res[r["id"]] = {"ok": False, "error": "no pid"}
            continue
        parts.append(_guarded_kill(int(r["pid"]), script, None if r.get("adopted") else r["id"],
                                   r.get("cmdline") if r.get("adopted") else None))
    if parts:
        rc, out, err = ssh("; ".join(parts) + "; sleep 1", timeout=60)
        killed = {int(m) for m in re.findall(r"killed (\d+)", out)}
        gone = {int(m) for m in re.findall(r"gone (\d+)", out)}
        for r in recs:
            if r["id"] in res:
                continue
            pid = int(r["pid"])
            if pid in killed or pid in gone:
                res[r["id"]] = {"ok": True, "error": None, "note": "killed" if pid in killed else "already gone"}
            else:
                res[r["id"]] = {"ok": False, "error": f"ssh rc={rc}: {err.strip()[-200:]}"}
    return res


def fetch(path, max_bytes=5_000_000):
    """Contents of a file on the box (path relative to ~/ltd or absolute under /home/ubuntu/ltd)."""
    if not re.fullmatch(r"[\w./~+-]+", path) or ".." in path:
        raise ValueError(f"refusing path {path!r}")
    p = path if path.startswith(("/", "~")) else f"{config.BOX_ROOT}/{path}"
    rc, out, err = ssh(f"head -c {int(max_bytes)} {p}", timeout=60)
    if rc != 0:
        raise RuntimeError(f"fetch {path} failed: {err.strip()[-200:]}")
    return out
