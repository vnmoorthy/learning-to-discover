# Event Horizon — reproducible toy-model numerics around the black hole information paradox

Finite-dimensional quantum-information experiments: the Page curve of random pure states, Page's theorem,
sequential "evaporation" with Haar scrambling, the Bell-pair "Hawking" toy model (and, in `e1_*`/`e2_*`,
scrambling and Hayden–Preskill).

**What this is not.** Nothing here solves, or claims to solve, the information paradox. Every model is a
qubit toy model without gravity. The semiclassical-gravity derivations of a Page curve (quantum extremal
surfaces / islands: Penington 2019; Almheiri, Engelhardt, Marolf, Maxfield 2019) are a separate line of
argument and are only mentioned for context; no result here tests them.

Finding classes used throughout: 1 reproduction, 2 verification of a known relation, 3 new computational
observation within an existing model, 4 new conjecture, 5 potentially novel result needing investigation.
Everything in Problems A–D is class 1–2, with the trajectory-level tests of C class 3 (they confirm an
elementary exact statement). No class 4 or 5 claim is made.

## Layout

| Path | Content |
|---|---|
| `eh/qstates.py` | Haar states/unitaries/isometries (QR of complex Ginibre + phase fix, Mezzadri 2007), numpy and torch-cuda backends; partial trace for arbitrary bipartitions; Schmidt spectrum |
| `eh/entropy.py` | von Neumann entropy from eigenvalues / Schmidt probabilities (clipped at `CLIP = 1e-15`, never `log 0`), Rényi-2, purity |
| `eh/page.py` | Page's formula `S = H_{mn} − H_n − (m−1)/(2n)` (m ≤ n): exact rationals (`fractions`) for small arguments, digamma for large; nats and bits; asymptotic series (checked with SymPy) |
| `eh/pairs.py` | Bell-pair "Hawking" toy model |
| `tests/test_core.py` | core invariants + Page formula vs Monte Carlo (`tests/test_evaporation.py`: Problem C invariants) |
| `experiments/a_page_curve.py` | Problem A: Page curve, N = 8..20 (+22, 24) |
| `experiments/b_page_theorem.py` | Problem B: Monte Carlo vs exact vs asymptotic, 124 (m, n) pairs up to m·n = 2^24 |
| `experiments/c_evaporation.py` | Problem C: sequential Haar evaporation (`run`, `ks`, `variants`, `plot`); `c_recheck_full13.py`: follow-up of one outlier |
| `experiments/d_hawking_pairs.py` | Problem D: k Bell pairs vs C |
| `notes/A_derivation.md`, `notes/C_analysis.md`, `notes/D_derivation.md` | derivations and the analysis of the numbers |
| `results/*.json`, `results/*.npz`, `results/b_page_theorem_table.md` | numbers behind every figure, seeds and parameters included |
| `figures/*.png` | dark-theme figures, dpi 160 |
| `logs/` | raw run logs from the GPU box (including the pytest output) |

Files named `*_cpu.py`, `c_modal.py`, `modal_run.py` and the `results/c_log_*`, `results/c_cache`,
`results/raw` entries are leftovers of an earlier laptop-only attempt and are not used by the results reported here.

## How to run (GPU box: 8x A100 40 GB, GPU 0 only)

```bash
SSHC=<repo>/scripts/ssh_config
# 1. push the source (the Mac copy is the source of truth)
rsync -az --exclude .venv --exclude results --exclude figures --exclude logs --exclude __pycache__ \
      -e "ssh -F $SSHC" problems/event-horizon/ gpubox:event-horizon/
# 2. one-time venv on the box (system torch 2.7 + CUDA is reused; see requirements.txt for the numpy pin)
ssh -F $SSHC ltd 'python3 -m venv --system-site-packages ~/event-horizon/.venv && \
  ~/event-horizon/.venv/bin/pip install -q -r ~/event-horizon/requirements.txt'
# 3. on the box
ssh -F $SSHC ltd
cd ~/event-horizon; export CUDA_VISIBLE_DEVICES=0 OMP_NUM_THREADS=4; PY=.venv/bin/python
$PY -m pytest tests/test_core.py tests/test_evaporation.py -v            # ~40 s
run(){ n=$1; shift; (setsid nohup "$@" > logs/$n.log 2>&1 &); }          # detached: survives logout
run a  $PY experiments/a_page_curve.py                                   # ~8 min   (--replot redraws only)
run b  $PY experiments/b_page_theorem.py                                 # ~7 min, checkpointed (results/b_partial.json)
run c1 $PY experiments/c_evaporation.py run --mode isometry --Ns 6 7 8 9 10 11 12 13 14 15 16 18 20 22 24 26
run c2 $PY experiments/c_evaporation.py run --mode full --Ns 6 7 8 9 10 11 12 13 14   # literal 2^N x 2^N unitaries
run c3 $PY experiments/c_evaporation.py ks --N 10 --seeds 1000 --full-seeds 200       # distribution tests
run c4 $PY experiments/c_evaporation.py variants --N 6 --seeds 2000                   # controls that DO differ
$PY experiments/c_evaporation.py plot                                    # figure + results/c_summary.json
$PY experiments/d_hawking_pairs.py                                       # after C (uses its trajectories)
# 4. back on the Mac
rsync -az -e "ssh -F $SSHC" gpubox:event-horizon/results gpubox:event-horizon/figures gpubox:event-horizon/logs \
      problems/event-horizon/
```

