# Phoenixastar: build spec (single source of truth for every builder)

Hackathon: Iterate AI Research Hackathon, SF, Track 1 ("Build your own autoresearch framework: can your system
beat a best-known result in mathematics on its own?"). Judged on how far past the record we get, how new the
loop is, and whether every decision can be followed (the log). Sponsor challenges entered: Exa (Exa in the main
loop), past.dev (multi-agent memory, benchmarked vs markdown and RAG), Modal (parallel agent sandboxes),
Originator. Overall prize includes Tinker + OpenAI credits, so Tinker self-training and OpenAI models are core.

Tagline: **An AI lab that gets better at discovering mathematics by doing it.**

## 0. Ground rules for every builder

- Repo root: `<repo>` (call it `ROOT`). Stay inside your
  own directory (listed per builder). Never edit another builder's files.
- Secrets: API keys live in `ROOT/.env` (git-ignored). Load them ONLY with `import envload; envload.load()`
  (adds to `os.environ`). Never print, log, commit, or send a key anywhere except the provider's own API.
  Never copy `.env` to the GPU box or to Modal.
- Python 3.12 on the Mac (`python3`), anaconda env: fastapi, uvicorn, sse-starlette, httpx, openai 1.75,
  modal 1.5.4, tinker 0.39, numpy, pandas, sympy, numba, torch are installed. `pip3 install` more if needed.
- The GPU box: 8x A100 40GB, 124 CPU cores, Ubuntu, Python 3.10, reached ONLY via
  `ssh -F ROOT/scripts/ssh_config ltd '<cmd>'` (host alias `ltd`, user ubuntu, code in `~/ltd`).
  It is RUNNING LIVE SEARCHES that must not be disturbed. Read-only commands are fine
  (`python3 -B ~/ltd/scripts/telemetry.py`, `cat`, `ls`, `tail`, `nvidia-smi`). Never `pkill`/`kill` anything you
  did not start yourself; anything you start for testing must carry an id starting `test-` and be stopped by you.
  NEVER use `pkill -f <pattern>` where the pattern also appears in your own ssh command line (it kills the
  session); use the `[x]yz` bracket trick or pid files.
- No posting to EinsteinArena or any public site. Reading public GET endpoints is fine.
- Everything must actually work. No placeholder buttons, no fake data presented as real. If something is a
  snapshot or simulated, label it in the UI.

## 1. The problems (records from the live EinsteinArena leaderboard, Nov 15 2026)

Local copies: `ROOT/problems/<slug>/{verifier.py, meta.json, description.md, best_solutions.json}`.
`verifier.py` exposes `evaluate(solution: dict) -> float` (raises on invalid). Official, exact, integer math.

| slug | scoring | record (holder) | our status |
|---|---|---|---|
| no-three-in-line-75 | maximize | 148 (Thomas-Prellberg); 149 = new record, 150 settles D(75)=150 | ~110 SAT solvers, 5 symmetry classes |
| spencer-discrepancy | maximize | 1.697749375254331 = 7/sqrt(17) (Youhua-Li) | GPU tabu, n=20 D=8 and n=18 D=8 |
| hadamard-det-51 | maximize | 43.33745596194037 (kgrey), log10|det| | GPU batched tabu from record matrices |
| sidon-45-set | minimize | 0.5714285714285714 = 4/7 (Ma-Tang) | exact extension search (proved: no 1-point extension; none of 2 points in [-3000,4000]) |
| two-deletion-code-16 | maximize | 226 (kgrey) | strategy to be built |
| snake-in-the-box-13 | maximize | 2950 (kgrey) | not attacked (optional) |
| ring-loading-15 | maximize | 1.125 (JSAgent-Ring15) | not attacked (optional) |

## 2. Search strategies on the GPU box (`ROOT/search/`, synced to `~/ltd/search/`)

Each strategy is a CLI script. Outputs go to `~/ltd/runs/<family>/`. A verified record writes `FOUND_*.json`
containing `{"solution": <dict accepted by verifier.evaluate>, ...}`.

| template | script | params | resource | logs / artifacts |
|---|---|---|---|---|
| spencer_gpu | search/spencer_gpu.py | --n --D --seed --init {random,paley} --tenure --restart | 1 GPU | runs/spencer/gpu<k>.log lines `[n=20 D=8 seed=0] t=..s step=.. best_bad=..`; runs/spencer/log_n{n}_D{D}_s{seed}.jsonl with `rows` (bitmasks, bit j=1 means -1) of the best matrix |
| hadamard_gpu | search/hadamard_gpu.py | --seed --chains --perturb --tenure --restart --target | 1 GPU | runs/hadamard/gpu<k>.log `[s6] t=..s step=.. best_log10=..` |
| nothree_sat | search/nothree_sat.py | --sym {mirror-149,rot180-150,diag-149,diag-150,none-149,none-150} --seed --solver {cadical195,glucose4,maplechrono} --presolve-slopes | 1 CPU core | runs/nothree/<sym>_s<seed>.log `[mirror-149 s0] round 7 points=149 violated_lines=212 lines=3184 t=95s`; runs/nothree/latest_<sym>_s<seed>.json = `{sym, seed, round, count, violated, lines_added, t, points:[[x,y]], violated_lines:[[[x1,y1],[x2,y2],m]]}` (current model with fewest violated lines) |
| sidon_extend | search/sidon_extend.py | (none) | 1 CPU core | runs/sidon_extend.log |
| (new) twodel_ils, sidon_sa, ... | built by the strategies builder | see that builder | CPU | same conventions |

`scripts/telemetry.py` (runs on the box) prints one JSON snapshot:
`{time, problems:{slug:{runs|classes, found:[paths], procs}}, gpus:[{idx,util,mem}], load1, cpus}`.
Launcher used today: `scripts/launch_nothree.sh`. Processes already running were started by hand; the backend
must ADOPT them (discover via `pgrep -af "[s]pencer_gpu.py|[h]adamard_gpu.py|[n]othree_sat.py"`), not restart them.

## 3. Backend (`ROOT/ltd/` Python package + `ROOT/ltd/server.py`), runs on the Mac

Start: `python3 -m ltd.server` -> http://127.0.0.1:8787 (serves API under `/api` and the built frontend from
`ROOT/web/dist` at `/`). The autonomous loop runs in a background thread inside the server process.
State persists in `ROOT/data/ltd.sqlite` (decisions, telemetry history, memory facts, literature, artifacts) so a
restart keeps history. `ROOT/data/` is git-ignored except `ROOT/data/snapshot/` (see section 6).

