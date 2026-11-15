#!/usr/bin/env python3
"""Builds deck/Phoenixastar.pptx (10 slides, 16:9) and deck/storyboard.md from the live snapshot.

    python3 deck/build_deck.py            # build + validate
    python3 deck/build_deck.py --preview  # also render deck/build/preview/slide-NN.png (needs soffice + pdftoppm)

Every number comes from web/public/data/*.json at build time (see deckdata.py). Motion:
  - Morph transition on every slide (p159:morph inside mc:AlternateContent, fade fallback for old viewers);
    shapes named "!!..." (backdrop, wordmark, progress bar) morph between slides.
  - Staggered entrance animations (fade / zoom / wipe) that start by themselves when the slide appears.
  - Number build-ups: a stack of opaque frames revealed one after another, last frame = real value
    (static exports show only the real value).
  - The two Blender MP4s are embedded and set to autoplay, muted, looping.
"""
from __future__ import annotations

import argparse
import math
import os
import shutil
import subprocess
import sys
import zipfile

from lxml import etree
from PIL import Image, ImageDraw, ImageFilter
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml import parse_xml
from pptx.util import Emu, Inches, Pt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import deckdata as dd  # noqa: E402
from deckdata import clip, fmt, pct, short  # noqa: E402

OUT = os.path.join(HERE, "Phoenixastar.pptx")
BUILD = os.path.join(HERE, "build")
W, H = 13.333, 7.5

# palette (same as the web app)
BG = "0B0D10"
PANEL = "111418"
PANEL2 = "171B21"
LINE = "252B35"
CYAN = "4FD1E0"
AMBER = "E8B65C"
WHITE = "EEF2F6"
GREY = "8A94A3"
DIM = "5D6675"
RED = "E06C6C"
GREEN = "6CCB8F"
PROBLEM_COLORS = {
    "no-three-in-line-75": "4FD1E0",
    "spencer-discrepancy": "B18CFF",
    "hadamard-det-51": "6EE7A0",
    "two-deletion-code-16": "FF7AB6",
    "sidon-45-set": "7AA2FF",
    "snake-in-the-box-13": "F4F06A",
    "ring-loading-15": "C9D1DC",
}
SANS = "Helvetica Neue"
MONO = "Menlo"

NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
NSDECL = (f'xmlns:p="{NS_P}" xmlns:a="{NS_A}" '
          'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
          'xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" '
          'xmlns:p159="http://schemas.microsoft.com/office/powerpoint/2015/09/main"')


def rgb(h):
    return RGBColor.from_string(h)


def pcolor(slug):
    return PROBLEM_COLORS.get(slug, GREY)


# ------------------------------------------------------------------ drawing helpers
def _alpha(fill_owner, alpha):
    """alpha in 0..1 on a solid fill (python-pptx has no API for it)."""
    sf = fill_owner._xPr.find(f"{{{NS_A}}}solidFill") if hasattr(fill_owner, "_xPr") else None
    if sf is None:
        return
    clr = sf[0]
    for old in clr.findall(f"{{{NS_A}}}alpha"):
        clr.remove(old)
    a = etree.SubElement(clr, f"{{{NS_A}}}alpha")
    a.set("val", str(int(alpha * 100000)))


def box(slide, x, y, w, h, fill=PANEL, line=LINE, radius=0.06, name=None, alpha=None, lw=0.75, shape=MSO_SHAPE.ROUNDED_RECTANGLE):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = min(0.5, radius / max(0.01, min(w, h)))
    s.shadow.inherit = False
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = rgb(fill)
        if alpha is not None:
            _alpha(s.fill, alpha)
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = rgb(line)
        s.line.width = Pt(lw)
    if name:
        s.name = name
    return s


def text(slide, x, y, w, h, content, size=14, color=WHITE, bold=False, font=SANS, align="l", anchor="t", name=None,
         fill=None, spacing=None, line_spacing=None):
    """content: str | list of paragraphs; a paragraph is str | list of runs; a run is str | (str, {size,color,bold,font})."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if fill:
        tb.fill.solid()
        tb.fill.fore_color.rgb = rgb(fill)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
    paras = content if isinstance(content, list) else [content]
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
        if spacing is not None and i > 0:
            p.space_before = Pt(spacing)
        if line_spacing is not None:
            p.line_spacing = line_spacing
        runs = para if isinstance(para, list) else [para]
        for r in runs:
            t, st = (r, {}) if isinstance(r, str) else r
            run = p.add_run()
            run.text = t
            f = run.font
            f.name = st.get("font", font)
            f.size = Pt(st.get("size", size))
            f.bold = st.get("bold", bold)
            f.color.rgb = rgb(st.get("color", color))
    if name:
        tb.name = name
    return tb


def picture(slide, path, x, y, w=None, h=None, name=None):
    kw = {}
    if w is not None:
        kw["width"] = Inches(w)
    if h is not None:
        kw["height"] = Inches(h)
    pic = slide.shapes.add_picture(path, Inches(x), Inches(y), **kw)
    if name:
        pic.name = name
    return pic


def chip(slide, x, y, label, color=CYAN, size=10, w=None, h=0.3, filled=False):
    w = w or (0.2 + 0.088 * len(label) * size / 10)
    b = box(slide, x, y, w, h, fill=color if filled else PANEL, line=color, radius=h / 2, lw=0.75)
    tf = b.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = label
    r.font.name = MONO
    r.font.size = Pt(size)
    r.font.color.rgb = rgb(BG if filled else color)
    r.font.bold = filled
    return b, w


# ------------------------------------------------------------------ generated images
def make_backdrop(path):
    """Near-black backdrop with the app's faint grid and a soft cyan glow."""
    w, h = 1920, 1080
    img = Image.new("RGB", (w, h), "#" + BG)
    glow = Image.new("RGB", (w, h), "#" + BG)
    g = ImageDraw.Draw(glow)
    g.ellipse([w * 0.55, -h * 0.55, w * 1.25, h * 0.45], fill=(10, 38, 48))
    g.ellipse([-w * 0.3, h * 0.7, w * 0.25, h * 1.5], fill=(26, 20, 10))
    glow = glow.filter(ImageFilter.GaussianBlur(180))
    img = Image.blend(img, glow, 0.9)
    d = ImageDraw.Draw(img, "RGBA")
    for x in range(0, w, 48):
        d.line([(x, 0), (x, h)], fill=(120, 160, 190, 10))
    for y in range(0, h, 48):
        d.line([(0, y), (w, y)], fill=(120, 160, 190, 10))
    img.save(path, quality=92)


def make_fade(path, w, h, direction, color=BG, max_alpha=255, power=1.0):
    """RGBA gradient from `color` (opaque) to transparent. direction: 'down' = opaque at top, 'right' = opaque at left, etc."""
    c = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
    img = Image.new("RGBA", (w, h))
    px = img.load()
    for j in range(h):
        for i in range(w):
            t = {"down": j / (h - 1), "up": 1 - j / (h - 1), "right": i / (w - 1), "left": 1 - i / (w - 1)}[direction]
            px[i, j] = c + (int(max_alpha * (1 - t) ** power),)
    img.save(path)


def crop_to(src, dst, ratio, anchor=(0.5, 0.5), brightness=1.0):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    if w / h > ratio:
        nw = int(h * ratio)
        x0 = int((w - nw) * anchor[0])
        im = im.crop((x0, 0, x0 + nw, h))
    else:
        nh = int(w / ratio)
        y0 = int((h - nh) * anchor[1])
        im = im.crop((0, y0, w, y0 + nh))
    if brightness != 1.0:
        im = Image.eval(im, lambda v: int(v * brightness))
    im.save(dst, quality=90)
    return dst


def poster_from(mp4, fallback, dst):
    """First frame of the video (so play start is seamless); falls back to the still render."""
    if shutil.which("ffmpeg"):
        r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp4, "-frames:v", "1", "-q:v", "2", dst], capture_output=True)
        if r.returncode == 0 and os.path.exists(dst):
            return dst
    return fallback


def video_ms(mp4, default=8000):
    if shutil.which("ffprobe"):
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4], capture_output=True, text=True)
        try:
            return int(float(r.stdout.strip()) * 1000)
        except Exception:  # noqa: BLE001
            pass
    return default


def _mpl():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({
        "font.family": [SANS, "Helvetica", "Arial", "DejaVu Sans"], "font.size": 13,
        "axes.facecolor": "#" + PANEL, "figure.facecolor": "#" + PANEL, "savefig.facecolor": "#" + PANEL,
        "axes.edgecolor": "#" + LINE, "axes.labelcolor": "#" + GREY, "xtick.color": "#" + GREY, "ytick.color": "#" + GREY,
        "grid.color": "#" + LINE, "axes.spines.top": False, "axes.spines.right": False, "text.color": "#" + WHITE,
    })
    return plt


