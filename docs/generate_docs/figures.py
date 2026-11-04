"""Model and task figures for make_figures.py.

Scene helpers first, then figures by topic (models, team rule, task). Style in figstyle.py.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import replace
from typing import Any, NamedTuple

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Rectangle

from analysis.frontier import COLLAPSE, CROWDED, IMPROVING, SATURATED, TOO_FEW
from analysis.results import flock_radii
from docs.generate_docs.figstyle import (
    AQUA,
    BLUE,
    GRID,
    INK,
    MUTED,
    NS,
    ORANGE,
    RED,
    SURFACE,
    ZONE_COLOR,
    Point,
    dogs_at,
    grid,
    n_axis,
    save,
    style_map,
    window,
)
from docs.generate_docs.runs import STRICT_RUNS
from services.cells import Cell, Group, cell_config
from services.protocol import RESULTS_ROOT, load_protocol
from sim.drive_task.layouts import LAYOUTS, layout_extent, place_dogs, place_flock
from sim.state import SimulationState
from sim.strombom.params import METHOD, PAPER
from sim.strombom.shepherd import collect_threshold, drive_point, radius_of
from sim.strombom.team import team_targets
from sim.trial import initial_state, run_trial
from sim.vectors import unit

# ----- settings -----
Config = dict[str, Any]  # a run config, as cell_config builds it

R_S = PAPER["r_s"]
R_A = PAPER["r_a"]
SEED = 2026  # every scene starts from the same flock
MAIN_RUN = STRICT_RUNS[12]
MAIN = load_protocol(MAIN_RUN)  # every scene is a cell of this run
# The drive length's first two terms and the goal radius in flock radii.
DRIVE_MULTIPLE = MAIN.settings["drive_distance_multiple"]
DRIVE_FLOOR = MAIN.settings["drive_distance_min"]
GOAL_MULTIPLE = MAIN.settings["goal_radius_multiple"]


# Calibrated flock radii of the Strombom sheep, from the main run.
RF = flock_radii(RESULTS_ROOT / MAIN_RUN)[METHOD]


def cfg(
    layout: str, n: int, d: int, *, ticks: int = 300, settings: dict[str, Any] | None = None
) -> Config:
    """Run config of one cell of the main run, with the field sized for this cell alone."""
    method = replace(MAIN.methods[0], time_limit_ticks=ticks, time_limit_drive_multiple=None)
    protocol = replace(
        MAIN,
        settings={**MAIN.settings, **(settings or {})},
        methods=(method,),
        layouts=(layout,),
        shepherd_counts=(d,),
    )
    return cell_config(protocol, Cell(Group(METHOD, layout, n), d), RF[n])


def start(c: Config) -> tuple[np.ndarray, np.ndarray]:
    """Sheep and dogs at trial start on the shared seed."""
    return place_flock(c, np.random.default_rng(SEED)), place_dogs(c)


def field_config(n: int, max_dogs: int) -> Config:
    """dmin cell config whose field fits all four layouts and ``max_dogs`` dogs."""
    protocol = replace(MAIN, shepherd_counts=(1, max_dogs))
    return cell_config(protocol, Cell(Group(METHOD, "wide", n), max_dogs), RF[n])


# ----- drawing helpers -----
def xy(point: Point) -> tuple[float, float]:
    """Point as an (x, y) tuple for matplotlib patches."""
    return float(point[0]), float(point[1])


def arrow(
    ax: Axes, tip: Point, tail: Point, color: str, lw: float, style: str = "->", **kw: Any
) -> None:
    ax.annotate(
        "", xy=xy(tip), xytext=xy(tail), arrowprops=dict(arrowstyle=style, color=color, lw=lw, **kw)
    )


def bold_text(
    ax: Axes, x: float, y: float, text: str, color: str, fontsize: float = 9, **kw: Any
) -> None:
    ax.text(x, y, text, color=color, fontsize=fontsize, fontweight="bold", **kw)


def dog_label(ax: Axes, dog: np.ndarray, i: int) -> None:
    """Number a dog, to the left of its marker."""
    bold_text(ax, dog[0] - 16, dog[1] - 2, f"dog {i + 1}", ORANGE, fontsize=8.5)


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
    """Plot in-flock sheep plain and outliers with a ring."""
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
    """Mark the flock centre with a plus and optional label."""
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
    """Draw goal, sheep, dogs, and an optional arrow toward the goal."""
    center = np.asarray(c["flock_center"])
    goal = np.asarray(c["goal_center"])
    ax.add_patch(Circle(xy(goal), c["goal_radius"], fc="none", ec=AQUA, lw=1.5))
    ax.scatter(*sheep.T, s=7, color=BLUE, alpha=0.85, lw=0)
    dogs_at(ax, dogs)
    if goal_arrow:
        arrow(ax, goal - [c["goal_radius"] + 4, 0], center + [14, 0], MUTED, 0.9)


# ----- models: sheep forces -----
# The scene of the figure, in metres around the focal sheep at the origin.
FOCAL = np.array([0.0, 0.0])
FLOCK_NEIGHBORS = np.array(
    [
        [16.0, 12.0],
        [22.0, -3.0],
        [9.0, 24.0],
        [26.0, 16.0],
        [19.0, 27.0],
        [31.0, 6.0],
        [13.0, -14.0],
        [23.0, -17.0],
    ]
)
CLOSE_NEIGHBOR = np.array([-3.2, 2.8])
FORCE_DOG = np.array([-32.0, -26.0])
FORCE_ARROW_SCALE = 12.0  # arrow length per unit of weighted force


class ForceArrow(NamedTuple):
    """One of the five weighted terms of the sheep's heading."""

    label: str
    vec: np.ndarray
    color: str
    note: str
    tip_label: str
    tip_offset: tuple[float, float]


