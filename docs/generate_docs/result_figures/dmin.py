"""D_min against N and its comparisons across rules, deadlines and layouts."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from docs.generate_docs.figstyle import (
    BLUE,
    MUTED,
    ORANGE,
    SURFACE,
    grid,
    save,
)
from docs.generate_docs.result_figures.common import (
    BLUES,
    LAYOUT_COLOR,
    MAIN_RUNS,
    NS,
    THETA,
    cells,
    curve,
    d_axis,
    group_row,
    groups,
    have,
    log_ticks,
    rate_errorbars,
    short,
    theta_line,
    trials,
)
from services.protocol import RESULTS_ROOT


def fig_dmin_vs_n() -> None:
    """D_min against N from the three main runs, strict (solid, circles) and 99 percent of the
    flock (dashed, squares), with the two rules and the four layouts offset a little in N. A
    shaded bar runs from D_min_low to D_min where a smaller D stayed undecided at 200 seeds; a
    hollow triangle is a curve with no reliable D yet; a cross a curve with no reliable D on the
    grid."""
    if not have(*[n for pair in MAIN_RUNS.values() for n in pair]):
        return
    none_y = 40  # where "no reliable D" is drawn
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.4), sharey=True)
    for ax, (m, (strict, f99)) in zip(axes, MAIN_RUNS.items()):
        largest = 0
        for k, (name, marker) in enumerate(((strict, "o"), (f99, "s"))):
            g = groups(name)
            largest = max(largest, int(g["n"].max()))
            for li, (layout, color) in enumerate(LAYOUT_COLOR.items()):
                part = g[g["layout"] == layout].sort_values("n")
                xs, ys = [], []
                for _, r in part.iterrows():
                    # each rule and each layout has its own x offset, so markers do not overprint
                    x = r["n"] * (1.0 + 0.07 * (k - 0.5) + 0.022 * (li - 1.5))
                    if not np.isnan(r["d_min"]):
                        xs.append(x)
                        ys.append(r["d_min"])
                        if r["d_min_low"] < r["d_min"]:  # a smaller D is still open: a bracket
                            ax.plot(
                                [x, x],
                                [r["d_min_low"], r["d_min"]],
                                color=color,
                                lw=2.2,
                                alpha=0.45,
                            )
                            ax.plot(
                                x, r["d_min_low"], marker="_", color=color, ms=9, mew=1.6, ls=""
                            )
                    elif not np.isnan(r["d_min_low"]):
                        ax.plot(x, r["d_min_low"], marker="^", mfc="none", mec=color, ms=8, ls="")
                        ax.plot([x, x], [r["d_min_low"], 24], color=color, lw=0.8, alpha=0.5)
                    else:
                        ax.plot(x, none_y, marker="x", color=color, ms=7, ls="")
                if xs:
                    ax.plot(xs, ys, color=color, lw=1.2, alpha=0.85, ls="-" if k == 0 else "--")
                    ax.plot(xs, ys, marker=marker, color=color, ms=6, ls="", mec=SURFACE, mew=0.8)
        ax.set_xscale("log")
        ticks = [n for n in (*NS, 566) if n <= largest]
        ax.set_xticks(ticks)
        ax.set_xticklabels(ticks)
        log_ticks(
            ax,
            [1, 2, 3, 4, 6, 8, 12, 24, none_y],
            axis="y",
            labels=["1", "2", "3", "4", "6", "8", "12", "24", "none"],
        )
        ax.set_title(f"deadline {m} drive times")
        ax.set_xlabel("flock size N")
        grid(ax)
    axes[0].set_ylabel("D_min (dogs)")
    handles = [Line2D([], [], color=c, lw=2, label=name) for name, c in LAYOUT_COLOR.items()]
    handles += [
        Line2D([], [], color=MUTED, marker="o", ls="-", label="strict (every sheep)"),
        Line2D([], [], color=MUTED, marker="s", ls="--", label="99 percent of the sheep"),
        Line2D([], [], color=MUTED, lw=2.2, alpha=0.45, label="bracket: a smaller D still open"),
        Line2D(
            [],
            [],
            color=MUTED,
            marker="^",
            mfc="none",
            ls="",
            label="not decided: D_min_low (line up to 24)",
        ),
        Line2D([], [], color=MUTED, marker="x", ls="", label="none: no D up to 24 reliable"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False, fontsize=8.5)
    save(fig, "fig20_dmin_vs_n.png", rect=(0, 0.14, 1, 0.98))


def fig_straggler() -> None:
    """Left: with 6 or more dogs the faster dog brings 99 percent of the flock into the goal in
    nearly every trial, yet strict success is lower; the slower dog loses no trial. Right: one
    start flock; the faster dog's flock arrives with all but a sheep or two and is driven out
    and back, the slower dog's ends inside once. From dmin_s_base and dmin_s_dogspeed."""
    if not have("dmin_s_base", "dmin_s_dogspeed"):
        return
    panels = [(lay, n) for lay in ("wide", "outlier_rich") for n in (100, 200, 400)]
    many_dogs = 6
    trace = "strombom_multi__wide__N-400__D-16__seed-2.parquet"  # wide N = 400, 16 dogs, seed 2
    runs = (("dmin_s_base", "dog 1.5", BLUE), ("dmin_s_dogspeed", "dog 1.15", ORANGE))

    fig = plt.figure(figsize=(13, 5))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.15, 1])
    ax = fig.add_subplot(gs[:, 0])
    base, slow = trials("dmin_s_base"), trials("dmin_s_dogspeed")
    stats = []
    for lay, n in panels:
        b = base[
            (base.initial_layout == lay) & (base.n_sheep == n) & (base.n_shepherds >= many_dogs)
        ]
        s = slow[
            (slow.initial_layout == lay) & (slow.n_sheep == n) & (slow.n_shepherds >= many_dogs)
        ]
        stats.append(
            (b["success"].mean(), b["seconds_to_99pct_in_goal"].notna().mean(), s["success"].mean())
        )
    x = np.arange(len(panels))
    w = 0.26
    bars = (
        ("dog 1.5, every sheep in", BLUE, None),
        ("dog 1.5, 99 percent in at some tick", BLUE, "///"),
        ("dog 1.15, every sheep in", ORANGE, None),
    )
    for k, (label, color, hatch) in enumerate(bars):
        vals = [st[k] for st in stats]
        ax.bar(
            x + (k - 1) * w,
            vals,
            w * 0.92,
            color=color,
            hatch=hatch,
            ec=SURFACE if hatch is None else "white",
            alpha=0.55 if hatch else 1.0,
            label=label,
        )
    ax.set_xticks(x)
    ax.set_xticklabels([f"{short(lay)}\nN={n}" for lay, n in panels], fontsize=8)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("share of trials with 6 or more dogs (trials pooled)")
    ax.set_title("the flock arrives; the last sheep decides")
    grid(ax, axis="y")
    ax.legend(frameon=False, fontsize=8, loc="lower center", bbox_to_anchor=(0.5, -0.28), ncol=3)

    series = {}
    for name, label, color in runs:
        path = RESULTS_ROOT / name / "timeseries" / trace
        if path.exists():
            series[name] = (pd.read_parquet(path), label, color)
    ax1 = fig.add_subplot(gs[0, 1])
    ax2 = fig.add_subplot(gs[1, 1], sharex=ax1)
    for t, label, color in series.values():
        ax1.plot(t["tick"], t["gcm_goal"], color=color, lw=1.4, label=label)
        ax2.plot(t["tick"], 400 - t["sheep_in_goal"], color=color, lw=1.4)
    ax1.set_ylabel("flock centre to goal")
    # the count of sheep still outside, on a scale that is linear up to 1 and logarithmic above,
    # so that "all but a sheep or two" is visible and a full flock outside is too
    ax2.set_yscale("symlog", linthresh=1)
    ax2.set_ylim(0, 500)
    ax2.set_yticks([0, 1, 2, 5, 10, 100, 400])
    ax2.set_yticklabels(["0", "1", "2", "5", "10", "100", "400"])
    ax2.set_ylabel("sheep outside the goal")
    ax2.set_xlabel("time (ticks, 1 tick = 1 s)")
    ax1.set_title("one flock, wide N = 400, 16 dogs, seed 2")
    ax1.legend(frameon=False, fontsize=8)
    for a in (ax1, ax2):
        grid(a)
    plt.setp(ax1.get_xticklabels(), visible=False)
    save(fig, "fig22_straggler.png", rect=(0, 0, 1, 0.98))


