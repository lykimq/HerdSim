"""Correctness: Strombom 2014 Collect/Drive and sheep dynamics vs paper."""

from __future__ import annotations

import numpy as np
import pytest

from algorithms.strombom.algorithm import StrombomAlgorithm
from algorithms.strombom.heuristics import (
    collect_offset,
    collect_target,
    compute_threshold,
    drive_offset,
    drive_target,
    should_collect,
)
from core.agents.sheep import (
    compose_strombom_heading,
    compute_local_centroid_knn,
    compute_repulsion_from_neighbours,
    unit_vector,
)
from tests.backend.helpers import make_state, make_world


def test_threshold_matches_paper_formula():
    assert compute_threshold(8, 2.0) == pytest.approx(2.0 * (8 ** (2.0 / 3.0)))


def test_should_collect_when_outlier_beyond_threshold():
    sheep = [[50.0, 50.0], [51.0, 50.0], [50.0, 51.0], [90.0, 90.0]]
    state = make_state(sheep, [[70.0, 70.0]])
    assert should_collect(state, {"r_a": 2.0})


def test_should_drive_when_flock_is_compact():
    sheep = [[50.0, 50.0], [51.0, 50.5], [49.5, 51.0], [50.5, 49.5]]
    state = make_state(sheep, [[70.0, 70.0]])
    assert not should_collect(state, {"r_a": 2.0})


def test_collect_target_is_behind_furthest_sheep():
    sheep = [[50.0, 50.0], [51.0, 50.0], [50.0, 51.0], [80.0, 50.0]]
    state = make_state(sheep, [[90.0, 50.0]])
    target = collect_target(state, {"r_a": 2.0})
    assert target[0] > 80.0
    assert abs(target[1] - 50.0) < 1.0
    assert collect_offset({"r_a": 2.0}) == pytest.approx(2.0)


def test_drive_offset_is_ra_sqrt_n():
    sheep = [[40.0, 0.0], [42.0, 0.0], [41.0, 1.0], [39.0, -1.0]]
    state = make_state(sheep, [[60.0, 0.0]], world=make_world(goal_center=(0.0, 0.0)))
    assert drive_offset(state, {"r_a": 2.0}) == pytest.approx(2.0 * (4 ** 0.5))


def test_drive_target_is_behind_gcm_from_goal():
    world = make_world(goal_center=(0.0, 0.0), goal_radius=10.0)
    sheep = [[40.0, 0.0], [42.0, 0.0], [41.0, 1.0]]
    state = make_state(sheep, [[60.0, 0.0]], world=world)
    target = drive_target(state, {"r_a": 2.0})
    assert target[0] > state.sheep_centroid[0]
    expected_offset = 2.0 * (3 ** 0.5)
    gcm = state.sheep_centroid
    assert abs(np.linalg.norm(target - gcm) - expected_offset) < 1e-6


def test_shepherd_stops_within_three_ra():
    alg = StrombomAlgorithm()
    cfg = alg.default_config
    sheep = np.array([[50.0, 50.0], [52.0, 50.0], [50.0, 52.0]])
    dog = np.array([[51.0, 50.5]])  # closer than 3*r_a = 6
    state = make_state(sheep, dog, world=make_world(), seed=1)
    new_state = alg.step(state, cfg)
    assert np.allclose(new_state.shepherd_velocities[0], 0.0)


def test_sheep_graze_when_shepherd_beyond_rs():
    alg = StrombomAlgorithm()
    cfg = {**alg.default_config, "graze_move_prob": 0.0}
    sheep = np.array([[40.0, 40.0], [42.0, 40.0], [40.0, 42.0]])
    dog = np.array([[140.0, 140.0]])  # >> r_s
    state = make_state(sheep, dog, world=make_world(), seed=2)
    new_state = alg.step(state, cfg)
    assert np.allclose(new_state.sheep_velocities, 0.0)


def test_heading_uses_paper_additive_weights():
    prev = np.array([1.0, 0.0])
    attraction = np.array([0.0, 1.0])
    repulsion_sheep = np.array([1.0, 1.0])
    repulsion_shep = np.array([-1.0, 0.0])
    noise = np.zeros(2)
    heading = compose_strombom_heading(
        prev,
        attraction,
        repulsion_sheep,
        repulsion_shep,
        noise,
        inertia=0.5,
        c=1.05,
        ra_weight=2.0,
        rs_weight=1.0,
    )
    expected = unit_vector(
        0.5 * unit_vector(prev)
        + 1.05 * unit_vector(attraction)
        + 2.0 * unit_vector(repulsion_sheep)
        + 1.0 * unit_vector(repulsion_shep)
    )
    assert np.allclose(heading, expected)


def test_lcm_uses_n_nearest_neighbours():
    positions = np.array(
        [
            [0.0, 0.0],
            [1.0, 0.0],
            [10.0, 0.0],
            [100.0, 0.0],
        ]
    )
    lcm = compute_local_centroid_knn(positions, 0, n_neighbors=2)
    # nearest to origin: (1,0) and (10,0)
    assert np.allclose(lcm, [5.5, 0.0])


def test_neighbour_repulsion_matches_eq_4_1():
    """Paper eq. 4.1: R_a = sum of unit vectors away from neighbours."""
    # Single neighbour at distance 1: unit vector (-1, 0).
    positions = np.array([[0.0, 0.0], [1.0, 0.0]])
    ra = compute_repulsion_from_neighbours(positions, 0, repulsion_radius=2.0)
    assert np.allclose(ra, [-1.0, 0.0])

    # Two neighbours: sum of unit vectors away from each.
    positions = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 2.0]])
    ra = compute_repulsion_from_neighbours(positions, 0, repulsion_radius=3.0)
    # Away from (1,0) => (-1,0); away from (0,2) => (0,-1); sum = (-1,-1).
    assert np.allclose(ra, [-1.0, -1.0])
