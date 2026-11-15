"""Official verifier for 'three-body-periodic-orbits' (Phoenixastar lab problem, not an EinsteinArena problem).

solution = {"orbits": [{"vx": float, "vy": float, "T": float, "m3": float (optional, default 1)}, ...]}

Setup (Suvakov-Dmitrasinovic 2013 / Li-Liao 2017): G = 1, m1 = m2 = 1, m3 free, planar,
r1 = (-1, 0), r2 = (1, 0), r3 = (0, 0), v1 = v2 = (vx, vy), v3 = -2 (vx, vy) / m3  (zero momentum, zero angular momentum).

For every orbit this file
  1. integrates one period in float64 with an adaptive Dormand-Prince 8(5,3) method (own numpy implementation, the
     tableau is in dop853.json) at rtol = atol = 1e-13 and again at 1e-11 (step refinement check),
  2. requires return error |r(T) - r(0)| + |v(T) - v(0)| < 1e-8 at the tight tolerance, < 1e-6 at the loose one, and
     that both runs agree to 1e-6 (the result is converged with respect to the step size),
  3. rejects T that is an integer multiple (2..6) of a shorter period, E >= 0, or failed integrations,
  4. computes the topological class: the cyclic sequence of syzygies (collinear configurations, labelled by the body
     in the middle = which arc of the shape-sphere equator between two collision points is crossed), reduced by
     cancelling equal neighbours (Montgomery 1998). This is the conjugacy class of the free-group element used by
     Suvakov-Dmitrasinovic. It is canonicalised over start point, time reversal and relabelling of the bodies,
     and reduced to its primitive root (an orbit whose word is a power w^k is a "topological-power satellite" of the
     family w, e.g. the satellites of the figure-eight, and is not a separate family),
  5. compares with catalog.json (Suvakov-Dmitrasinovic 2013, Li-Liao 2017, Li-Liao 2018). An orbit is a NEW CANDIDATE only
     if its canonical word matches no catalog entry and no catalog entry has the same mass, scale-invariant period
     and initial velocity.

evaluate(solution) -> float: number of distinct verified families (canonical words) that are new candidates vs the
catalog. Raises ValueError if the solution is malformed or any listed orbit fails verification.
evaluate_detailed(solution) -> dict with a full per-orbit report (never raises for a bad orbit).
"""
import json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
_tab = json.load(open(os.path.join(HERE, "dop853.json")))
_A = np.array(_tab["A"]); _B = np.array(_tab["B"]); _E3 = np.array(_tab["E3"]); _E5 = np.array(_tab["E5"])

TOL_RETURN = 1e-8        # return error at rtol 1e-13
TOL_RETURN_COARSE = 1e-6 # return error at rtol 1e-11
TOL_CONSIST = 1e-6       # |y_fine(T) - y_coarse(T)|
TOL_MULTIPLE = 1e-4      # return distance at T/k below this => T is k times a shorter period
MAX_ORBITS = 20000
T_MIN, T_MAX = 0.5, 2000.0


def initial_state(vx, vy, m3):
    vx = np.atleast_1d(np.asarray(vx, dtype=np.float64)); vy = np.atleast_1d(np.asarray(vy, dtype=np.float64))
    m3 = np.atleast_1d(np.asarray(m3, dtype=np.float64))
    n = len(vx); y = np.zeros((n, 12))
    y[:, 0] = -1.0; y[:, 2] = 1.0
    y[:, 6] = vx; y[:, 7] = vy; y[:, 8] = vx; y[:, 9] = vy
    y[:, 10] = -2.0 * vx / m3; y[:, 11] = -2.0 * vy / m3
    return y


def energy(vx, vy, m3):
    v2 = vx * vx + vy * vy
    return v2 * (1.0 + 2.0 / m3) - (0.5 + 2.0 * m3)


