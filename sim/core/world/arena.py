"""Simulation environment: boundaries and goal zone."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class GoalZone:
    """Circular target zone where sheep should be herded."""

    center: np.ndarray  # (2,) position
    radius: float

    def contains(self, positions: np.ndarray) -> np.ndarray:
        """Boolean mask: which positions are inside the goal. Shape (N,)."""
        distances = np.linalg.norm(positions - self.center, axis=1)
        return distances <= self.radius


@dataclass
class World:
    """Defines the physical environment for the simulation."""

    width: float
    height: float
    goal: GoalZone

    def reflect_positions(self, positions: np.ndarray) -> np.ndarray:
        """Reflect positions that exceed world boundaries back inside.

        Uses elastic reflection: if an agent crosses a boundary, its position
        is mirrored back by the overshoot amount.
        """
        reflected = positions.copy()

        # Reflect X
        below_x = reflected[:, 0] < 0
        above_x = reflected[:, 0] > self.width
        reflected[below_x, 0] = -reflected[below_x, 0]
        reflected[above_x, 0] = 2 * self.width - reflected[above_x, 0]

        # Reflect Y
        below_y = reflected[:, 1] < 0
        above_y = reflected[:, 1] > self.height
        reflected[below_y, 1] = -reflected[below_y, 1]
        reflected[above_y, 1] = 2 * self.height - reflected[above_y, 1]

        return reflected

    def reflect_velocities(self, positions: np.ndarray, velocities: np.ndarray) -> np.ndarray:
        """Reverse velocity components for agents at boundaries."""
        reflected = velocities.copy()
        at_x_boundary = (positions[:, 0] <= 0) | (positions[:, 0] >= self.width)
        at_y_boundary = (positions[:, 1] <= 0) | (positions[:, 1] >= self.height)
        reflected[at_x_boundary, 0] *= -1
        reflected[at_y_boundary, 1] *= -1
        return reflected
