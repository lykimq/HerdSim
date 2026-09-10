"""Dog controller plugin interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from core.observation import ShepherdObservation
from core.simulation_state import SimulationState


class BaseDogController(ABC):
    """Update shepherd positions and velocities from observations."""

    @property
    @abstractmethod
    def id(self) -> str:
        """Unique dog-controller identifier."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name."""

    @property
    def default_config(self) -> dict[str, Any]:
        """Controller-specific defaults."""
        return {}

    @abstractmethod
    def step(
        self,
        state: SimulationState,
        observations: list[ShepherdObservation],
        config: dict[str, Any],
    ) -> SimulationState:
        """Return state with updated shepherd positions and velocities.

        Controllers must use observations only for sensing. Full state may be
        used for writing positions/velocities and metadata.
        """
