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


def test_flocking_dog_step_moves_agents():
    alg = FlockingDogAlgorithm()
    state = make_state(
        [[40.0, 40.0], [45.0, 42.0], [38.0, 48.0]],
        [[70.0, 70.0]],
        world=make_world(),
        seed=0,
    )
    new_state = alg.step(state, alg.default_config)
    assert not np.allclose(new_state.sheep_positions, state.sheep_positions)
    assert not np.allclose(new_state.shepherd_positions, state.shepherd_positions)
