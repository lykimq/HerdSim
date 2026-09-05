"""Unit tests for Kubo 2022 force-based algorithm."""

from __future__ import annotations

import numpy as np
import pytest

from algorithms.kubo.algorithm import KuboAlgorithm
from algorithms.kubo.forces import (
    clamp_speed,
    dog_force_components,
    sheep_force_components,
    target_sheep_farthest_from_goal,
)
from algorithms.registry import algorithm_registry
from core.simulation_runner import SimulationRunner
from core.simulation_state import SimulationState
from core.world import GoalZone, World
from metrics.registry import metric_registry
from scenarios.drive_to_goal import DriveToGoalScenario


@pytest.fixture
def kubo_state():
    rng = np.random.default_rng(0)
    world = World(
        width=150.0,
        height=150.0,
        goal=GoalZone(center=np.array([15.0, 15.0]), radius=15.0),
    )
    sheep = np.array([[40.0, 40.0], [45.0, 42.0], [38.0, 50.0], [70.0, 70.0]])
    dogs = np.array([[60.0, 60.0], [65.0, 55.0], [55.0, 65.0]])
    return SimulationState(
        tick=0,
        sheep_positions=sheep,
        sheep_velocities=np.zeros_like(sheep),
        shepherd_positions=dogs,
        shepherd_velocities=np.zeros_like(dogs),
        world=world,
        rng=rng,
        metadata={"r_a": 2.0},
    )


def test_kubo_registered():
    assert "kubo" in algorithm_registry.names()
    alg = algorithm_registry.get("kubo")
    assert alg.id == "kubo"
    assert "K_f4" in alg.default_config


def test_target_sheep_farthest_from_goal():
    goal = np.array([0.0, 0.0])
    sheep = np.array([[1.0, 0.0], [10.0, 0.0], [3.0, 0.0]])
    target = target_sheep_farthest_from_goal(goal, sheep)
    assert np.allclose(target, [10.0, 0.0])


def test_sheep_forces_nonzero_near_dog(kubo_state):
    a, b, c, d = sheep_force_components(
        0,
        kubo_state.sheep_positions,
        kubo_state.sheep_velocities,
        kubo_state.shepherd_positions,
        radius=60.0,
    )
    assert a.shape == (2,)
    assert d.shape == (2,)
    assert np.linalg.norm(d) > 0


def test_dog_dog_repulsion_present(kubo_state):
    # Asymmetric spacing so inverse-cube repulsion does not cancel.
    dogs = np.array([[60.0, 60.0], [68.0, 58.0], [52.0, 70.0]])
    _, _, _, d_i = dog_force_components(
        0,
        dogs,
        kubo_state.sheep_positions,
        kubo_state.world.goal.center,
        radius=60.0,
    )
    assert np.linalg.norm(d_i) > 0


def test_clamp_speed():
    vel = np.array([[10.0, 0.0], [1.0, 0.0]])
    out = clamp_speed(vel, 5.0)
    assert np.isclose(np.linalg.norm(out[0]), 5.0)
    assert np.allclose(out[1], [1.0, 0.0])


def test_kubo_step_moves_agents(kubo_state):
    alg = KuboAlgorithm()
    config = alg.default_config
    new_state = alg.step(kubo_state, config)
    assert new_state.sheep_positions.shape == kubo_state.sheep_positions.shape
    assert new_state.shepherd_positions.shape == kubo_state.shepherd_positions.shape
    assert not np.allclose(new_state.shepherd_positions, kubo_state.shepherd_positions)


def test_kubo_seed_determinism():
    alg = KuboAlgorithm()
    scen = DriveToGoalScenario()
    config = alg.default_config
    config["n_sheep"] = 15
    config["n_shepherds"] = 3

    def run_once():
        runner = SimulationRunner(
            algorithm=alg,
            scenario=scen,
            metrics=metric_registry.get_all(),
            config=config,
            seed=99,
        )
        runner.initialize()
        positions = []
        for _ in range(5):
            state, _, _ = runner.step()
            positions.append(
                (
                    state.sheep_positions.copy(),
                    state.shepherd_positions.copy(),
                )
            )
        return positions

    first = run_once()
    second = run_once()
    for (s1, d1), (s2, d2) in zip(first, second):
        assert np.allclose(s1, s2)
        assert np.allclose(d1, d2)
