"""Problem C: sequential evaporation of an N-qubit toy black hole with Haar scrambling.

Protocol (exact state-vector simulation, complex128, GPU)
---------------------------------------------------------
Initial state: |0>^{(x)N} on the black hole B (pure product state), radiation R empty.
Step t = 1..N:
  1. apply a fresh Haar-random unitary U_t to the REMAINING black-hole qubits
     (dimension 2^(N-t+1)); the radiation is not touched:  |psi> -> (I_R (x) U_t)|psi>;
  2. move the first remaining black-hole qubit to the radiation.
After step t: dim R = 2^t, dim B = 2^(N-t).  Recorded per step: emitted count, dims,
S(R), S(B), purity and Renyi-2 of rho_R, largest eigenvalue, entanglement spectrum.

Two samplers of step 1 (statistically identical, verified numerically in `ks`):
  --mode full      literal: draw the full 2^(N-t+1)-dim Haar unitary (QR + phase fix).
                   Memory 16 * 4^N bytes for U_1 alone  ->  N <= 14 on a 40 GB A100.
  --mode isometry  exact-in-distribution shortcut: the state has Schmidt rank r <= dim R, so
                   only the action of U_t on the r-dim support V of rho_B matters, and U_t V
                   is a Haar-random isometry (invariance of Haar measure).  Draw it directly
                   by reduced QR of a d x r Ginibre matrix.  Memory O(2^N)  ->  N up to ~28.

Sub-commands:  run | ks | variants | plot      (see README)
"""
import argparse
import glob
import json
import math
import os
import time

from _common import DEVICE, FIGURES, RESULTS, dump, env_info, log, np, sync, torch

from eh import entropy as E
from eh import page as P
from eh import qstates as Q

BOTH_SIDES_MAX = 2048  # compute S(B) from an independent eigvalsh of rho_B when dims allow


def spectra(psi, both_sides=True):
    """Schmidt probabilities (descending, smaller side) and independently computed S(B)."""
    a, d = psi.shape
    p = Q.schmidt_probs_t(psi)  # Gram on the smaller side
    sR_side_is_small = a <= d
    sB = None
    if both_sides and max(a, d) <= BOTH_SIDES_MAX:
        big = (psi.conj().T @ psi) if sR_side_is_small else (psi @ psi.conj().T)
        pb = torch.linalg.eigvalsh(big).clamp_min(0.0)
        pb = pb / pb.sum()
        other = E.von_neumann(pb).item()
        mine = E.von_neumann(p).item()
        # p came from rho_R if a<=d else from rho_B
        sR, sB = (mine, other) if sR_side_is_small else (other, mine)
    else:
        sR = sB = E.von_neumann(p).item()  # nonzero spectra coincide (Schmidt); not independent
    return torch.flip(p, dims=(-1,)), sR, sB


def scramble(psi, gen, mode):
    """(I_R (x) U)|psi> with U Haar on B.  psi is the (dim R) x (dim B) coefficient matrix."""
    a, d = psi.shape
    if mode == "full" or a >= d:
        u = Q.haar_unitary_t(d, gen)
        out = psi @ u.T
        del u
        return out
    # psi = R'^T Q'^T with Q' (d x a) an orthonormal basis of the support in B (QR of psi^T);
    # (I (x) U) psi = R'^T (U Q')^T and W = U Q' is a Haar isometry independent of Q'.
    q, r = torch.linalg.qr(psi.T, mode="reduced")
    del q
    w = Q.haar_isometry_t(d, a, gen)
    out = r.T @ w.T
    del w
    return out


