"""Strömböm et al. 2014 shepherd decision heuristic and locomotion.

Evaluates flock dispersion against the outlier threshold f(N) = r_a * N^(2/3):
- Collect mode: Targets a standoff distance behind the furthest outlier relative to flock center.
- Drive mode: Targets a standoff distance behind flock center relative to the goal.
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
    target: np.ndarray  # 2D waypoint for shepherd positioning
    centroid: np.ndarray  # Mean position of the sensed flock
    # Indices of outliers exceeding threshold f(N), sorted by distance descending.
    outliers: np.ndarray


def collect_threshold(n_sheep: int, r_a: float) -> float:
    # Outlier threshold distance f(N) = r_a * N^(2/3).
    return r_a * n_sheep ** (2.0 / 3.0)


def radius_of(flock: np.ndarray, centroid: np.ndarray) -> float:
    """Calculate flock radius as sqrt(2) * RMS distance from centroid."""
    return float(np.sqrt(2.0 * np.mean(np.sum((flock - centroid) ** 2, axis=1))))


def drive_point(flock: np.ndarray, goal: np.ndarray, config: dict[str, Any]) -> np.ndarray:
    # Standoff distance r_a * sqrt(N) positions dogs behind the rear flock edge.
    offset = float(config["r_a"]) * np.sqrt(int(config["n_sheep"]))
    cap = float(config.get("drive_offset_cap", 0.0))
    if cap > 0.0:
        # Cap standoff distance so dogs stay within sheep reaction range at large N.
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
    """Compute dog velocity toward target with angular noise.

    Halts forward motion when within stop distance of any sheep.
    """
    r_a = float(config["r_a"])
    stop_distance = float(config["shepherd_stop_multiple"]) * r_a
    if sheep.shape[0] and float(np.min(np.linalg.norm(sheep - dog, axis=1))) < stop_distance:
        return np.zeros(2)

    noise = float(config["noise_strength"]) * np.array([np.cos(noise_angle), np.sin(noise_angle)])
    return unit(unit(target - dog) + noise) * float(config["shepherd_speed"])
