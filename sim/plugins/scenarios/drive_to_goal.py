"""Drive task: herd every sheep into a circular goal.

Success rule (``is_success``): every sheep is inside the goal disk. This is a
HerdSim choice and differs from both papers. Strombom 2014 ends the task when
the flock's centre of mass (GCM) is within a certain distance of the target
(p.7, distance unstated); Kubo 2022 asks for the flock centre inside the target
and the whole flock fitting on a circle of radius 10 (section 4.1; its introduction states the
aim as all sheep in the goal at the same time). Strombom's
rule can be read afterwards from the per-tick ``gcm_in_goal``; Kubo's cannot,
since ``extent`` is an RMS radius and no metric records the farthest sheep.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from typing import Any

import numpy as np
import pandas as pd

from sim.core.simulation_state import SimulationState
from sim.core.world.arena import GoalZone, World
from sim.core.world.layouts import (
    DOG_STARTS,
    LAYOUTS,
    field_size,
    layout_extent,
    place_dogs,
    place_flock,
)

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
)

# Fractions of the flock whose first full arrival is recorded in every trial row, so a
# weaker success rule than "every sheep" (both papers use one) can be read afterwards.
ARRIVAL_FRACTIONS = (0.90, 0.95, 0.99)


def check(config: dict[str, Any]) -> None:
    """Task settings of a built run config."""
    if config["dog_start"] not in DOG_STARTS:
        raise ValueError(f"dog_start {config['dog_start']!r} not in {DOG_STARTS}")
    if config["initial_layout"] not in LAYOUTS:
        raise ValueError(f"initial_layout {config['initial_layout']!r} not in {LAYOUTS}")


def row_columns(config: dict[str, Any], history: pd.DataFrame) -> dict[str, Any]:
    """The task's columns of a trial row: the geometry it ran in and where it ended."""
    final = history.iloc[-1]
    return {
        **arrival_columns(config, history),
        "goal_radius": float(config["goal_radius"]),
        "success_fraction": float(config["success_fraction"]),
        "drive_distance": abs(float(config["goal_center"][0]) - float(config["flock_center"][0])),
        "world_width": float(config["world_width"]),
        "world_height": float(config["world_height"]),
        "final_gcm_goal": float(final["gcm_goal"]),
        "final_sheep_in_goal": float(final["sheep_in_goal"]),
    }


def arrival_columns(config: dict[str, Any], history: pd.DataFrame) -> dict[str, float]:
    """Model seconds until a fraction of the sheep first stood in the goal (NaN if never).

    Reads the first tick at which ``sheep_in_goal`` reached the fraction of N. These are
    first arrivals, not held ones: a sheep may leave again before the trial ends.
    """
    dt = float(config["dt"])
    n = int(config["n_sheep"])
    inside = history["sheep_in_goal"].to_numpy(dtype=float)
    out: dict[str, float] = {}
    for fraction in ARRIVAL_FRACTIONS:
        hit = np.flatnonzero(inside >= fraction * n)
        ticks = float(history["tick"].to_numpy()[hit[0]]) if hit.size else float("nan")
        out[f"seconds_to_{round(fraction * 100)}pct_in_goal"] = ticks * dt
    return out


def create_world(config: dict[str, Any]) -> World:
    return World(
        width=float(config["world_width"]),
        height=float(config["world_height"]),
        goal=GoalZone(
            center=np.asarray(config["goal_center"], dtype=float),
            radius=float(config["goal_radius"]),
            required_fraction=float(config["success_fraction"]),
        ),
    )


def initial_positions(
    config: dict[str, Any], rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray]:
    """Flock at its start centre and outside the goal; dogs behind it, away from the goal."""
    return place_flock(config, rng), place_dogs(config)


def is_success(state: SimulationState) -> bool:
    """Every sheep is inside the goal, or the share ``success_fraction`` of them when that is
    below 1 (HerdSim rule; see the module docstring)."""
    return state.world.goal.reached(state.sheep_positions)


def build_setup(
    settings: Mapping[str, Any],
    *,
    flock_radius: float,
    n_sheep: int,
    layouts: tuple[str, ...],
    max_dogs: int,
) -> dict[str, Any]:
    """Setup keys of one flock size, from the protocol settings and the flock radius R_f.

    The drive is max(``drive_distance_multiple`` x R_f, ``drive_distance_min``,
    reach + goal radius + R_f), where reach is the farthest start sheep of every
    layout in ``layouts``, so the goal never overlaps a start. The third term
    grows like the separation distance N^(2/3) while R_f grows more slowly, so
    in a protocol with scattered layouts the drive is longer than the multiple
    from about N = 200 on, for its compact cells too: computed with the
    calibrated R_f, 13.4 R_f at N = 200 and 18.1 R_f at N = 400 with all four
    layouts in the protocol (17.2 at N = 400 with wide only), against 13 R_f in
    a compact-only protocol.
    The drive length is recorded per trial, so analyses can condition on it.

    The field is sized for ``layouts`` and ``max_dogs`` (the protocol's largest
    D), so all cells of a protocol at one N and one method share one field and
    one goal (R_f is calibrated per method); the drive axis runs along x
    (mirrored for a negative ``drive_distance_multiple``).
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
