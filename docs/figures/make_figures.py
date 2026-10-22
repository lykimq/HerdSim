"""Figures of the D_min report (docs/report), drawn from the real code and the pilot trials.

    uv run --with matplotlib python docs/figures/make_figures.py

Needs matplotlib (not a project dependency). Every picture calls the same functions a campaign
uses (start layouts, dog arcs, the team rule, a real trial), so if the code changes, running
this script redraws them. The pictures are written next to this script. Flock radii come from
the calibration of the finished runs. Figures 18 and 19 read results/dmin_pilot/trials.csv and
are skipped when it is missing. The results figures (20 to 26) are drawn by
make_result_figures.py. Figure 10 reads data/wall_check_trials.csv, the trials of the wall check
that was run with the reflecting boundary before it was removed from the code.
"""

from __future__ import annotations

import sys
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import NullFormatter  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

from analysis.dmin import at_deadline  # noqa: E402
from services.cells import Cell, Group, cell_config  # noqa: E402
from services.protocol import load_protocol  # noqa: E402
from sim.core.simulation_runner import initial_state, run_trial  # noqa: E402
from sim.core.world.layouts import (  # noqa: E402
    dog_start_radius,
    layout_extent,
    place_dogs,
    place_flock,
)
from sim.core.vectors import behind, farthest_from, unit  # noqa: E402
from sim.methods.kubo.forces import clamp_speed, dog_velocity, sheep_velocities  # noqa: E402
from sim.methods.strombom import sheep as ssheep  # noqa: E402
from sim.methods.strombom.heuristics import collect_threshold, decide  # noqa: E402
from sim.plugins.dogs.collect_drive_multi import team_targets  # noqa: E402
from tests.helpers import config_for  # noqa: E402

OUT = Path(__file__).parent
SURFACE, INK, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"  # categorical slots 1 to 3


def calibrated(protocol: str, fallback: dict[int, float]) -> dict[int, float]:
    """Flock radii of a finished run (results/<protocol>/calibration.json), else the fallback."""
    import json

    path = REPO / "results" / protocol / "calibration.json"
    if not path.exists():
        return fallback
    radii = json.loads(path.read_text())["flock_radius"]["strombom_multi"]
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
    """Wrapped caption at the top left of the figure."""
    fig.text(0.01, 0.995, textwrap.fill(text, width), ha="left", va="top", fontsize=9, color=MUTED)


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
    ax.add_patch(plt.Circle(goal, c["goal_radius"], fc="none", ec=AQUA, lw=1.5))
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
        ax.add_patch(plt.Circle(center, f, fc="none", ec=MUTED, lw=0.9, ls="--"))
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


