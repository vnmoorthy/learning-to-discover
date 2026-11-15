"""Turn real artifacts into small, render-ready JSON files in viz/data/.

Inputs (all real, nothing synthesized):
  viz/data/nothree_latest.json            pulled read-only from the GPU box
                                          (~/ltd/runs/nothree/latest_<sym>_s<seed>.json with fewest violated lines)
  problems/no-three-in-line-75/best_solutions.json   record 148-point configuration
  problems/hadamard-det-51/best_solutions.json       record 51x51 +-1 matrix
  problems/spencer-discrepancy/best_solutions.json   record 17x17 sign matrix
  problems/snake-in-the-box-13/best_solutions.json   kgrey's 2950-edge snake

Outputs: viz/data/{lattice,hadamard,spencer,snake}.json

Run: python3 viz/prep_data.py
"""
import json, math, os, sys
from math import gcd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "viz", "data")
PROB = os.path.join(ROOT, "problems")


def best(slug, key=lambda e: e["score"], reverse=True):
    sols = json.load(open(os.path.join(PROB, slug, "best_solutions.json")))
    return sorted(sols, key=key, reverse=reverse)[0]


def clip_line_to_grid(p, q, n=75):
    """Extend the line through lattice points p, q to the [0, n-1]^2 square. Returns two float endpoints."""
    (x1, y1), (x2, y2) = p, q
    dx, dy = x2 - x1, y2 - y1
    g = gcd(abs(dx), abs(dy)) or 1
    dx, dy = dx // g, dy // g
    lo, hi = -1e9, 1e9
    for c, d in ((x1, dx), (y1, dy)):
        if d == 0:
            continue
        a, b = (0 - c) / d, (n - 1 - c) / d
        lo, hi = max(lo, min(a, b)), min(hi, max(a, b))
    return [[x1 + lo * dx, y1 + lo * dy], [x1 + hi * dx, y1 + hi * dy]]


def collinear_lines(pts):
    """Independent recount: every lattice line holding 3+ of the points, as a set of frozensets of points."""
    import collections, itertools
    lines = collections.defaultdict(set)
    for a, b in itertools.combinations(pts, 2):
        dx, dy = b[0] - a[0], b[1] - a[1]
        g = gcd(abs(dx), abs(dy))
        dx, dy = dx // g, dy // g
        if dx < 0 or (dx == 0 and dy < 0):
            dx, dy = -dx, -dy
        lines[(dx, dy, dy * a[0] - dx * a[1])].update((a, b))
    return {frozenset(v) for v in lines.values() if len(v) >= 3}


def snapshot_meta(live):
    """When the box wrote this snapshot (from viz/pull_snapshot.py), or None if unknown / not for this snapshot."""
    try:
        meta = json.load(open(os.path.join(DATA, "nothree_latest.meta.json")))
        if meta.get("snapshot") == [live["sym"], live["seed"], live["round"]]:
            return meta
    except (OSError, ValueError):
        pass
    return None


def lattice():
    live = json.load(open(os.path.join(DATA, "nothree_latest.json")))
    rec = best("no-three-in-line-75")
    pts = [tuple(p) for p in live["points"]]
    ptset = set(pts)
    if len(ptset) != len(pts) or live["count"] != len(pts):
        raise SystemExit("lattice: snapshot point count is inconsistent")
    beams = []
    for (a, b, m) in live["violated_lines"]:
        (x1, y1), (x2, y2) = a, b
        dx, dy = x2 - x1, y2 - y1
        g = gcd(abs(dx), abs(dy)) or 1
        sx, sy = dx // g, dy // g
        # chosen points that lie on this line (walk the whole lattice line)
        on = []
        for t in range(-150, 151):
            x, y = x1 + t * sx, y1 + t * sy
            if 0 <= x < 75 and 0 <= y < 75 and (x, y) in ptset:
                on.append([x, y])
        beams.append({"a": a, "b": b, "m": m, "ends": clip_line_to_grid(a, b), "on": on})
    # Never draw the search's own claim unchecked: recount the collinear lines from the points.
    indep = collinear_lines(pts)
    if indep != {frozenset(map(tuple, b["on"])) for b in beams} or live["violated"] != len(indep):
        raise SystemExit("lattice: violated_lines in the snapshot do not match an independent recount "
                         "(%d recounted vs %d claimed)" % (len(indep), live["violated"]))
    meta = snapshot_meta(live)
    out = {
        "source": "GPU box ~/ltd/runs/nothree/latest_%s_s%d.json (SAT model, round %d)" % (live["sym"], live["seed"], live["round"]),
        "n": 75,
        "sym": live["sym"], "seed": live["seed"], "round": live["round"],
        "count": live["count"], "violated": live["violated"],
        "points": live["points"],
        "violated_lines": beams,
        "record_points": rec["data"]["points"],
        "record_count": rec["score"], "record_holder": rec["agentName"],
        "snapshot_utc": meta["taken_utc"] if meta else None,
    }
    json.dump(out, open(os.path.join(DATA, "lattice.json"), "w"))
    return "lattice: %d pts, %d violated lines (recount agrees), snapshot %s, record %d (%s)" % (
        len(pts), len(beams), out["snapshot_utc"] or "time unknown", rec["score"], rec["agentName"])


