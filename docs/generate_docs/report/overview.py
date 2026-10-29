"""The overview tables: every run in one view, a row per protocol, layout and variant and a
column per N, one table per success rule.

    uv run cli/dmin_tables.py overview dmin_m12 dmin_m6 --value d_sat

docs/generate_docs/make_docs.py writes docs/report/summary_results.md from these tables, and the
``overview`` verb of cli/dmin_tables.py prints them.
"""

from __future__ import annotations

from collections.abc import Callable
from functools import cache
from pathlib import Path
from typing import NamedTuple

import pandas as pd

from analysis.curves import groups_table
from analysis.keys import split_factors
from services.protocol import load_protocol, results_folder

from .text import dmin_text, dsat_text, number_or_text, variant_label


class OverviewRun(NamedTuple):
    """One run of an overview: its folder, and the success share and layouts of its protocol."""

    folder: Path
    success_fraction: float
    layouts: tuple[str, ...]


@cache
def overview_run(name: str) -> OverviewRun:
    """The finished run of protocol ``name`` with the success share and layouts it ran with."""
    protocol = load_protocol(name, output=results_folder(name))
    fraction = float(protocol.settings["success_fraction"])
    return OverviewRun(protocol.output, fraction, protocol.layouts)


def overview_cell(row: pd.Series) -> str:
    """D_min, with D_max when it lies below the grid top and D_overcrowd when the curve has
    one: '3', '2-3 (max 6)', '[5] (over 15)', 'none'."""
    text = "none" if bool(row.get("d_min_above_grid", False)) else dmin_text(row)
    notes = []
    if pd.notna(row["d_max"]) and not bool(row["d_max_at_grid_top"]):
        notes.append(f"max {int(row['d_max'])}")
    if pd.notna(row["d_overcrowd"]):
        notes.append(f"over {int(row['d_overcrowd'])}")
    return f"{text} ({', '.join(notes)})" if notes else text


# What an overview cell shows, by the name of the value.
OVERVIEW_CELLS: dict[str, Callable[[pd.Series], str]] = {
    "d_min": overview_cell,
    "d_sat": dsat_text,
}


def _level_order(factors: list[tuple[str, str]]) -> tuple[tuple[str, float | str], ...]:
    """Sort key of a factor level: numbers by value, so 15.0 comes before 100.0."""
    return tuple((name, number_or_text(value)) for name, value in factors)


def n_columns(frame: pd.DataFrame) -> list[str]:
    """The 'N=25' columns of an overview table, in the order of N."""
    return sorted((c for c in frame.columns if c.startswith("N=")), key=lambda c: int(c[2:]))


def overview(
    table: pd.DataFrame,
    success_fraction: float,
    layouts: tuple[str, ...],
    cell: Callable[[pd.Series], str] = overview_cell,
) -> pd.DataFrame:
    """One row per layout and factor level of a run, one column per N ('N=25') holding
    ``cell(curve)``, blank where that N was not run.

    A swept success_fraction is taken out of the label into the share column, so a table per
    share never mixes two rules; otherwise the share is the run's ``success_fraction``. A run
    with several methods is refused: its rows would carry the same labels."""
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
    """N as rows and one column per curve, for runs with many flock sizes (the gather task).
    A column is named by its protocol, and by layout and variant only where they vary."""
    parts = ["protocol"] + [c for c in ("layout", "variant") if rows[c].nunique() > 1]
    labels = rows[parts].apply(lambda r: " ".join(v for v in r if v), axis=1)
    wide = rows[columns].set_axis(labels).T
    wide.index = [c.removeprefix("N=") for c in wide.index]
    return wide.rename_axis("N")


def overview_tables(
    runs: dict[str, OverviewRun], value: str = "d_min", transpose: bool = False
) -> list[tuple[float, pd.DataFrame]]:
    """Several runs in one view, one table per success share (highest first): a row per
    protocol, layout and variant, a column per N that any row has. ``runs`` maps the label
    of each run to it. With ``transpose`` N is the index instead."""
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
