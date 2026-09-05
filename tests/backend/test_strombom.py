"""Unit tests for Strömbom 2014 algorithm heuristics and execution."""

import numpy as np
from algorithms.strombom.algorithm import StrombomAlgorithm
from algorithms.strombom.heuristics import collect_target, drive_target, should_collect


def test_strombom_properties():
    alg = StrombomAlgorithm()
    assert alg.id == "strombom"
    assert "Strömbom" in alg.name
    assert "r_a" in alg.default_config


def test_collect_target(sample_state):
    config = {"collect_drive_offset": 5.0}
    target = collect_target(sample_state, config)
    assert target.shape == (2,)


def test_drive_target(sample_state):
    config = {"goal_center": [100.0, 100.0], "collect_drive_offset": 5.0}
    target = drive_target(sample_state, config)
    assert target.shape == (2,)


def test_strombom_step(sample_state, strombom_algorithm):
    config = strombom_algorithm.default_config
    new_state = strombom_algorithm.step(sample_state, config)
    # Shepherd should have moved
    assert not np.array_equal(new_state.shepherd_positions, sample_state.shepherd_positions)
