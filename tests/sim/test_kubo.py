"""Kubo 2022 forces: vectorised sheep step, goal-term sign, target rule."""

from __future__ import annotations

import numpy as np
import pytest

from sim.methods.kubo.forces import clamp_speed, dog_velocity, sheep_velocities
from sim.plugins.dogs import kubo_forces
from tests.helpers import config_for, make_state, make_world

CONFIG = config_for("kubo", n=20, d=2)
EPS = 1e-6


def _reference(positions, velocities, dogs, cfg):
    """Per-sheep loop of eqs. 2-6, one sheep at a time."""
    radius = cfg["sheep_radius"]
    out = np.zeros_like(positions)
    for i, x in enumerate(positions):
        dist = np.linalg.norm(x - positions, axis=1)
        nb = (dist < radius) & (dist > 0)
        a = b = c = np.zeros(2)
        if nb.any():
            diff = x - positions[nb]
            dd = np.maximum(np.linalg.norm(diff, axis=1), EPS)[:, None]
            a = np.mean(diff / dd**2, axis=0)
            c = -np.mean(diff / dd, axis=0)
            vel = velocities[nb]
            speed = np.linalg.norm(vel, axis=1)
            if np.any(speed > 0):
                b = np.mean(vel[speed > 0] / speed[speed > 0, None], axis=0)
        ddog = np.linalg.norm(x - dogs, axis=1)
        d = np.zeros(2)
        if np.any(ddog < radius):
            diff = x - dogs[ddog < radius]
            d = np.mean(diff / np.maximum(np.linalg.norm(diff, axis=1), EPS)[:, None] ** 3, axis=0)
        out[i] = cfg["K_s1"] * a + cfg["K_s2"] * b + cfg["K_s3"] * c + cfg["K_s4"] * d
    return clamp_speed(out, cfg["sheep_speed_max"])


def test_vectorised_sheep_match_reference():
    rng = np.random.default_rng(5)
    positions = rng.normal(0.0, 8.0, size=(40, 2))
    velocities = rng.normal(0.0, 1.0, size=(40, 2))
    velocities[:5] = 0.0  # stationary neighbours are left out of the alignment mean
    dogs = np.array([[5.0, 5.0], [40.0, 0.0]])
    np.testing.assert_allclose(
        sheep_velocities(positions, velocities, dogs, CONFIG),
        _reference(positions, velocities, dogs, CONFIG),
        atol=1e-10,
    )


def test_goal_term_pushes_the_dog_away_from_the_goal():
    cfg = {**CONFIG, "K_f1": 0.0, "K_f2": 0.0, "K_f3": 1.0, "K_f4": 0.0}
    v = dog_velocity(
        np.array([10.0, 0.0]), np.array([50.0, 50.0]), np.zeros(2), np.zeros((0, 2)), cfg
    )
    np.testing.assert_allclose(v, [1.0, 0.0])


def test_sheep_ignore_dogs_beyond_their_field_of_view():
    positions = np.array([[0.0, 0.0], [3.0, 0.0]])
    velocities = np.zeros((2, 2))
    far = np.array([[3.0 + CONFIG["sheep_radius"] + 1.0, 0.0]])  # beyond reach of both sheep
    np.testing.assert_allclose(
        sheep_velocities(positions, velocities, far, CONFIG),
        sheep_velocities(positions, velocities, np.zeros((0, 2)), CONFIG),
    )


def test_a_dog_targets_the_sheep_farthest_from_the_goal_however_far_it_is():
    world = make_world(width=500.0, height=500.0, goal_center=(0.0, 0.0), goal_radius=5.0)
    sheep = np.array([[50.0, 0.0], [200.0, 200.0]])  # the second is farthest from the goal
    state = make_state(sheep, [[100.0, 100.0]], world=world)
    moved = kubo_forces.step(state, {**CONFIG, "K_f3": 0.0, "K_f4": 0.0})
    step = moved.shepherd_positions[0] - state.shepherd_positions[0]
    toward = np.array([200.0, 200.0]) - state.shepherd_positions[0]
    assert np.dot(step, toward) > 0.0


def test_seconds_time_limit_converts_with_dt():
    from tests.helpers import BASE_PROTOCOL

    kubo = next(m for m in BASE_PROTOCOL.methods if m.name == "kubo")
    assert kubo.time_limit_ticks == pytest.approx(500 / CONFIG["dt"])  # unit.yaml: 500 s
