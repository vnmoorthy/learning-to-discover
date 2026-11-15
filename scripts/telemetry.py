"""Runs on the GPU box: one JSON snapshot of every search (best score, progress, liveness, found files).

Read-only: it only lists processes, reads logs / proc files and calls nvidia-smi.
  python3 -B ~/ltd/scripts/telemetry.py              # snapshot
  python3 -B ~/ltd/scripts/telemetry.py --artifacts  # snapshot + best artifacts (no-three model, spencer rows, found files)

Output (superset of the original format):
  {time, problems:{slug:{runs|classes, found:[paths], procs}}, gpus:[{idx,util,mem,uuid,pids}], load1, cpus,
   procs:[{pid, ppid, script, argv, cuda, gpus, etime_s, pcpu, strategy_id, log, cwd, family, log_info}],
   logs:{path: {family, mtime, size, ...parsed}}, other_busy, families}
"""
import glob, json, os, re, subprocess, sys, time

HOME = os.path.expanduser("~/ltd")
R = os.path.join(HOME, "runs")
BUILTIN = {"spencer": "spencer-discrepancy", "hadamard": "hadamard-det-51", "nothree": "no-three-in-line-75"}
SCRIPTS = {"spencer_gpu.py": "spencer", "hadamard_gpu.py": "hadamard", "nothree_sat.py": "nothree",
           "sidon_extend.py": "sidon"}


def tail(path, n=200, nbytes=40000):
    try:
        with open(path, "rb") as f:
            f.seek(0, 2); size = f.tell(); f.seek(max(0, size - nbytes))
            return f.read().decode(errors="ignore").splitlines()[-n:]
    except OSError:
        return []


def templates():
    """Template registry synced from the Mac (search/TEMPLATES.json); new families come from their out dir."""
    try:
        t = json.load(open(os.path.join(HOME, "search", "TEMPLATES.json")))
        return {k: v for k, v in t.items() if isinstance(v, dict) and v.get("script")}
    except (OSError, ValueError):
        return {}


def families(tpl):
    fam = dict(BUILTIN)
    for name, t in tpl.items():
        out = (t.get("out") or "").strip("/")
        if out.startswith("runs/"):
            f = out[5:].split("/")[0]
            if f and t.get("problem"):
                fam.setdefault(f, t["problem"])
        SCRIPTS.setdefault(os.path.basename(t["script"]), (out[5:].split("/")[0] if out.startswith("runs/") else name))
    return fam


KV = re.compile(r"([A-Za-z_][\w]*)=(-?\d+(?:\.\d+)?(?:e-?\d+)?)")


def parse_log(path, family):
    """Family-specific parse of one log; every result has t_last (s since process start) when available."""
    st = os.stat(path)
    info = {"family": family, "mtime": st.st_mtime, "size": st.st_size}
    lines = tail(path, 400 if family == "nothree" else 60, 200000 if family == "nothree" else 40000)
    info["last_line"] = lines[-1][-300:] if lines else ""
    info["unsat"] = any("UNSAT" in l for l in lines)
    info["found"] = any(l.startswith("FOUND") or " FOUND " in l for l in lines)
    if family == "spencer":
        for l in reversed(lines):
            m = re.search(r"n=(\d+) D=(\d+) seed=(\d+)\] t=(\d+)s step=(\d+) best_bad=(\d+)", l)
            if m:
                info.update(dict(zip(["n", "D", "seed", "t", "step", "best_bad"], map(int, m.groups()))))
                break
    elif family == "hadamard":
        for l in reversed(lines):
            m = re.search(r"\[s(\d+)\] t=(\d+)s step=(\d+) best_log10=([\d.]+)", l)
            if m:
                info.update({"seed": int(m[1]), "t": int(m[2]), "step": int(m[3]), "best_log10": float(m[4])})
                break
    elif family == "nothree":
        rounds = []
        for l in lines:
            m = re.search(r"\[([\w-]+) s(\d+)\] round (\d+) points=(\d+) violated_lines=(\d+) lines=(\d+) t=(\d+)s", l)
            if m:
                info["sym"], info["seed"] = m[1], int(m[2])
                rounds.append((int(m[3]), int(m[4]), int(m[5]), int(m[6]), int(m[7])))
            else:
                m = re.search(r"\[([\w-]+) s(\d+)\]", l)
                if m and "sym" not in info:
                    info["sym"], info["seed"] = m[1], int(m[2])
        if "sym" not in info:
            name = os.path.basename(path)[:-4]
            if "_s" in name:
                info["sym"], s = name.rsplit("_s", 1)
                info["seed"] = int(s) if s.isdigit() else None
        info["rounds"] = len(rounds)
        if rounds:
            r, pts, v, ln, t = rounds[-1]
            info.update({"round": r, "points": pts, "violated": v, "lines": ln, "t": t})
            best = min(rounds, key=lambda z: (z[2], z[4]))
            info["best_violated"], info["best_t"] = best[2], best[4]
            info["recent"] = [[z[0], z[2], z[4]] for z in rounds[-12:]]
    else:
        # generic convention: last line with key=value numbers (e.g. "best=226 step=.. t=..s")
        for l in reversed(lines):
            kv = KV.findall(l)
            if kv:
                info["values"] = {k: float(v) for k, v in kv}
                m = re.search(r"\bbest=(\d+)/(\d+)=([\d.]+)", l)   # sidon_sa: best=<h>/<n>=<score>
                if m:
                    info["values"].update({"best": float(m[3]), "best_h": float(m[1]), "best_n": float(m[2])})
                m = re.search(r"\bt=(\d+(?:\.\d+)?)s", l)
                if m:
                    info["t"] = float(m[1])
                break
        for l in reversed(lines):  # last JSON line, if the strategy prints JSON
            l = l.strip()
            if l.startswith("{") and l.endswith("}"):
                try:
                    info["json"] = json.loads(l)
                except ValueError:
                    pass
                break
    return info


