"""Stress: larger flocks / longer budgets (excluded from default suite)."""

from __future__ import annotations

import pytest

from tests.backend.helpers import run_trial


@pytest.mark.stress
def test_strombom_larger_flock_terminates():
    result = run_trial(
        "strombom",
        seed=2,
        num_sheep=80,
        num_shepherds=1,
        config_overrides={"max_ticks": 800},
    )
    assert result.total_ticks <= 800
    assert result.final_state.n_sheep == 80


@pytest.mark.stress
def test_kubo_paper_seed1_runs_to_budget():
    """Full paper Kubo seed 1 historically times out; assert clean termination."""
    result = run_trial("kubo", seed=1, preset="paper")
    assert result.total_ticks == result.final_state.tick
    assert result.total_ticks >= 1


@pytest.mark.stress
def test_strombom_obstacle_course_survives():
    result = run_trial(
        "strombom",
        "obstacle_course",
        seed=1,
        preset="scenario",
        config_overrides={"max_ticks": 400},
    )
    assert result.total_ticks <= 400
