"""Flock fragmentation: largest connected-component fraction under a measurement radius."""

from __future__ import annotations

import numpy as np

from core.base_metric import BaseMetric
from core.simulation_state import SimulationState


def largest_component_fraction(positions: np.ndarray, radius: float) -> float:
    """Fraction of agents in the largest component (edges if distance <= radius)."""
    n = int(positions.shape[0])
    if n == 0:
        return 0.0
    if n == 1:
        return 1.0
    if radius <= 0.0:
        return 1.0 / float(n)

    # Union-find over pairwise distances within the experimental radius.
    parent = np.arange(n, dtype=int)

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i: int, j: int) -> None:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[rj] = ri

    for i in range(n):
        for j in range(i + 1, n):
            if np.linalg.norm(positions[i] - positions[j]) <= radius:
                union(i, j)

    roots = np.array([find(i) for i in range(n)], dtype=int)
    _, counts = np.unique(roots, return_counts=True)
    return float(counts.max()) / float(n)


class FragmentationMetric(BaseMetric):
    """Largest connected-component size / N under experimental measurement_radius.

    measurement_radius is an experiment parameter (state.metadata / shared defaults),
    not an algorithm interaction radius such as Kubo radius or Strombom r_a.
    """

    @property
    def id(self) -> str:
        return "fragmentation"

    @property
    def name(self) -> str:
        return "Flock Fragmentation"

    @property
    def description(self) -> str:
        return (
            "Size of the largest sheep connected component divided by N, using "
            "edges when pairwise distance <= measurement_radius. 1.0 is one flock; "
            "lower values mean the flock is split. Radius is experimental, not "
            "taken from algorithm gains."
        )

    @property
    def unit(self) -> str:
        return "fraction"

    def compute(self, state: SimulationState) -> float:
        if state.n_sheep == 0:
            return 0.0
        radius = float(state.metadata.get("measurement_radius", 5.0))
        return largest_component_fraction(state.sheep_positions, radius)
