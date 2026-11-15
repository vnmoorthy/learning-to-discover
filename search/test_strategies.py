"""Unit tests for the strategies builder's searches: each objective must reproduce the OFFICIAL verifier exactly
on the public best solutions (problems/<slug>/best_solutions.json) and on random inputs.

Run from the repo root:  python3 search/test_strategies.py [twodel] [sidon] [snake]
"""
import itertools, json, os, random, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np


def test_twodel():
    import twodel_ils as T
    ver = T.load_verifier()
    p, d = T.word_descendants()
    rnd = random.Random(0)
    for _ in range(5000):
        w = rnd.randrange(1 << 16); s = T.w2s(w)
        assert sorted(int(x, 2) for x in ver.descendants(s)) == sorted(d[p[w]:p[w + 1]].tolist()), s
    pp, pi = T.build_parents(1 << 16, p, d, T.NE)
    assert (np.diff(pp) == 137).all()   # every length-14 string has sum_{i<=2} C(16,i) = 137 supersequences
    nitems = 1 << 16

    def fresh():
        IT = np.zeros((8, nitems), np.int64); IT[T.WT] = 1; IT[T.LCK] = -1
        EL = np.zeros((2, T.NE), np.int64); EL[T.OWN] = -1
        SC = np.zeros(11, np.int64); SC[T.S_UNDOCAP] = 1 << 20; SC[T.S_MINC1] = 2
        return (IT, EL, SC, np.zeros(nitems, np.int32), np.zeros(4 * nitems + 16, np.int32),
                np.zeros(1 << 20, np.int32), np.zeros(nitems + 1, np.int32))

    recs = json.load(open(os.path.join(T.PROB, "best_solutions.json")))
    for r in recs:
        words = r["data"]["words"]
        IT, EL, SC, sol, freel, undo, dq = fresh()
        bad = T.load_solution(np.array([T.s2w(s) for s in words], np.int32), p, d, pp, pi, IT, EL, SC, sol, freel,
                              undo, dq)
        off = ver.evaluate({"words": words})
        assert bad == 0 and SC[T.S_SCORE] == off == r["score"], (r["agentName"], bad, SC[T.S_SCORE], off)
        # tau / c1 bookkeeping equals a from-scratch recount
        tau = np.zeros(nitems, np.int64)
        S = set(sol[:SC[T.S_NSOL]].tolist())
        own = EL[T.OWN]
        for w in range(0, nitems, 97):
            if w in S:
                continue
            owners = {int(own[e]) for e in d[p[w]:p[w + 1]] if own[e] != -1}
            assert IT[T.TAU, w] == len(owners), (w, IT[T.TAU, w], owners)
        print(f"  twodel {r['agentName']:>16}: packing size {int(SC[T.S_SCORE])} == official {off:.0f}")
    # a corrupted code must be rejected by both
    words = list(recs[0]["data"]["words"])
    for w in range(1 << 16):
        s = T.w2s(w)
        if s not in words:
            try:
                ver.evaluate({"words": words + [s]})
            except ValueError:
                IT, EL, SC, sol, freel, undo, dq = fresh()
                bad = T.load_solution(np.array([T.s2w(x) for x in words + [s]], np.int32), p, d, pp, pi, IT, EL, SC,
                                      sol, freel, undo, dq)
                assert bad == 1
                break
    # symmetric orbit items: every orbit item is internally conflict-free
    for g in ["rev", "comp", "rc", "full"]:
        members, dp, di, wt = T.orbit_items(g, p, d)
        for i in range(0, len(members), 50):
            ver.evaluate({"words": [T.w2s(v) for v in members[i]]})
        print(f"  twodel group={g}: {len(members)} valid orbits, weights {sorted(set(wt.tolist()))}")
    print("twodel OK")


def test_sidon():
    import sidon_sa as S
    ver = S.load_verifier()
    recs = json.load(open(os.path.join(S.PROB, "best_solutions.json")))
    for r in recs:
        el = r["data"]["elements"]; mn = min(el)
        v = np.array([x - mn for x in el], np.int64); n = len(v)
        mark = np.zeros(int(v.max()) + 1, np.int8); part = np.zeros(n, np.int64)
        h = S.sidon_dfs(v, n, 0, mark, 0, 1, part)
        off = ver.evaluate({"elements": el})
        assert h / n == off == r["score"], (r["agentName"], h, n, off)
        assert all(S.quad_ok(*q) for q in itertools.combinations(v.tolist(), 4))
        assert mark.sum() == 0
        print(f"  sidon {r['agentName']:>18}: h={h} n={n} h/n={h/n:.16f} == official {off:.16f}")
    rnd = random.Random(1)
    for _ in range(300):
        n = rnd.randint(5, 11); v = np.array(rnd.sample(range(80), n), np.int64)
        mark = np.zeros(81, np.int8)
        for k in range(1, n + 1):
            part = np.zeros(n, np.int64)
            subs = [c for c in itertools.combinations(range(n), k) if ver.is_sidon(sorted(v[list(c)].tolist()))]
            assert S.sidon_dfs(v, n, k, mark, 10 ** 9, 0, part) == len(subs)
            assert part.tolist() == [sum(i in c for c in subs) for i in range(n)]
        hb = max(k for k in range(1, n + 1)
                 if any(ver.is_sidon(sorted(c)) for c in itertools.combinations(v.tolist(), k)))
        assert S.sidon_dfs(v, n, 0, mark, 0, 1, np.zeros(n, np.int64)) == hb
        y = rnd.randrange(80); i = rnd.randrange(n); w = v.copy(); w[i] = y
        rest = [x for j, x in enumerate(v.tolist()) if j != i]
        if all(S.quad_ok(*q) for q in itertools.combinations(rest, 4)):
            bf = len(set(w.tolist())) == n and all(S.quad_ok(*q) for q in itertools.combinations(w.tolist(), 4))
            assert S.ok45_with(v, n, i, y) == bf
            if bf and n >= 4:
                try:
                    off = ver.evaluate({"elements": [int(x) for x in w]})
                    assert off == S.sidon_dfs(w, n, 0, mark, 0, 1, np.zeros(n, np.int64)) / n
                except ValueError:
                    raise AssertionError("official verifier rejected a set we accept")
        assert mark.sum() == 0
    print("  sidon: 300 random sets: Sidon counts, participation, h and (4,5) checks match brute force/official")
    print("sidon OK")


def test_snake():
    import snake_beam as B
    ver = B.load_verifier()
    recs = json.load(open(os.path.join(B.PROB, "best_solutions.json")))
    for r in recs:
        acts = r["data"]["actions"]
        off = ver.evaluate({"actions": acts})
        ok, L = B.check_actions(np.array(acts, np.int64))
        assert ok and L == off == r["score"], (r["agentName"], ok, L, off)
        rv = list(reversed(acts))
        assert ver.evaluate({"actions": rv}) == off   # reversal keeps a snake (translated to start at 0)
        print(f"  snake {r['agentName']:>24}: length {L} == official {off:.0f} (reversed too)")
    bad = list(recs[0]["data"]["actions"]); bad[len(bad) // 2] = (bad[len(bad) // 2] + 1) % 13
    try:
        ver.evaluate({"actions": bad}); off_ok = True
    except ValueError:
        off_ok = False
    assert B.check_actions(np.array(bad, np.int64))[0] == off_ok
    print("snake OK")


if __name__ == "__main__":
    which = sys.argv[1:] or ["twodel", "sidon", "snake"]
    for w in which:
        t = time.time()
        {"twodel": test_twodel, "sidon": test_sidon, "snake": test_snake}[w]()
        print(f"  ({time.time()-t:.1f}s)")
