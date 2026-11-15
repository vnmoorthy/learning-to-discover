"""Tracks E + F: black holes as QEC codes (finite-dim) and island toy models (semiclassical formulas).

Run (CPU, ~minutes):  OMP_NUM_THREADS=1 python3 experiments/h_qec_islands.py
Outputs: results/h_qec_islands.json, figures/h1_qec_erasure.png, figures/h2_island_page_curve.png
All QEC numbers are exact linear algebra on statevectors (complex128); seeds are recorded.
Island numbers are closed-form semiclassical expressions (eh/islands.py) - a different category.
"""
import itertools
import json
import os
import sys
import time
from math import comb
from multiprocessing import Pool

os.environ.setdefault("OMP_NUM_THREADS", "1")
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np  # noqa: E402

from eh import qec, islands as isl  # noqa: E402
from eh.page import page_entropy  # noqa: E402

RESULTS = os.path.join(ROOT, "results")
FIGURES = os.path.join(ROOT, "figures")
LOG2 = np.log(2.0)
BASE_SEED = 20261115
MAX_PETZ_PER_E = 12
TOL = 1e-8
FAMILY_ID = {"513": 0, "stabilizer": 1, "haar": 2}


def run_code(args):
    family, n, seed = args
    rng = np.random.default_rng(np.random.SeedSequence([BASE_SEED, FAMILY_ID[family], n, seed]))
    if family == "513":
        _, V = qec.five_qubit_code()
    elif family == "stabilizer":
        V = qec.random_clifford_isometry(n, rng)
    else:
        V = qec.haar_isometry(n, rng)
    iso_err = float(np.abs(V.conj().T @ V - np.eye(2)).max())
    per_e = []
    I_RE_all = {}
    for e in range(n + 1):
        subsets = list(itertools.combinations(range(n), e))
        I_RA = []
        for E in subsets:
            d = qec.erasure_diagnostics(V, E, with_petz=False)
            I_RA.append(d["I_RA"])
            I_RE_all[E] = d["I_RE"]
        I_RA = np.array(I_RA)
        pick = rng.permutation(len(subsets))[:MAX_PETZ_PER_E]
        F = np.array([qec.erasure_diagnostics(V, subsets[i], with_petz=True)["F_petz"] for i in pick])
        per_e.append({
            "e_erased": e, "a_kept": n - e, "n_subsets": len(subsets),
            "I_RA_bits_mean": float(I_RA.mean() / LOG2), "I_RA_bits_min": float(I_RA.min() / LOG2),
            "I_RA_bits_max": float(I_RA.max() / LOG2),
            "frac_correctable": float(np.mean(I_RA > 2 * LOG2 - TOL)),
            "frac_I_RA_ge_1.9bits": float(np.mean(I_RA / LOG2 >= 1.9)),
            "F_petz_mean": float(F.mean()), "F_petz_min": float(F.min()), "n_petz": int(len(F)),
            "integer_valued_bits": bool(np.all(np.abs(I_RA / LOG2 - np.round(I_RA / LOG2)) < 1e-8)),
        })
    dist = qec.code_distance_from_erasures(I_RE_all, n)
    return {"family": family, "n": n, "seed": seed, "isometry_err": iso_err, "distance": dist, "per_e": per_e}


