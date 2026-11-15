"""Upgrade F: Renyi Page curves, entanglement spectra vs Marchenko-Pastur, and ensembles with
(nearly) the same mean von Neumann Page curve but different information structure.

Model classes are kept separate:
  * finite-dimensional circuit / state models: Haar states, random stabilizer states (deep random
    2-qubit-Clifford brickwork from |0..0>), local Haar brickwork circuits of depth D;
  * random-matrix (Wishart) predictions: Lubkin purity, exact Haar trace moments, MP law, GUE <r>.
No semiclassical-gravity or holographic claim is made or tested here.

Run (local CPU, numpy only; three independent parts can run in parallel):
    python experiments/f_spectra.py A      # Renyi Page curves + exact moment checks
    python experiments/f_spectra.py B      # MP spectra, finite-size corrections, level spacing
    python experiments/f_spectra.py C      # direction 6: Haar vs stabilizer vs brickwork
    python experiments/f_spectra.py E      # deeper brickwork grid, N = 10, 12
    python experiments/f_spectra.py D      # exact stabilizer ensemble by complete enumeration (N<=4)
    python experiments/f_spectra.py plot   # merge results/f_parts/*.json -> results/f_spectra.json + figures
"""
from __future__ import annotations

import json
import math
import os
import sys
import time

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(__file__))
RESULTS = os.path.join(ROOT, "results")
PARTS = os.path.join(RESULTS, "f_parts")
FIGURES = os.path.join(ROOT, "figures")
os.makedirs(PARTS, exist_ok=True)

import numpy as np  # noqa: E402

from eh import circuits as C  # noqa: E402
from eh import page as P  # noqa: E402
from eh import renyi as R  # noqa: E402
from eh import rmt  # noqa: E402

NS = (0.5, 1.0, 2.0, 3.0, math.inf)
NS_KEY = ("S_0.5", "S_1", "S_2", "S_3", "S_inf")
SEED_A, SEED_B, SEED_C = 20261115_1, 20261115_2, 20261115_3


def sem(a, axis=0):
    a = np.asarray(a, dtype=float)
    return a.std(axis=axis, ddof=1) / math.sqrt(a.shape[axis])


def spectrum_stats(p):
    """Per-spectrum scalar statistics (p: (..., d))."""
    out = {k: R.renyi(p, n) for k, n in zip(NS_KEY, NS)}
    out["purity"] = R.trace_moment(p, 2)
    out["tr3"] = R.trace_moment(p, 3)
    out["tr4"] = R.trace_moment(p, 4)
    out["capacity"] = R.capacity(p)
    out["S2_minus_Sinf"] = out["S_2"] - out["S_inf"]
    return out


def cut_profile(states, N):
    """states: list of (2,)*N tensors -> dict stat -> (n_samples, N+1) array; cut k = first k qubits
    (the spectrum is identical for the complement).  Also returns the half-cut spectra."""
    rows = {}
    half = []
    for s in states:
        per_cut = []
        for k in range(N + 1):
            p = C.schmidt_probs(s, k) if 0 < k < N else np.array([1.0])
            per_cut.append(spectrum_stats(p[None, :]))
            if k == N // 2:
                half.append(np.sort(p))
        for key in per_cut[0]:
            rows.setdefault(key, []).append([float(pc[key][0]) for pc in per_cut])
    return {k: np.array(v) for k, v in rows.items()}, np.array(half)


def summarise(prof):
    return {k: {"mean": v.mean(0).tolist(), "sem": sem(v).tolist(), "std": v.std(0, ddof=1).tolist()}
            for k, v in prof.items()}


def exact_curves(N):
    ks = list(range(N + 1))
    dims = [(2**k, 2 ** (N - k)) for k in ks]
    return {"page_S1": [P.page_entropy(m, n) for m, n in dims],
            "lubkin_purity": [R.lubkin_purity(m, n) for m, n in dims],
            "haar_tr3": [R.haar_trace_moment(3, m, n) for m, n in dims],
            "haar_tr4": [R.haar_trace_moment(4, m, n) for m, n in dims],
            "annealed_S2": [R.annealed_renyi(2, m, n) for m, n in dims],
            "annealed_S3": [R.annealed_renyi(3, m, n) for m, n in dims]}


def zscores(prof, ex):
    out = {}
    for key, exk in (("purity", "lubkin_purity"), ("tr3", "haar_tr3"), ("tr4", "haar_tr4"), ("S_1", "page_S1")):
        m, s = prof[key].mean(0), sem(prof[key])
        e = np.array(ex[exk])
        with np.errstate(divide="ignore", invalid="ignore"):
            z = np.where(s > 0, (m - e) / np.where(s > 0, s, 1.0), 0.0)
        out[key] = {"z_per_cut": z.tolist(), "max_abs_z": float(np.max(np.abs(z))),
                    "max_abs_dev": float(np.max(np.abs(m - e)))}
    return out


