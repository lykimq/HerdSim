"""Strombom multi-dog extension with outlier assignment and spaced drive."""

from __future__ import annotations

from typing import Any

import numpy as np

from algorithms.strombom.algorithm import StrombomAlgorithm
from algorithms.strombom.config import STROMBOM_DEFAULTS
from algorithms.strombom.heuristics import (
    collect_offset,
    compute_threshold,
    drive_offset,
    shepherd_step_toward,
)
from core.agents.goal import resolve_goal_center
from core.agents.shepherd import position_behind_target
from core.simulation_state import SimulationState


class StrombomMultiAlgorithm(StrombomAlgorithm):
    """Multi-shepherd Strombom: dogs cycle outliers; drive with angular spacing."""

    def __init__(self) -> None:
        super().__init__()
        self._last_assignment_lines: list[dict[str, Any]] = []
        self._last_mode: str = "drive"

    @property
    def id(self) -> str:
        return "strombom_multi"

    @property
    def name(self) -> str:
        return "Strombom Multi-Dog"

    @property
    def default_config(self) -> dict[str, Any]:
        cfg = STROMBOM_DEFAULTS.copy()
        cfg["n_shepherds"] = 3
        return cfg

    def step(self, state: SimulationState, config: dict[str, Any]) -> SimulationState:
        new_state = super().step(state, config)
        metadata = dict(new_state.metadata)
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
        if m == 0:
            return velocities

        centroid = state.sheep_centroid
        scale = float(config.get("collect_threshold_scale", 1.0))
        threshold = compute_threshold(state.n_sheep, config["r_a"]) * scale
        distances = state.distances_to_centroid()
        outliers = np.where(distances > threshold)[0]
        goal = resolve_goal_center(state, config)
        c_offset = collect_offset(config)
        d_offset = drive_offset(state, config)

        if len(outliers) == 0:
            # All dogs drive with angular spacing behind the flock.
            base = position_behind_target(centroid, goal, d_offset)
            for i in range(m):
                angle = (2 * np.pi * i) / m
                spaced = base + 8.0 * np.array([np.cos(angle), np.sin(angle)])
                velocities[i] = shepherd_step_toward(state, config, i, spaced)
                self._last_assignment_lines.append(
                    {
                        "from": state.shepherd_positions[i].tolist(),
                        "to": spaced.tolist(),
                        "mode": "drive",
                    }
                )
            return velocities

        self._last_mode = "collect"
        # Assign each dog to a distinct outlier (cycle if fewer outliers).
        order = outliers[np.argsort(-distances[outliers])]
        for i in range(m):
            sheep_idx = int(order[i % len(order)])
            target = position_behind_target(
                state.sheep_positions[sheep_idx], centroid, c_offset
            )
            # Lateral offset so dogs do not stack on the same point.
            tangential = np.array(
                [
                    -(state.sheep_positions[sheep_idx][1] - centroid[1]),
                    state.sheep_positions[sheep_idx][0] - centroid[0],
                ]
            )
            tn = np.linalg.norm(tangential)
            if tn > 1e-10:
                target = target + (tangential / tn) * (4.0 * (i - (m - 1) / 2.0))
            velocities[i] = shepherd_step_toward(state, config, i, target)
            self._last_assignment_lines.append(
                {
                    "from": state.shepherd_positions[i].tolist(),
                    "to": state.sheep_positions[sheep_idx].tolist(),
                    "mode": "collect",
                    "sheep_index": sheep_idx,
                }
            )
        return velocities
