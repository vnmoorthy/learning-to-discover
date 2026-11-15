"""Two-deletion-correcting binary code of length 16 (EinsteinArena 'two-deletion-code-16'): iterated local search.

Model: a code is a set packing. Elements = the 2^14 binary strings of length 14; a word w of length 16 "covers"
the set D(w) of its distinct 2-deletion descendants. A code is valid iff the D(w) of its words are pairwise
disjoint (exactly the official verifier's test), so the task is maximum (weighted) set packing / independent set
in the conflict graph (u ~ v iff D(u) and D(v) intersect).

Search: ARW-style iterated local search (Andrade, Resende, Werneck 2012) on that packing:
  * state: owner[e] (which codeword covers element e), tau[w] = number of codewords conflicting with w,
    c1[x] = number of non-code words whose ONLY conflicting codeword is x; all maintained incrementally;
  * local search: (1,2)-swaps (drop x, insert two mutually compatible words that only conflicted with x),
    for the weighted orbit model also improving (1,1)-swaps; free words are inserted greedily;
  * perturbation: force in k words whose tightness tau <= --perturb (k = 1 usually, geometric tail), the
    forced words are locked during the following local search;
  * acceptance (--accept arw): a worse solution is accepted with prob 1 / (1 + d * d*), otherwise undone exactly
    via an undo log (--accept plateau: worse solutions are always undone); after --restart non-improving iterations the search returns to the best solution.
Modes:
  from_record : start from a public best solution (problems/two-deletion-code-16/best_solutions.json)
  from_scratch: randomized min-ball greedy start
  symmetric   : the code is forced to be closed under a group G (--group rev|comp|rc|full); items are
                G-orbits that are internally compatible, weight = orbit size (shrinks the space ~|G| times)
Every saved/claimed code is re-checked with the OFFICIAL verifier. FOUND_*.json only when size > --target.
Single-threaded (one core). Log line: `[twodel s<seed>] t=..s best=<size>`.
"""
import argparse, importlib.util, json, os, sys, time

