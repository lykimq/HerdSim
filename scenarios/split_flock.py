"""Split-flock scenario: recover multiple initial clusters into the goal."""

from __future__ import annotations

from typing import Any

import numpy as np

from core.base_scenario import BaseScenario
from core.simulation_state import SimulationState
from core.world import GoalZone, World


class SplitFlockScenario(BaseScenario):
    """Start sheep in 2-3 separated clusters to stress Collect / recovery."""

    @property
    def id(self) -> str:
        return "split_flock"

    @property
    def name(self) -> str:
        return "Split Flock"

    @property
    def description(self) -> str:
        return (
            "Sheep start in multiple separated clusters; tests collect/recovery "
            "before driving to the goal."
        )

    @property
    def default_config(self) -> dict[str, Any]:
        return {
            "n_sheep": 45,
            "n_shepherds": 1,
            "n_clusters": 3,
            "world_width": 150.0,
            "world_height": 150.0,
            "goal_center": [15.0, 15.0],
            "goal_radius": 15.0,
            "initial_spread": 8.0,
            "max_ticks": 4000,
            # Extension (not in Strombom 2014): the three initial clusters start
            # ~90 world-units from the corner goal.  With the paper's threshold
            # f(N) = r_a * N^(2/3), a single stray sheep triggers Collect mode
            # and pulls the shepherd far enough that goal sheep lose shepherd
            # detection (r_s = 65) and drift away, causing chronic oscillation.
            # Scale 1.5 raises the effective threshold to ~1.5 * f(N), reducing
            # unnecessary Collect interruptions during the Drive phase.
            "collect_threshold_scale": 1.5,
            # A single shepherd cannot reliably achieve 100 % occupancy on this
            # scenario; 0.95 (95 % of the flock) is an achievable target.
            "success_fraction": 0.95,
        }

    def create_world(self, config: dict[str, Any]) -> World:
        width = float(config.get("world_width", 150.0))
        height = float(config.get("world_height", 150.0))
        goal_center = np.array(config.get("goal_center", [15.0, 15.0]), dtype=float)
        goal_radius = float(config.get("goal_radius", 15.0))
        return World(
            width=width,
            height=height,
            goal=GoalZone(center=goal_center, radius=goal_radius),
        )

    def initial_positions(
        self, config: dict[str, Any], rng: np.random.Generator
    ) -> tuple[np.ndarray, np.ndarray]:
        n_sheep = int(config.get("n_sheep", 45))
        n_shepherds = int(config.get("n_shepherds", 1))
        n_clusters = max(2, int(config.get("n_clusters", 3)))
        width = float(config.get("world_width", 150.0))
        height = float(config.get("world_height", 150.0))
        spread = float(config.get("initial_spread", 8.0))

        centers = [
            np.array([width * 0.35, height * 0.35]),
            np.array([width * 0.70, height * 0.40]),
            np.array([width * 0.55, height * 0.75]),
        ][:n_clusters]

        per = n_sheep // n_clusters
        rem = n_sheep - per * n_clusters
        chunks = []
        for i, center in enumerate(centers):
            count = per + (1 if i < rem else 0)
            chunks.append(center + rng.uniform(-spread, spread, size=(count, 2)))
        sheep_pos = np.vstack(chunks)

        shepherd_pos = np.array([[width * 0.85, height * 0.85]])
        if n_shepherds > 1:
            extras = shepherd_pos + rng.uniform(-8, 8, size=(n_shepherds - 1, 2))
            shepherd_pos = np.vstack([shepherd_pos, extras])
        return sheep_pos, shepherd_pos

    def is_success(self, state: SimulationState, config: dict[str, Any]) -> bool:
        goal = state.world.goal
        if goal is None:
            return False
        frac = float(config.get("success_fraction", 1.0))
        return float(np.mean(goal.contains(state.sheep_positions))) >= frac

    def max_ticks(self, config: dict[str, Any]) -> int:
        return int(config.get("max_ticks", 4000))
