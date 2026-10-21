"""Tasks, keyed by the protocol ``task``.

A task owns everything that depends on what the dogs are asked to do:

- ``build_setup`` turns protocol settings into setup keys (field, goal, starts),
  and ``required_keys`` lists the ones it reads back from the run config;
- ``check`` validates its settings in a built run config;
- ``create_world``, ``initial_positions`` and ``is_success`` run the trial;
- ``metrics`` are recorded every tick next to the generic ones;
- ``row_columns`` and ``classify_failure`` turn a finished trial into its
  task columns and its failure label.

A new task (gate, hold, exit, ...) is one module with these pieces and one
entry below; the engine, the methods and the campaign do not change.
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

from . import drive_failures, drive_metrics, drive_to_goal


@dataclass(frozen=True)
class Scenario:
    required_keys: tuple[str, ...]
    # (settings, flock_radius, n_sheep, layouts, max_dogs) -> the task's setup keys
    build_setup: Callable[..., dict[str, Any]]
    check: Callable[[dict[str, Any]], None]
    create_world: Callable[[dict[str, Any]], World]
    initial_positions: Callable[
        [dict[str, Any], np.random.Generator], tuple[np.ndarray, np.ndarray]
    ]
    is_success: Callable[[SimulationState], bool]
    metrics: Mapping[str, Metric]
    row_columns: Callable[[dict[str, Any], pd.DataFrame], dict[str, Any]]
    # (history, success=, config=) -> Failure
    classify_failure: Callable[..., drive_failures.Failure]


SCENARIOS: dict[str, Scenario] = {
    "drive_to_goal": Scenario(
        required_keys=drive_to_goal.REQUIRED_KEYS,
        build_setup=drive_to_goal.build_setup,
        check=drive_to_goal.check,
        create_world=drive_to_goal.create_world,
        initial_positions=drive_to_goal.initial_positions,
        is_success=drive_to_goal.is_success,
        metrics={
            "gcm_goal": drive_metrics.gcm_goal,
            "gcm_in_goal": drive_metrics.gcm_in_goal,
            "sheep_in_goal": drive_metrics.sheep_in_goal,
            "dogs_goal_side": drive_metrics.dogs_goal_side,
        },
        row_columns=drive_to_goal.row_columns,
        classify_failure=drive_failures.classify_failure,
    ),
}
