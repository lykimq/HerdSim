"""Correctness: V-formation controller behaviour."""

from __future__ import annotations

import numpy as np

from algorithms.registry import algorithm_registry
from controllers.v_formation import VFormationController
from core.observation_models import GlobalObservation
from core.presets import get_preset
from tests.backend.helpers import build_runner, make_state, make_world, snapshot_positions


def test_v_formation_registered():
    assert "v_formation" in algorithm_registry.names()


def test_v_formation_step_runs():
    ctrl = VFormationController()
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
    obs = GlobalObservation().observe_all(state, ctrl.default_config)
    new_state = ctrl.step(state, obs, ctrl.default_config)
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
    ctrl = VFormationController()
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

    cfg_paper = {**ctrl.default_config, "r_a": r_a, "collect_threshold_scale": 1.0}
    cfg_scaled = {**ctrl.default_config, "r_a": r_a, "collect_threshold_scale": 1.5}
    obs = GlobalObservation().observe_all(state, cfg_paper)
    assert ctrl.step(state, obs, cfg_paper).metadata["herding_mode"] == "collect"
    assert ctrl.step(state, obs, cfg_scaled).metadata["herding_mode"] == "drive"
