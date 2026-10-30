"""Seed, flock radii and the helpers that draw the pieces every scene uses."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any

import numpy as np
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.patches import Circle
from matplotlib.ticker import NullFormatter

from analysis.results import flock_radii
from docs.generate_docs.figstyle import (
    AQUA,
    BLUE,
    INK,
    MUTED,
    ORANGE,
    REPO,
    SURFACE,
)
from docs.generate_docs.report.overview import ORIGINAL_NS
from services.cells import Cell, Group, cell_config
from services.protocol import load_protocol
from sim.core.vectors import unit
from sim.core.world.layouts import place_dogs, place_flock
from tests.helpers import config_for

# ------------------------------------------------------------------------------------ settings

Config = dict[str, Any]  # a run config, as cell_config and config_for build it
Point = Sequence[float] | np.ndarray

SEED = 2026  # every scene starts from the same flock
NS = ORIGINAL_NS
RED = "#d9534f"  # the one extra colour: personal space and the crossing assignment


def calibrated(protocol: str, fallback: dict[int, float]) -> dict[int, float]:
    """Flock radii of a finished run (results/<protocol>/calibration.json), else the fallback."""
    folder = REPO / "results" / protocol
    if not (folder / "calibration.json").exists():
        return fallback
    radii = flock_radii(folder)["strombom_multi"]
    return {int(n): float(r) for n, r in radii.items()}


# Calibrated flock radii of the strombom sheep, from the main run when it is present.
RF = calibrated("dmin_m12", {25: 6.2, 50: 7.6, 100: 9.08, 200: 10.47, 400: 11.4})


def cfg(layout: str, n: int, d: int, **kw: Any) -> Config:
    return config_for("strombom_multi", n=n, d=d, layout=layout, flock_radius=RF[n], **kw)


def start(c: Config) -> tuple[np.ndarray, np.ndarray]:
    """Sheep and dogs at the start of a trial with this config, on the shared seed."""
    return place_flock(c, np.random.default_rng(SEED)), place_dogs(c)


def field_config(n: int, max_dogs: int) -> Config:
    """Run config of a cell of the dmin protocol, whose field is sized for all four layouts and
    for ``max_dogs`` dogs; the field is the same for every cell of that N and largest D."""
    from dataclasses import replace

    protocol = load_protocol("dmin_m12", output=Path("/tmp/herdsim-figures"))
    protocol = replace(protocol, shepherd_counts=(1, max_dogs))
    return cell_config(protocol, Cell(Group("strombom_multi", "wide", (), n), max_dogs), RF[n])


# ------------------------------------------------------------------------------ drawing helpers


def xy(point: Point) -> tuple[float, float]:
    """A point as the (x, y) tuple matplotlib patches take."""
    return float(point[0]), float(point[1])


def style_map(ax: Axes, title: str) -> None:
    """A map panel: equal axes, no ticks, no frame."""
    ax.set_aspect("equal")
    ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks([])
    for side in ("left", "bottom"):
        ax.spines[side].set_visible(False)


def window(ax: Axes, centre: Point, left: float, right: float, down: float, up: float) -> None:
    """View the area from ``left`` to ``right`` and ``down`` to ``up`` around ``centre``."""
    ax.set_xlim(centre[0] - left, centre[0] + right)
    ax.set_ylim(centre[1] - down, centre[1] + up)


def arrow(
    ax: Axes, tip: Point, tail: Point, color: str, lw: float, style: str = "->", **kw: Any
) -> None:
    ax.annotate(
        "", xy=xy(tip), xytext=xy(tail), arrowprops=dict(arrowstyle=style, color=color, lw=lw, **kw)
    )


def dogs_at(
    ax: Axes, dogs: np.ndarray, s: float = 34, lw: float = 0.8, zorder: int = 3, **kw: Any
) -> None:
    ax.scatter(*dogs.T, s=s, marker="^", color=ORANGE, ec=SURFACE, lw=lw, zorder=zorder, **kw)


def targets_at(
    ax: Axes, targets: np.ndarray, s: float, lw: float, zorder: int = 4, **kw: Any
) -> None:
    ax.scatter(*targets.T, s=s, marker="x", color=INK, lw=lw, zorder=zorder, **kw)


def flock_split(
    ax: Axes,
    sheep: np.ndarray,
    far: np.ndarray,
    s_in: float,
    s_out: float,
    lw_out: float,
    alpha_in: float = 0.6,
    labels: tuple[str | None, str | None] = (None, None),
) -> None:
    """Sheep inside the collect distance plain, outliers ringed."""
    ax.scatter(*sheep[~far].T, s=s_in, color=BLUE, alpha=alpha_in, lw=0, label=labels[0])
    ax.scatter(*sheep[far].T, s=s_out, color=BLUE, ec=INK, lw=lw_out, label=labels[1])


def gcm(
    ax: Axes,
    centre: Point,
    label: str | None = "GCM",
    s: float = 40,
    lw: float | None = None,
    color: str = INK,
    zorder: int = 4,
    text_at: tuple[float, float] = (3, 3),
    fontsize: float = 8,
    **text_kw: Any,
) -> None:
    """The flock centre as a plus, with an optional label offset by ``text_at``."""
    ax.scatter(*centre, s=s, marker="+", color=color, lw=lw, zorder=zorder)
    if label is not None:
        ax.text(
            centre[0] + text_at[0],
            centre[1] + text_at[1],
            label,
            color=color,
            fontsize=fontsize,
            **text_kw,
        )


def draw_scene(
    ax: Axes, c: Config, sheep: np.ndarray, dogs: np.ndarray, goal_arrow: bool = True
) -> None:
    """Goal, sheep and dogs of a start, with an arrow toward the goal."""
    center = np.asarray(c["flock_center"])
    goal = np.asarray(c["goal_center"])
    ax.add_patch(Circle(xy(goal), c["goal_radius"], fc="none", ec=AQUA, lw=1.5))
    ax.scatter(*sheep.T, s=7, color=BLUE, alpha=0.85, lw=0)
    dogs_at(ax, dogs)
    if goal_arrow:
        arrow(ax, goal - [c["goal_radius"] + 4, 0], center + [14, 0], MUTED, 0.9)


def force_arrows(
    ax: Axes, origin: Point, forces: dict[str, np.ndarray], colors: Sequence[str]
) -> list[Line2D]:
    """One arrow per force from ``origin``, with legend handles giving each magnitude.

    Arrow length is 3.2 times the square root of the force, and at least 3.5, so that forces
    of very different sizes all show."""
    handles = []
    for (label, v), color in zip(forces.items(), colors):
        mag = float(np.linalg.norm(v))
        arrow(ax, unit(v) * max(np.sqrt(mag) * 3.2, 3.5), origin, color, 1.6)
        handles.append(Line2D([0], [0], color=color, lw=2, label=f"{label}  {mag:.1f}"))
    return handles


def n_axis(ax: Axes, ns: Sequence[int] = NS) -> None:
    """Flock size on a log axis, with only the sizes run labelled."""
    ax.set_xscale("log")
    ax.set_xticks(ns)
    ax.set_xticklabels([str(k) for k in ns])
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xlabel("flock size N")