def chart_learning(D, path):
    plt = _mpl()
    steps = D["steps"]
    fig, ax = plt.subplots(figsize=(9.2, 4.6), dpi=200)
    if steps:
        xs = [s["step"] for s in steps]
        mean = [s.get("reward_mean") for s in steps]
        best = [s.get("reward_best") for s in steps]
        valid = [s.get("valid_rate") or 0 for s in steps]
        ax2 = ax.twinx()
        ax2.fill_between(xs, [100 * v for v in valid], color="#" + AMBER, alpha=0.13, step="mid", linewidth=0)
        ax2.plot(xs, [100 * v for v in valid], color="#" + AMBER, alpha=0.55, linewidth=1.2, drawstyle="steps-mid")
        ax2.set_ylim(0, 105)
        ax2.set_ylabel("valid constructions (%)", color="#" + AMBER)
        ax2.tick_params(axis="y", colors="#" + AMBER)
        ax2.spines["top"].set_visible(False)
        ax2.spines["right"].set_color("#" + LINE)
        ax.plot(xs, best, color="#" + CYAN, alpha=0.35, linewidth=1.4, linestyle="--", label="best in batch")
        ax.plot(xs, mean, color="#" + CYAN, linewidth=3.0, label="mean reward", solid_capstyle="round")
        ax.scatter([xs[-1]], [mean[-1]], color="#" + CYAN, s=60, zorder=5)
        ax.set_zorder(ax2.get_zorder() + 1)
        ax.patch.set_visible(False)
        ax.set_xlim(xs[0], xs[-1] + 0.5)
        ax.set_ylim(0, max(max(best), max(mean)) * 1.12)
        ax.legend(loc="lower right", frameon=False, labelcolor="#" + GREY, fontsize=11)
    ax.set_xlabel("RL step")
    ax.set_ylabel("reward from the official verifier", color="#" + CYAN)
    ax.tick_params(axis="y", colors="#" + CYAN)
    ax.grid(True, axis="y", linewidth=0.6)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def chart_bench(D, path):
    plt = _mpl()
    S = D["bench_systems"]
    order = [n for n in ("past.dev", "markdown", "rag") if n in S] + [n for n in S if n not in ("past.dev", "markdown", "rag")]
    fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.9), dpi=200)
    specs = [("accuracy", lambda s: 100 * (s.get("accuracy") or 0), "{:.0f}%", "accuracy  (higher is better)"),
             ("latency", lambda s: s.get("latency_ms") or 0, "{:.0f} ms", "lookup latency  (lower)"),
             ("cost", lambda s: 1000 * (s.get("cost_per_question_usd") or ((s.get("cost_usd") or 0) / max(1, s.get("n") or 1))), "${:.2f}", "cost per 1k questions  (lower)")]
    for ax, (key, fn, f, title) in zip(axes, specs):
        vals = [fn(S[n]) for n in order]
        cols = ["#" + (CYAN if n == "past.dev" else DIM) for n in order]
        bars = ax.bar(order, vals, color=cols, width=0.62)
        top = max(vals) if vals and max(vals) > 0 else 1
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + top * 0.03, f.format(v), ha="center", va="bottom", fontsize=10.5,
                    color="#" + WHITE, family=[MONO, "DejaVu Sans Mono"])
        ax.set_ylim(0, top * 1.25)
        ax.set_title(title, fontsize=10, color="#" + GREY, pad=8)
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
        ax.tick_params(axis="x", labelsize=10, length=0)
    fig.tight_layout(w_pad=1.2)
    fig.savefig(path)
    plt.close(fig)


def image_cpu_grid(D, path, cols=31):
    """One cell per CPU core, coloured by the problem that owns it (from compute.cpu_procs)."""
    n = D["cpus"] or 0
    rows = max(1, math.ceil(n / cols))
    cell, gap = 34, 7
    img = Image.new("RGB", (cols * (cell + gap) - gap, rows * (cell + gap) - gap), "#" + PANEL)
    d = ImageDraw.Draw(img)
    owners = []
    for slug, k in sorted(D["cpu_procs"].items(), key=lambda kv: -kv[1]):
        owners += [slug] * int(k)
    for i in range(n):
        r, c = divmod(i, cols)
        x, y = c * (cell + gap), r * (cell + gap)
        col = "#" + pcolor(owners[i]) if i < len(owners) else "#1A2130"
        d.rounded_rectangle([x, y, x + cell, y + cell], radius=7, fill=col)
    img.save(path)
    return img.size


def image_grid(D, path):
    """The current best no-three-in-line model: points and still-violated lines (from problems/no-three-in-line-75.json)."""
    art = (D["details"].get("no-three-in-line-75") or {}).get("artifact") or {}
    pts = art.get("points") or []
    if not pts:
        return None
    n = art.get("n") or 75
    S, pad = 1200, 40
    sc = (S - 2 * pad) / (n - 1)
    img = Image.new("RGB", (S, S), "#" + PANEL)
    d = ImageDraw.Draw(img, "RGBA")
    for i in range(n):
        for j in range(n):
            d.point((pad + i * sc, pad + j * sc), fill=(70, 84, 104, 255))
    for ln in art.get("violated_lines") or []:
        try:
            (x1, y1), (x2, y2) = ln[0], ln[1]
        except Exception:  # noqa: BLE001
            continue
        dx, dy = x2 - x1, y2 - y1
        if dx == 0 and dy == 0:
            continue
        ts = []
        for a, da in ((x1, dx), (y1, dy)):
            if da:
                ts += [(0 - a) / da, (n - 1 - a) / da]
        lo = max(min(ts[i:i + 2]) for i in range(0, len(ts), 2))
        hi = min(max(ts[i:i + 2]) for i in range(0, len(ts), 2))
        d.line([(pad + (x1 + lo * dx) * sc, pad + (y1 + lo * dy) * sc), (pad + (x1 + hi * dx) * sc, pad + (y1 + hi * dy) * sc)],
               fill=(255, 92, 108, 105), width=2)
    for x, y in pts:
        cx, cy = pad + x * sc, pad + y * sc
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(61, 245, 255, 60))
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(61, 245, 255, 255))
    img.save(path)
    return art


# ------------------------------------------------------------------ motion: timing + transitions
class Motion:
    """Collects entrance effects for one slide and writes <p:timing>. All effects start by themselves."""

    def __init__(self):
        self.effects = []     # (spid, kind, delay_ms, dur_ms)
        self.videos = []      # (spid, dur_ms)
        self._id = 2

    def nid(self):
        self._id += 1
        return self._id

    def add(self, shape, kind="fade", delay=0, dur=500):
        self.effects.append((shape.shape_id, kind, int(delay), int(dur)))
        return shape

    def stagger(self, shapes, kind="fade", start=0, step=120, dur=450):
        for i, s in enumerate(shapes):
            self.add(s, kind, start + i * step, dur)
        return start + len(shapes) * step

    def video(self, shape, dur_ms):
        self.videos.append((shape.shape_id, int(dur_ms)))

    def _set_visible(self, spid):
        return (f'<p:set><p:cBhvr><p:cTn id="{self.nid()}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
                f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr>'
                f'<p:to><p:strVal val="visible"/></p:to></p:set>')

    def _effect(self, spid, kind, delay, dur):
        tgt = f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>'
        if kind == "appear":
            preset, sub, body = 1, 0, self._set_visible(spid)
        elif kind == "fade":
            preset, sub = 10, 0
            body = self._set_visible(spid) + f'<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{self.nid()}" dur="{dur}"/>{tgt}</p:cBhvr></p:animEffect>'
        elif kind.startswith("wipe"):
            side = kind.split("-")[1] if "-" in kind else "left"
            preset, sub = 22, {"left": 8, "right": 2, "up": 1, "down": 4}[side]
            body = self._set_visible(spid) + f'<p:animEffect transition="in" filter="wipe({side})"><p:cBhvr><p:cTn id="{self.nid()}" dur="{dur}"/>{tgt}</p:cBhvr></p:animEffect>'
        elif kind == "zoom":
            preset, sub = 53, 16
            body = self._set_visible(spid)
            for attr in ("ppt_w", "ppt_h"):
                body += (f'<p:anim calcmode="lin" valueType="num"><p:cBhvr><p:cTn id="{self.nid()}" dur="{dur}" fill="hold"/>{tgt}'
                         f'<p:attrNameLst><p:attrName>{attr}</p:attrName></p:attrNameLst></p:cBhvr><p:tavLst>'
                         f'<p:tav tm="0"><p:val><p:fltVal val="0"/></p:val></p:tav><p:tav tm="100000"><p:val><p:strVal val="#{attr}"/></p:val></p:tav>'
                         f'</p:tavLst></p:anim>')
            body += f'<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{self.nid()}" dur="{dur}"/>{tgt}</p:cBhvr></p:animEffect>'
        else:
            raise ValueError(kind)
        return (f'<p:par><p:cTn id="{self.nid()}" presetID="{preset}" presetClass="entr" presetSubtype="{sub}" fill="hold" nodeType="withEffect">'
                f'<p:stCondLst><p:cond delay="{delay}"/></p:stCondLst><p:childTnLst>{body}</p:childTnLst></p:cTn></p:par>')

    def _media_call(self, spid, dur):
        return (f'<p:par><p:cTn id="{self.nid()}" presetID="1" presetClass="mediacall" presetSubtype="0" fill="hold" nodeType="withEffect">'
                f'<p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst><p:cmd type="call" cmd="playFrom(0.0)"><p:cBhvr>'
                f'<p:cTn id="{self.nid()}" dur="{dur}" fill="hold"/><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:cmd>'
                f'</p:childTnLst></p:cTn></p:par>')

    def xml(self):
        if not self.effects and not self.videos:
            return None
        inner = "".join(self._media_call(s, d) for s, d in self.videos)
        inner += "".join(self._effect(*e) for e in self.effects)
        seq = (f'<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
               f'<p:par><p:cTn id="{self.nid()}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/>'
               f'<p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond></p:stCondLst><p:childTnLst>'
               f'<p:par><p:cTn id="{self.nid()}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>{inner}</p:childTnLst></p:cTn></p:par>'
               f'</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn>'
               f'<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
               f'<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>')
        vids = "".join(
            f'<p:video><p:cMediaNode vol="0" mute="1"><p:cTn id="{self.nid()}" repeatCount="indefinite" fill="hold" display="0">'
            f'<p:stCondLst><p:cond delay="indefinite"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="{s}"/></p:tgtEl></p:cMediaNode></p:video>'
            for s, _ in self.videos)
        return (f'<p:timing {NSDECL}><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">'
                f'<p:childTnLst>{seq}{vids}</p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>')


