"""Problem B: Monte Carlo test of Page's theorem  <S_{m,n}> = H_{mn} - H_n - (m-1)/(2n).

Haar states on C^m (x) C^n are sampled on the GPU as m x n complex Ginibre matrices
(normalising a Ginibre matrix gives a Haar state); the Schmidt probabilities are the
eigenvalues of G G^dagger / Tr(G G^dagger) (eigvalsh, clipped at 1e-15).
Sizes up to m*n = 2^24 (m = n = 4096, and m = 2, n = 2^23).

Classification: 2 (verification of a known, proven relation).
"""
import math
import os
import time

import json

from _common import DEVICE, FIGURES, RESULTS, dump, env_info, log, np, sync, torch

from eh import entropy as E
from eh import page as P
from eh import qstates as Q

BASE_SEED = 2000
MAX_DIM = 2**24


def grid():
    ms = [2, 3, 4, 5, 8, 10, 16, 32, 64, 100, 128, 256, 512, 1000, 1024, 2048, 4096]
    pairs = set()
    for m in ms:
        for f in (1, 2, 4, 16, 64, 256, 1024, 4096):
            if m * m * f <= MAX_DIM:
                pairs.add((m, m * f))
        nmax = MAX_DIM // m
        pairs.add((m, nmax))
    pairs.update({(2, 3), (3, 5), (7, 11), (6, 35), (100, 101), (1000, 1000), (1000, 16777)})
    return sorted(p for p in pairs if p[0] <= p[1])


def random_bipartite_probs(rng, m, n):
    """Entanglement spectrum of a Haar-random pure state on C^m (x) C^n: squared singular
    values of a normalised complex Ginibre m x n matrix."""
    z = (rng.standard_normal((m, n)) + 1j * rng.standard_normal((m, n))) / np.sqrt(2.0)
    s = np.linalg.svd(z, compute_uv=False) ** 2
    return s / s.sum()


