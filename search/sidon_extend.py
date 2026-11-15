"""Exact extension search for the Sidon (4,5)-set problem.

Base: Ma-Tang's 14-point (4,5)-set A with h(A) = 8 (score 8/14 = 4/7).
Adding a point x keeps h = 8 iff every Sidon 8-subset S of A is blocked by x, i.e. x lies in
F(S) = {s_j + s_k - s_i} U {(s_j + s_k)/2} U S. So the good x are exactly the intersection of the F(S):
a finite set, which we enumerate completely (no range limit). Same idea one level deeper for 2 points.
"""
import itertools, json, sys, time
from functools import reduce

def is_sidon(S):
    sums = set()
    for i, a in enumerate(S):
        for b in S[i:]:
            if a + b in sums: return False
            sums.add(a + b)
    return True

def is45(A):
    for four in itertools.combinations(sorted(A), 4):
        if len({four[j] - four[i] for i in range(4) for j in range(i + 1, 4)}) < 5: return False
    return True

def is45_with(A, x):
    for three in itertools.combinations(A, 3):
        four = sorted(three + (x,))
        if len({four[j] - four[i] for i in range(4) for j in range(i + 1, 4)}) < 5: return False
    return True

def F(S):
    out = set(S)
    for j, a in enumerate(S):
        for b in S[j:]:
            if (a + b) % 2 == 0: out.add((a + b) // 2)
            for c in S: out.add(a + b - c)
    return out

def h(A):
    A = sorted(A)
    for k in range(len(A), 0, -1):
        if any(is_sidon(S) for S in itertools.combinations(A, k)): return k

def main(base, depth2_range):
    A = sorted(base); hA = h(A); n = len(A)
    t = time.time()
    top = [S for S in itertools.combinations(A, hA) if is_sidon(S)]
    print(f"base n={n} h={hA} score={hA/n:.6f}; Sidon {hA}-subsets: {len(top)}", flush=True)
    good1 = reduce(lambda a, b: a & b, (F(S) for S in top)) - set(A)
    good1 = sorted(x for x in good1 if is45_with(A, x))
    print(f"single-point extensions keeping h={hA}: {good1}  ({time.time()-t:.1f}s)", flush=True)
    for x in good1:
        B = sorted(A + [x]); print("RECORD CANDIDATE", B, h(B), is45(B), h(B) / len(B), flush=True)
    # two points: 16 elements, h <= hA + 1
    lo, hi = depth2_range
    found = []
    for x in range(lo, hi + 1):
        if x in A or not is45_with(A, x): continue
        ext = [S + (x,) for S in top if x not in F(S)]   # Sidon (hA+1)-subsets of A+{x} that contain x
        if not ext:
            continue
        cand = reduce(lambda a, b: a & b, (F(sorted(S)) for S in ext)) - set(A) - {x}
        Ax = A + [x]
        for y in sorted(cand):
            if y > x and is45_with(Ax, y):
                B = sorted(Ax + [y]); hb = h(B)
                if hb is not None and hb / len(B) < hA / n - 1e-12:
                    print("RECORD CANDIDATE", B, hb, hb / len(B), flush=True); found.append(B)
        if (x - lo) % 500 == 0: print(f"x={x} ext={len(ext)} cand={len(cand)} t={time.time()-t:.0f}s", flush=True)
    json.dump(found, open(sys.argv[1] if len(sys.argv) > 1 else "sidon_found.json", "w"))

if __name__ == "__main__":
    MA_TANG = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
    main(MA_TANG, (-3000, 4000))
