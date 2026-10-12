"""Auto-discovers and registers metric plugins from the plugins.metrics package."""

from __future__ import annotations

from typing import Any

from .base import BaseMetric


class MetricRegistry:
    """Central registry for algorithm-agnostic metrics."""

    def __init__(self):
        self._metric_classes: dict[str, type[BaseMetric]] = {}

    def register(self, metric_cls: type[BaseMetric]) -> None:
        instance = metric_cls()
        self._metric_classes[instance.id] = metric_cls

    def get(self, metric_id: str) -> BaseMetric:
        if metric_id not in self._metric_classes:
            available = list(self._metric_classes.keys())
            raise KeyError(f"Unknown metric '{metric_id}'. Available: {available}")
        return self._metric_classes[metric_id]()

    def get_all(self) -> list[BaseMetric]:
        """Return fresh metric instances for a simulation session."""
        return [cls() for cls in self._metric_classes.values()]

    def list_all(self) -> list[dict[str, Any]]:
        return [
            {
                "id": m.id,
                "name": m.name,
                "description": m.description,
                "unit": m.unit,
            }
            for m in self.get_all()
        ]


metric_registry = MetricRegistry()


def _auto_register():
    from .aspect_ratio import AspectRatioMetric
    from .cohesion import CohesionMetric
    from .extent import ExtentMetric
    from .flock_density import FlockDensityMetric
    from .fragmentation import FragmentationMetric
    from .gcm_goal import GcmGoalMetric
    from .hull_area import HullAreaMetric
    from .mean_spread import MeanSpreadMetric
    from .min_separation import MinSeparationMetric
    from .outlier_count import OutlierCountMetric
    from .perimeter import PerimeterMetric
    from .polarization import PolarizationMetric
    from .sheep_in_goal import SheepInGoalMetric
    from .shepherd_coverage import ShepherdCoverageMetric
    from .shepherd_interference import ShepherdInterferenceMetric
    from .shepherd_path import ShepherdPathMetric
    from .success_rate import SuccessRateMetric
    from .time_to_goal import TimeToGoalMetric

    for cls in [
        CohesionMetric,
        GcmGoalMetric,
        TimeToGoalMetric,
        ShepherdPathMetric,
        SuccessRateMetric,
        SheepInGoalMetric,
        PolarizationMetric,
        OutlierCountMetric,
        MinSeparationMetric,
        FragmentationMetric,
        MeanSpreadMetric,
        ExtentMetric,
        PerimeterMetric,
        HullAreaMetric,
        FlockDensityMetric,
        AspectRatioMetric,
        ShepherdInterferenceMetric,
        ShepherdCoverageMetric,
    ]:
        metric_registry.register(cls)


_auto_register()
