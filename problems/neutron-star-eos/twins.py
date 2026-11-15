"""Twin-star analysis + figures + results/phase_transitions.json, from the cache of phase_sweep.py.
Equal-mass twin pairs (hadronic/connected branch vs disconnected third family): Delta R, Delta Lambda
(Love-number jump condition at the density discontinuity, sf/tov.py jump_dy), Lambda without the jump,
robustness to +-2% perturbations of (p_t, d_eps, c_s^2_q). Units: MeV/fm^3, M_sun, km.
Usage: .venv/bin/python twins.py"""
import json, math, os, time
from multiprocessing import Pool
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sf import tov as T, units as u
from sf.fastcss import FastCSS
import phase_sweep as S

HERE = os.path.dirname(os.path.abspath(__file__))
BG, FG, A1, A2 = "#0B0D10", "#E7E9EC", "#4FD1E0", "#E2B25C"
MEV = S.MEV
plt.rcParams.update({"figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG, "text.color": FG,
                     "axes.labelcolor": FG, "axes.edgecolor": FG, "xtick.color": FG, "ytick.color": FG,
                     "legend.facecolor": BG, "legend.edgecolor": "#3a3f46", "font.size": 10})


def sequence(pt, de, cq):
    h = S.had()
    eos = FastCSS(h, pt, de, cq)
    pmax = max(12 * pt, 2500 * MEV)
    pcs = [pt * (1 - 1e-4), pt] + [pt * (1 + x) for x in S.XS] + list(np.geomspace(pt * 1.03, pmax, 24))
    st = [T.solve_star(eos, float(p), tidal=False, rtol=S.RTOL) for p in pcs]
    M = np.array([s["M"] for s in st]); R = np.array([s["R"] for s in st]); pc = np.array(pcs)
    ks = S.btm_modes(R, M); segs = S.segments(ks)
    first = [s for s in segs if s[0] <= 1 <= s[1]]
    a_end = first[0][1] if first else 1
    later = [s for s in segs if s[0] > a_end and (M[s[1]] - M[s[0]]) > 1e-4]
    return eos, pc, M, R, a_end, later


def bracket(pc, M, i0, i1, Mt):
    for i in range(i0, i1):
        if (M[i] - Mt) * (M[i + 1] - Mt) <= 0:
            return pc[i], pc[i + 1]
    return None


def pair_at_mass(eos, pc, M, a_end, later, Mt, hseq):
    """Equal-mass pair: branch A (hadronic + connected), branch B (first disconnected stable segment)."""
    if not later:
        return None
    hpc, hM = np.array(hseq["pc"]), np.array(hseq["M"])
    m = hpc < pc[0]
    pcA = np.concatenate([hpc[m], pc[:a_end + 1]]); MA = np.concatenate([hM[m], M[:a_end + 1]])
    bA = bracket(pcA, MA, 0, len(pcA) - 1, Mt)
    a, b = later[0]
    bB = bracket(pc, M, a, b, Mt)
    if bA is None or bB is None:
        return None
    out = {}
    for lab, br in (("A", bA), ("B", bB)):
        s = T.star_of_mass(eos, Mt, br[0], br[1], rtol=1e-9)
        out[lab] = {k: s[k] for k in ("M", "R", "Lambda", "k2", "pc", "y_R")}
        out[lab]["pc_mev"] = s["pc"] / MEV
        out[lab]["has_quark_core"] = s["pc"] > eos.p_t
        out[lab]["r_core_km"] = s["r_transition"]
    # Lambda with the jump condition switched off (diagnostic only; physically wrong)
    jd = T.jump_dy
    T.jump_dy = lambda *args: 0.0
    try:
        sB = T.solve_star(eos, out["B"]["pc"], rtol=1e-9)
        out["B"]["Lambda_no_jump"] = sB["Lambda"]
    finally:
        T.jump_dy = jd
    out["dR_km"] = out["A"]["R"] - out["B"]["R"]
    out["dLambda"] = out["A"]["Lambda"] - out["B"]["Lambda"]
    out["Lambda_ratio_A_over_B"] = out["A"]["Lambda"] / out["B"]["Lambda"]
    return out


def twin_task(args):
    tag, pt, de, cq, Mt, hseq = args
    t0 = time.time()
    eos, pc, M, R, a_end, later = sequence(pt, de, cq)
    pr = pair_at_mass(eos, pc, M, a_end, later, Mt, hseq)
    return dict(tag=tag, p_t_mev=pt / MEV, delta_eps_mev=de / MEV, cs2_q=cq, M_target=Mt, pair=pr,
                has_third_family=bool(later), M_t=float(M[1]),
                M_max_third=float(max(M[b] for a, b in later)) if later else None, seconds=time.time() - t0)


