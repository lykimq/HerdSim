"""Correctness: Kubo force terms match MATLAB reference formulas."""

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


def test_sheep_repulsion_matches_matlab_mean_inv_sq():
    # Two sheep on x-axis; sheep 0 sees sheep 1 at distance 2.
    sheep = np.array([[0.0, 0.0], [2.0, 0.0]])
    vel = np.zeros_like(sheep)
    dogs = np.array([[100.0, 100.0]])
    a, b, c, d = sheep_force_components(0, sheep, vel, dogs, radius=60.0)
    # a = mean((p_i - p_j) / r^2) = (-2,0)/4 = (-0.5, 0)
    assert np.allclose(a, [-0.5, 0.0])
    # c = -mean((p_i - p_j)/r) = -(-2,0)/2 = (1, 0)
    assert np.allclose(c, [1.0, 0.0])
    assert np.allclose(b, 0.0)
    assert np.allclose(d, 0.0)


def test_sheep_dog_repulsion_inv_cube():
    sheep = np.array([[0.0, 0.0], [5.0, 0.0]])
    vel = np.zeros_like(sheep)
    dogs = np.array([[2.0, 0.0]])
    _, _, _, d = sheep_force_components(0, sheep, vel, dogs, radius=60.0)
    # diff = (0-2,0)=(-2,0), |diff|=2, d = (-2,0)/8 = (-0.25, 0)
    assert np.allclose(d, [-0.25, 0.0])


def test_dog_components_attraction_and_inv_cube_repulsion():
    dogs = np.array([[0.0, 0.0], [100.0, 0.0]])  # other dog out of radius 60
    sheep = np.array([[4.0, 0.0], [1.0, 0.0]])
    goal = np.array([-10.0, 0.0])
    a, b, c, d = dog_force_components(0, dogs, sheep, goal, radius=60.0)
    # farthest from goal in range is sheep at x=4
    assert np.allclose(a, [1.0, 0.0])  # unit toward target
    assert np.allclose(b, np.array([-4.0, 0.0]) / (4.0**3))  # inv-cube away
    # C = unit(dog - goal) = (10,0)/10
    assert np.allclose(c, [1.0, 0.0])
    assert np.allclose(d, 0.0)


def test_dog_empty_range_weak_goal_pull():
    dogs = np.array([[10.0, 0.0]])
    sheep = np.array([[100.0, 0.0]])
    goal = np.array([0.0, 0.0])
    a, b, c, d = dog_force_components(0, dogs, sheep, goal, radius=5.0)
    assert np.allclose(a, 0.0)
    assert np.allclose(b, 0.0)
    assert np.allclose(d, 0.0)
    # C = 0.1 * (goal - dog) / |goal - dog|
    expected = 0.1 * (goal - dogs[0]) / np.linalg.norm(goal - dogs[0])
    assert np.allclose(c, expected)


def test_clamp_speed_caps_fast_agents_only():
    vel = np.array([[10.0, 0.0], [1.0, 0.0]])
    out = clamp_speed(vel, 5.0)
    assert np.isclose(np.linalg.norm(out[0]), 5.0)
    assert np.allclose(out[1], [1.0, 0.0])


def test_kubo_step_dogs_see_updated_sheep_positions():
    """Runner updates sheep before dog forces use sheep positions."""
    from controllers.kubo_forces import KuboDogController
    from core.observation_models import GlobalObservation
    from dynamics.kubo import KuboSheepDynamics
    from tests.backend.helpers import make_world

    sheep_dyn = KuboSheepDynamics()
    dogs = KuboDogController()
    cfg = {**sheep_dyn.default_config, **dogs.default_config, "dt": 0.05, "radius": 60.0}
    state = make_state(
        [[40.0, 40.0], [42.0, 40.0], [40.0, 42.0]],
        [[55.0, 40.0], [58.0, 45.0]],
        world=make_world(),
        seed=0,
    )
    mid = sheep_dyn.step(state, cfg)
    obs = GlobalObservation().observe_all(mid, cfg)
    new_state = dogs.step(mid, obs, cfg)
    assert not np.allclose(mid.sheep_positions, state.sheep_positions)
    assert new_state.shepherd_positions.shape == state.shepherd_positions.shape
