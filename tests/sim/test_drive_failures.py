"""Failure labels of the drive task on synthetic histories."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from sim.plugins.scenarios import drive_failures as ft

CONFIG = {"goal_radius": 10.0, "flock_radius": 5.0, "dt": 1.0, "metrics_stride": 1}
TICKS = 1000


def history(**columns) -> pd.DataFrame:
    base = {
        "gcm_goal": np.full(TICKS, 100.0),
        "coverage": np.ones(TICKS),
        "lost_sheep": np.zeros(TICKS),
        "fragmentation": np.ones(TICKS),
        "extent": np.full(TICKS, 5.0),
    }
    base.update(columns)
    return pd.DataFrame(base)


def test_success_has_no_label():
    assert ft.classify_failure(history(), success=True, config=CONFIG).mode == ft.NONE


def test_still_flock_is_stuck():
    assert ft.classify_failure(history(), success=False, config=CONFIG).mode == ft.STUCK


def test_flock_driven_away_is_escaped():
    out = ft.classify_failure(
        history(gcm_goal=np.linspace(100, 300, TICKS)), success=False, config=CONFIG
    )
    assert out.mode == ft.FLOCK_ESCAPED


def test_dogs_out_of_reach():
    out = ft.classify_failure(history(coverage=np.zeros(TICKS)), success=False, config=CONFIG)
    assert out.mode == ft.DOGS_OUT_OF_RANGE


def test_split_and_scatter():
    split = ft.classify_failure(
        history(fragmentation=np.full(TICKS, 0.3)), success=False, config=CONFIG
    )
    assert split.mode == ft.SPLIT
    spread = ft.classify_failure(history(extent=np.full(TICKS, 20.0)), success=False, config=CONFIG)
    assert spread.mode == ft.SCATTER


def test_oscillation_needs_large_swings_not_noise():
    t = np.arange(TICKS)
    swing = 100.0 + 40.0 * np.sin(2 * np.pi * t / 250.0)
    out = ft.classify_failure(history(gcm_goal=swing), success=False, config=CONFIG)
    assert out.mode == ft.OSCILLATION
    noise = 100.0 + np.random.default_rng(0).normal(0.0, 0.5, TICKS)
    assert (
        ft.classify_failure(history(gcm_goal=noise), success=False, config=CONFIG).mode == ft.STUCK
    )


@pytest.mark.parametrize(
    "series, expected",
    [([0, 5, 0, 5, 0], 3), ([0, 1, 0, 1, 0], 0), ([0, 10, 20, 30], 0), ([0, 10, 0], 1)],
)
def test_swings(series, expected):
    assert ft.swings(np.asarray(series, dtype=float), amplitude=2.0) == expected


def test_oscillation_window_is_in_model_seconds():
    assert ft.smooth_window(1.0) == 200  # Strombom: 1 s per tick
    assert ft.smooth_window(0.05) == 4000  # Kubo: the same 200 s of model time
    assert ft.smooth_window(0.05, 10) == 400  # one row per 10 ticks: the same 200 s


def test_per_method_coverage_threshold():
    low = history(coverage=np.full(TICKS, 0.08))
    assert ft.classify_failure(low, success=False, config=CONFIG).mode == ft.DOGS_OUT_OF_RANGE
    kubo_like = {**CONFIG, "low_coverage": 0.05}
    assert ft.classify_failure(low, success=False, config=kubo_like).mode == ft.STUCK


def test_failure_regime_classification():
    assert ft.classify_failure_regime(history(), success=True, config=CONFIG) == "none"

    # Stalled far from goal (100m, goal_radius=10m) -> structural gather failure
    far = history(gcm_goal=np.full(TICKS, 100.0))
    assert ft.classify_failure_regime(far, success=False, config=CONFIG) == ft.STRUCTURAL_GATHER

    # Stalled near goal (15m <= 2 * 10m) -> boundary temporal failure
    near = history(gcm_goal=np.full(TICKS, 15.0))
    assert ft.classify_failure_regime(near, success=False, config=CONFIG) == ft.BOUNDARY_TEMPORAL
