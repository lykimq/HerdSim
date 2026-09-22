"""Unified simulation state passed between engine, plugins, and metrics."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any

import numpy as np

from core.world import World


@dataclass
class SimulationState:
    """Snapshot of the full simulation at one tick.

    Sheep dynamics and dog controllers return an updated copy each tick.
    Metrics read this to compute scalar values.

    Per-agent arrays are always length-N or length-M after construction.
    Empty defaults are resized in ``__post_init__``.
    """

    tick: int
    sheep_positions: np.ndarray  # shape (N, 2)
    sheep_velocities: np.ndarray  # shape (N, 2)
    shepherd_positions: np.ndarray  # shape (M, 2)
    shepherd_velocities: np.ndarray  # shape (M, 2)
    world: World
    rng: np.random.Generator
    metadata: dict[str, Any] = field(default_factory=dict)
    sheep_response: np.ndarray = field(
        default_factory=lambda: np.ones(0, dtype=float)
    )
    sheep_cohesion: np.ndarray = field(
        default_factory=lambda: np.ones(0, dtype=float)
    )
    shepherd_speed_scale: np.ndarray = field(
        default_factory=lambda: np.ones(0, dtype=float)
    )
    shepherd_sensing_scale: np.ndarray = field(
        default_factory=lambda: np.ones(0, dtype=float)
    )
    shepherd_active: np.ndarray = field(
        default_factory=lambda: np.ones(0, dtype=bool)
    )

    def __post_init__(self) -> None:
        n = int(self.sheep_positions.shape[0])
        m = int(self.shepherd_positions.shape[0])
        if int(self.sheep_response.shape[0]) != n:
            self.sheep_response = np.ones(n, dtype=float)
        else:
            self.sheep_response = np.asarray(self.sheep_response, dtype=float)
        if int(self.sheep_cohesion.shape[0]) != n:
            self.sheep_cohesion = np.ones(n, dtype=float)
        else:
            self.sheep_cohesion = np.asarray(self.sheep_cohesion, dtype=float)
        if int(self.shepherd_speed_scale.shape[0]) != m:
            self.shepherd_speed_scale = np.ones(m, dtype=float)
        else:
            self.shepherd_speed_scale = np.asarray(
                self.shepherd_speed_scale, dtype=float
            )
        if int(self.shepherd_sensing_scale.shape[0]) != m:
            self.shepherd_sensing_scale = np.ones(m, dtype=float)
        else:
            self.shepherd_sensing_scale = np.asarray(
                self.shepherd_sensing_scale, dtype=float
            )
        if int(self.shepherd_active.shape[0]) != m:
            self.shepherd_active = np.ones(m, dtype=bool)
        else:
            self.shepherd_active = np.asarray(self.shepherd_active, dtype=bool)

    @property
    def n_sheep(self) -> int:
        return self.sheep_positions.shape[0]

    @property
    def n_shepherds(self) -> int:
        return self.shepherd_positions.shape[0]

    @property
    def sheep_centroid(self) -> np.ndarray:
        """Global centre of mass (GCM) of the flock."""
        if self.n_sheep == 0:
            return np.zeros(2)
        return np.mean(self.sheep_positions, axis=0)

    def distances_to_centroid(self) -> np.ndarray:
        """Euclidean distance of each sheep to the flock centroid. Shape (N,)."""
        diff = self.sheep_positions - self.sheep_centroid
        return np.linalg.norm(diff, axis=1)

    def furthest_sheep_index(self) -> int:
        """Index of the sheep furthest from the flock centroid."""
        return int(np.argmax(self.distances_to_centroid()))

    def copy_with(self, **kwargs: Any) -> SimulationState:
        """Return a new state with selected fields replaced."""
        return replace(self, **kwargs)
