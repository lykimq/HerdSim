"""World / layout defaults for experiment config composition.

Algorithm config modules declare only agent counts plus algorithm-specific
behavior parameters. World / layout keys are owned by scenarios; these defaults
are the fallback when a scenario omits a key.

Composition order: see ``core.config.experiment.resolve_experiment_config``.
"""

from __future__ import annotations

from typing import Any

# World keys a scenario may own (drive_to_goal, collect_hold_gate).
WORLD_KEYS = (
    "world_width",
    "world_height",
    "goal_center",
    "goal_radius",
    "max_ticks",
    "initial_spread",
    "shepherd_start_offset",
    "success_fraction",
    # Scenario may widen Strombom-style f(N); algorithms declare the default.
    "collect_threshold_scale",
    # Experimental flock-connectivity radius for fragmentation metric.
    "measurement_radius",
)

# Fallback layout when scenario / overrides omit a world key.
WORLD_DEFAULTS: dict[str, Any] = {
    "world_width": 150.0,
    "world_height": 150.0,
    "goal_center": [15.0, 15.0],
    "goal_radius": 15.0,
    "max_ticks": 3000,
    # Experimental (not algorithm-specific) radius for fragmentation.
    "measurement_radius": 5.0,
}


def scenario_world_config(scenario_defaults: dict[str, Any]) -> dict[str, Any]:
    """World / layout keys from the selected scenario (goal, arena, etc.)."""
    return {k: v for k, v in scenario_defaults.items() if k in WORLD_KEYS}
