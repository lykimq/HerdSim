"""Multi-dog Collect/Drive with outlier assignment."""

from __future__ import annotations

from typing import Any

import numpy as np

from algorithms.strombom.config import STROMBOM_DEFAULTS
from algorithms.strombom.heuristics import (
    collect_offset,
    compute_threshold,
    drive_offset,
    shepherd_step_toward,
)
from controllers.helpers import apply_dog_speeds, empty_dog_velocities, view_from_observation
from core.agents.goal import resolve_goal_center
from core.agents.shepherd import position_behind_target
from core.dog_controller import BaseDogController
from core.observation import ShepherdObservation
from core.simulation_state import SimulationState


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
        # Use union of observed sheep when communication is global_shared;
        # otherwise each dog uses its own observation for local decisions.
        comm = str(config.get("communication", "none"))
        if not observations:
            return state.copy_with(shepherd_velocities=velocities)

        if comm == "global_shared":
            sheep_pos = state.sheep_positions
            local_state = state
        else:
            # Merge observed sheep from all observations for assignment when
            # communication is neighbour_broadcast; else per-dog views.
            if comm == "neighbour_broadcast":
                chunks = [o.sheep_positions for o in observations if o.n_sheep_seen]
                if chunks:
                    sheep_pos = np.vstack(chunks)
                else:
                    sheep_pos = np.zeros((0, 2))
                local_state = state.copy_with(sheep_positions=sheep_pos)
            else:
                local_state = view_from_observation(state, observations[0])
                sheep_pos = local_state.sheep_positions

        m = state.n_shepherds
        if m == 0 or sheep_pos.shape[0] == 0:
            return state.copy_with(shepherd_velocities=velocities)

        centroid = np.mean(sheep_pos, axis=0)
        scale = float(config.get("collect_threshold_scale", 1.0))
        threshold = compute_threshold(sheep_pos.shape[0], config["r_a"]) * scale
        distances = np.linalg.norm(sheep_pos - centroid, axis=1)
        outliers = np.where(distances > threshold)[0]
        goal = resolve_goal_center(state, config)
        c_offset = collect_offset(config)
        # drive_offset needs n_sheep on state
        drive_state = local_state.copy_with(sheep_positions=sheep_pos)
        d_offset = drive_offset(drive_state, config)

        if len(outliers) == 0:
            base = position_behind_target(centroid, goal, d_offset)
            spacing = 4.0 * float(config.get("r_a", 2.0))
            for i in range(m):
                if not state.shepherd_active[i]:
                    continue
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
            mode = "collect"
            order = outliers[np.argsort(-distances[outliers])]
            lateral_step = 2.0 * float(config.get("r_a", 2.0))
            for i in range(m):
                if not state.shepherd_active[i]:
                    continue
                sheep_idx = int(order[i % len(order)])
                target = position_behind_target(
                    sheep_pos[sheep_idx], centroid, c_offset
                )
                tangential = np.array(
                    [
                        -(sheep_pos[sheep_idx][1] - centroid[1]),
                        sheep_pos[sheep_idx][0] - centroid[0],
                    ]
                )
                tn = np.linalg.norm(tangential)
                if tn > 1e-10:
                    target = target + (tangential / tn) * (
                        lateral_step * (i - (m - 1) / 2.0)
                    )
                velocities[i] = shepherd_step_toward(drive_state, config, i, target)
                lines.append(
                    {
                        "from": state.shepherd_positions[i].tolist(),
                        "to": sheep_pos[sheep_idx].tolist(),
                        "mode": "collect",
                        "sheep_index": sheep_idx,
                    }
                )

        velocities = apply_dog_speeds(velocities, state, config)
        metadata = dict(state.metadata)
        metadata["herding_mode"] = mode
        metadata["assignment_lines"] = lines
        return state.copy_with(
            shepherd_positions=state.shepherd_positions + velocities,
            shepherd_velocities=velocities,
            metadata=metadata,
        )
