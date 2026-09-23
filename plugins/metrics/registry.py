"""Auto-discovers and registers metric plugins from the plugins.metrics package."""

from __future__ import annotations

from typing import Any

from core.base_metric import BaseMetric


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
    from plugins.metrics.aspect_ratio import AspectRatioMetric
    from plugins.metrics.cohesion import CohesionMetric
    from plugins.metrics.extent import ExtentMetric
    from plugins.metrics.flock_density import FlockDensityMetric
    from plugins.metrics.fragmentation import FragmentationMetric
    from plugins.metrics.gcm_goal import GcmGoalMetric
    from plugins.metrics.hull_area import HullAreaMetric
    from plugins.metrics.mean_spread import MeanSpreadMetric
    from plugins.metrics.min_separation import MinSeparationMetric
    from plugins.metrics.outlier_count import OutlierCountMetric
    from plugins.metrics.perimeter import PerimeterMetric
    from plugins.metrics.polarization import PolarizationMetric
    from plugins.metrics.sheep_in_goal import SheepInGoalMetric
    from plugins.metrics.shepherd_coverage import ShepherdCoverageMetric
    from plugins.metrics.shepherd_interference import ShepherdInterferenceMetric
    from plugins.metrics.shepherd_path import ShepherdPathMetric
    from plugins.metrics.success_rate import SuccessRateMetric
    from plugins.metrics.time_to_goal import TimeToGoalMetric

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
