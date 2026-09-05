"""Time to Goal metric: tick count when success condition is first met."""

from core.base_metric import BaseMetric
from core.simulation_state import SimulationState
import numpy as np


class TimeToGoalMetric(BaseMetric):
    """Reports the current tick if all sheep are in the goal, else -1.

    The actual time-to-goal is determined post-hoc from the history
    as the first tick where this metric returns a non-negative value.
    """

    @property
    def id(self) -> str:
        return "time_to_goal"

    @property
    def name(self) -> str:
        return "Time to Goal"

    @property
    def description(self) -> str:
        return "Current tick if all sheep in goal zone, else -1."

    def compute(self, state: SimulationState) -> float:
        goal = state.world.goal
        if goal is None:
            return -1.0
        if np.all(goal.contains(state.sheep_positions)):
            return float(state.tick)
        return -1.0
