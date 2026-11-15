"""Build the presenter demo video from the presenter's own take.

  python3 video/compose_talk.py align   [path/to/take.mov]  # transcribe (OpenAI whisper-1, word timestamps), find sections
  python3 video/compose_talk.py record                      # screen clips per section (video/record_talk.py)
  python3 video/compose_talk.py compose                     # screen + presenter picture-in-picture + their audio
  python3 video/compose_talk.py all     [path/to/take.mov]

Sections follow docs/TALK_TRACK.md. Each section starts where the presenter says its first words (fuzzy match on the
transcript); if a phrase is not found, the boundary falls back to the longest pause near the expected time.
Output: video/phoenixastar_demo_presenter.mp4 (1920x1080, H.264 + AAC).
"""
import difflib, glob, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ME = f"{HERE}/me"
OUT = f"{HERE}/phoenixastar_demo_presenter.mp4"
FONT = "/System/Library/Fonts/Helvetica.ttc"
SECTIONS = [  # id, first words the presenter says, lower-third title
    ("s1", "what if a research lab ran itself", "Phoenixastar"),
    ("s2", "every three minutes with no human in the loop", "The autonomous loop"),
    ("s3", "predictions get checked", "Predictions get checked"),
    ("s4", "the same loop now does physics", "EVENT HORIZON · ray-traced live in the browser"),
    ("s5", "starforge asks what matter inside a neutron star", "STARFORGE · neutron-star matter"),
    ("s6", "on the three-body problem", "Three-body periodic orbits"),
    ("s7", "the lab also improves itself", "It learns: Tinker, Devin, Modal, past.dev"),
    ("s8", "no breakthroughs claimed", "Research that verifies itself"),
]


def sh(*a, **k):
    return subprocess.run(list(a), check=True, **k)


def probe_duration(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True, check=True).stdout.strip())


def find_take(arg=None):
    if arg:
        return os.path.abspath(arg)
    c = sorted(glob.glob(f"{ME}/take.*") + glob.glob(f"{ME}/*.mov") + glob.glob(f"{ME}/*.mp4") + glob.glob(f"{ME}/*.m4v"))
    if not c:
        sys.exit(f"no take found in {ME}/ (expected take.mov or take.mp4)")
    return c[0]


