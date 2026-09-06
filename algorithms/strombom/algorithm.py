"""Strombom 2014 herding algorithm.

Collect/Drive shepherding (Strombom et al., J. R. Soc. Interface 2014).
Sheep: topological LCM attraction, neighbour/shepherd repulsion, inertia, noise;
graze when beyond r_s.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from algorithms.strombom.config import STROMBOM_DEFAULTS
from algorithms.strombom.heuristics import compute_shepherd_velocity
from core.agents.sheep import (
    compose_strombom_heading,
    compute_attraction,
    compute_local_centroid_knn,
    compute_noise,
    compute_repulsion_from_neighbours,
    compute_repulsion_from_shepherds,
    unit_vector,
)
from core.base_algorithm import BaseAlgorithm
from core.simulation_state import SimulationState


class StrombomAlgorithm(BaseAlgorithm):
    """Strombom 2014 Collect/Drive shepherding algorithm."""

    @property
    def id(self) -> str:
        return "strombom"

    @property
    def name(self) -> str:
        return "Strombom 2014"

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
        metadata["collect_threshold_scale"] = float(
            config.get(
                "collect_threshold_scale",
                metadata.get("collect_threshold_scale", 1.0),
            )
        )

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
        """Paper sheep update: graze beyond r_s; else eq. (4.2)-(4.3)."""
        n = state.n_sheep
        velocities = np.zeros((n, 2))
        r_a = float(config["r_a"])
        r_s = float(config["r_s"])
        n_neighbors = int(config.get("n_neighbors", -1))
        c = float(config["c"])
        ra_weight = float(config.get("ra_weight", r_a))
        rs_weight = float(config.get("rs_weight", 1.0))
        noise_str = float(config["noise_strength"])
        speed = float(config["sheep_speed"])
        inertia = float(config["inertia"])
        graze_p = float(config.get("graze_move_prob", 0.05))

        for i in range(n):
            min_shep_dist = (
                float(
                    np.min(
                        np.linalg.norm(
                            state.shepherd_positions - state.sheep_positions[i],
                            axis=1,
                        )
                    )
                )
                if state.n_shepherds
                else float("inf")
            )

            if min_shep_dist > r_s:
                if state.rng.random() < graze_p:
                    velocities[i] = unit_vector(compute_noise(state.rng, 1.0)) * speed
                continue

            lcm = compute_local_centroid_knn(state.sheep_positions, i, n_neighbors)
            attraction = compute_attraction(state.sheep_positions[i], lcm)
            repulsion_sheep = compute_repulsion_from_neighbours(
                state.sheep_positions, i, r_a
            )
            repulsion_shep = compute_repulsion_from_shepherds(
                state.sheep_positions[i], state.shepherd_positions, r_s
            )
            noise = compute_noise(state.rng, noise_str)
            heading = compose_strombom_heading(
                state.sheep_velocities[i],
                attraction,
                repulsion_sheep,
                repulsion_shep,
                noise,
                inertia=inertia,
                c=c,
                ra_weight=ra_weight,
                rs_weight=rs_weight,
            )
            velocities[i] = heading * speed
        return velocities

    def _update_shepherds(self, state: SimulationState, config: dict) -> np.ndarray:
        """Compute new velocities for all shepherds."""
        velocities = np.zeros_like(state.shepherd_positions)
        for i in range(state.n_shepherds):
            velocities[i] = compute_shepherd_velocity(state, config, i)
        return velocities
