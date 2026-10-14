"""Few core checks for the collect_hold_gate scenario."""

from __future__ import annotations

import numpy as np
import pytest
from methods.strombom.config import STROMBOM_DEFAULTS
from plugins.scenarios import SCENARIOS
from plugins.scenarios.collect_hold_gate import (
    PHASE_COLLECT,
    PHASE_EXIT,
    PHASE_HOLD,
)

from services.layout import load_run_protocol
from services.runner import goal_radius_for_n, task_setup
from tests.helpers import make_state

_, _, _, PHASE8 = load_run_protocol("phase8_size_scout")


def _config(n_sheep: int, n_shepherds: int = 1, **overrides) -> dict:
    """Flat scenario config for one Phase 8 cell, as the runner builds it."""
    setup = task_setup(PHASE8, n_sheep)
    cfg = {
        **{k: v for k, v in setup.items() if not k.startswith("goal_center_")},
        "goal_center": [setup["goal_center_x"], setup["goal_center_y"]],
        "n_sheep": n_sheep,
        "n_shepherds": n_shepherds,
        "initial_layout": "compact",
        "max_ticks": PHASE8["time_limit_t0"],
        "r_a": STROMBOM_DEFAULTS["r_a"],
    }
    cfg.update(overrides)
    return cfg


def test_hold_radius_matches_draft_clamp():
    assert goal_radius_for_n(PHASE8, 5) == pytest.approx(23.0)
    assert goal_radius_for_n(PHASE8, 100) == pytest.approx(25.0)
    assert goal_radius_for_n(PHASE8, 400) == pytest.approx(27.0)


def test_scenario_registered_and_world_finite():
    scenario = SCENARIOS["collect_hold_gate"]
    world = scenario.create_world(_config(50))
    assert world.width == 500.0
    assert world.height == 500.0
    assert world.gate_half_width == 30.0
    assert np.isfinite(world.goal.radius)


def test_initial_positions_at_hold_center_for_large_n():
    scenario = SCENARIOS["collect_hold_gate"]
    sheep, dogs = scenario.initial_positions(_config(400, 2), np.random.default_rng(0))
    assert sheep.shape == (400, 2)
    assert dogs.shape == (2, 2)
    assert np.all(sheep[:, 0] >= 1.0) and np.all(sheep[:, 0] <= 499.0)
    assert np.all(sheep[:, 1] >= 1.0) and np.all(sheep[:, 1] <= 499.0)
    # Dogs start on the side of the flock away from the right-wall gate.
    assert np.all(dogs[:, 0] < 250.0)


def test_hold_timer_resets_when_leaving_zone():
    scenario = SCENARIOS["collect_hold_gate"]
    world = scenario.create_world(
        _config(
            4,
            world_width=100.0,
            world_height=100.0,
            goal_center=[50.0, 50.0],
            goal_radius=10.0,
            gate_half_width=20.0,
        )
    )
    cfg = {"hold_ticks": 3}
    # All sheep inside hold disk.
    inside = np.array([[50.0, 50.0], [51.0, 50.0], [50.0, 51.0], [49.0, 50.0]])
    state = make_state(inside, [[20.0, 50.0]], world=world)
    state.metadata["chg_phase"] = PHASE_COLLECT
    assert not scenario.is_success(state, cfg)
    assert state.metadata["chg_phase"] == PHASE_HOLD
    assert state.metadata["chg_hold_count"] == 1

    assert not scenario.is_success(state, cfg)
    assert state.metadata["chg_hold_count"] == 2

    # Leave the zone: timer resets to collect.
    outside = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    state = state.copy_with(sheep_positions=outside)
    assert not scenario.is_success(state, cfg)
    assert state.metadata["chg_phase"] == PHASE_COLLECT
    assert state.metadata["chg_hold_count"] == 0


def test_success_requires_hold_then_gate_exit():
    scenario = SCENARIOS["collect_hold_gate"]
    world = scenario.create_world(
        _config(
            2,
            world_width=100.0,
            world_height=100.0,
            goal_center=[50.0, 50.0],
            goal_radius=20.0,
            gate_half_width=30.0,
        )
    )
    cfg = {"hold_ticks": 2}
    inside = np.array([[50.0, 50.0], [51.0, 50.0]])
    state = make_state(inside, [[20.0, 50.0]], world=world)
    state.metadata["chg_phase"] = PHASE_COLLECT
    assert not scenario.is_success(state, cfg)
    assert not scenario.is_success(state, cfg)
    assert state.metadata["chg_phase"] == PHASE_EXIT
    assert state.metadata.get("chg_hold_complete") is True

    # Still inside arena: not success yet.
    assert not scenario.is_success(state, cfg)

    # Through the gate (x >= width).
    exited = np.array([[100.0, 50.0], [101.0, 50.0]])
    state = state.copy_with(sheep_positions=exited)
    state.metadata["chg_phase"] = PHASE_EXIT
    state.metadata["chg_hold_complete"] = True
    assert scenario.is_success(state, cfg)
