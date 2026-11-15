"""Extension 1: scramblers in the sequential evaporation model (GPU, torch complex128).

Run on the GPU box (GPU 0 only):
  CUDA_VISIBLE_DEVICES=0 OMP_NUM_THREADS=4 .venv/bin/python experiments/e1_scrambling.py --Ns 8,10,12,14,16 --tag small
  ... --Ns 24 --tag n24            (one process per size is fine)
  ... --oneshot --Ns 8,...,24 --tag oneshot
  ... --plot                       (merge results/e1_parts/*.json -> results/e1_scrambling.json + figures)

Model: N qubits in |0..0>; per evaporation step a scrambler acts on the
remaining black-hole qubits (open chain, brickwork), then the edge qubit is
emitted.  S(R) of the radiation is recorded after each emission (nats).
Finite-dimensional toy model: no gravity, no islands.
"""
from __future__ import annotations
import argparse, glob, json, os, sys, time
import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from eh import circuits as c

BASE_SEED = 20261115
FAMILY_ID = {"haar_shortcut": 0, "local_haar": 1, "clifford": 2, "identity": 3,
             "swap": 4, "h_cnot": 5, "oneshot_haar": 6, "oneshot_clifford": 7, "haar": 8}
DEPTHS = [1, 2, 4, 8, 16]
EPS = 0.05  # nats; scrambling-depth threshold on max_t (Page - <S>)
# N: (n_seeds, batch)
PLAN = {8: (256, 256), 9: (256, 256), 10: (256, 256), 11: (256, 128), 12: (256, 128), 13: (128, 64),
        14: (128, 64), 15: (64, 32), 16: (64, 32), 18: (32, 16), 20: (24, 12), 22: (12, 6),
        24: (8, 4), 26: (4, 2), 28: (2, 1)}
EXPLICIT_HAAR = {8: 64, 9: 64, 10: 64, 11: 32, 12: 32, 13: 16, 14: 8}   # seeds; N=15 would need >40 GB for QR
ONESHOT = {8: (64, 64), 10: (64, 64), 12: (64, 64), 14: (64, 32), 16: (32, 16), 18: (16, 8),
           20: (16, 8), 22: (8, 4), 24: (8, 4)}
PARTS = os.path.join(ROOT, "results", "e1_parts")


