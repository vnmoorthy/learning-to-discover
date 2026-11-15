# Event Horizon: reproducible finite-dimensional numerics around the black hole information paradox

*Page curves, Page's theorem, sequential evaporation, the Bell-pair "Hawking" model, local scramblers and Hayden-Preskill recovery, computed exactly on one A100 and independently re-verified.*

Date of the runs: 2026-11-15. Hardware: Lambda A100 40 GB, GPU 0 only. Code and data: this repository (`eh/`, `experiments/`, `verify/`, `results/`, `figures/`).

---

## Abstract

We report a reproducible set of exact state-vector computations on qubit toy models that are commonly used to discuss the black hole information paradox. (i) The Page curve of Haar-random pure states is reproduced for N = 8..24 qubits and Page's formula is checked at 124 dimension pairs (m, n) up to m·n = 2^24 (max |z| = 2.69, rms z = 1.00). (ii) A sequential "evaporation" protocol with a fresh Haar unitary on the remaining hole at every step is run literally up to N = 14 qubits and with an exact-in-distribution isometry sampler up to N = 26 (one trajectory at N = 27); we give the elementary proof that its whole entropy trajectory has exactly the law of the nested cuts of one Haar state, and the numerics agree. (iii) The Bell-pair model of Hawking emission gives S(R) = k ln 2 to round-off and exceeds the assumed capacity of the remaining hole for every k > N/2. (iv) With local brickwork scramblers the radiation entropy approaches the Page curve only when enough layers are applied per emission; the one-shot half-cut scrambling depth of Haar brickwork grows linearly, D* ≈ 1.87 N + 1.9 layers for N = 8..24 at a 0.05-nat threshold. Scrambled stabilizer (Clifford) states have flat spectra and a mean half-cut entropy *below* the Page value (−0.088 ± 0.015 nats at N = 10), so they never come within 0.05 nats of it. (v) In the Hayden-Preskill setting with a Haar scrambler the measured decoupling distance obeys the bound E T ≤ ½·2^(k−m) (ratio to the finite-d bound 0.83–0.87), with recovery thresholds essentially independent of the hole size for an old hole and shifted by ≈ n_B/2 for a young one. An independent verifier that shares no code with the builders reproduced eight of nine checked claims and corrected the sign of one interpretive statement. All findings are reproductions (class 1), verifications of known relations (class 2) or computational observations inside known models (class 3).

**This work does not solve, and does not claim to solve, the information paradox.** Every model is a finite-dimensional qubit system without gravity. The island formula of semiclassical gravity is summarised in a separate section (Sec. 8) and is neither derived nor tested by anything computed here.

---

## 1. Introduction

Hawking's semiclassical calculation gives radiation that is thermal and uncorrelated with what formed the hole, so the fine-grained entropy of the radiation would grow monotonically; unitarity of quantum mechanics instead requires it to return to zero when a hole formed from a pure state has evaporated. Page (1993a, 1993b) turned this tension into a quantitative statement: if the joint state of hole and radiation is a typical pure state, the radiation entropy rises, peaks when half of the degrees of freedom have been emitted, and falls. Hayden and Preskill (2007) later showed that, for a hole already maximally entangled with its early radiation, information thrown in re-emerges after only a few more quanta than the size of the message.

These statements are finite-dimensional quantum information theory and can be checked exactly on a computer. The purpose of this study is modest and specific:

1. reproduce the standard results with documented seeds, units and numerical thresholds;
2. push the exact sizes as far as one 40 GB GPU allows and quantify the cost;
3. have every key number re-derived by an independent implementation;
4. classify each finding honestly on the scale **1** reproduction, **2** verification of a known relation, **3** new computational observation within an existing model, **4** new conjecture, **5** potentially novel result needing investigation.

No finding here is above class 3.

## 2. Physical background

*Fine-grained versus coarse-grained entropy.* The von Neumann entropy S(ρ) = −Tr ρ ln ρ of the radiation is the fine-grained quantity; the Bekenstein-Hawking entropy A/(4 G_N) is a coarse-grained (thermodynamic) entropy that bounds the fine-grained entropy of the hole. If hole + radiation is pure, S(radiation) = S(hole) ≤ S_BH, which decreases as the hole shrinks. Hawking's result has S(radiation) increasing throughout. The two cross near the *Page time*.

*What the toy models keep and what they drop.* We replace the hole by N qubits and "emission" by moving qubits from the hole register to the radiation register. This keeps unitarity, purity and the dimension counting. It drops geometry, energy, temperature, the horizon, locality of the emission process and any notion of physical time. Throughout this paper "Page time" means *the step at which N/2 qubits have been emitted*; for odd N the Page curve has two equal maxima at k = (N ± 1)/2.

