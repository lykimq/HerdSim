"""Kubo 2022 sheep motion (sheep_model=kubo).

Each sheep integrates a force sum over continuous time step dt: self-propulsion,
alignment, cohesion, and dog repulsion within sensing radius, with gains K_s1
through K_s4. Speed is clipped to sheep_speed_max. Paired with the Kubo force
dog controller in the kubo method; not a Collect/Drive sheep model.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from core.simulation_state import SimulationState
from methods.kubo.forces import clamp_speed, sheep_force_components


def step(state: SimulationState, config: dict[str, Any]) -> SimulationState:
    radius = float(config["radius"])
    dt = float(config["dt"])
    n = state.n_sheep
    velocities = np.zeros((n, 2))
    ks1 = float(config["K_s1"])
    ks2 = float(config["K_s2"])
    ks3 = float(config["K_s3"])
    ks4 = float(config["K_s4"])
    dogs = state.shepherd_positions

    for i in range(n):
        a_i, b_i, c_i, d_i = sheep_force_components(
            i,
            state.sheep_positions,
            state.sheep_velocities,
            dogs,
            radius,
        )
        velocities[i] = ks1 * a_i + ks2 * b_i + ks3 * c_i + ks4 * d_i

    velocities = clamp_speed(velocities, float(config["sheep_speed_max"]))
    return state.copy_with(
        sheep_positions=state.sheep_positions + dt * velocities,
        sheep_velocities=velocities,
    )
