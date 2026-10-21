"""Figures for design_v2.md, drawn from the real code (placement, shepherd rule, formation, a real trial).

    cd /home/gwen/HerdSim && uv run --with matplotlib python docs/science/figures/make_figures.py

matplotlib is not a project dependency; uv adds it for this one run. Every position in the figures
comes from the same functions a campaign uses, so the pictures change when the code changes.
"""

from __future__ import annotations

import math
import os
import sys
from pathlib import Path

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Circle, Rectangle  # noqa: E402

from sim.core.simulation_runner import initial_state, run_trial  # noqa: E402
from sim.core.world.layouts import (  # noqa: E402
    dog_start_radius,
    layout_extent,
    place_dogs,
    place_flock,
)
from sim.methods.strombom.heuristics import COLLECT, decide  # noqa: E402
from sim.plugins.dogs.collect_drive_multi import drive_slot  # noqa: E402
from tests.helpers import config_for  # noqa: E402

OUT = Path(__file__).resolve().parent
SHEEP, DOG, GOAL, GREY, RED = "#3b6fb6", "#d9731f", "#2e8b57", "#8a8a8a", "#c0392b"
RF = {5: 3.14, 10: 4.35, 25: 6.2, 50: 7.6, 100: 9.08, 200: 10.47, 400: 11.4}  # calibrated, see design_v2


