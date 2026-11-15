"""Problem A: the Page curve of a Haar-random N-qubit pure state.

For each N and each seed ONE global Haar state |psi> in (C^2)^{(x)N} is drawn on the GPU; for
every k = 0..N the first k qubits are called R, the state is reshaped to a 2^k x 2^(N-k)
matrix and S(R) is computed from the Schmidt spectrum (eigvalsh of the Gram matrix on the
smaller side; eigenvalues <= 1e-15 clipped).  Compared with Page's exact formula.

Classification: 1 (reproduction of the Page curve) / 2 (verification of Page's formula).
Note: values at different k for the same N share the same states, so their z-scores are
correlated; values at different N are independent.

Usage: python experiments/a_page_curve.py [--Ns 8 9 ... 20] [--extra 22 24]
"""
import argparse
import math

from _common import DEVICE, FIGURES, RESULTS, dump, env_info, log, np, sync, torch
import os
import time

from eh import entropy as E
from eh import page as P
from eh import qstates as Q

BASE_SEED = 1000
BOTH_SIDES_MAX = 2048  # S(B) computed independently from rho_B when dim(larger side) <= this


def seeds_for(N):
    if N <= 14:
        return 400
    if N <= 16:
        return 200
    if N <= 18:
        return 100
    if N <= 20:
        return 50
    if N <= 22:
        return 16
    return 8


