"""Start positions: flock layouts and the dog line.

Two lengths size the layouts. The compact flock (and the cluster size of the split
layout) uses the flock radius ``R_f``. The scattered layouts (wide, split ring,
outliers) use the separation distance, the distance from the flock centre beyond
which Strombom 2014 treats a sheep as separated (r_a N^(2/3), p.7). A scattered layout
sized by R_f never leaves the drive rule at N >= 100: measured, none of the split or
outlier starts had a sheep beyond that distance.

The separation distance is Strombom's collect threshold. It has no meaning for Kubo
sheep, which have no collect rule and whose only length scale is the attraction
range 20 (Kubo 2022 Table 1): for them a scattered start is just a sparse flock in
Strombom units. The protocols therefore restrict Kubo to the compact layout.

Every Gaussian draw is cut at ``CUT_SIGMAS`` sigma, so ``layout_extent`` is an exact
bound on where a sheep can start and the field, the drive and the dog arcs are
sized from it. The outlier ring is bounded by construction.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import numpy as np

from sim.core.vectors import rotate, unit

LAYOUTS = ("compact", "wide", "split", "outlier_rich")

# Agents start at least this far inside the field edge.
EDGE_MARGIN = 1.0
# Radius of the Gaussian layouts in sigmas (HerdSim choice). An uncut 2-D Gaussian
# has e^(-4.5) = 1.1% of its mass beyond 3 sigma, so the cut barely changes the
# shape but gives every layout a hard edge.
CUT_SIGMAS = 3.0

# Draws n candidate points at once, shape (n, 2).
Draw = Callable[[int], np.ndarray]


def _draw_n(n: int, draw: Draw, config: dict[str, Any]) -> np.ndarray:
    """``n`` points, all inside the field (with margin) and outside the goal.

    The task sizes the field and the drive from ``layout_extent`` so that every
    possible start fits; a point outside is a sizing bug, so it raises instead
    of being redrawn (a redraw would quietly change the layout's shape).
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
    """Gaussian cut at ``CUT_SIGMAS`` sigma: hard cluster edges, exact split gaps and extent."""

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
    """(clusters, cluster sigma, distance of cluster centres from the flock centre).

    Each cluster holds about N / k sheep, so its sigma is the compact sigma
    scaled by 1 / sqrt(k) (same density). The clusters stand on a ring of
    ``split_ring`` separation distances around the flock centre, so the
    farthest sheep lie beyond the distance at which Strombom collects.
    """
    k = 2 if n_sheep < 12 else 3
    sigma = float(config["compact_spread"]) * flock_radius / np.sqrt(k)
    return k, sigma, float(config["split_ring"]) * float(config["separation_distance"])


def split_centres(config: dict[str, Any]) -> np.ndarray:
    """Cluster centres of the split layout, shape (k, 2).

    Angles are measured from the direction away from the goal and are symmetric
    about the drive axis: 0, +120 and -120 degrees for three clusters, +90 and
    -90 for two. A mirrored drive therefore gives the mirrored set of centres.
    """
    center = np.asarray(config["flock_center"], dtype=float)
    k, _, ring_radius = split_geometry(
        int(config["n_sheep"]), float(config["flock_radius"]), config
    )
    back = unit(center - np.asarray(config["goal_center"], dtype=float))
    angles = (0.0, 2.0 * np.pi / 3.0, -2.0 * np.pi / 3.0) if k == 3 else (np.pi / 2.0, -np.pi / 2.0)
    return np.array([center + ring_radius * rotate(back, angle) for angle in angles])


def place_flock(config: dict[str, Any], rng: np.random.Generator) -> np.ndarray:
    """Sheep positions for the configured layout around the flock start centre."""
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
        n_out = int(round(float(config["outlier_fraction"]) * n))
        core = _draw_n(n - n_out, _truncated_gaussian(center, compact_sigma, rng), config)
        reach = float(config["separation_distance"])
        near, far = float(config["outlier_near"]), float(config["outlier_far"])

        def outlier_ring(k: int) -> np.ndarray:
            angle = rng.uniform(0.0, 2.0 * np.pi, k)
            radius = reach * rng.uniform(near, far, k)
            return center + radius[:, None] * np.stack([np.cos(angle), np.sin(angle)], axis=1)

        return np.vstack([core, _draw_n(n_out, outlier_ring, config)])
    raise ValueError(f"Unknown initial_layout {layout!r}; expected one of {LAYOUTS}")


def layout_extent(config: dict[str, Any]) -> float:
    """Largest distance a sheep can start from the flock centre.

    Exact: every Gaussian is cut at ``CUT_SIGMAS`` sigma and the outlier ring ends
    at ``outlier_far`` separation distances.
    """
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

    ``drive`` is the distance from the flock centre to the goal centre. A point outside this
    cone is outside the goal, whatever its distance from the flock.
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

    ``arcs`` (the base): dogs stand on half circles around the flock centre, on the side
    away from the goal, so all of them start equally far from the flock and none starts on
    the goal side. The first arc is ``dog_start_gap`` beyond ``layout_extent``, the farthest
    any sheep can start, so every dog starts behind every sheep on every layout. On the
    scattered layouts that puts the dogs farther than Strombom's r_s from most of the
    sheep and they walk in first; that approach time is deterministic (the start is fixed
    by the layout and D) and is part of the finish time.

    ``ring``: the same, but on circles round the flock, goal side included, leaving out the
    cone of half-angle ``goal_half_angle`` that holds the goal. A full circle put a dog on
    the drive axis between flock and goal for every even D, and from N = 200 that dog
    started inside the goal (the ring radius exceeds the distance to the goal's near edge).

    ``handler``: every dog starts at one point, straight behind the flock on the drive axis
    at the radius of the first arc, as if released from a handler's post. The team rule then
    sends each dog to its own target.

    The dogs of an arc or ring are spread evenly over it (``place_dogs``), so each added dog
    starts at its own station, not next to the others. A circle takes as many dogs as fit at
    least ``dog_start_spacing`` apart, and the next one lies one spacing further out.
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

    The drive axis runs along x. Behind the flock start lies the larger of the
    flock layouts and the dogs' arcs, then ``drive`` to the goal, then the goal radius.
    Sideways lies the larger of the layouts, the dogs' arcs and the goal.
    ``field_clearance`` is kept free around all of it. The field only places the start; there
    is no boundary. The size depends on the
    layouts and on ``n_shepherds`` of ``config``, never on one cell's layout
    or D, so every cell of a protocol at one N and one method shares the field
    (one method, because R_f is calibrated per method and sizes everything here).
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

    arcs: the ``count`` dogs of an arc sit at the centres of ``count`` equal sectors of the
    half circle behind the flock, angles -90 + 180 (j + 0.5) / count degrees from straight
    behind, so neighbours are pi r / count >= ``dog_start_spacing`` apart along it.
    ring: the same sector centres over the ring's span (the circle less the goal's cone),
    angles -span / 2 + span (j + 0.5) / count from straight behind, so one dog starts straight
    behind the flock when the count is odd and none starts in the goal's cone.
    handler: all dogs at the point straight behind.
    """
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
