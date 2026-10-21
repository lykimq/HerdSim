"""Per-tick view of a state with shared, lazily computed geometry.

Several metrics need the same distances; the view computes each once per tick.
``config`` is the trial's run config, where metrics read their constants
(measurement radius, lost radius, ...).
"""

from __future__ import annotations

from functools import cached_property
from typing import Any

import numpy as np
from scipy.spatial import ConvexHull, QhullError, cKDTree
from scipy.spatial.distance import pdist

from sim.core.simulation_state import SimulationState


class TickView:
    def __init__(self, state: SimulationState, config: dict[str, Any]) -> None:
        self.state = state
        self.config = config

    @cached_property
    def centroid(self) -> np.ndarray:
        return self.state.sheep_positions.mean(axis=0)

    @cached_property
    def distances_to_centroid(self) -> np.ndarray:
        return np.linalg.norm(self.state.sheep_positions - self.centroid, axis=1)

    @cached_property
    def sheep_tree(self) -> cKDTree:
        return cKDTree(self.state.sheep_positions)

    @cached_property
    def hull(self) -> tuple[float, float]:
        """(perimeter, area) of the sheep convex hull.

        Fewer than 3 sheep, or all on one line: area 0 and perimeter twice the
        longest sheep-sheep distance.
        """
        pts = self.state.sheep_positions
        if pts.shape[0] >= 3:
            try:
                hull = ConvexHull(pts)
            except QhullError:
                pass
            else:
                return float(hull.area), float(hull.volume)
        return (2.0 * float(pdist(pts).max()) if pts.shape[0] > 1 else 0.0), 0.0

    @cached_property
    def dog_pair_distances(self) -> np.ndarray:
        """Condensed pairwise dog distances (scipy ``pdist`` order)."""
        return pdist(self.state.shepherd_positions)

    @cached_property
    def dog_speeds(self) -> np.ndarray:
        return np.linalg.norm(self.state.shepherd_velocities, axis=1)
