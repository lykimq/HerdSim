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
        return (
            "Herd all sheep into a circular goal zone near the field origin "
            "(corner). Grid lines are display-only world-unit markers."
        )

    @property
    def default_config(self) -> dict[str, Any]:
        return {
            "n_sheep": 50,
            "n_shepherds": 1,
            "world_width": 150.0,
            "world_height": 150.0,
            "goal_center": [15.0, 15.0],
            "goal_radius": 15.0,
            "initial_spread": 30.0,
            "shepherd_start_offset": 50.0,
            "shepherd_jitter": 5.0,
            "max_ticks": 3000,
            "success_fraction": 1.0,
        }

    def create_world(self, config: dict[str, Any]) -> World:
        width = config.get("world_width", 150.0)
        height = config.get("world_height", 150.0)
        goal_radius = config.get("goal_radius", 15.0)
        goal_center = np.array(config.get("goal_center", [15.0, 15.0]), dtype=float)
        return World(
            dt=float(config.get("dt", 0.1)),
            scale=float(config.get("scale", 1.0)),
            width=width,
            height=height,
            goal=GoalZone(center=goal_center, radius=goal_radius),
        )

    def initial_positions(
        self, config: dict[str, Any], rng: np.random.Generator
    ) -> tuple[np.ndarray, np.ndarray]:
        from core.x0_generators import generate_initial_positions, normalize_layout

        n_sheep = config.get("n_sheep", 50)
        n_shepherds = config.get("n_shepherds", 1)
        world_width = config.get("world_width", 150.0)
        world_height = config.get("world_height", 150.0)

        # Sheep start according to the X0 family in initial_layout.
        center = np.array([world_width / 2, world_height / 2])
        spread = config.get("initial_spread", 30.0)
        layout = normalize_layout(str(config.get("initial_layout", "compact")))
        measurement_radius = float(config.get("measurement_radius", 5.0))
        r_a = float(config.get("r_a", 2.0))
        lost_threshold = r_a * (float(n_sheep) ** (2.0 / 3.0))
        goal_center = np.array(config.get("goal_center", [15.0, 15.0]), dtype=float)
        goal_radius = float(config.get("goal_radius", 15.0))
        sheep_pos = generate_initial_positions(
            int(n_sheep),
            layout,
            center,
            rng,
            spread=float(spread),
            interaction_radius=measurement_radius,
            lost_threshold=lost_threshold,
            world_width=float(world_width),
            world_height=float(world_height),
            goal_center=goal_center,
            goal_radius=goal_radius,
        )

        # Shepherds start on the side of the flock opposite the goal.
        # The default corner goal keeps the historical diagonal offset.
        shepherd_offset = float(config.get("shepherd_start_offset", 50.0))
        default_corner = np.array([15.0, 15.0])
        if np.allclose(goal_center, default_corner):
            shepherd_base = center + np.array([shepherd_offset, shepherd_offset])
        else:
            away = center - goal_center
            norm = float(np.linalg.norm(away))
            direction = away / norm if norm > 1e-9 else np.array([1.0, 0.0])
            shepherd_base = center + direction * shepherd_offset
        jitter = config.get("shepherd_jitter", 5.0)
        shepherd_pos = shepherd_base + rng.uniform(-jitter, jitter, size=(n_shepherds, 2))

        return sheep_pos, shepherd_pos

    def is_success(self, state: SimulationState, config: dict[str, Any]) -> bool:
        """Success when all sheep are inside the goal zone."""
        goal = state.world.goal
        if goal is None:
            return False
        success_fraction = config.get("success_fraction", 1.0)
        inside = goal.contains(state.sheep_positions)
        return bool(np.mean(inside) >= success_fraction)

    def max_ticks(self, config: dict[str, Any]) -> int:
        return config.get("max_ticks", 3000)