def save(fig, name: str) -> None:
    fig.savefig(OUT / f"{name}.png", dpi=130, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", name)


def cell(n: int, d: int, layout: str = "compact", **kw):
    return config_for("strombom_multi", n=n, d=d, layout=layout, flock_radius=RF.get(n, 11.4), **kw)


def draw_goal(ax, cfg, label=True):
    c = cfg["goal_center"]
    ax.add_patch(Circle(c, cfg["goal_radius"], fc=GOAL, alpha=0.18, ec=GOAL, lw=1.5))
    if label:
        ax.annotate("goal", (c[0], c[1]), ha="center", va="center", color=GOAL, fontsize=9)


def draw_agents(ax, sheep, dogs, s=7, dog_s=60):
    ax.scatter(sheep[:, 0], sheep[:, 1], s=s, c=SHEEP, zorder=3)
    if len(dogs):
        ax.scatter(dogs[:, 0], dogs[:, 1], s=dog_s, c=DOG, marker="^", ec="black", lw=0.5, zorder=4)


def frame(ax, centre, half, title):
    ax.set_xlim(centre[0] - half, centre[0] + half)
    ax.set_ylim(centre[1] - half, centre[1] + half)
    ax.set_aspect("equal")
    ax.set_title(title, fontsize=10)
    ax.tick_params(labelsize=7)


# --- 1. the field --------------------------------------------------------------------------
def fig_field():
    cfg = cell(100, 24)
    w, h, k = cfg["world_width"], cfg["world_height"], cfg["field_clearance"]
    sheep = place_flock(cfg, np.random.default_rng(1))
    dogs = place_dogs(cfg)
    fig, ax = plt.subplots(figsize=(9, 6.2))
    ax.add_patch(Rectangle((0, 0), w, h, fill=False, ec="black", lw=1.6))
    ax.add_patch(Rectangle((k, k), w - 2 * k, h - 2 * k, fill=False, ec=GREY, ls="--", lw=1))
    draw_goal(ax, cfg)
    draw_agents(ax, sheep, dogs)
    c = cfg["flock_center"]
    g = cfg["goal_center"]
    ax.add_patch(Circle(c, cfg["flock_radius"], fill=False, ec=SHEEP, lw=1.2, ls=":"))
    ax.annotate("", xy=(g[0] - cfg["goal_radius"], g[1] - 38), xytext=(c[0], c[1] - 38),
                arrowprops=dict(arrowstyle="<->", color="black"))
    drive = g[0] - c[0]
    ax.text((c[0] + g[0]) / 2, c[1] - 52, f"drive = {drive:.0f}  (13 x R_f = 13 x {cfg['flock_radius']:.2f})",
            ha="center", fontsize=9)
    ax.annotate("sheep flock, radius R_f", (c[0] + 4, c[1] + cfg["flock_radius"]), (c[0] + 5, c[1] + 62),
                fontsize=9, arrowprops=dict(arrowstyle="-", color=GREY))
    ax.annotate("24 dogs on arcs behind the flock", (dogs[0, 0], dogs[0, 1]), (k + 2, h - k - 10), fontsize=9,
                arrowprops=dict(arrowstyle="-", color=GREY))
    ax.annotate("", xy=(0, h - k / 2), xytext=(k, h - k / 2), arrowprops=dict(arrowstyle="<->", color=GREY))
    ax.text(k / 2, h - k / 2 + 6, "clearance 80", ha="center", fontsize=8, color=GREY)
    ax.text(w / 2, 6, f"field {w:.0f} x {h:.0f}  (N = 100, compact start, D = 24; one field per protocol and N)",
            ha="center", fontsize=9)
    ax.set_xlim(-10, w + 10)
    ax.set_ylim(-10, h + 10)
    ax.set_aspect("equal")
    ax.set_title("Figure 1. The field of one cell. Dashed line: the clearance kept free around the task", fontsize=10)
    save(fig, "fig01_field")


# --- 2. layouts ----------------------------------------------------------------------------
def fig_layouts():
    names = ["compact", "wide", "split", "outlier_rich"]
    fig, axes = plt.subplots(1, 4, figsize=(17, 4.8))
    cfgs = {name: cell(100, 8, name) for name in names}
    half = max(dog_start_radius(c) for c in cfgs.values()) + 12
    for ax, name in zip(axes, names):
        cfg = cfgs[name]
        sheep = place_flock(cfg, np.random.default_rng(3))
        dogs = place_dogs(cfg)
        c = cfg["flock_center"]
        ax.add_patch(Circle(c, cfg["separation_distance"], fill=False, ec=RED, ls="--", lw=1))
        ax.add_patch(Circle(c, layout_extent(cfg), fill=False, ec=GREY, ls=":", lw=1))
        draw_goal(ax, cfg, label=False)
        draw_agents(ax, sheep, dogs)
        far = np.linalg.norm(sheep - np.asarray(c), axis=1).max()
        collect = "collects" if far > cfg["separation_distance"] else "drives"
        frame(ax, c, half, f"{name}\nfarthest sheep {far:.0f}: dog {collect}")
    axes[0].text(0.02, 0.02, "red dashed: collect distance 2 N^(2/3) = 43\ngrey dotted: farthest a sheep can start",
                 transform=axes[0].transAxes, fontsize=7, va="bottom")
    fig.suptitle("Figure 2. The four starting layouts, N = 100 (same scale in every panel)", fontsize=11)
    save(fig, "fig02_layouts")


# --- 3. the one-dog rule -------------------------------------------------------------------
def fig_rule():
    cfg = cell(50, 1)
    rng = np.random.default_rng(5)
    compact = place_flock(cfg, rng)
    stray = compact.copy()
    stray[0] = compact.mean(axis=0) + np.array([-34.0, 22.0])
    goal = np.asarray(cfg["goal_center"])
    dog_start = place_dogs(cfg)[0]
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.8))
    for ax, flock, label in zip(axes, (compact, stray), ("drive", "collect")):
        d = decide(flock, goal, cfg)
        gcm = d.centroid
        ax.add_patch(Circle(gcm, 2.0 * 50 ** (2 / 3), fill=False, ec=RED, ls="--", lw=1))
        ax.add_patch(Circle(dog_start, cfg["r_s"], fill=False, ec=DOG, ls=":", lw=1))
        ax.add_patch(Circle(dog_start, 3 * cfg["r_a"], fill=False, ec=DOG, lw=1))
        draw_agents(ax, flock, dog_start[None], s=14, dog_s=90)
        ax.scatter(*gcm, marker="x", c="black", s=40, zorder=5)
        ax.scatter(*d.target, marker="*", c=DOG, s=170, ec="black", lw=0.6, zorder=5)
        ax.annotate("", xy=d.target, xytext=dog_start, arrowprops=dict(arrowstyle="->", color=DOG, lw=1.4))
        ax.annotate("flock centre (GCM)", gcm, gcm + np.array([-10, -34]), fontsize=8,
                    arrowprops=dict(arrowstyle="-", color=GREY))
        point = "Pd" if d.mode != COLLECT else "Pc"
        ax.annotate(f"target {point}", d.target, d.target + np.array([-14, 14]), fontsize=8,
                    arrowprops=dict(arrowstyle="-", color=GREY))
        ax.annotate("", xy=gcm + np.array([40, 0]), xytext=gcm + np.array([20, 0]),
                    arrowprops=dict(arrowstyle="->", color=GOAL))
        ax.text(gcm[0] + 42, gcm[1], "to goal", color=GOAL, fontsize=8, va="center")
        frame(ax, gcm + np.array([-18, 0]), 62, f"mode: {d.mode}")
    axes[0].text(0.02, 0.02, "red dashed: f(N) = r_a N^(2/3) = 27\norange dotted: sheep reaction distance r_s = 65\n"
                 "orange solid: stop distance 3 r_a = 6 (the dog stands still inside it)",
                 transform=axes[0].transAxes, fontsize=7, va="bottom")
    fig.suptitle("Figure 3. Strombom 2014 shepherd rule, N = 50, one dog (computed by the same function the runs use)",
                 fontsize=11)
    save(fig, "fig03_rule")