def rhs(y, m3):
    r1 = y[:, 0:2]; r2 = y[:, 2:4]; r3 = y[:, 4:6]
    d12 = r2 - r1; d13 = r3 - r1; d23 = r3 - r2
    i12 = ((d12 * d12).sum(1)) ** -1.5; i13 = ((d13 * d13).sum(1)) ** -1.5; i23 = ((d23 * d23).sum(1)) ** -1.5
    g12 = d12 * i12[:, None]; g13 = d13 * (m3 * i13)[:, None]; g23 = d23 * (m3 * i23)[:, None]
    out = np.empty_like(y)
    out[:, 0:6] = y[:, 6:12]
    out[:, 6:8] = g12 + g13
    out[:, 8:10] = g23 - g12
    out[:, 10:12] = -(d13 * i13[:, None]) - (d23 * i23[:, None])
    return out


def _area(p):
    return (p[:, 2] - p[:, 0]) * (p[:, 5] - p[:, 1]) - (p[:, 3] - p[:, 1]) * (p[:, 4] - p[:, 0])


def _middle(p):
    """index (1..3) of the body lying between the other two for (nearly) collinear configurations p (n,6)."""
    r = p.reshape(-1, 3, 2)
    d = np.empty((len(p), 3))
    for i, (j, k) in enumerate(((1, 2), (0, 2), (0, 1))):
        d[:, i] = ((r[:, j] - r[:, i]) * (r[:, k] - r[:, i])).sum(1)
    return d.argmin(1) + 1


