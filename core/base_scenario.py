"""Abstract base class for pluggable simulation scenarios."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import numpy as np

from core.simulation_state import SimulationState
from core.world import World


class BaseScenario(ABC):
    """Interface contract for simulation scenario plugins.

    A scenario defines WHAT the simulation setup looks like:
    - World configuration (boundaries, goals, obstacles)
    - Initial agent placement
    - Success and timeout conditions

    An algorithm defines HOW agents behave.
    Scenarios and algorithms are independent — any algorithm can run in any scenario.
    """

    @property
    @abstractmethod
    def id(self) -> str:
        """Unique string identifier, e.g. 'drive_to_goal'."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable display name."""

    @property
    @abstractmethod
    def description(self) -> str:
        """One-line description of the scenario objective."""

    @property
    def default_config(self) -> dict[str, Any]:
        """Scenario-owned defaults for agents/world (used by 'scenario' preset)."""
        return {}

    @abstractmethod
    def create_world(self, config: dict[str, Any]) -> World:
        """Build the world environment for this scenario."""

    @abstractmethod
    def initial_positions(
        self, config: dict[str, Any], rng: np.random.Generator
    ) -> tuple[np.ndarray, np.ndarray]:
        """Generate initial (sheep_positions, shepherd_positions).

        Returns:
            sheep_positions: shape (n_sheep, 2)
            shepherd_positions: shape (n_shepherds, 2)
        """

    @abstractmethod
    def is_success(self, state: SimulationState, config: dict[str, Any]) -> bool:
        """Check if the scenario objective has been achieved."""

    @abstractmethod
    def max_ticks(self, config: dict[str, Any]) -> int:
        """Maximum number of ticks before the scenario times out."""
