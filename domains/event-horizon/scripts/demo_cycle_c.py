#!/usr/bin/env python
"""DEMO helper: prints the numbers of research cycle C (sequential Haar evaporation) step by step.
Reads stored results only (no GPU needed, nothing is overwritten).
Usage: python scripts/demo_cycle_c.py {predict|gpu|compare|critic|verify|all}"""
import json, math, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
R = lambda f: json.load(open(os.path.join(ROOT, "results", f)))


def page(m, n):
    if m > n: m, n = n, m
    return math.fsum(1.0 / j for j in range(n + 1, m * n + 1)) - (m - 1) / (2.0 * n)


def predict():
    N = 14
    print("PREDICTION (Sec. 4.4 of the paper): every intermediate state is exactly Haar, so")
    print("<S(R_t)> = Page(2^t, 2^(N-t)) with no correction.  N = 14, nats:")
    print("  t   :", " ".join(f"{t:6d}" for t in range(1, N)))
    print("  Page:", " ".join(f"{page(2**t, 2**(N-t)):6.3f}" for t in range(1, N)))
    print(f"  half-cut deficit (N/2) ln2 - Page = {N/2*math.log(2) - page(2**7, 2**7):.4f} nats (-> 1/2)")


def gpu():
    print("GPU SIMULATION (stored runs on the A100, GPU 0, complex128):")
    print(f"  {'mode':9s} {'N':>3s} {'seeds':>5s} {'device':>6s} {'max|z|':>7s} {'max|mean-Page|':>15s} {'s/traj':>8s} {'peak GiB':>9s}")
    for mode, Ns in (("full", [10, 11, 12, 13, 14]), ("isometry", [22, 24, 26, 27])):
        for N in Ns:
            d = R(f"c_evap_{mode}_N{N}.json")
            mem = d.get("peak_gpu_mem_GiB"); mem = float("nan") if mem is None else mem
            print(f"  {mode:9s} {N:3d} {d['seeds']:5d} {d['device']:>6s} {d['max_abs_z']:7.2f} {d['max_abs_dev_nats']:15.2e} "
                  f"{d['wall_s_per_seed_min']:8.2f} {mem:9.2f}")
    print("  (N = 27 is a single trajectory: its z has no meaning.)")


def compare():
    d = R("c_evap_full_N14.json")
    print("COMPARISON, literal protocol N = 14,", d["seeds"], "trajectories, seed rule:", d["seed_rule"])
    print(f"  {'t':>3s} {'mean S(R)':>10s} {'Page':>10s} {'stderr':>9s} {'z':>6s}")
    for i, t in enumerate(d["t"]):
        if 0 < t < d["N"]:
            print(f"  {t:3d} {d['S_R_mean'][i]:10.5f} {d['page'][i]:10.5f} {d['S_R_stderr'][i]:9.1e} {d['z_vs_page'][i]:6.2f}")
    print(f"  max |S(R) - S(B)| = {d['max_abs_SR_minus_SB']:.1e} nats")
    s = R("c_summary.json")["z_all_runs_ge8_seeds"]
    print(f"  all runs pooled: {s['n']} cells, rms z = {s['rms']:.2f}, {100*s['frac_gt_2']:.1f}% with |z| > 2, max |z| = {s['max_abs']:.2f}  <-- one cell above 4")


def critic():
    b = R("c_summary.json")["recheck_full_N13"]
    print("CRITIC OBJECTION: full mode, N = 13, step t = 2 has z = +4.19 with 40 seeds.  Bias or fluctuation?")
    print(f"  {'seed block':>10s} {'n':>5s} {'z(t=2)':>7s} {'std(t=2)':>9s} {'max|z| all steps':>17s}")
    for k, v in b.items():
        if isinstance(v, dict):
            print(f"  {k:>10s} {v['n']:5d} {v['z_t2']:7.2f} {v['std_t2']:9.1e} {v['max_abs_z']:17.2f}")
    print("  ->", b["note"])


def verify():
    v = R("verification.json")[1]; n = v["numbers"]
    print("INDEPENDENT VERIFICATION (verify/independent.py; no import of eh/; scipy unitary_group, CPU):")
    print(" ", v["claim"])
    print("  t               :", n["t"][1:-1])
    print("  exact Page      :", n["page_exact_nats"][1:-1])
    print("  verifier mean   :", n["verifier_mean"][1:-1])
    print("  z vs Page       :", n["z_vs_page"][1:-1])
    print("  z vs builder    :", n["z_vs_builder_full"])
    print("  step correlation:", n["corr_consecutive_steps"], "| max |S(R)-S(B)| =", f"{n['max_abs_SR_minus_SB']:.1e}")
    print("  agree:", v["agree"], "|", v["tolerance"])
    a = R("verification.json")
    print(f"  whole verification: {sum(x['agree'] for x in a)} of {len(a)} claims agree; the one that does not:")
    for x in a:
        if not x["agree"]: print("   ", x["claim"][:200])


STEPS = {"predict": predict, "gpu": gpu, "compare": compare, "critic": critic, "verify": verify}
if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    for name, fn in STEPS.items():
        if which in (name, "all"):
            fn(); print()
