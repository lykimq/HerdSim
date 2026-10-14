"""Farthest-agent targeting (FAT) under local observations."""

from __future__ import annotations

from typing import Any

import numpy as np
from core.observation import ShepherdObservation
from core.simulation_state import SimulationState
from core.world.goal import resolve_goal_center
from methods.strombom.config import STROMBOM_DEFAULTS
from methods.strombom.heuristics import shepherd_step_toward

from .base import BaseDogController
from .helpers import (
    empty_dog_velocities,
    finalize_dog_step,
    position_behind_target,
    view_from_observation,
)


class FatController(BaseDogController):
    """Drive the locally farthest observed sheep toward the goal."""

    @property
    def id(self) -> str:
        return "fat"

    @property
    def default_config(self) -> dict[str, Any]:
        return {
            k: STROMBOM_DEFAULTS[k]
            for k in (
                "n_shepherds",
                "r_a",
                "noise_strength",
                "shepherd_speed",
                "shepherd_stop_multiple",
            )
        }

    def step(
        self,
        state: SimulationState,
        observations: list[ShepherdObservation],
        config: dict[str, Any],
    ) -> SimulationState:
        velocities = empty_dog_velocities(state)
        goal = resolve_goal_center(state, config)
        offset = float(config.get("r_a", 2.0))

        for obs in observations:
            if obs.n_sheep_seen == 0:
                continue
            i = obs.shepherd_index
            local = view_from_observation(state, obs)
            # Farthest from dog among observed sheep. Bearing-only proxies sit at
            # equal depth, so fall back to farthest from the goal among proxies.
            dists = np.linalg.norm(obs.sheep_positions - obs.self_position, axis=1)
            if float(np.ptp(dists)) < 1e-9:
                far_idx = int(np.argmax(np.linalg.norm(obs.sheep_positions - goal, axis=1)))
            else:
                far_idx = int(np.argmax(dists))
            sheep_pos = obs.sheep_positions[far_idx]
            target = position_behind_target(sheep_pos, goal, offset)
            velocities[i] = shepherd_step_toward(
                local, config, i, target, proximity_sheep=state.sheep_positions
            )

        return finalize_dog_step(
            state, velocities, config, metadata_updates={"herding_mode": "fat"}
        )
