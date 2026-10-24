"""A replay is the stored trial, or it stops."""

from __future__ import annotations

import pytest

from services.replay import ReplayJob, ReplayMismatch, replay_trial
from sim.core.simulation_runner import run_trial
from tests.helpers import config_for


def test_replay_reproduces_the_stored_trial_and_refuses_one_that_differs():
    config = config_for(n=25, d=2, layout="wide", ticks=120)
    stored = run_trial(config, 2026)
    outcome = (stored.success, stored.total_ticks)
    label = {"seed_index": 0}
    result = replay_trial(ReplayJob(config, 2026, outcome, label))
    assert (result.success, result.total_ticks) == outcome
    with pytest.raises(ReplayMismatch):
        replay_trial(ReplayJob(config, 2026, (stored.success, stored.total_ticks + 1), label))
    # a replay with a changed setting carries no stored outcome and is not checked
    replay_trial(ReplayJob(config, 2026, None, label))