def fig_sheep_rule() -> None:
    """The Strombom sheep heading, computed from the code, and the reaction distance."""
    c = config_for("strombom_multi", n=12, d=1)
    rng = np.random.default_rng(3)
    focal = np.zeros(2)
    near = np.array([[1.1, 0.9], [-1.0, 1.1]])  # inside r_a
    others = rng.normal(0.0, 4.5, (9, 2)) + [4.0, 0.5]
    pos = np.vstack([focal, near, others])
    dog = np.array([[-30.0, -12.0]])
    prev = np.zeros_like(pos)
    prev[0] = unit(np.array([0.8, 0.6]))
    idx = np.array([0])
    k = len(pos) - 1
    parts = {
        "inertia  h H": float(c["inertia"]) * prev[0],
        "to neighbours  c C": float(c["c"]) * unit(ssheep.neighbour_centres(pos, idx, k)[0] - focal),
        "from close sheep  rho_a R_a": float(c["rho_a"]) * unit(
            ssheep.sheep_repulsion(pos, idx, c["r_a"])[0]),
        "from the dog  rho_s R_s": float(c["rs_weight"]) * unit(focal - dog[0]),
        "noise  e eps": float(c["noise_strength"]) * np.array([np.cos(2.4), np.sin(2.4)]),
    }
    total = unit(sum(parts.values()))
    draws = ssheep.SheepDraws(np.ones(len(pos)), np.zeros(len(pos)), np.full(len(pos), 2.4))
    code = ssheep.velocities(pos, prev, dog, draws, c, k)[0]
    assert np.allclose(code, total * c["sheep_speed"]), "figure disagrees with the sheep code"
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.4))
    ax = axes[0]
    colors = [MUTED, BLUE, ORANGE, "#e87ba4", "#6250d6"]
    ax.add_patch(plt.Circle(focal, c["r_a"], fc="none", ec=ORANGE, lw=0.8, ls="--"))
    ax.scatter(*pos[1:].T, s=26, color="#a8a7a0", lw=0)
    ax.scatter(*focal, s=60, color=INK, zorder=4)
    for (label, vec), color in zip(parts.items(), colors):
        ax.annotate("", xy=vec * 3.2, xytext=focal,
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.6))
    ax.annotate("", xy=total * 3.2, xytext=focal, arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.4))
    from matplotlib.lines import Line2D

    handles = [Line2D([0], [0], color=col, lw=2, label=f"{label}  (weight {np.linalg.norm(v):.2g})")
               for (label, v), col in zip(parts.items(), colors)]
    handles.append(Line2D([0], [0], color=INK, lw=3, label="new heading H' (unit length)"))
    ax.legend(handles=handles, loc="lower left", frameon=False, fontsize=8)
    ax.text(-8.6, 7.2, "dashed circle: r_a = 2; the dog is 32 away, to the lower left",
            color=MUTED, fontsize=8)
    ax.set_xlim(-9, 9)
    ax.set_ylim(-11, 8)
    style_map(ax, "one sheep inside the reaction distance: its five terms")
    # reaction distance
    ax = axes[1]
    rng = np.random.default_rng(5)
    rad = 105 * np.sqrt(rng.random(70))
    ang = rng.uniform(0, 2 * np.pi, 70)
    herd = np.stack([rad * np.cos(ang), rad * np.sin(ang)], axis=1) + [20.0, 0.0]
    d0 = np.zeros((1, 2))
    drw = ssheep.draw(np.random.default_rng(8), len(herd))
    kk = int(c["r_s"])
    vel = ssheep.velocities(herd, np.zeros_like(herd), d0, drw, c, len(herd) - 1)
    reacting = np.linalg.norm(herd - d0[0], axis=1) < c["r_s"]
    ax.add_patch(plt.Circle(d0[0], c["r_s"], fc=ORANGE, ec=ORANGE, alpha=0.07, lw=1.0))
    ax.scatter(*herd[~reacting].T, s=14, color="#a8a7a0", lw=0)
    ax.scatter(*herd[reacting].T, s=14, color=BLUE, lw=0)
    for p0, v in zip(herd[reacting], vel[reacting]):
        ax.annotate("", xy=p0 + v * 7, xytext=p0, arrowprops=dict(arrowstyle="->", color=BLUE, lw=0.8))
    ax.scatter(*d0.T, s=60, marker="^", color=ORANGE, zorder=4)
    ax.text(0, -kk - 12, f"reaction distance r_s = {kk}: inside, a sheep moves; outside, it grazes",
            ha="center", color=MUTED, fontsize=8)
    ax.set_xlim(-90, 135)
    ax.set_ylim(-100, 105)
    style_map(ax, "who reacts to the dog")
    caption(fig, "The Strombom et al. (2014) sheep, computed with the HerdSim code (the figure "
            "checks its own arrow against the code). A sheep closer than r_s to a dog takes the "
            "weighted sum of five unit vectors, shown with their weights, and moves one step along "
            "it; a sheep farther away grazes. Arrow lengths on the left are the weights times 3.", 130)
    fig.tight_layout(rect=(0, 0, 1, 0.9))
    fig.savefig(OUT / "fig1_sheep_rule.png", dpi=150)
    plt.close(fig)


