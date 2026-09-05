"""Scenario registry and behaviour tests."""

from __future__ import annotations

import numpy as np

from core.simulation_state import SimulationState
from scenarios.containment import ContainmentScenario
from scenarios.drive_to_goal import DriveToGoalScenario
from scenarios.obstacle_course import ObstacleCourseScenario
from scenarios.registry import scenario_registry


def test_scenarios_registered():
    names = set(scenario_registry.names())
    assert {"drive_to_goal", "containment", "obstacle_course"} <= names


def test_drive_to_goal_success():
    scen = DriveToGoalScenario()
    config = {"goal_center": [15.0, 15.0], "goal_radius": 20.0, "n_sheep": 5}
    world = scen.create_world(config)
    rng = np.random.default_rng(1)
    sheep = np.tile(world.goal.center, (5, 1))
    state = SimulationState(
        tick=10,
        sheep_positions=sheep,
        sheep_velocities=np.zeros_like(sheep),
        shepherd_positions=np.array([[50.0, 50.0]]),
        shepherd_velocities=np.zeros((1, 2)),
        world=world,
        rng=rng,
    )
    assert scen.is_success(state, config)


def test_containment_initial_inside_pen():
    scen = ContainmentScenario()
    config = {"n_sheep": 20, "n_shepherds": 3, "pen_radius": 35.0}
    world = scen.create_world(config)
    rng = np.random.default_rng(2)
    sheep, dogs = scen.initial_positions(config, rng)
    assert sheep.shape == (20, 2)
    assert dogs.shape == (3, 2)
    assert world.goal is not None
    assert float(np.mean(world.goal.contains(sheep))) > 0.5


def test_obstacle_course_has_obstacles():
    scen = ObstacleCourseScenario()
    world = scen.create_world({})
    assert len(world.obstacles) >= 2
    resolved = world.resolve_obstacles(np.array([[60.0, 20.0], [10.0, 10.0]]))
    # First point starts inside an obstacle column and should be pushed out.
    assert not (
        (55.0 < resolved[0, 0] < 65.0) and (0.0 <= resolved[0, 1] <= 55.0)
    )
