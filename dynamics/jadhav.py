"""Jadhav 2024 topological flocking sheep dynamics."""

from __future__ import annotations

from typing import Any

import numpy as np

from algorithms.flocking_dog.config import FLOCKING_DOG_DEFAULTS
from algorithms.flocking_dog.dynamics import (
    dog_repulsion_unit,
    random_alignment,
    random_attraction,
    sheep_repulsion,
)
from core.agents.sheep import compute_noise, nearest_neighbor_indices, unit_vector
from core.sheep_dynamics import BaseSheepDynamics
from core.simulation_state import SimulationState


class JadhavSheepDynamics(BaseSheepDynamics):
    @property
    def id(self) -> str:
        return "jadhav"

    @property
    def name(self) -> str:
        return "Jadhav Sheep"

    @property
    def default_config(self) -> dict[str, Any]:
        keys = {
            "n_sheep",
            "r_a",
            "r_s",
            "k_neighbors",
            "n_attraction",
            "n_alignment",
            "inertia",
            "sheep_repulsion_weight",
            "dog_repulsion_weight",
            "attraction_weight",
            "alignment_weight",
            "noise_strength",
            "sheep_speed",
            "collect_threshold_scale",
        }
        return {k: FLOCKING_DOG_DEFAULTS[k] for k in keys}

    def step(self, state: SimulationState, config: dict[str, Any]) -> SimulationState:
        n = state.n_sheep
        out = np.zeros((n, 2))
        active = state.shepherd_positions[state.shepherd_active]
        if active.shape[0] == 0:
            return state.copy_with(sheep_velocities=out)

        # Primary dog for interaction distance (paper is single-dog; use nearest).
        r_s = float(config["r_s"])
        r_a = float(config["r_a"])
        k = int(config["k_neighbors"])
        n_att = int(config["n_attraction"])
        n_ali = int(config["n_alignment"])
        h = float(config["inertia"])
        rho_a = float(config["sheep_repulsion_weight"])
        rho_d = float(config["dog_repulsion_weight"])
        c = float(config["attraction_weight"]) * float(
            config.get("cohesion_scale", 1.0)
        )
        alg_w = float(config["alignment_weight"])
        e = float(config["noise_strength"])
        speed = float(config["sheep_speed"])

        for i in range(n):
            dog_dists = np.linalg.norm(active - state.sheep_positions[i], axis=1)
            dog_idx = int(np.argmin(dog_dists))
            dog = active[dog_idx]
            dist_dog = float(dog_dists[dog_idx])
            if dist_dog > r_s:
                continue

            neighbors = nearest_neighbor_indices(state.sheep_positions, i, k)
            atr, atr_idx = random_attraction(
                state.sheep_positions, i, neighbors, n_att, state.rng
            )
            ali = random_alignment(state.sheep_velocities, atr_idx, n_ali, state.rng)
            rep = sheep_repulsion(state.sheep_positions, i, r_a)
            dog_rep = dog_repulsion_unit(state.sheep_positions[i], dog)
            noise = compute_noise(state.rng, e)

            heading = (
                h * unit_vector(state.sheep_velocities[i])
                + rho_a * rep
                + rho_d * dog_rep * float(state.sheep_response[i])
                + c * atr * float(state.sheep_cohesion[i])
                + alg_w * ali
                + noise
            )
            out[i] = unit_vector(heading) * speed

        return state.copy_with(
            sheep_positions=state.sheep_positions + out,
            sheep_velocities=out,
        )
