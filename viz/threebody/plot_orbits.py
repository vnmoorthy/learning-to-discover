"""Plot verified periodic three-body orbits (output of search/threebody_gpu.py) with matplotlib.

  python3 viz/threebody/plot_orbits.py runs/threebody/orbits_<id>.json --out viz/threebody/out [--top 6]

Writes one PNG per selected orbit and a contact sheet of all families. Trajectories are re-integrated here from the
stored initial conditions (scipy DOP853, rtol 1e-12), so a plot is the actual solution, not a sketch.
Palette: background #07080B, body 1 cyan #3DF5FF, body 2 amber #FFB547, body 3 magenta #FF4FA3.
"""
import argparse, json, math, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

BG, C1, C2, C3, FG = "#07080B", "#3DF5FF", "#FFB547", "#FF4FA3", "#C9D1E0"


def traj(o, n=6000):
    m3 = o.get("m3", 1.0); vx, vy, T = o["vx"], o["vy"], o["T"]
    y0 = [-1, 0, 1, 0, 0, 0, vx, vy, vx, vy, -2 * vx / m3, -2 * vy / m3]
    def f(t, y):
        r = np.asarray(y[:6]).reshape(3, 2); m = (1.0, 1.0, m3); a = np.zeros((3, 2))
        for i in range(3):
            for j in range(3):
                if i != j:
                    d = r[j] - r[i]; a[i] += m[j] * d / (d @ d) ** 1.5
        return np.concatenate([y[6:], a.ravel()])
    s = solve_ivp(f, (0, T), y0, method="DOP853", rtol=1e-12, atol=1e-12, t_eval=np.linspace(0, T, n))
    return s.y[:6].T.reshape(-1, 3, 2)


def short(w, k=34):
    return w if w is None or len(w) <= k else w[:k - 3] + "... (%d letters)" % len(w)


def draw(ax, o, lw=1.2, dots=True):
    r = traj(o, n=int(min(40000, 3000 + 400 * o["T"])))
    for b, c in enumerate((C1, C2, C3)):
        ax.plot(r[:, b, 0], r[:, b, 1], color=c, lw=lw * 3.2, alpha=0.10, solid_capstyle="round")
        ax.plot(r[:, b, 0], r[:, b, 1], color=c, lw=lw, alpha=0.95, solid_capstyle="round")
        if dots: ax.plot([r[0, b, 0]], [r[0, b, 1]], "o", color=c, ms=7, mec=BG, mew=1.2, zorder=5)
    ax.set_aspect("equal"); ax.axis("off"); ax.margins(0.06)


def one(o, path, title):
    fig = plt.figure(figsize=(10, 10), dpi=160, facecolor=BG)
    ax = fig.add_axes([0.04, 0.12, 0.92, 0.78], facecolor=BG)
    draw(ax, o)
    fig.text(0.05, 0.955, title, color=FG, fontsize=20, fontweight="bold", family="DejaVu Sans")
    tag = {"new_candidate": "NEW CANDIDATE: not in our catalog of 2060 literature orbits (not proven new)", "known": "rediscovery of a known family"}.get(o.get("status"), "novelty not assessed")
    fig.text(0.05, 0.925, tag, color=C2 if o.get("status") == "new_candidate" else C1, fontsize=13)
    l1 = "vx = %.10f   vy = %.10f   T = %.8f   m3 = %g" % (o["vx"], o["vy"], o["T"], o.get("m3", 1.0))
    l2 = "T* = T|E|^1.5 = %.3f    return error %.1e (float64, official verifier)    free-group word %s" % (o.get("Tstar", float("nan")), o.get("err", float("nan")), short(o.get("free_group_word")))
    l3 = (o.get("match") or "no catalog match: candidate, not checked against the catalogs listed in catalog.json 'not_included'")
    fig.text(0.05, 0.085, l1, color=FG, fontsize=11.5, family="DejaVu Sans Mono")
    fig.text(0.05, 0.055, l2, color=FG, fontsize=10, alpha=0.85)
    fig.text(0.05, 0.027, l3[:150], color=FG, fontsize=10, alpha=0.6)
    for b, (c, lab) in enumerate(((C1, "body 1"), (C2, "body 2"), (C3, "body 3"))):
        fig.text(0.74 + 0.075 * b, 0.962, lab, color=c, fontsize=11)
    fig.savefig(path, facecolor=BG); plt.close(fig)


def sheet(orbs, path, title):
    n = len(orbs); cols = min(6, max(3, math.ceil(math.sqrt(n * 1.5)))); rows = math.ceil(n / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(3.2 * cols, 3.2 * rows + 0.9), dpi=130, facecolor=BG, squeeze=False)
    for ax in axes.ravel(): ax.set_facecolor(BG); ax.axis("off")
    for ax, o in zip(axes.ravel(), orbs):
        draw(ax, o, lw=0.7, dots=False)
        ax.set_title("T=%.2f  T*=%.2f%s" % (o["T"], o.get("Tstar", 0), "  NEW?" if o.get("status") == "new_candidate" else ""),
                     color=C2 if o.get("status") == "new_candidate" else FG, fontsize=9)
    fig.suptitle(title, color=FG, fontsize=15, y=0.995)
    fig.tight_layout(rect=[0, 0, 1, 0.97]); fig.savefig(path, facecolor=BG); plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("orbits"); ap.add_argument("--out", default="viz/threebody/out"); ap.add_argument("--top", type=int, default=6)
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    d = json.load(open(a.orbits)); orbs = d["orbits"]; summ = d.get("summary", {})
    fam = {}
    for o in sorted(orbs, key=lambda o: (o.get("power", 1), o["err"])): fam.setdefault(o.get("family", o["word"]), o)
    reps = sorted(fam.values(), key=lambda o: o["T"])
    # most interesting first: new candidates, then longest words (most intricate), always include the figure-eight
    pick = sorted(orbs, key=lambda o: (o.get("status") != "new_candidate", -len(o["word"])))[:max(0, a.top - 1)]
    f8 = [o for o in orbs if o["word"] == "123123" and abs(o["T"] - 6.3259) < 0.01]
    if f8 and f8[0] not in pick: pick.append(f8[0])
    out = []
    for k, o in enumerate(pick):
        nm = (o.get("match") or "").replace("rediscovery of ", "").replace("same topological family (free-group class) as ", "family of ").replace("topological-power satellite", "satellite").replace("the family of SD2013 figure-eight (Moore 1993)", "the figure-eight").split(" (same")[0]
        nm = nm.replace("SD2013 ", "").replace("LL2017 ", "Li-Liao 2017 ").replace("LL2018 ", "Li-Jing-Liao 2018 ")
        if o.get("status") != "known": nm = ""
        title = "Figure-eight (Moore 1993)" if o in f8 else ("Candidate new orbit" if o.get("status") == "new_candidate" else (nm[:1].upper() + nm[1:]) or "Periodic orbit")
        p = os.path.join(a.out, "threebody_%02d.png" % k); one(o, p, title[:60]); out.append({"file": p, "title": title, "orbit": o})
    sp = os.path.join(a.out, "threebody_sheet.png")
    sheet(reps[:48], sp, "Periodic three-body orbits verified by the lab: %d families from %s seeds (run %s)" % (len(reps), summ.get("seeds_scanned", "?"), summ.get("id", "?")))
    json.dump({"plots": out, "sheet": sp, "summary": summ}, open(os.path.join(a.out, "plots.json"), "w"), indent=1)
    print(json.dumps({"plots": [x["file"] for x in out], "sheet": sp}))


if __name__ == "__main__":
    main()