def n_samples(m, n):
    d = m * n
    s = min(4096, max(16, 2**27 // d))
    if m >= 64:
        s = min(s, 1024)
    if m >= 256:
        s = min(s, 256)
    if m >= 1024:
        s = min(s, 48)
    if m >= 4096:
        s = 16
    return int(s)


def sample(m, n, ns, gen, chunk_cap=None):
    chunk = max(1, min(ns, 2**24 // (m * n)))
    if chunk_cap:
        chunk = min(chunk, chunk_cap)
    out, pur = [], []
    done = 0
    while done < ns:
        c = min(chunk, ns - done)
        g = Q.ginibre_t((c, m, n), gen)
        p = Q.schmidt_probs_t(g)
        del g
        out.append(E.von_neumann(p).cpu().numpy())
        pur.append(E.purity(p).cpu().numpy())
        done += c
    return np.concatenate(out), np.concatenate(pur)


def convergence(gen):
    """Running-mean error vs number of samples for (m,n) = (8,16)."""
    m, n = 8, 16
    s, _ = sample(m, n, 2**18, gen, chunk_cap=2**13)  # small batches: GPU 0 is shared, keep the footprint < 0.5 GiB
    exact = P.page_entropy(m, n)
    sizes = [2**j for j in range(4, 19)]
    reps_rms = []
    for sz in sizes:
        k = len(s) // sz
        means = s[: k * sz].reshape(k, sz).mean(1)
        reps_rms.append(float(np.sqrt(np.mean((means - exact) ** 2))))
    sigma = float(s.std(ddof=1))
    # slope fitted where there are >= 16 replicas
    use = [i for i, sz in enumerate(sizes) if len(s) // sz >= 16]
    slope = float(np.polyfit(np.log([sizes[i] for i in use]), np.log([reps_rms[i] for i in use]), 1)[0])
    return {"m": m, "n": n, "total_samples": len(s), "sizes": sizes, "rms_error": reps_rms, "sigma": sigma,
            "fitted_slope": slope, "expected_slope": -0.5}


def main():
    rows = []
    t_all = time.time()
    part = os.path.join(RESULTS, "b_partial.json")  # checkpoint: rows are appended as they finish
    if os.path.exists(part):
        rows = json.load(open(part))
        log(f"resuming from checkpoint with {len(rows)} rows")
    done = {(r["m"], r["n"]) for r in rows}
    for idx, (m, n) in enumerate(grid()):
        if (m, n) in done:
            continue
        ns = n_samples(m, n)
        seed = BASE_SEED + idx
        t0 = time.time()
        for attempt in range(90):  # GPU 0 is shared: on OOM wait and retry the same (m,n) with the same seed
            try:
                gen = Q.torch_generator(seed, DEVICE)
                s, pur = sample(m, n, ns, gen)
                break
            except (torch.OutOfMemoryError, RuntimeError) as e:
                if "out of memory" not in str(e).lower():
                    raise
                log(f"OOM at m={m} n={n} (attempt {attempt}); sleeping 20 s")
                torch.cuda.empty_cache(); time.sleep(20)
        else:
            raise SystemExit("GPU memory never became available")
        sync()
        wall = time.time() - t0
        exact = P.page_entropy(m, n)
        mean = float(s.mean()); std = float(s.std(ddof=1)); se = std / math.sqrt(ns)
        a0, a1, a2 = (P.page_asymptotic(m, n, o) for o in (0, 1, 2))
        row = {
            "m": m, "n": n, "dim": m * n, "samples": ns, "torch_seed": seed,
            "mc_mean": mean, "mc_std": std, "mc_stderr": se, "page_exact": exact,
            "z": (mean - exact) / se, "mc_minus_exact": mean - exact,
            "asym0": a0, "asym1": a1, "asym2": a2,
            "asym0_err": a0 - exact, "asym1_err": a1 - exact, "asym2_err": a2 - exact,
            "deficit_exact": math.log(m) - exact, "deficit_mc": math.log(m) - mean,
            "page_exact_bits": exact / math.log(2), "mc_mean_bits": mean / math.log(2),
            "mean_purity": float(pur.mean()), "purity_exact": (m + n) / (m * n + 1.0),
            "wall_s": wall,
        }
        rows.append(row)
        log(f"m={m:5d} n={n:9d} ns={ns:5d} mean={mean:.8f} exact={exact:.8f} se={se:.2e} z={row['z']:+.2f} "
            f"asym0_err={row['asym0_err']:+.2e} wall={wall:.1f}s")
        json.dump(rows, open(part, "w"))
        if DEVICE.type == "cuda":
            torch.cuda.empty_cache()
    rows.sort(key=lambda r: (r["m"], r["n"]))
    zs = np.array([r["z"] for r in rows])
    conv = convergence(Q.torch_generator(BASE_SEED + 999, DEVICE))
    sym = P.sympy_verify_asymptotic()
    # exact-only finite-size table (no sampling): asymptotic error for m = n and m << n
    fs = []
    for j in range(1, 13):
        m = 2**j
        for n in (m, 4 * m, 64 * m):
            ex = P.page_entropy(m, n)
            fs.append({"m": m, "n": n, "exact": ex, "log_m": math.log(m), "deficit": math.log(m) - ex, "m_over_2n": m / (2 * n),
                       "asym0_err": P.page_asymptotic(m, n, 0) - ex, "asym1_err": P.page_asymptotic(m, n, 1) - ex,
                       "asym2_err": P.page_asymptotic(m, n, 2) - ex})
    purity_z = [(r["mean_purity"] - r["purity_exact"]) for r in rows]
    summary = {
        "problem": "B", "classification": "2 (verification of a known relation: Page's formula)",
        "env": env_info(), "base_seed": BASE_SEED, "seed_rule": "torch.Generator(cuda).manual_seed(2000 + row index)",
        "clip": E.CLIP, "units": "nats",
        "n_pairs": len(rows), "max_dim": max(r["dim"] for r in rows),
        "max_abs_z": float(np.abs(zs).max()), "z_mean": float(zs.mean()), "z_rms": float(np.sqrt((zs**2).mean())),
        "frac_abs_z_gt_2": float((np.abs(zs) > 2).mean()), "frac_abs_z_gt_3": float((np.abs(zs) > 3).mean()),
        "max_abs_purity_dev": float(np.max(np.abs(purity_z))),
        "total_wall_s": float(sum(r["wall_s"] for r in rows)),  # sum over rows (robust to checkpoint resume)
        "rows": rows, "convergence": conv, "sympy_asymptotic_check": sym, "finite_size_exact": fs,
    }
    dump("b_page_theorem.json", summary)
    # markdown table
    with open(os.path.join(os.path.dirname(FIGURES), "results", "b_page_theorem_table.md"), "w") as f:
        f.write("| m | n | m*n | samples | MC mean [nats] | stderr | Page exact | z | ln m - m/2n | asym err (order 0) | asym err (+1/2mn) |\n|---|---|---|---|---|---|---|---|---|---|---|\n")
        for r in rows:
            f.write(f"| {r['m']} | {r['n']} | {r['dim']} | {r['samples']} | {r['mc_mean']:.9f} | {r['mc_stderr']:.2e} | {r['page_exact']:.9f} | {r['z']:+.2f} | {r['asym0']:.9f} | {r['asym0_err']:+.2e} | {r['asym1_err']:+.2e} |\n")
    plot(summary)
    log("SUMMARY pairs", len(rows), "max|z|", summary["max_abs_z"], "z_rms", summary["z_rms"], "conv slope", conv["fitted_slope"])


def plot(sm):
    from eh.plotting import AMBER, CYAN, FG, GREEN, MAGENTA, apply_theme, save

    plt = apply_theme()
    rows = sm["rows"]
    fig, ax = plt.subplots(2, 2, figsize=(13, 9))
    # (a) m = n deficit
    d = sorted([r for r in rows if r["m"] == r["n"]], key=lambda r: r["m"])
    mm = np.array([r["m"] for r in d])
    xs = np.unique(np.round(np.logspace(np.log10(2), np.log10(4096), 80)).astype(int))
    ax[0, 0].plot(xs, [math.log(x) - P.page_entropy(x, x) for x in xs], "-", color=CYAN, label="exact Page: ln m - <S>")
    ax[0, 0].plot(xs, 0.5 - 1 / (2.0 * xs**2), "--", color=MAGENTA, lw=1, label="asymptotic incl. 1/(2mn): 1/2 - 1/(2m²)")
    ax[0, 0].errorbar(mm, [r["deficit_mc"] for r in d], yerr=[1.96 * r["mc_stderr"] for r in d], fmt="o", color=AMBER, ms=4, label="Monte Carlo (95% CI)")
    ax[0, 0].axhline(0.5, color=FG, ls=":", lw=0.8)
    ax[0, 0].set_xscale("log"); ax[0, 0].set_xlabel("m = n  [Hilbert-space dimension]"); ax[0, 0].set_ylabel("ln m - <S>  [nats]")
    ax[0, 0].set_title("Finite-size effect at m = n: deficit -> 1/2 nat"); ax[0, 0].legend(fontsize=8)
    # (b) asymptotic error
    fs = sm["finite_size_exact"]
    for ratio, c in ((1, CYAN), (4, AMBER), (64, GREEN)):
        sel = [r for r in fs if r["n"] == ratio * r["m"]]
        x = [r["m"] * r["n"] for r in sel]
        ax[0, 1].plot(x, [abs(r["asym0_err"]) for r in sel], "-o", color=c, ms=3, label=f"n = {ratio} m: |ln m - m/2n - exact|")
        ax[0, 1].plot(x, [abs(r["asym1_err"]) for r in sel], "--s", color=c, ms=3, alpha=0.7, label=f"n = {ratio} m: with +1/(2mn)")
    ax[0, 1].set_xscale("log"); ax[0, 1].set_yscale("log")
    ax[0, 1].set_xlabel("m n  [total dimension]"); ax[0, 1].set_ylabel("|asymptotic - exact|  [nats]")
    ax[0, 1].set_title("Error of the asymptotic formula (exact arithmetic, no sampling)"); ax[0, 1].legend(fontsize=6.5)
    # (c) z-scores
    zs = np.array([r["z"] for r in rows]); dims = np.array([r["dim"] for r in rows])
    ax[1, 0].scatter(dims, zs, s=14, color=CYAN)
    for y in (-2, 2):
        ax[1, 0].axhline(y, color=AMBER, ls="--", lw=0.8)
    for y in (-4, 4):
        ax[1, 0].axhline(y, color=MAGENTA, ls=":", lw=0.8)
    ax[1, 0].set_xscale("log"); ax[1, 0].set_ylim(-5, 5)
    ax[1, 0].set_xlabel("m n  [total dimension]"); ax[1, 0].set_ylabel("z = (MC mean - Page) / stderr")
    ax[1, 0].set_title(f"{len(rows)} (m,n) pairs up to mn = 2^24: max|z| = {np.abs(zs).max():.2f}, rms z = {np.sqrt((zs**2).mean()):.2f}")
    # (d) convergence
    cv = sm["convergence"]
    sz = np.array(cv["sizes"])
    ax[1, 1].plot(sz, cv["rms_error"], "o", color=CYAN, label="RMS error of sample mean (over replicas)")
    ax[1, 1].plot(sz, cv["sigma"] / np.sqrt(sz), "-", color=AMBER, label="sigma / sqrt(samples)")
    ax[1, 1].set_xscale("log"); ax[1, 1].set_yscale("log")
    ax[1, 1].set_xlabel("samples per estimate"); ax[1, 1].set_ylabel("RMS |mean - Page|  [nats]")
    ax[1, 1].set_title(f"Monte Carlo convergence, (m,n)=({cv['m']},{cv['n']}): fitted slope {cv['fitted_slope']:.3f} (expect -0.5)"); ax[1, 1].legend(fontsize=8)
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    save(fig, os.path.join(FIGURES, "b_page_theorem.png"),
         "Assumptions: Haar-random pure states on C^m (x) C^n sampled as normalised complex Ginibre matrices (complex128, A100); entropy of the m-dim subsystem in nats; eigenvalues <= 1e-15 clipped.")


if __name__ == "__main__":
    main()
