"""Drive task: herd all sheep into a circular goal zone."""

from __future__ import annotations

from typing import Any

import numpy as np
from core.simulation_state import SimulationState
from core.world import GoalZone, World
from core.world.layouts import place_dogs, place_flock


def create_world(config: dict[str, Any]) -> World:
    return World(
        width=float(config["world_width"]),
        height=float(config["world_height"]),
        goal=GoalZone(
            center=np.array(config["goal_center"], dtype=float),
            radius=float(config["goal_radius"]),
        ),
    )


def initial_positions(
    config: dict[str, Any], rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray]:
    # Flock starts at the field center, outside the goal; dogs start on the
    # side of the flock opposite the goal.
    center = np.array([config["world_width"] / 2, config["world_height"] / 2], dtype=float)
    goal_center = np.array(config["goal_center"], dtype=float)
    sheep_pos = place_flock(config, center, rng, keep_out_of_goal=True)
    shepherd_pos = place_dogs(config, center, goal_center, rng)
    return sheep_pos, shepherd_pos


def is_success(state: SimulationState, _config: dict[str, Any]) -> bool:
    """Success when all sheep are inside the goal zone."""
    return bool(np.all(state.world.goal.contains(state.sheep_positions)))
