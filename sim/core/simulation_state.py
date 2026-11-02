"""State of one trial at one tick, passed between the engine, plugins and metrics."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any

import numpy as np

from sim.core.world.arena import World


@dataclass
class SimulationState:
    """Positions, velocities, world, RNGs; sheep/dog streams kept apart for paired D."""

    tick: int
    sheep_positions: np.ndarray  # (N, 2)
    sheep_velocities: np.ndarray  # (N, 2)
    shepherd_positions: np.ndarray  # (D, 2)
    shepherd_velocities: np.ndarray  # (D, 2)
    world: World
    rng: np.random.Generator
    dog_rng: np.random.Generator
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def n_sheep(self) -> int:
        return self.sheep_positions.shape[0]

    @property
    def n_shepherds(self) -> int:
        return self.shepherd_positions.shape[0]

    def copy_with(self, **kwargs: Any) -> SimulationState:
        """New state with the given fields replaced."""
        return replace(self, **kwargs)
