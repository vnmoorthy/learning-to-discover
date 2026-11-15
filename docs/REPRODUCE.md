# Reproduce

[Back to the README](../README.md) · [Architecture](ARCHITECTURE.md) · [Results](RESULTS.md) · [Sponsors](SPONSORS.md)

Four levels, from "no setup" to "the whole lab". Pick the one that answers your question.

| Level | You need | You get |
|---|---|---|
| [1. Replay](#1-replay-the-run) | Node 18+ | The mission control UI over the snapshotted run |
| [2. Verify](#2-verify-solutions-yourself) | Python 3.10+ | Official scores for any solution, on your machine |
| [3. Search](#3-run-a-search-strategy) | Python + numpy/numba/pysat (GPU for some) | One strategy running and logging |
| [4. The lab](#4-run-the-whole-lab) | API keys, a GPU box, Modal | The autonomous loop |

## 1. Replay the run

No keys, no backend. The replay reads `web/public/data/*.json`, the export of the live run.

```bash
cd web
npm install
npm run build:static
VITE_STATIC=1 npx vite preview --outDir dist-static     # prints the URL
```

Or open the hosted copy: <https://vnmoorthy.github.io/phoenixastar/>.

Every mutating button is disabled in replay mode and a banner states the snapshot time. To explore the UI with
no data at all, `npm run dev:fixtures` runs an in-browser simulated backend (labelled as simulated).

## 2. Verify solutions yourself

Each problem directory holds the official EinsteinArena verifier and the public best solutions:

```text
problems/<slug>/verifier.py          evaluate(solution: dict) -> float, raises on an invalid solution
problems/<slug>/meta.json            scoring direction, minImprovement, solution schema
problems/<slug>/best_solutions.json  the public leaderboard entries with their data
problems/<slug>/description.md
```

Score any solution the same way the critic does (a subprocess, JSON on stdin):

```bash
python3 -m ltd.verify_worker sidon-45-set < my_solution.json
# {"ok": true, "score": 0.5714285714285714, "error": null, "seconds": 0.025}
```

For example, re-verify the current record for a problem:

```bash
python3 - <<'EOF' | python3 -m ltd.verify_worker sidon-45-set
import json
rows = json.load(open("problems/sidon-45-set/best_solutions.json"))
print(json.dumps(min(rows, key=lambda r: float(r["score"]))["data"]))   # use max(...) for maximize problems
EOF
```

A solution is a record only if it is strictly better than the top of the leaderboard by at least `minImprovement`
(`ltd/config.py: beats_record`).

The exact negative result for Sidon sets takes about a minute on one core:

```bash
python3 search/sidon_extend.py        # compare with runs/sidon_extend.log
```

## 3. Run a search strategy

```bash
python3 -m pip install numpy numba sympy python-sat     # torch as well for the *_gpu strategies
```

numba must match your numpy (at the time of writing numba required NumPy 2.4 or older).

Templates, parameters, ranges and defaults are declared in [`search/TEMPLATES.json`](../search/TEMPLATES.json).
Each script documents its method in its module docstring. Examples:

```bash
python3 search/nothree_sat.py --sym rot180-150 --seed 1 --solver cadical195 --presolve-slopes 2
python3 search/twodel_ils.py  --seed 1 --mode from_record --algo ils --seconds 300
python3 search/sidon_sa.py    --seed 1 --n 15 --target 8 --seconds 300
python3 search/spencer_gpu.py --n 20 --D 8 --seed 0 --init paley      # needs a CUDA GPU
```

Conventions: one parseable progress line per step in the log, `FOUND_*.json` with `{"solution": ...}` only after
the script's own exact check. Then verify it as in level 2.

Tests that tie the search objectives to the official verifier:

```bash
python3 search/test_strategies.py          # objectives == official verifier on public bests and random inputs
python3 search/test_strategies_cli.py      # end-to-end CLI runs with test- ids in a throwaway directory
```

## 4. Run the whole lab

### Install

```bash
python3 -m pip install fastapi uvicorn sse-starlette httpx openai modal tinker \
                       numpy numba sympy python-sat torch matplotlib
cd web && npm install && npm run build && cd ..
```

Developed on Python 3.12 (laptop) and Python 3.10 (GPU box).

### Keys

Create `.env` in the repo root (git-ignored). Only the names are listed here; never commit values.

```text
OPENAI_API_KEY=
EXA_API_KEY=
PAST_API_KEY=
TINKER_API_KEY=
DEVIN_API_KEY=
```

Each part degrades on its own: without a key, that part of the lab is unavailable and the rest keeps running
(a failing proposer leaves the deterministic planner in charge; a failing referee abstains).

### Compute

1. **GPU box.** Edit `scripts/ssh_config` so the host alias `ltd` points at your machine (user, address, key
   path). The lab only ever runs `ssh -F scripts/ssh_config ltd '<cmd>'`. Code is synced to `~/ltd` on the box
   (`search/` and `scripts/`); the box needs Python 3.10+, numpy, numba, python-sat and torch with CUDA.
   Capacity constants (8 GPUs, 124 cores, target 118 busy) are in `ltd/config.py`.
2. **Modal.** `modal token new`, then `modal deploy ltd/modal_fleet.py` for the CPU fleet (redeploy after
   changing search code). The sandbox app is created on first use.
3. **Referee.** Install the Claude Code CLI so that `claude` is on `PATH`.

### Start

```bash
LTD_LOOP_AUTOSTART=0 LTD_TEST_MODE=1 python3 -m ltd.server    # first run: paused, stops are dry runs
python3 -m ltd.smoke                                          # read-only check of every GET endpoint
python3 -m ltd.server                                         # for real: http://127.0.0.1:8787
```

Searches that are already running on the box are adopted, not restarted. Pause, resume and "run cycle now" are
buttons on Mission Control (and `POST /api/loop/pause | resume | run-now`).

### The side systems

```bash
python3 -m ltd.sandboxes sidon-45-set 8                       # 8 LLM-written programs in Modal sandboxes
python3 -m ltd.learning 12                                    # 12 Tinker RL steps in the foreground
python3 -m ltd.modal_fleet launch nothree_sat '{"sym":"rot180-150","seed":1}'
python3 -m ltd.modal_fleet telemetry
python3 -m ltd.referee                                        # referee demo on two sample proposals
curl -X POST http://127.0.0.1:8787/api/memory/benchmark       # past.dev vs markdown vs RAG
```

### Export and publish

```bash
python3 -m ltd.snapshot               # live DB -> web/public/data/*.json
python3 docs/update_results.py        # refresh the result blocks in README.md and docs/RESULTS.md
cd web && npm run build:static        # -> web/dist-static, the GitHub Pages site
```

`python3 docs/update_results.py --check` exits non-zero when the committed docs are stale against the data.

### Renders

```bash
bash viz/build_all.sh                 # needs Blender; scripts in viz/scripts/ were written by GPT-6 Astra
```

Every prompt, script version and model reply is kept next to the script (`viz/scripts/<name>.vN.*`).

## What you will not reproduce exactly

- **Search trajectories.** GPU searches and SAT portfolios depend on seeds, hardware and timing. Verified
  solutions are reproducible; the path to them is not.
- **Model outputs.** Proposals, queries and sandbox programs come from hosted models. The replay shows what they
  said in this run; a new run will say something else.
- **The leaderboard.** Records are the EinsteinArena values on Nov 15 2026, cached in `problems/` and `arena/`.

## Troubleshooting

- **The UI says "not a JSON reply".** Something else is listening on port 8787. Set `LTD_PORT`.
- **`Numba needs NumPy 2.4 or less`.** Downgrade numpy or upgrade numba; the CPU strategies need numba.
- **The referee always abstains.** `claude` is not on `PATH`, or the call exceeded `LTD_REFEREE_TIMEOUT`.
- **A GPU strategy refuses to launch on Modal.** By design: `GPU_AVAILABLE = False` in `ltd/modal_fleet.py`.
