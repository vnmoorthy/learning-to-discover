"""Trim silence from each narration file and time-compress slightly so the total fits 2:00."""
import json, subprocess, os
HERE = os.path.dirname(os.path.abspath(__file__)); TARGET = 116.0; PAD_IN, PAD_OUT = 0.25, 0.30
J = json.load(open(f"{HERE}/sections.json")); S = J["sections"]
def dur(f): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
sil = "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05"
for x in S:
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{HERE}/audio/{x['id']}.wav", "-af", f"{sil},areverse,{sil},areverse", f"{HERE}/audio/{x['id']}_trim.wav"], check=True)
tot = sum(dur(f"{HERE}/audio/{x['id']}_trim.wav") for x in S); tempo = min(1.18, max(1.0, tot / TARGET)); print("trimmed total", tot, "tempo", tempo)
t = 0
for x in S:
    f = f"{HERE}/audio/{x['id']}_final.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{HERE}/audio/{x['id']}_trim.wav", "-af", f"atempo={tempo:.4f},loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000", "-ac", "2", f], check=True)
    x["adur"] = dur(f); x["vdur"] = round(PAD_IN + x["adur"] + PAD_OUT, 2); x["start"] = round(t, 2); t += x["vdur"]
    print(x["id"], round(x["adur"], 2), x["vdur"], x["start"])
S[-1]["vdur"] += 1.0; t += 1.0
J["tempo"] = tempo; J["total"] = t; J["pad_in"] = PAD_IN; print("total video", t)
json.dump(J, open(f"{HERE}/sections.json", "w"), indent=1)
