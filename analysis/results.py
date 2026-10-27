"""Reading a finished results folder, and printing a table as Markdown.

A run writes its tables as CSV files whose first line is the AUTO-GENERATED notice, and the
calibrated flock radii as calibration.json (services/store.py). Every reader of a results
folder goes through these functions, so the file names and the notice line are known in
one place.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def read_table(path: Path) -> pd.DataFrame:
    """A generated CSV: the first line is the AUTO-GENERATED notice."""
    return pd.read_csv(path, skiprows=1, low_memory=False)


def read_trials(folder: Path) -> pd.DataFrame:
    return read_table(folder / "trials.csv")


def read_cells(folder: Path) -> pd.DataFrame:
    return read_table(folder / "frontier_cells.csv")


def read_groups(folder: Path) -> pd.DataFrame:
    return read_table(folder / "frontier_groups.csv")


def flock_radii(folder: Path) -> dict[str, dict[str, float]]:
    """Calibrated R_f per method, keyed by N as text."""
    return json.loads((folder / "calibration.json").read_text())["flock_radius"]


def markdown(frame: pd.DataFrame, index: bool = False) -> str:
    """A Markdown table; no extra dependency. A "|" inside a cell is escaped, because a row of
    several factors is labelled "a=1|b=2" and would otherwise split into two cells."""
    if frame.empty:
        return "(no rows)"
    frame = frame.reset_index() if index else frame

    def text(v: object) -> str:
        return "" if isinstance(v, float) and pd.isna(v) else str(v).replace("|", "\\|")

    columns = [text(c) for c in frame.columns]
    lines = ["| " + " | ".join(columns) + " |", "|" + "|".join("---" for _ in columns) + "|"]
    for row in frame.itertuples(index=False):
        lines.append("| " + " | ".join(text(v) for v in row) + " |")
    return "\n".join(lines)
