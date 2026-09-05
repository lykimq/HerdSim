"""Auto-discovers and registers metric plugins from the metrics/ package."""

from __future__ import annotations

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

    def list_all(self) -> list[dict]:
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
    from metrics.cohesion import CohesionMetric
    from metrics.min_separation import MinSeparationMetric
    from metrics.outlier_count import OutlierCountMetric
    from metrics.polarization import PolarizationMetric
    from metrics.sheep_in_goal import SheepInGoalMetric
    from metrics.shepherd_path import ShepherdPathMetric
    from metrics.success_rate import SuccessRateMetric
    from metrics.time_to_goal import TimeToGoalMetric

    for cls in [
        CohesionMetric,
        TimeToGoalMetric,
        ShepherdPathMetric,
        SuccessRateMetric,
        SheepInGoalMetric,
        PolarizationMetric,
        OutlierCountMetric,
        MinSeparationMetric,
    ]:
        metric_registry.register(cls)


_auto_register()
