"""Shared figure style: colours, defaults, output paths, save, log/N-axis and map helpers."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any, Literal

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.axes import Axes  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402

from analysis.frontier import (  # noqa: E402
    COLLAPSE,
    CROWDED,
    IMPROVING,
    RECOVERED,
    SATURATED,
    TOO_FEW,
    UNDECIDED,
    UNRELIABLE_DIP,
)
from docs.generate_docs.runs import ORIGINAL_NS  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "docs" / "figures"
GIF_OUT = REPO / "docs" / "gifs"
DPI = 150

SURFACE, INK, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"  # categorical slots 1 to 3
RED = "#d9534f"  # the one extra colour: failure, personal space, a crossing assignment
NS = ORIGINAL_NS  # flock sizes every N-axis figure labels
Point = Sequence[float] | np.ndarray
ZONE_COLOR = {
    TOO_FEW: RED,
    UNRELIABLE_DIP: RED,
    COLLAPSE: INK,
    UNDECIDED: MUTED,
    IMPROVING: AQUA,
    SATURATED: BLUE,
    CROWDED: ORANGE,
    RECOVERED: AQUA,
}

plt.rcParams.update(
    {
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "axes.edgecolor": MUTED,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": False,
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.titleweight": "normal",
        "axes.titlelocation": "left",
    }
)


def grid(ax: Axes, axis: Literal["both", "x", "y"] = "both") -> None:
    ax.grid(axis=axis, color=GRID, lw=0.6)


def log_ticks(
    ax: Axes,
    ticks: Sequence[float],
    axis: str = "x",
    labels: Sequence[str] | None = None,
) -> None:
    """Log scale with only the given ticks (minors off after the scale is set)."""
    shown = [str(t) for t in ticks] if labels is None else list(labels)
    if axis == "x":
        ax.set_xscale("log")
        ax.set_xticks(ticks)
        ax.set_xticklabels(shown)
    else:
        ax.set_yscale("log")
        ax.set_yticks(ticks)
        ax.set_yticklabels(shown)
    ax.minorticks_off()


def n_axis(ax: Axes, ns: Sequence[int] = NS) -> None:
    """Flock size on a log axis, with only the sizes run labelled."""
    log_ticks(ax, ns)
    ax.set_xlabel("flock size N")


def style_map(ax: Axes, title: str) -> None:
    """A map panel: equal axes, no ticks, no frame."""
    ax.set_aspect("equal")
    ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks([])
    for side in ("left", "bottom"):
        ax.spines[side].set_visible(False)


def window(ax: Axes, centre: Point, left: float, right: float, down: float, up: float) -> None:
    """Set axes limits around ``centre`` by left/right/down/up offsets."""
    ax.set_xlim(centre[0] - left, centre[0] + right)
    ax.set_ylim(centre[1] - down, centre[1] + up)


def dogs_at(
    ax: Axes, dogs: np.ndarray, s: float = 34, lw: float = 0.8, zorder: int = 3, **kw: Any
) -> None:
    """Dogs as orange triangles."""
    ax.scatter(*dogs.T, s=s, marker="^", color=ORANGE, ec=SURFACE, lw=lw, zorder=zorder, **kw)


def save(
    fig: Figure,
    file: str,
    rect: tuple[float, float, float, float] | None = None,
    note: str | None = None,
    note_y: float = 0.01,
    layout: bool = True,
) -> None:
    """Tight-layout (unless off), optional source note, save PNG, close the figure."""
    if layout:
        fig.tight_layout(rect=rect)
    if note is not None:
        fig.text(0.5, note_y, note, ha="center", fontsize=8, color=MUTED)
    fig.savefig(OUT / file, dpi=DPI)
    plt.close(fig)