def fig_shepherd() -> None:
    """The paper's shepherd: collect or drive, one dog."""
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.2))
    for ax, layout, mode in ((axes[0], "wide", "collect"), (axes[1], "compact", "drive")):
        c = cfg(layout, 100, 1)
        sheep = place_flock(c, np.random.default_rng(2026))
        dog = place_dogs(c)
        goal = np.asarray(c["goal_center"])
        d = decide(sheep, goal, c)
        f = collect_threshold(100, c["r_a"])
        far = np.linalg.norm(sheep - d.centroid, axis=1) > f
        ax.add_patch(plt.Circle(d.centroid, f, fc="none", ec=MUTED, lw=0.9, ls="--"))
        ax.add_patch(plt.Circle(dog[0], 3 * c["r_a"], fc=ORANGE, ec="none", alpha=0.2))
        ax.scatter(*sheep[~far].T, s=11, color=BLUE, alpha=0.7, lw=0)
        ax.scatter(*sheep[far].T, s=22, color=BLUE, ec=INK, lw=0.7)
        ax.scatter(*dog.T, s=50, marker="^", color=ORANGE, ec=SURFACE, lw=0.8, zorder=4)
        ax.scatter(*d.centroid, s=40, marker="+", color=INK, zorder=4)
        ax.scatter(*d.target, s=60, marker="x", color=INK, lw=1.6, zorder=4)
        ax.annotate("", xy=d.target, xytext=dog[0], arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.4))
        ax.text(d.centroid[0] + 2, d.centroid[1] + 2, "GCM", color=INK, fontsize=8)
        ax.text(d.target[0], d.target[1] - 8, "Pc" if mode == "collect" else "Pd", color=INK,
                fontsize=9, ha="center")
        if mode == "collect":
            fi = d.outliers[0]
            ax.scatter(*sheep[fi], s=70, facecolors="none", ec=ORANGE, lw=1.4)
            ax.text(sheep[fi][0], sheep[fi][1] + 8, "farthest from the GCM", color=INK, fontsize=8,
                    ha="center")
            ax.set_xlim(d.centroid[0] - 130, d.centroid[0] + 70)
            ax.set_ylim(d.centroid[1] - 95, d.centroid[1] + 95)
            style_map(ax, "collect: a sheep is beyond f(N)")
            ax.set_xlabel("Pc is r_a behind the farthest sheep, seen from the GCM", color=MUTED, fontsize=8)
        else:
            ax.annotate("", xy=d.centroid + [40, 0], xytext=d.centroid + [14, 0],
                        arrowprops=dict(arrowstyle="->", color=AQUA, lw=1.4))
            ax.text(d.centroid[0] + 42, d.centroid[1], "goal", color=AQUA, va="center", fontsize=9)
            ax.set_xlim(d.centroid[0] - 60, d.centroid[0] + 65)
            ax.set_ylim(d.centroid[1] - 50, d.centroid[1] + 50)
            style_map(ax, "drive: every sheep is within f(N)")
            ax.set_xlabel("Pd is r_a sqrt(N) behind the GCM, seen from the goal", color=MUTED, fontsize=8)
    caption(fig, "The shepherd of Strombom et al. (2014), one dog, N = 100, from the code. Dashed "
            "circle: f(N) = r_a N^(2/3) around the GCM, the centre of mass. The dog collects while "
            "any sheep is beyond it and drives otherwise, walks straight at its point with the sheep "
            "noise, and stands still within 3 r_a of a sheep (shaded).", 130)
    fig.tight_layout(rect=(0, 0, 1, 0.88))
    fig.savefig(OUT / "fig2_shepherd.png", dpi=150)
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
    assert np.allclose(code, clamp_speed(sum(terms.values())[None, :], c["sheep_speed_max"])[0]), \
        "figure disagrees with the Kubo sheep code"
    ax = axes[0]
    ax.add_patch(plt.Circle(focal, c["sheep_radius"], fc="none", ec=MUTED, lw=0.8, ls="--"))
    ax.scatter(*nbr.T, s=24, color="#a8a7a0", lw=0)
    ax.scatter(*dog.T, s=50, marker="^", color=ORANGE, zorder=4)
    ax.scatter(*focal, s=50, color=INK, zorder=4)
    palette = [MUTED, BLUE, AQUA, ORANGE]
    from matplotlib.lines import Line2D

    legend_s = []
    for (label, v), col in zip(terms.items(), palette):
        mag = float(np.linalg.norm(v))
        tip = unit(v) * np.sqrt(mag) * 3.2
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
        tip = unit(v) * np.sqrt(mag) * 3.2
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
    cen = sh.mean(axis=0)
    ax.add_patch(plt.Circle(np.asarray(ck["goal_center"]), ck["goal_radius"], fc="none", ec=AQUA, lw=1.4))
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
        ax.add_patch(plt.Circle(goal, c["goal_radius"], fc="none", ec=AQUA, lw=1.5))
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


