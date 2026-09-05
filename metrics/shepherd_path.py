"""Shepherd Path Length metric: cumulative distance traveled by shepherds."""

import numpy as np

from core.base_metric import BaseMetric
from core.simulation_state import SimulationState


class ShepherdPathMetric(BaseMetric):
    """Tracks cumulative path length across ticks.

    Each call adds the current step distance to the running total.
    """

    def __init__(self):
        self._cumulative = 0.0
        self._prev_positions: np.ndarray | None = None

    @property
    def id(self) -> str:
        return "shepherd_path"

    @property
    def name(self) -> str:
        return "Shepherd Path Length"

    @property
    def description(self) -> str:
        return "Cumulative Euclidean distance traveled by all shepherds."

    def compute(self, state: SimulationState) -> float:
        if self._prev_positions is not None:
            step_distances = np.linalg.norm(
                state.shepherd_positions - self._prev_positions, axis=1
            )
            self._cumulative += float(step_distances.sum())
        self._prev_positions = state.shepherd_positions.copy()
        return self._cumulative

    def reset(self) -> None:
        self._cumulative = 0.0
        self._prev_positions = None