def force_arrows(lcm: np.ndarray) -> list[ForceArrow]:
    """The five terms of Strombom (2014) with the paper's weights, in the order of the figure."""
    h, c, rho_a, rho_s, e = (
        PAPER[k] for k in ("inertia", "c", "rho_a", "rs_weight", "noise_strength")
    )
    # (label, weight, unit vector the weight multiplies, colour, weight note, tip label, offset)
    terms = (
        (
            r"1. Previous heading $h\,\mathbf{H}_i$",
            h,
            unit(np.array([0.5, 0.85])),
            BLUE,
            f"weight h = {h}",
            r"$h\,\mathbf{H}_i$",
            (0.5, 1.0),
        ),
        (
            r"2. Attraction to the flock $c\,\mathbf{C}_i$",
            c,
            unit(lcm - FOCAL),
            AQUA,
            f"weight c = {c}",
            r"$c\,\mathbf{C}_i$",
            (1.0, 0),
        ),
        (
            r"3. Keeping space $\rho_a\,\mathbf{R}_{a,i}$",
            rho_a,
            unit(FOCAL - CLOSE_NEIGHBOR),
            RED,
            f"weight $\\rho_a$ = {rho_a} (highest)",
            r"$\rho_a\,\mathbf{R}_{a,i}$",
            (1.0, -2.2),
        ),
        (
            r"4. Running from the dog $\rho_s\,\mathbf{R}_{s,i}$",
            rho_s,
            unit(FOCAL - FORCE_DOG),
            ORANGE,
            f"weight $\\rho_s$ = {rho_s}",
            r"$\rho_s\,\mathbf{R}_{s,i}$",
            (1.0, 0),
        ),
        (
            r"5. Noise $e\,\mathbf{\epsilon}_i$",
            e,
            unit(np.array([-0.8, 0.5])),
            MUTED,
            f"weight e = {e}",
            r"$e\,\mathbf{\epsilon}_i$",
            (-2.0, 1.0),
        ),
    )
    return [
        ForceArrow(label, weight * direction, color, note, tip, offset)
        for label, weight, direction, color, note, tip, offset in terms
    ]


def forces_geometry_panel(ax: Axes, lcm: np.ndarray) -> None:
    """Who the focal sheep reacts to: neighbours, a too-close neighbour, the local centre, a dog."""
    r_a_drawn = R_A * 3.0  # drawn 3x so the close neighbour and circle are legible at r_s scale
    ax.add_patch(Circle((0, 0), R_S, fc=ORANGE, alpha=0.04, ec="none"))
    ax.add_patch(Circle((0, 0), R_S, fc="none", ec=ORANGE, lw=1.1, ls="--", alpha=0.75))
    ax.plot([], [], color=ORANGE, lw=1.1, ls="--", label=f"dog detection radius $r_s = {R_S:g}$ m")
    ax.add_patch(
        Circle(
            (0, 0),
            r_a_drawn,
            fc=RED,
            alpha=0.18,
            ec=RED,
            lw=1.2,
            label=f"repulsion zone $r_a = {R_A:g}$ m (drawn 3x)",
        )
    )
    ax.scatter(*FLOCK_NEIGHBORS.T, s=35, color=BLUE, alpha=0.75, lw=0, label="flock-mates")
    ax.scatter(
        *CLOSE_NEIGHBOR,
        s=50,
        color=RED,
        ec=INK,
        lw=0.9,
        zorder=4,
        label=r"neighbour closer than $r_a$",
    )
    ax.scatter(*FOCAL, s=85, color=INK, zorder=5, label="sheep $i$")
    bold_text(ax, FOCAL[0] + 2.5, FOCAL[1] - 5.5, "Sheep $i$", INK)
    ax.scatter(
        *lcm, s=75, marker="+", color=AQUA, lw=2.2, zorder=4, label="local centre of mass (LCM)"
    )
    bold_text(ax, lcm[0] + 2.5, lcm[1] - 1.5, r"$\mathrm{LCM}_i$", AQUA)
    dogs_at(ax, FORCE_DOG, s=95, lw=1.0, zorder=5, label=r"dog (within $r_s$)")
    bold_text(ax, FORCE_DOG[0] - 2.0, FORCE_DOG[1] - 6.5, "dog", ORANGE)
    ax.text(46, -54, f"$r_s = {R_S:g}$ m", color=ORANGE, fontsize=8.5)
    ax.set_xlim(-72, 72)
    ax.set_ylim(-72, 72)
    ax.legend(loc="upper left", frameon=False, fontsize=8)
    style_map(ax, "A. What sheep $i$ responds to")


