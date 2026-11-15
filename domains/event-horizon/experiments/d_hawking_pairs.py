"""Problem D: Bell-pair "Hawking" toy model vs unitary evaporation (Problem C).

Model: k independent Bell pairs, one qubit of each pair in the radiation R, its partner
behind the horizon.  Derivation (see also notes/D_derivation.md and eh/pairs.py):

    |Psi_k> = |Phi+>^{(x)k},   rho_R = Tr_partners |Psi_k><Psi_k| = (I/2)^{(x)k}
    =>  S(R) = k log 2 exactly,  Tr rho_R^2 = 2^-k,  monotone in k.

A black hole that started with N qubits of capacity and has emitted k of them can hold at
most (N-k) log 2 of entropy.  For k > N/2 the Hawking-pair entropy exceeds this.

The script (i) verifies S(R) = k log 2 numerically from explicitly constructed states
(two independent constructions), (ii) tabulates Hawking vs capacity vs Page vs the
averaged sequential-evaporation trajectory of Problem C (read from results/c_evap_*.json),
(iii) plots them.  Tiny matrices only -> runs on the CPU by default.

Classification: 1 (reproduction of a textbook toy model) + 2 (exact relation verified).
"""
import glob
import json
import math
import os

os.environ.setdefault("EH_DEVICE", "cpu")
from _common import DEVICE, FIGURES, RESULTS, dump, env_info, log, np, torch  # noqa: E402

from eh import entropy as E  # noqa: E402
from eh import page as P  # noqa: E402
from eh import pairs  # noqa: E402
from eh import qstates as Q  # noqa: E402

LOG2 = math.log(2.0)


def verify(kmax_matrix=12, kmax_vector=10):
    rows = []
    for k in range(0, kmax_matrix + 1):
        m = pairs.bell_pairs_state(k, xp=torch, device=DEVICE)  # (2^k x 2^k) radiation | partners
        p = Q.schmidt_probs_t(m, "svd")
        row = {"k": k, "dim_R": 2**k, "S_R_numeric_nats": E.von_neumann(p).item(), "S_R_exact_nats": k * LOG2,
               "purity_numeric": E.purity(p).item(), "purity_exact": 2.0**-k,
               "renyi2_numeric_nats": E.renyi2(p).item(),
               "max_dev_from_flat_spectrum": (p - 2.0**-k).abs().max().item()}
        if 1 <= k <= kmax_vector:  # independent route: 2k-qubit state vector, trace out odd (partner) qubits
            psi = torch.as_tensor(pairs.bell_pairs_statevector(k), device=DEVICE)
            rho = Q.reduced_density_matrix(psi, (2,) * (2 * k), tuple(range(0, 2 * k, 2)))
            ev = torch.linalg.eigvalsh(rho)
            row["S_R_statevector_route_nats"] = E.von_neumann(ev).item()
            row["rho_R_minus_identity_over_d_maxabs"] = (rho - torch.eye(2**k, dtype=rho.dtype, device=DEVICE) / 2**k).abs().max().item()
        row["abs_err_nats"] = abs(row["S_R_numeric_nats"] - row["S_R_exact_nats"])
        rows.append(row)
    return rows


def table(N):
    rows = []
    cfile = os.path.join(RESULTS, f"c_evap_isometry_N{N}.json")
    c = json.load(open(cfile)) if os.path.exists(cfile) else None
    for k in range(0, N + 1):
        hawking = pairs.hawking_entropy(k)
        cap = pairs.bh_capacity(N, k)
        page = P.page_entropy(2**k, 2 ** (N - k))
        r = {"k": k, "hawking_S_R_nats": hawking, "bh_capacity_nats": cap, "page_nats": page,
             "unitary_bound_min_nats": min(k, N - k) * LOG2,
             "hawking_minus_capacity_nats": hawking - cap, "hawking_exceeds_capacity": bool(hawking > cap + 1e-12),
             "hawking_bits": k, "capacity_bits": N - k, "page_bits": page / LOG2}
        if c is not None:
            r["C_mean_S_R_nats"] = 0.0 if k == 0 else c["S_R_mean"][k - 1]
            r["C_std_S_R_nats"] = 0.0 if k == 0 else c["S_R_std"][k - 1]
            r["hawking_minus_C_nats"] = hawking - r["C_mean_S_R_nats"]
        rows.append(r)
    first = next((r["k"] for r in rows if r["hawking_exceeds_capacity"]), None)
    return {"N": N, "page_time_k": N / 2, "first_k_exceeding_capacity": first, "C_seeds": c["seeds"] if c else None,
            "final_hawking_S_R_nats": N * LOG2, "final_unitary_S_R_nats": 0.0, "rows": rows}


