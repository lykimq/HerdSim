"""Arena: start rectangle and circular goal.

No walls (Strombom 2014): agents may leave. The rectangle only sizes the start,
goal and dog arcs (see ``field_size`` in layouts.py).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


@dataclass
class GoalZone:
    """Circular target zone."""

    center: np.ndarray  # (2,)
    radius: float
    # Share of the sheep that must be inside for the goal to count as reached; 1 is every sheep.
    required_fraction: float = 1.0

    def contains(self, positions: np.ndarray) -> np.ndarray:
        """Which positions are inside the goal, shape (n,)."""
        return np.linalg.norm(positions - self.center, axis=1) <= self.radius

    def reached(self, positions: np.ndarray) -> bool:
        """True when at least ``required_fraction`` of the sheep are inside (all, at 1)."""
        needed = math.ceil(self.required_fraction * len(positions) - 1e-9)
        return int(self.contains(positions).sum()) >= needed


@dataclass
class World:
    width: float
    height: float
    goal: GoalZone