# --- 4. many dogs on rings -----------------------------------------------------------------
def fig_formation():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.6))
    for ax, d in zip(axes, (8, 24, 64)):
        cfg = cell(100, d, settings={"dog_radius": 1.0}, params={"drive_edge_limit": 0.6})
        sheep = place_flock(cfg, np.random.default_rng(2))
        goal = np.asarray(cfg["goal_center"])
        dec = decide(sheep, goal, cfg)
        slots = np.array([drive_slot(dec, i, d, 2.0 * 1.0) for i in range(d)])
        draw_agents(ax, sheep, np.zeros((0, 2)), s=9)
        ring = np.array([np.linalg.norm(p - dec.centroid) for p in slots])
        order = np.unique(np.round(ring, 1))
        for i, r in enumerate(order):  # one colour per ring: darker is the first ring
            on = np.round(ring, 1) == r
            ax.scatter(slots[on, 0], slots[on, 1], s=34, marker="^", ec="black", lw=0.5, zorder=4,
                       c=DOG, alpha=max(0.35, 1.0 - 0.18 * i))
        ax.scatter(*dec.centroid, marker="x", c="black", s=40, zorder=5)
        ax.annotate("", xy=dec.centroid + np.array([45, 0]), xytext=dec.centroid + np.array([22, 0]),
                    arrowprops=dict(arrowstyle="->", color=GOAL))
        frame(ax, dec.centroid + np.array([-12, 0]), 62, f"D = {d}")
    fig.suptitle("Figure 4. Drive slots with dog_radius 1 (dogs keep 2 apart), N = 100. "
                 "The first ring holds 32 dogs; more dogs open further rings behind it. None stands in front.",
                 fontsize=10)
    save(fig, "fig04_formation")


# --- 5/6. a trial, snapshot by snapshot ----------------------------------------------------
def snapshots(cfg, seed, picks, fname, title, half):
    start = initial_state(cfg, seed)
    taken: dict = {0: (start.sheep_positions.copy(), start.shepherd_positions.copy())}

    def keep(state):
        t = state.tick
        if t in picks:
            taken[t] = (state.sheep_positions.copy(), state.shepherd_positions.copy())
        taken["last"] = (t, state.sheep_positions.copy(), state.shepherd_positions.copy())

    result = run_trial(cfg, seed, on_tick=keep)
    ticks = [0] + [t for t in picks if t in taken] + ["last"]
    everyone = np.vstack(taken[0])
    goal = np.asarray(cfg["goal_center"])
    x0, x1 = everyone[:, 0].min() - 15, goal[0] + cfg["goal_radius"] + 15
    y0, y1 = everyone[:, 1].min() - 20, everyone[:, 1].max() + 20
    fig, axes = plt.subplots(len(ticks), 1, figsize=(9, 2.9 * len(ticks) * (y1 - y0) / (x1 - x0) * 3.1))
    for ax, t in zip(axes, ticks):
        if t == "last":
            tick, sheep, dogs = taken["last"]
        else:
            tick, (sheep, dogs) = t, taken[t]
        draw_goal(ax, cfg, label=False)
        draw_agents(ax, sheep, dogs, s=9, dog_s=50)
        ax.set_xlim(x0, x1)
        ax.set_ylim(y0, y1)
        ax.set_aspect("equal")
        ax.tick_params(labelsize=7)
        ax.set_title(f"tick {tick}" + ("  (success)" if t == "last" and result.success else ""), fontsize=9)
    fig.tight_layout(rect=(0, 0, 1, 0.975))
    fig.suptitle(title, fontsize=11)
    save(fig, fname)
    return result


def fig_trials():
    cfg = cell(100, 2, "compact", ticks=1500)
    snapshots(cfg, 2026, (30, 70, 130), "fig05_trial_compact",
              "Figure 5. One real trial: compact start, N = 100, D = 2 (seed 2026). Dogs drive the flock to the goal.", 80)
    cfg = cell(200, 2, "wide", ticks=4000)
    snapshots(cfg, 2026, (50, 120, 200), "fig06_trial_wide",
              "Figure 6. One real trial: wide start, N = 200, D = 2 (seed 2026). The dogs first collect, then drive.", 150)


