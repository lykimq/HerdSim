"""Strombom 2014 sheep motion (sheep_model=strombom).

Beyond shepherd range r_s, sheep graze: usually stay still, sometimes take a
random step. Within r_s they update heading from inertia, attraction to the
local neighbour centre, sheep-sheep repulsion inside r_a, repulsion from
shepherds, and angular noise, then advance by sheep_speed (displacement per
tick). Used by the Strombom-family methods; the dog side is a separate
controller (multi-dog Collect/Drive or FAT).
"""

from __future__ import annotations

from typing import Any

import numpy as np
from core.simulation_state import SimulationState

from .helpers import (
    compose_strombom_heading,
    compute_attraction,
    compute_local_centroid_knn,
    compute_noise,
    compute_repulsion_from_neighbours,
    compute_repulsion_from_shepherds,
    unit_vector,
)


def step(state: SimulationState, config: dict[str, Any]) -> SimulationState:
    n = state.n_sheep
    velocities = np.zeros((n, 2))
    r_a = float(config["r_a"])
    r_s = float(config["r_s"])
    n_neighbors = int(config["n_neighbors"])
    c = float(config["c"])
    # Paper uses r_a as both the repulsion distance and its weight.
    ra_weight = r_a
    rs_weight = float(config["rs_weight"])
    noise_str = float(config["noise_strength"])
    speed = float(config["sheep_speed"])
    inertia = float(config["inertia"])
    graze_p = float(config["graze_move_prob"])
    dogs = state.shepherd_positions

    for i in range(n):
        min_shep_dist = (
            float(np.min(np.linalg.norm(dogs - state.sheep_positions[i], axis=1)))
            if len(dogs)
            else float("inf")
        )

        if min_shep_dist > r_s:
            if state.rng.random() < graze_p:
                velocities[i] = unit_vector(compute_noise(state.rng, 1.0)) * speed
            continue

        lcm = compute_local_centroid_knn(state.sheep_positions, i, n_neighbors)
        attraction = compute_attraction(state.sheep_positions[i], lcm)
        repulsion_sheep = compute_repulsion_from_neighbours(state.sheep_positions, i, r_a)
        repulsion_shep = compute_repulsion_from_shepherds(state.sheep_positions[i], dogs, r_s)
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

    return state.copy_with(
        sheep_positions=state.sheep_positions + velocities,
        sheep_velocities=velocities,
    )
