"""Settings, data access and axis helpers that every results figure uses."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from functools import cache, wraps

import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.colors import LinearSegmentedColormap

from analysis.curves import groups_table, split_group_key
from analysis.results import read_cells, read_trials
from docs.generate_docs.figstyle import (
    AQUA,
    BLUE,
    MUTED,
    ORANGE,
    SURFACE,
)
from docs.generate_docs.report.overview import F99_MAIN, ORIGINAL_NS, STRICT_MAIN
from services.protocol import RESULTS_ROOT

# ------------------------------------------------------------------------------------ settings

# Runs shared by several figures: (strict, 99 percent) per deadline in drive times.
MAIN_RUNS = dict(zip((12, 6, 3), zip(STRICT_MAIN, F99_MAIN, strict=True), strict=True))

LAYOUT_COLOR = {"compact": MUTED, "wide": BLUE, "split": ORANGE, "outlier_rich": AQUA}
# Light to dark blues for an ordered series (deadlines, flock sizes).
BLUES = ("#bcd3f0", "#8fb9ec", "#5b95de", "#2a78d6", "#0b2f66")
SEQ = LinearSegmentedColormap.from_list("seq", ["#eaf1fb", "#2a78d6", "#0b2f66"])

NS = ORIGINAL_NS
D_TICKS = (1, 2, 4, 8, 16, 24)
THETA = 0.9
FEW_TRIALS = 30  # a cell with fewer trials is drawn hollow: its rate is less certain


# ---------------------------------------------------------------------------------- data access


def have(*names: str) -> bool:
    missing = [n for n in names if not (RESULTS_ROOT / n / "frontier_cells.csv").exists()]
    if missing:
        print("missing", missing, ": figure skipped")
    return not missing


def read_once(load: Callable[[str], pd.DataFrame]) -> Callable[[str], pd.DataFrame]:
    """Read a run's file once for all figures (the trial files are 25 to 64 MB). Each call gets a
    copy, so a figure may add columns without changing what the next figure reads."""
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
    return read_trials(RESULTS_ROOT / name)


@read_once
def groups(name: str) -> pd.DataFrame:
    return groups_table(RESULTS_ROOT / name)


def curve(t: pd.DataFrame, layout: str, n: int) -> pd.DataFrame:
    """The cells of one D curve, in order of D."""
    return t[(t["layout"] == layout) & (t["n"] == n)].sort_values("d")


def group_row(g: pd.DataFrame, layout: str, n: int) -> pd.Series:
    return g[(g["layout"] == layout) & (g["n"] == n)].iloc[0]


def short(layout: str) -> str:
    """Layout name for a crowded tick label."""
    return layout.replace("_rich", "")


# ---------------------------------------------------------------------------------- axes helpers


def log_ticks(
    ax: Axes,
    ticks: Sequence[float],
    axis: str = "x",
    labels: Sequence[str] | None = None,
) -> None:
    """Log scale with only the given ticks, labelled as plain numbers.

    Minor ticks are switched off last, because setting a log scale brings them back.
    """
    shown = [str(t) for t in ticks] if labels is None else list(labels)
    if axis == "x":
        ax.set_xscale("log")
        ax.set_xticks(ticks)
        ax.set_xticklabels(shown)
    else:
        ax.set_yscale("log")
        ax.set_yticks(ticks)
        ax.set_yticklabels(shown)
    ax.minorticks_off()


def d_axis(ax: Axes, ticks: Sequence[float] = D_TICKS, label: str = "dogs D") -> None:
    """The team-size axis most figures share."""
    log_ticks(ax, ticks)
    ax.set_xlabel(label)


def theta_line(ax: Axes, color: str = MUTED, ls: str = ":") -> None:
    ax.axhline(THETA, color=color, lw=0.8, ls=ls)


def rate_line(
    ax: Axes,
    t: pd.DataFrame,
    color: str,
    marker: str,
    ls: str = "-",
    label: str | None = None,
    dx: float = 1.0,
    few: int = FEW_TRIALS,
) -> None:
    """Success rate against D for one curve; a hollow marker is a cell with fewer than ``few``
    trials, whose rate is less certain (cells decided early stop receiving seeds)."""
    ax.plot(
        t["d"] * dx, t["success_rate"], color=color, marker=marker, ms=5, lw=1.1, ls=ls, label=label
    )
    small = t[t["n_seeds"] < few]
    ax.plot(
        small["d"] * dx,
        small["success_rate"],
        ls="",
        marker=marker,
        ms=5,
        mfc=SURFACE,
        mec=color,
        zorder=4,
    )


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
