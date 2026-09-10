"""Communication-free multi-dog local Collect/Drive decisions."""

from __future__ import annotations

from typing import Any

from algorithms.strombom.config import STROMBOM_DEFAULTS
from algorithms.strombom.heuristics import (
    compute_shepherd_velocity,
    should_collect,
)
from controllers.helpers import apply_dog_speeds, empty_dog_velocities, view_from_observation
from core.dog_controller import BaseDogController
from core.observation import ShepherdObservation
from core.simulation_state import SimulationState


class CommunicationFreeController(BaseDogController):
    """Each dog decides Collect/Drive from its own observation only."""

    @property
    def id(self) -> str:
        return "communication_free"

    @property
    def name(self) -> str:
        return "Communication-Free"

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
        lines = []
        modes = []
        obs_by_idx = {o.shepherd_index: o for o in observations}
        for i in range(state.n_shepherds):
            if not state.shepherd_active[i] or i not in obs_by_idx:
                continue
            obs = obs_by_idx[i]
            if obs.n_sheep_seen == 0:
                continue
            local = view_from_observation(state, obs)
            velocities[i] = compute_shepherd_velocity(local, config, i)
            mode = "collect" if should_collect(local, config) else "drive"
            modes.append(mode)
            lines.append(
                {
                    "from": state.shepherd_positions[i].tolist(),
                    "to": (
                        local.sheep_positions[int(local.furthest_sheep_index())].tolist()
                        if mode == "collect"
                        else local.sheep_centroid.tolist()
                    ),
                    "mode": mode,
                }
            )

        velocities = apply_dog_speeds(velocities, state, config)
        metadata = dict(state.metadata)
        metadata["herding_mode"] = modes[0] if modes else "drive"
        metadata["assignment_lines"] = lines
        return state.copy_with(
            shepherd_positions=state.shepherd_positions + velocities,
            shepherd_velocities=velocities,
            metadata=metadata,
        )
