"""Correctness: Strombom Collect/Drive switching and targets."""

from __future__ import annotations

import pytest

from algorithms.strombom.heuristics import (
    collect_target,
    compute_threshold,
    drive_target,
    should_collect,
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
    target = collect_target(state, {"r_a": 2.0, "collect_drive_offset": 5.0})
    assert target[0] > 80.0
    assert abs(target[1] - 50.0) < 1.0


def test_drive_target_is_behind_gcm_from_goal():
    world = make_world(goal_center=(0.0, 0.0), goal_radius=10.0)
    sheep = [[40.0, 0.0], [42.0, 0.0], [41.0, 1.0]]
    state = make_state(sheep, [[60.0, 0.0]], world=world)
    target = drive_target(state, {"collect_drive_offset": 5.0})
    assert target[0] > state.sheep_centroid[0]