*Scrambling.* A unitary is a good scrambler if it spreads initially local information over the whole system. A Haar-random unitary is the idealised limit; random local circuits approach it only at sufficient depth. Sections 6.5–6.6 ask how much of the idealisation is needed.

## 3. Mathematical formulation

* Hilbert space H = H_R ⊗ H_B, dim H_R = m, dim H_B = n; for qubits m = 2^k, n = 2^(N−k).
* A pure state |ψ⟩ = Σ_ab M_ab |a⟩_R |b⟩_B is an m×n matrix M with Tr M M† = 1; ρ_R = M M†.
* Entropies: S = −Σ p_i ln p_i (nats; bits = nats/ln 2), Rényi-2 S_2 = −ln Σ p_i², purity Tr ρ² = Σ p_i².
* Haar measure: the unique unitarily invariant probability measure on U(d); Haar states are U|0⟩.
* Mutual information I(X:Y) = S(X) + S(Y) − S(XY); trace distance T(ρ, σ) = ½‖ρ − σ‖₁.
* z-score of a Monte Carlo mean: z = (mean − exact)/(sample standard error).

## 4. Derivations

### 4.1 Schmidt decomposition ⇒ S(R) = S(B)

Singular value decomposition M = U diag(s) V† with s_i ≥ 0, i = 1..min(m, n), gives |ψ⟩ = Σ_i s_i |u_i⟩_R |v_i⟩_B with Σ s_i² = 1. Then

  ρ_R = M M† = Σ_i s_i² |u_i⟩⟨u_i|,  ρ_B = (M† M)^T = Σ_i s_i² |v_i⟩⟨v_i|.

Both have the same non-zero eigenvalues p_i = s_i², hence S(R) = S(B) ≤ ln min(m, n). This is the only place where purity of the global state enters, and it alone forces the radiation entropy back to zero at the end.

### 4.2 Typical states are nearly maximally entangled (purity argument)

For a Haar state on D = mn dimensions, E[|ψ⟩⟨ψ|^{⊗2}] = (1 + F)/(D(D+1)) with F the swap of the two copies. Evaluating Tr ρ_R² = Tr[|ψ⟩⟨ψ|^{⊗2} F_R] gives (Lubkin 1978)

  E[Tr ρ_R²] = (m + n)/(mn + 1).

Since S ≥ S_2 and −ln is convex (Jensen), E[S(R)] ≥ −ln E[Tr ρ_R²] ≥ ln m − m/n for m ≤ n. The mean entropy is therefore within m/n = 2^(2k−N) nats of its maximum: exponentially close before the half-way point and within O(1) at it.

### 4.3 Page's formula and its expansion

Page (1993a) conjectured, and Foong and Kanno (1994), Sánchez-Ruiz (1995) and Sen (1996) proved, that for m ≤ n

  ⟨S_{m,n}⟩ = Σ_{j=n+1}^{mn} 1/j − (m−1)/(2n) = H_{mn} − H_n − (m−1)/(2n).

With H_x = ln x + γ + 1/(2x) − 1/(12x²) + 1/(120x⁴) − …:

  ⟨S_{m,n}⟩ = ln m − m/(2n) + 1/(2mn) + (1 − m^{−2})/(12 n²) − … .

The first two terms are Page's large-n form; the remaining ones follow from the exact formula (checked symbolically, `eh/page.py`). For N qubits, m = 2^{min(k, N−k)}, n = 2^{max(k, N−k)}:

  ⟨S(R_k)⟩ = min(k, N−k) ln 2 − ½·2^{−|N−2k|} + O(2^{−N}).

So the curve rises by one bit per qubit, has a deficit of ½ nat (0.72 bit) at k = N/2 for even N (¼ nat at k = (N ± 1)/2 for odd N), and falls symmetrically.

### 4.4 Sequential evaporation is exactly Haar

Protocol: start in |0…0⟩ on N qubits; for t = 1..N draw a fresh Haar unitary U_t on the remaining hole (N − t + 1 qubits), apply 1_R ⊗ U_t, then move one hole qubit to the radiation.

1. U_1 acts on all N qubits, so |ψ_1⟩ = U_1|0…0⟩ is Haar.
2. If |ψ_t⟩ is Haar and W = 1_R ⊗ U_{t+1} is any unitary independent of it, W|ψ_t⟩ is Haar (left-invariance, applied for each fixed W). By induction every |ψ_t⟩ is Haar on the full space, so S(R_t) has exactly the distribution of Page's ensemble with (m, n) = (2^t, 2^{N−t}).
3. Later unitaries act only on the hole and cannot change ρ_{R_t}. Hence the whole history (S(R_1), …, S(R_{N−1})) is a function of the nested cuts of the single final state, which is Haar.

Predictions: (a) the mean equals Page's formula with no finite-N correction and independently of the initial state; (b) entropies at consecutive steps are correlated exactly as nested cuts of one Haar state; (c) the statement fails if U_1 does not act on the whole system or if the scrambler is not Haar on the whole remaining hole.

