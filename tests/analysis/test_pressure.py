"""Pressure replays: the distance shares, and that a replay is the stored trial or stops."""

from __future__ import annotations

import numpy as np
import pytest

from analysis.pressure import ReplayJob, ReplayMismatch, near_shares, replay
from sim.core.simulation_runner import run_trial
from tests.helpers import config_for


def test_near_shares_count_sheep_strictly_inside_each_radius():
    sheep = np.array([[0.0, 0.0], [10.0, 0.0], [0.0, 3.0], [100.0, 100.0]])
    dogs = np.array([[0.0, 1.0], [10.0, 5.0]])
    # nearest dog: 1, 5, 2, far. Inside 5 strictly: two of four; inside 1.5: one of four.
    assert near_shares(sheep, dogs, reach=5.0, close=1.5) == (0.5, 0.25)
    assert near_shares(sheep, np.empty((0, 2)), reach=5.0, close=1.5) == (0.0, 0.0)


def test_replay_reproduces_the_stored_trial_and_refuses_one_that_differs():
    config = config_for(n=25, d=2, layout="wide", ticks=120)
    stored = run_trial(config, 2026)
    label = {"layout": "wide", "n": 25, "d": 2, "role": "D_min", "seed_index": 0}
    row = replay(ReplayJob(config, 2026, stored.success, stored.total_ticks, label))
    assert row["finish_seconds"] == stored.total_ticks * float(config["dt"])
    assert 0.0 <= row["mean_flight_share"] <= row["peak_flight_share"] <= 1.0
    assert row["close_seconds_per_sheep"] <= row["flight_seconds_per_sheep"]
    with pytest.raises(ReplayMismatch):
        replay(ReplayJob(config, 2026, stored.success, stored.total_ticks + 1, label))