def _env_key():
    k = os.environ.get("OPENAI_API_KEY")
    if k:
        return k
    for line in open(f"{ROOT}/.env"):
        if line.startswith("OPENAI_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"')
    sys.exit("OPENAI_API_KEY not set")


def norm(t):
    return re.sub(r"[^a-z0-9 ]", " ", t.lower().replace("-", " ")).split()


def align(take):
    os.makedirs(ME, exist_ok=True)
    dur = probe_duration(take)
    audio = f"{ME}/audio.mp3"
    sh("ffmpeg", "-y", "-v", "error", "-i", take, "-vn", "-ac", "1", "-ar", "16000", "-b:a", "64k", audio)
    from openai import OpenAI
    cli = OpenAI(api_key=_env_key())
    tr = cli.audio.transcriptions.create(model="whisper-1", file=open(audio, "rb"), response_format="verbose_json",
                                         timestamp_granularities=["word", "segment"])
    tr = tr.model_dump() if hasattr(tr, "model_dump") else dict(tr)
    json.dump(tr, open(f"{ME}/transcript.json", "w"), indent=1)
    words = [(w["start"], w["end"], norm(w["word"])[0] if norm(w["word"]) else "") for w in tr.get("words") or []]
    words = [w for w in words if w[2]]
    toks = [w[2] for w in words]
    starts, pos = [], 0
    for i, (sid, phrase, _) in enumerate(SECTIONS):
        if i == 0:
            starts.append(0.0); continue
        ph = norm(phrase); n = len(ph); best, bi = 0.0, None
        for j in range(pos, max(pos, len(toks) - n + 1)):
            r = difflib.SequenceMatcher(None, " ".join(toks[j:j + n]), " ".join(ph)).ratio()
            if r > best:
                best, bi = r, j
        if bi is not None and best >= 0.62:
            starts.append(max(0.0, words[bi][0] - 0.25)); pos = bi + n
            print(f"{sid}: '{' '.join(toks[bi:bi + n])}' at {words[bi][0]:.2f}s (match {best:.2f})")
        else:   # fall back: longest pause near the proportional position
            exp = dur * i / len(SECTIONS)
            gaps = [(words[k + 1][0] - words[k][1], words[k][1], k + 1) for k in range(len(words) - 1)
                    if abs(words[k][1] - exp) < dur * 0.08 and k + 1 > pos]
            if gaps:
                g = max(gaps); starts.append(g[1] + min(0.3, g[0] / 2)); pos = g[2]
            else:
                starts.append(exp)
            print(f"{sid}: phrase not found (best {best:.2f}); boundary at {starts[-1]:.2f}s")
    secs = []
    for i, (sid, phrase, title) in enumerate(SECTIONS):
        a = starts[i]; b = starts[i + 1] if i + 1 < len(starts) else dur
        secs.append({"id": sid, "start": round(a, 3), "end": round(b, 3), "dur": round(b - a, 3), "title": title})
    json.dump({"take": take, "duration": dur, "text": tr.get("text"), "sections": secs}, open(f"{ME}/sections.json", "w"), indent=1)
    print(json.dumps(secs, indent=1))


def record():
    sh(sys.executable, f"{HERE}/record_talk.py")


def compose():
    meta = json.load(open(f"{ME}/sections.json"))
    take, secs = meta["take"], meta["sections"]
    lst = f"{ME}/concat.txt"
    with open(lst, "w") as f:
        for s in secs:
            clip = f"{HERE}/clips_talk/{s['id']}.mp4"
            if not os.path.exists(clip):
                sys.exit(f"missing {clip}: run record first")
            f.write(f"file '{clip}'\n")
    screen = f"{ME}/screen.mp4"
    sh("ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", screen)
    banner = f"{ROOT}/docs/assets/banner.png"
    from PIL import Image, ImageDraw, ImageFont
    font = ImageFont.truetype(FONT, 34)
    title_inputs, overlays = [], []
    for k, s in enumerate(secs):   # lower-third titles as transparent PNGs (this ffmpeg build has no drawtext)
        tw = int(font.getlength(s["title"])) + 44
        im = Image.new("RGBA", (tw, 70), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, tw - 1, 69), radius=10, fill=(11, 13, 16, 190))
        d.rectangle((0, 14, 3, 55), fill=(79, 209, 224, 255))
        d.text((22, 16), s["title"], font=font, fill=(231, 233, 236, 255))
        fn = f"{ME}/title_{s['id']}.png"; im.save(fn); title_inputs += ["-loop", "1", "-t", f"{meta['duration']:.2f}", "-i", fn]
        t0, t1 = s["start"] + 0.4, s["start"] + 4.2
        overlays.append((3 + k, t0, t1))
    pip = 300
    fc = (
        f"[0:v]setpts=PTS-STARTPTS[scr];"
        f"[2:v]scale=1920:-1,pad=1920:1080:0:(1080-ih)/2:color=0x0B0D10,format=rgba,"
        f"fade=t=out:st=2.6:d=0.7:alpha=1[ban];"
        f"[1:v]crop='min(iw,ih)':'min(iw,ih)',scale={pip}:{pip},format=yuva420p,"
        f"geq=lum='p(X,Y)':cb='p(X,Y)':cr='p(X,Y)':a='if(lte(hypot(X-{pip/2},Y-{pip/2}),{pip/2 - 1}),255,0)'[cam];"
        f"color=c=0x4FD1E0:s={pip + 8}x{pip + 8},format=yuva420p,"
        f"geq=lum='p(X,Y)':cb='p(X,Y)':cr='p(X,Y)':a='if(lte(hypot(X-{(pip + 8)/2},Y-{(pip + 8)/2}),{(pip + 8)/2 - 1}),200,0)'[ring];"
        f"[scr][ring]overlay=W-w-56:H-h-56:shortest=1[a];"
        f"[a][cam]overlay=W-w-60:H-h-60:shortest=1[b];"
        f"[b][ban]overlay=0:0:enable='lte(t,3.4)'[t0];"
    )
    last = "t0"
    for k, (idx, t0, t1) in enumerate(overlays):
        fc += (f"[{idx}:v]format=rgba,fade=t=in:st={t0:.2f}:d=0.3:alpha=1,fade=t=out:st={t1 - 0.3:.2f}:d=0.3:alpha=1[ti{k}];"
               f"[{last}][ti{k}]overlay=60:H-h-60:enable='between(t,{t0:.2f},{t1:.2f})'[t{k + 1}];")
        last = f"t{k + 1}"
    fc += f"[{last}]null[v]"
    sh("ffmpeg", "-y", "-v", "error", "-i", screen, "-i", take, "-loop", "1", "-t", "3.4", "-i", banner, *title_inputs,
       "-filter_complex", fc, "-map", "[v]", "-map", "1:a:0", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
       "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
       "-movflags", "+faststart", "-t", f"{meta['duration']:.2f}", OUT)
    print("wrote", OUT, round(probe_duration(OUT), 1), "s")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    arg = sys.argv[2] if len(sys.argv) > 2 else None
    if cmd in ("align", "all"):
        align(find_take(arg))
    if cmd in ("record", "all"):
        record()
    if cmd in ("compose", "all"):
        compose()
