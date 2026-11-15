"""Writes script.md (narration + shot list + captions) from sections.json."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); J = json.load(open(f"{H}/sections.json")); S = J["sections"]; N = J["numbers"]
w = sum(len(x["text"].split()) for x in S)
o = ["# Phoenixastar: 2-minute demo video script", "",
 f"Iterate AI Research Hackathon, Track 1. Narration: {w} spoken words, OpenAI `gpt-4o-mini-tts` (voice onyx), time-compressed x{J['tempo']:.2f} to fit {J['total']:.0f} s.",
 f"All numbers were read from the live app (`/api/state`, `/api/memory`, `/api/learning`, `/api/decisions`) at {J['read_at']} and are phrased as floors (\"over N\") where the live counter keeps moving.", "",
 "Honesty rules: no math record is claimed; the three-body result is described only as candidate orbits not found in the catalogs we checked; Devin: no strategy adopted yet; the past.dev benchmark is reported as measured (markdown is more accurate).", "",
 "| # | Time | Shot (screen) | Narration | Lower-third caption |", "|---|---|---|---|---|"]
for i, x in enumerate(S, 1):
    a = x["start"]; b = a + x["vdur"]
    o.append(f"| {i} | {int(a//60)}:{a%60:04.1f}-{int(b//60)}:{b%60:04.1f} | {x['shot']} | {x['text']} | {x['caption'].replace('|', '/')} |")
o += ["", "## Numbers read at narration time", "", "```json", json.dumps(N, indent=1), "```", "", "## Pipeline (one command: `./make_video.sh`)", "",
 "1. `narrate.py` reads live numbers, writes `sections.json`, synthesises one audio file per section (`audio/`).",
 "2. `prep_audio.py` trims silence, time-compresses, loudness-normalises, and fixes each section's video length.",
 "3. `record.py` records each shot from the live app at 1920x1080 through a headless Chromium CDP screencast (read-only navigation; the only click expands a decision card).",
 "4. `assemble.py` builds each section (clip or `lattice_orbit.mp4` B-roll + narration + lower third), concatenates, writes `phoenixastar_demo.mp4` and `poster.png`.", ""]
open(f"{H}/script.md", "w").write("\n".join(o)); print("wrote script.md,", w, "words")
