"""Correctness: metric formulas on known geometric cases."""

from __future__ import annotations

import numpy as np
import pytest

from metrics.cohesion import CohesionMetric
from metrics.shepherd_path import ShepherdPathMetric
from metrics.success_rate import SuccessRateMetric
from tests.backend.helpers import make_state, make_world


def test_cohesion_is_mean_distance_to_centroid():
    sheep = [[0.0, 0.0], [2.0, 0.0], [0.0, 2.0], [2.0, 2.0]]
    state = make_state(sheep, [[10.0, 10.0]])
    # Centroid is (1,1); each sheep is sqrt(2) away.
    assert CohesionMetric().compute(state) == pytest.approx(np.sqrt(2.0))


def test_success_rate_fraction_inside_goal():
    world = make_world(goal_center=(0.0, 0.0), goal_radius=5.0)
    sheep = [[0.0, 0.0], [1.0, 0.0], [20.0, 20.0], [30.0, 30.0]]
    state = make_state(sheep, [[10.0, 10.0]], world=world)
    assert SuccessRateMetric().compute(state) == pytest.approx(0.5)


def test_sheep_in_goal_counts_centers_inside_circle():
    from metrics.sheep_in_goal import SheepInGoalMetric

    world = make_world(goal_center=(0.0, 0.0), goal_radius=5.0)
    sheep = [[0.0, 0.0], [1.0, 0.0], [20.0, 20.0], [30.0, 30.0]]
    state = make_state(sheep, [[10.0, 10.0]], world=world)
    assert SheepInGoalMetric().compute(state) == pytest.approx(2.0)


def test_shepherd_path_accumulates_step_distance():
    world = make_world()
    metric = ShepherdPathMetric()
    start = make_state([[50.0, 50.0]], [[0.0, 0.0]], world=world, tick=0)
    assert metric.compute(start) == 0.0

    moved = make_state([[50.0, 50.0]], [[3.0, 4.0]], world=world, tick=1)
    assert metric.compute(moved) == pytest.approx(5.0)