# --- 7. flock size -------------------------------------------------------------------------
def fig_flock_size():
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    sn = [5, 10, 25, 50, 100, 200, 400]
    ax.plot(sn, [3.14, 4.35, 6.2, 7.6, 9.08, 10.47, 11.4], "o-", c=SHEEP, label="Strombom sheep, one dog (calibrated)")
    ax.plot([25, 50, 100, 200, 400], [6.3, 8.04, 10.18, 12.56, 14.63], "s-", c=DOG, label="FAT (same sheep, other dogs)")
    ax.plot([25, 50, 100], [6.19, 6.06, 5.9], "^-", c=GOAL, label="Kubo (point-particle sheep)")
    big = np.array([400, 800, 1200, 1600])
    ax.plot(big, 11.4 * np.sqrt(big / 400), "o--", c=SHEEP, mfc="white", label="Strombom beyond 400: imposed density rule")
    ax.scatter([14], [1.21 * 2 / 1.25 * 1.0], c="black", marker="*", s=120, zorder=5,
               label="real flock, 14 sheep (Jadhav 2024), see text")
    ax.set_xscale("log")
    ax.set_xlabel("number of sheep N")
    ax.set_ylabel("flock radius R_f (units; 1 unit ~ 1 m)")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    ax.set_title("Figure 7. Flock radius R_f against N", fontsize=10)
    save(fig, "fig07_flock_size")


# --- 8. local view -------------------------------------------------------------------------
def fig_local_view():
    cfg = cell(200, 4, "wide")
    sheep = place_flock(cfg, np.random.default_rng(4))
    dogs = place_dogs(cfg)
    c = cfg["flock_center"]
    dog = dogs[len(dogs) // 2]
    fig, ax = plt.subplots(figsize=(7.4, 7.0))
    dist = np.linalg.norm(sheep - dog, axis=1)
    seen = dist < 65.0
    ax.scatter(sheep[~seen, 0], sheep[~seen, 1], s=9, c="#b8c4d6", zorder=3)
    ax.scatter(sheep[seen, 0], sheep[seen, 1], s=11, c=SHEEP, zorder=3)
    for rng_, ls in ((15, ":"), (45, "--"), (65, "-")):
        ax.add_patch(Circle(dog, rng_, fill=False, ec=DOG, ls=ls, lw=1.2))
        ax.text(dog[0] + rng_ * 0.72, dog[1] + rng_ * 0.72, str(rng_), color=DOG, fontsize=8)
    draw_agents(ax, np.zeros((0, 2)), dogs, dog_s=40)
    ax.scatter(*dog, s=120, marker="^", c=DOG, ec="black", zorder=6)
    ax.add_patch(Circle(c, cfg["separation_distance"], fill=False, ec=RED, ls="--", lw=1))
    draw_goal(ax, cfg, label=False)
    counts = ", ".join(f"{int(np.sum(dist < r))} at {r}" for r in (15, 45, 65))
    frame(ax, c, 150, "Figure 8. What one dog sees (wide start, N = 200, dog on its start arc).\n"
          f"Sheep in range: {counts} (of 200). Grey sheep are out of range.")
    save(fig, "fig08_local_view")


# --- 9. time courses -----------------------------------------------------------------------
def fig_time_courses():
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.6))
    for ax, (n, layout, ticks) in zip(axes, ((100, "compact", 600), (200, "wide", 3000))):
        for d, colour in ((1, GREY), (4, DOG)):
            cfg = cell(n, d, layout, ticks=ticks)
            h = run_trial(cfg, 2026).history
            ax.plot(h.index, h["gcm_goal"], c=colour, label=f"D = {d}")
        ax.set_xlabel("tick (1 tick = 1 s)")
        ax.set_ylabel("distance of the flock centre to the goal")
        ax.set_title(f"N = {n}, {layout} start", fontsize=10)
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)
    fig.suptitle("Figure 9. Distance of the flock centre to the goal during one trial (seed 2026)", fontsize=11)
    save(fig, "fig09_time_courses")


if __name__ == "__main__":
    for fn in (fig_field, fig_layouts, fig_rule, fig_formation, fig_trials, fig_flock_size, fig_local_view,
               fig_time_courses):
        fn()
