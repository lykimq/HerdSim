"""Summary tables of finished runs: D_min, D_sat, their growth with N, cost, zones, comparisons.

    uv run cli/dmin_tables.py dmin dmin_f99_m12 dmin_f99_m6
    uv run cli/dmin_tables.py growth dmin_f99_m6
    uv run cli/dmin_tables.py --help                  # every table, one verb each

Each function takes what a finished run wrote (frontier_groups.csv, frontier_cells.csv,
trials.csv) and returns a DataFrame; cli/dmin_tables.py has one verb per table and prints it as
Markdown. Nothing here runs a simulation, so every table can be redone in seconds after a rule
or a run changes.

The file has five sections:

- reading a finished run: the groups table with method, layout, factors and N split out of the
  key
- D_min as text and bracket: '4', '2-4', '[2]' or 'none on grid', and the bracket behind each
- growth with N: the range of log-log slopes the brackets allow, and the shape fits
- D_sat: its text, bracket and growth
- cost, zones, checks and comparisons: effort beyond D_sat, cells where more dogs did worse, the
  flock's size against R_f, and one run beside another

A D curve has two numbers, so growth is a range:

- ``d_min``: the smallest D decided reliable
- ``d_min_low``: the smallest D whose success interval still reaches theta
- the true D_min lies in [d_min_low, d_min] when d_min exists, and at or above d_min_low when it
  does not (no D on the grid is decided reliable yet); the slope of D_min against N is reported
  as the range the brackets allow
"""

from __future__ import annotations

import itertools
import math
from collections.abc import Callable
from pathlib import Path
from typing import Any

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


# -------------------------------------------------------------------- D_min as text and bracket


def dmin_text(row: pd.Series) -> str:
    """The true D_min as far as the curve decides it.

    '4' when D_min is decided (every smaller D is unreliable), '2-4' when D = 4 is the
    smallest reliable D but a D from 2 up is still undecided, '[2]' when no D is reliable
    yet and D_min is 2 or more, 'none on grid' when every D is unreliable, '-' with no data.
    """
    if pd.notna(row["d_min"]):
        high = int(row["d_min"])
        low = int(row["d_min_low"]) if pd.notna(row["d_min_low"]) else high
        return str(high) if low >= high else f"{low}-{high}"
    if bool(row.get("d_min_above_grid", False)):
        return "none on grid"
    if pd.notna(row["d_min_low"]):
        return f"[{int(row['d_min_low'])}]"
    return "-"


def one_level(table: pd.DataFrame) -> pd.DataFrame:
    """``table`` itself; raises when it holds several factor levels, which a table keyed by
    layout and N would mix (a factor protocol such as dmin_s_gap is shown with ``compare``)."""
    if "factors" in table and table["factors"].nunique() > 1:
        levels = sorted(table["factors"].unique())
        raise ValueError(f"several factor levels {levels}; use compare, which keeps them apart")
    return table


def _by_layout_and_n(
    table: pd.DataFrame, text: Any, layouts: tuple[str, ...] | None
) -> pd.DataFrame:
    """Layouts as rows, N as columns, ``text(row)`` in each cell."""
    table = one_level(table)
    shown = table.assign(text=table.apply(text, axis=1))
    wide = shown.pivot_table(index="layout", columns="n", values="text", aggfunc="first")
    if layouts is not None:
        wide = wide.reindex([layout for layout in layouts if layout in wide.index])
    return wide.fillna("-")


def layout_by_n(table: pd.DataFrame, layouts: tuple[str, ...] | None = None) -> pd.DataFrame:
    """The D_min table: layouts as rows, N as columns, one text entry per curve."""
    return _by_layout_and_n(table, dmin_text, layouts)


def bracket(row: pd.Series) -> tuple[float, float] | None:
    """(low, high) of the true D_min, or None when no D on the grid is decided reliable."""
    if pd.isna(row["d_min"]) or pd.isna(row["d_min_low"]):
        return None
    return float(row["d_min_low"]), float(row["d_min"])


# ------------------------------------------------------------------------------- growth with N


def slope_range(points: list[tuple[int, float, float]]) -> tuple[float, float] | None:
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


def _slope_text(result: tuple[float, float] | None) -> str:
    return "-" if result is None else f"{result[0]:.2f} to {result[1]:.2f}"


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


