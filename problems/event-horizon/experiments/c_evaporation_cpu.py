"""Problem C (laptop/CPU numpy version): sequential unitary evaporation of an N-qubit toy
black hole, N = 6..12, exact state vectors.

(experiments/c_evaporation.py is a separate torch/GPU implementation of the same protocol;
this file is self-contained, numpy-only and writes *_cpu outputs so the two never collide.)

Usage:
  OMP_NUM_THREADS=2 python3 experiments/c_evaporation_cpu.py            # everything (uses caches)
  OMP_NUM_THREADS=2 python3 experiments/c_evaporation_cpu.py --only 9   # compute+cache main run for one N
  OMP_NUM_THREADS=2 python3 experiments/c_evaporation_cpu.py --quick    # small smoke run
  modal run experiments/c_modal.py --n 12 --seeds 20                     # optional: N=11/12 on Modal CPUs
Outputs: results/c_evaporation_cpu.json, results/c_evaporation_cpu_spectra.npz,
         figures/c_evaporation_cpu.png, figures/c_distribution_cpu.png, figures/c_runtime_cpu.png
"""
import os, sys, time, argparse, pickle, glob
import numpy as np
from scipy import stats

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from eh import qstates as qs, page as pg, evaporation as ev  # noqa: E402
from eh.entropy import von_neumann, purity  # noqa: E402
from eh import plotstyle as ps  # noqa: E402

BASE_SEED = 20261115
LN2 = np.log(2.0)
ent = lambda p: float(von_neumann(p))
pur = lambda p: float(purity(p))


def rng_for(tag, N, i):
    return np.random.default_rng(np.random.SeedSequence([BASE_SEED, tag, N, i]))


