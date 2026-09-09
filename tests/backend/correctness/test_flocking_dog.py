"""Correctness: Flocking Dog 2024 paper dynamics."""

from __future__ import annotations

import numpy as np
import pytest

from algorithms.flocking_dog.algorithm import FlockingDogAlgorithm
from algorithms.flocking_dog.dynamics import sheep_repulsion
from core.agents.sheep import nearest_neighbor_indices
from algorithms.strombom.heuristics import compute_threshold
from tests.backend.helpers import make_state, make_world


def test_flocking_dog_defaults_match_paper():
    cfg = FlockingDogAlgorithm().default_config
    assert cfg["r_a"] == 2.0
    assert cfg["r_s"] == 12.0
    assert cfg["k_neighbors"] == 10
    assert cfg["n_attraction"] == 5
    assert cfg["n_alignment"] == 1
    assert cfg["sheep_speed"] == 1.0
    assert cfg["dog_speed"] == 1.5
    assert cfg["dog_close_speed"] == 0.05


def test_sheep_graze_when_dog_beyond_rd():
    alg = FlockingDogAlgorithm()
    cfg = alg.default_config
    state = make_state(
        [[40.0, 40.0], [42.0, 40.0], [40.0, 42.0]],
        [[100.0, 100.0]],  # >> r_s=12
        world=make_world(),
        seed=0,
    )
    new_state = alg.step(state, cfg)
    assert np.allclose(new_state.sheep_velocities, 0.0)


def test_dog_slows_within_ra():
    alg = FlockingDogAlgorithm()
    cfg = alg.default_config
    state = make_state(
        [[50.0, 50.0], [52.0, 50.0], [50.0, 52.0]],
        [[51.0, 50.5]],  # within r_a=2
        world=make_world(),
        seed=1,
    )
    state.shepherd_velocities[:] = [[1.0, 0.0]]
    new_state = alg.step(state, cfg)
    assert np.isclose(np.linalg.norm(new_state.shepherd_velocities[0]), 0.05)
    assert np.allclose(
        new_state.shepherd_velocities[0] / 0.05, [1.0, 0.0], atol=1e-9
    )


def test_collect_threshold_is_ra_n_two_thirds():
    n = 14
    r_a = 2.0
    assert compute_threshold(n, r_a) == pytest.approx(r_a * (n ** (2.0 / 3.0)))


def test_nearest_neighbors_topological():
    pos = np.array([[0.0, 0.0], [1.0, 0.0], [10.0, 0.0], [100.0, 0.0]])
    idx = nearest_neighbor_indices(pos, 0, k=2)
    assert set(idx.tolist()) == {1, 2}


def test_sheep_repulsion_points_away():
    pos = np.array([[0.0, 0.0], [1.0, 0.0]])
    rep = sheep_repulsion(pos, 0, radius=2.0)
    assert rep[0] < 0
    assert abs(rep[1]) < 1e-6


def test_threatened_sheep_move_away_from_dog():
    alg = FlockingDogAlgorithm()
    cfg = {**alg.default_config, "noise_strength": 0.0}
    # Dog to the right of a tight flock within Rd.
    sheep = np.array([[50.0, 50.0], [51.0, 50.0], [50.0, 51.0], [51.0, 51.0]])
    dog = np.array([[55.0, 50.5]])
    state = make_state(sheep, dog, world=make_world(), seed=3)
    state.sheep_velocities[:] = [[0.0, 1.0]] * 4
    new_state = alg.step(state, cfg)
    # Mean sheep displacement should have a leftward (away-from-dog) component.
    delta = new_state.sheep_positions.mean(axis=0) - sheep.mean(axis=0)
    assert delta[0] < 0
