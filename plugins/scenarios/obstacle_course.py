"""Obstacle-course scenario: guide flock through corridor obstacles to a goal."""

from __future__ import annotations

from typing import Any

import numpy as np

from core.base_scenario import BaseScenario
from core.simulation_state import SimulationState
from core.world import GoalZone, Obstacle, World


class ObstacleCourseScenario(BaseScenario):
    """Drive sheep to a goal while navigating rectangular obstacles."""

    @property
    def id(self) -> str:
        return "obstacle_course"

    @property
    def name(self) -> str:
        return "Obstacle Course"

    @property
    def description(self) -> str:
        return "Guide the flock through obstacles into a goal zone."

    @property
    def default_config(self) -> dict[str, Any]:
        return {
            "n_sheep": 30,
            "n_shepherds": 2,
            "world_width": 150.0,
            "world_height": 150.0,
            "goal_center": [130.0, 75.0],
            "goal_radius": 15.0,
            "initial_spread": 15.0,
            "max_ticks": 4000,
            "success_fraction": 1.0,
            "obstacles": [
                {"min_corner": [55.0, 0.0], "max_corner": [65.0, 55.0]},
                {"min_corner": [55.0, 95.0], "max_corner": [65.0, 150.0]},
                {"min_corner": [95.0, 40.0], "max_corner": [105.0, 110.0]},
            ],
        }

    def create_world(self, config: dict[str, Any]) -> World:
        width = float(config.get("world_width", 150.0))
        height = float(config.get("world_height", 150.0))
        goal_center = np.array(config.get("goal_center", [130.0, 75.0]), dtype=float)
        goal_radius = float(config.get("goal_radius", 15.0))

        raw_obstacles = config.get("obstacles")
        if raw_obstacles is None:
            raw_obstacles = self.default_config["obstacles"]

        obstacles = [
            Obstacle(
                min_corner=np.array(item["min_corner"], dtype=float),
                max_corner=np.array(item["max_corner"], dtype=float),
            )
            for item in raw_obstacles
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
        sheep_center = np.array([25.0, 75.0])
        spread = float(config.get("initial_spread", 15.0))
        sheep_pos = sheep_center + rng.uniform(-spread, spread, size=(n_sheep, 2))

        shepherd_base = np.array([10.0, 75.0])
        shepherd_pos = shepherd_base + rng.uniform(-5, 5, size=(n_shepherds, 2))
        return sheep_pos, shepherd_pos

    def is_success(self, state: SimulationState, config: dict[str, Any]) -> bool:
        goal = state.world.goal
        if goal is None:
            return False
        success_fraction = float(config.get("success_fraction", 1.0))
        return float(np.mean(goal.contains(state.sheep_positions))) >= success_fraction

    def max_ticks(self, config: dict[str, Any]) -> int:
        return int(config.get("max_ticks", 4000))
