"""Correctness: metric formulas on known geometric cases."""

from __future__ import annotations

import numpy as np
import pytest

from metrics.cohesion import CohesionMetric
from metrics.fragmentation import FragmentationMetric, largest_component_fraction
from metrics.gcm_goal import GcmGoalMetric
from metrics.min_separation import MinSeparationMetric
from metrics.outlier_count import OutlierCountMetric
from metrics.polarization import PolarizationMetric
from metrics.sheep_in_goal import SheepInGoalMetric
from metrics.shepherd_path import ShepherdPathMetric
from metrics.success_rate import SuccessRateMetric
from metrics.time_to_goal import TimeToGoalMetric
from tests.backend.helpers import make_state, make_world


def test_cohesion_is_mean_distance_to_centroid():
    sheep = [[0.0, 0.0], [2.0, 0.0], [0.0, 2.0], [2.0, 2.0]]
    state = make_state(sheep, [[10.0, 10.0]])
    # Centroid is (1,1); each sheep is sqrt(2) away.
    assert CohesionMetric().compute(state) == pytest.approx(np.sqrt(2.0))


def test_gcm_goal_is_centroid_to_goal_distance():
    world = make_world(goal_center=(0.0, 0.0), goal_radius=5.0)
    sheep = [[0.0, 0.0], [2.0, 0.0], [0.0, 2.0], [2.0, 2.0]]
    state = make_state(sheep, [[10.0, 10.0]], world=world)
    # Centroid is (1,1); distance to goal (0,0) is sqrt(2).
    assert GcmGoalMetric().compute(state) == pytest.approx(np.sqrt(2.0))


def test_success_rate_fraction_inside_goal():
    world = make_world(goal_center=(0.0, 0.0), goal_radius=5.0)
    sheep = [[0.0, 0.0], [1.0, 0.0], [20.0, 20.0], [30.0, 30.0]]
    state = make_state(sheep, [[10.0, 10.0]], world=world)
    assert SuccessRateMetric().compute(state) == pytest.approx(0.5)


def test_sheep_in_goal_counts_centers_inside_circle():
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


def test_polarization_is_norm_of_mean_unit_velocity():
    sheep = [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]]
    state = make_state(sheep, [[10.0, 10.0]])
    state.sheep_velocities[:] = [[1.0, 0.0], [1.0, 0.0], [1.0, 0.0]]
    assert PolarizationMetric().compute(state) == pytest.approx(1.0)

    state.sheep_velocities[:] = [[1.0, 0.0], [-1.0, 0.0], [0.0, 0.0]]
    assert PolarizationMetric().compute(state) == pytest.approx(0.0)


def test_outlier_count_uses_ra_n_two_thirds():
    # Many sheep at one point keep GCM there; one straggler beyond f(N).
    flock = [[10.0, 10.0]] * 7 + [[40.0, 10.0]]
    state = make_state(flock, [[20.0, 10.0]], metadata={"r_a": 2.0})
    # f(8) = 2 * 8^(2/3) ~= 8.0; only the sheep at x=40 is beyond.
    assert OutlierCountMetric().compute(state) == pytest.approx(1.0)


def test_min_separation_is_closest_pair_distance():
    sheep = [[0.0, 0.0], [3.0, 0.0], [0.0, 10.0]]
    state = make_state(sheep, [[5.0, 5.0]])
    assert MinSeparationMetric().compute(state) == pytest.approx(3.0)


def test_time_to_goal_returns_tick_when_all_inside():
    world = make_world(goal_center=(0.0, 0.0), goal_radius=5.0)
    inside = make_state(
        [[0.0, 0.0], [1.0, 0.0]],
        [[10.0, 10.0]],
        world=world,
        tick=42,
    )
    assert TimeToGoalMetric().compute(inside) == pytest.approx(42.0)

    outside = make_state(
        [[0.0, 0.0], [20.0, 20.0]],
        [[10.0, 10.0]],
        world=world,
        tick=42,
    )
    assert TimeToGoalMetric().compute(outside) == pytest.approx(-1.0)


def test_time_to_goal_stays_negative_until_every_sheep_is_inside():
    """time_to_goal uses all-inside; success_rate can be partial."""
    world = make_world(goal_center=(0.0, 0.0), goal_radius=5.0)
    mostly_inside = make_state(
        [[0.0, 0.0], [1.0, 0.0], [20.0, 20.0]],
        [[10.0, 10.0]],
        world=world,
        tick=10,
    )
    assert SuccessRateMetric().compute(mostly_inside) == pytest.approx(2.0 / 3.0)
    assert TimeToGoalMetric().compute(mostly_inside) == pytest.approx(-1.0)


def test_fragmentation_is_largest_component_over_n():
    # Two pairs far apart: largest component has 2 of 4 sheep -> 0.5.
    sheep = [[0.0, 0.0], [1.0, 0.0], [50.0, 0.0], [51.0, 0.0]]
    state = make_state(sheep, [[10.0, 10.0]], metadata={"measurement_radius": 2.0})
    assert FragmentationMetric().compute(state) == pytest.approx(0.5)
    assert largest_component_fraction(np.asarray(sheep, dtype=float), 2.0) == pytest.approx(
        0.5
    )


def test_fragmentation_is_one_when_fully_connected():
    sheep = [[0.0, 0.0], [1.0, 0.0], [2.0, 0.0]]
    state = make_state(sheep, [[10.0, 10.0]], metadata={"measurement_radius": 2.0})
    assert FragmentationMetric().compute(state) == pytest.approx(1.0)
