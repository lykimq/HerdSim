"""Correctness: obstacle-aware Collect/Drive controller."""

from __future__ import annotations

import numpy as np

from algorithms.obstacle_aware.geometry import (
    deflect_drive_point,
    find_gate_gap_center,
    segment_intersects_aabb,
)
from algorithms.registry import algorithm_registry
from controllers.obstacle_aware_drive import ObstacleAwareDriveController
from core.observation_models import GlobalObservation
from core.presets import get_preset
from core.world import Obstacle
from tests.backend.helpers import build_runner, make_state, make_world, run_trial, snapshot_positions


def test_obstacle_aware_registered():
    assert "obstacle_aware" in algorithm_registry.names()


def test_obstacle_aware_determinism_same_seed():
    snaps_a = snapshot_positions(
        build_runner(
            "obstacle_aware",
            "obstacle_course",
            preset="scenario",
            seed=7,
            num_sheep=10,
            num_shepherds=1,
        ),
        5,
    )
    snaps_b = snapshot_positions(
        build_runner(
            "obstacle_aware",
            "obstacle_course",
            preset="scenario",
            seed=7,
            num_sheep=10,
            num_shepherds=1,
        ),
        5,
    )
    for (sa, da), (sb, db) in zip(snaps_a, snaps_b):
        assert np.allclose(sa, sb)
        assert np.allclose(da, db)


def test_obstacle_aware_runs_obstacle_course_without_crash():
    result = run_trial(
        "obstacle_aware",
        "obstacle_course",
        seed=1,
        preset="scenario",
        config_overrides={"max_ticks": 80, "n_shepherds": 1},
    )
    assert result.total_ticks >= 1
    assert result.total_ticks <= 80
    assert result.final_state.n_sheep >= 1


def test_obstacle_aware_step_emits_mode_metadata():
    ctrl = ObstacleAwareDriveController()
    sheep = [[40.0, 40.0], [42.0, 40.0], [40.0, 42.0], [41.0, 41.0]]
    dogs = [[70.0, 40.0]]
    state = make_state(sheep, dogs, world=make_world(goal_center=(120.0, 40.0)), seed=2)
    obs = GlobalObservation().observe_all(state, ctrl.default_config)
    new_state = ctrl.step(state, obs, ctrl.default_config)
    assert new_state.metadata.get("herding_mode") in {"collect", "drive"}
    assert isinstance(new_state.metadata.get("assignment_lines"), list)


def test_segment_intersects_and_gate_gap():
    wall = Obstacle(
        min_corner=np.array([50.0, 0.0]),
        max_corner=np.array([60.0, 40.0]),
    )
    assert segment_intersects_aabb(
        np.array([0.0, 20.0]), np.array([100.0, 20.0]), wall
    )
    assert not segment_intersects_aabb(
        np.array([0.0, 80.0]), np.array([100.0, 80.0]), wall
    )

    lower = Obstacle(min_corner=np.array([70.0, 0.0]), max_corner=np.array([78.0, 66.0]))
    upper = Obstacle(min_corner=np.array([70.0, 84.0]), max_corner=np.array([78.0, 150.0]))
    gap = find_gate_gap_center([lower, upper])
    assert gap is not None
    assert abs(gap[0] - 74.0) < 1e-6
    assert abs(gap[1] - 75.0) < 1e-6


def test_deflect_drive_point_offsets_when_blocked():
    gcm = np.array([20.0, 75.0])
    goal = np.array([130.0, 75.0])
    base = np.array([10.0, 75.0])
    obs = [
        Obstacle(min_corner=np.array([55.0, 40.0]), max_corner=np.array([65.0, 110.0])),
    ]
    deflected = deflect_drive_point(gcm, goal, base, obs, clearance=5.0)
    assert not np.allclose(deflected, base)
    assert abs(deflected[1] - base[1]) > 1.0
