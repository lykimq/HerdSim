"""Context-aware adaptive dog controller with optional lead/herd switch."""

from __future__ import annotations

from typing import Any

import numpy as np

from algorithms.strombom.config import STROMBOM_DEFAULTS
from algorithms.strombom.heuristics import (
    collect_target,
    compute_threshold,
    drive_target,
    shepherd_step_toward,
)
from controllers.helpers import apply_dog_speeds, empty_dog_velocities, view_from_observation
from core.agents.goal import resolve_goal_center
from core.agents.shepherd import move_toward, position_behind_target
from core.dog_controller import BaseDogController
from core.observation import ShepherdObservation
from core.simulation_state import SimulationState


def classify_flock_state(state: SimulationState, config: dict) -> str:
    """Classify observed flock as dispersed, cohesive, or fragmented."""
    if state.n_sheep == 0:
        return "dispersed"
    scale = float(config.get("collect_threshold_scale", 1.0))
    threshold = compute_threshold(state.n_sheep, float(config.get("r_a", 2.0))) * scale
    distances = state.distances_to_centroid()
    outliers = int(np.sum(distances > threshold))
    # Fragmentation proxy: many outliers relative to flock size.
    if outliers >= max(2, state.n_sheep // 3):
        return "fragmented"
    if outliers > 0:
        return "dispersed"
    return "cohesive"


class AdaptiveController(BaseDogController):
    """Select collect / drive / recover / lead from classified flock state."""

    @property
    def id(self) -> str:
        return "adaptive"

    @property
    def name(self) -> str:
        return "Adaptive"

    @property
    def default_config(self) -> dict[str, Any]:
        cfg = {
            k: STROMBOM_DEFAULTS[k]
            for k in (
                "n_shepherds",
                "r_a",
                "noise_strength",
                "shepherd_speed",
                "shepherd_stop_multiple",
                "collect_threshold_scale",
            )
        }
        cfg["lead_enabled"] = True
        return cfg

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
        flock_state = classify_flock_state(local, config)
        lines = []
        mode = flock_state

        for i in range(state.n_shepherds):
            if not state.shepherd_active[i]:
                continue
            if local.n_sheep == 0:
                continue
            if flock_state == "dispersed":
                target = collect_target(local, config)
                behaviour = "collect"
            elif flock_state == "fragmented":
                # Recover: move to geometric median-ish (centroid) stand-off.
                goal = resolve_goal_center(state, config)
                target = position_behind_target(
                    local.sheep_centroid, goal, float(config.get("r_a", 2.0)) * 2.0
                )
                behaviour = "recover"
            elif bool(config.get("lead_enabled", True)) and flock_state == "cohesive":
                # Lead when possible: move ahead of flock toward goal.
                goal = resolve_goal_center(state, config)
                ahead = local.sheep_centroid + 0.35 * (goal - local.sheep_centroid)
                target = ahead
                behaviour = "lead"
            else:
                target = drive_target(local, config)
                behaviour = "drive"

            if behaviour == "lead":
                speed = float(config.get("shepherd_speed", 1.5))
                velocities[i] = move_toward(state.shepherd_positions[i], target, speed)
            else:
                velocities[i] = shepherd_step_toward(local, config, i, target)
            lines.append(
                {
                    "from": state.shepherd_positions[i].tolist(),
                    "to": target.tolist(),
                    "mode": behaviour,
                }
            )
            mode = behaviour

        velocities = apply_dog_speeds(velocities, state, config)
        metadata = dict(state.metadata)
        metadata["herding_mode"] = mode
        metadata["flock_state"] = flock_state
        metadata["assignment_lines"] = lines
        return state.copy_with(
            shepherd_positions=state.shepherd_positions + velocities,
            shepherd_velocities=velocities,
            metadata=metadata,
        )
