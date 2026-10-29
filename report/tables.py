"""The tables of cli/dmin_tables.py whose cells are written for the docs: D_min and D_sat as
text by layout and N, their growth, the cost beyond D_sat, the upper end of the curves, runs and
methods side by side, the gather task read two ways, and the failure and spread tables.

Each function takes what analysis/ computed from a finished run and returns a DataFrame;
report.text.markdown prints it. The values themselves (brackets, slopes, fits, zones) are
decided in analysis/, so a change here changes how a table reads, never a result.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from typing import Any

import pandas as pd

from analysis.curves import bracket, dsat_bracket, effort, growth, one_level, upper_end
from analysis.herdability import paper_nstar
from analysis.keys import join_group

from .text import dmin_text, dsat_text, int_or_dash, numbers_text, slope_text

# ------------------------------------------------------------------------- helpers


def _with_text(table: pd.DataFrame, text: Callable[[pd.Series], str]) -> pd.DataFrame:
    """``table`` with a column ``text`` holding ``text(row)``."""
    return table.assign(text=table.apply(text, axis=1))


def _by_layout_and_n(
    table: pd.DataFrame, text: Callable[[pd.Series], str], layouts: tuple[str, ...] | None
) -> pd.DataFrame:
    """Layouts as rows, N as columns, ``text(row)`` in each cell."""
    shown = _with_text(one_level(table), text)
    wide = shown.pivot_table(index="layout", columns="n", values="text", aggfunc="first")
    kept = [layout for layout in layouts or () if layout in wide.index]
    if kept:  # a task with its own layouts (the gather task's uniform) keeps them all
        wide = wide.reindex(kept)
    return wide.fillna("-")


# ------------------------------------------------------------------------- D_min and D_sat


def layout_by_n(table: pd.DataFrame, layouts: tuple[str, ...] | None = None) -> pd.DataFrame:
    """The D_min table: layouts as rows, N as columns, one text entry per curve."""
    return _by_layout_and_n(table, dmin_text, layouts)


def dsat_by_n(table: pd.DataFrame, layouts: tuple[str, ...] | None = None) -> pd.DataFrame:
    """D_sat as text, layouts as rows and N as columns, like ``layout_by_n``."""
    return _by_layout_and_n(table, dsat_text, layouts)


def growth_table(table: pd.DataFrame) -> pd.DataFrame:
    """Per layout: the slope range, the N values used, and the N values left out and why.

    A flock size is left out when its D_min is not decided. Two cases are told apart: no D
    on the grid is reliable (D_min is above the grid, so the growth is censored there), or
    some D is still open on reliability.
    """
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


def dsat_growth(table: pd.DataFrame) -> pd.DataFrame:
    """Per layout: the range of slopes of log2 D_sat against log2 N over the D_sat brackets."""
    rows = []
    for layout, part in one_level(table).groupby("layout", sort=False):
        g = growth(part, dsat_bracket)
        rows.append(
            {
                "layout": layout,
                "slope_range": "0 (flat)" if g.flat else slope_text(g.slope),
                "n_used": numbers_text([p[0] for p in g.points]),
                "n_left_out": numbers_text(g.left_out),
            }
        )
    return pd.DataFrame(rows)


# ------------------------------------------------------------------- cost and upper end


def effort_table(cells: pd.DataFrame, table: pd.DataFrame) -> pd.DataFrame:
    """What dogs beyond D_sat cost (analysis.curves.effort), per curve with a D_sat below its
    largest working D: ratios to the D_sat cell at D_double and at the largest working D."""
    rows = []
    for _, curve in one_level(table).iterrows():
        e = effort(cells, curve)
        if e is None:
            continue
        row: dict[str, Any] = {
            "layout": curve["layout"],
            "n": int(curve["n"]),
            "d_sat": dsat_text(curve),
            "d_double": e.d_double if e.d_double is not None else "-",
        }
        for label, r in (("double", e.double), ("top", e.top)):
            for name in ("time", "dog_time", "path"):
                row[f"{name}_{label}"] = round(r[name], 2) if name in r else "-"
        row["d_top"] = e.d_top
        rows.append(row)
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows).sort_values(["layout", "n"], ignore_index=True)


def upper_values(table: pd.DataFrame, cells: pd.DataFrame) -> tuple[dict[str, int], pd.DataFrame]:
    """The upper end of every curve (analysis.curves.upper_end): its counts, and one row per
    curve whose D_max lies below the grid top or that has a D_crowd or D_overcrowd."""
    counts, flagged, top = upper_end(table, cells)
    rows = []
    for _, curve in flagged.iterrows():
        group = join_group(curve["method"], curve["layout"], curve["factors"], int(curve["n"]))
        rows.append(
            {
                "method": curve["method"],
                "layout": curve["layout"],
                "factors": curve["factors"] or "-",
                "n": int(curve["n"]),
                "d_min": dmin_text(curve),
                "d_max": int_or_dash(curve["d_max"]),
                "grid_top": int(top[group]) if group in top else "-",
                "d_crowd": int_or_dash(curve["d_crowd"]),
                "d_overcrowd": int_or_dash(curve["d_overcrowd"]),
            }
        )
    return counts, pd.DataFrame(rows)


# --------------------------------------------------------------------- comparing runs


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
                "d_crowd": int_or_dash(curve["d_crowd"]),
                "d_max": int_or_dash(curve["d_max"]),
            }
        )
    return pd.DataFrame(rows).sort_values(["method", "layout", "n"], ignore_index=True)


def compare(base: pd.DataFrame, variant: pd.DataFrame) -> pd.DataFrame:
    """The variant beside the base for the same curve: 'base / variant' per layout and N.

    A variant with a factor (the dog start gap) has one curve per level; the level goes in
    the row label.
    """
    keys = ["layout", "n"]
    b = _with_text(base, dmin_text)[keys + ["text"]]
    v = _with_text(variant, dmin_text)[keys + ["factors", "text"]]
    merged = v.merge(b, on=keys, how="left", suffixes=("_variant", "_base"))
    merged["pair"] = merged["text_base"].fillna("-") + " / " + merged["text_variant"]
    merged["row"] = merged["factors"]
    merged["col"] = merged["layout"] + " N=" + merged["n"].astype(str)
    out = merged.pivot_table(index="row", columns="col", values="pair", aggfunc="first")
    return out.fillna("-")


# ---------------------------------------------------------------------- the gather task


def side_by_side(trials: pd.DataFrame, groups: pd.DataFrame, level: float = 0.99) -> pd.DataFrame:
    """Per flock size: the paper's N* at ``level`` and HerdSim's D_min (with its brackets)."""
    paper = paper_nstar(trials, (level,)).set_index("n")
    out = []
    for _, g in groups.sort_values("n").iterrows():
        n = int(g["n"])
        out.append(
            {
                "N (targets)": n,
                "sqrt N": round(math.sqrt(n), 2),
                f"paper N* (mean share >= {level:g})": paper.loc[n, f"nstar_{level:.2f}"],
                "HerdSim D_min": dmin_text(g),
                "best mean share": paper.loc[n, "best_mean_share"],
            }
        )
    return pd.DataFrame(out)


# ------------------------------------------------------------ failures and start spread


def failure_table(failure_df: pd.DataFrame) -> pd.DataFrame:
    """The failure regimes per run (analysis.dispersion_burden) with readable headers."""
    if failure_df.empty:
        return pd.DataFrame()
    return pd.DataFrame(
        {
            "Protocol": failure_df["campaign"],
            "Rule": failure_df["description"],
            "Failed": failure_df["total_failed"],
            "Structural": failure_df["structural"],
            "Boundary": failure_df["boundary"],
            "% Structural": failure_df["pct_structural"].map(lambda v: f"{v:.1f}%"),
        }
    )


def dispersion_table(disp_df: pd.DataFrame) -> pd.DataFrame:
    """The start spread S0 and the burden S0 x N per layout and N, with readable headers."""
    if disp_df.empty:
        return pd.DataFrame()
    return pd.DataFrame(
        {
            "Layout": disp_df["layout"],
            "N": disp_df["n"],
            "S0 (m)": disp_df["s0"].map(lambda v: f"{v:.2f}"),
            "Burden S0 x N": disp_df["dispersion_burden"].map(lambda v: f"{v:.1f}"),
            "Success rate": disp_df["overall_sr"].map(lambda v: f"{v * 100:.1f}%"),
        }
    )
