"""Reference sweep: M-R, P-eps, c_s^2 for Read et al. 2009 PP EOSs (+ two illustrative models).
Writes figures/{mr,p_eps,cs2}_reference.png and results/core.json. Usage: .venv/bin/python sweep_reference.py"""
import json, os, time
from multiprocessing import Pool
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sf import eos as E, tov as T, units as u, models

HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = ["SLy", "APR4", "MPA1", "H4", "CS", "CSS"]
# Read et al. 2009 Table III values for the *tabulated* EOSs (literature comparison; recalled values,
# to be re-checked against the paper): M_max [M_sun], R_1.4 [km]
LIT = {"SLy": (2.049, 11.736), "APR4": (2.213, 11.428), "MPA1": (2.461, 12.475), "H4": (2.032, 13.774)}
BG, FG, A1, A2 = "#0B0D10", "#E7E9EC", "#4FD1E0", "#E2B25C"
COLORS = {"SLy": A1, "APR4": A2, "MPA1": "#9F7AEA", "H4": "#68D391", "CS": "#F687B3", "CSS": "#FC8181"}


def get(name):
    if name == "CS":
        return models.example_cs()
    if name == "CSS":
        return models.example_css()
    return E.reference_eos(name)


def run(name):
    t0 = time.time()
    e = get(name)
    kw = dict(rtol=1e-9, atol=1e-13)
    pcs = np.geomspace(u.mevfm3_to_geo(8.0), min(u.mevfm3_to_geo(3000.0), e.p_max * 0.99), 70)
    seq = T.mr_sequence(e, pcs, **kw)
    st = seq["stability"]
    i0, i1 = st["branches"][0]
    imax = st["maxima"][0] if st["maxima"] else int(np.argmax(seq["M"]))
    lo = max(imax - 1, 0)
    mm = T.max_mass(e, pcs[lo] if lo else pcs[0], pcs[min(imax + 1, len(pcs) - 1)], num=6, **kw)
    s14 = T.star_of_mass(e, 1.4, pcs[i0], mm["pc"], **kw) if seq["M"][i0] < 1.4 < mm["M"] else None
    chk = e.check(1e-14, mm["pc"])
    branches = [dict(M_range_Msun=[float(seq["M"][a]), float(seq["M"][b])],
                     R_range_km=[float(seq["R"][b]), float(seq["R"][a])]) for a, b in st["branches"]]
    res = dict(
        eos=e.name, novelty_level=1,
        novelty_note="reproduction of known EOS models with an independent solver",
        M_max_Msun=mm["M"], R_at_Mmax_km=mm["R"], pc_at_Mmax_MeV_fm3=float(u.geo_to_mevfm3(mm["pc"])),
        eps_c_at_Mmax_MeV_fm3=float(u.geo_to_mevfm3(mm["eps_c"])),
        R_1p4_km=s14["R"] if s14 else None, Lambda_1p4=s14["Lambda"] if s14 else None,
        k2_1p4=s14["k2"] if s14 else None,
        causal_up_to_Mmax=chk["causal"], cs2_max_up_to_Mmax=chk["cs2_max"],
        p_acausal_min_MeV_fm3=None if chk["p_acausal_min"] is None else float(u.geo_to_mevfm3(chk["p_acausal_min"])),
        n_stable_branches=len(st["branches"]), stable_branches=branches,
        literature_ReadEtAl2009_Mmax_R14=LIT.get(name), runtime_s=time.time() - t0,
        curves=dict(R_km=seq["R"].tolist(), M_Msun=seq["M"].tolist(), Lambda=seq["Lambda"].tolist(),
                    stable=st["stable"].tolist(), pc_MeV_fm3=u.geo_to_mevfm3(seq["pc"]).tolist()),
    )
    if name == "CSS":
        res["transition"] = dict(p_t_MeV_fm3=80.0, delta_eps_MeV_fm3=250.0, cs2_quark=1.0)
    return name, res


def style(ax):
    ax.set_facecolor(BG)
    for s in ax.spines.values():
        s.set_color(FG)
    ax.tick_params(colors=FG, which="both")
    ax.xaxis.label.set_color(FG); ax.yaxis.label.set_color(FG); ax.title.set_color(FG)
    ax.grid(alpha=0.15, color=FG)