### Modules
- `ltd/config.py`: paths, problem registry (slug, title, scoring, record, holder, family, metric), model names:
  `PROPOSER_MODEL = "gpt-6-astra"` (fallback `gpt-5.5`), `FAST_MODEL = "gpt-5.4-mini"`, loop interval (default 300 s).
- `ltd/box.py`: SSH wrapper (subprocess `ssh -F scripts/ssh_config ltd`), with timeouts. Functions: `telemetry()`,
  `list_processes()` (pid, cmdline, parsed template + params), `launch(strategy_id, template, params, resource)`,
  `stop(strategy_id)` (pid file `~/ltd/runs/strategies/<id>.pid`; for adopted processes, by pid), `fetch(path)`,
  `sync_code()` (rsync `search/` and `scripts/`). Launch command lines come ONLY from `ltd/strategies.py`.
- `ltd/strategies.py`: registry of templates with JSON-schema-like param specs (types, ranges, enums), resource
  type (gpu|cpu) and a `command(params)` builder. Validation rejects anything outside the schema. GPU assignment
  uses `CUDA_VISIBLE_DEVICES` of a free GPU (a GPU is free if no adopted/launched strategy owns it).
- `ltd/ledger.py`: SQLite event store. Tables: `decisions`, `telemetry`, `facts`, `literature`, `artifacts`,
  `strategies`, `learning`. Every agent action is a `decision` row (schema in section 4).
- `ltd/literature.py` (**Exa**, main loop): for a problem, the proposer asks for queries; run `exa search`
  (+ contents/highlights) via the Exa REST API (`https://api.exa.ai/search`, header `x-api-key`), store
  title/url/published date/highlights, return compact cards to the proposer. Cache by query. Each card that the
  proposer cites is linked to that decision.
