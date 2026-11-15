# Problem C — sequential evaporation vs the i.i.d. Haar ensemble

Classification: **2 (verification of a known relation)** for "sequential Haar evaporation reproduces Page";
the distribution-level/trajectory-level tests are **3 (computational observation within an existing model)**
that confirm an elementary exact statement (below). No new physics is claimed.

## Protocol (`eh/evaporation.py`, `experiments/c_evaporation_cpu.py`)
N qubits, initial pure state |0…0⟩ (a Haar-random initial state is run as a control). For k = 0..N−1:
(1) draw a fresh Haar unitary U_{k+1} on the 2^{N−k}-dimensional *remaining* hole and apply 1_R ⊗ U_{k+1};
(2) move one hole qubit to the radiation. Recorded each step: k, dim R, dim B, S(R), S(B) (independently, from
ρ_B), Tr ρ_R², full spectrum of ρ_R.

## Exact statement: where does the sequential process differ from a Haar-random state? (It does not, for entropies.)

Let |ψ_k⟩ be the global state after step k and R_k the first k emitted qubits.

1. **Marginal law.** U_1 acts on all N qubits, so |ψ_1⟩ = U_1|0…0⟩ is Haar on C^{2^N}. If |ψ_k⟩ is Haar and
   W = 1_{R_k} ⊗ U_{k+1} is any unitary independent of it, then W|ψ_k⟩ is again Haar (left-invariance of the
   Haar measure, applied for each fixed W). By induction **every |ψ_k⟩ is exactly Haar-distributed on the full
   Hilbert space**, so S(R_k) has exactly the distribution of Page's ensemble with (m, n) = (2^k, 2^{N−k}); the
   mean is Page's formula with no finite-N correction, and the initial state is irrelevant.
2. **Joint law of the whole trajectory.** Later unitaries act only on B_j ⊂ B_k (j ≥ k), so they do not change
   ρ_{R_k}: spec ρ_{R_k}(ψ_j) = spec ρ_{R_k}(ψ_k) for all j ≥ k. Hence the entire entropy history
   (S(R_1), …, S(R_{N−1})) is a function of the single final state |ψ_N⟩ — its nested cuts — and |ψ_N⟩ is Haar.
   **The trajectory therefore has exactly the same joint distribution as the nested cuts of one Haar state.**
   The unitaries U_2 … U_N are statistically invisible in every spectral quantity of the radiation.
3. **"Restricted sense".** What is *not* true: (a) conditioned on the already-emitted radiation state ρ_{R_k}
   the remaining randomness is only Haar on B (the state is U_B-invariant, not freshly Haar on R ⊗ B);
   (b) the entropies at different k are *not* independent draws — they are strongly correlated because they come
   from one state. A comparison with "an independent Haar state for every k" matches every single-k
   distribution but has zero cross-k correlation.
4. **When it genuinely differs.** Only if an assumption is dropped: U_1 not acting on the whole system (or
   the initial state being mixed / entangled with a reference), or the scrambler not being Haar on the *whole*
   remaining hole. A unitary 2-design would still give the exact mean purity (dR+dB)/(dR dB+1) (Lubkin 1978)
   but is not guaranteed to reproduce the mean von Neumann entropy; a single brickwork layer of 2-qubit gates
   per emission (control below) falls far below Page.

## Numerical tests

All numbers: `results/c_evap_{full,isometry}_N*.json` (+ `_spectra.npz`), `results/c_ks_N{8,10}.json`,
`results/c_variants_N6.json`, `results/c_recheck_full_N13.json`, `results/c_summary.json`; figure
`figures/c_evaporation.png`. complex128 throughout; seed rule `manual_seed(3000 + 100 N + s)` (full) and
`+50000` (isometry). z = (mean S(R) − Page)/(sample stderr).

**Two samplers.** `full` draws the literal 2^{N−t+1}-dimensional Haar unitary at every step. `isometry` uses
the fact that the state has Schmidt rank r ≤ dim R, so only the action of U on the r-dimensional support in B
matters and that is a Haar isometry (reduced QR of a d × r Ginibre matrix): exact in distribution, memory
O(2^N) instead of O(4^N). The two agree (KS p = 0.88 at the Page time of N = 10, and see the tables).

| mode | N | seeds | device | max\|z\| over steps | max \|mean − Page\| [nats] | best wall / trajectory | peak GPU mem |
|---|---|---|---|---|---|---|---|
| full | 6–9 | 200 each | CPU | 0.82, 1.24, 1.65, 1.11 | 3.3e-3 … 1.5e-3 | 3.7 ms … 0.22 s | – |
| full | 10 | 100 | A100 | 2.84 | 2.9e-3 | 0.069 s | 0.10 GiB |
| full | 11 | 40 | A100 | 2.73 | 1.3e-3 | 0.17 s | 0.39 GiB |
| full | 12 | 20 | A100 | 1.96 | 8.6e-4 | 0.35 s | 0.83 GiB |
| full | 13 | 40 | A100 | 4.19 (see below) | 9.6e-4 | 0.93 s | 3.1 GiB |
| full | 14 | 20 | A100 | 1.94 | 6.7e-4 | 4.3 s | 12.3 GiB |
| isometry | 6–12 | 200 (100 at N = 12) | CPU | 1.31 … 2.24 | 4.0e-3 … 3.8e-4 | – | – |
| isometry | 13, 14, 15, 16, 18, 20 | 60, 40, 240, 20, 40, 20 | CPU | 1.66, 2.14, 2.20, 2.26, 1.89, 2.02 | 8.2e-4 … 8.5e-5 | – | – |
| isometry | 22 | 100 | A100 | 2.31 | 1.2e-5 | 0.62 s | 0.45 GiB |
| isometry | 24 | 100 | A100 | 2.42 | 9.2e-6 | 2.5 s | 1.8 GiB |
| isometry | 26 | 16 | A100 | 3.65 | 2.3e-5 | 12.7 s | 7.0 GiB |
| isometry | 27 | 1 | A100 | (single trajectory, no stderr) | 1.9e-5 | 28 s | 8.1 GiB |

