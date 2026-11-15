"""Extension 2 (CPU / Modal track): Hayden-Preskill recovery, finite-dimensional toy model.

Run:  OMP_NUM_THREADS=1 python3 experiments/e2_hayden_preskill_cpu.py [--quick]   (local)
      modal run experiments/modal_run.py --which e2                              (Modal CPU, same seeds)
Outputs: results/e2_hayden_preskill_cpu.json, figures/e2_cpu_*.png
(The *_cpu suffix keeps this numpy track separate from the torch/GPU track in
experiments/e2_hayden_preskill.py written by another agent.)
"""
from __future__ import annotations
import argparse, json, os, sys, time
from multiprocessing import Pool
import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from eh import circuits as c
from eh import hayden_preskill as hp

BASE_SEED = 20261116
KIND_ID = {"old_haar": 0, "young_haar": 1, "old_local": 2}
MAX_DIM = 512  # dense trace-distance / fidelity only when d_R d_B' <= MAX_DIM
KEYS = ["I_R_ED", "I_R_Bp", "T_prod", "T_mm", "F_uhl", "F_EPR", "P_EPR", "purity_RBp"]


def rng_for(kind, k, nB, extra, idx):
    """Seed rule: SeedSequence([BASE, kind_id, k, n_B, extra, seed_index])."""
    return np.random.default_rng(np.random.SeedSequence([BASE_SEED, KIND_ID[kind], k, nB, extra, idx]))


def job(args):
    kind, k, nB, extra, idx = args
    rng = rng_for(kind, k, nB, extra, idx)
    n = k + nB
    row = {key: np.full(n + 1, np.nan) for key in KEYS}
    if kind == "old_haar":
        U = c.haar_unitary(2 ** n, rng)
    elif kind == "old_local":
        U = c.brickwork_unitary(n, extra, rng, "haar")  # extra = depth
    else:
        V = hp.haar_isometry(2 ** n, 2 ** k, rng)
    for m in range(n + 1):
        if kind == "young_haar":
            T = hp.hp_state_young(V, k, nB, m)
        else:
            T = hp.hp_state_old(U, k, nB, m)
            y = hp.yoshida_kitaev(U, k, nB, m)
            row["F_EPR"][m], row["P_EPR"][m] = y["F_EPR"], y["P_EPR"]
        a = hp.analyze(T, k, with_decoupling=(kind != "old_local"), max_dim=MAX_DIM)
        for key in a:
            if key in row:
                row[key][m] = a[key]
    return [kind, k, nB, extra, {key: [None if np.isnan(x) else float(x) for x in v] for key, v in row.items()}]


def summarise(rows):
    out = {}
    for key in KEYS:
        arr = np.array([[np.nan if x is None else x for x in r[key]] for r in rows], dtype=float)
        if np.isnan(arr).all():
            continue
        ns = np.isfinite(arr).sum(0)
        mean = np.full(arr.shape[1], np.nan); std = np.full(arr.shape[1], np.nan)
        for j in range(arr.shape[1]):
            col = arr[:, j][np.isfinite(arr[:, j])]
            if len(col):
                mean[j] = col.mean()
            if len(col) > 1:
                std[j] = col.std(ddof=1)
        f = lambda x: None if np.isnan(x) else float(x)
        out[key] = {"mean": [f(x) for x in mean], "std": [f(x) for x in std],
                    "ci95": [f(1.96 * x / np.sqrt(max(q, 1))) for x, q in zip(std, ns)]}
    return out


def build_jobs(quick=False):
    q = quick
    configs = []  # (kind, k, nB, extra, n_seeds)
    for k in (1, 2, 3):
        for nB in (2, 4, 6):
            configs.append(("old_haar", k, nB, 0, 6 if q else (100 if k + nB <= 8 else 50)))
    for k in (1, 2):
        configs.append(("old_haar", k, 8, 0, 3 if q else 24))
    for k, nB in ((1, 6), (1, 8), (1, 10), (2, 6), (2, 8)):
        configs.append(("young_haar", k, nB, 0, 6 if q else 100))
    for depth in (1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 16, 24):
        configs.append(("old_local", 1, 6, depth, 6 if q else 60))
    jobs = [(kind, k, nB, extra, i) for (kind, k, nB, extra, ns) in configs for i in range(ns)]
    return configs, jobs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--procs", type=int, default=2)
    a = ap.parse_args()
    t0 = time.time()
    configs, jobs = build_jobs(a.quick)
    with Pool(a.procs) as pool:
        res = pool.map(job, jobs, chunksize=2)
    finalize(configs, res, a.quick, t0, "local multiprocessing (numpy)")


