"""Extension 2: Hayden-Preskill recovery in a finite-dimensional toy model (GPU).

Run on the GPU box (GPU 0 only):
  CUDA_VISIBLE_DEVICES=0 OMP_NUM_THREADS=4 .venv/bin/python experiments/e2_hayden_preskill.py --part old
  ... --part young      ... --part local      ... --part big   (n = 13: 26-qubit global state)
  ... --plot            (merge results/e2_parts/*.json -> results/e2_hayden_preskill.json + figures)

Setup: diary A (k qubits) maximally entangled with reference R; black hole B
(n_B qubits). OLD: B maximally entangled with early radiation E.  YOUNG: B in
|0..0>, no E.  Scrambler U on A+B (n = k + n_B qubits), then the last m
qubits D are emitted.  Bob holds E D (old) or D (young).
Toy model of unitary scrambling; no gravity, no islands.  Entropies in nats.
"""
from __future__ import annotations
import argparse, glob, json, os, sys, time
import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from eh import circuits as c
from eh import hayden_preskill as hp

BASE_SEED = 20261115
EXP_ID = 2
VARIANT = {"old_haar": 0, "young_haar": 1, "old_local_haar": 2, "old_local_clifford": 3}
PARTS = os.path.join(ROOT, "results", "e2_parts")
L2 = float(np.log(2.0))
OLD_KEYS = ("I_R_ED", "I_R_Bp", "T_prod", "F_uhl", "F_EPR", "P_EPR", "purity_RBp")
YOUNG_KEYS = ("I_R_D", "I_R_Bp", "T_prod", "T_mm", "F_uhl", "purity_RBp")


def seed_for(variant, k, n_B, extra, idx):
    return int(np.random.SeedSequence([BASE_SEED, EXP_ID, VARIANT[variant], k, n_B, extra, idx]).generate_state(1)[0])


def old_seeds(n):
    return 200 if n <= 7 else 100 if n <= 9 else 48 if n == 10 else 24 if n == 11 else 12 if n == 12 else 4


def young_seeds(n):
    return 100 if n <= 14 else 32 if n <= 18 else 12 if n <= 20 else 6


def bound_closed_form(k, n, m):
    """E T <= 1/2 sqrt( (d_R^2 - 1)(d_D^-2 - d^-2)/(1 - d^-2) )  <=  1/2 * 2^(k-m)."""
    return 0.5 * np.sqrt((4.0 ** k - 1) * (4.0 ** (-m) - 4.0 ** (-n)) / (1 - 4.0 ** (-n)))


def stats(arr):
    arr = np.asarray(arr, dtype=float)          # (seeds, m)
    ns = arr.shape[0]
    with np.errstate(invalid="ignore"):
        mean = np.nanmean(arr, 0) if np.isfinite(arr).any() else np.full(arr.shape[1], np.nan)
        sd = np.nanstd(arr, 0, ddof=1) if ns > 1 else np.zeros(arr.shape[1])
    f = lambda v: [None if not np.isfinite(x) else float(x) for x in v]
    return {"mean": f(mean), "std": f(sd), "ci95": f(1.96 * sd / np.sqrt(ns))}


def first_m(vals, cond):
    """Smallest m with cond(vals[m]).  If an uncomputed entry (None; e.g. the dense
    young-black-hole F_uhl / T_prod beyond d_R d_B' > 256) precedes the first hit,
    the threshold is censored and None is returned (never a misleading late m)."""
    for m, v in enumerate(vals):
        if v is None:
            return None
        if cond(v):
            return m
    return None


def thresholds(rec):
    k = rec["k"]
    I = rec["I_R_ED" if rec["kind"] == "old" else "I_R_D"]["mean"]
    T = rec["T_prod" if rec["kind"] == "old" else "T_mm"]["mean"]
    return {"m_I90": first_m(I, lambda v: v >= 0.9 * 2 * k * L2),
            "m_I99": first_m(I, lambda v: v >= 0.99 * 2 * k * L2),
            "m_T10": first_m(T, lambda v: v <= 0.1),
            "m_F90": first_m(rec["F_uhl"]["mean"], lambda v: v >= 0.9)}


