"""Auto-discovers and registers algorithm plugins from the algorithms/ package."""

from __future__ import annotations

from core.base_algorithm import BaseAlgorithm


class AlgorithmRegistry:
    """Central registry for herding algorithm plugins."""

    def __init__(self):
        self._algorithms: dict[str, BaseAlgorithm] = {}

    def register(self, algorithm: BaseAlgorithm) -> None:
        self._algorithms[algorithm.id] = algorithm

    def get(self, algorithm_id: str) -> BaseAlgorithm:
        if algorithm_id not in self._algorithms:
            available = list(self._algorithms.keys())
            raise KeyError(f"Unknown algorithm '{algorithm_id}'. Available: {available}")
        return self._algorithms[algorithm_id]

    def list_all(self) -> list[dict]:
        return [
            {"id": a.id, "name": a.name, "default_config": a.default_config}
            for a in self._algorithms.values()
        ]

    def names(self) -> list[str]:
        return list(self._algorithms.keys())


algorithm_registry = AlgorithmRegistry()


def _auto_register():
    from algorithms.flocking_dog.algorithm import FlockingDogAlgorithm
    from algorithms.heterogeneous.algorithm import HeterogeneousAlgorithm
    from algorithms.kubo.algorithm import KuboAlgorithm
    from algorithms.obstacle_aware.algorithm import ObstacleAwareAlgorithm
    from algorithms.strombom.algorithm import StrombomAlgorithm
    from algorithms.strombom_multi.algorithm import StrombomMultiAlgorithm
    from algorithms.strombom_noise.algorithm import StrombomNoiseAlgorithm
    from algorithms.v_formation.algorithm import VFormationAlgorithm

    for cls in [
        StrombomAlgorithm,
        KuboAlgorithm,
        FlockingDogAlgorithm,
        StrombomMultiAlgorithm,
        StrombomNoiseAlgorithm,
        VFormationAlgorithm,
        HeterogeneousAlgorithm,
        ObstacleAwareAlgorithm,
    ]:
        algorithm_registry.register(cls())


_auto_register()
