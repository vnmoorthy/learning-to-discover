"""Shared dark plotting theme."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

BG = "#07080B"
FG = "#E6EDF3"
CYAN = "#3DF5FF"
AMBER = "#FFB547"
MAGENTA = "#FF5DA8"
GREEN = "#6CF29A"
PALETTE = [CYAN, AMBER, MAGENTA, GREEN, "#B48CFF", "#FF7A59", "#8AB4FF"]


def apply_theme():
    plt.rcParams.update(
        {
            "figure.facecolor": BG,
            "axes.facecolor": BG,
            "savefig.facecolor": BG,
            "text.color": FG,
            "axes.labelcolor": FG,
            "axes.edgecolor": "#3A4150",
            "xtick.color": FG,
            "ytick.color": FG,
            "grid.color": "#1C212B",
            "axes.grid": True,
            "legend.facecolor": "#0D1016",
            "legend.edgecolor": "#3A4150",
            "font.size": 10,
            "axes.titlesize": 11,
            "axes.prop_cycle": matplotlib.cycler(color=PALETTE),
        }
    )
    return plt


def caption(fig, text):
    fig.text(0.5, 0.005, text, ha="center", va="bottom", fontsize=7.5, color="#9AA4B2", wrap=True)


def save(fig, path, cap=None):
    if cap:
        caption(fig, cap)
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