def aggregate(runs):
    out = {}
    for fam in ["513", "stabilizer", "haar"]:
        for n in sorted({r["n"] for r in runs if r["family"] == fam}):
            rs = [r for r in runs if r["family"] == fam and r["n"] == n]
            rows = []
            for e in range(n + 1):
                vals = [r["per_e"][e] for r in rs]
                I = np.array([v["I_RA_bits_mean"] for v in vals])
                fc = np.array([v["frac_correctable"] for v in vals])
                F = np.array([v["F_petz_mean"] for v in vals])
                row = {"e_erased": e, "a_kept": n - e,
                       "I_RA_bits_mean": float(I.mean()), "I_RA_bits_sem": float(I.std(ddof=1) / np.sqrt(len(I))) if len(I) > 1 else 0.0,
                       "frac_correctable_mean": float(fc.mean()),
                       "F_petz_mean": float(F.mean()), "F_petz_sem": float(F.std(ddof=1) / np.sqrt(len(F))) if len(F) > 1 else 0.0,
                       "F_opt_upper_sqrtPetz": float(np.sqrt(F).mean()),
                       "all_integer_bits": bool(all(v["integer_valued_bits"] for v in vals))}
                if fam == "haar":
                    row["I_RA_bits_page_approx"] = float(qec.page_approx_I_RA(n, n - e) / LOG2)
                rows.append(row)
            d = np.array([r["distance"] for r in rs])
            # "how much radiation is needed": smallest kept |A| with mean I(R:A) >= 1.9 bits / fraction >= 1/2
            a_I = min([row["a_kept"] for row in rows if row["I_RA_bits_mean"] >= 1.9], default=None)
            a_half = min([row["a_kept"] for row in rows if row["frac_correctable_mean"] >= 0.5], default=None)
            out[f"{fam}_n{n}"] = {
                "family": fam, "n": n, "n_seeds": len(rs), "seeds": [r["seed"] for r in rs],
                "max_isometry_err": float(max(r["isometry_err"] for r in rs)),
                "distance_hist": {str(k): int((d == k).sum()) for k in sorted(set(d.tolist()))},
                "distance_mean": float(d.mean()),
                "a_kept_needed_I_ge_1.9bits": a_I, "a_kept_needed_half_patterns_perfect": a_half,
                "rows": rows}
            if fam == "haar":
                out[f"{fam}_n{n}"]["distance_note"] = (
                    "exact-erasure distance (tol 1e-8) is not meaningful for Haar isometries, which correct no "
                    "erasure exactly; use the I(R:A) and F_petz curves (approximate recovery) instead")
    return out


