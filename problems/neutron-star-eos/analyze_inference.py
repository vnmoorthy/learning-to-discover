"""Diagnostics, figures and results/inference.json from the cached chains of run_inference.py.
Convergence rule: a chain is reported as a posterior only if (after discarding the first half as burn-in)
the run length exceeds 50 integrated autocorrelation times for every parameter, emcee's tau estimate is
reliable, and the mean acceptance fraction is in [0.15, 0.7]. Otherwise its samples are labelled
NOT_A_POSTERIOR and only diagnostics are reported."""
import json
import os
import sys

sys.modules.setdefault("h5py", None)
import numpy as np
import emcee
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.special import logsumexp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from run_inference import LABELS, M_GRID, BOUNDS  # noqa: E402

BG, FG, C1, C2 = "#0B0D10", "#E7E9EC", "#4FD1E0", "#E2B25C"
plt.rcParams.update({"figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG, "text.color": FG,
                     "axes.labelcolor": FG, "xtick.color": FG, "ytick.color": FG, "axes.edgecolor": FG,
                     "legend.facecolor": BG, "legend.edgecolor": FG, "font.size": 9})
FIG = os.path.join(HERE, "figures")


def load(model, prior):
    d = np.load(os.path.join(HERE, "results", f"chain_{model}_{prior}.npz"))
    return {k: d[k] for k in d.files}


def diagnose(d):
    ch = d["chain"]
    nstep, nw, nd = ch.shape
    burn = nstep // 2
    post = ch[burn:]
    try:
        tau = emcee.autocorr.integrated_time(post, quiet=True)
    except Exception:
        tau = np.full(nd, np.nan)
    n_post = post.shape[0]
    tau_max = float(np.nanmax(tau)) if np.any(np.isfinite(tau)) else float("nan")
    acc = float(np.mean(d["acc"]))
    neff = float(nw * n_post / tau_max) if np.isfinite(tau_max) and tau_max > 0 else float("nan")
    ok = bool(np.isfinite(tau_max) and n_post > 50 * tau_max and 0.15 <= acc <= 0.7)
    return dict(n_steps=int(nstep), n_walkers=int(nw), burn_in=int(burn), acceptance_fraction=acc,
                tau=[float(t) for t in tau], tau_max=tau_max, steps_over_tau=float(n_post / tau_max) if np.isfinite(tau_max) else None,
                n_independent=neff, wall_s=float(d["wall"]), converged=ok), burn


def q(x):
    x = x[np.isfinite(x)]
    if len(x) < 5:
        return None
    a = np.percentile(x, [5, 16, 50, 84, 95])
    return dict(median=float(a[2]), ci68=[float(a[1]), float(a[3])], ci90=[float(a[0]), float(a[4])], n=int(len(x)))


def flat(d, burn):
    ch = d["chain"][burn:].reshape(-1, 4)
    bl = d["blobs"][burn:].reshape(-1, d["blobs"].shape[-1]).astype(float)
    good = np.isfinite(d["lnp"][burn:].reshape(-1))
    return ch[good], bl[good]