def fig_split_curves() -> None:
    """Success against D at 6 drive times. On split the rate does not rise with D at N = 200 and
    400 and the intervals are wide where cells have 10 to 70 seeds; wide at N = 400 is the
    contrast. Dotted line: theta = 0.90."""
    strict, f99 = MAIN_RUNS[6]
    if not have(strict, f99):
        return
    panels = (("split", 100), ("split", 200), ("split", 400), ("wide", 400))
    rules = ((strict, "strict", BLUE, "o", 0.97), (f99, "99 percent", ORANGE, "s", 1.03))
    data = {name: cells(name) for name, *_ in rules}
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.8), sharey=True)
    for ax, (lay, n) in zip(axes, panels):
        for name, label, color, marker, dx in rules:
            t = curve(data[name], lay, n)
            rate_errorbars(
                ax,
                t,
                t["d"] * dx,
                color,
                marker + "-",
                label,
                ms=5,
                lw=1,
                elinewidth=0.8,
                capsize=2,
            )
        theta_line(ax)
        d_axis(ax)
        ax.set_title(f"{lay}, N = {n}")
        grid(ax)
    axes[0].set_ylabel("success rate, 99% interval")
    axes[0].legend(frameon=False, fontsize=8, loc="lower left")
    save(fig, "fig23_split_curves.png", rect=(0, 0, 1, 0.98))