def plot(tabs):
    from eh.plotting import AMBER, CYAN, FG, GREEN, MAGENTA, PALETTE, apply_theme, save

    plt = apply_theme()
    fig, ax = plt.subplots(1, 2, figsize=(14, 5.2))
    main = [t for t in tabs if "C_mean_S_R_nats" in t["rows"][0]]
    good = [t for t in main if t.get("C_seeds", 0) >= 20]  # main panel: largest N with >= 20 evaporation seeds
    T = good[-1] if good else (main[-1] if main else tabs[-1])
    N = T["N"]; k = np.array([r["k"] for r in T["rows"]])
    ax[0].plot(k, [r["hawking_bits"] for r in T["rows"]], "-o", ms=3, color=MAGENTA, label="D: Hawking Bell pairs, S(R) = k log 2 (exact)")
    ax[0].plot(k, [r["capacity_bits"] for r in T["rows"]], "--", color=AMBER, label="black-hole capacity log dim B = (N-k) log 2")
    ax[0].plot(k, [r["page_bits"] for r in T["rows"]], "-", color=CYAN, lw=1.2, label="Page's formula (Haar state on R (x) B)")
    if "C_mean_S_R_nats" in T["rows"][0]:
        m = np.array([r["C_mean_S_R_nats"] for r in T["rows"]]) / LOG2; s = np.array([r["C_std_S_R_nats"] for r in T["rows"]]) / LOG2
        ax[0].fill_between(k, m - s, m + s, color=GREEN, alpha=0.35)
        ax[0].plot(k, m, "s", ms=4, color=GREEN, label=f"C: sequential Haar evaporation, mean ± 1 std ({T['C_seeds']} seeds)")
    ax[0].axvline(N / 2, color=FG, ls=":", lw=0.8); ax[0].text(N / 2 + 0.15, 0.3, "Page time k = N/2", fontsize=8)
    kk = k[k >= N / 2]
    ax[0].fill_between(kk, N - kk, kk, color=MAGENTA, alpha=0.10, label="excess: S(R) > log dim B (impossible if R∪B pure)")
    ax[0].set_xlabel("k = emitted qubits"); ax[0].set_ylabel("entropy  [bits]"); ax[0].set_title(f"N = {N}: independent Hawking pairs vs unitary evaporation"); ax[0].legend(fontsize=7.5)
    for i, t in enumerate(tabs):
        kk = np.array([r["k"] for r in t["rows"]]) / t["N"]
        ax[1].plot(kk, [r["hawking_minus_capacity_nats"] / (t["N"] * LOG2) for r in t["rows"]], "-", color=PALETTE[i % len(PALETTE)], lw=1, alpha=0.6)
        if "hawking_minus_C_nats" in t["rows"][0]:
            ax[1].plot(kk, [r["hawking_minus_C_nats"] / (t["N"] * LOG2) for r in t["rows"]], "o", ms=3, color=PALETTE[i % len(PALETTE)], label=f"N={t['N']}")
    ax[1].plot([], [], "-", color=FG, lw=1, label="lines: (S_D - log dim B)/(N log 2) = 2k/N - 1")
    ax[1].plot([], [], "o", ms=3, color=FG, label="dots: (S_D - <S_C>)/(N log 2)")
    ax[1].axhline(0, color=FG, lw=0.6); ax[1].axvline(0.5, color=FG, ls=":", lw=0.8)
    ax[1].set_xlabel("k / N  [fraction emitted]"); ax[1].set_ylabel("entropy difference / (N log 2)  [dimensionless]")
    ax[1].set_title("Where the two models part ways"); ax[1].legend(fontsize=6.5, ncol=3, loc="upper left")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    save(fig, os.path.join(FIGURES, "d_hawking_pairs.png"),
         "Assumptions: D = k independent Bell pairs (partner space grows as 2^k, no interaction between emissions); C = fixed 2^N-dim pure state, Haar scrambling of the remaining qubits; toy models only, no gravity.")


def main():
    ver = verify()
    max_err = max(r["abs_err_nats"] for r in ver)
    max_err2 = max(abs(r.get("S_R_statevector_route_nats", r["S_R_exact_nats"]) - r["S_R_exact_nats"]) for r in ver)
    Ns = sorted({int(os.path.basename(f).split("_N")[1].split(".")[0]) for f in glob.glob(os.path.join(RESULTS, "c_evap_isometry_N*.json"))}) or [12]
    tabs = [table(N) for N in Ns]
    out = {"problem": "D", "classification": "1 (reproduction of the standard pair-creation toy argument) / 2 (exact relation S(R)=k log 2 verified)",
           "env": env_info(), "seeds": "none (deterministic states)", "clip": E.CLIP, "units": "nats (bits also stored)",
           "verification": ver, "max_abs_err_S_R_nats": max_err, "max_abs_err_S_R_statevector_route_nats": max_err2,
           "monotone": all(ver[i + 1]["S_R_numeric_nats"] > ver[i]["S_R_numeric_nats"] for i in range(len(ver) - 1)),
           "tables": tabs,
           "assumptions_producing_the_difference": [
               "D: every emission creates a FRESH maximally entangled pair; the global state is a product over emission steps, so emitted qubits are mutually uncorrelated and rho_R is exactly maximally mixed.",
               "D: the partner (interior) Hilbert space grows by a factor 2 per emission (dim 2^k) and is never constrained by the shrinking black-hole capacity 2^(N-k); nothing ever returns the partners' entanglement to the outside.",
               "C: the total Hilbert space is fixed (2^N), the global state stays pure, the remaining black hole has dim 2^(N-k) and is unitarily scrambled before each emission; hence S(R) = S(B) <= min(k, N-k) log 2 and late qubits are correlated with early radiation.",
               "The curves agree up to O(2^(2k-N)) for k < N/2 and differ by (2k-N) log 2 + O(1) for k > N/2; neither toy model contains gravity or says which assumption nature violates."]}
    dump("d_hawking_pairs.json", out)
    plot(tabs)
    log(f"D: max |S_numeric - k log 2| = {max_err:.2e} (matrix route, k<=12), {max_err2:.2e} (state-vector route, k<=10); Ns={Ns}")


if __name__ == "__main__":
    main()
