"""Drive task: herd sheep into a circular goal zone.

Success requires that at least `success_fraction` of the flock stays continuously
inside the goal zone for `hold_ticks` ticks.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from typing import Any

import numpy as np
import pandas as pd

from sim.core.simulation_state import SimulationState
from sim.core.world import layouts
from sim.core.world.layouts import DOG_STARTS, field_size, layout_extent, place_dogs, place_flock

from .goal import arrival_columns
from .team_settings import KEYS as TEAM_KEYS
from .team_settings import check as check_team
from .team_settings import setup as team_setup

# The start layouts of this task: the flock shapes sized by R_f and the separation distance.
LAYOUTS = layouts.LAYOUTS

# Setup keys this task reads from the run config (agent counts and the layout
# name are set by build_config itself).
REQUIRED_KEYS = (
    "world_width",
    "world_height",
    "flock_center",
    "goal_center",
    "goal_radius",
    "success_fraction",
    "flock_radius",
    "compact_spread",
    "wide_sigma",
    "split_ring",
    "outlier_fraction",
    "outlier_near",
    "outlier_far",
    "separation_distance",
    "dog_start",
    "dog_start_gap",
    "dog_start_spacing",
    # Read only at setup time (field_size), but part of the setup record.
    "field_clearance",
    "hold_ticks",
    *TEAM_KEYS,
)


def check(config: dict[str, Any]) -> None:
    """Task settings of a built run config."""
    if config["dog_start"] not in DOG_STARTS:
        raise ValueError(f"dog_start {config['dog_start']!r} not in {DOG_STARTS}")
    if config["initial_layout"] not in LAYOUTS:
        raise ValueError(f"initial_layout {config['initial_layout']!r} not in {LAYOUTS}")
    if int(config["hold_ticks"]) < 0:
        raise ValueError("hold_ticks must not be negative")
    check_team(config)


def drive_length(setup: Mapping[str, Any]) -> float:
    """The drive: the distance from the flock's start centre to the goal centre."""
    return abs(float(setup["goal_center"][0]) - float(setup["flock_center"][0]))


def row_columns(config: dict[str, Any], history: pd.DataFrame) -> dict[str, Any]:
    """The task's columns of a trial row: the geometry it ran in and where it ended."""
    final = history.iloc[-1]
    return {
        **arrival_columns(config, history),
        "goal_radius": float(config["goal_radius"]),
        "success_fraction": float(config["success_fraction"]),
        "drive_distance": drive_length(config),
        "world_width": float(config["world_width"]),
        "world_height": float(config["world_height"]),
        "final_gcm_goal": float(final["gcm_goal"]),
        "final_sheep_in_goal": float(final["sheep_in_goal"]),
    }


def initial_positions(
    config: dict[str, Any], rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray]:
    """Flock at its start centre and outside the goal; dogs behind it, away from the goal."""
    return place_flock(config, rng), place_dogs(config)


def is_success(state: SimulationState) -> bool:
    """Return True if the goal condition has held continuously for hold_ticks."""
    goal = state.world.goal
    if not goal.reached(state.sheep_positions):
        state.metadata.pop("reached_since", None)
        return False
    since = state.metadata.setdefault("reached_since", state.tick)
    return state.tick - since >= goal.hold_ticks


def build_setup(
    settings: Mapping[str, Any],
    *,
    flock_radius: float,
    n_sheep: int,
    layouts: tuple[str, ...],
    max_dogs: int,
) -> dict[str, Any]:
    """Compute task geometry and field dimensions for a given flock size and method.

    Computes drive distance and field boundaries to ensure:
    - Drive distance scales with flock radius R_f while enforcing non-overlap
      with the widest initial layout extent.
    - Field dimensions accommodate all specified layouts, maximum dog count,
      and clearance buffers around the goal and starting positions.
    """
    s = settings
    if not 0.0 < float(s["success_fraction"]) <= 1.0:
        raise ValueError("success_fraction must be in (0, 1]")
    if float(s["dog_start_spacing"]) <= 0.0:
        raise ValueError("dog_start_spacing must be positive")
    multiple = float(s["drive_distance_multiple"])
    if multiple == 0.0:
        raise ValueError("drive_distance_multiple must not be 0 (its sign is the drive direction)")
    setup: dict[str, Any] = {
        "goal_radius": float(s["goal_radius_multiple"]) * flock_radius,
        "success_fraction": float(s["success_fraction"]),
        "flock_radius": flock_radius,
        "compact_spread": float(s["compact_spread"]),
        "wide_sigma": float(s["wide_sigma"]),
        "split_ring": float(s["split_ring"]),
        "outlier_fraction": float(s["outlier_fraction"]),
        "outlier_near": float(s["outlier_near"]),
        "outlier_far": float(s["outlier_far"]),
        "separation_distance": float(s["separation_scale"]) * n_sheep ** (2.0 / 3.0),
        "lost_radius": float(s["lost_radius_multiple"]) * flock_radius,
        "dog_start": str(s["dog_start"]),
        "dog_start_gap": float(s["dog_start_gap"]),
        "dog_start_spacing": float(s["dog_start_spacing"]),
        "field_clearance": float(s["field_clearance"]),
        **team_setup(s),
    }
    sizing = {**setup, "n_sheep": n_sheep, "n_shepherds": max_dogs}
    reach = max(layout_extent({**sizing, "initial_layout": name}) for name in layouts)
    length = max(
        abs(multiple) * flock_radius,
        float(s["drive_distance_min"]),
        reach + setup["goal_radius"] + flock_radius,
    )
    width, height, start_x = field_size(sizing, layouts, length)
    start = start_x if multiple > 0 else width - start_x
    goal = start + math.copysign(length, multiple)
    return {
        **setup,
        "world_width": width,
        "world_height": height,
        "flock_center": [start, height / 2.0],
        "goal_center": [goal, height / 2.0],
    }
