"""Short real trials: every-tick physics bounds, and sheep draws paired across dog counts."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import numpy as np
import pytest

from sim.core.simulation_runner import run_trial
from sim.core.simulation_state import SimulationState
from tests.helpers import config_for

METHOD = "strombom_multi"
SEED = 2026
FLOCK_RADIUS = 7.0
TICKS = 200
SPEED_SLACK = 1e-9  # floating-point room on speed caps

# Overrides on top of n=30, d=3. Covers dog count, neighbour rule, and every start layout.
CASES: list[dict[str, Any]] = [
    {},
    {"d": 24},
    {"params": {"n_neighbors": 7}, "d": 6},
    {"layout": "wide"},
    {"layout": "split", "n": 60},
    {"layout": "outlier_rich", "n": 60},
]


# --- helpers -----------------------------------------------------------------


def tick_checker(config: dict[str, Any]) -> Callable[[SimulationState], None]:
    """Finite values, fixed N, speed caps, and dog steps within the speed limit."""
    n = int(config["n_sheep"])
    sheep_cap = config["sheep_speed"]
    dog_cap = config["shepherd_speed"]
    dt = float(config["dt"])
    previous_dogs: np.ndarray | None = None

    def check(state: SimulationState) -> None:
        nonlocal previous_dogs
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
        if previous_dogs is not None:
            step = np.linalg.norm(state.shepherd_positions - previous_dogs, axis=1).max()
            assert step <= dog_cap * dt + SPEED_SLACK
        previous_dogs = state.shepherd_positions.copy()

    return check


def case_id(options: dict[str, Any]) -> str:
    if not options:
        return "default"
    return "-".join(f"{key}={value}" for key, value in options.items())


# --- every-tick bounds -------------------------------------------------------


@pytest.mark.parametrize("options", CASES, ids=case_id)
def test_every_tick_respects_the_invariants(options: dict[str, Any]) -> None:
    cell: dict[str, Any] = {"n": 30, "d": 3, **options}
    config = config_for(METHOD, ticks=TICKS, flock_radius=FLOCK_RADIUS, **cell)
    history = run_trial(config, SEED, on_tick=tick_checker(config)).history

    for column in ("fragmentation", "coverage", "dogs_stopped", "dogs_goal_side"):
        assert history[column].between(0.0, 1.0).all(), column
    assert history["i_dir"].between(0.0, 1.0).all()
    assert history["gcm_in_goal"].isin([0.0, 1.0]).all()
    assert history["shepherd_path"].is_monotonic_increasing


# --- sheep RNG pairing -------------------------------------------------------


def test_sheep_draws_are_paired_across_dog_counts() -> None:
    """Same seed, different D: the sheep move identically until a dog reaches them."""
    far = {"dog_start_gap": 400.0, "field_clearance": 500.0}
    one = config_for(METHOD, n=20, d=1, ticks=5, settings=far)
    four = config_for(METHOD, n=20, d=4, ticks=5, settings=far)
    seen: dict[int, list[np.ndarray]] = {1: [], 4: []}

    run_trial(one, 7, on_tick=lambda state: seen[1].append(state.sheep_positions.copy()))
    run_trial(four, 7, on_tick=lambda state: seen[4].append(state.sheep_positions.copy()))

    for a, b in zip(seen[1], seen[4], strict=True):
        np.testing.assert_array_equal(a, b)
