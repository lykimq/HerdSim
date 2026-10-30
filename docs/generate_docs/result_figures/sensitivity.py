"""Variants of the base design: sensitivity, fat targets, metrics, spacing, holding goal and
view range."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from analysis.curves import bracket
from docs.generate_docs.figstyle import (
    AQUA,
    BLUE,
    INK,
    MUTED,
    ORANGE,
    SURFACE,
    grid,
    save,
)
from docs.generate_docs.report.text import dmin_text
from docs.generate_docs.result_figures.common import (
    LAYOUT_COLOR,
    MAIN_RUNS,
    SEQ,
    cells,
    curve,
    d_axis,
    group_row,
    groups,
    have,
    rate_line,
    short,
    theta_line,
    trials,
)
from services.protocol import RESULTS_ROOT


def fig_sensitivity() -> None:
    """D_min of each sensitivity run on the shared grid (6 drive times), shaded by D_min. Light
    cells are open (a bracket or a lower bound); hatched cells have no reliable D up to 16. Rows
    above the line use strict success, rows below 99 percent of the flock."""
    variants = ["matched", "handler", "ring", "goal", "gap", "dogspeed"]
    if not have(*[f"dmin_{rule}s_{v}" for rule in ("", "f99_") for v in ["base", *variants]]):
        return
    cols = [
        ("wide", 100),
        ("wide", 200),
        ("wide", 400),
        ("outlier_rich", 100),
        ("outlier_rich", 200),
        ("outlier_rich", 400),
    ]
    rows_of_rule = (  # (row label, run suffix, factor level picked from a swept run)
        ("base", "base", None),
        ("matched sheep set", "matched", None),
        ("handler start", "handler", None),
        ("ring start", "ring", None),
        ("goal 1.5 R_f", "goal", None),
        ("gap 15", "gap", "15.0"),
        ("gap 60", "gap", "60.0"),
        ("dog speed 1.15", "dogspeed", None),
    )
    darkest = 16  # D_min that gets the darkest shade

    def row(name: str, factor: str | None) -> list[tuple[str, float]]:
        g = groups(name)
        if factor is not None:
            g = g[g["factors"].str.contains(factor, regex=False)]
        out = []
        for lay, n in cols:
            r = group_row(g, lay, n)
            text = dmin_text(r).replace("none on grid", "none")
            value = r["d_min"] if not np.isnan(r["d_min"]) else r["d_min_low"]
            out.append((text, value))
        return out

    rows = []
    for rule, rule_label in (("", "strict"), ("f99_", "99%")):
        for k, (label, suffix, factor) in enumerate(rows_of_rule):
            name = f"{rule_label}: {label}" if k == 0 else label
            rows.append((name, row(f"dmin_{rule}s_{suffix}", factor)))
    fig, ax = plt.subplots(figsize=(11, 7.6))
    for i, (_, cells_) in enumerate(rows):
        for j, (text, value) in enumerate(cells_):
            if text == "none" or np.isnan(value):
                ax.add_patch(
                    Rectangle(
                        (j - 0.5, i - 0.5), 1, 1, fc="#d9d8d3", ec=SURFACE, lw=1.5, hatch="//"
                    )
                )
                ax.text(j, i, "none", ha="center", va="center", fontsize=8, color=INK)
                continue
            shade = np.log2(max(value, 1)) / np.log2(darkest)
            open_ = text.startswith("[") or "-" in text
            ax.add_patch(
                Rectangle(
                    (j - 0.5, i - 0.5),
                    1,
                    1,
                    fc=SEQ(min(shade, 1)),
                    ec=SURFACE,
                    lw=1.5,
                    alpha=0.55 if open_ else 1.0,
                )
            )
            ax.text(
                j,
                i,
                text,
                ha="center",
                va="center",
                fontsize=9,
                color="white" if shade > 0.55 and not open_ else INK,
            )
    ax.set_xlim(-0.5, len(cols) - 0.5)
    ax.set_ylim(len(rows) - 0.5, -0.5)
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels([f"{short(lay)}\nN = {n}" for lay, n in cols], fontsize=8.5)
    ax.xaxis.tick_top()
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=9)
    ax.axhline(len(rows) / 2 - 0.5, color=INK, lw=1)
    for side in ("left", "bottom", "top"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=0)
    save(fig, "fig24_sensitivity.png", rect=(0, 0, 1, 0.98))


def fig_fat() -> None:
    """The team rule against FAT, where every dog aims behind the sheep farthest from the goal,
    on the same task, seeds and deadline (6 drive times). FAT success does not rise with D: its
    dogs pick the same sheep and move as copies. Hollow: fewer than 30 trials. Dotted: theta."""
    runs = (
        ("dmin_m6", "strombom_multi, strict", BLUE, "o", "-"),
        ("dmin_f99_m6", "strombom_multi, 99 percent", BLUE, "s", "--"),
        ("dmin_fat", "FAT, strict", ORANGE, "^", "-"),
        ("dmin_f99_fat", "FAT, 99 percent", ORANGE, "v", "--"),
    )
    panels = [("compact", 400), ("wide", 200), ("wide", 400), ("outlier_rich", 200), ("split", 200)]
    if not have(*[r[0] for r in runs]):
        return
    data = {r[0]: cells(r[0]) for r in runs}
    fig, axes = plt.subplots(1, len(panels), figsize=(14, 3.9), sharey=True)
    for ax, (lay, n) in zip(axes, panels):
        for name, label, color, marker, ls in runs:
            rate_line(ax, curve(data[name], lay, n), color, marker, ls=ls, label=label)
        theta_line(ax)
        d_axis(ax)
        ax.set_title(f"{lay}, N = {n}", fontsize=10)
        grid(ax)
    axes[0].set_ylabel("success rate")
    fig.legend(
        *axes[0].get_legend_handles_labels(),
        loc="lower center",
        ncol=4,
        frameon=False,
        fontsize=8.5,
    )
    save(fig, "fig26_fat.png", rect=(0, 0.1, 1, 0.98))


def fig_metrics() -> None:
    """Flock spread against success across cells, and dog crowding and standing still by layout.

    The trials hold the mean, min and max of every per-tick metric over the whole trial. Panel
    (a) correlates a cell's success rate with its mean flock spread (RMS distance to the
    centroid); panels (b) and (c) read the share of dogs standing still and the share of dogs
    with a twin within 2 units, for the three scattered layouts at N = 200.
    """
    strict, f99 = MAIN_RUNS[6]
    if not have(strict, f99):
        return
    from scipy.stats import spearmanr

    min_seeds = 20  # cells with fewer seeds are left out
    n_panels = 200
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.2))

    ax = axes[0]
    rho_text = []
    for name, marker, label in ((strict, "o", "strict"), (f99, "s", "99 percent")):
        t = trials(name)
        c = (
            t.groupby(["initial_layout", "n_sheep", "n_shepherds"])
            .agg(success=("success", "mean"), spread=("mean_extent", "mean"), n=("success", "size"))
            .reset_index()
        )
        c = c[c["n"] >= min_seeds]
        rho = spearmanr(c["spread"], c["success"])[0]
        rho_text.append(f"{label}: Spearman {rho:.2f} ({len(c)} cells)")
        for layout, color in LAYOUT_COLOR.items():
            part = c[c["initial_layout"] == layout]
            ax.scatter(
                part["spread"],
                part["success"],
                s=22,
                marker=marker,
                color=color,
                alpha=0.6,
                lw=0,
                label=f"{layout}, {label}" if layout == "wide" else None,
            )
    ax.text(
        0.98,
        0.04,
        "\n".join(rho_text),
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=8.5,
        color=INK,
    )
    ax.set_xlabel("mean flock spread over the trial (RMS distance to centroid)")
    ax.set_ylabel("success rate of the cell")
    ax.set_title("(a) spread against success, deadline 6, cells with >= 20 seeds", fontsize=9.5)
    grid(ax)
    handles = [
        Line2D([], [], color=c, marker="o", ls="", label=name) for name, c in LAYOUT_COLOR.items()
    ]
    handles += [
        Line2D([], [], color=MUTED, marker="o", ls="", label="strict"),
        Line2D([], [], color=MUTED, marker="s", ls="", label="99 percent"),
    ]
    ax.legend(handles=handles, frameon=False, fontsize=7.5, loc="center right")

    t = trials(f99)
    t = t[t["n_sheep"] == n_panels]
    panels = (
        (
            axes[1],
            "mean_dogs_stopped",
            "(b) dogs standing still",
            "share of dogs standing still\n(median over trials)",
        ),
        (
            axes[2],
            "mean_dog_overlap",
            "(c) dogs with a twin within 2",
            "share of dogs with a twin\n(median over trials)",
        ),
    )
    for ax, col, title, ylabel in panels:
        for layout in ("wide", "split", "outlier_rich"):
            g = t[t["initial_layout"] == layout].groupby("n_shepherds")
            med = g[col].median()[g.size() >= min_seeds]
            ax.plot(
                med.index,
                med.values,
                marker="o",
                ms=4,
                lw=1.4,
                color=LAYOUT_COLOR[layout],
                label=layout,
            )
        d_axis(ax)
        ax.set_ylabel(ylabel)
        ax.set_title(f"{title}, N = {n_panels}, 99 percent", fontsize=9.5)
        grid(ax)
    axes[1].legend(frameon=False, fontsize=8, loc="upper left")
    save(fig, "fig27_metrics.png", rect=(0, 0, 1, 0.98))


def fig_spacing() -> None:
    """Holding task: success against D with point dogs and with dogs that take up room."""
    runs = (
        ("dmin_f99_hold", ":", "point dogs", MUTED),
        ("dmin_f99_hold_spacing", "-", "dogs 2 apart", BLUE),
    )
    n = 400
    arc_capacity = (10, 12)  # dogs the drive arc holds at 2 apart
    if not have(*[r[0] for r in runs]):
        return
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
    for ax, layout in zip(axes, ("wide", "outlier_rich")):
        for name, ls, label, color in runs:
            rate_line(ax, curve(cells(name), layout, n), color, "o", ls=ls, label=label)
        theta_line(ax, color=INK, ls="--")
        ax.axvspan(*arc_capacity, color=ORANGE, alpha=0.12)
        ax.text(arc_capacity[0] + 0.2, 0.05, "drive-arc\ncapacity", fontsize=8, color=ORANGE)
        d_axis(ax)
        ax.set_ylim(0, 1.02)
        ax.set_title(f"{layout}, N = {n}, holding task", fontsize=10)
        grid(ax)
    axes[0].set_ylabel("success rate (99 percent held for one drive time)")
    axes[0].legend(frameon=False, fontsize=8, loc="center right")
    save(
        fig,
        "fig36_spacing.png",
        rect=(0, 0.07, 1, 1),
        note=(
            "dmin_f99_hold and dmin_f99_hold_spacing, 6 drive times. "
            "Dashed: theta = 0.90. Shaded: dogs the "
            "drive arc holds at 2 apart (N = 200 to 400).\nHollow: fewer than 30 trials."
        ),
    )


def fig_hold_goal() -> None:
    """Holding task: success against the goal radius in metres, for each share that must stay
    in. If the flock's walk past the goal while the dogs withdraw sets the limit, the curves
    of the three flock sizes cross theta at about the same radius in metres."""
    if not have("dmin_f99_hold_share", "dmin_f99_hold_goal"):
        return
    from analysis.results import flock_radii

    shares = {
        0.90: "two of 25, five of 50",
        0.95: "one of 25, two of 50",
        0.99: "none below N = 100",
    }
    colors = {25: BLUE, 50: ORANGE, 100: AQUA}
    default_goal = 1.9  # flock radii
    # the D of the share protocol's grid only, leaving out the midpoints the adaptive run added,
    # so every point averages the same 20 cells; the 3.0 level exists only in dmin_f99_hold_goal
    grid_d = [1, 2, 4, 8, 24]

    def level(t: pd.DataFrame, key: str) -> pd.Series:
        return t["factors"].str.extract(rf"{key}=([\d.]+)")[0].astype(float)

    radius = {
        int(n): r
        for n, r in flock_radii(RESULTS_ROOT / "dmin_f99_hold_share")["strombom_multi"].items()
    }
    share = cells("dmin_f99_hold_share")
    share["g"] = level(share, "goal_radius_multiple")
    share["f"] = level(share, "success_fraction")
    goal = cells("dmin_f99_hold_goal")
    goal["g"] = level(goal, "goal_radius_multiple")
    goal["f"] = 0.99
    t = pd.concat([share, goal[goal["g"] == 3.0]], ignore_index=True)
    t = t[t["d"].isin(grid_d)]
    t["goal_m"] = t["g"] * t["n"].map(radius)

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), sharey=True)
    for ax, (f, out) in zip(axes, shares.items()):
        for n, color in colors.items():
            part = t[(t["f"] == f) & (t["n"] == n)]
            # equal weight per cell (layout x D), so cells that drew more seeds count once
            per = part.groupby("goal_m")["success_rate"].agg(["mean", "min", "max"]).reset_index()
            ax.vlines(per["goal_m"], per["min"], per["max"], color=color, lw=4, alpha=0.18)
            ax.plot(
                per["goal_m"], per["mean"], color=color, marker="o", ms=5, lw=1.2, label=f"N = {n}"
            )
            default = per[np.isclose(per["goal_m"], default_goal * radius[n])]
            ax.plot(
                default["goal_m"],
                default["mean"],
                ls="",
                marker="o",
                ms=9,
                mfc="none",
                mec=INK,
                mew=1.0,
            )
        theta_line(ax, color=INK, ls="--")
        ax.set_ylim(0, 1.02)
        ax.set_xlabel("goal radius (m)")
        ax.set_title(f"{int(round(f * 100))} percent must stay in (out: {out})", fontsize=10)
        grid(ax)
    axes[0].set_ylabel("success rate, mean over layouts and D")
    axes[0].legend(frameon=False, fontsize=8, loc="lower right")
    save(
        fig,
        "fig40_hold_goal.png",
        rect=(0, 0.08, 1, 1),
        note=(
            "dmin_f99_hold_share (goal 1.9 to 2.5 R_f) "
            "and dmin_f99_hold_goal (3.0 R_f, 99 percent), "
            "holding for one drive time at 6 drive times. "
            "Bars: range over the cells (4 layouts x D = 1, 2, 4, 8, 24).\n"
            "Ringed: the default goal of 1.9 R_f. Dashed: theta = 0.90."
        ),
    )


def fig_view() -> None:
    """D_min against what a dog sees: sensing range, and sharing at range 65."""
    if not have("dmin_f99_view_range", "dmin_f99_view_comm"):
        return

    ranges = [15.0, 30.0, 45.0, 65.0, 100.0]
    reaction = 65  # r_s, the distance at which a sheep reacts to a dog
    # x offset of each (layout, N) so the bars at one range do not overprint
    offset = {("wide", 100): -1.5, ("wide", 200): -0.5, ("split", 100): 0.5, ("split", 200): 1.5}
    sharing = (
        ("no sharing", "range", "sensing_range=65.0", ":"),
        ("with dogs in range", "comm", "communication=neighbour", "--"),
        ("whole team", "comm", "communication=shared", "-"),
        ("global view", "range", "sensing_range=0.0", "-"),
    )

    g = groups("dmin_f99_view_range")
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    ax = axes[0]
    for layout, marker in (("wide", "o"), ("split", "s")):
        for n, alpha in ((100, 0.5), (200, 1.0)):
            color = LAYOUT_COLOR[layout]
            dx = offset[(layout, n)]
            for r_ in ranges:
                row = g[
                    (g["layout"] == layout)
                    & (g["n"] == n)
                    & (g["factors"] == f"sensing_range={r_}")
                ]
                if row.empty:
                    continue
                b = bracket(row.iloc[0])
                if b:
                    ax.plot([r_ + dx] * 2, b, color=color, alpha=alpha, lw=3)
                    ax.plot(r_ + dx, b[1], marker=marker, color=color, alpha=alpha, ls="")
                elif pd.notna(row.iloc[0]["d_min_low"]):
                    ax.plot(
                        r_ + dx,
                        float(row.iloc[0]["d_min_low"]),
                        marker="^",
                        ls="",
                        mfc=SURFACE,
                        mec=color,
                        alpha=alpha,
                    )
            ax.plot(
                [], [], marker=marker, color=color, alpha=alpha, ls="", label=f"{layout}, N = {n}"
            )
    ax.set_xlabel("sensing range of each dog (no sharing)")
    ax.set_ylabel("D_min (bar: bracket; hollow: lower bound)")
    ax.set_title("a narrower view needs more dogs", fontsize=10)
    ax.axvline(reaction, color=MUTED, lw=0.8, ls="--")
    ax.text(reaction + 1, 0.6, "r_s", fontsize=8, color=MUTED)
    ax.set_ylim(0, 8)
    grid(ax)
    ax.legend(frameon=False, fontsize=8)

    data = {"comm": cells("dmin_f99_view_comm"), "range": cells("dmin_f99_view_range")}
    ax = axes[1]
    for label, run, factor, ls in sharing:
        t = data[run]
        part = curve(t[t["factors"] == factor], "wide", 200)
        rate_line(ax, part, INK if label == "global view" else BLUE, "o", ls=ls, label=label)
    theta_line(ax, color=INK, ls="--")
    d_axis(ax, ticks=(1, 2, 3, 4, 6, 8, 12, 16))
    ax.set_ylim(0, 1.02)
    ax.set_ylabel("success rate")
    ax.set_title("wide, N = 200, range 65: sharing", fontsize=10)
    grid(ax)
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    save(
        fig,
        "fig37_view.png",
        rect=(0, 0.05, 1, 1),
        note=(
            "dmin_f99_view_range and dmin_f99_view_comm (99 percent rule, 6 drive times). "
            "A dog that sees no "
            "sheep walks to the flock centre it last knew."
        ),
    )
