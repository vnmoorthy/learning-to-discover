"""Sidon subsets of (4,5)-sets (EinsteinArena 'sidon-45-set'): simulated annealing over integer (4,5)-sets.

Goal: an integer (4,5)-set A (every 4 elements determine >= 5 distinct differences) with h(A)/|A| < 4/7, where
h(A) is the largest Sidon subset. Targets: |A|=15 with h=8, |A|=16 with h=9, |A|=18 with h=10.

State: n distinct integers in [0, M], always a (4,5)-set (hard constraint, checked exactly for every move).
Energy: E(A) = number of Sidon (t+1)-subsets of A, t = target h (E = 0  <=>  h(A) <= t), counted exactly by a
numba DFS that marks absolute differences (S is Sidon iff all its pairwise |differences| are distinct).
SA uses dE = log(1+E') - log(1+E). Moves (replace one element x by y; x is picked proportionally to its participation in Sidon (t+1)-subsets
with prob --pw):
  * hub (--phub): y closes >= 2 additive relations at once (multiplicity-weighted among a+b-c, (a+b)/2, 2a-b);
  * structured (default 55%): y = a+b-c, (a+b)/2 or 2a-b for random a,b,c in A\\{x}: creates an additive
    relation, which is what kills large Sidon subsets, while the (4,5) check keeps at most one per 4-set;
  * local: y = x +- d, small d;   * random: y uniform in [0, M].
Cycles of geometric cooling T0 -> T1; at each reheat, with prob 1/2 jump back to the best state.
Init: matang (Ma-Tang's 14-point set, plus extra structured points if n > 14) or random greedy (4,5)-set.
Exact h(A) by branch and bound; every claim is re-checked by the OFFICIAL verifier before FOUND_*.json is written.
Single-threaded. Log line: `[sidon s<seed>] t=..s best=<h>/<n>=<score>`.
"""
import argparse, importlib.util, json, math, os, time