def finalize(configs, res, q, t0, backend):
    runs = []
    for (kind, k, nB, extra, ns) in configs:
        rows = [r[4] for r in res if tuple(r[:4]) == (kind, k, nB, extra)]
        n = k + nB
        entry = {"kind": kind, "k": k, "n_B": nB, "n_seeds": len(rows), "m": list(range(n + 1)), "stats": summarise(rows)}
        if kind == "old_local":
            entry["depth"] = extra
        old = kind != "young_haar"
        entry["analytic"] = {
            "decoupling_bound_T_mm": [hp.decoupling_bound_mm(k, nB, m, old) for m in range(n + 1)],
            "haar_mean_purity_RBp": [(hp.haar_mean_purity_RBp_old if old else hp.haar_mean_purity_RBp_young)(k, nB, m) for m in range(n + 1)],
        }
        if old:
            entry["analytic"]["F_EPR_from_mean_purity"] = [hp.yk_fidelity_prediction(k, nB, m) for m in range(n + 1)]
            entry["analytic"]["F_EPR_large_d"] = [hp.yk_fidelity_large_d(k, m) for m in range(n + 1)]
        runs.append(entry)
    out = {"experiment": "e2_hayden_preskill_cpu", "units": "nats", "base_seed": BASE_SEED,
           "seed_rule": "numpy default_rng(SeedSequence([base_seed, kind_id, k, n_B, extra(depth or 0), seed_index]))",
           "kind_id": KIND_ID, "max_dim_dense": MAX_DIM, "p_clip": c.P_CLIP, "quick": q, "backend": backend,
           "geometry": "A = first k qubits of the n=k+n_B scrambled register, D = last m qubits, B' = first n-m",
           "runs": runs, "runtime_s": time.time() - t0}
    with open(os.path.join(ROOT, "results", "e2_hayden_preskill_cpu.json"), "w") as f:
        json.dump(out, f)
    plots(out)
    print("done in %.1fs" % out["runtime_s"])
    L2 = np.log(2)
    for r in runs:
        k = r["k"]; s = r["stats"]; top = len(r["m"])
        if r["kind"] == "old_local":
            print(f"old_local depth={r['depth']}: I(R:ED) bits m=1,2,3,5: " + " ".join("%.3f" % (s["I_R_ED"]["mean"][m] / L2) for m in (1, 2, 3, 5))
                  + " | F_YK: " + " ".join("%.3f" % s["F_EPR"]["mean"][m] for m in (1, 2, 3, 5)))
            continue
        line = f"{r['kind']} k={k} nB={r['n_B']} seeds={r['n_seeds']}: I(R:ED)/(2k bits) all m: " + \
               " ".join("%.3f" % (s["I_R_ED"]["mean"][m] / (2 * k * L2)) for m in range(top))
        if "F_EPR" in s:
            line += " | F_YK: " + " ".join("%.3f" % s["F_EPR"]["mean"][m] for m in range(top))
        if "F_uhl" in s:
            line += " | F_uhl: " + " ".join("nan" if s["F_uhl"]["mean"][m] is None else "%.3f" % s["F_uhl"]["mean"][m] for m in range(top))
        if "T_prod" in s:
            line += " | T_prod: " + " ".join("nan" if s["T_prod"]["mean"][m] is None else "%.3f" % s["T_prod"]["mean"][m] for m in range(top))
        print(line)


