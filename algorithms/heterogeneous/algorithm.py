"""Strombom Collect/Drive with responsive vs stubborn sheep.

Stubborn sheep use a reduced shepherd-repulsion weight (rs). Response factors
are assigned once from state.rng and stored in metadata["sheep_response"].
"""

from __future__ import annotations

from typing import Any

import numpy as np

from algorithms.heterogeneous.config import HETEROGENEOUS_DEFAULTS
from algorithms.strombom.algorithm import StrombomAlgorithm
from algorithms.strombom.heuristics import should_collect, strombom_assignment_lines
from core.agents.sheep import (
    compose_strombom_heading,
    compute_attraction,
    compute_local_centroid_knn,
    compute_noise,
    compute_repulsion_from_neighbours,
    compute_repulsion_from_shepherds,
    unit_vector,
)
from core.simulation_state import SimulationState


def assign_sheep_response(
    n_sheep: int, config: dict, rng: np.random.Generator
) -> np.ndarray:
    """Deterministic responsive/stubborn factors in (0, 1] from rng."""
    frac = float(config.get("stubborn_fraction", 0.2))
    frac = min(max(frac, 0.0), 1.0)
    scale = float(config.get("stubborn_rs_scale", 0.25))
    scale = min(max(scale, 1e-6), 1.0)
    response = np.ones(n_sheep, dtype=float)
    n_stubborn = int(round(frac * n_sheep))
    if n_stubborn <= 0:
        return response
    n_stubborn = min(n_stubborn, n_sheep)
    idx = rng.choice(n_sheep, size=n_stubborn, replace=False)
    response[idx] = scale
    return response


def ensure_sheep_response(
    state: SimulationState, config: dict
) -> np.ndarray:
    """Return cached or newly assigned sheep_response of length n_sheep."""
    existing = state.metadata.get("sheep_response")
    if existing is not None and len(existing) == state.n_sheep:
        return np.asarray(existing, dtype=float)
    return assign_sheep_response(state.n_sheep, config, state.rng)


class HeterogeneousAlgorithm(StrombomAlgorithm):
    """Strombom herding with per-sheep shepherd repulsion response."""

    @property
    def id(self) -> str:
        return "heterogeneous"

    @property
    def name(self) -> str:
        return "Heterogeneous Sheep"

    @property
    def default_config(self) -> dict[str, Any]:
        return HETEROGENEOUS_DEFAULTS.copy()

    def step(self, state: SimulationState, config: dict[str, Any]) -> SimulationState:
        response = ensure_sheep_response(state, config)
        # Seed metadata before sheep update so _update_sheep can read it.
        seeded = SimulationState(
            tick=state.tick,
            sheep_positions=state.sheep_positions,
            sheep_velocities=state.sheep_velocities,
            shepherd_positions=state.shepherd_positions,
            shepherd_velocities=state.shepherd_velocities,
            world=state.world,
            rng=state.rng,
            metadata={**dict(state.metadata), "sheep_response": response.tolist()},
        )
        new_sheep_vel = self._update_sheep(seeded, config)
        new_shepherd_vel = self._update_shepherds(seeded, config)

        new_sheep_pos = seeded.sheep_positions + new_sheep_vel
        new_shepherd_pos = seeded.shepherd_positions + new_shepherd_vel

        metadata = dict(seeded.metadata)
        metadata["r_a"] = float(config.get("r_a", metadata.get("r_a", 2.0)))
        metadata["collect_threshold_scale"] = float(
            config.get(
                "collect_threshold_scale",
                metadata.get("collect_threshold_scale", 1.0),
            )
        )
        metadata["sheep_response"] = response.tolist()
        if seeded.n_shepherds and seeded.n_sheep:
            metadata["assignment_lines"] = strombom_assignment_lines(seeded, config)
            metadata["herding_mode"] = (
                "collect" if should_collect(seeded, config) else "drive"
            )

        return SimulationState(
            tick=seeded.tick,
            sheep_positions=new_sheep_pos,
            sheep_velocities=new_sheep_vel,
            shepherd_positions=new_shepherd_pos,
            shepherd_velocities=new_shepherd_vel,
            world=seeded.world,
            rng=seeded.rng,
            metadata=metadata,
        )

    def _update_sheep(self, state: SimulationState, config: dict) -> np.ndarray:
        """Strombom sheep update with per-sheep effective rs_weight."""
        n = state.n_sheep
        velocities = np.zeros((n, 2))
        r_a = float(config["r_a"])
        r_s = float(config["r_s"])
        n_neighbors = int(config.get("n_neighbors", -1))
        c = float(config["c"])
        ra_weight = float(config.get("ra_weight", r_a))
        base_rs = float(config.get("rs_weight", 1.0))
        noise_str = float(config["noise_strength"])
        speed = float(config["sheep_speed"])
        inertia = float(config["inertia"])
        graze_p = float(config.get("graze_move_prob", 0.05))
        response = ensure_sheep_response(state, config)

        for i in range(n):
            min_shep_dist = (
                float(
                    np.min(
                        np.linalg.norm(
                            state.shepherd_positions - state.sheep_positions[i],
                            axis=1,
                        )
                    )
                )
                if state.n_shepherds
                else float("inf")
            )

            if min_shep_dist > r_s:
                if state.rng.random() < graze_p:
                    velocities[i] = unit_vector(compute_noise(state.rng, 1.0)) * speed
                continue

            lcm = compute_local_centroid_knn(state.sheep_positions, i, n_neighbors)
            attraction = compute_attraction(state.sheep_positions[i], lcm)
            repulsion_sheep = compute_repulsion_from_neighbours(
                state.sheep_positions, i, r_a
            )
            repulsion_shep = compute_repulsion_from_shepherds(
                state.sheep_positions[i], state.shepherd_positions, r_s
            )
            noise = compute_noise(state.rng, noise_str)
            rs_weight = base_rs * float(response[i])
            heading = compose_strombom_heading(
                state.sheep_velocities[i],
                attraction,
                repulsion_sheep,
                repulsion_shep,
                noise,
                inertia=inertia,
                c=c,
                ra_weight=ra_weight,
                rs_weight=rs_weight,
            )
            velocities[i] = heading * speed
        return velocities
