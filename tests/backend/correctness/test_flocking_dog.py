"""Correctness: Jadhav / Flocking Dog 2024 sheep and dog dynamics."""

from __future__ import annotations

import numpy as np
import pytest

from algorithms.flocking_dog.dynamics import sheep_repulsion
from algorithms.strombom.heuristics import compute_threshold
from controllers.collect_drive import CollectDriveController
from core.agents.sheep import nearest_neighbor_indices
from core.observation_models import GlobalObservation
from core.presets import get_preset
from dynamics.jadhav import JadhavSheepDynamics
from tests.backend.helpers import make_state, make_world


def test_flocking_dog_defaults_match_paper():
    cfg = get_preset("flocking_dog")["default_config"]
    assert cfg["r_a"] == 2.0
    assert cfg["r_s"] == 12.0
    assert cfg["k_neighbors"] == 10
    assert cfg["n_attraction"] == 5
    assert cfg["n_alignment"] == 1
    assert cfg["sheep_speed"] == 1.0
    assert cfg["dog_speed"] == 1.5
    assert cfg["dog_close_speed"] == 0.05


def test_sheep_graze_when_dog_beyond_rd():
    sheep = JadhavSheepDynamics()
    cfg = sheep.default_config
    state = make_state(
        [[40.0, 40.0], [42.0, 40.0], [40.0, 42.0]],
        [[100.0, 100.0]],
        world=make_world(),
        seed=0,
    )
    new_state = sheep.step(state, cfg)
    assert np.allclose(new_state.sheep_velocities, 0.0)


def test_dog_slows_within_ra():
    ctrl = CollectDriveController()
    cfg = {**get_preset("flocking_dog")["default_config"]}
    state = make_state(
        [[50.0, 50.0], [52.0, 50.0], [50.0, 52.0]],
        [[51.0, 50.5]],
        world=make_world(),
        seed=1,
    )
    state.shepherd_velocities[:] = [[1.0, 0.0]]
    obs = GlobalObservation().observe_all(state, cfg)
    new_state = ctrl.step(state, obs, cfg)
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
    sheep = JadhavSheepDynamics()
    cfg = {**sheep.default_config, "noise_strength": 0.0}
    sheep_pos = np.array([[50.0, 50.0], [51.0, 50.0], [50.0, 51.0], [51.0, 51.0]])
    dog = np.array([[55.0, 50.5]])
    state = make_state(sheep_pos, dog, world=make_world(), seed=3)
    state.sheep_velocities[:] = [[0.0, 1.0]] * 4
    new_state = sheep.step(state, cfg)
    delta = new_state.sheep_positions.mean(axis=0) - sheep_pos.mean(axis=0)
    assert delta[0] < 0
