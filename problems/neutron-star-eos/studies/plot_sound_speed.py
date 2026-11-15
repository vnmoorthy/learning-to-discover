"""Figure for results/sound_speed.json -> figures/cs2_requirement.png (novelty level 2)."""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(ROOT, "results", "sound_speed.json")))
BG, FG, A1, A2 = "#0B0D10", "#E7E9EC", "#4FD1E0", "#E2B25C"
plt.rcParams.update({"figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG, "text.color": FG,
                     "axes.labelcolor": FG, "xtick.color": FG, "ytick.color": FG, "axes.edgecolor": FG})
cols = {1.1: A1, 1.5: "#9AA3AD", 2.0: A2}
fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))
g = [r for r in d["grid"] if r["shape"] == "step"]
for fm in (1.1, 1.5, 2.0):
    rr = sorted([r for r in g if r["n_match_nsat"] == fm], key=lambda r: r["cs2max"])
    x = [r["cs2max"] for r in rr]
    ax[0].plot(x, [r["M_max"] for r in rr], "o-", color=cols[fm], label=f"SLy below n_m = {fm} n_sat")
    ax[2].plot(x, [r.get("R_1p4", float("nan")) for r in rr], "o-", color=cols[fm], label=f"n_m = {fm} n_sat")
for a in (ax[0],):
    a.axhline(2.0, color=FG, ls="--", lw=0.8); a.axhline(2.08, color=FG, ls=":", lw=0.8)
for a in (ax[0], ax[2]):
    a.axvline(1 / 3, color=FG, ls="-.", lw=0.8)
    a.text(1 / 3 + 0.01, a.get_ylim()[0] + 0.03 * (a.get_ylim()[1] - a.get_ylim()[0]), "c_s^2 = 1/3 (benchmark)",
           fontsize=8)
ax[0].set_xlabel(r"$c_{s,\max}^2$ above $n_m$  [$c^2$]"); ax[0].set_ylabel(r"$M_{\max}$  [$M_\odot$]")
ax[0].set_title("'step' completion: $M_{max}$ vs stiffness", color=FG, fontsize=10); ax[0].legend(fontsize=8, frameon=False)
for tg, mk in ((2.0, "o"), (2.08, "s")):
    rr = sorted([r for r in d["requirement"] if r["target"] == tg and r["shape"] == "step" and r["cs2_min"]],
                key=lambda r: r["n_match_nsat"])
    ax[1].plot([r["n_match_nsat"] for r in rr], [r["cs2_min"] for r in rr], mk + "-", color=A1,
               label=f"step, M_max >= {tg} M_sun")
rr = sorted([r for r in d["requirement"] if r["shape"] == "ramp" and r["cs2_min"]], key=lambda r: r["n_match_nsat"])
ax[1].plot([r["n_match_nsat"] for r in rr], [r["cs2_min"] for r in rr], "D--", color=A2,
           label="ramp over 1.5 n_sat, M_max >= 2.0 M_sun")
ax[1].axhline(1 / 3, color=FG, ls="-.", lw=0.8)
ax[1].set_xlabel(r"matching density $n_m$  [$n_{sat}$ = 0.16 fm$^{-3}$]")
ax[1].set_ylabel(r"minimum $c_{s,\max}^2$  [$c^2$]")
ax[1].set_title("required stiffness vs matching density", color=FG, fontsize=10); ax[1].legend(fontsize=8, frameon=False)
ax[2].set_xlabel(r"$c_{s,\max}^2$ above $n_m$  [$c^2$]"); ax[2].set_ylabel(r"$R_{1.4}$  [km]")
ax[2].set_title("radius of a 1.4 $M_\odot$ star", color=FG, fontsize=10); ax[2].legend(fontsize=8, frameon=False)
fig.suptitle("Sound-speed requirement for 2 M_sun (SLy fixed below n_m; novelty level 2: verification of known relation)",
             color=FG, fontsize=11)
fig.tight_layout()
fig.savefig(os.path.join(ROOT, "figures", "cs2_requirement.png"), dpi=160)
