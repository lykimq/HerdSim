"""Trial- and cell-level tables that do not depend on curve decisions."""

from __future__ import annotations

import math

import pandas as pd

from . import keys


def reach_by_n(trials: pd.DataFrame) -> pd.DataFrame:
    """Reach of a single dog per layout and flock size: the median, over the one-dog trials,
    of each trial's mean ``coverage`` (the share of the outer half of the flock within the
    reaction radius of the dog). Columns: layout, n, trials, reach."""
    one = trials[trials["n_shepherds"] == 1]
    grouped = one.groupby(["initial_layout", "n_sheep"])["mean_coverage"]
    table = grouped.agg(trials="size", reach="median").reset_index()
    return table.rename(columns={"initial_layout": "layout", "n_sheep": "n"})


def nested_deadlines(longer: pd.DataFrame, shorter: pd.DataFrame) -> dict[str, float]:
    """Compare two runs that differ only in deadline, matched on trial_key."""
    pair = longer.merge(shorter, on="trial_key", suffixes=("_long", "_short"))
    within = pair["success_long"].astype(bool) & (
        pair["finish_seconds_long"] <= pair["time_limit_seconds_short"]
    )
    both = pair["success_long"].astype(bool) & pair["success_short"].astype(bool)
    same_finish = (pair["finish_seconds_long"] - pair["finish_seconds_short"]).abs() < 1e-9
    return {
        "shared_trials": int(len(pair)),
        "outcome_as_cut_long_trial": float((within == pair["success_short"].astype(bool)).mean()),
        "both_succeed": int(both.sum()),
        "same_finish_when_both_succeed": float(same_finish[both].mean())
        if both.any()
        else math.nan,
    }


def _is_curve(group_key: str, layout: str, n: int) -> bool:
    group = keys.split_group(group_key)
    return group["layout"] == layout and group["n"] == n


def curve_across(cells: dict[str, pd.DataFrame], layout: str, n: int) -> pd.DataFrame:
    """One layout-and-N curve from several folders, side by side per D."""
    rows = []
    for name, frame in cells.items():
        part = frame[[_is_curve(key, layout, n) for key in frame["group_key"].astype(str)]]
        for _, cell in part.sort_values(["group_key", "n_shepherds"]).iterrows():
            rows.append(
                {
                    "folder": name,
                    "group": cell["group_key"],
                    "d": int(cell["n_shepherds"]),
                    "successes": f"{int(cell['n_success'])}/{int(cell['n_seeds'])}",
                    "rate": round(float(cell["success_rate"]), 2),
                    "reliability": cell["reliability"],
                    "median_finish_s": cell["median_finish_seconds"],
                }
            )
    return pd.DataFrame(rows)
