"""Fixed-k min-conflict search with DYNAMIC DESCENDANT WEIGHTS for two-deletion-correcting codes of length 16
(EinsteinArena 'two-deletion-code-16', record 226 by kgrey). CPU, single core, numba.

Model: a code is a set of 16-bit words whose 2-deletion descendant sets (subsets of the 16,384 length-14 words)
are pairwise disjoint. We hold exactly k words (k = 227 by default = record + 1) and minimise
    cost = sum_d w[d] * max(0, cnt[d] - 1),      cnt[d] = number of chosen words that have descendant d,
where w[d] >= 1 is a dynamic weight (breakout / NuMVC style). cost == 0  <=>  a valid code of size k.

Move = swap (remove one conflicting word u, add an outside word v). Every step evaluates, for every conflicting
non-tabu word u, the exact best partner v using A[v] = sum_{d in desc(v), cnt[d] >= 1} w[d] (maintained
incrementally for all 65,536 words) and R[u] = sum_{d in desc(u), cnt[d] >= 2} w[d]:
    delta(u, v) = A[v] - sum_{d in desc(u) & desc(v), cnt[d] == 1} w[d] - R[u].
  * delta <= 0: do the swap (ties random). With prob --noise u is a random conflicting word instead.
  * tabu: a word cannot be removed for 1..--tenure steps after it was added; configuration checking: a word
    that left the code may only come back after the coverage of one of its descendants has changed;
  * delta >= 0 (local minimum of the weighted cost): breakout, w[d] += 1 for every descendant covered 2+ times
    (no uphill move unless --force); every --decay bumps the weights are smoothed towards the base weight
    w = w0 + floor(rho * (w - w0));
  * weights are capped at --wcap; if every over-covered descendant is at the cap the best swap is forced (uphill);
  * elite: the configuration with the least over-coverage is kept; when the walk strays more than --band
    over-covered descendants above it, it returns to the elite with the learned weights kept, so the next
    excursion leaves in a different direction;
  * stagnation (--restart steps without a new minimum): weights reset, --kick random words re-inserted greedily.
Starts from different basins: --init record0..record4 (the 5 public codes padded to k by best-weighted insertion)
or scratch (greedy).
Exact repair: when at most --repair-at words are in conflict (4 = two disjoint pairs), free the conflicting words, the chosen words within
Hamming distance 2 of them and their nearest chosen neighbours (--repair-r words, then 3x as many), list every
word compatible with the kept words and ask CaDiCaL (pysat) for a packing of the same number of words.
SAT -> a valid code of size k. Every claimed code is checked with the OFFICIAL verifier; FOUND_*.json is written
only when the verified score beats the record. After a success the search continues with k + 1.

Log: [twodel_w s<seed>] t=..s best=<largest valid code held> conf=<fewest conflicting pairs at size k>
     cwords=<conflicting words> over=<over-covered descendants> k=.. steps=.. rate=<steps per CPU second> restarts=..
     repairs=<sat>/<unsat>/<timeout> ...
"""
import argparse, importlib.util, json, os, sys, time

os.environ.setdefault("NUMBA_CACHE_DIR", os.path.expanduser("~/.cache/ltd_numba"))
import numpy as np
from numba import njit

L = 16
N = 1 << L
ND = 1 << (L - 2)
HERE = os.path.dirname(os.path.abspath(__file__))
PROB = os.path.join(HERE, "..", "problems", "two-deletion-code-16")
FAM = "twodel_w"