TRANSITION = (f'<mc:AlternateContent {NSDECL}>'
              '<mc:Choice Requires="p159"><p:transition spd="slow" p14:dur="1400"><p159:morph option="byObject"/></p:transition></mc:Choice>'
              '<mc:Fallback><p:transition spd="med"><p:fade/></p:transition></mc:Fallback>'
              '</mc:AlternateContent>')


def finish_slide(slide, motion):
    """Insert transition + timing in schema order: cSld, clrMapOvr, transition, timing, extLst."""
    sld = slide._element
    for tag in ("timing", "transition"):
        for el in sld.findall(f"{{{NS_P}}}{tag}"):
            sld.remove(el)
    for el in sld.findall("{http://schemas.openxmlformats.org/markup-compatibility/2006}AlternateContent"):
        sld.remove(el)
    anchor = sld.find(f"{{{NS_P}}}clrMapOvr")
    if anchor is None:
        anchor = sld.find(f"{{{NS_P}}}cSld")
    tr = parse_xml(TRANSITION)
    anchor.addnext(tr)
    tx = motion.xml()
    if tx:
        tr.addnext(parse_xml(tx))


def counter(slide, motion, x, y, w, h, value, formatter=fmt, size=34, color=WHITE, fill=PANEL, start=0, align="l", frames=7, step=85):
    """Number build-up. Frames are opaque and stacked, so the last (real) value is what any static export shows."""
    try:
        v = float(value)
    except Exception:  # noqa: BLE001
        v = None
    seq = []
    if v is not None and v != 0:
        is_int = abs(v - round(v)) < 1e-9
        for i in range(1, frames):
            t = 1 - (1 - i / frames) ** 2.2
            seq.append(formatter(int(round(v * t)) if is_int else v * t))
    seq.append(formatter(value) if v is not None else str(value))
    out = []
    for i, s in enumerate(seq):
        tb = text(slide, x, y, w, h, s, size=size, color=color, font=MONO, bold=True, align=align, anchor="m", fill=fill)
        motion.add(tb, "appear" if i else "fade", start + i * step, 250)
        out.append(tb)
    return start + len(seq) * step


def add_video(slide, motion, mp4, poster, x, y, w, h, name):
    mv = slide.shapes.add_movie(mp4, Inches(x), Inches(y), Inches(w), Inches(h), poster_frame_image=poster, mime_type="video/mp4")
    mv.name = name
    motion.video(mv, video_ms(mp4))
    return mv


# ------------------------------------------------------------------ slide scaffolding
def new_slide(prs, D, idx, total, kicker=None, title=None, black=False, title_w=11.6):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = rgb("000000" if black else BG)
    if not black:      # slides with a boxed black-background video use a plain black slide so the video has no visible edge
        picture(s, os.path.join(BUILD, "backdrop.jpg"), 0, 0, w=W, h=H, name="!!backdrop")
    m = Motion()
    s._ltd = {"idx": idx, "total": total}
    if kicker:
        text(s, 0.6, 0.62, 9, 0.3, kicker.upper(), size=11, color=CYAN, font=MONO, name="kicker")
    if title:
        text(s, 0.6, 0.95, title_w, 1.0, title, size=30, bold=True, color=WHITE, name="title", line_spacing=0.95)
    return s, m


def chrome(s, D):
    """Wordmark, snapshot time and progress bar. Drawn last so it sits above full-bleed media. '!!' names morph."""
    idx, total = s._ltd["idx"], s._ltd["total"]
    text(s, 0.6, 0.28, 5, 0.25, [[("PHOENIXASTAR", {"color": WHITE, "bold": True}), ("  ·  autonomous research lab", {"color": DIM})]],
         size=9, font=MONO, name="!!wordmark")
    text(s, W - 5.6, 0.28, 5, 0.25, [[("● ", {"color": AMBER}), (f"{D['label']} · as of {D['asof']}", {"color": GREY})]],
         size=9, font=MONO, align="r", name="!!asof")
    box(s, 0.6, 7.12, W - 1.2, 0.02, fill=LINE, line=None, shape=MSO_SHAPE.RECTANGLE, name="!!track")
    box(s, 0.6, 7.105, (W - 1.2) * idx / total, 0.05, fill=CYAN, line=None, shape=MSO_SHAPE.RECTANGLE, name="!!progress")
    text(s, W - 2.6, 7.2, 2.0, 0.2, f"{idx:02d} / {total:02d}", size=8, color=DIM, font=MONO, align="r", name="!!page")


def stat_tile(s, m, x, y, w, h, value, label, color=WHITE, start=0, formatter=fmt, size=32, sub=None):
    p = box(s, x, y, w, h)
    m.add(p, "fade", start, 350)
    end = counter(s, m, x + 0.22, y + 0.16, w - 0.44, h * 0.5, value, formatter=formatter, size=size, color=color, start=start + 150)
    lab = [[(label, {"color": GREY})]]
    if sub:
        lab.append([(sub, {"color": DIM, "size": 9})])
    t = text(s, x + 0.22, y + h * 0.5 + 0.2, w - 0.44, h * 0.5 - 0.26, lab, size=11, spacing=2)
    m.add(t, "fade", start + 150, 350)
    return end


