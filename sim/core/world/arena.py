"""Simulation environment: boundaries, goal zone, optional exit gate."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

# Exited agents park at most this far past the right wall.
EXIT_PARK_DEPTH = 5.0


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
    # Optional gate centred on the right wall: agents inside the opening may
    # leave at x >= width.
    gate_half_width: float | None = None

    @property
    def gate_center(self) -> np.ndarray:
        return np.array([float(self.width), 0.5 * float(self.height)])

    def _in_right_gate(self, positions: np.ndarray) -> np.ndarray:
        if self.gate_half_width is None:
            return np.zeros(len(positions), dtype=bool)
        cy = 0.5 * float(self.height)
        return np.abs(positions[:, 1] - cy) <= float(self.gate_half_width)

    def reflect_positions(self, positions: np.ndarray) -> np.ndarray:
        """Reflect positions that exceed world boundaries back inside.

        Uses elastic reflection: if an agent crosses a boundary, its position
        is mirrored back by the overshoot amount. Agents at the optional right
        gate may park just outside the wall (exited) instead of reflecting.
        """
        reflected = positions.copy()

        # Reflect X
        below_x = reflected[:, 0] < 0
        above_x = reflected[:, 0] > self.width
        reflected[below_x, 0] = -reflected[below_x, 0]
        in_gate = self._in_right_gate(reflected)
        reflect_right = above_x & ~in_gate
        exited = above_x & in_gate
        reflected[reflect_right, 0] = 2 * self.width - reflected[reflect_right, 0]
        if np.any(exited):
            reflected[exited, 0] = np.minimum(reflected[exited, 0], self.width + EXIT_PARK_DEPTH)

        # Reflect Y
        below_y = reflected[:, 1] < 0
        above_y = reflected[:, 1] > self.height
        reflected[below_y, 1] = -reflected[below_y, 1]
        reflected[above_y, 1] = 2 * self.height - reflected[above_y, 1]

        return reflected

    def reflect_velocities(self, positions: np.ndarray, velocities: np.ndarray) -> np.ndarray:
        """Reverse velocity components for agents at boundaries."""
        reflected = velocities.copy()
        in_gate = self._in_right_gate(positions)
        at_right = positions[:, 0] >= self.width
        at_left = positions[:, 0] <= 0
        at_x_boundary = at_left | (at_right & ~in_gate)
        at_y_boundary = (positions[:, 1] <= 0) | (positions[:, 1] >= self.height)
        reflected[at_x_boundary, 0] *= -1
        reflected[at_y_boundary, 1] *= -1
        return reflected
