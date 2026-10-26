"""Local sensing range limits and inter-shepherd communication pooling."""

from __future__ import annotations

import numpy as np
import pytest

from sim.core.simulation_runner import run_trial
from sim.plugins.dogs.collect_drive_multi import known_sheep, local_targets
from tests.helpers import config_for, make_state


@pytest.mark.parametrize("communication", ["none", "neighbour", "shared"])
def test_a_range_beyond_the_field_is_the_global_trial(communication):
    base = config_for(n=60, d=4, layout="wide", ticks=200)
    wide_view = {**base, "sensing_range": 1e6, "communication": communication}
    a, b = run_trial(base, 2026), run_trial(wide_view, 2026)
    np.testing.assert_array_equal(a.history.to_numpy(), b.history.to_numpy())


def test_views_are_pooled_as_the_communication_setting_says():
    sheep = np.array([[0.0, 0.0], [100.0, 0.0], [200.0, 0.0]])
    dogs = np.array([[1.0, 0.0], [20.0, 0.0], [199.0, 0.0]])
    config = {"sensing_range": 25.0}
    own = known_sheep(sheep, dogs, {**config, "communication": "none"})
    assert own.tolist() == [[True, False, False], [True, False, False], [False, False, True]]
    near = known_sheep(sheep, dogs, {**config, "communication": "neighbour"})
    assert near[1].tolist() == [True, False, False]  # hears dog 0, which sees sheep 0
    shared = known_sheep(sheep, dogs, {**config, "communication": "shared"})
    assert shared.tolist() == [[True, False, True]] * 3


def test_a_dog_that_knows_no_sheep_goes_to_the_centre_it_last_knew():
    config = {**config_for(n=3, d=1), "sensing_range": 5.0, "communication": "none"}
    state = make_state([[50.0, 50.0], [51.0, 50.0], [50.0, 51.0]], [[0.0, 0.0]])
    first = local_targets(state, config)
    np.testing.assert_array_equal(first[0], config["flock_center"])
    state.shepherd_positions = np.array([[50.0, 48.0]])  # now sees all three sheep
    local_targets(state, config)
    state.shepherd_positions = np.array([[0.0, 0.0]])  # and loses it again
    np.testing.assert_allclose(local_targets(state, config)[0], [50 + 1 / 3, 50 + 1 / 3])


@pytest.mark.parametrize(
    ("method", "settings"),
    [
        ("fat", {"sensing_range": 30.0}),
        ("strombom_multi", {"sensing_range": 30.0, "hold_withdraw": True}),
        ("strombom_multi", {"communication": "radio"}),
    ],
)
def test_sensing_settings_that_do_not_fit_are_refused(method, settings):
    with pytest.raises(ValueError):
        config_for(method, settings=settings)
