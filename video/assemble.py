"""Assembles the final demo: screen clips + B-roll + per-section narration + lower-third captions."""
import json, os, subprocess
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
J = json.load(open(f"{HERE}/sections.json")); S = J["sections"]; PAD_IN = J["pad_in"]; W, H = 1920, 1080
BROLL = f"{ROOT}/web/public/gallery/lattice_orbit.mp4"
FB, FR = "/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/System/Library/Fonts/Supplemental/Arial.ttf"
def font(p, n): return ImageFont.truetype(p, n)
def run(a): subprocess.run(["ffmpeg", "-y", "-v", "error"] + a, check=True)
def lower_third(text, out):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); f = font(FB, 30); parts = [p.strip() for p in text.split("|")]
    sep = "    "; widths = [d.textlength(p, font=f) for p in parts]; sw = d.textlength(sep, font=f); tw = sum(widths) + sw * (len(parts) - 1)
    if tw > W - 200:
        f = font(FB, 25); widths = [d.textlength(p, font=f) for p in parts]; sw = d.textlength(sep, font=f); tw = sum(widths) + sw * (len(parts) - 1)
    x0 = (W - tw) / 2; y0, y1 = H - 104, H - 40
    d.rounded_rectangle([x0 - 36, y0, x0 + tw + 36, y1], radius=14, fill=(7, 8, 11, 235), outline=(61, 245, 255, 200), width=2)
    x = x0
    for i, p in enumerate(parts):
        d.text((x, (y0 + y1) / 2), p, font=f, fill=(255, 255, 255, 255) if i else (61, 245, 255, 255), anchor="lm"); x += widths[i]
        if i < len(parts) - 1:
            d.ellipse([x + sw / 2 - 4, (y0 + y1) / 2 - 4, x + sw / 2 + 4, (y0 + y1) / 2 + 4], fill=(255, 181, 71, 255)); x += sw
    im.save(out)
def card(title, lines, out):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, H], fill=(4, 5, 8, 120)); d.rectangle([0, 330, W, 750], fill=(4, 5, 8, 185))
    d.text((W / 2, 450), title, font=font(FB, 104), fill=(255, 255, 255, 255), anchor="mm")
    for i, (t, col) in enumerate(lines): d.text((W / 2, 570 + i * 62), t, font=font(FR, 40), fill=col, anchor="mm")
    im.save(out)
CY, AM, GR = (61, 245, 255, 255), (255, 181, 71, 255), (200, 206, 216, 255)
card("Phoenixastar", [("An autonomous AI lab for open math problems", CY), ("Iterate AI Research Hackathon  |  Track 1  |  live run, Nov 15", GR)], f"{HERE}/build/card_s1.png")
card("Phoenixastar", [("No math record beaten yet. Three-body orbits are candidates. Every decision is logged.", AM), ("vnmoorthy.github.io/phoenixastar", CY)], f"{HERE}/build/card_s9.png")
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", "30"]
segs = []
for x in S:
    sid, vd = x["id"], x["vdur"]; raw = f"{HERE}/build/{sid}_raw.mp4"; out = f"{HERE}/build/{sid}.mp4"
    if sid in ("s1_intro", "s9_close"):
        run(["-stream_loop", "3", "-i", BROLL, "-t", f"{vd}", "-vf", f"scale={W}:{H}:flags=lanczos,fps=30,format=yuv420p", "-an"] + ENC + [raw]); ov = f"{HERE}/build/card_{sid[:2]}.png"
    else:
        parts = sorted(f for f in os.listdir(f"{HERE}/clips") if f.startswith(sid[:2]) and f.endswith(".mp4"))
        assert parts, f"no clip for {sid}"
        open(f"{HERE}/build/{sid}.txt", "w").write("".join(f"file '{HERE}/clips/{p}'\n" for p in parts))
        run(["-f", "concat", "-safe", "0", "-i", f"{HERE}/build/{sid}.txt", "-vf", f"fps=30,tpad=stop_mode=clone:stop_duration=3,format=yuv420p", "-t", f"{vd}", "-an"] + ENC + [raw])
        ov = f"{HERE}/build/cap_{sid}.png"; lower_third(x["caption"], ov)
    run(["-i", raw, "-loop", "1", "-i", ov, "-i", f"{HERE}/audio/{sid}_final.wav",
         "-filter_complex", f"[1:v]format=rgba,fade=in:st=0.2:d=0.4:alpha=1[o];[0:v][o]overlay=0:0:shortest=0[v];[2:a]adelay={int(PAD_IN*1000)}:all=1,apad[a]",
         "-map", "[v]", "-map", "[a]", "-t", f"{vd}"] + ENC + ["-c:a", "aac", "-b:a", "192k", "-ar", "48000", out])
    segs.append(out); print("built", sid, vd, flush=True)
open(f"{HERE}/build/all.txt", "w").write("".join(f"file '{p}'\n" for p in segs))
final = f"{HERE}/phoenixastar_demo.mp4"
run(["-f", "concat", "-safe", "0", "-i", f"{HERE}/build/all.txt", "-vf", "fade=in:st=0:d=0.5,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "30",
     "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", final])
run(["-ss", "2.5", "-i", final, "-frames:v", "1", "-vf", "scale=1280:720:flags=lanczos", f"{HERE}/poster.png"])
print(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration,size:stream=codec_name,width,height,pix_fmt,r_frame_rate", "-of", "default=nw=1", final]).decode())
