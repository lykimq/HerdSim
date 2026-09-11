"""Tests for moving-goal environment updates and arena clamping."""

from __future__ import annotations

import numpy as np

from core.agent_attributes import apply_environment_updates
from core.simulation_state import SimulationState
from core.world import GoalZone, World, clamp_goal_center
from tests.backend.helpers import make_state, make_world


def test_clamp_goal_center_keeps_disk_inside_arena():
    center = clamp_goal_center([0.0, 0.0], radius=15.0, width=150.0, height=150.0)
    assert center[0] == 15.0
    assert center[1] == 15.0

    center = clamp_goal_center([149.0, 149.0], radius=15.0, width=150.0, height=150.0)
    assert center[0] == 135.0
    assert center[1] == 135.0


def test_clamp_goal_center_pins_when_radius_too_large():
    center = clamp_goal_center([10.0, 10.0], radius=100.0, width=150.0, height=150.0)
    assert center[0] == 75.0
    assert center[1] == 75.0


def test_moving_goal_does_not_leave_disk_outside_arena():
    world = make_world(goal_center=(15.0, 15.0), goal_radius=15.0)
    # Minimal state: empty agents are fine for environment updates.
    state = make_state(
        np.zeros((1, 2)),
        np.zeros((1, 2)),
        world=world,
        seed=1,
    )
    config = {
        "goal_mode": "moving",
        "goal_velocity": [1.0, 1.0],
    }

    # Drive the goal into the far corner; disk must remain inside.
    for _ in range(500):
        state = apply_environment_updates(state, config)

    goal = state.world.goal
    assert goal is not None
    cx, cy = goal.center
    r = goal.radius
    assert cx >= r - 1e-9
    assert cy >= r - 1e-9
    assert cx <= state.world.width - r + 1e-9
    assert cy <= state.world.height - r + 1e-9