`EH_DEVICE=cpu` forces the CPU backend (the small-N runs of C were made that way, see `scripts/launch_c_cpu.sh`;
each result JSON records its device). The scripts fall back to numpy/CPU on a laptop without CUDA; the
torch tests are then skipped.

## Conventions

* Entropies in nats unless a column says bits. Eigenvalues are clipped to `[1e-15, ∞)` only inside the logarithm.
* Seeds: every result JSON has a `seed_rule` / `torch_seed` field; all runs are complex128.
* z = (Monte Carlo mean − Page) / (sample standard error). Cuts of the same state are correlated, so z values
  within one N are not independent.

## Results in one screen (details and limitations: `notes/`)

* **Tests**: `tests/test_core.py` 49 passed; `tests/test_evaporation.py` 5 passed (`logs/pytest_core_final2.log`,
  `logs/pytest_core_final.log`).
  Whole suite incl. `tests/test_ext.py` (extensions): **109 passed in 21.3 s** (`logs/pytest_verifier.log`).
* **A** (class 1/2): 213 cells (N, k), N = 8..24: max |z| = 3.38 (N = 24, 8 states), 2.66 for N ≤ 20; rms z = 1.05;
  max |S(R) − S(B)| = 5.3e-15.
* **B** (class 2): 124 (m, n) pairs, m·n up to 16 777 216 (incl. m = n up to 4096): max |z| = 2.69, rms z = 1.00,
  4.0 % with |z| > 2, none > 3; Monte Carlo error slope −0.476 (expected −0.5). The asymptotic
  `ln m − m/(2n)` errs by −0.140 nats at (2, 2) and by −3.0e-8 ≈ −1/(2mn) at m·n = 2^24; including the next
  term `+1/(2mn)` reduces the error to −1.5e-2 at (2, 2), −2.0e-8 at (2048, 2048) and at most 1.3e-9 for the
  m·n = 2^24 rows with m ≤ 2048 (`results/b_page_theorem_table.md`).
* **C** (class 2/3): sequential Haar evaporation reproduces Page's mean at every step and — as proven in
  `notes/C_analysis.md` — the whole entropy trajectory has exactly the law of the nested cuts of a single Haar
  state. Literal full-unitary runs to N = 14 (12.3 GiB peak), exact-in-distribution isometry sampler to N = 26
  (7.0 GiB), one N = 27 trajectory.
* **D** (class 1/2): k Bell pairs give S(R) = k ln 2 to 4.4e-15; exceeds the remaining hole's capacity
  (N − k) ln 2 for every k > N/2.

## Independent verification

`verify/independent.py` re-derives the key numbers without importing `eh/` (scipy `unitary_group`, CPU numpy,
Philox RNG, exact rational Page values, explicit-loop partial traces): `results/verification.json` (claim by
claim), `results/verification_raw.json` (all numbers), `notes/critic.md` (objections, fixed / open).
Run on the box: `OMP_NUM_THREADS=4 .venv/bin/python verify/independent.py` (~4 min, CPU only).
All reproduced numbers agree within the stated Monte Carlo errors. One interpretive statement was corrected:
scrambled Clifford (stabilizer) states lie on average **below** the Page value at the half cut
(0.088 ± 0.015 nats at N = 10), not above it — see `notes/critic.md`.

## Paper, notebook, demo, dashboard data

| Path | Content |
|---|---|
| `paper/event_horizon.md` | the write-up: derivations, methods, results with classes 1-5, island formula as a separate theory section, limitations (no PDF: pandoc is not installed) |
| `notebooks/event_horizon.ipynb` | small-size CPU reproduction of A, B, C, D, E1, E2 (executed: 10 code cells, 22 s, 0 errors); rebuild with `python notebooks/build_notebook.py`, execute with `.venv/bin/python notebooks/run_notebook.py` |
| `results/research_log.json` | research cycles A, B, C, D, E1, E2 (question ... conclusion, classification) |
| `results/dashboard.json` | title, summary, figures with captions, tests, verification summary, hardware |
| `DEMO.md` | 4-minute walk through cycle C; helpers `scripts/demo_cycle_c.py` (reads stored results) and `scripts/demo_live_gpu.py` (live literal run, writes nothing) |

## References (existence checked)

* D. N. Page, "Average entropy of a subsystem", Phys. Rev. Lett. 71, 1291 (1993).
* D. N. Page, "Information in black hole radiation", Phys. Rev. Lett. 71, 3743 (1993).
* S. K. Foong and S. Kanno, Phys. Rev. Lett. 72, 1148 (1994); J. Sánchez-Ruiz, Phys. Rev. E 52, 5653 (1995);
  S. Sen, Phys. Rev. Lett. 77, 1 (1996), arXiv:hep-th/9601132 — proofs of Page's formula.
* E. Lubkin, J. Math. Phys. 19, 1028 (1978) — mean purity of a random subsystem.
* F. Mezzadri, "How to generate random matrices from the classical compact groups", Notices AMS 54, 592 (2007).
* P. Hayden and J. Preskill, JHEP 0709:120 (2007).
* G. Penington, arXiv:1905.08255; A. Almheiri, N. Engelhardt, D. Marolf, H. Maxfield, arXiv:1905.08762 (JHEP 12 (2019) 063).
