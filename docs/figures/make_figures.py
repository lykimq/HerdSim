"""Figures of the model and the task in the README, drawn from the real code.

    uv run --with matplotlib python docs/figures/make_figures.py

Needs matplotlib (not a project dependency). Every picture calls the same functions a campaign
uses (start layouts, dog arcs, the team rule, a real trial), so if the code changes, running
this script redraws them. The pictures are written next to this script. Flock radii come from
the calibration of the finished runs. The results figures are drawn by make_result_figures.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.patches import Circle, Rectangle  # noqa: E402
from matplotlib.ticker import NullFormatter  # noqa: E402
import numpy as np  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

from analysis.results import flock_radii  # noqa: E402
from services.cells import Cell, Group, cell_config  # noqa: E402
from services.protocol import load_protocol  # noqa: E402
from sim.core.simulation_runner import initial_state, run_trial  # noqa: E402
from sim.core.world.layouts import (  # noqa: E402
    layout_extent,
    place_dogs,
    place_flock,
)
from sim.core.vectors import behind, farthest_from, unit  # noqa: E402
from sim.methods.kubo.forces import clamp_speed, dog_velocity, sheep_velocities  # noqa: E402
from sim.methods.strombom.heuristics import collect_threshold, decide  # noqa: E402
from sim.plugins.dogs.collect_drive_multi import team_targets  # noqa: E402
from tests.helpers import config_for  # noqa: E402

OUT = Path(__file__).parent
SURFACE, INK, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"  # categorical slots 1 to 3


def calibrated(protocol: str, fallback: dict[int, float]) -> dict[int, float]:
    """Flock radii of a finished run (results/<protocol>/calibration.json), else the fallback."""
    folder = REPO / "results" / protocol
    if not (folder / "calibration.json").exists():
        return fallback
    radii = flock_radii(folder)["strombom_multi"]
    return {int(n): float(r) for n, r in radii.items()}


# Calibrated flock radii of the strombom sheep, from the main run when it is present.
RF = calibrated("dmin_m12", {25: 6.2, 50: 7.6, 100: 9.08, 200: 10.47, 400: 11.4})

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


def cfg(layout: str, n: int, d: int, **kw):
    return config_for("strombom_multi", n=n, d=d, layout=layout, flock_radius=RF[n], **kw)


def caption(fig, text: str, width: int = 150) -> None:
    """Marks the figure as captioned and draws nothing.

    The captions live in the documents (report and README), so the pictures carry none and
    the layout below keeps the whole canvas. The text argument stays at every call as a note
    of what the figure shows.
    """
    fig._has_caption = True  # noqa: SLF001


_tight_layout = Figure.tight_layout


def _tight_layout_full_canvas(self, *args, rect=None, **kwargs):
    """tight_layout that gives the room reserved for a caption back to the axes."""
    if rect is not None and getattr(self, "_has_caption", False):
        rect = (rect[0], rect[1], rect[2], 0.98)
    return _tight_layout(self, *args, rect=rect, **kwargs)


Figure.tight_layout = _tight_layout_full_canvas  # type: ignore[method-assign]


def xy(point) -> tuple[float, float]:
    """A point as the (x, y) tuple matplotlib patches take."""
    return float(point[0]), float(point[1])


def style_map(ax, title: str) -> None:
    ax.set_aspect("equal")
    ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks([])
    for side in ("left", "bottom"):
        ax.spines[side].set_visible(False)


def draw_scene(ax, c, sheep, dogs, goal_arrow: bool = True) -> None:
    center = np.asarray(c["flock_center"])
    goal = np.asarray(c["goal_center"])
    ax.add_patch(Circle(xy(goal), c["goal_radius"], fc="none", ec=AQUA, lw=1.5))
    ax.scatter(*sheep.T, s=7, color=BLUE, alpha=0.85, lw=0)
    ax.scatter(*dogs.T, s=34, marker="^", color=ORANGE, ec=SURFACE, lw=0.8, zorder=3)
    if goal_arrow:
        ax.annotate("", xy=goal - [c["goal_radius"] + 4, 0], xytext=center + [14, 0],
                    arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))


def fig_layouts() -> None:
    n = 200
    fig, axes = plt.subplots(2, 2, figsize=(10, 6.6))
    for ax, layout in zip(axes.flat, ("compact", "wide", "split", "outlier_rich")):
        c = cfg(layout, n, 4)
        sheep = place_flock(c, np.random.default_rng(2026))
        dogs = place_dogs(c)
        draw_scene(ax, c, sheep, dogs)
        center = np.asarray(c["flock_center"])
        f = collect_threshold(n, c["r_a"])
        ax.add_patch(Circle(xy(center), f,fc="none", ec=MUTED, lw=0.9, ls="--"))
        ax.text(center[0] - f * 0.72, center[1] + f * 0.78, "f(N)", color=MUTED, ha="center")
        ax.set_xlim(center[0] - 150, center[0] + 175)  # same window in every panel
        ax.set_ylim(center[1] - 150, center[1] + 150)
        style_map(ax, layout)
    fig.text(0.01, 0.02, "sheep", color=BLUE)
    fig.text(0.07, 0.02, "dogs (D = 4)", color=ORANGE)
    fig.text(0.16, 0.02, "goal", color=AQUA)
    fig.text(0.21, 0.02, "dashed: collect distance f(N) = r_a N^(2/3)", color=MUTED)
    caption(fig, f"Start layouts at N = {n}, one seed, same scale in every panel. A dog collects "
            "while any sheep is outside the dashed circle and drives otherwise. Dogs start behind the "
            "farthest sheep that can start, so the arc is closer for the compact layout.", 110)
    fig.tight_layout(rect=(0, 0.04, 1, 0.94))
    fig.savefig(OUT / "fig7_layouts.png", dpi=150)
    plt.close(fig)


def fig_dog_starts() -> None:
    counts = (1, 2, 4, 8, 24, 64)
    fig, axes = plt.subplots(2, 6, figsize=(13, 6.0))
    for ax, d in zip(axes[0], counts):
        c = cfg("compact", 100, d)
        sheep = place_flock(c, np.random.default_rng(2026))
        dogs = place_dogs(c)
        center = np.asarray(c["flock_center"])
        draw_scene(ax, c, sheep, dogs, goal_arrow=False)
        r = np.linalg.norm(dogs - center, axis=1).max() + 8
        ax.set_xlim(center[0] - r, center[0] + 35)
        ax.set_ylim(center[1] - r, center[1] + r)
        style_map(ax, f"arcs, D = {d}")
    for ax, mode in zip(axes[1][:3], ("arcs", "ring", "handler")):
        c = cfg("wide", 200, 8, settings={"dog_start": mode})
        sheep = place_flock(c, np.random.default_rng(2026))
        dogs = place_dogs(c)
        center = np.asarray(c["flock_center"])
        draw_scene(ax, c, sheep, dogs, goal_arrow=False)
        ax.set_xlim(center[0] - 160, center[0] + 160)
        ax.set_ylim(center[1] - 160, center[1] + 160)
        style_map(ax, f"{mode}, wide, N = 200, D = 8")
    for ax in axes[1][3:]:
        ax.axis("off")
    axes[1][3].text(0.0, 0.9, "arcs: half circles behind the flock (base)\n"
                    "ring: circles round the flock, less the\n    goal's cone\n"
                    "handler: all dogs at one point behind,\n"
                    "    as if released from a post", transform=axes[1][3].transAxes,
                    color=MUTED, va="top", fontsize=9)
    caption(fig, "Dog start stations. Top: arcs for D = 1 to 64 on a compact start, N = 100. Dogs "
            "stand behind the flock, 30 units beyond the farthest sheep that can start, spread "
            "evenly and at least 5 apart; more dogs go on arcs 5 farther out. Bottom: the three "
            "start placements for 8 dogs on a wide start, N = 200.", 130)
    fig.tight_layout(rect=(0, 0, 1, 0.9))
    fig.savefig(OUT / "fig8_dog_starts.png", dpi=150)
    plt.close(fig)


def fig_team_rule() -> None:
    counts = (1, 2, 4, 8)
    fig, axes = plt.subplots(2, 4, figsize=(13, 7.0))
    for col, d in enumerate(counts):
        for row, (layout, n) in enumerate((("wide", 200), ("compact", 200))):
            c = cfg(layout, n, d)
            sheep = place_flock(c, np.random.default_rng(2026))
            dogs = place_dogs(c)
            goal = np.asarray(c["goal_center"])
            targets = team_targets(sheep, goal, dogs, c)
            centroid = sheep.mean(axis=0)
            ax = axes[row, col]
            far = np.linalg.norm(sheep - centroid, axis=1) > collect_threshold(n, c["r_a"])
            ax.scatter(*sheep[~far].T, s=7, color=BLUE, alpha=0.6, lw=0)
            ax.scatter(*sheep[far].T, s=14, color=BLUE, ec=INK, lw=0.5)
            ax.scatter(*dogs.T, s=34, marker="^", color=ORANGE, ec=SURFACE, lw=0.8, zorder=3)
            ax.scatter(*targets.T, s=22, marker="x", color=INK, lw=1.1, zorder=3)
            if row == 1 and d > 1:  # the drive slots lie on an arc; a thin line makes them readable
                ordered = targets[np.argsort(targets[:, 1])]
                ax.plot(*ordered.T, color=INK, lw=0.5, alpha=0.4, zorder=2)
            for dog, target in zip(dogs, targets):
                ax.annotate("", xy=target, xytext=dog,
                            arrowprops=dict(arrowstyle="->", color=ORANGE, lw=0.9))
            if row == 0:
                ax.set_xlim(centroid[0] - 185, centroid[0] + 115)
                ax.set_ylim(centroid[1] - 170, centroid[1] + 170)
                title = f"collect, D = {d}" + ("  (the paper)" if d == 1 else "")
            else:
                ax.set_xlim(centroid[0] - 80, centroid[0] + 35)
                ax.set_ylim(centroid[1] - 70, centroid[1] + 70)
                title = f"drive, D = {d}" + ("  (the paper)" if d == 1 else "")
            style_map(ax, title)
    caption(fig, "From one dog to many. With one dog the rule is the paper's (left column). With "
            "more dogs HerdSim gives every dog its own job. Collecting (top, wide start): each dog "
            "goes to the collect point of its own outlier, matched by least total walk. Driving "
            "(bottom, compact start): the dogs take slots on an arc behind the flock, spread over "
            "its width, with the paper's drive point in the middle. Crosses are the targets.", 140)
    fig.tight_layout(rect=(0, 0, 1, 0.91))
    fig.savefig(OUT / "fig3_team_rule.png", dpi=150)
    plt.close(fig)


def fig_fat() -> None:
    """FAT against the paper's shepherd, and many FAT dogs."""
    c1 = cfg("wide", 100, 1)
    sheep = place_flock(c1, np.random.default_rng(2026))
    goal = np.asarray(c1["goal_center"])
    centroid = sheep.mean(axis=0)
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.8))
    for k, ax in enumerate(axes):
        d = 4 if k == 2 else 1
        c = cfg("wide", 100, d)
        dogs = place_dogs(c)
        ax.scatter(*sheep.T, s=9, color=BLUE, alpha=0.75, lw=0)
        ax.scatter(*dogs.T, s=40, marker="^", color=ORANGE, ec=SURFACE, lw=0.8, zorder=4)
        ax.annotate("", xy=centroid + [80, 0], xytext=centroid + [55, 0],
                    arrowprops=dict(arrowstyle="->", color=AQUA, lw=1.4))
        ax.text(centroid[0] + 82, centroid[1], "goal", color=AQUA, va="center", fontsize=9)
        if k == 0:
            dd = decide(sheep, goal, c1)
            tgt = dd.target[None, :]
            pick = sheep[dd.outliers[0]]
            ax.scatter(*centroid, s=40, marker="+", color=INK, zorder=4)
            ax.text(centroid[0] + 2, centroid[1] + 3, "GCM", color=INK, fontsize=8)
            title = "Strombom, one dog: farthest from the GCM"
        else:
            pick = farthest_from(sheep, goal)
            tgt = np.tile(behind(pick, goal, c1["r_a"]), (len(dogs), 1))
            title = "FAT, one dog: farthest from the goal" if k == 1 else "FAT, 4 dogs: one target"
        ax.scatter(*pick, s=80, facecolors="none", ec=ORANGE, lw=1.4)
        ax.scatter(*tgt.T, s=60, marker="x", color=INK, lw=1.6, zorder=4)
        for dog, t in zip(dogs, tgt):
            ax.annotate("", xy=t, xytext=dog, arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))
        ax.set_xlim(centroid[0] - 130, centroid[0] + 100)
        ax.set_ylim(centroid[1] - 125, centroid[1] + 125)
        style_map(ax, title)
    caption(fig, "FAT, from the code, on a wide start, N = 100. Each FAT dog aims r_a behind the "
            "sheep farthest from the goal, with the Strombom step. Left: the paper's rule picks the "
            "sheep farthest from the centre of mass instead. Middle: the FAT choice with one dog. "
            "Right: with several dogs, every FAT dog sees the same sheep and picks the same point, so the dogs become copies once they "
            "meet. FAT is a HerdSim construction that borrows the target choice of Kubo's "
            "farthest-individual rule. Crosses are the targets, the circled sheep is the choice.", 140)
    fig.tight_layout(rect=(0, 0, 1, 0.84))
    fig.savefig(OUT / "fig4_fat.png", dpi=150)
    plt.close(fig)


