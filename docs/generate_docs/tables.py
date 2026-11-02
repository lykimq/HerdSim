"""DataFrame layouts for cli/dmin_tables.py and overview tables."""

from __future__ import annotations

import math
from collections.abc import Callable
from functools import cache
from pathlib import Path
from typing import Any, NamedTuple

import pandas as pd

from analysis.curves import (
    bracket,
    dsat_bracket,
    effort,
    groups_table,
    growth,
    one_level,
    upper_end,
)
from analysis.herdability import paper_nstar
from analysis.keys import join_group, split_factors
from docs.generate_docs.format import (
    dmin_text,
    dsat_text,
    int_or_dash,
    number_or_text,
    numbers_text,
    slope_text,
    variant_label,
)
from services.protocol import load_protocol, results_folder

# ------------------------------------------------------------------------- helpers


def _with_text(table: pd.DataFrame, text: Callable[[pd.Series], str]) -> pd.DataFrame:
    """Add a ``text`` column from ``text(row)``."""
    return table.assign(text=table.apply(text, axis=1))


def _by_layout_and_n(
    table: pd.DataFrame, text: Callable[[pd.Series], str], layouts: tuple[str, ...] | None
) -> pd.DataFrame:
    """Pivot: layouts as rows, N as columns, ``text(row)`` in each cell."""
    shown = _with_text(one_level(table), text)
    wide = shown.pivot_table(index="layout", columns="n", values="text", aggfunc="first")
    kept = [layout for layout in layouts or () if layout in wide.index]
    if kept:  # keep task-specific layouts (e.g. gather task uniform) in protocol order
        wide = wide.reindex(kept)
    return wide.fillna("-")


# ------------------------------------------------------------------------- D_min and D_sat


def layout_by_n(table: pd.DataFrame, layouts: tuple[str, ...] | None = None) -> pd.DataFrame:
    """D_min table: layout rows, N columns."""
    return _by_layout_and_n(table, dmin_text, layouts)


def dsat_by_n(table: pd.DataFrame, layouts: tuple[str, ...] | None = None) -> pd.DataFrame:
    """D_sat table in the same shape as ``layout_by_n``."""
    return _by_layout_and_n(table, dsat_text, layouts)


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


def dsat_growth(table: pd.DataFrame) -> pd.DataFrame:
    """Per layout: slope range of log2 D_sat vs log2 N over D_sat brackets."""
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
    """Cost of dogs beyond D_sat, relative to the D_sat cell (see analysis.curves.effort)."""
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
    """Upper-end counts plus rows with D_max below the top, D_crowd, or D_overcrowd."""
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
    """D_min, D_sat, D_crowd and D_max of every curve as text."""
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
    """Side-by-side D_min as 'base / variant' per layout and N."""
    keys = ["layout", "n"]
    b = _with_text(base, dmin_text)[keys + ["text"]]
    v = _with_text(variant, dmin_text)[keys + ["factors", "text"]]
    merged = v.merge(b, on=keys, how="left", suffixes=("_variant", "_base"))
    merged["pair"] = merged["text_base"].fillna("-") + " / " + merged["text_variant"]
    merged["row"] = merged["factors"]
    merged["col"] = merged["layout"] + " N=" + merged["n"].astype(str)
    out = merged.pivot_table(index="row", columns="col", values="pair", aggfunc="first")
    columns = merged.sort_values(keys)["col"].drop_duplicates()  # keep N in numeric order
    return out[list(columns)].fillna("-")


# ---------------------------------------------------------------------- the gather task


def side_by_side(trials: pd.DataFrame, groups: pd.DataFrame, level: float = 0.99) -> pd.DataFrame:
    """Paper N* at ``level`` beside HerdSim D_min, one row per flock size."""
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
    """Failure regimes per run with readable headers."""
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
    """Start spread S0 and burden S0 x N per layout and N."""
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

# --------------------------------------------------------------------- overview

# Main grids at 12, 6 and 3 drive times (strict and 99 percent).
STRICT_MAIN = ("dmin_m12", "dmin_m6", "dmin_m3")
F99_MAIN = ("dmin_f99_m12", "dmin_f99_m6", "dmin_f99_m3")
# Flock sizes of the first study; later runs add 71, 141, 283, 566.
ORIGINAL_NS = (25, 50, 100, 200, 400)


