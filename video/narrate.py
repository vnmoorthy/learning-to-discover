"""Reads live numbers from the app, writes sections.json + script.md, and TTS audio per section."""
import json, sys, urllib.request, subprocess, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "http://127.0.0.1:8787"
def get(p): return json.load(urllib.request.urlopen(BASE + p, timeout=20))
s = get("/api/state"); mem = get("/api/memory"); learn = get("/api/learning"); dec = get("/api/decisions?limit=1000")
t = s["totals"]; c = s["compute"]; modal = c.get("modal") or {}
n3 = next(p for p in s["problems"] if p["slug"] == "no-three-in-line-75")
assert not any(p["beats_record"] for p in s["problems"] if p["slug"] != "three-body-periodic-orbits"), "a math record fell: rewrite the script!"
viol = int(n3["metric"]["value"]); rec = int(n3["record"]["score"])
bench = {x["name"]: x for x in mem["benchmark"]["systems"]}
pct = lambda v: round(v * 100)
ev = learn["eval"]; nsteps = len(learn["steps"]) if isinstance(learn["steps"], list) else learn["steps"]
acts = collections.Counter((d["agent"], d["action"]) for d in dec)
comm, rej = acts[("toolsmith", "commission")], acts[("toolsmith", "rejected")]
adopted = sum(v for (a, k), v in acts.items() if a == "toolsmith" and k not in ("commission", "rejected"))
ref_ok = acts[("referee", "approve")]
floor = lambda n, k: n // k * k
N = dict(cycles=t["cycles"], decisions=t["decisions"], dec_floor=floor(t["decisions"], 50), gpus=len(c["gpus"]), cpus=c["cpus"],
         fleet=modal.get("containers"), fleet_max=modal.get("max"), viol=viol, rec=rec, facts=len(mem["facts"]), facts_floor=floor(len(mem["facts"]), 10),
         past=pct(bench["past.dev"]["accuracy"]), md=pct(bench["markdown"]["accuracy"]), rag=pct(bench["rag"]["accuracy"]), nq=bench["past.dev"]["n"],
         v0=pct(ev["gen0"]["valid_rate"]), vN=pct(ev["genN"]["valid_rate"]), steps=nsteps, sandboxes=t["sandboxes_run"],
         comm=comm, rej=rej, adopted=adopted, ref_ok=ref_ok, interval=s["loop"]["interval_s"] // 60, problems=len(s["problems"]))
print(N)
devin = ("Devin writes new search programs, tested in Modal sandboxes; so far none has passed."
         if adopted == 0 else f"Devin writes new search programs, tested in Modal sandboxes: {adopted} adopted so far.")
S = [
 dict(id="s1_intro", shot="B-roll: web/public/gallery/lattice_orbit.mp4 (Blender render of the live no-three-in-line SAT snapshot), title card overlay.",
      caption="Phoenixastar  |  an autonomous AI lab for open math problems",
      text="This is Phoenixastar: an autonomous AI lab that hunts for records on open math problems, and improves by doing it."),
 dict(id="s2_loop", shot="Mission Control /: hero and totals counters, then slow scroll so the Autonomous Loop phase stepper is centred; cursor sweeps the eight phases left to right.",
      caption=f"One loop every {N['interval']} min  |  {floor(N['cycles'],5)}+ cycles, {N['dec_floor']}+ logged decisions, all auditable",
      text=f"This is the live lab. Every {N['interval']} minutes, with no human in the loop, it reads telemetry, re-verifies every claim, recalls memory, searches papers with Exa, proposes experiments with GPT-6 Astra, has Claude Fable referee them, then executes. Over {floor(N['cycles'],5)} cycles and {N['dec_floor']} logged decisions so far."),
 dict(id="s3_compute", shot="Mission Control /: scroll to the Compute Map; hover GPU tiles, then the CPU core grid, then the Modal fleet row.",
      caption=f"{N['gpus']} x A100  |  {N['cpus']} CPU cores  |  Modal fleet {N['fleet']}/{N['fleet_max']} containers",
      text=f"It runs on {N['gpus']} A100 GPUs and {N['cpus']} CPU cores, coloured by the problem that owns them, plus an elastic Modal fleet: {N['fleet']} containers right now."),
 dict(id="s4_problem", shot="/problems/no-three-in-line-75: header (record vs ours), then the 75x75 construction canvas with red violated lines; hover two points to isolate their lines.",
      caption=f"No-three-in-line 75x75  |  record {N['rec']}  |  ours: 150 points, {floor(N['viol'],100)}+ violated lines (not valid yet)",
      text=f"The flagship problem: no three in line, on a 75 by 75 grid. The record is {N['rec']} points. Our best candidate places 150, but over {floor(N['viol'],100)} lines, in red, still cross three or more. Zero would be a new record. We are not there yet."),
 dict(id="s5_decisions", shot="/decisions filtered to proposer, decision #211 expanded (rationale, queries, 3 Exa sources); cut to referee filter, #219 expanded (Claude Fable approve); cut to #191 expanded (prediction vs outcome, REFUTED).",
      caption="Decision #211: GPT-6 Astra proposes, 3 Exa sources  |  #219: Claude Fable 5.2 approves  |  #191: prediction refuted",
      text="Every action is a card in the audit log. Here GPT-6 Astra asks for research, citing three Exa sources. Claude Fable reviews and approves it, with its own reasoning. Launches carry a falsifiable prediction: this one expected 16 collinear triples in 30 minutes. The critic observed 17, and marked it refuted."),
 dict(id="s6_memory", shot="/memory: agent graph (hover the proposer node), then scroll to the Memory Benchmark bars and table.",
      caption=f"past.dev shared memory: {N['facts_floor']}+ facts  |  benchmark on {N['nq']} questions: past.dev {N['past']}%, markdown {N['md']}%, RAG {N['rag']}%",
      text=f"Agents share memory through past.dev: over {N['facts_floor']} facts. Benchmarked honestly, it scores {N['past']} percent, against {N['md']} for plain markdown and {N['rag']} for RAG."),
 dict(id="s7_learning", shot="/learning: Tinker RL reward curve and valid-construction curve, gen-0 vs gen-N panel, then scroll to the Modal sandboxes table.",
      caption=f"Tinker RL, reward = official verifier  |  held-out valid rate {N['v0']}% -> {N['vN']}% in {N['steps']} steps  |  {N['sandboxes']} Modal sandbox runs",
      text=f"The lab also trains itself. Tinker fine-tunes an open Qwen model with the verifier as reward: valid constructions on held-out prompts went from {N['v0']} to {N['vN']} percent in {N['steps']} steps. " + devin),
 dict(id="s8_gallery", shot="/gallery: Blender renders (Lattice, Hadamard City, Snake), then scroll to the three-body orbit plots (figure-eight, moth II, candidates, 7 families).",
      caption="Three-body domain: known families rediscovered  |  candidate orbits not found in the catalogs we checked",
      text="The same loop now runs astrophysics: periodic three-body orbits. Our GPU search rediscovered the figure-eight and other known families, and reports candidate orbits not found in the catalogs we checked."),
 dict(id="s9_close", shot="B-roll: lattice_orbit.mp4 again, closing card with the replay URL.",
      caption="No math record beaten yet; three-body orbits are candidates  |  replay: vnmoorthy.github.io/phoenixastar",
      text="No math record is beaten yet, and the three-body orbits are candidates, not discoveries. Every decision, source and prediction is logged and replayable. Phoenixastar."),
]
words = sum(len(x["text"].split()) for x in S); print("words", words)
json.dump(dict(numbers=N, read_at=s["now"], sections=S), open(f"{HERE}/sections.json", "w"), indent=1)
if "--no-tts" in sys.argv: sys.exit()
sys.path.insert(0, '/Users/moorthy/Downloads/Projects/iterate/phoenixastar'); import envload; envload.load()
def tts(model, text, out, instr=None):
    body = dict(model=model, voice="onyx", input=text, response_format="mp3")
    if instr: body["instructions"] = instr
    rq = urllib.request.Request("https://api.openai.com/v1/audio/speech", data=json.dumps(body).encode(),
        headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"], "Content-Type": "application/json"})
    open(out, "wb").write(urllib.request.urlopen(rq, timeout=120).read())
ONLY=[a for a in sys.argv[1:] if not a.startswith('-')]
for x in S:
    out = f"{HERE}/audio/{x['id']}.mp3"
    if ONLY and x["id"] not in ONLY: m = "gpt-4o-mini-tts"
    else:
      try:
        tts("gpt-4o-mini-tts", x["text"], out, "Calm, confident technical presenter. Clear and brisk pace, no long pauses. No theatrics."); m = "gpt-4o-mini-tts"
      except Exception as e:
        print("fallback tts-1-hd:", type(e).__name__, str(e)[:200]); tts("tts-1-hd", x["text"], out); m = "tts-1-hd"
    wav = out.replace(".mp3", ".wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", out, "-ar", "48000", "-ac", "2", wav], check=True)
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav]))
    x["dur"] = d; x["tts_model"] = m; print(x["id"], m, round(d, 2))
print("total narration", sum(x["dur"] for x in S))
json.dump(dict(numbers=N, read_at=s["now"], sections=S), open(f"{HERE}/sections.json", "w"), indent=1)
