# Learning to Discover: 2-minute demo video script

Iterate AI Research Hackathon, Track 1. Narration: 310 spoken words, OpenAI `gpt-4o-mini-tts` (voice onyx), time-compressed x1.17 to fit 122 s.
All numbers were read from the live app (`/api/state`, `/api/memory`, `/api/learning`, `/api/decisions`) at 2026-11-15T18:48:51Z and are phrased as floors ("over N") where the live counter keeps moving.

Honesty rules used: no math record is claimed (the app shows none on the EinsteinArena problems); the three-body result is described only as candidate orbits not found in the catalogs we checked; Devin: no strategy adopted yet; past.dev benchmark reported as measured (markdown is more accurate).

| # | Time | Shot (screen) | Narration | Lower-third caption |
|---|---|---|---|---|
| 1 | 0:00.0-0:07.0 | B-roll: web/public/gallery/lattice_orbit.mp4 (Blender render of the live no-three-in-line SAT snapshot), title card overlay. | This is Phoenixastar: an autonomous AI lab that hunts for records on open math problems, and improves by doing it. | Phoenixastar  /  an autonomous AI lab for open math problems |
| 2 | 0:07.0-0:26.1 | Mission Control /: hero and totals counters, then slow scroll so the Autonomous Loop phase stepper is centred; cursor sweeps the eight phases left to right. | This is the live lab. Every 3 minutes, with no human in the loop, it reads telemetry, re-verifies every claim, recalls memory, searches papers with Exa, proposes experiments with GPT-6 Astra, has Claude Fable referee them, then executes. Over 35 cycles and 900 logged decisions so far. | One loop every 3 min  /  35+ cycles, 900+ logged decisions, all auditable |
| 3 | 0:26.1-0:37.3 | Mission Control /: scroll to the Compute Map; hover GPU tiles, then the CPU core grid, then the Modal fleet row. | It runs on 8 A100 GPUs and 124 CPU cores, coloured by the problem that owns them, plus an elastic Modal fleet: 140 containers right now. | 8 x A100  /  124 CPU cores  /  Modal fleet 140/140 containers |
| 4 | 0:37.3-0:53.0 | /problems/no-three-in-line-75: header (record vs ours), then the 75x75 construction canvas with red violated lines; hover two points to isolate their lines. | The flagship problem: no three in line, on a 75 by 75 grid. The record is 148 points. Our best candidate places 150, but over 100 lines, in red, still cross three or more. Zero would be a new record. We are not there yet. | No-three-in-line 75x75  /  record 148  /  ours: 150 points, 100+ violated lines (not valid yet) |
| 5 | 0:53.0-1:12.1 | /decisions filtered to proposer, decision #211 expanded (rationale, queries, 3 Exa sources); cut to referee filter, #219 expanded (Claude Fable approve); cut to #191 expanded (prediction vs outcome, REFUTED). | Every action is a card in the audit log. Here GPT-6 Astra asks for research, citing three Exa sources. Claude Fable reviews and approves it, with its own reasoning. Launches carry a falsifiable prediction: this one expected 16 collinear triples in 30 minutes. The critic observed 17, and marked it refuted. | Decision #211: GPT-6 Astra proposes, 3 Exa sources  /  #219: Claude Fable 5.2 approves  /  #191: prediction refuted |
| 6 | 1:12.1-1:24.4 | /memory: agent graph (hover the proposer node), then scroll to the Memory Benchmark bars and table. | Agents share memory through past.dev: over 390 facts. Benchmarked honestly, it scores 74 percent, against 100 for plain markdown and 97 for RAG. | past.dev shared memory: 390+ facts  /  benchmark on 31 questions: past.dev 74%, markdown 100%, RAG 97% |
| 7 | 1:24.4-1:41.2 | /learning: Tinker RL reward curve and valid-construction curve, gen-0 vs gen-N panel, then scroll to the Modal sandboxes table. | The lab also trains itself. Tinker fine-tunes an open Qwen model with the verifier as reward: valid constructions on held-out prompts went from 0 to 50 percent in 40 steps. Devin writes new search programs, tested in Modal sandboxes; so far none has passed. | Tinker RL, reward = official verifier  /  held-out valid rate 0% -> 50% in 40 steps  /  28 Modal sandbox runs |
| 8 | 1:41.2-1:52.3 | /gallery: Blender renders (Lattice, Hadamard City, Snake), then scroll to the three-body orbit plots (figure-eight, moth II, candidates, 7 families). | The same loop now runs astrophysics: periodic three-body orbits. Our GPU search rediscovered the figure-eight and other known families, and reports candidate orbits not found in the catalogs we checked. | Three-body domain: known families rediscovered  /  candidate orbits not found in the catalogs we checked |
| 9 | 1:52.3-2:02.0 | B-roll: lattice_orbit.mp4 again, closing card with the replay URL. | No math record is beaten yet, and the three-body orbits are candidates, not discoveries. Every decision, source and prediction is logged and replayable. Phoenixastar. | No math record beaten yet; three-body orbits are candidates  /  replay: vnmoorthy.github.io/phoenixastar |

## Numbers read at narration time

```json
{
 "cycles": 39,
 "decisions": 914,
 "dec_floor": 900,
 "gpus": 8,
 "cpus": 124,
 "fleet": 140,
 "fleet_max": 140,
 "viol": 109,
 "rec": 148,
 "facts": 397,
 "facts_floor": 390,
 "past": 74,
 "md": 100,
 "rag": 97,
 "nq": 31,
 "v0": 0,
 "vN": 50,
 "steps": 40,
 "sandboxes": 28,
 "comm": 18,
 "rej": 25,
 "adopted": 0,
 "ref_ok": 35,
 "interval": 3,
 "problems": 12
}
```

## Pipeline

1. `narrate.py` reads live numbers, writes `sections.json`, synthesises one audio file per section (`audio/`).
2. `prep_audio.py` trims silence, time-compresses, loudness-normalises, and fixes each section's video length.
3. `record.py` records each shot from the live app at 1920x1080 through a headless Chromium CDP screencast (read-only navigation; the only click is expanding a decision card).
4. `assemble.py` builds each section (clip or `lattice_orbit.mp4` B-roll + narration + PIL-rendered lower third), concatenates, and writes `learning_to_discover_demo.mp4` and `poster.png`.