A consequence that the critic stressed: U_2 … U_N are statistically invisible in the radiation spectrum, so the sequential simulation is logically redundant with Sec. 4.3. Only the literal runs test the protocol; the larger "isometry" runs are reference Page curves.

### 4.5 Bell-pair ("Hawking") model

Each emission creates a fresh Bell pair |Φ⁺⟩ = (|00⟩ + |11⟩)/√2 on (r_j, p_j); r_j is radiated, p_j stays inside. After k emissions |Ψ_k⟩ = |χ⟩_M ⊗ |Φ⁺⟩^{⊗k}. Because Tr_p |Φ⁺⟩⟨Φ⁺| = I/2 and the state is a product,

  ρ_R = (I/2)^{⊗k},  S(R) = k ln 2,  Tr ρ_R² = 2^{−k},  I(r_i : r_j) = 0.

S(R) never turns over. If the remaining hole is assigned capacity (N − k) ln 2 (a modelling assumption, labelled A4 in `notes/D_derivation.md`), then S(R) − capacity = (2k − N) ln 2 > 0 for every k > N/2. The assumptions that produce the difference from Sec. 4.4 are: independent pair creation (A1), no correlations among radiation quanta (A2), partners that never leave (A3), together with a shrinking capacity (A4).

### 4.6 Decoupling bound for Hayden-Preskill

Setup (old hole): diary A (k qubits) maximally entangled with a reference R; hole B (n_B qubits) maximally entangled with early radiation E; Haar U on AB, d = 2^{k+n_B} = d_R d_E; the last m output qubits D are emitted and B' remains, d = d_D d_{B'}. Bob holds E and D. By Uhlmann's theorem Bob can recover the diary if and only if R is decoupled from B'.

