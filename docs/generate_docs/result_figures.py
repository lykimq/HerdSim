"""Result figures for make_result_figures.py.

Data and axis helpers first, then the three figures of D_min against N and the deadline.
Style in figstyle.py; a missing run folder stops the figure with an error.
"""

from __future__ import annotations

from collections.abc import Hashable, Sequence
from itertools import product
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.lines import Line2D

from analysis.curves import groups_table, split_group_key
from analysis.frontier import clopper_pearson, confirming_team
from analysis.growth_fits import consistent_range, interval_of
from analysis.results import read_cells, read_once, read_trials
from analysis.trial_measures import reach_by_n
from docs.generate_docs.figstyle import (
    AQUA,
    BLUE,
    INK,
    MUTED,
    ORANGE,
    RED,
    SURFACE,
    ZONE_COLOR,
    grid,
    log_ticks,
    n_axis,
    save,
)
from docs.generate_docs.runs import F99_RUNS, FAT_RUNS, NINE_SIZE_RUNS, STRICT_RUNS
from services.protocol import RESULTS_ROOT, load_protocol
from services.replay import open_run
from sim.strombom.params import FAT, METHOD
from sim.trial import initial_state

Row = dict[Hashable, Any]  # one row of a groups table, from DataFrame.to_dict("records")

# ----- settings -----
LAYOUT_COLOR = {"compact": MUTED, "wide": BLUE, "split": ORANGE, "outlier_rich": AQUA}
# Light to dark blues for an ordered series (deadlines, flock sizes).
BLUES = ("#bcd3f0", "#8fb9ec", "#5b95de", "#2a78d6", "#0b2f66")

_STRICT_GRID = load_protocol(STRICT_RUNS[12])
_F99_GRID = load_protocol(NINE_SIZE_RUNS[0])
D_MAX = max(_STRICT_GRID.shepherd_counts)  # largest team size the runs try
N_TOP = max(_F99_GRID.flock_sizes)  # largest flock size the runs try
THETA = _STRICT_GRID.settings["reliability_theta"]
D_TICKS = (1, 2, 4, 8, 16, D_MAX)

# D_min against N: marker and line style of the strict rule, then of the 99 percent rule.
RULE_STYLES = (("o", "-"), ("s", "--"))
RULE_COLORS = (BLUE, ORANGE)
RULE_LABELS = ("strict (every sheep)", "99 percent of the sheep")
DMIN_XTICKS = (25, 50, 100, 200, 400, N_TOP)
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

# Adaptive-sampling figures: one stored curve where D = 2 stays undecided at 200 seeds and the
# campaign added D = 5 between an improving and a saturated team.
ADAPTIVE_CASE = (F99_RUNS[6], "wide", 400, 2)

# Growth-fit figure: sizes the fits are extended to, and the shapes with their line style.
FIT_AHEAD = np.array([N_TOP, 800, 1131, 1600, 2263, 3200])
FIT_SHAPES = (("power law", "--"), ("saturating", ":"))
# Smallest tested N whose calibration fails its 5% limits with 3 seeds per start
# (results/diagnostics/calibration_dmin_f99_m6.csv).
CALIBRATION_EDGE = 630

# FAT baseline comparison at 6 drive times, strict and 99 percent rules.
FAT_PANELS = (
    ("compact", 400),
    ("wide", 200),
    ("wide", 400),
    ("outlier_rich", 200),
    ("split", 200),
)
FAT_SERIES = (
    (STRICT_RUNS[6], METHOD, f"{METHOD}, strict", BLUE, "o-", -1.5),
    (F99_RUNS[6], METHOD, f"{METHOD}, 99 percent", BLUE, "s--", -0.5),
    (FAT_RUNS[0], FAT, f"{FAT}, strict", ORANGE, "o-", 0.5),
    (FAT_RUNS[1], FAT, f"{FAT}, 99 percent", ORANGE, "s--", 1.5),
)


# ----- data access -----
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
        if low < d_min:  # a smaller D is still undecided: a bracket
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
        xs, ys = zip(*points, strict=True)
        ax.plot(xs, ys, color=color, lw=1.2, alpha=0.85, ls=ls)
        ax.plot(xs, ys, marker=marker, color=color, ms=6, ls="", mec=SURFACE, mew=0.8)


