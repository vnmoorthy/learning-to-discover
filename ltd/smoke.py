"""Read-only smoke test against a running server: python3 -m ltd.smoke [base_url]

Hits every GET endpoint, checks the contract keys, reads 3 SSE events. Never mutates anything.
"""
import json
import sys
import time

import httpx

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8787"
SLUGS = ["no-three-in-line-75", "spencer-discrepancy", "hadamard-det-51", "sidon-45-set", "two-deletion-code-16",
         "snake-in-the-box-13", "ring-loading-15"]


def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")
    return ok


def main():
    c = httpx.Client(base_url=BASE, timeout=30)
    ok = True
    t = time.time()
    s = c.get("/api/state").json()
    ok &= check("GET /api/state", {"now", "loop", "compute", "problems", "totals"} <= set(s),
                f"{(time.time() - t) * 1000:.0f} ms, loop={s['loop']['status']}/{s['loop']['phase']} cycle={s['loop']['cycle']} box={s['compute']['box']}")
    ps = s["problems"][0]
    ok &= check("ProblemSummary keys", {"slug", "title", "scoring", "record", "ours", "beats_record", "metric", "status",
                                       "compute", "strategies"} <= set(ps))
    for slug in SLUGS:
        r = c.get(f"/api/problems/{slug}")
        d = r.json()
        ok &= check(f"GET /api/problems/{slug}", r.status_code == 200 and {"description_md", "leaderboard", "metric_history",
                                                                          "artifact", "templates"} <= set(d),
                    f"status={d.get('status')} metric={d.get('metric', {}).get('value')} artifact={(d.get('artifact') or {}).get('kind')}"
                    f"/{(d.get('artifact') or {}).get('source')} strategies={len(d.get('strategies', []))}")
    ok &= check("GET /api/problems/unknown -> 404", c.get("/api/problems/nope").status_code == 404)
    d = c.get("/api/decisions", params={"limit": 5}).json()
    ok &= check("GET /api/decisions", isinstance(d, list) and (not d or {"id", "cycle", "agent", "action", "rationale",
                                                                          "prediction", "outcome", "sources"} <= set(d[0])), f"{len(d)} rows")
    for path, keys in (("/api/memory", {"facts", "agents", "links", "benchmark"}),):
        m = c.get(path).json()
        ok &= check(f"GET {path}", keys <= set(m), f"{len(m['facts'])} facts, {len(m['links'])} links")
    for path in ("/api/literature", "/api/sandboxes", "/api/gallery"):
        v = c.get(path).json()
        ok &= check(f"GET {path}", isinstance(v, list), f"{len(v)} rows")
    lr = c.get("/api/learning").json()
    ok &= check("GET /api/learning", {"status", "base_model", "problem", "steps", "eval", "best"} <= set(lr), lr.get("status"))
    n, evs = 0, []
    with c.stream("GET", "/api/events", timeout=20) as r:
        for line in r.iter_lines():
            if line.startswith("event:"):
                evs.append(line.split(":", 1)[1].strip()); n += 1
                if n >= 2:
                    break
    ok &= check("GET /api/events (SSE)", "phase" in evs and "telemetry" in evs, ",".join(evs))
    print("ALL PASS" if ok else "SOME FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