def integrate(vx, vy, T, m3, rtol=1e-13, atol=1e-13, events=True, max_steps=None):
    """Batched adaptive DOP853 over one period. Returns dict of per-orbit arrays (+ syzygy sequences if events)."""
    vx = np.atleast_1d(np.asarray(vx, float)); vy = np.atleast_1d(np.asarray(vy, float))
    T = np.atleast_1d(np.asarray(T, float)); m3 = np.atleast_1d(np.asarray(m3, float))
    n = len(vx)
    y0 = initial_state(vx, vy, m3); y = y0.copy(); f = rhs(y, m3)
    t = np.zeros(n); h = np.minimum(1e-3, T / 100.0)
    done = np.zeros(n, bool); failed = np.zeros(n, bool)
    rmin = np.full(n, np.inf); nsteps = np.zeros(n, np.int64)
    if max_steps is None: max_steps = int(4000 + 3000 * float(T.max()))
    prev = np.zeros(n); first = np.zeros(n)
    seqs = [[] for _ in range(n)]
    KS = (2, 3, 4, 5, 6); dk = np.full((n, len(KS)), np.inf)
    thetas = (0.25, 0.5, 0.75, 1.0)
    for _ in range(max_steps):
        idx = np.nonzero(~(done | failed))[0]
        if len(idx) == 0: break
        ya = y[idx]; ma = m3[idx]; ta = t[idx]; Ta = T[idx]
        rem = Ta - ta
        last = h[idx] >= rem
        ha = np.where(last, rem, h[idx])
        K = np.empty((13, len(idx), 12)); K[0] = f[idx]
        for s in range(1, 12):
            K[s] = rhs(ya + ha[:, None] * np.tensordot(_A[s, :s], K[:s], 1), ma)
        yn = ya + ha[:, None] * np.tensordot(_B, K[:12], 1)
        K[12] = rhs(yn, ma)
        sc = atol + rtol * np.maximum(np.abs(ya), np.abs(yn))
        e5 = ((np.tensordot(_E5, K, 1) / sc) ** 2).sum(1); e3 = ((np.tensordot(_E3, K, 1) / sc) ** 2).sum(1)
        den = e5 + 0.01 * e3
        with np.errstate(divide="ignore", invalid="ignore"):
            en = np.where(den > 0, np.abs(ha) * e5 / np.sqrt(den * 12.0), 0.0)
            en = np.where(np.isfinite(en), en, 1e10)
            fac = np.where(en > 0, 0.9 * en ** (-0.125), 10.0)
        acc = en <= 1.0
        fac = np.where(acc, np.minimum(10.0, fac), np.maximum(0.2, np.minimum(fac, 0.9)))
        h[idx] = ha * fac
        failed[idx[h[idx] < 1e-13]] = True
        a = np.nonzero(acc)[0]
        if len(a) == 0: continue
        ia = idx[a]; y_0 = ya[a]; y_1 = yn[a]; f_0 = K[0][a]; f_1 = K[12][a]; hh = ha[a][:, None]; la = last[a]
        if events:
            for th in thetas:
                h00 = 2 * th**3 - 3 * th**2 + 1; h10 = th**3 - 2 * th**2 + th; h01 = -2 * th**3 + 3 * th**2; h11 = th**3 - th**2
                p = h00 * y_0[:, :6] + h10 * hh * f_0[:, :6] + h01 * y_1[:, :6] + h11 * hh * f_1[:, :6]
                s = np.sign(_area(p))
                if th == 1.0: s = np.where(la, 0.0, s)       # t = T is the (collinear) start again: handled by wrap
                pv = prev[ia]
                cross = np.nonzero((s != 0) & (pv != 0) & (s != pv))[0]
                if len(cross):
                    mid = _middle(p[cross])
                    for c, m in zip(cross, mid): seqs[ia[c]].append(int(m))
                fresh = (pv == 0) & (s != 0)
                first[ia[fresh]] = s[fresh]
                prev[ia] = np.where(s != 0, s, pv)
            for q, k in enumerate(KS):
                tk = T[ia] / k
                hit = np.nonzero((t[ia] < tk) & (tk <= t[ia] + hh[:, 0]))[0]
                if len(hit):
                    th = ((tk[hit] - t[ia][hit]) / hh[hit, 0])[:, None]
                    h00 = 2 * th**3 - 3 * th**2 + 1; h10 = th**3 - 2 * th**2 + th; h01 = -2 * th**3 + 3 * th**2; h11 = th**3 - th**2
                    yy = h00 * y_0[hit] + h10 * hh[hit] * f_0[hit] + h01 * y_1[hit] + h11 * hh[hit] * f_1[hit]
                    dd = yy - y0[ia[hit]]
                    dk[ia[hit], q] = np.sqrt((dd[:, :6] ** 2).sum(1)) + np.sqrt((dd[:, 6:] ** 2).sum(1))
        y[ia] = y_1; f[ia] = f_1; t[ia] = np.where(la, T[ia], t[ia] + hh[:, 0]); nsteps[ia] += 1
        done[ia[la]] = True
        r = y_1.reshape(-1, 2, 3, 2)[:, 0]
        rm = np.minimum(np.minimum(np.linalg.norm(r[:, 0] - r[:, 1], axis=1), np.linalg.norm(r[:, 0] - r[:, 2], axis=1)),
                        np.linalg.norm(r[:, 1] - r[:, 2], axis=1))
        rmin[ia] = np.minimum(rmin[ia], rm)
    failed |= ~done
    if events:
        mid0 = _middle(y0[:, :6])
        for i in range(n):
            if prev[i] != 0 and first[i] != 0 and prev[i] != first[i]: seqs[i].append(int(mid0[i]))
    d = y - y0
    err = np.sqrt((d[:, :6] ** 2).sum(1)) + np.sqrt((d[:, 6:] ** 2).sum(1))
    err = np.where(failed, np.inf, err)
    return {"yT": y, "err": err, "failed": failed, "rmin": rmin, "nsteps": nsteps, "dk": dk, "seqs": seqs}


# ---------------------------------------------------------------- topology
def reduce_cyclic(seq):
    """cancel equal neighbours in a cyclic sequence of symbols 1,2,3 (crossing the same arc back and forth)."""
    st = []
    for s in seq:
        if st and st[-1] == s: st.pop()
        else: st.append(s)
    i, j = 0, len(st) - 1
    while j > i and st[i] == st[j]: i += 1; j -= 1
    return st[i:j + 1]


_PERMS = [{"1": a, "2": b, "3": c} for a, b, c in ("123", "132", "213", "231", "312", "321")]


def canonical_word(seq):
    """canonical representative of the reduced cyclic syzygy sequence under rotation, reversal and body relabelling."""
    r = "".join(map(str, reduce_cyclic(seq)))
    L = len(r)
    if L == 0: return ""
    best = None
    for p in _PERMS:
        s = "".join(p[c] for c in r)
        for u in (s, s[::-1]):
            d = u + u
            m = min(d[i:i + L] for i in range(L))
            if best is None or m < best: best = m
    return best


