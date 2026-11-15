"""Phoenixastar README banner and GitHub social preview, set over a ray-traced black hole.

The black holes are real renders, not drawings. viz/blackhole/raytrace.py traces one light ray per sub-pixel backwards
along Schwarzschild null geodesics on an A100 (thin Keplerian disk, Doppler beaming, gravitational redshift, lensed
star field). The two backgrounds are committed next to it and were made on GPU 0 of the Lambda box with:

  CUDA_VISIBLE_DEVICES=0 python3 viz/blackhole/raytrace.py --w 2400 --h 900 --ss 3 --fov 60 --yaw -13 --rout 13 --tpeak 4800 --elev 5 --sat 1.2 --out viz/blackhole/out/banner_bg.png
      -> viz/blackhole/banner_bg.png   (19.4M rays, 10.6 s; metadata in viz/blackhole/banner_bg.json)
  CUDA_VISIBLE_DEVICES=0 python3 viz/blackhole/raytrace.py --w 1280 --h 640 --ss 3 --fov 56 --yaw -13 --rout 13 --tpeak 4800 --elev 5 --sat 1.2 --out viz/blackhole/out/social_bg.png
      -> viz/blackhole/social_bg.png   (7.4M rays, 5.5 s; metadata in viz/blackhole/social_bg.json)

A negative --yaw turns the camera left, so the hole sits right of centre and the text gets the dark sky on the left.
This script only (1) dims the far, receding tail of the disk behind the text with a soft horizontal gradient,
(2) lifts pure black to the palette background, and (3) sets the type. The live stats line reads
web/public/data/state.json (read only); if the totals are missing the line is left out, never invented.

The shadow position and size are computed from the same camera (critical impact parameter b = 3*sqrt(3) M), and the
script refuses to write an image in which any text touches the shadow or photon ring, or any main-column text runs
onto the lensed disk arc, or (social preview) any text sits closer than 48 px to an edge.

  /opt/anaconda3/bin/python3 viz/make_banner.py
      -> docs/assets/banner.png (2400x900) and docs/assets/social-preview.png (1280x640)
"""
import json, math, os, sys

import numpy as np
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BG, FG, MUTED, ACC = "#0A0C0F", "#EEF2F6", "#8A94A3", "#4FD1E0"
SANS = ["Avenir Next", "Helvetica Neue", "Inter"]
MONO = ["Menlo", "SF Mono", "DejaVu Sans Mono"]

TAGLINE = "An AI lab that gets better at discovering mathematics and physics by doing it. Every claim verified."
INFRA = "8x A100  ·  Modal fleet  ·  GPT-6 Astra + Claude Fable 5.2"
FOOT = "Black hole ray-traced on an A100 · Schwarzschild null geodesics"

# Camera of each committed background (must match the command lines above; dist 30, pitch 0 are raytrace defaults).
CAM = {
    "banner": dict(w=2400, h=900, fov=60.0, yaw=-13.0, elev=5.0, dist=30.0),
    "social": dict(w=1280, h=640, fov=56.0, yaw=-13.0, elev=5.0, dist=30.0),
}

LAYOUT = {
    # All positions in output pixels; y values are text baselines measured from the top.
    "banner": dict(
        bg="viz/blackhole/banner_bg.png", out="docs/assets/banner.png", margin=36,
        x0=132, label=(170, 30), word=(352, 176), tag=([
            "An AI lab that gets better at discovering",
            "mathematics and physics by doing it.",
            "Every claim verified."], 432, 46, 1.36),
        stats=(694, 31), infra=(748, 31), foot=(22, 36, 34),
        dim_lo=0.22, dim_from=0.16),
    "social": dict(
        bg="viz/blackhole/social_bg.png", out="docs/assets/social-preview.png", margin=48,
        x0=72, label=(150, 21), word=(262, 108), tag=([
            "An AI lab that gets better at",
            "discovering mathematics and physics",
            "by doing it. Every claim verified."], 322, 31, 1.38),
        stats=None, infra=(484, 18), foot=(15, 48, 48),
        dim_lo=0.22, dim_from=0.12),
}


