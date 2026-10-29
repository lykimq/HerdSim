"""The D curves of a finished run as numbers: the groups table, the brackets of D_min and D_sat,
and how D_min grows with N.

A D curve has two numbers for its smallest reliable team:

- ``d_min``: the smallest D decided reliable
- ``d_min_low``: the smallest D whose success interval still reaches theta
- the true D_min lies in [d_min_low, d_min] when d_min exists, and at or above d_min_low when it
  does not (no D on the grid is decided reliable yet); the slope of D_min against N is the range
  the brackets allow

How these numbers are written in the docs ('2-4', '[2]') is in docs/generate_docs/report/text.py.
"""

from __future__ import annotations

import itertools
import math
from collections.abc import Callable
from pathlib import Path
from typing import NamedTuple

import numpy as np
import pandas as pd

from .frontier import COLLAPSE, CROWDED, RECOVERED, RELIABLE, UNRELIABLE, UNRELIABLE_DIP
from .growth_fits import compare as compare_shapes
from .growth_fits import interval_of
from .keys import join_group, split_group
from .results import read_groups

# Zones of a cell where more dogs did worse.
WORSE_ZONES = (CROWDED, UNRELIABLE_DIP, COLLAPSE, RECOVERED)

Bracket = tuple[float, float]

# ------------------------------------------------------------------- reading a finished run


def split_group_key(frame: pd.DataFrame) -> pd.DataFrame:
    """``frame`` with its group_key column replaced by method, layout, factors and n."""
    keys = pd.DataFrame([split_group(k) for k in frame["group_key"]], index=frame.index)
    return pd.concat([keys, frame.drop(columns=["group_key"])], axis=1)


def groups_table(folder: Path) -> pd.DataFrame:
    """One row per D curve: method, layout, factors, n and the D values."""
    return split_group_key(read_groups(folder))


def one_level(table: pd.DataFrame) -> pd.DataFrame:
    """``table`` itself; raises when it holds several factor levels, which a table keyed by
    layout and N would mix (a factor protocol such as dmin_s_gap is shown with ``compare``)."""
    if "factors" in table and table["factors"].nunique() > 1:
        levels = sorted(table["factors"].unique())
        raise ValueError(f"several factor levels {levels}; use compare, which keeps them apart")
    return table


# ---------------------------------------------------------------------------------- brackets


def bracket(row: pd.Series) -> Bracket | None:
    """(low, high) of the true D_min, or None when no D on the grid is decided reliable."""
    if pd.isna(row["d_min"]) or pd.isna(row["d_min_low"]):
        return None
    return float(row["d_min_low"]), float(row["d_min"])


def dsat_bracket(row: pd.Series) -> Bracket | None:
    """(low, high) of the true D_sat, or None when the curve has no D_sat or the grid
    censors it.

    An undecided D_sat can only move up: what is open is whether a larger reliable D is
    faster than it. So the true value lies between d_sat and the largest working D, d_max.
    A curve still improving at the top of the grid has its D_sat above the grid.
    """
    if pd.isna(row["d_sat"]) or bool(row.get("still_improving_at_top", False)):
        return None
    low = float(row["d_sat"])
    if bool(row.get("d_sat_undecided", False)) and pd.notna(row["d_max"]):
        return low, max(low, float(row["d_max"]))
    return low, low


def midpoint(row: pd.Series) -> float | None:
    """Geometric middle of the bracket, or D_min_low when only the low end is known."""
    b = bracket(row)
    if b:
        return math.sqrt(b[0] * b[1])
    if pd.notna(row["d_min_low"]):
        return float(row["d_min_low"])
    return None


# ------------------------------------------------------------------------------- growth with N


def slope_range(points: list[tuple[int, float, float]]) -> Bracket | None:
    """Range of the least-squares slope of log2 D against log2 N over the brackets.

    ``points`` are (N, low, high). The fitted slope is linear in the D values, so its
    extremes are reached when every D sits at one end of its bracket; every combination
    is tried. None with fewer than two flock sizes.
    """
    if len(points) < 2:
        return None
    x = np.log2([p[0] for p in points])
    x = x - x.mean()
    ends = [(math.log2(p[1]), math.log2(p[2])) for p in points]
    slopes = []
    for pick in itertools.product((0, 1), repeat=len(points)):
        y = np.array([ends[i][pick[i]] for i in range(len(points))])
        slopes.append(float((x * (y - y.mean())).sum() / (x * x).sum()))
    return min(slopes), max(slopes)


