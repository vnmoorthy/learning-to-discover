"""Static replay export: python3 -m phoenixastar.snapshot  ->  web/public/data/*.json (same shapes as the live API).

Reads only the local DB (no SSH), so it works with the box offline. The state is marked as a snapshot.
"""
import argparse
import json
import os

from . import config, ledger, monitor, views


def _scrub(text):
    """The replay is published: no local filesystem paths (home directory, repo location) in it."""
    home = os.path.expanduser("~")
    for a, b in ((config.ROOT, "<repo>"), (json.dumps(config.ROOT)[1:-1], "<repo>"), (home, "~")):
        if a and len(a) > 1:
            text = text.replace(a, b)
    return text


def write(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        f.write(_scrub(json.dumps(obj, default=str, separators=(",", ":"))))
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=config.SNAPSHOT_OUT)
    ap.add_argument("--decisions", type=int, default=3000)
    a = ap.parse_args()
    ledger.conn()
    monitor.restore_from_db()
    lc = ledger.kv_get("last_cycle", {}) or {}
    loop_view = {"status": "paused", "cycle": ledger.max_cycle(), "phase": "idle", "next_cycle_at": None,
                 "interval_s": config.LOOP_INTERVAL_S, "proposer_model": config.PROPOSER_MODEL,
                 "started_at": lc.get("time") or ledger.now()}
    st = views.state(loop_view)
    st["snapshot"] = {"generated_at": ledger.now(), "label": "replay of a live run", "telemetry_at": st["compute"].get("telemetry_at")}
    st["compute"]["box"] = "offline"
    out = a.out
    write(os.path.join(out, "state.json"), st)
    for slug in config.PROBLEMS:
        write(os.path.join(out, "problems", f"{slug}.json"), views.problem_detail(slug))
    write(os.path.join(out, "decisions.json"), ledger.decisions(limit=a.decisions))
    write(os.path.join(out, "memory.json"), views.memory_view())
    write(os.path.join(out, "literature.json"), views.literature())
    write(os.path.join(out, "learning.json"), views.learning())
    write(os.path.join(out, "sandboxes.json"), views.sandboxes(1000))
    write(os.path.join(out, "gallery.json"), views.gallery())
    write(os.path.join(out, "physics.json"), views.physics())
    # copy of the memory benchmark for the repo (data/snapshot is the only tracked part of data/)
    bench = views.memory_view().get("benchmark")
    if bench and os.path.realpath(out) == os.path.realpath(config.SNAPSHOT_OUT):   # a test export (--out) leaves it alone
        write(os.path.join(config.DATA_SNAPSHOT, "memory_benchmark.json"), bench)
    sizes = {f: os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(out) for f in fs}
    print(json.dumps({"out": out, "files": len(sizes), "bytes": sum(sizes.values()), "decisions": len(ledger.decisions(limit=a.decisions)),
                      "generated_at": st["snapshot"]["generated_at"]}))


if __name__ == "__main__":
    main()
