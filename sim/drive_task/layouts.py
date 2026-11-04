"""Flock start layouts and dog start stations.

Compact (and split clusters) use R_f. Scattered layouts use the Strombom collect
distance r_a N^(2/3), so they leave the drive rule. ``layout_extent`` bounds every
start (Gaussians cut at ``CUT_SIGMAS``); the field and dog stations size from it.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import numpy as np

from sim.vectors import angle_vectors, rotate, unit

LAYOUTS = ("compact", "wide", "split", "outlier_rich")
DOG_STARTS = ("arcs", "ring", "handler")
# Sheep and dogs uniform in two square boxes, as Strombom et al. (2014, section 4.1) start them.
# Not a study layout above: only the check against that paper (paper_check/) uses it.
BOX_LAYOUT = "boxes"

# Agents start at least this far inside the field edge.
EDGE_MARGIN = 1.0
# Hard edge of Gaussian layouts (2-D Gaussian keeps ~98.9% of mass inside 3 sigma).
CUT_SIGMAS = 3.0
# Split layout: two clusters for a small flock, three from this many sheep, at these angles.
SPLIT_THREE_FROM_N = 12
SPLIT_TWO_ANGLES = (np.pi / 2.0, -np.pi / 2.0)
SPLIT_THREE_ANGLES = (0.0, 2.0 * np.pi / 3.0, -2.0 * np.pi / 3.0)

Draw = Callable[[int], np.ndarray]


def _draw_n(n: int, draw: Draw, config: dict[str, Any]) -> np.ndarray:
    """``n`` points inside the field (with margin) and outside the goal.

    Out-of-bounds means a sizing bug: raise rather than redraw (that would change the layout).
    """
    if n <= 0:
        return np.zeros((0, 2))
    points = draw(n)
    w = float(config["world_width"])
    h = float(config["world_height"])
    goal = np.asarray(config["goal_center"], dtype=float)
    inside = (
        (points[:, 0] >= EDGE_MARGIN)
        & (points[:, 0] <= w - EDGE_MARGIN)
        & (points[:, 1] >= EDGE_MARGIN)
        & (points[:, 1] <= h - EDGE_MARGIN)
        & (np.linalg.norm(points - goal, axis=1) > float(config["goal_radius"]))
    )
    if not inside.all():
        raise RuntimeError(f"{int((~inside).sum())} start sheep outside the field or in the goal")
    return points


def _truncated_gaussian(center: np.ndarray, sigma: float, rng: np.random.Generator) -> Draw:
    """Gaussian around ``center``, cut at ``CUT_SIGMAS`` sigma."""
    cut = CUT_SIGMAS * sigma

    def draw(k: int) -> np.ndarray:
        # Same draw size each round keeps the RNG stream, and so the stored trials, identical.
        chunks: list[np.ndarray] = []
        filled = 0
        while filled < k:
            points = rng.normal(0.0, sigma, size=(k, 2))
            kept = points[np.linalg.norm(points, axis=1) <= cut]
            chunks.append(kept)
            filled += kept.shape[0]
        return center + np.vstack(chunks)[:k]

    return draw


def _compact_sigma(config: dict[str, Any]) -> float:
    return float(config["compact_spread"]) * float(config["flock_radius"])


def _wide_sigma(config: dict[str, Any]) -> float:
    return float(config["wide_sigma"]) * float(config["separation_distance"])


def _split_params(config: dict[str, Any]) -> tuple[tuple[float, ...], float, float]:
    """(cluster angles, cluster sigma, ring radius): same density as compact, past the collect
    distance. The angles are from the direction away from the goal."""
    angles = SPLIT_TWO_ANGLES if int(config["n_sheep"]) < SPLIT_THREE_FROM_N else SPLIT_THREE_ANGLES
    sigma = _compact_sigma(config) / np.sqrt(len(angles))
    ring = float(config["split_ring"]) * float(config["separation_distance"])
    return angles, sigma, ring


def _place_compact(config: dict[str, Any], rng: np.random.Generator) -> np.ndarray:
    center = np.asarray(config["flock_center"], dtype=float)
    draw = _truncated_gaussian(center, _compact_sigma(config), rng)
    return _draw_n(int(config["n_sheep"]), draw, config)


def _place_wide(config: dict[str, Any], rng: np.random.Generator) -> np.ndarray:
    center = np.asarray(config["flock_center"], dtype=float)
    draw = _truncated_gaussian(center, _wide_sigma(config), rng)
    return _draw_n(int(config["n_sheep"]), draw, config)


def _place_split(config: dict[str, Any], rng: np.random.Generator) -> np.ndarray:
    """Clusters in turn; the remainder of N / k goes to the first clusters."""
    n = int(config["n_sheep"])
    center = np.asarray(config["flock_center"], dtype=float)
    angles, sigma, ring = _split_params(config)
    back = unit(center - np.asarray(config["goal_center"], dtype=float))
    centres = np.array([center + ring * rotate(back, angle) for angle in angles])
    counts = np.full(len(angles), n // len(angles), dtype=int)
    counts[: n % len(angles)] += 1
    parts = [
        _draw_n(int(count), _truncated_gaussian(centre, sigma, rng), config)
        for centre, count in zip(centres, counts, strict=True)
    ]
    return np.vstack(parts)


def _place_outlier_rich(config: dict[str, Any], rng: np.random.Generator) -> np.ndarray:
    """A compact core plus outliers on a ring between ``outlier_near`` and ``outlier_far``."""
    n = int(config["n_sheep"])
    center = np.asarray(config["flock_center"], dtype=float)
    n_out = round(float(config["outlier_fraction"]) * n)
    core = _draw_n(n - n_out, _truncated_gaussian(center, _compact_sigma(config), rng), config)
    reach = float(config["separation_distance"])
    near = float(config["outlier_near"])
    far = float(config["outlier_far"])

    def outlier_ring(k: int) -> np.ndarray:
        angle = rng.uniform(0.0, 2.0 * np.pi, k)
        radius = reach * rng.uniform(near, far, k)
        return center + radius[:, None] * angle_vectors(angle)

    return np.vstack([core, _draw_n(n_out, outlier_ring, config)])


_PLACERS: dict[str, Callable[[dict[str, Any], np.random.Generator], np.ndarray]] = {
    "compact": _place_compact,
    "wide": _place_wide,
    "split": _place_split,
    "outlier_rich": _place_outlier_rich,
}


def place_boxes(config: dict[str, Any], rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Sheep uniform in the square ``sheep_box``, then the dogs uniform in the square
    ``dog_box``, both from ``rng``; a box is (low, high) on both axes."""
    sheep_low, sheep_high = config["sheep_box"]
    dog_low, dog_high = config["dog_box"]
    sheep = rng.uniform(float(sheep_low), float(sheep_high), (int(config["n_sheep"]), 2))
    dogs = rng.uniform(float(dog_low), float(dog_high), (int(config["n_shepherds"]), 2))
    return sheep, dogs