# ------------------------------------------------------------------ the ten slides
def build(D, team):
    os.makedirs(BUILD, exist_ok=True)
    make_backdrop(os.path.join(BUILD, "backdrop.jpg"))
    make_fade(os.path.join(BUILD, "fade_top.png"), 8, 256, "down", max_alpha=235, power=1.3)
    make_fade(os.path.join(BUILD, "fade_title.png"), 8, 256, "down", max_alpha=255, power=0.55)
    make_fade(os.path.join(BUILD, "fade_bottom.png"), 8, 256, "up", max_alpha=215, power=1.6)
    make_fade(os.path.join(BUILD, "fade_left.png"), 256, 8, "right", max_alpha=255, power=1.25)

    G = dd.GALLERY
    gal = {os.path.basename(g.get("src", "")): g for g in D["gallery"]}
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    N = 10
    notes = []
    T = D["totals"]
    recs = D["records"]

    # ---------- 1. Title
    s, m = new_slide(prs, D, 1, N)
    orbit = os.path.join(G, "lattice_orbit.mp4")
    hero = os.path.join(G, "hero.jpg") if os.path.exists(os.path.join(G, "hero.jpg")) else os.path.join(G, "hero.png")
    if os.path.exists(orbit):
        add_video(s, m, orbit, poster_from(orbit, hero, os.path.join(BUILD, "poster_orbit.jpg")), 0, 0, W, H, "lattice orbit (video)")
    elif os.path.exists(hero):
        picture(s, hero, 0, 0, w=W, h=H, name="hero")
    picture(s, os.path.join(BUILD, "fade_title.png"), 0, 0, w=W, h=5.2, name="fade-top")
    picture(s, os.path.join(BUILD, "fade_bottom.png"), 0, H - 2.4, w=W, h=2.4, name="fade-bottom")
    k = text(s, 0.6, 0.95, 10, 0.3, "ITERATE AI RESEARCH HACKATHON · SF · TRACK 1: AUTORESEARCH", size=11, color=CYAN, font=MONO)
    t1 = text(s, 0.6, 1.3, 12, 1.1, "Phoenixastar", size=66, bold=True, name="title")
    t2 = text(s, 0.62, 2.55, 11, 0.6, "An AI lab that gets better at discovering mathematics by doing it.", size=24, color=WHITE)
    cap = gal.get("hero.jpg") or gal.get("lattice_orbit.mp4") or {}
    hero_title = (gal.get("hero.jpg") or {}).get("title") or "Live search snapshot"
    c1 = text(s, 0.6, 6.25, 9.5, 0.6,
              [[("LIVE DATA, NOT ART  ", {"color": AMBER, "font": MONO, "size": 9, "bold": True}), (hero_title, {"color": WHITE, "size": 12, "bold": True})],
               [(clip("Our no-three-in-line search on the 75×75 grid: glowing pillars are chosen points, red threads are lines that still hold three. " + (cap.get("made_with") or ""), 190), {"color": GREY, "size": 10})]],
              spacing=3)
    m.add(k, "fade", 200, 500); m.add(t1, "wipe-left", 350, 900); m.add(t2, "fade", 1000, 700); m.add(c1, "fade", 1700, 600)
    chrome(s, D)
    finish_slide(s, m)
    notes.append("This is Phoenixastar. An AI lab that gets better at discovering mathematics by doing it. "
                 f"What you see moving is not art. It is our live search on the no-three-in-line problem, rendered in Blender: {hero_title}.")

    # ---------- 2. The problem
    s, m = new_slide(prs, D, 2, N, "The problem")
    city = os.path.join(G, "hadamard_city.jpg")
    if os.path.exists(city):
        crop_to(city, os.path.join(BUILD, "city_crop.jpg"), 7.2 / 7.5, anchor=(0.62, 0.5), brightness=0.8)
        picture(s, os.path.join(BUILD, "city_crop.jpg"), W - 7.2, 0, w=7.2, h=H, name="hadamard city")
        picture(s, os.path.join(BUILD, "fade_left.png"), W - 7.2, 0, w=4.2, h=H, name="fade-left")
        picture(s, os.path.join(BUILD, "fade_top.png"), W - 7.2, 0, w=7.2, h=1.6, name="fade-top")
    h1 = text(s, 0.6, 1.25, 7.6, 2.3, [[("AI finds math records with search loops ", {}), ("nobody can audit.", {"color": AMBER})]], size=40, bold=True, line_spacing=0.98, name="title")
    h2 = text(s, 0.6, 3.75, 7.0, 0.6, "And a static loop never gets better at searching.", size=22, color=GREY)
    rows = [("OPAQUE", "A score appears. Why that experiment ran is gone."),
            ("STATIC", "Hour 30 searches exactly like hour 1."),
            ("UNCHECKED", "Claims are trusted, not re-verified.")]
    items = []
    for i, (tag, line) in enumerate(rows):
        y = 4.75 + i * 0.52
        items.append(text(s, 0.6, y, 7.4, 0.4, [[(f"{tag:<12}", {"font": MONO, "color": CYAN, "size": 11, "bold": True}), (line, {"color": WHITE, "size": 15})]], anchor="m"))
    capc = text(s, W - 4.6, 6.55, 4.0, 0.4, [[("The record 51×51 ±1 matrix (Hadamard max-det), drawn as a city", {"color": GREY})]], size=9, align="r")
    m.add(h1, "fade", 150, 700); m.add(h2, "fade", 900, 600); m.stagger(items, "wipe-left", 1500, 350, 500); m.add(capc, "fade", 2600, 500)
    chrome(s, D)
    finish_slide(s, m)
    notes.append("Today, AI systems do find new records in mathematics. But they find them with search loops nobody can audit. "
                 "A score appears, and the reason that experiment ran is gone. And the loop is static. Hour thirty searches exactly like hour one. "
                 "We wanted a lab that explains every move, and learns from its own results.")

    # ---------- 3. What we built
    s, m = new_slide(prs, D, 3, N, "What we built", "One lab. One loop. Every step logged.")
    steps = [("telemetry", "8 GPUs · all cores"), ("critic", "official verifier"), ("memory", "past.dev"), ("literature", "Exa search"),
             ("propose", "GPT-6 Astra"), ("referee", "Claude Fable 5.2"), ("plan", "budgets · kills"), ("execute", "Lambda + Modal")]
    cx, cy, rx, ry = 4.0, 4.3, 2.55, 1.9
    ring = box(s, cx - rx, cy - ry, 2 * rx, 2 * ry, fill=None, line="1D4E57", shape=MSO_SHAPE.OVAL, lw=1.5, name="loop ring")
    m.add(ring, "fade", 100, 600)
    mid = text(s, cx - 1.3, cy - 0.55, 2.6, 1.1,
               [[("↻", {"size": 26, "color": CYAN})], [(f"every {D['interval_min']} min", {"size": 15, "bold": True})], [("no human in the loop", {"size": 10, "color": GREY})]],
               align="c", anchor="m", spacing=1)
    m.add(mid, "fade", 300, 600)
    cw, ch = 1.72, 0.6
    for i, (nm, sub) in enumerate(steps):
        a = -math.pi / 2 + i * 2 * math.pi / len(steps)
        x, y = cx + rx * math.cos(a) - cw / 2, cy + ry * math.sin(a) - ch / 2
        hot = nm in ("critic", "referee")
        b = box(s, x, y, cw, ch, fill=PANEL2, line=AMBER if hot else CYAN, radius=0.12, lw=1.0, name=f"step {nm}")
        t = text(s, x, y + 0.07, cw, ch - 0.1, [[(f"{i + 1} ", {"color": DIM, "font": MONO, "size": 9}), (nm, {"bold": True, "size": 13})], [(sub, {"color": AMBER if hot else CYAN, "size": 9, "font": MONO})]],
                 align="c", anchor="m")
        m.add(b, "zoom", 500 + i * 170, 380); m.add(t, "fade", 560 + i * 170, 380)
    px, pw = 7.75, 4.98
    panels = [
        ("COMPUTE", CYAN, f"Lambda box: {len(D['gpus'])}× A100, {D['cpus']} CPU cores", "plus an elastic Modal CPU fleet the planner launches"),
        ("SELF-IMPROVEMENT", AMBER, "Tinker RL: Qwen3-8B learns to write constructions", "Modal sandboxes run AI-written programs · Devin builds new tools"),
        ("AUDIT", WHITE, "Mission control: every decision replayable", "rationale · prediction · sources · verdict · outcome"),
    ]
    for i, (tag, col, l1, l2) in enumerate(panels):
        y = 2.3 + i * 1.5
        b = box(s, px, y, pw, 1.3)
        bar = box(s, px, y + 0.18, 0.05, 0.94, fill=col, line=None, shape=MSO_SHAPE.RECTANGLE)
        t = text(s, px + 0.28, y + 0.17, pw - 0.5, 1.0, [[(tag, {"font": MONO, "size": 10, "color": col, "bold": True})], [(l1, {"size": 15, "bold": True})], [(l2, {"size": 10.5, "color": GREY})]], spacing=4)
        for sh in (b, bar, t):
            m.add(sh, "fade", 2100 + i * 300, 450)
    sp = text(s, 0.6, 6.78, W - 1.2, 0.25, "OpenAI · Tinker · Exa · past.dev · Modal · Devin · Originator   +   Claude Fable 5.2 (referee) · Blender (visuals)", size=9.5, color=DIM, font=MONO, align="c")
    m.add(sp, "fade", 3100, 500)
    chrome(s, D)
    finish_slide(s, m)
    notes.append(f"So we built a lab. Every {D['interval_min']} minutes it runs one loop, with no human in it. It reads telemetry from the cluster. "
                 "A critic re-checks every claimed result with the official verifier. Each problem agent writes what it learned to shared memory. "
                 "Exa searches the literature. GPT-6 Astra proposes experiments, each with a falsifiable prediction. "
                 "Claude Fable referees every proposal. A deterministic planner enforces budgets. Then it executes on Lambda and Modal.")

    # ---------- 4. Live compute
    s, m = new_slide(prs, D, 4, N, "Live", f"{D['cpu_total']} searches live on {len(D['gpus'])} GPUs and {D['cpus']} cores")
    gx, gy, tw, th, gg = 0.6, 2.25, 1.18, 1.0, 0.1
    lab = text(s, gx, gy - 0.32, 5.2, 0.25, f"LAMBDA · {len(D['gpus'])}× A100 · {D['gpu_busy']} busy", size=10, color=GREY, font=MONO)
    m.add(lab, "fade", 100, 400)
    for i, g in enumerate(D["gpus"][:8]):
        r, c = divmod(i, 4)
        x, y = gx + c * (tw + gg), gy + r * (th + gg)
        col = pcolor(g.get("problem")) if g.get("problem") else DIM
        b = box(s, x, y, tw, th, fill=PANEL, line=col, lw=1.0)
        t = text(s, x + 0.12, y + 0.1, tw - 0.24, th - 0.2,
                 [[(f"GPU {g.get('idx', i)}", {"font": MONO, "size": 8.5, "color": GREY})], [(f"{g.get('util', 0)}%", {"font": MONO, "size": 21, "bold": True, "color": col})],
                  [(dd.TINY.get(g.get("problem"), g.get("problem") or "free"), {"size": 9, "color": WHITE})]], spacing=1)
        m.add(b, "zoom", 250 + i * 90, 320); m.add(t, "fade", 300 + i * 90, 320)
    cw_px = image_cpu_grid(D, os.path.join(BUILD, "cpu_grid.png"))
    cy0 = gy + 2 * (th + gg) + 0.45
    lab2 = text(s, gx, cy0 - 0.32, 5.2, 0.25, f"{D['cpus']} CPU CORES · load {fmt(D['load1'], 4)} · {D['cpu_total']} search processes", size=10, color=GREY, font=MONO)
    gw = 4 * tw + 3 * gg
    gp = picture(s, os.path.join(BUILD, "cpu_grid.png"), gx, cy0, w=gw, name="cpu grid")
    m.add(lab2, "fade", 1100, 400); m.add(gp, "wipe-left", 1200, 900)
    ly = cy0 + gw * cw_px[1] / cw_px[0] + 0.18
    lx = gx
    for slug, k in sorted(D["cpu_procs"].items(), key=lambda kv: -kv[1]):
        d_ = box(s, lx, ly + 0.05, 0.12, 0.12, fill=pcolor(slug), line=None, radius=0.03)
        t = text(s, lx + 0.18, ly, 1.3, 0.22, f"{dd.TINY.get(slug, slug)} {k}", size=9, color=GREY, font=MONO)
        m.add(d_, "fade", 2000, 400); m.add(t, "fade", 2000, 400)
        lx += 0.42 + 0.085 * len(f"{dd.TINY.get(slug, slug)} {k}")
    sx, sw, sh, sg = 6.15, 2.1, 1.38, 0.14
    tiles = [(T.get("cycles"), "loop cycles", WHITE), (T.get("decisions"), "decisions logged", CYAN), (T.get("experiments_run"), "experiments run", WHITE),
             (T.get("sandboxes_run"), "Modal sandboxes", WHITE), (T.get("sources"), "Exa sources read", WHITE), (T.get("facts"), "memory facts", WHITE)]
    for i, (v, lb, col) in enumerate(tiles):
        r, c = divmod(i, 3)
        stat_tile(s, m, sx + c * (sw + sg), 1.93 + r * (sh + sg), sw, sh, v, lb, color=col, start=700 + i * 220)
    my = 1.93 + 2 * (sh + sg)
    mb = box(s, sx, my, 3 * sw + 2 * sg, 1.3)
    fleet = D["modal"]
    if fleet and (fleet.get("containers") or fleet.get("launches")):
        l1 = f"{fmt(fleet.get('containers') or fleet.get('launches'))} Modal containers launched by the planner"
        l2 = "Elastic CPU fleet: same search scripts, same telemetry parser, same verifier."
    else:
        l1 = f"{fmt(D['n_sandboxes'])} Modal sandboxes run so far"
        l2 = "Elastic CPU fleet: the planner launches Modal containers when the box is full. None recorded in this snapshot."
    mt = text(s, sx + 0.28, my + 0.18, 3 * sw + 2 * sg - 0.5, 1.0, [[("MODAL · ELASTIC FLEET", {"font": MONO, "size": 10, "color": CYAN, "bold": True})], [(l1, {"size": 15, "bold": True})], [(l2, {"size": 10.5, "color": GREY})]], spacing=4)
    m.add(mb, "fade", 2300, 450); m.add(mt, "fade", 2400, 450)
    chrome(s, D)
    finish_slide(s, m)
    notes.append(f"This is the lab, as of {D['asof_short']}. {len(D['gpus'])} A100s and {D['cpus']} cores, coloured by the problem that owns them. "
                 f"{D['cpu_total']} searches are running on {len(D['active'])} open problems. So far: {fmt(T.get('cycles'))} loop cycles, {fmt(T.get('decisions'))} logged decisions, "
                 f"{fmt(T.get('experiments_run'))} experiments, {fmt(T.get('sandboxes_run'))} Modal sandboxes. The planner decides where every core goes. Not us.")

    # ---------- 5. A real decision
    f = D["featured"]
    s, m = new_slide(prs, D, 5, N, "The loop decides", "A real decision, straight from the log")
    if f:
        cxl, cyt, cwd, cht = 0.6, 1.95, 7.05, 4.85
        card = box(s, cxl, cyt, cwd, cht, line=CYAN, lw=1.0)
        m.add(card, "fade", 100, 500)
        x = cxl + 0.3
        for lbl, col, filled in ((f"#{f.get('id')}", CYAN, True), (f"cycle {f.get('cycle')}", GREY, False), (str(f.get("action")), AMBER, False), (dd.TINY.get(f.get("problem"), f.get("problem") or "lab"), pcolor(f.get("problem")), False)):
            b, w_ = chip(s, x, cyt + 0.28, lbl, col, filled=filled)
            m.add(b, "fade", 300, 400)
            x += w_ + 0.1
        who = text(s, cxl + 0.3, cyt + 0.78, cwd - 0.6, 0.3, [[("PROPOSER  ", {"font": MONO, "size": 10, "color": CYAN, "bold": True}), (f"{f.get('model') or D['proposer_model']} · {short(f.get('problem'))}", {"size": 11, "color": GREY})]])
        rtxt = clip(f.get("rationale"), 430)
        rat = text(s, cxl + 0.3, cyt + 1.2, cwd - 0.6, 2.5, "“" + rtxt + "”", size=17 if len(rtxt) < 330 else 15, color=WHITE, line_spacing=1.08)
        nxt = D["featured_lit"] or D["featured_planner"]
        if nxt:
            nx_ = text(s, cxl + 0.3, cyt + 3.72, cwd - 0.6, 0.55, [[(f"THEN · #{nxt.get('id')} {nxt.get('agent')}  ", {"font": MONO, "size": 9.5, "color": CYAN, "bold": True}), (clip(nxt.get("rationale"), 120), {"size": 11, "color": GREY})]])
            m.add(nx_, "fade", 1500, 400)
        meta = []
        if f.get("tokens"):
            meta.append(f"{fmt(f['tokens'])} tokens")
        if f.get("latency_ms"):
            meta.append(f"{f['latency_ms'] / 1000:.1f} s")
        q = (f.get("params") or {}).get("queries")
        if q:
            meta.append(f"{len(q)} Exa queries")
        mt = text(s, cxl + 0.3, cyt + cht - 0.5, cwd - 0.6, 0.3, "  ·  ".join(meta + [dd.pt_label(f.get("time"))]), size=9.5, color=DIM, font=MONO)
        m.add(who, "fade", 450, 400); m.add(rat, "wipe-left", 600, 1100); m.add(mt, "fade", 1500, 400)

        rx0, rw, rh, rg = 7.95, 4.78, 1.5, 0.175
        # a) prediction
        pc = D["pred_card"]
        if pc:
            pd_, sc = pc["d"], pc["score"]
            pr = pd_.get("prediction") or {}
            out = (sc or pd_).get("outcome") or {}
            verdict = out.get("verdict") or "pending"
            vcol = {"confirmed": GREEN, "refuted": RED}.get(verdict, GREY)
            same = pd_.get("id") == f.get("id")
            head = "PREDICTION" + ("" if same else f" · decision #{pd_.get('id')} ({dd.TINY.get(pd_.get('problem'), '')})")
            l1 = [(f"{pr.get('metric')} → {fmt(pr.get('expected'))}", {"font": MONO, "size": 15, "bold": True}), (f"  within {pr.get('horizon_min')} min", {"size": 11, "color": GREY})]
            l2 = [("critic: ", {"size": 11, "color": GREY}), (verdict.upper(), {"font": MONO, "size": 11, "bold": True, "color": vcol})]
            if out.get("observed") is not None:
                l2.append((f"  observed {fmt(out.get('observed'))}", {"font": MONO, "size": 11, "color": WHITE}))
        else:
            head, l1, l2 = "PREDICTION", [("no prediction in this snapshot", {"size": 13, "color": GREY})], [("", {})]
        # b) exa
        srcs = f.get("sources") or []
        lit = D["featured_lit"]
        if srcs:
            s0 = srcs[0]
            dom = (s0.get("url") or "").split("//")[-1].split("/")[0]
            e1 = [(clip(s0.get("title"), 46), {"size": 13, "bold": True})]
            e2 = [(dom + (f" · {str(s0.get('published'))[:10]}" if s0.get("published") else ""), {"font": MONO, "size": 10, "color": CYAN}),
                  (f"   + {len(srcs) - 1} more cited" if len(srcs) > 1 else "", {"size": 10, "color": GREY})]
            if lit:
                e2.append((f" · search stored {len(lit.get('sources') or [])}", {"size": 10, "color": GREY}))
        else:
            e1 = [(f"{fmt(D['n_sources'])} sources read, {fmt(D['n_cited'])} cited in decisions", {"size": 13, "bold": True})]
            e2 = [("this decision cites none", {"size": 10, "color": GREY})]
        # c) referee
        rf = D["featured_referee"]
        if rf:
            v = (rf.get("verdict") or "").lower()
            vcol2 = {"approve": GREEN, "veto": RED, "amend": AMBER}.get(dd._norm_verdict(v), GREY)
            r1 = [(v.upper(), {"font": MONO, "size": 15, "bold": True, "color": vcol2})]
            r2 = [(clip(rf.get("reason"), 150), {"size": 10.5, "color": WHITE})]
        else:
            pl = D["featured_planner"]
            r1 = [("no referee verdict recorded for this decision", {"size": 12, "color": GREY})]
            r2 = [(clip("Planner: " + pl.get("rationale"), 140) if pl else "Referee abstains on failure; the planner's hard limits still apply.", {"size": 10.5, "color": GREY})]
        blocks = [(head, AMBER, [l1, l2]), ("EXA SOURCE", CYAN, [e1, e2]), ("REFEREE · CLAUDE FABLE 5.2", WHITE, [r1, r2])]
        for i, (hd, col, lines) in enumerate(blocks):
            y = cyt + i * (rh + rg)
            b = box(s, rx0, y, rw, rh)
            bar = box(s, rx0, y + 0.2, 0.05, rh - 0.4, fill=col, line=None, shape=MSO_SHAPE.RECTANGLE)
            t = text(s, rx0 + 0.28, y + 0.2, rw - 0.5, rh - 0.3, [[(hd, {"font": MONO, "size": 9.5, "color": col, "bold": True})]] + lines, spacing=5)
            for sh_ in (b, bar, t):
                m.add(sh_, "fade", 1700 + i * 450, 450)
        notes.append(f"Here is one real decision, number {f.get('id')}, from cycle {f.get('cycle')}. The proposer explains itself in plain English. "
                     + ("It cites papers it found through Exa. " if srcs else "")
                     + "Every proposal carries a prediction with a deadline, and the critic scores it later. "
                     + (f"The referee's verdict was: {rf.get('verdict')}. " if rf else "A second model, Claude Fable, referees proposals before any compute moves. ")
                     + "Nothing runs without a reason on the record.")
    else:
        text(s, 0.6, 3.0, 12, 1, "No proposer decision in this snapshot yet.", size=24, color=GREY)
        notes.append("Every decision is a card: rationale, prediction, sources, referee verdict, outcome.")
    chrome(s, D)
    finish_slide(s, m)

    # ---------- 6. Results
    if recs:
        ttl = "New record: " + ", ".join(short(p["slug"]) for p in recs)
    else:
        ttl = "No record beaten yet. Here is the honest distance."
    s, m = new_slide(prs, D, 6, N, "Results", ttl)
    art = image_grid(D, os.path.join(BUILD, "grid.png"))
    tx0, tw_ = 0.6, (8.55 if art else W - 1.2)
    cols = [("PROBLEM", 0.0, 2.95), ("RECORD", 2.95, 1.85), ("OURS, VERIFIED", 4.8, 1.45), ("LIVE SEARCH SIGNAL", 6.25, 2.3)]
    if not art:
        cols = [("PROBLEM", 0.0, 4.0), ("RECORD", 4.0, 2.9), ("OURS, VERIFIED", 6.9, 2.2), ("LIVE SEARCH SIGNAL", 9.1, 3.0)]
    ty = 2.05
    hdr = [text(s, tx0 + cx_ + 0.15, ty, cw_, 0.25, nm, size=9, color=DIM, font=MONO) for nm, cx_, cw_ in cols]
    m.stagger(hdr, "fade", 100, 0, 400)
    probs = D["problems"][:7]
    rh_ = min(0.6, 4.2 / max(1, len(probs)))
    for i, p in enumerate(probs):
        y = ty + 0.33 + i * rh_
        win = p.get("beats_record")
        rowb = box(s, tx0, y, tw_, rh_ - 0.07, fill=PANEL, line=AMBER if win else LINE, lw=1.25 if win else 0.5)
        st = p.get("status") or ""
        scol = {"record": AMBER, "searching": CYAN, "stalled": GREY, "proved-negative": "B18CFF", "idle": DIM}.get(st, GREY)
        dot = box(s, tx0 + 0.15, y + (rh_ - 0.07) / 2 - 0.06, 0.12, 0.12, fill=pcolor(p["slug"]), line=None, radius=0.06)
        c0 = text(s, tx0 + cols[0][1] + 0.38, y, cols[0][2] - 0.4, rh_ - 0.07, [[(short(p["slug"]), {"size": 12.5, "bold": True})], [(st, {"font": MONO, "size": 8.5, "color": scol})]], anchor="m")
        rec = p.get("record") or {}
        c1 = text(s, tx0 + cols[1][1] + 0.15, y, cols[1][2] - 0.15, rh_ - 0.07, [[(fmt(rec.get("score")), {"font": MONO, "size": 13, "color": AMBER, "bold": True})], [(clip(str(rec.get("holder") or ""), 22), {"size": 8.5, "color": DIM})]], anchor="m")
        ours = p.get("ours")
        if ours and ours.get("score") is not None:
            c2c = [[(fmt(ours["score"]), {"font": MONO, "size": 13, "color": AMBER if win else WHITE, "bold": True})], [("official verifier ✓" if ours.get("verified") else "unverified", {"size": 8.5, "color": GREEN if ours.get("verified") else RED})]]
        else:
            c2c = [[("–", {"font": MONO, "size": 13, "color": DIM})], [("no valid solution yet" if st not in ("idle",) else "not attacked", {"size": 8.5, "color": DIM})]]
        c2 = text(s, tx0 + cols[2][1] + 0.15, y, cols[2][2] - 0.15, rh_ - 0.07, c2c, anchor="m")
        mt_ = p.get("metric") or {}
        if p.get("known_negative"):
            c3c = [[("proved: no extension", {"size": 11, "color": "B18CFF", "bold": True})], [("exact search, negative result", {"size": 8.5, "color": DIM})]]
        elif mt_.get("value") is not None:
            tgt = mt_.get("target")
            c3c = [[(fmt(mt_["value"]), {"font": MONO, "size": 13, "color": CYAN, "bold": True}), (f"  → {fmt(tgt)}" if tgt is not None else "", {"font": MONO, "size": 10.5, "color": GREY})],
                   [(dd.METRIC_LABEL.get(mt_.get("name"), mt_.get("name") or "") + (" · at record, not past" if tgt is not None and not win and abs(float(mt_["value"]) - float(rec.get("score") or 0)) < 1e-9 else ""), {"size": 8.5, "color": DIM})]]
        else:
            c3c = [[("–", {"font": MONO, "size": 13, "color": DIM})], [("", {})]]
        c3 = text(s, tx0 + cols[3][1] + 0.15, y, cols[3][2] - 0.15, rh_ - 0.07, c3c, anchor="m")
        for sh_ in (rowb, dot, c0, c1, c2, c3):
            m.add(sh_, "wipe-left" if sh_ is rowb else "fade", 350 + i * 200, 420)
    fn = text(s, tx0, ty + 0.33 + len(probs) * rh_ + 0.03, tw_, 0.4,
              "“Ours, verified” = scored by the official EinsteinArena verifier. “Live search signal” is progress inside a running search (some searches start from the record), not a claim.",
              size=8.5, color=DIM)
    m.add(fn, "fade", 350 + len(probs) * 200, 400)
    if art:
        gx0, gs = 9.4, 3.23
        gb = box(s, gx0 - 0.1, ty - 0.02, gs + 0.2, gs + 1.37, line=CYAN if not recs else LINE)
        gp = picture(s, os.path.join(BUILD, "grid.png"), gx0, ty + 0.08, w=gs, h=gs, name="no-three grid")
        nv = len(art.get("violated_lines") or [])
        endc = counter(s, m, gx0 + 0.1, ty + gs + 0.2, 1.25, 0.6, nv, size=30, color=RED if nv else GREEN, start=1500)
        gt = text(s, gx0 + 1.35, ty + gs + 0.2, gs - 1.4, 0.6, [[("lines still hold 3 points", {"size": 11, "bold": True})], [(f"{art.get('count')} points placed · 0 = solved", {"size": 9, "color": GREY})]], anchor="m")
        gt2 = text(s, gx0 + 0.1, ty + gs + 0.85, gs - 0.1, 0.4, f"No-three-in-line 75×75, SAT model {art.get('sym', '')}, round {art.get('round', '')}. Not yet valid.", size=8.5, color=DIM)
        m.add(gb, "fade", 1100, 500); m.add(gp, "zoom", 1200, 700); m.add(gt, "fade", 1500, 400); m.add(gt2, "fade", endc, 400)
    chrome(s, D)
    finish_slide(s, m)
    nt = (D["details"].get("no-three-in-line-75") or {}).get("artifact") or {}
    if recs:
        p = recs[0]
        notes.append(f"And it worked. On {short(p['slug'])} the lab found {fmt((p.get('ours') or {}).get('score'))}. The record was {fmt(p['record']['score'])}, held by {p['record']['holder']}. "
                     "The official verifier confirmed it. The log shows every decision that led there.")
    else:
        vs = [p for p in D["problems"] if (p.get("ours") or {}).get("verified")]
        notes.append("Results, honestly. We have not beaten a record yet. "
                     + (f"Our closest search is no-three-in-line: {nt.get('count')} points on the grid, {len(nt.get('violated_lines') or [])} lines still to remove. Zero means a solved open case. " if nt else "")
                     + (f"We hold verified solutions on {len(vs)} problems, below the record. " if vs else "")
                     + (f"And one proved negative result on {short(D['negatives'][0]['slug'])}. " if D["negatives"] else "")
                     + "Every number here went through the official verifier, or is labelled as a live signal.")

    # ---------- 7. Self-improvement
    ev = D["eval"] or {}
    g0, gN = ev.get("gen0") or {}, ev.get("genN") or {}
    s, m = new_slide(prs, D, 7, N, "It improves itself", "The model learns to write better constructions")
    chart_learning(D, os.path.join(BUILD, "learning.png"))
    cb = box(s, 0.6, 1.95, 7.9, 4.85)
    ct = text(s, 0.85, 2.1, 7.4, 0.3, [[("TINKER RL  ", {"font": MONO, "size": 10, "color": CYAN, "bold": True}),
                                         (f"{D['base_model']} LoRA · {len(D['steps'])} steps" + (f" · {D['learn_minutes']} min" if D["learn_minutes"] else "") + f" · problem: {short(D['learn_problem'])}", {"size": 10.5, "color": GREY})]])
    cp = picture(s, os.path.join(BUILD, "learning.png"), 0.75, 2.5, w=7.6, name="reward curve")
    m.add(cb, "fade", 100, 400); m.add(ct, "fade", 250, 400); m.add(cp, "wipe-left", 500, 1800)
    rx0, rw = 8.75, 3.98
    hd = text(s, rx0, 1.95, rw, 0.3, "HELD-OUT PROMPTS · GEN 0 → GEN N", size=10, color=GREY, font=MONO)
    m.add(hd, "fade", 1500, 400)

    def duo(y, label, a, b, formatter, start):
        bx = box(s, rx0, y, rw, 1.35)
        m.add(bx, "fade", start, 350)
        t0 = text(s, rx0 + 0.25, y + 0.2, 1.1, 0.62, formatter(a), size=24, color=DIM, font=MONO, bold=True, anchor="m")
        ar = text(s, rx0 + 1.35, y + 0.2, 0.5, 0.62, "→", size=22, color=GREY, anchor="m", align="c")
        m.add(t0, "fade", start + 100, 350); m.add(ar, "fade", start + 250, 350)
        counter(s, m, rx0 + 1.9, y + 0.2, 1.9, 0.62, b, formatter=formatter, size=30, color=CYAN, start=start + 400)
        lb = text(s, rx0 + 0.25, y + 0.92, rw - 0.5, 0.3, label, size=10.5, color=GREY)
        m.add(lb, "fade", start + 100, 350)

    duo(2.3, "valid constructions (official verifier)", g0.get("valid_rate"), gN.get("valid_rate"), lambda v: pct(v), 1700)
    duo(3.8, "mean reward per sample", g0.get("score"), gN.get("score"), lambda v: "–" if v is None else f"{float(v):.2f}", 2300)
    tr = ev.get("train") or {}
    lp = next((p for p in D["problems"] if p["slug"] == D["learn_problem"]), None)
    br = gN.get("best_ratio") or (tr.get("genN") or {}).get("best_ratio")
    lines = []
    if tr:
        lines.append([(f"On training prompts: valid {pct((tr.get('gen0') or {}).get('valid_rate'))} → {pct((tr.get('genN') or {}).get('valid_rate'))}", {"size": 10.5, "color": WHITE})])
    if br is not None and lp:
        beat = (D["learning"].get("best") or {}).get("beats_record")
        lines.append([(f"Best held-out ratio {fmt(br, 3)} vs record {fmt(lp['record']['score'], 3)}. " + ("New record." if beat else "Not a record: the claim is the curve."), {"size": 10.5, "color": AMBER if beat else GREY})])
    hb = box(s, rx0, 5.3, rw, 1.5, fill=PANEL2)
    ht = text(s, rx0 + 0.25, 5.47, rw - 0.5, 1.2, [[("HONEST READ", {"font": MONO, "size": 9.5, "color": AMBER, "bold": True})]] + lines, spacing=5)
    m.add(hb, "fade", 3000, 400); m.add(ht, "fade", 3100, 400)
    chrome(s, D)
    finish_slide(s, m)
    notes.append(f"This is the part that learns. With Tinker we fine-tune an open model, {D['base_model'].split('/')[-1]}, with reinforcement learning. The reward is the official verifier. "
                 f"At the start, {pct(g0.get('valid_rate'))} of its constructions were valid on held-out prompts. After {len(D['steps'])} steps"
                 + (f", about {round(D['learn_minutes'])} minutes" if D["learn_minutes"] else "") + f", {pct(gN.get('valid_rate'))} are. "
                 + ("It has not beaten the record. What we claim is the curve: the lab gets better at the task by doing it." if not (D["learning"].get("best") or {}).get("beats_record") else "And it produced a record-beating construction."))

    # ---------- 8. Memory and tools
    s, m = new_slide(prs, D, 8, N, "Memory and tools", "Agents share what they learn, and build their own tools")
    cw3, cg3, y0, h3 = 3.93, 0.17, 1.95, 4.85
    # past.dev
    x = 0.6
    b = box(s, x, y0, cw3 * 1.28, h3)
    hd = text(s, x + 0.25, y0 + 0.2, cw3 * 1.28 - 0.5, 0.25, "PAST.DEV · SHARED MEMORY", size=10, color=CYAN, font=MONO, bold=True)
    m.add(b, "fade", 100, 400); m.add(hd, "fade", 200, 400)
    counter(s, m, x + 0.25, y0 + 0.55, 1.0, 0.6, D["n_facts"], size=30, color=WHITE, start=350)
    t = text(s, x + 1.3, y0 + 0.55, 3.5, 0.6, [[(f"facts written by {D['n_agents']} agents", {"size": 12, "bold": True})], [(f"{fmt(D['cross_reads'])} reads of a fact another agent wrote", {"size": 10, "color": GREY})]], anchor="m")
    m.add(t, "fade", 450, 400)
    if D["bench_systems"]:
        chart_bench(D, os.path.join(BUILD, "bench.png"))
        bp = picture(s, os.path.join(BUILD, "bench.png"), x + 0.15, y0 + 1.4, w=cw3 * 1.28 - 0.3, name="memory benchmark")
        m.add(bp, "wipe-down", 800, 900)
        bt = text(s, x + 0.25, y0 + 3.55, cw3 * 1.28 - 0.5, 1.15, [[("MEASURED, NOT CLAIMED  ", {"font": MONO, "size": 9, "color": AMBER, "bold": True})], [(dd.bench_sentence(D), {"size": 10.5, "color": WHITE})]], spacing=4)
        m.add(bt, "fade", 1500, 500)
    else:
        bt = text(s, x + 0.25, y0 + 1.6, cw3 * 1.28 - 0.5, 1.0, "Benchmark vs markdown and RAG: not run in this snapshot.", size=12, color=GREY)
        m.add(bt, "fade", 800, 500)
    # Modal sandboxes
    x2 = x + cw3 * 1.28 + cg3
    w2 = (W - 0.6 - x2 - cg3) / 2
    b = box(s, x2, y0, w2, h3)
    hd = text(s, x2 + 0.25, y0 + 0.2, w2 - 0.5, 0.25, "MODAL · SANDBOXES", size=10, color=CYAN, font=MONO, bold=True)
    m.add(b, "fade", 1300, 400); m.add(hd, "fade", 1400, 400)
    counter(s, m, x2 + 0.25, y0 + 0.55, w2 - 0.5, 0.75, D["n_sandboxes"], size=44, color=WHITE, start=1550)
    sb_lines = [[("AI-written search programs, run in parallel", {"size": 12, "bold": True})],
                [("no network · no secrets · 120 s", {"size": 10, "color": GREY, "font": MONO})],
                [(f"{fmt(D['sb_ok'])} returned a solution the official verifier accepted", {"size": 10.5, "color": WHITE})],
                [(f"{fmt(D['sb_matched_record'])} matched a record · {fmt(D['sb_beat'])} beat one", {"size": 10.5, "color": AMBER if D['sb_beat'] else GREY})],
                [(f"problems: {', '.join(dd.TINY.get(p, p) for p in D['sb_problems']) or '–'}", {"size": 9.5, "color": DIM, "font": MONO})]]
    t = text(s, x2 + 0.25, y0 + 1.5, w2 - 0.5, 2.0, sb_lines, spacing=7)
    m.add(t, "fade", 1750, 500)
    seen, progs = set(), []
    for sb in D["sandboxes"]:
        key = (sb.get("problem"), sb.get("approach"))
        if sb.get("approach") and sb.get("score") is not None and key not in seen and sb.get("problem") not in {p_[0] for p_ in progs}:
            seen.add(key)
            progs.append((sb.get("problem"), sb.get("approach"), sb.get("score")))
    if progs:
        pl_ = [[("PROGRAMS IT WROTE", {"font": MONO, "size": 9, "color": AMBER, "bold": True})]]
        for pr_, ap_, sc_ in progs[:3]:
            pl_.append([(f"{dd.TINY.get(pr_, pr_)} {fmt(sc_, 4)}  ", {"font": MONO, "size": 9, "color": CYAN}), (clip(ap_, 30), {"size": 9.5, "color": GREY})])
        t = text(s, x2 + 0.25, y0 + 3.55, w2 - 0.5, 1.2, pl_, spacing=4)
        m.add(t, "fade", 2100, 500)
    # Devin
    x3 = x2 + w2 + cg3
    b = box(s, x3, y0, w2, h3)
    hd = text(s, x3 + 0.25, y0 + 0.2, w2 - 0.5, 0.25, "DEVIN · TOOLSMITH", size=10, color=CYAN, font=MONO, bold=True)
    m.add(b, "fade", 2300, 400); m.add(hd, "fade", 2400, 400)
    ts = D["toolsmith"]
    if ts:
        counter(s, m, x3 + 0.25, y0 + 0.55, w2 - 0.5, 0.75, ts.get("adopted") or 0, size=44, color=AMBER if ts.get("adopted") else WHITE, start=2550)
        tl = [[(f"new strategies adopted, of {fmt(ts.get('requested'))} commissioned", {"size": 12, "bold": True})],
              [(f"{fmt(ts.get('rejected'))} rejected by the verifier", {"size": 10.5, "color": GREY})]]
        if ts.get("last"):
            tl.append([(clip(ts["last"]["text"], 150), {"size": 9.5, "color": DIM})])
        t = text(s, x3 + 0.25, y0 + 1.5, w2 - 0.5, 3.1, tl, spacing=9)
    else:
        flow = [("1", "The lab commissions a new search program from Devin"), ("2", "It is tested in a Modal sandbox against the official verifier"), ("3", "Adopted as a strategy only if it passes")]
        tl = [[(n_ + "  ", {"font": MONO, "size": 12, "color": CYAN, "bold": True}), (tx_, {"size": 13, "color": WHITE})] for n_, tx_ in flow]
        tl.append([("No toolsmith session in this snapshot.", {"size": 9.5, "color": DIM})])
        t = text(s, x3 + 0.25, y0 + 0.7, w2 - 0.5, 3.9, tl, spacing=16)
    m.add(t, "fade", 2700, 500)
    chrome(s, D)
    finish_slide(s, m)
    notes.append(f"Agents share memory through past.dev. {fmt(D['n_facts'])} facts so far, and {fmt(D['cross_reads'])} times an agent used a fact that a different agent wrote. "
                 f"We benchmarked it against markdown and RAG. {dd.bench_sentence(D)} "
                 f"On Modal, {fmt(D['n_sandboxes'])} AI-written search programs ran in sandboxes, with no network and no secrets. "
                 "And Devin is our toolsmith. The lab commissions a new search program, tests it in a sandbox against the verifier, and adopts it only if it passes.")

    # ---------- 9. Rigour
    s, m = new_slide(prs, D, 9, N, "Rigour", "Nothing is true until the official verifier says so")
    tw4, tg4 = 2.9, 0.176
    refuted_or_vetoed = D["planner_rejects"] + ((D["referee"] or {}).get("veto", 0))
    tiles = [(D["verifier_checks"], "official verifier runs", "by the critic, never the search itself", CYAN),
             (D["pred_made"], "falsifiable predictions", f"{D['pred_confirmed']} confirmed · {D['pred_refuted']} refuted · {D['pred_pending']} pending", WHITE),
             (refuted_or_vetoed, "proposals blocked", f"{D['planner_rejects']} by the planner" + (f" · {(D['referee'] or {}).get('veto', 0)} referee vetoes" if D["referee"] else ""), AMBER),
             (D["n_decisions"], "decisions, replayable", "rationale · sources · outcome", WHITE)]
    for i, (v, lb, sub, col) in enumerate(tiles):
        stat_tile(s, m, 0.6 + i * (tw4 + tg4), 1.95, tw4, 1.75, v, lb, color=col, start=200 + i * 300, size=38, sub=sub)
    fy = 3.95
    fb = box(s, 0.6, fy, W - 1.2, 2.85)
    fh = text(s, 0.88, fy + 0.22, 8, 0.25, "WHAT FAILED, ON THE RECORD", size=10, color=AMBER, font=MONO, bold=True)
    m.add(fb, "fade", 1500, 400); m.add(fh, "fade", 1600, 400)
    fails = []
    for p in D["negatives"][:1]:
        fails.append((short(p["slug"]), clip("Proved negative: " + (p.get("known_negative") or "exact search found no improvement"), 175)))
    stalled = [p for p in D["problems"] if p.get("status") == "stalled"]
    if stalled:
        fails.append((f"{len(stalled)} searches stalled", "The loop reports them as stalled: " + ", ".join(dd.TINY.get(p["slug"], p["slug"]) for p in stalled) + f". It stopped {D['stops']} runs to free compute."))
    rj = next((d for d in D["decisions"] if d.get("agent") == "planner" and d.get("action") == "reject"), None)
    if rj:
        fails.append((f"decision #{rj.get('id')}", clip(rj.get("rationale"), 150)))
    if D["referee"] and D["referee"].get("veto"):
        vd = next((d for d in D["decisions"] if d.get("agent") == "proposer" and dd._norm_verdict((dd.referee_of(d, D["ref_idx"]) or {}).get("verdict")) == "veto"), None)
        if vd:
            fails.append((f"veto on #{vd.get('id')}", clip(dd.referee_of(vd, D["ref_idx"]).get("reason"), 150)))
    if not recs:
        fails.append(("records beaten", f"{fmt(T.get('records') or 0)} so far. We say so on the results slide."))
    rows_ = []
    for i, (tag, line) in enumerate(fails[:4]):
        rows_.append(text(s, 0.88, fy + 0.65 + i * 0.52, W - 1.76, 0.45, [[(f"{tag}", {"font": MONO, "size": 10.5, "color": CYAN, "bold": True}), ("   " + line, {"size": 11.5, "color": WHITE})]], anchor="m"))
    m.stagger(rows_, "wipe-left", 1800, 350, 500)
    chrome(s, D)
    finish_slide(s, m)
    notes.append(f"On rigour. The search never grades itself. The critic ran the official verifier {fmt(D['verifier_checks'])} times. "
                 f"The proposer made {fmt(D['pred_made'])} falsifiable predictions, and the critic scores each one when its deadline passes. "
                 f"{fmt(refuted_or_vetoed)} proposals were blocked before they used compute. "
                 "And we report what failed: a proved negative result, stalled searches, rejected ideas. All of it is in a log you can replay.")

    # ---------- 10. Close
    s, m = new_slide(prs, D, 10, N, black=True)
    snake = os.path.join(G, "snake_turntable.mp4")
    still = os.path.join(G, "snake.jpg") if os.path.exists(os.path.join(G, "snake.jpg")) else os.path.join(G, "snake.png")
    vw = 7.9
    if os.path.exists(snake):
        add_video(s, m, snake, poster_from(snake, still, os.path.join(BUILD, "poster_snake.jpg")), W - vw, (H - vw * 9 / 16) / 2, vw, vw * 9 / 16, "snake turntable (video)")
    elif os.path.exists(still):
        picture(s, still, W - vw, (H - vw * 9 / 16) / 2, w=vw, name="snake")
    pass
    k = text(s, 0.6, 0.95, 8, 0.3, "WHAT'S NEXT", size=11, color=CYAN, font=MONO)
    h1 = text(s, 0.6, 1.3, 7.2, 2.2, [[("Any domain with an ", {}), ("exact verifier.", {"color": CYAN})]], size=42, bold=True, line_spacing=0.98, name="title")
    nx = text(s, 0.6, 3.3, 6.4, 1.3,
              [[("Already running: physics. ", {"bold": True}), ("16 candidate new three-body orbit families, verified periodic to 1e-8, absent from 2,060 catalogued orbits; EVENT HORIZON: 8 of 9 black-hole-information claims independently verified.", {"color": GREY})],
               [("Same loop. Same log. A different verifier.", {"color": WHITE})]], size=15, spacing=10)
    rb = box(s, 0.6, 4.95, 6.3, 0.62, fill=PANEL, line=CYAN, lw=1.0)
    rt = text(s, 0.82, 4.95, 5.9, 0.62, dd.REPO_URL.replace("https://", ""), size=14, color=CYAN, font=MONO, bold=True, anchor="m")
    for sh_ in (rb, rt):                      # shape-level link keeps the text colour (run-level links take the theme colour)
        sh_.click_action.hyperlink.address = dd.REPO_URL
    tm = text(s, 0.6, 5.8, 7.0, 0.7, [[(team, {"size": 13, "bold": True})], [("OpenAI · Tinker · Exa · past.dev · Modal · Devin · Originator · Claude Fable 5.2 · Blender", {"size": 8.5, "color": DIM, "font": MONO})]], spacing=5)
    sc = gal.get("snake.jpg") or gal.get("snake_turntable.mp4") or {}
    cap = text(s, W - 5.1, 6.55, 4.5, 0.4, clip("The record 2950-edge snake in the 13-cube, projected to 3D. " + (sc.get("made_with") or ""), 120), size=9, color=GREY, align="r")
    m.add(k, "fade", 200, 400); m.add(h1, "wipe-left", 350, 900); m.add(nx, "fade", 1100, 600); m.add(rb, "zoom", 1800, 450); m.add(rt, "fade", 1900, 450); m.add(tm, "fade", 2300, 500); m.add(cap, "fade", 2300, 500)
    chrome(s, D)
    finish_slide(s, m)
    notes.append("Mathematics is where we start, because the verifier is exact. But the loop does not care about the domain. "
                 "Anything with an exact verifier works, and it is already doing physics: sixteen candidate new families of periodic three-body orbits, "
                 "verified and absent from the catalogs we checked, and a black-hole-information study whose own verifier caught and corrected a wrong claim. "
                 "The code, the log and a replay of this run are public. Phoenixastar. Thank you.")

    for sl, n in zip(prs.slides, notes):
        sl.notes_slide.notes_text_frame.text = n
    prs.core_properties.title = "Phoenixastar"
    prs.core_properties.subject = f"Pitch deck, snapshot {D['asof']}"
    prs.core_properties.author = team
    prs.save(OUT)
    return notes