def pilot() -> pd.DataFrame | None:
    path = REPO / "results" / "dmin_pilot" / "trials.csv"
    return pd.read_csv(path, skiprows=1) if path.exists() else None


def fig_pilot_success(trials: pd.DataFrame) -> None:
    speed = {"strombom_multi": 1.0}
    colors = {3: BLUE, 6: ORANGE, 12: AQUA}
    panels = [("wide", 200), ("wide", 400), ("outlier_rich", 200), ("outlier_rich", 400)]
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.2), sharey=True)
    for ax, (layout, n) in zip(axes, panels):
        for m, color in colors.items():
            rows = at_deadline(trials, m, speed)
            rows = rows[(rows["initial_layout"] == layout) & (rows["n_sheep"] == n)]
            rate = rows.groupby("n_shepherds")["success"].mean()
            ax.plot(rate.index, rate.values, color=color, lw=2, marker="o", ms=4,
                    label=f"deadline {m} drive times")
        ax.axhline(0.9, color=MUTED, lw=0.8, ls="--")
        ax.set_xscale("log")
        ax.set_xticks([1, 2, 4, 8, 16])
        ax.set_xticklabels(["1", "2", "4", "8", "16"])
        ax.set_xlim(0.85, 24)
        ax.set_ylim(-0.03, 1.05)
        ax.set_title(f"{layout}, N = {n}")
        ax.set_xlabel("dogs D")
        ax.grid(axis="y", color=GRID, lw=0.6)
    axes[0].set_ylabel("success rate")
    axes[0].legend(loc="lower right", frameon=False, fontsize=8)
    caption(fig, "Pilot: success against D at deadlines of 3, 6 and 12 drive times. Dashed line: "
            "theta = 0.90. 10 seeds per point, so this is a map and not a result.", 170)
    fig.tight_layout(rect=(0, 0, 1, 0.9))
    fig.savefig(OUT / "fig18_pilot_success.png", dpi=150)
    plt.close(fig)


def fig_pilot_finish(trials: pd.DataFrame) -> None:
    n = 200
    won = trials[trials["success"] & (trials["n_sheep"] == n)]
    drive = float(trials[trials["n_sheep"] == n]["drive_distance"].iloc[0])
    fig, ax = plt.subplots(figsize=(7.4, 4.0))
    colors = {"compact": BLUE, "wide": ORANGE, "outlier_rich": AQUA}
    for layout, color in colors.items():
        rows = won[won["initial_layout"] == layout]
        med = rows.groupby("n_shepherds")["finish_seconds"].median()
        ax.plot(med.index, med.values, color=color, lw=2, marker="o", ms=4, label=layout)
    for m in (3, 6, 12):
        ax.axhline(m * drive, color=MUTED, lw=0.8, ls="--")
        ax.text(26, m * drive, f"deadline {m} drive times", color=MUTED, va="bottom",
                ha="right", fontsize=8)
    ax.legend(loc="lower left", bbox_to_anchor=(0.02, 0.07), frameon=False, fontsize=8)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks([1, 2, 4, 8, 16])
    ax.set_xticklabels(["1", "2", "4", "8", "16"])
    ax.set_xlim(0.9, 28)
    ax.set_xlabel("dogs D")
    ax.set_ylabel("median finish time of successful trials (s)")
    ax.set_title(f"Why the deadline matters (pilot, N = {n}, drive time {drive:.0f} s)")
    ax.grid(axis="y", color=GRID, lw=0.6)
    fig.tight_layout()
    fig.savefig(OUT / "fig19_finish_vs_deadline.png", dpi=150)
    plt.close(fig)


def field_config(n: int, max_dogs: int) -> dict:
    """Run config of a cell of the dmin protocol, whose field is sized for all four layouts and
    for ``max_dogs`` dogs; the field is the same for every cell of that N and largest D."""
    from dataclasses import replace

    protocol = load_protocol("dmin_m12", output=Path("/tmp/herdsim-figures"))
    protocol = replace(protocol, shepherd_counts=(1, max_dogs))
    return cell_config(protocol, Cell(Group("strombom_multi", "wide", (), n), max_dogs), RF[n])


