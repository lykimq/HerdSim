"""Containment scenario: keep sheep inside a central pen boundary."""

from __future__ import annotations

from typing import Any

import numpy as np

from core.base_scenario import BaseScenario
from core.simulation_state import SimulationState
from core.world import World


class ContainmentScenario(BaseScenario):
    """Keep the flock inside a soft containment region for as long as possible."""

    @property
    def id(self) -> str:
        return "containment"

    @property
    def name(self) -> str:
        return "Containment"

    @property
    def description(self) -> str:
        return "Keep all sheep inside a central pen; escape counts as failure."

    @property
    def default_config(self) -> dict[str, Any]:
        return {
            "n_sheep": 40,
            "n_shepherds": 3,
            "world_width": 150.0,
            "world_height": 150.0,
            "pen_center": [75.0, 75.0],
            "pen_radius": 35.0,
            "initial_spread": 20.0,
            "max_ticks": 2000,
            "containment_fraction": 0.95,
            "containment_min_ticks": 200,
        }

    def create_world(self, config: dict[str, Any]) -> World:
        width = float(config.get("world_width", 150.0))
        height = float(config.get("world_height", 150.0))
        # Re-use GoalZone as the pen region for success checks.
        from core.world import GoalZone

        pen_center = np.array(
            config.get("pen_center", [width / 2.0, height / 2.0]), dtype=float
        )
        pen_radius = float(config.get("pen_radius", 35.0))
        return World(
            dt=float(config.get("dt", 0.1)),
            scale=float(config.get("scale", 1.0)),
            width=width,
            height=height,
            goal=GoalZone(center=pen_center, radius=pen_radius),
        )

    def initial_positions(
        self, config: dict[str, Any], rng: np.random.Generator
    ) -> tuple[np.ndarray, np.ndarray]:
        n_sheep = int(config.get("n_sheep", 40))
        n_shepherds = int(config.get("n_shepherds", 3))
        width = float(config.get("world_width", 150.0))
        height = float(config.get("world_height", 150.0))
        center = np.array([width / 2.0, height / 2.0])
        spread = float(config.get("initial_spread", 20.0))

        sheep_pos = center + rng.uniform(-spread, spread, size=(n_sheep, 2))
        # Dogs start around the pen perimeter.
        angles = np.linspace(0, 2 * np.pi, n_shepherds, endpoint=False)
        radius = float(config.get("pen_radius", 35.0)) + 10.0
        shepherd_pos = center + np.stack(
            [radius * np.cos(angles), radius * np.sin(angles)], axis=1
        )
        shepherd_pos += rng.uniform(-2, 2, size=shepherd_pos.shape)
        return sheep_pos, shepherd_pos

    def is_success(self, state: SimulationState, config: dict[str, Any]) -> bool:
        """Success if flock remains inside pen until timeout window fraction."""
        goal = state.world.goal
        if goal is None:
            return False
        inside_fraction = float(np.mean(goal.contains(state.sheep_positions)))
        required = float(config.get("containment_fraction", 0.95))
        min_ticks = int(config.get("containment_min_ticks", 200))
        return state.tick >= min_ticks and inside_fraction >= required

    def max_ticks(self, config: dict[str, Any]) -> int:
        return int(config.get("max_ticks", 2000))
