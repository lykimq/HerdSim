"""Kubo 2022 sheep dynamics."""

from __future__ import annotations

from typing import Any

import numpy as np

from algorithms.kubo.config import KUBO_DEFAULTS
from algorithms.kubo.forces import clamp_speed, sheep_force_components
from core.sheep_dynamics import BaseSheepDynamics
from core.simulation_state import SimulationState


class KuboSheepDynamics(BaseSheepDynamics):
    @property
    def id(self) -> str:
        return "kubo"

    @property
    def name(self) -> str:
        return "Kubo Sheep"

    @property
    def default_config(self) -> dict[str, Any]:
        keys = {
            "n_sheep",
            "radius",
            "K_s1",
            "K_s2",
            "K_s3",
            "K_s4",
            "dt",
            "sheep_speed_max",
            "r_a",
        }
        return {k: KUBO_DEFAULTS[k] for k in keys}

    def step(self, state: SimulationState, config: dict[str, Any]) -> SimulationState:
        radius = float(config["radius"])
        dt = float(config["dt"])
        n = state.n_sheep
        velocities = np.zeros((n, 2))
        ks1 = float(config["K_s1"])
        ks2 = float(config["K_s2"])
        ks3 = float(config["K_s3"]) * float(config.get("cohesion_scale", 1.0))
        ks4 = float(config["K_s4"])
        dogs = state.shepherd_positions[state.shepherd_active]

        for i in range(n):
            a_i, b_i, c_i, d_i = sheep_force_components(
                i,
                state.sheep_positions,
                state.sheep_velocities,
                dogs,
                radius,
            )
            # Scale dog repulsion by per-sheep response.
            d_i = d_i * float(state.sheep_response[i])
            c_i = c_i * float(state.sheep_cohesion[i])
            velocities[i] = ks1 * a_i + ks2 * b_i + ks3 * c_i + ks4 * d_i

        velocities = clamp_speed(velocities, float(config["sheep_speed_max"]))
        return state.copy_with(
            sheep_positions=state.sheep_positions + dt * velocities,
            sheep_velocities=velocities,
        )