def lambda_curve(args):
    tag, pt, de, cq, hseq = args
    eos, pc, M, R, a_end, later = sequence(pt, de, cq)
    hpc, hM = np.array(hseq["pc"]), np.array(hseq["M"])
    pcsA = [p for p, mm in zip(hpc, hM) if p < pt and mm > 0.3 * M[1]] or [0.3 * pt]
    pcsA = list(np.geomspace(pcsA[0], pc[a_end], 9))
    a, b = later[0]
    pcsB = list(np.geomspace(pc[a], pc[b], 10))
    ca = [T.solve_star(eos, float(p), rtol=1e-9) for p in pcsA]
    cb = [T.solve_star(eos, float(p), rtol=1e-9) for p in pcsB]
    f = lambda L: dict(M=[s["M"] for s in L], R=[s["R"] for s in L], Lambda=[s["Lambda"] for s in L])
    return dict(tag=tag, A=f(ca), B=f(cb), seq=dict(M=M.tolist(), R=R.tolist(), a_end=a_end, later=later))


def main():
    t0 = time.time()
    G = json.load(open(os.path.join(HERE, "results/phase_grid.json")))
    cases, hseq = G["cases"], G["hadronic_sequence"]
    # ---- topology statistics + Seidov comparison
    agree = [c for c in cases if c["connected"] != c["seidov_predicts_unstable"]]
    disagree = [dict(rp=c["rp"], rd=c["rd"], cs2_q=c["cs2_q"], topology=c["topology"],
                     seidov_bound=0.5 + 1.5 * c["rp"]) for c in cases if c["connected"] == c["seidov_predicts_unstable"]]
    sr = np.array([[c["slope_ratio_num"], c["slope_ratio_pred"]] for c in cases])
    err = np.abs(sr[:, 0] - sr[:, 1])
    counts = {}
    for c in cases:
        key = f"cs2={c['cs2_q']:.3f}"
        counts.setdefault(key, {"C": 0, "D": 0, "B": 0, "N": 0})[c["topology"]] += 1
    twin_cases = [c for c in cases if c["twins"]]
    # ---- representative twins: widest mass overlap per cs2
    reps = {}
    for cq in S.CQ:
        tc = [c for c in twin_cases if abs(c["cs2_q"] - cq) < 1e-9]
        if tc:
            heavy = [c for c in tc if c["twins"][0]["M_hi"] >= 1.0] or tc   # prefer astrophysical masses
            reps[cq] = max(heavy, key=lambda c: c["twins"][0]["M_hi"] - c["twins"][0]["M_lo"])
    tasks, ltasks = [], []
    for cq, c in reps.items():
        pt, de = c["p_t_mev"] * MEV, c["delta_eps_mev"] * MEV
        tw = c["twins"][0]
        Mt = 0.5 * (tw["M_lo"] + tw["M_hi"])
        tag = f"cs2={cq:.3f}"
        tasks.append((tag + ":nominal", pt, de, cq, Mt, hseq))
        for nm, f in (("p_t+2%", (1.02, 1, 1)), ("d_eps+2%", (1, 1.02, 1)), ("cs2-2%", (1, 1, 0.98))):
            tasks.append((tag + ":" + nm, pt * f[0], de * f[1], cq * f[2], Mt, hseq))
        ltasks.append((tag, pt, de, cq, hseq))
    with Pool(6) as pool:
        lres = pool.map_async(lambda_curve, ltasks)
        tres = pool.map(twin_task, tasks)
        lres = lres.get()
    # ---- figures
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.6), sharey=True)
    cmap = {"C": A1, "D": A2, "B": "#9F7AEA", "N": "#4a5059"}
    for ax, cq in zip(axs, S.CQ):
        cc = [c for c in cases if abs(c["cs2_q"] - cq) < 1e-9]
        for t in "CDBN":
            pts = [(c["rp"], c["rd"]) for c in cc if c["topology"] == t]
            if pts:
                x, y = zip(*pts)
                ax.scatter(x, y, s=150, marker="s", color=cmap[t], label={"C": "C: connected", "D": "D: disconnected",
                           "B": "B: both", "N": "N: absent"}[t], edgecolors="none")
        tw = [(c["rp"], c["rd"]) for c in cc if c["twins"]]
        if tw:
            x, y = zip(*tw)
            ax.scatter(x, y, s=22, marker="x", color=BG, label="twin pair found", linewidths=1.4)
        xx = np.linspace(0, 0.45, 50)
        ax.plot(xx, 0.5 + 1.5 * xx, color=FG, lw=1.4, ls="--", label=r"Seidov: $\Delta\varepsilon/\varepsilon_t=1/2+3p_t/2\varepsilon_t$")
        ax.set_xlim(0.01, 0.43); ax.set_ylim(0.0, 1.8)
        ax.set_xlabel(r"$p_t/\varepsilon_t$  (dimensionless; $p_t$, $\varepsilon_t$ in MeV fm$^{-3}$)")
        ax.set_title(f"SLy + CSS, $c_s^2$(quark) = {cq:.3g} (units of $c^2$)", color=FG, fontsize=10)
    axs[0].set_ylabel(r"$\Delta\varepsilon/\varepsilon_t$  (dimensionless)")
    axs[1].legend(loc="upper left", fontsize=7.5)
    fig.suptitle("Hybrid-branch topology (Alford-Han-Prakash categories), Maxwell transition", color=FG)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "figures/phase_diagram.png"), dpi=160); plt.close(fig)

    nominal = {r["tag"].split(":")[0]: r for r in tres if r["tag"].endswith("nominal")}
    hM, hR = np.array(hseq["M"]), np.array(hseq["R"])
    fig, axs = plt.subplots(1, len(lres), figsize=(5.4 * len(lres), 4.6))
    axs = np.atleast_1d(axs)
    for ax, L in zip(axs, lres):
        ax.plot(hR, hM, color="#6b7280", lw=1.0, label="SLy (hadronic only)")
        sq = L["seq"]; R_, M_ = np.array(sq["R"]), np.array(sq["M"])
        ax.plot(R_, M_, color=FG, lw=0.8, ls=":", label="hybrid sequence (incl. unstable)")
        ax.plot(L["A"]["R"], L["A"]["M"], color=A1, lw=2, label="stable: hadronic branch")
        ax.plot(L["B"]["R"], L["B"]["M"], color=A2, lw=2, label="stable: third family (quark core)")
        pr = nominal[L["tag"]]["pair"]
        if pr:
            ax.plot([pr["A"]["R"], pr["B"]["R"]], [pr["A"]["M"]] * 2, "o-", color="#FC8181", ms=5,
                    label=f"twins at M={pr['A']['M']:.3f}: dR={pr['dR_km']:.2f} km")
        c = nominal[L["tag"]]
        ax.set_title(f"{L['tag']}: $p_t$={c['p_t_mev']:.1f}, $\\Delta\\varepsilon$={c['delta_eps_mev']:.1f} MeV fm$^{{-3}}$", fontsize=9.5)
        ax.set_xlabel("R  (km)"); ax.set_ylabel(r"M  ($M_\odot$)"); ax.set_xlim(8, 16); ax.set_ylim(0.3, 2.2)
        ax.legend(fontsize=7, loc="upper right")
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "figures/twin_mr.png"), dpi=160); plt.close(fig)

    fig, axs = plt.subplots(1, len(lres), figsize=(5.4 * len(lres), 4.6))
    axs = np.atleast_1d(axs)
    for ax, L in zip(axs, lres):
        ax.semilogy(L["A"]["M"], L["A"]["Lambda"], color=A1, lw=2, label="hadronic branch")
        ax.semilogy(L["B"]["M"], L["B"]["Lambda"], color=A2, lw=2, label="third family (with jump condition)")
        pr = nominal[L["tag"]]["pair"]
        if pr:
            ax.semilogy([pr["A"]["M"]] * 2, [pr["A"]["Lambda"], pr["B"]["Lambda"]], "o-", color="#FC8181", ms=5,
                        label=f"equal-mass twins: $\\Lambda_A/\\Lambda_B$={pr['Lambda_ratio_A_over_B']:.2f}")
            ax.semilogy([pr["B"]["M"]], [pr["B"]["Lambda_no_jump"]], "^", color=FG, ms=6,
                        label="third-family star, jump condition omitted (wrong)")
        ax.set_xlabel(r"M  ($M_\odot$)"); ax.set_ylabel(r"$\Lambda = (2/3) k_2 (R/M)^5$  (dimensionless)")
        ax.set_title(L["tag"], fontsize=10); ax.legend(fontsize=7.5)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "figures/twin_lambda.png"), dpi=160); plt.close(fig)

    slim = [{k: c[k] for k in ("rp", "rd", "cs2_q", "p_t_mev", "eps_t_mev", "n_t_fm3", "delta_eps_mev", "M_t", "R_t",
                               "topology", "seidov_predicts_unstable", "slope_ratio_num", "slope_ratio_pred",
                               "M_max_third", "twins")} for c in cases]
    out = dict(meta=G["meta"], topology_counts=counts,
               seidov=dict(n_cases=len(cases), n_agree=len(agree), disagreements=disagree,
                           slope_ratio_abs_err_max=float(err.max()), slope_ratio_abs_err_median=float(np.median(err))),
               twin_cases=len(twin_cases), twin_runs=tres, lambda_curves=lres, cases=slim, wall_s=time.time() - t0)
    json.dump(out, open(os.path.join(HERE, "results/phase_transitions.json"), "w"), indent=1, default=float)
    print(json.dumps(dict(counts=counts, seidov=out["seidov"] | {"disagreements": disagree[:8]}, twin_cases=len(twin_cases)), indent=1))
    for r in tres:
        p = r["pair"]
        print(r["tag"], round(r["p_t_mev"], 2), round(r["delta_eps_mev"], 2), "Mt", round(r["M_target"], 4),
              "third", r["has_third_family"], "Mmax3", r["M_max_third"],
              None if not p else dict(RA=p["A"]["R"], RB=p["B"]["R"], dR=p["dR_km"], LA=p["A"]["Lambda"],
                                      LB=p["B"]["Lambda"], LBnj=p["B"]["Lambda_no_jump"], rcore=p["B"]["r_core_km"]))
    print("wall", time.time() - t0)


if __name__ == "__main__":
    main()
