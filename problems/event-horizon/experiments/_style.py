"""Shared dark plot style for Event Horizon figures."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BG, FG = "#07080B", "#E6EDF3"
CYAN, AMBER, MAGENTA, GREEN = "#3DF5FF", "#FFB547", "#FF5DA8", "#6CF29A"
GREY = "#8B949E"
PALETTE = [CYAN, AMBER, MAGENTA, GREEN, "#B8A1FF", "#FF8A5C", "#9AD1FF", GREY]


def setup():
    plt.rcParams.update({
        "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
        "text.color": FG, "axes.labelcolor": FG, "axes.edgecolor": "#30363D",
        "xtick.color": FG, "ytick.color": FG, "grid.color": "#21262D",
        "axes.grid": True, "grid.linewidth": 0.6, "font.size": 10,
        "legend.facecolor": "#0D1117", "legend.edgecolor": "#30363D",
        "legend.fontsize": 8, "axes.titlesize": 11,
    })
    return plt


def caption(fig, text):
    fig.text(0.5, 0.005, text, ha="center", va="bottom", fontsize=7.5, color=GREY, wrap=True)
