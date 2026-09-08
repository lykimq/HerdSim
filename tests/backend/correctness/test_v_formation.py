"""Correctness: V-formation algorithm behaviour."""

from __future__ import annotations

import numpy as np

from algorithms.registry import algorithm_registry
from algorithms.v_formation.algorithm import VFormationAlgorithm
from tests.backend.helpers import build_runner, make_state, make_world, snapshot_positions


def test_v_formation_registered():
    assert "v_formation" in algorithm_registry.names()


def test_v_formation_step_runs():
    alg = VFormationAlgorithm()
    sheep = [
        [50.0, 50.0],
        [51.0, 50.0],
        [50.0, 51.0],
        [49.5, 49.5],
        [50.5, 49.5],
        [49.5, 50.5],
    ]
    dogs = [[80.0, 50.0], [82.0, 48.0]]
    state = make_state(sheep, dogs, world=make_world(goal_center=(10.0, 10.0)), seed=3)
    new_state = alg.step(state, alg.default_config)
    assert new_state.n_sheep == len(sheep)
    assert new_state.n_shepherds == 2
    assert new_state.metadata.get("herding_mode") in {"collect", "drive"}
    assert isinstance(new_state.metadata.get("assignment_lines"), list)


def test_v_formation_determinism_same_seed():
    snaps_a = snapshot_positions(
        build_runner("v_formation", seed=11, num_sheep=12, num_shepherds=2),
        5,
    )
    snaps_b = snapshot_positions(
        build_runner("v_formation", seed=11, num_sheep=12, num_shepherds=2),
        5,
    )
    for (sa, da), (sb, db) in zip(snaps_a, snaps_b):
        assert np.allclose(sa, sb)
        assert np.allclose(da, db)


def test_v_formation_collect_threshold_scale_affects_mode():
    alg = VFormationAlgorithm()
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
    dogs = [[90.0, 50.0], [92.0, 48.0]]
    state = make_state(sheep, dogs, world=make_world(goal_center=(10.0, 10.0)), seed=1)
    r_a = 2.0
    n = len(sheep)
    base_threshold = r_a * (n ** (2.0 / 3.0))
    dist = float(np.max(state.distances_to_centroid()))
    assert dist > base_threshold
    assert dist <= base_threshold * 1.5

    cfg_paper = {**alg.default_config, "r_a": r_a, "collect_threshold_scale": 1.0}
    cfg_scaled = {**alg.default_config, "r_a": r_a, "collect_threshold_scale": 1.5}
    alg._update_shepherds(state, cfg_paper)
    assert alg._last_mode == "collect"
    alg._update_shepherds(state, cfg_scaled)
    assert alg._last_mode == "drive"
