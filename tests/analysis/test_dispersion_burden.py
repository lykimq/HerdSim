"""Unit tests for dispersion burden and failure regime analysis."""

import pandas as pd
import pytest

from analysis.dispersion_burden import analyze_failure_regimes, compute_dispersion_burdens


def test_analyze_failure_regimes_synthetic():
    df = pd.DataFrame({
        "success": [True, False, False, False],
        "final_gcm_goal": [5.0, 15.0, 80.0, 120.0],
        "goal_radius": [10.0, 10.0, 10.0, 10.0],
    })
    stats = analyze_failure_regimes(df)
    assert stats["total_failed"] == 3
    # final_gcm_goal <= 20.0 (15.0) -> boundary
    assert stats["boundary"] == 1
    # final_gcm_goal > 20.0 (80.0, 120.0) -> structural
    assert stats["structural"] == 2
    assert stats["pct_structural"] == pytest.approx(66.666666, rel=1e-3)


def test_compute_dispersion_burdens_synthetic():
    df = pd.DataFrame({
        "initial_layout": ["compact", "compact", "wide"],
        "n_sheep": [25, 25, 100],
        "min_extent": [3.0, 4.0, 6.0],
        "success": [True, True, False],
    })
    res = compute_dispersion_burdens(df)
    assert len(res) == 2
    compact_row = res[res["layout"] == "compact"].iloc[0]
    assert compact_row["s0"] == pytest.approx(3.5)
    assert compact_row["dispersion_burden"] == pytest.approx(3.5 * 25)
    assert compact_row["overall_sr"] == pytest.approx(1.0)
