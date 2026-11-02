"""DataFrame layouts for the tables of docs/generate_docs/page.py."""

from __future__ import annotations

from collections.abc import Callable

import pandas as pd

from analysis.curves import bracket, growth, one_level
from docs.generate_docs.format import dmin_text, numbers_text, slope_text

# Main grids at 12, 6 and 3 drive times (strict and 99 percent).
STRICT_MAIN = ("dmin_m12", "dmin_m6", "dmin_m3")
F99_MAIN = ("dmin_f99_m12", "dmin_f99_m6", "dmin_f99_m3")
# Flock sizes of the first study; the 99 percent grids at 12 and 6 drive times add 71, 141,
# 283 and 566.
ORIGINAL_NS = (25, 50, 100, 200, 400)


def _with_text(table: pd.DataFrame, text: Callable[[pd.Series], str]) -> pd.DataFrame:
    """Add a ``text`` column from ``text(row)``."""
    return table.assign(text=table.apply(text, axis=1))


def layout_by_n(table: pd.DataFrame, layouts: tuple[str, ...] | None = None) -> pd.DataFrame:
    """D_min table: layout rows in ``layouts`` order, N columns."""
    shown = _with_text(one_level(table), dmin_text)
    wide = shown.pivot_table(index="layout", columns="n", values="text", aggfunc="first")
    kept = [layout for layout in layouts or () if layout in wide.index]
    if kept:
        wide = wide.reindex(kept)
    return wide.fillna("-")


def growth_table(table: pd.DataFrame) -> pd.DataFrame:
    """Per layout: slope range, N used, and notes for undecided sizes."""
    rows = []
    for layout, part in one_level(table).groupby("layout", sort=False):
        g = growth(part, bracket)
        open_ = [n for n in g.left_out if n not in g.above_grid]
        notes = []
        if g.flat and not g.left_out:
            notes.append("D_min = 1 throughout")
        elif g.flat:
            notes.append("D_min = 1 where decided")
        if g.above_grid:
            notes.append("no reliable D on the grid at N = " + numbers_text(g.above_grid))
        if open_:
            notes.append("still open on reliability at N = " + numbers_text(open_))
        if g.flat:
            slope = "0 (flat, decided sizes only)" if g.left_out else "0 (flat)"
        else:
            slope = slope_text(g.slope)
            if g.slope is None:
                notes.append("fewer than two decided flock sizes")
        rows.append(
            {
                "layout": layout,
                "slope_range": slope,
                "n_used": numbers_text([p[0] for p in g.points]),
                "note": "; ".join(notes),
            }
        )
    return pd.DataFrame(rows)