def _dmin_panel(ax: Axes, runs: Sequence[str], layout: str) -> None:
    """One deadline and one layout: both rules."""
    for k, (name, (marker, ls), color) in enumerate(
        zip(runs, RULE_STYLES, RULE_COLORS, strict=True)
    ):
        shift = 1.0 + 0.05 * (k - 0.5)
        _dmin_layout(ax, layout_rows(groups(name), layout), color, shift, marker, ls)
    log_ticks(ax, DMIN_XTICKS)
    log_ticks(
        ax,
        [*DMIN_YTICKS, NONE_Y],
        axis="y",
        labels=[*map(str, DMIN_YTICKS), "none"],
    )
    grid(ax)


def _dmin_legend_handles() -> list[Line2D]:
    rules = [
        Line2D([], [], color=color, marker=marker, ls=ls, label=label)
        for (marker, ls), color, label in zip(RULE_STYLES, RULE_COLORS, RULE_LABELS, strict=True)
    ]
    return [
        *rules,
        Line2D(
            [], [], color=MUTED, lw=2.2, alpha=0.45, label="bracket: a smaller D still undecided"
        ),
        Line2D(
            [],
            [],
            color=MUTED,
            marker="^",
            mfc="none",
            ls="",
            label=f"not decided: D_min_low (line up to {D_MAX})",
        ),
        Line2D(
            [],
            [],
            color=MUTED,
            marker="x",
            ls="",
            label=f"none: every D tested, up to {D_MAX}, unreliable",
        ),
    ]


def fig_dmin_vs_n() -> None:
    """D_min vs N for the three main runs (strict and 99 percent), with undecided brackets."""
    layouts = [layout for layout in LAYOUT_COLOR if layout != "compact"]
    pairs = {m: (STRICT_RUNS[m], F99_RUNS[m]) for m in STRICT_RUNS}  # strict, then 99 percent
    fig, axes = plt.subplots(len(layouts), len(pairs), figsize=(11, 8.6), sharex=True, sharey=True)
    for (layout, runs), ax in zip(product(layouts, pairs.values()), axes.flat, strict=True):
        _dmin_panel(ax, runs, layout)
    for ax, m in zip(axes[0], pairs, strict=True):
        ax.set_title(f"{m} drive times")
    for ax, layout in zip(axes[:, 0], layouts, strict=True):
        ax.set_ylabel(f"{layout}\nD_min (dogs)")
    for ax in axes[-1]:
        ax.set_xlabel("flock size N")
    fig.legend(
        handles=_dmin_legend_handles(), loc="lower center", ncol=3, frameon=False, fontsize=8.5
    )
    save(fig, "fig20_dmin_vs_n.png", rect=(0, 0.07, 1, 1))


# ----- reach -----
def fig_reach() -> None:
    """Median reach of one dog against N per layout, 99 percent rule, at the three deadlines."""
    fig, axes = plt.subplots(1, len(F99_RUNS), figsize=(11, 3.6), sharey=True)
    for ax, (m, name) in zip(axes, F99_RUNS.items(), strict=True):
        table = reach_by_n(trials(name))
        for layout, color in LAYOUT_COLOR.items():
            rows = table[table["layout"] == layout].sort_values("n")
            ax.plot(rows["n"], rows["reach"], color=color, marker="o", ms=4, label=layout)
        n_axis(ax, DMIN_XTICKS)
        ax.set_ylim(0, 1.05)
        ax.set_title(f"{m} drive times")
        grid(ax)
    axes[0].set_ylabel("reach of one dog (median)")
    axes[0].legend(frameon=False, fontsize=8, loc="lower left")
    save(fig, "fig_reach.png")


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
            ax.plot(
                *zip(*points, strict=True), color=color, lw=1.0, ls=ls, label=f"{layout}, N = {n}"
            )
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
    data = {m: cells(name) for m, name in F99_RUNS.items()}
    tables = {m: groups(name) for m, name in F99_RUNS.items()}

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.4))
    for ax, (layout, n) in zip(axes[:2], SUCCESS_CURVES, strict=True):
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


# ----- adaptive sampling -----
def _running_rates(
    successes: np.ndarray, looks: np.ndarray, confidence: float
) -> tuple[np.ndarray, np.ndarray]:
    """The rate and its interval after each look, from the successes in seed order."""
    wins = np.cumsum(successes)[looks - 1]
    bounds = np.array(
        [clopper_pearson(int(k), int(n), confidence) for k, n in zip(wins, looks, strict=True)]
    )
    return wins / looks, bounds


