"""Good-path / strengthen: known-good configs and reproducibility."""

from __future__ import annotations

import numpy as np

from tests.backend.helpers import build_runner, run_trial, snapshot_positions


def test_strombom_paper_seed1_reaches_goal():
    """Regression: paper Strombom on drive_to_goal seed 1 succeeds quickly."""
    result = run_trial("strombom", seed=1, preset="paper")
    assert result.success is True
    assert result.total_ticks < 500


def test_strombom_seed_determinism():
    a = snapshot_positions(
        build_runner("strombom", seed=99, num_sheep=12, num_shepherds=1),
        ticks=5,
    )
    b = snapshot_positions(
        build_runner("strombom", seed=99, num_sheep=12, num_shepherds=1),
        ticks=5,
    )
    for (s1, d1), (s2, d2) in zip(a, b, strict=True):
        assert np.allclose(s1, s2)
        assert np.allclose(d1, d2)


def test_kubo_seed_determinism():
    a = snapshot_positions(
        build_runner("kubo", seed=99, num_sheep=12, num_shepherds=3),
        ticks=5,
    )
    b = snapshot_positions(
        build_runner("kubo", seed=99, num_sheep=12, num_shepherds=3),
        ticks=5,
    )
    for (s1, d1), (s2, d2) in zip(a, b, strict=True):
        assert np.allclose(s1, s2)
        assert np.allclose(d1, d2)


def test_kubo_short_run_terminates_cleanly():
    """Strengthen: Kubo completes without crash under a tight tick budget."""
    result = run_trial(
        "kubo",
        seed=1,
        preset="paper",
        num_sheep=10,
        num_shepherds=2,
        config_overrides={"max_ticks": 40},
    )
    assert result.total_ticks == 40
    assert result.final_state.n_sheep == 10
    assert result.final_state.n_shepherds == 2


def test_flocking_dog_seed_determinism():
    a = snapshot_positions(
        build_runner("flocking_dog", seed=99, num_sheep=12, num_shepherds=1),
        ticks=5,
    )
    b = snapshot_positions(
        build_runner("flocking_dog", seed=99, num_sheep=12, num_shepherds=1),
        ticks=5,
    )
    for (s1, d1), (s2, d2) in zip(a, b, strict=True):
        assert np.allclose(s1, s2)
        assert np.allclose(d1, d2)


def test_flocking_dog_short_run_terminates_cleanly():
    result = run_trial(
        "flocking_dog",
        seed=1,
        preset="paper",
        num_sheep=10,
        num_shepherds=1,
        config_overrides={"max_ticks": 40},
    )
    assert result.total_ticks == 40
    assert result.final_state.n_sheep == 10
    assert result.final_state.n_shepherds == 1
