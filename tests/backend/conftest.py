"""Pytest fixtures for backend tests."""

import numpy as np
import pytest
from algorithms.strombom.algorithm import StrombomAlgorithm
from core.simulation_state import SimulationState
from core.world import World
from scenarios.drive_to_goal import DriveToGoalScenario


@pytest.fixture
def sample_world():
    return World(width=150.0, height=150.0)


@pytest.fixture
def sample_state(sample_world):
    rng = np.random.default_rng(42)
    sheep_pos = np.array([[50.0 + i, 50.0] for i in range(10)])
    shepherd_pos = np.array([[10.0, 10.0]])
    return SimulationState(
        tick=0,
        sheep_positions=sheep_pos,
        sheep_velocities=np.zeros_like(sheep_pos),
        shepherd_positions=shepherd_pos,
        shepherd_velocities=np.zeros_like(shepherd_pos),
        world=sample_world,
        rng=rng,
    )


@pytest.fixture
def strombom_algorithm():
    return StrombomAlgorithm()


@pytest.fixture
def default_scenario():
    return DriveToGoalScenario()
