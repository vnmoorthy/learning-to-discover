"""Extension 1 (CPU / Modal track): scramblers in the sequential evaporation model.

Run:  OMP_NUM_THREADS=1 python3 experiments/e1_scrambling_cpu.py [--quick]   (local)
      modal run experiments/modal_run.py --which e1                          (Modal CPU, same seeds)
Outputs: results/e1_scrambling_cpu.json, figures/e1_cpu_*.png
(The *_cpu suffix keeps this numpy state-vector track separate from the
torch/GPU track in experiments/e1_scrambling.py written by another agent.)

Model: N qubits in |0..0>; per evaporation step a scrambler acts on the
remaining black-hole qubits, then the edge qubit is emitted. S(R) of the
radiation is recorded after each emission (nats). Toy model, no gravity.
"""
from __future__ import annotations
import argparse, json, os, sys, time
from multiprocessing import Pool
import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from eh import circuits as c

BASE_SEED = 20261115
FAMILY_ID = {"haar_shortcut": 0, "local_haar": 1, "clifford": 2, "identity": 3,
             "swap": 4, "h_cnot": 5, "oneshot_haar": 6, "oneshot_clifford": 7}
NS = [8, 9, 10, 11, 12]
DEPTHS = [1, 2, 3, 4, 6, 8, 12, 16]
EPS = 0.05  # nats; scrambling-depth threshold on max_t (Page - <S>)


def rng_for(n, family, depth, idx):
    """Seed rule (recorded in the JSON): SeedSequence([BASE, N, family_id, depth, idx])."""
    return np.random.default_rng(np.random.SeedSequence([BASE_SEED, n, FAMILY_ID[family], depth, idx]))


def job(args):
    n, fam, depth, n_seeds = args
    half = n // 2
    svn = np.zeros((n_seeds, n + 1)); s2 = np.zeros((n_seeds, n + 1))
    rr = np.full(n_seeds, np.nan); spec = np.zeros(2 ** half)
    for i in range(n_seeds):
        r = c.evaporate(n, fam, rng_for(n, fam, depth, i), depth=depth, return_spectra=True)
        svn[i], s2[i] = r["s_vn"], r["s_2"]
        p = r["spectra"][half]                      # radiation = `half` qubits
        rr[i] = c.spacing_ratio(p)
        spec += np.sort(p)[::-1] / n_seeds
    page = c.page_curve(n)
    sem = svn.std(0, ddof=1) / np.sqrt(n_seeds)
    gap = svn - s2
    return {
        "N": n, "family": fam, "depth": depth, "n_seeds": n_seeds,
        "S_vn_mean": svn.mean(0).tolist(), "S_vn_std": svn.std(0, ddof=1).tolist(),
        "S_vn_ci95": (1.96 * sem).tolist(),
        "S_2_mean": s2.mean(0).tolist(), "S_2_std": s2.std(0, ddof=1).tolist(),
        "gap_vn_minus_r2_mean": gap.mean(0).tolist(),
        "gap_vn_minus_r2_ci95": (1.96 * gap.std(0, ddof=1) / np.sqrt(n_seeds)).tolist(),
        "page_minus_S_mean": (page - svn.mean(0)).tolist(),
        "max_dev_from_page": float((page - svn.mean(0)).max()),
        "max_dev_ci95": float((1.96 * sem)[int(np.argmax(page - svn.mean(0)))]),
        "mean_abs_dev_from_page": float(np.abs(page - svn.mean(0))[1:-1].mean()),
        "half_cut_spacing_ratio_mean": (float(np.nanmean(rr)) if np.isfinite(rr).any() else None),
        "half_cut_spacing_ratio_n_defined": int(np.isfinite(rr).sum()),
        "half_cut_mean_sorted_spectrum": spec.tolist(),
    }


