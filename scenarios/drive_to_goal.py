"""Default scenario: herd all sheep into a circular goal zone."""

from __future__ import annotations

from typing import Any

import numpy as np

from core.base_scenario import BaseScenario
from core.simulation_state import SimulationState
from core.world import GoalZone, World


class DriveToGoalScenario(BaseScenario):
    """Classic shepherding task: move all sheep into a goal circle."""

    @property
    def id(self) -> str:
        return "drive_to_goal"

    @property
    def name(self) -> str:
        return "Drive to Goal"

    @property
    def description(self) -> str:
        return "Herd all sheep into a circular goal zone at a corner of the field."

    def create_world(self, config: dict[str, Any]) -> World:
        width = config.get("world_width", 150.0)
        height = config.get("world_height", 150.0)
        goal_radius = config.get("goal_radius", 15.0)
        goal_center = np.array(config.get("goal_center", [15.0, 15.0]), dtype=float)
        return World(
            width=width,
            height=height,
            goal=GoalZone(center=goal_center, radius=goal_radius),
        )

    def initial_positions(
        self, config: dict[str, Any], rng: np.random.Generator
    ) -> tuple[np.ndarray, np.ndarray]:
        n_sheep = config.get("n_sheep", 50)
        n_shepherds = config.get("n_shepherds", 1)
        world_width = config.get("world_width", 150.0)
        world_height = config.get("world_height", 150.0)

        # Sheep start clustered near the centre of the field
        center = np.array([world_width / 2, world_height / 2])
        spread = config.get("initial_spread", 30.0)
        sheep_pos = center + rng.uniform(-spread, spread, size=(n_sheep, 2))

        # Shepherd starts at a distance behind the flock (opposite side from goal)
        shepherd_offset = config.get("shepherd_start_offset", 50.0)
        shepherd_base = center + np.array([shepherd_offset, shepherd_offset])
        shepherd_pos = shepherd_base + rng.uniform(-5, 5, size=(n_shepherds, 2))

        return sheep_pos, shepherd_pos

    def is_success(self, state: SimulationState, config: dict[str, Any]) -> bool:
        """Success when all sheep are inside the goal zone."""
        goal = state.world.goal
        if goal is None:
            return False
        success_fraction = config.get("success_fraction", 1.0)
        inside = goal.contains(state.sheep_positions)
        return np.mean(inside) >= success_fraction

    def max_ticks(self, config: dict[str, Any]) -> int:
        return config.get("max_ticks", 3000)