def load_verifier():
    spec = importlib.util.spec_from_file_location("twodel_verifier", os.path.join(PROB, "verifier.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def to_str(w):
    return format(int(w), f"0{L}b")


def build_tables():
    """D[x, :nd[x]] = distinct 2-deletion descendants of word x (as ints, MSB first like the verifier strings);
    inverse CSR (ip, ix): words that have descendant d."""
    words = np.arange(N, dtype=np.int64)
    bits = ((words[:, None] >> np.arange(L - 1, -1, -1)) & 1).astype(np.int64)
    pw = 1 << np.arange(L - 3, -1, -1)
    cols = []
    for i in range(L - 1):
        for j in range(i + 1, L):
            keep = [q for q in range(L) if q != i and q != j]
            cols.append(bits[:, keep] @ pw)
    D = np.sort(np.stack(cols, 1), 1)
    dup = np.zeros(D.shape, dtype=bool); dup[:, 1:] = D[:, 1:] == D[:, :-1]
    D[dup] = ND                                               # sentinel, sorts last
    D = np.sort(D, 1)
    nd = (D < ND).sum(1).astype(np.int32)
    D = np.ascontiguousarray(D[:, :nd.max()]).astype(np.int32)
    xs, js = np.nonzero(D < ND)
    ds = D[xs, js]
    order = np.argsort(ds, kind="stable")
    ix = xs[order].astype(np.int32)
    ip = np.zeros(ND + 1, dtype=np.int64)
    np.cumsum(np.bincount(ds, minlength=ND), out=ip[1:])
    return D, nd, ip, ix


@njit(cache=True)
def seed_rng(s):
    np.random.seed(s)


@njit(cache=True)
def recompute_A(D, nd, cnt, w, A):
    for x in range(D.shape[0]):
        s = 0
        for j in range(nd[x]):
            d = D[x, j]
            if cnt[d] >= 1:
                s += w[d]
        A[x] = s


@njit(cache=True)
def add_word(x, D, nd, ip, ix, cnt, w, A, lastchg, tick):
    dc = 0
    for j in range(nd[x]):
        d = D[x, j]
        c = cnt[d]; cnt[d] = c + 1; lastchg[d] = tick
        if c == 0:
            wd = w[d]
            for q in range(ip[d], ip[d + 1]):
                A[ix[q]] += wd
        else:
            dc += 1
    return dc


@njit(cache=True)
def remove_word(x, D, nd, ip, ix, cnt, w, A, lastchg, tick):
    dc = 0
    for j in range(nd[x]):
        d = D[x, j]
        c = cnt[d]; cnt[d] = c - 1; lastchg[d] = tick
        if c == 1:
            wd = w[d]
            for q in range(ip[d], ip[d + 1]):
                A[ix[q]] -= wd
        else:
            dc -= 1
    return dc


@njit(cache=True)
def pick_add(D, nd, A, inS, t_rem, lastchg, forbid):
    """Outside word with the smallest weighted insertion cost that passes configuration checking."""
    best = np.int64(1) << 60; nt = 0; pick = -1
    for x in range(D.shape[0]):
        if inS[x] or x == forbid:
            continue
        a = A[x]
        if a > best:
            continue
        tr = t_rem[x]
        if tr >= 0:
            ok = False
            for j in range(nd[x]):
                if lastchg[D[x, j]] > tr:
                    ok = True; break
            if not ok:
                continue
        if a < best:
            best = a; nt = 1; pick = x
        else:
            nt += 1
            if np.random.randint(nt) == 0:
                pick = x
    return pick


@njit(cache=True)
def search(D, nd, ip, ix, cnt, w, A, inS, S, t_rem, tabu_until, lastchg, stamp, st, Sbest, tmp, touched,
           max_steps, tenure, noise, decay, rho, w0, force, band, wcap, cand):
    """st = [step, tick, over-coverage, nbumps, chunk-best conflicting words, stampid, sum of conflicting words over
    steps, over-coverage of the chunk-best]. Runs up to max_steps steps; stops at over-coverage == 0.
    Sbest is the elite: the configuration with the least over-coverage (ties: fewest conflicting words).
    Each step evaluates the exact best swap (u out, v in) for every non-tabu conflicting word u:
        delta(u, v) = A[v] - sum_{d in desc(u) & desc(v), cnt[d] == 1} w[d] - R[u]."""
    k = S.shape[0]
    BIG = np.int64(1) << 60
    step = st[0]; tick = st[1]; conf = st[2]; nb = st[3]; sid = st[5]
    cbest = st[4]; cover = st[7]                              # elite (persists across calls until a kick)
    R = np.zeros(k, dtype=np.int64)
    done = 0; csum = st[6]; stuck = False
    while done < max_steps and conf > 0:
        done += 1; step += 1
        nconf = 0
        for i in range(k):
            x = S[i]; r = 0
            for j in range(nd[x]):
                d = D[x, j]
                if cnt[d] >= 2:
                    r += w[d]
            R[i] = r
            if r > 0:
                nconf += 1
        csum += nconf
        if conf < cover or (conf == cover and nconf <= cbest):  # '<=': the elite drifts along its plateau
            cbest = nconf; cover = conf
            Sbest[:] = S
        elif conf > cover + band:                             # strayed too far: back to the elite, keep the weights
            for i in range(k):
                if S[i] != Sbest[i]:
                    tick += 1
                    conf += remove_word(S[i], D, nd, ip, ix, cnt, w, A, lastchg, tick)
                    inS[S[i]] = 0; t_rem[S[i]] = tick
            for i in range(k):
                if S[i] != Sbest[i]:
                    tick += 1
                    conf += add_word(Sbest[i], D, nd, ip, ix, cnt, w, A, lastchg, tick)
                    inS[Sbest[i]] = 1; S[i] = Sbest[i]
            st[8] += 1
            continue
        g = pick_add(D, nd, A, inS, t_rem, lastchg, -1)        # best insertion that shares nothing private with u
        Ag = A[g] if g >= 0 else BIG
        rnd = np.random.random() < noise
        ru = -1
        if rnd:
            pickn = np.random.randint(nconf)
            for i in range(k):
                if R[i] > 0:
                    if pickn == 0:
                        ru = i; break
                    pickn -= 1
        bestd = BIG; bu = -1; bv = -1; nt = 0
        for p in range(2):                                    # pass 0 honours tabu, pass 1 ignores it
            for i in range(k):
                if R[i] == 0:
                    continue
                if rnd:
                    if i != ru:
                        continue
                elif p == 0 and tabu_until[S[i]] > step:
                    continue
                elif nconf > cand and np.random.randint(nconf) >= cand:
                    continue                                  # many conflicting words: evaluate a random subset
                u = S[i]
                ntch = 0
                for j in range(nd[u]):
                    d = D[u, j]
                    if cnt[d] == 1:
                        wd = w[d]
                        for q in range(ip[d], ip[d + 1]):
                            x = ix[q]
                            if inS[x]:
                                continue
                            if tmp[x] == 0:
                                touched[ntch] = x; ntch += 1
                            tmp[x] += wd
                mv = Ag; v = g; ntv = 1
                for t in range(ntch):
                    x = touched[t]
                    val = A[x] - tmp[x]; tmp[x] = 0
                    if val > mv:
                        continue
                    tr = t_rem[x]
                    if tr >= 0:
                        ok = False
                        for j in range(nd[x]):
                            if lastchg[D[x, j]] > tr:
                                ok = True; break
                        if not ok:
                            continue
                    if val < mv:
                        mv = val; v = x; ntv = 1
                    else:
                        ntv += 1
                        if np.random.randint(ntv) == 0:
                            v = x
                if v < 0:
                    continue
                dl = mv - R[i]
                if dl < bestd:
                    bestd = dl; bu = i; bv = v; nt = 1
                elif dl == bestd:
                    nt += 1
                    if np.random.randint(nt) == 0:
                        bu = i; bv = v
            if bu >= 0:
                break
        if bu >= 0 and (bestd <= 0 or rnd or stuck or np.random.random() < force):
            u = S[bu]
            tick += 1
            conf += remove_word(u, D, nd, ip, ix, cnt, w, A, lastchg, tick)
            inS[u] = 0; t_rem[u] = tick
            tick += 1
            conf += add_word(bv, D, nd, ip, ix, cnt, w, A, lastchg, tick)
            inS[bv] = 1; S[bu] = bv
            tabu_until[bv] = step + 1 + np.random.randint(tenure)
        if bu >= 0 and bestd < 0:
            stuck = False
        if bestd >= 0 and conf > 0:                           # local minimum of the weighted cost: breakout
            sid += 1; nb += 1
            stuck = True                                      # all over-covered weights at the cap: force a move next
            for i in range(k):
                x = S[i]
                for j in range(nd[x]):
                    d = D[x, j]
                    if cnt[d] >= 2 and stamp[d] != sid and w[d] < wcap:
                        stamp[d] = sid; stuck = False
                        w[d] += 1
                        for q in range(ip[d], ip[d + 1]):
                            A[ix[q]] += 1
            if nb % decay == 0:
                for d in range(w.shape[0]):
                    if w[d] > w0:
                        nw = w0 + np.int64(rho * (w[d] - w0))
                        if cnt[d] >= 1:
                            dl2 = w[d] - nw
                            for q in range(ip[d], ip[d + 1]):
                                A[ix[q]] -= dl2
                        w[d] = nw
    if conf == 0:
        cbest = 0; cover = 0
        Sbest[:] = S
    st[0] = step; st[1] = tick; st[2] = conf; st[3] = nb; st[4] = cbest; st[5] = sid; st[6] = csum; st[7] = cover
    return done


class State:
    def __init__(self, T, k, w0=1):
        self.T = T; self.k = k; self.w0 = w0
        self.cnt = np.zeros(ND, dtype=np.int32); self.w = np.full(ND, w0, dtype=np.int64)
        self.A = np.zeros(N, dtype=np.int64); self.inS = np.zeros(N, dtype=np.int8)
        self.S = np.zeros(k, dtype=np.int32); self.Sbest = np.zeros(k, dtype=np.int32)
        self.t_rem = np.full(N, -1, dtype=np.int64); self.tabu = np.zeros(N, dtype=np.int64)
        self.lastchg = np.zeros(ND, dtype=np.int64); self.stamp = np.zeros(ND, dtype=np.int64)
        self.st = np.zeros(9, dtype=np.int64); self.n = 0
        self.st[4] = 1 << 40; self.st[7] = 1 << 40
        self.tmp = np.zeros(N, dtype=np.int64); self.touched = np.zeros(N, dtype=np.int32)

    def _add(self, x):
        D, nd, ip, ix = self.T
        self.st[1] += 1
        self.st[2] += add_word(x, D, nd, ip, ix, self.cnt, self.w, self.A, self.lastchg, self.st[1])
        self.inS[x] = 1

    def fill(self, words):
        """Start from `words` (may be empty) and pad to k by best-weighted insertion."""
        for x in words[:self.k]:
            self._add(int(x)); self.S[self.n] = x; self.n += 1
        D, nd, ip, ix = self.T
        while self.n < self.k:
            v = pick_add(D, nd, self.A, self.inS, self.t_rem, self.lastchg, -1)
            self._add(v); self.S[self.n] = v; self.n += 1

    def kick(self, m, rng):
        """Reset weights and memory; replace m random words by greedy insertions."""
        D, nd, ip, ix = self.T
        self.w[:] = self.w0; self.t_rem[:] = -1; self.tabu[:] = 0; self.st[4] = 1 << 40; self.st[7] = 1 << 40
        recompute_A(D, nd, self.cnt, self.w, self.A)
        slots = rng.choice(self.k, size=min(m, self.k), replace=False)
        out = []
        for i in slots:
            u = int(self.S[i]); self.st[1] += 1
            self.st[2] += remove_word(u, D, nd, ip, ix, self.cnt, self.w, self.A, self.lastchg, self.st[1])
            self.inS[u] = 0; out.append(u)
        for n_, i in enumerate(slots):
            v = pick_add(D, nd, self.A, self.inS, self.t_rem, self.lastchg, out[n_])
            self._add(v); self.S[i] = v

    def run(self, steps, a):
        D, nd, ip, ix = self.T
        return search(D, nd, ip, ix, self.cnt, self.w, self.A, self.inS, self.S, self.t_rem, self.tabu,
                      self.lastchg, self.stamp, self.st, self.Sbest, self.tmp, self.touched, steps, a.tenure, a.noise,
                      a.decay, a.rho, a.w0, a.force, a.band, a.wcap, a.cand)


def conflict_info(T, words):
    """(conflicting pairs, sorted list of words that share a descendant with another word)."""
    D, nd = T[0], T[1]
    owner = {}
    pairs = set()
    for x in words:
        for d in D[x, :nd[x]].tolist():
            owner.setdefault(d, []).append(int(x))
    for lst in owner.values():
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                pairs.add((lst[i], lst[j]))
    return pairs, sorted({x for p in pairs for x in p})


def valid_subcode(T, words):
    """Greedy: drop the word with most conflict partners until no conflict remains."""
    words = [int(x) for x in words]
    while True:
        pairs, bad = conflict_info(T, words)
        if not pairs:
            return words
        deg = {}
        for p, q in pairs:
            deg[p] = deg.get(p, 0) + 1; deg[q] = deg.get(q, 0) + 1
        words.remove(max(bad, key=lambda x: deg[x]))


def exact_repair(T, words, r, budget):
    """Free the conflicting words + chosen words within Hamming distance 2 + nearest chosen words up to r words in
    total; ask CaDiCaL for as many pairwise-disjoint compatible words. Returns (status, code or None, freed)."""
    from pysat.card import CardEnc, EncType
    from pysat.formula import IDPool
    from pysat.solvers import Solver
    D, nd = T[0], T[1]
    words = [int(x) for x in words]
    _, bad = conflict_info(T, words)
    dist = {x: min(bin(x ^ c).count("1") for c in bad) for x in words}
    order = sorted(words, key=lambda x: (dist[x], x))
    nfree = max(r, sum(1 for x in words if dist[x] <= 2))
    freed = order[:nfree]; kept = order[nfree:]
    blocked = np.zeros(ND + 1, dtype=bool)
    if kept:
        blocked[D[kept].ravel()] = True
    blocked[ND] = False                                       # padding sentinel
    cand = np.nonzero(~blocked[D].any(1))[0]
    if len(cand) < nfree:
        return "unsat", None, nfree
    pool = IDPool()
    var = {int(x): pool.id(int(x)) for x in cand}
    by = {}
    for x in cand:
        for d in D[x, :nd[x]].tolist():
            by.setdefault(d, []).append(var[int(x)])
    clauses = []
    for lits in by.values():
        if len(lits) > 1:
            enc = EncType.pairwise if len(lits) < 7 else EncType.seqcounter
            clauses.extend(CardEnc.atmost(lits=lits, bound=1, vpool=pool, encoding=enc).clauses)
    clauses.extend(CardEnc.atleast(lits=list(var.values()), bound=nfree, vpool=pool, encoding=EncType.seqcounter).clauses)
    with Solver(name="cadical195", bootstrap_with=clauses) as s:
        s.conf_budget(budget)
        res = s.solve_limited()
        if res is True:
            model = set(l for l in s.get_model() if l > 0)
            return "sat", kept + [int(x) for x in cand if var[int(x)] in model], nfree
        return ("unsat" if res is False else "timeout"), None, nfree


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--seconds", type=float, default=6 * 3600)
    ap.add_argument("--out", default=f"runs/{FAM}")
    ap.add_argument("--k", type=int, default=227, help="fixed code size searched for (record + 1); 0 = size of the start code + 1, then +1 after every success")
    ap.add_argument("--init", default="record0", choices=["record0", "record1", "record2", "record3", "record4", "scratch"])
    ap.add_argument("--tenure", type=int, default=10, help="a word cannot be removed for 1..tenure steps after insertion")
    ap.add_argument("--noise", type=float, default=0.05, help="probability of removing a random conflicting word")
    ap.add_argument("--decay", type=int, default=200, help="smooth all weights every this many breakout bumps")
    ap.add_argument("--w0", type=int, default=1, help="base descendant weight (1 = pure breakout; larger = weights act as a bias)")
    ap.add_argument("--force", type=float, default=0.0, help="probability of making the best swap even when it raises the weighted cost")
    ap.add_argument("--band", type=int, default=10, help="return to the elite configuration (weights kept) when the over-coverage exceeds the elite's by more than this")
    ap.add_argument("--wcap", type=int, default=4, help="maximum descendant weight; when every over-covered descendant is at the cap the best swap is forced")
    ap.add_argument("--cand", type=int, default=12, help="max conflicting words evaluated per step (random subset when more are in conflict)")
    ap.add_argument("--rho", type=float, default=0.5, help="weight smoothing factor")
    ap.add_argument("--restart", type=int, default=400000, help="steps without a new minimum before a kick")
    ap.add_argument("--kick", type=int, default=12, help="words re-inserted at a kick (0 = rebuild from --init)")
    ap.add_argument("--repair-at", dest="repair_at", type=int, default=4, help="exact SAT repair when the number of conflicting words <= this")
    ap.add_argument("--repair-r", dest="repair_r", type=int, default=12, help="words freed in the exact repair (then 3x)")
    ap.add_argument("--repair-conflicts", dest="repair_conflicts", type=int, default=20000, help="SAT conflict budget per repair")
    ap.add_argument("--repair-frac", dest="repair_frac", type=float, default=0.3, help="max fraction of wall time spent in SAT repair")
    ap.add_argument("--chunk", type=int, default=5000, help="swaps per jitted call")
    ap.add_argument("--record", type=int, default=226, help="leaderboard top; FOUND when verified size beats it")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    sid = os.environ.get("LTD_STRATEGY_ID", f"s{a.seed}")
    tag = f"[{FAM} s{a.seed}]"
    ver = load_verifier()
    try:
        min_imp = int(json.load(open(os.path.join(PROB, "meta.json"))).get("minImprovement", 1))
    except Exception:
        min_imp = 1
    t0 = time.time()
    T = build_tables()
    rng = np.random.default_rng(a.seed)
    seed_rng(a.seed)

    def start_words():
        if a.init == "scratch":
            return []
        best = json.load(open(os.path.join(PROB, "best_solutions.json")))
        best = best if isinstance(best, list) else best.get("solutions", best)
        return [int(s, 2) for s in best[min(int(a.init[6:]), len(best) - 1)]["data"]["words"]]

    base = start_words()
    best_valid = valid_subcode(T, base) if base else []
    if best_valid:
        ver.evaluate({"words": [to_str(x) for x in best_valid]})
    k = max(a.k, len(best_valid) + 1) if a.k > 0 else max(len(best_valid) + 1, 2)   # --k 0: start size + 1

    def save_best(extra):
        json.dump({"count": len(best_valid), "words": [to_str(x) for x in best_valid], **extra},
                  open(os.path.join(a.out, f"best_{sid}.json"), "w"))

    def claim(words, how):
        """Official check of a conflict-free code; FOUND only if it beats the record."""
        nonlocal best_valid
        sol = {"words": [to_str(x) for x in words]}
        score = ver.evaluate(sol)                              # raises if invalid
        if score > len(best_valid):
            best_valid = [int(x) for x in words]
            save_best({"how": how})
        if score >= a.record + min_imp:
            fn = os.path.join(a.out, f"FOUND_{sid}_{int(score)}.json")
            json.dump({"score": int(score), "solution": sol, "how": how, "seed": a.seed, "init": a.init}, open(fn, "w"))
            print(f"FOUND two-deletion code of size {int(score)} verified by official verifier -> {fn}", flush=True)
        return score

    def new_state(words, k):
        s = State(T, k, a.w0); s.fill(np.array(words, dtype=np.int64)); return s

    s = new_state(base, k)
    steps = 0; restarts = 0; rep = {"sat": 0, "unsat": 0, "timeout": 0}; rep_time = 0.0
    since = 0; last_print = 0.0; seen = set(); csum_last = 0; steps_last = 0; cpu = 0.0   # cpu = CPU seconds in the search core
    pairs0, bad0 = conflict_info(T, s.S)
    gmin = len(pairs0)                 # fewest conflicting pairs seen in the whole run
    rmin = int(s.st[2])                # least over-coverage since the last kick (drives --restart)
    print(f"{tag} t={time.time()-t0:.0f}s best={len(best_valid)} conf={gmin} cwords={len(bad0)} over={int(s.st[2])} k={k} "
          f"init={a.init} steps=0 start (tables {time.time()-t0:.1f}s)", flush=True)
    save_best({"how": "init"})
    while time.time() - t0 < a.seconds:
        tc = time.process_time(); done = s.run(a.chunk, a); cpu += time.process_time() - tc
        steps += done; since += done
        cw = int(s.st[4]); solved = None; ov = int(s.st[7])
        pairs, _ = conflict_info(T, s.Sbest)
        if cw == 0:
            solved = ([int(x) for x in s.Sbest], "search")
        elif cw <= a.repair_at and rep_time <= a.repair_frac * (time.time() - t0):
            key = hash(frozenset(s.Sbest.tolist()))
            if key not in seen:
                seen.add(key)
                for r in (a.repair_r, 3 * a.repair_r):
                    tr = time.time()
                    status, code, nfree = exact_repair(T, s.Sbest, r, a.repair_conflicts)
                    rep_time += time.time() - tr; rep[status] += 1
                    if status == "sat":
                        solved = (code, f"sat-repair r={nfree}"); break
                    if status == "timeout":
                        break
        if ov < rmin:
            rmin = ov; since = 0
        if len(pairs) < gmin or solved:
            gmin = min(gmin, len(pairs))
            sub = valid_subcode(T, s.Sbest)
            if len(sub) > len(best_valid):
                claim(sub, "sub-code of a k-configuration")
            el = time.time() - t0
            print(f"{tag} t={el:.0f}s best={len(best_valid)} conf={len(pairs)} cwords={cw} over={int(s.st[7])} k={k} "
                  f"steps={steps} rate={steps/max(cpu, 1e-9):.0f}/cpu-s restarts={restarts} "
                  f"repairs={rep['sat']}/{rep['unsat']}/{rep['timeout']} improved", flush=True)
        if solved:
            score = claim(solved[0], solved[1])
            print(f"{tag} t={time.time()-t0:.0f}s best={len(best_valid)} conf=0 cwords=0 over=0 k={k} steps={steps} "
                  f"valid code of size {int(score)} via {solved[1]}; continuing with k={k+1}", flush=True)
            k += 1
            s = new_state(best_valid, k)
            p_, b_ = conflict_info(T, s.S)
            gmin = len(p_); rmin = int(s.st[2]); since = 0; seen.clear(); csum_last = 0; steps_last = steps
        elif since >= a.restart:
            restarts += 1; since = 0
            if a.kick > 0:
                s.kick(a.kick, rng)
            else:
                s = new_state(start_words() if len(base) >= len(best_valid) else best_valid, k)
                csum_last = 0; steps_last = steps
            rmin = int(s.st[2])
        if time.time() - last_print > 30:
            last_print = time.time(); el = time.time() - t0
            avg = (int(s.st[6]) - csum_last) / max(steps - steps_last, 1); csum_last = int(s.st[6]); steps_last = steps
            print(f"{tag} t={el:.0f}s best={len(best_valid)} conf={gmin} cur_over={int(s.st[2])} avg_cwords={avg:.1f} "
                  f"runmin_over={rmin} k={k} steps={steps} rate={steps/max(cpu, 1e-9):.0f}/cpu-s "
                  f"bumps={int(s.st[3])} returns={int(s.st[8])} wmax={int(s.w.max())} restarts={restarts} "
                  f"repairs={rep['sat']}/{rep['unsat']}/{rep['timeout']} repair_s={rep_time:.0f}", flush=True)
    print(json.dumps({"words": [to_str(x) for x in best_valid]}))


if __name__ == "__main__":
    main()
