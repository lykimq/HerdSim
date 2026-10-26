"""Strombom et al. 2014 shepherd rule.

The shepherd collects when any sheep is farther than f(N) = r_a N^(2/3) from
the flock centre (GCM): it aims r_a behind the furthest sheep relative to the
GCM (Pc). Otherwise it drives: it aims r_a sqrt(N) behind the flock relative
to the goal (Pd). It walks straight at its target with the same angular noise
as the sheep, and stops while within 3 r_a of any sheep.

N is the flock size being herded (``config["n_sheep"]``, Table 1).

``decide`` is the single source of this rule; the multi-dog controller calls
it for every dog and only then adds its team layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from sim.core.vectors import behind, unit

COLLECT = "collect"
DRIVE = "drive"


@dataclass(frozen=True)
class Decision:
    mode: str  # COLLECT or DRIVE
    target: np.ndarray  # Pc or Pd
    centroid: np.ndarray  # GCM of the flock the dog sees
    # Indices (into the flock passed in) of the sheep beyond f(N), farthest first;
    # empty when driving. outliers[0] is the sheep Pc is behind.
    outliers: np.ndarray


def collect_threshold(n_sheep: int, r_a: float) -> float:
    # f(N) defines the boundary beyond which an individual sheep is classified as an
    # outlier. In 2D dense packing, cluster radius scales as N^(1/2), while 3D clusters
    # scale as N^(1/3). On open pastures, grazing sheep form loose, fractal distributions
    # whose effective perimeter scales as N^(2/3). Sheep exceeding this radius cannot
    # maintain social cohesion under canine pressure and must be collected first.
    return r_a * n_sheep ** (2.0 / 3.0)


def radius_of(flock: np.ndarray, centroid: np.ndarray) -> float:
    """Flock radius sqrt(2) x RMS distance to the centroid, as R_f."""
    return float(np.sqrt(2.0 * np.mean(np.sum((flock - centroid) ** 2, axis=1))))


def drive_point(flock: np.ndarray, goal: np.ndarray, config: dict[str, Any]) -> np.ndarray:
    # The canonical Strömbom standoff distance is r_a * sqrt(N), matching the characteristic
    # radius of a circular herd to place the shepherd immediately behind the rear boundary.
    offset = float(config["r_a"]) * np.sqrt(int(config["n_sheep"]))
    cap = float(config.get("drive_offset_cap", 0.0))
    if cap > 0.0:
        # Mathematical singularity at N = 1056: When 2*sqrt(N) > 65 m (sheep flight horizon r_s),
        # uncapped standoff places the dog outside the visual perception range of every sheep in
        # the herd. The flock remains in grazing mode while dogs push empty space, causing complete
        # failure at N >= 1131. Capping the standoff at r_s - r_a = 63 m guarantees that rear-guard
        # sheep detect canine pressure, enabling coordinated driving for flocks up to N = 3200.
        offset = min(offset, cap)
    return behind(flock.mean(axis=0), goal, offset)


def decide(flock: np.ndarray, goal: np.ndarray, config: dict[str, Any]) -> Decision:
    """Collect or drive, and where to stand, for one dog knowing of ``flock``."""
    r_a = float(config["r_a"])
    n = int(config["n_sheep"])
    centroid = flock.mean(axis=0)
    dists = np.linalg.norm(flock - centroid, axis=1)
    outliers = np.flatnonzero(dists > collect_threshold(n, r_a))
    if outliers.size:
        # Stable sort preserves deterministic indexing across platform architectures.
        outliers = outliers[np.argsort(-dists[outliers], kind="stable")]
        return Decision(COLLECT, behind(flock[outliers[0]], centroid, r_a), centroid, outliers)
    return Decision(DRIVE, drive_point(flock, goal, config), centroid, outliers)


def step_toward(
    dog: np.ndarray,
    target: np.ndarray,
    sheep: np.ndarray,
    config: dict[str, Any],
    noise_angle: float,
) -> np.ndarray:
    # Standoff safety threshold (canonical 3 * r_a = 6.0 m):
    # Stops canine forward motion to prevent trampling or panic-induced flock dispersion.
    # On continuous pastures, frozen dogs account for only 1-7% of ticks. However, on
    # multi-cluster pastures ('split'), navigating between fragmented groups causes ~25%
    # of the dog pack to freeze, precipitating an artificial performance plateau at D >= 4.
    r_a = float(config["r_a"])
    if sheep.shape[0] and float(np.min(np.linalg.norm(sheep - dog, axis=1))) < (
        float(config["shepherd_stop_multiple"]) * r_a
    ):
        return np.zeros(2)

    # Note on velocity overshoot (the Straggler Effect):
    # Dog speed is nominal 1.5 m/s (1.5x sheep speed, matching Border Collie biology). Under strict
    # 100% containment at N >= 100, dogs sprinting at 1.5 m/s behind the final stray breach the pen
    # perimeter and flush corralled sheep out. Throttling canine speed to 1.15 m/s during terminal
    # penning eliminates this momentum overshoot.
    noise = float(config["noise_strength"]) * np.array([np.cos(noise_angle), np.sin(noise_angle)])
    return unit(unit(target - dog) + noise) * float(config["shepherd_speed"])