def run_family(n, fam, depth, n_seeds, batch, dev):
    import torch
    t0 = time.time()
    half = n // 2
    acc = {k: [] for k in ("s_vn", "s_2", "s_min", "rank", "norm")}
    spec = None
    keep = half if n <= 24 else None
    for b in range(0, n_seeds, batch):
        bs = min(batch, n_seeds - b)
        ss = np.random.SeedSequence([BASE_SEED, n, FAMILY_ID[fam], depth, b // batch])
        r = c.t_evaporate(n, fam, bs, ss, depth=depth, device=dev, keep_spectrum_at=keep)
        for k in acc:
            acc[k].append(r[k])
        if keep is not None:
            s = r["spectrum"].sum(0)
            spec = s if spec is None else spec + s
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    A = {k: np.concatenate(v, 0) for k, v in acc.items()}
    svn, s2, smin = A["s_vn"], A["s_2"], A["s_min"]
    ns = svn.shape[0]
    sd = lambda x: x.std(0, ddof=1) if ns > 1 else np.zeros(x.shape[1])
    page = c.page_curve(n)
    sem = sd(svn) / np.sqrt(ns)
    dev_t = page - svn.mean(0)
    it = int(np.argmax(dev_t))
    rec = {
        "N": n, "family": fam, "depth": depth, "n_seeds": ns, "batch": batch,
        "seed_rule": "SeedSequence([%d, N, family_id, depth, batch_index])" % BASE_SEED,
        "S_vn_mean": svn.mean(0).tolist(), "S_vn_std": sd(svn).tolist(), "S_vn_ci95": (1.96 * sem).tolist(),
        "S_2_mean": s2.mean(0).tolist(), "S_2_std": sd(s2).tolist(),
        "S_min_mean": smin.mean(0).tolist(),
        "gap_vn_minus_r2_mean": (svn - s2).mean(0).tolist(),
        "gap_vn_minus_r2_ci95": (1.96 * sd(svn - s2) / np.sqrt(ns)).tolist(),
        "gap_vn_minus_r2_max_abs_single_run": float(np.abs(svn - s2).max()),
        "rank_half_mean": float(A["rank"][:, half].mean()),
        "page_minus_S_mean": dev_t.tolist(),
        "max_dev_from_page": float(dev_t.max()), "max_dev_t": it, "max_dev_ci95": float(1.96 * sem[it]),
        "half_dev_from_page": float(dev_t[half]), "half_dev_ci95": float(1.96 * sem[half]),
        "mean_abs_dev_from_page": float(np.abs(dev_t)[1:-1].mean()),
        "max_norm_error": float(np.abs(A["norm"] - 1).max()),
        "half_cut_mean_sorted_spectrum": (spec / ns).tolist() if spec is not None else None,
        "runtime_s": time.time() - t0,
        "gpu_peak_GB": torch.cuda.max_memory_allocated() / 1e9 if torch.cuda.is_available() else None,
    }
    print("N=%d %-13s d=%-2d seeds=%-3d maxdev=%.4f+-%.4f (t=%d) half gap=%.4f  %.1fs  peak %.1f GB" % (
        n, fam, depth, ns, rec["max_dev_from_page"], rec["max_dev_ci95"], it,
        rec["gap_vn_minus_r2_mean"][half], rec["runtime_s"], rec["gpu_peak_GB"] or 0), flush=True)
    return rec


def write_part(tag, payload):
    os.makedirs(PARTS, exist_ok=True)
    with open(os.path.join(PARTS, "e1_%s.json" % tag), "w") as f:
        json.dump(payload, f)


def main_runs(a):
    dev = c.get_device()
    c.two_qubit_clifford_group()
    depths = [int(x) for x in a.depths.split(",")] if a.depths else DEPTHS
    runs = []
    for n in [int(x) for x in a.Ns.split(",")]:
        ns, batch = PLAN[n]
        if a.seeds:
            ns = a.seeds
        runs.append(run_family(n, "haar_shortcut", 0, ns, batch, dev))
        if n in EXPLICIT_HAAR and not a.no_explicit:
            runs.append(run_family(n, "haar", 0, EXPLICIT_HAAR[n], min(batch, 16), dev))
        for fam in ("identity", "swap", "h_cnot"):
            runs.append(run_family(n, fam, 1, 2, 1 if n >= 26 else 2, dev))
        write_part(a.tag, {"runs": runs, "device": str(dev), "complete": False})
        for d in depths:
            for fam in ("local_haar", "clifford"):
                runs.append(run_family(n, fam, d, ns, batch, dev))
                write_part(a.tag, {"runs": runs, "device": str(dev), "complete": False})
    write_part(a.tag, {"runs": runs, "device": str(dev), "complete": True})


def main_oneshot(a):
    dev = c.get_device()
    out = []
    for n in [int(x) for x in a.Ns.split(",")]:
        ns, batch = ONESHOT[n]
        half = n // 2
        for gate in ("haar", "clifford"):
            t0 = time.time()
            sv, s2 = [], []
            for b in range(0, ns, batch):
                ss = np.random.SeedSequence([BASE_SEED, n, FAMILY_ID["oneshot_" + gate], 0, b // batch])
                r = c.t_one_shot(n, gate, 3 * n, batch, ss, dev)
                sv.append(r["s_vn"]); s2.append(r["s_2"])
            sv = np.concatenate(sv, 0); s2 = np.concatenate(s2, 0)
            rec = {"N": n, "gate": gate, "n_seeds": sv.shape[0], "depths": r["depths"],
                   "S_half_mean": sv.mean(0).tolist(),
                   "S_half_ci95": (1.96 * sv.std(0, ddof=1) / np.sqrt(sv.shape[0])).tolist(),
                   "S2_half_mean": s2.mean(0).tolist(),
                   "page_half": c.page_entropy(2 ** half, 2 ** (n - half)), "runtime_s": time.time() - t0}
            out.append(rec)
            print("oneshot N=%d %s done %.1fs, final dev %.4f" % (n, gate, rec["runtime_s"],
                  rec["page_half"] - rec["S_half_mean"][-1]), flush=True)
            write_part(a.tag, {"one_shot": out, "complete": False})
    write_part(a.tag, {"one_shot": out, "complete": True})


def first_depth_below(depths, devs, eps):
    for d, v in zip(depths, devs):
        if v <= eps:
            return d
    return None


def merge():
    runs, ones = [], []
    for p in sorted(glob.glob(os.path.join(PARTS, "e1_*.json"))):
        d = json.load(open(p))
        runs += d.get("runs", []); ones += d.get("one_shot", [])
    # de-duplicate (keep the record with most seeds)
    best = {}
    for r in runs:
        key = (r["N"], r["family"], r["depth"])
        if key not in best or r["n_seeds"] > best[key]["n_seeds"]:
            best[key] = r
    runs = sorted(best.values(), key=lambda r: (r["N"], r["family"], r["depth"]))
    Ns = sorted({r["N"] for r in runs})
    prox = {"eps_nats": EPS, "per_step": [], "one_shot": []}
    for n in Ns:
        for fam in ("local_haar", "clifford"):
            rs = sorted([r for r in runs if r["N"] == n and r["family"] == fam], key=lambda r: r["depth"])
            if rs:
                prox["per_step"].append({
                    "N": n, "family": fam, "depths": [r["depth"] for r in rs], "n_seeds": rs[0]["n_seeds"],
                    "max_dev": [r["max_dev_from_page"] for r in rs], "max_dev_ci95": [r["max_dev_ci95"] for r in rs],
                    "d_star": first_depth_below([r["depth"] for r in rs], [r["max_dev_from_page"] for r in rs], EPS)})
    for r in sorted(ones, key=lambda r: (r["N"], r["gate"])):
        devs = [r["page_half"] - s for s in r["S_half_mean"]]
        # reference for Clifford: its own late-time plateau (stabilizer average != Page)
        plateau = float(np.mean(r["S_half_mean"][-max(4, len(devs) // 6):]))
        prox["one_shot"].append({
            "N": r["N"], "gate": r["gate"], "n_seeds": r["n_seeds"], "depths": r["depths"], "dev_half": devs,
            "dev_half_ci95": r["S_half_ci95"], "late_time_plateau_S": plateau,
            "page_minus_plateau": r["page_half"] - plateau,
            "D_star_vs_page": first_depth_below(r["depths"], devs, EPS),
            "D_star_vs_own_plateau": first_depth_below(r["depths"], [plateau - s for s in r["S_half_mean"]], EPS)})
    fits = {}
    for g, key in (("haar", "D_star_vs_page"), ("clifford", "D_star_vs_own_plateau"), ("haar", "D_star_vs_own_plateau")):
        pts = [(p["N"], p[key]) for p in prox["one_shot"] if p["gate"] == g and p[key] is not None]
        if len(pts) >= 3:
            x, y = np.array(pts, dtype=float).T
            sl, ic = np.polyfit(x, y, 1)
            fits["%s:%s" % (g, key)] = {"slope_layers_per_qubit": float(sl), "intercept": float(ic),
                                        "max_abs_residual": float(np.abs(sl * x + ic - y).max()), "points": pts}
    prox["one_shot_linear_fits"] = fits
    out = {"experiment": "e1_scrambling", "units": "nats", "base_seed": BASE_SEED, "family_id": FAMILY_ID,
           "backend": "torch complex128 on CUDA (A100 40GB), Gram-matrix eigvalsh spectra",
           "gram_clip": c.GRAM_CLIP, "Ns": Ns,
           "page_curves": {str(n): c.page_curve(n).tolist() for n in Ns},
           "haar_gap_half_cut_from_exact_mean_purity": {
               str(n): float(c.page_entropy(2 ** (n // 2), 2 ** (n - n // 2))
                             + np.log(c.haar_mean_purity(2 ** (n // 2), 2 ** (n - n // 2)))) for n in Ns},
           "runs": runs, "one_shot": ones, "scrambling_proxies": prox}
    with open(os.path.join(ROOT, "results", "e1_scrambling.json"), "w") as f:
        json.dump(out, f)
    return out


def plots(out):
    import _style as st
    plt = st.setup()
    figdir = os.path.join(ROOT, "figures"); os.makedirs(figdir, exist_ok=True)
    L2 = np.log(2)
    runs = out["runs"]

    def get(n, fam, d):
        return next((r for r in runs if r["N"] == n and r["family"] == fam and r["depth"] == d), None)
    full = [n for n in out["Ns"] if all(get(n, f, d) for f in ("local_haar", "clifford") for d in DEPTHS)]
    n = max(full); t = np.arange(n + 1)
    ns_main = get(n, "local_haar", 1)["n_seeds"]

    # fig 1: trajectories ------------------------------------------------------
    fig, axs = plt.subplots(1, 2, figsize=(12.5, 5), sharey=True)
    page = np.array(out["page_curves"][str(n)]) / L2
    for ax, fam, title in ((axs[0], "local_haar", "local Haar brickwork (d layers per emission)"),
                           (axs[1], "clifford", "random Clifford brickwork (d layers per emission)")):
        for i, d in enumerate(DEPTHS):
            r = get(n, fam, d); m = np.array(r["S_vn_mean"]) / L2; s = np.array(r["S_vn_std"]) / L2
            ax.plot(t, m, "-o", ms=3, color=st.PALETTE[i], label=f"d={d}")
            ax.fill_between(t, m - s, m + s, color=st.PALETTE[i], alpha=0.18, lw=0)
        ax.plot(t, page, "--", color=st.FG, lw=1.2, label="Page formula (exact Haar mean)")
        ax.plot(t, np.array(get(n, "haar_shortcut", 0)["S_vn_mean"]) / L2, "x", color=st.FG, ms=6, label="global Haar (sampled)")
        ax.plot(t, np.array(get(n, "h_cnot", 1)["S_vn_mean"]) / L2, ":", color=st.GREY, label="control: static Bell dimers")
        ax.plot(t, np.array(get(n, "identity", 1)["S_vn_mean"]) / L2, "-", color="#6E7681", label="control: identity / SWAP network")
        ax.set_title(title); ax.set_xlabel("emitted qubits t")
    axs[0].set_ylabel("radiation entropy S(R) [bits]"); axs[0].legend(loc="upper left")
    fig.suptitle(f"Extension 1: radiation entropy by scrambler, N = {n} qubits (exact state vector, A100)")
    st.caption(fig, f"Sequential evaporation of N={n} qubits from |0..0>; open-chain brickwork on the remaining black hole, edge qubit emitted "
                    f"each step; bands = std over {ns_main} seeds. Finite-dimensional toy model, no gravity.")
    fig.tight_layout(rect=(0, 0.04, 1, 0.95)); fig.savefig(os.path.join(figdir, "e1_trajectories.png"), dpi=160); plt.close(fig)

    # fig 2: deviation vs depth + scrambling proxies -----------------------------
    fig, axs = plt.subplots(1, 3, figsize=(16, 4.9))
    cm = plt.get_cmap("cool")
    for ax, fam in ((axs[0], "local_haar"), (axs[1], "clifford")):
        ps = [p for p in out["scrambling_proxies"]["per_step"] if p["family"] == fam and p["N"] % 2 == 0]
        for i, p in enumerate(ps):
            ax.errorbar(p["depths"], np.maximum(p["max_dev"], 1e-3), yerr=p["max_dev_ci95"], fmt="-o", ms=3,
                        color=cm(i / max(1, len(ps) - 1)), label=f"N={p['N']} ({p['n_seeds']} seeds)", capsize=2, lw=1)
        ax.axhline(out["scrambling_proxies"]["eps_nats"], color=st.AMBER, ls="--", lw=1)
        ax.set_xscale("log", base=2); ax.set_yscale("log"); ax.set_ylim(1e-3, 10)
        ax.set_xlabel("depth per emission d [brickwork layers]"); ax.set_ylabel("max_t [ S_Page(t) - <S(R_t)> ]  [nats]")
        ax.set_title({"local_haar": "local Haar brickwork", "clifford": "Clifford brickwork"}[fam]); ax.legend(fontsize=6.5, ncol=2)
    ax = axs[2]
    pr = out["scrambling_proxies"]
    for g, key, col, lab in (("haar", "D_star_vs_page", st.CYAN, "Haar gates: D* to within eps of Page"),
                             ("clifford", "D_star_vs_own_plateau", st.AMBER, "Clifford gates: D* to within eps of own plateau")):
        ps = [p for p in pr["one_shot"] if p["gate"] == g and p[key] is not None]
        ax.plot([p["N"] for p in ps], [p[key] for p in ps], "o", color=col, label=lab)
        f = pr["one_shot_linear_fits"].get("%s:%s" % (g, key))
        if f:
            xs = np.array([min(p["N"] for p in ps), max(p["N"] for p in ps)])
            ax.plot(xs, f["slope_layers_per_qubit"] * xs + f["intercept"], "-", color=col, lw=1,
                    label="  linear fit: %.2f N %+.1f" % (f["slope_layers_per_qubit"], f["intercept"]))
    ax.set_xlabel("N [qubits]"); ax.set_ylabel("one-shot scrambling depth D* [layers]")
    ax.set_title(f"one-shot half-cut scrambling depth (eps = {pr['eps_nats']} nats)"); ax.legend(fontsize=7)
    st.caption(fig, "Error bars = 95% CI (1.96 sem over seeds) of <S> at the worst cut; values <= 1e-3 (incl. negative: Clifford mean above Page) drawn at 1e-3; amber = eps. One-shot: D brickwork layers on all N qubits "
                    "from |0..0>, half cut, D* read off the seed-mean curve (integer layers). Toy model, open 1D chain.")
    fig.tight_layout(rect=(0, 0.05, 1, 1)); fig.savefig(os.path.join(figdir, "e1_deviation_scrambling_depth.png"), dpi=160); plt.close(fig)

    # fig 3: spectrum ------------------------------------------------------------
    fig, axs = plt.subplots(1, 2, figsize=(12.5, 4.9))
    ax = axs[0]
    sel = [("haar_shortcut", 0, "global Haar"), ("local_haar", 1, "local Haar d=1"), ("local_haar", 4, "local Haar d=4"),
           ("local_haar", 16, "local Haar d=16"), ("clifford", 16, "Clifford d=16 (flat: gap = 0)")]
    for i, (fam, d, lab) in enumerate(sel):
        r = get(n, fam, d); g = np.array(r["gap_vn_minus_r2_mean"]); e = np.array(r["gap_vn_minus_r2_ci95"])
        ax.errorbar(t, g, yerr=e, fmt="-o", ms=3, color=st.PALETTE[i], label=lab, capsize=2)
    ax.axhline(out["haar_gap_half_cut_from_exact_mean_purity"][str(n)], color=st.GREY, ls="--", lw=1,
               label="S_Page + log E[tr rho^2] (Haar, half cut)")
    ax.set_xlabel("emitted qubits t"); ax.set_ylabel("S_vN - S_2  [nats]"); ax.set_title(f"spectral non-flatness, N={n}"); ax.legend(fontsize=7)
    ax = axs[1]
    sel2 = [("haar_shortcut", 0, "global Haar"), ("local_haar", 1, "local Haar d=1"), ("local_haar", 2, "local Haar d=2"),
            ("local_haar", 16, "local Haar d=16"), ("clifford", 16, "Clifford d=16 (seed-avg of flat spectra)")]
    n_spec = max(x for x in full if get(x, "haar_shortcut", 0)["half_cut_mean_sorted_spectrum"] is not None)  # spectra stored for N <= 24
    for i, (fam, d, lab) in enumerate(sel2):
        r = get(n_spec, fam, d)
        p = np.array(r["half_cut_mean_sorted_spectrum"]); D = len(p)
        ax.plot(np.arange(1, D + 1) / D, np.maximum(p * D, 1e-12), "-", color=st.PALETTE[i], label=lab)
    xs = np.linspace(1e-4, 1, 400)
    ax.set_yscale("log"); ax.set_ylim(1e-6, 30)
    ax.set_xlabel("Schmidt index i / 2^(N/2) (sorted, descending)"); ax.set_ylabel("seed-averaged eigenvalue  p_i * 2^(N/2)")
    ax.set_title(f"entanglement spectrum at the half cut, N={n_spec} ({get(n_spec, 'local_haar', 1)['n_seeds']} seeds)"); ax.legend(fontsize=7)
    st.caption(fig, f"Error bars = 95% CI over {ns_main} seeds. Stabilizer (Clifford) states have exactly flat spectra (S_vN = S_2 = S_min per run); "
                    "the seed average of sorted Clifford spectra mixes different ranks. Toy model.")
    fig.tight_layout(rect=(0, 0.04, 1, 1)); fig.savefig(os.path.join(figdir, "e1_spectrum.png"), dpi=160); plt.close(fig)

    # fig 4: size scaling --------------------------------------------------------
    fig, axs = plt.subplots(1, 3, figsize=(16, 4.8))
    for ax, fam in ((axs[0], "local_haar"), (axs[1], "clifford")):
        for i, d in enumerate(DEPTHS):
            rs = [r for r in runs if r["family"] == fam and r["depth"] == d and r["N"] % 2 == 0]
            ax.errorbar([r["N"] for r in rs], [r["max_dev_from_page"] for r in rs], yerr=[r["max_dev_ci95"] for r in rs],
                        fmt="-o", ms=3, color=st.PALETTE[i], label=f"d={d}", capsize=2)
        rs = [r for r in runs if r["family"] == "haar_shortcut" and r["N"] % 2 == 0]
        ax.errorbar([r["N"] for r in rs], [abs(r["max_dev_from_page"]) for r in rs], yerr=[r["max_dev_ci95"] for r in rs],
                    fmt=":x", color=st.FG, label="global Haar (|.|, sampling noise)", capsize=2)
        ax.set_yscale("log"); ax.set_xlabel("N [qubits]"); ax.set_ylabel("max_t [ S_Page - <S> ]  [nats]")
        ax.set_title("deviation from Page vs size: " + {"local_haar": "local Haar", "clifford": "Clifford"}[fam]); ax.legend(fontsize=7)
    ax = axs[2]
    for fam, d, col in (("local_haar", 16, st.CYAN), ("clifford", 16, st.AMBER), ("haar_shortcut", 0, st.GREEN), ("haar", 0, st.MAGENTA)):
        rs = [r for r in runs if r["family"] == fam and r["depth"] == d]
        ax.plot([r["N"] for r in rs], [r["runtime_s"] / r["n_seeds"] for r in rs], "-o", ms=3, color=col,
                label={"haar": "explicit sequential Haar (dense QR)", "haar_shortcut": "global Haar state"}.get(fam, f"{fam} d=16"))
    ax.set_yscale("log"); ax.set_xlabel("N [qubits]"); ax.set_ylabel("wall time per seed [s] (batched, shared GPU)")
    ax.set_title("cost scaling on one A100 (complex128)"); ax.legend(fontsize=7)
    st.caption(fig, "Error bars = 95% CI over seeds (seed counts shrink with N: see JSON). Runtime includes all N entanglement spectra per run; "
                    "memory is 16 * 2^N bytes per state (4.3 GB at N=28). Toy model.")
    fig.tight_layout(rect=(0, 0.05, 1, 1)); fig.savefig(os.path.join(figdir, "e1_size_scaling.png"), dpi=160); plt.close(fig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--Ns", default="8,10,12")
    ap.add_argument("--tag", default="default")
    ap.add_argument("--depths", default="")
    ap.add_argument("--seeds", type=int, default=0)
    ap.add_argument("--no-explicit", action="store_true")
    ap.add_argument("--oneshot", action="store_true")
    ap.add_argument("--plot", action="store_true")
    a = ap.parse_args()
    if a.plot:
        o = merge(); plots(o)
        for p in o["scrambling_proxies"]["per_step"]:
            print("per-step", p["N"], p["family"], "d*=", p["d_star"], ["%.4f" % v for v in p["max_dev"]])
        for p in o["scrambling_proxies"]["one_shot"]:
            print("one-shot", p["N"], p["gate"], "D*page=", p["D_star_vs_page"], "D*plateau=", p["D_star_vs_own_plateau"],
                  "page-plateau=%.4f" % p["page_minus_plateau"])
        print(json.dumps(o["scrambling_proxies"]["one_shot_linear_fits"], indent=1))
    elif a.oneshot:
        main_oneshot(a)
    else:
        main_runs(a)
