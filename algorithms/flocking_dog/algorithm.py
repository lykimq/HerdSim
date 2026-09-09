"""Flocking Dog 2024 herding algorithm (Jadhav et al.).

Reference:
Collective responses of flocking sheep to a herding dog,
Communications Biology, 2024.
https://doi.org/10.1038/s42003-024-07245-8

Dynamics follow Methods / Fig. 7 and MATLAB `model/herding_model.m`.
Collect/Drive targets reuse Strombom helpers; dog slowdown within r_a
and topological sheep rules are flocking-specific.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from algorithms.flocking_dog.config import FLOCKING_DOG_DEFAULTS
from algorithms.flocking_dog.dynamics import (
    dog_repulsion_unit,
    random_alignment,
    random_attraction,
    sheep_repulsion,
)
from algorithms.strombom.heuristics import (
    collect_target,
    drive_target,
    should_collect,
    strombom_assignment_lines,
)
from core.agents.sheep import compute_noise, nearest_neighbor_indices, unit_vector
from core.agents.shepherd import move_toward
from core.base_algorithm import BaseAlgorithm
from core.simulation_state import SimulationState


class FlockingDogAlgorithm(BaseAlgorithm):
    """Topological flocking sheep with Collect/Drive dog (paper defaults)."""

    @property
    def id(self) -> str:
        return "flocking_dog"

    @property
    def name(self) -> str:
        return "Flocking Dog 2024"

    @property
    def default_config(self) -> dict[str, Any]:
        return FLOCKING_DOG_DEFAULTS.copy()

    def step(self, state: SimulationState, config: dict[str, Any]) -> SimulationState:
        sheep_vel = self._update_sheep(state, config)
        dog_vel = self._update_dogs(state, config)

        sheep_pos = state.sheep_positions + sheep_vel
        dog_pos = state.shepherd_positions + dog_vel

        metadata = dict(state.metadata)
        metadata["r_a"] = float(config.get("r_a", 2.0))
        if state.n_shepherds and state.n_sheep:
            metadata["assignment_lines"] = strombom_assignment_lines(state, config)
            metadata["herding_mode"] = (
                "collect" if should_collect(state, config) else "drive"
            )

        return SimulationState(
            tick=state.tick,
            sheep_positions=sheep_pos,
            sheep_velocities=sheep_vel,
            shepherd_positions=dog_pos,
            shepherd_velocities=dog_vel,
            world=state.world,
            rng=state.rng,
            metadata=metadata,
        )

    def _update_sheep(self, state: SimulationState, config: dict) -> np.ndarray:
        n = state.n_sheep
        out = np.zeros((n, 2))
        if state.n_shepherds == 0:
            return out

        dog = state.shepherd_positions[0]
        r_s = float(config["r_s"])
        r_a = float(config["r_a"])
        k = int(config["k_neighbors"])
        n_att = int(config["n_attraction"])
        n_ali = int(config["n_alignment"])
        h = float(config["inertia"])
        rho_a = float(config["sheep_repulsion_weight"])
        rho_d = float(config["dog_repulsion_weight"])
        c = float(config["attraction_weight"])
        alg_w = float(config["alignment_weight"])
        e = float(config["noise_strength"])
        speed = float(config["sheep_speed"])

        for i in range(n):
            dist_dog = float(np.linalg.norm(dog - state.sheep_positions[i]))
            # Graze (no motion) when dog beyond Rd.
            if dist_dog > r_s:
                continue

            neighbors = nearest_neighbor_indices(state.sheep_positions, i, k)
            atr, atr_idx = random_attraction(
                state.sheep_positions, i, neighbors, n_att, state.rng
            )
            ali = random_alignment(state.sheep_velocities, atr_idx, n_ali, state.rng)
            rep = sheep_repulsion(state.sheep_positions, i, r_a)
            dog_rep = dog_repulsion_unit(state.sheep_positions[i], dog)
            noise = compute_noise(state.rng, e)

            heading = (
                h * unit_vector(state.sheep_velocities[i])
                + rho_a * rep
                + rho_d * dog_rep
                + c * atr
                + alg_w * ali
                + noise
            )
            out[i] = unit_vector(heading) * speed
        return out

    def _update_dogs(self, state: SimulationState, config: dict) -> np.ndarray:
        out = np.zeros_like(state.shepherd_positions)
        if state.n_shepherds == 0 or state.n_sheep == 0:
            return out

        r_a = float(config["r_a"])
        speed = float(config["dog_speed"])
        close_speed = float(config["dog_close_speed"])
        e = float(config["noise_strength"])
        centroid = state.sheep_centroid

        for i in range(state.n_shepherds):
            dog = state.shepherd_positions[i]
            min_dist = float(np.min(np.linalg.norm(state.sheep_positions - dog, axis=1)))

            # Author MATLAB: continue previous unit heading at absolute 0.05
            # when within r_a of any sheep (not 0.05*vDog; not toward Pdrive).
            if min_dist <= r_a:
                prev = unit_vector(state.shepherd_velocities[i])
                if np.linalg.norm(prev) < 1e-10:
                    prev = unit_vector(centroid - dog)
                out[i] = prev * close_speed
                continue

            if should_collect(state, config):
                target = collect_target(state, config)
            else:
                target = drive_target(state, config)

            base = move_toward(dog, target, speed)
            noise = compute_noise(state.rng, e)
            direction = unit_vector(base + noise)
            step = min(speed, float(np.linalg.norm(target - dog)))
            out[i] = direction * step
        return out