def fig_deadline() -> None:
    """How the deadline moves the success curve and D_min (99 percent rule, main runs)."""
    runs = {m: pair[1] for m, pair in MAIN_RUNS.items()}
    if not have(*runs.values()):
        return
    shade = {12: BLUES[1], 6: BLUES[3], 3: BLUES[4]}
    curves = (("wide", 400), ("outlier_rich", 200))
    combos = [
        ("wide", 200, "-", "o"),
        ("wide", 400, "--", "s"),
        ("outlier_rich", 200, "-", "o"),
        ("outlier_rich", 400, "--", "s"),
    ]
    data = {m: cells(name) for m, name in runs.items()}
    tables = {m: groups(name) for m, name in runs.items()}

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.4))
    for ax, (layout, n) in zip(axes[:2], curves):
        for k, m in enumerate(runs):
            part = curve(data[m], layout, n)
            rate_errorbars(
                ax,
                part,
                part["d"] * (1 + 0.03 * (k - 1)),
                shade[m],
                "o-",
                f"{m} drive times",
                ms=3.5,
                lw=1.2,
                elinewidth=0.7,
                capsize=1.5,
            )
        theta_line(ax)
        d_axis(ax)
        ax.set_ylim(-0.03, 1.04)
        ax.set_ylabel("success rate, 99 percent rule")
        ax.set_title(f"{layout}, N = {n}", fontsize=10)
        grid(ax)
    axes[0].legend(frameon=False, fontsize=8, loc="lower right", title="deadline", title_fontsize=8)

    ax = axes[2]
    xs = {12: 0, 6: 1, 3: 2}
    for layout, n, ls, marker in combos:
        color = LAYOUT_COLOR[layout]
        pts = []
        for m, x in xs.items():
            row = group_row(tables[m], layout, n)
            off = 0.05 * (1 if ls == "--" else -1) + (0.0 if layout == "wide" else 0.1)
            if not np.isnan(row["d_min"]):
                ax.plot(
                    [x + off, x + off],
                    [row["d_min_low"], row["d_min"]],
                    color=color,
                    lw=3,
                    alpha=0.35,
                    solid_capstyle="butt",
                )
                ax.plot(x + off, row["d_min"], marker=marker, ms=6, color=color)
                pts.append((x + off, row["d_min"]))
            elif not np.isnan(row["d_min_low"]):
                ax.plot(x + off, row["d_min_low"], marker=">", ms=7, mfc=SURFACE, mec=color)
        if len(pts) > 1:
            ax.plot(*zip(*pts), color=color, lw=1.0, ls=ls, label=f"{layout}, N = {n}")
    log_ticks(ax, [1, 2, 3, 4, 6, 8, 12], axis="y")
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(["12", "6", "3"])
    ax.set_xlabel("deadline (drive times, tighter to the right)")
    ax.set_ylabel("D_min (99 percent rule)")
    ax.set_title("D_min against the deadline", fontsize=10)
    grid(ax)
    ax.legend(frameon=False, fontsize=7.5, loc="upper left")
    save(
        fig,
        "fig29_deadline.png",
        rect=(0, 0.04, 1, 1),
        note_y=0.005,
        note=(
            "right: filled marker D_min, shaded bar the bracket down to D_min_low, "
            "hollow '>' a lower bound with no reliable D yet (outlier_rich N = 400 at 3 drive "
            "times)"
        ),
    )


