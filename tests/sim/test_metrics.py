"""Correctness: metrics that feed failure labels and analysis, on known geometry."""

from __future__ import annotations

import numpy as np
import pytest
from plugins.metrics.cohesion import CohesionMetric
from plugins.metrics.fragmentation import FragmentationMetric
from plugins.metrics.gcm_goal import GcmGoalMetric
from plugins.metrics.shepherd_path import ShepherdPathMetric

from tests.helpers import make_state, make_world

SQUARE = [[0.0, 0.0], [2.0, 0.0], [0.0, 2.0], [2.0, 2.0]]


def test_cohesion_and_gcm_goal():
    state = make_state(SQUARE, [[10.0, 10.0]], world=make_world(goal_center=(0.0, 0.0)))
    # Centroid (1, 1): each sheep and the goal are sqrt(2) away.
    assert CohesionMetric().compute(state) == pytest.approx(np.sqrt(2.0))
    assert GcmGoalMetric().compute(state) == pytest.approx(np.sqrt(2.0))


def test_shepherd_path_accumulates_step_distance():
    metric = ShepherdPathMetric()
    assert metric.compute(make_state([[50.0, 50.0]], [[0.0, 0.0]], tick=0)) == 0.0
    assert metric.compute(make_state([[50.0, 50.0]], [[3.0, 4.0]], tick=1)) == pytest.approx(5.0)


def test_fragmentation_is_largest_component_over_n():
    meta = {"measurement_radius": 2.0}
    pairs = [[0.0, 0.0], [1.0, 0.0], [50.0, 0.0], [51.0, 0.0]]
    split = make_state(pairs, [[9.0, 9.0]], metadata=meta)
    chain = make_state([[0.0, 0.0], [1.0, 0.0], [2.0, 0.0]], [[9.0, 9.0]], metadata=meta)
    assert FragmentationMetric().compute(split) == pytest.approx(0.5)
    assert FragmentationMetric().compute(chain) == pytest.approx(1.0)
