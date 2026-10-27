from __future__ import annotations

import pandas as pd

from analysis.trial_measures import nested_deadlines


def _trials(rows: list[tuple[str, bool, float]], limit: float) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"trial_key": k, "success": ok, "finish_seconds": t, "time_limit_seconds": limit}
            for k, ok, t in rows
        ]
    )


def test_nested_deadlines_finds_a_trial_that_is_not_a_cut_of_the_longer_one():
    longer = _trials([("a", True, 100.0), ("b", True, 300.0), ("c", False, float("nan"))], 400.0)
    cut = _trials(
        [("a", True, 100.0), ("b", False, float("nan")), ("c", False, float("nan"))], 200.0
    )
    assert nested_deadlines(longer, cut)["outcome_as_cut_long_trial"] == 1.0
    # "b" finished at 300 s, after the 200 s limit, so it cannot succeed at the shorter one.
    broken = _trials([("a", True, 100.0), ("b", True, 150.0), ("c", False, float("nan"))], 200.0)
    result = nested_deadlines(longer, broken)
    assert result["outcome_as_cut_long_trial"] < 1.0
    assert result["same_finish_when_both_succeed"] == 0.5
