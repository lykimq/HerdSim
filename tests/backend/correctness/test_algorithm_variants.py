"""Correctness: algorithm variants keep distinct herding behaviour."""

from __future__ import annotations

import numpy as np

from algorithms.flocking_dog.algorithm import FlockingDogAlgorithm
from algorithms.registry import algorithm_registry
from algorithms.strombom_multi.algorithm import StrombomMultiAlgorithm
from algorithms.strombom_noise.algorithm import StrombomNoiseAlgorithm
from tests.backend.helpers import make_state, make_world


def test_variants_registered():
    names = set(algorithm_registry.names())
    assert {"strombom_multi", "strombom_noise", "flocking_dog"} <= names


def test_strombom_noise_default_strength():
    assert StrombomNoiseAlgorithm().default_config["noise_strength"] >= 0.8


def test_strombom_multi_dogs_take_distinct_positions():
    alg = StrombomMultiAlgorithm()
    world = make_world()
    sheep = [
        [50.0, 50.0],
        [80.0, 50.0],
        [50.0, 90.0],
        [55.0, 52.0],
        [48.0, 55.0],
    ]
    dogs = [[100.0, 100.0], [110.0, 90.0], [90.0, 110.0]]
    state = make_state(sheep, dogs, world=world, seed=1)
    new_state = alg.step(state, alg.default_config)
    uniq = {tuple(np.round(p, 3)) for p in new_state.shepherd_positions}
    assert len(uniq) == 3


def test_strombom_multi_stops_within_three_ra():
    """Multi-dog shepherds use the same 3*r_a stop as Strombom 2014."""
    alg = StrombomMultiAlgorithm()
    cfg = alg.default_config
    sheep = np.array([[50.0, 50.0], [52.0, 50.0], [50.0, 52.0]])
    # All three dogs closer than 3*r_a = 6 to some sheep.
    dogs = np.array([[51.0, 50.5], [50.5, 51.0], [51.5, 51.5]])
    state = make_state(sheep, dogs, world=make_world(), seed=1)
    new_state = alg.step(state, cfg)
    assert np.allclose(new_state.shepherd_velocities, 0.0)


def test_strombom_multi_applies_shepherd_noise():
    """With noise on and stop disabled, multi-dog headings are not pure aim."""
    alg = StrombomMultiAlgorithm()
    cfg = {
        **alg.default_config,
        "noise_strength": 1.0,
        "shepherd_stop_multiple": 0.0,
        "n_shepherds": 1,
    }
    sheep = np.array([[40.0, 40.0], [42.0, 40.0], [40.0, 42.0], [41.0, 41.0]])
    dog = np.array([[80.0, 40.0]])
    state = make_state(sheep, dog, world=make_world(goal_center=(0.0, 0.0)), seed=7)
    # Two steps with same seed path: with noise, velocity should be non-zero
    # and not exactly along the geometric aim vector alone across RNG draws.
    v0 = alg._update_shepherds(state, cfg)[0]
    state2 = make_state(sheep, dog, world=make_world(goal_center=(0.0, 0.0)), seed=99)
    v1 = alg._update_shepherds(state2, cfg)[0]
    assert np.linalg.norm(v0) > 0
    assert np.linalg.norm(v1) > 0
    assert not np.allclose(v0, v1)


def test_flocking_dog_step_moves_agents():
    alg = FlockingDogAlgorithm()
    # Dog within Rd so sheep are active (not grazing).
    state = make_state(
        [[40.0, 40.0], [42.0, 40.0], [40.0, 42.0]],
        [[48.0, 41.0]],
        world=make_world(),
        seed=0,
    )
    state.sheep_velocities[:] = [[0.0, 1.0], [0.0, 1.0], [0.0, 1.0]]
    new_state = alg.step(state, alg.default_config)
    assert not np.allclose(new_state.sheep_positions, state.sheep_positions)
    assert not np.allclose(new_state.shepherd_positions, state.shepherd_positions)