def plots(out):
    import _style as st
    plt = st.setup()
    figdir = os.path.join(ROOT, "figures"); os.makedirs(figdir, exist_ok=True)
    L2 = np.log(2)
    runs = out["runs"]
    sel = lambda kind, k: sorted([r for r in runs if r["kind"] == kind and r["k"] == k], key=lambda r: r["n_B"])
    arr = lambda x: np.array([np.nan if v is None else v for v in x], dtype=float)

    fig, axs = plt.subplots(1, 3, figsize=(15, 4.6))
    for ax, k in zip(axs, (1, 2, 3)):
        for i, r in enumerate(sel("old_haar", k)):
            m = np.array(r["m"]); y = arr(r["stats"]["I_R_ED"]["mean"]) / L2; e = arr(r["stats"]["I_R_ED"]["std"]) / L2
            ax.errorbar(m, y, yerr=e, fmt="-o", ms=3.5, capsize=2, color=st.PALETTE[i], label=f"n_B={r['n_B']} ({r['n_seeds']} seeds)")
        ax.axhline(2 * k, color=st.GREY, ls="--", lw=1); ax.axvline(k, color=st.GREY, ls=":", lw=1)
        ax.text(k + 0.1, 0.1, "m = k", color=st.GREY, fontsize=8)
        ax.set_title(f"old black hole, k = {k} diary qubit(s)"); ax.set_xlabel("emitted qubits m after the diary")
        ax.set_ylabel("I(R_A : E D) [bits]"); ax.legend(loc="lower right")
    st.caption(fig, "Haar U on diary+black hole; B maximally entangled with early radiation E (old black hole). Error bars = std over seeds. "
                    "Dashed: 2k bits (full recovery). Toy model, no gravity.")
    fig.tight_layout(rect=(0, 0.04, 1, 1)); fig.savefig(os.path.join(figdir, "e2_cpu_mutual_information.png"), dpi=160); plt.close(fig)

    fig, axs = plt.subplots(1, 3, figsize=(15, 4.6))
    for ax, k in zip(axs, (1, 2, 3)):
        rs = sel("old_haar", k)
        for i, r in enumerate(rs):
            m = np.array(r["m"])
            ax.errorbar(m, arr(r["stats"]["F_EPR"]["mean"]), yerr=arr(r["stats"]["F_EPR"]["std"]), fmt="o", ms=4, capsize=2,
                        color=st.PALETTE[i], label=f"YK decoder F_EPR, n_B={r['n_B']}")
            ax.plot(m, r["analytic"]["F_EPR_from_mean_purity"], "-", lw=0.9, color=st.PALETTE[i], alpha=0.8)
            ax.plot(m, arr(r["stats"]["F_uhl"]["mean"]), ":", lw=1.2, color=st.PALETTE[i])
        mm = np.linspace(0, max(rs[-1]["m"]), 200)
        ax.plot(mm, 1 / (1 + 4.0 ** (k - mm) - 4.0 ** (-mm)), "--", color=st.FG, lw=1, label="large-d: 1/(1+4^(k-m)-4^(-m))")
        ax.plot([], [], "-", color=st.GREY, lw=0.9, label="exact Haar-mean-purity prediction")
        ax.plot([], [], ":", color=st.GREY, label="Uhlmann lower bound on optimal F")
        ax.axvline(k, color=st.GREY, ls=":", lw=1)
        ax.set_title(f"old black hole, k = {k}"); ax.set_xlabel("emitted qubits m after the diary"); ax.set_ylabel("recovery fidelity with |Bell>_{R R'}")
        ax.legend(loc="lower right", fontsize=7)
    st.caption(fig, "Yoshida-Kitaev probabilistic decoder (post-selected on Bell projection of D D'); error bars = std over seeds. "
                    f"Uhlmann bound F(rho_RB', rho_R x rho_B') shown only where d_R d_B' <= {out['max_dim_dense']}.")
    fig.tight_layout(rect=(0, 0.04, 1, 1)); fig.savefig(os.path.join(figdir, "e2_cpu_recovery_fidelity.png"), dpi=160); plt.close(fig)

    fig, axs = plt.subplots(1, 3, figsize=(15, 4.6))
    for ax, k in zip(axs, (1, 2, 3)):
        rs = sel("old_haar", k)
        for i, r in enumerate(rs):
            m = np.array(r["m"]); y = arr(r["stats"]["T_prod"]["mean"]); e = arr(r["stats"]["T_prod"]["ci95"])
            ok = y > 1e-9
            ax.errorbar(m[ok], y[ok], yerr=e[ok], fmt="-o", ms=3.5, capsize=2, color=st.PALETTE[i], label=f"n_B={r['n_B']}")
            ax.plot(m, np.maximum(r["analytic"]["decoupling_bound_T_mm"], 1e-9), "--", lw=0.8, color=st.PALETTE[i], alpha=0.7)
        mm = np.arange(0, max(rs[-1]["m"]) + 1)
        ax.plot(mm, 0.5 * 2.0 ** (k - mm), "-", color=st.FG, lw=1, label="(1/2) 2^(k-m)  (large-d bound on E[T_mm])")
        ax.plot([], [], "--", color=st.GREY, lw=0.8, label="finite-d bound (1/2)sqrt(D E[P]-1)")
        ax.set_yscale("log"); ax.set_ylim(1e-3, 2)
        ax.set_title(f"old black hole, k = {k}"); ax.set_xlabel("emitted qubits m after the diary")
        ax.set_ylabel("(1/2)||rho_RB' - rho_R x rho_B'||_1"); ax.legend(loc="lower left", fontsize=7)
    st.caption(fig, "Decoupling of the reference from the remaining black hole B'. Error bars = 95% CI over seeds. m = n (B' empty, T = 0) omitted on the log axis; "
                    f"values only where d_R d_B' <= {out['max_dim_dense']}.")
    fig.tight_layout(rect=(0, 0.04, 1, 1)); fig.savefig(os.path.join(figdir, "e2_cpu_decoupling.png"), dpi=160); plt.close(fig)

    fig, axs = plt.subplots(1, 2, figsize=(12, 4.6))
    for i, r in enumerate(sel("young_haar", 1)):
        m = np.array(r["m"]); nB = r["n_B"]
        axs[0].errorbar(m, arr(r["stats"]["I_R_ED"]["mean"]) / L2, yerr=arr(r["stats"]["I_R_ED"]["std"]) / L2, fmt="-o", ms=3.5, capsize=2,
                        color=st.PALETTE[i], label=f"young, n_B={nB}")
        axs[0].axvline(1 + nB / 2, color=st.PALETTE[i], ls=":", lw=1)
        axs[1].errorbar(m, arr(r["stats"]["F_uhl"]["mean"]), yerr=arr(r["stats"]["F_uhl"]["std"]), fmt="-o", ms=3.5, capsize=2,
                        color=st.PALETTE[i], label=f"young, n_B={nB}")
        axs[1].axvline(1 + nB / 2, color=st.PALETTE[i], ls=":", lw=1)
    for r in sel("old_haar", 1):
        if r["n_B"] == 8:
            m = np.array(r["m"])
            axs[0].plot(m, arr(r["stats"]["I_R_ED"]["mean"]) / L2, "--s", ms=3.5, color=st.FG, label="old, n_B=8")
            axs[1].plot(m, arr(r["stats"]["F_uhl"]["mean"]), "--s", ms=3.5, color=st.FG, label="old, n_B=8")
    axs[0].set_xlabel("emitted qubits m"); axs[0].set_ylabel("I(R_A : Bob's radiation) [bits]"); axs[0].set_title("k = 1: young (no early radiation) vs old black hole")
    axs[1].set_xlabel("emitted qubits m"); axs[1].set_ylabel("Uhlmann lower bound on optimal recovery fidelity"); axs[1].set_title("young: recovery needs m > k + n_B/2")
    axs[0].legend(); axs[1].legend()
    st.caption(fig, "Young: B starts in |0..0>, Bob holds only D. Dotted verticals: m = k + n_B/2. Error bars = std over seeds; "
                    f"fidelity bound only where d_R d_B' <= {out['max_dim_dense']}.")
    fig.tight_layout(rect=(0, 0.04, 1, 1)); fig.savefig(os.path.join(figdir, "e2_cpu_young_vs_old.png"), dpi=160); plt.close(fig)

    loc = sorted([r for r in runs if r["kind"] == "old_local"], key=lambda r: r["depth"])
    if loc:
        fig, axs = plt.subplots(1, 2, figsize=(12, 4.6))
        ds = [r["depth"] for r in loc]
        haar = next(r for r in runs if r["kind"] == "old_haar" and r["k"] == 1 and r["n_B"] == 6)
        for i, m in enumerate((1, 2, 3, 5)):
            for ax, key, sc in ((axs[0], "I_R_ED", L2), (axs[1], "F_EPR", 1.0)):
                y = [r["stats"][key]["mean"][m] / sc for r in loc]; e = [(r["stats"][key]["ci95"][m] or 0) / sc for r in loc]
                ax.errorbar(ds, y, yerr=e, fmt="-o", ms=3.5, capsize=2, color=st.PALETTE[i], label=f"m={m}")
                ax.axhline(haar["stats"][key]["mean"][m] / sc, color=st.PALETTE[i], ls="--", lw=0.8)
        axs[0].set_ylabel("I(R_A : E D) [bits]"); axs[1].set_ylabel("YK decoder fidelity F_EPR")
        for ax in axs:
            ax.set_xscale("log", base=2); ax.set_xlabel("brickwork depth of U [layers]"); ax.legend()
        axs[0].set_title("local-circuit scrambler, k=1, n_B=6 (7-qubit chain)"); axs[1].set_title("dashed = Haar-U value")
        st.caption(fig, "U = open-chain brickwork of Haar 2-qubit gates; diary at qubit 0, D = last m qubits (far end: worst case, light-cone delay). "
                        f"Error bars = 95% CI over {loc[0]['n_seeds']} seeds.")
        fig.tight_layout(rect=(0, 0.04, 1, 1)); fig.savefig(os.path.join(figdir, "e2_cpu_local_circuit.png"), dpi=160); plt.close(fig)


if __name__ == "__main__":
    main()
