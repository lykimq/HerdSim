"""Holding (hold time, withdrawal) and dog spacing."""

from __future__ import annotations

from dataclasses import replace

import numpy as np
import pytest

from sim.core.simulation_runner import run_trial
from sim.core.vectors import unit_rows
from sim.plugins.dogs.collect_drive_multi import withdraw_targets
from sim.plugins.dogs.helpers import spaced
from sim.plugins.scenarios.drive_to_goal import is_success
from tests.helpers import config_for, make_state, make_world


def test_success_waits_for_the_hold_and_restarts_when_the_flock_leaves():
    world = make_world(goal_center=(0.0, 0.0), goal_radius=5.0)
    world = replace(world, goal=replace(world.goal, hold_ticks=3))
    inside, outside = np.zeros((4, 2)), np.full((4, 2), 50.0)
    state = make_state(inside, [[30.0, 0.0]], world=world)
    seen = []
    for tick, sheep in enumerate([inside, inside, outside, inside, inside, inside, inside]):
        state.tick, state.sheep_positions = tick, sheep
        seen.append(is_success(state))
    # Reached at tick 0, left at tick 2, reached again at tick 3: 3 ticks later is tick 6.
    assert seen == [False, False, False, False, False, False, True]


def test_no_hold_and_no_spacing_leave_the_trial_unchanged():
    base = config_for(n=60, d=4, layout="wide", ticks=200)
    explicit = {**base, "hold_ticks": 0, "hold_withdraw": False, "dog_spacing": 0.0}
    a, b = run_trial(base, 2026), run_trial(explicit, 2026)
    np.testing.assert_array_equal(a.history.to_numpy(), b.history.to_numpy())


def test_withdrawn_dogs_stand_beyond_the_reaction_distance_of_every_sheep():
    config = config_for(n=40, d=5)
    rng = np.random.default_rng(3)
    flock = rng.normal(0.0, 4.0, size=(40, 2))
    dogs = rng.normal(0.0, 20.0, size=(5, 2))
    targets = withdraw_targets(flock, dogs, config)
    nearest = np.min(np.linalg.norm(flock[:, None, :] - targets[None, :, :], axis=2), axis=0)
    # r_a beyond r_s, so a dog jittering by one step (delta_s = 1.5 < r_a = 2) stays outside it.
    assert np.all(nearest >= config["reaction_radius"] + config["r_a"] - 1e-9)
    centre = flock.mean(axis=0)
    bearing, along = unit_rows(dogs - centre), unit_rows(targets - centre)
    np.testing.assert_allclose(bearing, along)


def test_dogs_keep_their_spacing():
    dogs = np.array([[0.0, 0.0], [1.0, 0.0], [10.0, 0.0], [13.0, 0.0]])
    steps = np.array([[0.0, 0.0], [0.0, 1.5], [1.5, 0.0], [0.0, 1.5]])
    out = spaced(dogs, steps, spacing=2.0, speed=1.5, dt=1.0)
    np.testing.assert_allclose(out[0], [-1.5, 0.0])  # too close: walks away, stop rule or not
    np.testing.assert_array_equal(out[1], steps[1])  # dog 0 has moved off: dog 1 is free
    np.testing.assert_array_equal(out[2], [0.0, 0.0])  # would step to 1.5 from dog 3: waits
    np.testing.assert_array_equal(out[3], steps[3])  # free to step (dog 2 stayed 3 away)
    np.testing.assert_array_equal(spaced(dogs, steps, spacing=0.0, speed=1.5, dt=1.0), steps)


def test_a_crowded_drive_keeps_the_dogs_apart():
    config = config_for(n=100, d=16, layout="compact", ticks=150, settings={"dog_spacing": 2.0})
    closest = []
    run_trial(config, 2026, on_tick=lambda s: closest.append(_closest_pair(s.shepherd_positions)))
    assert min(closest[20:]) >= 2.0 - 1e-9  # once apart, no dog steps into another's space


def _closest_pair(dogs: np.ndarray) -> float:
    d = np.linalg.norm(dogs[:, None, :] - dogs[None, :, :], axis=2)
    return float(d[~np.eye(len(dogs), dtype=bool)].min())


@pytest.mark.parametrize(
    ("method", "settings"),
    [("fat", {"hold_withdraw": True}), ("kubo", {"dog_spacing": 2.0})],
)
def test_settings_a_dog_rule_cannot_use_are_refused(method, settings):
    with pytest.raises(ValueError):
        config_for(method, settings=settings)
