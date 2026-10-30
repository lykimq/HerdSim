"""How a team of shepherds shares the work: the team rule, independent shepherds, Hungarian
matching and the driving arc."""

from __future__ import annotations

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Circle

from docs.generate_docs.figstyle import (
    AQUA,
    BLUE,
    INK,
    MUTED,
    ORANGE,
    save,
)
from docs.generate_docs.model_figures.scene import (
    RED,
    arrow,
    cfg,
    dogs_at,
    flock_split,
    gcm,
    start,
    style_map,
    targets_at,
    window,
    xy,
)
from sim.core.vectors import unit
from sim.methods.strombom.heuristics import collect_threshold, decide, drive_point, radius_of
from sim.plugins.dogs.collect_drive_multi import team_targets


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