def islands_part():
    P = dict(beta=2 * np.pi, c=24.0, eps=0.01, b=1.0, phi0=200.0)
    out = {"model1_params_base": P}
    phir_base = 20.0 * P["c"] * P["beta"] / (24 * np.pi) * np.e ** 0  # chosen so 24 pi phi_r/(c beta) = 20
    ext = isl.island_extremum(phir=phir_base, **P)
    tP, S_isl = isl.page_time_eternal(phir=phir_base, **P)
    out["model1_base"] = {"phi_r": phir_base, **ext, "t_Page": tP,
                          "t_Page_leading": isl.page_time_eternal_leading(phir=phir_base, **P),
                          "S_no_island_t0": float(isl.S_no_island(0.0, P["beta"], P["c"], P["eps"])),
                          "late_slope_numeric": float((isl.S_no_island(60.0, P["beta"], P["c"], P["eps"]) -
                                                       isl.S_no_island(50.0, P["beta"], P["c"], P["eps"])) / 10.0),
                          "late_slope_exact_2pic_over_3beta": float(2 * np.pi * P["c"] / (3 * P["beta"]))}
    scan = []
    for ratio in np.geomspace(0.5, 5e4, 25):  # ratio = phi_r / (c beta)
        phir = ratio * P["c"] * P["beta"]
        e = isl.island_extremum(phir=phir, **P)
        tP_, _ = isl.page_time_eternal(phir=phir, **P)
        scan.append({"phir_over_cbeta": float(ratio), **e, "t_Page": tP_,
                     "rel_err_vs_AMM": float(abs(e["a_star"] - e["a_AMM_asymptotic"]) / e["a_star"])})
    out["model1_scan_phir"] = scan
    m2 = []
    for g in [1.0, 4.0 / 3.0, 1.4847]:
        tPf, f = isl.page_time_evap(g)
        tt = np.linspace(0, 1, 200001)
        Sr = isl.S_rad_evap(tt, 1.0, 1.0, g)
        i = int(np.argmax(Sr))
        m2.append({"gamma": g, "t_Page_over_t_evap_exact": tPf, "S_BH_over_S0_at_tP": f,
                   "t_Page_numeric_grid": float(tt[i]), "S_rad_max_over_S0": float(Sr[i])})
    out["model2_evap"] = m2
    # finite-dimensional comparison: Page's formula for N qubits (exact Haar average; separate model)
    N = 20
    k = np.arange(N + 1)
    Spage = np.array([page_entropy(2 ** kk, 2 ** (N - kk)) for kk in k])
    x = k / N
    Smin = np.minimum(x, 1 - x) * N * LOG2  # gamma = 1 two-saddle cartoon in the same units
    out["finite_dim_vs_cartoon_N20"] = {
        "N_qubits": N, "x": x.tolist(), "S_page_nats": Spage.tolist(), "S_cartoon_gamma1_nats": Smin.tolist(),
        "max_abs_diff_nats": float(np.abs(Spage - Smin).max()),
        "diff_at_x_half_nats": float(Smin[N // 2] - Spage[N // 2]),
        "page_correction_reference_half_nat": 0.5,
        "note": "Same ideal shape min(x,1-x) by construction of the gamma=1 cartoon; the Page curve "
                "is smooth with a ~1/2-nat deficit at x=1/2. This is a shape comparison, not a derivation."}
    return out


def make_figures(agg, isl_out):
    from _style import setup, caption, CYAN, AMBER, MAGENTA, GREEN, GREY, PALETTE
    plt = setup()
    # ---------------- h1
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))
    colors = {5: CYAN, 7: AMBER, 9: MAGENTA, 11: GREEN}
    for key, v in agg.items():
        n = v["n"]
        a = np.array([r["a_kept"] for r in v["rows"]])
        I = np.array([r["I_RA_bits_mean"] for r in v["rows"]])
        F = np.array([r["F_petz_mean"] for r in v["rows"]])
        fc = np.array([r["frac_correctable_mean"] for r in v["rows"]])
        if v["family"] == "513":
            ax[0].plot(a / n, I, "s-", color="white", lw=2, ms=6, label="[[5,1,3]]", zorder=5)
            ax[1].plot(a / n, F, "s-", color="white", lw=2, ms=6, label="[[5,1,3]] Petz", zorder=5)
            ax[2].plot(1 - a / n, fc, "s-", color="white", lw=2, ms=6, label="[[5,1,3]]", zorder=5)
            continue
        ls = "-" if v["family"] == "haar" else "--"
        mk = "o" if v["family"] == "haar" else "^"
        lab = f"{'Haar' if v['family'] == 'haar' else 'stabilizer'} n={n}"
        ax[0].plot(a / n, I, ls, marker=mk, ms=4, color=colors[n], label=lab)
        ax[1].plot(a / n, F, ls, marker=mk, ms=4, color=colors[n], label=lab)
        ax[2].plot(1 - a / n, fc, ls, marker=mk, ms=4, color=colors[n], label=lab)
        if v["family"] == "haar" and n == 11:
            Ip = np.array([r["I_RA_bits_page_approx"] for r in v["rows"]])
            ax[0].plot(a / n, Ip, ":", color=GREY, lw=1.5, label="Page approx. (Haar n=11)")
    ax[0].axvline(0.5, color=GREY, lw=0.8, ls=":")
    ax[0].set_xlabel("fraction of physical qubits kept |A|/n  ('radiation collected')")
    ax[0].set_ylabel("mutual information I(R:A)  [bits]  (2 = perfectly recoverable)")
    ax[0].set_title("(a) logical information in the kept qubits")
    ax[1].set_xlabel("fraction of physical qubits kept |A|/n")
    ax[1].set_ylabel("Petz recovery entanglement fidelity  (<= F_opt <= sqrt F_Petz)")
    ax[1].set_title("(b) recovery fidelity from A")
    ax[1].axhline(0.25, color=GREY, lw=0.8, ls=":")
    ax[2].set_xlabel("fraction of physical qubits erased |E|/n")
    ax[2].set_ylabel("fraction of erasure patterns perfectly correctable")
    ax[2].set_title("(c) erasure thresholds vs code")
    ax[2].axvline(0.5, color=GREY, lw=0.8, ls=":")
    for a_ in ax:
        a_.legend(fontsize=6.5, ncol=2)
    caption(fig, "Finite-dimensional codes, 1 logical qubit + reference R; exact statevectors; seeds in results/h_qec_islands.json. "
                 "Illustrates the QEC language for black holes; it does not derive holography.")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(os.path.join(FIGURES, "h1_qec_erasure.png"), dpi=150)
    plt.close(fig)
    # ---------------- h2
    P = isl_out["model1_params_base"]
    phir = isl_out["model1_base"]["phi_r"]
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))
    t = np.linspace(0, 1.3 * isl_out["model1_base"]["t_Page"], 600)
    Sno = isl.S_no_island(t, P["beta"], P["c"], P["eps"])
    Sis = isl_out["model1_base"]["S_island"]
    ax[0].plot(t, Sno, "--", color=AMBER, label="no-island saddle")
    ax[0].plot(t, np.full_like(t, Sis), "--", color=MAGENTA, label="island saddle (min over a)")
    ax[0].plot(t, np.minimum(Sno, Sis), "-", color=CYAN, lw=2.2, label="S_rad = min over saddles")
    ax[0].axvline(isl_out["model1_base"]["t_Page"], color=GREY, ls=":", lw=1)
    ax[0].set_xlabel("boundary time t  (units with beta = 2 pi)")
    ax[0].set_ylabel("generalized entropy  [nats, 1/4G absorbed in phi]")
    ax[0].set_title("(a) eternal BH + bath (JT, AMM 2019 formulas)")
    ax[0].legend()
    a = np.linspace(0.05, 12, 800)
    Sg = isl.S_gen_island(a, phir=phir, **P)
    ax[1].plot(a, Sg, color=MAGENTA, label="S_gen(a), island at sigma=-a")
    ax[1].axvline(isl_out["model1_base"]["a_star"], color=CYAN, ls="-", lw=1, label="numerical extremum a*")
    ax[1].axvline(isl_out["model1_base"]["a_AMM_asymptotic"], color=AMBER, ls=":", lw=1.4, label="AMM asymptotic a*")
    ax[1].set_ylim(Sis - 5, Sis + 60)
    ax[1].set_xlabel("island endpoint depth a  (horizon at a -> infinity)")
    ax[1].set_ylabel("S_gen(a)  [nats]")
    ax[1].set_title("(b) locating the quantum extremal surface")
    ax[1].legend()
    cmp = isl_out["finite_dim_vs_cartoon_N20"]
    x = np.array(cmp["x"]); N = cmp["N_qubits"]
    ax[2].plot(x, np.array(cmp["S_page_nats"]) / (N * LOG2), "o", color=CYAN, ms=4,
               label=f"finite-dim Page curve, N={N} qubits (Page 1993)")
    tt = np.linspace(0, 1, 801)
    for g, col in [(1.0, GREEN), (1.4847, AMBER)]:
        xs = 1 - isl.S_BH_evap(tt, 1.0, 1.0)   # fraction of initial S_BH lost
        ax[2].plot(xs, isl.S_rad_evap(tt, 1.0, 1.0, g), "-", color=col,
                   label=f"semiclassical 2-saddle cartoon, gamma={g:g}")
    ax[2].set_xlabel("fraction of initial entropy radiated  (k/N  |  1 - S_BH(t)/S_0)")
    ax[2].set_ylabel("S_rad / S_0   (S_0 = N log 2 for the qubit model)")
    ax[2].set_title("(c) shapes only: separate models, neither derives the other")
    ax[2].legend(fontsize=7)
    caption(fig, "(a,b) closed-form semiclassical generalized entropy, JT gravity + bath, c=24, beta=2pi, eps=0.01, b=1, phi0=200; "
                 "(c) Haar-average finite-dimensional Page curve vs evaporating cartoon. Not a circuit derivation of the island formula.")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(os.path.join(FIGURES, "h2_island_page_curve.png"), dpi=150)
    plt.close(fig)


