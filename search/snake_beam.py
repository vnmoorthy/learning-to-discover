"""Snake-in-the-box in Q_13 (EinsteinArena 'snake-in-the-box-13'): local surgery on the record snake.

A snake is an induced path; it is stored as its vertex list v_0..v_L (L edges). One CPU core.
Moves (all exact, numba DFS over the hypercube with an occupancy-adjacency counter c[u] = #path vertices next
to u, so a vertex z may extend the current end e iff z is free and c[z] == 1, i.e. its only path neighbour is e):
  * bridge surgery: cut the window v_i..v_j (w = j - i edges, w in [--wmin, --wmax]) and regrow an induced path
    from v_i to v_j through free space with >= w + 2 edges (parity forces steps of 2). DFS is randomised,
    pruned by Hamming distance to v_j, and limited to --budget nodes per attempt. If no longer bridge exists,
    with prob --psideways an equal-length different bridge is accepted (plateau walk, diversifies the snake);
  * end regrowth (prob --pend): cut the last w edges of either end and regrow the longest tail found (DFS).
Every improvement is re-checked by the OFFICIAL verifier before FOUND_*.json (only when L > --target).
Log line: `[snake s<seed>] t=..s best=<L>`.
"""
import argparse, importlib.util, json, os, time

os.environ.setdefault("NUMBA_CACHE_DIR", os.path.expanduser("~/.cache/ltd_numba"))
for _v in ("NUMBA_NUM_THREADS", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")   # one core per process
import numpy as np
from numba import njit

HERE = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.dirname(HERE)
PROB = os.path.join(ROOT, "problems", "snake-in-the-box-13")
DIM = 13
NV = 1 << DIM
CAP = NV


def load_verifier():
    spec = importlib.util.spec_from_file_location("snake_verifier", os.path.join(PROB, "verifier.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


@njit(cache=True)
def seed_rng(s):
    np.random.seed(s)


@njit(cache=True)
def check_actions(acts):
    """(ok, length) with exactly the official verifier's rules."""
    vis = np.zeros(NV, np.int8)
    cur = 0
    vis[0] = 1
    for a in acts:
        if a < 0 or a >= DIM:
            return False, 0
        nx = cur ^ (1 << a)
        if vis[nx]:
            return False, 0
        for d in range(DIM):
            nb = nx ^ (1 << d)
            if vis[nb] and nb != cur:
                return False, 0
        vis[nx] = 1
        cur = nx
    return True, len(acts)


@njit(cache=True)
def occupy(z, vis, c):
    vis[z] = 1
    for d in range(DIM):
        c[z ^ (1 << d)] += 1


@njit(cache=True)
def vacate(z, vis, c):
    vis[z] = 0
    for d in range(DIM):
        c[z ^ (1 << d)] -= 1


@njit(cache=True)
def popcount(x):
    n = 0
    while x:
        x &= x - 1
        n += 1
    return n


@njit(cache=True)
def dfs_bridge(a, b, minm, maxm, budget, vis, c, out):
    """Induced path a -> u_1..u_m -> b through free vertices, minm <= m <= maxm. Returns m (path in out) or -1.
    Precondition: a, b occupied (part of the remaining snake), interior of the old window vacated."""
    node = np.empty(maxm + 2, np.int64)
    perm = np.empty((maxm + 2, DIM), np.int64)
    nxt = np.zeros(maxm + 2, np.int64)
    node[0] = a
    for d in range(DIM):
        perm[0, d] = d
    for d in range(DIM - 1, 0, -1):
        r = np.random.randint(d + 1); t = perm[0, d]; perm[0, d] = perm[0, r]; perm[0, r] = t
    nxt[0] = 0
    depth = 0
    pushes = 0
    while depth >= 0:
        if nxt[depth] >= DIM or pushes >= budget:
            # pop
            if depth == 0:
                return -1
            vacate(node[depth], vis, c)
            depth -= 1
            if pushes >= budget:
                continue
            continue
        e = node[depth]
        z = e ^ (1 << perm[depth, nxt[depth]])
        nxt[depth] += 1
        if vis[z]:
            continue
        adj_b = popcount(z ^ b) == 1
        dz = depth + 1
        if adj_b:
            if c[z] == 2 and dz >= minm and dz <= maxm:
                # close: out = u_1..u_m
                for q in range(1, dz):
                    out[q - 1] = node[q]
                out[dz - 1] = z
                # vacate the DFS interior (caller re-occupies when splicing)
                for q in range(depth, 0, -1):
                    vacate(node[q], vis, c)
                return dz
            continue
        if c[z] != 1:
            continue
        if dz + popcount(z ^ b) - 1 > maxm or dz >= maxm:
            continue
        pushes += 1
        occupy(z, vis, c)
        depth = dz
        node[depth] = z
        for d in range(DIM):
            perm[depth, d] = d
        for d in range(DIM - 1, 0, -1):
            r = np.random.randint(d + 1); t = perm[depth, d]; perm[depth, d] = perm[depth, r]; perm[depth, r] = t
        nxt[depth] = 0
    return -1


@njit(cache=True)
def dfs_extend(a, maxdepth, budget, vis, c, out):
    """Longest induced extension from end a (a occupied, all its other path neighbours fixed). Returns length."""
    node = np.empty(maxdepth + 2, np.int64)
    perm = np.empty((maxdepth + 2, DIM), np.int64)
    nxt = np.zeros(maxdepth + 2, np.int64)
    node[0] = a
    for d in range(DIM):
        perm[0, d] = d
    for d in range(DIM - 1, 0, -1):
        r = np.random.randint(d + 1); t = perm[0, d]; perm[0, d] = perm[0, r]; perm[0, r] = t
    depth = 0; pushes = 0; best = 0
    while depth >= 0:
        if nxt[depth] >= DIM or pushes >= budget:
            if depth == 0:
                break
            vacate(node[depth], vis, c)
            depth -= 1
            continue
        e = node[depth]
        z = e ^ (1 << perm[depth, nxt[depth]])
        nxt[depth] += 1
        if vis[z] or c[z] != 1 or depth + 1 > maxdepth:
            continue
        pushes += 1
        occupy(z, vis, c)
        depth += 1
        node[depth] = z
        if depth > best:
            best = depth
            for q in range(1, depth + 1):
                out[q - 1] = node[q]
        for d in range(DIM):
            perm[depth, d] = d
        for d in range(DIM - 1, 0, -1):
            r = np.random.randint(d + 1); t = perm[depth, d]; perm[depth, d] = perm[depth, r]; perm[depth, r] = t
        nxt[depth] = 0
    return best


@njit(cache=True)
def surgery_chunk(attempts, path, Larr, vis, c, wmin, wmax, budget, psideways, pend, stats, out, tmp):
    """path: vertices (capacity NV); Larr[0] = number of edges. stats = [attempts, improvements, sideways].
    Returns gain (edges) of this chunk."""
    gain = 0
    for at in range(attempts):
        stats[0] += 1
        L = Larr[0]
        if np.random.random() < pend:
            # end regrowth: reverse the path with prob 1/2 so both ends are worked on
            if np.random.random() < 0.5:
                for q in range((L + 1) // 2):
                    t = path[q]; path[q] = path[L - q]; path[L - q] = t
            w = wmin + np.random.randint(wmax - wmin + 1)
            if w > L - 1:
                w = L - 1
            for q in range(L, L - w, -1):
                vacate(path[q], vis, c)
            m = dfs_extend(path[L - w], w + 64, budget, vis, c, out)
            if m > w:
                for q in range(m):
                    path[L - w + 1 + q] = out[q]
                    occupy(out[q], vis, c)
                Larr[0] = L - w + m
                gain += m - w; stats[1] += 1
            else:
                for q in range(L - w + 1, L + 1):
                    occupy(path[q], vis, c)
            continue
        w = wmin + np.random.randint(wmax - wmin + 1)
        if w > L:
            w = L
        i = np.random.randint(L - w + 1)
        j = i + w
        for q in range(i + 1, j):
            vacate(path[q], vis, c)
        a = path[i]; b = path[j]
        m = dfs_bridge(a, b, w + 1, w + 1 + 2 * ((wmax + 1) // 4 + 1), budget, vis, c, out)
        sideways = False
        if m < 0 and np.random.random() < psideways:
            m = dfs_bridge(a, b, w - 1, w - 1, budget // 4 + 1, vis, c, out)
            if m >= 0:
                same = True
                for q in range(m):
                    if out[q] != path[i + 1 + q]:
                        same = False; break
                if same:
                    m = -1
                else:
                    sideways = True
        if m < 0:
            for q in range(i + 1, j):
                occupy(path[q], vis, c)
            continue
        # splice: path[:i+1] + out[:m] + path[j:]
        tail = L - j + 1
        for q in range(tail):
            tmp[q] = path[j + q]
        for q in range(m):
            path[i + 1 + q] = out[q]
            occupy(out[q], vis, c)
        for q in range(tail):
            path[i + 1 + m + q] = tmp[q]
        Larr[0] = i + 1 + m + tail - 1
        if sideways:
            stats[2] += 1
        else:
            stats[1] += 1
            gain += (m + 1) - w
    return gain


def path_to_actions(path, L):
    x = np.bitwise_xor(path[1:L + 1], path[:L])
    return [int(v).bit_length() - 1 for v in x]


def actions_to_path(acts):
    path = np.zeros(NV, np.int64)
    cur = 0
    for k, a in enumerate(acts):
        cur ^= 1 << a; path[k + 1] = cur
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--rank", type=int, default=0, help="which public snake to start from (0 = record)")
    ap.add_argument("--init-file", default=None, help="optional JSON with {'actions': [...]}")
    ap.add_argument("--wmin", type=int, default=4)
    ap.add_argument("--wmax", type=int, default=24)
    ap.add_argument("--budget", type=int, default=20000, help="DFS nodes per attempt")
    ap.add_argument("--psideways", type=float, default=0.5)
    ap.add_argument("--pend", type=float, default=0.05)
    ap.add_argument("--seconds", type=float, default=3600 * 6)
    ap.add_argument("--target", type=int, default=2950)
    ap.add_argument("--out", default="runs/snake")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    tag = f"[snake s{a.seed}]"
    # the template validates wmin and wmax independently, so wmin > wmax (or a tiny window) can arrive here;
    # np.random.randint(wmax - wmin + 1) would then crash inside numba ("empty range for randrange()")
    w0 = (a.wmin, a.wmax)
    a.wmin, a.wmax = max(2, min(a.wmin, a.wmax)), max(2, a.wmin, a.wmax)
    a.budget = max(1, a.budget)
    if (a.wmin, a.wmax) != w0:
        print(f"{tag} note: window [{w0[0]},{w0[1]}] normalised to [{a.wmin},{a.wmax}]", flush=True)
    ver = load_verifier()
    t0 = time.time(); seed_rng(a.seed)
    if a.init_file:
        acts = json.load(open(a.init_file))["actions"]
    else:
        recs = json.load(open(os.path.join(PROB, "best_solutions.json")))
        acts = recs[min(a.rank, len(recs) - 1)]["data"]["actions"]
    L0 = int(ver.evaluate({"actions": acts}))
    path = actions_to_path(acts)
    vis = np.zeros(NV, np.int8); c = np.zeros(NV, np.int64)
    for q in range(L0 + 1):
        occupy(path[q], vis, c)
    Larr = np.array([L0], np.int64); stats = np.zeros(3, np.int64)
    out = np.zeros(NV, np.int64); tmp = np.zeros(NV, np.int64)
    best = L0
    sid = os.environ.get("PHOENIX_STRATEGY_ID")      # set by the backend launcher: unique file names per strategy
    best_file = os.path.join(a.out, f"best_{sid}.json" if sid else f"best_s{a.seed}.json")

    def save(final=False):
        acts_now = path_to_actions(path, int(Larr[0]))
        score = ver.evaluate({"actions": acts_now})          # official verifier; raises if not a snake
        assert int(score) == int(Larr[0])
        json.dump({"seed": a.seed, "length": int(score), "t": round(time.time() - t0, 1), "attempts": int(stats[0]),
                   "actions": acts_now}, open(best_file + ".tmp", "w"))
        os.replace(best_file + ".tmp", best_file)
        if score > a.target:
            fn = os.path.join(a.out, f"FOUND_{sid or 's' + str(a.seed)}_{int(score)}.json")
            json.dump({"solution": {"actions": acts_now}, "score": score, "seed": a.seed,
                       "t": round(time.time() - t0, 1)}, open(fn, "w"))
            print(f"FOUND snake of length {int(score)} verified by official verifier -> {fn}", flush=True)

    save()
    print(f"{tag} setup L0={L0} window=[{a.wmin},{a.wmax}] budget={a.budget} t={time.time()-t0:.1f}s", flush=True)
    print(f"{tag} t={time.time()-t0:.0f}s best={best} attempts=0", flush=True)
    chunk = 200; last_hb = time.time(); last_save = time.time()
    while time.time() - t0 < a.seconds:
        c0 = time.time(); s0 = int(stats[0])
        surgery_chunk(chunk, path, Larr, vis, c, a.wmin, a.wmax, a.budget, a.psideways, a.pend, stats, out, tmp)
        dt = max(time.time() - c0, 1e-3)
        chunk = int(min(max((int(stats[0]) - s0) / dt, 10), 1 << 20))
        if Larr[0] > best:
            best = int(Larr[0]); save(); last_save = time.time()
            print(f"{tag} t={time.time()-t0:.0f}s best={best} attempts={int(stats[0])} "
                  f"improvements={int(stats[1])} sideways={int(stats[2])}", flush=True)
        elif time.time() - last_save > 300:
            save(); last_save = time.time()     # keep the (sideways-walked) current snake on disk
        if time.time() - last_hb > 60:
            last_hb = time.time()
            print(f"{tag} t={time.time()-t0:.0f}s best={best} cur={int(Larr[0])} attempts={int(stats[0])} "
                  f"improvements={int(stats[1])} sideways={int(stats[2])} rate={stats[0]/(time.time()-t0):.0f}/s",
                  flush=True)
    save()
    print(f"{tag} done t={time.time()-t0:.0f}s best={best} attempts={int(stats[0])}", flush=True)


if __name__ == "__main__":
    main()