def fig_stopping() -> None:
    """Interval bounds after each batch: all failures, all successes, and one stored cell
    that stays undecided at the seed limit."""
    name, layout, n, d = ADAPTIVE_CASE
    s = load_protocol(name).settings
    batch, cap, conf = s["batch_seeds"], s["max_seeds"], s["confidence"]
    looks = np.arange(batch, cap + 1, batch)
    cell = curve(trials(name), layout, n)
    cell = cell[cell["d"] == d].sort_values("seed_index")
    seen = looks[looks <= len(cell)]
    if not len(seen):
        raise ValueError(f"{name} {layout} N = {n} D = {d}: fewer than {batch} stored trials")
    rates, bounds = _running_rates(cell["success"].to_numpy(dtype=int), seen, conf)

    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    # (share of trials that succeed, which bound to draw, colour, label)
    for share, side, color, label in (
        (0, 1, RED, "upper bound, no trial succeeds"),
        (1, 0, AQUA, "lower bound, every trial succeeds"),
    ):
        edge = [clopper_pearson(share * int(k), int(k), conf)[side] for k in looks]
        ax.plot(looks, edge, color=color, marker="o", ms=3, label=label)
    ax.errorbar(
        seen,
        rates,
        yerr=[rates - bounds[:, 0], bounds[:, 1] - rates],
        color=BLUE,
        marker="o",
        ms=3,
        capsize=2,
        lw=1,
        label=f"{layout}, N = {n}, D = {d}: rate and interval",
    )
    theta_line(ax, color=INK, ls="--")
    ax.set_xticks(looks[1::2])
    ax.set_xlabel("trials in the cell")
    ax.set_ylabel("success rate")
    ax.set_ylim(0, 1.02)
    grid(ax)
    ax.legend(frameon=False, fontsize=8, loc="center right")
    save(fig, "fig_adaptive_1_refinement.png")


def fig_densification() -> None:
    """One stored curve: the protocol's team sizes and those the campaign added, by zone."""
    name, layout, n, _ = ADAPTIVE_CASE
    listed = set(load_protocol(name).shepherd_counts)
    c = curve(cells(name), layout, n)

    fig, ax = plt.subplots(figsize=(7.5, 1.9))
    for row in c.itertuples():
        added = row.d not in listed
        ax.plot(
            row.d,
            0,
            ls="",
            marker="*" if added else "o",
            ms=16 if added else 10,
            color=ZONE_COLOR[str(row.zone)],
            mec=INK,
            mew=0.6,
        )
    for zone in dict.fromkeys(c["zone"]):
        ax.plot([], [], ls="", marker="o", color=ZONE_COLOR[str(zone)], label=str(zone))
    ax.plot([], [], ls="", marker="*", ms=10, color=MUTED, label="added by the campaign")
    d_axis(ax, ticks=tuple(c["d"]))
    ax.set_ylim(-0.5, 0.8)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_title(f"{layout}, N = {n} ({name})", fontsize=10)
    ax.legend(frameon=False, fontsize=7.5, ncol=5, loc="upper center", bbox_to_anchor=(0.5, 1.0))
    save(fig, "fig_adaptive_2_densification.png")


def fig_paired_seeds() -> None:
    """The start of seeds 0 to 2 at three team sizes of one stored curve, with each outcome."""
    name, layout, n, _ = ADAPTIVE_CASE
    run = open_run(name)  # refuses a folder whose protocol now gives other physics
    teams, seeds = (2, 3, 4), (0, 1, 2)

    # One scale for every panel, so the same seed shows the same flock at every team size.
    fig, axes = plt.subplots(len(teams), len(seeds), figsize=(7.5, 6.6), sharex=True, sharey=True)
    for (d, i), ax in zip(product(teams, seeds), axes.flat, strict=True):
        job = run.job(METHOD, layout, n, d, i)
        state = initial_state(job.config, job.seed)
        ax.plot(*state.sheep_positions.T, ls="", marker="o", ms=1.2, color=BLUE)
        ax.plot(*state.shepherd_positions.T, ls="", marker="^", ms=5, color=ORANGE)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        ok = job.stored[0]
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color(AQUA if ok else RED)
        ax.set_title(f"seed {job.seed}, D = {d}: {'success' if ok else 'failure'}", fontsize=8.5)
    save(fig, "fig_adaptive_4_paired_seeds.png")


