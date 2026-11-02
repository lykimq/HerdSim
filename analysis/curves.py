"""D_min brackets from a finished run, and how they grow with N."""

from __future__ import annotations

import itertools
import math
from collections.abc import Callable
from pathlib import Path
from typing import NamedTuple

import numpy as np
import pandas as pd

from .growth_fits import compare as compare_shapes
from .growth_fits import interval_of
from .keys import split_group
from .results import read_groups

Bracket = tuple[float, float]

# Layouts the shape comparison covers; `split` is left out, since its success does not rise
# with D at N >= 200, and `compact` stays at D = 1.
SHAPE_LAYOUTS = ("wide", "outlier_rich")

# ----- reading a finished run -----


def split_group_key(frame: pd.DataFrame) -> pd.DataFrame:
    """Replace ``group_key`` with method, layout and n columns."""
    keys = pd.DataFrame([split_group(k) for k in frame["group_key"]], index=frame.index)
    return pd.concat([keys, frame.drop(columns=["group_key"])], axis=1)


def groups_table(folder: Path) -> pd.DataFrame:
    """One row per D curve from a results folder."""
    return split_group_key(read_groups(folder))


# ----- brackets -----


def bracket(row: pd.Series) -> Bracket | None:
    """(low, high) for D_min, or None if no reliable D on the grid."""
    if pd.isna(row["d_min"]) or pd.isna(row["d_min_low"]):
        return None
    return float(row["d_min_low"]), float(row["d_min"])


def midpoint(row: pd.Series) -> float | None:
    """Geometric midpoint of the bracket, or D_min_low alone if that is all there is."""
    b = bracket(row)
    if b:
        return math.sqrt(b[0] * b[1])
    if pd.notna(row["d_min_low"]):
        return float(row["d_min_low"])
    return None


# ----- growth with N -----


def slope_range(points: list[tuple[int, float, float]]) -> Bracket | None:
    """Min and max log2-D vs log2-N slope over bracket end-point combinations."""
    if len(points) < 2:
        return None
    log_n = np.log2([p[0] for p in points])
    x = log_n - log_n.mean()
    ends = [(math.log2(p[1]), math.log2(p[2])) for p in points]
    slopes = []
    for pick in itertools.product((0, 1), repeat=len(points)):
        y = np.array([ends[i][pick[i]] for i in range(len(points))])
        slopes.append(float((x * (y - y.mean())).sum() / (x * x).sum()))
    return min(slopes), max(slopes)


def _brackets_by_n(
    part: pd.DataFrame, bracket_of: Callable[[pd.Series], Bracket | None]
) -> tuple[list[tuple[int, float, float]], list[pd.Series]]:
    """Bracketed (N, low, high) points and the rows with no bracket, in N order."""
    points, rest = [], []
    for _, row in part.sort_values("n").iterrows():
        b = bracket_of(row)
        if b:
            points.append((int(row["n"]), b[0], b[1]))
        else:
            rest.append(row)
    return points, rest


class Growth(NamedTuple):
    """Growth of one layout's D_min brackets with N."""

    points: list[tuple[int, float, float]]  # (N, low, high)
    left_out: list[int]  # N with no bracket
    above_grid: list[int]  # left_out with no reliable D on the grid
    flat: bool  # every bracket is exactly 1
    slope: Bracket | None  # log-log slope range


def growth(part: pd.DataFrame, bracket_of: Callable[[pd.Series], Bracket | None]) -> Growth:
    """Growth summary for one layout under ``bracket_of``."""
    points, rest = _brackets_by_n(part, bracket_of)
    return Growth(
        points=points,
        left_out=[int(r["n"]) for r in rest],
        above_grid=[int(r["n"]) for r in rest if bool(r.get("d_min_above_grid", False))],
        flat=bool(points) and all(p[1] == p[2] == 1.0 for p in points),
        slope=slope_range(points),
    )


def _mean_spread(groups: dict[object, list[float]]) -> float:
    """Mean log2 of max / min over the groups that hold at least two midpoints."""
    spreads = [math.log2(max(v) / min(v)) for _, v in sorted(groups.items()) if len(v) >= 2]
    return float(np.mean(spreads)) if spreads else float("nan")


def layout_against_n(table: pd.DataFrame) -> dict[str, float]:
    """Mean log2 spread of midpoints: across layouts at fixed N, and across N at fixed layout."""
    by_n: dict[object, list[float]] = {}
    by_layout: dict[object, list[float]] = {}
    for _, r in table.iterrows():
        value = midpoint(r)
        if value is not None:
            by_n.setdefault(int(r["n"]), []).append(value)
            by_layout.setdefault(str(r["layout"]), []).append(value)
    return {
        "layout_spread_at_fixed_n": _mean_spread(by_n),
        "n_spread_at_fixed_layout": _mean_spread(by_layout),
    }


def shape_table(table: pd.DataFrame) -> pd.DataFrame:
    """Compare power-law vs saturating fits of D_min(N) on the two layouts that keep rising."""
    rows = []
    for layout in SHAPE_LAYOUTS:
        points = []
        for _, r in table[table["layout"] == layout].sort_values("n").iterrows():
            found = interval_of(float(r["d_min"]), float(r["d_min_low"]))
            if found is not None:
                points.append((int(r["n"]), found))
        rows.append({"layout": layout, **compare_shapes(points)})
    return pd.DataFrame(rows)