# ============================================================================ part A
def part_A():
    t0 = time.time()
    ss = np.random.SeedSequence(SEED_A)
    res = {"seed_base": SEED_A, "model": "Haar-random pure states (finite-dimensional circuit/state model)"}
    # (i) Renyi Page curves on N qubits
    for N, ns in ((12, 400), (8, 1000)):
        rng = np.random.default_rng(ss.spawn(1)[0])
        prof, _ = cut_profile([C.haar_state(N, rng) for _ in range(ns)], N)
        ex = exact_curves(N)
        res[f"N{N}"] = {"n_samples": ns, "stats": summarise(prof), "exact": ex, "z": zscores(prof, ex)}
        print(f"A N={N} done {time.time()-t0:.1f}s", flush=True)
    # (ii) Lubkin and higher moments on general (m, n), sampled directly as normalised Ginibre
    lub = []
    for (m, n) in [(2, 2), (2, 3), (2, 16), (3, 5), (4, 4), (4, 64), (8, 8), (16, 16), (8, 128), (32, 32)]:
        rng = np.random.default_rng(ss.spawn(1)[0])
        ns = 40000 if m * n <= 256 else 10000
        p = rmt.haar_reduced_spectra(m, n, ns, rng)
        row = {"m": m, "n": n, "n_samples": ns}
        for k in (2, 3, 4):
            v = R.trace_moment(p, k)
            ex = R.haar_trace_moment(k, m, n)
            row[f"tr{k}_mean"] = float(v.mean())
            row[f"tr{k}_sem"] = float(sem(v))
            row[f"tr{k}_exact"] = ex
            row[f"tr{k}_z"] = float((v.mean() - ex) / sem(v))
        lub.append(row)
    res["moments_mn"] = lub
    res["moments_max_abs_z"] = float(max(abs(r[f"tr{k}_z"]) for r in lub for k in (2, 3, 4)))
    res["runtime_s"] = time.time() - t0
    json.dump(res, open(os.path.join(PARTS, "A.json"), "w"), indent=1)
    print("A done", res["runtime_s"], "max|z|", res["moments_max_abs_z"], flush=True)


