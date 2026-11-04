"""Result figures for make_result_figures.py.

Data and axis helpers first, then the three figures of D_min against N and the deadline.
Style in figstyle.py; a figure is skipped when its run folder is missing.
"""

from __future__ import annotations

from collections.abc import Callable, Hashable, Sequence
from functools import cache, wraps
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.lines import Line2D

from analysis.curves import groups_table, split_group_key
from analysis.frontier import confirming_team
from analysis.growth_fits import consistent_range, interval_of
from analysis.results import read_cells, read_trials
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
from services.protocol import RESULTS_ROOT, load_protocol

Row = dict[Hashable, Any]  # one row of a groups table, from DataFrame.to_dict("records")

# ----- settings -----
MAIN_RUNS = dict(zip((12, 6, 3), zip(STRICT_MAIN, F99_MAIN, strict=True), strict=True))

LAYOUT_COLOR = {"compact": MUTED, "wide": BLUE, "split": ORANGE, "outlier_rich": AQUA}
# Light to dark blues for an ordered series (deadlines, flock sizes).
BLUES = ("#bcd3f0", "#8fb9ec", "#5b95de", "#2a78d6", "#0b2f66")

D_TICKS = (1, 2, 4, 8, 16, 24)
D_MAX = 24  # largest team size the runs try
THETA = 0.9

# D_min against N: marker and line style of the strict rule, then of the 99 percent rule.
RULE_STYLES = (("o", "-"), ("s", "--"))
NONE_Y = 40  # where "no reliable D" is drawn
DMIN_YTICKS = (1, 2, 3, 4, 6, 8, 12, D_MAX)

# Deadline figure: the success curves, and the (layout, N, line, marker) of the D_min panel.
SUCCESS_CURVES = (("wide", 400), ("outlier_rich", 200))
DEADLINE_SHADE = {12: BLUES[1], 6: BLUES[3], 3: BLUES[4]}
DEADLINE_COMBOS = (
    ("wide", 200, "-", "o"),
    ("wide", 400, "--", "s"),
    ("outlier_rich", 200, "-", "o"),
    ("outlier_rich", 400, "--", "s"),
)

# Growth-fit figure: sizes the fits are extended to, and the shapes with their line style.
FIT_AHEAD = np.array([566, 800, 1131, 1600, 2263, 3200])
FIT_SHAPES = (("power law", "--"), ("saturating", ":"))
CALIBRATION_EDGE = 600  # largest N with a calibrated flock radius


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
def trials(name: str) -> pd.DataFrame:
    t = split_group_key(read_trials(RESULTS_ROOT / name))
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


def layout_rows(g: pd.DataFrame, layout: str) -> list[Row]:
    """The groups of one layout, in order of N."""
    return g[g["layout"] == layout].sort_values("n").to_dict("records")


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
def _dmin_cell(ax: Axes, r: Row, x: float, color: str) -> float | None:
    """Draw one (layout, N) cell; return its D_min when decided, else None."""
    d_min, low = r["d_min"], r["d_min_low"]
    if not np.isnan(d_min):
        if low < d_min:  # a smaller D is still open: a bracket
            ax.plot([x, x], [low, d_min], color=color, lw=2.2, alpha=0.45)
            ax.plot(x, low, marker="_", color=color, ms=9, mew=1.6, ls="")
        return d_min
    if not np.isnan(low):
        ax.plot(x, low, marker="^", mfc="none", mec=color, ms=8, ls="")
        ax.plot([x, x], [low, D_MAX], color=color, lw=0.8, alpha=0.5)
    else:
        ax.plot(x, NONE_Y, marker="x", color=color, ms=7, ls="")
    return None


def _dmin_layout(ax: Axes, rows: list[Row], color: str, shift: float, marker: str, ls: str) -> None:
    """One layout's D_min against N under one rule; ``shift`` offsets x against overprinting."""
    points = []
    for r in rows:
        x = r["n"] * shift
        d_min = _dmin_cell(ax, r, x, color)
        if d_min is not None:
            points.append((x, d_min))
    if points:
        xs, ys = zip(*points)
        ax.plot(xs, ys, color=color, lw=1.2, alpha=0.85, ls=ls)
        ax.plot(xs, ys, marker=marker, color=color, ms=6, ls="", mec=SURFACE, mew=0.8)


def _dmin_panel(ax: Axes, m: int, runs: Sequence[str]) -> None:
    """One deadline: both rules, every layout."""
    largest = 0
    for k, (name, (marker, ls)) in enumerate(zip(runs, RULE_STYLES, strict=True)):
        g = groups(name)
        largest = max(largest, int(g["n"].max()))
        for li, (layout, color) in enumerate(LAYOUT_COLOR.items()):
            shift = 1.0 + 0.07 * (k - 0.5) + 0.022 * (li - 1.5)
            _dmin_layout(ax, layout_rows(g, layout), color, shift, marker, ls)
    ax.set_xscale("log")
    ticks = [n for n in (*NS, 566) if n <= largest]
    ax.set_xticks(ticks)
    ax.set_xticklabels([str(n) for n in ticks])
    log_ticks(
        ax,
        [*DMIN_YTICKS, NONE_Y],
        axis="y",
        labels=[*map(str, DMIN_YTICKS), "none"],
    )
    ax.set_title(f"deadline {m} drive times")
    ax.set_xlabel("flock size N")
    grid(ax)


