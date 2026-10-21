"""Per-tick metrics that apply to every task. Every trial records all of them, plus
its task's own metrics (``Scenario.metrics``); the key is the column name.

A metric is a function of a TickView, which carries the state and the run
config, returning one float. A new metric is one function and one entry here
(or in the task's table when it needs the task's geometry); the engine, the
trial row and the tables pick it up by name.
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
