"""Strombom Collect/Drive dog controller."""

from __future__ import annotations

from typing import Any

from core.observation import ShepherdObservation
from core.simulation_state import SimulationState
from methods.strombom.config import STROMBOM_DEFAULTS
from methods.strombom.heuristics import (
    compute_shepherd_velocity,
    should_collect,
    strombom_assignment_lines,
)

from .base import BaseDogController
from .helpers import (
    empty_dog_velocities,
    finalize_dog_step,
    iter_active_observations,
    view_from_observation,
)


class CollectDriveController(BaseDogController):
    @property
    def id(self) -> str:
        return "collect_drive"

    @property
    def name(self) -> str:
        return "Collect/Drive"

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
                "collect_threshold_scale",
            )
        }

    def step(
        self,
        state: SimulationState,
        observations: list[ShepherdObservation],
        config: dict[str, Any],
    ) -> SimulationState:
        velocities = empty_dog_velocities(state)
        modes = []
        lines = []
        for i, obs in iter_active_observations(state, observations):
            if obs.n_sheep_seen == 0:
                continue
            local = view_from_observation(state, obs)
            velocities[i] = compute_shepherd_velocity(
                local, config, i, proximity_sheep=state.sheep_positions
            )
            modes.append("collect" if should_collect(local, config) else "drive")
            lines.extend(strombom_assignment_lines(local, config)[:1])

        updates: dict[str, Any] = {"r_a": float(config.get("r_a", 2.0))}
        if modes:
            updates["herding_mode"] = modes[0]
        if lines:
            updates["assignment_lines"] = lines
        return finalize_dog_step(state, velocities, config, metadata_updates=updates)
