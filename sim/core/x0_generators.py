"""X0 initial-layout generators for collective-state families (Cap I5)."""

from __future__ import annotations

import numpy as np

# Canonical X0 family names from the scaling protocol.
X0_FAMILIES = ("compact", "wide", "split", "outlier_rich")


def normalize_layout(layout: str) -> str:
    """Normalize layout name for comparison (strip + lower)."""
    return str(layout).strip().lower()


def _point_ok(
    pos: np.ndarray,
    *,
    world_width: float | None,
    world_height: float | None,
    goal_center: np.ndarray | None,
    goal_radius: float | None,
    margin: float = 1.0,
) -> bool:
    if world_width is not None and world_height is not None:
        if not (
            margin <= float(pos[0]) <= float(world_width) - margin
            and margin <= float(pos[1]) <= float(world_height) - margin
        ):
            return False
    if goal_center is not None and goal_radius is not None:
        if float(np.linalg.norm(pos - goal_center)) <= float(goal_radius):
            return False
    return True


def _draw_valid(
    draw_one,
    *,
    world_width: float | None,
    world_height: float | None,
    goal_center: np.ndarray | None,
    goal_radius: float | None,
    max_tries: int = 400,
) -> np.ndarray:
    """Redraw until the point is inside the field and outside the goal."""
    last = None
    for _ in range(max_tries):
        pos = np.asarray(draw_one(), dtype=float).reshape(2)
        last = pos
        if _point_ok(
            pos,
            world_width=world_width,
            world_height=world_height,
            goal_center=goal_center,
            goal_radius=goal_radius,
        ):
            return pos
    raise RuntimeError(
        f"Could not place a sheep inside the field and outside the goal. Last draw was {last}."
    )


def generate_initial_positions(
    n_sheep: int,
    layout: str,
    center: np.ndarray,
    rng: np.random.Generator,
    *,
    spread: float = 30.0,
    interaction_radius: float = 5.0,
    lost_threshold: float | None = None,
    world_width: float | None = None,
    world_height: float | None = None,
    goal_center: np.ndarray | None = None,
    goal_radius: float | None = None,
) -> np.ndarray:
    """Generate sheep positions for a named X0 family.

    Layouts
    -------
    compact:
        Single Gaussian cluster with sigma = 0.3 * spread.
    wide:
        Single Gaussian cluster with sigma = 2.0 * spread.
    split:
        Two or three separated subclusters at distance >= 2 * interaction_radius.
    outlier_rich:
        Core cluster (80%) plus outliers (20%) beyond the lost threshold.
    """
    if n_sheep <= 0:
        return np.zeros((0, 2), dtype=float)

    family = normalize_layout(layout)
    center = np.asarray(center, dtype=float).reshape(2)
    goal = None if goal_center is None else np.asarray(goal_center, dtype=float).reshape(2)
    bounds = dict(
        world_width=world_width,
        world_height=world_height,
        goal_center=goal,
        goal_radius=goal_radius,
    )
    if family == "compact":
        sigma = 0.3 * float(spread)
        pos = _gaussian_cluster(n_sheep, center, sigma, rng, **bounds)
    elif family == "wide":
        sigma = 2.0 * float(spread)
        pos = _gaussian_cluster(n_sheep, center, sigma, rng, **bounds)
    elif family == "split":
        pos = _split_positions(
            n_sheep,
            center,
            rng,
            separation=max(2.0 * float(interaction_radius), 0.8 * float(spread)),
            **bounds,
        )
    elif family == "outlier_rich":
        threshold = lost_threshold
        if threshold is None:
            # Match shared collect-style scale when r_a is unknown at init.
            threshold = 2.0 * (float(n_sheep) ** (2.0 / 3.0))
        pos = _outlier_rich_positions(
            n_sheep,
            center,
            rng,
            core_sigma=0.4 * float(spread),
            lost_threshold=float(threshold),
            **bounds,
        )
    else:
        raise ValueError(f"Unknown initial_layout '{layout}'. Expected one of {X0_FAMILIES}.")
    return pos


def _gaussian_cluster(
    n_sheep: int,
    center: np.ndarray,
    sigma: float,
    rng: np.random.Generator,
    **bounds,
) -> np.ndarray:
    rows = [
        _draw_valid(
            lambda: center + rng.normal(0.0, sigma, size=2),
            **bounds,
        )
        for _ in range(n_sheep)
    ]
    return np.vstack(rows)


def _split_positions(
    n_sheep: int,
    center: np.ndarray,
    rng: np.random.Generator,
    *,
    separation: float,
    **bounds,
) -> np.ndarray:
    n_clusters = 2 if n_sheep < 12 else 3
    # Place cluster centres on a circle around the flock centre.
    angles = np.linspace(0.0, 2.0 * np.pi, n_clusters, endpoint=False)
    radius = 0.5 * float(separation)
    centres = np.stack(
        [center[0] + radius * np.cos(angles), center[1] + radius * np.sin(angles)],
        axis=1,
    )
    # Assign sheep round-robin to clusters.
    counts = np.full(n_clusters, n_sheep // n_clusters, dtype=int)
    counts[: n_sheep % n_clusters] += 1
    parts = []
    sigma = max(0.15 * separation, 1.0)
    for i, count in enumerate(counts):
        if count <= 0:
            continue
        origin = centres[i]
        rows = [
            _draw_valid(
                lambda origin=origin, sigma=sigma: origin + rng.normal(0.0, sigma, size=2),
                **bounds,
            )
            for _ in range(int(count))
        ]
        parts.append(np.vstack(rows))
    return np.vstack(parts)


def _outlier_rich_positions(
    n_sheep: int,
    center: np.ndarray,
    rng: np.random.Generator,
    *,
    core_sigma: float,
    lost_threshold: float,
    **bounds,
) -> np.ndarray:
    n_out = max(1, int(round(0.2 * n_sheep))) if n_sheep >= 5 else 1
    n_out = min(n_out, n_sheep - 1) if n_sheep > 1 else 0
    n_core = n_sheep - n_out
    core = _gaussian_cluster(n_core, center, core_sigma, rng, **bounds)
    if n_out == 0:
        return core

    def _one_outlier() -> np.ndarray:
        angle = float(rng.uniform(0.0, 2.0 * np.pi))
        radius = float(lost_threshold) * float(rng.uniform(1.1, 1.6))
        return np.array([center[0] + radius * np.cos(angle), center[1] + radius * np.sin(angle)])

    outliers = np.vstack([_draw_valid(_one_outlier, **bounds) for _ in range(n_out)])
    return np.vstack([core, outliers])
