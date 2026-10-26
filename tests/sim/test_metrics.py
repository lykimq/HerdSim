"""Metrics on hand-made geometry."""

from __future__ import annotations

import numpy as np
import pytest

from sim.plugins.metrics import dogs, flock
from sim.plugins.metrics.view import TickView
from sim.plugins.scenarios import goal
from tests.helpers import make_state, make_world

SQUARE = [[0.0, 0.0], [2.0, 0.0], [0.0, 2.0], [2.0, 2.0]]
# Run-config constants the metrics read.
CONFIG = {
    "measurement_radius": 2.0,
    "lost_radius": 10.0,
    "dog_overlap_distance": 2.0,
    "reaction_radius": 5.0,
}


def view(sheep, shepherds, **kw) -> TickView:
    return TickView(make_state(sheep, shepherds, metadata={"shepherd_path": 0.0}, **kw), CONFIG)


def test_centroid_distance_and_spread():
    v = view(SQUARE, [[10.0, 10.0]], world=make_world(goal_center=(0.0, 0.0)))
    assert goal.gcm_goal(v) == pytest.approx(np.sqrt(2.0))
    assert flock.cohesion(v) == pytest.approx(np.sqrt(2.0))
    assert flock.extent(v) == pytest.approx(np.sqrt(2.0))


def test_hull_perimeter_area_density():
    v = view(SQUARE, [[9.0, 9.0]])
    assert flock.perimeter(v) == pytest.approx(8.0)
    assert flock.hull_area(v) == pytest.approx(4.0)
    assert flock.flock_density(v) == pytest.approx(1.0)


def test_hull_of_flat_flock():
    line = view([[0.0, 0.0], [1.0, 0.0], [3.0, 0.0]], [[9.0, 9.0]])
    assert flock.perimeter(line) == pytest.approx(6.0)
    assert flock.hull_area(line) == 0.0
    assert np.isnan(flock.flock_density(line))
    one = view([[0.0, 0.0]], [[9.0, 9.0]])
    assert flock.perimeter(one) == 0.0


def test_fragmentation_and_lost_sheep():
    pairs = [[0.0, 0.0], [1.0, 0.0], [50.0, 0.0], [51.0, 0.0]]
    v = view(pairs, [[9.0, 9.0]])
    assert flock.fragmentation(v) == pytest.approx(0.5)
    assert flock.lost_sheep(v) == 4.0  # every sheep is 25 from the centroid
    assert flock.lost_sheep(view(SQUARE, [[9.0, 9.0]])) == 0.0


def test_dogs_goal_side():
    world = make_world(goal_center=(100.0, 0.0))
    v = view([[0.0, 0.0], [1.0, 0.0]], [[-5.0, 0.0], [-7.0, 0.0], [10.0, 0.0]], world=world)
    assert goal.dogs_goal_side(v) == pytest.approx(1 / 3)


def test_dog_overlap_counts_dogs_with_a_twin():
    v = view(SQUARE, [[0.0, 0.0], [1.0, 0.0], [10.0, 0.0]])
    assert dogs.dog_overlap(v) == pytest.approx(2 / 3)  # the two dogs 1 apart, not the third
    assert dogs.dog_overlap(view(SQUARE, [[0.0, 0.0]])) == 0.0
    assert np.isnan(dogs.dog_overlap(view(SQUARE, np.zeros((0, 2)))))


def test_gcm_in_goal_follows_the_centroid():
    world = make_world(goal_center=(0.0, 0.0), goal_radius=5.0)
    assert goal.gcm_in_goal(view(SQUARE, [[9.0, 9.0]], world=world)) == 1.0  # centroid (1, 1)
    far = [[20.0, 0.0], [22.0, 0.0], [20.0, 2.0], [22.0, 2.0]]
    assert goal.gcm_in_goal(view(far, [[9.0, 9.0]], world=world)) == 0.0


def test_aspect_ratio_degenerate_flocks_are_nan():
    assert flock.aspect_ratio(view(SQUARE, [[9.0, 9.0]])) == pytest.approx(1.0)
    assert np.isnan(flock.aspect_ratio(view([[0.0, 0.0], [1.0, 0.0]], [[9.0, 9.0]])))
    assert np.isnan(flock.aspect_ratio(view([[0.0, 0.0], [1.0, 0.0], [3.0, 0.0]], [[9.0, 9.0]])))
    assert np.isnan(flock.aspect_ratio(view([[1.0, 1.0]] * 4, [[9.0, 9.0]])))


def test_coverage_and_i_dir_without_dogs():
    assert np.isnan(dogs.coverage(view(SQUARE, np.zeros((0, 2)))))
    assert dogs.i_dir(view(SQUARE, np.zeros((0, 2)))) == 0.0


def test_stopped_dogs_and_direction_conflict():
    v = view(
        SQUARE,
        [[9.0, 9.0], [8.0, 8.0], [7.0, 7.0]],
        velocities=[[1.0, 0.0], [-1.0, 0.0], [0.0, 0.0]],
    )
    assert dogs.dogs_stopped(v) == pytest.approx(1 / 3)
    assert dogs.i_dir(v) == pytest.approx(1.0)


def test_coverage_counts_outer_sheep_within_reaction_radius():
    sheep = [[0.0, 0.0], [1.0, 0.0], [-1.0, 0.0], [20.0, 0.0], [-20.0, 0.0]]
    v = view(sheep, [[22.0, 0.0]])
    assert dogs.coverage(v) == pytest.approx(0.5)  # outer: the two at +-20; one is within 5


def test_collect_mode_detects_outliers():
    # 4 sheep in tight square at origin: distances to centroid are sqrt(2) ~ 1.41
    # f(4) = 2.0 * 4^(2/3) ~ 5.04
    tight = view(SQUARE, [[10.0, 10.0]])
    assert dogs.collect_mode(tight) == 0.0

    # Add a distant stray at (30, 0)
    stray = [[0.0, 0.0], [2.0, 0.0], [0.0, 2.0], [30.0, 0.0]]
    scattered = view(stray, [[10.0, 10.0]])
    assert dogs.collect_mode(scattered) == 1.0