# ----- pruning -----
def fig_pruning() -> None:
    """Finish time and dog overlap along one stored curve, with the cells pruning skips."""
    name, layout, n = F99_RUNS[6], "compact", 200
    c = curve(cells(name), layout, n)
    overlap = curve(trials(name), layout, n).groupby("d")["mean_dog_overlap"].mean()
    d_sat = int(group_row(groups(name), layout, n)["d_sat"])
    confirm = confirming_team(dict(zip(c["d"], c["zone"], strict=True)), d_sat)
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
    ax.set_title(f"{layout}, N = {n} ({name})", fontsize=10)
    save(fig, "fig_adaptive_3_pruning.png")


# ----- growth fits -----
def _fit_layout(ax: Axes, g: pd.DataFrame, layout: str, marker: str, shift: float) -> None:
    """The D_min brackets of one layout and the range each fitted shape allows beyond them;
    ``shift`` offsets x so the two layouts do not hide each other."""
    color = LAYOUT_COLOR[layout]
    points = []
    for r in layout_rows(g, layout):
        found = interval_of(float(r["d_min"]), float(r["d_min_low"]))
        if found is None:
            continue
        points.append((int(r["n"]), found))
        x = r["n"] * shift
        ax.plot([x, x], [found[0] + 0.5, found[1] - 0.5], color=color, lw=3, alpha=0.5)
        ax.plot(x, found[1] - 0.5, marker=marker, color=color, ms=5, ls="")
    for shape, ls in FIT_SHAPES:
        lo, hi = zip(*[consistent_range(points, shape, int(n)) for n in FIT_AHEAD], strict=True)
        ax.fill_between(FIT_AHEAD, lo, hi, color=color, alpha=0.08 if ls == ":" else 0.15)
        ax.plot(FIT_AHEAD, hi, color=color, lw=0.9, ls=ls)
    ax.plot([], [], color=color, marker=marker, ls="", label=layout)


def _fit_panel(ax: Axes, name: str, title: str) -> None:
    g = groups(name)
    for layout, marker, shift in (("wide", "o", 0.96), ("outlier_rich", "s", 1.04)):
        _fit_layout(ax, g, layout, marker, shift)
    ax.axvline(CALIBRATION_EDGE, color=MUTED, lw=0.8)
    ax.text(CALIBRATION_EDGE + 20, 17, "calibration edge", fontsize=8, color=MUTED)
    log_ticks(ax, [25, 50, 100, 200, 400, 800, 1600, 3200])
    log_ticks(ax, [1, 2, 3, 5, 10, 20], axis="y")
    ax.set_xlabel("flock size N")
    ax.set_title(f"D_min, 99 percent rule, {title}", fontsize=10)
    grid(ax)


def fig_growth_fits() -> None:
    """D_min against N on the nine sizes (99 percent), with the range each fitted shape allows."""
    runs = [(name, f"{m} drive times") for m, name in F99_RUNS.items() if name in NINE_SIZE_RUNS]
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4), sharey=True)
    for ax, (name, title) in zip(axes, runs, strict=True):
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
            f"Shaded beyond N = {N_TOP}: the "
            "range of D allowed by every curve of each shape that passes through all the brackets."
        ),
    )


# ----- FAT baseline -----
def _fat_panel(ax: Axes, data: dict[str, pd.DataFrame], layout: str, n: int) -> None:
    """Success rate against D for strombom_multi and fat at 6 drive times."""
    for name, method, label, color, fmt, step in FAT_SERIES:
        part = curve(data[name], layout, n)
        part = part[part["method"] == method]
        rate_errorbars(
            ax,
            part,
            part["d"] * (1 + 0.025 * step),
            color,
            fmt,
            label,
            ms=4,
            lw=1.3,
            elinewidth=0.75,
            capsize=1.6,
        )
    theta_line(ax)
    d_axis(ax)
    ax.set_ylim(-0.04, 1.05)
    ax.set_title(f"{layout}, N = {n}", fontsize=10)
    grid(ax)


def fig_fat() -> None:
    """Success rate vs D for strombom_multi and fat at 6 drive times (strict and 99 percent)."""
    data = {name: cells(name) for name, *_ in FAT_SERIES}
    fig, axes = plt.subplots(1, len(FAT_PANELS), figsize=(16.5, 3.8), sharey=True)
    for ax, (layout, n) in zip(axes, FAT_PANELS, strict=True):
        _fat_panel(ax, data, layout, n)
    axes[0].set_ylabel("success rate (6 drive times)")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4, frameon=False, fontsize=8.5)
    save(fig, "fig26_fat.png", rect=(0, 0.08, 1, 1))