def fig_wall_check() -> None:
    path = OUT / "data" / "wall_check_trials.csv"
    if not path.exists():
        print("data/wall_check_trials.csv missing: figure 10 skipped")
        return
    t = pd.read_csv(path)
    colors = {80.0: ORANGE, 250.0: BLUE, 3000.0: AQUA}
    names = {80.0: "walls, clearance 80", 250.0: "walls, clearance 250",
             3000.0: "no wall reached (3000)"}
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.3), sharey=True)
    panels = [("wide", 400), ("split", 400), ("outlier_rich", 400), (None, 200)]
    for ax, (layout, n) in zip(axes, panels):
        rows = t[t["n_sheep"] == n] if layout is None else t[(t["n_sheep"] == n) &
                                                              (t["initial_layout"] == layout)]
        for clearance, color in colors.items():
            rate = rows[rows["field_clearance"] == clearance].groupby("n_shepherds")["success"].mean()
            ax.plot(rate.index, rate.values, color=color, lw=2, marker="o", ms=4,
                    label=names[clearance])
        ax.set_xscale("log")
        ax.set_xticks([1, 2, 3, 4, 6, 8])
        ax.set_xticklabels(["1", "2", "3", "4", "6", "8"])
        ax.set_title(f"{layout}, N = {n}" if layout else f"all scattered layouts, N = {n}")
        ax.set_xlabel("dogs D")
        ax.set_ylim(-0.03, 1.05)
        ax.grid(axis="y", color=GRID, lw=0.6)
    axes[0].set_ylabel("success rate")
    axes[0].legend(loc="upper left", frameon=False, fontsize=8)
    caption(fig, "Wall check: success against D with a reflecting wall at clearance 80 (the old "
            "default), clearance 250 and clearance 3000, where no trial reaches a wall. Deadline 6 "
            "drive times, 20 seeds per point, same seeds in every line. The clear difference is "
            "outlier_rich at N = 400 (D = 6: 0.85 with the wall, 0.55 without); elsewhere the "
            "lines overlap within the noise of 20 seeds.", 170)
    fig.tight_layout(rect=(0, 0, 1, 0.88))
    fig.savefig(OUT / "fig10_wall_check.png", dpi=150)
    plt.close(fig)


def reach_scene(ax, c, sheep, dogs, rs: float) -> float:
    """Sheep within ``rs`` of some dog are blue, the rest grey; returns the share out of reach."""
    near = (np.linalg.norm(sheep[:, None] - dogs[None], axis=2).min(axis=1) < rs)
    for dog in dogs:
        ax.add_patch(plt.Circle(dog, rs, fc=ORANGE, ec="none", alpha=0.08))
        ax.add_patch(plt.Circle(dog, rs, fc="none", ec=ORANGE, lw=0.5, alpha=0.5))
    ax.scatter(*sheep[near].T, s=8, color=BLUE, lw=0)
    ax.scatter(*sheep[~near].T, s=8, color="#a8a7a0", lw=0)
    ax.scatter(*dogs.T, s=34, marker="^", color=ORANGE, ec=SURFACE, lw=0.8, zorder=3)
    ax.add_patch(plt.Circle(np.asarray(c["goal_center"]), c["goal_radius"], fc="none", ec=AQUA,
                            lw=1.5))
    return float(1.0 - near.mean())


