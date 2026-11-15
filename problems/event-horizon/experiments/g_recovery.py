"""Tracks C + D: explicit Hayden-Preskill recovery, imperfect scrambling, noise, OTOCs.

Run (local CPU, small exact computations, numpy only):
  python experiments/g_recovery.py g1      # Haar: old vs young, finite size
  python experiments/g_recovery.py g2      # brickwork / Clifford scramblers x depolarizing noise
  python experiments/g_recovery.py g3      # OTOCs vs depth and their link to recovery
  python experiments/g_recovery.py plot    # merge -> results/g_recovery.json + figures g1-g3

Decoder: Petz recovery map (transpose channel) with sigma = 1/d_M, entanglement
fidelity computed exactly (eh/recovery.py). Yoshida-Kitaev P_EPR/F_EPR from
eh/hayden_preskill.py are reported alongside for the old hole.
Hypotheses (stated before the full runs; a single-instance smoke test of the
noisy Petz fidelity at p = 0.1 had been run while writing the code):
  H-G1 (light cone, expected theorem): for brickwork depth t < n - m the message
       cannot reach D, so F_Petz = 1/d_M^2 = 0.25 exactly (k = 1).
  H-G2 (noise robustness): depolarizing noise on the new radiation D shifts the
       0.9-threshold m*_0.9 by LESS for the old hole than for the young hole.
  H-G3 (2-design): deep Clifford brickwork matches the Haar mean of the purity
       tr rho_QB'^2 (a second-moment quantity) within 3 standard errors, while
       its Petz fidelity distribution is discrete (stabilizer states).
  H-G4 (OTOC vs recovery): the depth at which the mean OTOC between the message
       qubit and the farthest D qubit drops below 0.1 equals, within +-1 layer,
       the depth at which mean F_Petz(m=3) reaches 90% of its Haar value.
"""
import json
import os
import sys
import time

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np  # noqa: E402

from eh import recovery as rc  # noqa: E402
from eh import otoc as ot  # noqa: E402
from eh import hayden_preskill as hp  # noqa: E402
from eh.circuits import haar_unitary, brickwork_unitary  # noqa: E402

PARTS = os.path.join(ROOT, "results", "g_recovery_parts")
os.makedirs(PARTS, exist_ok=True)
SEED = 20261115


def log(*a):
    print(time.strftime("[%H:%M:%S]"), *a, flush=True)


