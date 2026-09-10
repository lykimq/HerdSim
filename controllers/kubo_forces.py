"""Kubo force-based dog controller."""

from __future__ import annotations

from typing import Any

import numpy as np

from algorithms.kubo.config import KUBO_DEFAULTS
from algorithms.kubo.forces import clamp_speed, dog_force_components
from controllers.helpers import apply_dog_speeds, empty_dog_velocities, view_from_observation
from core.agents.goal import resolve_goal_center
from core.dog_controller import BaseDogController
from core.observation import ShepherdObservation
from core.simulation_state import SimulationState


class KuboDogController(BaseDogController):
    @property
    def id(self) -> str:
        return "kubo_forces"

    @property
    def name(self) -> str:
        return "Kubo Forces"

    @property
    def default_config(self) -> dict[str, Any]:
        keys = {
            "n_shepherds",
            "radius",
            "K_f1",
            "K_f2",
            "K_f3",
            "K_f4",
            "dt",
            "dog_speed_max",
            "r_a",
        }
        return {k: KUBO_DEFAULTS[k] for k in keys}

    def step(
        self,
        state: SimulationState,
        observations: list[ShepherdObservation],
        config: dict[str, Any],
    ) -> SimulationState:
        velocities = empty_dog_velocities(state)
        if not observations:
            return state.copy_with(shepherd_velocities=velocities)

        radius = float(config["radius"])
        dt = float(config["dt"])
        goal = resolve_goal_center(state, config)
        kf1 = float(config["K_f1"])
        kf2 = float(config["K_f2"])
        kf3 = float(config["K_f3"])
        kf4 = float(config["K_f4"])
        obs_by_idx = {o.shepherd_index: o for o in observations}

        for i in range(state.n_shepherds):
            if not state.shepherd_active[i] or i not in obs_by_idx:
                continue
            obs = obs_by_idx[i]
            if obs.n_sheep_seen == 0:
                continue
            local = view_from_observation(state, obs)
            a_i, b_i, c_i, d_i = dog_force_components(
                i,
                local.shepherd_positions,
                local.sheep_positions,
                goal if obs.goal_center is None else obs.goal_center,
                radius,
            )
            velocities[i] = kf1 * a_i + kf2 * b_i + kf3 * c_i + kf4 * d_i

        velocities = clamp_speed(velocities, float(config["dog_speed_max"]))
        velocities = apply_dog_speeds(velocities, state, config)
        metadata = dict(state.metadata)
        metadata["r_a"] = float(config.get("r_a", metadata.get("r_a", 2.0)))
        return state.copy_with(
            shepherd_positions=state.shepherd_positions + dt * velocities,
            shepherd_velocities=velocities,
            metadata=metadata,
        )