def proc_table(tpl):
    """All python processes running a known search script, with GPU env, stdout log and cpu use."""
    out = subprocess.run(["ps", "-eo", "pid=,ppid=,etimes=,pcpu=,args="], capture_output=True, text=True).stdout
    procs, other_busy = [], 0
    scripts = set(SCRIPTS)
    for line in out.splitlines():
        parts = line.split(None, 4)
        if len(parts) < 5:
            continue
        pid, ppid, et, pc, args = int(parts[0]), int(parts[1]), int(parts[2]), float(parts[3]), parts[4]
        try:
            argv = open(f"/proc/{pid}/cmdline", "rb").read().decode(errors="ignore").split("\0")
            argv = [a for a in argv if a != ""]
        except OSError:
            continue
        if not argv:
            continue
        script = next((a for a in argv[1:4] if a.endswith(".py") and os.path.basename(a) in scripts), None)
        if not script or not os.path.basename(argv[0]).startswith("python"):
            if pc > 50 and "telemetry.py" not in args:
                other_busy += 1
            continue
        env = {}
        try:
            for kv in open(f"/proc/{pid}/environ", "rb").read().decode(errors="ignore").split("\0"):
                if kv.startswith(("CUDA_VISIBLE_DEVICES=", "LTD_STRATEGY_ID=")):
                    k, v = kv.split("=", 1); env[k] = v
        except OSError:
            pass
        try:
            log = os.readlink(f"/proc/{pid}/fd/1")
        except OSError:
            log = None
        try:
            cwd = os.readlink(f"/proc/{pid}/cwd")
        except OSError:
            cwd = None
        procs.append({"pid": pid, "ppid": ppid, "etime_s": et, "pcpu": pc, "script": script, "argv": argv,
                      "family": SCRIPTS.get(os.path.basename(script)), "cuda": env.get("CUDA_VISIBLE_DEVICES"),
                      "strategy_id": env.get("LTD_STRATEGY_ID"), "log": log, "cwd": cwd, "gpus": []})
    return procs, other_busy


def gpu_table():
    q = subprocess.run(["nvidia-smi", "--query-gpu=index,uuid,utilization.gpu,memory.used", "--format=csv,noheader,nounits"],
                       capture_output=True, text=True).stdout.strip().splitlines()
    gpus, by_uuid = [], {}
    for g in q:
        p = [x.strip() for x in g.split(",")]
        if len(p) < 4:
            continue
        d = {"idx": int(p[0]), "uuid": p[1], "util": int(p[2]), "mem": int(p[3]), "pids": []}
        gpus.append(d); by_uuid[p[1]] = d
    apps = subprocess.run(["nvidia-smi", "--query-compute-apps=pid,gpu_uuid,used_memory", "--format=csv,noheader,nounits"],
                          capture_output=True, text=True).stdout.strip().splitlines()
    for a in apps:
        p = [x.strip() for x in a.split(",")]
        if len(p) >= 2 and p[1] in by_uuid and p[0].isdigit():
            by_uuid[p[1]]["pids"].append(int(p[0]))
    return gpus


def best_nothree():
    best = None
    for f in glob.glob(f"{R}/nothree/latest_*.json"):
        try:
            d = json.load(open(f))
        except (OSError, ValueError):
            continue
        key = (d.get("violated", 1e9), -d.get("count", 0))
        if best is None or key < best[0]:
            best = (key, f, d)
    if not best:
        return None
    d = best[2]; d["file"] = best[1]
    return d


def best_spencer():
    """Best (fewest bad vectors) logged matrix per (n, D) from runs/spencer/log_*.jsonl."""
    out = {}
    for f in glob.glob(f"{R}/spencer/log_n*_D*_s*.jsonl"):
        m = re.search(r"log_n(\d+)_D(\d+)_s(\d+)\.jsonl$", f)
        if not m:
            continue
        n, D, seed = map(int, m.groups())
        for l in reversed(tail(f, 5, 20000)):
            try:
                d = json.loads(l)
            except ValueError:
                continue
            if "rows" not in d:
                continue
            key = (n, D)
            if key not in out or d["bad"] < out[key]["bad"]:
                out[key] = {"n": n, "D": D, "seed": seed, "bad": d["bad"], "rows": d["rows"], "t": d.get("t"),
                            "file": f, "mtime": os.path.getmtime(f)}
            break
    return list(out.values())


