"""Scenario contracts: placement shapes, success rules, and bounds."""

from __future__ import annotations

import numpy as np
import pytest

from scenarios.registry import scenario_registry
from tests.backend.helpers import make_state


REQUIRED_SCENARIOS = {
    "drive_to_goal",
    "containment",
    "obstacle_course",
    "split_flock",
    "narrow_gate",
    "wide_field",
}


def test_all_expected_scenarios_registered():
    assert REQUIRED_SCENARIOS <= set(scenario_registry.names())


@pytest.mark.parametrize("scenario_id", sorted(REQUIRED_SCENARIOS))
def test_initial_positions_match_agent_counts(scenario_id):
    scen = scenario_registry.get(scenario_id)
    config = dict(scen.default_config)
    config.setdefault("n_sheep", 10)
    config.setdefault("n_shepherds", 1)
    n_sheep = int(config["n_sheep"])
    n_dogs = int(config["n_shepherds"])
    rng = np.random.default_rng(7)
    sheep, dogs = scen.initial_positions(config, rng)
    assert sheep.shape == (n_sheep, 2)
    assert dogs.shape == (n_dogs, 2)
    assert scen.max_ticks(config) > 0


@pytest.mark.parametrize("scenario_id", sorted(REQUIRED_SCENARIOS))
def test_create_world_returns_finite_bounds(scenario_id):
    scen = scenario_registry.get(scenario_id)
    world = scen.create_world(dict(scen.default_config))
    assert world.width > 0
    assert world.height > 0


def test_drive_to_goal_success_when_all_sheep_in_goal():
    scen = scenario_registry.get("drive_to_goal")
    config = {"goal_center": [15.0, 15.0], "goal_radius": 20.0, "n_sheep": 5}
    world = scen.create_world(config)
    state = make_state(
        np.tile(world.goal.center, (5, 1)),
        [[50.0, 50.0]],
        world=world,
        seed=1,
        tick=10,
    )
    assert scen.is_success(state, config)


def test_containment_starts_mostly_inside_pen():
    scen = scenario_registry.get("containment")
    config = {"n_sheep": 20, "n_shepherds": 3, "pen_radius": 35.0}
    world = scen.create_world(config)
    sheep, dogs = scen.initial_positions(config, np.random.default_rng(2))
    assert sheep.shape == (20, 2)
    assert dogs.shape == (3, 2)
    assert world.goal is not None
    assert float(np.mean(world.goal.contains(sheep))) > 0.5


def test_obstacle_course_resolves_agents_out_of_obstacles():
    scen = scenario_registry.get("obstacle_course")
    world = scen.create_world({})
    assert len(world.obstacles) >= 2
    resolved = world.resolve_obstacles(np.array([[60.0, 20.0], [10.0, 10.0]]))
    assert not ((55.0 < resolved[0, 0] < 65.0) and (0.0 <= resolved[0, 1] <= 55.0))
