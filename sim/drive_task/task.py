"""Drive task: herd the flock into a circular goal.

Success in the study: all sheep in the goal (or share ``success_fraction``); Strombom's GCM
rule is recorded every tick as ``gcm_in_goal``. The check against Strombom et al. (2014) starts
from two square boxes (layout ``boxes``) and ends on that GCM rule (``success_rule``).
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from typing import Any

import numpy as np
import pandas as pd

from sim.state import SimulationState

from .goal import (
    CENTROID,
    SHEEP_SHARE,
    SUCCESS_RULES,
    arrival_columns,
    dogs_goal_side,
    gcm_goal,
    gcm_in_goal,
    sheep_in_goal,
)
from .layouts import (
    BOX_LAYOUT,
    DOG_STARTS,
    LAYOUTS,
    field_size,
    layout_extent,
    place_boxes,
    place_dogs,
    place_flock,
)

TASK = "drive_to_goal"

# The task's per-tick metrics, recorded ahead of the generic ones.
METRICS = {
    "gcm_goal": gcm_goal,
    "gcm_in_goal": gcm_in_goal,
    "sheep_in_goal": sheep_in_goal,
    "dogs_goal_side": dogs_goal_side,
}

# Setup keys this task reads from the run config (agent counts and the layout name are set
# by build_config itself): the world and goal for every start, then the keys of the study
# layouts, which are sized from R_f, or of the box start.
WORLD_KEYS = (
    "world_width",
    "world_height",
    "goal_center",
    "goal_radius",
    "success_fraction",
    "success_rule",
)
STUDY_KEYS = (
    "flock_center",
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
)
BOX_KEYS = ("sheep_box", "dog_box")


def required_keys(layout: str) -> tuple[str, ...]:
    """The setup keys a run config with start ``layout`` needs."""
    if layout == BOX_LAYOUT:
        return WORLD_KEYS + BOX_KEYS
    if layout in LAYOUTS:
        return WORLD_KEYS + STUDY_KEYS
    raise ValueError(f"initial_layout {layout!r} not in {LAYOUTS + (BOX_LAYOUT,)}")


def check(config: dict[str, Any]) -> None:
    """Task settings of a built run config."""
    if config["success_rule"] not in SUCCESS_RULES:
        raise ValueError(f"success_rule {config['success_rule']!r} not in {SUCCESS_RULES}")
    if config["initial_layout"] != BOX_LAYOUT and config["dog_start"] not in DOG_STARTS:
        raise ValueError(f"dog_start {config['dog_start']!r} not in {DOG_STARTS}")


def check_settings(s: Mapping[str, Any]) -> None:
    """Task settings of a protocol, before any setup is built from them."""
    if not 0.0 < float(s["success_fraction"]) <= 1.0:
        raise ValueError("success_fraction must be in (0, 1]")
    if float(s["dog_start_spacing"]) <= 0.0:
        raise ValueError("dog_start_spacing must be positive")
    if float(s["drive_distance_multiple"]) == 0.0:
        raise ValueError("drive_distance_multiple must not be 0 (its sign is the drive direction)")


def _typed_setup(s: Mapping[str, Any], flock_radius: float, n_sheep: int) -> dict[str, Any]:
    """The setup keys that are plain copies or multiples of the settings."""
    return {
        "goal_radius": float(s["goal_radius_multiple"]) * flock_radius,
        "success_fraction": float(s["success_fraction"]),
        "success_rule": SHEEP_SHARE,
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
    }


def build_setup(
    settings: Mapping[str, Any],
    *,
    flock_radius: float,
    n_sheep: int,
    layouts: tuple[str, ...],
    max_dogs: int,
) -> dict[str, Any]:
    """Setup for one N: drive clears every layout; field shared across layouts and max D."""
    check_settings(settings)
    setup = _typed_setup(settings, flock_radius, n_sheep)
    multiple = float(settings["drive_distance_multiple"])
    sizing = {**setup, "n_sheep": n_sheep, "n_shepherds": max_dogs}
    reach = max(layout_extent({**sizing, "initial_layout": name}) for name in layouts)
    length = max(
        abs(multiple) * flock_radius,
        float(settings["drive_distance_min"]),
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


def box_setup(
    sheep_box: tuple[float, float], dog_box: tuple[float, float], goal_radius: float
) -> dict[str, Any]:
    """Setup of a box start: sheep and dogs start in their square boxes ((low, high) on both
    axes) of an open field, the goal is at the origin, and the trial is over when the flock
    centre is within ``goal_radius`` of it."""
    side = max(float(sheep_box[1]), float(dog_box[1]))  # the field only records the extent
    return {
        "world_width": side,
        "world_height": side,
        "goal_center": [0.0, 0.0],
        "goal_radius": goal_radius,
        "success_fraction": 1.0,  # unused: the centroid rule counts no sheep
        "success_rule": CENTROID,
        "sheep_box": list(sheep_box),
        "dog_box": list(dog_box),
    }


def drive_length(setup: Mapping[str, Any]) -> float:
    """The drive: the distance from the flock's start centre to the goal centre."""
    return abs(float(setup["goal_center"][0]) - float(setup["flock_center"][0]))


def initial_positions(
    config: dict[str, Any], rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray]:
    """Flock at its start centre and outside the goal; dogs behind it, away from the goal.
    The box start draws the sheep and then the dogs from ``rng``."""
    if config["initial_layout"] == BOX_LAYOUT:
        return place_boxes(config, rng)
    return place_flock(config, rng), place_dogs(config)


def is_success(state: SimulationState) -> bool:
    """The goal's success rule holds this tick (share of sheep, or the flock centre)."""
    return state.world.goal.reached(state.sheep_positions)


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
