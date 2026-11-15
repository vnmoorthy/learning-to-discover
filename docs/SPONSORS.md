# Sponsors and credits

[Back to the README](../README.md) · [Architecture](ARCHITECTURE.md) · [Results](RESULTS.md) · [Reproduce](REPRODUCE.md)

Built at the Iterate AI Research Hackathon, San Francisco, Track 1: "Build your own autoresearch framework: can
your system beat a best-known result in mathematics on its own?" Sponsor challenges entered: Exa, past.dev,
Modal and Originator.

For each tool: what it does in this lab, where the code is, and what we can show for it. Numbers are in
[RESULTS.md](RESULTS.md), generated from the run's data.

| | Role | Code |
|---|---|---|
| [OpenAI](#openai) | Proposer, program writer, technical artist, image model | `ltd/proposer.py`, `ltd/sandboxes.py`, `viz/astra.py` |
| [Tinker](#tinker) | RL self-improvement | `ltd/learning.py` |
| [Exa](#exa) | Literature search in the loop | `ltd/literature.py` |
| [past.dev](#pastdev) | Shared multi-agent memory | `ltd/memory.py`, `ltd/memory_bench.py` |
| [Modal](#modal) | Agent sandboxes and CPU fleet | `ltd/sandboxes.py`, `ltd/modal_fleet.py` |
| [Devin](#devin) | Toolsmith | `ltd/toolsmith.py` |
| [Claude Fable 5.2](#claude-fable-52) | Referee | `ltd/referee.py` |
| [Originator](#originator) | Sponsor challenge | |
| [Lambda](#lambda) | GPU box | `ltd/box.py`, `scripts/` |

## OpenAI

- **GPT-6 Astra as the proposer.** One Responses API call per cycle with strict JSON-schema output. It sees the
  compact lab state (telemetry, gaps to record, strategy history with outcomes, recalled memory, literature
  cards, free GPUs and cores) and returns actions with a rationale and a falsifiable prediction. Fallback model:
  `gpt-5.5`. The proposer has no shell and no way to exceed the planner's budget.
- **Program writer.** For cheap problems it writes self-contained search programs that run in Modal sandboxes.
- **Fast model.** `gpt-5.4-mini` writes Exa queries and answers and grades the memory benchmark;
  `text-embedding-3-small` powers the RAG baseline.
- **Technical artist.** `viz/astra.py` asks GPT-6 Astra to write and repair the Blender `bpy` scripts behind the
  gallery. Each round's prompt, script and reply is saved as `viz/scripts/<name>.vN.*`.
- **gpt-image-2** painted the banner backdrop. It is labelled as illustration; the lattice on the banner is a
  render of real search data.

## Tinker

GRPO-style RL on a LoRA of `Qwen/Qwen3-8B`: sample completions with the Tinker sampling client, score each with
the official `sidon-45-set` verifier, take advantage = reward minus the mean of its prompt group, apply an
importance-sampling policy-gradient step (`forward_backward` + `optim_step`), save weights, refresh the sampler.
The evaluation compares the base sampler with the trained one at the same sample budget, on training prompts and
on held-out prompts. Curves and the comparison are in [RESULTS.md](RESULTS.md#self-improvement-tinker). The
trained model has not produced a record construction.

## Exa

Exa is a phase of the main loop, not a side tool. When a problem is stalled (or has no sources yet), a fast model
writes queries from the problem's current situation, `ltd/literature.py` calls `https://api.exa.ai/search` with
highlights, and the results become literature cards stored in the ledger. Cards are passed to the proposer;
a decision that cites one links to it, and the Literature page shows which decisions cited which source.
Searches are cached by query and limited to one round per problem per hour.

## past.dev

All agents (planner, proposer, critic, literature and one agent per problem) write to and recall from a single
shared past.dev identity, so each reads what the others learned; the writer travels in the metadata and every
read is recorded. The critic writes a lesson whenever it scores a prediction.

The lab also benchmarks past.dev against two baselines on its own facts: a markdown file kept whole in context,
and a small RAG. We publish the result as measured. In the run reported in
[RESULTS.md](RESULTS.md#memory-benchmark-pastdev-vs-markdown-vs-rag) the markdown baseline had the highest
accuracy and past.dev used the fewest context tokens per question; the memory was small enough to fit in
context, which favours the baseline.

## Modal

- **Agent sandboxes** (`ltd/sandboxes.py`). N model-written programs run in parallel `modal.Sandbox`es built from
  a slim image with numpy and numba: networking blocked, no secrets, killed after 110 s. The last stdout line is
  parsed as a solution and verified locally with the official verifier. Every program and its score is a
  decision in the ledger.
- **CPU fleet** (`ltd/modal_fleet.py`). The app `ltd-fleet` runs each search strategy as a 1-core container that
  logs to the shared Volume `ltd-runs`; a `telemetry` function parses the logs with the same parser as the GPU
  box. GPU strategies stay on the Lambda box.
- **Toolsmith smoke tests** run in a sandbox as well.

## Devin

`ltd/toolsmith.py` opens a Devin session with a precise spec: the problem statement, the official verifier's
source, the record, the CLI and log conventions every strategy follows, and a structured-output schema. When
Devin returns code, it is saved under `search/devin/`, run in a Modal sandbox on a short budget, and its printed
solution is scored by the official verifier. Only a strategy that produces a valid solution is appended to
`search/TEMPLATES.json`. Session state is in `data/toolsmith.json`; see
[RESULTS.md](RESULTS.md#detail) for the current sessions.

## Claude Fable 5.2

`ltd/referee.py` sends the proposer's actions and a compact view of the live evidence to Claude Fable 5.2
through the local Claude Code CLI, run in an empty temporary directory so no project files leak in. It answers
`approve`, `veto` or `amend` for each action, with a reason that cites the evidence. Two models from different
labs then have to agree before compute moves. Any failure is an abstention, so the loop never waits on it.
See [integration status](ARCHITECTURE.md#integration-status).

## Originator

Learning to Discover is entered in the Originator sponsor challenge. There is no Originator-specific code in
this repository.

## Lambda

The searches run on a Lambda machine with 8 A100 40 GB GPUs and 124 CPU cores, reached only over SSH.

## Open source and data

| | Used for |
|---|---|
| **EinsteinArena** | The problems, the live leaderboards and the official verifiers (`problems/`, `arena/`) |
| **pysat** with **CaDiCaL**, Glucose, MapleChrono | SAT search for no-three-in-line and the exact sub-solver in `twodel_lns.py` |
| **PyTorch** | Batched GPU tabu and min-conflicts searches |
| **numba**, **numpy**, **sympy** | Exact energies and DFS in the CPU searches; exact determinant re-checks (Bareiss) |
| **Blender** | Every 3D render in the gallery |
| **FastAPI**, sse-starlette, SQLite | Server, event stream, ledger |
| **React**, Vite, Tailwind, recharts, framer-motion, three.js | Mission control |

Record holders whose public constructions the lab starts from or displays: Thomas-Prellberg, Youhua-Li, kgrey,
Ma-Tang and JSAgent-Ring15 (names as listed on the EinsteinArena leaderboard).
