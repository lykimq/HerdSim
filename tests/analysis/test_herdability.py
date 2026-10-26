"""The paper's herdability statistic read from trial rows (analysis/herdability.py)."""

from __future__ import annotations

import pandas as pd

from analysis.herdability import paper_nstar, stable_first


def _trials(shares: dict[tuple[int, int], list[float]]) -> pd.DataFrame:
    rows = [
        {"n_sheep": n, "n_shepherds": d, "final_in_goal_fraction": s}
        for (n, d), values in shares.items()
        for s in values
    ]
    return pd.DataFrame(rows)


def test_nstar_is_the_smallest_team_from_which_every_larger_one_reaches_the_level():
    trials = _trials(
        {
            (100, 8): [0.95, 0.99],  # mean 0.97
            (100, 9): [1.0, 0.98],  # mean 0.99: first to reach 0.99
            (100, 10): [0.97, 0.99],  # mean 0.98: falls back below
            (100, 11): [1.0, 0.99],
            (100, 12): [1.0, 1.0],
        }
    )
    row = paper_nstar(trials, (0.99,)).iloc[0]
    assert row["first_0.99"] == 9 and row["nstar_0.99"] == 11
    assert row["best_mean_share"] == 1.0


def test_a_level_never_reached_at_the_top_has_no_nstar():
    assert stable_first([4, 8, 12], [True, True, False]) == (None, 4)
    assert stable_first([4, 8, 12], [False, False, False]) == (None, None)
