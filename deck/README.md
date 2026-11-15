# Pitch deck and storyboard

| File | What it is |
|---|---|
| `Phoenixastar.pptx` | 10 slides, 16:9, dark mission-control design, speaker notes on every slide |
| `storyboard.md` | Presenter script: 3-minute finals (pitch + live demo), 5-minute Round 1 (pitch + Q&A answers), 10-minute walkthrough |
| `build_deck.py` | Builds and validates the deck, then writes `storyboard.md` |
| `deckdata.py` | Reads the snapshot and derives every number shown |
| `storyboard_gen.py` | Wording of the storyboard (edit here, not in `storyboard.md`) |

## Rebuild

```
python3 -m phoenixastar.snapshot              # refresh web/public/data/*.json (from the repo root)
python3 deck/build_deck.py           # build + validate, about 10 s
python3 deck/build_deck.py --preview # also render deck/build/preview/slide-NN.png
```

Needs `python-pptx`, `matplotlib`, `Pillow`, `lxml`. `ffmpeg` is optional (video poster frames); `--preview` needs
LibreOffice (`soffice`) and `pdftoppm`.

No result is hard-coded. Every number is read at build time from `web/public/data/` (`state.json`,
`decisions.json`, `memory.json`, `learning.json`, `sandboxes.json`, `literature.json`, `problems/*.json`) and
`web/public/gallery/`. Every slide shows "as of <snapshot time>" in the top right corner. `storyboard.md` is
regenerated with the same numbers, so rebuild after the last snapshot and re-read the script once.

Team line on the last slide: put it in `deck/team.txt` (one line) or pass `--team "A · B · C"`. Without it the
slide says "Team Phoenixastar".

## Slides

1. **Title.** Full-bleed `lattice_orbit.mp4` (autoplay, muted, loop), tagline, caption from `gallery.json`.
2. **The problem.** Search loops nobody can audit; static loops do not learn. Hadamard City render.
3. **What we built.** The eight-step loop as a ring (telemetry, critic, memory, literature, propose, referee,
   plan, execute) plus compute, self-improvement and audit panels. Interval from `state.loop.interval_s`.
4. **Live.** 8 GPU tiles and the CPU core grid coloured by owning problem (`state.compute`), six counters from
   `state.totals`, Modal panel (fleet size if the snapshot has it, sandboxes otherwise).
5. **The loop decides.** One real proposer decision chosen from `decisions.json` (prefers one with Exa sources, a
   referee verdict and a prediction), with a prediction and its critic score, the Exa source and the referee verdict.
6. **Results.** Record vs ours (verified) vs live search signal for every problem in `state.problems`, plus the
   current no-three-in-line model drawn from `problems/no-three-in-line-75.json`. If any problem has
   `beats_record: true` the title and the row turn into the record announcement; otherwise it states the distance.
7. **It improves itself.** Tinker reward and valid-rate curve (matplotlib, from `learning.json`), gen 0 vs gen N.
8. **Memory and tools.** past.dev facts and cross-agent reads, benchmark vs markdown and RAG as measured
   (`memory.json`), Modal sandboxes (`sandboxes.json`), Devin toolsmith (numbers only if the snapshot has them).
9. **Rigour.** Verifier runs, predictions made and scored, proposals blocked, decisions logged, and what failed.
10. **Close.** Any domain with an exact verifier; next: three-body periodic orbits. Repo link, team,
    `snake_turntable.mp4`.

## Motion

- **Morph** transition on every slide (`p159:morph` inside `mc:AlternateContent`, fade fallback). The backdrop,
  wordmark, snapshot stamp and progress bar are named `!!...` so they morph between slides.
- **Entrance animations** (fade, zoom, wipe), staggered, starting by themselves when a slide appears.
- **Number build-ups**: stacked opaque frames revealed in sequence; the last frame is the real value, so PDF
  exports and thumbnails show only the real value.
- **Videos** are embedded with a first-frame poster and set to autoplay, muted, looping.

Morph, autoplay and looping need PowerPoint 2019 / Microsoft 365. Keynote, Google Slides and LibreOffice open the
file but show a fade and may need a click to play the videos.

## Fields the deck looks for but does not require

Referee verdicts (`agent: "referee"` decisions or a `referee` object on a decision), a Modal fleet
(`compute.modal*` / `compute.fleet*`, strategies with `where: "modal"`), toolsmith events (`agent: "toolsmith"` or
`"devin"`). If the snapshot lacks them the slide says so instead of showing a number, and `storyboard.md` lists
what not to claim under "Things not to say".
