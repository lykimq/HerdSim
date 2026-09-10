"""Farthest-agent targeting (FAT) under local observations."""

from __future__ import annotations

from typing import Any

import numpy as np

from algorithms.strombom.config import STROMBOM_DEFAULTS
from algorithms.strombom.heuristics import shepherd_step_toward
from controllers.helpers import apply_dog_speeds, empty_dog_velocities, view_from_observation
from core.agents.goal import resolve_goal_center
from core.agents.shepherd import position_behind_target
from core.dog_controller import BaseDogController
from core.observation import ShepherdObservation
from core.simulation_state import SimulationState


class FatController(BaseDogController):
    """Drive the locally farthest observed sheep toward the goal."""

    @property
    def id(self) -> str:
        return "fat"

    @property
    def name(self) -> str:
        return "FAT"

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
        lines = []
        obs_by_idx = {o.shepherd_index: o for o in observations}
        goal = resolve_goal_center(state, config)
        offset = float(config.get("r_a", 2.0))

        for i in range(state.n_shepherds):
            if not state.shepherd_active[i] or i not in obs_by_idx:
                continue
            obs = obs_by_idx[i]
            if obs.n_sheep_seen == 0:
                continue
            local = view_from_observation(state, obs)
            # Farthest from dog among observed sheep.
            dists = np.linalg.norm(obs.sheep_positions - obs.self_position, axis=1)
            far_idx = int(np.argmax(dists))
            sheep_pos = obs.sheep_positions[far_idx]
            target = position_behind_target(sheep_pos, goal, offset)
            velocities[i] = shepherd_step_toward(local, config, i, target)
            lines.append(
                {
                    "from": state.shepherd_positions[i].tolist(),
                    "to": sheep_pos.tolist(),
                    "mode": "fat",
                    "sheep_index": int(obs.sheep_indices[far_idx])
                    if obs.sheep_indices.size
                    else far_idx,
                }
            )

        velocities = apply_dog_speeds(velocities, state, config)
        metadata = dict(state.metadata)
        metadata["herding_mode"] = "fat"
        metadata["assignment_lines"] = lines
        return state.copy_with(
            shepherd_positions=state.shepherd_positions + velocities,
            shepherd_velocities=velocities,
            metadata=metadata,
        )