def fig_kubo() -> None:
    """The Kubo force model: sheep forces, dog forces, and the formation the dogs make."""
    c = config_for("kubo", n=20, d=2)
    fig, axes = plt.subplots(1, 3, figsize=(14, 5.0))
    # sheep forces on one sheep
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
    terms = {"K_s1 repulsion": c["K_s1"] * a, "K_s2 alignment": c["K_s2"] * b,
             "K_s3 attraction": c["K_s3"] * cc, "K_s4 flight from the dog": c["K_s4"] * dflee}
    code = sheep_velocities(pos, vel, dog, c)[0]
    total = np.sum(list(terms.values()), axis=0)
    assert np.allclose(code, clamp_speed(total[None, :], c["sheep_speed_max"])[0]), \
        "figure disagrees with the Kubo sheep code"
    ax = axes[0]
    ax.add_patch(Circle(xy(focal),c["sheep_radius"], fc="none", ec=MUTED, lw=0.8, ls="--"))
    ax.scatter(*nbr.T, s=24, color="#a8a7a0", lw=0)
    ax.scatter(*dog.T, s=50, marker="^", color=ORANGE, zorder=4)
    ax.scatter(*focal, s=50, color=INK, zorder=4)
    palette = [MUTED, BLUE, AQUA, ORANGE]
    from matplotlib.lines import Line2D

    legend_s = []
    for (label, v), col in zip(terms.items(), palette):
        mag = float(np.linalg.norm(v))
        tip = unit(v) * max(np.sqrt(mag) * 3.2, 3.5)  # at least 3.5 long, so small forces show
        ax.annotate("", xy=tip, xytext=focal, arrowprops=dict(arrowstyle="->", color=col, lw=1.6))
        legend_s.append(Line2D([0], [0], color=col, lw=2, label=f"{label}  {mag:.1f}"))
    ax.legend(handles=legend_s, loc="lower left", frameon=False, fontsize=8)
    ax.set_xlim(-22, 22)
    ax.set_ylim(-34, 20)
    style_map(ax, "sheep: four forces, field of view 20 (dashed)")
    # dog forces
    X = np.zeros(2)
    T = np.array([30.0, 9.0])
    G = np.array([95.0, -30.0])
    other = np.array([[-6.0, -24.0]])
    parts = {
        "K_f1 toward the target": c["K_f1"] * unit(T - X),
        "K_f2 keep off the target": c["K_f2"] * (X - T) / np.linalg.norm(X - T) ** 3,
        "K_f3 away from the goal": c["K_f3"] * unit(X - G),
        "K_f4 away from the other dog": c["K_f4"] * ((X - other) / np.linalg.norm(X - other, axis=1,
                                                                                keepdims=True) ** 3).mean(axis=0),
    }
    full = dog_velocity(X, T, G, other, c)
    assert np.allclose(full, sum(parts.values())), "figure disagrees with the Kubo dog code"
    ax = axes[1]
    ax.scatter(*X, s=60, marker="^", color=ORANGE, zorder=4)
    ax.scatter(*T, s=50, color=BLUE, zorder=4)
    ax.scatter(*other.T, s=50, marker="^", color="#e8b9a4", zorder=4)
    ax.text(T[0], T[1] + 3.5, "target sheep", color=BLUE, fontsize=8, ha="center")
    ax.text(other[0, 0], other[0, 1] - 4, "other dog", color=MUTED, fontsize=8, ha="center")
    ax.annotate("", xy=(48, -10), xytext=(30, -3), arrowprops=dict(arrowstyle="->", color=AQUA, lw=1.0))
    ax.text(49, -11.5, "goal, far to the right", color=AQUA, fontsize=8)
    legend_d = []
    for (label, v), col in zip(parts.items(), [BLUE, MUTED, AQUA, "#e87ba4"]):
        mag = float(np.linalg.norm(v))
        tip = unit(v) * max(np.sqrt(mag) * 3.2, 3.5)  # at least 3.5 long, so small forces show
        ax.annotate("", xy=tip, xytext=X, arrowprops=dict(arrowstyle="->", color=col, lw=1.6))
        legend_d.append(Line2D([0], [0], color=col, lw=2, label=f"{label}  {mag:.1f}"))
    ax.annotate("", xy=unit(full) * np.sqrt(np.linalg.norm(full)) * 3.2, xytext=X,
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.4))
    legend_d.append(Line2D([0], [0], color=INK, lw=3,
                           label=f"sum, capped at {c['dog_speed_max']:.0f}  {np.linalg.norm(full):.1f}"))
    ax.legend(handles=legend_d, loc="lower right", frameon=False, fontsize=8)
    ax.set_xlim(-25, 62)
    ax.set_ylim(-34, 22)
    style_map(ax, "dog: four forces (the target, the goal and one other dog)")
    # formation from a real trial
    ck = config_for("kubo", n=50, d=4, flock_radius=5.9, ticks=3000)
    snap = {}

    def keep(state) -> None:
        if state.tick == 450:
            snap["s"] = (state.sheep_positions.copy(), state.shepherd_positions.copy())

    run_trial(ck, 2026, on_tick=keep)
    sh, dg = snap["s"]
    ax = axes[2]
    ax.add_patch(Circle(xy(ck["goal_center"]),ck["goal_radius"], fc="none", ec=AQUA, lw=1.4))
    ax.scatter(*sh.T, s=10, color=BLUE, lw=0)
    ax.scatter(*dg.T, s=44, marker="^", color=ORANGE, ec=SURFACE, lw=0.8, zorder=4)
    allp = np.vstack([sh, dg, np.asarray(ck["goal_center"])[None, :]])
    lo, hi = allp.min(axis=0) - 12, allp.max(axis=0) + 12
    ax.set_xlim(lo[0], hi[0])
    ax.set_ylim(lo[1], hi[1])
    style_map(ax, "a real Kubo trial, N = 50, 4 dogs, tick 450")
    caption(fig, "The Kubo et al. (2022) force model, from the code; the figures check their "
            "own arrows against it. Sheep (left) and dogs (middle) move by the sum of four "
            "forces, arrow length is the square root of the force so that all four show, and the "
            "number is the force. The repulsion between dogs (K_f4) keeps them apart; the paper reports "
            "that it makes the dogs form a circle round the flock, and a real trial is shown on the "
            "right. Each dog targets the sheep farthest from the goal.", 150)
    fig.tight_layout(rect=(0, 0, 1, 0.84))
    fig.savefig(OUT / "fig5_kubo.png", dpi=150)
    plt.close(fig)