def fig_start_distances() -> None:
    layouts = ("compact", "wide", "split", "outlier_rich")
    sizes = (100, 200, 400)
    fig, axes = plt.subplots(4, 3, figsize=(12, 11))
    for r, layout in enumerate(layouts):
        for k, n in enumerate(sizes):
            ax = axes[r, k]
            c = cfg(layout, n, 1)
            sheep = place_flock(c, np.random.default_rng(2026))
            dog = place_dogs(c)
            centre = np.asarray(c["flock_center"])
            out = reach_scene(ax, c, sheep, dog, c["r_s"])
            dist = float(np.linalg.norm(dog[0] - centre))
            ax.plot([dog[0, 0], centre[0]], [dog[0, 1], centre[1]], color=MUTED, lw=0.8, ls=":")
            ax.annotate(f"{dist:.0f}", xy=((dog[0, 0] + centre[0]) / 2, centre[1] + 6),
                        color=INK, ha="center", fontsize=9)
            ax.set_xlim(centre[0] - 250, centre[0] + 240)
            ax.set_ylim(centre[1] - 215, centre[1] + 215)
            style_map(ax, f"{layout}, N = {n}: {100 * out:.0f}% out of reach")
    fig.text(0.01, 0.012, "blue: sheep within 65 of the dog, they react at tick 0", color=BLUE)
    fig.text(0.40, 0.012, "grey: out of reach, they graze until a dog comes", color="#7c7b75")
    fig.text(0.74, 0.012, "number: dog to flock centre", color=INK)
    caption(fig, "How the start looks with one dog on arcs, same scale in every panel. The dog "
            "(orange triangle) and the circle of radius 65 within which a sheep reacts to it. "
            "The dog always starts 30 beyond the farthest sheep that can start, so its distance "
            "to the flock grows with the layout and N.", 120)
    fig.tight_layout(rect=(0, 0.02, 1, 0.94))
    fig.savefig(OUT / "fig11_start_distances.png", dpi=150)
    plt.close(fig)


MATCHED ={"params": {"r_a": 1.0, "noise_strength": 0.1, "r_s": 75.0},
           "settings": {"separation_scale": 1.0, "dog_overlap_distance": 1.0}}
# Calibrated flock radii of the matched set, from dmin_s_matched when it is present.
RF_MATCHED = calibrated("dmin_s_matched", {100: 6.60, 200: 6.82})


def fig_realism_numbers() -> None:
    """Real flock (Jadhav et al., reported numbers) against the base and matched sets."""
    names = ["real flock\n(14 sheep)", "base\n(N = 100)", "matched\n(N = 100)"]
    colors = [MUTED, BLUE, ORANGE]
    real_radius = 1.5 * 1.21  # disc radius from the reported mean radius 1.21 m
    panels = [
        ("flock radius (m)", [real_radius, RF[100], RF_MATCHED[100]], None),
        ("density (sheep per m2)",
         [14 / (np.pi * real_radius**2), 100 / (np.pi * RF[100] ** 2),
          100 / (np.pi * RF_MATCHED[100] ** 2)], None),
        ("dog behind the flock centre (m)", [5.0, 2.0 * np.sqrt(100), 1.0 * np.sqrt(100)],
         (3.0, 7.0)),
        ("dog stop distance (m)", [2.5, 6.0, 3.0], (1.0, 4.0)),
    ]
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.6))
    for ax, (title, vals, band) in zip(axes, panels):
        ax.bar(range(3), vals, 0.62, color=colors)
        if band is not None:
            ax.vlines(0, band[0], band[1], color=INK, lw=1.6)
            ax.hlines([band[0], band[1]], -0.08, 0.08, color=INK, lw=1.6)
        for i, v in enumerate(vals):
            ax.text(i, v, f"{v:.2g}", ha="center", va="bottom", fontsize=8, color=INK)
        ax.set_xticks(range(3))
        ax.set_xticklabels(names, fontsize=8)
        ax.set_title(title)
        ax.set_ylim(0, max(vals + [band[1] if band else 0]) * 1.2)
        ax.grid(axis="y", color=GRID, lw=0.6)
    caption(fig, "The real flock against the base setting (Strombom Table 1) and the field-matched "
            "set, at N = 100. Real values are the numbers reported by Jadhav et al. for 14 sheep "
            "and one dog: flock radius from the mean radius 1.21 m, dog 3 to 7 m from the centre "
            "and 1 to 4 m from the rear sheep (black bars give the range). The model flock is "
            "larger, so the densities are not those of equal flocks; the matched set is closer on "
            "every row. Reaction distance: base 65, matched 75, real not measured.", 150)
    fig.tight_layout(rect=(0, 0, 1, 0.82))
    fig.savefig(OUT / "fig14_realism_numbers.png", dpi=150)
    plt.close(fig)


def driven_flock(radius: float, params=None, settings=None, tick: int = 120):
    """State of a compact N = 100 flock driven by one dog, at ``tick``."""
    c = config_for("strombom_multi", n=100, d=1, flock_radius=radius, ticks=600,
                   params=params, settings=settings)
    seen = {}

    def keep(state) -> None:
        if state.tick == tick:
            seen["state"] = (state.sheep_positions.copy(), state.shepherd_positions.copy())

    run_trial(c, 2026, on_tick=keep)
    return c, seen["state"]