def forces_sum_panel(ax: Axes, arrows: Sequence[ForceArrow]) -> None:
    """The five weighted terms from the sheep, and their sum as the resultant heading."""
    scale = FORCE_ARROW_SCALE
    resultant = sum((a.vec for a in arrows), start=np.zeros(2)) * (scale * 0.55)
    handles = []
    for a in arrows:
        arrow(ax, a.vec * scale, (0, 0), a.color, 2.2)
        handles.append(Line2D([0], [0], color=a.color, lw=2.2, label=f"{a.label} ({a.note})"))
    arrow(ax, resultant, (0, 0), INK, 3.2, style="-|>")
    handles.append(
        Line2D(
            [0],
            [0],
            color=INK,
            lw=3.2,
            label=(
                r"new heading $\mathbf{H}_i'$ "
                r"($\mathbf{x}_i^{t+1} = \mathbf{x}_i^t + \delta\,\mathbf{H}_i' / "
                r"\|\mathbf{H}_i'\|$)"
            ),
        )
    )
    ax.scatter(0, 0, s=70, color=INK, zorder=5)
    bold_text(ax, -1.5, -3.2, "Sheep $i$", INK, ha="right")
    for a in arrows:
        dx, dy = a.tip_offset
        bold_text(ax, a.vec[0] * scale + dx, a.vec[1] * scale + dy, a.tip_label, a.color)
    bold_text(ax, resultant[0] + 1.2, resultant[1] + 0.5, r"$\mathbf{H}_i'$", INK, 9.5)
    ax.legend(handles=handles, loc="lower left", frameon=False, fontsize=8)
    ax.set_xlim(-18, 32)
    ax.set_ylim(-28, 22)
    style_map(ax, r"B. The five weighted terms and the new heading $\mathbf{H}_i'$")


def fig_sheep_forces() -> None:
    """Strombom (2014) sheep forces: interaction geometry (left) and weighted sum (right)."""
    lcm = np.vstack([FLOCK_NEIGHBORS, CLOSE_NEIGHBOR]).mean(axis=0)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.8))
    forces_geometry_panel(axes[0], lcm)
    forces_sum_panel(axes[1], force_arrows(lcm))
    save(fig, "fig_sheep_forces.png", rect=(0, 0, 1, 0.98))


# ----- team rule -----
def team_rule_panel(ax: Axes, layout: str, n: int, d: int, collecting: bool) -> None:
    """One start: the flock, the dogs and the team's targets, in a collect or a drive window."""
    c = cfg(layout, n, d)
    sheep, dogs = start(c)
    targets = team_targets(sheep, np.asarray(c["goal_center"]), dogs, c)
    centroid = sheep.mean(axis=0)
    f_n = collect_threshold(n, c["r_a"])
    far = np.linalg.norm(sheep - centroid, axis=1) > f_n
    if collecting:
        ax.add_patch(Circle(xy(centroid), f_n, fc="none", ec=MUTED, lw=0.9, ls="--"))
    flock_split(ax, sheep, far, s_in=7, s_out=14, lw_out=0.5)
    dogs_at(ax, dogs)
    targets_at(ax, targets, s=22, lw=1.1, zorder=3)
    if not collecting and d > 1:  # the drive slots lie on an arc; a thin line makes them readable
        ordered = targets[np.argsort(targets[:, 1])]
        ax.plot(*ordered.T, color=INK, lw=0.5, alpha=0.4, zorder=2)
    for dog, target in zip(dogs, targets, strict=True):
        arrow(ax, target, dog, ORANGE, 0.9)
    window(ax, centroid, *((185, 115, 170, 170) if collecting else (80, 35, 70, 70)))
    job = "collect" if collecting else "drive"
    style_map(ax, f"{job}, D = {d}" + ("  (the paper)" if d == 1 else ""))


def fig_team_rule() -> None:
    """Team rule from D=1 to 8: collect (wide) and drive (compact)."""
    counts = (1, 2, 4, 8)
    rows = (("wide", 200), ("compact", 200))
    fig, axes = plt.subplots(2, 4, figsize=(13, 7.2))
    for col, d in enumerate(counts):
        for row, (layout, n) in enumerate(rows):
            team_rule_panel(axes[row, col], layout, n, d, collecting=row == 0)
    fig.text(0.01, 0.015, "light blue: sheep inside f(N)", color=BLUE, fontsize=8.5)
    fig.text(0.19, 0.015, "dark-outlined: outliers (> f(N))", color=INK, fontsize=8.5)
    fig.text(
        0.39, 0.015, "orange triangles + arrows: dogs -> targets (x)", color=ORANGE, fontsize=8.5
    )
    fig.text(
        0.69,
        0.015,
        "dashed circle: collect threshold f(N) = r_a N^(2/3)",
        color=MUTED,
        fontsize=8.5,
    )
    save(fig, "fig3_team_rule.png", rect=(0, 0.04, 1, 0.98))


