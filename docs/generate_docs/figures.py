"""Model and task figures for make_figures.py.

Scene helpers first, then figures by topic (models, team rule, task). Style in figstyle.py.
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Rectangle

from analysis.results import flock_radii
from docs.generate_docs.figstyle import (
    AQUA,
    BLUE,
    GRID,
    INK,
    MUTED,
    NS,
    ORANGE,
    REPO,
    SURFACE,
    grid,
    n_axis,
    save,
)
from services.cells import Cell, Group, cell_config
from services.protocol import load_protocol
from sim.core.simulation_runner import initial_state, run_trial
from sim.core.simulation_state import SimulationState
from sim.core.vectors import unit
from sim.core.world.layouts import layout_extent, place_dogs, place_flock
from sim.methods.strombom.config import PAPER
from sim.methods.strombom.heuristics import collect_threshold, drive_point, radius_of
from sim.plugins.dogs.collect_drive_multi import team_targets
from tests.helpers import config_for

# ----- settings -----
Config = dict[str, Any]  # a run config, as cell_config and config_for build it
Point = Sequence[float] | np.ndarray

R_S = PAPER["r_s"]
SEED = 2026  # every scene starts from the same flock
RED = "#d9534f"  # the one extra colour: personal space and the crossing assignment


def calibrated(protocol: str) -> dict[int, float]:
    """Flock radii from results/<protocol>/calibration.json."""
    radii = flock_radii(REPO / "results" / protocol)["strombom_multi"]
    return {int(n): float(r) for n, r in radii.items()}


# Calibrated flock radii of the Strombom sheep, from the main run.
RF = calibrated("dmin_m12")


def cfg(layout: str, n: int, d: int, **kw: Any) -> Config:
    return config_for("strombom_multi", n=n, d=d, layout=layout, flock_radius=RF[n], **kw)


def start(c: Config) -> tuple[np.ndarray, np.ndarray]:
    """Sheep and dogs at trial start on the shared seed."""
    return place_flock(c, np.random.default_rng(SEED)), place_dogs(c)


def field_config(n: int, max_dogs: int) -> Config:
    """dmin cell config whose field fits all four layouts and ``max_dogs`` dogs."""
    from dataclasses import replace

    protocol = load_protocol("dmin_m12", output=Path("/tmp/herdsim-figures"))
    protocol = replace(protocol, shepherd_counts=(1, max_dogs))
    return cell_config(protocol, Cell(Group("strombom_multi", "wide", (), n), max_dogs), RF[n])


# ----- drawing helpers -----
def xy(point: Point) -> tuple[float, float]:
    """Point as an (x, y) tuple for matplotlib patches."""
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
    """Set axes limits around ``centre`` by left/right/down/up offsets."""
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


# ----- models -----
def fig_sheep_forces() -> None:
    """Strombom (2014) sheep forces: interaction geometry (left) and weighted sum (right)."""
    focal = np.array([0.0, 0.0])
    flock_neighbors = np.array(
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
    close_neighbor = np.array([1.2, 0.9])
    dog = np.array([-25.0, -20.0])
    lcm = np.vstack([flock_neighbors, close_neighbor]).mean(axis=0)
    # the paper's weights, and the unit vector each one multiplies
    h, c, rho_a, rho_s, e = (
        PAPER[k] for k in ("inertia", "c", "rho_a", "rs_weight", "noise_strength")
    )
    H_i = unit(np.array([0.5, 0.85]))
    C_i = unit(lcm - focal)
    R_a = unit(focal - close_neighbor)
    R_s = unit(focal - dog)
    eps = unit(np.array([-0.8, 0.5]))
    H_prime = h * H_i + c * C_i + rho_a * R_a + rho_s * R_s + e * eps
    scale = 12.0  # arrow length per unit of weighted force

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.8))
    ax0 = axes[0]
    ax0.add_patch(
        Circle(
            (0, 0),
            R_S,
            fc=ORANGE,
            alpha=0.04,
            ec=ORANGE,
            lw=1.0,
            ls="--",
            label=f"Threat detection $r_s = {R_S:g}$ m",
        )
    )
    ax0.add_patch(
        Circle((0, 0), 2.0, fc=RED, alpha=0.25, ec=RED, lw=1.2, label="Personal space $r_a = 2$ m")
    )
    ax0.scatter(*flock_neighbors.T, s=35, color=BLUE, alpha=0.75, lw=0, label="Flock-mates")
    ax0.scatter(
        *close_neighbor,
        s=50,
        color=RED,
        ec=INK,
        lw=0.9,
        zorder=4,
        label=r"Intruding neighbor ($< r_a$)",
    )
    ax0.scatter(*focal, s=85, color=INK, zorder=5, label="Focal sheep $i$")
    ax0.text(focal[0] + 1.5, focal[1] - 3.2, "Sheep $i$", color=INK, fontsize=9, fontweight="bold")
    ax0.scatter(
        *lcm, s=75, marker="+", color=AQUA, lw=2.2, zorder=4, label="Local Center of Mass (LCM)"
    )
    ax0.text(
        lcm[0] + 2.0, lcm[1] - 1.0, r"$\mathrm{LCM}_i$", color=AQUA, fontsize=9, fontweight="bold"
    )
    dogs_at(ax0, dog, s=95, lw=1.0, zorder=5, label=r"Shepherd dog ($< r_s$)")
    ax0.text(
        dog[0] - 2.0, dog[1] - 4.5, r"Dog ($< r_s$)", color=ORANGE, fontsize=9, fontweight="bold"
    )
    ax0.set_xlim(-40, 45)
    ax0.set_ylim(-35, 45)
    ax0.legend(loc="upper left", frameon=False, fontsize=8)
    style_map(ax0, "A. Biological interaction geometry on open pasture")

    ax1 = axes[1]
    # (legend label, weighted vector, colour, weight note, tip label, tip label offset)
    vectors = [
        (
            r"1. Momentum $h\,\mathbf{H}_i$",
            h * H_i,
            BLUE,
            f"weight h = {h}",
            r"$h\,\mathbf{H}_i$",
            (0.5, 1.0),
        ),
        (
            r"2. Social Cohesion $c\,\mathbf{C}_i$",
            c * C_i,
            AQUA,
            f"weight c = {c}",
            r"$c\,\mathbf{C}_i$",
            (1.0, 0),
        ),
        (
            r"3. Avoidance $\rho_a\,\mathbf{R}_{a,i}$",
            rho_a * R_a,
            RED,
            f"weight $\\rho_a$ = {rho_a} (highest)",
            r"$\rho_a\,\mathbf{R}_{a,i}$",
            (-2.0, -2.0),
        ),
        (
            r"4. Predator Escape $\rho_s\,\mathbf{R}_{s,i}$",
            rho_s * R_s,
            ORANGE,
            f"weight $\\rho_s$ = {rho_s}",
            r"$\rho_s\,\mathbf{R}_{s,i}$",
            (1.0, 0),
        ),
        (
            r"5. Noise $e\,\mathbf{\epsilon}_i$",
            e * eps,
            MUTED,
            f"weight e = {e}",
            r"$e\,\mathbf{\epsilon}_i$",
            (-2.0, 1.0),
        ),
    ]
    handles = []
    for label, vec, color, note, _, _ in vectors:
        arrow(ax1, vec * scale, (0, 0), color, 2.2)
        handles.append(Line2D([0], [0], color=color, lw=2.2, label=f"{label} ({note})"))
    tip_res = H_prime * (scale * 0.42)
    arrow(ax1, tip_res, (0, 0), INK, 3.2, style="-|>")
    handles.append(
        Line2D(
            [0],
            [0],
            color=INK,
            lw=3.2,
            label=(
                r"Resultant Heading $\mathbf{H}_i'$ "
                r"($\mathbf{x}_i^{t+1} = \mathbf{x}_i^t + \delta\,\mathbf{H}_i' / "
                r"\|\mathbf{H}_i'\|$)"
            ),
        )
    )
    ax1.scatter(0, 0, s=70, color=INK, zorder=5)
    ax1.text(0, -2.5, "Sheep $i$", color=INK, fontsize=9, fontweight="bold", ha="center")
    for _, vec, color, _, tip_label, (dx, dy) in vectors:
        ax1.text(
            vec[0] * scale + dx,
            vec[1] * scale + dy,
            tip_label,
            color=color,
            fontsize=9,
            fontweight="bold",
        )
    ax1.text(
        tip_res[0] + 1.2,
        tip_res[1] - 1.2,
        r"$\mathbf{H}_i'$ (Resultant)",
        color=INK,
        fontsize=9.5,
        fontweight="bold",
    )
    ax1.legend(handles=handles, loc="lower left", frameon=False, fontsize=8)
    ax1.set_xlim(-30, 25)
    ax1.set_ylim(-30, 20)
    style_map(ax1, r"B. 5 competing instinct forces and Resultant heading $\mathbf{H}_i'$")
    save(fig, "fig_sheep_forces.png", rect=(0, 0, 1, 0.98))


# ----- team rule -----
def fig_team_rule() -> None:
    """Team rule from D=1 to 8: collect (wide) and drive (compact)."""
    counts = (1, 2, 4, 8)
    rows = (("wide", 200), ("compact", 200))
    fig, axes = plt.subplots(2, 4, figsize=(13, 7.0))
    for col, d in enumerate(counts):
        for row, (layout, n) in enumerate(rows):
            c = cfg(layout, n, d)
            sheep, dogs = start(c)
            targets = team_targets(sheep, np.asarray(c["goal_center"]), dogs, c)
            centroid = sheep.mean(axis=0)
            ax = axes[row, col]
            far = np.linalg.norm(sheep - centroid, axis=1) > collect_threshold(n, c["r_a"])
            flock_split(ax, sheep, far, s_in=7, s_out=14, lw_out=0.5)
            dogs_at(ax, dogs)
            targets_at(ax, targets, s=22, lw=1.1, zorder=3)
            if row == 1 and d > 1:  # the drive slots lie on an arc; a thin line makes them readable
                ordered = targets[np.argsort(targets[:, 1])]
                ax.plot(*ordered.T, color=INK, lw=0.5, alpha=0.4, zorder=2)
            for dog, target in zip(dogs, targets):
                arrow(ax, target, dog, ORANGE, 0.9)
            job = "collect" if row == 0 else "drive"
            if row == 0:
                window(ax, centroid, 185, 115, 170, 170)
            else:
                window(ax, centroid, 80, 35, 70, 70)
            style_map(ax, f"{job}, D = {d}" + ("  (the paper)" if d == 1 else ""))
    save(fig, "fig3_team_rule.png", rect=(0, 0, 1, 0.98))


def fig_hungarian_matching() -> None:
    """Outliers and Pc (left); Hungarian matching vs a crossing assignment (right)."""
    n, d = 100, 4
    c = cfg("wide", n, d)
    sheep, dogs = start(c)
    goal = np.asarray(c["goal_center"])
    centroid = sheep.mean(axis=0)
    thresh = collect_threshold(n, c["r_a"])
    dists = np.linalg.norm(sheep - centroid, axis=1)
    far = dists > thresh
    stray = sheep[np.argsort(dists)[::-1][0]]
    # drawn four times farther out than the real r_a, or the cross would sit on the sheep
    pc_pos = stray + float(c["r_a"]) * 4.0 * unit(stray - centroid)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.8))

    ax0 = axes[0]
    ax0.add_patch(
        Circle(
            xy(centroid),
            thresh,
            fc=BLUE,
            alpha=0.04,
            ec=MUTED,
            lw=1.2,
            ls="--",
            label=r"threshold $f(N) = r_a N^{2/3}$",
        )
    )
    flock_split(
        ax0,
        sheep,
        far,
        s_in=18,
        s_out=30,
        lw_out=0.8,
        labels=("sheep inside the flock", r"outliers ($> f(N)$)"),
    )
    gcm(
        ax0,
        centroid,
        label="GCM (flock centre)",
        s=65,
        lw=2.0,
        zorder=5,
        text_at=(3, -4),
        fontsize=9,
        fontweight="bold",
    )
    arrow(ax0, pc_pos, centroid, MUTED, 1.0, ls=":")
    ax0.scatter(*stray, s=95, facecolors="none", ec=ORANGE, lw=1.8, zorder=4)
    ax0.text(
        stray[0] + 3, stray[1] - 2, r"outlier $o$", color=ORANGE, fontsize=9.5, fontweight="bold"
    )
    ax0.scatter(*pc_pos, s=90, marker="x", color=INK, lw=2.2, zorder=5)
    ax0.text(
        pc_pos[0] + 3,
        pc_pos[1] + 3,
        r"collect point $P_c$" + "\n" + r"($r_a = 2$ m behind, drawn 4x)",
        color=INK,
        fontsize=9,
        fontweight="bold",
    )
    ax0.text(
        centroid[0] - thresh * 0.72,
        centroid[1] + thresh * 0.72,
        r"flock region: $f(N) = r_a N^{2/3}$",
        color=MUTED,
        fontsize=8.5,
    )
    ax0.legend(loc="lower left", frameon=False, fontsize=8.5)
    window(ax0, centroid, 130, 90, 110, 110)
    style_map(ax0, "A. outliers and the collect point Pc")

    ax1 = axes[1]
    targets = team_targets(sheep, goal, dogs, c)
    flock_split(ax1, sheep, far, s_in=15, s_out=28, lw_out=0.6, alpha_in=0.5)
    gcm(ax1, centroid, label=None, s=50, lw=1.5, color=MUTED, zorder=3)
    dogs_at(ax1, dogs, s=70, lw=1.0, zorder=5, label="dogs ($D = 4$)")
    targets_at(ax1, targets, s=65, lw=1.8, zorder=5, label="collect points $P_{c,1..4}$")
    for dog, tgt in zip(dogs, targets):
        arrow(ax1, tgt, dog, ORANGE, 1.8)
    ax1.plot(
        [dogs[0, 0], targets[2, 0]],
        [dogs[0, 1], targets[2, 1]],
        color=RED,
        ls="--",
        lw=1.0,
        alpha=0.45,
        label="a crossing assignment (drawn by hand)",
    )
    ax1.plot(
        [dogs[2, 0], targets[0, 0]],
        [dogs[2, 1], targets[0, 1]],
        color=RED,
        ls="--",
        lw=1.0,
        alpha=0.45,
    )
    for i, dog in enumerate(dogs):
        ax1.text(
            dog[0] - 16, dog[1] - 2, f"dog {i + 1}", color=ORANGE, fontsize=8.5, fontweight="bold"
        )
    ax1.legend(loc="lower left", frameon=False, fontsize=8.5)
    window(ax1, centroid, 130, 90, 110, 110)
    style_map(ax1, "B. Hungarian assignment: no two paths cross")
    save(fig, "fig_hungarian_matching.png", rect=(0, 0, 1, 0.98))


def fig_driving_arc() -> None:
    """Drive point Pd (left) and the driving arc (right)."""
    c = cfg("compact", 100, 4)
    sheep, dogs = start(c)
    goal = np.asarray(c["goal_center"])
    centroid = sheep.mean(axis=0)
    r_flock = radius_of(sheep, centroid)
    pd = drive_point(sheep, goal, c)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.8))

    ax0 = axes[0]
    ax0.add_patch(
        Circle(
            xy(centroid),
            r_flock,
            fc=BLUE,
            alpha=0.15,
            ec=BLUE,
            lw=1.2,
            label=r"the flock ($R_{\mathrm{flock}} \propto r_a\sqrt{N}$)",
        )
    )
    ax0.scatter(*sheep.T, s=14, color=BLUE, alpha=0.7, lw=0)
    gcm(ax0, centroid, s=65, lw=2.0, text_at=(1.5, -3.5), fontsize=9, fontweight="bold")
    arrow(ax0, centroid + unit(goal - centroid) * 32, centroid, AQUA, 2.0)
    ax0.text(
        centroid[0] + 16,
        centroid[1] + 3.0,
        r"toward the goal $\mathbf{x}_{\mathrm{goal}}$",
        color=AQUA,
        fontsize=9,
        fontweight="bold",
    )
    ax0.plot([centroid[0], pd[0]], [centroid[1], pd[1]], color=MUTED, ls=":", lw=1.2)
    ax0.scatter(*pd, s=95, marker="x", color=INK, lw=2.2, zorder=5, label=r"drive point $P_d$")
    ax0.text(
        pd[0] - 2,
        pd[1] - 4.5,
        r"$P_d$ ($r_a\sqrt{N}$ behind the GCM)",
        color=INK,
        fontsize=9,
        fontweight="bold",
        ha="center",
    )
    mid = (centroid + pd) / 2.0
    ax0.text(
        mid[0] - 1.5,
        mid[1] + 2.5,
        r"offset $r_a\sqrt{N} = 20$ m",
        color=MUTED,
        fontsize=8.5,
        ha="center",
    )
    ax0.legend(loc="upper left", frameon=False, fontsize=8.5)
    window(ax0, centroid, 35, 38, 28, 28)
    style_map(ax0, "A. the drive point Pd")

    ax1 = axes[1]
    targets_arc = team_targets(sheep, goal, dogs, c)
    ax1.scatter(*sheep.T, s=14, color=BLUE, alpha=0.6, lw=0)
    gcm(ax1, centroid, label=None, s=50, lw=1.5, color=MUTED, zorder=3)
    ordered_arc = targets_arc[np.argsort(targets_arc[:, 1])]
    ax1.plot(*ordered_arc.T, color=AQUA, lw=2.0, ls="-", label="driving arc")
    targets_at(ax1, targets_arc, s=65, lw=1.8, label="arc slots")
    dogs_at(ax1, dogs, s=70, lw=1.0, zorder=5, label="dogs ($D = 4$)")
    for i, (dog, tgt) in enumerate(zip(dogs, targets_arc)):
        arrow(ax1, tgt, dog, ORANGE, 1.6)
        arrow(ax1, tgt + unit(centroid - tgt) * 6, tgt, AQUA, 1.2, ls="--")
        ax1.text(
            dog[0] - 16, dog[1] - 2, f"dog {i + 1}", color=ORANGE, fontsize=8.5, fontweight="bold"
        )
    ax1.text(
        centroid[0] + 2,
        centroid[1] + r_flock + 2,
        "upper flank covered",
        color=AQUA,
        fontsize=8.5,
        fontstyle="italic",
    )
    ax1.text(
        centroid[0] + 2,
        centroid[1] - r_flock - 4,
        "lower flank covered",
        color=AQUA,
        fontsize=8.5,
        fontstyle="italic",
    )
    arrow(ax1, goal - [c["goal_radius"] + 5, 0], centroid + [25, 0], AQUA, 1.5)
    ax1.text(
        centroid[0] + 27,
        centroid[1] + 2,
        "toward the goal",
        color=AQUA,
        fontsize=8.5,
        fontweight="bold",
    )
    ax1.legend(loc="upper left", frameon=False, fontsize=8.5)
    window(ax1, centroid, 65, 55, 55, 55)
    style_map(ax1, "B. the driving arc round the flock's sides")
    save(fig, "fig_driving_arc.png", rect=(0, 0, 1, 0.98))


# ----- task -----
def fig_layouts() -> None:
    """Four start layouts at N=200, same scale; dashed circle is f(N)."""
    n, d = 200, 4
    fig, axes = plt.subplots(2, 2, figsize=(10, 6.6))
    for ax, layout in zip(axes.flat, ("compact", "wide", "split", "outlier_rich")):
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


def fig_dog_starts() -> None:
    """Dog starts: arcs by D (top) and arcs/ring/handler at D=8 (bottom)."""
    counts = (1, 2, 4, 8, 24, 64)
    modes = ("arcs", "ring", "handler")
    fig, axes = plt.subplots(2, 6, figsize=(13, 6.0))
    for ax, d in zip(axes[0], counts):
        c = cfg("compact", 100, d)
        sheep, dogs = start(c)
        center = np.asarray(c["flock_center"])
        draw_scene(ax, c, sheep, dogs, goal_arrow=False)
        r = np.linalg.norm(dogs - center, axis=1).max() + 8
        window(ax, center, r, 35, r, r)
        style_map(ax, f"arcs, D = {d}")
    for ax, mode in zip(axes[1][:3], modes):
        c = cfg("wide", 200, 8, settings={"dog_start": mode})
        sheep, dogs = start(c)
        center = np.asarray(c["flock_center"])
        draw_scene(ax, c, sheep, dogs, goal_arrow=False)
        window(ax, center, 160, 160, 160, 160)
        style_map(ax, f"{mode}, wide, N = 200, D = 8")
    for ax in axes[1][3:]:
        ax.axis("off")
    axes[1][3].text(
        0.0,
        0.9,
        (
            "arcs: half circles behind the flock (base)\n"
            "ring: circles round the flock, less the\n    goal's cone\n"
            "handler: all dogs at one point behind,\n"
            "    as if released from a post"
        ),
        transform=axes[1][3].transAxes,
        color=MUTED,
        va="top",
        fontsize=9,
    )
    save(fig, "fig8_dog_starts.png", rect=(0, 0, 1, 0.98))


def fig_trial() -> None:
    """Real trial wide N=200, D=4, seed 2026: collect then drive."""
    n, d = 200, 4
    c = cfg("wide", n, d, ticks=1500)
    states: dict[int, tuple[np.ndarray, np.ndarray]] = {}
    path: list[np.ndarray] = []
    state0 = initial_state(c, SEED)
    states[0] = (state0.sheep_positions.copy(), state0.shepherd_positions.copy())
    path.append(state0.shepherd_positions.copy())

    def keep(state: SimulationState) -> None:
        path.append(state.shepherd_positions.copy())
        states[state.tick] = (state.sheep_positions.copy(), state.shepherd_positions.copy())

    result = run_trial(c, SEED, on_tick=keep)
    last = result.total_ticks
    shots = [0, last // 5, last // 2, last]
    fig, axes = plt.subplots(2, 2, figsize=(10, 6.2))
    trail = np.array(path)  # (ticks + 1, D, 2)
    goal = np.asarray(c["goal_center"])
    centre = np.asarray(c["flock_center"])
    for ax, tick in zip(axes.flat, shots):
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


def fig_task_geometry() -> None:
    """Task geometry: field to scale, drive-length terms, and radii against N."""
    n, max_dogs = 200, 24
    layouts = ("compact", "wide", "split", "outlier_rich")
    drive_multiple, drive_floor = 13.0, 80.0  # the drive length's first two terms
    goal_multiple = 1.9  # goal radius in flock radii

    def reach_of(cc: Config) -> float:
        """The farthest a sheep can start, over every layout of the protocol."""
        return max(layout_extent({**cc, "initial_layout": k}) for k in layouts)

    c = field_config(n, max_dogs)
    fig = plt.figure(figsize=(13, 5.4))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.5, 1, 1])

    ax = fig.add_subplot(gs[0, 0])
    centre = np.asarray(c["flock_center"])
    goal = np.asarray(c["goal_center"])
    rf = c["flock_radius"]
    reach = reach_of(c)
    ax.add_patch(Rectangle((0, 0), c["world_width"], c["world_height"], fc="none", ec=GRID, lw=1.0))
    ax.add_patch(Circle(xy(centre), reach, fc=BLUE, ec="none", alpha=0.10))
    ax.add_patch(Circle(xy(centre), rf, fc="none", ec=BLUE, lw=1.0, ls=":"))
    sheep = place_flock({**c, "initial_layout": "compact"}, np.random.default_rng(SEED))
    ax.scatter(*sheep.T, s=7, color=BLUE, lw=0)
    ax.add_patch(Circle(xy(goal), c["goal_radius"], fc="none", ec=AQUA, lw=1.6))
    drive = float(goal[0] - centre[0])
    arrow(
        ax,
        (goal[0], centre[1] - reach - 28),
        (centre[0], centre[1] - reach - 28),
        INK,
        1.0,
        style="<->",
    )
    ax.text(
        (centre[0] + goal[0]) / 2,
        centre[1] - reach - 46,
        f"drive length {drive:.0f}",
        ha="center",
        color=INK,
    )
    ax.annotate(
        f"R_f = {rf:.1f}",
        xy=(centre[0] + rf * 0.71, centre[1] - rf * 0.71),
        xytext=(centre[0] + 25, centre[1] - 60),
        color=BLUE,
        arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.7),
    )
    ax.annotate(
        f"farthest start sheep, {reach:.0f}\n(widest layout)",
        xy=(centre[0] - reach * 0.71, centre[1] + reach * 0.71),
        xytext=(centre[0] - reach - 10, centre[1] + reach + 22),
        color=BLUE,
        arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.7),
    )
    ax.text(
        goal[0],
        goal[1] + c["goal_radius"] + 8,
        f"goal {c['goal_radius']:.1f} = 1.9 R_f",
        ha="center",
        color=AQUA,
    )
    ax.text(
        c["world_width"],
        c["world_height"] + 6,
        f"field {c['world_width']:.0f} x {c['world_height']:.0f}, places the start, no boundary",
        ha="right",
        color=MUTED,
        fontsize=8,
    )
    ax.set_xlim(-10, c["world_width"] + 10)
    ax.set_ylim(-10, c["world_height"] + 24)
    style_map(ax, f"the task to scale, N = {n}")

    configs = [field_config(k, max_dogs) for k in NS]
    t1 = [drive_multiple * ck["flock_radius"] for ck in configs]
    t2 = [drive_floor for _ in configs]
    t3 = [reach_of(ck) + ck["goal_radius"] + ck["flock_radius"] for ck in configs]
    actual = [float(ck["goal_center"][0] - ck["flock_center"][0]) for ck in configs]
    ax = fig.add_subplot(gs[0, 1])
    ax.plot(
        NS, actual, color=INK, lw=5, alpha=0.25, solid_capstyle="round", label="drive length used"
    )
    ax.plot(NS, t1, color=BLUE, lw=1.6, marker="o", ms=3, label="13 R_f")
    ax.plot(NS, t2, color=MUTED, lw=1.2, ls="--", label="minimum 80")
    ax.plot(NS, t3, color=ORANGE, lw=1.6, marker="o", ms=3, label="reach + goal radius + R_f")
    n_axis(ax)
    ax.set_ylabel("length (units)")
    ax.set_title("drive length: the largest of three terms")
    grid(ax, axis="y")
    ax.legend(frameon=False, fontsize=8, loc="upper left")

    ax = fig.add_subplot(gs[0, 2])
    radii = [ck["flock_radius"] for ck in configs]
    ax.plot(
        NS,
        [goal_multiple * r for r in radii],
        color=AQUA,
        lw=1.6,
        marker="o",
        ms=3,
        label="goal radius 1.9 R_f",
    )
    ax.plot(NS, radii, color=BLUE, lw=1.6, marker="o", ms=3, label="flock radius R_f")
    n_axis(ax)
    ax.set_ylabel("length (units)")
    ax.set_title("flock radius and goal radius")
    ax.set_ylim(0, goal_multiple * max(radii) * 1.1)
    grid(ax, axis="y")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    save(fig, "fig6_task_geometry.png", rect=(0, 0, 1, 0.98))
