"""Short real trials for every method and layout, checked on every tick."""

from __future__ import annotations

from typing import Any

import numpy as np
import pytest

from sim.core.simulation_runner import run_trial
from sim.core.simulation_state import SimulationState
from tests.helpers import config_for

SPEED_SLACK = 1e-9

CASES: list[tuple[str, dict[str, Any]]] = [
    ("strombom_multi", {}),
    ("strombom_multi", {"d": 24}),
    ("strombom_multi", {"params": {"n_neighbors": 7}, "d": 6}),
    ("strombom_multi", {"layout": "wide"}),
    ("strombom_multi", {"layout": "split", "n": 60}),
    ("strombom_multi", {"layout": "outlier_rich", "n": 60}),
    ("fat", {}),
    ("fat", {"layout": "wide", "d": 6}),
    ("kubo", {}),
    ("kubo", {"d": 6}),
]


def _checker(config: dict[str, Any]):
    """Per-tick checks: finite, N constant, speeds capped, dog steps bounded.

    A dog moves at most its speed cap per tick. Nothing bounds where agents may go: there is
    no boundary.
    """
    n = int(config["n_sheep"])
    kubo = config["sheep_model"] == "kubo"
    sheep_cap = config["sheep_speed_max"] if kubo else config["sheep_speed"]
    dog_cap = config["dog_speed_max"] if kubo else config["shepherd_speed"]
    dt = float(config["dt"])
    previous: dict[str, np.ndarray] = {}

    def check(state: SimulationState) -> None:
        for arr in (
            state.sheep_positions,
            state.sheep_velocities,
            state.shepherd_positions,
            state.shepherd_velocities,
        ):
            assert np.all(np.isfinite(arr))
        assert state.n_sheep == n
        assert np.linalg.norm(state.sheep_velocities, axis=1).max() <= sheep_cap + SPEED_SLACK
        assert np.linalg.norm(state.shepherd_velocities, axis=1).max() <= dog_cap + SPEED_SLACK
        if "dogs" in previous:
            step = np.linalg.norm(state.shepherd_positions - previous["dogs"], axis=1).max()
            assert step <= dog_cap * dt + SPEED_SLACK
        previous["dogs"] = state.shepherd_positions.copy()

    return check


@pytest.mark.parametrize(
    "method, options", CASES, ids=[f"{m}-{i}" for i, (m, _) in enumerate(CASES)]
)
def test_every_tick_respects_the_invariants(method, options):
    options = {"n": 30, "d": 3, **options}
    config = config_for(method, ticks=200, flock_radius=7.0, **options)
    history = run_trial(config, 2026, on_tick=_checker(config)).history
    for column in ("fragmentation", "coverage", "dogs_stopped", "dogs_goal_side"):
        assert history[column].between(0.0, 1.0).all(), column
    assert history["i_dir"].between(0.0, 1.0).all()
    assert history["gcm_in_goal"].isin([0.0, 1.0]).all()
    assert history["shepherd_path"].is_monotonic_increasing


def test_sheep_draws_are_paired_across_dog_counts():
    """Same seed, different D: the sheep move identically until a dog reaches them."""
    far = {"dog_start_gap": 400.0, "field_clearance": 500.0}
    one = config_for("strombom_multi", n=20, d=1, ticks=5, settings=far)
    two = config_for("strombom_multi", n=20, d=4, ticks=5, settings=far)
    seen: dict[int, list[np.ndarray]] = {1: [], 4: []}
    run_trial(one, 7, on_tick=lambda s: seen[1].append(s.sheep_positions.copy()))
    run_trial(two, 7, on_tick=lambda s: seen[4].append(s.sheep_positions.copy()))
    for a, b in zip(seen[1], seen[4]):
        np.testing.assert_array_equal(a, b)
