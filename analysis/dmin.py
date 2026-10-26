"""Counterfactual deadline and arrival threshold re-analysis.

Re-evaluates existing simulation trials under counterfactual conditions without
re-running the model:
- Counterfactual deadlines: Relabels trials under tighter deadline multiples.
- Partial arrival thresholds: Relabels success based on the timestamp when at least
  X% of the flock first entered the goal area.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

import numpy as np
import pandas as pd

from .frontier import Rules, frontier

DMIN_COLUMNS = ("d_min", "d_min_low", "d_max", "d_best", "d_sat")


def deadline_seconds(
    trials: pd.DataFrame, multiple: float, speed: Mapping[str, float]
) -> pd.Series:
    """Calculates model-second deadlines as ``multiple * drive_distance / sheep_speed``."""
    top = trials["method"].map(speed)
    if top.isna().any():
        raise ValueError(f"no sheep speed for methods {sorted(set(trials['method'][top.isna()]))}")
    return multiple * trials["drive_distance"] / top


def at_deadline(trials: pd.DataFrame, multiple: float, speed: Mapping[str, float]) -> pd.DataFrame:
    """Relabels trial outcomes under a tighter deadline multiple of drive time.

    Raises ValueError if requested deadline is looser than the trial's time limit.
    """
    deadline = deadline_seconds(trials, multiple, speed)
    ran = trials["time_limit_seconds"].astype(float)
    if (ran < deadline - 1e-9).any():
        raise ValueError(
            f"a deadline of {multiple:g} drive times is looser than the one these trials ran with"
        )
    out = trials.copy()
    seconds = out["finish_seconds"].astype(float)
    kept = out["success"].astype(bool) & (seconds <= deadline + 1e-9)
    out["success"] = kept
    for column in ("finish_ticks", "finish_seconds"):
        out[column] = out[column].where(kept, np.nan)
    return out


def dmin_table(
    trials: pd.DataFrame,
    rules: Rules,
    multiples: Sequence[float],
    speed: Mapping[str, float],
) -> pd.DataFrame:
    """Evaluates frontier boundaries across multiple counterfactual deadlines."""
    rows = []
    for multiple in multiples:
        front = frontier(at_deadline(trials, multiple, speed), rules)
        open_cells = (
            front.cells.assign(open=front.cells["reliability"] == "undecided")
            .groupby("group_key")["open"]
            .sum()
        )
        part = front.groups[["group_key", *DMIN_COLUMNS]].copy()
        part.insert(1, "deadline_multiple", multiple)
        part["cells_undecided"] = part["group_key"].map(open_cells).astype(int)
        rows.append(part)
    return pd.concat(rows, ignore_index=True)


def at_arrival(trials: pd.DataFrame, pct: int) -> pd.DataFrame:
    """Relabels trials with success defined as at least ``pct``% of the flock reaching the goal."""
    seconds = trials[f"seconds_to_{pct}pct_in_goal"].astype(float)
    limit = trials["time_limit_seconds"].astype(float)
    ok = seconds.notna() & (seconds <= limit + 1e-9)
    out = trials.copy()
    out["success"] = ok
    out["finish_seconds"] = seconds.where(ok)
    out["finish_ticks"] = (seconds / trials["dt"].astype(float)).where(ok)
    return out


def arrival_groups(trials: pd.DataFrame, rules: Rules, pct: int) -> pd.DataFrame:
    """Computes frontier metrics where success is defined as ``pct``% goal arrival."""
    front = frontier(at_arrival(trials, pct), rules)
    return front.groups[["group_key", *DMIN_COLUMNS, "d_min_above_grid"]].copy()
