# EVENT HORIZON: technical research audit (pre-upgrade)

Auditor pass, 2026-11-15, 12:53 to 13:05 PST. Scope: the state marked by tag `eh-pre-upgrade-checkpoint`.
This audit is read-only. Its only output is this file. Sources read: `eh/*.py`, `paper/event_horizon.md`
(Secs. 4 to 10), `notes/critic.md`, `results/verification.json` (head), `meta.json`, and `results/dashboard.json`
(keys only). Re-run during the audit: `pytest tests` gave **109 passed in 59.1 s** on this Mac
(`/opt/anaconda3/bin/python3`, `-p no:cacheprovider`, no files written).

Separation of levels, as used throughout: **[C]** finite-dimensional circuit model, **[RMT]** random-matrix or Haar
ensemble result, **[SG]** semiclassical gravity formula, **[H]** holographic interpretation. Nothing in the
codebase tests [SG] or [H]. No circuit result here proves the island formula or resolves the information paradox.

---

## 1. Implemented models

| Model | Where | Level | What is computed | Analytic reference in code |
|---|---|---|---|---|
| Haar pure state on C^m ⊗ C^n | `eh/qstates.py`, `eh/page.py` | RMT | S_vN, purity and Rényi-2 of the smaller factor | Page 1993; exact Fraction value, digamma for large mn; expansion to O(n^-4), checked with SymPy and 60-digit mpmath |
| Page curve on N qubits | `experiments/a_page_curve.py` | RMT | S(R) vs k = 0..N, N = 8..24 | `page_curve(N)` |
| Sequential Haar evaporation | `eh/evaporation.py` (emits the **first** hole qubit), `eh/circuits.evaporate("haar")` (emits the **last**) | C, with RMT reference | S(R), S(B), λ spectra per step, N ≤ 14 literal, N ≤ 27 via isometry | Exact-Haar argument (paper §4.4) |
| Bell-pair "Hawking" model | `eh/pairs.py` | C (toy) | S(R) = k ln 2, flat spectrum, capacity (N−k) ln 2 | Exact |
| Brickwork local scramblers (Haar 2-qubit, Clifford 2-qubit from an enumerated 11 520-element group, SWAP, H+CNOT, identity) | `eh/circuits.py` | C | Per-emission depth sweeps, one-shot depth D*, spacing ratio, vN vs Rényi-2 | **None** (class 3, no analytic reference) |
| Hayden-Preskill, old hole (Choi state of U) and young hole (isometry) | `eh/hayden_preskill.py` | C, with RMT bounds | I(R:ED), trace distances T_prod and T_mm, Uhlmann F, Yoshida-Kitaev P_EPR and F_EPR | Exact Weingarten second moments (old and young), decoupling bound ½√(D·E[P]−1), YK identities P·F = 1/d_A² |
| Independent verifier | `verify/independent.py` | – | Re-implements A, B, C (N = 8), D, E1 (N = 8, depth 2), E2 (k = 1, n_B = 4), Clifford flatness | Exact rationals; scipy `unitary_group` |

## 2. Simulations and outputs (as stored)

* **A**: 213 (N, k) cells, max |z| 3.38 (N = 24, 8 states), rms z 1.05; |S(R) − S(B)| ≤ 5.3e-15. Seeds and samples per N are in `results/a_page_curve.json`.
* **B**: 124 (m, n) pairs up to mn = 2^24, max |z| 2.69. The asymptotic-error table is in `results/b_page_theorem_table.md`.
* **C**: literal protocol for N = 6..14 (files `c_evap_full_N*.json`) and the isometry sampler for N = 6..27; KS tests at N = 8 and 10; the z = 4.19 outlier was followed up with 1000 seeds (z → 1.36); two controls that do differ from Page (`c_variants_N6.json`).
* **D**: k = 0..12, error ≤ 8.9e-15; crossing at k = ⌊N/2⌋+1 for N = 6..26.
* **E1**: depth table N = 8..26 × depth {1, 2, 4, 8, 16}; one-shot D* fit 1.87 N + 1.9 (9 points, no error bars); Clifford half-cut offset −0.088 ± 0.015 nats (N = 10, 800 states).
* **E2**: Haar thresholds m_I90, m_I99, m_T10 for k = 1..3 and n_B = 3..12; young-hole shift ≈ n_B/2; local-scrambler HP at one size (10 qubits, 32 seeds).
* Figures: 16 PNGs in `figures/`, including 3 laptop-era `e1_cpu_*`. Summary files: `results/dashboard.json`, `results/research_log.json` and `results/verification.json` (8 of 9 claims agree; the one that did not, the Clifford sign, was corrected).

## 3. Tests