def _brackets_by_n(
    part: pd.DataFrame, bracket_of: Callable[[pd.Series], Bracket | None]
) -> tuple[list[tuple[int, float, float]], list[pd.Series]]:
    """For one layout, in order of N: (N, low, high) of every curve ``bracket_of`` can
    bracket, and the rows it cannot."""
    points, rest = [], []
    for _, row in part.sort_values("n").iterrows():
        b = bracket_of(row)
        if b:
            points.append((int(row["n"]), b[0], b[1]))
        else:
            rest.append(row)
    return points, rest


class Growth(NamedTuple):
    """How one layout's curves grow with N under one bracket (of D_min or D_sat)."""

    points: list[tuple[int, float, float]]  # (N, low, high) of the bracketed curves
    left_out: list[int]  # N of the curves with no bracket, in order of N
    above_grid: list[int]  # those of them with no reliable D on the grid
    flat: bool  # every bracketed value is 1
    slope: Bracket | None  # range of the log-log slope, None with fewer than two points


def growth(part: pd.DataFrame, bracket_of: Callable[[pd.Series], Bracket | None]) -> Growth:
    """The growth of one layout's curves: what ``bracket_of`` can bracket, what it leaves out
    and why, and the slope range over the brackets."""
    points, rest = _brackets_by_n(part, bracket_of)
    return Growth(
        points=points,
        left_out=[int(r["n"]) for r in rest],
        above_grid=[int(r["n"]) for r in rest if bool(r.get("d_min_above_grid", False))],
        flat=bool(points) and all(p[1] == p[2] == 1.0 for p in points),
        slope=slope_range(points),
    )


def layout_against_n(table: pd.DataFrame) -> dict[str, float]:
    """How much D_min moves between layouts at one N against between N at one layout.

    Both are in doublings (log2 of the largest over the smallest bracket midpoint),
    averaged over the N values and over the layouts respectively. Descriptive only: it
    states which axis moves D_min more here and says nothing more.
    """
    rows = one_level(table).iterrows()
    mid = {(str(r["layout"]), int(r["n"])): midpoint(r) for _, r in rows}
    mid = {k: v for k, v in mid.items() if v is not None}

    def spread(values: list[float]) -> float | None:
        return math.log2(max(values) / min(values)) if len(values) >= 2 else None

    by_n = [
        spread([v for (_, n2), v in mid.items() if n2 == n]) for n in sorted({n for _, n in mid})
    ]
    by_layout = [
        spread([v for (lay2, _), v in mid.items() if lay2 == lay])
        for lay in sorted({lay for lay, _ in mid})
    ]
    by_n = [s for s in by_n if s is not None]
    by_layout = [s for s in by_layout if s is not None]
    return {
        "layout_spread_at_fixed_n": float(np.mean(by_n)) if by_n else float("nan"),
        "n_spread_at_fixed_layout": float(np.mean(by_layout)) if by_layout else float("nan"),
    }


def shape_table(
    table: pd.DataFrame, layouts: tuple[str, ...] = ("wide", "outlier_rich")
) -> pd.DataFrame:
    """Per layout: a power law against a curve that levels off, fitted to D_min(N) over the
    brackets. split is not fitted by default: its success does not rise with D at N >= 200."""
    rows = []
    for layout in layouts:
        points = []
        for _, r in table[table["layout"] == layout].sort_values("n").iterrows():
            found = interval_of(float(r["d_min"]), float(r["d_min_low"]))
            if found is not None:
                points.append((int(r["n"]), found))
        rows.append({"layout": layout, **compare_shapes(points)})
    return pd.DataFrame(rows)


# ----------------------------------------------------------------- cost and upper end


class Effort(NamedTuple):
    """What dogs beyond D_sat cost on one curve, relative to the D_sat cell: finish time, dog
    time and dog path as ratios, at D_double and at D_top (empty where that D has no cell)."""

    d_double: int | None  # smallest reliable working D at or above 2 D_sat
    d_top: int  # largest working D
    double: dict[str, float]
    top: dict[str, float]


def _cell_medians(cells: pd.DataFrame, key: str) -> dict[int, tuple[float, float, float]]:
    """Per reliable D of the curve ``key``: (median finish, median dog ticks, total dog path)."""
    mine = cells[(cells["group_key"] == key) & (cells["reliability"] == RELIABLE)]
    return {
        int(c["n_shepherds"]): (
            float(c["median_finish"]),
            float(c["median_dog_ticks"]),
            int(c["n_shepherds"]) * float(c["median_path_per_dog"]),
        )
        for _, c in mine.iterrows()
    }


def _ratios(values: tuple[float, ...], base: tuple[float, ...]) -> dict[str, float]:
    """Finish time, dog time and dog path of one cell relative to the D_sat cell."""
    return dict(zip(("time", "dog_time", "path"), (v / b for v, b in zip(values, base))))