def run_N(N):
    ns = seeds_for(N)
    seed = BASE_SEED + N
    gen = Q.torch_generator(seed, DEVICE)
    chunk = max(1, min(ns, 2**24 // 2**N))
    S = np.zeros((ns, N + 1))
    PUR = np.zeros((ns, N + 1))
    sym = 0.0  # max |S(R) - S(B)|, S(B) from an independent eigvalsh of rho_B (larger side)
    sym_checked = 0
    t0 = time.time()
    done = 0
    while done < ns:
        c = min(chunk, ns - done)
        psi = Q.haar_states_t(c, 2**N, gen)
        for k in range(N + 1):
            p = Q.schmidt_probs_t(psi.reshape(c, 2**k, 2 ** (N - k)))
            S[done:done + c, k] = E.von_neumann(p).cpu().numpy()
            PUR[done:done + c, k] = E.purity(p).cpu().numpy()
            if 2 ** max(k, N - k) <= BOTH_SIDES_MAX and sym_checked < 4000:
                m = psi[: min(c, 8)].reshape(-1, 2**k, 2 ** (N - k))
                big = (m.conj().transpose(-1, -2) @ m) if k <= N - k else (m @ m.conj().transpose(-1, -2))
                pb = torch.linalg.eigvalsh(big).clamp_min(0.0)
                pb = pb / pb.sum(-1, keepdim=True)
                diff = (E.von_neumann(pb) - E.von_neumann(p[: m.shape[0]])).abs().max().item()
                sym = max(sym, diff)
                sym_checked += m.shape[0]
        done += c
    sync()
    wall = time.time() - t0
    page = np.array(P.page_curve(N))
    mean, std = S.mean(0), S.std(0, ddof=1)
    se = std / math.sqrt(ns)
    z = np.zeros(N + 1)
    inner = slice(1, N)
    z[inner] = (mean[inner] - page[inner]) / se[inner]
    out = {
        "N": N, "seeds": ns, "torch_seed": seed, "wall_s": wall,
        "k": list(range(N + 1)),
        "mean_nats": mean.tolist(), "std_nats": std.tolist(), "stderr_nats": se.tolist(),
        "page_nats": page.tolist(), "z": z.tolist(),
        "mean_bits": (mean / math.log(2)).tolist(), "page_bits": (page / math.log(2)).tolist(),
        "mean_purity": PUR.mean(0).tolist(),
        "max_abs_z": float(np.abs(z).max()), "max_abs_dev_nats": float(np.abs(mean - page).max()),
        "max_abs_SR_minus_SB": sym, "SR_SB_states_checked": sym_checked,
        "endpoints_abs_max": float(max(np.abs(S[:, 0]).max(), np.abs(S[:, N]).max())),
    }
    log(f"N={N:2d} seeds={ns:4d} wall={wall:6.1f}s max|z|={out['max_abs_z']:.2f} max|dev|={out['max_abs_dev_nats']:.2e} "
        f"max|S(R)-S(B)|={sym:.1e}")
    return out


def plot(res):
    from eh.plotting import AMBER, CYAN, FG, GREEN, MAGENTA, PALETTE, apply_theme, save

    plt = apply_theme()
    fig, ax = plt.subplots(1, 3, figsize=(16, 4.8))
    show = [r for r in res if r["N"] in (8, 12, 16, 20, 24)]
    for i, r in enumerate(show):
        k = np.array(r["k"]); c = PALETTE[i % len(PALETTE)]
        m, s = np.array(r["mean_nats"]), np.array(r["std_nats"])
        ax[0].fill_between(k, m - s, m + s, color=c, alpha=0.25)
        ax[0].plot(k, r["page_nats"], "-", color=c, lw=1.2)
        ax[0].plot(k, m, "o", color=c, ms=3.5, label=f"N={r['N']} ({r['seeds']} seeds)")
    ax[0].plot([], [], "-", color=FG, lw=1.2, label="Page formula (lines)")
    ax[0].set_xlabel("k = number of radiation qubits"); ax[0].set_ylabel("S(R)  [nats]")
    ax[0].set_title("Page curve: numerics (dots, ±1 std band) vs exact formula", fontsize=9.5); ax[0].legend(fontsize=7)
    for i, r in enumerate(show):
        k = np.array(r["k"]); N = r["N"]; c = PALETTE[i % len(PALETTE)]
        cap = np.minimum(k, N - k) * math.log(2)
        ax[1].plot(k - N / 2, cap - np.array(r["page_nats"]), "-", color=c, lw=1.2)
        ax[1].errorbar(k - N / 2, cap - np.array(r["mean_nats"]), yerr=1.96 * np.array(r["stderr_nats"]), fmt="o", ms=3.5, color=c, label=f"N={N}")
    ax[1].axhline(0.5, color=FG, ls=":", lw=0.8)
    ax[1].set_xlim(-6, 6); ax[1].set_yscale("log"); ax[1].set_ylim(1e-4, 1)
    ax[1].set_xlabel("k - N/2  [qubits]"); ax[1].set_ylabel("min(k,N-k) log 2 - S(R)  [nats]")
    ax[1].set_title("Deficit near the Page time (95% CI; dotted: 1/2 nat)", fontsize=9.5); ax[1].legend(fontsize=7)
    zs = np.concatenate([np.array(r["z"])[1:-1] for r in res])
    ax[2].hist(zs, bins=30, color=CYAN, alpha=0.8, density=True)
    xx = np.linspace(-4.5, 4.5, 200)
    ax[2].plot(xx, np.exp(-xx**2 / 2) / math.sqrt(2 * math.pi), color=AMBER, label="N(0,1)")
    ax[2].set_xlabel("z = (mean - Page) / stderr  [dimensionless]"); ax[2].set_ylabel("density")
    ax[2].set_title(f"z-scores, all (N,k), 0<k<N: n={len(zs)}, max|z|={np.abs(zs).max():.2f}", fontsize=9.5); ax[2].legend()
    save(fig, os.path.join(FIGURES, "a_page_curve.png"),
         "Assumptions: global state Haar-random pure on N qubits (complex128, A100); R = first k qubits; entropy in nats, eigenvalues <= 1e-15 clipped; no dynamics, no gravity.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--Ns", type=int, nargs="*", default=list(range(8, 21)))
    ap.add_argument("--extra", type=int, nargs="*", default=[22, 24])
    ap.add_argument("--replot", action="store_true", help="only redraw the figure from results/a_page_curve.json")
    a = ap.parse_args()
    if a.replot:
        import json
        plot(json.load(open(os.path.join(RESULTS, "a_page_curve.json")))["per_N"])
        return
    res = []
    for N in a.Ns + a.extra:
        res.append(run_N(N))
        torch.cuda.empty_cache() if DEVICE.type == "cuda" else None
    zs = np.concatenate([np.array(r["z"])[1:-1] for r in res])
    summary = {
        "problem": "A", "classification": "1 (reproduction) / 2 (verification of Page's formula)",
        "env": env_info(), "base_seed": BASE_SEED, "seed_rule": "torch.Generator(cuda).manual_seed(1000 + N)",
        "clip": E.CLIP, "units": "nats (bits also stored)",
        "n_cells": int(len(zs)), "max_abs_z_overall": float(np.abs(zs).max()),
        "z_mean": float(zs.mean()), "z_rms": float(np.sqrt((zs**2).mean())),
        "frac_abs_z_gt_2": float((np.abs(zs) > 2).mean()),
        "max_abs_dev_nats_overall": float(max(r["max_abs_dev_nats"] for r in res)),
        "max_abs_SR_minus_SB_overall": float(max(r["max_abs_SR_minus_SB"] for r in res)),
        "per_N": res,
    }
    dump("a_page_curve.json", summary)
    plot(res)
    log("SUMMARY cells", summary["n_cells"], "max|z|", summary["max_abs_z_overall"], "z_rms", summary["z_rms"])


if __name__ == "__main__":
    main()
