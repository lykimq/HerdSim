"""Scenarios (task layouts and success criteria), keyed by the protocol ``task``.

A scenario is three functions: build the world, place the agents, and check
success. Every setup value comes from the run config; ``required_keys`` lists
what the protocol must supply.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import numpy as np
from core.simulation_state import SimulationState
from core.world import World

from . import drive_to_goal

# Setup keys every scenario reads.
SETUP_KEYS = (
    "world_width",
    "world_height",
    "goal_center",
    "goal_radius",
    "initial_layout",
    "initial_spread",
    "measurement_radius",
    "shepherd_start_offset",
    "shepherd_jitter",
    "max_ticks",
)


@dataclass(frozen=True)
class Scenario:
    required_keys: tuple[str, ...]
    create_world: Callable[[dict[str, Any]], World]
    initial_positions: Callable[
        [dict[str, Any], np.random.Generator], tuple[np.ndarray, np.ndarray]
    ]
    is_success: Callable[[SimulationState, dict[str, Any]], bool]


SCENARIOS: dict[str, Scenario] = {
    "drive_to_goal": Scenario(
        required_keys=SETUP_KEYS,
        create_world=drive_to_goal.create_world,
        initial_positions=drive_to_goal.initial_positions,
        is_success=drive_to_goal.is_success,
    ),
}
