"""No-three-in-line on the 75 x 75 grid (EinsteinArena 'no-three-in-line-75'): SAT with symmetry + lazy lines.

Symmetry classes (the planner picks which to run, the solver never assumes more than it encodes):
  rot180-150  : point-symmetric about the centre, 75 orbit pairs, every row/col exactly 2      -> 150 points
  mirror-149  : symmetric about the middle column; 74 rows hold a mirror pair, one row holds a
                single point on the axis                                                         -> 149 points
  diag-149    : symmetric about the main diagonal; 74 off-diagonal pairs + 1 diagonal point     -> 149 points
  diag-150    : symmetric about the main diagonal; 74 pairs + 2 diagonal points               -> 150 points
  none-149 / none-150 : no symmetry assumed
Lines: rows and columns are encoded as exact cardinalities. Every other line with >= 3 grid points is
added lazily: solve, list every line that holds 3+ chosen points, add 'at most 2' for those lines, repeat
(counter-example guided). A model with no violated line is a valid configuration, re-checked with the
EinsteinArena verifier's exact integer test before it is saved.
"""
import argparse, itertools, json, math, os, random, time
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver

N = 75


def orbit_map(sym):
    """point -> representative; returns rep_of dict and list of reps."""
    rep = {}
    for x in range(N):
        for y in range(N):
            if sym.startswith("rot180"):
                o = [(x, y), (N - 1 - x, N - 1 - y)]
            elif sym.startswith("mirror"):
                o = [(x, y), (N - 1 - x, y)]
            elif sym.startswith("diag"):
                o = [(x, y), (y, x)]
            else:
                o = [(x, y)]
            rep[(x, y)] = min(o)
    return rep


def line_key(p, q):
    (x1, y1), (x2, y2) = p, q
    a, b = y2 - y1, x1 - x2
    g = math.gcd(a, b); a //= g; b //= g
    if a < 0 or (a == 0 and b < 0): a, b = -a, -b
    return (a, b, a * x1 + b * y1)


def points_on_line(key):
    a, b, c = key
    pts = []
    if b == 0:
        if c % a == 0 and 0 <= c // a < N: pts = [(c // a, y) for y in range(N)]
        return pts
    for x in range(N):
        if (c - a * x) % b == 0:
            y = (c - a * x) // b
            if 0 <= y < N: pts.append((x, y))
    return pts


def violations(points):
    cnt = {}
    for p, q in itertools.combinations(points, 2):
        k = line_key(p, q); cnt[k] = cnt.get(k, 0) + 1
    return [k for k, c in cnt.items() if c >= 3]   # c = C(m,2) >= 3 <=> m >= 3


