"""Result figures for make_result_figures.py.

Data and axis helpers first, then the three figures of D_min against N and the deadline.
Style in figstyle.py; a figure is skipped when its run folder is missing.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from functools import cache, wraps

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.lines import Line2D

from analysis.curves import groups_table, split_group_key
from analysis.results import read_cells
from docs.generate_docs.figstyle import (
    AQUA,
    BLUE,
    INK,
    MUTED,
    NS,
    ORANGE,
    SURFACE,
    grid,
    log_ticks,
    save,
)
from docs.generate_docs.tables import F99_MAIN, STRICT_MAIN
from services.protocol import RESULTS_ROOT

# ----- settings -----
MAIN_RUNS = dict(zip((12, 6, 3), zip(STRICT_MAIN, F99_MAIN, strict=True), strict=True))

LAYOUT_COLOR = {"compact": MUTED, "wide": BLUE, "split": ORANGE, "outlier_rich": AQUA}
# Light to dark blues for an ordered series (deadlines, flock sizes).
BLUES = ("#bcd3f0", "#8fb9ec", "#5b95de", "#2a78d6", "#0b2f66")

D_TICKS = (1, 2, 4, 8, 16, 24)
THETA = 0.9


# ----- data access -----
def have(*names: str) -> bool:
    missing = [n for n in names if not (RESULTS_ROOT / n / "frontier_cells.csv").exists()]
    if missing:
        print("missing", missing, ": figure skipped")
    return not missing


def read_once(load: Callable[[str], pd.DataFrame]) -> Callable[[str], pd.DataFrame]:
    """Cache a run file once; each call returns a copy."""
    cached = cache(load)

    @wraps(load)
    def frame(name: str) -> pd.DataFrame:
        return cached(name).copy()

    return frame


@read_once
def cells(name: str) -> pd.DataFrame:
    t = split_group_key(read_cells(RESULTS_ROOT / name))
    t["d"] = t["n_shepherds"].astype(int)
    return t


@read_once
def groups(name: str) -> pd.DataFrame:
    return groups_table(RESULTS_ROOT / name)


def curve(t: pd.DataFrame, layout: str, n: int) -> pd.DataFrame:
    """The cells of one D curve, in order of D."""
    return t[(t["layout"] == layout) & (t["n"] == n)].sort_values("d")


def group_row(g: pd.DataFrame, layout: str, n: int) -> pd.Series:
    return g[(g["layout"] == layout) & (g["n"] == n)].iloc[0]


# ----- axes helpers -----
def d_axis(ax: Axes, ticks: Sequence[float] = D_TICKS, label: str = "dogs D") -> None:
    """The team-size axis most figures share."""
    log_ticks(ax, ticks)
    ax.set_xlabel(label)


def theta_line(ax: Axes, color: str = MUTED, ls: str = ":") -> None:
    ax.axhline(THETA, color=color, lw=0.8, ls=ls)


def rate_errorbars(
    ax: Axes,
    t: pd.DataFrame,
    x: pd.Series | np.ndarray,
    color: str,
    fmt: str,
    label: str,
    ms: float,
    lw: float,
    elinewidth: float,
    capsize: float,
) -> None:
    """Success rate against D with its 99 percent interval as error bars."""
    yerr = [t["success_rate"] - t["rate_low"], t["rate_high"] - t["success_rate"]]
    ax.errorbar(
        x,
        t["success_rate"],
        yerr=yerr,
        fmt=fmt,
        color=color,
        ms=ms,
        lw=lw,
        elinewidth=elinewidth,
        capsize=capsize,
        label=label,
    )


# ----- dmin -----
def fig_dmin_vs_n() -> None:
    """D_min vs N for the three main runs (strict and 99 percent), with open brackets."""
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


def fig_growth_fits() -> None:
    """D_min against N on the nine sizes (99 percent), with the range each fitted shape allows."""
    from analysis.growth_fits import consistent_range, interval_of

    runs = ((MAIN_RUNS[12][1], "12 drive times"), (MAIN_RUNS[6][1], "6 drive times"))
    if not have(*[r for r, _ in runs]):
        return
    ahead = np.array([566, 800, 1131, 1600, 2263, 3200])  # sizes the fits are extended to
    edge = 600  # largest N with a calibrated flock radius
    shapes = (("power law", "--"), ("saturating", ":"))
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4), sharey=True)
    for ax, (name, title) in zip(axes, runs):
        g = groups(name)
        for layout, marker in (("wide", "o"), ("outlier_rich", "s")):
            color = LAYOUT_COLOR[layout]
            points = []
            for _, r in g[g["layout"] == layout].sort_values("n").iterrows():
                found = interval_of(float(r["d_min"]), float(r["d_min_low"]))
                if found is None:
                    continue
                points.append((int(r["n"]), found))
                ax.plot(
                    [r["n"], r["n"]], [found[0] + 0.5, found[1] - 0.5], color=color, lw=3, alpha=0.5
                )
                ax.plot(r["n"], found[1] - 0.5, marker=marker, color=color, ms=5, ls="")
            for shape, ls in shapes:
                lo, hi = zip(*[consistent_range(points, shape, int(n)) for n in ahead])
                ax.fill_between(ahead, lo, hi, color=color, alpha=0.08 if ls == ":" else 0.15)
                ax.plot(ahead, hi, color=color, lw=0.9, ls=ls)
            ax.plot([], [], color=color, marker=marker, ls="", label=layout)
        ax.axvline(edge, color=MUTED, lw=0.8)
        ax.text(edge + 10, 0.85, "calibration edge", fontsize=8, color=MUTED)
        log_ticks(ax, [25, 50, 100, 200, 400, 800, 1600, 3200])
        log_ticks(ax, [1, 2, 3, 5, 10, 20], axis="y")
        ax.set_xlabel("flock size N")
        ax.set_title(f"D_min, 99 percent rule, {title}", fontsize=10)
        grid(ax)
    axes[0].set_ylabel("dogs")
    axes[0].plot([], [], color=INK, ls="--", lw=0.9, label="power law: largest allowed")
    axes[0].plot([], [], color=INK, ls=":", lw=0.9, label="saturating: largest allowed")
    axes[0].legend(frameon=False, fontsize=8, loc="upper left")
    save(
        fig,
        "fig35_growth_fits.png",
        rect=(0, 0.05, 1, 1),
        note=(
            "Bars: the D_min bracket at each N (marker at the reliable D). "
            "Shaded beyond N = 566: the "
            "range of D allowed by every curve of each shape that passes through all the brackets."
        ),
    )
