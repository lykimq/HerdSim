"""Trial- and cell-level tables that do not depend on curve decisions."""

from __future__ import annotations

import math

import pandas as pd


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


def curve_across(cells: dict[str, pd.DataFrame], layout: str, n: int) -> pd.DataFrame:
    """One layout-and-N curve from several folders, side by side per D."""
    rows = []
    for name, frame in cells.items():
        keys = frame["group_key"].astype(str)
        part = frame[keys.str.contains(f"|{layout}|", regex=False) & keys.str.endswith(f"|N={n}")]
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
