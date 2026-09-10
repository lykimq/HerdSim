"""Obstacle-aware Collect/Drive dog controller."""

from __future__ import annotations

from typing import Any

from algorithms.obstacle_aware.config import OBSTACLE_AWARE_DEFAULTS
from algorithms.obstacle_aware.geometry import deflect_drive_point
from algorithms.strombom.heuristics import (
    collect_target,
    drive_offset,
    shepherd_step_toward,
    should_collect,
)
from controllers.helpers import apply_dog_speeds, empty_dog_velocities, view_from_observation
from core.agents.goal import resolve_goal_center
from core.agents.shepherd import position_behind_target
from core.dog_controller import BaseDogController
from core.observation import ShepherdObservation
from core.simulation_state import SimulationState


def obstacle_aware_drive_target(state: SimulationState, config: dict):
    centroid = state.sheep_centroid
    goal = resolve_goal_center(state, config)
    offset = drive_offset(state, config)
    base = position_behind_target(centroid, goal, offset)
    clearance = float(config.get("obstacle_clearance", 5.0))
    return deflect_drive_point(
        centroid, goal, base, state.world.obstacles, clearance
    )


class ObstacleAwareDriveController(BaseDogController):
    @property
    def id(self) -> str:
        return "obstacle_aware_drive"

    @property
    def name(self) -> str:
        return "Obstacle-Aware Drive"

    @property
    def default_config(self) -> dict[str, Any]:
        return {
            k: OBSTACLE_AWARE_DEFAULTS[k]
            for k in (
                "n_shepherds",
                "r_a",
                "noise_strength",
                "shepherd_speed",
                "shepherd_stop_multiple",
                "collect_threshold_scale",
                "obstacle_clearance",
            )
        }

    def step(
        self,
        state: SimulationState,
        observations: list[ShepherdObservation],
        config: dict[str, Any],
    ) -> SimulationState:
        velocities = empty_dog_velocities(state)
        if not observations:
            return state.copy_with(shepherd_velocities=velocities)
        local = view_from_observation(state, observations[0])
        if local.n_sheep == 0:
            return state.copy_with(shepherd_velocities=velocities)

        collecting = should_collect(local, config)
        mode = "collect" if collecting else "drive"
        lines = []
        for i in range(state.n_shepherds):
            if not state.shepherd_active[i]:
                continue
            if collecting:
                target = collect_target(local, config)
                sheep_idx = int(local.furthest_sheep_index())
                line_to = local.sheep_positions[sheep_idx]
                lines.append(
                    {
                        "from": state.shepherd_positions[i].tolist(),
                        "to": line_to.tolist(),
                        "mode": "collect",
                        "sheep_index": sheep_idx,
                    }
                )
            else:
                target = obstacle_aware_drive_target(local, config)
                lines.append(
                    {
                        "from": state.shepherd_positions[i].tolist(),
                        "to": target.tolist(),
                        "mode": "drive",
                    }
                )
            velocities[i] = shepherd_step_toward(local, config, i, target)

        velocities = apply_dog_speeds(velocities, state, config)
        metadata = dict(state.metadata)
        metadata["herding_mode"] = mode
        metadata["assignment_lines"] = lines
        return state.copy_with(
            shepherd_positions=state.shepherd_positions + velocities,
            shepherd_velocities=velocities,
            metadata=metadata,
        )
