"""Contact sheet + single panels for the verified candidate orbits (data/threebody_candidates.json).
Trajectories are re-integrated from the stored initial conditions (DOP853, rtol 1e-12)."""
import json, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plot_orbits import traj, BG, C1, C2, C3, FG  # noqa: E402

orbs = json.load(open(sys.argv[1]))["orbits"]
out = sys.argv[2]; os.makedirs(out, exist_ok=True)
cols = 4; rows = (len(orbs) + cols - 1) // cols
fig, axs = plt.subplots(rows, cols, figsize=(4.2 * cols, 4.2 * rows), facecolor=BG)
for ax in axs.ravel():
    ax.set_facecolor(BG); ax.axis("off")
for i, o in enumerate(orbs):
    tr = traj(o, n=9000)
    ax = axs.ravel()[i]
    for b, c in enumerate((C1, C2, C3)):
        ax.plot(tr[:, b, 0], tr[:, b, 1], color=c, lw=0.9, alpha=0.95)
    ax.set_aspect("equal")
    ax.set_title(f"candidate {i+1}  m3={o.get('m3', 1)}  T={o['T']:.3f}", color=FG, fontsize=10)
    f2, a2 = plt.subplots(figsize=(6, 6), facecolor=BG); a2.set_facecolor(BG); a2.axis("off")
    for b, c in enumerate((C1, C2, C3)):
        a2.plot(tr[:, b, 0], tr[:, b, 1], color=c, lw=1.1)
    a2.set_aspect("equal"); f2.savefig(os.path.join(out, f"candidate_{i+1}.png"), dpi=160, facecolor=BG, bbox_inches="tight"); plt.close(f2)
fig.suptitle(f"Three-body: {len(orbs)} verified periodic orbits whose topological families are absent from the 2,060 catalogued orbits checked\n"
             "(candidates, not proven new; float64 DOP853, return error < 1e-8; m1 = m2 = 1, m3 as labelled)", color=FG, fontsize=13)
fig.savefig(os.path.join(out, "candidates_contact_sheet.png"), dpi=150, facecolor=BG, bbox_inches="tight")
print("ok", len(orbs))