def place_flock(config: dict[str, Any], rng: np.random.Generator) -> np.ndarray:
    """Sheep positions for the configured layout around the flock start centre."""
    layout = str(config["initial_layout"])
    if layout not in _PLACERS:
        raise ValueError(f"Unknown initial_layout {layout!r}; expected one of {LAYOUTS}")
    return _PLACERS[layout](config, rng)


def layout_extent(config: dict[str, Any]) -> float:
    """Largest distance a sheep can start from the flock centre (exact per layout)."""
    layout = str(config["initial_layout"])
    compact_cut = CUT_SIGMAS * _compact_sigma(config)
    if layout == "compact":
        return compact_cut
    if layout == "wide":
        return CUT_SIGMAS * _wide_sigma(config)
    if layout == "split":
        _, sigma, ring = _split_params(config)
        return ring + CUT_SIGMAS * sigma
    if layout == "outlier_rich":
        far = float(config["outlier_far"]) * float(config["separation_distance"])
        return max(compact_cut, far)
    raise ValueError(f"Unknown initial_layout {layout!r}; expected one of {LAYOUTS}")


def goal_half_angle(config: dict[str, Any], drive: float) -> float:
    """Half-angle of the goal disc as seen from the flock centre at distance ``drive``."""
    if drive <= 0.0:
        return 0.0
    return float(np.arcsin(min(1.0, float(config["goal_radius"]) / drive)))


def _dog_arcs(config: dict[str, Any], drive: float) -> list[tuple[float, float, int]]:
    """(radius, span, count) rings for ``dog_start``. Handler uses span 0 (stacked at one point)."""
    spacing = float(config["dog_start_spacing"])
    radius = layout_extent(config) + float(config["dog_start_gap"])
    left = int(config["n_shepherds"])
    mode = str(config["dog_start"])
    if left <= 0:
        return []
    if mode == "handler":
        return [(radius, 0.0, left)]
    span = np.pi if mode == "arcs" else 2.0 * np.pi - 2.0 * goal_half_angle(config, drive)
    arcs: list[tuple[float, float, int]] = []
    while left > 0:
        count = min(left, max(1, int(span * radius / spacing)))
        arcs.append((radius, span, count))
        left -= count
        radius += spacing
    return arcs


def place_dogs(config: dict[str, Any]) -> np.ndarray:
    """Deterministic dog starts for ``dog_start`` (sector centres; handler = one point)."""
    flock = np.asarray(config["flock_center"], dtype=float)
    goal = np.asarray(config["goal_center"], dtype=float)
    back = unit(flock - goal)
    mode = str(config["dog_start"])
    arcs = _dog_arcs(config, float(np.linalg.norm(goal - flock)))
    n_dogs = sum(count for _, _, count in arcs)
    if n_dogs == 0:
        return np.zeros((0, 2))

    positions = np.empty((n_dogs, 2))
    i = 0
    for radius, span, count in arcs:
        if mode == "handler":
            positions[i : i + count] = flock + radius * back
            i += count
            continue
        angles = -span / 2.0 + span * (np.arange(count) + 0.5) / count
        for angle in angles:
            positions[i] = flock + radius * rotate(back, float(angle))
            i += 1
    return positions


def field_size(
    config: dict[str, Any], layouts: tuple[str, ...], drive: float
) -> tuple[float, float, float]:
    """(width, height, flock_x): shared field for all layouts and ``n_shepherds`` at one N."""
    abs_drive = abs(drive)
    goal_radius = float(config["goal_radius"])
    clearance = float(config["field_clearance"])
    reach = 0.0
    dogs = 0.0
    for name in layouts:
        cfg = {**config, "initial_layout": name}
        reach = max(reach, layout_extent(cfg))
        arcs = _dog_arcs(cfg, abs_drive)
        if arcs:
            dogs = max(dogs, arcs[-1][0])
    behind = max(reach, dogs)
    sideways = max(behind, goal_radius)
    width = 2.0 * clearance + behind + abs_drive + goal_radius
    height = 2.0 * (sideways + clearance)
    flock_x = clearance + behind
    return width, height, flock_x
