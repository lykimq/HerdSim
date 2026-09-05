"""Flock Polarisation metric: alignment of sheep headings."""

import numpy as np

from core.base_metric import BaseMetric
from core.simulation_state import SimulationState


class PolarizationMetric(BaseMetric):
    @property
    def id(self) -> str:
        return "polarization"

    @property
    def name(self) -> str:
        return "Flock Polarisation"

    @property
    def description(self) -> str:
        return "Mean alignment of sheep velocity unit vectors (0=disordered, 1=aligned)."

    def compute(self, state: SimulationState) -> float:
        if state.n_sheep == 0:
            return 0.0
        speeds = np.linalg.norm(state.sheep_velocities, axis=1, keepdims=True)
        # Avoid division by zero for stationary sheep
        moving = speeds.flatten() > 1e-10
        if not np.any(moving):
            return 0.0
        unit_vecs = state.sheep_velocities[moving] / speeds[moving]
        mean_vec = np.mean(unit_vecs, axis=0)
        return float(np.linalg.norm(mean_vec))
