#!/usr/bin/env bash
# Rebuild every visual from real data with the current Astra-written scripts (no LLM calls unless --astra).
#   bash viz/build_all.sh            # re-render + publish (about 8-10 min on an M-series Mac)
#   bash viz/build_all.sh --pull     # also pull the newest no-three SAT snapshot from the GPU box (read-only)
# Iterating a script with GPT-6 Astra:  python3 viz/astra.py fix <lattice|hadamard_city|snake> --feedback "..." --image <png>
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if [[ "${1:-}" == "--pull" ]]; then
  # One read-only ssh call; validated locally; keeps the old snapshot (with a WARNING) if the box is unreachable.
  python3 viz/pull_snapshot.py
fi
python3 viz/prep_data.py
python3 viz/render.py lattice -- --data viz/data/lattice.json --out viz/renders/hero.png --mode still --res 1920x1080 --samples 64
python3 viz/render.py lattice -- --data viz/data/lattice.json --out viz/renders/wip/lattice_banner.png --mode still --res 1280x640 --samples 32
python3 viz/render.py hadamard_city -- --data viz/data/hadamard.json --out viz/renders/hadamard_city.png --res 1920x1080 --samples 64
python3 viz/render.py snake -- --data viz/data/snake.json --out viz/renders/snake.png --res 1920x1080 --samples 64
python3 viz/render.py lattice --timeout 1500 -- --data viz/data/lattice.json --out viz/renders/lattice_orbit.mp4 --mode loop --res 1280x720 --samples 8 --frames 192 --fps 24
python3 viz/render.py snake --timeout 1500 -- --data viz/data/snake.json --out viz/renders/snake_turntable.mp4 --mode turntable --res 1280x720 --samples 8 --frames 192 --fps 24
python3 viz/og_banner.py --plate viz/renders/wip/lattice_banner.png
python3 viz/publish.py