# ----- team rule: collect point and Hungarian matching -----
def outlier_panel(
    ax: Axes, c: Config, sheep: np.ndarray, far: np.ndarray, centroid: np.ndarray, thresh: float
) -> None:
    """Outliers beyond f(N) and the collect point behind the farthest one."""
    stray = sheep[np.argmax(np.linalg.norm(sheep - centroid, axis=1))]
    # drawn four times farther out than the real r_a, or the cross would sit on the sheep
    pc_pos = stray + float(c["r_a"]) * 4.0 * unit(stray - centroid)
    ax.add_patch(Circle(xy(centroid), thresh, fc=BLUE, alpha=0.04, ec="none"))
    ax.add_patch(Circle(xy(centroid), thresh, fc="none", ec=MUTED, lw=1.1, ls="--", alpha=0.7))
    ax.plot([], [], color=MUTED, lw=1.1, ls="--", label=r"collect threshold $f(N) = r_a N^{2/3}$")
    flock_split(
        ax,
        sheep,
        far,
        s_in=18,
        s_out=30,
        lw_out=0.8,
        labels=("sheep inside $f(N)$", r"outliers ($> f(N)$)"),
    )
    gcm(
        ax,
        centroid,
        label="GCM (flock centre)",
        s=65,
        lw=2.0,
        zorder=5,
        text_at=(3, -4),
        fontsize=9,
        fontweight="bold",
    )
    arrow(ax, pc_pos, centroid, MUTED, 1.0, ls=":")
    ax.scatter(*stray, s=95, facecolors="none", ec=ORANGE, lw=1.8, zorder=4)
    bold_text(ax, stray[0] + 3, stray[1] - 2, r"outlier $o$", ORANGE, 9.5)
    ax.scatter(*pc_pos, s=90, marker="x", color=INK, lw=2.2, zorder=5)
    bold_text(
        ax,
        pc_pos[0] + 3,
        pc_pos[1] + 3,
        r"collect point $P_c$" + "\n" + f"($r_a = {R_A:g}$ m behind, drawn 4x)",
        INK,
    )
    ax.text(
        centroid[0] + thresh + 3,
        centroid[1] - 12,
        r"$f(N) = r_a N^{2/3}$",
        color=MUTED,
        fontsize=8.5,
    )
    ax.legend(loc="lower left", frameon=False, fontsize=8.5)
    window(ax, centroid, 130, 90, 110, 110)
    style_map(ax, "A. Outliers and the collect point Pc")


def matching_panel(
    ax: Axes,
    c: Config,
    sheep: np.ndarray,
    dogs: np.ndarray,
    far: np.ndarray,
    centroid: np.ndarray,
) -> None:
    """The assignment of dogs to collect points, against a hand-drawn crossing one."""
    targets = team_targets(sheep, np.asarray(c["goal_center"]), dogs, c)
    thresh = collect_threshold(int(c["n_sheep"]), c["r_a"])
    ax.add_patch(Circle(xy(centroid), thresh, fc="none", ec=MUTED, lw=0.9, ls="--", alpha=0.6))
    flock_split(ax, sheep, far, s_in=15, s_out=28, lw_out=0.6, alpha_in=0.5)
    gcm(ax, centroid, label=None, s=50, lw=1.5, color=MUTED, zorder=3)
    dogs_at(ax, dogs, s=70, lw=1.0, zorder=5, label="dogs ($D = 4$)")
    targets_at(ax, targets, s=65, lw=1.8, zorder=5, label="collect points $P_{c,1..4}$")
    ax.plot([], [], color=ORANGE, lw=1.8, label="Hungarian assignment (min total walk)")
    for dog, tgt in zip(dogs, targets, strict=True):
        arrow(ax, tgt, dog, ORANGE, 1.8)
    for k, (i, j) in enumerate(((0, 2), (2, 0))):  # dog i to the target of dog j
        ax.plot(
            [dogs[i, 0], targets[j, 0]],
            [dogs[i, 1], targets[j, 1]],
            color=RED,
            ls="--",
            lw=1.0,
            alpha=0.45,
            label="crossing assignment (longer total walk)" if k == 0 else None,
        )
    for i, dog in enumerate(dogs):
        dog_label(ax, dog, i)
    ax.legend(loc="lower right", frameon=False, fontsize=8.5)
    window(ax, centroid, 130, 90, 110, 110)
    style_map(ax, "B. Hungarian assignment: no two paths cross")


