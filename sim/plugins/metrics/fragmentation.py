"""Flock fragmentation: largest connected-component fraction under a measurement radius."""

from __future__ import annotations

import numpy as np
from core.simulation_state import SimulationState
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components
from scipy.spatial.distance import pdist, squareform

from .base import BaseMetric


def largest_component_fraction(positions: np.ndarray, radius: float) -> float:
    """Fraction of agents in the largest component (edges if distance <= radius)."""
    n = int(positions.shape[0])
    if n == 0:
        return 0.0
    if n == 1:
        return 1.0
    if radius <= 0.0:
        return 1.0 / float(n)

    # Connected components of the graph with edges where distance <= radius.
    adjacency = squareform(pdist(positions)) <= radius
    _, labels = connected_components(csr_matrix(adjacency), directed=False)
    return float(np.bincount(labels).max()) / float(n)


class FragmentationMetric(BaseMetric):
    """Largest connected-component size / N under experimental measurement_radius.

    measurement_radius is an experiment parameter (state.metadata / shared defaults),
    not an algorithm interaction radius such as Kubo radius or Strombom r_a.
    """

    @property
    def id(self) -> str:
        return "fragmentation"

    def compute(self, state: SimulationState) -> float:
        if state.n_sheep == 0:
            return 0.0
        radius = float(state.metadata.get("measurement_radius", 5.0))
        return largest_component_fraction(state.sheep_positions, radius)