def fig_matched_scene() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(13, 5.6))
    for ax, (label, radius, kw) in zip(
        axes[:2], [("base", RF[100], {}), ("field-matched", RF_MATCHED[100], MATCHED)]
    ):
        c, (sheep, dogs) = driven_flock(radius, kw.get("params"), kw.get("settings"))
        centre = sheep.mean(axis=0)
        dog = dogs[0]
        ax.add_patch(plt.Circle(dog, 3.0 * c["r_a"], fc=ORANGE, ec="none", alpha=0.18))
        ax.add_patch(plt.Circle(centre, radius, fc="none", ec=BLUE, lw=0.9, ls=":"))
        ax.scatter(*sheep.T, s=9, color=BLUE, lw=0)
        ax.scatter(*dog, s=44, marker="^", color=ORANGE, ec=SURFACE, lw=0.8, zorder=3)
        ax.plot([dog[0], centre[0]], [dog[1], centre[1]], color=MUTED, lw=0.8, ls=":")
        ax.set_xlim(centre[0] - 40, centre[0] + 25)
        ax.set_ylim(centre[1] - 32, centre[1] + 32)
        style_map(ax, f"{label}: dog {np.linalg.norm(dog - centre):.0f} behind the centre\n"
                      f"flock radius {radius:.1f} (dotted), stop distance {3 * c['r_a']:.0f} "
                      f"(shaded)")
    # goal radius against the settled flock
    c, (sheep, _) = driven_flock(RF[100])
    centred = sheep - sheep.mean(axis=0)
    ax = axes[2]
    ax.scatter(*centred.T, s=9, color=BLUE, lw=0)
    ring_colors = {1.9: AQUA, 1.5: ORANGE, 1.3: "#eda100", 1.1: MUTED}
    far = np.linalg.norm(centred, axis=1)
    lines = []
    for mult, color in ring_colors.items():
        ax.add_patch(plt.Circle((0, 0), mult * RF[100], fc="none", ec=color, lw=1.4))
        lines.append((mult, color, int((far > mult * RF[100]).sum())))
    for k, (mult, color, out) in enumerate(lines):
        ax.text(0.02, 0.02 + 0.06 * (3 - k), f"goal {mult} R_f: {out} sheep outside", color=INK,
                transform=ax.transAxes, va="bottom", fontsize=8)
        ax.plot([0.0], [0.0], color=color)
    ax.set_xlim(-22, 22)
    ax.set_ylim(-34, 22)
    style_map(ax, "goal radius against the driven flock")
    caption(fig, "The base and the field-matched sets as driven flocks, N = 100, one dog, at tick "
            "120, on one scale. The matched flock is tighter, the dog drives from half the "
            "distance and stops at half the distance. Right: the flock centred in goals of "
            "different radii (green 1.9, orange 1.5, yellow 1.3, grey 1.1 flock radii). Success "
            "needs every sheep inside, so a tighter goal leaves stragglers outside the settled flock; "
            "1.5 is the tightest value that still works.", 125)
    fig.tight_layout(rect=(0, 0, 1, 0.8))
    fig.savefig(OUT / "fig15_matched_scene.png", dpi=150)
    plt.close(fig)