os.environ.setdefault("NUMBA_CACHE_DIR", os.path.expanduser("~/.cache/ltd_numba"))
for _v in ("NUMBA_NUM_THREADS", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")   # one core per process
import numpy as np
from numba import njit

HERE = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.dirname(HERE)
PROB = os.path.join(ROOT, "problems", "two-deletion-code-16")
N = 16
NE = 1 << (N - 2)

# rows of the per-item state matrix IT
INS, TAU, C1, STP, POS, LCK, DRT, WT = range(8)
# rows of the per-element state matrix EL
OWN, EST = range(2)
# scalars SC
S_STAMP, S_NSOL, S_SCORE, S_ESTAMP, S_NFREE, S_NUNDO, S_NDIRTY, S_LOCK, S_LOG, S_UNDOCAP, S_MINC1 = range(11)


def load_verifier():
    spec = importlib.util.spec_from_file_location("twodel_verifier", os.path.join(PROB, "verifier.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def w2s(w):
    return format(int(w), "016b")


def s2w(s):
    return int(s, 2)


# ----------------------------------------------------------------------------- precompute
@njit(cache=True)
def word_descendants():
    """CSR of distinct 2-deletion descendants per word. String position i <-> bit (15 - i)."""
    cnt = np.zeros(1 << N, np.int64)
    tmp = np.empty(N * (N - 1) // 2, np.int64)
    buf = np.empty((1 << N) * 120, np.int32)
    ptr = np.zeros((1 << N) + 1, np.int64)
    pos = 0
    for w in range(1 << N):
        t = 0
        for i in range(N - 1):
            for j in range(i + 1, N):
                # delete string positions i < j: bits b_i = 15-i > b_j = 15-j
                bi = N - 1 - i; bj = N - 1 - j
                hi = w >> (bi + 1)                       # string positions < i
                mid = (w >> (bj + 1)) & ((1 << (bi - bj - 1)) - 1)  # positions i+1..j-1
                lo = w & ((1 << bj) - 1)                 # positions > j
                d = (hi << (N - 2 - i)) | (mid << bj) | lo
                tmp[t] = d; t += 1
        s = np.sort(tmp[:t])
        last = -1
        for k in range(t):
            if s[k] != last:
                buf[pos] = s[k]; pos += 1; last = s[k]
        ptr[w + 1] = pos
    return ptr, buf[:pos].copy()


@njit(cache=True)
def build_parents(nitems, dptr, didx, ne):
    cnt = np.zeros(ne + 1, np.int64)
    for x in range(nitems):
        for k in range(dptr[x], dptr[x + 1]):
            cnt[didx[k] + 1] += 1
    for e in range(ne):
        cnt[e + 1] += cnt[e]
    fill = cnt[:-1].copy()
    pidx = np.empty(cnt[ne], np.int32)
    for x in range(nitems):
        for k in range(dptr[x], dptr[x + 1]):
            e = didx[k]
            pidx[fill[e]] = x; fill[e] += 1
    return cnt, pidx


def rev16(w):
    return int(format(w, "016b")[::-1], 2)


def orbit_items(group, wdptr, wdidx):
    """Return items (list of member-word lists), item CSR (union of descendants), weights."""
    comp = lambda w: w ^ 0xFFFF
    gens = {"none": [], "rev": [rev16], "comp": [comp], "rc": [lambda w: rev16(comp(w))],
            "full": [rev16, comp]}[group]
    seen = np.zeros(1 << N, bool)
    items, ptr, idx, wt = [], [0], [], []
    for w in range(1 << N):
        if seen[w]:
            continue
        orb = {w}; frontier = [w]
        while frontier:
            v = frontier.pop()
            for g in gens:
                u = g(v)
                if u not in orb:
                    orb.add(u); frontier.append(u)
        for v in orb:
            seen[v] = True
        orb = sorted(orb)
        ds = [wdidx[wdptr[v]:wdptr[v + 1]] for v in orb]
        tot = sum(len(d) for d in ds)
        u = np.unique(np.concatenate(ds))
        if len(u) != tot:          # two orbit members conflict: orbit can never be in a G-closed code
            continue
        items.append(orb); idx.append(u.astype(np.int32)); ptr.append(ptr[-1] + len(u)); wt.append(len(orb))
    return items, np.array(ptr, np.int64), np.concatenate(idx).astype(np.int32), np.array(wt, np.int64)


# ----------------------------------------------------------------------------- core moves
@njit(cache=True)
def push_dirty(x, IT, SC, dq):
    if IT[DRT, x] == 0:
        IT[DRT, x] = 1
        dq[SC[S_NDIRTY]] = x; SC[S_NDIRTY] += 1


@njit(cache=True)
def find_owner(w, skip, dptr, didx, EL):
    for k in range(dptr[w], dptr[w + 1]):
        o = EL[OWN, didx[k]]
        if o != -1 and o != skip:
            return o
    return -1


@njit(cache=True)
def nb_add(x, dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq):
    IT[INS, x] = 1
    IT[POS, x] = SC[S_NSOL]; sol[SC[S_NSOL]] = x; SC[S_NSOL] += 1
    SC[S_SCORE] += IT[WT, x]
    for k in range(dptr[x], dptr[x + 1]):
        EL[OWN, didx[k]] = x
    SC[S_STAMP] += 1; s = SC[S_STAMP]
    IT[STP, x] = s
    c = 0
    for k in range(dptr[x], dptr[x + 1]):
        e = didx[k]
        for m in range(pptr[e], pptr[e + 1]):
            w = pidx[m]
            if IT[STP, w] == s:
                continue
            IT[STP, w] = s
            t = IT[TAU, w] + 1
            IT[TAU, w] = t
            if t == 1:
                c += 1
            elif t == 2:
                y = find_owner(w, x, dptr, didx, EL)
                IT[C1, y] -= 1
    IT[C1, x] = c
    if c >= SC[S_MINC1]:
        push_dirty(x, IT, SC, dq)
    if SC[S_LOG] == 1:
        if SC[S_NUNDO] < SC[S_UNDOCAP]:
            undo[SC[S_NUNDO]] = x + 1; SC[S_NUNDO] += 1
        else:
            SC[S_LOG] = 2   # overflow: cannot undo this iteration


@njit(cache=True)
def nb_remove(x, dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq):
    IT[INS, x] = 0
    p = IT[POS, x]; last = sol[SC[S_NSOL] - 1]
    sol[p] = last; IT[POS, last] = p; SC[S_NSOL] -= 1
    SC[S_SCORE] -= IT[WT, x]
    for k in range(dptr[x], dptr[x + 1]):
        EL[OWN, didx[k]] = -1
    SC[S_STAMP] += 1; s = SC[S_STAMP]
    IT[STP, x] = s
    for k in range(dptr[x], dptr[x + 1]):
        e = didx[k]
        for m in range(pptr[e], pptr[e + 1]):
            w = pidx[m]
            if IT[STP, w] == s:
                continue
            IT[STP, w] = s
            t = IT[TAU, w] - 1
            IT[TAU, w] = t
            if t == 0:
                if SC[S_NFREE] < freel.shape[0]:
                    freel[SC[S_NFREE]] = w; SC[S_NFREE] += 1
            elif t == 1:
                y = find_owner(w, -1, dptr, didx, EL)
                IT[C1, y] += 1
                if IT[C1, y] >= SC[S_MINC1]:
                    push_dirty(y, IT, SC, dq)
    IT[C1, x] = 0
    if SC[S_NFREE] < freel.shape[0]:
        freel[SC[S_NFREE]] = x; SC[S_NFREE] += 1
    if SC[S_LOG] == 1:
        if SC[S_NUNDO] < SC[S_UNDOCAP]:
            undo[SC[S_NUNDO]] = -(x + 1); SC[S_NUNDO] += 1
        else:
            SC[S_LOG] = 2


@njit(cache=True)
def fill_free(dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq):
    # random order over the free candidates; prefer heavier then random
    n = SC[S_NFREE]
    while n > 0:
        r = np.random.randint(n)
        w = freel[r]; freel[r] = freel[n - 1]; n -= 1
        SC[S_NFREE] = n
        if IT[INS, w] == 0 and IT[TAU, w] == 0:
            nb_add(w, dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq)
            n = SC[S_NFREE]
    SC[S_NFREE] = 0


@njit(cache=True)
def try_swap(x, dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq, L):
    """Look for an improving (1,1) or (1,2) swap around solution item x; apply it. Returns True if applied."""
    SC[S_STAMP] += 1; s = SC[S_STAMP]
    IT[STP, x] = s
    nl = 0
    for k in range(dptr[x], dptr[x + 1]):
        e = didx[k]
        for m in range(pptr[e], pptr[e + 1]):
            w = pidx[m]
            if IT[STP, w] == s:
                continue
            IT[STP, w] = s
            if IT[TAU, w] == 1 and IT[INS, w] == 0 and nl < L.shape[0]:
                L[nl] = w; nl += 1
    if nl == 0:
        return False
    # shuffle
    for i in range(nl - 1, 0, -1):
        j = np.random.randint(i + 1)
        t = L[i]; L[i] = L[j]; L[j] = t
    wx = IT[WT, x]
    # (1,1) improving (weighted model only)
    for i in range(nl):
        if IT[WT, L[i]] > wx:
            u = L[i]
            nb_remove(x, dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq)
            nb_add(u, dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq)
            fill_free(dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq)
            return True
    if nl < 2:
        return False
    for i in range(nl - 1):
        u = L[i]
        SC[S_ESTAMP] += 1; es = SC[S_ESTAMP]
        for k in range(dptr[u], dptr[u + 1]):
            EL[EST, didx[k]] = es
        for j in range(i + 1, nl):
            v = L[j]
            if IT[WT, u] + IT[WT, v] <= wx:
                continue
            ok = True
            for k in range(dptr[v], dptr[v + 1]):
                if EL[EST, didx[k]] == es:
                    ok = False; break
            if ok:
                nb_remove(x, dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq)
                nb_add(u, dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq)
                nb_add(v, dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq)
                fill_free(dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq)
                return True
    return False


@njit(cache=True)
def local_search(dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq, L):
    fill_free(dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq)
    while SC[S_NDIRTY] > 0:
        r = np.random.randint(SC[S_NDIRTY])
        x = dq[r]; dq[r] = dq[SC[S_NDIRTY] - 1]; SC[S_NDIRTY] -= 1
        IT[DRT, x] = 0
        if IT[INS, x] == 0 or IT[LCK, x] == SC[S_LOCK] or IT[C1, x] < SC[S_MINC1]:
            continue
        try_swap(x, dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq, L)


@njit(cache=True)
def clear_queues(IT, SC, dq):
    for i in range(SC[S_NDIRTY]):
        IT[DRT, dq[i]] = 0
    SC[S_NDIRTY] = 0
    SC[S_NFREE] = 0


@njit(cache=True)
def force_insert(v, dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq):
    # remove every codeword conflicting with v, then insert v
    while True:
        y = find_owner(v, -1, dptr, didx, EL)
        if y == -1:
            break
        nb_remove(y, dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq)
    nb_add(v, dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq)


@njit(cache=True)
def undo_all(dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq):
    SC[S_LOG] = 0
    for i in range(SC[S_NUNDO] - 1, -1, -1):
        op = undo[i]
        if op > 0:
            nb_remove(op - 1, dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq)
        else:
            nb_add(-op - 1, dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq)
    SC[S_NUNDO] = 0
    clear_queues(IT, SC, dq)


@njit(cache=True)
def load_solution(items, dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq):
    SC[S_LOG] = 0
    while SC[S_NSOL] > 0:
        nb_remove(sol[SC[S_NSOL] - 1], dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq)
    clear_queues(IT, SC, dq)
    bad = 0
    for x in items:
        if IT[INS, x] == 0 and IT[TAU, x] == 0:
            nb_add(x, dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq)
        else:
            bad += 1
    return bad


@njit(cache=True)
def seed_rng(s):
    np.random.seed(s)


@njit(cache=True)
def ils_chunk(iters, perturb, restart, pmulti, dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq, L,
              best, bstate, nitems, accept):
    """Run `iters` ILS iterations. bstate = [best_score, best_n, since_best, total_iters]. Returns improved?"""
    improved = False
    for it in range(iters):
        bstate[3] += 1
        score0 = SC[S_SCORE]
        SC[S_NUNDO] = 0; SC[S_LOG] = 1
        SC[S_LOCK] += 1
        # k forced insertions (geometric tail)
        k = 1
        while k < 8 and np.random.random() < pmulti:
            k += 1
        for _ in range(k):
            v = -1; bt = 1 << 30
            for tries in range(4000):
                c = np.random.randint(nitems)
                if IT[INS, c] == 1:
                    continue
                t = IT[TAU, c]
                if t <= perturb and t >= 1:
                    v = c; break
                if t < bt:
                    bt = t; v = c
            if v == -1:
                continue
            force_insert(v, dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq)
            IT[LCK, v] = SC[S_LOCK]
        local_search(dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq, L)
        score1 = SC[S_SCORE]
        if score1 > bstate[0]:
            bstate[0] = score1; bstate[1] = SC[S_NSOL]; bstate[2] = 0
            for i in range(SC[S_NSOL]):
                best[i] = sol[i]
            improved = True
        else:
            bstate[2] += 1
        if score1 < score0 and SC[S_LOG] == 1:
            d = score0 - score1; ds = bstate[0] - score1
            if accept == 1 or np.random.random() >= 1.0 / (1.0 + d * ds):   # accept=1: plateau-only walk
                undo_all(dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq)
        SC[S_LOG] = 0
        clear_queues(IT, SC, dq)
        if bstate[2] >= restart:
            bstate[2] = 0
            load_solution(best[:bstate[1]].copy(), dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq)
        if improved:
            return True
    return improved


# ----------------------------------------------------------------------------- fixed-k tabu (algo=tabu)
# State: k items in C; cover[e]; f = sum_e max(0, cover[e]-1) (0 <=> valid packing);
# occ[w] = #{e in D(w): cover[e] >= 1}, kept in a bucket-sorted array (ordb / posb / bst) for O(1) updates.
# Move: pick a random conflicting member x, swap it for the non-tabu item y minimising the new f
# (delta = occ[y] - common1(x,y) - conf_in(x)); x is tabu to re-enter for ~tenure moves. f == 0 -> record the
# code, then grow k by one (insert the min-occ item) and continue.
@njit(cache=True)
def tb_occ_inc(w, occ, ordb, posb, bst):
    v = occ[w]
    j = bst[v + 1] - 1            # last slot of bucket v
    u = ordb[j]; p = posb[w]
    ordb[p] = u; posb[u] = p; ordb[j] = w; posb[w] = j
    bst[v + 1] -= 1
    occ[w] = v + 1


@njit(cache=True)
def tb_occ_dec(w, occ, ordb, posb, bst):
    v = occ[w]
    j = bst[v]                    # first slot of bucket v
    u = ordb[j]; p = posb[w]
    ordb[p] = u; posb[u] = p; ordb[j] = w; posb[w] = j
    bst[v] += 1
    occ[w] = v - 1


@njit(cache=True)
def tb_add(x, dptr, didx, pptr, pidx, cover, occ, ordb, posb, bst, inC, F):
    inC[x] = 1
    for k in range(dptr[x], dptr[x + 1]):
        e = didx[k]
        c = cover[e]; cover[e] = c + 1
        if c >= 1:
            F[0] += 1
        else:
            for m in range(pptr[e], pptr[e + 1]):
                tb_occ_inc(pidx[m], occ, ordb, posb, bst)


@njit(cache=True)
def tb_remove(x, dptr, didx, pptr, pidx, cover, occ, ordb, posb, bst, inC, F):
    inC[x] = 0
    for k in range(dptr[x], dptr[x + 1]):
        e = didx[k]
        c = cover[e]; cover[e] = c - 1
        if c >= 2:
            F[0] -= 1
        else:
            for m in range(pptr[e], pptr[e + 1]):
                tb_occ_dec(pidx[m], occ, ordb, posb, bst)


@njit(cache=True)
def tb_conf(x, dptr, didx, cover):
    c = 0
    for k in range(dptr[x], dptr[x + 1]):
        if cover[didx[k]] >= 2:
            c += 1
    return c


@njit(cache=True)
def tb_best_global(occ, ordb, bst, inC, tabu, it, skip, maxv, limit_val):
    """random non-C, non-tabu item with minimal occ (< limit_val); -1 if none."""
    for v in range(maxv + 1):
        if v >= limit_val:
            return -1, v
        lo = bst[v]; hi = bst[v + 1]
        if hi <= lo:
            continue
        cnt = 0; pick = -1
        scan = hi - lo
        if scan > 256:
            scan = 256
        off = np.random.randint(hi - lo)
        for q in range(scan):
            y = ordb[lo + (off + q) % (hi - lo)]
            if inC[y] == 1 or y == skip or tabu[y] > it:
                continue
            cnt += 1
            if np.random.randint(cnt) == 0:
                pick = y
        if pick != -1:
            return pick, v
    return -1, maxv + 1


@njit(cache=True)
def tabu_chunk(steps, tenure, dptr, didx, pptr, pidx, cover, occ, ordb, posb, bst, inC, F, members, tabu, acc,
               stamp, tst, maxv):
    """members: int32[k_max] items in C (first tst[1] used); tst = [it, k, bestF_at_k, stamp]."""
    for s in range(steps):
        tst[0] += 1; it = tst[0]
        k = tst[1]
        if F[0] == 0:
            return 1
        # pick a random conflicting member
        x = -1; xi = -1
        for tries in range(4 * k + 64):
            q = np.random.randint(k)
            if tb_conf(members[q], dptr, didx, cover) > 0:
                x = members[q]; xi = q; break
        if x == -1:
            for q in range(k):
                if tb_conf(members[q], dptr, didx, cover) > 0:
                    x = members[q]; xi = q; break
        gx = tb_conf(x, dptr, didx, cover)
        # neighbours y with common1(x, y) > 0
        tst[3] += 1; st = tst[3]
        nb = 0
        bestv = 1 << 30; besty = -1; nties = 0
        for kk in range(dptr[x], dptr[x + 1]):
            e = didx[kk]
            if cover[e] != 1:
                continue
            for m in range(pptr[e], pptr[e + 1]):
                y = pidx[m]
                if stamp[y] != st:
                    stamp[y] = st; acc[y] = 0
                acc[y] += 1
        for kk in range(dptr[x], dptr[x + 1]):
            e = didx[kk]
            if cover[e] != 1:
                continue
            for m in range(pptr[e], pptr[e + 1]):
                y = pidx[m]
                if stamp[y] != st or inC[y] == 1 or y == x:
                    continue
                val = occ[y] - acc[y]
                stamp[y] = st - 1 if st > 1 else -5        # visit once
                newF = F[0] - gx + val
                if tabu[y] > it and not newF < tst[2]:
                    continue
                if val < bestv:
                    bestv = val; besty = y; nties = 1
                elif val == bestv:
                    nties += 1
                    if np.random.randint(nties) == 0:
                        besty = y
        gy, gv = tb_best_global(occ, ordb, bst, inC, tabu, it, x, maxv, bestv + 1)
        if gy != -1 and (gv < bestv or (gv == bestv and np.random.random() < 0.5)):
            besty = gy; bestv = gv
        if besty == -1:
            continue
        tb_remove(x, dptr, didx, pptr, pidx, cover, occ, ordb, posb, bst, inC, F)
        tb_add(besty, dptr, didx, pptr, pidx, cover, occ, ordb, posb, bst, inC, F)
        members[xi] = besty
        tabu[x] = it + tenure + np.random.randint(tenure // 2 + 1)
        if F[0] < tst[2]:
            tst[2] = F[0]
        if F[0] == 0:
            return 1
    return 0


def run_tabu(a, tag, t0, dptr, didx, pptr, pidx, wt, init_items, words_of, ver):
    nitems = len(dptr) - 1
    sizes = np.diff(dptr)
    maxv = int(sizes.max())
    occ = np.zeros(nitems, np.int64)
    ordb = np.argsort(occ, kind="stable").astype(np.int64); posb = np.empty(nitems, np.int64); posb[ordb] = np.arange(nitems)
    bst = np.zeros(maxv + 2, np.int64); bst[1:] = nitems    # all items in bucket 0
    cover = np.zeros(NE, np.int64); inC = np.zeros(nitems, np.int8); F = np.zeros(1, np.int64)
    tabu = np.zeros(nitems, np.int64); acc = np.zeros(nitems, np.int64); stamp = np.zeros(nitems, np.int64)
    kmax = 4096
    members = np.zeros(kmax, np.int64)
    k = 0
    for x in init_items:
        tb_add(int(x), dptr, didx, pptr, pidx, cover, occ, ordb, posb, bst, inC, F)
        members[k] = x; k += 1
    assert F[0] == 0, "initial code is not a valid packing"
    best_items = members[:k].copy(); best_score = int(wt[best_items].sum())
    rng = np.random.default_rng(a.seed + 7)

    def grow():
        nonlocal k
        # insert the non-member with the fewest covered descendants (random tie-break)
        cand = np.flatnonzero(inC == 0)
        o = occ[cand]
        y = int(rng.choice(cand[o == o.min()]))
        tb_add(y, dptr, didx, pptr, pidx, cover, occ, ordb, posb, bst, inC, F)
        members[k] = y; k += 1

    grow()
    tst = np.array([0, k, F[0], 1], np.int64)
    sid = os.environ.get("PHOENIX_STRATEGY_ID")      # set by the backend launcher: unique file names per strategy
    best_file = os.path.join(a.out, f"best_{sid}.json" if sid else f"best_{a.mode}_tabu_s{a.seed}.json")

    def save(items):
        words = words_of(items.tolist())
        score = ver.evaluate({"words": words})
        json.dump({"mode": a.mode, "algo": "tabu", "seed": a.seed, "count": len(words), "t": round(time.time() - t0, 1),
                   "iters": int(tst[0]), "words": sorted(words)}, open(best_file + ".tmp", "w"))
        os.replace(best_file + ".tmp", best_file)
        if len(words) > a.target:
            fn = os.path.join(a.out, f"FOUND_{sid or a.mode + '_tabu_s' + str(a.seed)}_{len(words)}.json")
            json.dump({"solution": {"words": sorted(words)}, "score": score, "mode": a.mode, "algo": "tabu",
                       "seed": a.seed, "t": round(time.time() - t0, 1)}, open(fn, "w"))
            print(f"FOUND two-deletion code of size {len(words)} verified by official verifier -> {fn}", flush=True)
        return score

    save(best_items)
    print(f"{tag} t={time.time()-t0:.0f}s best={best_score} iters=0 algo=tabu k={k} conflicts={int(F[0])}", flush=True)
    last_hb = time.time(); chunk = 5000; last_bestF = int(tst[2])
    while time.time() - t0 < a.seconds:
        c0 = time.time(); i0 = int(tst[0])
        done = tabu_chunk(chunk, a.tenure, dptr, didx, pptr, pidx, cover, occ, ordb, posb, bst, inC, F, members,
                          tabu, acc, stamp, tst, maxv)
        dt = max(time.time() - c0, 1e-3)
        chunk = int(min(max((int(tst[0]) - i0) / dt, 100), 1 << 22))
        if done:
            # fixed-k tabu counts items; with orbit items (symmetric mode) a valid k-item packing can weigh LESS
            # than the best so far, so only a heavier packing replaces the saved best (the best never goes down)
            items_k = members[:k].copy(); score_k = int(wt[items_k].sum())
            if score_k > best_score:
                best_items = items_k; best_score = score_k
                score = save(best_items)
                assert int(score) == best_score
                print(f"{tag} t={time.time()-t0:.0f}s best={best_score} iters={int(tst[0])} algo=tabu", flush=True)
            else:
                print(f"{tag} t={time.time()-t0:.0f}s best={best_score} iters={int(tst[0])} algo=tabu k={k} "
                      f"valid_k_words={score_k}", flush=True)
            grow(); tst[1] = k; tst[2] = F[0]; last_bestF = int(F[0])
        if time.time() - last_hb > 60:
            last_hb = time.time()
            print(f"{tag} t={time.time()-t0:.0f}s best={best_score} k={k} conflicts={int(F[0])} "
                  f"min_conflicts={int(tst[2])} iters={int(tst[0])} rate={tst[0]/(time.time()-t0):.0f}/s", flush=True)
    print(f"{tag} done t={time.time()-t0:.0f}s best={best_score} iters={int(tst[0])} algo=tabu", flush=True)


# ----------------------------------------------------------------------------- driver
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--mode", default="from_record", choices=["from_record", "from_scratch", "symmetric"])
    ap.add_argument("--algo", default="ils", choices=["ils", "tabu"], help="ARW iterated local search or fixed-k tabu")
    ap.add_argument("--tenure", type=int, default=15, help="tabu tenure (algo=tabu)")
    ap.add_argument("--group", default="full", choices=["rev", "comp", "rc", "full"], help="symmetric mode only")
    ap.add_argument("--rank", type=int, default=0, help="from_record: which public solution (0 = best)")
    ap.add_argument("--init-file", default=None, help="optional JSON with {'words': [...]} to start from")
    ap.add_argument("--perturb", type=int, default=1, help="max tightness of a force-inserted word (1 = plateau swaps)")
    ap.add_argument("--pmulti", type=float, default=0.15, help="prob. of each extra forced insertion")
    ap.add_argument("--accept", default="arw", choices=["arw", "plateau"],
                    help="arw: accept worse w.p. 1/(1+d*d*) (ARW 2012); plateau: never accept a worse solution")
    ap.add_argument("--restart", type=int, default=50000, help="non-improving iterations before return to best")
    ap.add_argument("--seconds", type=float, default=3600 * 6)
    ap.add_argument("--target", type=int, default=226, help="record to beat (FOUND when size > target)")
    ap.add_argument("--out", default="runs/twodel")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    tag = f"[twodel s{a.seed}]"
    ver = load_verifier()
    t0 = time.time()
    seed_rng(a.seed); rng = np.random.default_rng(a.seed)

    wdptr, wdidx = word_descendants()
    if a.mode == "symmetric":
        members, dptr, didx, wt = orbit_items(a.group, wdptr, wdidx)
        item_of = {}
        for i, orb in enumerate(members):
            for v in orb:
                item_of[v] = i
    else:
        members = None
        dptr, didx = wdptr, wdidx
        wt = np.ones(1 << N, np.int64)
    nitems = len(dptr) - 1
    pptr, pidx = build_parents(nitems, dptr, didx, NE)
    IT = np.zeros((8, nitems), np.int64); IT[WT] = wt; IT[LCK] = -1
    EL = np.zeros((2, NE), np.int64); EL[OWN] = -1
    SC = np.zeros(11, np.int64)
    SC[S_UNDOCAP] = 1 << 20
    SC[S_MINC1] = 1 if a.mode == "symmetric" else 2
    sol = np.zeros(nitems, np.int32); best = np.zeros(nitems, np.int32)
    freel = np.zeros(4 * nitems + 16, np.int32); undo = np.zeros(1 << 20, np.int32)
    dq = np.zeros(nitems + 1, np.int32); L = np.zeros(8192, np.int32)

    def words_of(item_list):
        if members is None:
            return [w2s(x) for x in item_list]
        return [w2s(v) for x in item_list for v in members[x]]

    # ---- initial solution
    init = []
    if a.init_file:
        init = [s2w(s) for s in json.load(open(a.init_file))["words"]]
    elif a.mode == "from_record":
        recs = json.load(open(os.path.join(PROB, "best_solutions.json")))
        init = [s2w(s) for s in recs[min(a.rank, len(recs) - 1)]["data"]["words"]]
    if members is not None and init:
        init = sorted({item_of[w] for w in init if w in item_of})
    if not init:   # randomized min-ball greedy: small descendant sets first
        sizes = np.diff(dptr).astype(float) / wt
        order = np.argsort(sizes + rng.random(nitems) * 3.0)
        init = list(order)
    bad = load_solution(np.array(init, np.int32), dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq)
    if a.init_file or a.mode == "from_record":
        print(f"{tag} init {a.mode} items={len(init)} rejected={bad}", flush=True)
    SC[S_LOG] = 0
    local_search(dptr, didx, pptr, pidx, IT, EL, SC, sol, freel, undo, dq, L)
    clear_queues(IT, SC, dq)
    bstate = np.array([SC[S_SCORE], SC[S_NSOL], 0, 0], np.int64)
    best[:SC[S_NSOL]] = sol[:SC[S_NSOL]]
    print(f"{tag} setup mode={a.mode}{' group=' + a.group if members is not None else ''} items={nitems} "
          f"desc_entries={len(didx)} t={time.time()-t0:.1f}s start={SC[S_SCORE]}", flush=True)

    if a.algo == "tabu":
        run_tabu(a, tag, t0, dptr, didx, pptr, pidx, wt, sol[:SC[S_NSOL]].copy(), words_of, ver)
        return
    sid = os.environ.get("PHOENIX_STRATEGY_ID")      # set by the backend launcher: unique file names per strategy
    best_file = os.path.join(a.out, f"best_{sid}.json" if sid else
                             f"best_{a.mode}{'_' + a.group if members is not None else ''}_s{a.seed}.json")
    last_saved = -1

    def save_best():
        nonlocal last_saved
        words = words_of(best[:bstate[1]].tolist())
        score = ver.evaluate({"words": words})          # official verifier; raises if invalid
        assert int(score) == int(bstate[0]), (score, bstate[0])
        json.dump({"mode": a.mode, "group": a.group if members is not None else None, "seed": a.seed,
                   "count": len(words), "t": round(time.time() - t0, 1), "iters": int(bstate[3]),
                   "words": sorted(words)}, open(best_file + ".tmp", "w"))
        os.replace(best_file + ".tmp", best_file)
        last_saved = len(words)
        if len(words) > a.target:
            fn = os.path.join(a.out, f"FOUND_{sid or a.mode + '_s' + str(a.seed)}_{len(words)}.json")
            json.dump({"solution": {"words": sorted(words)}, "score": score, "mode": a.mode, "seed": a.seed,
                       "t": round(time.time() - t0, 1)}, open(fn, "w"))
            print(f"FOUND two-deletion code of size {len(words)} verified by official verifier -> {fn}", flush=True)

    save_best()
    print(f"{tag} t={time.time()-t0:.0f}s best={int(bstate[0])} iters=0", flush=True)
    last_hb = time.time(); chunk = 2000
    while time.time() - t0 < a.seconds:
        c0 = time.time(); i0 = int(bstate[3])
        improved = ils_chunk(chunk, a.perturb, a.restart, a.pmulti, dptr, didx, pptr, pidx, IT, EL, SC, sol,
                             freel, undo, dq, L, best, bstate, nitems, 1 if a.accept == "plateau" else 0)
        dt = max(time.time() - c0, 1e-3)
        rate = (int(bstate[3]) - i0) / dt
        chunk = int(min(max(rate * 1.0, 50), 1 << 22))   # ~1 s per chunk
        if improved:
            save_best()
            print(f"{tag} t={time.time()-t0:.0f}s best={int(bstate[0])} iters={int(bstate[3])}", flush=True)
        if time.time() - last_hb > 60:
            last_hb = time.time()
            print(f"{tag} t={time.time()-t0:.0f}s best={int(bstate[0])} cur={int(SC[S_SCORE])} "
                  f"iters={int(bstate[3])} rate={bstate[3]/(time.time()-t0):.0f}/s", flush=True)
    print(f"{tag} done t={time.time()-t0:.0f}s best={int(bstate[0])} iters={int(bstate[3])}", flush=True)


if __name__ == "__main__":
    main()