def _dmin_legend_handles() -> list[Line2D]:
    handles = [Line2D([], [], color=c, lw=2, label=name) for name, c in LAYOUT_COLOR.items()]
    return handles + [
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
            label=f"not decided: D_min_low (line up to {D_MAX})",
        ),
        Line2D([], [], color=MUTED, marker="x", ls="", label=f"none: no D up to {D_MAX} reliable"),
    ]


def fig_dmin_vs_n() -> None:
    """D_min vs N for the three main runs (strict and 99 percent), with open brackets."""
    if not have(*[n for pair in MAIN_RUNS.values() for n in pair]):
        return
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.4), sharey=True)
    for ax, (m, runs) in zip(axes, MAIN_RUNS.items()):
        _dmin_panel(ax, m, runs)
    axes[0].set_ylabel("D_min (dogs)")
    fig.legend(
        handles=_dmin_legend_handles(), loc="lower center", ncol=4, frameon=False, fontsize=8.5
    )
    save(fig, "fig20_dmin_vs_n.png", rect=(0, 0.14, 1, 0.98))


# ----- deadline -----
def _success_panel(ax: Axes, data: dict[int, pd.DataFrame], layout: str, n: int) -> None:
    """Success rate against D for one (layout, N), one curve per deadline."""
    for k, m in enumerate(data):
        part = curve(data[m], layout, n)
        rate_errorbars(
            ax,
            part,
            part["d"] * (1 + 0.03 * (k - 1)),
            DEADLINE_SHADE[m],
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


def _deadline_cell(ax: Axes, row: pd.Series, x: float, color: str, marker: str) -> float | None:
    """Draw D_min and its bracket at deadline position ``x``; return D_min when decided."""
    if not np.isnan(row["d_min"]):
        ax.plot(
            [x, x],
            [row["d_min_low"], row["d_min"]],
            color=color,
            lw=3,
            alpha=0.35,
            solid_capstyle="butt",
        )
        ax.plot(x, row["d_min"], marker=marker, ms=6, color=color)
        return row["d_min"]
    if not np.isnan(row["d_min_low"]):
        ax.plot(x, row["d_min_low"], marker=">", ms=7, mfc=SURFACE, mec=color)
    return None


def _dmin_deadline_panel(ax: Axes, tables: dict[int, pd.DataFrame]) -> None:
    """D_min against the deadline, one line per (layout, N)."""
    for layout, n, ls, marker in DEADLINE_COMBOS:
        color = LAYOUT_COLOR[layout]
        # the offset keeps the two N of a layout, and the two layouts, from overprinting
        off = 0.05 * (1 if ls == "--" else -1) + (0.0 if layout == "wide" else 0.1)
        points = []
        for x, table in enumerate(tables.values()):
            d_min = _deadline_cell(ax, group_row(table, layout, n), x + off, color, marker)
            if d_min is not None:
                points.append((x + off, d_min))
        if len(points) > 1:
            ax.plot(*zip(*points), color=color, lw=1.0, ls=ls, label=f"{layout}, N = {n}")
    log_ticks(ax, [1, 2, 3, 4, 6, 8, 12], axis="y")
    ax.set_xticks(range(len(tables)))
    ax.set_xticklabels([str(m) for m in tables])
    ax.set_xlabel("deadline (drive times, tighter to the right)")
    ax.set_ylabel("D_min (99 percent rule)")
    ax.set_title("D_min against the deadline", fontsize=10)
    grid(ax)
    ax.legend(frameon=False, fontsize=7.5, loc="upper left")


def fig_deadline() -> None:
    """How the deadline moves the success curve and D_min (99 percent rule, main runs)."""
    runs = {m: pair[1] for m, pair in MAIN_RUNS.items()}
    if not have(*runs.values()):
        return
    data = {m: cells(name) for m, name in runs.items()}
    tables = {m: groups(name) for m, name in runs.items()}

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.4))
    for ax, (layout, n) in zip(axes[:2], SUCCESS_CURVES):
        _success_panel(ax, data, layout, n)
    axes[0].legend(frameon=False, fontsize=8, loc="lower right", title="deadline", title_fontsize=8)
    _dmin_deadline_panel(axes[2], tables)
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


