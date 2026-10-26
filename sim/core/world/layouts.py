"""Initial agent placement across layouts and dog starting formations.

Layout geometries:
- Compact layout: sized by calibrated flock radius R_f.
- Scattered layouts (wide, split, outlier_rich): scaled by separation distance
  r_a * N^(2/3) to ensure initial outliers require active collection.
- Uniform layout: uniform distribution over a disc (gather scenario).
Gaussian initializations are truncated at CUT_SIGMAS (3.0) to bound starting extents.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import numpy as np

from sim.core.vectors import rotate, unit

LAYOUTS = ("compact", "wide", "split", "outlier_rich")

# Uniform disc layout centered around the goal.
UNIFORM = "uniform"

# Minimum clearance distance from the field boundary.
EDGE_MARGIN = 1.0
# Truncation radius (in standard deviations) for Gaussian flock layouts.
CUT_SIGMAS = 3.0

# Sampler function generating n 2D points with shape (n, 2).
Draw = Callable[[int], np.ndarray]


def _draw_n(n: int, draw: Draw, config: dict[str, Any]) -> np.ndarray:
    """Draw n positions bounded within field margins and strictly outside the goal zone."""
    points = draw(n)
    w, h = float(config["world_width"]), float(config["world_height"])
    goal = np.asarray(config["goal_center"], dtype=float)
    ok = (
        (points[:, 0] >= EDGE_MARGIN)
        & (points[:, 0] <= w - EDGE_MARGIN)
        & (points[:, 1] >= EDGE_MARGIN)
        & (points[:, 1] <= h - EDGE_MARGIN)
        & (np.linalg.norm(points - goal, axis=1) > float(config["goal_radius"]))
    )
    if not ok.all():
        raise RuntimeError(f"{int((~ok).sum())} start sheep outside the field or in the goal")
    return points


def _truncated_gaussian(center: np.ndarray, sigma: float, rng: np.random.Generator) -> Draw:
    """Return a point-drawing closure for a 2D Gaussian truncated at CUT_SIGMAS."""

    def draw(k: int) -> np.ndarray:
        out = np.zeros((0, 2))
        while out.shape[0] < k:
            points = rng.normal(0.0, sigma, size=(k, 2))
            out = np.vstack([out, points[np.linalg.norm(points, axis=1) <= CUT_SIGMAS * sigma]])
        return center + out[:k]

    return draw


def split_geometry(
    n_sheep: int, flock_radius: float, config: dict[str, Any]
) -> tuple[int, float, float]:
    """Return (cluster_count, cluster_sigma, ring_radius) for split flock geometry."""
    k = 2 if n_sheep < 12 else 3
    sigma = float(config["compact_spread"]) * flock_radius / np.sqrt(k)
    return k, sigma, float(config["split_ring"]) * float(config["separation_distance"])


def split_centres(config: dict[str, Any]) -> np.ndarray:
    """Compute cluster center coordinates for the split flock layout."""
    center = np.asarray(config["flock_center"], dtype=float)
    k, _, ring_radius = split_geometry(
        int(config["n_sheep"]), float(config["flock_radius"]), config
    )
    back = unit(center - np.asarray(config["goal_center"], dtype=float))
    angles = (0.0, 2.0 * np.pi / 3.0, -2.0 * np.pi / 3.0) if k == 3 else (np.pi / 2.0, -np.pi / 2.0)
    return np.array([center + ring_radius * rotate(back, angle) for angle in angles])


def place_flock(config: dict[str, Any], rng: np.random.Generator) -> np.ndarray:
    """Sample initial sheep positions for the configured flock layout."""
    n = int(config["n_sheep"])
    layout = str(config["initial_layout"])
    r_f = float(config["flock_radius"])
    center = np.asarray(config["flock_center"], dtype=float)
    compact_sigma = float(config["compact_spread"]) * r_f

    if layout == "compact":
        return _draw_n(n, _truncated_gaussian(center, compact_sigma, rng), config)
    if layout == "wide":
        sigma = float(config["wide_sigma"]) * float(config["separation_distance"])
        return _draw_n(n, _truncated_gaussian(center, sigma, rng), config)
    if layout == "split":
        centres = split_centres(config)
        k, sigma, _ = split_geometry(n, r_f, config)
        counts = np.full(k, n // k)
        counts[: n % k] += 1
        parts = []
        for c, count in zip(centres, counts):
            parts.append(_draw_n(int(count), _truncated_gaussian(c, sigma, rng), config))
        return np.vstack(parts)
    if layout == "outlier_rich":
        n_out = round(float(config["outlier_fraction"]) * n)
        core = _draw_n(n - n_out, _truncated_gaussian(center, compact_sigma, rng), config)
        reach = float(config["separation_distance"])
        near, far = float(config["outlier_near"]), float(config["outlier_far"])

        def outlier_ring(k: int) -> np.ndarray:
            angle = rng.uniform(0.0, 2.0 * np.pi, k)
            radius = reach * rng.uniform(near, far, k)
            return center + radius[:, None] * np.stack([np.cos(angle), np.sin(angle)], axis=1)

        return np.vstack([core, _draw_n(n_out, outlier_ring, config)])
    raise ValueError(f"Unknown initial_layout {layout!r}; expected one of {LAYOUTS}")


def place_uniform_disc(
    centre: np.ndarray, radius: float, n: int, rng: np.random.Generator
) -> np.ndarray:
    """Uniformly sample `n` positions within a 2D disc of specified radius and center."""
    r = radius * np.sqrt(rng.random(n))
    angle = rng.uniform(0.0, 2.0 * np.pi, n)
    return centre + np.stack([r * np.cos(angle), r * np.sin(angle)], axis=1)


def layout_extent(config: dict[str, Any]) -> float:
    """Maximum possible distance of an initial sheep position from the flock center."""
    r_f = float(config["flock_radius"])
    layout = str(config["initial_layout"])
    compact_cut = CUT_SIGMAS * float(config["compact_spread"]) * r_f
    if layout == "compact":
        return compact_cut
    if layout == "wide":
        return CUT_SIGMAS * float(config["wide_sigma"]) * float(config["separation_distance"])
    if layout == "split":
        _, sigma, ring_radius = split_geometry(int(config["n_sheep"]), r_f, config)
        return ring_radius + CUT_SIGMAS * sigma
    far = float(config["outlier_far"]) * float(config["separation_distance"])
    return max(compact_cut, far)


DOG_STARTS = ("arcs", "ring", "handler")


def goal_half_angle(config: dict[str, Any], drive: float) -> float:
    """Angular half-width of the subtended goal disc cone viewed from flock center."""
    if drive <= 0.0:
        return 0.0
    return float(np.arcsin(min(1.0, float(config["goal_radius"]) / drive)))


def _ring_span(config: dict[str, Any], drive: float) -> float:
    """Angular span available for dog rings, excluding the goal-subtended cone."""
    return 2.0 * np.pi - 2.0 * goal_half_angle(config, drive)


def _drive_of(config: dict[str, Any]) -> float:
    flock_center = np.asarray(config["flock_center"], dtype=float)
    return float(np.linalg.norm(np.asarray(config["goal_center"], dtype=float) - flock_center))


def _dog_arcs(config: dict[str, Any], drive: float) -> list[tuple[float, int]]:
    """Compute (radius, dog_count) stations for initial dog placement based on dog_start mode:

    - 'arcs': Concentric semi-circles behind the flock opposite the goal.
    - 'ring': Concentric circular rings around the flock excluding the goal-facing cone.
    - 'handler': Single staging location behind the flock along the drive axis.
    """
    spacing = float(config["dog_start_spacing"])
    radius = layout_extent(config) + float(config["dog_start_gap"])
    left = int(config["n_shepherds"])
    mode = str(config["dog_start"])
    if mode == "handler":
        return [(radius, left)] if left > 0 else []
    span = np.pi if mode == "arcs" else _ring_span(config, drive)
    arcs = []
    while left > 0:
        count = min(left, max(1, int(span * radius / spacing)))
        arcs.append((radius, count))
        left -= count
        radius += spacing
    return arcs


def dog_start_radius(config: dict[str, Any], drive: float) -> float:
    """Distance from flock center to outermost dog starting station."""
    arcs = _dog_arcs(config, drive)
    if not arcs:  # No dogs configured: return zero radius
        return 0.0
    return arcs[-1][0]


def field_size(
    config: dict[str, Any], layouts: tuple[str, ...], drive: float
) -> tuple[float, float, float]:
    """Calculate field dimensions (width, height, flock_start_x) with clearance bounds."""
    reach = max(layout_extent({**config, "initial_layout": name}) for name in layouts)
    dogs = max(dog_start_radius({**config, "initial_layout": name}, abs(drive)) for name in layouts)
    behind = max(reach, dogs)
    sideways = max(behind, float(config["goal_radius"]))
    clearance = float(config["field_clearance"])
    width = clearance + behind + abs(drive) + float(config["goal_radius"]) + clearance
    return width, 2.0 * (sideways + clearance), clearance + behind


def place_dogs(config: dict[str, Any]) -> np.ndarray:
    """Compute deterministic initial dog coordinates based on configured start layout."""
    flock_center = np.asarray(config["flock_center"], dtype=float)
    back = unit(flock_center - np.asarray(config["goal_center"], dtype=float))
    mode = str(config["dog_start"])
    drive = _drive_of(config)
    span = _ring_span(config, drive)
    positions = []
    for radius, count in _dog_arcs(config, drive):
        for j in range(count):
            if mode == "arcs":
                angle = -np.pi / 2.0 + np.pi * (j + 0.5) / count
            elif mode == "ring":
                angle = -span / 2.0 + span * (j + 0.5) / count
            else:
                angle = 0.0
            positions.append(flock_center + radius * rotate(back, angle))
    return np.array(positions).reshape(-1, 2)
