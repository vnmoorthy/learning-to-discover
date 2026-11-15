# Critic's notes — independent verification and adversarial review

Verifier pass, 2026-11-15. Scope: Problems A–D and Extensions 1–2 (scrambling, Hayden–Preskill).
Independent code: `verify/independent.py` (no import of `eh/`; scipy `unitary_group`, CPU numpy, Philox RNG,
exact rational Page values, explicit-loop partial traces, clip 1e-14). Numbers: `results/verification.json`,
`results/verification_raw.json`. Log: `logs/verify_independent.log`. Tests: `logs/pytest_verifier.log`.

Nothing here (or anywhere in this project) solves or claims to solve the information paradox. All models are
finite-dimensional qubit toys without gravity; island / quantum-extremal-surface results are a separate
semiclassical argument that none of these numbers test.

## What was reproduced (all in nats)

| Claim | Class | Verifier result | Agrees |
|---|---|---|---|
| Page formula vs Monte Carlo, 7 (m, n) from (2,2) to (32,64) | 2 | max \|z\| = 1.23 against exact rationals; SVD vs loop partial trace differ ≤ 1.3e-15 | yes |
| Builder A/B summary statistics | 2 | recomputed from stored means with independent Page values: A 213 cells, max \|z\| 3.378, rms 1.046; B 124 rows, max \|z\| 2.694, rms 0.997 | yes |
| Sequential Haar evaporation, N = 8, 400 trajectories | 2 | max \|z\| = 1.26 vs Page, 1.52 vs builder `full`, 1.47 vs builder `isometry`; \|S(R) − S(B)\| ≤ 2.2e-15; step correlation 0.38–0.54 | yes |
| Bell pairs, S(R) = k ln 2, k = 0..6 | 1 | error ≤ 8.9e-16, flat spectrum | yes |
| Hayden–Preskill old BH, k = 1, n_B = 4, m = 0..5 (I(R:ED), I(R:B'), T, F_EPR, P_EPR, F_uhl) | 2 | max \|z\| = 1.30 vs builder; thresholds m_I90 = 2, m_I99 = 4, m_T10 = 3 identical | yes |
| Decoupling bound and F ≥ (1 − T)² | 2 | re-derived by hand; holds; T/bound = 0.83–0.87 for m = 1..4 | yes |
| Local-Haar brickwork evaporation, N = 8, depth 2 | 3 | max \|z\| = 1.54 vs builder; max deviation 0.713 vs 0.725 | yes |
| Clifford spectra flat, entropies integer bits | 3 | \|vN − Rényi-2\| ≤ 8.5e-13 over 800 states, all cuts | yes |
| "Scrambled Clifford sits above Page by up to ~0.19 nats" (builder hand-off report) | 3 | mean is **below** Page by 0.088 ± 0.015 nats (N = 10) | **no** |
| Test suite | – | 109 passed in 21.32 s (49 core + 5 evaporation + 55 extensions) | yes |

## Objections — fixed

1. **Sign of the Clifford offset from Page.** The builder's report explains the non-convergence of Clifford
   circuits by saying a scrambled stabilizer state sits *above* Page at the half cut. It is the other way round
   on average: 800 deep-circuit stabilizer states at N = 10 give ⟨S⟩ = 2.878 ± 0.015 against Page 2.966.
   Half-cut entropies were 5, 4, 3, 2 bits with frequencies 0.279, 0.601, 0.114, 0.006 (a random 5×5 GF(2)
   matrix has corank 0, 1, 2, 3 with probability 0.298, 0.577, 0.120, 0.004 — a heuristic reference, not a
   cited theorem; it predicts −0.077 nats). The mean purity 0.06207 matches the Haar value 0.06244, as it
   must for a 2-design. The builder's own one-shot Clifford plateaus are below Page at 8 of 9 sizes
   (−0.10 … −0.19 nats). A zero-deficit stabilizer state is 0.5 nat above Page and a one-bit-deficit state
   0.193 nat below, which is probably where "0.19" came from.
   *Consequence:* with ε = 0.05 nats, Clifford circuits cannot reach "within ε of Page" at the half cut at any
   depth. "d* undefined for Clifford" is a property of the stabilizer ensemble, not evidence of slower
   scrambling. Fixed by recording the correction in `README.md`, `results/verification.json` and here; the
   wrong sentence was not in any repo file, so no code or caption was changed.
2. **README did not report the whole test suite or the extensions' tests.** Added the 109-pass line and a
   verification section.
3. **Sen reference.** The builder cited PRL 77, 1 (1996) from memory. A web search confirms
   arXiv:hep-th/9601132 (S. Sen, "Average Entropy of a Subsystem") and a secondary source gives the same
   journal reference. The PRL page itself was not opened.

## Objections — open (not bugs; wording, statistics, scope)

**Statistics**
- Pooled z statistics (A: 213 cells, C: 296 cells) are over strongly correlated cells (nested cuts of the same
  states, step correlation ≈ 0.45). "6 % with |z| > 2" is descriptive only.
- For dim R ≪ dim B the distribution of S(R) is very skewed, so the sample standard error from 8–40 states is
  unreliable. This produced the z = 4.19 cell (resolved by the builder with 1000 seeds) and likely the
  z = 3.38 (A, N = 24, 8 states) and z = 3.65 (C, N = 26, 16 seeds) cells, which were **not** followed up.
- B rows at m·n = 2^24 rest on 16 samples each. The "−0.476 vs −0.5" Monte Carlo slope is a fit to one (m, n).
- E1 "max deviation over t" is the maximum of noisy means and is biased upward when seeds are few; it is also
  floored at 0 by the t = 0 point. The Clifford panels at N ≥ 22 (4–12 seeds) carry no usable information
  beyond "consistent with the smaller sizes".
- d* and D* have no error bars, sit on a coarse depth grid, and depend on the arbitrary ε = 0.05 nats. The fit
  D* = 1.87 N + 1.9 is nine points, N = 8..24; the slope is specific to this gate set, open chain and ε.
  Linear-in-N depth is the expected behaviour of a 1D local circuit, so the class-3 content is only the
  coefficient.
- E2 thresholds are integers read from seed-mean curves. "Independent of n_B over 3..12" is slightly too
  strong: at n_B = 3, 4 some thresholds are one lower (k = 2: m_I99 = 4, m_T10 = 4; k = 3, n_B = 3: m_T10 = 5).
  The 26-qubit records have 4 seeds.

**Wording / physics**
- "Page time" throughout means *number of emitted qubits = N/2* (half of the initial coarse-grained
  entropy radiated). It is not a physical time; for odd N the Page curve has two equal maxima at
  k = (N ± 1)/2. Nothing here maps k to a Hawking evaporation time.
- Problem C's result that the sequential state is exactly Haar is correct (checked), and it makes the
  sequential simulation logically redundant with Problem A: every later unitary is statistically invisible in
  the radiation spectrum. The N = 22–27 "isometry" runs and the E1 `haar_shortcut` runs are therefore
  reference Page curves, not additional tests of evaporation dynamics. Only the literal runs (N ≤ 14) exercise
  the protocol.
- The same argument depends on U_1 acting on the whole system of a pure state. It says nothing about a hole
  that is entangled with something else before scrambling, or about non-Haar dynamics.
- Decoupling bound: it bounds the Haar **average** of T, not each instance, and "m ≥ k + log2(1/ε)" is a
  sufficient condition for average error ≤ ε (constants from Cauchy–Schwarz + Jensen + Fuchs–van de Graaf),
  about one qubit more than the measured thresholds need. The asymptotic constant ½·2^(k−m) is never tight.
- `yk_fidelity_prediction` is 1/E[1/F]-like (mean purity inserted), not E[F]; agreement "to 4 digits" reflects
  concentration at these sizes, not an exact identity.
- Young black hole: `m_F90` is `None` in most records (F_uhl not computed where R+B' is large). Those entries
  must not be read as "threshold not reached".
- Local-scrambler Hayden–Preskill was run at one size (10 qubits), one geometry tabulated; no scaling claim
  can be made from it.
- Problem D: identifying (N − k) ln 2 with a Bekenstein–Hawking-like capacity is an assumption of the toy
  (stated as A4 in the note). The "violation" is a statement about that assumption set, not about gravity.
- Classification: nothing is above class 3. The class-3 items (trajectory law tests, brickwork depths,
  local-scrambler thresholds) are observations inside known models; none is claimed as new physics.

**Reproducibility / hygiene**
- Leftover laptop-era files (`*_cpu.py`, `c_modal.py`, `modal_run.py`, `results/c_log_*`, `results/c_cache`,
  `results/raw`, `results/gpu_keep_*`, `results/keep_iso_*`, `results/b_partial.json`, `figures/e1_cpu_*`)
  are still in the tree and could be mistaken for results.
- There is no `notes/` file for Extensions 1–2; their derivation lives only in a JSON string field.
- Small-N Problem C runs were on CPU (device recorded in each JSON), so "verified on the A100" applies to
  N ≥ 10 for the literal protocol.
- GPU memory figures for sizes not run (full N = 15, isometry N = 28) are estimates.
- Verifier limits: one point each of C, E1 and E2 was reproduced independently (N = 8; k = 1, n_B = 4), all on
  CPU at small size. The large-N GPU numbers were checked only for internal consistency of the stored JSON,
  not re-run. References other than Sen were not re-checked.