def fig_hungarian_matching() -> None:
    """Outliers and Pc (left); Hungarian matching vs a crossing assignment (right)."""
    n, d = 100, 4
    c = cfg("wide", n, d)
    sheep, dogs = start(c)
    centroid = sheep.mean(axis=0)
    thresh = collect_threshold(n, c["r_a"])
    far = np.linalg.norm(sheep - centroid, axis=1) > thresh
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.8))
    outlier_panel(axes[0], c, sheep, far, centroid, thresh)
    matching_panel(axes[1], c, sheep, dogs, far, centroid)
    save(fig, "fig_hungarian_matching.png", rect=(0, 0, 1, 0.98))


# ----- team rule: driving arc -----
def drive_point_panel(
    ax: Axes, c: Config, sheep: np.ndarray, centroid: np.ndarray, r_flock: float
) -> None:
    """The drive point Pd, a fixed offset behind the flock centre on the line to the goal."""
    goal = np.asarray(c["goal_center"])
    pd = drive_point(sheep, goal, c)
    ax.add_patch(
        Circle(
            xy(centroid),
            r_flock,
            fc=BLUE,
            alpha=0.15,
            ec=BLUE,
            lw=1.2,
            label=r"flock radius $R_{\mathrm{flock}}$ ($\sqrt{2}\times\mathrm{RMS}$)",
        )
    )
    ax.scatter(*sheep.T, s=14, color=BLUE, alpha=0.7, lw=0)
    gcm(ax, centroid, s=65, lw=2.0, text_at=(1.5, -3.5), fontsize=9, fontweight="bold")
    arrow(ax, centroid + unit(goal - centroid) * 32, centroid, AQUA, 2.0)
    bold_text(
        ax,
        centroid[0] + 16,
        centroid[1] + 3.0,
        r"toward the goal $\mathbf{x}_{\mathrm{goal}}$",
        AQUA,
    )
    ax.plot([centroid[0], pd[0]], [centroid[1], pd[1]], color=MUTED, ls=":", lw=1.2)
    ax.scatter(*pd, s=95, marker="x", color=INK, lw=2.2, zorder=5, label=r"drive point $P_d$")
    bold_text(ax, pd[0] - 2, pd[1] - 4.5, r"$P_d$ ($r_a\sqrt{N}$ behind the GCM)", INK, ha="center")
    mid = (centroid + pd) / 2.0
    ax.text(
        mid[0] - 3.5,
        mid[1] + 2.5,
        r"offset $r_a\sqrt{N} = 20$ m",
        color=MUTED,
        fontsize=8.5,
        ha="center",
    )
    ax.legend(loc="upper left", frameon=False, fontsize=8.5)
    window(ax, centroid, 35, 38, 28, 28)
    style_map(ax, "A. The drive point Pd (N = 100)")


def flank_label(ax: Axes, x: float, y: float, text: str) -> None:
    ax.text(x, y, text, color=AQUA, fontsize=8.5, fontstyle="italic")


def arc_panel(
    ax: Axes,
    c: Config,
    sheep: np.ndarray,
    dogs: np.ndarray,
    centroid: np.ndarray,
    r_flock: float,
) -> None:
    """The team's targets on an arc round the flock's sides, one dog to each slot."""
    goal = np.asarray(c["goal_center"])
    targets = team_targets(sheep, goal, dogs, c)
    ax.add_patch(Circle(xy(centroid), r_flock, fc=BLUE, alpha=0.10, ec=BLUE, lw=0.9, ls="--"))
    ax.scatter(*sheep.T, s=14, color=BLUE, alpha=0.6, lw=0)
    gcm(ax, centroid, label="GCM", s=50, lw=1.5, color=INK, zorder=3, text_at=(2, -3.5))
    ordered = targets[np.argsort(targets[:, 1])]
    for end in (ordered[0], ordered[-1]):
        ax.plot([centroid[0], end[0]], [centroid[1], end[1]], color=MUTED, ls=":", lw=0.9)
    ax.plot(
        *ordered.T,
        color=AQUA,
        lw=2.0,
        ls="-",
        label=r"driving arc (span $\pm\arcsin(R_{\mathrm{flock}}/R_{\mathrm{arc}})$)",
    )
    targets_at(ax, targets, s=65, lw=1.8, label="arc slots (angular order)")
    dogs_at(ax, dogs, s=70, lw=1.0, zorder=5, label="dogs ($D = 4$)")
    for i, (dog, tgt) in enumerate(zip(dogs, targets, strict=True)):
        arrow(ax, tgt, dog, ORANGE, 1.6)
        arrow(ax, tgt + unit(centroid - tgt) * 6, tgt, AQUA, 1.2, ls="--")
        dog_label(ax, dog, i)
    flank_label(ax, centroid[0] - 2, centroid[1] + r_flock + 5, "upper flank covered")
    flank_label(ax, centroid[0] - 2, centroid[1] - r_flock - 6, "lower flank covered")
    arrow(ax, goal - [c["goal_radius"] + 5, 0], centroid + [25, 0], AQUA, 1.5)
    bold_text(ax, centroid[0] + 27, centroid[1] + 2, "toward the goal", AQUA, 8.5)
    ax.legend(loc="upper left", frameon=False, fontsize=8.5)
    window(ax, centroid, 65, 55, 55, 55)
    style_map(ax, "B. Driving arc slots matched by angle")


