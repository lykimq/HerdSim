"""Start positions: flock layouts and the dog stations.

Two lengths size the layouts. The compact flock (and each cluster of the split layout)
uses the flock radius R_f. The scattered layouts (wide, split ring, outliers) use the
separation distance, the distance from the flock centre beyond which Strombom 2014 collects
a sheep (r_a N^(2/3), p.7). A scattered layout sized by R_f never leaves the drive rule at
N >= 100, so it would not test collecting at all.

The separation distance means nothing to Kubo sheep, which have no collect rule and whose
only length is the view radius 20; for them a scattered start is just a sparse flock. The
protocols therefore run Kubo on the compact layout only.

Every Gaussian draw is cut at ``CUT_SIGMAS`` sigma and the outlier ring is bounded by
construction, so ``layout_extent`` is an exact bound on where a sheep can start, and the
field, the drive and the dog stations are sized from it.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import numpy as np

from sim.core.vectors import rotate, unit

LAYOUTS = ("compact", "wide", "split", "outlier_rich")

# The gather task's layout: agents uniform over a disc round the goal (Lama and di Bernardo
# 2024, Fig. 1a), sized by the disc radius, not by R_f.
UNIFORM = "uniform"

# Agents start at least this far inside the field edge.
EDGE_MARGIN = 1.0
# Radius of the Gaussian layouts in sigmas. A 2-D Gaussian has 1.1% of its mass beyond
# 3 sigma, so the cut barely changes the shape but gives every layout a hard edge.
CUT_SIGMAS = 3.0

# Draws n candidate points at once, shape (n, 2).
Draw = Callable[[int], np.ndarray]


def _draw_n(n: int, draw: Draw, config: dict[str, Any]) -> np.ndarray:
    """``n`` points, all inside the field (with margin) and outside the goal.

    The task sizes the field and the drive from ``layout_extent`` so that every possible
    start fits. A point outside is a sizing bug, so it raises instead of being redrawn:
    a redraw would quietly change the layout's shape.
    """
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
    """Gaussian round ``center`` cut at ``CUT_SIGMAS`` sigma, as a drawing function."""

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
    """(clusters, cluster sigma, distance of the cluster centres from the flock centre).

    Each cluster holds about N / k sheep, so its sigma is the compact sigma over sqrt(k)
    (same density). The clusters stand on a ring of ``split_ring`` separation distances, so
    the farthest sheep lie beyond the distance at which Strombom collects.
    """
    k = 2 if n_sheep < 12 else 3
    sigma = float(config["compact_spread"]) * flock_radius / np.sqrt(k)
    return k, sigma, float(config["split_ring"]) * float(config["separation_distance"])


def split_centres(config: dict[str, Any]) -> np.ndarray:
    """Cluster centres of the split layout, shape (k, 2).

    Angles are measured from the direction away from the goal and are symmetric about the
    drive axis: 0, +120 and -120 degrees for three clusters, +90 and -90 for two, so a
    mirrored drive gives the mirrored centres.
    """
    center = np.asarray(config["flock_center"], dtype=float)
    k, _, ring_radius = split_geometry(
        int(config["n_sheep"]), float(config["flock_radius"]), config
    )
    back = unit(center - np.asarray(config["goal_center"], dtype=float))
    angles = (0.0, 2.0 * np.pi / 3.0, -2.0 * np.pi / 3.0) if k == 3 else (np.pi / 2.0, -np.pi / 2.0)
    return np.array([center + ring_radius * rotate(back, angle) for angle in angles])


def _compact_sigma(config: dict[str, Any]) -> float:
    return float(config["compact_spread"]) * float(config["flock_radius"])


def _place_compact(config: dict[str, Any], rng: np.random.Generator) -> np.ndarray:
    center = np.asarray(config["flock_center"], dtype=float)
    draw = _truncated_gaussian(center, _compact_sigma(config), rng)
    return _draw_n(int(config["n_sheep"]), draw, config)


def _place_wide(config: dict[str, Any], rng: np.random.Generator) -> np.ndarray:
    center = np.asarray(config["flock_center"], dtype=float)
    sigma = float(config["wide_sigma"]) * float(config["separation_distance"])
    return _draw_n(int(config["n_sheep"]), _truncated_gaussian(center, sigma, rng), config)


def _place_split(config: dict[str, Any], rng: np.random.Generator) -> np.ndarray:
    """The clusters in turn, the remainder of N / k going to the first ones."""
    n = int(config["n_sheep"])
    k, sigma, _ = split_geometry(n, float(config["flock_radius"]), config)
    counts = np.full(k, n // k)
    counts[: n % k] += 1
    parts = [
        _draw_n(int(count), _truncated_gaussian(centre, sigma, rng), config)
        for centre, count in zip(split_centres(config), counts)
    ]
    return np.vstack(parts)


def _place_outlier_rich(config: dict[str, Any], rng: np.random.Generator) -> np.ndarray:
    """A compact core, then ``outlier_fraction`` of the sheep on a ring round it."""
    n = int(config["n_sheep"])
    center = np.asarray(config["flock_center"], dtype=float)
    n_out = round(float(config["outlier_fraction"]) * n)
    core = _draw_n(n - n_out, _truncated_gaussian(center, _compact_sigma(config), rng), config)
    reach = float(config["separation_distance"])
    near, far = float(config["outlier_near"]), float(config["outlier_far"])

    def outlier_ring(k: int) -> np.ndarray:
        angle = rng.uniform(0.0, 2.0 * np.pi, k)
        radius = reach * rng.uniform(near, far, k)
        return center + radius[:, None] * np.stack([np.cos(angle), np.sin(angle)], axis=1)

    return np.vstack([core, _draw_n(n_out, outlier_ring, config)])


PLACERS = {
    "compact": _place_compact,
    "wide": _place_wide,
    "split": _place_split,
    "outlier_rich": _place_outlier_rich,
}


def place_flock(config: dict[str, Any], rng: np.random.Generator) -> np.ndarray:
    """Sheep positions for the configured layout around the flock start centre."""
    layout = str(config["initial_layout"])
    if layout not in PLACERS:
        raise ValueError(f"Unknown initial_layout {layout!r}; expected one of {LAYOUTS}")
    return PLACERS[layout](config, rng)


def place_uniform_disc(
    centre: np.ndarray, radius: float, n: int, rng: np.random.Generator
) -> np.ndarray:
    """``n`` points uniform over the disc (radius sqrt(u) R, angle uniform), shape (n, 2)."""
    r = radius * np.sqrt(rng.random(n))
    angle = rng.uniform(0.0, 2.0 * np.pi, n)
    return centre + np.stack([r * np.cos(angle), r * np.sin(angle)], axis=1)


def layout_extent(config: dict[str, Any]) -> float:
    """Largest distance a sheep can start from the flock centre, exact for every layout."""
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
    """Half-angle of the cone, seen from the flock centre, that holds the goal disc.

    ``drive`` is the distance from the flock centre to the goal centre. A point outside
    this cone is outside the goal, whatever its distance from the flock.
    """
    if drive <= 0.0:
        return 0.0
    return float(np.arcsin(min(1.0, float(config["goal_radius"]) / drive)))


def _ring_span(config: dict[str, Any], drive: float) -> float:
    """Angle of the full circle that the ring uses: all of it but the goal's cone."""
    return 2.0 * np.pi - 2.0 * goal_half_angle(config, drive)


