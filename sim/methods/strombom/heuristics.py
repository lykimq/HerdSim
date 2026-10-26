"""Strombom et al. 2014 shepherd rule.

The shepherd collects when any sheep is farther than f(N) = r_a N^(2/3) from the flock
centre: it aims r_a behind the farthest such sheep, seen from the centre (Pc). Otherwise it
drives: it aims r_a sqrt(N) behind the flock, seen from the goal (Pd). It walks straight at
its target with the same angular noise as the sheep, and stops while within 3 r_a of any
sheep. N is the flock size being herded (``config["n_sheep"]``).

``decide`` is the single source of this rule; the multi-dog controller calls it and only
then adds its team layer.
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
    centroid: np.ndarray  # centre of the flock the dog knows of
    # Indices (into the flock passed in) of the sheep beyond f(N), farthest first; empty
    # when driving. outliers[0] is the sheep Pc stands behind.
    outliers: np.ndarray


def collect_threshold(n_sheep: int, r_a: float) -> float:
    """f(N) = r_a N^(2/3): a sheep farther than this from the centre has to be collected."""
    return r_a * n_sheep ** (2.0 / 3.0)


def radius_of(flock: np.ndarray, centroid: np.ndarray) -> float:
    """Flock radius sqrt(2) x RMS distance to the centroid, the same measure as R_f."""
    return float(np.sqrt(2.0 * np.mean(np.sum((flock - centroid) ** 2, axis=1))))


def drive_point(flock: np.ndarray, goal: np.ndarray, config: dict[str, Any]) -> np.ndarray:
    """Pd: r_a sqrt(N) behind the flock centre, seen from the goal.

    The paper's offset passes the reaction distance r_s at N = (r_s / r_a)^2 = 1056, where
    the dog stands where no sheep feels it. ``drive_offset_cap`` (0 is off) caps it so the
    drive point stays within reach; it is a labelled variant, not the paper rule.
    """
    offset = float(config["r_a"]) * np.sqrt(int(config["n_sheep"]))
    cap = float(config.get("drive_offset_cap", 0.0))
    if cap > 0.0:
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
    noise = float(config["noise_strength"]) * np.array([np.cos(noise_angle), np.sin(noise_angle)])
    return unit(unit(target - dog) + noise) * float(config["shepherd_speed"])