def stats(x):
    x = np.asarray(x, float)
    return {"mean": float(x.mean()), "sem": float(x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 1 else 0.0,
            "min": float(x.min()), "max": float(x.max()), "n": int(len(x))}


def threshold(ms, F, level=0.9):
    """Smallest m (linear interpolation) at which F(m) >= level."""
    for i in range(1, len(ms)):
        if F[i - 1] < level <= F[i]:
            return float(ms[i - 1] + (level - F[i - 1]) / (F[i] - F[i - 1]))
    return float(ms[0]) if F[0] >= level else None


def make_U(n, scr, rng):
    if scr == "haar":
        return haar_unitary(2 ** n, rng)
    gate, depth = scr.split(":")
    return brickwork_unitary(n, int(depth), rng, gate=gate)


def dump(name, obj):
    p = os.path.join(PARTS, name)
    with open(p, "w") as f:
        json.dump(obj, f, indent=1)
    log("wrote", p)


# ----------------------------------------------------------------------------
def part_g1():
    """Haar scrambler: old vs young, k = 1 (n_B = 3..7) and k = 2 (n_B = 5)."""
    configs = [(1, nb) for nb in (3, 4, 5, 6, 7)] + [(2, 5)]
    out = {"seed_base": SEED + 1000, "configs": []}
    for ci, (k, nB) in enumerate(configs):
        n = k + nB
        S = 24 if n <= 7 else 12
        log(f"g1 k={k} n_B={nB}: max dim rho_QB' = {2 ** (k + n)}, seeds {S}")
        for old in (True, False):
            rows = {m: [] for m in range(n + 1)}
            seeds = [SEED + 1000 + 100 * ci + s for s in range(S)]
            for sd in seeds:
                U = haar_unitary(2 ** n, np.random.default_rng(sd))
                for m in range(n + 1):
                    rows[m].append(rc.recovery_metrics(U, k, nB, m, old=old, with_yk=old))
            res = {"k": k, "n_B": nB, "old": old, "seeds": seeds, "m": list(range(n + 1)), "metrics": {}}
            for key in rows[0][0]:
                res["metrics"][key] = [stats([r[key] for r in rows[m]]) for m in range(n + 1)]
            res["bounds"] = [rc.haar_bounds(k, nB, m, old) for m in range(n + 1)]
            res["haar_purity_exact"] = [(hp.haar_mean_purity_RBp_old if old else hp.haar_mean_purity_RBp_young)(k, nB, m)
                                        for m in range(n + 1)]
            Fm = [s["mean"] for s in res["metrics"]["F_petz"]]
            res["m_star_0.9"] = threshold(res["m"], Fm, 0.9)
            res["m_star_0.99"] = threshold(res["m"], Fm, 0.99)
            out["configs"].append(res)
            log(f"  old={old} m*0.9={res['m_star_0.9']} F={np.round(Fm, 3).tolist()}")
    dump("g1.json", out)


# ----------------------------------------------------------------------------
SCRAMBLERS_G2 = ["haar", "haar:1", "haar:2", "haar:3", "haar:4", "haar:6", "haar:10",
                 "clifford:2", "clifford:4", "clifford:10", "clifford:30"]


SCRAMBLERS_G2_N4 = ["haar", "haar:1", "haar:2", "haar:3", "haar:4", "haar:8",
                    "clifford:2", "clifford:4", "clifford:8", "clifford:24"]


def part_g2(which, nB=4, scr_list=None, outname=None):
    """k = 1, n = 1 + n_B. which = 'D' (noise on new radiation, all scramblers)
    or 'DR' (noise on all radiation Bob holds)."""
    k = 1
    n = k + nB
    ps = [0.0, 0.03, 0.1, 0.3]
    S = 10
    if scr_list is None:
        scr_list = SCRAMBLERS_G2 if which == "D" else ["haar", "haar:10", "clifford:30"]
    log(f"g2[{which}] n={n}: max dim rho_QX = {2 ** (k + n + nB)} (old), seeds {S}")
    out = {"k": k, "n_B": nB, "ps": ps, "noise_on": which, "results": []}
    for si, scr in enumerate(scr_list):
        seeds = [SEED + 2000 + 100 * si + s for s in range(S)]
        for old in (True, False):
            F = np.zeros((len(ps), n + 1, S))
            pur = np.zeros((n + 1, S))
            for j, sd in enumerate(seeds):
                U = make_U(n, scr, np.random.default_rng(sd))
                for m in range(n + 1):
                    Psi = rc.hp_tensor(U, k, nB, m, old)
                    F[0, m, j] = rc.petz_fidelity_pure(Psi)
                    pur[m, j] = rc.decoupling(Psi)["purity_QBp"]
                    for ip, p in enumerate(ps[1:], 1):
                        if which == "DR" and not old:
                            F[ip, m, j] = np.nan  # young hole has no early radiation; DR == D
                            continue
                        F[ip, m, j] = rc.noisy_petz_fidelity(U, k, nB, m, p, old=old, noise_on=which)
            res = {"scrambler": scr, "old": old, "seeds": seeds,
                   "F_petz": [[stats(F[ip, m]) if not np.isnan(F[ip, m]).any() else None for m in range(n + 1)]
                              for ip in range(len(ps))],
                   "F_petz_values_p0": F[0].tolist(),
                   "purity": [stats(pur[m]) for m in range(n + 1)],
                   "haar_purity_exact": [(hp.haar_mean_purity_RBp_old if old else hp.haar_mean_purity_RBp_young)(k, nB, m)
                                         for m in range(n + 1)]}
            res["m_star_0.9"] = [threshold(list(range(n + 1)), [F[ip, m].mean() for m in range(n + 1)], 0.9)
                                 if not np.isnan(F[ip]).any() else None for ip in range(len(ps))]
            out["results"].append(res)
            log(f"  {scr} old={old} m*0.9 vs p: {res['m_star_0.9']}")
    out["scramblers"] = scr_list
    dump(outname or f"g2_{which}.json", out)


# ----------------------------------------------------------------------------
def part_g3(fast=False):
    """(a) OTOC vs depth on N = 9 (fast: 8) qubits, Haar and Clifford brickwork.
    (b) N = 7 (k = 1, n_B = 6) old hole: recovery vs depth together with OTOCs."""
    out = {}
    N, T, S = (8, 14, 10) if fast else (9, 16, 12)
    sites = [1, 4, N - 1]
    pairs = []
    for j in sites:
        for w in "XYZ":
            for v in "XYZ":
                pairs.append(({j: w}, {0: v}))
    out["a"] = {"N": N, "depths": list(range(T + 1)), "V_site": 0, "W_sites": sites,
                "haar_value": ot.haar_otoc(N), "convention": ot.__doc__.split("\n\n")[1], "gates": {}}
    for gi, gate in enumerate(("haar", "clifford")):
        seeds = [SEED + 3000 + 100 * gi + s for s in range(S)]
        if fast:
            wl = [{j: w} for j in sites for w in "XYZ"]
            vl = [{0: v} for v in "XYZ"]
            vals = np.stack([ot.otoc_vs_depth_fast(N, T, np.random.default_rng(sd), gate, wl, vl) for sd in seeds])
            vals = vals.reshape(S, T + 1, len(sites), 3, 3).mean(axis=(3, 4))
        else:
            vals = np.stack([ot.otoc_vs_depth(N, T, np.random.default_rng(sd), gate, pairs) for sd in seeds])
            vals = vals.reshape(S, T + 1, len(sites), 9).mean(axis=3)  # average the 9 Pauli pairs
        out["a"]["gates"][gate] = {"seeds": seeds,
                                   "otoc": {str(j): [stats(vals[:, t, i]) for t in range(T + 1)]
                                            for i, j in enumerate(sites)}}
        log(f"g3a {gate} done")
    # (b)
    k, nB = 1, 6
    n = k + nB
    depths = list(range(0, 13))
    S = 16
    ms = [1, 2, 3, 4]
    out["b"] = {"k": k, "n_B": nB, "n": n, "depths": depths, "m": ms, "gates": {}}
    for gi, gate in enumerate(("haar", "clifford")):
        seeds = [SEED + 4000 + 100 * gi + s for s in range(S)]
        rec = {m: np.zeros((len(depths), S, 3)) for m in ms}
        oto = np.zeros((len(depths), S))
        pairs7 = [({n - 1: w}, {0: v}) for w in "XYZ" for v in "XYZ"]
        for j, sd in enumerate(seeds):
            rng = np.random.default_rng(sd)
            o = ot.otoc_vs_depth(n, max(depths), np.random.default_rng(sd), gate, pairs7).mean(axis=1)
            oto[:, j] = o
            for di, dep in enumerate(depths):
                U = brickwork_unitary(n, dep, np.random.default_rng(sd), gate=gate) if dep > 0 else np.eye(2 ** n, dtype=complex)
                for m in ms:
                    r = rc.recovery_metrics(U, k, nB, m, old=True, with_yk=True)
                    rec[m][di, j] = (r["F_petz"], r["P_EPR"], r["F_EPR"])
            del rng
        haar_ref = {}
        for m in ms:
            hr = [rc.recovery_metrics(haar_unitary(2 ** n, np.random.default_rng(SEED + 4500 + s)), k, nB, m)["F_petz"]
                  for s in range(S)]
            haar_ref[str(m)] = stats(hr)
        g = {"seeds": seeds, "otoc_q0_qlast": [stats(oto[d]) for d in range(len(depths))],
             "F_petz": {str(m): [stats(rec[m][d, :, 0]) for d in range(len(depths))] for m in ms},
             "P_EPR": {str(m): [stats(rec[m][d, :, 1]) for d in range(len(depths))] for m in ms},
             "F_EPR": {str(m): [stats(rec[m][d, :, 2]) for d in range(len(depths))] for m in ms},
             "haar_F_petz": haar_ref, "haar_seeds": [SEED + 4500 + s for s in range(S)]}
        Fm = [s["mean"] for s in g["F_petz"]["3"]]
        target = 0.9 * haar_ref["3"]["mean"]
        g["d_rec"] = next((d for d, f in zip(depths, Fm) if f >= target), None)
        om = [s["mean"] for s in g["otoc_q0_qlast"]]
        g["d_otoc"] = next((d for d, f in zip(depths, om) if f < 0.1), None)
        out["b"]["gates"][gate] = g
        log(f"g3b {gate}: d_rec={g['d_rec']} d_otoc={g['d_otoc']}")
    dump("g3_fast.json" if fast else "g3.json", out)


# ----------------------------------------------------------------------------
def part_plot():
    sys.path.insert(0, os.path.dirname(__file__))
    import _style as st
    plt = st.setup()
    g1 = json.load(open(os.path.join(PARTS, "g1.json")))
    big = all(os.path.exists(os.path.join(PARTS, f)) for f in ("g2_D.json", "g2_DR.json"))
    g2 = json.load(open(os.path.join(PARTS, "g2_D.json" if big else "g2_D_n4.json")))
    g2r = json.load(open(os.path.join(PARTS, "g2_DR.json" if big else "g2_DR_n4.json")))
    if "scramblers" not in g2:
        g2["scramblers"] = SCRAMBLERS_G2
    small = {f: json.load(open(os.path.join(PARTS, f))) for f in ("g2_D_n4.json", "g2_DR_n4.json")}
    g3 = json.load(open(os.path.join(PARTS, "g3_fast.json")))
    extra = {f: json.load(open(os.path.join(PARTS, f))) for f in ("g2_D.json", "g2_DR.json", "g3.json")
             if os.path.exists(os.path.join(PARTS, f))}
    FIG = os.path.join(ROOT, "figures")

    # ---------------- g1
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))
    cols = {3: st.CYAN, 4: st.AMBER, 5: st.MAGENTA, 6: st.GREEN, 7: "#B8A1FF"}
    for c in g1["configs"]:
        if c["k"] != 1:
            continue
        ms = np.array(c["m"])
        F = np.array([s["mean"] for s in c["metrics"]["F_petz"]])
        e = np.array([s["sem"] for s in c["metrics"]["F_petz"]])
        ls = "-" if c["old"] else "--"
        ax[0].errorbar(ms - c["k"], F, yerr=e, ls=ls, marker="o", ms=3, color=cols[c["n_B"]],
                       label=f"n_B={c['n_B']} {'old' if c['old'] else 'young'}")
        if c["old"]:
            Fyk = [s["mean"] for s in c["metrics"]["F_EPR"]]
            ax[0].plot(ms - c["k"], Fyk, ":", color=cols[c["n_B"]], lw=1)
        T = np.array([s["mean"] for s in c["metrics"]["T_mm"]])
        Tb = np.array([b["T_mm_bound"] for b in c["bounds"]])
        ax[1].semilogy(ms - c["k"], np.clip(T, 1e-6, None), ls=ls, marker="o", ms=3, color=cols[c["n_B"]])
        ax[1].semilogy(ms - c["k"], np.clip(Tb, 1e-6, None), ls=ls, lw=0.8, color=cols[c["n_B"]], alpha=0.5)
    mm = np.linspace(-1, 8, 50)
    ax[1].semilogy(mm, 0.5 * 2.0 ** (-mm), color=st.GREY, lw=1, label="old, large-d bound  2^(k-m)/2")
    ax[0].axhline(0.25, color=st.GREY, lw=0.8)
    ax[0].set_xlabel("m - k  (new-radiation qubits beyond message size)")
    ax[0].set_ylabel("Petz entanglement fidelity F_Petz (solid/dashed); F_EPR(YK) dotted")
    ax[0].set_title("Message recovery from R+D (Haar, k = 1)")
    ax[0].legend(ncol=2, fontsize=6.5)
    ax[1].set_xlabel("m - k")
    ax[1].set_ylabel("T_mm = 1/2 ||rho_QB' - 1/(d_Q d_B')||_1")
    ax[1].set_title("Decoupling: markers = measured mean, thin = exact-Haar bound")
    ax[1].set_ylim(1e-4, 1.2)
    ax[1].legend(fontsize=7)
    # finite size: F_Petz at m - k = 1, 2 vs n_B, old
    for off, colr in ((1, st.CYAN), (2, st.AMBER), (3, st.MAGENTA)):
        xs, ys, es = [], [], []
        for c in g1["configs"]:
            if c["k"] == 1 and c["old"]:
                s = c["metrics"]["F_petz"][c["k"] + off]
                xs.append(c["n_B"]); ys.append(1 - s["mean"]); es.append(s["sem"])
        ax[2].errorbar(xs, ys, yerr=es, marker="o", color=colr, label=f"old, m - k = {off}")
        pr = [c["bounds"][c["k"] + off]["T_mm_bound"] ** 2 for c in g1["configs"] if c["k"] == 1 and c["old"]]
        ax[2].plot(xs, pr, ":", color=colr, lw=1.2, label="(D E[tr rho^2] - 1)/4 (Bures 2nd order)" if off == 1 else None)
    ax[2].set_yscale("log")
    ax[2].set_xlabel("black-hole qubits n_B")
    ax[2].set_ylabel("1 - F_Petz (finite-size infidelity)")
    ax[2].set_title("Finite-size corrections at fixed m - k (old hole)")
    ax[2].legend(fontsize=6.5)
    st.caption(fig, "Exact dense simulation, Haar U on M+B, Petz (transpose-channel) decoder with sigma = 1/d_M; "
                    "mean +- s.e.m. over 24 (12 for n = 8) seeds. Finite-dimensional circuit model, no gravity.")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(os.path.join(FIG, "g1_recovery_fidelity.png"), dpi=150)
    plt.close(fig)

    # ---------------- g2
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))
    n = g2["k"] + g2["n_B"]
    ms = np.arange(n + 1)
    cmap = {"haar:8": st.MAGENTA, "clifford:8": "#B8A1FF", "clifford:24": "#d9c8ff", "haar": st.FG, "haar:1": "#9AD1FF", "haar:2": st.CYAN, "haar:3": st.GREEN, "haar:4": st.AMBER,
            "haar:6": "#FF8A5C", "haar:10": st.MAGENTA, "clifford:2": "#555c66", "clifford:4": st.GREY,
            "clifford:10": "#B8A1FF", "clifford:30": "#d9c8ff"}
    for r in g2["results"]:
        if not r["old"]:
            continue
        F = [s["mean"] for s in r["F_petz"][0]]
        ax[0].plot(ms, F, marker="o", ms=3, color=cmap[r["scrambler"]],
                   ls="-" if not r["scrambler"].startswith("clifford") else "--", label=r["scrambler"])
    ax[0].axhline(0.25, color=st.GREY, lw=0.8)
    ax[0].set_xlabel("new-radiation qubits m")
    ax[0].set_ylabel("F_Petz (old hole, noiseless)")
    ax[0].set_title(f"Scrambler: brickwork depth / Clifford (n = {n}, k = 1)")
    ax[0].legend(fontsize=6.5, ncol=2)
    for r in g2["results"]:
        if r["scrambler"] != "haar":
            continue
        for ip, p in enumerate(g2["ps"]):
            F = [s["mean"] for s in r["F_petz"][ip]]
            ax[1].plot(ms, F, marker="o" if r["old"] else "s", ms=3, color=st.PALETTE[ip],
                       ls="-" if r["old"] else "--", label=f"p={p} {'old' if r['old'] else 'young'}")
    if g2r:
        for r in g2r["results"]:
            if r["scrambler"] == "haar" and r["old"]:
                for ip, p in enumerate(g2r["ps"][1:], 1):
                    F = [s["mean"] for s in r["F_petz"][ip]]
                    ax[1].plot(ms, F, ":", color=st.PALETTE[ip], lw=1.2, label=f"p={p} old, noise on R+D")
    ax[1].set_xlabel("new-radiation qubits m")
    ax[1].set_ylabel("F_Petz")
    ax[1].set_title("Depolarizing noise on radiation (Haar)")
    ax[1].legend(fontsize=6, ncol=2)
    labels = list(g2["scramblers"])
    for oi, old in enumerate((True, False)):
        for ip, p in enumerate(g2["ps"]):
            ys = []
            for s in labels:
                r = next(x for x in g2["results"] if x["scrambler"] == s and x["old"] == old)
                v = r["m_star_0.9"][ip]
                ys.append(np.nan if v is None else v)
            ax[2].plot(np.arange(len(labels)) + 0.08 * ip, ys, marker="o" if old else "s", ls="none",
                       color=st.PALETTE[ip], label=f"p={p} {'old' if old else 'young'}", alpha=1 if old else 0.6)
    ax[2].set_xticks(range(len(labels)))
    ax[2].set_xticklabels(labels, rotation=45, fontsize=7)
    ax[2].set_ylabel("threshold m* (mean F_Petz = 0.9)")
    ax[2].set_xlabel("scrambler (missing marker: never reaches 0.9)")
    ax[2].set_title("Threshold shift")
    yl = ax[2].get_ylim()
    ax[2].set_ylim(yl[0] - 0.1, yl[1] + 0.9)
    ax[2].legend(fontsize=6, ncol=4, loc="upper center")
    st.caption(fig, f"n = {n} (k = 1, n_B = {n - 1}) exact density-matrix simulation; single-qubit depolarizing x -> (1-p)x + p 1/2 on each "
                    "radiation qubit before Petz decoding; 10 seeds per point. Toy circuit model, not gravity.")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(os.path.join(FIG, "g2_noise_scrambling.png"), dpi=150)
    plt.close(fig)

    # ---------------- g3
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))
    a = g3["a"]
    for gi, gate in enumerate(("haar", "clifford")):
        for i, j in enumerate(a["W_sites"]):
            s = a["gates"][gate]["otoc"][str(j)]
            ax[0].errorbar(a["depths"], [x["mean"] for x in s], yerr=[x["sem"] for x in s],
                           color=st.PALETTE[i], ls="-" if gate == "haar" else "--", marker="o", ms=2.5,
                           label=f"{gate}, W on q{j}")
    ax[0].axhline(a["haar_value"], color=st.GREY, lw=0.8, label="Haar value -1/(d^2-1)")
    ax[0].set_xlabel("brickwork depth t")
    ax[0].set_ylabel("F(t) = 2^-N Tr[W(t) V W(t) V], V on q0 (Pauli-avg)")
    ax[0].set_title(f"Infinite-temperature OTOC, N = {a['N']}")
    ax[0].legend(fontsize=6.5)
    b = g3["b"]
    for gi, gate in enumerate(("haar", "clifford")):
        g = b["gates"][gate]
        for i, m in enumerate(b["m"]):
            s = g["F_petz"][str(m)]
            ax[1].plot(b["depths"], [x["mean"] for x in s], color=st.PALETTE[i], ls="-" if gate == "haar" else "--",
                       marker="o", ms=2.5, label=f"{gate}, m={m}")
            if gate == "haar":
                ax[1].axhline(g["haar_F_petz"][str(m)]["mean"], color=st.PALETTE[i], lw=0.6, alpha=0.5)
    ax[1].set_xlabel("brickwork depth t")
    ax[1].set_ylabel("F_Petz (old hole, n = 7, k = 1)")
    ax[1].set_title("Recovery onset vs depth (thin: Haar value)")
    ax[1].legend(fontsize=6.5, ncol=2)
    lp = os.path.join(PARTS, "g3_long.json")
    if os.path.exists(lp):
        L = json.load(open(lp))
        dd = L["depths"]
        ax[2].plot(dd, [x["mean"] for x in L["otoc_q0_farthestD"]], color=st.CYAN, marker="o", ms=3,
                   label="OTOC q0 vs farthest D qubit q6")
        ax[2].plot(dd, [x["mean"] for x in L["otoc_q0_nearestD"]], color="#9AD1FF", marker="o", ms=3, ls="--",
                   label="OTOC q0 vs nearest D qubit q4")
        ax[2].plot(dd, [(4 * x["mean"] - 1) / 3 for x in L["P_EPR"]], color=st.AMBER, marker="s", ms=3,
                   label="(d_M^2 P_EPR - 1)/(d_M^2 - 1): non-identity Pauli-avg OTOC(M, D), m=3")
        ax[2].plot(dd, [x["mean"] for x in L["F_petz"]], color=st.MAGENTA, marker="^", ms=3, label="F_Petz, m=3")
        ax[2].axhline(0.9 * L["haar_F_petz"]["mean"], color=st.MAGENTA, lw=0.6, alpha=0.6)
        ax[2].axhline(0.1, color=st.CYAN, lw=0.6, alpha=0.6)
        g3["long"] = L
    else:
        g = b["gates"]["haar"]
        ax[2].plot(b["depths"], [x["mean"] for x in g["otoc_q0_qlast"]], color=st.CYAN, marker="o", ms=3,
                   label="OTOC q0 vs q6 (9 Pauli pairs)")
        ax[2].plot(b["depths"], [(x["mean"] * 4 - 1) / 3 for x in g["P_EPR"]["3"]], color=st.AMBER, marker="s", ms=3,
                   label="(d_M^2 P_EPR - 1)/(d_M^2 - 1), m=3")
        ax[2].plot(b["depths"], [x["mean"] for x in g["F_petz"]["3"]], color=st.MAGENTA, marker="^", ms=3,
                   label="F_Petz, m=3")
    ax[2].set_xlabel("brickwork depth t (Haar gates)")
    ax[2].set_ylabel("value")
    ax[2].set_title("OTOC decay vs recovery onset (n = 7)")
    ax[2].legend(fontsize=6.5)
    st.caption(fig, "OTOC convention: beta = 0, W(t) = U_t^dag W U_t, Pauli W, V; mean +- s.e.m. over 12 (a) / 16 (b) circuits. "
                    "P_EPR = Pauli-averaged OTOC is the exact Yoshida-Kitaev identity (checked to 1e-12 in tests).")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(os.path.join(FIG, "g3_otoc.png"), dpi=150)
    plt.close(fig)

    merged = {"description": "Tracks C+D: explicit HP recovery (Petz decoder), scrambling quality, noise, OTOCs",
              "decoder": "Petz recovery map (transpose channel), sigma = 1/d_M; Yoshida-Kitaev P_EPR/F_EPR alongside",
              "g1": g1, "g2_noise_D": g2, "g2_noise_DR": g2r, "g3": g3,
              "g2_used_n": g2["k"] + g2["n_B"],
              "g2_clifford_purity": json.load(open(os.path.join(PARTS, "g2_clifford_purity.json")))
              if os.path.exists(os.path.join(PARTS, "g2_clifford_purity.json")) else None, "g2_n4_runs": small,
              "extra_larger_runs_if_finished": extra}
    with open(os.path.join(ROOT, "results", "g_recovery.json"), "w") as f:
        json.dump(merged, f, indent=1)
    log("wrote results/g_recovery.json and figures g1-g3")


