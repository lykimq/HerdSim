"""Registers the built-in scenarios (task definitions)."""

from __future__ import annotations

from core.registry import Registry

from .base import BaseScenario

scenario_registry: Registry[BaseScenario] = Registry("scenario")


def _auto_register() -> None:
    from .collect_hold_gate import CollectHoldGateScenario
    from .drive_to_goal import DriveToGoalScenario

    scenario_registry.register("drive_to_goal", DriveToGoalScenario)
    scenario_registry.register("collect_hold_gate", CollectHoldGateScenario)


_auto_register()
