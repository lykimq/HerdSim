"""Observation models for shepherd sensing."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

import numpy as np

from core.simulation_state import SimulationState


@dataclass
class ShepherdObservation:
    """Per-shepherd observation used by dog controllers."""

    shepherd_index: int
    self_position: np.ndarray
    self_velocity: np.ndarray
    goal_center: np.ndarray | None
    sheep_positions: np.ndarray
    sheep_velocities: np.ndarray
    sheep_indices: np.ndarray
    other_shepherd_positions: np.ndarray
    other_shepherd_indices: np.ndarray
    bearings_to_sheep: np.ndarray | None = None
    distances_to_sheep: np.ndarray | None = None
    mode: str = "global"
    messages: list[dict[str, Any]] = field(default_factory=list)

    @property
    def n_sheep_seen(self) -> int:
        return int(self.sheep_positions.shape[0])


class BaseObservationModel(ABC):
    """Build per-shepherd observations from world state."""

    @property
    @abstractmethod
    def id(self) -> str:
        """Observation mode id."""

    @abstractmethod
    def observe(
        self,
        state: SimulationState,
        shepherd_index: int,
        config: dict[str, Any],
    ) -> ShepherdObservation:
        """Return the observation available to one shepherd."""

    def observe_all(
        self, state: SimulationState, config: dict[str, Any]
    ) -> list[ShepherdObservation]:
        return [
            self.observe(state, i, config)
            for i in range(state.n_shepherds)
            if bool(state.shepherd_active[i])
        ]
