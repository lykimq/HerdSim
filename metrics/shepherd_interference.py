"""Shepherd interference index I_dir from realised shepherd velocities."""

from __future__ import annotations

import numpy as np

from core.base_metric import BaseMetric
from core.simulation_state import SimulationState

# Shepherds slower than this are treated as stationary and excluded from I_dir.
_STATIONARY_SPEED = 1e-6


class ShepherdInterferenceMetric(BaseMetric):
    """Directional conflict among moving shepherds.

    I_dir = 1 - ||sum u_i|| / M_active, where u_i are unit velocity directions of
    shepherds with speed above the stationary threshold. 0 means all moving
    shepherds agree in direction; 1 means maximal conflict.

    Caveat: uses realised (post-constraint) velocities, so wall reflections can
    inflate I_dir near boundaries.
    """

    @property
    def id(self) -> str:
        return "i_dir"

    @property
    def name(self) -> str:
        return "Shepherd Interference"

    @property
    def description(self) -> str:
        return (
            "Interference index I_dir = 1 - ||sum unit velocities|| / M_active "
            "over moving shepherds (speed > 1e-6). Realised velocities; walls "
            "may inflate the value near boundaries."
        )

    @property
    def unit(self) -> str:
        return "fraction"

    def compute(self, state: SimulationState) -> float:
        vels = np.asarray(state.shepherd_velocities, dtype=float)
        if vels.size == 0:
            return 0.0
        speeds = np.linalg.norm(vels, axis=1)
        moving = speeds > _STATIONARY_SPEED
        m_active = int(moving.sum())
        if m_active == 0:
            return 0.0
        unit_vecs = vels[moving] / speeds[moving, np.newaxis]
        resultant = float(np.linalg.norm(unit_vecs.sum(axis=0)))
        return float(1.0 - resultant / m_active)
