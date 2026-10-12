"""Tests for algorithm-agnostic failure taxonomy heuristics."""

from __future__ import annotations

import pandas as pd

from protocols.packaging.failure_taxonomy import (
    FAILURE_NONE,
    FAILURE_OSCILLATION,
    FAILURE_SCATTER,
    FAILURE_SPLIT,
    FAILURE_STUCK,
    FAILURE_TIMEOUT,
    classify_failure,
)


def test_success_is_none():
    result = classify_failure(pd.DataFrame({"cohesion": [1.0]}), success=True)
    assert result["failure_mode"] == FAILURE_NONE
    assert result["failure_hints"] == []


def test_split_when_fragmentation_low():
    history = pd.DataFrame(
        {
            "fragmentation": [1.0] * 10 + [0.3] * 20,
            "cohesion": [5.0] * 30,
            "gcm_goal": list(range(30, 0, -1)),
        }
    )
    result = classify_failure(history, success=False, n_shepherds=1)
    assert result["failure_mode"] == FAILURE_SPLIT
    assert FAILURE_SPLIT in result["failure_hints"]


def test_stuck_when_gcm_barely_moves():
    history = pd.DataFrame(
        {
            "fragmentation": [1.0] * 40,
            "cohesion": [6.0] * 40,
            "gcm_goal": [50.0] * 40,
        }
    )
    result = classify_failure(history, success=False)
    assert result["failure_mode"] == FAILURE_STUCK
    assert FAILURE_STUCK in result["failure_hints"]


def test_scatter_when_cohesion_stays_high():
    history = pd.DataFrame(
        {
            "fragmentation": [1.0] * 30,
            "cohesion": [22.0] * 30,
            "gcm_goal": [40.0 - i * 0.5 for i in range(30)],
        }
    )
    result = classify_failure(history, success=False)
    assert FAILURE_SCATTER in result["failure_hints"]
    assert result["failure_mode"] == FAILURE_SCATTER


def test_oscillation_detected_from_gcm_flips():
    gcm = []
    for i in range(40):
        gcm.append(30.0 + (3.0 if i % 2 == 0 else -3.0))
    history = pd.DataFrame(
        {
            "fragmentation": [1.0] * 40,
            "cohesion": [8.0] * 40,
            "gcm_goal": gcm,
        }
    )
    result = classify_failure(history, success=False)
    assert FAILURE_OSCILLATION in result["failure_hints"]


def test_timeout_fallback():
    history = pd.DataFrame(
        {
            "fragmentation": [1.0] * 10,
            "cohesion": [4.0] * 10,
            "gcm_goal": [40.0 - 2.0 * i for i in range(10)],
        }
    )
    result = classify_failure(history, success=False)
    assert result["failure_mode"] == FAILURE_TIMEOUT
    assert result["failure_hints"] == [FAILURE_TIMEOUT]


def test_stacking_when_dogs_stay_close():
    from protocols.packaging.failure_taxonomy import FAILURE_STACKING

    history = pd.DataFrame(
        {
            "fragmentation": [1.0] * 20,
            "cohesion": [5.0] * 20,
            "gcm_goal": [40.0 - i for i in range(20)],
            "min_dog_separation": [0.5] * 20,
        }
    )
    result = classify_failure(history, success=False, n_shepherds=3)
    assert FAILURE_STACKING in result["failure_hints"]
    assert result["failure_mode"] == FAILURE_STACKING
