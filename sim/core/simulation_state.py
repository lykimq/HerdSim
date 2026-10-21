"""State of one trial at one tick, passed between the engine, plugins and metrics."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any

import numpy as np

from sim.core.world.arena import World


@dataclass
class SimulationState:
    """Positions and velocities of every agent, plus the world and the trial RNGs.

    Sheep models and dog controllers return an updated copy each tick.
    ``rng`` is the sheep's random stream and ``dog_rng`` the dogs', kept
    apart so the sheep draw the same numbers whatever the dog count.
    ``metadata`` holds per-trial constants the metrics need (radii), the
    running dog path length, and what the controllers remember between
    ticks (the dogs' last known flock centroid), so a seed replays exactly
    from the state alone.
    """

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
