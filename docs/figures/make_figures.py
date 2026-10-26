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
from matplotlib.lines import Line2D  # noqa: E402
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
from sim.methods.lama.dynamics import herder_velocities  # noqa: E402
from sim.methods.strombom.heuristics import (  # noqa: E402
    collect_threshold,
    decide,
    drive_point,
    radius_of,
)
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


def lama_rule_panel(ax, c) -> None:
    """The Lama herder rule on a hand-placed scene, checked against the code.

    Positions are relative to the goal centre, as in the dynamics. H1 senses three targets:
    it leaves the farthest one to H2, which is closer to it, and chases the next farthest.
    H3 senses nothing and walks home."""
    herders = np.array([[24.0, 2.0], [29.0, -6.0], [-20.0, 15.0]])
    targets = np.array([[27.0, 9.0], [31.0, -3.0], [20.0, 0.0], [38.0, 14.0],
                        [3.0, 2.0], [-4.0, -1.0], [1.0, -5.0]])
    goal_r = float(c["goal_radius"])
    velocity, choice = herder_velocities(targets, herders, goal_r, c)
    assert list(choice.target) == [0, 1, -1], "figure disagrees with the Lama herder code"
    xi, lam, delta = c["sensing_radius"], c["repulsion_radius"], c["chase_offset"]
    ax.add_patch(Circle((0, 0), goal_r, fc="none", ec=AQUA, lw=1.5))
    ax.text(0, -goal_r - 2.5, "goal", color=AQUA, fontsize=8, ha="center")
    ax.add_patch(Circle(xy(herders[0]), xi, fc="none", ec=MUTED, lw=0.9, ls="--"))
    ax.text(herders[0][0], herders[0][1] - xi - 2.5, "H1 senses within xi", color=MUTED,
            fontsize=8, ha="center")
    for h in herders:
        ax.add_patch(Circle(xy(h), lam, fc=ORANGE, ec="none", alpha=0.12))
    ax.scatter(*targets.T, s=26, color=BLUE, lw=0, zorder=3)
    ax.scatter(*herders.T, s=60, marker="^", color=ORANGE, ec=SURFACE, lw=0.8, zorder=4)
    for name, h in zip(("H1", "H2", "H3"), herders):
        ax.text(h[0] - 1.0, h[1] - 3.2, name, color=ORANGE, fontsize=9, ha="right")
    # the chase point, delta beyond the target on the ray from the goal centre
    aim = targets[0]
    point = aim + delta * unit(aim)
    ray = aim * (1 + 4 / np.linalg.norm(aim))
    ax.plot([0, ray[0]], [0, ray[1]], color=MUTED, lw=0.7, ls=":")
    ax.scatter(*point, s=22, marker="x", color=INK, zorder=4)
    for i in range(3):
        tip = herders[i] + velocity[i] * 0.9
        ax.annotate("", xy=xy(tip), xytext=xy(herders[i]),
                    arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.6))
    ax.text(aim[0] - 1, aim[1] + 2.5, "chased by H1", color=BLUE, fontsize=8, ha="right")
    ax.text(point[0] + 1.2, point[1] + 0.3, "where H1 stands", color=INK, fontsize=8)
    ax.text(targets[1][0] + 4.0, targets[1][1] - 0.5, "farther, but closer\nto H2: left to H2",
            color=BLUE, fontsize=8, va="center")
    ax.text(targets[3][0], targets[3][1] + 2.0, "not sensed", color=BLUE, fontsize=8, ha="center")
    ax.text(herders[2][0], herders[2][1] + 3.0, "senses nothing: walks home",
            color=ORANGE, fontsize=8, ha="center")
    ax.set_xlim(-32, 52)
    ax.set_ylim(-17, 21)
    style_map(ax, "the herder rule")