def growth_table(table: pd.DataFrame) -> pd.DataFrame:
    """Per layout: the slope range, the N values used, and the N values left out and why.

    A flock size is left out when its D_min is not decided. Two cases are told apart: no D
    on the grid is reliable (D_min is above the grid, so the growth is censored there), or
    some D is still open on reliability.
    """
    rows = []
    for layout, part in one_level(table).groupby("layout", sort=False):
        points, rest = _brackets_by_n(part, bracket)
        above = [int(r["n"]) for r in rest if bool(r.get("d_min_above_grid", False))]
        open_ = [int(r["n"]) for r in rest if not bool(r.get("d_min_above_grid", False))]
        flat = bool(points) and all(p[1] == 1.0 and p[2] == 1.0 for p in points)
        notes = []
        if flat and not above and not open_:
            notes.append("D_min = 1 throughout")
        elif flat:
            notes.append("D_min = 1 where decided")
        if above:
            notes.append("no reliable D on the grid at N = " + " ".join(map(str, above)))
        if open_:
            notes.append("still open on reliability at N = " + " ".join(map(str, open_)))
        if flat:
            slope = "0 (flat, decided sizes only)" if above or open_ else "0 (flat)"
        else:
            slope = _slope_text(slope_range(points))
            if slope == "-":
                notes.append("fewer than two decided flock sizes")
        rows.append(
            {
                "layout": layout,
                "slope_range": slope,
                "n_used": " ".join(str(p[0]) for p in points) or "-",
                "note": "; ".join(notes),
            }
        )
    return pd.DataFrame(rows)


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


# ------------------------------------------------------------------------------------ D_sat


def dsat_bracket(row: pd.Series) -> tuple[float, float] | None:
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


def dsat_text(row: pd.Series) -> str:
    """'5' decided, '5-24' when a larger D may still turn out faster, '[24]' when the curve
    is still improving at the top of the grid, '-' without a reliable D."""
    if pd.isna(row["d_sat"]):
        return "-"
    if bool(row.get("still_improving_at_top", False)):
        return f"[{int(row['d_sat'])}]"
    low, high = dsat_bracket(row) or (row["d_sat"], row["d_sat"])
    return str(int(low)) if low >= high else f"{int(low)}-{int(high)}"


def dsat_by_n(table: pd.DataFrame, layouts: tuple[str, ...] | None = None) -> pd.DataFrame:
    """D_sat as text, layouts as rows and N as columns, like ``layout_by_n``."""
    return _by_layout_and_n(table, dsat_text, layouts)


def dsat_growth(table: pd.DataFrame) -> pd.DataFrame:
    """Per layout: the range of slopes of log2 D_sat against log2 N over the D_sat brackets."""
    rows = []
    for layout, part in one_level(table).groupby("layout", sort=False):
        points, rest = _brackets_by_n(part, dsat_bracket)
        left_out = [int(r["n"]) for r in rest]
        if points and all(p[1] == p[2] == 1.0 for p in points):
            slope = "0 (flat)"
        else:
            slope = _slope_text(slope_range(points))
        rows.append(
            {
                "layout": layout,
                "slope_range": slope,
                "n_used": " ".join(str(p[0]) for p in points) or "-",
                "n_left_out": " ".join(map(str, left_out)) or "-",
            }
        )
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- cost, zones and checks


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


