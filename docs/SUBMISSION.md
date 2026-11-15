# Submission: Phoenixastar

Ready-to-paste text for the Iterate submission form. Numbers are from the live run on Nov 15 2026 (about 11:00 PT,
loop cycle 38); the replay at https://vnmoorthy.github.io/phoenixastar/ shows the snapshot they come from.

- **Project:** Phoenixastar
- **Track:** Track 1: Build your own autoresearch framework
- **Challenges entered:** Exa (research agents that search), past.dev (multi-agent memory), Best use of Modal, Originator
- **Repo:** https://github.com/vnmoorthy/phoenixastar
- **Live replay (public):** https://vnmoorthy.github.io/phoenixastar/

## Short description (about 150 words)

Phoenixastar is an autonomous AI research lab that attacks open mathematics problems on its own and proves every
result with the official verifier. Every three minutes a loop reads live telemetry from an 8xA100 box and an elastic
Modal fleet, re-verifies every claimed result, shares what each problem's agent learned through past.dev, searches the
literature with Exa, and lets GPT-6 Astra propose the next experiments, each with a falsifiable prediction. Claude Fable
5.2 referees every proposal before compute moves; a deterministic planner enforces budgets and kills provably dead
searches; Devin writes new search programs that are adopted only after passing the verifier in a Modal sandbox; Tinker
trains an open model on its own verified attempts. In one morning it made 900 logged decisions over 38 cycles and ran
598 experiments. No EinsteinArena record has fallen yet (distances are reported), and in a celestial-mechanics domain it
found 17 verified periodic three-body orbits in 16 families absent from the 2,060 catalogued orbits we checked, two of them at equal masses.

## Long description (about 400 words)

**Question.** Can an AI system run the research loop by itself (choose what to try, run it, read the result, decide what
to try next) on problems where the answer is checkable, and can every decision be followed?

**What we built.** A lab, not a script. Eight phases per cycle: telemetry -> critic -> memory -> literature -> propose ->
referee -> plan -> execute. The critic re-runs the official EinsteinArena verifier on every claimed solution and scores
the proposer's past predictions against what actually happened. Problem agents write observations to a shared past.dev
space and read each other's before proposing. Exa supplies papers when a problem stalls, and decisions cite them. GPT-6
Astra proposes; Claude Fable 5.2, a second lab's model, approves, vetoes or amends each proposal with the evidence it
cites. The planner turns approved proposals into validated launches and stops on an 8xA100 Lambda box (GPU and CPU
searches: SAT/CEGAR, GPU min-conflicts, tabu, exact LNS, prox-linear polishing) and on a Modal fleet it scales itself
(140 containers at peak). The lab extends itself: it commissions new search programs from Devin, smoke-tests them in Modal
sandboxes against the verifier, and adopts only what passes.

**Results.** Ten problems attacked; no EinsteinArena record beaten by 11:00. Closest: two-deletion code (best valid code 226 = the record; a
weighted search reached 227 words with one conflicting pair), first autocorrelation (3.2e-10 below the record; a record needs 1e-8),
no-three-in-line 75x75 (best SAT model 107 violated lines). Proved negatives are logged too (no one-point extension of the
Sidon record; UNSAT neighbourhoods; dead symmetry classes). In the astrophysics domain, 17 verified periodic orbits in 16 topological families (float64 DOP853,
return error < 1e-8; two at equal masses) that do not appear in the 2,060-orbit catalog we checked: candidates, not proven new. EVENT HORIZON reproduces the Page curve, Page's theorem and Hayden-Preskill decoupling on the A100s (classified as
reproductions; independent-verification status in `domains/event-horizon`).

**Self-improvement and rigour.** 49 decisions carried falsifiable predictions (9 confirmed, 11 refuted, the rest not
scorable or pending); Tinker RL took an open model from 0% to 100% valid constructions on its training prompts. Every
decision, source, memory read/write, verdict and verification is in the replayable log.

## Sponsor challenges

### Exa: research agents that search
- **Where Exa runs in the main loop:** `phoenixastar/literature.py` (`search()`, Exa `/search` with contents and highlights,
  cached by query), called from the loop's literature phase (`phoenixastar/loop.py`, `_literature`) for every stalled or new problem
  and from proposer-requested research actions (`phoenixastar/planner.py`, `execute`, kind `research`).
- **How results are used:** cards (title, URL, published date, highlight) go into the proposer's state; decisions cite
  card ids (`cite`), which the ledger links back (`cited_by`). The Literature page shows every source and which decisions
  cited it. So far: 188 sources across the problems.
- **Checkable output:** every cited source has its URL and date in the decision log.

### past.dev: multi-agent memory
- **More than one agent writes:** one agent per problem (`agent:<slug>`), plus `proposer` and `planner`
  (`phoenixastar/memory.py` `write`, called from `phoenixastar/loop.py` and `phoenixastar/planner.py`).
- **More than one agent reads, and reads others' data:** each problem agent recalls from the shared space (identity
  `phoenixastar-lab`) before every proposal (`phoenixastar/loop.py`, `_memory` -> `memory.recall`); the proposer uses facts written by
  other agents and lists their ids in `memory_used`, recorded as `read_by`. Live: 387 facts, 13 agents, 509 cross-agent
  read links (Memory page graph).
- **Which memory holds what:** past.dev holds the shared, cross-agent observations and plans; `data/memory.md` is an
  append-only markdown log of the same facts; the RAG baseline embeds the same facts with OpenAI embeddings.
- **Benchmark (`phoenixastar/memory_bench.py`, `data/snapshot/memory_benchmark.json`):** on a small set of lab facts, past.dev
  scored 74% accuracy against markdown 100% and RAG 97%, using the fewest context tokens. Why it lost: the whole memory
  is small enough to fit in one prompt, which favours the markdown baseline, and past.dev's recall was weakest on
  cross-agent questions. We report it as measured.

### Best use of Modal
- **Planner-controlled fleet:** `phoenixastar/fleet.py` + `phoenixastar/modal_fleet.py`. The proposer chooses `where: "modal"`, the planner
  launches and cancels containers (up to 140), the monitor merges the fleet's logs into telemetry, and the critic verifies
  FOUND files read from the fleet Volume.
- **Agent sandboxes:** `phoenixastar/sandboxes.py`, where GPT writes search programs that run in parallel in network-blocked Modal
  sandboxes with no secrets, then get verified locally (28 so far).
- **Toolsmith bench:** Devin's code is smoke-tested in a Modal sandbox (`phoenixastar/toolsmith.py`, `run_in_modal`).

### Originator
Agent sessions from the build are uploaded with the submission.

## Demo video
2-minute demo: `video/phoenixastar_demo.mp4` in the repo (also attached to the GitHub release).
