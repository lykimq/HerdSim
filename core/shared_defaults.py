"""Shared config ownership for HerdSim experiments.

Algorithm config modules declare only agent counts plus algorithm-specific
behavior parameters. World / layout keys are owned by scenarios; these shared
defaults are the fallback when a scenario omits a key.

Composition order (see resolve_experiment_config):
  SHARED_WORLD_DEFAULTS -> algorithm.default_config -> scenario overlay
"""

from __future__ import annotations

from typing import Any

# Paper agent counts: declared per algorithm, overridable by scenario preset.
AGENT_KEYS = ("n_sheep", "n_shepherds")

# Keys owned by the selected scenario (paper/custom take these from scenario).
WORLD_KEYS = (
    "world_width",
    "world_height",
    "goal_center",
    "goal_radius",
    "max_ticks",
    "pen_center",
    "pen_radius",
    "obstacles",
    "initial_spread",
    "shepherd_start_offset",
    "success_fraction",
    "n_clusters",
    "gate_width",
    "gate_y",
    # Scenario may widen Strombom-style f(N); algorithms declare the default.
    "collect_threshold_scale",
)

# Fallback layout when scenario / overrides omit a world key.
SHARED_WORLD_DEFAULTS: dict[str, Any] = {
    "world_width": 150.0,
    "world_height": 150.0,
    "goal_center": [15.0, 15.0],
    "goal_radius": 15.0,
    "max_ticks": 3000,
}


def scenario_world_config(scenario_defaults: dict[str, Any]) -> dict[str, Any]:
    """World / layout keys from the selected scenario (goal, obstacles, etc.)."""
    return {k: v for k, v in scenario_defaults.items() if k in WORLD_KEYS}
