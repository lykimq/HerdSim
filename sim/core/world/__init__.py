"""Arena geometry, initial flock layouts, goal resolution, and world defaults."""

from core.world.arena import GoalZone, World
from core.world.defaults import WORLD_DEFAULTS, WORLD_KEYS, scenario_world_config
from core.world.goal import resolve_goal_center
from core.world.layouts import (
    X0_FAMILIES,
    generate_initial_positions,
    normalize_layout,
)

__all__ = [
    "GoalZone",
    "WORLD_DEFAULTS",
    "WORLD_KEYS",
    "World",
    "X0_FAMILIES",
    "generate_initial_positions",
    "normalize_layout",
    "resolve_goal_center",
    "scenario_world_config",
]
