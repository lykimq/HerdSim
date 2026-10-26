"""Tasks, keyed by the protocol ``task``.

A task owns everything that depends on what the dogs are asked to do:

- ``layouts`` names its start layouts, and ``own_settings`` the canonical settings only it
  reads (hashed only when it runs);
- ``build_setup`` turns protocol settings into setup keys (field, goal, starts),
  and ``required_keys`` lists the ones it reads back from the run config;
- ``calibrates`` says whether its geometry is sized from the calibrated flock radius
  (the drive task) or from its own settings (the gather task);
- ``drive_length`` is the length that deadlines and hold times are multiples of;
- ``check`` validates its settings in a built run config;
- ``create_world``, ``initial_positions``, ``is_success`` and ``is_over`` run the trial:
  ``is_over`` ends a trial before the time limit, as a failure unless ``is_success`` holds;
- ``metrics`` are recorded every tick next to the generic ones;
- ``row_columns`` and ``classify_failure`` turn a finished trial into its
  task columns and its failure label.

A new task is one module with these pieces and one entry below; the engine, the methods and
the campaign do not change.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from sim.core.simulation_state import SimulationState
from sim.core.world.arena import World
from sim.plugins.metrics import Metric

from . import drive_failures, drive_to_goal, gather, goal
from .failures import Failure


def never_over(state: SimulationState, config: dict[str, Any]) -> bool:
    """A task that runs to success or the time limit."""
    return False


@dataclass(frozen=True)
class Scenario:
    layouts: tuple[str, ...]
    own_settings: tuple[str, ...]
    required_keys: tuple[str, ...]
    calibrates: bool
    # (settings, flock_radius, n_sheep, layouts, max_dogs) -> the task's setup keys
    build_setup: Callable[..., dict[str, Any]]
    drive_length: Callable[[Mapping[str, Any]], float]
    check: Callable[[dict[str, Any]], None]
    create_world: Callable[[dict[str, Any]], World]
    initial_positions: Callable[
        [dict[str, Any], np.random.Generator], tuple[np.ndarray, np.ndarray]
    ]
    is_success: Callable[[SimulationState], bool]
    is_over: Callable[[SimulationState, dict[str, Any]], bool]
    metrics: Mapping[str, Metric]
    row_columns: Callable[[dict[str, Any], pd.DataFrame], dict[str, Any]]
    # (history, success=, config=) -> Failure
    classify_failure: Callable[..., Failure]


SCENARIOS: dict[str, Scenario] = {
    "drive_to_goal": Scenario(
        layouts=drive_to_goal.LAYOUTS,
        own_settings=(),
        required_keys=drive_to_goal.REQUIRED_KEYS,
        calibrates=True,
        build_setup=drive_to_goal.build_setup,
        drive_length=drive_to_goal.drive_length,
        check=drive_to_goal.check,
        create_world=goal.create_world,
        initial_positions=drive_to_goal.initial_positions,
        is_success=drive_to_goal.is_success,
        is_over=never_over,
        metrics={
            "gcm_goal": goal.gcm_goal,
            "gcm_in_goal": goal.gcm_in_goal,
            "sheep_in_goal": goal.sheep_in_goal,
            "dogs_goal_side": goal.dogs_goal_side,
        },
        row_columns=drive_to_goal.row_columns,
        classify_failure=drive_failures.classify_failure,
    ),
    "gather": Scenario(
        layouts=gather.LAYOUTS,
        own_settings=gather.OWN_SETTINGS,
        required_keys=gather.REQUIRED_KEYS,
        calibrates=False,
        build_setup=gather.build_setup,
        drive_length=gather.drive_length,
        check=gather.check,
        create_world=goal.create_world,
        initial_positions=gather.initial_positions,
        is_success=gather.is_success,
        is_over=gather.is_over,
        metrics={
            "gcm_goal": goal.gcm_goal,
            "gcm_in_goal": goal.gcm_in_goal,
            "sheep_in_goal": goal.sheep_in_goal,
            "unseen_targets": gather.unseen_targets,
            "dog_radius": gather.dog_radius,
        },
        row_columns=gather.row_columns,
        classify_failure=gather.classify_failure,
    ),
}
