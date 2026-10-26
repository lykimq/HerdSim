"""Failure regimes and the start spread, on hand-made trial rows."""

from __future__ import annotations

import pandas as pd
import pytest

from analysis.dispersion_burden import analyze_failure_regimes, compute_dispersion_burdens


def test_failed_trials_split_at_two_goal_radii():
    df = pd.DataFrame(
        {
            "success": [True, False, False, False],
            "final_gcm_goal": [5.0, 15.0, 80.0, 120.0],
            "goal_radius": [10.0, 10.0, 10.0, 10.0],
        }
    )
    stats = analyze_failure_regimes(df)
    assert stats["total_failed"] == 3
    assert stats["boundary"] == 1  # 15 is within 2 x 10 of the goal
    assert stats["structural"] == 2
    assert stats["pct_structural"] == pytest.approx(200 / 3)


def test_burden_is_the_start_extent_times_n():
    df = pd.DataFrame(
        {
            "initial_layout": ["compact", "compact", "wide"],
            "n_sheep": [25, 25, 100],
            "max_extent": [3.0, 4.0, 60.0],
            "success": [True, True, False],
        }
    )
    res = compute_dispersion_burdens(df).set_index("layout")
    assert len(res) == 2
    assert res.loc["compact", "s0"] == pytest.approx(3.5)
    assert res.loc["compact", "dispersion_burden"] == pytest.approx(3.5 * 25)
    assert res.loc["compact", "overall_sr"] == pytest.approx(1.0)
    assert res.loc["wide", "dispersion_burden"] == pytest.approx(6000.0)
