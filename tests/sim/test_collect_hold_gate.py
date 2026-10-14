"""Few core checks for the collect_hold_gate scenario."""

from __future__ import annotations

import numpy as np
import pytest
from plugins.scenarios.collect_hold_gate import (
    PHASE_COLLECT,
    PHASE_EXIT,
    PHASE_HOLD,
    CollectHoldGateScenario,
    hold_radius_for_n,
)
from plugins.scenarios.registry import scenario_registry

from tests.helpers import make_state


def test_hold_radius_matches_draft_clamp():
    assert hold_radius_for_n(5) == pytest.approx(23.0)
    assert hold_radius_for_n(100) == pytest.approx(25.0)
    assert hold_radius_for_n(400) == pytest.approx(27.0)


def test_scenario_registered_and_world_finite():
    assert scenario_registry.get("collect_hold_gate").id == "collect_hold_gate"
    scenario = scenario_registry.get("collect_hold_gate")
    world = scenario.create_world(
        {
            "n_sheep": 50,
            "world_width": 500.0,
            "world_height": 500.0,
            "hold_center": [250.0, 250.0],
            "gate_half_width": 30.0,
        }
    )
    assert world.width == 500.0
    assert world.height == 500.0
    assert world.goal is not None
    assert world.gate_half_width == 30.0
    assert np.isfinite(world.goal.radius)


def test_initial_positions_at_hold_center_for_large_n():
    scenario = CollectHoldGateScenario()
    cfg = {
        "n_sheep": 400,
        "n_shepherds": 2,
        "world_width": 500.0,
        "world_height": 500.0,
        "hold_center": [250.0, 250.0],
        "initial_layout": "compact",
        "initial_spread": 30.0,
        "hold_radius_scale": 2.5,
        "hold_radius_min": 23.0,
        "hold_radius_max": 27.0,
    }
    sheep, dogs = scenario.initial_positions(cfg, np.random.default_rng(0))
    assert sheep.shape == (400, 2)
    assert dogs.shape == (2, 2)
    assert np.all(sheep[:, 0] >= 1.0) and np.all(sheep[:, 0] <= 499.0)
    assert np.all(sheep[:, 1] >= 1.0) and np.all(sheep[:, 1] <= 499.0)


def test_hold_timer_resets_when_leaving_zone():
    scenario = CollectHoldGateScenario()
    cfg = {
        "hold_ticks": 3,
        "n_sheep": 4,
        "goal_center": [0.0, 0.0],
        "goal_radius": 10.0,
    }
    world = scenario.create_world(
        {
            **cfg,
            "world_width": 100.0,
            "world_height": 100.0,
            "hold_center": [50.0, 50.0],
            "hold_radius_scale": 2.5,
            "hold_radius_min": 10.0,
            "hold_radius_max": 10.0,
            "gate_half_width": 20.0,
        }
    )
    # All sheep inside hold disk.
    inside = np.array([[50.0, 50.0], [51.0, 50.0], [50.0, 51.0], [49.0, 50.0]])
    state = make_state(inside, [[20.0, 50.0]], world=world)
    state.metadata["chg_phase"] = PHASE_COLLECT
    assert not scenario.is_success(state, {"hold_ticks": 3})
    assert state.metadata["chg_phase"] == PHASE_HOLD
    assert state.metadata["chg_hold_count"] == 1

    assert not scenario.is_success(state, {"hold_ticks": 3})
    assert state.metadata["chg_hold_count"] == 2

    # Leave the zone: timer resets to collect.
    outside = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    state = state.copy_with(sheep_positions=outside)
    assert not scenario.is_success(state, {"hold_ticks": 3})
    assert state.metadata["chg_phase"] == PHASE_COLLECT
    assert state.metadata["chg_hold_count"] == 0


def test_success_requires_hold_then_gate_exit():
    scenario = CollectHoldGateScenario()
    world = scenario.create_world(
        {
            "n_sheep": 2,
            "world_width": 100.0,
            "world_height": 100.0,
            "hold_center": [50.0, 50.0],
            "hold_radius_scale": 2.5,
            "hold_radius_min": 20.0,
            "hold_radius_max": 20.0,
            "gate_half_width": 30.0,
        }
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
