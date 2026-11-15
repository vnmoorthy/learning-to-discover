"""Run one Astra-written Blender script headless and log the output.

Usage: python3 viz/render.py <name> [--timeout S] -- <args passed to the bpy script>
  e.g. python3 viz/render.py lattice -- --data viz/data/lattice.json --out viz/renders/hero.png --mode still --res 1920x1080 --samples 64
  <name> is a script in viz/scripts/ (lattice, hadamard_city, snake).
Log: viz/logs/<name>.log. Relative --data/--out paths are made absolute.
On success it writes <out>.stamp.json (sha1 of the --data file) so publish.py can check captions match pixels.
"""
import hashlib, json, os, subprocess, sys, time

VIZ = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(VIZ)
BLENDER = "/Applications/Blender.app/Contents/MacOS/Blender"


def main():
    argv = sys.argv[1:]
    if "--" in argv:
        i = argv.index("--"); mine, rest = argv[:i], argv[i + 1:]
    else:
        mine, rest = argv, []
    name = mine[0]
    timeout = int(mine[mine.index("--timeout") + 1]) if "--timeout" in mine else 900
    for k in ("--data", "--out"):
        if k in rest:
            j = rest.index(k) + 1
            rest[j] = os.path.abspath(os.path.join(ROOT, rest[j]) if not os.path.isabs(rest[j]) else rest[j])
    script = os.path.join(VIZ, "scripts", name + ".py")
    if not os.path.isfile(script):
        sys.exit("render.py: no script %s (have: %s)" % (os.path.relpath(script, ROOT), ", ".join(sorted(
            f[:-3] for f in os.listdir(os.path.join(VIZ, "scripts")) if f.endswith(".py") and ".v" not in f))))
    if "--data" in rest and not os.path.isfile(rest[rest.index("--data") + 1]):
        sys.exit("render.py: no data file %s (run python3 viz/prep_data.py)" % rest[rest.index("--data") + 1])
    # Checks above run before anything is deleted, so a typo never removes a good render.
    out = rest[rest.index("--out") + 1] if "--out" in rest else None
    if out:
        os.makedirs(os.path.dirname(out), exist_ok=True)
        for stale in (out, out + ".stamp.json"):
            if os.path.exists(stale):
                os.remove(stale)  # so a stale file never counts as success
    os.makedirs(os.path.join(VIZ, "logs"), exist_ok=True)
    log = os.path.join(VIZ, "logs", name + ".log")
    cmd = [BLENDER, "-b", "--factory-startup", "-P", script, "--"] + rest
    t = time.time()
    with open(log, "w") as f:
        try:
            p = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, timeout=timeout)
            rc = p.returncode
        except subprocess.TimeoutExpired:
            rc = "timeout"
    dt = time.time() - t
    text = open(log, errors="replace").read()
    failed = rc != 0 or "Traceback" in text or "Error:" in text or (out and not os.path.exists(out))
    print("%s: rc=%s %.1fs out=%s %s" % (name, rc, dt, out, "FAILED" if failed else "ok"))
    if failed:
        lines = [l for l in text.splitlines() if l.strip() and not l.startswith("Fra:")]
        print("\n".join(lines[-25:]))
        sys.exit(1)
    if out and "--data" in rest:
        # Stamp: which data file (by content hash) this render was made from. publish.py refuses to pair a
        # render with a caption computed from different data.
        data = rest[rest.index("--data") + 1]
        stamp = {"data": os.path.relpath(data, ROOT), "data_sha1": sha1(data), "script": name,
                 "script_sha1": sha1(script), "rendered_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        json.dump(stamp, open(out + ".stamp.json", "w"), indent=1)


def sha1(path):
    return hashlib.sha1(open(path, "rb").read()).hexdigest()


if __name__ == "__main__":
    main()
