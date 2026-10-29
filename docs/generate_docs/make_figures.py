"""Figures of the model and the task in the README, drawn from the real code.

    uv run --with matplotlib python docs/generate_docs/make_figures.py

Needs matplotlib (not a project dependency). Every picture calls the same functions a campaign
uses (start layouts, dog arcs, the team rule, a real trial), so if the code changes, running
this script redraws them. The pictures are written to docs/figures. Flock radii come from
the calibration of the finished runs. The results figures are drawn by make_result_figures.py.

The file has three parts: the shared settings (seed, flock radii), helpers that draw the
pieces every scene uses (sheep, dogs, targets, arrows, the view window), and one function per
figure. Colours, matplotlib defaults and saving are in figstyle.py. The captions are in the
README and report; each function's docstring says what the figure shows.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from figstyle import AQUA, BLUE, GRID, INK, MUTED, ORANGE, REPO, SURFACE, grid, save
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Rectangle
from matplotlib.ticker import NullFormatter

sys.path.insert(0, str(REPO))

from analysis.results import flock_radii  # noqa: E402
from services.cells import Cell, Group, cell_config  # noqa: E402
from services.protocol import load_protocol  # noqa: E402
from sim.core.simulation_runner import initial_state, run_trial  # noqa: E402
from sim.core.vectors import behind, farthest_from, unit  # noqa: E402
from sim.core.world.layouts import layout_extent, place_dogs, place_flock  # noqa: E402
from sim.methods.kubo.forces import clamp_speed, dog_velocity, sheep_velocities  # noqa: E402
from sim.methods.lama.dynamics import herder_velocities  # noqa: E402
from sim.methods.strombom.heuristics import (  # noqa: E402
    collect_threshold,
    decide,
    drive_point,
    radius_of,
)
from sim.plugins.dogs.collect_drive_multi import team_targets  # noqa: E402
from tests.helpers import config_for  # noqa: E402

# ------------------------------------------------------------------------------------ settings

SEED = 2026  # every scene starts from the same flock
NS = (25, 50, 100, 200, 400)
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


def cfg(layout: str, n: int, d: int, **kw):
    return config_for("strombom_multi", n=n, d=d, layout=layout, flock_radius=RF[n], **kw)


def start(c) -> tuple[np.ndarray, np.ndarray]:
    """Sheep and dogs at the start of a trial with this config, on the shared seed."""
    return place_flock(c, np.random.default_rng(SEED)), place_dogs(c)


def field_config(n: int, max_dogs: int) -> dict:
    """Run config of a cell of the dmin protocol, whose field is sized for all four layouts and
    for ``max_dogs`` dogs; the field is the same for every cell of that N and largest D."""
    from dataclasses import replace

    protocol = load_protocol("dmin_m12", output=Path("/tmp/herdsim-figures"))
    protocol = replace(protocol, shepherd_counts=(1, max_dogs))
    return cell_config(protocol, Cell(Group("strombom_multi", "wide", (), n), max_dogs), RF[n])


# ------------------------------------------------------------------------------ drawing helpers


def xy(point) -> tuple[float, float]:
    """A point as the (x, y) tuple matplotlib patches take."""
    return float(point[0]), float(point[1])


def style_map(ax, title: str) -> None:
    """A map panel: equal axes, no ticks, no frame."""
    ax.set_aspect("equal")
    ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks([])
    for side in ("left", "bottom"):
        ax.spines[side].set_visible(False)


def window(ax, centre, left: float, right: float, down: float, up: float) -> None:
    """View the area from ``left`` to ``right`` and ``down`` to ``up`` around ``centre``."""
    ax.set_xlim(centre[0] - left, centre[0] + right)
    ax.set_ylim(centre[1] - down, centre[1] + up)


def arrow(ax, tip, tail, color: str, lw: float, style: str = "->", **kw) -> None:
    ax.annotate(
        "", xy=tip, xytext=tail, arrowprops=dict(arrowstyle=style, color=color, lw=lw, **kw)
    )


def dogs_at(ax, dogs, s: float = 34, lw: float = 0.8, zorder: int = 3, **kw) -> None:
    ax.scatter(*dogs.T, s=s, marker="^", color=ORANGE, ec=SURFACE, lw=lw, zorder=zorder, **kw)


def targets_at(ax, targets, s: float, lw: float, zorder: int = 4, **kw) -> None:
    ax.scatter(*targets.T, s=s, marker="x", color=INK, lw=lw, zorder=zorder, **kw)


def flock_split(
    ax,
    sheep,
    far,
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
    ax,
    centre,
    label: str | None = "GCM",
    s: float = 40,
    lw=None,
    color: str = INK,
    zorder: int = 4,
    text_at=(3, 3),
    fontsize: float = 8,
    **text_kw,
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


def draw_scene(ax, c, sheep, dogs, goal_arrow: bool = True) -> None:
    """Goal, sheep and dogs of a start, with an arrow toward the goal."""
    center = np.asarray(c["flock_center"])
    goal = np.asarray(c["goal_center"])
    ax.add_patch(Circle(xy(goal), c["goal_radius"], fc="none", ec=AQUA, lw=1.5))
    ax.scatter(*sheep.T, s=7, color=BLUE, alpha=0.85, lw=0)
    dogs_at(ax, dogs)
    if goal_arrow:
        arrow(ax, goal - [c["goal_radius"] + 4, 0], center + [14, 0], MUTED, 0.9)


def force_arrows(ax, origin, forces: dict[str, np.ndarray], colors) -> list[Line2D]:
    """One arrow per force from ``origin``, with legend handles giving each magnitude.

    Arrow length is 3.2 times the square root of the force, and at least 3.5, so that forces
    of very different sizes all show."""
    handles = []
    for (label, v), color in zip(forces.items(), colors):
        mag = float(np.linalg.norm(v))
        arrow(ax, unit(v) * max(np.sqrt(mag) * 3.2, 3.5), origin, color, 1.6)
        handles.append(Line2D([0], [0], color=color, lw=2, label=f"{label}  {mag:.1f}"))
    return handles


def n_axis(ax, ns=NS) -> None:
    """Flock size on a log axis, with only the sizes run labelled."""
    ax.set_xscale("log")
    ax.set_xticks(ns)
    ax.set_xticklabels([str(k) for k in ns])
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xlabel("flock size N")


# ------------------------------------------------------------------------------------- figures


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
        "arcs: half circles behind the flock (base)\n"
        "ring: circles round the flock, less the\n    goal's cone\n"
        "handler: all dogs at one point behind,\n"
        "    as if released from a post",
        transform=axes[1][3].transAxes,
        color=MUTED,
        va="top",
        fontsize=9,
    )
    save(fig, "fig8_dog_starts.png", rect=(0, 0, 1, 0.98))


def fig_team_rule() -> None:
    """From one dog to many. With one dog the rule is the paper's (left column). Collecting
    (top, wide start): each dog goes to the collect point of its own outlier. Driving (bottom,
    compact start): the dogs take slots on an arc behind the flock. Crosses are the targets."""
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


def fig_fat() -> None:
    """FAT against the paper's shepherd, and many FAT dogs, on a wide start, N = 100. Each FAT
    dog aims r_a behind the sheep farthest from the goal; with several dogs every FAT dog picks
    the same point. Crosses are the targets, the circled sheep is the choice."""
    c1 = cfg("wide", 100, 1)
    sheep = place_flock(c1, np.random.default_rng(SEED))
    goal = np.asarray(c1["goal_center"])
    centroid = sheep.mean(axis=0)
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.8))
    for k, ax in enumerate(axes):
        d = 4 if k == 2 else 1
        dogs = place_dogs(cfg("wide", 100, d))
        ax.scatter(*sheep.T, s=9, color=BLUE, alpha=0.75, lw=0)
        dogs_at(ax, dogs, s=40, zorder=4)
        arrow(ax, centroid + [80, 0], centroid + [55, 0], AQUA, 1.4)
        ax.text(centroid[0] + 82, centroid[1], "goal", color=AQUA, va="center", fontsize=9)
        if k == 0:
            dd = decide(sheep, goal, c1)
            tgt = dd.target[None, :]
            pick = sheep[dd.outliers[0]]
            gcm(ax, centroid, text_at=(2, 3))
            title = "Strombom, one dog: farthest from the GCM"
        else:
            pick = farthest_from(sheep, goal)
            tgt = np.tile(behind(pick, goal, c1["r_a"]), (len(dogs), 1))
            title = "FAT, one dog: farthest from the goal" if k == 1 else "FAT, 4 dogs: one target"
        ax.scatter(*pick, s=80, facecolors="none", ec=ORANGE, lw=1.4)
        targets_at(ax, tgt, s=60, lw=1.6)
        for dog, t in zip(dogs, tgt):
            arrow(ax, t, dog, ORANGE, 1.2)
        window(ax, centroid, 130, 100, 125, 125)
        style_map(ax, title)
    save(fig, "fig4_fat.png", rect=(0, 0, 1, 0.98))


def kubo_sheep_panel(ax, c) -> None:
    """The four forces on one sheep of the Kubo model, on a hand-placed scene, checked against
    the code."""
    focal = np.zeros(2)
    nbr = np.array([[5.0, 3.0], [-4.0, 6.0], [8.0, -5.0], [-7.0, -4.0], [2.0, -9.0]])
    heading = np.array([[1.0, 0.2], [0.8, 0.5], [0.0, 0.0], [1.0, -0.3], [0.9, 0.1]])
    heading = heading / np.maximum(np.linalg.norm(heading, axis=1, keepdims=True), 1e-9)
    dog = np.array([[-12.0, 9.0]])
    pos = np.vstack([focal, nbr])
    vel = np.vstack([[0.8, 0.2], heading * 1.0])
    diff = focal - nbr
    dist = np.linalg.norm(diff, axis=1)
    moving = np.linalg.norm(vel[1:], axis=1) > 0
    a = (diff / dist[:, None] ** 2).mean(axis=0)
    cc = -(diff / dist[:, None]).mean(axis=0)
    b = (vel[1:][moving] / np.linalg.norm(vel[1:][moving], axis=1, keepdims=True)).mean(axis=0)
    dd_ = focal - dog
    dflee = (dd_ / np.linalg.norm(dd_, axis=1, keepdims=True) ** 3).mean(axis=0)
    terms = {
        "K_s1 repulsion": c["K_s1"] * a,
        "K_s2 alignment": c["K_s2"] * b,
        "K_s3 attraction": c["K_s3"] * cc,
        "K_s4 flight from the dog": c["K_s4"] * dflee,
    }
    code = sheep_velocities(pos, vel, dog, c)[0]
    total = np.sum(list(terms.values()), axis=0)
    assert np.allclose(code, clamp_speed(total[None, :], c["sheep_speed_max"])[0]), (
        "figure disagrees with the Kubo sheep code"
    )
    ax.add_patch(Circle(xy(focal), c["sheep_radius"], fc="none", ec=MUTED, lw=0.8, ls="--"))
    ax.scatter(*nbr.T, s=24, color="#a8a7a0", lw=0)
    ax.scatter(*dog.T, s=50, marker="^", color=ORANGE, zorder=4)
    ax.scatter(*focal, s=50, color=INK, zorder=4)
    handles = force_arrows(ax, focal, terms, [MUTED, BLUE, AQUA, ORANGE])
    ax.legend(handles=handles, loc="lower left", frameon=False, fontsize=8)
    ax.set_xlim(-22, 22)
    ax.set_ylim(-34, 20)
    style_map(ax, "sheep: four forces, field of view 20 (dashed)")


def kubo_dog_panel(ax, c) -> None:
    """The four forces on one Kubo dog (the target, the goal and one other dog), checked
    against the code, with their capped sum."""
    X = np.zeros(2)
    T = np.array([30.0, 9.0])
    G = np.array([95.0, -30.0])
    other = np.array([[-6.0, -24.0]])
    away = (X - other) / np.linalg.norm(X - other, axis=1, keepdims=True) ** 3
    parts = {
        "K_f1 toward the target": c["K_f1"] * unit(T - X),
        "K_f2 keep off the target": c["K_f2"] * (X - T) / np.linalg.norm(X - T) ** 3,
        "K_f3 away from the goal": c["K_f3"] * unit(X - G),
        "K_f4 away from the other dog": c["K_f4"] * away.mean(axis=0),
    }
    full = dog_velocity(X, T, G, other, c)
    assert np.allclose(full, sum(parts.values())), "figure disagrees with the Kubo dog code"
    ax.scatter(*X, s=60, marker="^", color=ORANGE, zorder=4)
    ax.scatter(*T, s=50, color=BLUE, zorder=4)
    ax.scatter(*other.T, s=50, marker="^", color="#e8b9a4", zorder=4)
    ax.text(T[0], T[1] + 3.5, "target sheep", color=BLUE, fontsize=8, ha="center")
    ax.text(other[0, 0], other[0, 1] - 4, "other dog", color=MUTED, fontsize=8, ha="center")
    arrow(ax, (48, -10), (30, -3), AQUA, 1.0)
    ax.text(49, -11.5, "goal, far to the right", color=AQUA, fontsize=8)
    handles = force_arrows(ax, X, parts, [BLUE, MUTED, AQUA, "#e87ba4"])
    arrow(ax, unit(full) * np.sqrt(np.linalg.norm(full)) * 3.2, X, INK, 2.4, style="-|>")
    handles.append(
        Line2D(
            [0],
            [0],
            color=INK,
            lw=3,
            label=f"sum, capped at {c['dog_speed_max']:.0f}  {np.linalg.norm(full):.1f}",
        )
    )
    ax.legend(handles=handles, loc="lower right", frameon=False, fontsize=8)
    ax.set_xlim(-25, 62)
    ax.set_ylim(-34, 22)
    style_map(ax, "dog: four forces (the target, the goal and one other dog)")


def fig_kubo() -> None:
    """The Kubo et al. (2022) force model, from the code: the four forces on a sheep (left)
    and on a dog (middle), and the circle the dogs form round the flock in a real trial
    (right). Arrow length is the square root of the force, the number is the force."""
    c = config_for("kubo", n=20, d=2)
    ck = config_for("kubo", n=50, d=4, flock_radius=5.9, ticks=3000)
    tick = 450  # the snapshot of the real trial
    fig, axes = plt.subplots(1, 3, figsize=(14, 5.0))
    kubo_sheep_panel(axes[0], c)
    kubo_dog_panel(axes[1], c)
    snap = {}

    def keep(state) -> None:
        if state.tick == tick:
            snap["s"] = (state.sheep_positions.copy(), state.shepherd_positions.copy())

    run_trial(ck, SEED, on_tick=keep)
    sh, dg = snap["s"]
    ax = axes[2]
    ax.add_patch(Circle(xy(ck["goal_center"]), ck["goal_radius"], fc="none", ec=AQUA, lw=1.4))
    ax.scatter(*sh.T, s=10, color=BLUE, lw=0)
    dogs_at(ax, dg, s=44, zorder=4)
    allp = np.vstack([sh, dg, np.asarray(ck["goal_center"])[None, :]])
    lo, hi = allp.min(axis=0) - 12, allp.max(axis=0) + 12
    ax.set_xlim(lo[0], hi[0])
    ax.set_ylim(lo[1], hi[1])
    style_map(ax, f"a real Kubo trial, N = 50, 4 dogs, tick {tick}")
    save(fig, "fig5_kubo.png", rect=(0, 0, 1, 0.98))


def lama_rule_panel(ax, c) -> None:
    """The Lama herder rule on a hand-placed scene, checked against the code.

    Positions are relative to the goal centre, as in the dynamics. H1 senses three targets:
    it leaves the farthest one to H2, which is closer to it, and chases the next farthest.
    H3 senses nothing and walks home."""
    herders = np.array([[24.0, 2.0], [29.0, -6.0], [-20.0, 15.0]])
    targets = np.array(
        [
            [27.0, 9.0],
            [31.0, -3.0],
            [20.0, 0.0],
            [38.0, 14.0],
            [3.0, 2.0],
            [-4.0, -1.0],
            [1.0, -5.0],
        ]
    )
    goal_r = float(c["goal_radius"])
    velocity, choice = herder_velocities(targets, herders, goal_r, c)
    assert list(choice.target) == [0, 1, -1], "figure disagrees with the Lama herder code"
    xi, lam, delta = c["sensing_radius"], c["repulsion_radius"], c["chase_offset"]
    ax.add_patch(Circle((0, 0), goal_r, fc="none", ec=AQUA, lw=1.5))
    ax.text(0, -goal_r - 2.5, "goal", color=AQUA, fontsize=8, ha="center")
    ax.add_patch(Circle(xy(herders[0]), xi, fc="none", ec=MUTED, lw=0.9, ls="--"))
    ax.text(
        herders[0][0],
        herders[0][1] - xi - 2.5,
        "H1 senses within xi",
        color=MUTED,
        fontsize=8,
        ha="center",
    )
    for h in herders:
        ax.add_patch(Circle(xy(h), lam, fc=ORANGE, ec="none", alpha=0.12))
    ax.scatter(*targets.T, s=26, color=BLUE, lw=0, zorder=3)
    dogs_at(ax, herders, s=60, zorder=4)
    for name, h in zip(("H1", "H2", "H3"), herders):
        ax.text(h[0] - 1.0, h[1] - 3.2, name, color=ORANGE, fontsize=9, ha="right")
    # the chase point, delta beyond the target on the ray from the goal centre
    aim = targets[0]
    point = aim + delta * unit(aim)
    ray = aim * (1 + 4 / np.linalg.norm(aim))
    ax.plot([0, ray[0]], [0, ray[1]], color=MUTED, lw=0.7, ls=":")
    ax.scatter(*point, s=22, marker="x", color=INK, zorder=4)
    for i in range(3):
        arrow(ax, xy(herders[i] + velocity[i] * 0.9), xy(herders[i]), ORANGE, 1.6)
    ax.text(aim[0] - 1, aim[1] + 2.5, "chased by H1", color=BLUE, fontsize=8, ha="right")
    ax.text(point[0] + 1.2, point[1] + 0.3, "where H1 stands", color=INK, fontsize=8)
    ax.text(
        targets[1][0] + 4.0,
        targets[1][1] - 0.5,
        "farther, but closer\nto H2: left to H2",
        color=BLUE,
        fontsize=8,
        va="center",
    )
    ax.text(targets[3][0], targets[3][1] + 2.0, "not sensed", color=BLUE, fontsize=8, ha="center")
    ax.text(
        herders[2][0],
        herders[2][1] + 3.0,
        "senses nothing: walks home",
        color=ORANGE,
        fontsize=8,
        ha="center",
    )
    ax.set_xlim(-32, 52)
    ax.set_ylim(-17, 21)
    style_map(ax, "the herder rule")


def fig_lama() -> None:
    """The Lama and di Bernardo (2024) gather method. Top: the herder rule on a hand-made
    scene, checked against the code. Bottom: one real trial at xi = 10, N = 196, D = 20."""
    protocol = load_protocol("lama_r50")
    n, d = 196, 20
    c = cell_config(protocol, Cell(Group("lama", "uniform", (), n), d), float("nan"))
    goal = np.asarray(c["goal_center"])
    snaps: dict[int, tuple[np.ndarray, np.ndarray, np.ndarray]] = {}
    first = initial_state(c, SEED)
    snaps[0] = (first.sheep_positions.copy(), first.shepherd_positions.copy(), np.full(d, -1))

    def keep(state) -> None:
        snaps[state.tick] = (
            state.sheep_positions.copy(),
            state.shepherd_positions.copy(),
            np.asarray(state.metadata["herder_target"]).copy(),
        )

    result = run_trial(c, SEED, on_tick=keep)
    assert result.success, "the example trial should gather the targets"
    last = result.total_ticks
    fig = plt.figure(figsize=(13, 10))
    gs = fig.add_gridspec(2, 3, height_ratios=(1.15, 1))
    lama_rule_panel(fig.add_subplot(gs[0, :]), c)
    shots = [fig.add_subplot(gs[1, k]) for k in range(3)]
    span = c["start_radius"] + 6
    for ax, tick in zip(shots, (0, last // 3, last)):
        targets, herders, chosen = snaps[tick]
        ax.add_patch(Circle(xy(goal), c["start_radius"], fc="none", ec=GRID, lw=1.0, ls="--"))
        ax.add_patch(Circle(xy(goal), c["goal_radius"], fc="none", ec=AQUA, lw=1.5))
        if 0 < tick < last:
            for h in herders:
                ax.add_patch(
                    Circle(
                        xy(h), c["sensing_radius"], fc="none", ec=MUTED, lw=0.5, ls="--", alpha=0.6
                    )
                )
            for h, t in zip(herders, chosen):
                if t >= 0:
                    ax.plot(*np.array([h, targets[t]]).T, color=ORANGE, lw=0.8)
        ax.scatter(*targets.T, s=7, color=BLUE, alpha=0.85, lw=0)
        dogs_at(ax, herders)
        window(ax, goal, span, span, span, span)
        style_map(ax, f"t = {tick * c['dt']:.0f} s (tick {tick})")
    save(fig, "fig_lama.png")


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

    def keep(state) -> None:
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

    def reach_of(cc) -> float:
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


def fig_sheep_forces() -> None:
    """The 5 Strömbom (2014) sheep instincts. Left: a focal sheep senses nearby flock-mates,
    an intruding neighbour closer than r_a = 2 m, and a dog within r_s = 65 m. Right: the
    weighted sum of the five unit vectors."""
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
    h, c, rho_a, rho_s, e = 0.5, 1.05, 2.0, 1.0, 0.3
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
            65,
            fc=ORANGE,
            alpha=0.04,
            ec=ORANGE,
            lw=1.0,
            ls="--",
            label="Threat detection $r_s = 65$ m",
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
            label=r"Resultant Heading $\mathbf{H}_i'$ "
            r"($\mathbf{x}_i^{t+1} = \mathbf{x}_i^t + \delta\,\mathbf{H}_i' / \|\mathbf{H}_i'\|$)",
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


def fig_independent() -> None:
    """strombom_multi against the independent controller, D = 4. Left: strombom_multi assigns
    strays one to one. Middle: independent dogs all chase the same farthest stray. Right: in
    drive mode independent dogs all head for one drive point instead of an arc."""
    n, d = 100, 4
    c_wide = cfg("wide", n, d)
    sheep_w, dogs_w = start(c_wide)
    goal_w = np.asarray(c_wide["goal_center"])
    centroid_w = sheep_w.mean(axis=0)
    far_w = np.linalg.norm(sheep_w - centroid_w, axis=1) > collect_threshold(n, c_wide["r_a"])
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.0))

    ax0 = axes[0]
    targets_multi = team_targets(sheep_w, goal_w, dogs_w, c_wide)
    flock_split(ax0, sheep_w, far_w, s_in=9, s_out=16, lw_out=0.6)
    gcm(ax0, centroid_w)
    dogs_at(ax0, dogs_w, s=42, zorder=4)
    targets_at(ax0, targets_multi, s=36, lw=1.4)
    for dog, tgt in zip(dogs_w, targets_multi):
        arrow(ax0, tgt, dog, ORANGE, 1.2)
    window(ax0, centroid_w, 130, 80, 110, 110)
    style_map(ax0, "strombom_multi: Hungarian Matching (Parallel)")

    ax1 = axes[1]
    flock_split(ax1, sheep_w, far_w, s_in=9, s_out=16, lw_out=0.6)
    gcm(ax1, centroid_w)
    dogs_at(ax1, dogs_w, s=42, zorder=4)
    dec = decide(sheep_w, goal_w, c_wide)
    ax1.scatter(*sheep_w[dec.outliers[0]], s=90, facecolors="none", ec=ORANGE, lw=1.5, zorder=3)
    ax1.scatter(*dec.target, s=70, marker="x", color=INK, lw=1.8, zorder=4)
    for dog in dogs_w:
        arrow(ax1, dec.target, dog, ORANGE, 1.2, ls="--")
    window(ax1, centroid_w, 130, 80, 110, 110)
    style_map(ax1, "independent: Collect (All 4 dogs chase 1 stray)")

    c_comp = cfg("compact", n, d)
    sheep_c, dogs_c = start(c_comp)
    goal_c = np.asarray(c_comp["goal_center"])
    centroid_c = sheep_c.mean(axis=0)
    targets_arc = team_targets(sheep_c, goal_c, dogs_c, c_comp)
    pd_single = drive_point(sheep_c, goal_c, c_comp)
    ax2 = axes[2]
    ax2.scatter(*sheep_c.T, s=9, color=BLUE, alpha=0.7, lw=0)
    gcm(ax2, centroid_c, text_at=(2, 2))
    dogs_at(ax2, dogs_c, s=42, zorder=4)
    ordered_arc = targets_arc[np.argsort(targets_arc[:, 1])]
    ax2.plot(*ordered_arc.T, color=AQUA, lw=1.2, ls=":", label="strombom_multi arc")
    ax2.scatter(
        *pd_single, s=80, marker="x", color=INK, lw=2.0, zorder=4, label="independent Pd (single)"
    )
    for dog in dogs_c:
        arrow(ax2, pd_single, dog, ORANGE, 1.2, ls="--")
    arrow(ax2, goal_c - [c_comp["goal_radius"] + 5, 0], centroid_c + [20, 0], AQUA, 1.2)
    ax2.text(centroid_c[0] + 25, centroid_c[1] + 3, "to goal", color=AQUA, fontsize=8)
    window(ax2, centroid_c, 50, 40, 45, 45)
    ax2.legend(loc="upper left", frameon=False, fontsize=8)
    style_map(ax2, "independent: Drive (Crowding single point Pd)")
    save(fig, "fig_independent.png", rect=(0, 0, 1, 0.98))


def fig_hungarian_matching() -> None:
    """Outlier detection and Hungarian assignment in strombom_multi. Left: any sheep outside
    f(N) = r_a N^(2/3) starts collecting; the collect point P_c is r_a behind the stray on the
    ray from the GCM. Right: the assignment matches dogs to collect points one to one, so no
    two paths cross (dashed red: a crossing assignment drawn by hand)."""
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
    """Driving formation in strombom_multi. Left: the drive point P_d, r_a sqrt(N) behind the
    GCM on the ray from the goal. Right: the dogs fan out on an arc across the flock's width."""
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


FIGURES = (
    fig_sheep_forces,
    fig_team_rule,
    fig_hungarian_matching,
    fig_driving_arc,
    fig_fat,
    fig_independent,
    fig_kubo,
    fig_lama,
    fig_task_geometry,
    fig_layouts,
    fig_dog_starts,
    fig_trial,
)


def main() -> None:
    for draw in FIGURES:
        draw()


if __name__ == "__main__":
    main()