def part_g3long():
    """H-G4 follow-up: n = 7 old hole, Haar brickwork, depths 0..24, m = 3."""
    k, nB, m = 1, 6, 3
    n = k + nB
    T, S = 24, 16
    seeds = [SEED + 4000 + s for s in range(S)]  # same circuits as g3b (haar) for depth <= 12
    wl = [{n - 1: w} for w in "XYZ"] + [{n - m: w} for w in "XYZ"]
    vl = [{0: v} for v in "XYZ"]
    F = np.zeros((T + 1, S)); P = np.zeros((T + 1, S)); O = np.zeros((T + 1, S, 2))
    for j, sd in enumerate(seeds):
        o = ot.otoc_vs_depth_fast(n, T, np.random.default_rng(sd), "haar", wl, vl)
        O[:, j, 0] = o[:, :3].mean(axis=(1, 2)); O[:, j, 1] = o[:, 3:].mean(axis=(1, 2))
        for dep in range(T + 1):
            U = brickwork_unitary(n, dep, np.random.default_rng(sd), gate="haar") if dep else np.eye(2 ** n, dtype=complex)
            r = rc.recovery_metrics(U, k, nB, m, old=True, with_yk=True)
            F[dep, j], P[dep, j] = r["F_petz"], r["P_EPR"]
    hr = stats([rc.recovery_metrics(haar_unitary(2 ** n, np.random.default_rng(SEED + 4500 + s)), k, nB, m)["F_petz"]
                for s in range(S)])
    out = {"k": k, "n_B": nB, "m": m, "depths": list(range(T + 1)), "seeds": seeds, "haar_F_petz": hr,
           "F_petz": [stats(F[d]) for d in range(T + 1)], "P_EPR": [stats(P[d]) for d in range(T + 1)],
           "otoc_q0_farthestD": [stats(O[d, :, 0]) for d in range(T + 1)],
           "otoc_q0_nearestD": [stats(O[d, :, 1]) for d in range(T + 1)]}
    Fm = F.mean(axis=1)
    out["d_rec"] = next((d for d in range(T + 1) if Fm[d] >= 0.9 * hr["mean"]), None)
    out["d_otoc_farthest"] = next((d for d in range(T + 1) if O[d, :, 0].mean() < 0.1), None)
    out["d_otoc_nearest"] = next((d for d in range(T + 1) if O[d, :, 1].mean() < 0.1), None)
    log("g3long", out["d_rec"], out["d_otoc_farthest"], out["d_otoc_nearest"])
    dump("g3_long.json", out)


