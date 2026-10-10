"""Wide-field scenario: long-drive efficiency on a larger arena."""

from __future__ import annotations

from typing import Any

import numpy as np

from core.base_scenario import BaseScenario
from core.simulation_state import SimulationState
from core.world import GoalZone, World


class WideFieldScenario(BaseScenario):
    """Large field with distant goal; tests sustained drive efficiency."""

    @property
    def id(self) -> str:
        return "wide_field"

    @property
    def name(self) -> str:
        return "Wide Field"

    @property
    def description(self) -> str:
        return "Large arena with a distant goal; tests long-drive efficiency and scaling."

    @property
    def default_config(self) -> dict[str, Any]:
        return {
            "n_sheep": 60,
            "n_shepherds": 2,
            "world_width": 250.0,
            "world_height": 250.0,
            "goal_center": [20.0, 20.0],
            "goal_radius": 20.0,
            "initial_spread": 25.0,
            "shepherd_start_offset": 70.0,
            "max_ticks": 6000,
            "success_fraction": 1.0,
        }

    def create_world(self, config: dict[str, Any]) -> World:
        width = float(config.get("world_width", 250.0))
        height = float(config.get("world_height", 250.0))
        goal_center = np.array(config.get("goal_center", [20.0, 20.0]), dtype=float)
        goal_radius = float(config.get("goal_radius", 20.0))
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
        n_sheep = int(config.get("n_sheep", 60))
        n_shepherds = int(config.get("n_shepherds", 2))
        width = float(config.get("world_width", 250.0))
        height = float(config.get("world_height", 250.0))
        center = np.array([width * 0.65, height * 0.65])
        spread = float(config.get("initial_spread", 25.0))
        sheep_pos = center + rng.uniform(-spread, spread, size=(n_sheep, 2))
        offset = float(config.get("shepherd_start_offset", 70.0))
        shepherd_base = center + np.array([offset, offset])
        shepherd_pos = shepherd_base + rng.uniform(-8, 8, size=(n_shepherds, 2))
        return sheep_pos, shepherd_pos

    def is_success(self, state: SimulationState, config: dict[str, Any]) -> bool:
        goal = state.world.goal
        if goal is None:
            return False
        frac = float(config.get("success_fraction", 1.0))
        return float(np.mean(goal.contains(state.sheep_positions))) >= frac

    def max_ticks(self, config: dict[str, Any]) -> int:
        return int(config.get("max_ticks", 6000))
