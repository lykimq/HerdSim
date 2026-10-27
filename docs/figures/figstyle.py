"""The look every figure shares: colours, matplotlib defaults, where figures go, and saving.

Both figure scripts import this module, so a colour, a default or the resolution changes in
one place. The captions are in the report and README, so a figure carries no caption text;
``save`` lays it out, adds an optional source note under the panels and writes the PNG.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.axes import Axes  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
OUT = Path(__file__).parent
DPI = 150

SURFACE, INK, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"  # categorical slots 1 to 3

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


def grid(ax: Axes, axis: str = "both") -> None:
    ax.grid(axis=axis, color=GRID, lw=0.6)


def save(
    fig: Figure,
    file: str,
    rect: tuple[float, float, float, float] | None = None,
    note: str | None = None,
    note_y: float = 0.01,
    layout: bool = True,
) -> None:
    """Lay out (unless ``layout`` is off, for figures placed by hand), add the source note
    under the panels, write the PNG and free the figure."""
    if layout:
        fig.tight_layout(rect=rect)
    if note is not None:
        fig.text(0.5, note_y, note, ha="center", fontsize=8, color=MUTED)
    fig.savefig(OUT / file, dpi=DPI)
    plt.close(fig)
