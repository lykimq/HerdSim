"""Strombom multi-dog extension with sector-based shepherd assignment."""

from __future__ import annotations

from typing import Any

import numpy as np

from algorithms.strombom.algorithm import StrombomAlgorithm
from algorithms.strombom.config import STROMBOM_DEFAULTS
from algorithms.strombom.heuristics import compute_threshold
from core.agents.shepherd import move_toward, position_behind_target
from core.simulation_state import SimulationState


class StrombomMultiAlgorithm(StrombomAlgorithm):
    """Multi-shepherd Strombom with explicit outlier sector assignment."""

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
        cfg["sector_assignment"] = True
        return cfg

    def _update_shepherds(self, state: SimulationState, config: dict) -> np.ndarray:
        velocities = np.zeros_like(state.shepherd_positions)
        m = state.n_shepherds
        if m == 0:
            return velocities

        centroid = state.sheep_centroid
        threshold = compute_threshold(state.n_sheep, config["r_a"])
        distances = state.distances_to_centroid()
        outliers = np.where(distances > threshold)[0]

        if state.world.goal is not None:
            goal = state.world.goal.center
        else:
            goal = np.array(config.get("goal_center", [15.0, 15.0]), dtype=float)

        offset = float(config.get("collect_drive_offset", config.get("r_a", 2.0)))
        speed = float(config.get("shepherd_speed", 2.0))

        if len(outliers) == 0:
            # All dogs drive with angular spacing behind the flock.
            base = position_behind_target(centroid, goal, offset)
            for i in range(m):
                angle = (2 * np.pi * i) / m
                spaced = base + 8.0 * np.array([np.cos(angle), np.sin(angle)])
                velocities[i] = move_toward(state.shepherd_positions[i], spaced, speed)
            return velocities

        # Assign each dog to a distinct outlier (cycle if fewer outliers).
        order = outliers[np.argsort(-distances[outliers])]
        for i in range(m):
            sheep_idx = int(order[i % len(order)])
            target = position_behind_target(
                state.sheep_positions[sheep_idx], centroid, offset
            )
            # Slight lateral offset so dogs do not stack.
            tangential = np.array(
                [
                    -(state.sheep_positions[sheep_idx][1] - centroid[1]),
                    state.sheep_positions[sheep_idx][0] - centroid[0],
                ]
            )
            tn = np.linalg.norm(tangential)
            if tn > 1e-10:
                target = target + (tangential / tn) * (4.0 * (i - (m - 1) / 2.0))
            velocities[i] = move_toward(state.shepherd_positions[i], target, speed)
        return velocities