def fig_strict_vs_99() -> None:
    """Strict against 99 percent success of the same cells, on the same seeds."""
    if not have(*[n for p in MAIN_RUNS.values() for n in p]):
        return
    min_seeds = 20
    min_n = 100
    keys = ["initial_layout", "n_sheep", "n_shepherds", "seed_index"]
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.7), sharex=True, sharey=True)
    for ax, (m, (strict_name, f99_name)) in zip(axes, MAIN_RUNS.items()):
        a = trials(strict_name)[keys + ["success"]].rename(columns={"success": "strict"})
        b = trials(f99_name)[keys + ["success"]].rename(columns={"success": "f99"})
        both = a.merge(b, on=keys)
        both = both[(both["initial_layout"] != "compact") & (both["n_sheep"] >= min_n)]
        cell = (
            both.groupby(["initial_layout", "n_sheep", "n_shepherds"])
            .agg(strict=("strict", "mean"), f99=("f99", "mean"), n=("strict", "size"))
            .reset_index()
        )
        cell = cell[cell["n"] >= min_seeds]
        ax.add_patch(Rectangle((0, THETA), THETA, 0.1, fc="#f3dccf", ec="none", alpha=0.7))
        for layout in ("wide", "split", "outlier_rich"):
            part = cell[cell["initial_layout"] == layout]
            ax.scatter(
                part["strict"],
                part["f99"],
                s=26,
                color=LAYOUT_COLOR[layout],
                alpha=0.75,
                lw=0,
                label=layout,
            )
        ax.plot([0, 1], [0, 1], color=MUTED, lw=0.8)
        ax.axvline(THETA, color=MUTED, lw=0.8, ls=":")
        theta_line(ax)
        only = int(((cell["strict"] < THETA) & (cell["f99"] >= THETA)).sum())
        ax.set_title(
            f"{m} drive times: {only} of {len(cell)} cells above 0.90 only under 99%", fontsize=9.5
        )
        ax.set_xlabel("success rate, every sheep in")
        ax.set_xlim(-0.02, 1.03)
        ax.set_ylim(-0.02, 1.03)
        ax.set_aspect("equal")
        grid(ax)
    axes[0].set_ylabel("success rate, 99 percent in")
    axes[0].legend(frameon=False, fontsize=8, loc="lower right")
    save(
        fig,
        "fig30_strict_vs_99.png",
        rect=(0, 0.04, 1, 0.97),
        note_y=0.005,
        note=(
            "one point per cell with at least 20 shared seeds, scattered layouts, N >= 100; "
            "both rates use the same seeds, so no point lies below the diagonal; shaded: reliable "
            "level reached only under the 99 percent rule"
        ),
    )


def fig_compact() -> None:
    """Compact flocks: finish time against D for the Strombom sheep and the Kubo model."""
    if not have("dmin_m6", "dmin_kubo"):
        return
    kubo_ns = (25, 50, 100)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))

    ax = axes[0]
    t = trials("dmin_m6")
    t = t[(t["initial_layout"] == "compact") & t["success"]]
    for n, color in zip(NS, BLUES):
        part = t[t["n_sheep"] == n]
        med = (
            (part["finish_seconds"] / part["drive_distance"]).groupby(part["n_shepherds"]).median()
        )
        ax.plot(med.index, med.values, marker="o", ms=3.5, lw=1.3, color=color, label=f"N = {n}")
    d_axis(ax)
    ax.set_ylim(0, 2.0)
    ax.set_ylabel("median finish time / drive time")
    ax.set_title("Strombom sheep, compact start: no effect of D", fontsize=10)
    grid(ax)
    ax.legend(frameon=False, fontsize=8, loc="lower right", ncol=2)

    ax = axes[1]
    k = trials("dmin_kubo")
    for n, color in zip(kubo_ns, (BLUES[1], BLUES[3], BLUES[4])):
        part = k[(k["n_sheep"] == n) & k["success"]]
        med = part["finish_seconds"].groupby(part["n_shepherds"]).median()
        ax.plot(med.index, med.values, marker="o", ms=3.5, lw=1.3, color=color, label=f"N = {n}")
    d_axis(ax, ticks=(1, 2, 4, 6, 10))
    ax.set_ylim(0, 130)
    ax.set_ylabel("median finish time (s)")
    ax.set_title("Kubo model, compact start: finish time falls with D", fontsize=10)
    grid(ax)
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    save(
        fig,
        "fig31_compact.png",
        rect=(0, 0.05, 1, 1),
        note=(
            "left: dmin_m6, successful trials, 6 drive times; right: dmin_kubo, 500 s "
            "deadline. Success is 1.00 in every cell of both "
            "(at least 60 trials per cell on the right)."
        ),
    )
