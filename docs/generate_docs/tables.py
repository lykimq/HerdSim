"""DataFrame layouts for the tables of docs/generate_docs/page.py."""

from __future__ import annotations

from collections.abc import Callable

import pandas as pd

from analysis.curves import bracket, growth
from docs.generate_docs.format import dmin_text, numbers_text, slope_text


def _with_text(table: pd.DataFrame, text: Callable[[pd.Series], str]) -> pd.DataFrame:
    """Add a ``text`` column from ``text(row)``."""
    return table.assign(text=table.apply(text, axis=1))


def layout_by_n(table: pd.DataFrame, layouts: tuple[str, ...] | None = None) -> pd.DataFrame:
    """D_min table: layout rows in ``layouts`` order, N columns."""
    shown = _with_text(table, dmin_text)
    wide = shown.pivot_table(index="layout", columns="n", values="text", aggfunc="first")
    kept = [layout for layout in layouts or () if layout in wide.index]
    if kept:
        wide = wide.reindex(kept)
    return wide.fillna("-")


def reach_table(table: pd.DataFrame, layouts: tuple[str, ...]) -> pd.DataFrame:
    """Reach of one dog: layout rows in ``layouts`` order, N columns."""
    wide = table.pivot_table(index="layout", columns="n", values="reach", aggfunc="first")
    return wide.reindex([layout for layout in layouts if layout in wide.index]).map("{:.2f}".format)


def growth_table(table: pd.DataFrame) -> pd.DataFrame:
    """Per layout: slope range, N used, and notes for undecided sizes."""
    rows = []
    for layout, part in table.groupby("layout", sort=False):
        g = growth(part, bracket)
        undecided = [n for n in g.left_out if n not in g.above_grid]
        notes = []
        if g.flat and not g.left_out:
            notes.append("D_min = 1 throughout")
        elif g.flat:
            notes.append("D_min = 1 where decided")
        if g.above_grid:
            notes.append("no reliable D on the grid at N = " + numbers_text(g.above_grid))
        if undecided:
            notes.append("still undecided on reliability at N = " + numbers_text(undecided))
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
