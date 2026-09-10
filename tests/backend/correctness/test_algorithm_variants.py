"""Correctness: instrument variants keep distinct herding behaviour."""

from __future__ import annotations

import numpy as np

from algorithms.registry import algorithm_registry
from controllers.collect_drive_multi import CollectDriveMultiController
from core.observation_models import GlobalObservation
from core.presets import get_preset
from dynamics.jadhav import JadhavSheepDynamics
from dynamics.strombom import StrombomSheepDynamics
from tests.backend.helpers import make_state, make_world


def test_variants_registered():
    names = set(algorithm_registry.names())
    assert {
        "strombom_multi",
        "strombom_noise",
        "flocking_dog",
        "v_formation",
        "heterogeneous",
        "obstacle_aware",
        "fat",
        "adaptive",
    } <= names


def test_strombom_noise_default_strength():
    assert get_preset("strombom_noise")["default_config"]["noise_strength"] >= 0.8


def test_strombom_multi_dogs_take_distinct_positions():
    ctrl = CollectDriveMultiController()
    world = make_world()
    sheep = [
        [50.0, 50.0],
        [80.0, 50.0],
        [50.0, 90.0],
        [55.0, 52.0],
        [48.0, 55.0],
    ]
    dogs = [[100.0, 100.0], [110.0, 90.0], [90.0, 110.0]]
    state = make_state(sheep, dogs, world=world, seed=1)
    obs = GlobalObservation().observe_all(state, ctrl.default_config)
    new_state = ctrl.step(state, obs, ctrl.default_config)
    uniq = {tuple(np.round(p, 3)) for p in new_state.shepherd_positions}
    assert len(uniq) == 3


def test_strombom_multi_stops_within_three_ra():
    ctrl = CollectDriveMultiController()
    cfg = ctrl.default_config
    sheep = np.array([[50.0, 50.0], [52.0, 50.0], [50.0, 52.0]])
    dogs = np.array([[51.0, 50.5], [50.5, 51.0], [51.5, 51.5]])
    state = make_state(sheep, dogs, world=make_world(), seed=1)
    obs = GlobalObservation().observe_all(state, cfg)
    new_state = ctrl.step(state, obs, cfg)
    assert np.allclose(new_state.shepherd_velocities, 0.0)


def test_strombom_multi_applies_shepherd_noise():
    ctrl = CollectDriveMultiController()
    cfg = {
        **ctrl.default_config,
        "noise_strength": 1.0,
        "shepherd_stop_multiple": 0.0,
        "n_shepherds": 1,
    }
    sheep = np.array([[40.0, 40.0], [42.0, 40.0], [40.0, 42.0], [41.0, 41.0]])
    dog = np.array([[80.0, 40.0]])
    state = make_state(sheep, dog, world=make_world(goal_center=(0.0, 0.0)), seed=7)
    obs = GlobalObservation().observe_all(state, cfg)
    v0 = ctrl.step(state, obs, cfg).shepherd_velocities[0]
    state2 = make_state(sheep, dog, world=make_world(goal_center=(0.0, 0.0)), seed=99)
    obs2 = GlobalObservation().observe_all(state2, cfg)
    v1 = ctrl.step(state2, obs2, cfg).shepherd_velocities[0]
    assert np.linalg.norm(v0) > 0
    assert np.linalg.norm(v1) > 0
    assert not np.allclose(v0, v1)


def test_strombom_multi_respects_collect_threshold_scale():
    ctrl = CollectDriveMultiController()
    sheep = [
        [50.0, 50.0],
        [51.0, 50.0],
        [50.0, 51.0],
        [49.5, 49.5],
        [50.5, 49.5],
        [49.5, 50.5],
        [51.0, 51.0],
        [62.0, 50.0],
    ]
    dogs = [[90.0, 50.0], [92.0, 48.0], [88.0, 52.0]]
    state = make_state(sheep, dogs, world=make_world(goal_center=(10.0, 10.0)), seed=1)
    r_a = 2.0
    n = len(sheep)
    base_threshold = r_a * (n ** (2.0 / 3.0))
    dist = float(np.max(state.distances_to_centroid()))
    assert dist > base_threshold
    assert dist <= base_threshold * 1.5

    cfg_paper = {**ctrl.default_config, "r_a": r_a, "collect_threshold_scale": 1.0}
    cfg_scaled = {**ctrl.default_config, "r_a": r_a, "collect_threshold_scale": 1.5}
    obs = GlobalObservation().observe_all(state, cfg_paper)
    assert ctrl.step(state, obs, cfg_paper).metadata["herding_mode"] == "collect"
    assert ctrl.step(state, obs, cfg_scaled).metadata["herding_mode"] == "drive"


def test_jadhav_step_moves_agents():
    sheep = JadhavSheepDynamics()
    state = make_state(
        [[40.0, 40.0], [42.0, 40.0], [40.0, 42.0]],
        [[48.0, 41.0]],
        world=make_world(),
        seed=0,
    )
    state.sheep_velocities[:] = [[0.0, 1.0], [0.0, 1.0], [0.0, 1.0]]
    cfg = sheep.default_config
    new_sheep = sheep.step(state, cfg)
    assert not np.allclose(new_sheep.sheep_positions, state.sheep_positions)
