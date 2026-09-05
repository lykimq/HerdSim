"""Flocking Dog 2024 inspired reciprocal herding algorithm.

Reference:
Collective responses of flocking sheep to a herding dog,
Communications Biology, 2024.
https://doi.org/10.1038/s42003-024-07245-8

This is a simplified runnable model capturing reciprocal dog-sheep coupling
and front-to-back information flow, not a full UWB data replay.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from algorithms.flocking_dog.config import FLOCKING_DOG_DEFAULTS
from algorithms.flocking_dog.dynamics import (
    alignment_force,
    front_biased_dog_coupling,
    unit,
)
from algorithms.strombom.heuristics import (
    collect_target,
    drive_target,
    should_collect,
)
from core.agents.sheep import (
    compute_attraction,
    compute_local_centroid,
    compute_noise,
    compute_repulsion_from_neighbours,
    compute_repulsion_from_shepherds,
)
from core.agents.shepherd import move_toward
from core.base_algorithm import BaseAlgorithm
from core.simulation_state import SimulationState


class FlockingDogAlgorithm(BaseAlgorithm):
    """Reciprocal flocking-dog herding with Collect/Drive shepherding."""

    @property
    def id(self) -> str:
        return "flocking_dog"

    @property
    def name(self) -> str:
        return "Flocking Dog 2024"

    @property
    def default_config(self) -> dict[str, Any]:
        return FLOCKING_DOG_DEFAULTS.copy()

    def step(self, state: SimulationState, config: dict[str, Any]) -> SimulationState:
        sheep_vel = self._update_sheep(state, config)
        dog_vel = self._update_dogs(state, config)

        sheep_pos = state.world.reflect_positions(state.sheep_positions + sheep_vel)
        dog_pos = state.world.reflect_positions(state.shepherd_positions + dog_vel)
        sheep_vel = state.world.reflect_velocities(sheep_pos, sheep_vel)
        dog_vel = state.world.reflect_velocities(dog_pos, dog_vel)

        metadata = dict(state.metadata)
        metadata["r_a"] = float(config.get("r_a", 3.0))

        return SimulationState(
            tick=state.tick,
            sheep_positions=sheep_pos,
            sheep_velocities=sheep_vel,
            shepherd_positions=dog_pos,
            shepherd_velocities=dog_vel,
            world=state.world,
            rng=state.rng,
            metadata=metadata,
        )

    def _update_sheep(self, state: SimulationState, config: dict) -> np.ndarray:
        n = state.n_sheep
        out = np.zeros((n, 2))
        dog = state.shepherd_positions[0] if state.n_shepherds else np.zeros(2)
        for i in range(n):
            lcm = compute_local_centroid(state.sheep_positions, i, config["r_n"])
            attraction = compute_attraction(state.sheep_positions[i], lcm)
            repulsion = compute_repulsion_from_neighbours(
                state.sheep_positions, i, config["r_a"]
            )
            align = alignment_force(
                state.sheep_positions, state.sheep_velocities, i, config["r_n"]
            )
            dog_rep = compute_repulsion_from_shepherds(
                state.sheep_positions[i], state.shepherd_positions, config["r_s"]
            )
            couple = front_biased_dog_coupling(
                state.sheep_positions[i],
                state.sheep_velocities[i],
                dog,
                config["r_s"],
                config["front_bias"],
            )
            noise = compute_noise(state.rng, config["noise_strength"])
            desired = (
                config["c"] * attraction
                + repulsion
                + config["alignment_weight"] * align
                + config["dog_repulsion"] * dog_rep
                + config["sheep_attraction_to_dog"] * couple
                + noise
            )
            blended = (
                config["inertia"] * state.sheep_velocities[i]
                + (1.0 - config["inertia"]) * desired
            )
            direction = unit(blended)
            out[i] = direction * config["sheep_speed"]
        return out

    def _update_dogs(self, state: SimulationState, config: dict) -> np.ndarray:
        out = np.zeros_like(state.shepherd_positions)
        for i in range(state.n_shepherds):
            if should_collect(state, config):
                target = collect_target(state, config)
            else:
                target = drive_target(state, config)
            # Mild reciprocal pull toward flock front sheep.
            centroid = state.sheep_centroid
            to_front = unit(centroid - state.shepherd_positions[i])
            base = move_toward(
                state.shepherd_positions[i], target, config["shepherd_speed"]
            )
            out[i] = base + config["drive_gain"] * 0.15 * to_front * config[
                "shepherd_speed"
            ]
        return out
