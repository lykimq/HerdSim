"""Generic per-tick metrics (TickView -> float), keyed by column name.

Every trial records these plus the task's own ``Scenario.metrics``.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping

from . import dogs, flock
from .view import TickView

Metric = Callable[[TickView], float]

METRICS: dict[str, Metric] = {
    "cohesion": flock.cohesion,
    "extent": flock.extent,
    "aspect_ratio": flock.aspect_ratio,
    "perimeter": flock.perimeter,
    "hull_area": flock.hull_area,
    "flock_density": flock.flock_density,
    "fragmentation": flock.fragmentation,
    "lost_sheep": flock.lost_sheep,
    "min_separation": flock.min_separation,
    "shepherd_path": dogs.shepherd_path,
    "min_dog_separation": dogs.min_dog_separation,
    "dog_overlap": dogs.dog_overlap,
    "dogs_stopped": dogs.dogs_stopped,
    "i_dir": dogs.i_dir,
    "coverage": dogs.coverage,
}


def record(view: TickView, task_metrics: Mapping[str, Metric]) -> dict[str, float]:
    """The task's metrics, then every generic metric, for one tick."""
    return {name: metric(view) for name, metric in {**task_metrics, **METRICS}.items()}