def fig_driving_arc() -> None:
    """Drive point Pd (left) and the driving arc (right)."""
    c = cfg("compact", 100, 4)
    sheep, dogs = start(c)
    centroid = sheep.mean(axis=0)
    r_flock = radius_of(sheep, centroid)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.8))
    drive_point_panel(axes[0], c, sheep, centroid, r_flock)
    arc_panel(axes[1], c, sheep, dogs, centroid, r_flock)
    save(fig, "fig_driving_arc.png", rect=(0, 0, 1, 0.98))


# ----- task -----
def fig_layouts() -> None:
    """Four start layouts at N=200, same scale; dashed circle is f(N)."""
    n, d = 200, 4
    fig, axes = plt.subplots(2, 2, figsize=(10, 6.6))
    for ax, layout in zip(axes.flat, LAYOUTS, strict=True):
        c = cfg(layout, n, d)
        sheep, dogs = start(c)
        draw_scene(ax, c, sheep, dogs)
        center = np.asarray(c["flock_center"])
        f = collect_threshold(n, c["r_a"])
        ax.add_patch(Circle(xy(center), f, fc="none", ec=MUTED, lw=0.9, ls="--"))
        ax.text(center[0] - f * 0.72, center[1] + f * 0.78, "f(N)", color=MUTED, ha="center")
        window(ax, center, 150, 175, 150, 150)  # same window in every panel
        style_map(ax, layout)
    fig.text(0.01, 0.02, "sheep", color=BLUE)
    fig.text(0.07, 0.02, "dogs (D = 4)", color=ORANGE)
    fig.text(0.16, 0.02, "goal", color=AQUA)
    fig.text(0.21, 0.02, "dashed: collect distance f(N) = r_a N^(2/3)", color=MUTED)
    save(fig, "fig7_layouts.png", rect=(0, 0.04, 1, 0.98))


def dog_starts_note(ax: Axes) -> None:
    """The text panel that explains the three start modes."""
    ax.axis("off")
    ax.text(
        0.0,
        0.9,
        (
            "arcs: half circles behind the flock (base)\n"
            "ring: circles round the flock, less the\n    goal's cone\n"
            "handler: all dogs at one point behind,\n"
            "    as if released from a post"
        ),
        transform=ax.transAxes,
        color=MUTED,
        va="top",
        fontsize=9,
    )


def fig_dog_starts() -> None:
    """Dog starts: arcs by D (top) and arcs/ring/handler at D=8 (bottom)."""
    counts = (1, 2, 4, 8, 24, 64)
    modes = ("arcs", "ring", "handler")
    fig, axes = plt.subplots(2, 6, figsize=(13, 6.0))
    for ax, d in zip(axes[0], counts, strict=True):
        c = cfg("compact", 100, d)
        sheep, dogs = start(c)
        center = np.asarray(c["flock_center"])
        draw_scene(ax, c, sheep, dogs, goal_arrow=False)
        r = np.linalg.norm(dogs - center, axis=1).max() + 8
        window(ax, center, r, 35, r, r)
        style_map(ax, f"arcs, D = {d}")
    for ax, mode in zip(axes[1][:3], modes, strict=True):
        c = cfg("wide", 200, 8, settings={"dog_start": mode})
        sheep, dogs = start(c)
        draw_scene(ax, c, sheep, dogs, goal_arrow=False)
        window(ax, np.asarray(c["flock_center"]), 160, 160, 160, 160)
        style_map(ax, f"{mode}, wide, N = 200, D = 8")
    for ax in axes[1][4:]:
        ax.axis("off")
    dog_starts_note(axes[1][3])
    save(fig, "fig8_dog_starts.png", rect=(0, 0, 1, 0.98))


def record_trial(c: Config) -> tuple[dict[int, tuple[np.ndarray, np.ndarray]], np.ndarray, int]:
    """Run one trial; return sheep and dogs at every tick, the dogs' trail and the last tick."""
    state0 = initial_state(c, SEED)
    states = {0: (state0.sheep_positions.copy(), state0.shepherd_positions.copy())}
    path = [state0.shepherd_positions.copy()]

    def keep(state: SimulationState) -> None:
        path.append(state.shepherd_positions.copy())
        states[state.tick] = (state.sheep_positions.copy(), state.shepherd_positions.copy())

    result = run_trial(c, SEED, on_tick=keep, history=False)
    return states, np.array(path), result.total_ticks  # trail is (ticks + 1, D, 2)