def fig_lama() -> None:
    """The Lama and di Bernardo gather method: the herder rule and a real trial."""
    protocol = load_protocol("lama_r50")
    n, d = 196, 20
    c = cell_config(protocol, Cell(Group("lama", "uniform", (), n), d), float("nan"))
    goal = np.asarray(c["goal_center"])
    snaps: dict[int, tuple[np.ndarray, np.ndarray, np.ndarray]] = {}
    start = initial_state(c, 2026)
    snaps[0] = (start.sheep_positions.copy(), start.shepherd_positions.copy(), np.full(d, -1))

    def keep(state) -> None:
        snaps[state.tick] = (state.sheep_positions.copy(), state.shepherd_positions.copy(),
                             np.asarray(state.metadata["herder_target"]).copy())

    result = run_trial(c, 2026, on_tick=keep)
    assert result.success, "the example trial should gather the targets"
    last = result.total_ticks
    fig = plt.figure(figsize=(13, 10))
    grid = fig.add_gridspec(2, 3, height_ratios=(1.15, 1))
    lama_rule_panel(fig.add_subplot(grid[0, :]), c)
    shots = [fig.add_subplot(grid[1, k]) for k in range(3)]
    for ax, tick in zip(shots, (0, last // 3, last)):
        targets, herders, chosen = snaps[tick]
        ax.add_patch(Circle(xy(goal), c["start_radius"], fc="none", ec=GRID, lw=1.0, ls="--"))
        ax.add_patch(Circle(xy(goal), c["goal_radius"], fc="none", ec=AQUA, lw=1.5))
        if 0 < tick < last:
            for h in herders:
                ax.add_patch(Circle(xy(h), c["sensing_radius"], fc="none", ec=MUTED, lw=0.5,
                                    ls="--", alpha=0.6))
            for h, t in zip(herders, chosen):
                if t >= 0:
                    ax.plot(*np.array([h, targets[t]]).T, color=ORANGE, lw=0.8)
        ax.scatter(*targets.T, s=7, color=BLUE, alpha=0.85, lw=0)
        ax.scatter(*herders.T, s=34, marker="^", color=ORANGE, ec=SURFACE, lw=0.8, zorder=3)
        span = c["start_radius"] + 6
        ax.set_xlim(goal[0] - span, goal[0] + span)
        ax.set_ylim(goal[1] - span, goal[1] + span)
        style_map(ax, f"t = {tick * c['dt']:.0f} s (tick {tick})")
    caption(fig, "The Lama and di Bernardo (2024) gather method. Top: the herder rule on a "
            "hand-made scene, checked against the code. Bottom: one real trial at xi = 10, "
            f"N = {n} targets, D = {d} herders, seed 2026.", 150)
    fig.tight_layout()
    fig.savefig(OUT / "fig_lama.png", dpi=150)
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


def fig_sheep_forces() -> None:
    """The 5 Strömbom (2014) sheep instincts: geometry and vector decomposition."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.8))
    focal = np.array([0.0, 0.0])
    flock_neighbors = np.array([
        [16.0, 12.0], [22.0, -3.0], [9.0, 24.0], [26.0, 16.0],
        [19.0, 27.0], [31.0, 6.0], [13.0, -14.0], [23.0, -17.0],
    ])
    close_neighbor = np.array([1.2, 0.9])
    dog = np.array([-25.0, -20.0])
    all_neighbors = np.vstack([flock_neighbors, close_neighbor])
    lcm = all_neighbors.mean(axis=0)

    H_i = unit(np.array([0.5, 0.85]))
    h = 0.5
    C_i = unit(lcm - focal)
    c = 1.05
    R_a = unit(focal - close_neighbor)
    rho_a = 2.0
    R_s = unit(focal - dog)
    rho_s = 1.0
    eps = unit(np.array([-0.8, 0.5]))
    e = 0.3
    H_prime = h * H_i + c * C_i + rho_a * R_a + rho_s * R_s + e * eps

    ax0 = axes[0]
    ax0.add_patch(Circle((0, 0), 65, fc="#eb6834", alpha=0.04, ec=ORANGE, lw=1.0, ls="--", label="Threat detection $r_s = 65$ m"))
    ax0.add_patch(Circle((0, 0), 2.0, fc="#d9534f", alpha=0.25, ec="#d9534f", lw=1.2, label="Personal space $r_a = 2$ m"))
    ax0.scatter(*flock_neighbors.T, s=35, color=BLUE, alpha=0.75, lw=0, label="Flock-mates")
    ax0.scatter(*close_neighbor, s=50, color="#d9534f", ec=INK, lw=0.9, zorder=4, label=r"Intruding neighbor ($< r_a$)")
    ax0.scatter(*focal, s=85, color=INK, zorder=5, label="Focal sheep $i$")
    ax0.text(focal[0] + 1.5, focal[1] - 3.2, "Sheep $i$", color=INK, fontsize=9, fontweight="bold")
    ax0.scatter(*lcm, s=75, marker="+", color=AQUA, lw=2.2, zorder=4, label="Local Center of Mass (LCM)")
    ax0.text(lcm[0] + 2.0, lcm[1] - 1.0, r"$\mathrm{LCM}_i$", color=AQUA, fontsize=9, fontweight="bold")
    ax0.scatter(*dog, s=95, marker="^", color=ORANGE, ec=SURFACE, lw=1.0, zorder=5, label=r"Shepherd dog ($< r_s$)")
    ax0.text(dog[0] - 2.0, dog[1] - 4.5, r"Dog ($< r_s$)", color=ORANGE, fontsize=9, fontweight="bold")
    ax0.set_xlim(-40, 45)
    ax0.set_ylim(-35, 45)
    ax0.legend(loc="upper left", frameon=False, fontsize=8)
    style_map(ax0, "A. Biological interaction geometry on open pasture")

    ax1 = axes[1]
    scale = 12.0
    vectors = [
        (r"1. Momentum $h\,\mathbf{H}_i$", h * H_i, BLUE, f"weight h = {h}"),
        (r"2. Social Cohesion $c\,\mathbf{C}_i$", c * C_i, AQUA, f"weight c = {c}"),
        (r"3. Avoidance $\rho_a\,\mathbf{R}_{a,i}$", rho_a * R_a, "#d9534f", f"weight $\\rho_a$ = {rho_a} (highest)"),
        (r"4. Predator Escape $\rho_s\,\mathbf{R}_{s,i}$", rho_s * R_s, ORANGE, f"weight $\\rho_s$ = {rho_s}"),
        (r"5. Noise $e\,\mathbf{\epsilon}_i$", e * eps, MUTED, f"weight e = {e}"),
    ]
    legend_handles = []
    for label, vec, color, note in vectors:
        tip = vec * scale
        ax1.annotate("", xy=tip, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=color, lw=2.2))
        legend_handles.append(Line2D([0], [0], color=color, lw=2.2, label=f"{label} ({note})"))

    tip_res = H_prime * (scale * 0.42)
    ax1.annotate("", xy=tip_res, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=INK, lw=3.2))
    legend_handles.append(Line2D([0], [0], color=INK, lw=3.2,
                                 label=r"Resultant Heading $\mathbf{H}_i'$ ($\mathbf{x}_i^{t+1} = \mathbf{x}_i^t + \delta\,\mathbf{H}_i' / \|\mathbf{H}_i'\|$)"))
    ax1.scatter(0, 0, s=70, color=INK, zorder=5)
    ax1.text(0, -2.5, "Sheep $i$", color=INK, fontsize=9, fontweight="bold", ha="center")
    ax1.text(vectors[0][1][0] * scale + 0.5, vectors[0][1][1] * scale + 1.0, r"$h\,\mathbf{H}_i$", color=BLUE, fontsize=9, fontweight="bold")
    ax1.text(vectors[1][1][0] * scale + 1.0, vectors[1][1][1] * scale, r"$c\,\mathbf{C}_i$", color=AQUA, fontsize=9, fontweight="bold")
    ax1.text(vectors[2][1][0] * scale - 2.0, vectors[2][1][1] * scale - 2.0, r"$\rho_a\,\mathbf{R}_{a,i}$", color="#d9534f", fontsize=9, fontweight="bold")
    ax1.text(vectors[3][1][0] * scale + 1.0, vectors[3][1][1] * scale, r"$\rho_s\,\mathbf{R}_{s,i}$", color=ORANGE, fontsize=9, fontweight="bold")
    ax1.text(vectors[4][1][0] * scale - 2.0, vectors[4][1][1] * scale + 1.0, r"$e\,\mathbf{\epsilon}_i$", color=MUTED, fontsize=9, fontweight="bold")
    ax1.text(tip_res[0] + 1.2, tip_res[1] - 1.2, r"$\mathbf{H}_i'$ (Resultant)", color=INK, fontsize=9.5, fontweight="bold")
    ax1.legend(handles=legend_handles, loc="lower left", frameon=False, fontsize=8)
    ax1.set_xlim(-30, 25)
    ax1.set_ylim(-30, 20)
    style_map(ax1, r"B. 5 competing instinct forces and Resultant heading $\mathbf{H}_i'$")

    caption(fig, "The 5 Strömbom (2014) sheep instincts. Left: focal sheep i senses nearby flock-mates, "
            "an intruding neighbor closer than personal space r_a = 2 m, and a dog within threat horizon r_s = 65 m. "
            "Right: weighted sum of the 5 unit vectors. Collision avoidance carries the highest weight (rho_a = 2.0), "
            "preventing stampedes, while cohesion (c = 1.05) and predator flight (rho_s = 1.0) steer the sheep safely away.", 150)
    fig.tight_layout(rect=(0, 0, 1, 0.90))
    fig.savefig(OUT / "fig_sheep_forces.png", dpi=150)
    plt.close(fig)


def fig_independent() -> None:
    """Comparison of strombom_multi vs uncoordinated independent controllers."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.0))
    rng = np.random.default_rng(2026)

    # Panel 1: strombom_multi (wide start, D=4)
    c_wide = cfg("wide", 100, 4)
    sheep_w = place_flock(c_wide, rng)
    dogs_w = place_dogs(c_wide)
    goal_w = np.asarray(c_wide["goal_center"])
    centroid_w = sheep_w.mean(axis=0)
    thresh_w = collect_threshold(100, c_wide["r_a"])
    dists_w = np.linalg.norm(sheep_w - centroid_w, axis=1)
    far_w = dists_w > thresh_w
    targets_multi = team_targets(sheep_w, goal_w, dogs_w, c_wide)

    ax0 = axes[0]
    ax0.scatter(*sheep_w[~far_w].T, s=9, color=BLUE, alpha=0.6, lw=0)
    ax0.scatter(*sheep_w[far_w].T, s=16, color=BLUE, ec=INK, lw=0.6)
    ax0.scatter(*centroid_w, s=40, marker="+", color=INK, zorder=4)
    ax0.text(centroid_w[0] + 3, centroid_w[1] + 3, "GCM", color=INK, fontsize=8)
    ax0.scatter(*dogs_w.T, s=42, marker="^", color=ORANGE, ec=SURFACE, lw=0.8, zorder=4)
    ax0.scatter(*targets_multi.T, s=36, marker="x", color=INK, lw=1.4, zorder=4)
    for dog, tgt in zip(dogs_w, targets_multi):
        ax0.annotate("", xy=tgt, xytext=dog, arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))
    ax0.set_xlim(centroid_w[0] - 130, centroid_w[0] + 80)
    ax0.set_ylim(centroid_w[1] - 110, centroid_w[1] + 110)
    style_map(ax0, "strombom_multi: Hungarian Matching (Parallel)")

    # Panel 2: independent collecting (wide start, D=4)
    ax1 = axes[1]
    ax1.scatter(*sheep_w[~far_w].T, s=9, color=BLUE, alpha=0.6, lw=0)
    ax1.scatter(*sheep_w[far_w].T, s=16, color=BLUE, ec=INK, lw=0.6)
    ax1.scatter(*centroid_w, s=40, marker="+", color=INK, zorder=4)
    ax1.text(centroid_w[0] + 3, centroid_w[1] + 3, "GCM", color=INK, fontsize=8)
    ax1.scatter(*dogs_w.T, s=42, marker="^", color=ORANGE, ec=SURFACE, lw=0.8, zorder=4)

    dec = decide(sheep_w, goal_w, c_wide)
    single_tgt = dec.target
    farthest_stray = sheep_w[dec.outliers[0]]
    ax1.scatter(*farthest_stray, s=90, facecolors="none", ec=ORANGE, lw=1.5, zorder=3)
    ax1.scatter(*single_tgt, s=70, marker="x", color=INK, lw=1.8, zorder=4)
    for dog in dogs_w:
        ax1.annotate("", xy=single_tgt, xytext=dog, arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2, ls="--"))
    ax1.set_xlim(centroid_w[0] - 130, centroid_w[0] + 80)
    ax1.set_ylim(centroid_w[1] - 110, centroid_w[1] + 110)
    style_map(ax1, "independent: Collect (All 4 dogs chase 1 stray)")

    # Panel 3: independent driving (compact start, D=4)
    c_comp = cfg("compact", 100, 4)
    sheep_c = place_flock(c_comp, np.random.default_rng(2026))
    dogs_c = place_dogs(c_comp)
    goal_c = np.asarray(c_comp["goal_center"])
    centroid_c = sheep_c.mean(axis=0)
    targets_arc = team_targets(sheep_c, goal_c, dogs_c, c_comp)
    pd_single = drive_point(sheep_c, goal_c, c_comp)

    ax2 = axes[2]
    ax2.scatter(*sheep_c.T, s=9, color=BLUE, alpha=0.7, lw=0)
    ax2.scatter(*centroid_c, s=40, marker="+", color=INK, zorder=4)
    ax2.text(centroid_c[0] + 2, centroid_c[1] + 2, "GCM", color=INK, fontsize=8)
    ax2.scatter(*dogs_c.T, s=42, marker="^", color=ORANGE, ec=SURFACE, lw=0.8, zorder=4)
    ordered_arc = targets_arc[np.argsort(targets_arc[:, 1])]
    ax2.plot(*ordered_arc.T, color=AQUA, lw=1.2, ls=":", label="strombom_multi arc")
    ax2.scatter(*pd_single, s=80, marker="x", color=INK, lw=2.0, zorder=4, label="independent Pd (single)")
    for dog in dogs_c:
        ax2.annotate("", xy=pd_single, xytext=dog, arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2, ls="--"))
    ax2.annotate("", xy=goal_c - [c_comp["goal_radius"] + 5, 0], xytext=centroid_c + [20, 0],
                 arrowprops=dict(arrowstyle="->", color=AQUA, lw=1.2))
    ax2.text(centroid_c[0] + 25, centroid_c[1] + 3, "to goal", color=AQUA, fontsize=8)
    ax2.set_xlim(centroid_c[0] - 50, centroid_c[0] + 40)
    ax2.set_ylim(centroid_c[1] - 45, centroid_c[1] + 45)
    ax2.legend(loc="upper left", frameon=False, fontsize=8)
    style_map(ax2, "independent: Drive (Crowding single point Pd)")

    caption(fig, "Comparison of multi-dog controllers: strombom_multi vs independent. Left: strombom_multi "
            "assigns strays 1-to-1 via Hungarian matching, gathering multiple strays in parallel. "
            "Middle: independent controller lacks team coordination; every dog targets the same single "
            "farthest stray, chasing one sheep sequentially. Right: during drive mode, independent dogs "
            "all converge on a single Pd point without fanning out along an arc.", 150)
    fig.tight_layout(rect=(0, 0, 1, 0.88))
    fig.savefig(OUT / "fig_independent.png", dpi=150)
    plt.close(fig)


