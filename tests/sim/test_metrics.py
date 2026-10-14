"""Correctness: metrics that feed failure labels and analysis, on known geometry."""

from __future__ import annotations

import numpy as np
import pytest
from methods.strombom.config import STROMBOM_DEFAULTS
from plugins.metrics.flock import cohesion, fragmentation
from plugins.metrics.goal import gcm_goal

from services.layout import load_run_protocol
from services.runner import ScalingCell, _run_cell, task_setup
from tests.helpers import make_state, make_world

SQUARE = [[0.0, 0.0], [2.0, 0.0], [0.0, 2.0], [2.0, 2.0]]


def test_cohesion_and_gcm_goal():
    state = make_state(SQUARE, [[10.0, 10.0]], world=make_world(goal_center=(0.0, 0.0)))
    # Centroid (1, 1): each sheep and the goal are sqrt(2) away.
    assert cohesion(state) == pytest.approx(np.sqrt(2.0))
    assert gcm_goal(state) == pytest.approx(np.sqrt(2.0))


def test_shepherd_path_accumulates_and_respects_dog_speed():
    _, _, _, canonical = load_run_protocol("phase1_scout")
    n_dogs, ticks = 2, 60
    cell = ScalingCell(
        n_sheep=20,
        n_shepherds=n_dogs,
        seed=2026,
        initial_layout="compact",
        method="strombom_multi",
        scenario=str(canonical["task"]),
        max_ticks=ticks,
        **task_setup(canonical, 20),
    )
    path = _run_cell(cell)["history"]["shepherd_path"].to_numpy()
    assert path[0] == 0.0
    assert np.all(np.diff(path) >= 0.0)
    # Each Strombom dog moves at most shepherd_speed per tick.
    assert 0.0 < path[-1] <= n_dogs * ticks * STROMBOM_DEFAULTS["shepherd_speed"] + 1e-9


def test_fragmentation_is_largest_component_over_n():
    meta = {"measurement_radius": 2.0}
    pairs = [[0.0, 0.0], [1.0, 0.0], [50.0, 0.0], [51.0, 0.0]]
    split = make_state(pairs, [[9.0, 9.0]], metadata=meta)
    chain = make_state([[0.0, 0.0], [1.0, 0.0], [2.0, 0.0]], [[9.0, 9.0]], metadata=meta)
    assert fragmentation(split) == pytest.approx(0.5)
    assert fragmentation(chain) == pytest.approx(1.0)