def summarise(x):
    x = np.asarray(x, dtype=float)
    n = x.shape[0]
    sd = x.std(axis=0, ddof=1)
    return {"mean": x.mean(axis=0), "std": sd, "sem": sd / np.sqrt(n), "ci95": 1.96 * sd / np.sqrt(n)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--only", type=int, default=None, help="compute and cache the main run for this N only, then exit")
    ap.add_argument("--part", type=str, default=None, help="with --only: i/n, compute seeds i mod n only (parallel chunks)")
    a = ap.parse_args()
    seeds = {6: 200, 7: 200, 8: 200, 9: 200, 10: 100, 11: 40, 12: 20}
    if a.quick:
        seeds = {6: 40, 7: 40, 8: 40, 9: 20}
    res = {"description": "Sequential evaporation: fresh Haar unitary on ALL remaining BH qubits, then emit one qubit.",
           "units": "nats", "base_seed": BASE_SEED,
           "seed_rule": "np.random.SeedSequence([BASE_SEED, tag, N, i]); tag 0=haar/zero-init main runs, 1=haar/random-init, "
                        "2=brickwork control, 3=direct Haar reference, 4=distribution-test sequential sample",
           "timing_note": "seconds_per_trajectory is CPU time (time.process_time, summed over <=2 BLAS threads) on the "
                          "laptop, because the machine is shared and wall time is unreliable",
           "runs": {}, "controls": {}, "timing": {}, "modal_vs_local_max_abs_dS": {}}
    npz = {}
    for N, ns in seeds.items():
        if a.only is not None and N != a.only:
            continue
        cache = os.path.join(ps.RES, "c_cache", f"N{N}_seeds{ns}.pkl")
        cache_modal = cache.replace(".pkl", "_modal.pkl")
        source = "local laptop"
        if a.part is not None:
            pi, pn = (int(v) for v in a.part.split("/"))
            idx = [i for i in range(ns) if i % pn == pi]
            t0 = time.process_time()
            tr = [ev.run_trajectory(N, rng_for(0, N, i), init="zero") for i in idx]
            os.makedirs(os.path.dirname(cache), exist_ok=True)
            pickle.dump((idx, tr, time.process_time() - t0), open(cache.replace(".pkl", f"_part{pi}of{pn}.pkl"), "wb"))
            return
        parts = sorted(glob.glob(cache.replace(".pkl", "_part*of*.pkl")))
        if not os.path.exists(cache) and parts:
            got = {}
            cpu = 0.0
            for f in parts:
                idx, tr, c = pickle.load(open(f, "rb"))
                got.update(dict(zip(idx, tr)))
                cpu += c
            if sorted(got) == list(range(ns)):
                pickle.dump(([got[i] for i in range(ns)], cpu), open(cache, "wb"))
        if os.path.exists(cache):
            trajs, cpu = pickle.load(open(cache, "rb"))
        elif os.path.exists(cache_modal):
            # identical seeds and code, executed by experiments/c_modal.py on Modal CPU containers
            trajs, _ = pickle.load(open(cache_modal, "rb"))
            source = "Modal CPU containers (experiments/c_modal.py); timing re-measured locally on 2 trajectories"
            t0 = time.process_time()
            loc = [ev.run_trajectory(N, rng_for(0, N, i), init="zero") for i in range(2)]
            cpu = (time.process_time() - t0) / 2 * ns
            res["modal_vs_local_max_abs_dS"][str(N)] = float(max(
                np.max(np.abs(np.array(loc[i]["S_R"]) - np.array(trajs[i]["S_R"]))) for i in range(2)))
        else:
            t0 = time.process_time()
            trajs = [ev.run_trajectory(N, rng_for(0, N, i), init="zero") for i in range(ns)]
            cpu = time.process_time() - t0
            os.makedirs(os.path.dirname(cache), exist_ok=True)
            pickle.dump((trajs, cpu), open(cache, "wb"))
        SR = np.array([t["S_R"] for t in trajs])
        SB = np.array([t["S_B"] for t in trajs])
        PU = np.array([t["purity_R"] for t in trajs])
        page = np.array(pg.page_curve(N))
        s = summarise(SR)
        z = np.zeros(N + 1)
        z[1:-1] = (s["mean"][1:-1] - page[1:-1]) / s["sem"][1:-1]
        dR = np.array(trajs[0]["dim_R"]); dB = np.array(trajs[0]["dim_B"])
        res["runs"][str(N)] = {
            "N": N, "n_seeds": ns, "init": "|0...0>", "computed_on": source, "k": list(range(N + 1)),
            "dim_R": dR, "dim_B": dB, "S_R": s, "S_B": summarise(SB), "purity_R": summarise(PU),
            "purity_haar_exact": (dR + dB) / (dR * dB + 1.0),
            "page": page, "z_vs_page": z, "max_abs_z": float(np.max(np.abs(z))),
            "max_abs_dev_nats": float(np.max(np.abs(s["mean"] - page))),
            "max_abs_SR_minus_SB": float(np.max(np.abs(SR - SB))),
            "max_norm_error": float(max(np.abs(np.array(t["norm"]) - 1).max() for t in trajs)),
            "mean_spectrum_desc": [np.mean([t["spectra"][k] for t in trajs], axis=0) for k in range(N + 1)],
            "S_R_per_seed": SR, "seconds_per_trajectory": cpu / ns,
            "mean_step_seconds_wall": np.mean([t["step_seconds"] for t in trajs], axis=0),
        }
        for k in range(N + 1):
            npz[f"N{N}_k{k}"] = np.array([t["spectra"][k] for t in trajs])
        res["timing"][str(N)] = cpu / ns
        print(f"N={N:2d} seeds={ns:3d} {cpu/ns:8.3f} cpu-s/traj  max|z|={np.max(np.abs(z)):.2f} "
              f"max|S_R-S_B|={res['runs'][str(N)]['max_abs_SR_minus_SB']:.1e} [{source[:5]}]", flush=True)
    if a.only is not None:
        return
    Ns = sorted(seeds)
    tt = np.array([res["timing"][str(N)] for N in Ns])
    big = [i for i, N in enumerate(Ns) if N >= 9]
    slope = float(np.polyfit(np.array(Ns)[big], np.log2(tt[big]), 1)[0]) if len(big) >= 2 else float("nan")
    res["timing_fit"] = {"N_used": [Ns[i] for i in big], "log2_cpu_seconds_per_qubit": slope,
                         "expected": "-> 3 asymptotically (Householder QR of a 2^N x 2^N Ginibre matrix is O(8^N)); memory O(4^N)"}
    all_z = np.concatenate([np.array(r["z_vs_page"])[1:-1] for r in res["runs"].values()])
    res["z_summary"] = {"n_points": int(all_z.size), "max_abs": float(np.abs(all_z).max()), "std": float(all_z.std(ddof=1)),
                        "fraction_within_2": float(np.mean(np.abs(all_z) < 2)),
                        "note": "different k of the same N share trajectories and are correlated"}

    # ---------------- controls / distribution tests (N = 8) ----------------
    Nc = 8
    nc = 300 if a.quick else 3000
    seq = [ev.run_trajectory(Nc, rng_for(4, Nc, i), init="zero", check_B=False)["spectra"] for i in range(nc)]
    dire = [ev.nested_cut_spectra(qs.haar_state(2 ** Nc, rng_for(3, Nc, i)), Nc) for i in range(nc)]

    def stat(arr, k, f):
        return np.array([float(f(np.asarray(arr[i][k], dtype=float))) for i in range(nc)])

    fs = {"S": ent, "purity": pur, "lambda_max": np.max, "lambda_min": np.min}
    dist = {"N": Nc, "n_seeds_each": nc, "k": list(range(1, Nc)), "tests": {}}
    allp = []
    for name, f in fs.items():
        rows = []
        for k in range(1, Nc):
            x, y = stat(seq, k, f), stat(dire, k, f)
            ks = stats.ks_2samp(x, y)
            rows.append({"k": k, "seq_mean": x.mean(), "dir_mean": y.mean(), "seq_std": x.std(ddof=1),
                         "dir_std": y.std(ddof=1), "ks_stat": ks.statistic, "ks_p": ks.pvalue})
            allp.append(ks.pvalue)
        dist["tests"][name] = rows
    dist.update({"n_tests": len(allp), "min_p": float(min(allp)), "bonferroni_threshold_0.05": 0.05 / len(allp),
                 "any_reject_bonferroni": bool(min(allp) < 0.05 / len(allp)),
                 "fraction_p_below_0.05": float(np.mean(np.array(allp) < 0.05)),
                 "note": "the 28 tests are not independent (same samples, related statistics)"})
    Sseq = np.array([stat(seq, k, ent) for k in range(1, Nc)]).T
    Sdir = np.array([stat(dire, k, ent) for k in range(1, Nc)]).T
    cs, cd = np.corrcoef(Sseq.T), np.corrcoef(Sdir.T)
    dist.update({"corr_S_sequential": cs, "corr_S_direct_nested": cd, "corr_max_abs_diff": float(np.max(np.abs(cs - cd))),
                 "corr_sampling_error_scale": float(1 / np.sqrt(nc)),
                 "corr_adjacent_sequential": [cs[i, i + 1] for i in range(Nc - 2)],
                 "corr_adjacent_direct": [cd[i, i + 1] for i in range(Nc - 2)],
                 "S_samples_k4_sequential": Sseq[:, 3], "S_samples_k4_direct": Sdir[:, 3]})
    res["controls"]["distribution_test"] = dist
    print("distribution test: min KS p =", dist["min_p"], "over", len(allp), "tests; corr max diff",
          dist["corr_max_abs_diff"], "(sampling scale", dist["corr_sampling_error_scale"], ")", flush=True)

    nr = 40 if a.quick else 200
    SRr = np.array([ev.run_trajectory(Nc, rng_for(1, Nc, i), init="random", check_B=False)["S_R"] for i in range(nr)])
    sr = summarise(SRr)
    pc = np.array(pg.page_curve(Nc))
    res["controls"]["random_init"] = {"N": Nc, "n_seeds": nr, "S_R": sr, "page": pc,
                                      "max_abs_z": float(np.max(np.abs((sr["mean"] - pc)[1:-1] / sr["sem"][1:-1])))}
    bw = {}
    for Nb in ([8] if a.quick else [8, 10]):
        nbw = 40 if a.quick else 200
        SRb = np.array([ev.run_trajectory(Nb, rng_for(2, Nb, i), init="zero", scrambler="brickwork", check_B=False)["S_R"]
                        for i in range(nbw)])
        pb = np.array(pg.page_curve(Nb))
        sb = summarise(SRb)
        bw[str(Nb)] = {"N": Nb, "n_seeds": nbw, "S_R": sb, "page": pb,
                       "max_deficit_vs_page_nats": float(np.max(pb - sb["mean"])),
                       "k_of_max_deficit": int(np.argmax(pb - sb["mean"]))}
    res["controls"]["brickwork_one_layer"] = bw
    print("random-init max|z| =", res["controls"]["random_init"]["max_abs_z"],
          "; brickwork max deficit (nats):", {k: v["max_deficit_vs_page_nats"] for k, v in bw.items()}, flush=True)

    ps.dump(res, "c_evaporation_cpu.json")
    np.savez_compressed(os.path.join(ps.RES, "c_evaporation_cpu_spectra.npz"), **npz)
    make_figures(res)


def make_figures(res):
    plt = ps.apply()
    cols = [ps.CYAN, ps.AMBER, ps.MAGENTA, ps.GREEN]
    fig, ax = plt.subplots(1, 2, figsize=(12.5, 5.2))
    Ns = sorted(int(n) for n in res["runs"])
    show = [n for n in Ns if n % 2 == 0]
    for i, N in enumerate(show):
        r = res["runs"][str(N)]
        k = np.array(r["k"]); m = np.array(r["S_R"]["mean"]); sd = np.array(r["S_R"]["std"])
        c = cols[i % 4]
        ax[0].fill_between(k, (m - sd) / LN2, (m + sd) / LN2, color=c, alpha=0.25, lw=0)
        ax[0].plot(k, m / LN2, "o", ms=4, color=c, label=f"N={N} sequential ({r['n_seeds']} seeds)")
        ax[0].plot(k, np.array(r["page"]) / LN2, "-", color=c, lw=1, alpha=0.9)
    ax[0].plot([], [], "-", color=ps.FG, lw=1, label="Page formula (same bipartition)")
    bw = res["controls"]["brickwork_one_layer"]
    Nb = max(int(n) for n in bw)
    b = bw[str(Nb)]
    ax[0].errorbar(np.arange(Nb + 1), np.array(b["S_R"]["mean"]) / LN2, yerr=np.array(b["S_R"]["std"]) / LN2,
                   fmt="x--", color="#9AA7B4", ms=4, lw=0.8, label=f"control: 1 brickwork layer/step, N={Nb} (±1 std)")
    ax[0].set_xlabel("emitted qubits k"); ax[0].set_ylabel("S(R) [bits]")
    ax[0].set_title("Sequential unitary evaporation vs Page (band = ±1 std over seeds)")
    ax[0].legend(fontsize=7.5)
    for i, N in enumerate(Ns):
        r = res["runs"][str(N)]
        z = np.array(r["z_vs_page"])[1:-1]
        ax[1].plot(np.arange(1, N) / N, z, "o-", ms=3, lw=0.8, color=plt.cm.cool(i / max(1, len(Ns) - 1)), label=f"N={N}")
    ax[1].axhline(0, color=ps.FG, lw=0.6)
    for y in (-2, 2):
        ax[1].axhline(y, color=ps.AMBER, lw=0.6, ls=":")
    ax[1].set_xlabel("fraction emitted k/N"); ax[1].set_ylabel("(mean S(R) − Page) / standard error")
    ax[1].set_title("Residuals in units of the standard error (dotted: ±2)")
    ax[1].legend(fontsize=7, ncol=2)
    fig.tight_layout(rect=(0, 0.035, 1, 1))
    ps.caption(fig, "Assumptions: finite-dim toy model, N qubits, pure initial state |0…0>, fresh Haar unitary on ALL remaining BH "
                    "qubits before each single-qubit emission; exact state vectors; no gravity, no geometry.")
    ps.save(fig, "c_evaporation_cpu.png")

    d = res["controls"]["distribution_test"]
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.8))
    x, y = np.array(d["S_samples_k4_sequential"]) / LN2, np.array(d["S_samples_k4_direct"]) / LN2
    bins = np.linspace(min(x.min(), y.min()), max(x.max(), y.max()), 45)
    ax[0].hist(x, bins=bins, histtype="stepfilled", alpha=0.35, color=ps.CYAN, density=True, label="sequential evaporation")
    ax[0].hist(y, bins=bins, histtype="step", color=ps.AMBER, density=True, lw=1.4, label="single Haar state")
    pk = [t for t in d["tests"]["S"] if t["k"] == 4][0]
    ax[0].set_title(f"S(R) distribution, N={d['N']}, k=4 (KS p={pk['ks_p']:.2f})")
    ax[0].set_xlabel("S(R) [bits]"); ax[0].set_ylabel("probability density [1/bit]"); ax[0].legend(fontsize=8)
    for name, c in zip(["S", "purity", "lambda_max", "lambda_min"], cols):
        ax[1].plot(d["k"], [t["ks_p"] for t in d["tests"][name]], "o-", color=c, ms=4, lw=0.8, label=name)
    ax[1].axhline(d["bonferroni_threshold_0.05"], color=ps.FG, ls=":", lw=0.8, label=f"Bonferroni 0.05/{d['n_tests']}")
    ax[1].set_yscale("log"); ax[1].set_xlabel("emitted qubits k"); ax[1].set_ylabel("two-sample KS p-value")
    ax[1].set_title(f"Sequential vs direct Haar: KS tests ({d['n_seeds_each']} seeds each)")
    ax[1].legend(fontsize=7.5)
    cs, cd = np.array(d["corr_S_sequential"]), np.array(d["corr_S_direct_nested"])
    n = len(d["k"])
    im = ax[2].imshow(np.where(np.tri(n, k=0, dtype=bool), cs, cd), cmap="magma", vmin=-0.1, vmax=1,
                      extent=(0.5, n + 0.5, n + 0.5, 0.5))
    ax[2].grid(False)
    ax[2].set_title("corr[S(R_k), S(R_k')]: lower △ sequential, upper △ single Haar state", fontsize=9)
    ax[2].set_xlabel("k'"); ax[2].set_ylabel("k")
    fig.colorbar(im, ax=ax[2]).set_label("Pearson correlation")
    fig.tight_layout(rect=(0, 0.035, 1, 1))
    ps.caption(fig, f"Assumptions: N={d['N']} qubits; 'sequential' = Haar unitary on the remaining BH at each step; 'single Haar state' = "
                    "one Haar state per seed cut at its first k qubits; independent seeds; KS p-values uncorrected.")
    ps.save(fig, "c_distribution_cpu.png")

    fig, ax = plt.subplots(figsize=(6.6, 4.8))
    t = np.array([res["timing"][str(N)] for N in Ns])
    ax.semilogy(Ns, t, "o-", color=ps.CYAN, label="measured (mean over seeds)")
    ax.semilogy(Ns, t[-1] * 8.0 ** (np.array(Ns) - Ns[-1]), "--", color=ps.AMBER, label="8^N reference (dense QR)")
    ax.set_title(f"CPU time per trajectory; fitted 2^({res['timing_fit']['log2_cpu_seconds_per_qubit']:.2f} N) for N≥9")
    ax.set_xlabel("black hole size N [qubits]"); ax.set_ylabel("CPU time per trajectory [s]"); ax.legend(fontsize=8)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    ps.caption(fig, "Assumptions: shared laptop, ≤2 BLAS threads, CPU time; includes S(R) and S(B) eigendecompositions each step.")
    ps.save(fig, "c_runtime_cpu.png")


if __name__ == "__main__":
    main()