def fig_trial() -> None:
    """Real trial wide N=200, D=4, seed 2026: collect then drive."""
    n, d = 200, 4
    c = cfg("wide", n, d, ticks=1500)
    states, trail, last = record_trial(c)
    goal = np.asarray(c["goal_center"])
    centre = np.asarray(c["flock_center"])
    fig, axes = plt.subplots(2, 2, figsize=(10, 6.2))
    for ax, tick in zip(axes.flat, (0, last // 5, last // 2, last), strict=True):
        sheep, dogs = states[tick]
        ax.add_patch(Circle(xy(goal), c["goal_radius"], fc="none", ec=AQUA, lw=1.5))
        for j in range(d):
            ax.plot(*trail[: tick + 1, j].T, color=ORANGE, lw=0.7, alpha=0.6)
        ax.scatter(*sheep.T, s=7, color=BLUE, alpha=0.85, lw=0)
        dogs_at(ax, dogs)
        ax.set_xlim(centre[0] - 150, goal[0] + 40)
        ax.set_ylim(centre[1] - 130, centre[1] + 130)
        style_map(ax, f"tick {tick}")
    save(fig, "fig17_trial.png", rect=(0, 0, 1, 0.98))


# ----- task geometry -----
def start_reach(c: Config) -> float:
    """The farthest a sheep can start, over every layout of the protocol."""
    return max(layout_extent({**c, "initial_layout": k}) for k in LAYOUTS)


def field_panel(ax: Axes, c: Config, n: int) -> None:
    """The field to scale: start region, flock radius, goal and the drive between them."""
    centre = np.asarray(c["flock_center"])
    goal = np.asarray(c["goal_center"])
    rf = c["flock_radius"]
    r_goal = c["goal_radius"]
    reach = start_reach(c)
    from matplotlib.colors import to_rgb

    ax.add_patch(Rectangle((0, 0), c["world_width"], c["world_height"], fc="none", ec=GRID, lw=1.0))
    ax.add_patch(
        Circle(xy(centre), reach, fc=(*to_rgb(BLUE), 0.08), ec=BLUE, lw=1.0, ls="--", zorder=1)
    )
    sheep = place_flock({**c, "initial_layout": "compact"}, np.random.default_rng(SEED))
    ax.scatter(*sheep.T, s=5, color=BLUE, alpha=0.45, lw=0, zorder=2)
    ax.add_patch(Circle(xy(centre), rf, fc="none", ec=INK, lw=1.4, zorder=4))
    ax.scatter(*centre, s=35, marker="+", color=INK, lw=1.2, zorder=5)
    ax.add_patch(Circle(xy(goal), r_goal, fc="none", ec=AQUA, lw=1.6, zorder=4))
    ax.scatter(*goal, s=35, marker="+", color=AQUA, lw=1.2, zorder=5)
    below = centre[1] - reach - 28
    ax.plot([centre[0], centre[0]], [centre[1], below], color=MUTED, lw=0.7, ls=":")
    ax.plot([goal[0], goal[0]], [goal[1], below], color=MUTED, lw=0.7, ls=":")
    arrow(ax, (goal[0], below), (centre[0], below), INK, 1.0, style="<->")
    ax.text(
        (centre[0] + goal[0]) / 2,
        below - 18,
        f"drive distance l = {goal[0] - centre[0]:.1f} m",
        ha="center",
        color=INK,
    )
    angle_rf = -np.pi / 4
    ax.annotate(
        f"R_f = {rf:.1f} m\n(settled flock radius)",
        xy=(centre[0] + rf * np.cos(angle_rf), centre[1] + rf * np.sin(angle_rf)),
        xytext=(centre[0] + 22, centre[1] - 68),
        color=INK,
        fontsize=8.5,
        arrowprops=dict(arrowstyle="->", color=INK, lw=0.9),
    )
    angle_reach = 2.35
    ax.annotate(
        f"l_reach = {reach:.1f} m\nmax start radius (outlier_rich)",
        xy=(centre[0] + reach * np.cos(angle_reach), centre[1] + reach * np.sin(angle_reach)),
        xytext=(centre[0] - reach - 15, centre[1] + reach + 18),
        color=BLUE,
        fontsize=8.5,
        arrowprops=dict(arrowstyle="->", color=BLUE, lw=0.9),
    )
    ax.text(
        goal[0],
        goal[1] + r_goal + 10,
        f"R_goal = {r_goal:.1f} m\n({GOAL_MULTIPLE} R_f)",
        ha="center",
        color=AQUA,
        fontsize=8.5,
    )
    ax.text(
        c["world_width"],
        c["world_height"] + 6,
        f"field {c['world_width']:.0f} x {c['world_height']:.0f} m (open, no boundary)",
        ha="right",
        color=MUTED,
        fontsize=8,
    )
    ax.set_xlim(-10, c["world_width"] + 10)
    ax.set_ylim(-10, c["world_height"] + 24)
    style_map(ax, f"the task to scale, N = {n}")


def drive_length_panel(ax: Axes, configs: Sequence[Config]) -> None:
    """The drive length used, against the three terms it is the largest of."""
    actual = [float(c["goal_center"][0] - c["flock_center"][0]) for c in configs]
    from_radius = [DRIVE_MULTIPLE * c["flock_radius"] for c in configs]
    from_reach = [start_reach(c) + c["goal_radius"] + c["flock_radius"] for c in configs]
    ax.plot(
        NS, actual, color=INK, lw=5, alpha=0.25, solid_capstyle="round", label="drive length used"
    )
    ax.plot(NS, from_radius, color=BLUE, lw=1.6, marker="o", ms=3, label=f"{DRIVE_MULTIPLE:g} R_f")
    ax.plot(
        NS,
        [DRIVE_FLOOR] * len(configs),
        color=MUTED,
        lw=1.2,
        ls="--",
        label=f"minimum {DRIVE_FLOOR:g}",
    )
    ax.plot(NS, from_reach, color=ORANGE, lw=1.6, marker="o", ms=3, label="l_reach + R_goal + R_f")
    n_axis(ax)
    ax.set_ylabel("length (m)")
    ax.set_title("drive length: the largest of three terms")
    grid(ax, axis="y")
    ax.legend(frameon=False, fontsize=8, loc="upper left")


def radii_panel(ax: Axes, configs: Sequence[Config]) -> None:
    """Flock radius and goal radius against N."""
    radii = [c["flock_radius"] for c in configs]
    ax.plot(
        NS,
        [GOAL_MULTIPLE * r for r in radii],
        color=AQUA,
        lw=1.6,
        marker="o",
        ms=3,
        label=f"goal radius {GOAL_MULTIPLE} R_f",
    )
    ax.plot(NS, radii, color=BLUE, lw=1.6, marker="o", ms=3, label="flock radius R_f")
    n_axis(ax)
    ax.set_ylabel("length (m)")
    ax.set_title("flock radius and goal radius")
    ax.set_ylim(0, GOAL_MULTIPLE * max(radii) * 1.1)
    grid(ax, axis="y")
    ax.legend(frameon=False, fontsize=8, loc="upper left")


def fig_task_geometry() -> None:
    """Task geometry: field to scale, drive-length terms, and radii against N."""
    n, max_dogs = 200, 24
    fig = plt.figure(figsize=(13, 5.4))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.5, 1, 1])
    field_panel(fig.add_subplot(gs[0, 0]), field_config(n, max_dogs), n)
    configs = [field_config(k, max_dogs) for k in NS]
    drive_length_panel(fig.add_subplot(gs[0, 1]), configs)
    radii_panel(fig.add_subplot(gs[0, 2]), configs)
    save(fig, "fig6_task_geometry.png", rect=(0, 0, 1, 0.98))


