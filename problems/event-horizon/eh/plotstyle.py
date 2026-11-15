"""Shared dark plot theme + JSON helper."""
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BG, FG = "#07080B", "#E6EDF3"
CYAN, AMBER, MAGENTA, GREEN = "#3DF5FF", "#FFB547", "#FF5DA8", "#6CF29A"
GRID = "#1E2530"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FIG = os.path.join(ROOT, "figures")
RES = os.path.join(ROOT, "results")


def apply():
    plt.rcParams.update({
        "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
        "text.color": FG, "axes.labelcolor": FG, "axes.edgecolor": "#3A4452",
        "xtick.color": FG, "ytick.color": FG, "grid.color": GRID, "axes.grid": True,
        "legend.facecolor": "#0D1016", "legend.edgecolor": "#3A4452", "font.size": 10,
        "axes.titlesize": 11, "figure.dpi": 100,
    })
    return plt


def caption(fig, text):
    fig.text(0.5, 0.005, text, ha="center", va="bottom", fontsize=7.5, color="#9AA7B4", wrap=True)


def save(fig, name):
    os.makedirs(FIG, exist_ok=True)
    path = os.path.join(FIG, name)
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def _default(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(type(o))


def dump(obj, name):
    os.makedirs(RES, exist_ok=True)
    path = os.path.join(RES, name)
    with open(path, "w") as f:
        json.dump(obj, f, indent=1, default=_default)
    return path