def effort_table(cells: pd.DataFrame, table: pd.DataFrame) -> pd.DataFrame:
    """What dogs beyond D_sat cost, per curve with a D_sat below its largest working D.

    Medians over the successful seeds of each cell (frontier_cells.csv), relative to the
    D_sat cell: finish time, dog time (D x finish ticks) and total dog path (D x path per
    dog). Shown at the smallest reliable working D at or above 2 D_sat, and at the largest
    working D. A finish time ratio near 1 with dog time near D / D_sat is effort spent for
    no gain.
    """
    rows = []
    for _, curve in one_level(table).iterrows():
        if pd.isna(curve["d_sat"]) or pd.isna(curve["d_max"]):
            continue
        sat, top = int(curve["d_sat"]), int(curve["d_max"])
        if top <= sat:
            continue
        factors = str(curve["factors"]) if curve.get("factors") else ""
        key = join_group(str(curve["method"]), str(curve["layout"]), factors, int(curve["n"]))
        medians = _cell_medians(cells, key)
        if sat not in medians:
            continue
        working = [d for d in medians if sat <= d <= top]
        double = next((d for d in sorted(working) if d >= 2 * sat), None)
        row: dict[str, Any] = {
            "layout": curve["layout"],
            "n": int(curve["n"]),
            "d_sat": dsat_text(curve),
            "d_double": double if double is not None else "-",
        }
        for label, d in (("double", double), ("top", top)):
            r = _ratios(medians[d], medians[sat]) if d is not None else {}
            for name in ("time", "dog_time", "path"):
                row[f"{name}_{label}"] = round(r[name], 2) if name in r else "-"
        row["d_top"] = top
        rows.append(row)
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows).sort_values(["layout", "n"], ignore_index=True)


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


def frontier_values(table: pd.DataFrame) -> pd.DataFrame:
    """D_min, D_sat, D_crowd and D_max of every curve as text, for a table across methods."""
    rows = []
    for _, curve in table.iterrows():
        rows.append(
            {
                "method": curve["method"],
                "layout": curve["layout"],
                "n": int(curve["n"]),
                "d_min": dmin_text(curve),
                "d_sat": dsat_text(curve),
                "d_crowd": "-" if pd.isna(curve["d_crowd"]) else int(curve["d_crowd"]),
                "d_max": "-" if pd.isna(curve["d_max"]) else int(curve["d_max"]),
            }
        )
    return pd.DataFrame(rows).sort_values(["method", "layout", "n"], ignore_index=True)


def extent_check(trials: pd.DataFrame, radii: dict[str, dict[str, float]]) -> pd.DataFrame:
    """Per cell: the flock's own size during the trial against the R_f its task was sized
    from.

    sqrt(2) x mean_extent is the radius of a uniform disc with the flock's RMS spread, the
    same measure R_f is (services/calibration.py). Above the calibration edge R_f is
    imposed, so a ratio far from 1 says the imposed size does not match the flock the model
    forms there. The mean runs over the whole trial, so on scattered layouts it also holds
    the spread before the flock is gathered; compact starts give the clean comparison.
    """
    rows = []
    for _, part in trials.groupby(["group_key", "n_shepherds"], sort=True):
        info = split_group(str(part["group_key"].iloc[0]))
        d = part["n_shepherds"].iloc[0]
        radius = radii[info["method"]][str(info["n"])]
        ratio = np.sqrt(2.0) * part["mean_extent"].astype(float) / radius
        rows.append(
            {
                "layout": info["layout"],
                "n": info["n"],
                "d": int(d),
                "r_f": round(radius, 2),
                "extent_over_r_f": round(float(ratio.median()), 2),
            }
        )
    return pd.DataFrame(rows).sort_values(["layout", "n", "d"], ignore_index=True)


# -------------------------------------------------------------------------- comparing runs


def midpoint(row: pd.Series) -> float | None:
    """Geometric middle of the bracket, or D_min_low when only the low end is known."""
    b = bracket(row)
    if b:
        return math.sqrt(b[0] * b[1])
    if pd.notna(row["d_min_low"]):
        return float(row["d_min_low"])
    return None


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


def compare(base: pd.DataFrame, variant: pd.DataFrame) -> pd.DataFrame:
    """The variant beside the base for the same curve: 'base / variant' per layout and N.

    A variant with a factor (the dog start gap) has one curve per level; the level goes in
    the row label.
    """
    keys = ["layout", "n"]
    b = base.assign(text=base.apply(dmin_text, axis=1))[keys + ["text"]]
    v = variant.assign(text=variant.apply(dmin_text, axis=1))[keys + ["factors", "text"]]
    merged = v.merge(b, on=keys, how="left", suffixes=("_variant", "_base"))
    merged["pair"] = merged["text_base"].fillna("-") + " / " + merged["text_variant"]
    merged["row"] = merged["factors"].where(merged["factors"] != "", "")
    merged["col"] = merged["layout"] + " N=" + merged["n"].astype(str)
    out = merged.pivot_table(index="row", columns="col", values="pair", aggfunc="first")
    return out.fillna("-")


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
