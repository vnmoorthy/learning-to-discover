# Event Horizon — 4-minute demo: one real research cycle

The cycle shown is **C: sequential Haar evaporation** (`results/research_log.json`, id `C`). Every number on screen comes from a stored result file or is recomputed live; nothing is typed in by hand.

Say this first (10 s): *"These are qubit toy models without gravity. Nothing here solves the information paradox. We reproduce known results, at sizes a laptop cannot reach, and show how an error was caught and corrected."*

## Setup (before the demo)

```bash
SSHC=<repo>/scripts/ssh_config
ssh -F $SSHC ltd
cd ~/event-horizon; export CUDA_VISIBLE_DEVICES=0 OMP_NUM_THREADS=4; PY=.venv/bin/python
```

Steps 1, 2, 5, 6, 7 also run on the Mac with plain `python3` from `problems/event-horizon` (they only read `results/`). Steps 3 and 4 need the box.

Optional, start now so it finishes during the talk (about 70 s, CPU only, writes to `/tmp`):

```bash
$PY verify/independent.py --quick --out /tmp/eh_verify_quick.json > /tmp/eh_verify_quick.log 2>&1 &
```

## Timeline

| Time | Step | Command or figure | What to say |
|---|---|---|---|
| 0:00 | **1. Question** | open `figures/d_hawking_pairs.png` | Hawking's picture, as independent Bell pairs, gives radiation entropy k ln 2 that never comes down. If instead the hole scrambles unitarily and emits its own qubits one at a time, what does the entropy do, and is it any different from Page's random-state curve? |
| 0:30 | **2. Formulation** | paper Sec. 4.4 (`paper/event_horizon.md`) | N qubits in \|0…0⟩. Each step: fresh Haar unitary on the remaining hole, then one qubit moves to the radiation. Record S(R) after every emission. |
| 0:50 | **3. Derived prediction** | `$PY scripts/demo_cycle_c.py predict` | Haar measure is left-invariant, so every intermediate state is exactly Haar. Prediction: mean S(R_t) equals Page's formula with no correction; deficit exactly ½ nat at the half-way point; consecutive steps correlated like nested cuts of one state. |
| 1:20 | **4. GPU simulation** | `$PY scripts/demo_live_gpu.py 12 10` (live, about 3 s on GPU 0, writes nothing), then `$PY scripts/demo_cycle_c.py gpu` | Live: ten literal trajectories at N = 12, each drawing 4096×4096 down to 2×2 Haar unitaries. Stored: literal protocol to N = 14 (12.3 GiB), isometry sampler to N = 26 (7.0 GiB). N = 15 literal would need about 49 GiB, so we stopped. |
| 2:00 | **5. Comparison** | `$PY scripts/demo_cycle_c.py compare`, then open `figures/c_evaporation.png` | N = 14: every step within 2 standard errors of Page; S(R) = S(B) to 2e-15. Pooled over 296 cells rms z is 1.11. But one cell is at z = 4.19. |
| 2:35 | **6. Critic objection** | `$PY scripts/demo_cycle_c.py critic` | The critic asks: bias or fluctuation? The same 40 seeds reproduce 4.19 bit for bit; seeds 20–39 alone give 6.09. With 1000 trajectories z falls to 1.36. The entropy distribution is skewed when the radiation is small, so a 40-sample standard error is too small. Second objection, accepted: since the state is exactly Haar, the big isometry runs are reference Page curves, not extra tests of the dynamics. |
| 3:10 | **7. Independent verification** | `$PY scripts/demo_cycle_c.py verify` (stored), or `tail -3 /tmp/eh_verify_quick.log` if the background run finished | A second implementation that shares no code (scipy unitaries, CPU, opposite qubit ordering) gets max \|z\| = 1.26 against exact Page and 1.52 against the builder. Across the project 8 of 9 claims agree. The ninth was a sign error in a hand-off report: scrambled Clifford states sit 0.088 ± 0.015 nats *below* Page, not above. It was corrected before it reached any file. |
| 3:40 | **8. Conclusion** | `$PY -c "import json;c=[x for x in json.load(open('results/research_log.json'))['cycles'] if x['id']=='C'][0];print(c['conclusion']);print('class:',c['classification'])"` | Sequential Haar evaporation reproduces Page at every step; class 2, with class-3 trajectory tests. It is a reproduction, not a resolution: the model assumes unitarity and maximal scrambling. The island formula is a separate gravitational argument that we describe but do not test. |

## Backup material

* Tests: `$PY -m pytest -q tests` (109 passed in about 21 s on the box).
* Notebook, all six cycles at small size on CPU in about 22 s: `$PY notebooks/run_notebook.py`, then open `notebooks/event_horizon.ipynb`.
* Full verifier: `$PY verify/independent.py --out /tmp/eh_verify_full.json` (about 4 min).
* All step outputs at once: `$PY scripts/demo_cycle_c.py all`.
* Dashboard data: `results/dashboard.json`; cycle records: `results/research_log.json`; paper: `paper/event_horizon.md`.

## Numbers you may be asked for

| Item | Value |
|---|---|
| Page formula, 124 (m, n) pairs up to m·n = 2^24 | max \|z\| = 2.69, rms z = 1.00 |
| Bell pairs | \|S(R) − k ln 2\| ≤ 4.4e-15 nats |
| Local Haar brickwork, deviation from Page at depth 8 per emission | 0.04–0.08 nats for N = 8..26 |
| One-shot scrambling depth, Haar brickwork | D* ≈ 1.87 N + 1.9 layers (N = 8..24, threshold 0.05 nats, no error bars) |
| Hayden-Preskill, old hole, k = 1 | 90 % of the mutual information after m = 2 qubits, 99 % after m = 4, for every hole size 3..12 |
| Decoupling bound | measured T is 0.83–0.87 of the bound |
| Largest exact states | 26 qubits (27 once) on one A100 40 GB |

## What not to claim

* Not a solution of the information paradox, and not a test of the island formula.
* "Page time" here is a count of emitted qubits, not a physical time.
* The z = 3.38 (A, N = 24) and z = 3.65 (C, N = 26) cells were not followed up.
* The large-N GPU numbers were not re-run by the verifier.
