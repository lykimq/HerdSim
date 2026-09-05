"""Auto-discovers and registers scenario plugins from the scenarios/ package."""

from __future__ import annotations

from core.base_scenario import BaseScenario


class ScenarioRegistry:
    """Central registry for simulation scenarios."""

    def __init__(self):
        self._scenarios: dict[str, BaseScenario] = {}

    def register(self, scenario: BaseScenario) -> None:
        self._scenarios[scenario.id] = scenario

    def get(self, scenario_id: str) -> BaseScenario:
        if scenario_id not in self._scenarios:
            available = list(self._scenarios.keys())
            raise KeyError(f"Unknown scenario '{scenario_id}'. Available: {available}")
        return self._scenarios[scenario_id]

    def list_all(self) -> list[dict]:
        return [
            {
                "id": s.id,
                "name": s.name,
                "description": s.description,
                "default_config": s.default_config,
            }
            for s in self._scenarios.values()
        ]

    def names(self) -> list[str]:
        return list(self._scenarios.keys())


# Singleton registry — populated at import time
scenario_registry = ScenarioRegistry()


def _auto_register():
    """Import built-in scenarios to trigger registration."""
    from scenarios.containment import ContainmentScenario
    from scenarios.drive_to_goal import DriveToGoalScenario
    from scenarios.narrow_gate import NarrowGateScenario
    from scenarios.obstacle_course import ObstacleCourseScenario
    from scenarios.split_flock import SplitFlockScenario
    from scenarios.wide_field import WideFieldScenario

    for cls in [
        DriveToGoalScenario,
        ContainmentScenario,
        ObstacleCourseScenario,
        SplitFlockScenario,
        NarrowGateScenario,
        WideFieldScenario,
    ]:
        scenario_registry.register(cls())


_auto_register()
