"""Nested deadlines: a short run should only cut the same long trial short."""

from __future__ import annotations

import math

import pandas as pd

from analysis.trial_measures import nested_deadlines

# Three shared trial keys. Finish times are in seconds; nan means the trial failed.
LONG_LIMIT = 400.0
SHORT_LIMIT = 200.0


def trials(limit: float, outcomes: dict[str, tuple[bool, float]]) -> pd.DataFrame:
    """One run's rows: trial_key -> (success, finish_seconds)."""
    return pd.DataFrame(
        [
            {
                "trial_key": key,
                "success": success,
                "finish_seconds": finish,
                "time_limit_seconds": limit,
            }
            for key, (success, finish) in outcomes.items()
        ]
    )


def test_nested_deadlines_match_when_the_short_run_only_cuts_the_long_one():
    # Long run: a finishes early, b finishes after the short limit, c fails.
    long_run = trials(
        LONG_LIMIT,
        {
            "a": (True, 100.0),
            "b": (True, 300.0),
            "c": (False, math.nan),
        },
    )
    # Short run as a cut of that: a still succeeds, b and c do not.
    short_cut = trials(
        SHORT_LIMIT,
        {
            "a": (True, 100.0),
            "b": (False, math.nan),
            "c": (False, math.nan),
        },
    )
    assert nested_deadlines(long_run, short_cut)["outcome_as_cut_long_trial"] == 1.0

    # Broken short run: b "succeeds" at 150 s, but the long trial of b finished at 300 s,
    # so that success cannot be a cut of the long one.
    short_broken = trials(
        SHORT_LIMIT,
        {
            "a": (True, 100.0),
            "b": (True, 150.0),
            "c": (False, math.nan),
        },
    )
    result = nested_deadlines(long_run, short_broken)
    assert result["outcome_as_cut_long_trial"] < 1.0
    # a and b both succeed in each run; only a has the same finish time.
    assert result["same_finish_when_both_succeed"] == 0.5