def main():
    res = {"units": {"M": "M_sun", "R": "km", "Lambda": "dimensionless"}, "runs": {},
           "likelihood": "sf/likelihood.py; data/observations.json",
           "tov_solver": "sf/fasttov.py (RK4 in xi = sqrt(ln pc - ln P), 18 central pressures, 160 steps)",
           "novelty_level": 1, "novelty_note": "Level 1-2: reproduction of a standard multimessenger EOS inference with approximate likelihoods; not a discovery."}
    S = {}
    for model in ("PP", "CS"):
        for prior in ("A", "B"):
            try:
                d = load(model, prior)
            except FileNotFoundError:
                continue
            dg, burn = diagnose(d)
            ch, bl = flat(d, burn)
            S[(model, prior)] = (ch, bl, dg)
            summ = {"M_max": q(bl[:, 0]), "R_1.4": q(bl[:, 1]), "Lambda_1.4": q(bl[:, 2]),
                    "params": {LABELS[model][i]: q(ch[:, i]) for i in range(4)}}
            key = "posterior" if dg["converged"] else "unconverged_chain_quantiles_NOT_A_POSTERIOR"
            res["runs"][f"{model}_{prior}"] = {"diagnostics": dg, key: summ}
    # evidence (prior Monte Carlo, prior A)
    ev = {}
    for model in ("PP", "CS"):
        p = os.path.join(HERE, "results", f"evidence_{model}.npz")
        if not os.path.exists(p):
            continue
        e = np.load(p)
        lls = e["lls"]
        if len(lls) < 2:
            continue
        logZ = float(logsumexp(lls) - np.log(len(lls)))
        rng = np.random.default_rng(0)
        boots = [logsumexp(lls[rng.integers(0, len(lls), len(lls))]) - np.log(len(lls)) for _ in range(2000)]
        w = np.exp(lls - lls.max())
        ev[model] = dict(logZ=logZ, logZ_bootstrap_sd=float(np.std(boots)), n_support=int(e["nsupport"]),
                         n_draws=int(e["ndraw"]), support_fraction=float(e["nsupport"] / max(e["ndraw"], 1)),
                         ess_of_weights=float(w.sum() ** 2 / (w ** 2).sum()))
    if "PP" in ev and "CS" in ev:
        lnB = ev["CS"]["logZ"] - ev["PP"]["logZ"]
        sd = float(np.hypot(ev["CS"]["logZ_bootstrap_sd"], ev["PP"]["logZ_bootstrap_sd"]))
        ev["ln_Bayes_factor_CS_over_PP"] = dict(value=float(lnB), sd=sd,
            note="Prior-A evidences of the truncated priors via prior Monte Carlo (unbiased; error by bootstrap). "
                 "Same likelihood for both models, so normalisation constants cancel. |lnB| < ~1 is inconclusive (Jeffreys).")
    res["evidence"] = ev
    with open(os.path.join(HERE, "results", "inference.json"), "w") as f:
        json.dump(res, f, indent=2)

    # --- corner plots (prior A, both models)
    fig = plt.figure(figsize=(13, 6.4))
    subs = fig.subfigures(1, 2)
    for sf_, model in zip(subs, ("PP", "CS")):
        if (model, "A") not in S:
            continue
        ch, bl, dg = S[(model, "A")]
        ax = sf_.subplots(4, 4)
        for i in range(4):
            for j in range(4):
                a = ax[i, j]
                if j > i:
                    a.axis("off")
                    continue
                if i == j:
                    a.hist(ch[:, i], bins=20, color=C1, histtype="step")
                    a.set_yticks([])
                else:
                    a.plot(ch[:, j], ch[:, i], ".", ms=1.5, color=C1, alpha=0.5)
                if i == 3:
                    a.set_xlabel(LABELS[model][j], fontsize=7)
                else:
                    a.set_xticklabels([])
                if j == 0 and i > 0:
                    a.set_ylabel(LABELS[model][i], fontsize=7)
                a.tick_params(labelsize=6)
        tag = "converged" if dg["converged"] else "NOT CONVERGED - not a posterior"
        sf_.suptitle(f"{model} prior A: {dg['n_steps']} steps x {dg['n_walkers']} walkers, acc={dg['acceptance_fraction']:.2f}, "
                     f"tau_max={dg['tau_max']:.1f} [{tag}]", fontsize=8, color=FG)
    fig.savefig(os.path.join(FIG, "posterior_corner.png"), dpi=160)
    plt.close(fig)

    # --- M-R band
    fig, ax = plt.subplots(figsize=(6.4, 5.2))
    for (model, col) in (("PP", C1), ("CS", C2)):
        if (model, "A") not in S:
            continue
        ch, bl, dg = S[(model, "A")]
        R = bl[:, 3:]
        lo, hi, l9, h9 = [], [], [], []
        mm = []
        for k, m in enumerate(M_GRID):
            x = R[:, k][np.isfinite(R[:, k])]
            if len(x) < 10:
                continue
            a = np.percentile(x, [5, 16, 84, 95])
            mm.append(m); l9.append(a[0]); lo.append(a[1]); hi.append(a[2]); h9.append(a[3])
        mm = np.array(mm)
        ax.fill_betweenx(mm, l9, h9, color=col, alpha=0.15)
        ax.fill_betweenx(mm, lo, hi, color=col, alpha=0.35,
                         label=f"{model} (prior A) 68%/90%" + ("" if dg["converged"] else " - unconverged"))
    for (r, rm, rp, m, mmn, mp, lab) in [(12.71, 1.19, 1.14, 1.34, 0.16, 0.15, "J0030 Riley+19"),
                                         (13.02, 1.06, 1.24, 1.44, 0.14, 0.15, "J0030 Miller+19"),
                                         (12.39, 0.98, 1.30, 2.072, 0.066, 0.067, "J0740 Riley+21"),
                                         (13.7, 1.5, 2.6, 2.08, 0.07, 0.07, "J0740 Miller+21")]:
        ax.errorbar(r, m, xerr=[[rm], [rp]], yerr=[[mmn], [mp]], fmt="o", ms=3, color=FG, alpha=0.7, lw=0.8)
        ax.annotate(lab, (r, m), fontsize=6, color=FG, xytext=(3, 3), textcoords="offset points")
    ax.set_xlabel("R [km]")
    ax.set_ylabel("M [M$_\\odot$]")
    ax.set_xlim(9, 16)
    ax.set_ylim(0.9, 2.5)
    ax.legend(fontsize=7, loc="lower left")
    ax.set_title("Posterior-predictive M-R band (bars: published 68% NICER intervals)", fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "posterior_mr_band.png"), dpi=160)
    plt.close(fig)

    # --- prior sensitivity
    fig, axs = plt.subplots(2, 3, figsize=(11, 6))
    names = [("M_max [M$_\\odot$]", 0), ("R$_{1.4}$ [km]", 1), ("$\\Lambda_{1.4}$ [dimensionless]", 2)]
    for r_, model in enumerate(("PP", "CS")):
        for c_, (nm, k) in enumerate(names):
            a = axs[r_, c_]
            for prior, col in (("A", C1), ("B", C2)):
                if (model, prior) not in S:
                    continue
                x = S[(model, prior)][1][:, k]
                x = x[np.isfinite(x)]
                if len(x):
                    a.hist(x, bins=20, histtype="step", color=col, density=True, label=f"prior {prior}")
            a.set_xlabel(nm)
            a.set_ylabel("density [1/unit]")
            a.set_title(f"{model}", fontsize=8)
            a.legend(fontsize=7)
    fig.suptitle("Prior sensitivity (short chains; see diagnostics in results/inference.json)", fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "prior_sensitivity.png"), dpi=160)
    plt.close(fig)
    print(json.dumps(res, indent=1)[:6000])


if __name__ == "__main__":
    main()