def primitive_root(canon):
    """(root, k): canon = root^k as a closed loop on the shape sphere (root has even length). k > 1 means the orbit is
    a 'topological-power satellite' (Suvakov 2014) of the family 'root', which is not counted as a separate family."""
    L = len(canon)
    for p in range(1, L + 1):
        if L % p == 0 and canon == canon[:p] * (L // p):
            if p % 2: p *= 2
            if p > L or L % p: p = L
            return canon[:p], L // p
    return canon, 1


_PAIR = {(1, 2): "a", (2, 1): "A", (2, 3): "b", (3, 2): "B", (1, 3): "ab", (3, 1): "BA"}


def free_group_word(seq):
    """free-group element (letters a, b, A = a^-1, B = b^-1) of the reduced cyclic syzygy sequence, in our convention:
    x_i = path from the north to the south hemisphere of the shape sphere through equator arc i, a = x1 x2^-1,
    b = x2 x3^-1. Other papers use other generators, so compare conjugacy classes via canonical_word, not this string."""
    r = reduce_cyclic(seq)
    if len(r) % 2: return None
    st = []
    for q in range(0, len(r), 2):
        for ch in _PAIR.get((r[q], r[q + 1]), ""):
            if st and st[-1] == ch.swapcase(): st.pop()
            else: st.append(ch)
    i, j = 0, len(st) - 1
    while j > i and st[i] == st[j].swapcase(): i += 1; j -= 1
    return "".join(st[i:j + 1])


# ---------------------------------------------------------------- catalog / novelty
_CAT = None


def load_catalog():
    global _CAT
    if _CAT is None:
        p = os.path.join(HERE, "catalog.json")
        _CAT = json.load(open(p)) if os.path.exists(p) else {"entries": []}
        _CAT["_words"] = {}
        for e in _CAT["entries"]:
            if e.get("canon"):
                _CAT["_words"].setdefault(e["canon"], e["name"])
                _CAT["_words"].setdefault(primitive_root(e["canon"])[0], e["name"])
    return _CAT


def classify(vx, vy, T, m3, canon):
    """-> (status, match). status: 'known' (rediscovery / known family) or 'new_candidate'."""
    cat = load_catalog()
    if not cat["entries"]:
        return "unchecked", "catalog.json missing or empty: novelty cannot be assessed"
    tstar = T * abs(energy(vx, vy, m3)) ** 1.5
    for e in cat["entries"]:
        if abs(e["m3"] - m3) < 1e-6 and abs(abs(e["vx"]) - abs(vx)) < 2e-4 and abs(abs(e["vy"]) - abs(vy)) < 2e-4 \
                and abs(e["T"] - T) < 2e-3 * max(T, 1.0):
            return "known", "rediscovery of " + e["name"] + " (same initial condition and period)"
    if canon in cat["_words"]:
        return "known", "same topological family (free-group class) as " + cat["_words"][canon]
    root, k = primitive_root(canon)
    if root in cat["_words"]:
        return "known", "topological-power satellite (k=%d) of the family of %s" % (k, cat["_words"][root])
    if canon == "":
        return "known", "topologically trivial word: not counted as a family"
    for e in cat["entries"]:
        if abs(e["m3"] - m3) < 1e-6 and abs(e["Tstar"] - tstar) < 2e-3 * tstar and \
                math.hypot(abs(e["vx"]) - abs(vx), abs(e["vy"]) - abs(vy)) < 5e-3:
            return "known", "same T* and nearby initial condition as " + e["name"]
    return "new_candidate", None


# ---------------------------------------------------------------- evaluation
def _parse(solution):
    if not isinstance(solution, dict) or not isinstance(solution.get("orbits"), list):
        raise ValueError("solution must be {'orbits': [...]}")
    orbs = solution["orbits"]
    if not 1 <= len(orbs) <= MAX_ORBITS: raise ValueError("need 1..%d orbits" % MAX_ORBITS)
    out = []
    for o in orbs:
        try:
            vx = float(o["vx"]); vy = float(o["vy"]); T = float(o["T"]); m3 = float(o.get("m3", 1.0))
        except Exception:
            raise ValueError("each orbit needs numeric vx, vy, T (and optional m3)")
        if not all(map(math.isfinite, (vx, vy, T, m3))): raise ValueError("non-finite number")
        if not (T_MIN <= T <= T_MAX): raise ValueError("T out of range [%g, %g]" % (T_MIN, T_MAX))
        if not (0.01 <= m3 <= 100.0): raise ValueError("m3 out of range [0.01, 100]")
        if abs(vx) > 10 or abs(vy) > 10: raise ValueError("velocity out of range")
        out.append((vx, vy, T, m3))
    return out


def evaluate_detailed(solution):
    orbs = _parse(solution)
    vx, vy, T, m3 = (np.array(c, float) for c in zip(*orbs))
    fine = integrate(vx, vy, T, m3, 1e-13, 1e-13, events=True)
    coarse = integrate(vx, vy, T, m3, 1e-11, 1e-11, events=False)
    consist = np.abs(fine["yT"] - coarse["yT"]).max(1)
    E = energy(vx, vy, m3)
    rep = []; fam = {}
    for i in range(len(orbs)):
        r = {"vx": orbs[i][0], "vy": orbs[i][1], "T": orbs[i][2], "m3": orbs[i][3], "E": float(E[i]),
             "err": float(fine["err"][i]), "err_coarse": float(coarse["err"][i]), "consistency": float(consist[i]),
             "rmin": float(fine["rmin"][i]), "steps": int(fine["nsteps"][i])}
        why = None
        if fine["failed"][i] or coarse["failed"][i]: why = "integration failed (collision or step limit)"
        elif not E[i] < 0: why = "energy not negative"
        elif not r["err"] < TOL_RETURN: why = "return error %.3g >= %g" % (r["err"], TOL_RETURN)
        elif not r["err_coarse"] < TOL_RETURN_COARSE: why = "coarse return error %.3g >= %g" % (r["err_coarse"], TOL_RETURN_COARSE)
        elif not r["consistency"] < TOL_CONSIST: why = "not converged under step refinement (%.3g)" % r["consistency"]
        else:
            for q, k in enumerate((2, 3, 4, 5, 6)):
                if fine["dk"][i, q] < TOL_MULTIPLE:
                    why = "T is %d times a shorter period" % k; r["period_multiple"] = k
        seq = fine["seqs"][i]
        if why is None and len(reduce_cyclic(seq)) % 2: why = "odd syzygy count (numerical tangency)"
        r["valid"] = why is None; r["reason"] = why
        if why is None:
            r["Tstar"] = float(T[i] * abs(E[i]) ** 1.5)
            r["syzygies"] = len(seq)
            r["word"] = canonical_word(seq); r["free_group_word"] = free_group_word(seq)
            r["status"], r["match"] = classify(orbs[i][0], orbs[i][1], orbs[i][2], orbs[i][3], r["word"])
            r["family"], r["power"] = primitive_root(r["word"])
            if r["word"] != "":
                if r["family"] not in fam or r["status"] != "new_candidate": fam[r["family"]] = r["status"]
        rep.append(r)
    new = sorted(w for w, s in fam.items() if s == "new_candidate")
    return {"orbits": rep, "n_valid": sum(r["valid"] for r in rep), "families": len(fam), "new_families": len(new),
            "known_families": len(fam) - len(new), "new_words": new, "catalog_entries": len(load_catalog()["entries"])}


def evaluate(solution):
    d = evaluate_detailed(solution)
    bad = [r for r in d["orbits"] if not r["valid"]]
    if bad:
        raise ValueError("%d orbit(s) failed verification, first: vx=%r vy=%r T=%r: %s" % (len(bad), bad[0]["vx"], bad[0]["vy"], bad[0]["T"], bad[0]["reason"]))
    return float(d["new_families"])


if __name__ == "__main__":
    import sys
    sol = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else {"orbits": [{"vx": 0.3471168881, "vy": 0.5327249454, "T": 6.3259139829}]}
    if "solution" in sol: sol = sol["solution"]
    print(json.dumps(evaluate_detailed(sol), indent=1))
