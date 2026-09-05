"""Kubo 2022 force-based multi-dog herding algorithm.

Reference:
Kubo, M., Tashiro, M., Sato, H., et al. (2022).
"Herd guidance by multiple sheepdog agents with repulsive force",
Artificial Life and Robotics, 27, 416-427.

Python dynamics follow the MATLAB reference:
matlab/Force-Based-Sheep-Herding-Algorithm/src/main.m
"""

from __future__ import annotations

from typing import Any

import numpy as np

from algorithms.kubo.config import KUBO_DEFAULTS
from algorithms.kubo.forces import (
    clamp_speed,
    dog_force_components,
    sheep_force_components,
)
from core.base_algorithm import BaseAlgorithm
from core.simulation_state import SimulationState


class KuboAlgorithm(BaseAlgorithm):
    """Multi-dog repulsive-force herding (Kubo 2022 / MATLAB port)."""

    @property
    def id(self) -> str:
        return "kubo"

    @property
    def name(self) -> str:
        return "Kubo 2022"

    @property
    def default_config(self) -> dict[str, Any]:
        return KUBO_DEFAULTS.copy()

    def step(self, state: SimulationState, config: dict[str, Any]) -> SimulationState:
        radius = float(config["radius"])
        dt = float(config["dt"])
        goal = self._goal_position(state, config)

        sheep_vel = self._update_sheep(state, config, radius)
        dog_vel = self._update_dogs(state, config, radius, goal)

        sheep_pos = state.sheep_positions + dt * sheep_vel
        dog_pos = state.shepherd_positions + dt * dog_vel

        sheep_pos = state.world.reflect_positions(sheep_pos)
        dog_pos = state.world.reflect_positions(dog_pos)
        sheep_vel = state.world.reflect_velocities(sheep_pos, sheep_vel)
        dog_vel = state.world.reflect_velocities(dog_pos, dog_vel)

        metadata = dict(state.metadata)
        metadata["r_a"] = float(config.get("r_a", metadata.get("r_a", 2.0)))

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

    def _goal_position(self, state: SimulationState, config: dict) -> np.ndarray:
        if state.world.goal is not None:
            return state.world.goal.center.astype(float)
        return np.array(config.get("goal_center", [15.0, 15.0]), dtype=float)

    def _update_sheep(
        self, state: SimulationState, config: dict, radius: float
    ) -> np.ndarray:
        n = state.n_sheep
        velocities = np.zeros((n, 2))
        ks1 = float(config["K_s1"])
        ks2 = float(config["K_s2"])
        ks3 = float(config["K_s3"])
        ks4 = float(config["K_s4"])

        for i in range(n):
            a_i, b_i, c_i, d_i = sheep_force_components(
                i,
                state.sheep_positions,
                state.sheep_velocities,
                state.shepherd_positions,
                radius,
            )
            velocities[i] = ks1 * a_i + ks2 * b_i + ks3 * c_i + ks4 * d_i

        return clamp_speed(velocities, float(config["sheep_speed_max"]))

    def _update_dogs(
        self,
        state: SimulationState,
        config: dict,
        radius: float,
        goal: np.ndarray,
    ) -> np.ndarray:
        m = state.n_shepherds
        velocities = np.zeros((m, 2))
        kf1 = float(config["K_f1"])
        kf2 = float(config["K_f2"])
        kf3 = float(config["K_f3"])
        kf4 = float(config["K_f4"])

        for i in range(m):
            a_i, b_i, c_i, d_i = dog_force_components(
                i,
                state.shepherd_positions,
                state.sheep_positions,
                goal,
                radius,
            )
            velocities[i] = kf1 * a_i + kf2 * b_i + kf3 * c_i + kf4 * d_i

        return clamp_speed(velocities, float(config["dog_speed_max"]))