- `ltd/memory.py` (**past.dev**): agents = `planner`, `proposer`, `critic`, and one `agent:<slug>` per problem.
  `write(agent, problem, text, tags)` -> past.dev ingest (`POST https://app.past.dev/api/v1/ingest`, Bearer
  `PAST_API_KEY`, body `{id, content, label, timestamp, identity, metadata}`) + local `facts` row.
  `recall(agent, query, k)` -> `POST https://app.past.dev/api/v1/recall` body `{query, identity, level:"high",
  limit}`; record which agent read which fact (`read_by`). Use identity = `"ltd-lab"` for the shared space (so
  agents read each other's facts) and put the writer agent in metadata. Also keep two baselines for the
  benchmark: a markdown file `data/memory.md` (append-only) and a small RAG (OpenAI `text-embedding-3-small` +
  cosine top-k over the same facts).
- `ltd/memory_bench.py`: builds a QA set from facts (question -> expected fact), runs past.dev vs markdown
  (whole file in context) vs RAG; measures accuracy (LLM judge with FAST_MODEL, exact rubric), latency (ms),
  cost (tokens -> USD). Saves results to `learning` table key `memory_benchmark` and `data/snapshot/memory_benchmark.json`.
- `ltd/proposer.py` (**OpenAI**): one call per cycle with the Responses API (`client.responses.create`), JSON
  output validated against a schema: `{decisions:[{problem, action: launch|stop|keep|research|note,
  template?, params?, strategy_id?, rationale, prediction:{metric, expected, horizon_min}, cite:[literature_ids],
  memory_used:[fact_ids]}]}`. Input = compact state (telemetry per problem, gaps to record, strategy history with
  outcomes, recalled memory facts, literature cards, budget: free GPUs/cores). Must never exceed free resources.
- `ltd/planner.py`: deterministic layer under the LLM: computes per-problem progress rate and a UCB-style
  priority (gap closed per compute-hour, staleness), enforces budgets, kills strategies that are provably dead
  (UNSAT, no progress for N cycles) and turns proposer output into executable, validated actions.
- `ltd/critic.py`: (a) verifies every `FOUND_*` artifact by running the OFFICIAL verifier from
  `problems/<slug>/verifier.py` in a subprocess with a timeout (never trust the search's own claim); a record is
  only declared if `evaluate()` beats the leaderboard top by more than `minImprovement` (from meta.json);
  (b) scores past predictions: for each decision whose horizon has passed, compares predicted vs observed metric
  -> verdict `confirmed|refuted`, writes a lesson fact to memory.
- `ltd/sandboxes.py` (**Modal**, agent sandboxes): the proposer can emit `action: "sandbox"` with Python code
  (a self-contained search program printing one JSON solution on its last stdout line) for cheap problems
  (sidon-45-set, spencer-discrepancy n<=20, ring-loading-15). Run N programs in parallel in
  `modal.Sandbox.create(...)` (image: debian_slim + numpy + numba), 120 s timeout each, no network, no secrets;
  verify outputs locally with the official verifier; log every program + score as decisions.
- `ltd/learning.py` (**Tinker**, self-improvement): RL fine-tuning of an open model (default
  `Qwen/Qwen3-8B` LoRA, fallback `openai/gpt-oss-20b`) to output constructions for a cheap verifiable problem
  (sidon-45-set: integer sets; reward = official verifier score transformed so lower h/|A| is better, invalid
  = 0). GRPO-style: per step sample G=16 completions per prompt, advantages = reward - mean, importance-sampling
  policy-gradient loss via `forward_backward` + `optim_step`, save sampler weights each K steps; log reward mean,
  best, valid-rate per step to the `learning` table. Also a transfer eval: evaluate gen-0 vs gen-N sampler on a
  held-out variant (e.g. spencer-discrepancy small n) with the same budget. Endpoint starts it in a background
  thread; status/progress via `/api/learning`.
- `ltd/loop.py`: the cycle: `telemetry -> critic(found + predictions) -> memory recall -> literature (if
  stalled/new) -> proposer -> planner -> execute (box/sandboxes) -> memory write -> ledger`. Phase is published
  to SSE. Pause/resume/run-now supported. A cycle must never crash the server (catch, log as decision
  `agent:"system", action:"error"`).
- `ltd/server.py`: FastAPI app (section 4), SSE via sse-starlette, CORS for localhost:5173.

## 4. HTTP API contract (frontend and backend must match exactly)

All JSON. Times are ISO-8601 UTC strings. Scores are numbers in the problem's own units.

- `GET /api/state` ->
```
{ "now": str,
  "loop": {"status": "running"|"paused", "cycle": int, "phase": "idle"|"telemetry"|"critic"|"memory"|"literature"|"propose"|"plan"|"execute",
           "next_cycle_at": str|null, "interval_s": int, "proposer_model": str, "started_at": str},
  "compute": {"gpus": [{"idx": int, "util": int, "mem_mb": int, "problem": str|null, "strategy_id": str|null}],
              "cpus": int, "load1": float, "cpu_procs": {"<slug>": int}, "box": "online"|"offline"},
  "problems": [ProblemSummary],
  "totals": {"decisions": int, "cycles": int, "experiments_run": int, "sandboxes_run": int, "facts": int, "sources": int, "records": int} }
```
- `ProblemSummary` =
```
{ "slug": str, "title": str, "scoring": "maximize"|"minimize",
  "record": {"score": float, "holder": str},
  "ours": {"score": float, "verified": bool, "at": str, "strategy_id": str|null} | null,
  "beats_record": bool,
  "metric": {"name": str, "value": float|null, "target": float|null, "lower_is_better": bool},
  "status": "searching"|"stalled"|"record"|"idle"|"proved-negative",
  "compute": {"gpus": int, "cpu_procs": int, "share": float},
  "strategies": [{"id": str, "template": str, "params": {}, "resource": "gpu"|"cpu", "started_at": str|null, "adopted": bool, "metric_value": float|null}] }
```
  `metric` is the live progress signal: spencer `bad_vectors` (target 0), hadamard `best_log10` (target record),
  no-three `min_violated_lines` (target 0), sidon `best_score`, two-deletion `best_size`.
- `GET /api/problems/{slug}` -> ProblemSummary plus
  `{"description_md": str, "leaderboard": [{"rank": int, "agent": str, "score": float}], "metric_history": [[str_time, float]],
    "artifact": <see below>|null, "templates": [{"name": str, "resource": str, "params": {"<p>": {"type": "int"|"float"|"enum", "min"?, "max"?, "values"?, "default"}}}]}`
  Artifacts:
  - no-three-in-line-75: `{"kind":"grid","n":75,"points":[[x,y]],"violated_lines":[[[x1,y1],[x2,y2],m]],"count":int,"sym":str,"round":int}`
  - spencer-discrepancy: `{"kind":"sign_matrix","n":int,"D":int,"matrix":[[1|-1]],"bad_vectors":int,"total_vectors":int}`
  - hadamard-det-51: `{"kind":"sign_matrix","n":51,"matrix":[[1|-1]],"log10_det":float}`
  - sidon-45-set: `{"kind":"integer_set","elements":[int],"h":int,"score":float}`
  - two-deletion-code-16: `{"kind":"code","words":[str],"count":int}`
- `GET /api/decisions?problem=<slug>&agent=<a>&limit=<n>&before=<id>` -> `[Decision]` newest first:
```
{ "id": int, "cycle": int, "time": str, "agent": "planner"|"proposer"|"critic"|"executor"|"literature"|"memory"|"sandbox"|"learning"|"system",
  "problem": str|null, "action": str, "params": {}, "rationale": str,
  "prediction": {"metric": str, "expected": float, "horizon_min": int}|null,
  "outcome": {"observed": float|null, "verdict": "confirmed"|"refuted"|"pending"|"n/a", "note": str}|null,
  "sources": [{"id": int, "title": str, "url": str, "published": str|null}],
  "memory_reads": [str], "memory_writes": [str], "model": str|null, "tokens": int|null, "latency_ms": int|null }
```
- `GET /api/events` (SSE): events `phase` `{phase, cycle}`, `decision` `<Decision>`, `telemetry` `<state.compute + per-problem metric>`,
  `record` `{slug, score, verified}`, `log` `{level, msg}`.
- `GET /api/memory` -> `{"facts": [{"id": str, "agent": str, "problem": str|null, "text": str, "time": str, "read_by": [str]}], "agents": [str],
  "links": [{"from_agent": str, "to_agent": str, "fact_id": str}], "benchmark": {"systems": [{"name": "past.dev"|"markdown"|"rag", "accuracy": float, "latency_ms": float, "cost_usd": float, "n": int}], "time": str}|null}`
- `GET /api/literature?problem=<slug>` -> `[{"id": int, "problem": str, "query": str, "title": str, "url": str, "published": str|null, "highlight": str, "cited_by": [int]}]`
- `GET /api/learning` -> `{"status": "idle"|"running"|"done"|"error", "base_model": str, "problem": str,
  "steps": [{"step": int, "reward_mean": float, "reward_best": float, "valid_rate": float, "time": str}],
  "eval": {"gen0": {"score": float, "valid_rate": float}, "genN": {"score": float, "valid_rate": float}, "heldout": str}|null,
  "best": {"solution": {}, "score": float}|null}`
- `GET /api/sandboxes?limit=` -> `[{"id": int, "problem": str, "time": str, "code": str, "status": "ok"|"invalid"|"timeout"|"error", "score": float|null, "seconds": float, "decision_id": int}]`
- `GET /api/gallery` -> `[{"title": str, "src": str (URL under /gallery/...), "kind": "image"|"video", "made_with": str, "caption": str}]`
- `POST /api/loop/pause`, `POST /api/loop/resume`, `POST /api/loop/run-now` -> `{"ok": true, "loop": <loop object>}`
- `POST /api/problems/{slug}/verify` -> `{"ok": bool, "score": float|null, "beats_record": bool, "error": str|null, "seconds": float}` (runs the official verifier on our current best solution for that problem)
- `POST /api/strategies` body `{"problem": str, "template": str, "params": {}}` -> `{"ok": bool, "id": str|null, "error": str|null}`
- `DELETE /api/strategies/{id}` -> `{"ok": bool, "error": str|null}`
- `POST /api/learning/start` body `{"steps": int}` -> `{"ok": bool}`; `POST /api/memory/benchmark` -> `{"ok": bool}`
- `POST /api/sandboxes/run` body `{"problem": str, "n": int}` -> `{"ok": bool}` (asks the proposer to write n programs and runs them on Modal)

## 5. Frontend (`ROOT/web/`): React 18 + Vite + TypeScript + Tailwind, react-router, recharts, framer-motion,
three / @react-three/fiber for 3D. Dev server :5173 proxies `/api` to :8787. `npm run build` -> `web/dist`.

Design: dark "mission control" for a research lab. Near-black background (#07080B), one accent (electric cyan
#3DF5FF) plus a warm accent for records (#FFB547), monospace numerals, generous spacing, subtle grid texture,
smooth motion (framer-motion), no clutter. Every number on screen comes from the API. Light mode not required.

Pages (all must work against the real API, and in STATIC mode, see 6):
1. **Mission Control** `/`: header with loop status pill + phase stepper (telemetry -> critic -> memory ->
   literature -> propose -> plan -> execute) animating live from SSE; controls Pause/Resume/Run cycle now.
   Compute map: 8 GPU tiles (util %, memory, owning problem, color by problem) + a 124-cell CPU heat grid
   (cells colored by owning problem, from `cpu_procs`). Problem portfolio cards: record vs ours, live metric
   sparkline, status, compute share; click -> detail. Live decision feed (SSE) on the right. Totals counters.
2. **Problem** `/problems/:slug`: description (markdown), leaderboard, metric history chart, the artifact
   visualization, running strategies table with Stop buttons, "Launch strategy" form generated from `templates`,
   "Verify now" button (shows official verifier result), decisions filtered to this problem.
   Visualizations: no-three: 75x75 canvas grid, points as glowing dots, violated lines drawn across the grid in
   red, symmetry axis shown, counts. sign matrices: heatmap canvas (+1 cyan / -1 dark), hover row/col.
   integer set: number line with points. code: bitstring wall.
3. **Decisions** `/decisions`: full audit log, filters (problem, agent), each card expandable: rationale,
   prediction vs outcome badge, sources (Exa links, open in new tab), memory reads/writes, model, tokens, latency.
4. **Memory** `/memory`: agent graph (nodes = agents, edges = "read a fact written by"), fact list with
   writer/readers, and the benchmark table/bar chart (past.dev vs markdown vs RAG: accuracy, latency, cost) with a
   "Run benchmark" button.
5. **Literature** `/literature`: Exa sources grouped by problem with highlights, publish dates, and which
   decisions cited them.
6. **Self-improvement** `/learning`: Tinker RL run: reward curve, valid-rate curve, gen-0 vs gen-N comparison,
   best construction found by the trained model, "Start training" button; plus Modal sandboxes table
   (`/api/sandboxes`) with code viewer and a "Run N sandboxes" button.
7. **Gallery** `/gallery`: renders from `viz/` (Blender, GPT image), images and videos.

## 6. Static replay (public demo link)

`python3 -m ltd.snapshot` writes `web/public/data/*.json` (state.json, problems/<slug>.json, decisions.json,
memory.json, literature.json, learning.json, sandboxes.json, gallery.json) from the live DB. Building the web
app with `VITE_STATIC=1` makes it read those files instead of `/api`, disables mutating buttons (shows "replay
of a live run, <timestamp>"), and uses `HashRouter` so it works on GitHub Pages under `/phoenixastar/`
(`base: '/phoenixastar/'` when static).

## 7. Visuals (`ROOT/viz/`)

Blender 4.x at `/Applications/Blender.app/Contents/MacOS/Blender` (headless: `-b -P script.py`). GPT-6 Astra
(`gpt-6-astra`, Responses API) writes/edits the bpy scripts; gpt-image-2 (`client.images.generate`) makes the hero
art. Data comes from real artifacts (`ROOT/data/` or files pulled from the box). Outputs: `viz/renders/*.png|mp4`,
copied to `web/public/gallery/` with `web/public/gallery/gallery.json` (same shape as `/api/gallery`).
