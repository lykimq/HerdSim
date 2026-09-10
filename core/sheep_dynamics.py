"""Sheep dynamics plugin interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from core.simulation_state import SimulationState


class BaseSheepDynamics(ABC):
    """Update sheep positions and velocities for one tick."""

    @property
    @abstractmethod
    def id(self) -> str:
        """Unique sheep-model identifier."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name."""

    @property
    def default_config(self) -> dict[str, Any]:
        """Model-specific defaults (agent counts + behaviour params)."""
        return {}

    @abstractmethod
    def step(self, state: SimulationState, config: dict[str, Any]) -> SimulationState:
        """Return state with updated sheep positions and velocities."""
