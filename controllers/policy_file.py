"""Frozen policy-file dog controller for offline RL / imitation eval."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np

from algorithms.strombom.config import STROMBOM_DEFAULTS
from controllers.collect_drive import CollectDriveController
from controllers.helpers import apply_dog_speeds, empty_dog_velocities
from core.dog_controller import BaseDogController
from core.observation import ShepherdObservation
from core.simulation_state import SimulationState


class PolicyFileController(BaseDogController):
    """Load a simple JSON policy; fall back to Collect/Drive if missing.

    Policy format::
        {
          "type": "linear",
          "weights": [[...], [...]],
          "bias": [.., ..],
          "feature": "relative_gcm_goal"
        }
    """

    @property
    def id(self) -> str:
        return "policy_file"

    @property
    def name(self) -> str:
        return "Policy File"

    @property
    def default_config(self) -> dict[str, Any]:
        cfg = {
            k: STROMBOM_DEFAULTS[k]
            for k in ("n_shepherds", "r_a", "shepherd_speed", "noise_strength")
        }
        cfg["policy_path"] = ""
        return cfg

    def step(
        self,
        state: SimulationState,
        observations: list[ShepherdObservation],
        config: dict[str, Any],
    ) -> SimulationState:
        path = str(config.get("policy_path") or "").strip()
        if not path or not Path(path).is_file():
            return CollectDriveController().step(state, observations, config)

        policy = json.loads(Path(path).read_text(encoding="utf-8"))
        velocities = empty_dog_velocities(state)
        speed = float(config.get("shepherd_speed", 1.5))
        weights = np.asarray(policy.get("weights", [[1.0, 0.0], [0.0, 1.0]]), dtype=float)
        bias = np.asarray(policy.get("bias", [0.0, 0.0]), dtype=float)
        obs_by_idx = {o.shepherd_index: o for o in observations}

        for i in range(state.n_shepherds):
            if not state.shepherd_active[i] or i not in obs_by_idx:
                continue
            obs = obs_by_idx[i]
            if obs.n_sheep_seen == 0 or obs.goal_center is None:
                continue
            gcm = np.mean(obs.sheep_positions, axis=0)
            feat = np.concatenate(
                [
                    gcm - obs.self_position,
                    obs.goal_center - obs.self_position,
                ]
            )
            # Use first 2 feature dims if weights are 2x2; else truncate/pad.
            if weights.shape[1] != feat.shape[0]:
                feat = feat[: weights.shape[1]]
                if feat.shape[0] < weights.shape[1]:
                    feat = np.pad(feat, (0, weights.shape[1] - feat.shape[0]))
            action = weights @ feat + bias
            norm = np.linalg.norm(action)
            if norm > 1e-10:
                velocities[i] = (action / norm) * speed

        velocities = apply_dog_speeds(velocities, state, config)
        metadata = dict(state.metadata)
        metadata["herding_mode"] = "policy"
        return state.copy_with(
            shepherd_positions=state.shepherd_positions + velocities,
            shepherd_velocities=velocities,
            metadata=metadata,
        )
