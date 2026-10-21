"""D_min as a function of the deadline, read from the trials of one run.

A trial that succeeds at time t also succeeds under every deadline at or above t and fails
under every deadline below it, and a failed trial ran to its own limit. So the trials of a run
made with a loose deadline answer every tighter one: ``at_deadline`` relabels each trial
by whether it finished inside the tighter deadline, and ``dmin_table`` runs the frontier rules
on each relabelled table. The deadline is a multiple of the drive time, the drive length over
the top sheep speed, as in ``time_limit_drive_multiple``.

The seeds of an adaptive run were allocated to decide the run's own deadline. A tighter
deadline read from the same trials has the same paired seeds but no extra ones where its
boundary lies, so its cells may stay undecided; run that deadline as its own protocol when
that matters.
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
    """Deadline of every trial in model seconds: ``multiple`` x drive distance / sheep speed."""
    top = trials["method"].map(speed)
    if top.isna().any():
        raise ValueError(f"no sheep speed for methods {sorted(set(trials['method'][top.isna()]))}")
    return multiple * trials["drive_distance"] / top


def at_deadline(trials: pd.DataFrame, multiple: float, speed: Mapping[str, float]) -> pd.DataFrame:
    """The trials as they would have come out under a deadline of ``multiple`` drive times.

    Raises when a trial ran with a deadline tighter than the one asked for: it stopped
    before that time, so what would have happened later is unknown.
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
    """One row per D curve and deadline: the D values of the frontier rules plus the cells' state.

    Columns: group_key, deadline_multiple, the D values (nullable ints), and
    ``cells_undecided``, the number of cells of the curve whose reliability is still open.
    """
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
    """The trials with success redefined as ``pct`` percent of the flock having reached the goal.

    Uses the first-arrival column ``seconds_to_<pct>pct_in_goal`` (NaN when never reached). A
    trial succeeds when that time is within its own time limit, and its finish time becomes the
    arrival time. First arrival, not held arrival: a sheep may leave again afterwards.
    """
    seconds = trials[f"seconds_to_{pct}pct_in_goal"].astype(float)
    limit = trials["time_limit_seconds"].astype(float)
    ok = seconds.notna() & (seconds <= limit + 1e-9)
    out = trials.copy()
    out["success"] = ok
    out["finish_seconds"] = seconds.where(ok)
    out["finish_ticks"] = (seconds / trials["dt"].astype(float)).where(ok)
    return out


def arrival_groups(trials: pd.DataFrame, rules: Rules, pct: int) -> pd.DataFrame:
    """The frontier's D values per D curve when success means ``pct`` percent arrival."""
    front = frontier(at_arrival(trials, pct), rules)
    return front.groups[["group_key", *DMIN_COLUMNS]].copy()
