"""Abstract base class that all generic metrics must implement."""

from __future__ import annotations

from abc import ABC, abstractmethod

from core.simulation_state import SimulationState


class BaseMetric(ABC):
    """Interface contract for algorithm-agnostic metrics.

    Each metric computes a single scalar value from the current simulation state.
    Metrics are recorded per-tick by HistoryRecorder and exported as time-series.
    """

    @property
    @abstractmethod
    def id(self) -> str:
        """Unique string identifier, e.g. 'cohesion'."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable display name, e.g. 'Flock Cohesion'."""

    @property
    @abstractmethod
    def description(self) -> str:
        """One-line description shown in UI tooltips and exports."""

    @abstractmethod
    def compute(self, state: SimulationState) -> float:
        """Compute the metric value for the current simulation state.

        Must return a finite float. Return 0.0 for undefined cases
        (e.g. min_separation with < 2 sheep).
        """
