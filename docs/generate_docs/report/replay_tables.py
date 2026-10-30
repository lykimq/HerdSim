"""Summaries of the replay CSVs in results/diagnostics/, written by cli/diagnostics/*.py.

The replay tools call these to print their summary and docs/generate_docs/make_docs.py calls them
to write the same tables from the stored CSVs, so each summary has one definition.
"""

from __future__ import annotations

import pandas as pd

# Decimals of the shares and seconds printed in the summaries.
SUMMARY_DECIMALS_SPLIT = 2
SUMMARY_DECIMALS_WALK = 1


def split_summary(table: pd.DataFrame) -> pd.DataFrame:
    """Per deadline, N, D and version: the share of successful seeds, the median finish time of
    the successful ones, and the mean share of dogs standing still."""
    return (
        table.groupby(["deadline", "n", "d", "version"], sort=True)
        .agg(
            success=("success", "mean"),
            median_finish=("finish_seconds", "median"),
            stopped=("dogs_stopped", "mean"),
        )
        .round(SUMMARY_DECIMALS_SPLIT)
        .reset_index()
    )


def walk_summary(table: pd.DataFrame, by: list[str]) -> pd.DataFrame:
    """Medians per group over the replays whose dogs cleared r_s."""
    cleared = table.dropna(subset=["walk"]).assign(
        goal_needed=lambda t: t["walk"] / 2 + t["farthest"]
    )
    out = cleared.groupby(by)[["walk", "seconds", "farthest", "goal_needed"]].median()
    out.insert(0, "cleared", cleared.groupby(by).size())
    out.insert(0, "replays", table.groupby(by).size())
    return out.round(SUMMARY_DECIMALS_WALK).reset_index()