# ----- pruning -----
def fig_pruning() -> None:
    """Finish time and dog overlap along one stored curve, with the cells pruning skips."""
    name, layout, n = MAIN_RUNS[6][1], "compact", 200
    if not have(name):
        return
    c = curve(cells(name), layout, n)
    overlap = curve(trials(name), layout, n).groupby("d")["mean_dog_overlap"].mean()
    d_sat = int(group_row(groups(name), layout, n)["d_sat"])
    confirm = confirming_team(dict(zip(c["d"], c["zone"])), d_sat)
    threshold = load_protocol(name).settings["prune_overlap"]
    pruned = c[c["pruned"]]
    if confirm is None or confirm == c["d"].max():
        raise ValueError(f"{name} {layout} N = {n}: no team above a confirmed saturation")
    above = c.loc[c["d"] > confirm, "d"].min()  # shade only teams above the confirming one

    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    marks = ax.get_xaxis_transform()  # x in data, y in axes fraction
    ax.axvspan(np.sqrt(confirm * above), D_MAX * 1.15, color=ORANGE, alpha=0.07, lw=0)
    ax.axvline(confirm, color=MUTED, lw=0.8, ls="-.")
    ax.text(confirm * 1.04, 0.6, "confirming team", color=MUTED, fontsize=8, transform=marks)
    ax.axvline(d_sat, color=MUTED, lw=0.8, ls="--")
    ax.text(d_sat * 1.04, 0.6, "D_sat", color=MUTED, fontsize=8, transform=marks)
    ax.plot(c["d"], c["median_finish_seconds"], color=BLUE, marker="o", ms=4)
    ax.set_ylim(0, c["median_finish_seconds"].max() * 1.1)  # from 0, so a few seconds look flat
    ax.set_ylabel("median finish time (s)", color=BLUE)
    d_axis(ax, ticks=tuple(c["d"]))
    grid(ax, "x")

    right = ax.twinx()
    right.spines["right"].set_visible(True)
    right.plot(overlap.index, overlap.to_numpy(), color=ORANGE, marker="s", ms=4, ls="--")
    right.plot(
        pruned["d"],
        overlap[pruned["d"]],
        color=ORANGE,
        marker="s",
        ms=10,
        mfc="none",
        ls="",
        label="pruned cell",
    )
    right.axhline(threshold, color=ORANGE, lw=0.8, ls=":")
    right.set_ylim(-0.03, 1.03)
    right.set_ylabel("mean dog overlap", color=ORANGE)
    right.legend(frameon=False, fontsize=8, loc="lower right", bbox_to_anchor=(1, 0.3))
    ax.set_title(f"{layout}, N = {n}, 99 percent rule, 6 drive times", fontsize=10)
    save(fig, "fig_adaptive_3_pruning.png")


# ----- growth fits -----
def _fit_layout(ax: Axes, g: pd.DataFrame, layout: str, marker: str) -> None:
    """The D_min brackets of one layout and the range each fitted shape allows beyond them."""
    color = LAYOUT_COLOR[layout]
    points = []
    for r in layout_rows(g, layout):
        found = interval_of(float(r["d_min"]), float(r["d_min_low"]))
        if found is None:
            continue
        points.append((int(r["n"]), found))
        ax.plot([r["n"], r["n"]], [found[0] + 0.5, found[1] - 0.5], color=color, lw=3, alpha=0.5)
        ax.plot(r["n"], found[1] - 0.5, marker=marker, color=color, ms=5, ls="")
    for shape, ls in FIT_SHAPES:
        lo, hi = zip(*[consistent_range(points, shape, int(n)) for n in FIT_AHEAD])
        ax.fill_between(FIT_AHEAD, lo, hi, color=color, alpha=0.08 if ls == ":" else 0.15)
        ax.plot(FIT_AHEAD, hi, color=color, lw=0.9, ls=ls)
    ax.plot([], [], color=color, marker=marker, ls="", label=layout)


def _fit_panel(ax: Axes, name: str, title: str) -> None:
    g = groups(name)
    for layout, marker in (("wide", "o"), ("outlier_rich", "s")):
        _fit_layout(ax, g, layout, marker)
    ax.axvline(CALIBRATION_EDGE, color=MUTED, lw=0.8)
    ax.text(CALIBRATION_EDGE + 10, 0.85, "calibration edge", fontsize=8, color=MUTED)
    log_ticks(ax, [25, 50, 100, 200, 400, 800, 1600, 3200])
    log_ticks(ax, [1, 2, 3, 5, 10, 20], axis="y")
    ax.set_xlabel("flock size N")
    ax.set_title(f"D_min, 99 percent rule, {title}", fontsize=10)
    grid(ax)


def fig_growth_fits() -> None:
    """D_min against N on the nine sizes (99 percent), with the range each fitted shape allows."""
    runs = ((MAIN_RUNS[12][1], "12 drive times"), (MAIN_RUNS[6][1], "6 drive times"))
    if not have(*[r for r, _ in runs]):
        return
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4), sharey=True)
    for ax, (name, title) in zip(axes, runs):
        _fit_panel(ax, name, title)
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