def trajectory(N, gen, mode="isometry", order="scramble_then_emit", pre_pairs=0, keep_spec=True, both_sides=True):
    """One evaporation run.  Returns list of per-step records.

    pre_pairs > 0 (variant): the radiation initially holds `pre_pairs` qubits that are
    maximally entangled (Bell pairs) with `pre_pairs` of the N black-hole qubits.
    order = "emit_then_scramble" (variant): move the qubit first, scramble afterwards.
    """
    dev = gen.device
    a0 = 2**pre_pairs
    psi = torch.zeros((a0, 2**N), dtype=torch.complex128, device=dev)
    for i in range(a0):  # sum_i |i>_R |i>_{first pre_pairs BH qubits} |0...0>
        psi[i, i * 2 ** (N - pre_pairs)] = 1.0 / math.sqrt(a0)
    recs = []
    for t in range(1, N + 1):
        a, d = psi.shape
        if order == "scramble_then_emit":
            psi = scramble(psi, gen, mode)
            psi = psi.reshape(a * 2, d // 2)
        else:
            psi = psi.reshape(a * 2, d // 2)
            psi = scramble(psi, gen, mode)
        nrm = torch.linalg.vector_norm(psi).item()
        psi = psi / nrm
        p, sR, sB = spectra(psi, both_sides)
        rec = {"t": t, "emitted": t, "dimR": psi.shape[0], "dimB": psi.shape[1], "S_R": sR, "S_B": sB,
               "purity_R": E.purity(p).item(), "renyi2_R": E.renyi2(p).item(), "lambda_max": p[0].item(),
               "norm_drift": abs(nrm - 1.0)}
        if pre_pairs:
            m = psi.reshape(a0, -1)  # early radiation R0 | everything else
            rec["purity_R0"] = E.purity(Q.schmidt_probs_t(m)).item()
        if keep_spec:
            rec["spectrum"] = p.cpu().numpy()
        recs.append(rec)
    return recs


def default_seeds(N, mode):
    if mode == "full":
        return {6: 200, 7: 200, 8: 200, 9: 200, 10: 100, 11: 40, 12: 20, 13: 6, 14: 2}.get(N, 1)
    if N <= 12:
        return 200
    return {13: 100, 14: 100, 15: 60, 16: 40, 17: 30, 18: 20, 19: 16, 20: 12, 21: 8, 22: 6, 23: 4, 24: 3}.get(N, 1)


def run(args):
    for N in args.Ns:
        ns = args.seeds or default_seeds(N, args.mode)
        base = 3000 + 100 * N + (0 if args.mode == "full" else 50_000)
        if DEVICE.type == "cuda":
            # GPU 0 may be shared with other jobs of this project: wait (politely) for enough free memory.
            need = (3.5 * 16 * 4**N if args.mode == "full" else 12 * 16 * 2**N) + 0.7 * 2**30
            waited = 0
            while torch.cuda.mem_get_info()[0] < need and waited < args.wait * 60:
                if waited % 300 == 0:
                    log(f"N={N}: waiting for {need / 2**30:.1f} GiB free on GPU (free {torch.cuda.mem_get_info()[0] / 2**30:.1f})")
                time.sleep(20); waited += 20
            torch.cuda.reset_peak_memory_stats()
        keys = ["S_R", "S_B", "purity_R", "renyi2_R", "lambda_max", "norm_drift"]
        arr = {k: np.zeros((ns, N)) for k in keys}
        specs, walls = [], []
        oom = None
        for s in range(ns):
            gen = Q.torch_generator(base + s, DEVICE)
            sync(); t0 = time.time()
            try:
                recs = trajectory(N, gen, args.mode, keep_spec=(N <= 12 or s < 3))
            except torch.OutOfMemoryError as e:  # GPU shared with other jobs: stop cleanly, keep what we have
                oom = str(e)[:300]
                log(f"OOM at N={N} mode={args.mode} seed index {s}: {oom}")
                torch.cuda.empty_cache()
                break
            sync(); walls.append(time.time() - t0)
            for k in keys:
                arr[k][s] = [r[k] for r in recs]
            if "spectrum" in recs[0]:
                specs.append([r["spectrum"] for r in recs])
        done = len(walls)
        if done == 0:
            dump(f"c_oom_{args.mode}_N{N}.json", {"N": N, "mode": args.mode, "error": oom, "env": env_info(),
                                                  "note": "no trajectory completed; GPU 0 was shared with other jobs at the time"})
            continue
        if done < ns:
            arr = {k: v[:done] for k, v in arr.items()}
            ns = done
        peak = torch.cuda.max_memory_allocated() / 2**30 if DEVICE.type == "cuda" else float("nan")
        page = np.array([P.page_entropy(2**t, 2 ** (N - t)) for t in range(1, N + 1)])
        mean, std = arr["S_R"].mean(0), arr["S_R"].std(0, ddof=1) if ns > 1 else np.zeros(N)
        se = std / math.sqrt(ns)
        z = np.zeros(N); z[:-1] = (mean[:-1] - page[:-1]) / np.where(se[:-1] > 0, se[:-1], np.inf)
        pur_exact = np.array([(2**t + 2 ** (N - t)) / (2**N + 1.0) for t in range(1, N + 1)])
        out = {
            "problem": "C", "N": N, "mode": args.mode, "seeds": ns, "seed_rule": f"torch.Generator({DEVICE.type}).manual_seed({base} + s), s=0..{ns - 1}",
            "initial_state": "|0>^N on B, R empty", "env": env_info(), "clip": E.CLIP,
            "t": list(range(1, N + 1)), "dimR": [2**t for t in range(1, N + 1)], "dimB": [2 ** (N - t) for t in range(1, N + 1)],
            "S_R_mean": mean.tolist(), "S_R_std": std.tolist(), "S_R_stderr": se.tolist(),
            "S_R_q05": np.quantile(arr["S_R"], 0.05, axis=0).tolist(), "S_R_q95": np.quantile(arr["S_R"], 0.95, axis=0).tolist(),
            "S_R_min": arr["S_R"].min(0).tolist(), "S_R_max": arr["S_R"].max(0).tolist(),
            "S_B_mean": arr["S_B"].mean(0).tolist(), "page": page.tolist(), "z_vs_page": z.tolist(),
            "max_abs_z": float(np.abs(z).max()), "max_abs_dev_nats": float(np.abs(mean - page).max()),
            "max_abs_SR_minus_SB": float(np.abs(arr["S_R"] - arr["S_B"]).max()),
            "SB_independent": bool(2 ** (N - 1) <= BOTH_SIDES_MAX),
            "purity_mean": arr["purity_R"].mean(0).tolist(), "purity_haar_exact": pur_exact.tolist(),
            "renyi2_mean": arr["renyi2_R"].mean(0).tolist(), "lambda_max_mean": arr["lambda_max"].mean(0).tolist(),
            "max_norm_drift": float(arr["norm_drift"].max()),
            "wall_s_per_seed_mean": float(np.mean(walls)), "wall_s_per_seed_min": float(np.min(walls)), "peak_gpu_mem_GiB": peak,
            "state_bytes": 16 * 2**N, "full_unitary_bytes_step1": 16 * 4**N,
        }
        out["device"] = str(DEVICE); out["oom_stopped_early"] = oom
        dump(f"c_evap_{args.mode}_N{N}.json", out)
        if specs:
            np.savez_compressed(os.path.join(RESULTS, f"c_evap_{args.mode}_N{N}_spectra.npz"),
                                **{f"seed{i}_t{t + 1}": sp for i, traj in enumerate(specs) for t, sp in enumerate(traj)},
                                S_R=arr["S_R"])
        else:
            np.savez_compressed(os.path.join(RESULTS, f"c_evap_{args.mode}_N{N}_spectra.npz"), S_R=arr["S_R"])
        log(f"mode={args.mode} N={N} seeds={ns} wall/seed={np.mean(walls):.2f}s peak={peak:.2f}GiB max|z|={out['max_abs_z']:.2f} "
            f"max|dev|={out['max_abs_dev_nats']:.2e} max|SR-SB|={out['max_abs_SR_minus_SB']:.1e}")


def _stats(recs_list, key):
    return np.array([[r[key] for r in recs] for recs in recs_list])


def ks(args):
    """Is the state after each step distributed like a Haar state on R (x) B?  Spectrum statistics."""
    from scipy.stats import ks_2samp

    N, ns = args.N, args.seeds or 1500
    out = {"problem": "C-ks", "N": N, "samples_isometry": ns, "env": env_info(),
           "seed_rule": "sequential isometry: 700000+s; sequential full: 710000+s; direct Haar reference: generator 720000; second Haar reference (null check): 730000"}
    seq = [trajectory(N, Q.torch_generator(700000 + s, DEVICE), "isometry", keep_spec=False, both_sides=False) for s in range(ns)]
    nfull = min(ns, args.full_seeds)
    full = [trajectory(N, Q.torch_generator(710000 + s, DEVICE), "full", keep_spec=False, both_sides=False) for s in range(nfull)]
    out["samples_full"] = nfull

    def direct(seed):
        gen = Q.torch_generator(seed, DEVICE)
        psi = Q.haar_states_t(ns, 2**N, gen)
        S = np.zeros((ns, N)); L = np.zeros((ns, N))
        for t in range(1, N + 1):
            p = Q.schmidt_probs_t(psi.reshape(ns, 2**t, 2 ** (N - t)))
            S[:, t - 1] = E.von_neumann(p).cpu().numpy(); L[:, t - 1] = p[:, -1].cpu().numpy()
        return S, L

    Sd, Ld = direct(720000)
    Sd2, Ld2 = direct(730000)
    Ss, Ls = _stats(seq, "S_R"), _stats(seq, "lambda_max")
    Sf, Lf = _stats(full, "S_R"), _stats(full, "lambda_max")
    rows = []
    for t in range(1, N):
        i = t - 1
        rows.append({
            "t": t, "dimR": 2**t, "dimB": 2 ** (N - t), "page": P.page_entropy(2**t, 2 ** (N - t)),
            "seq_mean_S": float(Ss[:, i].mean()), "seq_std_S": float(Ss[:, i].std(ddof=1)),
            "haar_mean_S": float(Sd[:, i].mean()), "haar_std_S": float(Sd[:, i].std(ddof=1)),
            "p_S_seq_vs_haar": float(ks_2samp(Ss[:, i], Sd[:, i]).pvalue),
            "p_lmax_seq_vs_haar": float(ks_2samp(Ls[:, i], Ld[:, i]).pvalue),
            "p_S_full_vs_haar": float(ks_2samp(Sf[:, i], Sd[:, i]).pvalue),
            "p_lmax_full_vs_haar": float(ks_2samp(Lf[:, i], Ld[:, i]).pvalue),
            "p_S_full_vs_isometry": float(ks_2samp(Sf[:, i], Ss[:, i]).pvalue),
            "p_S_haar_vs_haar_null": float(ks_2samp(Sd2[:, i], Sd[:, i]).pvalue),
        })
    out["per_step"] = rows
    # joint (trajectory) statistics: correlation of S between consecutive steps; increments S_{t+1}-S_t
    def corr(S):
        return [float(np.corrcoef(S[:, i], S[:, i + 1])[0, 1]) for i in range(N - 2)]

    out["corr_consecutive_seq"] = corr(Ss)
    out["corr_consecutive_single_haar_state_nested_cuts"] = corr(Sd)
    out["corr_consecutive_full"] = corr(Sf)
    out["p_increment_seq_vs_nested"] = [float(ks_2samp(Ss[:, i + 1] - Ss[:, i], Sd[:, i + 1] - Sd[:, i]).pvalue) for i in range(N - 2)]
    # Fisher-z comparison of the correlations
    zc = []
    for a_, b_ in zip(out["corr_consecutive_seq"], out["corr_consecutive_single_haar_state_nested_cuts"]):
        zc.append(float((np.arctanh(a_) - np.arctanh(b_)) / math.sqrt(2.0 / (ns - 3))))
    out["corr_diff_fisher_z"] = zc
    allp = [r[k] for r in rows for k in r if k.startswith("p_") and "null" not in k] + out["p_increment_seq_vs_nested"]
    out["n_tests"] = len(allp); out["min_p"] = float(min(allp)); out["bonferroni_min_p"] = float(min(1.0, min(allp) * len(allp)))
    out["distribution_arrays"] = {"S_seq": Ss.tolist(), "S_haar": Sd.tolist()} if N <= 10 and ns <= 2000 else None
    dump(f"c_ks_N{N}.json", out)
    log(f"KS N={N}: tests={len(allp)} min p={out['min_p']:.3g} (Bonferroni {out['bonferroni_min_p']:.3g}); max |Fisher z| corr={np.abs(zc).max():.2f}")


def variants(args):
    """Protocols / initial states for which the sequential ensemble is NOT Haar on R (x) B."""
    from scipy.stats import ks_2samp

    N, ns = args.N, args.seeds or 1000
    out = {"problem": "C-variants", "N": N, "samples": ns, "env": env_info(),
           "seed_rule": "emit_then_scramble: 800000+s; pre_pairs: 810000+s; Haar reference generator 820000"}
    # (V1) emit first, scramble afterwards, from a product state: R never entangles.
    v1 = [trajectory(N, Q.torch_generator(800000 + s, DEVICE), "isometry", order="emit_then_scramble", keep_spec=False, both_sides=False) for s in range(ns)]
    S1 = _stats(v1, "S_R")
    se1 = S1.std(0, ddof=1) / math.sqrt(ns)
    pN = np.array([P.page_entropy(2**t, 2 ** (N - t)) for t in range(1, N + 1)])
    # prediction: first emitted qubit is |0> (unentangled); afterwards the standard protocol on N-1 qubits
    pShift = np.array([P.page_entropy(2 ** (t - 1), 2 ** (N - t)) for t in range(1, N + 1)])
    with np.errstate(divide="ignore", invalid="ignore"):
        zN = np.where(se1 > 0, (S1.mean(0) - pN) / se1, 0.0); zS = np.where(se1 > 0, (S1.mean(0) - pShift) / se1, 0.0)
    out["V1_emit_then_scramble"] = {"seeds": ns, "S_R_mean": S1.mean(0).tolist(), "S_R_stderr": se1.tolist(),
                                    "page_N_qubits_t_emitted": pN.tolist(), "page_Nminus1_qubits_tminus1_emitted": pShift.tolist(),
                                    "z_vs_page_N": zN.tolist(), "z_vs_shifted_page": zS.tolist(),
                                    "max_S_R_step1_nats": float(np.abs(S1[:, 0]).max())}
    # (V2) old black hole: r0 radiation qubits initially in Bell pairs with r0 of the N BH qubits.
    r0 = args.pre_pairs
    v2 = [trajectory(N, Q.torch_generator(810000 + s, DEVICE), "isometry", pre_pairs=r0, keep_spec=False, both_sides=False) for s in range(ns)]
    S2, L2, PR0 = _stats(v2, "S_R"), _stats(v2, "lambda_max"), _stats(v2, "purity_R0")
    gen = Q.torch_generator(820000, DEVICE)
    tot = N + r0
    psi = Q.haar_states_t(ns, 2**tot, gen)
    rows = []
    pur0_haar = E.purity(Q.schmidt_probs_t(psi.reshape(ns, 2**r0, 2**N))).cpu().numpy()
    for t in range(1, N + 1):
        dR, dB = 2 ** (r0 + t), 2 ** (N - t)
        p = Q.schmidt_probs_t(psi.reshape(ns, dR, dB))
        Sh = E.von_neumann(p).cpu().numpy(); Lh = p[:, -1].cpu().numpy()
        page = P.page_entropy(dR, dB)
        se = S2[:, t - 1].std(ddof=1) / math.sqrt(ns)
        rows.append({"t": t, "dimR": dR, "dimB": dB, "page": page, "seq_mean_S": float(S2[:, t - 1].mean()), "seq_stderr": float(se),
                     "seq_std_S": float(S2[:, t - 1].std(ddof=1)), "haar_std_S": float(Sh.std(ddof=1)),
                     "z_vs_page": float((S2[:, t - 1].mean() - page) / se) if se > 0 else 0.0,
                     "p_S_vs_haar": float(ks_2samp(S2[:, t - 1], Sh).pvalue), "p_lmax_vs_haar": float(ks_2samp(L2[:, t - 1], Lh).pvalue),
                     "purity_R0_seq_mean": float(PR0[:, t - 1].mean()), "purity_R0_seq_max_dev_from_flat": float(np.abs(PR0[:, t - 1] - 2.0**-r0).max())})
    out["V2_pre_entangled"] = {"pre_pairs": r0, "total_qubits": tot, "per_step": rows,
                               "purity_R0_haar_mean": float(pur0_haar.mean()), "purity_R0_haar_min": float(pur0_haar.min()),
                               "purity_R0_flat": 2.0**-r0,
                               "purity_R0_haar_exact_mean": (2**r0 + 2**N) / (2**tot + 1.0)}
    dump(f"c_variants_N{N}.json", out)
    log(f"variants N={N}: V1 max|z| vs Page_N={np.abs(zN[:-1]).max():.1f}, vs shifted Page={np.abs(zS).max():.2f}; "
        f"V2 max|z vs Page|={max(abs(r['z_vs_page']) for r in rows):.1f}, min KS p={min(min(r['p_S_vs_haar'], r['p_lmax_vs_haar']) for r in rows):.2e}")


def plot(args):
    from eh.plotting import AMBER, CYAN, FG, GREEN, MAGENTA, PALETTE, apply_theme, save

    plt = apply_theme()
    runs = {}
    for f in glob.glob(os.path.join(RESULTS, "c_evap_*_N*.json")):
        r = json.load(open(f)); runs[(r["mode"], r["N"])] = r
    fig, ax = plt.subplots(2, 3, figsize=(17, 9.5))
    # (a) trajectories
    showN = [n for n in (8, 12, 16, 20, 24, 26, 28) if ("isometry", n) in runs]
    for i, N in enumerate(showN):
        r = runs[("isometry", N)]; c = PALETTE[i % len(PALETTE)]; t = np.array([0] + r["t"])
        m = np.array([0] + r["S_R_mean"]); s = np.array([0] + r["S_R_std"])
        ax[0, 0].fill_between(t, m - s, m + s, color=c, alpha=0.3)
        ax[0, 0].plot(t, [0] + r["page"], "-", color=c, lw=1.1)
        ax[0, 0].plot(t, m, "o", ms=3.5, color=c, label=f"N={N} ({r['seeds']} seeds)")
    ax[0, 0].plot([], [], "-", color=FG, lw=1.1, label="Page formula (lines)")
    ax[0, 0].set_xlabel("emitted qubits t"); ax[0, 0].set_ylabel("S(R)  [nats]")
    ax[0, 0].set_title("Sequential Haar evaporation: mean S(R) (band ±1 std over seeds)"); ax[0, 0].legend(fontsize=7)
    # (b) z-scores vs page for all runs
    for mode, c, mk in (("isometry", CYAN, "o"), ("full", AMBER, "s")):
        xs, zs = [], []
        for (md, N), r in sorted(runs.items()):
            if md == mode and r["seeds"] >= 8:
                xs += [N + (t / N - 0.5) * 0.7 for t in r["t"][:-1]]; zs += r["z_vs_page"][:-1]
        ax[0, 1].scatter(xs, zs, s=9, color=c, marker=mk, label=f"mode={mode} (runs with >= 8 seeds)")
    for y in (-2, 2):
        ax[0, 1].axhline(y, color=FG, ls="--", lw=0.7)
    for y in (-4, 4):
        ax[0, 1].axhline(y, color=MAGENTA, ls=":", lw=0.7)
    ax[0, 1].set_xlabel("N  [qubits]  (points spread by step t within each N)"); ax[0, 1].set_ylabel("z = (mean S(R) - Page) / stderr")
    ax[0, 1].set_title("Deviation from Page's formula, every step"); ax[0, 1].legend(fontsize=7)
    # (c) distribution: std of S(R) vs Haar, from KS file
    ksf = sorted(glob.glob(os.path.join(RESULTS, "c_ks_N*.json")), key=lambda f: int(os.path.basename(f)[6:-5]))
    if ksf:  # largest N (numeric sort)
        k = json.load(open(ksf[-1])); rows = k["per_step"]; t = [r["t"] for r in rows]
        ax[0, 2].plot(t, [r["haar_std_S"] for r in rows], "-", color=AMBER, label="direct Haar states: std of S(R)")
        ax[0, 2].plot(t, [r["seq_std_S"] for r in rows], "o", color=CYAN, label="sequential evaporation: std of S(R)")
        ax[0, 2].set_yscale("log"); ax[0, 2].set_xlabel("emitted qubits t"); ax[0, 2].set_ylabel("std of S(R) over samples  [nats]")
        ax2 = ax[0, 2].twinx(); ax2.grid(False)
        ax2.plot(t, [r["p_S_seq_vs_haar"] for r in rows], "x", color=GREEN, label="KS p (S)")
        ax2.plot(t, [r["p_lmax_seq_vs_haar"] for r in rows], "+", color=MAGENTA, label="KS p (lambda_max)")
        ax2.set_ylim(0, 1.05); ax2.set_ylabel("two-sample KS p-value")
        ax[0, 2].set_title(f"Distribution test N={k['N']}, {k['samples_isometry']} samples: min p={k['min_p']:.2g} over {k['n_tests']} tests")
        ax[0, 2].legend(fontsize=6.5, loc="upper left"); ax2.legend(fontsize=6.5, loc="upper right")
        if k.get("distribution_arrays"):
            Ss = np.array(k["distribution_arrays"]["S_seq"]); Sd = np.array(k["distribution_arrays"]["S_haar"]); tm = k["N"] // 2
            lo = min(Ss[:, tm - 1].min(), Sd[:, tm - 1].min()); hi = max(Ss[:, tm - 1].max(), Sd[:, tm - 1].max())
            bins = np.linspace(lo, hi, 40)
            ax[1, 2].hist(Sd[:, tm - 1], bins=bins, color=AMBER, alpha=0.6, density=True, label="direct Haar states")
            ax[1, 2].hist(Ss[:, tm - 1], bins=bins, color=CYAN, alpha=0.6, density=True, label="sequential evaporation")
            ax[1, 2].axvline(P.page_entropy(2**tm, 2 ** (k["N"] - tm)), color=FG, ls="--", lw=1, label="Page mean")
            ax[1, 2].set_xlabel(f"S(R) at the Page time t={tm}, N={k['N']}  [nats]"); ax[1, 2].set_ylabel("probability density  [1/nat]")
            ax[1, 2].set_title("Full distribution at the Page time"); ax[1, 2].legend(fontsize=7)
    # (d) runtime / memory scaling
    for mode, c, mk in (("isometry", CYAN, "o"), ("full", AMBER, "s")):
        Ns = sorted(N for (md, N) in runs if md == mode)
        if not Ns:
            continue
        for dev, fill in (("cuda", c), ("cpu", "none")):
            sel = [N for N in Ns if str(runs[(mode, N)].get("device", "cpu")).startswith(dev)]
            if sel:
                ax[1, 0].plot(sel, [runs[(mode, N)]["wall_s_per_seed_min"] for N in sel], mk + ("-" if dev == "cuda" else ":"), color=c, mfc=fill, ms=5,
                              label=f"{mode}, {'A100 GPU' if dev == 'cuda' else 'CPU (4 threads, shared box)'}: best wall time / trajectory")
        ax[1, 1].plot(Ns, [runs[(mode, N)]["peak_gpu_mem_GiB"] for N in Ns], mk + "-", color=c, ms=4, label=f"{mode}: peak GPU memory")
    nn = np.arange(6, 30)
    ax[1, 1].plot(nn, 16 * 4.0**nn / 2**30, ":", color=AMBER, lw=1, label="16·4^N bytes (one full unitary)")
    ax[1, 1].plot(nn, 16 * 2.0**nn / 2**30, ":", color=CYAN, lw=1, label="16·2^N bytes (state vector)")
    ax[1, 1].axhline(40, color=MAGENTA, ls="--", lw=0.8, label="A100 40 GB")
    for a_, yl in ((ax[1, 0], "wall time per trajectory  [s]"), (ax[1, 1], "peak GPU memory  [GiB]")):
        a_.set_yscale("log"); a_.set_xlabel("N  [qubits]"); a_.set_ylabel(yl); a_.legend(fontsize=7)
    ax[1, 1].set_ylim(1e-4, 1e3)
    ax[1, 0].set_title("Runtime per trajectory (complex128; filled = A100, hollow = CPU)"); ax[1, 1].set_title("Memory scaling")
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    save(fig, os.path.join(FIGURES, "c_evaporation.png"),
         "Assumptions: N-qubit toy black hole, initial state |0>^N, fresh Haar unitary on the remaining BH qubits before each 1-qubit emission, radiation never acted on; exact state vectors; nats; finite-dimensional toy model, no gravity.")
    # summary json
    summ = {"runs": [{k: r[k] for k in ("mode", "N", "seeds", "max_abs_z", "max_abs_dev_nats", "max_abs_SR_minus_SB", "SB_independent",
                                         "wall_s_per_seed_mean", "wall_s_per_seed_min", "peak_gpu_mem_GiB", "max_norm_drift", "device")}
                     for _, r in sorted(runs.items())]}
    for mode in ("isometry", "full"):
        Ns = sorted(N for (md, N) in runs if md == mode and N >= 10 and str(runs[(md, N)].get("device")).startswith("cuda"))
        if len(Ns) >= 2:  # GPU runs only (CPU timings were taken on a shared, loaded box and are not comparable)
            w = [math.log2(runs[(mode, N)]["wall_s_per_seed_min"]) for N in Ns]
            summ[f"runtime_log2_slope_per_qubit_{mode}_gpu"] = {"Ns": Ns, "wall_s": [runs[(mode, N)]["wall_s_per_seed_min"] for N in Ns],
                                                                "slope": float(np.polyfit(Ns, w, 1)[0]), "note": "few points, shared GPU: indicative only"}
    summ["note_z"] = "z uses the sample stderr; steps within one N are correlated (nested cuts of one state); runs with < 8 seeds are excluded from the pooled z statistics because their stderr estimate is unreliable"
    zs = np.array([z for (md, N), r in runs.items() if r["seeds"] >= 8 for z in r["z_vs_page"][:-1]])
    summ["z_all_runs_ge8_seeds"] = {"n": int(len(zs)), "max_abs": float(np.abs(zs).max()), "rms": float(np.sqrt((zs**2).mean())),
                                    "frac_gt_2": float((np.abs(zs) > 2).mean())}
    rc = os.path.join(RESULTS, "c_recheck_full_N13.json")
    if os.path.exists(rc):  # follow-up of the one |z| > 4 cell (full mode, N=13, t=2, 40 seeds); see c_recheck_full13.py
        blocks = json.load(open(rc))["blocks"]
        summ["recheck_full_N13"] = {k: {"n": b["n"], "z_t2": b["z"][1], "std_t2": b["std"][1], "max_abs_z": b["max_abs_z"]} for k, b in blocks.items()}
        summ["recheck_full_N13"]["note"] = ("same seed rule 4300+s; the first 40 seeds reproduce z=4.19 at t=2 bit-for-bit, 1000 seeds give |z| <= 1.7 at every step: "
                                            "a small-sample fluctuation (skewed S distribution, sample std underestimated), not a bias")
    dump("c_summary.json", summ)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run"); r.add_argument("--mode", default="isometry", choices=["isometry", "full"])
    r.add_argument("--Ns", type=int, nargs="+", required=True); r.add_argument("--seeds", type=int, default=0)
    r.add_argument("--wait", type=float, default=45.0, help="max minutes to wait for free GPU memory")
    k = sub.add_parser("ks"); k.add_argument("--N", type=int, default=10); k.add_argument("--seeds", type=int, default=0)
    k.add_argument("--full-seeds", dest="full_seeds", type=int, default=400)
    v = sub.add_parser("variants"); v.add_argument("--N", type=int, default=6); v.add_argument("--seeds", type=int, default=0)
    v.add_argument("--pre-pairs", dest="pre_pairs", type=int, default=2)
    sub.add_parser("plot")
    a = ap.parse_args()
    {"run": run, "ks": ks, "variants": variants, "plot": plot}[a.cmd](a)


if __name__ == "__main__":
    main()