def fig_hungarian_matching() -> None:
    """Outlier detection geometry and Hungarian matching vs naive crossing."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.8))
    rng = np.random.default_rng(2026)
    c = cfg("wide", 100, 4)
    sheep = place_flock(c, rng)
    dogs = place_dogs(c)
    goal = np.asarray(c["goal_center"])
    centroid = sheep.mean(axis=0)
    thresh = collect_threshold(100, c["r_a"])
    dists = np.linalg.norm(sheep - centroid, axis=1)
    far = dists > thresh
    outlier_indices = np.argsort(dists)[::-1][:4]

    ax0 = axes[0]
    ax0.add_patch(Circle(xy(centroid), thresh, fc="#2a78d6", alpha=0.04, ec=MUTED, lw=1.2, ls="--", label=r"threshold $f(N) = r_a N^{2/3}$"))
    ax0.scatter(*sheep[~far].T, s=18, color=BLUE, alpha=0.6, lw=0, label="sheep inside the flock")
    ax0.scatter(*sheep[far].T, s=30, color=BLUE, ec=INK, lw=0.8, label=r"outliers ($> f(N)$)")
    ax0.scatter(*centroid, s=65, marker="+", color=INK, lw=2.0, zorder=5)
    ax0.text(centroid[0] + 3, centroid[1] - 4, "GCM (flock centre)", color=INK, fontsize=9, fontweight="bold")

    stray_idx = outlier_indices[0]
    stray_pos = sheep[stray_idx]
    vec_gcm_stray = unit(stray_pos - centroid)
    # drawn four times farther out than the real r_a, or the cross would sit on the sheep
    pc_pos = stray_pos + float(c["r_a"]) * 4.0 * vec_gcm_stray

    ax0.annotate("", xy=pc_pos, xytext=centroid, arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0, ls=":"))
    ax0.scatter(*stray_pos, s=95, facecolors="none", ec=ORANGE, lw=1.8, zorder=4)
    ax0.text(stray_pos[0] + 3, stray_pos[1] - 2, r"outlier $o$", color=ORANGE, fontsize=9.5, fontweight="bold")
    ax0.scatter(*pc_pos, s=90, marker="x", color=INK, lw=2.2, zorder=5)
    ax0.text(pc_pos[0] + 3, pc_pos[1] + 3, r"collect point $P_c$" + "\n" + r"($r_a = 2$ m behind, drawn 4x)", color=INK, fontsize=9, fontweight="bold")
    ax0.text(centroid[0] - thresh * 0.72, centroid[1] + thresh * 0.72, r"flock region: $f(N) = r_a N^{2/3}$", color=MUTED, fontsize=8.5)
    ax0.legend(loc="lower left", frameon=False, fontsize=8.5)
    ax0.set_xlim(centroid[0] - 130, centroid[0] + 90)
    ax0.set_ylim(centroid[1] - 110, centroid[1] + 110)
    style_map(ax0, "A. outliers and the collect point Pc")

    ax1 = axes[1]
    targets = team_targets(sheep, goal, dogs, c)
    ax1.scatter(*sheep[~far].T, s=15, color=BLUE, alpha=0.5, lw=0)
    ax1.scatter(*sheep[far].T, s=28, color=BLUE, ec=INK, lw=0.6)
    ax1.scatter(*centroid, s=50, marker="+", color=MUTED, lw=1.5, zorder=3)
    ax1.scatter(*dogs.T, s=70, marker="^", color=ORANGE, ec=SURFACE, lw=1.0, zorder=5, label="dogs ($D = 4$)")
    ax1.scatter(*targets.T, s=65, marker="x", color=INK, lw=1.8, zorder=5, label="collect points $P_{c,1..4}$")

    for dog, tgt in zip(dogs, targets):
        ax1.annotate("", xy=tgt, xytext=dog, arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.8))

    ax1.plot([dogs[0, 0], targets[2, 0]], [dogs[0, 1], targets[2, 1]], color="#d9534f", ls="--", lw=1.0, alpha=0.45, label="a crossing assignment (drawn by hand)")
    ax1.plot([dogs[2, 0], targets[0, 0]], [dogs[2, 1], targets[0, 1]], color="#d9534f", ls="--", lw=1.0, alpha=0.45)

    for i, d in enumerate(dogs):
        ax1.text(d[0] - 16, d[1] - 2, f"dog {i+1}", color=ORANGE, fontsize=8.5, fontweight="bold")

    ax1.legend(loc="lower left", frameon=False, fontsize=8.5)
    ax1.set_xlim(centroid[0] - 130, centroid[0] + 90)
    ax1.set_ylim(centroid[1] - 110, centroid[1] + 110)
    style_map(ax1, "B. Hungarian assignment: no two paths cross")

    caption(fig, "Outlier detection and Hungarian assignment in strombom_multi. Left: any sheep outside "
            "f(N) = r_a N^(2/3) triggers collection mode; waypoint P_c is placed r_a behind the stray "
            "along the ray from GCM. Right: Hungarian bipartite matching assigns dogs 1-to-1 to waypoints, "
            "minimizing total travel distance and preventing trajectory collisions (dashed red shows "
            "naive greedy crossing).", 150)
    fig.tight_layout(rect=(0, 0, 1, 0.90))
    fig.savefig(OUT / "fig_hungarian_matching.png", dpi=150)
    plt.close(fig)


def fig_driving_arc() -> None:
    """Driving arc formation and nominal drive point geometry."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.8))
    c = cfg("compact", 100, 4)
    sheep = place_flock(c, np.random.default_rng(2026))
    dogs = place_dogs(c)
    goal = np.asarray(c["goal_center"])
    centroid = sheep.mean(axis=0)
    r_flock = radius_of(sheep, centroid)
    pd = drive_point(sheep, goal, c)

    ax0 = axes[0]
    ax0.add_patch(Circle(xy(centroid), r_flock, fc="#2a78d6", alpha=0.15, ec=BLUE, lw=1.2, label=r"the flock ($R_{\mathrm{flock}} \propto r_a\sqrt{N}$)"))
    ax0.scatter(*sheep.T, s=14, color=BLUE, alpha=0.7, lw=0)
    ax0.scatter(*centroid, s=65, marker="+", color=INK, lw=2.0, zorder=4)
    ax0.text(centroid[0] + 1.5, centroid[1] - 3.5, "GCM", color=INK, fontsize=9, fontweight="bold")

    goal_dir = unit(goal - centroid)
    ax0.annotate("", xy=centroid + goal_dir * 32, xytext=centroid,
                 arrowprops=dict(arrowstyle="->", color=AQUA, lw=2.0))
    ax0.text(centroid[0] + 16, centroid[1] + 3.0, r"toward the goal $\mathbf{x}_{\mathrm{goal}}$", color=AQUA, fontsize=9, fontweight="bold")
    ax0.plot([centroid[0], pd[0]], [centroid[1], pd[1]], color=MUTED, ls=":", lw=1.2)
    ax0.scatter(*pd, s=95, marker="x", color=INK, lw=2.2, zorder=5, label=r"drive point $P_d$")
    ax0.text(pd[0] - 2, pd[1] - 4.5, r"$P_d$ ($r_a\sqrt{N}$ behind the GCM)", color=INK, fontsize=9, fontweight="bold", ha="center")

    mid_standoff = (centroid + pd) / 2.0
    ax0.text(mid_standoff[0] - 1.5, mid_standoff[1] + 2.5, r"offset $r_a\sqrt{N} = 20$ m", color=MUTED, fontsize=8.5, ha="center")
    ax0.legend(loc="upper left", frameon=False, fontsize=8.5)
    ax0.set_xlim(centroid[0] - 35, centroid[0] + 38)
    ax0.set_ylim(centroid[1] - 28, centroid[1] + 28)
    style_map(ax0, "A. the drive point Pd")

    ax1 = axes[1]
    targets_arc = team_targets(sheep, goal, dogs, c)
    ax1.scatter(*sheep.T, s=14, color=BLUE, alpha=0.6, lw=0)
    ax1.scatter(*centroid, s=50, marker="+", color=MUTED, lw=1.5, zorder=3)

    ordered_arc = targets_arc[np.argsort(targets_arc[:, 1])]
    ax1.plot(*ordered_arc.T, color=AQUA, lw=2.0, ls="-", label="driving arc")
    ax1.scatter(*targets_arc.T, s=65, marker="x", color=INK, lw=1.8, zorder=4, label="arc slots")
    ax1.scatter(*dogs.T, s=70, marker="^", color=ORANGE, ec=SURFACE, lw=1.0, zorder=5, label="dogs ($D = 4$)")

    for i, (dog, tgt) in enumerate(zip(dogs, targets_arc)):
        ax1.annotate("", xy=tgt, xytext=dog, arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.6))
        push_dir = unit(centroid - tgt)
        ax1.annotate("", xy=tgt + push_dir * 6, xytext=tgt, arrowprops=dict(arrowstyle="->", color=AQUA, lw=1.2, ls="--"))
        ax1.text(dog[0] - 16, dog[1] - 2, f"dog {i+1}", color=ORANGE, fontsize=8.5, fontweight="bold")

    ax1.text(centroid[0] + 2, centroid[1] + r_flock + 2, "upper flank covered", color=AQUA, fontsize=8.5, fontstyle="italic")
    ax1.text(centroid[0] + 2, centroid[1] - r_flock - 4, "lower flank covered", color=AQUA, fontsize=8.5, fontstyle="italic")
    ax1.annotate("", xy=goal - [c["goal_radius"] + 5, 0], xytext=centroid + [25, 0],
                 arrowprops=dict(arrowstyle="->", color=AQUA, lw=1.5))
    ax1.text(centroid[0] + 27, centroid[1] + 2, "toward the goal", color=AQUA, fontsize=8.5, fontweight="bold")
    ax1.legend(loc="upper left", frameon=False, fontsize=8.5)
    ax1.set_xlim(centroid[0] - 65, centroid[0] + 55)
    ax1.set_ylim(centroid[1] - 55, centroid[1] + 55)
    style_map(ax1, "B. the driving arc round the flock's sides")

    caption(fig, "Driving formation geometry in strombom_multi. Left: the nominal driving point P_d is "
            "placed r_a*sqrt(N) behind GCM along the goal ray, keeping shepherds immediately outside the flock disk. "
            "Right: multi-dog driving arc fanning out shepherds across the flock width, preventing flanking escapes.", 150)
    fig.tight_layout(rect=(0, 0, 1, 0.90))
    fig.savefig(OUT / "fig_driving_arc.png", dpi=150)
    plt.close(fig)


def main() -> None:
    fig_sheep_forces()
    fig_team_rule()
    fig_hungarian_matching()
    fig_driving_arc()
    fig_fat()
    fig_independent()
    fig_kubo()
    fig_lama()
    fig_task_geometry()
    fig_layouts()
    fig_dog_starts()
    fig_trial()


if __name__ == "__main__":
    main()
