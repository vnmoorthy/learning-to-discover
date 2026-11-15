"""Large-neighbourhood search with an EXACT SAT sub-solver for two-deletion-correcting codes of length 16
(EinsteinArena 'two-deletion-code-16', record 226).

Each iteration: keep all but r codewords of the current code (r chosen around a random centre word, nearest by
Hamming distance, or random), list every length-16 word whose 2-deletion descendants avoid all descendants of the
kept words, and ask a SAT solver whether r+1 of those candidates can be packed (pairwise disjoint descendants).
SAT -> the code grows by one (verified with the official rule before it is accepted). UNSAT -> that neighbourhood
is provably optimal; move on. Log: [twodel_lns s<seed>] t=..s best=<size> iters=.. sat=.. unsat=.. timeout=.. r=..
"""
import argparse, json, os, random, sys, time
import numpy as np
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver

L = 16


def descendants_table():
    words = np.arange(1 << L, dtype=np.int64)
    bits = ((words[:, None] >> np.arange(L - 1, -1, -1)) & 1).astype(np.int8)   # MSB first, like the strings
    out = []
    for i in range(L - 1):
        for j in range(i + 1, L):
            keep = [k for k in range(L) if k != i and k != j]
            sub = bits[:, keep]
            val = (sub * (1 << np.arange(L - 3, -1, -1))).sum(1)
            out.append(val)
    D = np.stack(out, 1)                                     # 65536 x 120 (with duplicates)
    return D


def to_int(s):
    return int(s, 2)


def to_str(w):
    return format(w, f"0{L}b")


def official_ok(words):
    used = set()
    for w in words:
        s = to_str(w); d = set()
        for i in range(L - 1):
            for j in range(i + 1, L):
                d.add(s[:i] + s[i + 1:j] + s[j + 1:])
        if not used.isdisjoint(d):
            return False
        used |= d
    return len(set(words)) == len(words)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--rmin", type=int, default=6)
    ap.add_argument("--rmax", type=int, default=24)
    ap.add_argument("--hood", default="hamming", choices=["hamming", "random", "mixed"])
    ap.add_argument("--conflicts", type=int, default=200000, help="SAT conflict budget per sub-problem")
    ap.add_argument("--rank", type=int, default=0, help="which public solution to start from")
    ap.add_argument("--seconds", type=float, default=6 * 3600)
    ap.add_argument("--out", default="runs/twodel_lns")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    rng = random.Random(a.seed)
    here = os.path.dirname(os.path.abspath(__file__))
    best_file = os.path.join(here, "..", "problems", "two-deletion-code-16", "best_solutions.json")
    best = json.load(open(best_file)); best = best if isinstance(best, list) else best.get("solutions", best)
    code = [to_int(s) for s in best[min(a.rank, len(best) - 1)]["data"]["words"]]
    sid = os.environ.get("PHOENIX_STRATEGY_ID", f"s{a.seed}")
    D = descendants_table()
    t0 = time.time(); it = sat = unsat = tout = 0
    record = 226
    print(f"[twodel_lns s{a.seed}] t=0s best={len(code)} iters=0 sat=0 unsat=0 timeout=0 r=0 start", flush=True)
    last_print = 0
    while time.time() - t0 < a.seconds:
        it += 1
        r = rng.randint(a.rmin, a.rmax)
        hood = a.hood if a.hood != "mixed" else rng.choice(["hamming", "random"])
        if hood == "hamming":
            c = rng.choice(code)
            order = sorted(code, key=lambda w: (bin(w ^ c).count("1"), rng.random()))
            removed = set(order[:r])
        else:
            removed = set(rng.sample(code, r))
        kept = [w for w in code if w not in removed]
        blocked = np.zeros(1 << (L - 2), dtype=bool)
        blocked[D[kept].ravel()] = True
        cand = np.nonzero(~blocked[D].any(1))[0]
        if len(cand) <= r:
            continue
        pool = IDPool()
        var = {int(w): pool.id(int(w)) for w in cand}
        by_desc = {}
        for w in cand:
            for d in set(D[w].tolist()):
                by_desc.setdefault(d, []).append(var[int(w)])
        clauses = []
        for lits in by_desc.values():
            if len(lits) > 1:
                clauses.extend(CardEnc.atmost(lits=lits, bound=1, vpool=pool, encoding=EncType.pairwise if len(lits) < 7 else EncType.seqcounter).clauses)
        clauses.extend(CardEnc.atleast(lits=list(var.values()), bound=r + 1, vpool=pool, encoding=EncType.seqcounter).clauses)
        with Solver(name="cadical195", bootstrap_with=clauses) as s:
            s.conf_budget(a.conflicts)
            res = s.solve_limited()
            if res is True:
                model = set(l for l in s.get_model() if l > 0)
                new = [int(w) for w in cand if var[int(w)] in model]
                newcode = kept + new
                if official_ok(newcode) and len(newcode) > len(code):
                    code = newcode; sat += 1
                    json.dump({"count": len(code), "words": [to_str(w) for w in code]},
                              open(os.path.join(a.out, f"best_{sid}.json"), "w"))
                    print(f"[twodel_lns s{a.seed}] t={time.time()-t0:.0f}s best={len(code)} iters={it} sat={sat} unsat={unsat} timeout={tout} r={r} improved", flush=True)
                    if len(code) > record:
                        fn = os.path.join(a.out, f"FOUND_{sid}_{len(code)}.json")
                        json.dump({"score": len(code), "solution": {"words": [to_str(w) for w in code]}}, open(fn, "w"))
                        print(f"FOUND {len(code)} words, verified -> {fn}", flush=True)
            elif res is False:
                unsat += 1
            else:
                tout += 1
        if time.time() - last_print > 30:
            last_print = time.time()
            print(f"[twodel_lns s{a.seed}] t={time.time()-t0:.0f}s best={len(code)} iters={it} sat={sat} unsat={unsat} timeout={tout} r={r} cand={len(cand)}", flush=True)
    print(json.dumps({"words": [to_str(w) for w in code]}))


if __name__ == "__main__":
    main()