def verify(points):
    s = set(points)
    if len(s) != len(points) or any(not (0 <= x < N and 0 <= y < N) for x, y in points): return False
    for (x1, y1), (x2, y2), (x3, y3) in itertools.combinations(points, 3):
        if (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1) == 0: return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sym", default="mirror-149")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--solver", default="cadical195")
    ap.add_argument("--seconds", type=float, default=6 * 3600)
    ap.add_argument("--presolve-slopes", type=int, default=2, help="add all lines with |dx|,|dy| <= this up front")
    ap.add_argument("--out", default="runs/nothree")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    random.seed(a.seed)
    sym, target = a.sym.rsplit("-", 1); target = int(target)
    rep = orbit_map(a.sym)
    reps = sorted(set(rep.values()))
    random.shuffle(reps)                      # variable order differs per seed
    pool = IDPool()
    var = {r: pool.id(("p", r)) for r in reps}
    members = {}
    for p, r in rep.items(): members.setdefault(r, []).append(p)
    clauses = []

    def add_card(lits_w, k, exact=False):
        """at most k (or exactly k) over weighted literals (weight = multiplicity of the orbit on the line)."""
        heavy = [l for l, w in lits_w if w > k]
        for l in heavy: clauses.append([-l])
        lw = [(l, w) for l, w in lits_w if w <= k]
        lits = []
        for l, w in lw: lits += [l] * 1
        two = [l for l, w in lw if w == 2]
        if k == 2 and two:      # an orbit counting twice on this line excludes every other orbit on it
            for t in two:
                for l, w in lw:
                    if l != t: clauses.append([-t, -l])
        ones = [l for l, w in lw if w == 1]
        if exact:
            enc = CardEnc.equals(lits=[l for l, _ in lw], bound=k, vpool=pool, encoding=EncType.seqcounter) if not two else None
            if enc is None:     # exact with weights: handled by row/col structure below
                enc = CardEnc.atmost(lits=ones, bound=k, vpool=pool, encoding=EncType.seqcounter)
            clauses.extend(enc.clauses)
        elif len(ones) > k:
            clauses.extend(CardEnc.atmost(lits=ones, bound=k, vpool=pool, encoding=EncType.seqcounter).clauses)

    def weighted(points):
        w = {}
        for p in points: w[var[rep[p]]] = w.get(var[rep[p]], 0) + 1
        return list(w.items())

    # rows and columns: tight encodings per symmetry class
    def eq(lits, k):
        if k == 1:
            clauses.append(list(lits)); clauses.extend([[-u, -v] for u, v in itertools.combinations(lits, 2)])
        else:
            clauses.extend(CardEnc.equals(lits=list(lits), bound=k, vpool=pool, encoding=EncType.seqcounter).clauses)
    def am(lits, k):
        if len(lits) > k:
            clauses.extend(CardEnc.atmost(lits=list(lits), bound=k, vpool=pool, encoding=EncType.seqcounter).clauses)
    C = N // 2
    if sym == "mirror" and target == 149:
        for y in range(N):   # each row: exactly one item (a mirror pair, or the axis point)
            eq([var[(x, y)] for x in range(C)] + [var[(C, y)]], 1)
        eq([var[(C, y)] for y in range(N)], 1)
        for x in range(C): am([var[(x, y)] for y in range(N)], 2)
    elif sym == "rot180" and target == 150:
        clauses.append([-var[(C, C)]])
        for y in range(N):
            if y == C:
                eq([var[rep[(x, C)]] for x in range(C)], 1)
            else:
                eq(sorted({var[rep[(x, y)]] for x in range(N)}), 2)
        for x in range(N):
            if x == C:
                eq([var[rep[(C, y)]] for y in range(C)], 1)
            else:
                eq(sorted({var[rep[(x, y)]] for y in range(N)}), 2)
    elif sym == "diag":
        for y in range(N):   # row y has the same count as column y
            lits = sorted({var[rep[(x, y)]] for x in range(N)})
            am(lits, 2)
            clauses.append(lits)
        diag = [var[(i, i)] for i in range(N)]
        eq(diag, 1 if target == 149 else 2)
        offd = [var[r] for r in reps if r[0] != r[1]]
        clauses.extend(CardEnc.equals(lits=offd, bound=74, vpool=pool, encoding=EncType.totalizer).clauses)
    else:  # no symmetry
        for y in range(N):
            row = [var[(x, y)] for x in range(N)]
            (eq(row, 2) if target == 150 else (am(row, 2), clauses.append(row)))
        for x in range(N):
            col = [var[(x, y)] for y in range(N)]
            (eq(col, 2) if target == 150 else (am(col, 2), clauses.append(col)))
        if target == 149:
            clauses.extend(CardEnc.atleast(lits=list(var.values()), bound=149, vpool=pool, encoding=EncType.totalizer).clauses)
    # up-front small-slope lines
    added = set()
    s = a.presolve_slopes
    for dx in range(0, s + 1):
        for dy in range(-s, s + 1):
            if (dx == 0 and dy <= 0) or math.gcd(dx, abs(dy)) != 1 or dx == 0 or dy == 0:
                continue
            for x0 in range(N):
                for y0 in range(N):
                    k = line_key((x0, y0), (x0 + dx, y0 + dy))
                    if k in added: continue
                    pts = points_on_line(k)
                    if len(pts) >= 3:
                        added.add(k); add_card(weighted(pts), 2)
    solver = Solver(name=a.solver, bootstrap_with=clauses)
    clauses.clear()
    t0 = time.time(); it = 0; best_bad = 10**9
    log = open(os.path.join(a.out, f"log_{a.sym}_s{a.seed}.jsonl"), "a")
    print(f"[{a.sym} s{a.seed}] vars={pool.top} upfront_lines={len(added)} built in {time.time()-t0:.0f}s", flush=True)
    while time.time() - t0 < a.seconds:
        ok = solver.solve()
        it += 1
        if not ok:
            print(f"[{a.sym} s{a.seed}] UNSAT after {it} rounds, {len(added)} lines, {time.time()-t0:.0f}s: no {target}-point configuration in this symmetry class", flush=True)
            log.write(json.dumps({"event": "unsat", "rounds": it, "lines": len(added), "t": time.time() - t0}) + "\n")
            return
        model = set(l for l in solver.get_model() if l > 0)
        chosen = [p for r in reps if var[r] in model for p in members[r]]
        bad = violations(chosen)
        # artifact for the UI: the current model and every line that still holds 3+ chosen points
        if it == 1 or len(bad) <= best_bad:
            best_bad = len(bad)
            chosen_set = set(chosen)
            vl = [sorted(p for p in points_on_line(k) if p in chosen_set) for k in bad]
            tmp = os.path.join(a.out, f".latest_{a.sym}_s{a.seed}.json")
            json.dump({"sym": a.sym, "seed": a.seed, "round": it, "count": len(chosen), "violated": len(bad),
                       "lines_added": len(added), "t": round(time.time() - t0, 1),
                       "points": [list(p) for p in sorted(chosen)],
                       "violated_lines": [[list(v[0]), list(v[-1]), len(v)] for v in vl]}, open(tmp, "w"))
            os.replace(tmp, os.path.join(a.out, f"latest_{a.sym}_s{a.seed}.json"))
        if True:
            print(f"[{a.sym} s{a.seed}] round {it} points={len(chosen)} violated_lines={len(bad)} lines={len(added)} t={time.time()-t0:.0f}s", flush=True)
            log.write(json.dumps({"round": it, "points": len(chosen), "violated": len(bad), "lines": len(added), "t": round(time.time() - t0, 1)}) + "\n"); log.flush()
        if not bad:
            pts = sorted(chosen)
            if verify(pts):
                fn = os.path.join(a.out, f"FOUND_{a.sym}_s{a.seed}_{len(pts)}.json")
                json.dump({"points_count": len(pts), "solution": {"points": [list(p) for p in pts]}}, open(fn, "w"))
                print(f"FOUND {len(pts)} points, verified -> {fn}", flush=True)
                return
        for k in bad:
            if k in added: continue
            added.add(k)
            for c in _card_clauses(weighted(points_on_line(k)), pool):
                solver.add_clause(c)


def _card_clauses(lw, pool):
    out = []
    two = [l for l, w in lw if w >= 2]
    ones = [l for l, w in lw if w == 1]
    for t in two:
        if dict(lw)[t] > 2: out.append([-t]); continue
        for l, _ in lw:
            if l != t: out.append([-t, -l])
    if len(ones) > 2:
        out.extend(CardEnc.atmost(lits=ones, bound=2, vpool=pool, encoding=EncType.seqcounter).clauses)
    return out


if __name__ == "__main__":
    main()
