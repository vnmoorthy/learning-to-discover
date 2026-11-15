"""Phoenixastar banner from REAL run data only (no generated art).

Layers: the live no-three-in-line SAT model (75x75 lattice, chosen points, still-violated lines) as a faint field, and
the 7 verified three-body candidate orbits re-integrated from their initial conditions (DOP853, rtol 1e-12) as the
hero. Text: wordmark, one-line claim, live numbers from the snapshot.

  python3 viz/make_banner.py            -> docs/assets/banner.png (2400x900) and docs/assets/social-preview.png (1280x640)
"""
import json, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from scipy.integrate import solve_ivp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BG, FG, MUTED, ACC, WARM, ROSE = "#0A0C0F", "#EEF2F6", "#8A94A3", "#4FD1E0", "#E8B65C", "#E06C9F"


def font(names, size, weight="regular"):
    for n in names:
        try:
            font_manager.findfont(n, fallback_to_default=False)
            return {"family": n, "size": size, "weight": weight}
        except Exception:
            continue
    return {"family": "DejaVu Sans", "size": size, "weight": weight}


def orbit(o, n=7000):
    m3 = o.get("m3", 1.0); vx, vy, T = o["vx"], o["vy"], o["T"]
    y0 = [-1, 0, 1, 0, 0, 0, vx, vy, vx, vy, -2 * vx / m3, -2 * vy / m3]
    m = (1.0, 1.0, m3)

    def f(t, y):
        r = np.asarray(y[:6]).reshape(3, 2); a = np.zeros((3, 2))
        for i in range(3):
            for j in range(3):
                if i != j:
                    d = r[j] - r[i]; a[i] += m[j] * d / (d @ d) ** 1.5
        return np.concatenate([y[6:], a.ravel()])
    s = solve_ivp(f, (0, T), y0, method="DOP853", rtol=1e-12, atol=1e-12, t_eval=np.linspace(0, T, n))
    return s.y[:6].T.reshape(-1, 3, 2)


def stats():
    try:
        s = json.load(open(os.path.join(ROOT, "web", "public", "data", "state.json")))
        t = s.get("totals", {})
        return t.get("decisions"), t.get("cycles"), t.get("experiments_run")
    except Exception:
        return None, None, None


def draw(w, h, out, compact=False):
    dpi = 200
    fig = plt.figure(figsize=(w / dpi, h / dpi), dpi=dpi, facecolor=BG)
    # background field: the live lattice model
    ax0 = fig.add_axes([0, 0, 1, 1]); ax0.set_facecolor(BG); ax0.axis("off")
    try:
        nt = json.load(open(os.path.join(ROOT, "web", "public", "data", "problems", "no-three-in-line-75.json")))
        art = nt.get("artifact") or {}
        pts = np.array(art.get("points") or [])
        n = art.get("n", 75)
        aspect = w / h
        X, Y = np.meshgrid(np.arange(n), np.arange(n))
        sx = lambda x: 0.36 + 0.64 * (x / (n - 1))        # lattice spans the right part
        sy = lambda y: 0.04 + 0.92 * (y / (n - 1))
        ax0.set_xlim(0, 1); ax0.set_ylim(0, 1)
        ax0.scatter(sx(X.ravel()), sy(Y.ravel()), s=0.6 if not compact else 0.35, c="#1B2129", lw=0)
        for a, b, *_ in (art.get("violated_lines") or [])[:160]:
            ax0.plot([sx(a[0]), sx(b[0])], [sy(a[1]), sy(b[1])], color=ROSE, lw=0.35, alpha=0.18)
        if len(pts):
            ax0.scatter(sx(pts[:, 0]), sy(pts[:, 1]), s=2.2 if not compact else 1.4, c="#2E6F78", lw=0, alpha=0.9)
    except Exception as e:
        print("lattice layer skipped:", e)
    # hero: the 7 candidate orbits, small multiples on the right
    orbs = json.load(open(os.path.join(ROOT, "problems", "three-body-periodic-orbits", "candidates_verified.json")))["orbits"]
    cols = [ACC, WARM, ROSE]
    pick = [1, 5, 6] if compact else [1, 5, 6, 2, 0]
    xs = np.linspace(0.47, 0.90, len(pick))
    size = 0.30 if compact else 0.27
    for k, (i, cx) in enumerate(zip(pick, xs)):
        tr = orbit(orbs[i])
        a = fig.add_axes([cx - size * h / w / 2 * (w / h) * 0.5, 0.5 - size / 2 - (0.06 if k % 2 else -0.04), size * h / w * (w / h) * 0.5, size])
        a.set_facecolor("none"); a.axis("off"); a.set_aspect("equal")
        for b in range(3):
            for lw, al in ((3.2, 0.06), (1.6, 0.14), (0.55, 0.95)):
                a.plot(tr[:, b, 0], tr[:, b, 1], color=cols[b], lw=lw * (0.8 if compact else 1), alpha=al, solid_capstyle="round")
    # text
    tf = font(["Avenir Next", "Helvetica Neue", "Inter"], 64 if not compact else 46, "bold")
    sf = font(["Avenir Next", "Helvetica Neue", "Inter"], 19 if not compact else 15)
    mf = font(["Menlo", "SF Mono", "DejaVu Sans Mono"], 12 if not compact else 10)
    x0 = 0.055
    fig.text(x0, 0.70, "AUTONOMOUS RESEARCH LAB", color=ACC, fontdict=font(["Menlo", "SF Mono"], 11 if not compact else 9), alpha=0.95)
    fig.text(x0, 0.52, "Phoenixastar", color=FG, fontdict=tf)
    fig.text(x0, 0.415, "An AI lab that gets better at discovering\nmathematics by doing it. Every claim verified.", color="#C9D1DC",
             fontdict=sf, linespacing=1.35, va="top")
    d, c, e = stats()
    line = "8x A100  ·  Modal fleet  ·  GPT-6 Astra + Claude Fable 5.2"
    if d:
        line2 = f"{d:,} logged decisions  ·  {c} cycles  ·  {e:,} experiments"
        fig.text(x0, 0.17 if not compact else 0.15, line2, color=MUTED, fontdict=mf)
    fig.text(x0, 0.11 if not compact else 0.09, line, color=MUTED, fontdict=mf)
    fig.text(0.985, 0.03, "real data: live 75x75 SAT model  ·  verified three-body candidate orbits", color="#5B6472",
             fontdict=font(["Menlo"], 8 if not compact else 7), ha="right")
    fig.savefig(out, dpi=dpi, facecolor=BG)
    plt.close(fig)
    print("wrote", out)


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "docs", "assets"), exist_ok=True)
    draw(2400, 900, os.path.join(ROOT, "docs", "assets", "banner.png"))
    draw(1280, 640, os.path.join(ROOT, "docs", "assets", "social-preview.png"), compact=True)