def face(families, style, size):
    """First installed family, in the requested style (picks the right face out of a .ttc collection)."""
    weight = {"Bold": "bold", "Medium": "medium"}.get(style, "regular")
    for fam in families:
        try:
            path = font_manager.findfont(font_manager.FontProperties(family=fam, weight=weight), fallback_to_default=False)
        except Exception:
            continue
        if path.lower().endswith(".ttc"):
            for i in range(64):
                try:
                    f = ImageFont.truetype(path, size, index=i)
                except OSError:
                    break
                if f.getname()[1].lower() == style.lower():
                    return f
            for i in range(64):  # family present but no exact style: take its regular face
                try:
                    f = ImageFont.truetype(path, size, index=i)
                except OSError:
                    break
                if f.getname()[1].lower() == "regular":
                    return f
        else:
            return ImageFont.truetype(path, size)
    return ImageFont.truetype(font_manager.findfont("DejaVu Sans"), size)


def stats():
    try:
        with open(os.path.join(ROOT, "web", "public", "data", "state.json")) as fh:
            t = json.load(fh).get("totals", {})
        d, c, e = t.get("decisions"), t.get("cycles"), t.get("experiments_run")
        if isinstance(d, int) and isinstance(c, int) and isinstance(e, int):
            return f"{d:,} logged decisions  ·  {c:,} cycles  ·  {e:,} experiments run"
    except Exception as ex:
        print("stats line skipped:", ex)
    return None


def hole(cam):
    """Screen centre and shadow radius (px) of the hole, from the raytracer's own camera model (r_s = 1)."""
    w, h, dist = cam["w"], cam["h"], cam["dist"]
    el = math.radians(cam["elev"])
    pos = np.array([0.0, dist * math.sin(el), -dist * math.cos(el)])
    f0 = -pos / np.linalg.norm(pos)
    upw = np.array([0.0, 1.0, 0.0])
    r0 = np.cross(upw, f0); r0 /= np.linalg.norm(r0)
    yaw = math.radians(cam["yaw"])
    f = f0 * math.cos(yaw) + r0 * math.sin(yaw); f /= np.linalg.norm(f)
    right = np.cross(upw, f); right /= np.linalg.norm(right)
    up = np.cross(f, right)
    tx = math.tan(math.radians(cam["fov"]) / 2); ty = tx * h / w
    u = (f0 @ right) / (f0 @ f) / tx; v = (f0 @ up) / (f0 @ f) / ty
    cx, cy = (u + 1) / 2 * w, (1 - v) / 2 * h
    sin_a = 1.5 * math.sqrt(3) * math.sqrt(1 - 1 / dist) / dist     # b_crit = 3 sqrt(3) M, M = 1/2
    off = math.acos(float(np.clip(f0 @ f, -1, 1)))                  # off-axis angle stretches the image
    r = math.tan(math.asin(sin_a)) / tx * (w / 2) / math.cos(off) ** 2
    return cx, cy, r


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def hexrgb(s, a=255):
    return tuple(int(s[i:i + 2], 16) for i in (1, 3, 5)) + (a,)


def tracked(draw, xy, text, font, fill, track):
    """Letter-spaced text (left, baseline); returns its bbox."""
    x, y = xy
    x_start = x
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill, anchor="ls")
        x += font.getlength(ch) + track
    top = y - font.getbbox("A", anchor="ls")[1] * -1
    return (x_start, y + font.getbbox("A", anchor="ls")[1], x - track, y + font.getbbox("g", anchor="ls")[3])