os.environ.setdefault("NUMBA_CACHE_DIR", os.path.expanduser("~/.cache/ltd_numba"))
for _v in ("NUMBA_NUM_THREADS", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")   # one core per process
import numpy as np
from numba import njit

HERE = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.dirname(HERE)
PROB = os.path.join(ROOT, "problems", "sidon-45-set")
MA_TANG = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
RECORD = 4 / 7


def load_verifier():
    spec = importlib.util.spec_from_file_location("sidon_verifier", os.path.join(PROB, "verifier.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def auto_target(n):
    """largest t with t/n < 4/7"""
    t = (4 * n - 1) // 7
    while (t + 1) * 7 < 4 * n:
        t += 1
    return t


@njit(cache=True)
def seed_rng(s):
    np.random.seed(s)


@njit(cache=True)
def quad_ok(a, b, c, d):
    """True iff {a,b,c,d} has >= 5 distinct absolute pairwise differences (at most one equal pair)."""
    x = np.empty(6, np.int64)
    x[0] = abs(a - b); x[1] = abs(a - c); x[2] = abs(a - d)
    x[3] = abs(b - c); x[4] = abs(b - d); x[5] = abs(c - d)
    eq = 0
    for p in range(6):
        for q in range(p + 1, 6):
            if x[p] == x[q]:
                eq += 1
                if eq >= 2:
                    return False
    return True


@njit(cache=True)
def ok45_with(vals, n, skip, y):
    """Would replacing vals[skip] by y (skip=-1: appending y) keep a distinct (4,5)-set?"""
    for i in range(n):
        if i != skip and vals[i] == y:
            return False
    for i in range(n):
        if i == skip:
            continue
        for j in range(i + 1, n):
            if j == skip:
                continue
            for k in range(j + 1, n):
                if k == skip:
                    continue
                if not quad_ok(vals[i], vals[j], vals[k], y):
                    return False
    return True


@njit(cache=True)
def sidon_dfs(vals, n, k, mark, cap, mode, part):
    """mode 0: count Sidon subsets of size exactly k (stops at cap); part[i] += number of counted subsets that
    contain element i. mode 1: return max Sidon subset size.
    mark: int8 array over |differences| (all zero on entry and on exit)."""
    idx = np.zeros(n + 1, np.int64)
    start = np.zeros(n + 1, np.int64)
    ch = np.zeros(n + 1, np.int64)
    nd = np.zeros((n + 1, n + 1), np.int64)
    best = 0
    cnt = 0
    if mode == 0 and k == 0:
        return 1
    depth = 0
    start[0] = 0
    while True:
        if mode == 0 and depth == k:
            cnt += 1
            for q in range(k):
                part[idx[q]] += 1
            depth -= 1
            for q in range(depth):
                mark[nd[depth, q]] = 0
            if cnt >= cap:
                # unwind everything
                for dd in range(depth - 1, -1, -1):
                    for q in range(dd):
                        mark[nd[dd, q]] = 0
                return cnt
            start[depth] = idx[depth] + 1
            continue
        found = False
        i = start[depth]
        while i < n:
            if mode == 0:
                if n - i < k - depth:
                    break
            else:
                if depth + (n - i) <= best:
                    break
            v = vals[i]
            ok = True
            m = 0
            for j in range(depth):
                d = abs(v - ch[j])
                if mark[d] != 0:
                    ok = False
                    break
                mark[d] = 1
                nd[depth, m] = d
                m += 1
            if ok:
                found = True
                break
            for q in range(m):
                mark[nd[depth, q]] = 0
            i += 1
        if found:
            idx[depth] = i
            ch[depth] = vals[i]
            depth += 1
            if mode == 1 and depth > best:
                best = depth
                if best == n:
                    for dd in range(depth - 1, -1, -1):
                        for q in range(dd):
                            mark[nd[dd, q]] = 0
                    return best
            start[depth] = i + 1
        else:
            if depth == 0:
                break
            depth -= 1
            for q in range(depth):
                mark[nd[depth, q]] = 0
            start[depth] = idx[depth] + 1
    if mode == 0:
        return cnt
    return best


@njit(cache=True)
def hub_candidate(vals, n, i, M, buf):
    """A value y that would close >= 2 additive relations with A minus element i at once (y = a+b-c, (a+b)/2,
    2a-b), sampled proportionally to its multiplicity; -1 if no value has multiplicity >= 2."""
    m = 0
    for a in range(n):
        if a == i:
            continue
        for b in range(a + 1, n):
            if b == i:
                continue
            s = vals[a] + vals[b]
            if s % 2 == 0:
                buf[m] = s // 2; m += 1
            for c in range(n):
                if c == i or c == a or c == b:
                    continue
                buf[m] = s - vals[c]; m += 1
            buf[m] = 2 * vals[a] - vals[b]; m += 1
            buf[m] = 2 * vals[b] - vals[a]; m += 1
    srt = np.sort(buf[:m])
    tot = 0
    q = 0
    while q < m:
        r = q
        while r + 1 < m and srt[r + 1] == srt[q]:
            r += 1
        if r > q and srt[q] >= 0 and srt[q] <= M:
            tot += r - q + 1
        q = r + 1
    if tot == 0:
        return -1
    pick = np.random.randint(tot)
    q = 0
    while q < m:
        r = q
        while r + 1 < m and srt[r + 1] == srt[q]:
            r += 1
        if r > q and srt[q] >= 0 and srt[q] <= M:
            if pick < r - q + 1:
                return srt[q]
            pick -= r - q + 1
        q = r + 1
    return -1


@njit(cache=True)
def propose(vals, n, i, M, pstruct, plocal, phub, buf):
    x = vals[i]
    r = np.random.random()
    if r < phub:
        return hub_candidate(vals, n, i, M, buf)
    r = np.random.random()
    if r < pstruct and n >= 4:
        a = i
        while a == i:
            a = np.random.randint(n)
        b = i
        while b == i or b == a:
            b = np.random.randint(n)
        kind = np.random.randint(3)
        if kind == 0:
            c = i
            while c == i or c == a or c == b:
                c = np.random.randint(n)
            return vals[a] + vals[b] - vals[c]
        elif kind == 1:
            s = vals[a] + vals[b]
            if s % 2 != 0:
                return -1
            return s // 2
        else:
            return 2 * vals[a] - vals[b]
    elif r < pstruct + plocal:
        span = max(2, M // 50)
        d = np.random.randint(1, span + 1)
        if np.random.random() < 0.5:
            d = -d
        return x + d
    return np.random.randint(M + 1)


@njit(cache=True)
def sa_chunk(steps, vals, n, t, M, mark, cap, T0, T1, cycle, pstruct, plocal, st, bestv, Ecur, pcur, pw, phub):
    """st = [phase, bestE, total_steps, accepted]; Ecur = [E]; pcur[i] = number of Sidon (t+1)-subsets of the
    current state containing element i. Returns 1 if best improved (or E hit 0)."""
    improved = 0
    ptmp = np.zeros(n, np.int64)
    buf = np.zeros(n * n * n + 4 * n * n, np.int64)
    for s in range(steps):
        st[2] += 1
        frac = st[0] / cycle
        T = T0 * (T1 / T0) ** frac
        st[0] += 1
        if st[0] >= cycle:
            st[0] = 0
            if np.random.random() < 0.5:
                for q in range(n):
                    vals[q] = bestv[q]
                for q in range(n):
                    ptmp[q] = 0
                Ecur[0] = sidon_dfs(vals, n, t + 1, mark, cap, 0, ptmp)
                for q in range(n):
                    pcur[q] = ptmp[q]
        # element to move: with prob pw proportional to its participation in Sidon (t+1)-subsets
        tot = 0
        for q in range(n):
            tot += pcur[q]
        if tot > 0 and np.random.random() < pw:
            r = np.random.randint(tot)
            i = 0
            while r >= pcur[i]:
                r -= pcur[i]; i += 1
        else:
            i = np.random.randint(n)
        x = vals[i]
        y = propose(vals, n, i, M, pstruct, plocal, phub, buf)
        if y < 0 or y > M or y == x:
            continue
        if not ok45_with(vals, n, i, y):
            continue
        vals[i] = y
        for q in range(n):
            ptmp[q] = 0
        E2 = sidon_dfs(vals, n, t + 1, mark, cap, 0, ptmp)
        dE = math.log1p(E2) - math.log1p(Ecur[0])
        if dE <= 0 or np.random.random() < math.exp(-dE / T):
            Ecur[0] = E2
            for q in range(n):
                pcur[q] = ptmp[q]
            st[3] += 1
            if E2 < st[1]:
                st[1] = E2
                for q in range(n):
                    bestv[q] = vals[q]
                improved = 1
                if E2 == 0:
                    return 1
        else:
            vals[i] = x
    return improved


def random_init(n, M, rng, base=None, max_tries=200000):
    vals = [int(v) for v in (base or [])]
    tries = 0
    while len(vals) < n:
        tries += 1
        if len(vals) >= 3 and rng.random() < 0.6:
            a, b, c = rng.choice(vals, 3, replace=False)
            y = int([a + b - c, 2 * a - b, (a + b) // 2][rng.integers(3)])
        else:
            y = int(rng.integers(0, M + 1))
        if 0 <= y <= M and ok45_with(np.array(vals + [0], np.int64), len(vals), -1, y):
            vals.append(y)
        if tries > max_tries:
            raise RuntimeError("could not build an initial (4,5)-set; increase --M")
    return vals


def init_set(n, M, rng, base, tag):
    """random_init, doubling M when [0, M] is too small for a greedy (4,5)-set of size n (e.g. n=18, M=200):
    the template accepts M down to 200, and crashing at startup would waste the launch."""
    for _ in range(12):
        try:
            return random_init(n, M, rng, base, max_tries=40000), M
        except RuntimeError:
            print(f"{tag} note: no greedy (4,5)-set of size {n} found in [0,{M}]; retrying with M={2 * M}",
                  flush=True)
            M *= 2
    raise RuntimeError(f"could not build an initial (4,5)-set of size {n} (M up to {M})")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--n", type=int, default=15, help="|A| (4..18)")
    ap.add_argument("--target", type=int, default=0, help="target h (0 = largest t with t/n < 4/7)")
    ap.add_argument("--M", type=int, default=2000, help="elements live in [0, M]")
    ap.add_argument("--init", default="matang", choices=["matang", "random"])
    ap.add_argument("--T0", type=float, default=0.3)
    ap.add_argument("--T1", type=float, default=0.01)
    ap.add_argument("--pw", type=float, default=0.8, help="prob. of moving an element weighted by participation")
    ap.add_argument("--cycle", type=int, default=20000, help="SA steps per cooling cycle")
    ap.add_argument("--pstruct", type=float, default=0.55)
    ap.add_argument("--plocal", type=float, default=0.2)
    ap.add_argument("--phub", type=float, default=0.2, help="prob. of a multi-relation 'hub' move")
    ap.add_argument("--cap", type=int, default=100000, help="stop counting Sidon subsets beyond this")
    ap.add_argument("--seconds", type=float, default=3600 * 6)
    ap.add_argument("--out", default="runs/sidon")
    a = ap.parse_args()
    assert 4 <= a.n <= 18
    os.makedirs(a.out, exist_ok=True)
    tag = f"[sidon s{a.seed}]"
    auto = auto_target(a.n)
    # E = 0 must imply a record (h <= t < 4n/7), so a target above the automatic one would make the search
    # converge to a non-record; a smaller target is allowed (more ambitious)
    t = min(a.target, auto) if a.target > 0 else auto
    if a.target > auto:
        print(f"{tag} note: --target {a.target} cannot beat 4/7 for n={a.n}; using {auto}", flush=True)
    ver = load_verifier()
    rng = np.random.default_rng(a.seed); seed_rng(a.seed)
    t0 = time.time()
    M = a.M
    if a.init == "matang":
        M = max(M, max(MA_TANG))
        base = MA_TANG[:a.n] if a.n <= 14 else MA_TANG
        vals, M = init_set(a.n, M, rng, base, tag)
    else:
        vals, M = init_set(a.n, M, rng, None, tag)
    vals = np.array(vals, np.int64)
    mark = np.zeros(M + 1, np.int8)
    pcur = np.zeros(a.n, np.int64); dummy = np.zeros(a.n, np.int64)
    E = sidon_dfs(vals, a.n, t + 1, mark, a.cap, 0, pcur)
    h = sidon_dfs(vals, a.n, 0, mark, 0, 1, dummy)
    st = np.array([0, E, 0, 0], np.int64); Ecur = np.array([E], np.int64); bestv = vals.copy()
    best_h = h; best_set = sorted(vals.tolist()); best_E = E     # best exact score seen (ties: lower excess)
    print(f"{tag} setup n={a.n} target_h={t} M={M} init={a.init} h0={h} E0={E} t={time.time()-t0:.1f}s", flush=True)
    sid = os.environ.get("LTD_STRATEGY_ID")      # set by the backend launcher: unique file names per strategy
    best_file = os.path.join(a.out, f"best_{sid}.json" if sid else f"best_n{a.n}_s{a.seed}.json")

    def save(sa_elements, sa_h, sa_E):
        # top-level elements/h/score = best exact h/n seen; sa_best = the SA's lowest-excess state
        json.dump({"n": a.n, "target_h": t, "seed": a.seed, "elements": [int(v) for v in best_set], "h": int(best_h),
                   "score": best_h / a.n, "excess": int(best_E), "t": round(time.time() - t0, 1), "steps": int(st[2]),
                   "sa_best": {"elements": [int(v) for v in sa_elements], "h": int(sa_h), "excess": int(sa_E)}},
                  open(best_file + ".tmp", "w"))
        os.replace(best_file + ".tmp", best_file)

    save(best_set, best_h, E)
    print(f"{tag} t={time.time()-t0:.0f}s best={best_h}/{a.n}={best_h/a.n:.6f} excess={E}", flush=True)
    last_hb = time.time(); chunk = 200
    while time.time() - t0 < a.seconds:
        c0 = time.time(); s0 = int(st[2])
        imp = sa_chunk(chunk, vals, a.n, t, M, mark, a.cap, a.T0, a.T1, a.cycle, a.pstruct, a.plocal, st, bestv, Ecur,
                       pcur, a.pw, a.phub)
        dt = max(time.time() - c0, 1e-3)
        chunk = int(min(max((int(st[2]) - s0) / dt, 20), 1 << 22))
        if imp:
            hb = sidon_dfs(bestv, a.n, 0, mark, 0, 1, dummy)
            if (hb, int(st[1])) < (best_h, best_E):
                best_h = hb; best_set = sorted(bestv.tolist()); best_E = int(st[1])
            save(sorted(bestv.tolist()), hb, st[1])
            print(f"{tag} t={time.time()-t0:.0f}s best={best_h}/{a.n}={best_h/a.n:.6f} excess={int(st[1])} "
                  f"h_cur_best={hb} steps={int(st[2])}", flush=True)
            if hb / a.n < RECORD - 1e-9:
                els = [int(v) for v in sorted(bestv.tolist())]
                score = ver.evaluate({"elements": els})     # official verifier (raises if not a (4,5)-set)
                if score < RECORD - 1e-9:
                    fn = os.path.join(a.out, f"FOUND_{sid or 'n' + str(a.n) + '_s' + str(a.seed)}_"
                                                 f"{int(round(score * a.n))}of{a.n}.json")
                    json.dump({"solution": {"elements": els}, "score": score, "n": a.n, "seed": a.seed,
                               "t": round(time.time() - t0, 1)}, open(fn, "w"))
                    print(f"FOUND sidon (4,5)-set n={a.n} h/n={score:.9f} verified by official verifier -> {fn}",
                          flush=True)
                    # last line keeps the parser's best=<h>/<n>=<score> format (telemetry reads the final line)
                    print(f"{tag} done t={time.time()-t0:.0f}s best={best_h}/{a.n}={best_h/a.n:.6f} excess=0 "
                          f"steps={int(st[2])} found=1", flush=True)
                    return
                print(f"{tag} official verifier disagrees: score={score}", flush=True)
        if time.time() - last_hb > 60:
            last_hb = time.time()
            print(f"{tag} t={time.time()-t0:.0f}s best={best_h}/{a.n}={best_h/a.n:.6f} excess={int(st[1])} "
                  f"cur_excess={int(Ecur[0])} steps={int(st[2])} rate={st[2]/(time.time()-t0):.0f}/s "
                  f"acc={st[3]/max(1, st[2]):.3f}", flush=True)
    print(f"{tag} done t={time.time()-t0:.0f}s best={best_h}/{a.n}={best_h/a.n:.6f} excess={int(st[1])} "
          f"steps={int(st[2])}", flush=True)


if __name__ == "__main__":
    main()
