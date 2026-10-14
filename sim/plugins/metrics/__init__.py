"""Per-tick metrics. Every trial records all of them; the key is the column name.

Order is the column order of the per-tick history and its Parquet files.
"""

from __future__ import annotations

from collections.abc import Callable

from core.simulation_state import SimulationState

from . import dogs, flock, goal

Metric = Callable[[SimulationState], float]

METRICS: dict[str, Metric] = {
    "cohesion": flock.cohesion,
    "gcm_goal": goal.gcm_goal,
    "time_to_goal": goal.time_to_goal,
    "shepherd_path": dogs.shepherd_path,
    "success_rate": goal.success_rate,
    "sheep_in_goal": goal.sheep_in_goal,
    "polarization": flock.polarization,
    "outlier_count": flock.outlier_count,
    "min_separation": flock.min_separation,
    "min_dog_separation": dogs.min_dog_separation,
    "fragmentation": flock.fragmentation,
    "mean_spread": flock.mean_spread,
    "extent": flock.extent,
    "perimeter": flock.perimeter,
    "hull_area": flock.hull_area,
    "flock_density": flock.flock_density,
    "aspect_ratio": flock.aspect_ratio,
    "i_dir": dogs.i_dir,
    "coverage": dogs.coverage,
}