# ============================================================================ part B
def part_B():
    t0 = time.time()
    ss = np.random.SeedSequence(SEED_B)
    res = {"seed_base": SEED_B, "model": "fixed-trace complex Wishart = reduced states of Haar states (random-matrix model)",
           "mp_assumptions": "d_A, d_B -> infinity with c = d_A/d_B fixed; x = d_A * lambda",
           "r_reference": {"poisson": rmt.R_POISSON, "goe": rmt.R_GOE, "gue": rmt.R_GUE}}
    sizes = [8, 16, 32, 64, 128, 256]
    for c_inv in (1, 4):
        c = 1.0 / c_inv
        lo, hi = rmt.mp_edges(c)
        rows = []
        for dA in sizes:
            dB = dA * c_inv
            ns = int(max(128, min(20000, 2**16 // dA)))
            rng = np.random.default_rng(ss.spawn(1)[0])
            p = rmt.haar_reduced_spectra(dA, dB, ns, rng)
            x = dA * p
            xmax = x[:, -1]
            xmin = x[:, 0]
            r_mean, r_se, n_r = rmt.mean_gap_ratio(p)
            row = {"dA": dA, "dB": dB, "n_samples": ns, "n_eigs": int(x.size),
                   "ks_mp": rmt.ks_distance_mp(x, c),
                   "ks_noise_scale_1_over_sqrt_n": 1.0 / math.sqrt(x.size),
                   "xmax_mean": float(xmax.mean()), "xmax_sem": float(sem(xmax)),
                   "edge_hi": hi, "edge_dev": float(hi - xmax.mean()),
                   "edge_dev_scaled_dA^2/3": float((hi - xmax.mean()) * dA ** (2 / 3)),
                   "xmin_mean": float(xmin.mean()), "edge_lo": lo,
                   "dA_purity_mean": float((dA * R.trace_moment(p, 2)).mean()),
                   "dA_purity_exact": dA * R.lubkin_purity(dA, dB), "mp_moment2": rmt.mp_moment(2, c),
                   "dA2_tr3_exact": dA**2 * R.haar_trace_moment(3, dA, dB), "mp_moment3": rmt.mp_moment(3, c),
                   "S1_mean": float(R.renyi(p, 1).mean()), "page_exact": P.page_entropy(dA, dB),
                   "mp_S1_leading": math.log(dA) - rmt.mp_xlogx(c),
                   "r_mean": r_mean, "r_sem": r_se, "n_ratios": n_r}
            if dA in (64, 256):
                h, edges = np.histogram(x.ravel(), bins=80, range=(0, hi * 1.08), density=True)
                row["hist"] = {"density": h.tolist(), "edges": edges.tolist()}
            rows.append(row)
            print(f"B c={c} dA={dA} ks={row['ks_mp']:.4f} r={r_mean:.4f} {time.time()-t0:.1f}s", flush=True)
        # finite-size exponent of the KS distance and of the edge deviation (log-log least squares
        # over dA >= 16)
        sel = [r for r in rows if r["dA"] >= 16]
        lx = np.log([r["dA"] for r in sel])
        ks_slope = float(np.polyfit(lx, np.log([r["ks_mp"] for r in sel]), 1)[0])
        ed = [r["edge_dev"] for r in sel]
        edge_slope = float(np.polyfit(lx, np.log(ed), 1)[0]) if min(ed) > 0 else float("nan")
        res[f"c={c}"] = {"c": c, "rows": rows, "ks_loglog_slope": ks_slope, "edge_dev_loglog_slope": edge_slope,
                          "mp_cdf_mass": rmt.mp_cdf_norm(c), "mp_xlogx": rmt.mp_xlogx(c), "mp_xlogx_exact": c / 2}
    res["runtime_s"] = time.time() - t0
    json.dump(res, open(os.path.join(PARTS, "B.json"), "w"), indent=1)
    print("B done", res["runtime_s"], flush=True)


# ============================================================================ part C
def brickwork_states(N, depths, gate, rng):
    """States after the first D layers of ONE brickwork circuit, for every D in depths."""
    s = C.zero_state(N)
    out = {}
    for layer in range(max(depths)):
        s = C.apply_brick_layer(s, N, layer, rng, gate)
        if layer + 1 in depths:
            out[layer + 1] = s.copy()
    return out


def part_C():
    t0 = time.time()
    ss = np.random.SeedSequence(SEED_C)
    res = {"seed_base": SEED_C,
           "models": {"haar": "Haar-random pure state on N qubits",
                      "stabilizer": "random 2-qubit-Clifford brickwork of depth 6N applied to |0..0> "
                                    "(converges to the uniform random stabilizer state; depths N,2N,4N,6N recorded as a convergence check)",
                      "brick_D": "Haar 2-qubit-gate brickwork of depth D on an open chain, from |0..0>"}}
    for N, ns in ((12, 300), (8, 600)):
        ex = exact_curves(N)
        blk = {"n_samples": ns, "exact": ex}
        # Haar
        rng = np.random.default_rng(ss.spawn(1)[0])
        prof, half = cut_profile([C.haar_state(N, rng) for _ in range(ns)], N)
        r_haar = rmt.mean_gap_ratio(half)
        blk["haar"] = {"stats": summarise(prof), "z": zscores(prof, ex), "half_r": r_haar,
                       "half_spectra_sample": half[:3].tolist()}
        haar_prof = prof
        print(f"C N={N} haar {time.time()-t0:.1f}s", flush=True)
        # stabilizer (deep Clifford brickwork)
        rng = np.random.default_rng(ss.spawn(1)[0])
        cdepths = [N, 2 * N, 4 * N, 6 * N]
        st = [brickwork_states(N, cdepths, "clifford", rng) for _ in range(ns)]
        blk["stabilizer_by_depth"] = {}
        for D in cdepths:
            prof, half = cut_profile([s[D] for s in st], N)
            flat = [rmt.flatness(h) for h in half]
            blk["stabilizer_by_depth"][D] = {
                "stats": summarise(prof), "z": zscores(prof, ex),
                "max_S2_minus_Sinf_any_cut": float(np.max(np.abs(prof["S2_minus_Sinf"]))),
                "max_capacity_any_cut": float(np.max(np.abs(prof["capacity"]))),
                "max_S05_minus_Sinf_any_cut": float(np.max(np.abs(prof["S_0.5"] - prof["S_inf"]))),
                "half_flat_max_rel_dev": float(max(f["max_rel_dev"] for f in flat)),
                "half_log2_rank_counts": {str(int(k)): int(v) for k, v in zip(*np.unique([f["log2_rank"] for f in flat], return_counts=True))},
                "half_r": rmt.mean_gap_ratio(half)}
            if D == 6 * N:
                stab_prof = prof
        print(f"C N={N} stabilizer {time.time()-t0:.1f}s", flush=True)
        # brickwork Haar circuits
        rng = np.random.default_rng(ss.spawn(1)[0])
        bdepths = [1, 2, 3, 4, 6, 8, 12, 16, 24] if N == 12 else [1, 2, 3, 4, 6, 8, 12, 16]
        bs = [brickwork_states(N, bdepths, "haar", rng) for _ in range(ns)]
        blk["brick"] = {}
        haar_mean = {k: v.mean(0) for k, v in haar_prof.items()}
        for D in bdepths:
            prof, half = cut_profile([s[D] for s in bs], N)
            m = {k: v.mean(0) for k, v in prof.items()}
            blk["brick"][D] = {"stats": summarise(prof), "z": zscores(prof, ex),
                               "max_dev_S1_vs_page": float(np.max(np.abs(m["S_1"] - np.array(ex["page_S1"])))),
                               "max_dev_S2_vs_haar": float(np.max(np.abs(m["S_2"] - haar_mean["S_2"]))),
                               "max_dev_Sinf_vs_haar": float(np.max(np.abs(m["S_inf"] - haar_mean["S_inf"]))),
                               "max_dev_delta_vs_haar": float(np.max(np.abs(m["S2_minus_Sinf"] - haar_mean["S2_minus_Sinf"]))),
                               "max_dev_capacity_vs_haar": float(np.max(np.abs(m["capacity"] - haar_mean["capacity"]))),
                               "half_r": rmt.mean_gap_ratio(half, floor=1e-12)}
        print(f"C N={N} brick {time.time()-t0:.1f}s", flush=True)
        # distinguishability at the half cut: d' = |mu1-mu2| / sqrt((s1^2+s2^2)/2) per sample
        h = N // 2
        dprime = {}
        for key in ("S_1", "S_2", "S_inf", "S2_minus_Sinf", "capacity"):
            a, b = haar_prof[key][:, h], stab_prof[key][:, h]
            pooled = math.sqrt(0.5 * (a.var(ddof=1) + b.var(ddof=1)))
            dprime[key] = {"haar_mean": float(a.mean()), "haar_sem": float(sem(a)), "stab_mean": float(b.mean()),
                           "stab_sem": float(sem(b)), "diff": float(a.mean() - b.mean()),
                           "d_prime": float(abs(a.mean() - b.mean()) / pooled) if pooled > 0 else float("inf")}
        blk["haar_vs_stab_half_cut"] = dprime
        blk["max_dev_S1_stab_vs_page"] = float(np.max(np.abs(stab_prof["S_1"].mean(0) - np.array(ex["page_S1"]))))
        res[f"N{N}"] = blk
    res["runtime_s"] = time.time() - t0
    json.dump(res, open(os.path.join(PARTS, "C.json"), "w"), indent=1, default=float)
    print("C done", res["runtime_s"], flush=True)


# ============================================================================ part E
SEED_E = 20261115_5


def part_E():
    """Finer / deeper brickwork depth grid (N = 10, 12) to locate the depth at which each
    statistic is within eps = 0.05 nats of its Haar value at every cut."""
    t0 = time.time()
    ss = np.random.SeedSequence(SEED_E)
    res = {"seed_base": SEED_E, "model": "Haar 2-qubit-gate brickwork, open chain, from |0..0>"}
    for N, ns, depths in ((10, 300, [4, 8, 12, 16, 20, 24, 32, 40]), (12, 300, [16, 20, 24, 28, 32, 40, 48])):
        ex = exact_curves(N)
        rng = np.random.default_rng(ss.spawn(1)[0])
        hprof, _ = cut_profile([C.haar_state(N, rng) for _ in range(ns)], N)
        hm = {k: v.mean(0) for k, v in hprof.items()}
        rng = np.random.default_rng(ss.spawn(1)[0])
        bs = [brickwork_states(N, depths, "haar", rng) for _ in range(ns)]
        blk = {"n_samples": ns, "haar_stats": summarise(hprof), "brick": {}}
        for D in depths:
            prof, half = cut_profile([s[D] for s in bs], N)
            m = {k: v.mean(0) for k, v in prof.items()}
            sm = summarise(prof)
            hs = summarise(hprof)
            dev = {}
            for key, ref in (("S_1", np.array(ex["page_S1"])), ("S_2", hm["S_2"]), ("S_3", hm["S_3"]),
                             ("S_inf", hm["S_inf"]), ("S2_minus_Sinf", hm["S2_minus_Sinf"]), ("capacity", hm["capacity"])):
                d = np.abs(m[key] - ref)
                comb = np.sqrt(np.array(sm[key]["sem"]) ** 2 + (0 if key == "S_1" else np.array(hs[key]["sem"]) ** 2))
                i = int(np.argmax(d))
                dev[key] = {"max_dev": float(d[i]), "at_cut": i, "sem_at_cut": float(comb[i])}
            blk["brick"][D] = {"stats": sm, "max_dev": dev, "half_r": rmt.mean_gap_ratio(half, floor=1e-12)}
        res[f"N{N}"] = blk
        print(f"E N={N} {time.time()-t0:.1f}s", flush=True)
    json.dump(res, open(os.path.join(PARTS, "E.json"), "w"), indent=1, default=float)
    print("E done", flush=True)


# ============================================================================ part D
def part_D():
    """Exact uniform stabilizer ensemble (complete enumeration, N = 2, 3, 4): exact averages of
    Tr rho^k, k = 2, 3, 4, and of S_1 at every contiguous cut, vs the exact Haar values."""
    from fractions import Fraction
    t0 = time.time()
    res = {"model": "uniform random stabilizer states, complete enumeration (no sampling, no seed)",
           "prediction": "Clifford orbit is a state 3-design => E Tr rho^k (k=2,3) equal Haar exactly; k=4 need not"}
    for N in (2, 3, 4):
        S = rmt.enumerate_stabilizer_states(N)
        assert len(S) == rmt.n_stabilizer_states(N)
        cuts = []
        for k in range(1, N):
            m, n = 2**k, 2 ** (N - k)
            mats = S.reshape(len(S), m, n)
            ev = np.clip(np.linalg.eigvalsh(mats @ np.conj(np.swapaxes(mats, 1, 2))), 0, None)
            ranks = (ev > 1e-9).sum(1)
            vals, cnt = np.unique(ranks, return_counts=True)
            M = len(S)
            row = {"k": k, "dims": [m, n], "n_states": M,
                   "rank_counts": {str(int(v)): int(c) for v, c in zip(vals, cnt)}}
            for q in (2, 3, 4):
                exact_stab = sum(Fraction(int(c), M) * Fraction(1, int(v)) ** (q - 1) for v, c in zip(vals, cnt))
                hq = R.haar_trace_moment(q, m, n)
                row[f"tr{q}_stab_exact"] = str(exact_stab)
                row[f"tr{q}_stab"] = float(exact_stab)
                row[f"tr{q}_haar"] = hq
                row[f"tr{q}_diff"] = float(exact_stab) - hq
                row[f"tr{q}_stab_float_check"] = float(R.trace_moment(ev, q).mean())
            row["S1_stab"] = float(sum(c * math.log(v) for v, c in zip(vals, cnt)) / M)
            row["S1_page"] = P.page_entropy(m, n)
            row["S1_diff"] = row["S1_stab"] - row["S1_page"]
            row["max_flat_dev"] = float(max(np.max(np.abs(e[e > 1e-9] * (e > 1e-9).sum() - 1)) for e in ev))
            cuts.append(row)
        res[f"N{N}"] = cuts
        print(f"D N={N} {len(S)} states {time.time()-t0:.1f}s", flush=True)
    json.dump(res, open(os.path.join(PARTS, "D.json"), "w"), indent=1)
    print("D done", flush=True)


def _fix_z(obj):
    """Cuts whose empirical SEM is numerically zero (every sample identical, e.g. all stabilizer
    samples maximally mixed on one qubit) have no meaningful z-score: set to None, recompute max."""
    if isinstance(obj, dict):
        if "stats" in obj and "z" in obj:
            for key, zk in obj["z"].items():
                st = obj["stats"][key]
                z = [None if (sd <= 1e-12 or not math.isfinite(zz)) else zz
                     for zz, sd in zip(zk["z_per_cut"], st["sem"])]
                zk["z_per_cut"] = z
                valid = [abs(v) for v in z if v is not None]
                zk["max_abs_z"] = max(valid) if valid else None
                zk["n_cuts_zero_variance"] = sum(v is None for v in z)
        for v in obj.values():
            _fix_z(v)
    return obj


TW2_MEAN = -1.7710868074  # mean of the GUE Tracy-Widom distribution


def tw_edge_prediction(dA, dB):
    """Leading soft-edge shift of <x_max> = d_A <lambda_max>: x_+ + s * E[TW2] with
    s = (sqrt dA + sqrt dB)(1/sqrt dA + 1/sqrt dB)^{1/3} / dB (Johansson 2000; Johnstone 2001)."""
    a, b = math.sqrt(dA), math.sqrt(dB)
    return (a + b) * (1 / a + 1 / b) ** (1 / 3) / dB * TW2_MEAN


# ============================================================================ plots + merge
def plot():
    from _style import setup, caption, PALETTE, CYAN, AMBER, MAGENTA, GREEN, GREY, FG
    plt = setup()
    A = json.load(open(os.path.join(PARTS, "A.json")))
    B = json.load(open(os.path.join(PARTS, "B.json")))
    Cc = _fix_z(json.load(open(os.path.join(PARTS, "C.json"))))
    A = _fix_z(A)
    Dd = json.load(open(os.path.join(PARTS, "D.json")))
    for cname in ("c=1.0", "c=0.25"):
        for r in B[cname]["rows"]:
            r["tw_pred_edge_dev"] = -tw_edge_prediction(r["dA"], r["dB"])
            r["edge_dev_over_tw_pred"] = r["edge_dev"] / r["tw_pred_edge_dev"]

    # ---------------- f1: Renyi Page curves
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.4))
    blk = A["N12"]
    N = 12
    ks = np.arange(N + 1)
    for i, key in enumerate(NS_KEY):
        st = blk["stats"][key]
        ax[0].errorbar(ks, st["mean"], yerr=st["sem"], fmt="o", ms=3.5, color=PALETTE[i], label=f"⟨{key}⟩ Haar (400 seeds)")
    ax[0].plot(ks, blk["exact"]["page_S1"], "-", color=FG, lw=0.9, label="Page exact ⟨S_1⟩")
    ax[0].plot(ks, blk["exact"]["annealed_S2"], "--", color=AMBER, lw=0.9, label="−log E Tr ρ² (Lubkin, exact)")
    ax[0].plot(ks, blk["exact"]["annealed_S3"], ":", color=MAGENTA, lw=0.9, label="−½ log E Tr ρ³ (exact)")
    ax[0].set_xlabel("subsystem size k (qubits), N = 12")
    ax[0].set_ylabel("Rényi entropy S_n (nats)")
    ax[0].set_title("Rényi-n Page curves of Haar states")
    ax[0].legend(loc="upper left", fontsize=6.5)
    rows = A["moments_mn"]
    lab = [f"{r['m']}×{r['n']}" for r in rows]
    xx = np.arange(len(rows))
    for j, (k, col) in enumerate(((2, CYAN), (3, AMBER), (4, MAGENTA))):
        ax[1].errorbar(xx + (j - 1) * 0.22, [r[f"tr{k}_z"] for r in rows], yerr=1.0, fmt="o", color=col, ms=4,
                       label=f"k={k}: (mean Tr ρ^k − exact)/SEM")
    ax[1].axhspan(-2, 2, color=GREY, alpha=0.15)
    ax[1].axhline(0, color=FG, lw=0.6)
    ax[1].set_xticks(xx)
    ax[1].set_xticklabels(lab, rotation=45, fontsize=7)
    ax[1].set_xlabel("dimensions d_A × d_B")
    ax[1].set_ylabel("z-score vs exact Haar moment")
    ax[1].set_title("Lubkin purity (k=2) and exact k=3,4 moments")
    ax[1].legend(fontsize=6.5)
    caption(fig, "Finite-dimensional Haar-state model. Exact: Page (1993); Lubkin (1978); k=3,4 from complex-Wishart moments. Seeds: SeedSequence(%d)." % A["seed_base"])
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(os.path.join(FIGURES, "f1_renyi_page.png"), dpi=150)
    plt.close(fig)

    # ---------------- f2: MP
    fig, ax = plt.subplots(2, 2, figsize=(11, 8))
    for col, cname in enumerate(("c=1.0", "c=0.25")):
        blk = B[cname]
        c = blk["c"]
        row = [r for r in blk["rows"] if r["dA"] == 256][0]
        e = np.array(row["hist"]["edges"])
        ctr = 0.5 * (e[1:] + e[:-1])
        ax[0, col].bar(ctr, row["hist"]["density"], width=np.diff(e), color=CYAN, alpha=0.55, label=f"d_A={row['dA']}, d_B={row['dB']}, {row['n_samples']} states")
        r64 = [r for r in blk["rows"] if r["dA"] == 64][0]
        e2 = np.array(r64["hist"]["edges"])
        ax[0, col].step(0.5 * (e2[1:] + e2[:-1]), r64["hist"]["density"], where="mid", color=AMBER, lw=0.9, label="d_A=64")
        xg = np.linspace(1e-4, rmt.mp_edges(c)[1] * 1.05, 800)
        ax[0, col].plot(xg, rmt.mp_density(xg, c), color=FG, lw=1.2, label=f"Marchenko–Pastur c={c:g}")
        ax[0, col].set_xlabel("x = d_A λ  (scaled eigenvalue of ρ_A)")
        ax[0, col].set_ylabel("density")
        ax[0, col].set_title(f"Entanglement spectrum vs MP, c = d_A/d_B = {c:g}")
        if c == 1.0:
            ax[0, col].set_ylim(0, 2.0)
        ax[0, col].legend(fontsize=7)
    for i, cname in enumerate(("c=1.0", "c=0.25")):
        blk = B[cname]
        d = [r["dA"] for r in blk["rows"]]
        ax[1, 0].loglog(d, [r["ks_mp"] for r in blk["rows"]], "o-", color=PALETTE[i], label=f"KS distance to MP, {cname} (slope {blk['ks_loglog_slope']:.2f})")
        ax[1, 0].loglog(d, [r["edge_dev"] for r in blk["rows"]], "s", color=PALETTE[i + 2], label=f"x_+ − ⟨x_max⟩, {cname} (slope {blk['edge_dev_loglog_slope']:.2f})")
        ax[1, 0].loglog(d, [r["tw_pred_edge_dev"] for r in blk["rows"]], "-", lw=0.8, color=PALETTE[i + 2], label=f"Tracy–Widom prediction (no fit), {cname}")
        ax[1, 1].errorbar(d, [r["r_mean"] for r in blk["rows"]], yerr=[r["r_sem"] for r in blk["rows"]], fmt="o-", color=PALETTE[i], ms=4, label=f"⟨r⟩ {cname}")
    dd = np.array([8, 256])
    ax[1, 0].loglog(dd, 0.3 * dd ** (-1.0), "-.", color=GREY, label="∝ d_A^{−1}")
    ax[1, 0].set_xlabel("d_A")
    ax[1, 0].set_ylabel("finite-size deviation")
    ax[1, 0].set_title("Finite-size corrections to MP")
    ax[1, 0].legend(fontsize=6.5)
    for val, name, col in ((rmt.R_GUE, "GUE 0.5996", GREEN), (rmt.R_GOE, "GOE 0.5307", AMBER), (rmt.R_POISSON, "Poisson 0.386", MAGENTA)):
        ax[1, 1].axhline(val, color=col, lw=0.8, ls="--", label=name)
    ax[1, 1].set_xscale("log", base=2)
    ax[1, 1].set_xlabel("d_A")
    ax[1, 1].set_ylabel("mean adjacent-gap ratio ⟨r⟩")
    ax[1, 1].set_title("Level-spacing statistics of ρ_A")
    ax[1, 1].legend(fontsize=6.5)
    caption(fig, "Random-matrix model (fixed-trace complex Wishart). MP applies for d_A,d_B→∞ at fixed c. Seeds: SeedSequence(%d)." % B["seed_base"])
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(os.path.join(FIGURES, "f2_spectrum_mp.png"), dpi=150)
    plt.close(fig)

    # ---------------- f3: ensembles
    blk = Cc["N12"]
    N = 12
    ks = np.arange(N + 1)
    Dst = str(6 * N)
    fig, axs = plt.subplots(2, 3, figsize=(16, 8))
    ax = axs[:, :2]
    ens = [("Haar", blk["haar"]["stats"], CYAN), ("stabilizer", blk["stabilizer_by_depth"][Dst]["stats"], MAGENTA)]
    bcols = {"2": "#9AD1FF", "4": "#B8A1FF", "8": AMBER, "24": GREEN}
    for D, col in bcols.items():
        if D in blk["brick"]:
            ens.append((f"brickwork D={D}", blk["brick"][D]["stats"], col))
    for name, st, col in ens:
        ax[0, 0].errorbar(ks, st["S_1"]["mean"], yerr=st["S_1"]["sem"], fmt="o-", ms=3, lw=0.8, color=col, label=name)
        ax[0, 1].errorbar(ks, st["S2_minus_Sinf"]["mean"], yerr=st["S2_minus_Sinf"]["sem"], fmt="o-", ms=3, lw=0.8, color=col, label=name)
    ax[0, 0].plot(ks, blk["exact"]["page_S1"], color=FG, lw=0.8, ls="--", label="Page exact")
    ax[0, 0].set_xlabel("subsystem size k (qubits), N = 12")
    ax[0, 0].set_ylabel("⟨S_1⟩ (nats)")
    ax[0, 0].set_title("Mean von Neumann Page curves")
    ax[0, 0].legend(fontsize=6.5)
    ax[0, 1].set_xlabel("subsystem size k (qubits), N = 12")
    ax[0, 1].set_ylabel("⟨S_2 − S_∞⟩ (nats)")
    ax[0, 1].set_title("Distinguishing metric: S_2 − S_∞ (0 for flat spectra)")
    ax[0, 1].legend(fontsize=6.5)
    # Renyi-n at half cut per ensemble
    h = N // 2
    names = [e[0] for e in ens]
    xx = np.arange(len(NS_KEY))
    w = 0.8 / len(ens)
    for i, (name, st, col) in enumerate(ens):
        ax[1, 0].bar(xx + (i - len(ens) / 2 + 0.5) * w, [st[k]["mean"][h] for k in NS_KEY], width=w, color=col,
                     yerr=[st[k]["sem"][h] for k in NS_KEY], label=name)
    ax[1, 0].set_xticks(xx)
    ax[1, 0].set_xticklabels(["n=1/2", "n=1", "n=2", "n=3", "n=∞"])
    ax[1, 0].set_ylabel("⟨S_n⟩ at half cut (nats)")
    ax[1, 0].set_ylim(2.0, 4.4)
    ax[1, 0].set_title("Rényi-n at the half cut, k = 6")
    ax[1, 0].legend(fontsize=6.5, ncol=2)
    bd = sorted(int(d) for d in blk["brick"])
    for key, lab, col in (("max_dev_S1_vs_page", "max_k |⟨S_1⟩ − Page|", CYAN),
                          ("max_dev_S2_vs_haar", "max_k |⟨S_2⟩ − ⟨S_2⟩_Haar|", AMBER),
                          ("max_dev_Sinf_vs_haar", "max_k |⟨S_∞⟩ − ⟨S_∞⟩_Haar|", MAGENTA),
                          ("max_dev_delta_vs_haar", "max_k |⟨S_2−S_∞⟩ − Haar|", GREEN),
                          ("max_dev_capacity_vs_haar", "max_k |⟨C_E⟩ − Haar|", "#B8A1FF")):
        ax[1, 1].semilogy(bd, [blk["brick"][str(d)][key] for d in bd], "o-", ms=3.5, color=col, label=lab)
    ax[1, 1].axhline(0.05, color=GREY, ls=":", lw=0.8, label="ε = 0.05 nats")
    ax[1, 1].set_xlabel("brickwork depth D (Haar 2-qubit gates)")
    ax[1, 1].set_ylabel("max deviation over cuts (nats)")
    ax[1, 1].set_title("Convergence of brickwork circuits to Haar")
    ax[1, 1].legend(fontsize=6.5)
    # exact stabilizer vs Haar moments (complete enumeration)
    a5 = axs[0, 2]
    labels, xs = [], 0
    for N in (2, 3, 4):
        for row in Dd[f"N{N}"]:
            for j, (q, col) in enumerate(((2, CYAN), (3, AMBER), (4, MAGENTA))):
                rel = row[f"tr{q}_diff"] / row[f"tr{q}_haar"]
                a5.bar(xs + (j - 1) * 0.27, rel, width=0.25, color=col, label=f"k={q}" if xs == 0 else None)
            labels.append(f"N={N}\nk_A={row['k']}")
            xs += 1
    a5.axhline(0, color=FG, lw=0.6)
    a5.set_xticks(range(xs))
    a5.set_xticklabels(labels, fontsize=7)
    a5.set_ylabel("(E_stab Tr ρ^k − E_Haar Tr ρ^k) / E_Haar")
    a5.set_title("Exact stabilizer ensemble: 3-design, not 4-design")
    a5.legend(fontsize=7)
    a6 = axs[1, 2]
    for name, key, col in (("Haar", None, CYAN), ("stabilizer (D=6N)", None, MAGENTA)):
        pass
    for i, (nm, blkN) in enumerate((("N=8", Cc["N8"]), ("N=12", Cc["N12"]))):
        bdd = sorted(int(d) for d in blkN["brick"])
        hh = int(nm.split("=")[1]) // 2
        a6.errorbar(bdd, [blkN["brick"][str(d)]["stats"]["S2_minus_Sinf"]["mean"][hh] for d in bdd],
                    yerr=[blkN["brick"][str(d)]["stats"]["S2_minus_Sinf"]["sem"][hh] for d in bdd],
                    fmt="o-", ms=3.5, color=PALETTE[i], label=f"brickwork, {nm}")
        a6.axhline(blkN["haar"]["stats"]["S2_minus_Sinf"]["mean"][hh], color=PALETTE[i], ls="--", lw=0.8, label=f"Haar, {nm}")
    a6.axhline(0, color=MAGENTA, lw=1.0, label="stabilizer (exactly 0)")
    a6.set_xlabel("brickwork depth D")
    a6.set_ylabel("⟨S_2 − S_∞⟩ at half cut (nats)")
    a6.set_title("Half-cut spectral width vs depth")
    a6.legend(fontsize=6.5)
    caption(fig, "Finite-dimensional circuit models only (N=12; 300 seeds each, SEM bars). Stabilizer = depth-72 random-Clifford brickwork; top-right panel: complete enumeration (exact). Seeds: SeedSequence(%d)." % Cc["seed_base"])
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(os.path.join(FIGURES, "f3_ensembles_distinguish.png"), dpi=150)
    plt.close(fig)

    merged = {"experiment": "f_spectra (upgrade tracks A, B, direction 6)",
              "time_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "backend": "numpy (local CPU), complex128", "A_renyi": A, "B_rmt": B, "C_ensembles": Cc,
              "D_stabilizer_exact": Dd}
    json.dump(merged, open(os.path.join(RESULTS, "f_spectra.json"), "w"), indent=1, default=float)
    print("wrote results/f_spectra.json and figures f1-f3")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "plot"
    {"A": part_A, "B": part_B, "C": part_C, "D": part_D, "E": part_E, "plot": plot}[which]()
