"""Unit tests for metric computations."""

import numpy as np
from metrics.cohesion import CohesionMetric
from metrics.outlier_count import OutlierCountMetric
from metrics.polarization import PolarizationMetric
from metrics.shepherd_path import ShepherdPathMetric
from metrics.time_to_goal import TimeToGoalMetric
from metrics.success_rate import SuccessRateMetric
from metrics.min_separation import MinSeparationMetric
from core.simulation_state import SimulationState


def test_cohesion_metric(sample_state):
    m = CohesionMetric()
    val = m.compute(sample_state)
    assert val >= 0.0


def test_outlier_count_metric(sample_state):
    m = OutlierCountMetric()
    val = m.compute(sample_state)
    assert isinstance(val, (int, float))


def test_polarization_metric(sample_state):
    m = PolarizationMetric()
    val = m.compute(sample_state)
    assert 0.0 <= val <= 1.0


def test_shepherd_path_metric(sample_state, sample_world):
    m = ShepherdPathMetric()
    assert m.compute(sample_state) == 0.0
    
    # Simulate step with moved positions
    moved_state = SimulationState(
        tick=1,
        sheep_positions=sample_state.sheep_positions,
        sheep_velocities=sample_state.sheep_velocities,
        shepherd_positions=sample_state.shepherd_positions + 5.0,
        shepherd_velocities=sample_state.shepherd_velocities,
        world=sample_world,
        rng=sample_state.rng,
    )
    val = m.compute(moved_state)
    assert val > 0.0


def test_min_separation_metric(sample_state):
    m = MinSeparationMetric()
    val = m.compute(sample_state)
    assert val >= 0.0