def job_oneshot(args):
    n, gate, depth, n_seeds = args
    fam = "oneshot_" + gate
    s = np.array([c.one_shot_entropies(n, depth, rng_for(n, fam, depth, i), gate) for i in range(n_seeds)])
    half = n // 2
    return {"N": n, "gate": gate, "depth": depth, "n_seeds": n_seeds,
            "S_half_mean": float(s[:, half].mean()),
            "S_half_ci95": float(1.96 * s[:, half].std(ddof=1) / np.sqrt(n_seeds)),
            "page_half": c.page_entropy(2 ** half, 2 ** (n - half))}


def first_depth_below(depths, devs, eps):
    for d, v in zip(depths, devs):
        if v <= eps:
            return d
    return None


def build_jobs(quick=False):
    seeds = (lambda n: 12) if quick else (lambda n: 300 if n <= 10 else 150)
    jobs = []
    for n in NS:
        jobs.append((n, "haar_shortcut", 0, seeds(n)))
        for fam in ("identity", "swap", "h_cnot"):
            jobs.append((n, fam, 1, 4))  # deterministic controls
        for d in DEPTHS:
            jobs.append((n, "local_haar", d, seeds(n)))
            jobs.append((n, "clifford", d, seeds(n)))
    os_seeds = 12 if quick else 150
    ojobs = [(n, g, d, os_seeds) for n in NS for g in ("haar", "clifford") for d in range(1, 3 * n + 1)]
    return jobs, ojobs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--procs", type=int, default=2)
    a = ap.parse_args()
    t0 = time.time()
    jobs, ojobs = build_jobs(a.quick)
    with Pool(a.procs) as pool:
        res = pool.map(job, jobs, chunksize=1)
        ores = pool.map(job_oneshot, ojobs, chunksize=4)
    finalize(res, ores, a.quick, t0, "local multiprocessing (numpy)")


def finalize(res, ores, quick, t0, backend):
    proxies = {"eps_nats": EPS, "per_step": [], "one_shot": []}
    for n in NS:
        for fam in ("local_haar", "clifford"):
            rs = sorted([r for r in res if r["N"] == n and r["family"] == fam], key=lambda r: r["depth"])
            proxies["per_step"].append({
                "N": n, "family": fam, "depths": [r["depth"] for r in rs],
                "max_dev": [r["max_dev_from_page"] for r in rs],
                "max_dev_ci95": [r["max_dev_ci95"] for r in rs],
                "d_star": first_depth_below([r["depth"] for r in rs], [r["max_dev_from_page"] for r in rs], EPS)})
        for g in ("haar", "clifford"):
            rs = sorted([r for r in ores if r["N"] == n and r["gate"] == g], key=lambda r: r["depth"])
            devs = [r["page_half"] - r["S_half_mean"] for r in rs]
            proxies["one_shot"].append({
                "N": n, "gate": g, "depths": [r["depth"] for r in rs], "dev_half": devs,
                "dev_half_ci95": [r["S_half_ci95"] for r in rs],
                "D_star": first_depth_below([r["depth"] for r in rs], devs, EPS)})
    hgap = {}
    for n in NS:
        h = n // 2
        hgap[str(n)] = float(c.page_entropy(2 ** h, 2 ** (n - h)) + np.log(c.haar_mean_purity(2 ** h, 2 ** (n - h))))
    out = {
        "experiment": "e1_scrambling_cpu", "units": "nats", "base_seed": BASE_SEED,
        "seed_rule": "numpy default_rng(SeedSequence([base_seed, N, family_id, depth, seed_index]))",
        "family_id": FAMILY_ID, "Ns": NS, "depths_per_step": DEPTHS, "quick": quick, "backend": backend,
        "p_clip": c.P_CLIP,
        "page_curves": {str(n): c.page_curve(n).tolist() for n in NS},
        "haar_gap_half_cut_page_plus_log_mean_purity": hgap,
        "runs": res, "one_shot": ores, "scrambling_proxies": proxies,
        "runtime_s": time.time() - t0,
    }
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "e1_scrambling_cpu.json"), "w") as f:
        json.dump(out, f)
    plots(out)
    print("done in %.1fs" % out["runtime_s"])
    for p in proxies["per_step"]:
        print("per-step", p["N"], p["family"], "d*=", p["d_star"], ["%.3f" % v for v in p["max_dev"]])
    for p in proxies["one_shot"]:
        print("one-shot", p["N"], p["gate"], "D*=", p["D_star"])