def main():
    tpl = templates()
    fam = families(tpl)
    now = time.time()
    snap = {"time": now, "problems": {}, "families": fam}
    logs = {}
    for f, slug in fam.items():
        for p in glob.glob(f"{R}/{f}/*.log"):
            try:
                logs[p] = parse_log(p, f)
            except OSError:
                pass
    procs, other_busy = proc_table(tpl)
    gpus = gpu_table()
    pid_gpu = {pid: g["idx"] for g in gpus for pid in g["pids"]}
    for p in procs:
        if p["pid"] in pid_gpu:
            p["gpus"] = [pid_gpu[p["pid"]]]
        elif p["cuda"] not in (None, ""):
            p["gpus"] = [int(x) for x in p["cuda"].split(",") if x.strip().isdigit()]
        li = logs.get(p["log"]) if p["log"] else None
        if li is None and p["log"] and p["log"].endswith(".log") and os.path.exists(p["log"]):
            try:
                li = parse_log(p["log"], p["family"] or "generic")
                logs[p["log"]] = li
            except OSError:
                li = None
        if li is not None:
            li["pid"] = p["pid"]
        p["log_info"] = li
    snap["procs"] = procs
    snap["other_busy"] = other_busy
    alive_logs = {p["log"] for p in procs if p["log"]}
    for path, li in logs.items():
        li["alive"] = path in alive_logs

    # Back-compatible per-problem summaries.
    def fam_procs(f):
        return sum(1 for p in procs if p["family"] == f)

    sp = [{k: li[k] for k in ("n", "D", "seed", "t", "step", "best_bad") if k in li}
          for path, li in logs.items() if li["family"] == "spencer" and "best_bad" in li]
    snap["problems"]["spencer-discrepancy"] = {"runs": sp, "found": glob.glob(f"{R}/spencer/FOUND*"), "procs": fam_procs("spencer")}
    hd = [{k: li[k] for k in ("seed", "t", "step", "best_log10") if k in li}
          for path, li in logs.items() if li["family"] == "hadamard" and "best_log10" in li]
    snap["problems"]["hadamard-det-51"] = {"runs": hd, "found": glob.glob(f"{R}/hadamard/FOUND*"), "procs": fam_procs("hadamard")}
    nt = {}
    for path, li in logs.items():
        if li["family"] != "nothree" or not li.get("sym"):
            continue
        st = nt.setdefault(li["sym"], {"runs": 0, "alive": 0, "unsat": 0, "found": 0, "v": [], "r": [], "ln": [], "bv": []})
        st["runs"] += 1; st["alive"] += int(li["alive"])
        st["unsat"] += int(li["unsat"]); st["found"] += int(li["found"])
        if "violated" in li:
            st["v"].append(li["violated"]); st["r"].append(li["round"]); st["ln"].append(li["lines"])
            st["bv"].append(li["best_violated"])
    for s in nt.values():
        for k, name in (("r", "rounds"), ("v", "violated"), ("ln", "lines")):
            v = sorted(s.pop(k))
            s[f"{name}_min"] = v[0] if v else None
            s[f"{name}_median"] = v[len(v) // 2] if v else None
        bv = s.pop("bv")
        s["best_violated_ever"] = min(bv) if bv else None
    snap["problems"]["no-three-in-line-75"] = {"classes": nt, "found": glob.glob(f"{R}/nothree/FOUND*"), "procs": fam_procs("nothree")}
    for f, slug in fam.items():
        if slug in snap["problems"]:
            continue
        runs = [dict(li, log=path) for path, li in logs.items() if li["family"] == f]
        snap["problems"].setdefault(slug, {"runs": [], "found": [], "procs": 0})
        snap["problems"][slug]["runs"] += runs
        snap["problems"][slug]["found"] += glob.glob(f"{R}/{f}/FOUND*")
        snap["problems"][slug]["procs"] += fam_procs(f)
    snap["logs"] = logs
    snap["gpus"] = gpus
    snap["load1"] = os.getloadavg()[0]; snap["cpus"] = os.cpu_count()
    if "--artifacts" in sys.argv:
        found = {}
        for f in fam:
            for p in glob.glob(f"{R}/{f}/FOUND*.json"):
                found[p] = os.path.getmtime(p)
        snap["artifacts"] = {"nothree_best": best_nothree(), "spencer_best": best_spencer(), "found": found,
                             "best_files": {f: {p: os.path.getmtime(p) for p in glob.glob(f"{R}/{f}/best*.json")} for f in fam}}
    print(json.dumps(snap))


if __name__ == "__main__":
    main()
