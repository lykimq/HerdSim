"""Multi-dog Collect/Drive with outlier assignment."""

from __future__ import annotations

from typing import Any

import numpy as np
from core.observation import ShepherdObservation, sensing_range
from core.simulation_state import SimulationState
from methods.strombom.heuristics import (
    collect_offset,
    compute_threshold,
    drive_offset,
    shepherd_step_toward,
)

from .helpers import empty_dog_velocities, finalize_dog_step, position_behind_target


def _union_sheep_positions(obs_list: list[ShepherdObservation]) -> np.ndarray:
    """Unique sheep by index across observations (true set union, not a stack)."""
    by_sheep: dict[int, np.ndarray] = {}
    for obs in obs_list:
        if not obs.n_sheep_seen:
            continue
        indices = np.asarray(obs.sheep_indices, dtype=int).reshape(-1)
        positions = np.asarray(obs.sheep_positions, dtype=float).reshape(-1, 2)
        if indices.shape[0] != positions.shape[0]:
            raise ValueError(
                "Observation sheep_indices and sheep_positions length mismatch "
                + f"({indices.shape[0]} vs {positions.shape[0]})."
            )
        for sheep_id, pos in zip(indices, positions):
            key = int(sheep_id)
            if key not in by_sheep:
                by_sheep[key] = pos
    if not by_sheep:
        return np.zeros((0, 2))
    order = sorted(by_sheep)
    return np.vstack([by_sheep[k] for k in order])


def _sheep_for_dog(
    dog_index: int,
    observations: list[ShepherdObservation],
    state: SimulationState,
    config: dict[str, Any],
) -> np.ndarray:
    """Sheep positions this dog may use under the communication rule.

    none: this dog's observation only.
    neighbour_broadcast: union of own observation and dogs inside the sensing radius.
    global_shared: union of sheep the dogs actually sensed, not true positions.
    """
    by_idx = {int(o.shepherd_index): o for o in observations}
    own = by_idx.get(dog_index)
    comm = str(config["communication"])

    if comm == "global_shared":
        return _union_sheep_positions(list(observations))
    if comm == "neighbour_broadcast":
        if own is None:
            selected: list[ShepherdObservation] = []
        else:
            selected = [own]
        origin = state.shepherd_positions[dog_index]
        radius = sensing_range(config)
        for obs in observations:
            if int(obs.shepherd_index) == dog_index:
                continue
            if float(np.linalg.norm(obs.self_position - origin)) <= radius:
                selected.append(obs)
        return _union_sheep_positions(selected)
    if own is None or own.n_sheep_seen == 0:
        return np.zeros((0, 2))
    return np.asarray(own.sheep_positions, dtype=float)


def step(
    state: SimulationState,
    observations: list[ShepherdObservation],
    config: dict[str, Any],
) -> SimulationState:
    velocities = empty_dog_velocities(state)
    m = state.n_shepherds
    if m == 0:
        return state.copy_with(shepherd_velocities=velocities)

    phase = str(state.metadata.get("chg_phase", "collect"))
    if phase == "exit":
        # Drive toward the right-wall gate center (collect_hold_gate task).
        goal = state.world.gate_center
    else:
        goal = state.world.goal.center
    r_a = float(config["r_a"])
    c_offset = collect_offset(config)
    any_collect = False

    for i in range(m):
        sheep_pos = _sheep_for_dog(i, observations, state, config)
        if sheep_pos.shape[0] == 0:
            continue
        # Sheep already past the gate are ignored for steering.
        if phase == "exit":
            active = sheep_pos[:, 0] < float(state.world.width)
            if not np.any(active):
                continue
            sheep_pos = sheep_pos[active]
        centroid = np.mean(sheep_pos, axis=0)
        threshold = compute_threshold(sheep_pos.shape[0], r_a)
        distances = np.linalg.norm(sheep_pos - centroid, axis=1)
        outliers = np.where(distances > threshold)[0]
        drive_state = state.copy_with(sheep_positions=sheep_pos)
        d_offset = drive_offset(drive_state, config)

        if len(outliers) == 0:
            base = position_behind_target(centroid, goal, d_offset)
            spacing = 4.0 * r_a
            angle = (2 * np.pi * i) / m
            spaced = base + spacing * np.array([np.cos(angle), np.sin(angle)])
            velocities[i] = shepherd_step_toward(
                drive_state,
                config,
                i,
                spaced,
                proximity_sheep=state.sheep_positions,
            )
        else:
            any_collect = True
            order = outliers[np.argsort(-distances[outliers])]
            lateral_step = 2.0 * r_a
            sheep_idx = int(order[i % len(order)])
            target = position_behind_target(sheep_pos[sheep_idx], centroid, c_offset)
            tangential = np.array(
                [
                    -(sheep_pos[sheep_idx][1] - centroid[1]),
                    sheep_pos[sheep_idx][0] - centroid[0],
                ]
            )
            tn = np.linalg.norm(tangential)
            if tn > 1e-10:
                target = target + (tangential / tn) * (lateral_step * (i - (m - 1) / 2.0))
            velocities[i] = shepherd_step_toward(
                drive_state,
                config,
                i,
                target,
                proximity_sheep=state.sheep_positions,
            )

    return finalize_dog_step(
        state,
        velocities,
        metadata_updates={"herding_mode": "collect" if any_collect else "drive"},
    )