class OverviewRun(NamedTuple):
    """One finished run: folder, success share, and layouts."""

    folder: Path
    success_fraction: float
    layouts: tuple[str, ...]


@cache
def overview_run(name: str) -> OverviewRun:
    """Load protocol ``name`` and return its OverviewRun."""
    protocol = load_protocol(name, output=results_folder(name))
    fraction = float(protocol.settings["success_fraction"])
    return OverviewRun(protocol.output, fraction, protocol.layouts)


def overview_cell(row: pd.Series) -> str:
    """D_min plus optional max / overcrowd notes, e.g. '3', '2-3 (max 6)'."""
    text = "none" if bool(row.get("d_min_above_grid", False)) else dmin_text(row)
    notes = []
    if pd.notna(row["d_max"]) and not bool(row["d_max_at_grid_top"]):
        notes.append(f"max {int(row['d_max'])}")
    if pd.notna(row["d_overcrowd"]):
        notes.append(f"over {int(row['d_overcrowd'])}")
    return f"{text} ({', '.join(notes)})" if notes else text


# Cell formatters keyed by the --value name.
OVERVIEW_CELLS: dict[str, Callable[[pd.Series], str]] = {
    "d_min": overview_cell,
    "d_sat": dsat_text,
}


def _level_order(factors: list[tuple[str, str]]) -> tuple[tuple[str, float | str], ...]:
    """Sort key for factor levels (numbers by value)."""
    return tuple((name, number_or_text(value)) for name, value in factors)


def n_columns(frame: pd.DataFrame) -> list[str]:
    """'N=...' columns sorted by N."""
    return sorted((c for c in frame.columns if c.startswith("N=")), key=lambda c: int(c[2:]))


def overview(
    table: pd.DataFrame,
    success_fraction: float,
    layouts: tuple[str, ...],
    cell: Callable[[pd.Series], str] = overview_cell,
) -> pd.DataFrame:
    """One row per layout and factor level; one N= column per flock size."""
    if table["method"].nunique() > 1:
        raise ValueError(f"several methods {sorted(table['method'].unique())} in one run")
    order = {layout: i for i, layout in enumerate(layouts)}
    rows = []
    for _, part in table.groupby(["layout", "factors"]):
        layout, factors = (str(part[c].iloc[0]) for c in ("layout", "factors"))
        share, kept = success_fraction, []
        for name, value in split_factors(factors):
            if name == "success_fraction":
                share = float(value)
            else:
                kept.append((name, value))
        row = {"share": share, "layout": layout, "variant": variant_label(kept)}
        row |= {f"N={int(c['n'])}": cell(c) for _, c in part.iterrows()}
        rows.append(((order.get(layout, len(order)), layout, _level_order(kept)), row))
    rows.sort(key=lambda pair: pair[0])
    frame = pd.DataFrame([row for _, row in rows])
    return frame[["share", "layout", "variant", *n_columns(frame)]].fillna("")


def _transposed(rows: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """N as rows, one column per curve (for runs with many flock sizes)."""
    parts = ["protocol"] + [c for c in ("layout", "variant") if rows[c].nunique() > 1]
    labels = rows[parts].apply(lambda r: " ".join(v for v in r if v), axis=1)
    wide = rows[columns].set_axis(labels).T
    wide.index = [c.removeprefix("N=") for c in wide.index]
    return wide.rename_axis("N")


def overview_tables(
    runs: dict[str, OverviewRun], value: str = "d_min", transpose: bool = False
) -> list[tuple[float, pd.DataFrame]]:
    """Combine runs into one table per success share (highest first)."""
    cell = OVERVIEW_CELLS[value]
    curves: list[pd.DataFrame] = []
    for name, run in runs.items():
        table = overview(groups_table(run.folder), run.success_fraction, run.layouts, cell)
        curves.append(table.assign(protocol=name))
    every = pd.concat(curves, ignore_index=True).fillna("")
    tables = []
    for share in sorted({float(s) for s in every["share"]}, reverse=True):
        rows = every[every["share"] == share]
        kept = [c for c in n_columns(rows) if (rows[c] != "").any()]
        if transpose:
            tables.append((share, _transposed(rows, kept)))
            continue
        labels = ["protocol", "layout"] + (["variant"] if (rows["variant"] != "").any() else [])
        tables.append((share, rows[labels + kept]))
    return tables