def part_g2cliff():
    """H-G3 with adequate statistics: purity tr rho_QB'^2 for depth-30 Clifford
    brickwork (n = 5, k = 1) vs the exact Haar second-moment formula; 400 seeds."""
    k, nB, S = 1, 4, 400
    n = k + nB
    seeds = [SEED + 6000 + s for s in range(S)]
    pur = {True: np.zeros((n + 1, S)), False: np.zeros((n + 1, S))}
    Fp = {True: np.zeros((n + 1, S)), False: np.zeros((n + 1, S))}
    for j, sd in enumerate(seeds):
        U = brickwork_unitary(n, 30, np.random.default_rng(sd), gate="clifford")
        for old in (True, False):
            for m in range(n + 1):
                Psi = rc.hp_tensor(U, k, nB, m, old)
                pur[old][m, j] = rc.decoupling(Psi)["purity_QBp"]
                Fp[old][m, j] = rc.petz_fidelity_pure(Psi)
    out = {"k": k, "n_B": nB, "depth": 30, "seeds": seeds, "rows": []}
    for old in (True, False):
        f = hp.haar_mean_purity_RBp_old if old else hp.haar_mean_purity_RBp_young
        for m in range(n + 1):
            s_ = stats(pur[old][m])
            h = f(k, nB, m)
            z = (s_["mean"] - h) / s_["sem"] if s_["sem"] > 0 else (0.0 if abs(s_["mean"] - h) < 1e-12 else float("inf"))
            vals, cnts = np.unique(np.round(Fp[old][m], 6), return_counts=True)
            out["rows"].append({"old": old, "m": m, "purity": s_, "haar_exact": h, "z": z,
                                "F_petz": stats(Fp[old][m]),
                                "F_petz_values": vals.tolist(), "F_petz_counts": cnts.tolist()})
            log(f"cliff old={old} m={m} purity {s_['mean']:.4f}+-{s_['sem']:.4f} haar {h:.4f} z={z:.2f} F vals {vals.tolist()}")
    dump("g2_clifford_purity.json", out)


if __name__ == "__main__":
    cmd = sys.argv[1]
    t0 = time.time()
    {"g1": part_g1, "g2": lambda: part_g2("D"), "g2r": lambda: part_g2("DR"),
     "g3": part_g3, "plot": part_plot,
     "g2fast": lambda: (part_g2("D", 3, SCRAMBLERS_G2_N4, "g2_D_n4.json"),
                        part_g2("DR", 3, ["haar", "haar:8", "clifford:24"], "g2_DR_n4.json")),
     "g3fast": lambda: part_g3(True), "g3long": part_g3long, "g2cliff": part_g2cliff}[cmd]()
    log(f"{cmd} done in {time.time() - t0:.1f}s")
