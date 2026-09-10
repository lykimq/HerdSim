"""Strombom 2014 sheep dynamics."""

from __future__ import annotations

from typing import Any

import numpy as np

from algorithms.strombom.config import STROMBOM_DEFAULTS
from core.agents.sheep import (
    compose_strombom_heading,
    compute_attraction,
    compute_local_centroid_knn,
    compute_noise,
    compute_repulsion_from_neighbours,
    compute_repulsion_from_shepherds,
    unit_vector,
)
from core.sheep_dynamics import BaseSheepDynamics
from core.simulation_state import SimulationState


class StrombomSheepDynamics(BaseSheepDynamics):
    @property
    def id(self) -> str:
        return "strombom"

    @property
    def name(self) -> str:
        return "Strombom Sheep"

    @property
    def default_config(self) -> dict[str, Any]:
        return {
            k: v
            for k, v in STROMBOM_DEFAULTS.items()
            if k
            not in {
                "n_shepherds",
                "shepherd_speed",
                "shepherd_stop_multiple",
            }
        }

    def step(self, state: SimulationState, config: dict[str, Any]) -> SimulationState:
        n = state.n_sheep
        velocities = np.zeros((n, 2))
        r_a = float(config["r_a"])
        r_s = float(config["r_s"])
        n_neighbors = int(config.get("n_neighbors", -1))
        c = float(config["c"]) * float(config.get("cohesion_scale", 1.0))
        ra_weight = float(config.get("ra_weight", r_a))
        rs_weight = float(config.get("rs_weight", 1.0))
        noise_str = float(config["noise_strength"])
        speed = float(config["sheep_speed"])
        inertia = float(config["inertia"])
        graze_p = float(config.get("graze_move_prob", 0.05))
        response = state.sheep_response
        cohesion = state.sheep_cohesion

        for i in range(n):
            min_shep_dist = (
                float(
                    np.min(
                        np.linalg.norm(
                            state.shepherd_positions[state.shepherd_active]
                            - state.sheep_positions[i],
                            axis=1,
                        )
                    )
                )
                if np.any(state.shepherd_active)
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
            active_dogs = state.shepherd_positions[state.shepherd_active]
            repulsion_shep = compute_repulsion_from_shepherds(
                state.sheep_positions[i], active_dogs, r_s
            )
            noise = compute_noise(state.rng, noise_str)
            sheep_c = float(c) * float(cohesion[i])
            sheep_rs = float(rs_weight) * float(response[i])
            heading = compose_strombom_heading(
                state.sheep_velocities[i],
                attraction,
                repulsion_sheep,
                repulsion_shep,
                noise,
                inertia=inertia,
                c=sheep_c,
                ra_weight=ra_weight,
                rs_weight=sheep_rs,
            )
            velocities[i] = heading * speed

        return state.copy_with(
            sheep_positions=state.sheep_positions + velocities,
            sheep_velocities=velocities,
        )
