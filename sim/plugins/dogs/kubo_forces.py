"""Kubo force-based dog controller."""

from __future__ import annotations

from typing import Any

from core.observation import ShepherdObservation
from core.simulation_state import SimulationState
from core.world.goal import resolve_goal_center
from methods.kubo.config import KUBO_DEFAULTS
from methods.kubo.forces import clamp_speed, dog_force_components

from .base import BaseDogController
from .helpers import empty_dog_velocities, finalize_dog_step, view_from_observation


class KuboDogController(BaseDogController):
    @property
    def id(self) -> str:
        return "kubo_forces"

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
        for obs in observations:
            if obs.n_sheep_seen == 0:
                continue
            i = obs.shepherd_index
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
        return finalize_dog_step(
            state,
            velocities,
            config,
            metadata_updates={"r_a": float(config.get("r_a", state.metadata.get("r_a", 2.0)))},
            dt=dt,
        )
