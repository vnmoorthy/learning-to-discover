"""Pull the newest no-three SAT snapshot from the GPU box (READ-ONLY) into viz/data/nothree_latest.json.

One ssh call runs a small read-only Python reader on the box (fed on stdin, nothing is written there): it reads
every ~/ltd/runs/nothree/latest_*.json and returns the one with the fewest violated lines (ties: more points),
plus its path and mtime. The result is validated here before it replaces the local snapshot, and the snapshot
time goes to viz/data/nothree_latest.meta.json so captions can say when it was taken.

If the box is unreachable or the data is bad, the old snapshot is kept and the exit code is 0 (with a WARNING),
so a rebuild before a demo never breaks on the network. Pass --strict to exit 1 instead.

Usage: python3 viz/pull_snapshot.py [--strict]
"""
import datetime, json, os, re, subprocess, sys

VIZ = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(VIZ)
DATA = os.path.join(VIZ, "data")
SNAP = os.path.join(DATA, "nothree_latest.json")
META = os.path.join(DATA, "nothree_latest.meta.json")

# Runs on the box with `python3 -B -`. Read-only: glob + json.load + stat.
REMOTE = r'''
import glob, json, os
best = None
for f in glob.glob(os.path.expanduser("~/ltd/runs/nothree/latest_*.json")):
    try:
        d = json.load(open(f))
        key = (int(d["violated"]), -int(d["count"]), -os.path.getmtime(f))
    except Exception:
        continue
    if best is None or key < best[0]:
        best = (key, f, os.path.getmtime(f), d)
print(json.dumps(None if best is None else {"path": best[1], "mtime": best[2], "data": best[3]}))
'''


def validate(d):
    pts = d["points"]
    assert isinstance(pts, list) and pts, "no points"
    assert all(len(p) == 2 and all(isinstance(c, int) and 0 <= c <= 74 for c in p) for p in pts), "bad point"
    assert len({tuple(p) for p in pts}) == len(pts), "duplicate points"
    assert d["count"] == len(pts), "count != len(points)"
    assert d["violated"] == len(d["violated_lines"]), "violated != len(violated_lines)"
    for k in ("sym", "seed", "round"):
        assert k in d, "missing " + k


def main():
    strict = "--strict" in sys.argv
    cmd = ["ssh", "-F", os.path.join(ROOT, "scripts", "ssh_config"), "-o", "ConnectTimeout=15", "ltd", "python3 -B -"]
    try:
        p = subprocess.run(cmd, input=REMOTE, capture_output=True, text=True, timeout=90)
        if p.returncode != 0:
            raise RuntimeError("ssh rc=%d: %s" % (p.returncode, p.stderr.strip()[-300:]))
        res = json.loads(p.stdout.strip().splitlines()[-1])
        if res is None:
            raise RuntimeError("no latest_*.json snapshots on the box")
        validate(res["data"])
    except Exception as e:  # noqa: BLE001
        print("WARNING: pull failed (%s: %s); keeping the old snapshot" % (type(e).__name__, str(e)[:300]))
        sys.exit(1 if strict else 0)
    d = res["data"]
    taken = datetime.datetime.fromtimestamp(res["mtime"], datetime.timezone.utc)
    meta = {"remote_path": re.sub(r"^/home/[^/]+", "~", res["path"]),
            "taken_utc": taken.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "pulled_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "snapshot": [d["sym"], d["seed"], d["round"]]}  # prep_data.py ignores this file if it does not match
    os.makedirs(DATA, exist_ok=True)
    for path, obj in ((SNAP, d), (META, meta)):
        tmp = path + ".tmp"
        json.dump(obj, open(tmp, "w"))
        os.replace(tmp, path)
    print("pulled %s: %s s%s round %s, %d points, %d violated lines (snapshot %s)" % (
        os.path.basename(res["path"]), d["sym"], d["seed"], d["round"], d["count"], d["violated"], meta["taken_utc"]))


if __name__ == "__main__":
    main()
