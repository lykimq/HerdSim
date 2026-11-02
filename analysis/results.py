"""Read a finished results folder and the run log."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


def read_table(path: Path) -> pd.DataFrame:
    """A generated CSV: the first line is the AUTO-GENERATED notice."""
    return pd.read_csv(path, skiprows=1, low_memory=False)


def read_trials(folder: Path) -> pd.DataFrame:
    csv = folder / "trials.csv"
    csv_gz = folder / "trials.csv.gz"
    if csv.exists():
        return read_table(csv)
    return read_table(csv_gz if csv_gz.exists() else csv)


def read_cells(folder: Path) -> pd.DataFrame:
    return read_table(folder / "frontier_cells.csv")


def read_groups(folder: Path) -> pd.DataFrame:
    return read_table(folder / "frontier_groups.csv")


def flock_radii(folder: Path) -> dict[str, dict[str, float]]:
    """Calibrated R_f per method, keyed by N as text."""
    return json.loads((folder / "calibration.json").read_text())["flock_radius"]


def last_queue_entries(queue_log: Path) -> dict[str, dict[str, Any]]:
    """The last queue_log line of each protocol; empty when there is no log."""
    if not queue_log.exists():
        return {}
    entries = [json.loads(line) for line in queue_log.read_text().splitlines() if line.strip()]
    return {entry["protocol"]: entry for entry in entries}


def _folder_status(results_root: Path, protocol: str) -> dict[str, Any] | None:
    """The folder's status.json, or None when it has none."""
    path = results_root / protocol / "status.json"
    return json.loads(path.read_text()) if path.exists() else None


def resumed_protocols(queue_log: Path, results_root: Path) -> list[str]:
    """Protocols whose folder holds more trials than their queue line recorded."""
    resumed = []
    for protocol, entry in last_queue_entries(queue_log).items():
        status = _folder_status(results_root, protocol)
        if status is not None and status["trials_done"] > entry["trials"]:
            resumed.append(protocol)
    return resumed


def run_record(queue_log: Path, results_root: Path | None = None) -> pd.DataFrame:
    """The table of runs: the last queue_log entry of each protocol.

    With ``results_root``, the counts come from each folder's status.json where it exists,
    so a folder resumed outside the queue (a top-up run) shows its current trials and
    cells; the finish time and hours stay those of the queue run.
    """
    last = last_queue_entries(queue_log)
    if not last:
        return pd.DataFrame()
    current = {
        "trials": "trials_done",
        "cells": "cells",
        "cells_needing_seeds": "cells_needing_seeds",
        "cells_at_max_seeds_undecided": "cells_at_max_seeds_undecided",
        "trial_errors": "trial_errors",
    }
    for protocol, entry in last.items():
        found = _folder_status(results_root, protocol) if results_root else None
        if found is not None:
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
