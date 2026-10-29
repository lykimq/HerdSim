"""Reading a finished results folder and the run log.

    uv run cli/dmin_tables.py record                  # the run log, read here

Every reader of a results folder goes through these functions, so the file names and the notice
line are known in one place. They read:

- the tables a run writes as CSV (trials.csv, frontier_cells.csv, frontier_groups.csv), skipping
  the AUTO-GENERATED notice on their first line
- the calibrated flock radii in calibration.json
- the queue log results/queue_log.jsonl, one entry per finished protocol, with each folder's
  status.json for the current counts
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

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


def run_record(queue_log: Path, results_root: Path | None = None) -> pd.DataFrame:
    """The table of runs: the last queue_log entry of each protocol.

    With ``results_root``, the counts come from each folder's status.json where it exists,
    so a folder resumed outside the queue (a top-up run) shows its current trials and
    cells; the finish time and hours stay those of the queue run.
    """
    if not queue_log.exists():
        return pd.DataFrame()
    entries = [json.loads(line) for line in queue_log.read_text().splitlines() if line.strip()]
    last: dict[str, dict[str, Any]] = {}
    for entry in entries:
        last[entry["protocol"]] = entry
    current = {
        "trials": "trials_done",
        "cells": "cells",
        "cells_needing_seeds": "cells_needing_seeds",
        "cells_at_max_seeds_undecided": "cells_at_max_seeds_undecided",
        "trial_errors": "trial_errors",
    }
    for protocol, entry in last.items():
        status = results_root / protocol / "status.json" if results_root else None
        if status is not None and status.exists():
            found = json.loads(status.read_text())
            last[protocol] = {**entry, **{k: found[v] for k, v in current.items() if v in found}}
    cols = [
        "protocol",
        "finished",
        "trials",
        "cells",
        "cells_needing_seeds",
        "cells_at_max_seeds_undecided",
        "trial_errors",
        "hours",
        "workers",
        "outcome",
    ]
    return pd.DataFrame([{c: e.get(c, "") for c in cols} for e in last.values()])