def fig_trial() -> None:
    n, d = 200, 4
    c = cfg("wide", n, d, ticks=1500)
    states: dict[int, tuple[np.ndarray, np.ndarray]] = {}
    path: list[np.ndarray] = []
    state0 = initial_state(c, 2026)
    states[0] = (state0.sheep_positions.copy(), state0.shepherd_positions.copy())
    path.append(state0.shepherd_positions.copy())

    def keep(state) -> None:
        path.append(state.shepherd_positions.copy())
        states[state.tick] = (state.sheep_positions.copy(), state.shepherd_positions.copy())

    result = run_trial(c, 2026, on_tick=keep)
    last = result.total_ticks
    shots = [0, last // 5, last // 2, last]
    fig, axes = plt.subplots(2, 2, figsize=(10, 6.2))
    trail = np.array(path)  # (ticks + 1, D, 2)
    goal = np.asarray(c["goal_center"])
    for ax, tick in zip(axes.flat, shots):
        sheep, dogs = states[tick]
        ax.add_patch(Circle(xy(goal), c["goal_radius"], fc="none", ec=AQUA, lw=1.5))
        for j in range(d):
            ax.plot(*trail[: tick + 1, j].T, color=ORANGE, lw=0.7, alpha=0.6)
        ax.scatter(*sheep.T, s=7, color=BLUE, alpha=0.85, lw=0)
        ax.scatter(*dogs.T, s=34, marker="^", color=ORANGE, ec=SURFACE, lw=0.8, zorder=3)
        centre = np.asarray(c["flock_center"])
        ax.set_xlim(centre[0] - 150, goal[0] + 40)
        ax.set_ylim(centre[1] - 130, centre[1] + 130)
        style_map(ax, f"tick {tick}")
    caption(fig, f"One real trial: wide start, N = {n}, D = {d}, seed 2026, finished in {last} "
            "ticks. Orange lines are dog paths, the teal circle is the goal. The dogs first "
            "collect the outliers, then drive the compact flock.", 120)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(OUT / "fig17_trial.png", dpi=150)
    plt.close(fig)


def field_config(n: int, max_dogs: int) -> dict:
    """Run config of a cell of the dmin protocol, whose field is sized for all four layouts and
    for ``max_dogs`` dogs; the field is the same for every cell of that N and largest D."""
    from dataclasses import replace

    protocol = load_protocol("dmin_m12", output=Path("/tmp/herdsim-figures"))
    protocol = replace(protocol, shepherd_counts=(1, max_dogs))
    return cell_config(protocol, Cell(Group("strombom_multi", "wide", (), n), max_dogs), RF[n])


def fig_task_geometry() -> None:
    n = 200
    c = field_config(n, 24)
    layouts = ("compact", "wide", "split", "outlier_rich")
    fig = plt.figure(figsize=(13, 5.4))
    grid = fig.add_gridspec(1, 3, width_ratios=[1.5, 1, 1])
    # (a) the task to scale
    ax = fig.add_subplot(grid[0, 0])
    centre = np.asarray(c["flock_center"])
    goal = np.asarray(c["goal_center"])
    rf = c["flock_radius"]
    reach = max(layout_extent({**c, "initial_layout": k}) for k in layouts)
    ax.add_patch(Rectangle((0, 0),c["world_width"], c["world_height"], fc="none", ec=GRID,
                               lw=1.0))
    ax.add_patch(Circle(xy(centre), reach, fc=BLUE, ec="none", alpha=0.10))
    ax.add_patch(Circle(xy(centre), rf,fc="none", ec=BLUE, lw=1.0, ls=":"))
    sheep = place_flock({**c, "initial_layout": "compact"}, np.random.default_rng(2026))
    ax.scatter(*sheep.T, s=7, color=BLUE, lw=0)
    ax.add_patch(Circle(xy(goal), c["goal_radius"], fc="none", ec=AQUA, lw=1.6))
    drive = float(goal[0] - centre[0])
    ax.annotate("", xy=(goal[0], centre[1] - reach - 28), xytext=(centre[0], centre[1] - reach - 28),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.0))
    ax.text((centre[0] + goal[0]) / 2, centre[1] - reach - 46, f"drive length {drive:.0f}",
            ha="center", color=INK)
    ax.annotate(f"R_f = {rf:.1f}", xy=(centre[0] + rf * 0.71, centre[1] - rf * 0.71),
                xytext=(centre[0] + 25, centre[1] - 60), color=BLUE,
                arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.7))
    ax.annotate(f"farthest start sheep, {reach:.0f}\n(widest layout)",
                xy=(centre[0] - reach * 0.71, centre[1] + reach * 0.71),
                xytext=(centre[0] - reach - 10, centre[1] + reach + 22), color=BLUE,
                arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.7))
    ax.text(goal[0], goal[1] + c["goal_radius"] + 8, f"goal {c['goal_radius']:.1f} = 1.9 R_f",
            ha="center", color=AQUA)
    ax.text(c["world_width"], c["world_height"] + 6, f"field {c['world_width']:.0f} x "
            f"{c['world_height']:.0f}, places the start, no boundary", ha="right", color=MUTED,
            fontsize=8)
    ax.set_xlim(-10, c["world_width"] + 10)
    ax.set_ylim(-10, c["world_height"] + 24)
    style_map(ax, f"the task to scale, N = {n}")
    # (b) the drive length and its three terms
    ns = (25, 50, 100, 200, 400)
    t1, t2, t3, actual = [], [], [], []
    for k in ns:
        ck = field_config(k, 24)
        ext = max(layout_extent({**ck, "initial_layout": m}) for m in layouts)
        t1.append(13.0 * ck["flock_radius"])
        t2.append(80.0)
        t3.append(ext + ck["goal_radius"] + ck["flock_radius"])
        actual.append(float(ck["goal_center"][0] - ck["flock_center"][0]))
    ax = fig.add_subplot(grid[0, 1])
    ax.plot(ns, actual, color=INK, lw=5, alpha=0.25, solid_capstyle="round",
            label="drive length used")
    ax.plot(ns, t1, color=BLUE, lw=1.6, marker="o", ms=3, label="13 R_f")
    ax.plot(ns, t2, color=MUTED, lw=1.2, ls="--", label="minimum 80")
    ax.plot(ns, t3, color=ORANGE, lw=1.6, marker="o", ms=3,
            label="reach + goal radius + R_f")
    ax.set_xscale("log")
    ax.set_xticks(ns)
    ax.set_xticklabels([str(k) for k in ns])
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xlabel("flock size N")
    ax.set_ylabel("length (units)")
    ax.set_title("drive length: the largest of three terms")
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    # (c) the flock and goal radii
    ax = fig.add_subplot(grid[0, 2])
    radii = [field_config(k, 24)["flock_radius"] for k in ns]
    ax.plot(ns, [1.9 * r for r in radii], color=AQUA, lw=1.6, marker="o", ms=3,
            label="goal radius 1.9 R_f")
    ax.plot(ns, radii, color=BLUE, lw=1.6, marker="o", ms=3, label="flock radius R_f")
    ax.set_xscale("log")
    ax.set_xticks(ns)
    ax.set_xticklabels([str(k) for k in ns])
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xlabel("flock size N")
    ax.set_ylabel("length (units)")
    ax.set_title("flock radius and goal radius")
    ax.set_ylim(0, 1.9 * max(radii) * 1.1)
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    caption(fig, "The task, from the code. Left: the flock starts around a centre and is driven to "
            "a circular goal; the blue disc is the farthest a sheep can start in any layout, and "
            "the field is only a rectangle that holds all of it. Middle: the drive length is the "
            "largest of 13 flock radii, 80, and the farthest start plus the goal and one flock "
            "radius, so it follows the widest layout of the protocol at large N. Right: the goal "
            "and the flock radius grow with N, as the flock grows.", 150)
    fig.tight_layout(rect=(0, 0, 1, 0.84))
    fig.savefig(OUT / "fig6_task_geometry.png", dpi=150)
    plt.close(fig)


def main() -> None:
    fig_team_rule()
    fig_fat()
    fig_kubo()
    fig_task_geometry()
    fig_layouts()
    fig_dog_starts()
    fig_trial()


if __name__ == "__main__":
    main()
