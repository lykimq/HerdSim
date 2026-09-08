"""Geometry helpers for obstacle-aware drive targeting."""

from __future__ import annotations

import numpy as np

from core.world import Obstacle


def _unit(vec: np.ndarray) -> np.ndarray:
    n = float(np.linalg.norm(vec))
    if n < 1e-10:
        return np.zeros(2)
    return vec / n


def segment_intersects_aabb(
    p0: np.ndarray, p1: np.ndarray, obs: Obstacle
) -> bool:
    """True if segment p0->p1 intersects the axis-aligned obstacle (Liang-Barsky)."""
    x0, y0 = float(obs.min_corner[0]), float(obs.min_corner[1])
    x1, y1 = float(obs.max_corner[0]), float(obs.max_corner[1])
    dx = float(p1[0] - p0[0])
    dy = float(p1[1] - p0[1])
    t0, t1 = 0.0, 1.0

    edges = (
        (-dx, float(p0[0]) - x0),
        (dx, x1 - float(p0[0])),
        (-dy, float(p0[1]) - y0),
        (dy, y1 - float(p0[1])),
    )
    for p, q in edges:
        if abs(p) < 1e-15:
            if q < 0:
                return False
            continue
        r = q / p
        if p < 0:
            if r > t1:
                return False
            if r > t0:
                t0 = r
        else:
            if r < t0:
                return False
            if r < t1:
                t1 = r
    return t0 <= t1


def blocking_obstacles(
    p0: np.ndarray, p1: np.ndarray, obstacles: list[Obstacle]
) -> list[Obstacle]:
    """Obstacles whose AABB intersects the segment from p0 to p1."""
    return [o for o in obstacles if segment_intersects_aabb(p0, p1, o)]


def find_gate_gap_center(obstacles: list[Obstacle]) -> np.ndarray | None:
    """Center of a narrow gate formed by two aligned wall obstacles, if any.

    Detects pairs that share an axis overlap with a gap on the other axis
    (narrow_gate style: same x-band, gap in y; or same y-band, gap in x).
    """
    n = len(obstacles)
    if n < 2:
        return None

    best: tuple[float, np.ndarray] | None = None
    for i in range(n):
        for j in range(i + 1, n):
            a, b = obstacles[i], obstacles[j]
            ax0, ay0 = float(a.min_corner[0]), float(a.min_corner[1])
            ax1, ay1 = float(a.max_corner[0]), float(a.max_corner[1])
            bx0, by0 = float(b.min_corner[0]), float(b.min_corner[1])
            bx1, by1 = float(b.max_corner[0]), float(b.max_corner[1])

            x_overlap = min(ax1, bx1) - max(ax0, bx0)
            if x_overlap > 0:
                if ay1 <= by0:
                    gap = by0 - ay1
                    if gap > 1e-6:
                        cx = 0.5 * (max(ax0, bx0) + min(ax1, bx1))
                        cy = 0.5 * (ay1 + by0)
                        cand = (gap, np.array([cx, cy]))
                        if best is None or cand[0] < best[0]:
                            best = cand
                elif by1 <= ay0:
                    gap = ay0 - by1
                    if gap > 1e-6:
                        cx = 0.5 * (max(ax0, bx0) + min(ax1, bx1))
                        cy = 0.5 * (by1 + ay0)
                        cand = (gap, np.array([cx, cy]))
                        if best is None or cand[0] < best[0]:
                            best = cand

            y_overlap = min(ay1, by1) - max(ay0, by0)
            if y_overlap > 0:
                if ax1 <= bx0:
                    gap = bx0 - ax1
                    if gap > 1e-6:
                        cy = 0.5 * (max(ay0, by0) + min(ay1, by1))
                        cx = 0.5 * (ax1 + bx0)
                        cand = (gap, np.array([cx, cy]))
                        if best is None or cand[0] < best[0]:
                            best = cand
                elif bx1 <= ax0:
                    gap = ax0 - bx1
                    if gap > 1e-6:
                        cy = 0.5 * (max(ay0, by0) + min(ay1, by1))
                        cx = 0.5 * (bx1 + ax0)
                        cand = (gap, np.array([cx, cy]))
                        if best is None or cand[0] < best[0]:
                            best = cand

    return None if best is None else best[1]


def _obs_center(obs: Obstacle) -> np.ndarray:
    return 0.5 * (
        np.asarray(obs.min_corner, dtype=float)
        + np.asarray(obs.max_corner, dtype=float)
    )


def _half_extent_along(obs: Obstacle, direction: np.ndarray) -> float:
    """Approximate half-width of AABB projected onto a unit direction."""
    half = 0.5 * (
        np.asarray(obs.max_corner, dtype=float)
        - np.asarray(obs.min_corner, dtype=float)
    )
    d = _unit(direction)
    return float(abs(half[0] * d[0]) + abs(half[1] * d[1]))


def deflect_drive_point(
    gcm: np.ndarray,
    goal: np.ndarray,
    base_pd: np.ndarray,
    obstacles: list[Obstacle],
    clearance: float,
) -> np.ndarray:
    """Offset Pd around blocking obstacles or toward a gate gap.

    If GCM->goal is clear, returns base_pd. If a narrow-gate gap exists and
    lies ahead, aims the virtual goal through the gap. Otherwise offsets
    perpendicular to GCM->goal by obstacle half-width + clearance on the
    shorter-path side.
    """
    blocked = blocking_obstacles(gcm, goal, obstacles)
    if not blocked:
        return base_pd

    to_goal = goal - gcm
    dist_goal = float(np.linalg.norm(to_goal))
    if dist_goal < 1e-10:
        return base_pd
    forward = to_goal / dist_goal
    perp = np.array([-forward[1], forward[0]])

    gate = find_gate_gap_center(obstacles)
    if gate is not None:
        along = float(np.dot(gate - gcm, forward))
        if 0.0 < along < dist_goal:
            aim = gate + forward * max(clearance, 1.0)
            offset = float(np.linalg.norm(base_pd - gcm))
            if offset < 1e-10:
                offset = clearance
            behind = gcm - aim
            bn = float(np.linalg.norm(behind))
            if bn < 1e-10:
                return base_pd
            return gcm + (behind / bn) * offset

    nearest = min(blocked, key=lambda o: float(np.linalg.norm(_obs_center(o) - gcm)))
    half_w = _half_extent_along(nearest, perp)
    lateral = half_w + float(clearance)

    left = base_pd + perp * lateral
    right = base_pd - perp * lateral
    obs_c = _obs_center(nearest)
    left_cost = float(np.linalg.norm(left - obs_c) + np.linalg.norm(goal - left))
    right_cost = float(np.linalg.norm(right - obs_c) + np.linalg.norm(goal - right))
    return left if left_cost <= right_cost else right
