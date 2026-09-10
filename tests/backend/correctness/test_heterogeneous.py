"""Correctness: heterogeneous sheep response as a flock factor."""

from __future__ import annotations

import numpy as np

from algorithms.registry import algorithm_registry
from core.agent_attributes import init_agent_attributes
from core.presets import get_preset
from dynamics.strombom import StrombomSheepDynamics
from tests.backend.helpers import build_runner, make_state, make_world, snapshot_positions


def test_heterogeneous_registered():
    assert "heterogeneous" in algorithm_registry.names()


def test_heterogeneous_determinism_same_seed():
    snaps_a = snapshot_positions(
        build_runner("heterogeneous", seed=21, num_sheep=15, num_shepherds=1),
        5,
    )
    snaps_b = snapshot_positions(
        build_runner("heterogeneous", seed=21, num_sheep=15, num_shepherds=1),
        5,
    )
    for (sa, da), (sb, db) in zip(snaps_a, snaps_b):
        assert np.allclose(sa, sb)
        assert np.allclose(da, db)


def test_heterogeneous_stubborn_weaker_dog_response():
    sheep_dyn = StrombomSheepDynamics()
    sheep = np.array(
        [
            [40.0, 40.0],
            [42.0, 40.0],
            [40.0, 42.0],
            [41.0, 41.0],
            [43.0, 41.0],
            [41.0, 43.0],
            [39.0, 41.0],
            [41.0, 39.0],
            [42.0, 42.0],
            [40.0, 41.0],
        ]
    )
    dog = np.array([[48.0, 41.0]])
    world = make_world(goal_center=(10.0, 10.0))
    base = {
        **get_preset("heterogeneous")["default_config"],
        "noise_strength": 0.0,
        "graze_move_prob": 0.0,
        "r_s": 65.0,
        "shepherd_stop_multiple": 0.0,
    }
    cfg_responsive = {**base, "stubborn_fraction": 0.0, "stubborn_rs_scale": 0.25}
    cfg_stubborn = {**base, "stubborn_fraction": 1.0, "stubborn_rs_scale": 0.25}

    state_r = init_agent_attributes(make_state(sheep, dog, world=world, seed=5), cfg_responsive)
    state_s = init_agent_attributes(make_state(sheep, dog, world=world, seed=5), cfg_stubborn)
    state_r.sheep_velocities[:] = [[0.0, 1.0]] * len(sheep)
    state_s.sheep_velocities[:] = [[0.0, 1.0]] * len(sheep)

    out_r = sheep_dyn.step(state_r, cfg_responsive)
    out_s = sheep_dyn.step(state_s, cfg_stubborn)

    assert all(abs(v - 1.0) < 1e-9 for v in out_r.sheep_response)
    assert all(abs(v - 0.25) < 1e-9 for v in out_s.sheep_response)

    dog_pos = dog[0]
    away_r = np.mean(
        [
            np.dot(out_r.sheep_positions[i] - sheep[i], sheep[i] - dog_pos)
            for i in range(len(sheep))
        ]
    )
    away_s = np.mean(
        [
            np.dot(out_s.sheep_positions[i] - sheep[i], sheep[i] - dog_pos)
            for i in range(len(sheep))
        ]
    )
    assert away_r > away_s
