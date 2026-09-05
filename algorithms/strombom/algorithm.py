"""Strömbom 2014 herding algorithm implementation.

Reference: Strömbom et al., "Solving the shepherding problem:
heuristics for herding autonomous, interacting agents",
J. Royal Soc. Interface, vol. 11, no. 100, 2014.

A single shepherd switches between Collect and Drive modes based on
flock cohesion. Sheep respond to attraction (local centroid), repulsion
(neighbours + shepherd), inertia, and noise.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from algorithms.strombom.config import STROMBOM_DEFAULTS
from algorithms.strombom.heuristics import compute_shepherd_velocity
from core.agents.sheep import (
    compute_attraction,
    compute_local_centroid,
    compute_noise,
    compute_repulsion_from_neighbours,
    compute_repulsion_from_shepherds,
)
from core.base_algorithm import BaseAlgorithm
from core.simulation_state import SimulationState


class StrombomAlgorithm(BaseAlgorithm):
    """Strömbom 2014 Collect/Drive shepherding algorithm."""

    @property
    def id(self) -> str:
        return "strombom"

    @property
    def name(self) -> str:
        return "Strömbom 2014"

    @property
    def default_config(self) -> dict[str, Any]:
        return STROMBOM_DEFAULTS.copy()

    def step(self, state: SimulationState, config: dict[str, Any]) -> SimulationState:
        new_sheep_vel = self._update_sheep(state, config)
        new_shepherd_vel = self._update_shepherds(state, config)

        new_sheep_pos = state.sheep_positions + new_sheep_vel
        new_shepherd_pos = state.shepherd_positions + new_shepherd_vel

        new_sheep_pos = state.world.reflect_positions(new_sheep_pos)
        new_shepherd_pos = state.world.reflect_positions(new_shepherd_pos)
        new_sheep_vel = state.world.reflect_velocities(new_sheep_pos, new_sheep_vel)
        new_shepherd_vel = state.world.reflect_velocities(
            new_shepherd_pos, new_shepherd_vel
        )

        metadata = dict(state.metadata)
        metadata["r_a"] = float(config.get("r_a", metadata.get("r_a", 2.0)))

        return SimulationState(
            tick=state.tick,
            sheep_positions=new_sheep_pos,
            sheep_velocities=new_sheep_vel,
            shepherd_positions=new_shepherd_pos,
            shepherd_velocities=new_shepherd_vel,
            world=state.world,
            rng=state.rng,
            metadata=metadata,
        )

    def _update_sheep(self, state: SimulationState, config: dict) -> np.ndarray:
        """Compute new velocities for all sheep."""
        n = state.n_sheep
        velocities = np.zeros((n, 2))
        r_a = config["r_a"]
        r_s = config["r_s"]
        r_n = config["r_n"]
        c = config["c"]
        noise_str = config["noise_strength"]
        speed = config["sheep_speed"]
        inertia = config["inertia"]

        for i in range(n):
            lcm = compute_local_centroid(state.sheep_positions, i, r_n)
            attraction = compute_attraction(state.sheep_positions[i], lcm)
            repulsion_sheep = compute_repulsion_from_neighbours(
                state.sheep_positions, i, r_a
            )
            repulsion_shep = compute_repulsion_from_shepherds(
                state.sheep_positions[i], state.shepherd_positions, r_s
            )
            noise = compute_noise(state.rng, noise_str)

            desired = c * attraction + repulsion_sheep + repulsion_shep + noise
            blended = inertia * state.sheep_velocities[i] + (1 - inertia) * desired

            norm = np.linalg.norm(blended)
            if norm > 1e-10:
                velocities[i] = (blended / norm) * speed
        return velocities

    def _update_shepherds(self, state: SimulationState, config: dict) -> np.ndarray:
        """Compute new velocities for all shepherds."""
        velocities = np.zeros_like(state.shepherd_positions)
        for i in range(state.n_shepherds):
            velocities[i] = compute_shepherd_velocity(state, config, i)
        return velocities
