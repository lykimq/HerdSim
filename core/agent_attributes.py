"""Agent attribute initialization and failure / environment updates."""

from __future__ import annotations

from typing import Any

import numpy as np

from core.simulation_state import SimulationState
from core.world import GoalZone, clamp_goal_center


def assign_sheep_response(
    n_sheep: int, config: dict[str, Any], rng: np.random.Generator
) -> np.ndarray:
    """Deterministic responsive/stubborn factors in (0, 1] from rng."""
    frac = float(config.get("stubborn_fraction", 0.0))
    frac = min(max(frac, 0.0), 1.0)
    scale = float(
        config.get(
            "stubborn_response_scale",
            config.get("stubborn_rs_scale", 0.25),
        )
    )
    scale = min(max(scale, 1e-6), 1.0)
    response = np.ones(n_sheep, dtype=float)
    n_stubborn = int(round(frac * n_sheep))
    if n_stubborn <= 0:
        return response
    n_stubborn = min(n_stubborn, n_sheep)
    idx = rng.choice(n_sheep, size=n_stubborn, replace=False)
    response[idx] = scale
    return response


def assign_sheep_cohesion(
    n_sheep: int, config: dict[str, Any]
) -> np.ndarray:
    scale = float(config.get("cohesion_scale", 1.0))
    return np.full(n_sheep, scale, dtype=float)


def init_agent_attributes(
    state: SimulationState, config: dict[str, Any]
) -> SimulationState:
    """Set per-agent arrays on a freshly initialized state."""
    response = assign_sheep_response(state.n_sheep, config, state.rng)
    cohesion = assign_sheep_cohesion(state.n_sheep, config)
    m = state.n_shepherds
    speed = np.full(m, float(config.get("speed_scale", 1.0)), dtype=float)
    sensing = np.full(m, float(config.get("sensing_scale", 1.0)), dtype=float)
    active = np.ones(m, dtype=bool)
    metadata = dict(state.metadata)
    metadata["sheep_response"] = response.tolist()
    return state.copy_with(
        sheep_response=response,
        sheep_cohesion=cohesion,
        shepherd_speed_scale=speed,
        shepherd_sensing_scale=sensing,
        shepherd_active=active,
        metadata=metadata,
    )


def apply_failure_factors(
    state: SimulationState, config: dict[str, Any]
) -> SimulationState:
    """Update active/speed/sensing masks according to failure_mode."""
    mode = str(config.get("failure_mode", "none"))
    fail_tick = int(config.get("failure_tick", -1))
    if mode == "none" or fail_tick < 0 or state.tick < fail_tick:
        return state
    if state.n_shepherds == 0:
        return state

    active = state.shepherd_active.copy()
    speed = state.shepherd_speed_scale.copy()
    sensing = state.shepherd_sensing_scale.copy()
    # Fail the last shepherd by default (deterministic).
    idx = state.n_shepherds - 1
    if mode == "inactive_after_tick":
        active[idx] = False
        speed[idx] = 0.0
    elif mode == "reduced_speed_after_tick":
        speed[idx] = 0.25 * float(config.get("speed_scale", 1.0))
    elif mode == "blind_after_tick":
        sensing[idx] = 0.0
    return state.copy_with(
        shepherd_active=active,
        shepherd_speed_scale=speed,
        shepherd_sensing_scale=sensing,
    )


def apply_environment_updates(
    state: SimulationState, config: dict[str, Any]
) -> SimulationState:
    """Advance moving goals when goal_mode=moving."""
    if str(config.get("goal_mode", "static")) != "moving":
        return state
    if state.world.goal is None:
        return state
    vel = np.asarray(config.get("goal_velocity", [0.0, 0.0]), dtype=float)
    if vel.shape != (2,) or float(np.linalg.norm(vel)) < 1e-12:
        return state
    new_center = state.world.goal.center + vel
    # Keep the full goal disk inside the arena (not only the centre point).
    new_center = clamp_goal_center(
        new_center,
        state.world.goal.radius,
        state.world.width,
        state.world.height,
    )
    world = state.world
    world.goal = GoalZone(center=new_center, radius=world.goal.radius)
    return state


def apply_robot_constraints(
    state: SimulationState,
    desired_velocities: np.ndarray,
    config: dict[str, Any],
    prev_velocities: np.ndarray,
) -> np.ndarray:
    """Clamp dog commands by optional v_max / a_max / omega_max / latency."""
    out = desired_velocities.copy()
    v_max = config.get("v_max")
    a_max = config.get("a_max")
    omega_max = config.get("omega_max")
    latency = int(config.get("latency", 0))

    if latency > 0:
        # Simple delay: blend toward previous command.
        alpha = 1.0 / (1.0 + latency)
        out = alpha * out + (1.0 - alpha) * prev_velocities

    if a_max is not None:
        delta = out - prev_velocities
        norms = np.linalg.norm(delta, axis=1, keepdims=True)
        scale = np.ones_like(norms)
        mask = norms.squeeze() > float(a_max)
        scale[mask] = float(a_max) / np.maximum(norms[mask], 1e-10)
        out = prev_velocities + delta * scale

    if omega_max is not None:
        for i in range(out.shape[0]):
            prev = prev_velocities[i]
            cur = out[i]
            if np.linalg.norm(prev) < 1e-8 or np.linalg.norm(cur) < 1e-8:
                continue
            ang_prev = np.arctan2(prev[1], prev[0])
            ang_cur = np.arctan2(cur[1], cur[0])
            d_ang = (ang_cur - ang_prev + np.pi) % (2 * np.pi) - np.pi
            if abs(d_ang) > float(omega_max):
                ang = ang_prev + np.sign(d_ang) * float(omega_max)
                speed = float(np.linalg.norm(cur))
                out[i] = np.array([np.cos(ang), np.sin(ang)]) * speed

    if v_max is not None:
        norms = np.linalg.norm(out, axis=1, keepdims=True)
        scale = np.ones_like(norms)
        mask = norms.squeeze() > float(v_max)
        scale[mask] = float(v_max) / np.maximum(norms[mask], 1e-10)
        out = out * scale
    return out