def fig(ax_fn, fname, title):
    f, ax = plt.subplots(figsize=(7, 5), facecolor=BG)
    style(ax)
    ax_fn(ax)
    ax.set_title(title)
    leg = ax.legend(facecolor=BG, edgecolor=FG, fontsize=8)
    for t in leg.get_texts():
        t.set_color(FG)
    f.tight_layout()
    f.savefig(os.path.join(HERE, "figures", fname), dpi=160, facecolor=BG)
    plt.close(f)


def main():
    t0 = time.time()
    with Pool(min(6, len(NAMES))) as pool:
        out = dict(pool.map(run, NAMES))

    def mr(ax):
        ax.axhspan(2.08 - 0.07, 2.08 + 0.07, color=A2, alpha=0.12, label="PSR J0740+6620, 2.08±0.07 M$_\\odot$ (Fonseca+2021)")
        for n, r in out.items():
            c = r["curves"]; R, M, s = map(np.array, (c["R_km"], c["M_Msun"], c["stable"]))
            ax.plot(np.where(s, R, np.nan), np.where(s, M, np.nan), color=COLORS[n], lw=2, label=r["eos"])
            ax.plot(R, M, color=COLORS[n], lw=0.8, ls=":", alpha=0.7)
        ax.set_xlim(8, 16); ax.set_ylim(0, 2.8)
        ax.set_xlabel("Radius R [km]"); ax.set_ylabel("Gravitational mass M [M$_\\odot$]")

    def pe(ax):
        for n in NAMES:
            e = get(n)
            P = np.geomspace(u.mevfm3_to_geo(0.05), min(u.mevfm3_to_geo(2000.), e.p_max * 0.99), 600)
            ax.loglog(u.geo_to_mevfm3(e.eps(P)), u.geo_to_mevfm3(P), color=COLORS[n], lw=1.8, label=e.name)
        ax.set_xlabel("Energy density $\\epsilon$ [MeV fm$^{-3}$]"); ax.set_ylabel("Pressure P [MeV fm$^{-3}$]")

    def cs(ax):
        for n in NAMES:
            e = get(n)
            P = np.geomspace(u.mevfm3_to_geo(0.05), min(u.mevfm3_to_geo(2000.), e.p_max * 0.99), 1500)
            ax.plot(e.n(P) / u.N_SAT, e.cs2(P), color=COLORS[n], lw=1.6, label=e.name)
        ax.axhline(1.0, color=FG, ls="--", lw=0.8, label="causal limit $c_s^2=1$")
        ax.axhline(1 / 3, color=FG, ls=":", lw=0.8, label="conformal $c_s^2=1/3$")
        ax.set_xlim(0, 10); ax.set_ylim(0, 1.3)
        ax.set_xlabel("Baryon density n / n$_{sat}$ (n$_{sat}$ = 0.16 fm$^{-3}$) [dimensionless]")
        ax.set_ylabel("Squared sound speed $c_s^2$ [c$^2$]")

    fig(mr, "mr_reference.png", "Mass-radius (solid: stable, dotted: unstable)")
    fig(pe, "p_eps_reference.png", "Equation of state P($\\epsilon$)")
    fig(cs, "cs2_reference.png", "Speed of sound")
    meta = dict(units=dict(mass="M_sun", radius="km", pressure="MeV/fm^3", Lambda="dimensionless",
                           internal="G=c=1, km; 1 MeV/fm^3 = %.6e km^-2; M_sun = %.7f km" % (u.GEO_PER_MEVFM3, u.M_SUN_KM)),
                solver="sf.tov.solve_star DOP853 rtol=1e-9 atol=1e-13, surface at P=1e-16 km^-2",
                novelty="level 1 (reproduction); CS/CSS entries are illustrative parameter choices, not fits",
                wall_time_s=time.time() - t0)
    json.dump(dict(meta=meta, eos=out), open(os.path.join(HERE, "results", "core.json"), "w"), indent=1)
    for n, r in out.items():
        print(n, "Mmax=%.4f R(Mmax)=%.3f R1.4=%s L1.4=%s causal=%s branches=%d" % (
            r["M_max_Msun"], r["R_at_Mmax_km"], r["R_1p4_km"], r["Lambda_1p4"], r["causal_up_to_Mmax"], r["n_stable_branches"]))


if __name__ == "__main__":
    main()
