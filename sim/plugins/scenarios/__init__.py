"""Tasks keyed by protocol ``task``: setup, success, metrics, and failure labels."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from sim.core.simulation_state import SimulationState
from sim.core.world.arena import World
from sim.core.world.layouts import LAYOUTS
from sim.plugins.metrics import Metric

from . import drive_failures, drive_to_goal, goal
from .failures import Failure


@dataclass(frozen=True)
class Scenario:
    layouts: tuple[str, ...]
    required_keys: tuple[str, ...]
    # (settings, flock_radius, n_sheep, layouts, max_dogs) -> the task's setup keys
    build_setup: Callable[..., dict[str, Any]]
    drive_length: Callable[[Mapping[str, Any]], float]
    check: Callable[[dict[str, Any]], None]
    create_world: Callable[[dict[str, Any]], World]
    initial_positions: Callable[
        [dict[str, Any], np.random.Generator], tuple[np.ndarray, np.ndarray]
    ]
    is_success: Callable[[SimulationState], bool]
    metrics: Mapping[str, Metric]
    row_columns: Callable[[dict[str, Any], pd.DataFrame], dict[str, Any]]
    # (history, success=, config=) -> Failure
    classify_failure: Callable[..., Failure]


SCENARIOS: dict[str, Scenario] = {
    "drive_to_goal": Scenario(
        layouts=LAYOUTS,
        required_keys=drive_to_goal.REQUIRED_KEYS,
        build_setup=drive_to_goal.build_setup,
        drive_length=drive_to_goal.drive_length,
        check=drive_to_goal.check,
        create_world=goal.create_world,
        initial_positions=drive_to_goal.initial_positions,
        is_success=drive_to_goal.is_success,
        metrics={
            "gcm_goal": goal.gcm_goal,
            "gcm_in_goal": goal.gcm_in_goal,
            "sheep_in_goal": goal.sheep_in_goal,
            "dogs_goal_side": goal.dogs_goal_side,
        },
        row_columns=drive_to_goal.row_columns,
        classify_failure=drive_failures.classify_failure,
    ),
}
