"""Simulation environment: boundaries, goal zones, obstacles."""

from __future__ import annotations

from dataclasses import dataclass, field

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


def clamp_goal_center(
    center: np.ndarray | list[float],
    radius: float,
    width: float,
    height: float,
) -> np.ndarray:
    """Clamp a goal centre so the full disk stays inside the arena.

    Clamping only the centre to [0, width] lets a goal with positive radius
    sit half outside the walls. Valid centres lie in
    [radius, width - radius] x [radius, height - radius] when the arena is
    large enough; otherwise the centre is pinned to the arena mid-point.
    """
    r = max(0.0, float(radius))
    w = float(width)
    h = float(height)
    c = np.asarray(center, dtype=float).reshape(2)

    if w <= 0 or h <= 0:
        return c.copy()

    if 2.0 * r >= w:
        cx = 0.5 * w
    else:
        cx = float(np.clip(c[0], r, w - r))

    if 2.0 * r >= h:
        cy = 0.5 * h
    else:
        cy = float(np.clip(c[1], r, h - r))

    return np.array([cx, cy], dtype=float)

@dataclass
class Obstacle:
    """Rectangular obstacle that agents cannot pass through."""

    min_corner: np.ndarray  # (2,) bottom-left
    max_corner: np.ndarray  # (2,) top-right


@dataclass
class World:
    """Defines the physical environment for the simulation."""

    width: float = 150.0
    height: float = 150.0
    dt: float = 0.1  # seconds per tick
    scale: float = 1.0  # meters per spatial unit
    goal: GoalZone | None = None
    obstacles: list[Obstacle] = field(default_factory=list)

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

    def reflect_velocities(
        self, positions: np.ndarray, velocities: np.ndarray
    ) -> np.ndarray:
        """Reverse velocity components for agents at boundaries."""
        reflected = velocities.copy()
        at_x_boundary = (positions[:, 0] <= 0) | (positions[:, 0] >= self.width)
        at_y_boundary = (positions[:, 1] <= 0) | (positions[:, 1] >= self.height)
        reflected[at_x_boundary, 0] *= -1
        reflected[at_y_boundary, 1] *= -1
        return reflected

    def resolve_obstacles(self, positions: np.ndarray) -> np.ndarray:
        """Push agents that overlap rectangular obstacles to the nearest edge."""
        if not self.obstacles:
            return positions

        resolved = positions.copy()
        for obs in self.obstacles:
            x0, y0 = obs.min_corner
            x1, y1 = obs.max_corner
            inside = (
                (resolved[:, 0] >= x0)
                & (resolved[:, 0] <= x1)
                & (resolved[:, 1] >= y0)
                & (resolved[:, 1] <= y1)
            )
            if not np.any(inside):
                continue

            pts = resolved[inside]
            dist_left = pts[:, 0] - x0
            dist_right = x1 - pts[:, 0]
            dist_bottom = pts[:, 1] - y0
            dist_top = y1 - pts[:, 1]
            dists = np.stack([dist_left, dist_right, dist_bottom, dist_top], axis=1)
            side = np.argmin(dists, axis=1)

            pts[side == 0, 0] = x0
            pts[side == 1, 0] = x1
            pts[side == 2, 1] = y0
            pts[side == 3, 1] = y1
            resolved[inside] = pts

        return resolved
