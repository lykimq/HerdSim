"""Correctness: experimental factors and observation models."""

from __future__ import annotations

import numpy as np
import pytest

from core.agent_attributes import apply_failure_factors, init_agent_attributes
from core.experimental_factors import ExperimentalFactors
from core.observation_models import (
    BearingOnlyObservation,
    GlobalObservation,
    LocalPositionsObservation,
    NoisyBearingObservation,
)
from core.experiment_config import resolve_experiment_config
from scenarios.drive_to_goal import DriveToGoalScenario
from tests.backend.helpers import make_state, make_world


def test_factors_validate_obs_mode():
    with pytest.raises(ValueError, match="observation mode"):
        ExperimentalFactors.from_dict({"obs_mode": "telepathy"})


def test_resolve_sets_obs_and_stubborn_factors():
    config = resolve_experiment_config(
        scenario=DriveToGoalScenario(),
        instrument="strombom",
        preset="custom",
        num_sheep=10,
        num_shepherds=2,
        algorithm_params={
            "obs_mode": "bearing_only",
            "stubborn_fraction": 0.4,
            "sensing_range": 33.0,
        },
    )
    assert config["obs_mode"] == "bearing_only"
    assert config["stubborn_fraction"] == 0.4
    assert config["sensing_range"] == 33.0
    assert config["sheep_model"] == "strombom"
    assert config["dog_controller"] == "collect_drive"


def test_local_observation_filters_by_range():
    state = make_state(
        [[0.0, 0.0], [100.0, 0.0]],
        [[0.0, 0.0]],
        world=make_world(),
        seed=1,
    )
    obs = LocalPositionsObservation().observe(
        state, 0, {"sensing_range": 10.0, "r_s": 10.0}
    )
    assert obs.n_sheep_seen == 1
    assert obs.mode == "local_positions"


def test_bearing_only_hides_metric_distances():
    state = make_state(
        [[5.0, 0.0], [0.0, 5.0]],
        [[0.0, 0.0]],
        world=make_world(),
        seed=1,
    )
    obs = BearingOnlyObservation().observe(
        state, 0, {"sensing_range": 20.0, "r_s": 20.0}
    )
    assert obs.n_sheep_seen == 2
    assert obs.distances_to_sheep is None
    assert obs.bearings_to_sheep is not None


def test_noisy_bearing_changes_angles():
    state = make_state(
        [[5.0, 0.0]],
        [[0.0, 0.0]],
        world=make_world(),
        seed=1,
    )
    clean = BearingOnlyObservation().observe(
        state, 0, {"sensing_range": 20.0, "r_s": 20.0}
    )
    noisy = NoisyBearingObservation().observe(
        state, 0, {"sensing_range": 20.0, "r_s": 20.0, "noise_sigma": 0.5}
    )
    assert clean.bearings_to_sheep is not None
    assert noisy.bearings_to_sheep is not None
    assert not np.allclose(clean.bearings_to_sheep, noisy.bearings_to_sheep)


def test_global_observation_sees_all():
    state = make_state(
        [[1.0, 1.0], [2.0, 2.0], [3.0, 3.0]],
        [[0.0, 0.0]],
        world=make_world(),
        seed=0,
    )
    obs = GlobalObservation().observe(state, 0, {})
    assert obs.n_sheep_seen == 3


def test_failure_inactive_after_tick():
    state = make_state(
        [[40.0, 40.0]],
        [[50.0, 50.0], [60.0, 60.0]],
        world=make_world(),
        seed=0,
        tick=5,
    )
    state = init_agent_attributes(state, {"speed_scale": 1.0})
    failed = apply_failure_factors(
        state, {"failure_mode": "inactive_after_tick", "failure_tick": 5}
    )
    assert bool(failed.shepherd_active[0])
    assert not bool(failed.shepherd_active[1])
