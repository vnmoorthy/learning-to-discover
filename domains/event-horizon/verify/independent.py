#!/usr/bin/env python
"""Independent verification of the Event Horizon key numbers.

Deliberately does NOT import the builders' `eh` package.  Different methods on purpose:
  * Haar unitaries from scipy.stats.unitary_group (not QR-of-Ginibre code of the builders);
  * CPU numpy only, RNG = numpy Philox bit generator, seeds 9xxxxx (builders: torch / PCG64);
  * Page values from exact rational arithmetic (fractions.Fraction);
  * entropies from eigvalsh of density matrices built with EXPLICIT-LOOP partial traces
    (small sizes) and cross-checked against SVD Schmidt coefficients;
  * eigenvalues <= CLIP = 1e-14 dropped before the log (never log 0).  Units: nats.

Sections
  V1  Page formula vs Monte Carlo at 7 (m, n)
  V2  sequential Haar evaporation N = 8 vs exact Page and vs the builders' JSON
  V3  Bell-pair model S(R) = k ln 2
  V4  Hayden-Preskill, old black hole, k = 1, n_B = 4, m = 0..5 vs the builders' JSON
      (+ decoupling bound, + Yoshida-Kitaev decoder simulated literally)
  V5  local-Haar brickwork evaporation N = 8, depth 2 per emission vs the builders' JSON
  V6  stabilizer (Clifford) states: flat spectra, half-cut entropy vs Page
Usage:  python verify/independent.py [--out results/verification_raw.json]
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from fractions import Fraction

import numpy as np
from scipy.stats import unitary_group

assert "eh" not in sys.modules
CLIP = 1e-14
LN2 = math.log(2.0)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def rng_for(tag: int) -> np.random.Generator:
    return np.random.Generator(np.random.Philox(key=900000 + tag))


# ------------------------------------------------------------------ primitives
def vn(p) -> float:
    p = np.asarray(p, dtype=float)
    p = p[p > CLIP]
    return float(-(p * np.log(p)).sum())


def page_exact(m: int, n: int) -> Fraction:
    """Page 1993: sum_{j=n+1}^{mn} 1/j - (m-1)/(2n), m <= n, exact rational."""
    if m > n:
        m, n = n, m
    s = Fraction(0)
    for j in range(n + 1, m * n + 1):
        s += Fraction(1, j)
    return s - Fraction(m - 1, 2 * n)


def ptrace_loop(psi: np.ndarray, m: int, n: int) -> np.ndarray:
    """rho_R[a, a'] = sum_b psi[a n + b] conj(psi[a' n + b]) with explicit Python loops."""
    rho = np.zeros((m, m), dtype=complex)
    for a in range(m):
        for a2 in range(m):
            acc = 0j
            for b in range(n):
                acc += psi[a * n + b] * np.conj(psi[a2 * n + b])
            rho[a, a2] = acc
    return rho


def haar_state_scipy(D: int, rng) -> np.ndarray:
    """First column of a scipy Haar unitary (D <= 512), else normalised complex Gaussian."""
    if D <= 512:
        return unitary_group.rvs(D, random_state=rng)[:, 0].copy()
    v = rng.standard_normal(D) + 1j * rng.standard_normal(D)
    return v / np.linalg.norm(v)


def summary(x):
    x = np.asarray(x, dtype=float)
    return float(x.mean()), float(x.std(ddof=1) / math.sqrt(len(x)))


# ------------------------------------------------------------------ V1
def v1_page(n_samples=4000):
    out = []
    for i, (m, n) in enumerate([(2, 2), (2, 8), (3, 5), (4, 4), (8, 16), (16, 16), (32, 64)]):
        rng = rng_for(100 + i)
        ns = n_samples if m * n <= 512 else 1500
        S = np.empty(ns)
        max_route_diff = 0.0
        for s in range(ns):
            psi = haar_state_scipy(m * n, rng)
            sv = np.linalg.svd(psi.reshape(m, n), compute_uv=False)
            S[s] = vn(sv ** 2)
            if s < 20 and m * n <= 256:   # second route: explicit-loop partial trace + eigvalsh, both sides
                sR = vn(np.linalg.eigvalsh(ptrace_loop(psi, m, n)))
                sB = vn(np.linalg.eigvalsh(ptrace_loop(psi.reshape(m, n).T.reshape(-1), n, m)))
                max_route_diff = max(max_route_diff, abs(sR - S[s]), abs(sB - S[s]))
        mean, se = summary(S)
        ex = page_exact(m, n)
        out.append({"m": m, "n": n, "samples": ns, "page_exact_fraction": f"{ex.numerator}/{ex.denominator}"
                    if len(str(ex.denominator)) < 40 else "long", "page_exact_nats": float(ex),
                    "page_exact_bits": float(ex) / LN2, "mc_mean_nats": mean, "mc_stderr": se,
                    "z": (mean - float(ex)) / se, "max_abs_diff_SVD_vs_loop_ptrace_R_and_B": max_route_diff})
        print("V1", out[-1], flush=True)
    return out


# ------------------------------------------------------------------ V2
def v2_evaporation(N=8, n_traj=400):
    """Literal protocol: fresh scipy Haar unitary on the remaining hole, then emit one qubit.
    Convention here (differs from the builders on purpose): hole qubits are the LEADING tensor
    factors, the emitted qubit is the last hole qubit."""
    rng = rng_for(200)
    S = np.zeros((n_traj, N + 1))
    SB = np.zeros((n_traj, N + 1))
    for s in range(n_traj):
        psi = np.zeros(2 ** N, dtype=complex)
        psi[0] = 1.0
        for t in range(N):
            nrem = N - t
            U = unitary_group.rvs(2 ** nrem, random_state=rng) if nrem > 0 else np.eye(1)
            M = psi.reshape(2 ** nrem, 2 ** t)          # rows: hole, cols: radiation
            psi = (U @ M).reshape(-1)
            Mcut = psi.reshape(2 ** (nrem - 1), 2 ** (t + 1))   # hole' | radiation (t+1 qubits)
            rhoR = Mcut.T @ Mcut.conj()                 # radiation density matrix
            rhoB = Mcut @ Mcut.conj().T
            S[s, t + 1] = vn(np.linalg.eigvalsh(rhoR))
            SB[s, t + 1] = vn(np.linalg.eigvalsh(rhoB))
    page = [float(page_exact(2 ** t, 2 ** (N - t))) for t in range(N + 1)]
    mean = S.mean(0)
    se = S.std(0, ddof=1) / math.sqrt(n_traj)
    res = {"N": N, "trajectories": n_traj, "t": list(range(N + 1)), "page_exact_nats": page,
           "S_R_mean": mean.tolist(), "S_R_stderr": se.tolist(),
           "z_vs_page": [0.0] + [float((mean[t] - page[t]) / se[t]) for t in range(1, N)] + [0.0],
           "max_abs_SR_minus_SB": float(np.abs(S - SB).max()),
           "corr_consecutive": [float(np.corrcoef(S[:, t], S[:, t + 1])[0, 1]) for t in range(1, N - 1)]}
    for mode in ("full", "isometry"):
        f = os.path.join(ROOT, "results", f"c_evap_{mode}_N{N}.json")
        if os.path.exists(f):
            b = json.load(open(f))
            zs = []
            for i, t in enumerate(b["t"]):
                if 0 < t < N:
                    zs.append(float((mean[t] - b["S_R_mean"][i]) / math.hypot(se[t], b["S_R_stderr"][i])))
            res[f"z_vs_builder_{mode}"] = zs
            res[f"builder_{mode}_mean"] = b["S_R_mean"]
            res[f"builder_{mode}_seeds"] = b["seeds"]
    print("V2", json.dumps(res), flush=True)
    return res


# ------------------------------------------------------------------ V3
def v3_bell(kmax=6):
    out = []
    for k in range(0, kmax + 1):
        nq = 2 * k                       # qubit order r1 p1 r2 p2 ...
        psi = np.zeros(2 ** nq, dtype=complex)
        amp = 2.0 ** (-k / 2)
        for bits in range(2 ** k):       # each pair is 00 or 11
            idx = 0
            for j in range(k):
                b = (bits >> j) & 1
                idx = (idx << 2) | (3 if b else 0)
            psi[idx] = amp
        # explicit-loop partial trace over the partner qubits (odd positions)
        dR = 2 ** k
        rho = np.zeros((dR, dR), dtype=complex)
        nz = np.nonzero(psi)[0]

        def split(i):
            r = p = 0
            for j in range(k):
                pair = (i >> (2 * (k - 1 - j))) & 3
                r = (r << 1) | (pair >> 1)
                p = (p << 1) | (pair & 1)
            return r, p
        sp = [split(int(i)) for i in nz]
        for (r1, p1), i1 in zip(sp, nz):
            for (r2, p2), i2 in zip(sp, nz):
                if p1 == p2:
                    rho[r1, r2] += psi[i1] * np.conj(psi[i2])
        ev = np.linalg.eigvalsh(rho)
        S = vn(ev)
        out.append({"k": k, "S_R_nats": S, "k_ln2": k * LN2, "abs_err": abs(S - k * LN2),
                    "S_R_bits": S / LN2, "max_dev_from_flat": float(np.abs(ev - 2.0 ** -k).max()),
                    "offdiag_max": float(np.abs(rho - np.diag(np.diag(rho))).max())})
    print("V3", out, flush=True)
    return out


# ------------------------------------------------------------------ V4
def v4_hayden_preskill(k=1, n_B=4, n_seeds=400):
    """Old black hole.  Psi[r, e, o] = U[o, (a=r, b=e)] / sqrt(d);  o = (b', d), D = last m qubits."""
    n = k + n_B
    d, dR, dE = 2 ** n, 2 ** k, 2 ** n_B
    rng = rng_for(400)
    ms = list(range(0, n + 1))
    keys = ("I_R_ED", "I_R_Bp", "T", "F_EPR", "P_EPR", "purity_RBp", "F_uhl")
    acc = {q: np.zeros((n_seeds, len(ms))) for q in keys}
    for s in range(n_seeds):
        U = unitary_group.rvs(d, random_state=rng)
        for mi, m in enumerate(ms):
            dD, dBp = 2 ** m, 2 ** (n - m)
            T = (U.reshape(dBp, dD, dR, dE) / math.sqrt(d))          # [b', d, r, e]
            # density matrices by explicit index contraction (einsum = sum over traced labels)
            rho_RBp = np.einsum("bdre,cdse->rbsc", T, T.conj()).reshape(dR * dBp, dR * dBp)
            rho_R = np.einsum("bdre,bdse->rs", T, T.conj())
            rho_Bp = np.einsum("bdre,cdre->bc", T, T.conj())
            rho_ED = np.einsum("bdre,bfrg->edgf", T, T.conj()).reshape(dE * dD, dE * dD)
            S_R, S_Bp = vn(np.linalg.eigvalsh(rho_R)), vn(np.linalg.eigvalsh(rho_Bp))
            S_RBp, S_ED = vn(np.linalg.eigvalsh(rho_RBp)), vn(np.linalg.eigvalsh(rho_ED))
            # global purity: S(RED) = S(B'), S(ED) = S(RB')
            acc["I_R_ED"][s, mi] = S_R + S_ED - S_Bp
            acc["I_R_Bp"][s, mi] = S_R + S_Bp - S_RBp
            sigma = np.kron(rho_R, rho_Bp)
            acc["T"][s, mi] = 0.5 * np.abs(np.linalg.eigvalsh(rho_RBp - sigma)).sum()
            acc["purity_RBp"][s, mi] = float(np.real(np.trace(rho_RBp @ rho_RBp)))
            # Uhlmann fidelity F(rho, sigma) = (tr sqrt(sqrt(sigma) rho sqrt(sigma)))^2; sigma = 1/D here
            w, v = np.linalg.eigh(sigma)
            sq = (v * np.sqrt(np.clip(w, 0, None))) @ v.conj().T
            acc["F_uhl"][s, mi] = float(np.sqrt(np.clip(np.linalg.eigvalsh(sq @ rho_RBp @ sq), 0, None)).sum() ** 2)
            # Yoshida-Kitaev decoder simulated literally:
            #  Bob: |Bell>_{A'R'}, U* on (A', E) -> (B'', D'), project D D' on Bell.
            Us = U.conj().reshape(dBp, dD, dR, dE)
            amp = np.einsum("bdre,cfse->rbdcfs", T, Us) / math.sqrt(dR)      # [r, b', d, b'', d', r']
            Phi = np.einsum("rbdcds->rbcs", amp) / math.sqrt(dD)             # <Bell_DD'| applied
            P = float(np.real(np.vdot(Phi, Phi)))
            ov = np.einsum("rbcr->bc", Phi) / math.sqrt(dR)                  # <Bell_RR'| applied
            acc["P_EPR"][s, mi] = P
            acc["F_EPR"][s, mi] = float(np.real(np.vdot(ov, ov))) / P
    res = {"k": k, "n_B": n_B, "n_seeds": n_seeds, "m": ms}
    for q in keys:
        res[q + "_mean"] = acc[q].mean(0).tolist()
        res[q + "_stderr"] = (acc[q].std(0, ddof=1) / math.sqrt(n_seeds)).tolist()
    # analytic checks derived independently here
    res["two_k_ln2"] = 2 * k * LN2
    res["bound_half_sqrt_D_EP_minus_1_using_MC_purity"] = [
        0.5 * math.sqrt(max(dR * 2 ** (n - m) * res["purity_RBp_mean"][i] - 1.0, 0.0)) for i, m in enumerate(ms)]
    res["bound_closed_form"] = [0.5 * math.sqrt((dR ** 2 - 1) * (4.0 ** -m - 1.0 / d ** 2) / (1 - 1.0 / d ** 2)) for m in ms]
    res["bound_asymptotic_half_2^(k-m)"] = [0.5 * 2.0 ** (k - m) for m in ms]
    res["bound_holds"] = bool(all(res["T_mean"][i] <= res["bound_closed_form"][i] + 3 * res["T_stderr"][i] + 1e-12
                                  for i in range(len(ms))))
    res["fuchs_vdg_holds_F_ge_(1-T)^2"] = bool((acc["F_uhl"] >= (1 - acc["T"]) ** 2 - 1e-9).all())
    res["I_sum_identity_max_err"] = float(np.abs(acc["I_R_ED"] + acc["I_R_Bp"] - 2 * k * LN2).max())
    f = os.path.join(ROOT, "results", "e2_hayden_preskill.json")
    if os.path.exists(f):
        j = json.load(open(f))
        for r in j["records"]:
            if r["kind"] == "old" and r["variant"] == "old_haar" and r["k"] == k and r["n_B"] == n_B:
                nb = r["n_seeds"]
                cmpd = {}
                for mine, theirs in (("I_R_ED", "I_R_ED"), ("I_R_Bp", "I_R_Bp"), ("T", "T_prod"),
                                     ("F_EPR", "F_EPR"), ("P_EPR", "P_EPR"), ("F_uhl", "F_uhl")):
                    zs = []
                    for i, m in enumerate(ms):
                        bi = r["m"].index(m)
                        bm, bs = r[theirs]["mean"][bi], r[theirs]["std"][bi]
                        if bm is None or bs is None:
                            zs.append(None)
                            continue
                        se = math.hypot(res[mine + "_stderr"][i], bs / math.sqrt(nb))
                        zs.append(float((res[mine + "_mean"][i] - bm) / se) if se > 1e-13 else
                                  float(res[mine + "_mean"][i] - bm))
                    cmpd[mine] = {"builder_mean": [r[theirs]["mean"][r["m"].index(m)] for m in ms],
                                  "z_or_absdiff_if_deterministic": zs}
                res["vs_builder"] = cmpd
                res["builder_n_seeds"] = nb
                res["builder_thresholds"] = r.get("thresholds")
    I = res["I_R_ED_mean"]
    res["verifier_thresholds"] = {
        "m_I90": next(m for i, m in enumerate(ms) if I[i] >= 0.9 * 2 * k * LN2),
        "m_I99": next(m for i, m in enumerate(ms) if I[i] >= 0.99 * 2 * k * LN2),
        "m_T10": next(m for i, m in enumerate(ms) if res["T_mean"][i] <= 0.1)}
    print("V4", json.dumps(res), flush=True)
    return res


# ------------------------------------------------------------------ V5
def apply_2q(state, g, i, n):
    """state: tensor (2,)*n ; g: 4x4 acting on qubits (i, i+1)."""
    t = np.tensordot(g.reshape(2, 2, 2, 2), state, axes=([2, 3], [i, i + 1]))
    return np.moveaxis(t, [0, 1], [i, i + 1])


def v5_local_brickwork(N=8, depth=2, n_seeds=400):
    """`depth` brickwork layers of scipy-Haar 2-qubit gates on the remaining hole (qubits 0..n_rem-1, open
    chain, layer parity continues across emissions, even layers start at bond (0,1)), then emit the last
    remaining qubit.  Same model as the builders' 'local_haar' family; independent code and RNG."""
    rng = rng_for(500)
    S = np.zeros((n_seeds, N + 1))
    for s in range(n_seeds):
        st = np.zeros((2,) * N, dtype=complex)
        st[(0,) * N] = 1.0
        layer = 0
        for t in range(N):
            nrem = N - t
            for _ in range(depth):
                for i in range(layer % 2, nrem - 1, 2):
                    st = apply_2q(st, unitary_group.rvs(4, random_state=rng), i, N)
                layer += 1
            sv = np.linalg.svd(st.reshape(2 ** (nrem - 1), 2 ** (t + 1)), compute_uv=False)
            S[s, t + 1] = vn(sv ** 2)
    mean, se = S.mean(0), S.std(0, ddof=1) / math.sqrt(n_seeds)
    page = np.array([float(page_exact(2 ** t, 2 ** (N - t))) for t in range(N + 1)])
    res = {"N": N, "depth": depth, "n_seeds": n_seeds, "S_mean": mean.tolist(), "S_stderr": se.tolist(),
           "max_dev_from_page": float((page - mean).max()), "argmax_t": int((page - mean).argmax())}
    f = os.path.join(ROOT, "results", "e1_scrambling.json")
    if os.path.exists(f):
        j = json.load(open(f))
        for r in j["runs"]:
            if r["N"] == N and r["family"] == "local_haar" and r["depth"] == depth:
                bse = np.array(r["S_vn_ci95"]) / 1.96
                z = [(float((mean[t] - r["S_vn_mean"][t]) / math.hypot(se[t], bse[t]))) for t in range(1, N)]
                res.update({"builder_S_mean": r["S_vn_mean"], "builder_n_seeds": r["n_seeds"],
                            "builder_max_dev": r["max_dev_from_page"], "z_vs_builder": z})
    print("V5", json.dumps(res), flush=True)
    return res


# ------------------------------------------------------------------ V6
def v6_clifford(N=10, layers=60, n_seeds=300):
    """Random stabilizer states from deep brickwork of random 2-qubit Clifford words (each gate = product of
    12 random generators from {H, S on either qubit, CNOT both directions}); deep circuit => close to a
    uniformly random stabilizer state.  Checks: spectra flat (vN = Renyi-2 = ln rank), entropies are integer
    bits, mean half-cut entropy vs Page."""
    rng = rng_for(600)
    H = np.array([[1, 1], [1, -1]]) / math.sqrt(2)
    Sg = np.diag([1, 1j])
    I2 = np.eye(2)
    CX = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)
    SW = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], dtype=complex)
    gens = [np.kron(H, I2), np.kron(I2, H), np.kron(Sg, I2), np.kron(I2, Sg), CX, SW @ CX @ SW]
    half = np.zeros(n_seeds)
    max_flat_err = 0.0
    max_nonint = 0.0
    for s in range(n_seeds):
        st = np.zeros((2,) * N, dtype=complex)
        st[(0,) * N] = 1.0
        for layer in range(layers):
            for i in range(layer % 2, N - 1, 2):
                g = np.eye(4, dtype=complex)
                for w in rng.integers(0, 6, size=12):
                    g = gens[w] @ g
                st = apply_2q(st, g, i, N)
        for cut in range(1, N):
            p = np.linalg.svd(st.reshape(2 ** cut, 2 ** (N - cut)), compute_uv=False) ** 2
            p = p[p > 1e-10]
            sv, s2 = vn(p), -math.log(float((p ** 2).sum()))
            max_flat_err = max(max_flat_err, abs(sv - s2), abs(sv - math.log(len(p))))
            max_nonint = max(max_nonint, abs(sv / LN2 - round(sv / LN2)))
            if cut == N // 2:
                half[s] = sv
    mean, se = summary(half)
    page = float(page_exact(2 ** (N // 2), 2 ** (N - N // 2)))
    vals, cnt = np.unique(np.round(half / LN2).astype(int), return_counts=True)
    # exact 2-design consistency: E[2^-S_bits] must equal the Haar mean purity (m+n)/(mn+1)
    mm = 2 ** (N // 2)
    # reference (heuristic, not a cited theorem): corank law of a uniformly random n x n GF(2) matrix
    nh = N // 2
    def n_rank(k):
        num = 1.0
        for i in range(k):
            num *= (2.0 ** nh - 2.0 ** i) ** 2 / (2.0 ** k - 2.0 ** i)
        return num
    gf2 = {nh - k: n_rank(k) / 2.0 ** (nh * nh) for k in range(nh + 1)}   # deficit (bits) -> probability
    gf2_mean_deficit_nats = sum(r * pr for r, pr in gf2.items()) * LN2
    res = {"N": N, "layers": layers, "n_seeds": n_seeds, "max_abs_vN_minus_Renyi2_or_lnrank": max_flat_err,
           "gf2_corank_reference_probs_by_deficit_bits": {int(r): pr for r, pr in sorted(gf2.items())},
           "gf2_reference_mean_half_cut_nats": nh * LN2 - gf2_mean_deficit_nats,
           "gf2_reference_minus_page_nats": nh * LN2 - gf2_mean_deficit_nats - page,
           "max_distance_from_integer_bits": max_nonint, "half_cut_mean_nats": mean, "half_cut_stderr": se,
           "page_half_nats": page, "stabilizer_minus_page_nats": mean - page,
           "half_cut_bits_histogram": {int(v): int(c) for v, c in zip(vals, cnt)},
           "mean_purity": float(np.mean(np.exp(-half))), "haar_mean_purity_exact": (2 * mm) / (mm * mm + 1.0)}
    print("V6", json.dumps(res), flush=True)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "results", "verification_raw.json"))
    ap.add_argument("--quick", action="store_true")
    a = ap.parse_args()
    q = 0.25 if a.quick else 1.0
    t0 = time.time()
    res = {"script": "verify/independent.py", "numpy": np.__version__, "rng": "numpy Philox, key = 900000 + tag",
           "clip": CLIP, "units": "nats",
           "V1_page": v1_page(int(4000 * q)),
           "V2_evaporation_N8": v2_evaporation(8, int(400 * q)),
           "V3_bell": v3_bell(6),
           "V4_hayden_preskill": v4_hayden_preskill(1, 4, int(400 * q)),
           "V5_local_brickwork": v5_local_brickwork(8, 2, int(400 * q)),
           "V6_clifford": v6_clifford(10, 60, int(800 * q))}
    res["runtime_s"] = time.time() - t0
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump(res, open(a.out, "w"), indent=1)
    print("wrote", a.out, "runtime", res["runtime_s"])


if __name__ == "__main__":
    main()