def main():
    t0 = time.time()
    seeds = {5: 40, 7: 40, 9: 30, 11: int(os.environ.get("EH_SEEDS_N11", 16))}
    jobs = [("513", 5, 0)]
    for fam in ["stabilizer", "haar"]:
        for n, ns in seeds.items():
            jobs += [(fam, n, s) for s in range(ns)]
    # warm Clifford cache in each worker lazily; 4 processes max
    with Pool(int(os.environ.get("EH_PROCS", 4))) as pool:
        runs = pool.map(run_code, jobs, chunksize=1)
    agg = aggregate(runs)
    # Knill-Laflamme for [[5,1,3]]
    _, V5 = qec.five_qubit_code()
    kl = {e: max(qec.knill_laflamme_deviation(V5, E, 5) for E in itertools.combinations(range(5), e)) for e in (1, 2)}
    kl3 = min(qec.knill_laflamme_deviation(V5, E, 5) for E in itertools.combinations(range(5), 3))
    isl_out = islands_part()
    res = {
        "problem": "H (Tracks E+F): QEC codes as black-hole toy models; island generalized-entropy toy models",
        "classification": {
            "513_perfect_code_erasure": "1 (reproduction: [[5,1,3]] is a perfect tensor / AME(6,2); I(R:A) = 0 or 2 bits)",
            "haar_isometry_erasure": "1-2 (reproduction of decoupling / Page-type threshold at |A| ~ n/2; exact numerics)",
            "random_stabilizer_codes": "2 (exact numerics of integer-valued I(R:A), distance distribution of random-Clifford-circuit codes)",
            "island_model1_AMM": "1 (reproduction of AMM 2019 eternal-BH island; formulas re-derived, extremum numerically)",
            "island_model2_evap_cartoon": "1 (textbook cartoon; t_P/t_evap closed form)",
            "shape_comparison": "2 (side-by-side comparison of separate models; no derivation claimed)"},
        "disclaimers": [
            "Finite-dimensional codes illustrate the QEC/entanglement-wedge language; they do not derive holography.",
            "Island results are semiclassical closed-form formulas under stated assumptions (eh/islands.py), not circuit simulations.",
            "No claim that any circuit simulation proves the island formula or resolves the information paradox."],
        "seeds": {"base": BASE_SEED, "scheme": "SeedSequence([base, family_id(513=0,stab=1,haar=2), n, seed])",
                  "n_seeds": seeds, "petz_subsets_per_e": MAX_PETZ_PER_E},
        "knill_laflamme_513": {"max_dev_single_erasure": kl[1], "max_dev_two_erasures": kl[2],
                               "min_dev_over_three_erasure_sets": kl3},
        "qec": agg,
        "islands": isl_out,
        "runtime_s": time.time() - t0,
        "env": {"numpy": np.__version__, "dtype": "complex128", "device": "cpu (local)",
                "time_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())},
    }
    with open(os.path.join(RESULTS, "h_qec_islands.json"), "w") as f:
        json.dump(res, f, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    make_figures(agg, isl_out)
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "rows"} for k, v in agg.items()}, indent=1))
    print(json.dumps(res["knill_laflamme_513"]), json.dumps(isl_out["model1_base"]), json.dumps(isl_out["model2_evap"]))
    print("runtime", time.time() - t0)


if __name__ == "__main__":
    main()
