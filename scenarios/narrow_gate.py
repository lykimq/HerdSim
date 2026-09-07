"""Narrow-gate scenario: herd through a choke point into the goal."""

from __future__ import annotations

from typing import Any

import numpy as np

from core.base_scenario import BaseScenario
from core.simulation_state import SimulationState
from core.world import GoalZone, Obstacle, World


class NarrowGateScenario(BaseScenario):
    """Two walls leave a narrow gate; flock must pass then reach the goal."""

    @property
    def id(self) -> str:
        return "narrow_gate"

    @property
    def name(self) -> str:
        return "Narrow Gate"

    @property
    def description(self) -> str:
        return "Guide the flock through a narrow gate (choke point) into the goal."

    @property
    def default_config(self) -> dict[str, Any]:
        return {
            "n_sheep": 30,
            "n_shepherds": 2,
            "world_width": 150.0,
            "world_height": 150.0,
            "goal_center": [130.0, 75.0],
            "goal_radius": 16.0,
            "gate_width": 18.0,
            "gate_x": 70.0,
            "wall_thickness": 8.0,
            "initial_spread": 12.0,
            "max_ticks": 4500,
            "success_fraction": 1.0,
        }

    def create_world(self, config: dict[str, Any]) -> World:
        width = float(config.get("world_width", 150.0))
        height = float(config.get("world_height", 150.0))
        goal_center = np.array(config.get("goal_center", [130.0, 75.0]), dtype=float)
        goal_radius = float(config.get("goal_radius", 16.0))
        gate_width = float(config.get("gate_width", 18.0))
        gate_x = float(config.get("gate_x", 70.0))
        thickness = float(config.get("wall_thickness", 8.0))
        mid = height / 2.0
        gap_half = gate_width / 2.0

        obstacles = [
            Obstacle(
                min_corner=np.array([gate_x, 0.0]),
                max_corner=np.array([gate_x + thickness, mid - gap_half]),
            ),
            Obstacle(
                min_corner=np.array([gate_x, mid + gap_half]),
                max_corner=np.array([gate_x + thickness, height]),
            ),
        ]
        return World(
            dt=float(config.get("dt", 0.1)),
            scale=float(config.get("scale", 1.0)),
            width=width,
            height=height,
            goal=GoalZone(center=goal_center, radius=goal_radius),
            obstacles=obstacles,
        )

    def initial_positions(
        self, config: dict[str, Any], rng: np.random.Generator
    ) -> tuple[np.ndarray, np.ndarray]:
        n_sheep = int(config.get("n_sheep", 30))
        n_shepherds = int(config.get("n_shepherds", 2))
        height = float(config.get("world_height", 150.0))
        spread = float(config.get("initial_spread", 12.0))
        sheep_center = np.array([25.0, height / 2.0])
        sheep_pos = sheep_center + rng.uniform(-spread, spread, size=(n_sheep, 2))
        shepherd_base = np.array([10.0, height / 2.0])
        shepherd_pos = shepherd_base + rng.uniform(-6, 6, size=(n_shepherds, 2))
        return sheep_pos, shepherd_pos

    def is_success(self, state: SimulationState, config: dict[str, Any]) -> bool:
        goal = state.world.goal
        if goal is None:
            return False
        frac = float(config.get("success_fraction", 1.0))
        return float(np.mean(goal.contains(state.sheep_positions))) >= frac

    def max_ticks(self, config: dict[str, Any]) -> int:
        return int(config.get("max_ticks", 4500))