def effort(cells: pd.DataFrame, curve: pd.Series) -> Effort | None:
    """The cost of dogs beyond D_sat on ``curve``, or None when it has no D_sat below its
    largest working D or no reliable D_sat cell.

    Medians over the successful seeds of each cell (frontier_cells.csv): finish time, dog
    time (D x finish ticks) and total dog path (D x path per dog). A finish time ratio near 1
    with dog time near D / D_sat is effort spent for no gain.
    """
    if pd.isna(curve["d_sat"]) or pd.isna(curve["d_max"]):
        return None
    sat, top = int(curve["d_sat"]), int(curve["d_max"])
    if top <= sat:
        return None
    factors = str(curve["factors"]) if curve.get("factors") else ""
    key = join_group(str(curve["method"]), str(curve["layout"]), factors, int(curve["n"]))
    medians = _cell_medians(cells, key)
    if sat not in medians:
        return None
    working = [d for d in medians if sat <= d <= top]
    double = next((d for d in sorted(working) if d >= 2 * sat), None)
    return Effort(
        d_double=double,
        d_top=top,
        double=_ratios(medians[double], medians[sat]) if double is not None else {},
        top=_ratios(medians[top], medians[sat]),
    )


class UpperEnd(NamedTuple):
    """What bounds the curves of a run from above."""

    counts: dict[str, int]
    flagged: pd.DataFrame  # curves with D_max below the grid top, a D_crowd or a D_overcrowd
    grid_top: pd.Series  # largest D run, by group key


def upper_end(table: pd.DataFrame, cells: pd.DataFrame) -> UpperEnd:
    """Counts of curves by what bounds them from above, and the curves bounded below the grid.

    A D_max at the grid top is a lower bound, not a value: the top cell is reliable and the
    curve has no D_overcrowd, so the count of such curves says how often no upper limit was
    found (cells below the top may still be undecided)."""
    has_min = table["d_min"].notna()
    below = has_min & ~table["d_max_at_grid_top"].astype(bool)
    counts = {
        "curves": len(table),
        "with D_min": int(has_min.sum()),
        "D_max at grid top": int((has_min & ~below).sum()),
        "D_max below grid top": int(below.sum()),
        "with D_crowd": int(table["d_crowd"].notna().sum()),
        "with D_overcrowd": int(table["d_overcrowd"].notna().sum()),
    }
    flagged = table[below | table["d_crowd"].notna() | table["d_overcrowd"].notna()]
    return UpperEnd(counts, flagged, cells.groupby("group_key")["n_shepherds"].max())


# ------------------------------------------------------------ cells where more dogs did worse


def unusual_zones(cells: pd.DataFrame) -> pd.DataFrame:
    """Curves with a cell where more dogs did worse: crowded (slower than D_best), an
    unreliable dip, a collapse or a recovery. One row per such cell, with the median finish
    of the curve's fastest reliable D beside it for scale."""
    flagged = cells[cells["zone"].isin(WORSE_ZONES)]
    rows = []
    for key, part in flagged.groupby("group_key", sort=True):
        curve = cells[cells["group_key"] == key]
        reliable = curve[curve["reliability"] == RELIABLE].sort_values("median_finish")
        fastest = reliable.iloc[0] if len(reliable) else None
        for _, cell in part.iterrows():
            rows.append(
                {
                    **{k: v for k, v in split_group(str(key)).items() if k != "factors"},
                    "d": int(cell["n_shepherds"]),
                    "zone": cell["zone"],
                    "success_rate": round(float(cell["success_rate"]), 2),
                    "median_finish": cell["median_finish"],
                    "fastest_d": int(fastest["n_shepherds"]) if fastest is not None else "-",
                    "fastest_finish": fastest["median_finish"] if fastest is not None else "-",
                }
            )
    return pd.DataFrame(rows)


def dips(cells: pd.DataFrame, groups: pd.DataFrame) -> pd.DataFrame:
    """Cells above D_min that are not reliable: success fell back below theta as D rose."""
    d_min = {r["group_key"]: r["d_min"] for _, r in groups.iterrows()}
    rows = []
    for _, cell in cells.iterrows():
        floor = d_min.get(cell["group_key"])
        if floor is None or pd.isna(floor):
            continue
        if cell["n_shepherds"] > floor and cell["reliability"] == UNRELIABLE:
            key = split_group(cell["group_key"])
            rows.append(
                {
                    "layout": key["layout"],
                    "n": key["n"],
                    "d": int(cell["n_shepherds"]),
                    "d_min": int(floor),
                    "success_rate": round(float(cell["success_rate"]), 2),
                    "seeds": int(cell["n_seeds"]),
                    "zone": cell["zone"],
                }
            )
    return pd.DataFrame(rows)