def _drive_of(config: dict[str, Any]) -> float:
    flock_center = np.asarray(config["flock_center"], dtype=float)
    return float(np.linalg.norm(np.asarray(config["goal_center"], dtype=float) - flock_center))


def _dog_arcs(config: dict[str, Any], drive: float) -> list[tuple[float, int]]:
    """(radius, dogs) of each start arc, ring or handler point, by ``dog_start``.

    arcs: half circles round the flock centre on the side away from the goal, so every dog
    starts equally far from the flock and none on the goal side. The first arc is
    ``dog_start_gap`` beyond ``layout_extent``, so every dog starts behind every sheep on
    every layout.

    ring: the same on full circles, goal side included, leaving out the cone that holds
    the goal. A full circle put a dog on the drive axis between flock and goal for every
    even D, and from N = 200 that dog started inside the goal.

    handler: every dog at one point straight behind the flock, at the radius of the first
    arc, as if released from a handler's post.

    A circle takes as many dogs as fit ``dog_start_spacing`` apart; the next one lies one
    spacing farther out.
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
    """Distance from the flock centre of the outermost dog at the start, for a goal ``drive``
    away (the ring leaves out the goal's cone, so how many dogs a circle holds depends on it)."""
    arcs = _dog_arcs(config, drive)
    if not arcs:  # no dogs: nothing stands outside the flock
        return 0.0
    return arcs[-1][0]


def field_size(
    config: dict[str, Any], layouts: tuple[str, ...], drive: float
) -> tuple[float, float, float]:
    """(width, height, flock start x) of a field that holds the whole task with clearance.

    The drive axis runs along x. Behind the flock start lies the larger of the layouts and
    the dog stations, then ``drive`` to the goal, then the goal radius. Sideways lies the
    larger of the layouts, the dog stations and the goal. ``field_clearance`` is kept free
    around all of it. The size depends on every layout of the protocol and on
    ``n_shepherds`` of ``config``, never on one cell's layout or D, so every cell of a
    protocol at one N and one method shares the field.
    """
    reach = max(layout_extent({**config, "initial_layout": name}) for name in layouts)
    dogs = max(dog_start_radius({**config, "initial_layout": name}, abs(drive)) for name in layouts)
    behind = max(reach, dogs)
    sideways = max(behind, float(config["goal_radius"]))
    clearance = float(config["field_clearance"])
    width = clearance + behind + abs(drive) + float(config["goal_radius"]) + clearance
    return width, 2.0 * (sideways + clearance), clearance + behind


def place_dogs(config: dict[str, Any]) -> np.ndarray:
    """Dogs at their start stations, by ``dog_start`` (no randomness).

    The ``count`` dogs of an arc sit at the centres of ``count`` equal sectors of the half
    circle behind the flock; of a ring, of its span (the circle less the goal's cone), so one
    dog starts straight behind the flock when the count is odd. The handler puts all dogs at
    the point straight behind.
    """
    flock_center = np.asarray(config["flock_center"], dtype=float)
    back = unit(flock_center - np.asarray(config["goal_center"], dtype=float))
    mode = str(config["dog_start"])
    drive = _drive_of(config)
    span = np.pi if mode == "arcs" else _ring_span(config, drive)
    positions = []
    for radius, count in _dog_arcs(config, drive):
        for j in range(count):
            angle = 0.0 if mode == "handler" else -span / 2.0 + span * (j + 0.5) / count
            positions.append(flock_center + radius * rotate(back, angle))
    return np.array(positions).reshape(-1, 2)
