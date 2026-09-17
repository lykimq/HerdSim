"""X0 initial-layout generators for collective-state families (Cap I5)."""

from __future__ import annotations

import numpy as np

# Canonical X0 family names from the budget protocol.
X0_FAMILIES = ("compact", "wide", "split", "outlier_rich")

# Legacy factor value used in older configs.
_LAYOUT_ALIASES = {
    "cluster": "compact",
}


def normalize_layout(layout: str) -> str:
    """Map legacy aliases to canonical X0 family names."""
    key = str(layout).strip().lower()
    return _LAYOUT_ALIASES.get(key, key)


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
    if family == "compact":
        sigma = 0.3 * float(spread)
        pos = center + rng.normal(0.0, sigma, size=(n_sheep, 2))
    elif family == "wide":
        sigma = 2.0 * float(spread)
        pos = center + rng.normal(0.0, sigma, size=(n_sheep, 2))
    elif family == "split":
        pos = _split_positions(
            n_sheep,
            center,
            rng,
            separation=max(2.0 * float(interaction_radius), 0.8 * float(spread)),
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
        )
    else:
        raise ValueError(
            f"Unknown initial_layout '{layout}'. Expected one of {X0_FAMILIES} "
            f"(alias: cluster -> compact)."
        )

    if world_width is not None and world_height is not None:
        pos[:, 0] = np.clip(pos[:, 0], 1.0, float(world_width) - 1.0)
        pos[:, 1] = np.clip(pos[:, 1], 1.0, float(world_height) - 1.0)
    return pos


def _split_positions(
    n_sheep: int,
    center: np.ndarray,
    rng: np.random.Generator,
    *,
    separation: float,
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
        parts.append(centres[i] + rng.normal(0.0, sigma, size=(int(count), 2)))
    return np.vstack(parts)


def _outlier_rich_positions(
    n_sheep: int,
    center: np.ndarray,
    rng: np.random.Generator,
    *,
    core_sigma: float,
    lost_threshold: float,
) -> np.ndarray:
    n_out = max(1, int(round(0.2 * n_sheep))) if n_sheep >= 5 else 1
    n_out = min(n_out, n_sheep - 1) if n_sheep > 1 else 0
    n_core = n_sheep - n_out
    core = center + rng.normal(0.0, core_sigma, size=(n_core, 2))
    if n_out == 0:
        return core
    # Place outliers beyond the lost threshold on random bearings.
    angles = rng.uniform(0.0, 2.0 * np.pi, size=n_out)
    radii = lost_threshold * rng.uniform(1.1, 1.6, size=n_out)
    outliers = np.stack(
        [center[0] + radii * np.cos(angles), center[1] + radii * np.sin(angles)],
        axis=1,
    )
    return np.vstack([core, outliers])