def fig_variants() -> None:
    n = 200
    variants = [
        ("base: arcs, gap 30", RF[n], {}, {}),
        ("matched sheep set", RF_MATCHED[n], MATCHED["params"], MATCHED["settings"]),
        ("handler start", RF[n], {}, {"dog_start": "handler"}),
        ("ring start", RF[n], {}, {"dog_start": "ring"}),
        ("gap 15", RF[n], {}, {"dog_start_gap": 15.0}),
        ("gap 60", RF[n], {}, {"dog_start_gap": 60.0}),
        ("goal 1.5 flock radii", RF[n], {}, {"goal_radius_multiple": 1.5}),
    ]
    fig, axes = plt.subplots(2, 4, figsize=(13, 6.6))
    for ax, (label, radius, params, settings) in zip(axes.flat, variants):
        c = config_for("strombom_multi", n=n, d=4, layout="wide", flock_radius=radius,
                       params=params, settings=settings)
        sheep = place_flock(c, np.random.default_rng(2026))
        dogs = place_dogs(c)
        centre = np.asarray(c["flock_center"])
        draw_scene(ax, c, sheep, dogs, goal_arrow=False)
        ax.set_xlim(centre[0] - 175, centre[0] + 175)
        ax.set_ylim(centre[1] - 175, centre[1] + 175)
        nearest = np.linalg.norm(sheep[:, None] - dogs[None], axis=2).min()
        style_map(ax, label)
        note = "; 4 dogs on one point" if settings.get("dog_start") == "handler" else ""
        ax.set_xlabel(f"dog to centre {np.linalg.norm(dogs - centre, axis=1).max():.0f}, "
                      f"nearest sheep {nearest:.0f}{note}", color=MUTED, fontsize=8)
    ax = axes.flat[-1]
    ax.axis("off")
    ax.text(0.0, 0.8, "dog speed 1.15:\nthe start looks the same as\nthe base; only the dogs'\n"
            "pace changes", transform=ax.transAxes, color=MUTED, va="top", fontsize=9)
    caption(fig, "The start of each sensitivity run, wide layout, N = 200, 4 dogs, one scale and "
            "one seed. The matched set shrinks the flock and the scatter, so the dogs start much "
            "closer. Handler puts all dogs at one point, ring spreads them round the flock, the "
            "gap moves the first circle in or out, and a tighter goal is a smaller teal circle.",
            140)
    fig.tight_layout(rect=(0, 0, 1, 0.9))
    fig.savefig(OUT / "fig16_variants.png", dpi=150)
    plt.close(fig)


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
    ax.add_patch(plt.Rectangle((0, 0), c["world_width"], c["world_height"], fc="none", ec=GRID,
                               lw=1.0))
    ax.add_patch(plt.Circle(centre, reach, fc=BLUE, ec="none", alpha=0.10))
    ax.add_patch(plt.Circle(centre, rf, fc="none", ec=BLUE, lw=1.0, ls=":"))
    sheep = place_flock({**c, "initial_layout": "compact"}, np.random.default_rng(2026))
    ax.scatter(*sheep.T, s=7, color=BLUE, lw=0)
    ax.add_patch(plt.Circle(goal, c["goal_radius"], fc="none", ec=AQUA, lw=1.6))
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
    rfs = {25: 6.2, **{k: v for k, v in RF.items()}}
    t1, t2, t3, actual = [], [], [], []
    for k in ns:
        ck = field_config(k, 24)
        ext = max(layout_extent({**ck, "initial_layout": m}) for m in layouts)
        t1.append(13.0 * ck["flock_radius"])
        t2.append(80.0)
        t3.append(ext + ck["goal_radius"] + ck["flock_radius"])
        actual.append(float(ck["goal_center"][0] - ck["flock_center"][0]))
    ax = fig.add_subplot(grid[0, 1])
    ax.plot(ns, t1, color=BLUE, lw=1.6, marker="o", ms=3, label="13 R_f")
    ax.plot(ns, t2, color=MUTED, lw=1.2, ls="--", label="minimum 80")
    ax.plot(ns, t3, color=ORANGE, lw=1.6, marker="o", ms=3,
            label="reach + goal radius + R_f")
    ax.plot(ns, actual, color=INK, lw=0.8, marker="s", ms=6, mfc="none", label="drive length used")
    ax.set_xscale("log")
    ax.set_xticks(ns)
    ax.set_xticklabels([str(k) for k in ns])
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xlabel("flock size N")
    ax.set_ylabel("length")
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
    ax.set_ylabel("length")
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
    fig_sheep_rule()
    fig_shepherd()
    fig_team_rule()
    fig_fat()
    fig_kubo()
    fig_task_geometry()
    fig_layouts()
    fig_dog_starts()
    fig_trial()
    fig_start_distances()
    fig_realism_numbers()
    fig_matched_scene()
    fig_variants()
    fig_wall_check()
    trials = pilot()
    if trials is None:
        print("results/dmin_pilot/trials.csv missing: figures 18 and 19 skipped")
        return
    fig_pilot_success(trials)
    fig_pilot_finish(trials)


if __name__ == "__main__":
    main()
