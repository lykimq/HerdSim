"""The sheep forces and the Kubo and Lama and di Bernardo models."""

from __future__ import annotations

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.patches import Circle

from docs.generate_docs.figstyle import (
    AQUA,
    BLUE,
    GRID,
    INK,
    MUTED,
    ORANGE,
    save,
)
from docs.generate_docs.model_figures.scene import (
    RED,
    SEED,
    Config,
    arrow,
    cfg,
    dogs_at,
    force_arrows,
    gcm,
    style_map,
    targets_at,
    window,
    xy,
)
from services.cells import Cell, Group, cell_config
from services.protocol import load_protocol
from sim.core.simulation_runner import initial_state, run_trial
from sim.core.simulation_state import SimulationState
from sim.core.vectors import behind, farthest_from, unit
from sim.core.world.layouts import place_dogs, place_flock
from sim.methods.kubo.forces import clamp_speed, dog_velocity, sheep_velocities
from sim.methods.lama.dynamics import herder_velocities
from sim.methods.strombom.heuristics import decide
from tests.helpers import config_for


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


def kubo_sheep_panel(ax: Axes, c: Config) -> None:
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


def kubo_dog_panel(ax: Axes, c: Config) -> None:
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

    def keep(state: SimulationState) -> None:
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


def lama_rule_panel(ax: Axes, c: Config) -> None:
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

    def keep(state: SimulationState) -> None:
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