def summarize(rec, per_seed, keys, k, info_key, t_key="T_prod"):
    for key in keys:
        rec[key] = stats([[r[key] for r in seed] for seed in per_seed])
    I = rec[info_key]["mean"]
    rec["thresholds"] = {
        "m_I90": first_m(I, lambda v: v >= 0.9 * 2 * k * L2),
        "m_I99": first_m(I, lambda v: v >= 0.99 * 2 * k * L2),
        "m_T10": first_m(rec[t_key]["mean"], lambda v: v <= 0.1),
        "m_F90": first_m(rec["F_uhl"]["mean"], lambda v: v >= 0.9),
    }
    return rec


def collect(fn, X, k, n_B, n, keys):
    """per_seed[s][m] = dict, from batched metric calls (one per m)."""
    S_ = X.shape[0]
    cols = [fn(X, k, n_B, m) for m in range(n + 1)]
    return [[{key: float(cols[m][key][s]) for key in cols[m]} for m in range(n + 1)] for s in range(S_)]


def run_old(k, n_B, ns, dev, variant="old_haar", depth=0, geometry="far"):
    import torch
    n = k + n_B
    t0 = time.time()
    per_seed, unit_err, tr_err = [], 0.0, 0.0
    chunk = max(1, min(ns, int(1.2e9 // (16 * 4 ** n))))
    for s0 in range(0, ns, chunk):
        bs = min(chunk, ns - s0)
        if variant == "old_haar":
            U = torch.stack([c.t_haar_unitary(2 ** n, seed_for(variant, k, n_B, 0, s0 + i), dev) for i in range(bs)])
        else:
            gate = "haar" if variant == "old_local_haar" else "clifford"
            rng = np.random.default_rng(np.random.SeedSequence(
                [BASE_SEED, EXP_ID, VARIANT[variant], k, n_B, depth, s0]))
            U = hp.t_brickwork_columns(n, depth, rng, gate, n, dev, batch=bs)
            if geometry == "near":   # feed the diary into the LAST k chain sites (next to where D is emitted)
                U = U.reshape(bs, 2 ** n, 2 ** n_B, 2 ** k).permute(0, 1, 3, 2).reshape(bs, 2 ** n, 2 ** n)
        if s0 == 0 and n <= 12:
            eye = torch.eye(2 ** n, dtype=U.dtype, device=U.device)
            unit_err = float((U[0].conj().T @ U[0] - eye).abs().max()); del eye
        rows = collect(hp.t_old_metrics_batch, U, k, n_B, n, OLD_KEYS)
        tr_err = max(tr_err, max(abs(r["trace"] - 1) for row in rows for r in row))
        per_seed += rows
        del U
        torch.cuda.empty_cache() if torch.cuda.is_available() else None
    rec = {"kind": "old", "variant": variant, "k": k, "n_B": n_B, "n": n, "global_qubits": 2 * n, "n_seeds": ns,
           "depth": depth, "geometry": geometry, "m": list(range(n + 1)),
           "seed_rule": ("torch.Generator seed = SeedSequence([%d, %d, variant_id, k, n_B, 0, seed_index]).generate_state(1)[0]"
                         if variant == "old_haar" else
                         "numpy default_rng(SeedSequence([%d, %d, variant_id, k, n_B, depth, chunk_start])) for the whole chunk")
                        % (BASE_SEED, EXP_ID),
           "unitarity_error_seed0": unit_err, "max_trace_error": tr_err,
           "bound_T_haar_finite_d": [hp.decoupling_bound_mm(k, n_B, m) for m in range(n + 1)],
           "bound_T_closed_form": [float(bound_closed_form(k, n, m)) for m in range(n + 1)],
           "bound_T_asymptotic": [0.5 * 2.0 ** (k - m) for m in range(n + 1)],
           "F_EPR_prediction_haar_mean_purity": [hp.yk_fidelity_prediction(k, n_B, m) for m in range(n + 1)],
           "F_EPR_prediction_large_d": [hp.yk_fidelity_large_d(k, m) for m in range(n + 1)]}
    summarize(rec, per_seed, OLD_KEYS, k, "I_R_ED")
    rec["runtime_s"] = time.time() - t0
    rec["gpu_peak_GB"] = torch.cuda.max_memory_allocated() / 1e9 if torch.cuda.is_available() else None
    print("old   %-18s k=%d n_B=%-2d d=%-2d %-4s seeds=%-3d thr=%s  T(m=k+3)=%.4f bound=%.4f  %.1fs peak %.1fGB" % (
        variant, k, n_B, depth, geometry, ns, rec["thresholds"], rec["T_prod"]["mean"][min(n, k + 3)],
        rec["bound_T_closed_form"][min(n, k + 3)], rec["runtime_s"], rec["gpu_peak_GB"] or 0), flush=True)
    return rec


def run_young(k, n_B, ns, dev):
    import torch
    n = k + n_B
    t0 = time.time()
    per_seed = []
    chunk = max(1, min(ns, int(1.0e9 // (16 * 2 ** (n + k) * 2 ** ((n + k) // 2) // 2 ** k + 1))))
    for s0 in range(0, ns, chunk):
        bs = min(chunk, ns - s0)
        V = torch.stack([hp.t_haar_isometry(2 ** n, 2 ** k, seed_for("young_haar", k, n_B, 0, s0 + i), dev) for i in range(bs)])
        per_seed += collect(hp.t_young_metrics_batch, V, k, n_B, n, YOUNG_KEYS)
        del V
        torch.cuda.empty_cache() if torch.cuda.is_available() else None
    rec = {"kind": "young", "variant": "young_haar", "k": k, "n_B": n_B, "n": n, "global_qubits": n + k, "n_seeds": ns,
           "m": list(range(n + 1)),
           "seed_rule": "torch.Generator seed = SeedSequence([%d, %d, variant_id, k, n_B, 0, seed_index]).generate_state(1)[0]" % (BASE_SEED, EXP_ID),
           "bound_T_prod_2x_mm": [2 * hp.decoupling_bound_mm(k, n_B, m, old=False) for m in range(n + 1)],
           "bound_T_mm_haar_finite_d": [hp.decoupling_bound_mm(k, n_B, m, old=False) for m in range(n + 1)],
           "bound_T_asymptotic": [0.5 * 2.0 ** (k + n_B / 2.0 - m) for m in range(n + 1)]}
    summarize(rec, per_seed, YOUNG_KEYS, k, "I_R_D", "T_mm")
    rec["runtime_s"] = time.time() - t0
    rec["gpu_peak_GB"] = torch.cuda.max_memory_allocated() / 1e9 if torch.cuda.is_available() else None
    print("young k=%d n_B=%-2d seeds=%-3d chunk=%d thr=%s  %.1fs" % (k, n_B, ns, chunk, rec["thresholds"], rec["runtime_s"]), flush=True)
    return rec


def write_part(tag, recs, complete):
    os.makedirs(PARTS, exist_ok=True)
    with open(os.path.join(PARTS, "e2_%s.json" % tag), "w") as f:
        json.dump({"records": recs, "complete": complete}, f)


def main(a):
    dev = c.get_device()
    recs = []
    if a.part == "old":
        for n_B in (3, 4, 5, 6, 7, 8, 9, 10, 11):
            for k in (1, 2, 3):
                if k + n_B <= 12:
                    recs.append(run_old(k, n_B, old_seeds(k + n_B), dev)); write_part("old", recs, False)
    elif a.part == "big":
        recs.append(run_old(1, 12, 4, dev)); write_part("big", recs, False)
        recs.append(run_old(3, 10, 4, dev))
    elif a.part == "young":
        for n_B in (4, 6, 8, 10, 12, 14, 16, 18, 20):
            for k in (1, 2, 3):
                recs.append(run_young(k, n_B, young_seeds(k + n_B), dev)); write_part("young", recs, False)
    elif a.part == "local":
        c.two_qubit_clifford_group()
        for k, n_B in ((1, 9), (2, 8)):
            for variant in ("old_local_haar", "old_local_clifford"):
                for geometry in ("far", "near"):
                    for depth in (1, 2, 3, 4, 6, 8, 10, 12, 16, 24, 32):
                        recs.append(run_old(k, n_B, 32, dev, variant, depth, geometry)); write_part("local", recs, False)
    write_part(a.part, recs, True)


DERIVATION = """Old black hole, Haar U on d = d_R d_E = d_D d_B' (d_R = 2^k, d_D = 2^m).
(1) Second-moment (Weingarten) average: E tr(rho_RB'^2) = [d_B' d_R + d_D d_E - (d_B' d_E + d_D d_R)/d]/(d^2-1).
(2) rho_R x rho_B' = 1/D exactly (D = d_R d_B'), so T := 1/2||rho_RB' - rho_R x rho_B'||_1
    <= 1/2 sqrt(D) ||rho_RB' - 1/D||_2 = 1/2 sqrt(D tr rho_RB'^2 - 1)  (Cauchy-Schwarz).
(3) Jensen: E T <= 1/2 sqrt(D E tr rho^2 - 1) = 1/2 sqrt((d_R^2-1)(d_D^-2 - d^-2)/(1-d^-2)) <= 1/2 * 2^(k-m).
(4) Uhlmann + Fuchs-van de Graaf: a decoder on E D exists with entanglement fidelity F >= (1-T)^2 >= 1 - 2T,
    so E[1-F] <= 2^(k-m): error eps needs m >= k + log2(1/eps), independent of n_B.
Young black hole (no E): the same steps give E T_mm <~ 1/2 * 2^(k + n_B/2 - m) and T_prod <= 2 T_mm,
    so m >~ n_B/2 + k + log2(1/eps): about half of the black hole must be radiated first (Page time).
This is the Hayden-Preskill (2007) decoupling argument specialised to qubits; constants here are from the purity bound."""


def merge():
    recs = []
    for p in sorted(glob.glob(os.path.join(PARTS, "e2_*.json"))):
        recs += json.load(open(p))["records"]
    for r in recs:          # recompute with the censoring-aware rule
        r["thresholds"] = thresholds(r)
    out = {"experiment": "e2_hayden_preskill", "units": "nats", "base_seed": BASE_SEED,
           "backend": "torch complex128 on CUDA (A100 40GB); spectra via Gram eigvalsh", "hp_clip": hp.HP_CLIP,
           "conventions": "A = first k qubits of the scrambler input, D = last m output qubits; thresholds are the smallest m "
                          "with seed-mean I >= 0.9 (0.99) * 2k log2, mean T <= 0.1 (T_prod for old = T_mm; T_mm for young), mean F_uhl >= 0.9",
           "derivation": DERIVATION, "records": recs}
    with open(os.path.join(ROOT, "results", "e2_hayden_preskill.json"), "w") as f:
        json.dump(out, f)
    return out


def arr(x):
    return np.array([np.nan if v is None else v for v in x], dtype=float)


def plots(out):
    import _style as st
    plt = st.setup()
    figdir = os.path.join(ROOT, "figures"); os.makedirs(figdir, exist_ok=True)
    R = out["records"]
    old = [r for r in R if r["variant"] == "old_haar"]
    young = [r for r in R if r["variant"] == "young_haar"]
    local = [r for r in R if r["variant"].startswith("old_local")]
    cm_o, cm_y = plt.get_cmap("cool"), plt.get_cmap("autumn")

    # fig 1: mutual information ------------------------------------------------
    fig, axs = plt.subplots(1, 3, figsize=(16, 4.9))
    for ax, k in zip(axs, (1, 2, 3)):
        ro = sorted([r for r in old if r["k"] == k], key=lambda r: r["n_B"])
        for i, r in enumerate(ro):
            y, e = arr(r["I_R_ED"]["mean"]) / L2, arr(r["I_R_ED"]["std"]) / L2
            ax.plot(r["m"], y, "-o", ms=2.5, lw=1, color=cm_o(i / max(1, len(ro) - 1)),
                    label="old n_B=%d" % r["n_B"] if i in (0, len(ro) - 1) else None)
            ax.fill_between(r["m"], y - e, y + e, color=cm_o(i / max(1, len(ro) - 1)), alpha=0.15, lw=0)
        ry = sorted([r for r in young if r["k"] == k], key=lambda r: r["n_B"])
        for i, r in enumerate(ry):
            y, e = arr(r["I_R_D"]["mean"]) / L2, arr(r["I_R_D"]["std"]) / L2
            ax.plot(r["m"], y, "--s", ms=2.5, lw=1, color=cm_y(0.15 + 0.8 * i / max(1, len(ry) - 1)),
                    label="young n_B=%d" % r["n_B"] if i in (0, len(ry) - 1) else None)
            ax.fill_between(r["m"], y - e, y + e, color=cm_y(0.15 + 0.8 * i / max(1, len(ry) - 1)), alpha=0.15, lw=0)
        ax.axhline(2 * k, color=st.FG, ls=":", lw=1)
        ax.set_xlim(-0.5, 23.5); ax.set_xlabel("emitted qubits m"); ax.set_title(f"k = {k} diary qubit(s);  2k = {2*k} bits = full recovery")
        ax.legend(fontsize=7, loc="center right")
    axs[0].set_ylabel("I(R : Bob's radiation)  [bits]")
    fig.suptitle("Extension 2: Hayden-Preskill. Old black hole (Bob holds E D): curves collapse for all n_B; young (Bob holds D): shift ~ n_B/2")
    st.caption(fig, "Haar scrambler on A+B, exact state vectors on an A100 (old: 2(k+n_B) qubits; young: 2k+n_B). Bands = std over seeds (4-200, see JSON). "
                    "Finite-dimensional toy model: no gravity, no islands.")
    fig.tight_layout(rect=(0, 0.04, 1, 0.94)); fig.savefig(os.path.join(figdir, "e2_mutual_information.png"), dpi=160); plt.close(fig)

    # fig 2: decoupling --------------------------------------------------------
    fig, axs = plt.subplots(1, 3, figsize=(16, 4.9))
    for ax, k in zip(axs[:2], (1, 3)):
        ro = sorted([r for r in old if r["k"] == k], key=lambda r: r["n_B"])
        for i, r in enumerate(ro):
            ax.errorbar(r["m"], np.maximum(arr(r["T_prod"]["mean"]), 1e-9), yerr=arr(r["T_prod"]["ci95"]), fmt="-o", ms=2.5, lw=1,
                        color=cm_o(i / max(1, len(ro) - 1)), label="n_B=%d (%d seeds)" % (r["n_B"], r["n_seeds"]), capsize=1.5)
        mm = np.arange(0, 14)
        ax.plot(mm, 0.5 * 2.0 ** (k - mm), "--", color=st.AMBER, lw=1.3, label="bound 1/2 * 2^(k-m)")
        ax.plot(ro[-1]["m"], np.maximum(ro[-1]["bound_T_closed_form"], 1e-9), ":", color=st.GREEN, lw=1.3, label="finite-d purity bound (largest n_B)")
        ax.set_yscale("log"); ax.set_ylim(1e-4, 2); ax.set_xlim(-0.5, 13.5)
        ax.set_xlabel("emitted qubits m"); ax.set_ylabel("T = 1/2 || rho_RB' - rho_R x rho_B' ||_1")
        ax.set_title(f"old black hole, k = {k}: decoupling of R from B'"); ax.legend(fontsize=6.5)
    ax = axs[2]
    ry = sorted([r for r in young if r["k"] == 1], key=lambda r: r["n_B"])
    for i, r in enumerate(ry):
        col = cm_y(0.15 + 0.8 * i / max(1, len(ry) - 1))
        ax.errorbar(np.array(r["m"]), np.maximum(arr(r["T_mm"]["mean"]), 1e-9), yerr=arr(r["T_mm"]["ci95"]), fmt="-s", ms=2.5, lw=1,
                    color=col, label="n_B=%d" % r["n_B"], capsize=1.5)
        ax.plot(np.array(r["m"]), arr(r["T_prod"]["mean"]), "x", ms=4, color=st.FG, alpha=0.6)
        ax.plot(r["m"], np.minimum(r["bound_T_asymptotic"], 2), ":", color=col, lw=0.8)
    ax.set_yscale("log"); ax.set_ylim(1e-4, 2)
    ax.set_xlabel("emitted qubits m"); ax.set_ylabel("T_mm = 1/2 || rho_RB' - 1/(d_R d_B') ||_1")
    ax.set_title("young black hole, k = 1 (dotted: 1/2 * 2^(k + n_B/2 - m))"); ax.legend(fontsize=6.5, ncol=2)
    st.caption(fig, "Error bars = 95% CI over seeds. Old: T exact from the spectrum of rho_RB' (rho_R x rho_B' = 1/D exactly). Young: T_mm exact from the spectrum; "
                    "white x = T_prod (dense, only where d_R d_B' <= 256). Bounds are on the Haar AVERAGE of T (purity + Jensen). Toy model.")
    fig.tight_layout(rect=(0, 0.05, 1, 1)); fig.savefig(os.path.join(figdir, "e2_decoupling.png"), dpi=160); plt.close(fig)

    # fig 3: fidelity ----------------------------------------------------------
    fig, axs = plt.subplots(1, 3, figsize=(16, 4.9))
    for ax, k in zip(axs, (1, 2, 3)):
        ro = sorted([r for r in old if r["k"] == k], key=lambda r: r["n_B"])
        for i, r in enumerate(ro):
            col = cm_o(i / max(1, len(ro) - 1))
            ax.errorbar(r["m"], arr(r["F_uhl"]["mean"]), yerr=arr(r["F_uhl"]["ci95"]), fmt="-o", ms=2.5, lw=1, color=col,
                        label="Uhlmann F(rho_RB', rho_R x rho_B')" if i == len(ro) - 1 else None, capsize=1.5)
            ax.errorbar(r["m"], arr(r["F_EPR"]["mean"]), yerr=arr(r["F_EPR"]["ci95"]), fmt="--^", ms=2.5, lw=1, color=col,
                        label="Yoshida-Kitaev F_EPR (post-selected)" if i == len(ro) - 1 else None, capsize=1.5)
        mm = np.arange(0, 14)
        ax.plot(mm, 1 / (1 + 4.0 ** (k - mm) - 4.0 ** (-mm)), ":", color=st.AMBER, lw=1.5, label="1/(1 + 4^(k-m) - 4^-m)")
        ax.plot(mm, np.clip(1 - 2.0 ** (k - mm), 0, 1), "-.", color=st.GREEN, lw=1, label="guarantee 1 - 2^(k-m)")
        ax.set_xlim(-0.5, 13.5); ax.set_ylim(0, 1.03); ax.set_xlabel("emitted qubits m"); ax.set_title(f"old black hole, k = {k} (colour = n_B)")
        ax.legend(fontsize=6.5, loc="lower right")
    axs[0].set_ylabel("recovery fidelity")
    st.caption(fig, "Uhlmann fidelity = lower bound on the optimal decoder's entanglement fidelity; F_EPR = fidelity of the Yoshida-Kitaev probabilistic decoder after "
                    "successful post-selection (success prob. P_EPR = 4^-k / F_EPR). Error bars = 95% CI over seeds. Toy model.")
    fig.tight_layout(rect=(0, 0.05, 1, 1)); fig.savefig(os.path.join(figdir, "e2_fidelity.png"), dpi=160); plt.close(fig)

    # fig 4: thresholds --------------------------------------------------------
    fig, axs = plt.subplots(1, 2, figsize=(12.5, 4.9))
    for ax, key, title in ((axs[0], "m_I90", "smallest m with <I> >= 0.9 * 2k bits"),
                           (axs[1], "m_T10", "smallest m with <T> <= 0.1")):
        for k, col in ((1, st.CYAN), (2, st.AMBER), (3, st.MAGENTA)):
            ro = sorted([r for r in old if r["k"] == k], key=lambda r: r["n_B"])
            ax.plot([r["n_B"] for r in ro], [r["thresholds"][key] if r["thresholds"][key] is not None else np.nan for r in ro],
                    "-o", color=col, label=f"old, k={k}")
            ry = sorted([r for r in young if r["k"] == k], key=lambda r: r["n_B"])
            ax.plot([r["n_B"] for r in ry], [r["thresholds"][key] if r["thresholds"][key] is not None else np.nan for r in ry],
                    "--s", color=col, label=f"young, k={k}")
        xs = np.array([4, 20])
        ax.plot(xs, xs / 2, ":", color=st.GREY, lw=1, label="n_B / 2")
        ax.set_xlabel("black hole size n_B [qubits]"); ax.set_ylabel("recovery threshold m* [qubits]"); ax.set_title(title); ax.legend(fontsize=7)
    st.caption(fig, "Thresholds read from seed-mean curves at integer m (so they are integers; no error bar). Old: independent of n_B (m* ~ k + const). "
                    "Young: m* ~ n_B/2 + k + const (Page time). Right panel uses T_mm for the young black hole. Toy model.")
    fig.tight_layout(rect=(0, 0.05, 1, 1)); fig.savefig(os.path.join(figdir, "e2_thresholds.png"), dpi=160); plt.close(fig)

    # fig 5: local circuits ----------------------------------------------------
    if local:
        fig, axs = plt.subplots(1, 2, figsize=(12.5, 4.9))
        for ax, k in zip(axs, (1, 2)):
            rk = [r for r in local if r["k"] == k]
            if not rk:
                continue
            n = rk[0]["n"]; m_show = k + 4
            for variant, geometry, col, ls in (("old_local_haar", "far", st.CYAN, "-o"), ("old_local_haar", "near", st.GREEN, "-s"),
                                               ("old_local_clifford", "far", st.AMBER, "--o"), ("old_local_clifford", "near", st.MAGENTA, "--s")):
                rs = sorted([r for r in rk if r["variant"] == variant and r["geometry"] == geometry], key=lambda r: r["depth"])
                y = np.array([r["I_R_ED"]["mean"][m_show] for r in rs]) / L2
                e = np.array([r["I_R_ED"]["ci95"][m_show] for r in rs]) / L2
                ax.errorbar([r["depth"] for r in rs], y, yerr=e, fmt=ls, ms=3.5, color=col, capsize=2,
                            label="%s gates, diary %s the emitted end" % (variant.split("_")[-1], "far from" if geometry == "far" else "next to"))
            ho = next((r for r in old if r["k"] == k and r["n"] == n), None)
            if ho:
                ax.axhline(ho["I_R_ED"]["mean"][m_show] / L2, color=st.FG, ls=":", lw=1, label="Haar on all n qubits")
            ax.axvline(n, color=st.GREY, ls="--", lw=0.8)
            ax.set_xscale("log", base=2); ax.set_xlabel("brickwork depth [layers]"); ax.set_ylabel(f"I(R : E D) at m = k+4 = {m_show}  [bits]")
            ax.set_title(f"old BH, local scrambler: k={k}, n_B={n-k} (dashed: depth = n = {n})", fontsize=10); ax.legend(fontsize=7)
        st.caption(fig, "Open-chain brickwork of 2-qubit gates on the n = k+n_B qubits; D = last m sites. Error bars = 95% CI over 32 seeds. "
                        "Recovery needs the diary's light cone to reach the emitted qubits (depth ~ distance). Toy model, 1D locality is an assumption.")
        fig.tight_layout(rect=(0, 0.05, 1, 1)); fig.savefig(os.path.join(figdir, "e2_local_scrambler.png"), dpi=160); plt.close(fig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", default="old")
    ap.add_argument("--plot", action="store_true")
    a = ap.parse_args()
    for k, n, m in ((1, 5, 2), (2, 9, 4), (3, 12, 0), (3, 12, 12)):   # closed form == Weingarten-based bound
        assert abs(bound_closed_form(k, n, m) - hp.decoupling_bound_mm(k, n - k, m)) < 1e-9
    if a.plot:
        o = merge(); plots(o)
        for r in o["records"]:
            print(r["variant"], "k=%d n_B=%d d=%s %s seeds=%d" % (r["k"], r["n_B"], r.get("depth"), r.get("geometry", ""), r["n_seeds"]), r["thresholds"])
    else:
        main(a)
