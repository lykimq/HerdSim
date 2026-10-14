"""Registers the built-in metrics; every trial records all of them per tick."""

from __future__ import annotations

from core.registry import Registry

from .base import BaseMetric

metric_registry: Registry[BaseMetric] = Registry("metric")


def _auto_register() -> None:
    from .aspect_ratio import AspectRatioMetric
    from .cohesion import CohesionMetric
    from .extent import ExtentMetric
    from .flock_density import FlockDensityMetric
    from .fragmentation import FragmentationMetric
    from .gcm_goal import GcmGoalMetric
    from .hull_area import HullAreaMetric
    from .mean_spread import MeanSpreadMetric
    from .min_dog_separation import MinDogSeparationMetric
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
        MinDogSeparationMetric,
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
        metric_registry.register(cls().id, cls)


_auto_register()