# ------------------------------------------------------------------ validation + preview
def validate(path):
    prs = Presentation(path)
    n = len(prs.slides)
    assert n == 10, f"expected 10 slides, got {n}"
    assert abs(prs.slide_width / prs.slide_height - 16 / 9) < 1e-3, "not 16:9"
    report = {"slides": n, "morph": 0, "timing": 0, "effects": 0, "videos": 0, "notes": 0, "xml_parts": 0, "media": []}
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        for name in z.namelist():
            if name.endswith((".xml", ".rels")):
                root = etree.fromstring(z.read(name))      # raises if not well-formed
                report["xml_parts"] += 1
                if name.startswith("ppt/slides/slide"):
                    kids = [etree.QName(c).localname for c in root]
                    order = [k for k in kids if k in ("cSld", "clrMapOvr", "AlternateContent", "transition", "timing", "extLst")]
                    assert order == sorted(order, key=["cSld", "clrMapOvr", "AlternateContent", "transition", "timing", "extLst"].index), f"{name}: bad child order {kids}"
                    x = z.read(name).decode()
                    report["morph"] += int("p159:morph" in x and "<p:fade" in x)
                    report["timing"] += int("<p:timing" in x)
                    report["effects"] += x.count('presetClass="entr"')
                    report["videos"] += x.count("playFrom(0.0)")
                    ids = [e.get("id") for e in root.iter(f"{{{NS_P}}}cTn")]
                    assert len(ids) == len(set(ids)), f"{name}: duplicate cTn ids"
                    spids = {e.get("id") for e in root.iter(f"{{{NS_P}}}cNvPr")}
                    for e in root.iter(f"{{{NS_P}}}spTgt"):
                        assert e.get("spid") in spids, f"{name}: animation targets missing shape {e.get('spid')}"
            if name.startswith("ppt/media/") and name.endswith(".mp4"):
                report["media"].append(f"{os.path.basename(name)} {z.getinfo(name).file_size // 1024} KB")
    for sl in prs.slides:
        report["notes"] += int(bool(sl.has_notes_slide and sl.notes_slide.notes_text_frame.text.strip()))
    assert report["morph"] == 10, "morph transition missing on some slide"
    assert report["notes"] == 10, "speaker notes missing on some slide"
    report["size_mb"] = round(os.path.getsize(path) / 1e6, 1)
    return report