109 pass (re-run here; 59 s locally, 21 s reported on the verifier machine). They come from 51 test functions (16 in `test_core`, 5 in `test_evaporation` and 30 in `test_ext`), with parametrisation giving 109 cases. Coverage is good for:
Page exact vs asymptotic; Haar phase fix; `haar_apply` ≡ `haar_unitary` (same RNG stream); S(R) = S(B);
Clifford group order and Pauli-normaliser; YK closed form vs brute-force state vector; Weingarten purities vs MC.

**Gaps in testing:**
1. No test pins the **emission-order convention**. `evaporation.py` emits the first hole qubit and `circuits.py` emits the last. The two agree for Haar dynamics but not for local circuits.
2. No test of the torch/GPU paths against numpy at the **sizes actually reported** (N ≥ 20). The Gram-matrix `eigvalsh` with `GRAM_CLIP = 1e-13` is justified by an error bound in a comment, not by a test.
3. No regression test that the stored JSON numbers can be regenerated from their recorded seeds.
4. Nothing tests E1's per-emission depth or D* against an analytic value, because none exists in the code (see Improvement 1).

## 4. Incomplete features

* The literal sequential protocol stops at N = 14. Every larger N result for C (and E1's `haar_shortcut`) is a reference Page curve, not a test of the dynamics (critic, paper §9).
* The z = 3.38 (A, N = 24) and z = 3.65 (C, N = 26) cells were **not followed up**.
* E1: d* and D* have no error bars, and the depth grid {1, 2, 4, 8, 16} does not resolve the threshold, which lies near depth 8. Clifford N ≥ 22 has 4 to 12 seeds.
* E2: `m_F90 = None` in most young-hole records (dense F_uhl is capped at `max_dim = 1024`). Trace distances are unavailable whenever d_R·d_B' > 1024. Local-scrambler HP was run at one size and one geometry.
* No `notes/` derivation for E1 and E2 (it lives in §4.6 and in a JSON string). No PDF (no pandoc).
* The verifier re-ran only small CPU points. The GPU numbers at N ≥ 20 were checked for internal consistency only.
* Hygiene: leftover `*_cpu.py`, `c_modal.py`, `modal_run.py`, `results/c_log_*`, `results/gpu_keep_*` and `figures/e1_cpu_*`. These must not be deleted under the upgrade rules, but they should be labelled as superseded.

## 5. Incorrect or oversimplified assumptions

None of the following are numerical bugs; the computations are right for the stated models. They limit what may be claimed.

1. **Infinite-temperature, all-to-all scrambler [C/RMT].** "Haar on the whole remaining hole" has no energy, no conserved charge, no greybody factor and no locality. The radiation is maximally mixed per qubit at every step. Real Hawking radiation is thermal at T_H and energy-conserving. Any agreement with the [SG] Page curve is an agreement of *shape* only.
2. **The "sequential = exactly Haar" result makes Problem C logically redundant with A.** It holds for *any* unitarily invariant ensemble (a later unitary on B ⊗ 1_R leaves the radiation entropies invariant, and Haar measure is invariant). The only non-trivial dynamics in the repo is E1 (local circuits). The project should present C as a *proof plus check*, not as an independent discovery.
3. **"Page time" means k = N/2 emitted qubits**, not a time. Nothing maps k to t; that mapping would need a dE/dt law, which [SG] supplies and [C] does not.
4. **Bell-pair capacity (N − k) ln 2** is an assumption (A4 in `notes/D_derivation.md`). The "violation" is of that assumption set, not of a gravitational bound.
5. **Hayden-Preskill decoder** assumes that Bob knows U exactly, perfect Bell projection and noiseless gates. The decoupling bound is on the Haar *average*, not per instance, and is about one qubit loose. `yk_fidelity_prediction` inserts E[P] into 1/P, which is not E[F].
6. **Statistics.** Pooled z values come from nested cuts of the *same* states, which are correlated (step correlation ≈ 0.45), so "6 % with |z| > 2" is descriptive only. When dim R ≪ dim B, S(R) is strongly skewed, so stderrs from 8 to 40 samples are biased low. This is the likely origin of every |z| > 3 cell. E1's "max over steps of (Page − mean)" is upward-biased at few seeds.
7. **Clifford threshold against Page.** Measuring Clifford circuits against the Haar mean is a category error. The stabilizer ensemble has its own exact mean, which sits below Page, so "d* undefined" says nothing about scrambling speed (critic objection 1). The present comparison number (−0.077 nats from GF(2) corank counting) is labelled a heuristic, not a theorem.
8. **Numerical conventions are duplicated.** There are three Haar samplers (`qstates`, `circuits`, `evaporation.haar_apply`), two `page_entropy` implementations and four clip thresholds (1e-15, 1e-15, 1e-13 Gram, 1e-14 verifier). They are consistent today but fragile. `circuits.page_entropy` also allocates `np.arange(n+1, mn+1)`: about 0.54 GB at N = 26 (half cut) and about 1.07 GB at N = 27. `eh/page.py` (fsum up to 2e6 terms, digamma beyond) has no such cost and should be the one used.

## 6. Bottlenecks

| Component | Scaling | Present limit | Cause |
|---|---|---|---|
| Literal C (dense Haar on 2^(N−k)) | O(8^(N−k)) per step for the QR | N = 14 (N = 15 estimated) | Dense unitary, not needed for radiation entropies (§5.2) |
| Isometry C | memory 2^N × 2^k | N = 27 | Statevector |
| E1 state-vector brickwork | 2^N × batch, complex128 | N = 26 (1 GiB/state) | Monte Carlo: seeds fall to 4 to 8 at N ≥ 24, so CIs widen exactly where the scaling claim needs them |
| E2 dense decoupling metrics | (d_R d_B')^3 eigendecomposition | d_R d_B' ≤ 1024 | Dense `eigvalsh` of 1024 × 1024 and up |
| Monte Carlo error in A, C, E1 | stderr ∝ S^(−1/2), skewed | 8 to 16 samples at the largest N | No exact variance used (§5.6) |
| Compute | – | Box CPUs saturated; GPU 0 shared (< 12 GB/process) | Environment |

The dominant scientific bottleneck is not hardware. **E1 and the large-N cells rely on sampling where exact
second-moment theory is available and cheap.**

---

## 7. The three highest-value mathematical improvements

Ranked by (scientific value to a judge) × (feasibility before the deadline) × (how many open objections it closes).

### Improvement 1: exact annealed Rényi-2 theory for local-circuit evaporation (E1) via the Weingarten domain-wall model

**What.** Averaging two copies of a Haar 2-qubit gate maps the circuit to a classical two-state spin model
(spin ∈ {identity, swap} on each leg). The local rule is exact for q = 2 (Nahum, Vijay and Haah, PRX 8, 021014 (2018);
Zhou and Nahum, PRB 99, 174205 (2019)):
input spins (s, s) → output (s, s) with weight 1; input (s, s̄) → (s, s) or (s̄, s̄), each with weight
K = q/(q²+1) = 2/5. With a top boundary of swap on R and identity on B, propagating this rule backwards through
exactly the gate schedule of `circuits.evaporate("local_haar", depth)` (emitted qubits frozen), and contracting with
the product state |0…0⟩ (weight 1 per site), gives **E[tr ρ_R²] exactly**. The cost is a real 2^N vector per
step, with no sampling and no unitaries.

**Feasibility check done during this audit** (scratch script, not added to the repo, numpy, seed 12345). For N = 8,
depth 2, the exact E[tr ρ_R²] for k = 1..7 is (0.8000, 0.5248, 0.3738, 0.2559, 0.2329, 0.3020, 0.5208). The
Monte Carlo mean of exp(−S₂) over 400 trajectories of `eh.circuits.evaporate` agrees with it at every step:
|z| ≤ 1.21, max |z| at k = 3.
The annealed Rényi-2 curve (0.22, 0.64, 0.98, 1.36, 1.46, 1.20, 0.65 nats) peaks at k = 5, not at N/2 = 4. The Haar
value −ln E[P] (Lubkin) peaks at 2.08 nats at k = 4. Shallow local scrambling **shifts and lowers** the Page
peak, and the theory gives that shape exactly.

**Why this ranks first.**
* It turns E1, currently the only non-trivial dynamics in the project and classed 3 with *no* analytic reference, into
  numerics with an exact [RMT/C] reference at every N, depth and step, for the second moment.
* It is exact up to N ≈ 26 to 28 on one GPU or on the Mac (a 2^26 float64 vector is 0.5 GB). It is independent of the
  shared CPUs and needs no seeds, so it removes the 4-to-8-seed problem at N ≥ 22.
* It yields an analytic prediction for the depth per emission needed to approach −ln E[P_Haar], and for the one-shot
  D*(N) slope (entanglement velocity v₂ = ln((q²+1)/(2q)) per unit circuit time in the bulk, to be re-derived for
  this layer convention). The fitted 1.87 N + 1.9 can then be compared rather than only reported.
* Honest caveat: it gives the **annealed** −ln E[tr ρ²], which is ≤ E[S₂] ≤ E[S_vN]. The quenched gap must be
  measured, not assumed. Classification: 2 (reproduction of a known mapping) for the method; 3 for its comparison
  with the stored E1 data.
* Deliverables: `eh/domain_wall.py`, `experiments/f1_annealed_purity.py` and `tests/test_domain_wall.py`. Minimal
  tests: no-gate case gives 1; single gate gives 2/5-weight values; Haar-depth→∞ limit approaches Lubkin
  (m+n)/(mn+1); MC agreement at N = 6, 8.

### Improvement 2: exact variance of the Page entropy, and correct inference for the skewed, correlated cells

**What.** The exact variance of S_vN for a Haar state on C^m ⊗ C^n is known in closed form (conjectured by Vivo,
Pato and Oshanin, PRE 93, 052106 (2016); proved by Wei, PRE 96, 022106 (2017); see also Bianchi and Donà,
PRD 100, 105010 (2019)). Lubkin's purity has an exact variance from the 4th-moment Weingarten calculus. Implement
`page_variance(m, n)` (exact, digamma and trigamma form) and use it in place of the sample stderr.

**Why.**
* It closes the open objection: every |z| > 3 cell (A N = 24: 3.38; C N = 26: 3.65; the old C N = 13: 4.19) sits in
  the regime where 8 to 40 samples misestimate σ because of skew. An exact σ_S/√S gives an exact-variance z for
  every stored mean *without re-running anything*, since the means are already in the JSON. The audit predicts that
  these cells fall to |z| < 3. That is a falsifiable check, not a promise.
* It enables a correct joint test across nested cuts. The cross-cut covariance is not in closed form, but it can be
  estimated once at moderate N with many samples. A Hotelling-type or max-|z| test with the exact marginal
  σ and simulated correlation then replaces "6 % with |z| > 2".
* It gives an analytic reference for the *width* of the Page curve band, which the figures show but never compare.
* Classification 2. Cost: hours, CPU-only, closed-form.

### Improvement 3: charge-conserving (U(1)) scramblers and the fixed-charge Page curve

**What.** Replace "Haar on the whole hole" by Haar **within each conserved-charge sector** (total excitation number
of the hole + radiation, a block-diagonal Haar unitary). Start the hole in a fixed-charge state (for example Q = N/2) or
in a thermal-like superposition of sectors. The radiation entropy then has a known analytic mean at fixed charge
(Bianchi and Donà 2019, "Typical entanglement entropy in the presence of a center"; at half filling compare Vidmar
and Rigol, PRL 119, 220603 (2017)). It differs from Page at O(1), with an additional term from the
number entropy (the classical sector distribution).

**Why.**
* It attacks assumption §5.1, the biggest physics simplification: no conserved quantity. A conserved charge is the
  minimal finite-dimensional stand-in for energy conservation and temperature. It splits S(R) into a
  number (Shannon) part and a configurational part, which is the structure that greybody and thermal effects
  impose. It stays strictly [C/RMT]; it is not [SG].
* The exact-Haar argument of §4.4 generalises (sector-Haar is invariant under charge-conserving B ⊗ 1_R), so the
  sequential protocol stays cheap (sample one sector-Haar state). The new Page curve is nonetheless *different* and has
  an analytic reference, a genuine new comparison instead of a reproduction of A.
* It can be combined with Improvement 1 (U(1)-conserving 2-qubit gates have their own domain-wall weights) and with
  E2: Hayden-Preskill with a conserved charge is known to leak charge information early. The latter would need
  expert review before any claim (class ≤ 4).
* Memory: the same 2^N statevector as A/C, or smaller (one sector of dimension C(N, N/2)); 26 qubits fits on one A100 slice.

### Runner-up (cheap, high value)

Exact stabilizer-state entanglement distribution (Smith and Leung, PRA 74, 062314 (2006); Dahlsten and Plenio,
QIC 6, 527 (2006); citations from memory, to be re-checked). This replaces the heuristic GF(2)-corank number in
critic objection 1 with an exact ensemble mean, so E1's Clifford threshold can be defined against the stabilizer
mean instead of against Page.

---

## 8. Summary of the audit

* The core numerics are correct for the stated models. 109 of 109 tests pass (re-run here). The independent
  verifier agrees on 8 of 9 claims, and the ninth (the Clifford sign) is already corrected.
* No result exceeds class 3, and the project already says so. The [C], [RMT], [SG] and [H] levels are kept apart in the paper (§8) and
  must stay apart in every upgrade.
* Main weaknesses:
  * Problem C is provably redundant with A beyond N = 14.
  * E1, the only non-trivial dynamics, has no analytic reference.
  * Large-N inference uses sample stderrs in a skewed, correlated regime.
  * The scrambler has no conserved quantity.
  * Conventions (emission end, samplers, clip thresholds, two Page implementations) are duplicated.
* Recommended order:
  1. Domain-wall exact purity for E1 (feasibility verified here: N = 8, depth 2, |z| ≤ 1.21 against 400 MC trajectories).
  2. Exact Page variance and re-scored z for the stored means.
  3. U(1) sector-Haar Page curve.
