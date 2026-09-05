"""Abstract base class that all herding algorithms must implement."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from core.simulation_state import SimulationState


class BaseAlgorithm(ABC):
    """Interface contract for herding algorithm plugins.

    To create a new algorithm:
    1. Create a folder in algorithms/<your_algo>/
    2. Subclass BaseAlgorithm in algorithm.py
    3. Implement id, name, default_config, step()
    4. It auto-registers via AlgorithmRegistry
    """

    @property
    @abstractmethod
    def id(self) -> str:
        """Unique string identifier, e.g. 'strombom'."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable display name, e.g. 'Strömbom 2014'."""

    @property
    @abstractmethod
    def default_config(self) -> dict[str, Any]:
        """Default parameter values shown in UI and used if not overridden."""

    @abstractmethod
    def step(self, state: SimulationState, config: dict[str, Any]) -> SimulationState:
        """Compute one simulation tick.

        Receives the current state and configuration parameters.
        Returns an updated SimulationState with new positions and velocities.
        The algorithm should use state.rng for any randomness.
        """