* Pooled over the 296 (run, step) cells with ≥ 8 seeds: rms z = 1.11, 6.1 % with |z| > 2, max 4.19. Steps of
  one N are correlated (consecutive-step correlation ≈ 0.45, below), so these are not 296 independent tests.
* **The one |z| > 4 cell was followed up** (`experiments/c_recheck_full13.py`): full mode, N = 13, t = 2,
  seeds 4300..4339 gives z = +4.19; the run is bit-for-bit reproducible, seeds 4320..4339 alone give +6.09.
  Extending the same seed rule to 1000 trajectories gives z(t=2) = +1.36 and max |z| = 1.64 over all steps
  (seeds 4340..5299 alone: max |z| = 1.58). The sample std at t = 2 was 2.2e-4 in the 40-seed run versus
  3.2e-4 with 1000 seeds: for dim R ≪ dim B the distribution of S(R) is strongly skewed towards its upper
  bound ln dim R, so a 20–40 sample stderr is unreliable. Conclusion: small-sample fluctuation, no bias.
  The same caveat applies to the 16-seed N = 26 run (max |z| = 3.65) and to every run with few seeds.
* S(R) vs S(B): max |S(R) − S(B)| ≤ 5.3e-15 nats, with S(B) from an independent eigvalsh of ρ_B whenever
  dim B ≤ 2048 (otherwise both come from the same Schmidt spectrum and the equality is not an independent
  check). Mean purity matches the exact Haar value (d_R + d_B)/(d_R d_B + 1) (e.g. N = 13 step 6: 0.023455
  vs 0.023435, 40 seeds). Norm drift ≤ 1e-14.
* **Distribution, not only the mean** (`ks`, N = 10: 1000 sequential-isometry, 200 sequential-full and 1000
  directly sampled Haar states; N = 8: 4000/1000/4000). Two-sample KS tests of S(R) and of λ_max at every step
  against direct Haar states, of full vs isometry, and of the one-step increments S(R_{t+1}) − S(R_t) against
  increments between nested cuts of single Haar states: N = 10: 53 tests, smallest p = 0.055
  (Bonferroni-adjusted 1.0); N = 8: 41 tests, smallest p = 0.024 (adjusted 0.98). At the Page time of N = 10
  the std of S(R) is 0.0157 (sequential) vs 0.0152 (direct Haar). Consecutive-step correlations of S(R):
  0.43–0.52 for the sequential process, 0.44–0.51 for nested cuts of one Haar state (Fisher-z differences
  all |z| < 1.5), versus 0 for independently drawn Haar states at each step. No statistically significant
  difference from the law derived above was found; a non-rejection is of course not a proof — the proof is
  the invariance argument.
* **Controls that do differ** (`variants`, N = 6, 2000 samples): (V1) emitting a qubit *before* the first
  scramble gives exactly the Page curve of N − 1 qubits shifted by one step (z vs shifted Page within ±1.4,
  z vs unshifted Page down to −783); (V2) starting with 2 hole qubits maximally entangled with 2 early
  radiation qubits gives S(R) above the N-qubit Page value by 67, 31, 16, 7.6, 3.6 standard errors at steps
  1–5 — here U_1 does not act on the whole system and the Haar-on-R⊗B statement fails, as item 4 says.

## Runtime and memory (A100 40 GB, GPU 0, shared box)

* `full`: memory is dominated by the first unitary and its QR workspace, 16·4^N bytes per matrix (N = 14:
  4 GiB per matrix, 12.3 GiB peak; N = 15 would need ≈ 49 GiB peak, more than the card — not attempted).
  Wall time per trajectory grows ×2.7 per qubit on average over N = 10..14 (fitted log2 slope 1.43; the
  asymptotic QR cost is ×8 per qubit, visible in the last step 0.93 s → 4.3 s).
* `isometry`: state vector 16·2^N bytes; peak 0.45 GiB (N = 22), 1.8 GiB (24), 7.0 GiB (26), 8.1 GiB (27);
  wall time ×2.2 per qubit over N = 22..27 (fitted log2 slope 1.11). The peak is set by the tall QR near the
  middle of the evaporation; N = 28 was not run (estimated ≈ 16–30 GiB, ≈ 1 min per trajectory).
* Timings on the CPU runs were taken while other jobs used all cores and are not comparable; they are not
  used for scaling statements.

## Limitations

* Seeds are few at the largest sizes (20 at N = 14 full, 16 at N = 26, 1 at N = 27); the z-scores there are
  indicative only.
* The isometry sampler is exact in distribution but does not literally build the unitaries; the literal
  protocol is verified only to N = 14.
* Haar scrambling of the whole remaining hole at every step is the strongest possible scrambling assumption.
  Nothing here says how fast a physical hole scrambles, and none of this involves gravity.
