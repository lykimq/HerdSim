"""Strombom et al. 2014 shepherd rule: collect (Pc) or drive (Pd).

Collect when any sheep is beyond f(N) = r_a N^(2/3); else drive. ``decide`` is the
single source; the multi-dog layer builds on it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from sim.vectors import FLOCK_RADIUS_FACTOR, angle_vectors, behind, unit

COLLECT = "collect"
DRIVE = "drive"


@dataclass(frozen=True)
class Decision:
    mode: str  # COLLECT or DRIVE
    target: np.ndarray  # Pc or Pd
    centroid: np.ndarray  # centre of the flock the dog knows of
    # Indices (into the flock passed in) of the sheep beyond f(N), farthest first; empty
    # when driving. outliers[0] is the sheep Pc stands behind.
    outliers: np.ndarray


def collect_threshold(n_sheep: int, r_a: float) -> float:
    """f(N) = r_a N^(2/3): a sheep farther than this from the centre has to be collected."""
    return r_a * n_sheep ** (2.0 / 3.0)


def radius_of(flock: np.ndarray, centroid: np.ndarray) -> float:
    """Flock radius sqrt(2) x RMS distance to the centroid, the same measure as R_f."""
    return float(FLOCK_RADIUS_FACTOR * np.sqrt(np.mean(np.sum((flock - centroid) ** 2, axis=1))))


def drive_point(flock: np.ndarray, goal: np.ndarray, config: dict[str, Any]) -> np.ndarray:
    """Pd: r_a sqrt(N) behind the flock centre, seen from the goal."""
    offset = float(config["r_a"]) * np.sqrt(int(config["n_sheep"]))
    return behind(flock.mean(axis=0), goal, offset)


def decide(flock: np.ndarray, goal: np.ndarray, config: dict[str, Any]) -> Decision:
    """Collect or drive, and where to stand, for one dog knowing of ``flock``."""
    r_a = float(config["r_a"])
    n = int(config["n_sheep"])
    centroid = flock.mean(axis=0)
    dists = np.linalg.norm(flock - centroid, axis=1)
    outliers = np.flatnonzero(dists > collect_threshold(n, r_a))
    if outliers.size:
        # Stable, so two sheep at the same distance keep their index order on every machine.
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
    """Velocity of one dog toward ``target`` with the paper's noise, or zero within the stop
    distance (``shepherd_stop_multiple`` x r_a) of any sheep."""
    r_a = float(config["r_a"])
    stop_distance = float(config["shepherd_stop_multiple"]) * r_a
    if sheep.shape[0] and float(np.min(np.linalg.norm(sheep - dog, axis=1))) < stop_distance:
        return np.zeros(2)
    noise = float(config["noise_strength"]) * angle_vectors(np.asarray(noise_angle))
    return unit(unit(target - dog) + noise) * float(config["shepherd_speed"])
