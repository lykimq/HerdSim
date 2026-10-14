"""Flock Polarisation metric: alignment of sheep headings."""

import numpy as np
from core.simulation_state import SimulationState

from .base import BaseMetric


class PolarizationMetric(BaseMetric):
    """Mean alignment of sheep velocity unit vectors (0=disordered, 1=aligned)."""

    @property
    def id(self) -> str:
        return "polarization"

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