*Step 1 (second moment).* Tr ρ_{RB'}² = Tr[Ψ^{⊗2} F_R F_{B'}], and Ψ^{⊗2} = U^{⊗2} Φ^{⊗2} U^{†⊗2} with Φ = Φ_{RA} ⊗ Φ_{EB}. For Haar U and any M on two copies, E[U^{†⊗2} M U^{⊗2}] = α 1 + β F with α = (Tr M − Tr(MF)/d)/(d² − 1), β = (Tr(MF) − Tr M/d)/(d² − 1). For M = F_{B'} ⊗ 1_D: Tr M = d_{B'} d_D², Tr(MF) = d_{B'}² d_D, so α = (d d_D − d_{B'})/(d² − 1), β = (d d_{B'} − d_D)/(d² − 1). The input-side traces are Tr[Φ^{⊗2} F_R] = 1/d_R and Tr[Φ^{⊗2} F_R F_A F_B] = 1/d_E. Therefore

  E Tr ρ_{RB'}² = α/d_R + β/d_E = [d_{B'} d_R + d_D d_E − (d_{B'} d_E + d_D d_R)/d]/(d² − 1).

*Step 2 (product state is maximally mixed).* The scrambler input on AB is maximally mixed, so ρ_R ⊗ ρ_{B'} = 1/D exactly, D = d_R d_{B'}.

*Step 3 (Cauchy-Schwarz).* T ≡ ½‖ρ_{RB'} − 1/D‖₁ ≤ ½ √D ‖ρ_{RB'} − 1/D‖₂ = ½ √(D Tr ρ_{RB'}² − 1).

*Step 4 (Jensen).* E T ≤ ½ √(D·E Tr ρ_{RB'}² − 1). Inserting Step 1 and simplifying,

  **E T ≤ ½ √[(d_R² − 1)(d_D^{−2} − d^{−2})/(1 − d^{−2})] ≤ ½·2^{k−m}.**

*Step 5 (decoder).* Uhlmann plus the Fuchs-van de Graaf inequality give a decoder on ED with entanglement fidelity F ≥ (1 − T)² ≥ 1 − 2T, so average error ε is guaranteed for m ≥ k + log₂(1/ε), independent of n_B. This is a sufficient condition on the Haar average, not a necessary one and not a per-instance statement.

*Young hole (B in |0…0⟩, no E).* The same steps give E T_mm ≲ ½·2^{k + n_B/2 − m} (distance to the maximally mixed state), so m ≳ n_B/2 + k + log₂(1/ε): roughly half of the hole must be radiated first. This is the Hayden-Preskill (2007) argument specialised to qubits; the constants are those of the purity bound.

Also, because the global state is pure, I(R:ED) + I(R:B') = 2 S(R) = 2k ln 2 exactly.

## 5. Methods

**Software.** Python 3.10, torch 2.7 (CUDA), complex128 throughout. Haar unitaries: QR of a complex Ginibre matrix with the phase fix of Mezzadri (2007). Spectra: `eigvalsh` of the smaller Gram matrix or SVD of the 2^k × 2^(N−k) reshaped state.

**Clipping.** Eigenvalues are clipped only inside the logarithm, at 1e-15 (Problems A–D, `eh/entropy.py`), 1e-13 (Gram-matrix spectra in E1/E2), 1e-14 (verifier and notebook). `log 0` is never evaluated.

**Units.** Nats unless a column says bits.

**Seeds** (recorded in every result JSON):

| Problem | Seed rule |
|---|---|
| A | `torch.Generator(cuda).manual_seed(1000 + N)` |
| B | `manual_seed(2000 + row index)` |
| C | `manual_seed(3000 + 100 N + s)` (full), `+ 50000` (isometry) |
| D | none (deterministic states) |
| E1 | `SeedSequence([20261115, N, family_id, depth, batch_index])` |
| E2 | `SeedSequence([20261115, 2, variant_id, k, n_B, extra, seed_index])` |
| Verifier | numpy Philox, key = 900000 + tag |
| Notebook | `default_rng(20261115 + tag)` |

**Sizes reached on the A100 (GPU 0) and their cost.**

| Computation | Largest size | Seeds there | Peak GPU memory | Wall time |
|---|---|---|---|---|
| A: Haar state, all cuts | N = 24 | 8 | not recorded | ≈ 8 min whole sweep |
| B: (m, n) pairs | m·n = 2^24 (m = n = 4096 included) | 16 per row | not recorded | 406 s whole sweep |
| C literal (2^N × 2^N unitaries) | N = 14 | 20 | 12.3 GiB | 4.3 s / trajectory |
| C isometry sampler | N = 26 (N = 27 once) | 16 (1) | 7.0 GiB (8.1 GiB) | 12.7 s (28 s) / trajectory |
| E1 brickwork evaporation | N = 26 | 4 | 10.8 GB | up to 344 s per (family, depth) |
| E1 one-shot brickwork | N = 24 | 8 | – | – |
| E2 old hole (2(k + n_B) qubits) | 26-qubit global state | 4 | 8.6 GB | 68–78 s per record |
| E2 young hole (2k + n_B qubits) | 26-qubit global state | 6 | 9.7 GB | 267 s |

Literal Haar evaporation costs 16·4^N bytes per unitary; N = 15 would need ≈ 49 GiB at peak and was not attempted. The isometry sampler costs 16·2^N bytes per state vector; N = 28 was not run (estimated 16–30 GiB). Both estimates are extrapolations, not measurements. Measured runtime growth is ×2.7 per qubit for the literal protocol (N = 10..14) and ×2.2 per qubit for the isometry sampler (N = 22..27); both fits use four or five points on a shared machine and are indicative only. Small-N runs of Problem C (N ≤ 9 literal, N ≤ 20 isometry) were made on CPU; each JSON records its device.

**Independent verification.** `verify/independent.py` does not import `eh/`; it uses scipy `unitary_group`, CPU numpy, exact rational Page values and explicit-loop partial traces (233 s on the box).

**Tests.** `pytest -q tests`: 109 passed, 0 failed, in 21.32 s (49 core + 5 evaporation + 55 extensions; `logs/pytest_verifier.log`).

## 6. Results

Error conventions are stated per figure. z-scores within one N come from nested cuts of the same states and are correlated, so pooled z statistics are descriptive.

### 6.1 Page curve (Problem A) — class 1 / 2

Figure: `figures/a_page_curve.png` (numerics with ±1 std band against the exact formula; deficit near the Page time with 95 % CI; z-scores). Data: `results/a_page_curve.json`.

* N = 8..20 plus 22 and 24; 400 states per N for N ≤ 14, falling to 16 at N = 22 and 8 at N = 24.
* 213 cells (N, k): max |z| = 3.38 (N = 24, 8 states); 2.66 for N ≤ 20; rms z = 1.05; 6.6 % with |z| > 2.
* max |mean − Page| = 1.6e-3 nats at N = 8, falling to 2.6e-5 nats at N = 24.
* max |S(R) − S(B)| = 5.3e-15 nats (independent `eigvalsh` of ρ_B when the larger side is ≤ 2048).

### 6.2 Page's theorem (Problem B) — class 2

Figure: `figures/b_page_theorem.png` (finite-size deficit at m = n; error of the asymptotic forms; z-scores; Monte Carlo convergence). Data: `results/b_page_theorem.json`, `results/b_page_theorem_table.md`.

* 124 (m, n) pairs up to m·n = 16 777 216: max |z| = 2.69, rms z = 1.00, 4.0 % with |z| > 2, none above 3.
* Monte Carlo error exponent −0.476 at (m, n) = (8, 16) (expected −0.5; a fit at one pair).
* `ln m − m/(2n)` errs by −0.140 nats at (2, 2) and by −3.0e-8 at m·n = 2^24; adding `+1/(2mn)` reduces this to −1.5e-2 at (2, 2) and −2.0e-8 at (2048, 2048).

### 6.3 Sequential Haar evaporation (Problem C) — class 2 (mean), class 3 (trajectory-level tests)

Figure: `figures/c_evaporation.png` (mean S(R) with ±1 std band; deviation from Page per step; distribution tests; runtime and memory). Data: `results/c_evap_*`, `results/c_ks_N{8,10}.json`, `results/c_variants_N6.json`, `results/c_summary.json`.

* Literal protocol, N = 6..14: max |z| per run between 0.82 and 2.84, except one run discussed below; max |mean − Page| from 3.3e-3 nats (N = 6) to 6.7e-4 nats (N = 14).
* Isometry sampler, N = 6..26: max |z| ≤ 2.42 for N ≤ 24 (100 seeds at N = 22 and 24), 3.65 at N = 26 (16 seeds).
* Pooled over 296 (run, step) cells with ≥ 8 seeds: rms z = 1.11, 6.1 % with |z| > 2.
* **Outlier followed up.** Literal N = 13, step 2, 40 seeds gave z = +4.19. Extending the same seed rule to 1000 trajectories gives z = +1.36 at that step and max |z| = 1.64 over all steps. For dim R ≪ dim B the entropy distribution is strongly skewed towards ln dim R, so a 20–40 sample standard error is too small. Conclusion: small-sample fluctuation, not bias.
* **Distribution level.** Two-sample KS tests of S(R), λ_max and one-step increments against directly sampled Haar states: N = 10, 53 tests, smallest p = 0.055 (Bonferroni-adjusted 1.0); N = 8, 41 tests, smallest p = 0.024 (adjusted 0.98). Consecutive-step correlations 0.43–0.52 (sequential) versus 0.44–0.51 (nested cuts of one Haar state). A non-rejection is not a proof; the proof is Sec. 4.4.
* **Controls that do differ** (N = 6, 2000 samples): emitting a qubit before the first scramble gives the Page curve of N − 1 qubits shifted by one step; starting with two hole qubits maximally entangled with two early radiation qubits puts S(R) above the N-qubit Page value by 67, 31, 16, 7.6 and 3.6 standard errors at steps 1–5.

### 6.4 Bell pairs versus unitary evaporation (Problem D) — class 1 / 2

Figure: `figures/d_hawking_pairs.png`. Data: `results/d_hawking_pairs.json`.

* |S(R) − k ln 2| ≤ 4.4e-15 nats for k = 0..12 (density-matrix route), ≤ 8.9e-15 (state-vector route); spectrum flat; S monotone.
* For each N = 6..26 the pair model first exceeds the assumed capacity (N − k) ln 2 at k = ⌊N/2⌋ + 1.
* At the end of evaporation the pair model has S(R) = N ln 2 and the unitary model has S(R) = 0.

### 6.5 Local scramblers (Extension E1) — class 3

Figures: `figures/e1_trajectories.png`, `figures/e1_deviation_scrambling_depth.png`, `figures/e1_size_scaling.png`, `figures/e1_spectrum.png` (error bars are 95 % CI over seeds). Data: `results/e1_scrambling.json`.

Model: before each emission, `depth` brickwork layers of random 2-qubit gates act on the remaining open chain; the edge qubit is emitted. Deviation = max over steps of (Page − ⟨S(R)⟩).

| N | seeds | depth 1 | depth 2 | depth 4 | depth 8 | depth 16 |
|---|---|---|---|---|---|---|
| 8 | 256 | 1.096 ± 0.023 | 0.725 ± 0.021 | 0.247 ± 0.013 | 0.056 ± 0.006 | 0.0029 ± 0.0009 |
| 12 | 256 | 1.979 ± 0.024 | 1.178 ± 0.018 | 0.333 ± 0.012 | 0.065 ± 0.005 | 0.0061 ± 0.0008 |
| 16 | 64 | 2.837 ± 0.052 | 1.640 ± 0.044 | 0.414 ± 0.026 | 0.066 ± 0.011 | 0.0071 ± 0.0021 |
| 20 | 24 | 3.774 ± 0.069 | 2.006 ± 0.065 | 0.439 ± 0.046 | 0.081 ± 0.026 | 0.0060 ± 0.0015 |
| 24 | 8 | 4.669 ± 0.134 | 2.492 ± 0.094 | 0.465 ± 0.074 | 0.055 ± 0.032 | 0.0091 ± 0.0054 |
| 26 | 4 | 5.084 ± 0.186 | 2.627 ± 0.132 | 0.436 ± 0.067 | 0.043 ± 0.016 | 0.0022 ± 0.0013 |

(local Haar gates; nats; ± is the 95 % CI of the mean at the worst step.)

* With one or two layers per emission the deviation grows with N; with 8 layers it is 0.04–0.08 nats for all N = 8..26; with 16 layers it is below 0.01 nats. On the grid {1, 2, 4, 8, 16} the smallest depth with deviation < 0.05 nats is 16 for most sizes and 8 at N = 9 and N = 26, i.e. the threshold sits near depth 8 and is not resolved by this grid.
* Trivial circuits (identity, SWAP, H+CNOT, 2 seeds each) stay far from Page, as they must.
* **One-shot scrambling.** D brickwork layers on all N qubits, then the half cut. Smallest D with Page − ⟨S⟩ < 0.05 nats for Haar gates: 16, 21, 24, 29, 32, 35, 40, 43, 46 layers at N = 8, 10, …, 24. Linear fit D* = 1.87 N + 1.9 (max residual 0.96 layers; nine points, no error bars). Linear growth is expected for a 1D chain; only the coefficient is an observation, and it is specific to this gate set, geometry and threshold.
* **Clifford circuits.** Spectra are exactly flat (|S_vN − S_2| ≤ 6.1e-14 in every single run, all sizes) and entropies are integer numbers of bits. The late-time one-shot Clifford plateau is below Page at all nine sizes by 0.06–0.20 nats; the verifier's 800 deep-circuit stabilizer states at N = 10 give ⟨S⟩ = 2.878 ± 0.015 against Page 2.966, i.e. **−0.088 ± 0.015 nats**, with half-cut entropies of 5, 4, 3, 2 bits at frequencies 0.279, 0.601, 0.114, 0.006. The mean purity (0.06207) matches the Haar value (0.06244), as it must for a 2-design. Consequently a 0.05-nat threshold relative to Page is unreachable for Clifford circuits at any depth: "d* undefined" is a property of the stabilizer ensemble, not evidence of slower scrambling. The builders' hand-off report had the sign of this offset wrong; no repository file did. One figure caption (`e1_deviation_scrambling_depth.png`) mentions "negative: Clifford mean above Page"; that refers to individual noisy cells (for example N = 24, depth 8, 8 seeds), not to the ensemble mean.
* Clifford results at N ≥ 22 (4–12 seeds) carry no information beyond consistency with smaller sizes.

### 6.6 Hayden-Preskill recovery (Extension E2) — class 2 (Haar), class 3 (local scramblers)

Figures: `figures/e2_mutual_information.png`, `figures/e2_decoupling.png`, `figures/e2_fidelity.png`, `figures/e2_thresholds.png`, `figures/e2_local_scrambler.png`. Data: `results/e2_hayden_preskill.json`.

Old hole, k = 1, n_B = 4, Haar scrambler (builder 200 seeds; verifier 400 seeds):

| m | I(R:ED) builder | I(R:ED) verifier | T (verifier) | bound (finite d) | ½·2^(k−m) | F_EPR (verifier) |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0.7500 | 0.8660 | 1.0000 | 0.2500 |
| 1 | 0.9769 | 0.9763 | 0.3734 | 0.4324 | 0.5000 | 0.5719 |
| 2 | 1.2923 | 1.2914 | 0.1838 | 0.2149 | 0.2500 | 0.8435 |
| 3 | 1.3644 | 1.3646 | 0.0882 | 0.1049 | 0.1250 | 0.9586 |
| 4 | 1.3821 | 1.3821 | 0.0389 | 0.0469 | 0.0625 | 0.9917 |
| 5 | 1.3863 | 1.3863 | 0 | 0 | 0.0313 | 1.0000 |

(I in nats, 2k ln 2 = 1.3863; F_EPR is the fidelity of the Yoshida-Kitaev probabilistic decoder after post-selection.)

* The bound of Sec. 4.6 holds on the mean and on every sample; T/bound = 0.83–0.87 for m = 1..4. The condition m ≥ k + log₂(1/ε) is about one qubit more than the measured thresholds need.
* Thresholds read from seed-mean curves (integers, no error bars): for k = 1, I ≥ 0.9·2k ln 2 at m = 2, I ≥ 0.99·2k ln 2 at m = 4, T ≤ 0.1 at m = 3, for every n_B = 3..12. For k = 2 and 3 they are (3, 5, 5) and (4, 5, 6) for most n_B, with some values one lower at n_B = 3 and 4. The 26-qubit records rest on 4 seeds.
* Young hole (no early radiation), k = 1: the I ≥ 0.9 threshold is m = 4, 5, 6, 7, 8, 9, 10, 11, 12 for n_B = 4, 6, …, 20, i.e. m ≈ n_B/2 + 2; the shift by n_B/2 predicted in Sec. 4.6 is observed up to a 26-qubit global state (n_B = 20, k = 3, 6 seeds). `m_F90 = None` entries mean "not computed", not "not reached".
* Local scramblers (one size only: 10 scrambler qubits, 32 seeds): with the diary at the far end of the chain from the emitted qubits, a Haar brickwork needs depth ≈ 24–32 before thresholds reach the Haar-scrambler values (for k = 1: m_I90 = 10 at depth 1–2, 6 at depth 10–12, 2 at depth 24–32). With the diary adjacent to the emitted qubits the thresholds are already at their Haar values by depth ≈ 4. No scaling claim can be made from one size.

## 7. Analytical comparisons and independent verification

| Claim | Class | Builder | Verifier | Agree |
|---|---|---|---|---|
| Page formula vs Monte Carlo | 2 | 124 pairs, max \|z\| 2.69; 213 cells, max \|z\| 3.38 | 7 (m, n) pairs vs exact rationals, max \|z\| 1.23; builder statistics recomputed to all digits | yes |
| Sequential evaporation, N = 8 | 2 | 200 + 200 trajectories | 400 trajectories, max \|z\| 1.26 vs Page, 1.52 vs builder; step correlation 0.38–0.54 | yes |
| Bell pairs S(R) = k ln 2 | 1 | error ≤ 4.4e-15 | error ≤ 8.9e-16 | yes |
| Hayden-Preskill, k = 1, n_B = 4 | 2 | table above | max \|z\| 1.30 across six quantities; identical thresholds | yes |
| Decoupling bound, F ≥ (1 − T)² | 2 | derived and compared | re-derived by hand; holds on every sample | yes |
| Brickwork evaporation, N = 8, depth 2 | 3 | max deviation 0.725 | 0.713, max \|z\| 1.54 | yes |
| Clifford spectra flat, integer bits | 3 | \|S_vN − S_2\| ≤ 6.1e-14 | ≤ 8.5e-13 over 800 states | yes |
| "Scrambled Clifford sits above Page by ≈ 0.19 nats" | 3 | hand-off report only | below Page by 0.088 ± 0.015 nats | **no (corrected)** |

A small-size CPU notebook (`notebooks/event_horizon.ipynb`, executed in 22 s on the box, 0 errors) re-derives the same items with a third implementation: Page curve N = 10 (max |z| = 2.01), seven (m, n) pairs (max |z| = 2.21), sequential evaporation N = 8 (max |z| = 1.37, step correlations 0.41–0.49), Bell pairs (error ≤ 2.7e-15), brickwork deviations at N = 8 (1.075, 0.742, 0.213, 0.040, 0.005 for depths 1–16; 48 seeds), stabilizer half cut at N = 8 (−0.137 ± 0.032 nats relative to Page), and Hayden-Preskill k = 1, n_B = 4 (same thresholds 2, 4, 3; bound holds).

## 8. The island formula (theoretical context; not derived or tested here)

This section summarises a result of semiclassical gravity. It is logically separate from Sections 3–7.

For a region R collecting Hawking radiation, the fine-grained entropy is given by the island rule (Penington 2019; Almheiri, Engelhardt, Marolf and Maxfield 2019):

  S(R) = min over I of ext over ∂I of S_gen(I),  S_gen = Area(∂I)/(4 G_N) + S_matter(R ∪ I),

where I is a candidate region (the island) in the gravitating spacetime, ∂I its boundary, and S_matter the entropy of quantum fields on R ∪ I computed semiclassically. One extremises S_gen over the position of ∂I and then takes the minimum over the extremal saddles.

* **No-island saddle (I = ∅).** S_gen = S_matter(R): Hawking's result, which grows as radiation accumulates.
* **Island saddle.** ∂I lies near the horizon; the island contains the interior partners of the radiation, so S_matter(R ∪ I) is small and S_gen ≈ A_horizon/(4 G_N) = S_BH, which decreases as the hole evaporates.
* **Minimum.** Early on the no-island saddle is smaller; after the Page time the island saddle is. The minimum therefore rises and then falls: a Page curve obtained within semiclassical gravity.

What must be stated plainly:

1. **The finite-dimensional models in this paper do not derive the island formula.** They contain no area term, no geometry, no extremisation and no gravitational path integral. Our Page curves follow from Haar typicality on a fixed qubit Hilbert space, which is an assumption about the dynamics, not a gravitational computation.
2. Conversely, the island computation makes no random-state assumption on a qubit Hilbert space. Agreement in shape between the two is a consistency of expectations, not a derivation of one from the other.
3. The island rule gives the entropy curve; by itself it does not exhibit the microscopic state of the radiation.

*Toy two-candidate illustration (labelled as a toy).* In the notebook (Sec. 7 there) we plot min(k ln 2, (N − k) ln 2), the smaller of the Bell-pair growth of Sec. 4.5 and the assumed capacity of the remaining hole, against Page's exact formula for N = 10; the two differ by at most 0.4994 nats, at k = N/2. This is an arithmetic analogy to "take the smaller of two candidates". The two candidates are not generalized entropies and nothing is extremised.

## 9. Limitations

**Statistics.**
* Pooled z statistics are over correlated cells and are descriptive only.
* With 8–40 seeds and dim R ≪ dim B the sample standard error is unreliable. The z = 3.38 cell (A, N = 24, 8 states) and the z = 3.65 cell (C, N = 26, 16 seeds) were not followed up; only the z = 4.19 cell was.
* B rows at m·n = 2^24 rest on 16 samples each.
* E1's "maximum over steps" is biased upward when seeds are few and is floored at 0.
* d* and D* have no error bars and depend on the arbitrary 0.05-nat threshold.
* E2 thresholds are integers read from seed-mean curves.

**Scope.**
* The sequential state is exactly Haar, so the N = 22–27 isometry runs and E1's `haar_shortcut` runs are reference Page curves, not further tests of evaporation dynamics. The literal protocol is exercised only for N ≤ 14.
* The decoupling bound is on the Haar average; it is sufficient, not necessary, and about one qubit loose.
* Local-scrambler Hayden-Preskill was run at one size.
* The capacity (N − k) ln 2 in Problem D is an assumption of the toy.
* "Page time" is a count of emitted qubits, not a physical time.

**Verification.**
* The verifier reproduced one small CPU point each of C, E1 and E2. The large-N GPU numbers were checked for internal consistency of the stored JSON and were not re-run.
* GPU memory figures for sizes not run (literal N = 15, isometry N = 28) are estimates.

**Hygiene.**
* Laptop-era leftovers (`*_cpu.py`, `c_modal.py`, `modal_run.py`, `results/c_cache`, `results/raw`, `figures/e1_cpu_*`) remain in the tree and are not used by any result reported here.
* There is no `notes/` file for E1/E2; their derivation is in Sec. 4.6 of this paper and in a string field of `results/e2_hayden_preskill.json`.
* No PDF was produced: `pandoc` is not installed on the machine where this was written.

## 10. Conclusions

1. Page's formula and the Page curve are reproduced to Monte Carlo accuracy up to 24 qubits and m·n = 2^24 (classes 1–2).
2. Sequential Haar evaporation is, provably and numerically, the same ensemble as a single Haar state viewed through nested cuts (class 2; trajectory-level tests class 3).
3. The Bell-pair model and the unitary model part ways exactly at k = N/2, and the four assumptions responsible are identified (class 1).
4. Local scrambling needs of order 8 brickwork layers per emitted qubit to stay within ≈ 0.05 nats of Page for N ≤ 26, and about 1.87 N layers in one shot; stabilizer ensembles sit a fraction of a bit below Page on average (class 3).
5. Hayden-Preskill recovery from an old hole needs m ≈ k + O(1) emitted qubits regardless of hole size, in line with the decoupling bound; a young hole needs about n_B/2 more (class 2).
6. An independent implementation confirms these numbers and corrected one interpretive error.

None of this resolves the information paradox. The models assume unitarity and strong scrambling and then display their consequences; whether and how gravity realises those assumptions is addressed by a separate body of work (Sec. 8) that this study does not test.

## References

Existence of each entry was checked by web search during this project (by the builders, the verifier or the writer); journal pages were not all opened.

1. D. N. Page, "Average entropy of a subsystem", Phys. Rev. Lett. **71**, 1291 (1993), arXiv:gr-qc/9305007.
2. D. N. Page, "Information in black hole radiation", Phys. Rev. Lett. **71**, 3743 (1993).
3. S. K. Foong and S. Kanno, Phys. Rev. Lett. **72**, 1148 (1994).
4. J. Sánchez-Ruiz, Phys. Rev. E **52**, 5653 (1995).
5. S. Sen, "Average entropy of a subsystem", Phys. Rev. Lett. **77**, 1 (1996), arXiv:hep-th/9601132 (journal reference from a secondary source).
6. E. Lubkin, J. Math. Phys. **19**, 1028 (1978).
7. F. Mezzadri, "How to generate random matrices from the classical compact groups", Notices of the AMS **54**, 592 (2007).
8. P. Hayden and J. Preskill, "Black holes as mirrors: quantum information in random subsystems", JHEP 0709:120 (2007), arXiv:0708.4025.
9. B. Yoshida and A. Kitaev, "Efficient decoding for the Hayden-Preskill protocol", arXiv:1710.03363.
10. G. Penington, "Entanglement wedge reconstruction and the information paradox", JHEP 09 (2020) 002, arXiv:1905.08255.
11. A. Almheiri, N. Engelhardt, D. Marolf and H. Maxfield, "The entropy of bulk quantum fields and the entanglement wedge of an evaporating black hole", JHEP 12 (2019) 063, arXiv:1905.08762.

The Cauchy-Schwarz, Jensen, Uhlmann and Fuchs-van de Graaf steps of Sec. 4.6 are textbook inequalities and are used without a specific citation.
