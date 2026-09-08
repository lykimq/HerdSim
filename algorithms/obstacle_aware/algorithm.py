"""Obstacle-aware Strombom Collect/Drive herding.

Sheep: Strombom 2014. Shepherds: standard Collect; Drive stand-off Pd is
deflected around blocking obstacles or toward a narrow-gate gap.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from algorithms.obstacle_aware.config import OBSTACLE_AWARE_DEFAULTS
from algorithms.obstacle_aware.geometry import deflect_drive_point
from algorithms.strombom.algorithm import StrombomAlgorithm
from algorithms.strombom.heuristics import (
    collect_target,
    drive_offset,
    shepherd_step_toward,
    should_collect,
)
from core.agents.goal import resolve_goal_center
from core.agents.shepherd import position_behind_target
from core.simulation_state import SimulationState


def obstacle_aware_drive_target(
    state: SimulationState, config: dict
) -> np.ndarray:
    """Drive stand-off behind GCM, deflected if GCM->goal is blocked."""
    centroid = state.sheep_centroid
    goal = resolve_goal_center(state, config)
    offset = drive_offset(state, config)
    base = position_behind_target(centroid, goal, offset)
    clearance = float(config.get("obstacle_clearance", 5.0))
    return deflect_drive_point(
        centroid, goal, base, state.world.obstacles, clearance
    )


class ObstacleAwareAlgorithm(StrombomAlgorithm):
    """Collect/Drive with obstacle- or gate-aware drive points."""

    def __init__(self) -> None:
        super().__init__()
        self._last_assignment_lines: list[dict[str, Any]] = []
        self._last_mode: str = "drive"

    @property
    def id(self) -> str:
        return "obstacle_aware"

    @property
    def name(self) -> str:
        return "Obstacle-Aware"

    @property
    def default_config(self) -> dict[str, Any]:
        return OBSTACLE_AWARE_DEFAULTS.copy()

    def step(self, state: SimulationState, config: dict[str, Any]) -> SimulationState:
        new_state = super().step(state, config)
        metadata = dict(new_state.metadata)
        if state.n_shepherds and state.n_sheep:
            metadata["assignment_lines"] = list(self._last_assignment_lines)
            metadata["herding_mode"] = self._last_mode
        return SimulationState(
            tick=new_state.tick,
            sheep_positions=new_state.sheep_positions,
            sheep_velocities=new_state.sheep_velocities,
            shepherd_positions=new_state.shepherd_positions,
            shepherd_velocities=new_state.shepherd_velocities,
            world=new_state.world,
            rng=new_state.rng,
            metadata=metadata,
        )

    def _update_shepherds(self, state: SimulationState, config: dict) -> np.ndarray:
        velocities = np.zeros_like(state.shepherd_positions)
        self._last_assignment_lines = []
        self._last_mode = "drive"
        m = state.n_shepherds
        if m == 0 or state.n_sheep == 0:
            return velocities

        collecting = should_collect(state, config)
        self._last_mode = "collect" if collecting else "drive"

        for i in range(m):
            if collecting:
                target = collect_target(state, config)
                line_to = state.sheep_positions[int(state.furthest_sheep_index())]
                line = {
                    "from": state.shepherd_positions[i].tolist(),
                    "to": line_to.tolist(),
                    "mode": "collect",
                    "sheep_index": int(state.furthest_sheep_index()),
                }
            else:
                target = obstacle_aware_drive_target(state, config)
                # Multi-shepherd: small lateral spacing so dogs do not stack.
                if m > 1:
                    goal = resolve_goal_center(state, config)
                    forward = state.sheep_centroid - goal
                    fn = float(np.linalg.norm(forward))
                    if fn > 1e-10:
                        perp = np.array([-forward[1], forward[0]]) / fn
                        target = target + perp * (6.0 * (i - (m - 1) / 2.0))
                line = {
                    "from": state.shepherd_positions[i].tolist(),
                    "to": target.tolist(),
                    "mode": "drive",
                }
            velocities[i] = shepherd_step_toward(state, config, i, target)
            self._last_assignment_lines.append(line)
        return velocities
