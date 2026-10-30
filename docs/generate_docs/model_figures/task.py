"""The start layouts, dog starts, one real trial and the geometry of the drive task."""

from __future__ import annotations

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Circle, Rectangle

from docs.generate_docs.figstyle import (
    AQUA,
    BLUE,
    GRID,
    INK,
    MUTED,
    ORANGE,
    grid,
    save,
)
from docs.generate_docs.model_figures.scene import (
    NS,
    SEED,
    Config,
    arrow,
    cfg,
    dogs_at,
    draw_scene,
    field_config,
    n_axis,
    start,
    style_map,
    window,
    xy,
)
from sim.core.simulation_runner import initial_state, run_trial
from sim.core.simulation_state import SimulationState
from sim.core.world.layouts import layout_extent, place_flock
from sim.methods.strombom.heuristics import collect_threshold


def fig_layouts() -> None:
    """Start layouts at N = 200, one seed, same scale in every panel. A dog collects while any
    sheep is outside the dashed circle and drives otherwise."""
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
    """Dog start stations. Top: arcs for D = 1 to 64 on a compact start, N = 100. Bottom: the
    three start placements for 8 dogs on a wide start, N = 200."""
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
    """One real trial: wide start, N = 200, D = 4, seed 2026. Orange lines are dog paths, the
    teal circle is the goal. The dogs first collect the outliers, then drive the flock."""
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
    """The task, from the code. Left: the flock starts around a centre and is driven to a
    circular goal; the blue disc is the farthest a sheep can start in any layout. Middle: the
    drive length is the largest of 13 flock radii, 80, and the farthest start plus the goal
    and one flock radius. Right: the goal and the flock radius grow with N."""
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
