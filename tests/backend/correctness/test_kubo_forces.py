"""Correctness: Kubo force selection and multi-dog terms."""

from __future__ import annotations

import numpy as np

from algorithms.kubo.forces import (
    clamp_speed,
    dog_force_components,
    sheep_force_components,
    target_sheep_farthest_from_goal,
)
from algorithms.registry import algorithm_registry
from tests.backend.helpers import make_state


def test_kubo_registered_with_force_gains():
    alg = algorithm_registry.get("kubo")
    assert alg.id == "kubo"
    assert {"K_f4", "K_s4", "radius"} <= set(alg.default_config)


def test_target_sheep_is_farthest_from_goal():
    goal = np.array([0.0, 0.0])
    sheep = np.array([[1.0, 0.0], [10.0, 0.0], [3.0, 0.0]])
    assert np.allclose(target_sheep_farthest_from_goal(goal, sheep), [10.0, 0.0])


def test_sheep_dog_repulsion_nonzero_when_dog_nearby():
    state = make_state(
        [[40.0, 40.0], [45.0, 42.0], [38.0, 50.0]],
        [[42.0, 42.0]],
    )
    _, _, _, d = sheep_force_components(
        0,
        state.sheep_positions,
        state.sheep_velocities,
        state.shepherd_positions,
        radius=60.0,
    )
    assert np.linalg.norm(d) > 0


def test_dog_dog_repulsion_nonzero_with_asymmetric_spacing():
    dogs = np.array([[60.0, 60.0], [68.0, 58.0], [52.0, 70.0]])
    sheep = np.array([[40.0, 40.0], [45.0, 42.0]])
    _, _, _, d_i = dog_force_components(0, dogs, sheep, np.array([15.0, 15.0]), radius=60.0)
    assert np.linalg.norm(d_i) > 0


def test_clamp_speed_caps_fast_agents_only():
    vel = np.array([[10.0, 0.0], [1.0, 0.0]])
    out = clamp_speed(vel, 5.0)
    assert np.isclose(np.linalg.norm(out[0]), 5.0)
    assert np.allclose(out[1], [1.0, 0.0])
