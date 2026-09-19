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
        return (
            "Simulation tick when all sheep are inside the goal zone, "
            "else -1. Strict full-goal metric (discrete ticks, not wall-clock). "
            "Scenario success may allow a partial flock; use first_success_tick "
            "in benchmark exports for the scenario criterion."
        )

    @property
    def unit(self) -> str:
        return "ticks"

    def compute(self, state: SimulationState) -> float:
        goal = state.world.goal
        if goal is None:
            return -1.0
        # Strict full-goal completion (all sheep). Scenario success may use a
        # lower success_fraction; see benchmark first_success_tick for that.
        if np.all(goal.contains(state.sheep_positions)):
            return float(state.tick)
        return -1.0
