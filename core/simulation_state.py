"""Unified simulation state passed between engine, algorithms, and metrics."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from core.world import World


@dataclass
class SimulationState:
    """Immutable-style snapshot of the full simulation at one tick.

    Algorithms receive this and return an updated copy.
    Metrics read this to compute scalar values.
    """

    tick: int
    sheep_positions: np.ndarray  # shape (N, 2)
    sheep_velocities: np.ndarray  # shape (N, 2)
    shepherd_positions: np.ndarray  # shape (M, 2)
    shepherd_velocities: np.ndarray  # shape (M, 2)
    world: World
    rng: np.random.Generator
    metadata: dict = field(default_factory=dict)

    @property
    def n_sheep(self) -> int:
        return self.sheep_positions.shape[0]

    @property
    def n_shepherds(self) -> int:
        return self.shepherd_positions.shape[0]

    @property
    def sheep_centroid(self) -> np.ndarray:
        """Global centre of mass (GCM) of the flock."""
        return np.mean(self.sheep_positions, axis=0)

    def distances_to_centroid(self) -> np.ndarray:
        """Euclidean distance of each sheep to the flock centroid. Shape (N,)."""
        diff = self.sheep_positions - self.sheep_centroid
        return np.linalg.norm(diff, axis=1)

    def furthest_sheep_index(self) -> int:
        """Index of the sheep furthest from the flock centroid."""
        return int(np.argmax(self.distances_to_centroid()))