def preview(path):
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice or not shutil.which("pdftoppm"):
        print("preview skipped: needs soffice and pdftoppm")
        return None
    out = os.path.join(BUILD, "preview")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", out, path], check=True, capture_output=True, timeout=300)
    pdf = os.path.join(out, os.path.splitext(os.path.basename(path))[0] + ".pdf")
    subprocess.run(["pdftoppm", "-r", "80", "-png", pdf, os.path.join(out, "slide")], check=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", action="store_true", help="render each slide to PNG (LibreOffice + pdftoppm)")
    ap.add_argument("--team", default=None, help="team line for the last slide (default: deck/team.txt, else a neutral line)")
    a = ap.parse_args()
    team = a.team
    tfile = os.path.join(HERE, "team.txt")
    if not team and os.path.exists(tfile):
        team = open(tfile).read().strip()
    team = team or "Team Phoenixastar"
    D = dd.load()
    notes = build(D, team)
    rep = validate(OUT)
    import storyboard_gen
    storyboard_gen.write(D, notes, os.path.join(HERE, "storyboard.md"))
    print(f"built {OUT}")
    print(f"snapshot: {D['asof']} ({D['label']})")
    print("validation:", rep)
    if a.preview:
        print("preview:", preview(OUT))


if __name__ == "__main__":
    main()