def hadamard():
    rec = best("hadamard-det-51")
    M = rec["data"]["matrix"]
    out = {"source": "problems/hadamard-det-51/best_solutions.json", "holder": rec["agentName"],
           "log10_det": rec["score"], "n": len(M), "matrix": M}
    json.dump(out, open(os.path.join(DATA, "hadamard.json"), "w"))
    return "hadamard: %dx%d log10|det|=%.6f (%s)" % (len(M), len(M[0]), rec["score"], rec["agentName"])


def spencer():
    rec = best("spencer-discrepancy")
    M = rec["data"]["matrix"]
    out = {"source": "problems/spencer-discrepancy/best_solutions.json", "holder": rec["agentName"],
           "score": rec["score"], "n": len(M), "matrix": M}
    json.dump(out, open(os.path.join(DATA, "spencer.json"), "w"))
    return "spencer: %dx%d score=%.9f (%s)" % (len(M), len(M[0]), rec["score"], rec["agentName"])


def snake():
    rec = best("snake-in-the-box-13")
    acts = rec["data"]["actions"]
    D = 13
    # Verify it is a real snake (same checks as the official verifier) before drawing it.
    cur, visited, verts = 0, {0}, [0]
    for a in acts:
        nxt = cur ^ (1 << a)
        assert nxt not in visited
        for c in range(D):
            nb = nxt ^ (1 << c)
            assert not (nb in visited and nb != cur), "chord"
        visited.add(nxt); verts.append(nxt); cur = nxt
    # Linear projection R^13 -> R^3: bit i maps to vector v_i, p(v) = sum_i bit_i(v) * v_i.
    # Bits are ranked by how often the snake flips them; the rarest bit gets the longest vector and each
    # more frequent bit is shorter by a factor r, with directions on a Fibonacci sphere. The result shows the
    # snake's real hierarchy: rare flips are long jumps between clusters, frequent flips are local wiggles.
    import collections
    freq = collections.Counter(acts)
    order = sorted(range(D), key=lambda b: freq[b])  # rarest first
    r, gold = 0.68, math.pi * (3 - math.sqrt(5))
    vecs = [None] * D
    for rank, b in enumerate(order):
        y = 1 - 2 * (rank + 0.5) / D
        rr, t = math.sqrt(1 - y * y), gold * rank
        L = r ** rank
        vecs[b] = [math.cos(t) * rr * L, y * L, math.sin(t) * rr * L]
    def proj(v):
        p = [0.0, 0.0, 0.0]
        for i in range(D):
            if v >> i & 1:
                for k in range(3):
                    p[k] += vecs[i][k]
        return p
    P = [proj(v) for v in verts]
    cx = [sum(p[k] for p in P) / len(P) for k in range(3)]
    ext = max(max(abs(p[k] - cx[k]) for p in P) for k in range(3))
    s = 4.0 / ext
    P = [[round((p[k] - cx[k]) * s, 5) for k in range(3)] for p in P]
    # all 8192 cube vertices projected (for faint background dust)
    allv = [[round((c - cx[k]) * s, 4) for k, c in enumerate(proj(v))] for v in range(1 << D)]
    out = {"source": "problems/snake-in-the-box-13/best_solutions.json", "holder": rec["agentName"],
           "edges": len(acts), "dimension": D, "projection_vectors": vecs, "scale": s,
           "path": P, "actions": acts, "cube_vertices": allv}
    json.dump(out, open(os.path.join(DATA, "snake.json"), "w"))
    return "snake: %d edges verified, %d path points (%s)" % (len(acts), len(P), rec["agentName"])


if __name__ == "__main__":
    for f in (lattice, hadamard, spencer, snake):
        print(f())
