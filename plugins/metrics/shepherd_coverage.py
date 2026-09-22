"""Shepherd coverage of peripheral sheep."""

from __future__ import annotations

import numpy as np

from core.base_metric import BaseMetric
from core.simulation_state import SimulationState


class ShepherdCoverageMetric(BaseMetric):
    """Fraction of peripheral sheep within at least one shepherd influence radius.

    Peripheral sheep are those farther from the flock centroid than the median
    sheep-centroid distance. Influence radius is ``influence_radius`` on
    state.metadata (the trial sensing range, else the method ``r_s``).
    """

    @property
    def id(self) -> str:
        return "coverage"

    @property
    def name(self) -> str:
        return "Shepherd Coverage"

    @property
    def description(self) -> str:
        return (
            "Fraction of peripheral sheep (distance to centroid > median) that "
            "lie within at least one shepherd's influence radius."
        )

    @property
    def unit(self) -> str:
        return "fraction"

    def compute(self, state: SimulationState) -> float:
        if state.n_sheep == 0 or state.n_shepherds == 0:
            return 0.0
        distances = state.distances_to_centroid()
        median = float(np.median(distances))
        peripheral = distances > median
        if not np.any(peripheral):
            # All sheep at the same distance (or single sheep): treat as covered
            # if any sheep is within range of a shepherd.
            peripheral = np.ones(state.n_sheep, dtype=bool)
        raw = state.metadata.get("influence_radius")
        if raw is None:
            return float("nan")
        r_s = float(raw)
        if not np.isfinite(r_s):
            return float("nan")
        sheep = state.sheep_positions[peripheral]
        shepherds = state.shepherd_positions
        # Pairwise sheep-shepherd distances.
        diffs = sheep[:, np.newaxis, :] - shepherds[np.newaxis, :, :]
        dist = np.linalg.norm(diffs, axis=2)
        covered = np.any(dist <= r_s, axis=1)
        return float(np.mean(covered))