def compose(name):
    L, cam = LAYOUT[name], CAM[name]
    W, H = cam["w"], cam["h"]
    src = Image.open(os.path.join(ROOT, L["bg"])).convert("RGB")
    assert src.size == (W, H), f"{L['bg']} is {src.size}, expected {(W, H)}"
    cx, cy, rs = hole(cam)
    keep_out = 1.30 * rs          # shadow + photon ring (+ the dark gap around it)
    arc_edge = cx - 1.95 * rs     # left edge of the lensed upper disk image

    # 1) dim the receding disk tail behind the text, 2) lift black to the palette background
    img = np.asarray(src).astype(np.float32) / 255
    xs = (np.arange(W) + 0.5)
    dim = L["dim_lo"] + (1 - L["dim_lo"]) * smoothstep(L["dim_from"] * W, arc_edge - 0.02 * W, xs)
    img = img * dim[None, :, None]
    bgc = np.array(hexrgb(BG)[:3], np.float32) / 255
    img = 1 - (1 - img) * (1 - bgc)
    base = Image.fromarray((img * 255 + 0.5).clip(0, 255).astype(np.uint8)).convert("RGBA")

    # 3) type
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(layer)
    boxes = []                    # (name, bbox, main_column)
    x0 = L["x0"]
    y, s = L["label"]
    fl = face(MONO, "Regular", s)
    boxes.append(("label", tracked(dr, (x0, y), "AUTONOMOUS RESEARCH LAB", fl, hexrgb(ACC), 0.22 * s), True))
    y, s = L["word"]
    fw = face(SANS, "Bold", s)
    dr.text((x0 - 0.04 * s, y), "Phoenixastar", font=fw, fill=hexrgb(FG), anchor="ls")
    boxes.append(("wordmark", dr.textbbox((x0 - 0.04 * s, y), "Phoenixastar", font=fw, anchor="ls"), True))
    lines, y, s, lsp = L["tag"]
    assert " ".join(lines) == TAGLINE, "tagline line breaks must join to the exact tagline"
    ft = face(SANS, "Medium", s)
    for i, ln in enumerate(lines):
        yy = round(y + i * s * lsp)
        dr.text((x0, yy), ln, font=ft, fill=hexrgb(FG, 236), anchor="ls")
        boxes.append((f"tagline{i}", dr.textbbox((x0, yy), ln, font=ft, anchor="ls"), True))
    if L["stats"]:
        line = stats()
        if line:
            y, s = L["stats"]
            fm = face(MONO, "Regular", s)
            dr.text((x0, y), line, font=fm, fill=hexrgb(MUTED), anchor="ls")
            boxes.append(("stats", dr.textbbox((x0, y), line, font=fm, anchor="ls"), True))
    y, s = L["infra"]
    fm = face(MONO, "Regular", s)
    dr.text((x0, y), INFRA, font=fm, fill=hexrgb(MUTED), anchor="ls")
    boxes.append(("infra", dr.textbbox((x0, y), INFRA, font=fm, anchor="ls"), True))
    s, rm, bm = L["foot"]
    ff = face(MONO, "Regular", s)
    fx, fy = W - rm, H - bm
    dr.text((fx, fy), FOOT, font=ff, fill=hexrgb(MUTED, 120), anchor="rd")
    boxes.append(("footnote", dr.textbbox((fx, fy), FOOT, font=ff, anchor="rd"), False))

    # checks: nothing on the shadow / photon ring, main column clear of the lensed arc, edge margins
    for nm, (a, b, c, d), main in boxes:
        nx, ny = min(max(cx, a), c), min(max(cy, b), d)          # closest point of the box to the hole centre
        assert math.hypot(nx - cx, ny - cy) > keep_out, f"{name}: {nm} covers the shadow/photon ring"
        if main and b < cy + 1.6 * rs and d > cy - 1.6 * rs:     # rows where the lensed disk image is
            assert c < arc_edge, f"{name}: {nm} runs onto the lensed arc (right edge {c:.0f} >= {arc_edge:.0f})"
        if name == "social":
            assert a >= 48 and b >= 48 and c <= W - 48 and d <= H - 48, f"social: {nm} is within 48 px of an edge"
    out = Image.alpha_composite(base, layer).convert("RGB")
    path = os.path.join(ROOT, L["out"])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    out.save(path, optimize=True)
    right = max(c for _, (a, b, c, d), m in boxes if m)
    print(f"wrote {L['out']} {W}x{H}  hole centre ({cx:.0f},{cy:.0f}) shadow r {rs:.0f}px  "
          f"text right edge {right:.0f} < arc {arc_edge:.0f}")


if __name__ == "__main__":
    for n in sys.argv[1:] or ["banner", "social"]:
        compose(n)
