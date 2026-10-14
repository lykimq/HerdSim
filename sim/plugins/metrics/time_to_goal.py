"""Time to Goal metric: tick count when success condition is first met."""

import numpy as np
from core.simulation_state import SimulationState

from .base import BaseMetric


class TimeToGoalMetric(BaseMetric):
    """Reports the current tick if all sheep are in the goal, else -1.

    The actual time-to-goal is determined post-hoc from the history
    as the first tick where this metric returns a non-negative value.
    """

    @property
    def id(self) -> str:
        return "time_to_goal"

    def compute(self, state: SimulationState) -> float:
        goal = state.world.goal
        if goal is None:
            return -1.0
        # Strict full-goal completion (all sheep). Scenario success may use a
        # lower success_fraction; trials.csv first_success_tick records that.
        if np.all(goal.contains(state.sheep_positions)):
            return float(state.tick)
        return -1.0