# ----- frontier values -----
# An invented curve: D -> (reliable, median finish s, zone).
EXAMPLE_CURVE = {
    1: (False, None, TOO_FEW),
    2: (True, 400, IMPROVING),
    3: (True, 300, IMPROVING),
    4: (True, 250, SATURATED),
    5: (True, 245, SATURATED),
    6: (True, 290, CROWDED),
    7: (False, None, COLLAPSE),
    8: (False, None, COLLAPSE),
}
# Its frontier values. D_best, D_sat and D_crowd rest on paired finish-time verdicts, which an
# invented curve has no trials for, so the values are stated with the curve, not derived.
EXAMPLE_VALUES = {"D_min": 2, "D_best = D_sat": 4, "D_crowd = D_max": 6, "D_overcrowd": 7}


def fig_zones() -> None:
    """An invented curve: zones and frontier values along D."""
    ds = list(EXAMPLE_CURVE)
    fig, (top, bottom) = plt.subplots(2, 1, figsize=(7.5, 4.2), sharex=True)
    for d, (reliable, _, zone) in EXAMPLE_CURVE.items():
        top.bar(d, 1, color=ZONE_COLOR[zone], alpha=0.85, width=0.8)
        top.text(
            d,
            0.5,
            zone.replace("_", " "),
            ha="center",
            va="center",
            fontsize=7.5,
            color=SURFACE,
            rotation=90,
        )
        top.text(
            d,
            1.08,
            "reliable" if reliable else "not",
            ha="center",
            fontsize=7.5,
            color=INK if reliable else RED,
        )
    top.set_ylim(0, 1.25)
    top.set_yticks([])
    top.spines["left"].set_visible(False)
    times = [(d, t) for d, (_, t, _) in EXAMPLE_CURVE.items() if t is not None]
    bottom.plot(*zip(*times, strict=True), color=INK, marker="o", ms=4)
    bottom.set_ylabel("median finish (s)")
    bottom.set_ylim(200, 430)
    for label, d in EXAMPLE_VALUES.items():
        bottom.axvline(d, color=MUTED, lw=0.8, ls=":")
        bottom.text(d + 0.06, 205, label, fontsize=7.5, color=MUTED, rotation=90, va="bottom")
    bottom.set_xticks(ds)
    bottom.set_xlabel("dogs D")
    grid(bottom, "y")
    save(fig, "def_D_zones.png")