def plots(out):
    import _style as st
    plt = st.setup()
    figdir = os.path.join(ROOT, "figures"); os.makedirs(figdir, exist_ok=True)
    L2 = np.log(2)
    get = lambda n, fam, d: next(r for r in out["runs"] if r["N"] == n and r["family"] == fam and r["depth"] == d)
    n = 12; t = np.arange(n + 1)
    ns_main = get(n, "local_haar", 1)["n_seeds"]

    fig, axs = plt.subplots(1, 2, figsize=(12, 4.8), sharey=True)
    page = np.array(out["page_curves"][str(n)]) / L2
    for ax, fam, title in ((axs[0], "local_haar", "local Haar brickwork (d layers / emission)"),
                           (axs[1], "clifford", "random Clifford brickwork (d layers / emission)")):
        for i, d in enumerate([1, 2, 4, 8, 16]):
            r = get(n, fam, d); m = np.array(r["S_vn_mean"]) / L2; s = np.array(r["S_vn_std"]) / L2
            ax.plot(t, m, "-o", ms=3, color=st.PALETTE[i], label=f"d={d}")
            ax.fill_between(t, m - s, m + s, color=st.PALETTE[i], alpha=0.15, lw=0)
        m = np.array(get(n, "haar_shortcut", 0)["S_vn_mean"]) / L2
        ax.plot(t, page, "--", color=st.FG, lw=1.2, label="Page formula (exact)")
        ax.plot(t, m, "x", color=st.FG, ms=6, label="global Haar (sampled)")
        ax.plot(t, np.array(get(n, "h_cnot", 1)["S_vn_mean"]) / L2, ":", color=st.GREY, label="control: Bell dimers (H + 1 CNOT layer)")
        ax.plot(t, np.array(get(n, "identity", 1)["S_vn_mean"]) / L2, "-", color="#555", label="control: identity / SWAPs")
        ax.set_title(title); ax.set_xlabel("emitted qubits t")
    axs[0].set_ylabel("radiation entropy S(R) [bits]"); axs[0].legend(loc="upper left")
    fig.suptitle(f"Extension 1: entropy trajectories by scrambler, N={n}")
    st.caption(fig, f"Sequential evaporation of N={n} qubits from |0..0>, open-chain brickwork, edge qubit emitted each step; "
                    f"bands = std over {ns_main} seeds. Finite-dimensional toy model, no gravity.")
    fig.tight_layout(rect=(0, 0.04, 1, 0.95)); fig.savefig(os.path.join(figdir, "e1_cpu_trajectories.png"), dpi=160); plt.close(fig)

    fig, axs = plt.subplots(1, 3, figsize=(15, 4.6))
    for ax, fam in ((axs[0], "local_haar"), (axs[1], "clifford")):
        for i, p in enumerate([p for p in out["scrambling_proxies"]["per_step"] if p["family"] == fam]):
            ax.errorbar(p["depths"], np.maximum(p["max_dev"], 1e-4), yerr=p["max_dev_ci95"], fmt="-o", ms=3,
                        color=st.PALETTE[i], label=f"N={p['N']}", capsize=2)
        ax.axhline(out["scrambling_proxies"]["eps_nats"], color=st.GREY, ls="--", lw=1)
        ax.set_xscale("log", base=2); ax.set_yscale("log")
        ax.set_xlabel("depth per emission d [layers]"); ax.set_ylabel("max_t [S_Page(t) - <S(R_t)>]  [nats]")
        ax.set_title({"local_haar": "local Haar brickwork", "clifford": "Clifford brickwork"}[fam]); ax.legend()
    ax = axs[2]
    for g, col in (("haar", st.CYAN), ("clifford", st.AMBER)):
        ps = [p for p in out["scrambling_proxies"]["one_shot"] if p["gate"] == g]
        ax.plot([p["N"] for p in ps], [p["D_star"] if p["D_star"] else np.nan for p in ps], "-o", color=col,
                label=f"one-shot D* ({g} gates)")
    for fam, col in (("local_haar", st.MAGENTA), ("clifford", st.GREEN)):
        ps = [p for p in out["scrambling_proxies"]["per_step"] if p["family"] == fam]
        ax.plot([p["N"] for p in ps], [p["d_star"] if p["d_star"] else np.nan for p in ps], "--s", color=col,
                label=f"per-emission d* ({fam})")
    ax.set_xlabel("N [qubits]"); ax.set_ylabel("depth to reach Page value within eps [layers]")
    ax.set_title(f"scrambling-depth proxies (eps = {out['scrambling_proxies']['eps_nats']} nats)"); ax.legend()
    st.caption(fig, "Error bars = 95% CI (1.96 sem over seeds) of <S> at the worst cut. One-shot: D brickwork layers on all N qubits, half cut. "
                    "d* is resolved only on the grid {1,2,3,4,6,8,12,16}; missing point = threshold not reached on the grid.")
    fig.tight_layout(rect=(0, 0.05, 1, 1)); fig.savefig(os.path.join(figdir, "e1_cpu_deviation_scrambling_depth.png"), dpi=160); plt.close(fig)

    fig, axs = plt.subplots(1, 2, figsize=(12, 4.6))
    ax = axs[0]
    for i, (fam, d, lab) in enumerate([("haar_shortcut", 0, "global Haar"), ("local_haar", 1, "local Haar d=1"),
                                        ("local_haar", 4, "local Haar d=4"), ("local_haar", 16, "local Haar d=16"),
                                        ("clifford", 16, "Clifford d=16")]):
        r = get(n, fam, d); g = np.array(r["gap_vn_minus_r2_mean"]); e = np.array(r["gap_vn_minus_r2_ci95"])
        ax.errorbar(t, g, yerr=e, fmt="-o", ms=3, color=st.PALETTE[i], label=lab, capsize=2)
    ax.axhline(out["haar_gap_half_cut_page_plus_log_mean_purity"][str(n)], color=st.GREY, ls="--", lw=1,
               label="S_Page + log E[purity] (Haar, half cut)")
    ax.set_xlabel("emitted qubits t"); ax.set_ylabel("S_vN - S_2  [nats]"); ax.set_title(f"spectral non-flatness, N={n}"); ax.legend()
    ax = axs[1]
    for i, (fam, d, lab) in enumerate([("haar_shortcut", 0, "global Haar"), ("local_haar", 1, "local Haar d=1"),
                                        ("local_haar", 2, "local Haar d=2"), ("local_haar", 16, "local Haar d=16"),
                                        ("clifford", 16, "Clifford d=16 (flat per sample)")]):
        p = np.array(get(n, fam, d)["half_cut_mean_sorted_spectrum"])
        ax.plot(np.arange(1, len(p) + 1), np.maximum(p, 1e-12), "-", color=st.PALETTE[i], label=lab)
    ax.set_yscale("log"); ax.set_ylim(1e-7, 1)
    ax.set_xlabel("Schmidt index i (sorted)"); ax.set_ylabel("seed-averaged eigenvalue p_i of rho_R")
    ax.set_title(f"entanglement spectrum at the half cut, N={n}"); ax.legend()
    st.caption(fig, f"Error bars = 95% CI over {ns_main} seeds. Stabilizer (Clifford) states have exactly flat spectra (S_vN = S_2); "
                    "the seed average of sorted Clifford spectra mixes different ranks.")
    fig.tight_layout(rect=(0, 0.04, 1, 1)); fig.savefig(os.path.join(figdir, "e1_cpu_spectrum.png"), dpi=160); plt.close(fig)


if __name__ == "__main__":
    main()
