"""Multi-dog Collect/Drive with outlier assignment."""

from __future__ import annotations

from typing import Any

import numpy as np

from methods.strombom.config import STROMBOM_DEFAULTS
from methods.strombom.heuristics import (
    collect_offset,
    compute_threshold,
    drive_offset,
    shepherd_step_toward,
)
from plugins.dogs.helpers import apply_dog_speeds, empty_dog_velocities
from core.agents.goal import resolve_goal_center
from core.agents.shepherd import position_behind_target
from core.dog_controller import BaseDogController
from core.observation import ShepherdObservation
from core.simulation_state import SimulationState


def _sensing_radius(config: dict[str, Any]) -> float:
    if config.get("sensing_range") is not None:
        return float(config["sensing_range"])
    return float(config.get("r_s", 65.0))


def _sheep_for_dog(
    dog_index: int,
    observations: list[ShepherdObservation],
    state: SimulationState,
    config: dict[str, Any],
) -> np.ndarray:
    """Sheep positions this dog may use under the communication rule.

    none: this dog's observation only.
    neighbour_broadcast: own observation plus dogs inside the sensing radius.
    global_shared: union of sheep the dogs actually sensed, not true positions.
    """
    by_idx = {int(o.shepherd_index): o for o in observations}
    own = by_idx.get(dog_index)
    comm = str(config.get("communication", "none"))

    def _stack(obs_list: list[ShepherdObservation]) -> np.ndarray:
        parts = [o.sheep_positions for o in obs_list if o.n_sheep_seen]
        if not parts:
            return np.zeros((0, 2))
        return np.vstack(parts)

    if comm == "global_shared":
        return _stack(list(observations))
    if comm == "neighbour_broadcast":
        if own is None:
            selected: list[ShepherdObservation] = []
        else:
            selected = [own]
        origin = state.shepherd_positions[dog_index]
        radius = _sensing_radius(config)
        for obs in observations:
            if int(obs.shepherd_index) == dog_index:
                continue
            if float(np.linalg.norm(obs.self_position - origin)) <= radius:
                selected.append(obs)
        return _stack(selected)
    if own is None or own.n_sheep_seen == 0:
        return np.zeros((0, 2))
    return np.asarray(own.sheep_positions, dtype=float)


class CollectDriveMultiController(BaseDogController):
    @property
    def id(self) -> str:
        return "collect_drive_multi"

    @property
    def name(self) -> str:
        return "Collect/Drive Multi"

    @property
    def default_config(self) -> dict[str, Any]:
        cfg = {
            k: STROMBOM_DEFAULTS[k]
            for k in (
                "r_a",
                "noise_strength",
                "shepherd_speed",
                "shepherd_stop_multiple",
                "collect_threshold_scale",
            )
        }
        cfg["n_shepherds"] = 3
        return cfg

    def step(
        self,
        state: SimulationState,
        observations: list[ShepherdObservation],
        config: dict[str, Any],
    ) -> SimulationState:
        velocities = empty_dog_velocities(state)
        lines: list[dict[str, Any]] = []
        mode = "drive"
        if not observations:
            return state.copy_with(shepherd_velocities=velocities)

        m = state.n_shepherds
        if m == 0:
            return state.copy_with(shepherd_velocities=velocities)

        goal = resolve_goal_center(state, config)
        c_offset = collect_offset(config)
        scale = float(config.get("collect_threshold_scale", 1.0))
        any_collect = False

        for i in range(m):
            if not state.shepherd_active[i]:
                continue
            sheep_pos = _sheep_for_dog(i, observations, state, config)
            if sheep_pos.shape[0] == 0:
                continue
            centroid = np.mean(sheep_pos, axis=0)
            threshold = compute_threshold(sheep_pos.shape[0], config["r_a"]) * scale
            distances = np.linalg.norm(sheep_pos - centroid, axis=1)
            outliers = np.where(distances > threshold)[0]
            drive_state = state.copy_with(sheep_positions=sheep_pos)
            d_offset = drive_offset(drive_state, config)

            if len(outliers) == 0:
                base = position_behind_target(centroid, goal, d_offset)
                spacing = 4.0 * float(config.get("r_a", 2.0))
                angle = (2 * np.pi * i) / m
                spaced = base + spacing * np.array([np.cos(angle), np.sin(angle)])
                velocities[i] = shepherd_step_toward(drive_state, config, i, spaced)
                lines.append(
                    {
                        "from": state.shepherd_positions[i].tolist(),
                        "to": spaced.tolist(),
                        "mode": "drive",
                    }
                )
            else:
                any_collect = True
                order = outliers[np.argsort(-distances[outliers])]
                lateral_step = 2.0 * float(config.get("r_a", 2.0))
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
                velocities[i] = shepherd_step_toward(drive_state, config, i, target)
                lines.append(
                    {
                        "from": state.shepherd_positions[i].tolist(),
                        "to": sheep_pos[sheep_idx].tolist(),
                        "mode": "collect",
                        "sheep_index": sheep_idx,
                    }
                )

        if any_collect:
            mode = "collect"

        velocities = apply_dog_speeds(velocities, state, config)
        metadata = dict(state.metadata)
        metadata["herding_mode"] = mode
        metadata["assignment_lines"] = lines
        return state.copy_with(
            shepherd_positions=state.shepherd_positions + velocities,
            shepherd_velocities=velocities,
            metadata=metadata,
        )
