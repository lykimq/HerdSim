"""V-formation multi-shepherd dog controller."""

from __future__ import annotations

from typing import Any

import numpy as np

from algorithms.strombom.heuristics import (
    collect_offset,
    compute_threshold,
    drive_offset,
    shepherd_step_toward,
)
from algorithms.v_formation.config import V_FORMATION_DEFAULTS
from controllers.helpers import apply_dog_speeds, empty_dog_velocities, view_from_observation
from core.agents.goal import resolve_goal_center
from core.agents.shepherd import position_behind_target
from core.dog_controller import BaseDogController
from core.observation import ShepherdObservation
from core.simulation_state import SimulationState


def v_arc_targets(state: SimulationState, config: dict) -> list[np.ndarray]:
    m = state.n_shepherds
    centroid = state.sheep_centroid
    goal = resolve_goal_center(state, config)
    offset = float(config["v_arc_offset"]) if "v_arc_offset" in config else drive_offset(
        state, config
    )
    spacing = np.radians(float(config.get("v_angle_deg", 35.0)))
    behind = centroid - goal
    bn = float(np.linalg.norm(behind))
    behind_u = np.array([1.0, 0.0]) if bn < 1e-10 else behind / bn
    targets: list[np.ndarray] = []
    for i in range(m):
        ang = (i - (m - 1) / 2.0) * spacing
        c, s = float(np.cos(ang)), float(np.sin(ang))
        rotated = np.array(
            [
                behind_u[0] * c - behind_u[1] * s,
                behind_u[0] * s + behind_u[1] * c,
            ]
        )
        targets.append(centroid + rotated * offset)
    return targets


class VFormationController(BaseDogController):
    @property
    def id(self) -> str:
        return "v_formation"

    @property
    def name(self) -> str:
        return "V-Formation"

    @property
    def default_config(self) -> dict[str, Any]:
        return {
            k: V_FORMATION_DEFAULTS[k]
            for k in (
                "n_shepherds",
                "r_a",
                "noise_strength",
                "shepherd_speed",
                "shepherd_stop_multiple",
                "collect_threshold_scale",
                "v_angle_deg",
            )
        }

    def step(
        self,
        state: SimulationState,
        observations: list[ShepherdObservation],
        config: dict[str, Any],
    ) -> SimulationState:
        velocities = empty_dog_velocities(state)
        if not observations:
            return state.copy_with(shepherd_velocities=velocities)
        local = view_from_observation(state, observations[0])
        if local.n_sheep == 0:
            return state.copy_with(shepherd_velocities=velocities)

        lines: list[dict[str, Any]] = []
        mode = "drive"
        m = state.n_shepherds
        scale = float(config.get("collect_threshold_scale", 1.0))
        threshold = compute_threshold(local.n_sheep, config["r_a"]) * scale
        distances = local.distances_to_centroid()
        outliers = np.where(distances > threshold)[0]
        centroid = local.sheep_centroid
        c_offset = collect_offset(config)

        if len(outliers) == 0:
            targets = v_arc_targets(local, config)
            for i in range(m):
                if not state.shepherd_active[i]:
                    continue
                target = targets[i]
                velocities[i] = shepherd_step_toward(local, config, i, target)
                lines.append(
                    {
                        "from": state.shepherd_positions[i].tolist(),
                        "to": target.tolist(),
                        "mode": "drive",
                    }
                )
        else:
            mode = "collect"
            order = outliers[np.argsort(-distances[outliers])]
            for i in range(m):
                if not state.shepherd_active[i]:
                    continue
                sheep_idx = int(order[i % len(order)])
                target = position_behind_target(
                    local.sheep_positions[sheep_idx], centroid, c_offset
                )
                tangential = np.array(
                    [
                        -(local.sheep_positions[sheep_idx][1] - centroid[1]),
                        local.sheep_positions[sheep_idx][0] - centroid[0],
                    ]
                )
                tn = float(np.linalg.norm(tangential))
                if tn > 1e-10:
                    target = target + (tangential / tn) * (4.0 * (i - (m - 1) / 2.0))
                velocities[i] = shepherd_step_toward(local, config, i, target)
                lines.append(
                    {
                        "from": state.shepherd_positions[i].tolist(),
                        "to": local.sheep_positions[sheep_idx].tolist(),
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
