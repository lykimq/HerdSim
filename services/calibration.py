"""Flock radius calibration R_f(N).

Empirically measures the steady-state flock radius R_f while driven by a single dog.
Task geometry (goal radius, field dimensions, lost-sheep radius) is scaled from R_f
so that models with different natural packing densities are compared fairly.

Runs a single dog driving a flock toward an unreachable goal, computing R_f as
sqrt(2) * RMS radius over the final window. Checks that compact and loose initializations
converge to the same radius before accepting the result.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np

from sim.core.config.experiment import build_config
from sim.core.simulation_runner import run_trial
from sim.plugins.scenarios import SCENARIOS

from .cells import method_spec, setup_for
from .pool import worker_pool
from .protocol import Protocol, method_dt, sheep_speed_per_second

CALIBRATION_TASK = "drive_to_goal"

# Settings that change the dogs or the end of the task, at the values of the paper's dog.
PAPER_DOG = {
    "sensing_range": 0.0,
    "communication": "none",
    "dog_spacing": 0.0,
    "hold_drive_multiple": 0.0,
    "hold_withdraw": False,
    "drive_offset_cap": 0.0,
}

# The calibration goal lies this many times farther than the sheep could travel at
# their top speed during the whole run, so no flock reaches it (HerdSim choice: a flock
# that reaches the goal is measured turning at it, not being driven).
DRIVE_SPEED_MARGIN = 1.5
# measure() raises when the flock centre comes closer to the goal than this many
# measured radii inside the measured windows (HerdSim choice: a flock within two of its
# own radii of the goal is being turned at it, not driven).
GOAL_CLEARANCE_RADII = 2.0


class CalibrationError(RuntimeError):
    """A flock size has no settled radius that is independent of the start."""


def start_radius(spacing: float, n_sheep: int) -> float:
    """Radius of the calibration start flock: spacing x sqrt(N / pi)."""
    return spacing * math.sqrt(n_sheep / math.pi)


def calibration_drive(protocol: Protocol, method: str) -> float:
    """Distance to calibration goal, placed far enough that the flock never reaches it."""
    params = method_spec(protocol, method).params
    seconds = protocol.settings["calibration_seconds"]
    return DRIVE_SPEED_MARGIN * sheep_speed_per_second(method, params) * seconds


def calibration_config(
    protocol: Protocol, method: str, n_sheep: int, spacing: float
) -> dict[str, Any]:
    """Build a calibration trial config with one dog and an unreachable goal."""
    spec = method_spec(protocol, method)
    driver = spec.calibrate_as or method
    s = protocol.settings
    radius = start_radius(spacing, n_sheep)
    drive = calibration_drive(protocol, method)
    far = {
        **s,
        **PAPER_DOG,
        "task": CALIBRATION_TASK,
        "drive_distance_multiple": drive / radius,
        "drive_distance_min": drive,
        "metrics_stride": 1,
    }
    setup = setup_for(
        far,
        spec,
        flock_radius=radius,
        n_sheep=n_sheep,
        layouts=("compact",),
        max_dogs=1,
    )
    setup["goal_radius"] = 0.0
    setup["max_ticks"] = math.ceil(s["calibration_seconds"] / method_dt(method, spec.params))
    return build_config(
        task=CALIBRATION_TASK,
        method=driver,
        params=dict(spec.params),
        setup=setup,
        n_sheep=n_sheep,
        n_shepherds=1,
        initial_layout="compact",
    )


def measure(job: tuple[dict[str, Any], int, int]) -> tuple[float, float]:
    """Measure late and early steady-state R_f windows from one trial.

    Raises CalibrationError if the flock came too close to the goal disc, which
    invalidates the assumption of an unreached steady drive.
    """
    config, seed, window = job
    history = run_trial(config, seed).history
    extent = history["extent"].to_numpy()
    late = math.sqrt(2.0) * extent[-window:].mean()
    early = math.sqrt(2.0) * extent[-2 * window : -window].mean()
    closest = float(history["gcm_goal"].to_numpy()[-2 * window :].min())
    if closest < GOAL_CLEARANCE_RADII * late:
        who = f"{config['method']} N={config['n_sheep']} seed {seed}"
        how = f"came within {closest:.1f} of the goal (R_f {late:.1f})"
        raise CalibrationError(f"{who}: the flock centre {how} during the measured windows")
    return float(late), float(early)


def summarise(
    label: str, runs: list[tuple[float, tuple[float, float]]], settings: dict[str, Any]
) -> tuple[float, list[str]]:
    """Compute median R_f across runs and check settlement and start-agreement tolerances."""
    starts = sorted({spacing for spacing, _ in runs})
    late = float(np.median([v[0] for _, v in runs]))
    early = float(np.median([v[1] for _, v in runs]))
    by_start = [float(np.median([v[0] for sp, v in runs if sp == x])) for x in starts]
    drift = abs(late - early) / early
    spread = (max(by_start) - min(by_start)) / late
    problems = []
    if drift > settings["settled_tolerance"]:
        problems.append(f"{label}: radius still changing ({drift:.0%} between windows)")
    if spread > settings["start_agreement"]:
        problems.append(f"{label}: radius depends on the start size ({spread:.0%})")
    return late, problems


def calibrate(protocol: Protocol, workers: int) -> dict[str, dict[int, float]]:
    """R_f for every method and flock size; raises where a calibrated size is not settled.

    With ``impose_radius_above`` the sizes above it are imposed from N_cal (module docstring),
    and the table also holds N_cal itself, the size they are imposed from. A protocol whose
    task sizes itself (``Scenario.calibrates`` false) has nothing to calibrate and is refused.
    """
    s = protocol.settings
    task = s["task"]
    if not SCENARIOS[task].calibrates:
        raise ValueError(f"task {task!r} sizes itself from its own settings; no R_f to calibrate")
    seeds = [s["master_seed"] + i for i in range(s["calibration_seeds"])]
    starts = list(s["calibration_starts"])
    above = s["impose_radius_above"]
    measured = sorted(
        {n for n in protocol.flock_sizes if not above or n <= above} | ({above} if above else set())
    )
    keys = [(m.name, n) for m in protocol.methods for n in measured]
    jobs, owners = [], []
    for method, n in keys:
        window = round(
            s["calibration_window_seconds"]
            / method_dt(method, method_spec(protocol, method).params)
        )
        for spacing in starts:
            config = calibration_config(protocol, method, n, spacing)
            for seed in seeds:
                jobs.append((config, seed, window))
                owners.append((method, n, spacing))
    with worker_pool(workers) as pool:
        values = list(pool.map(measure, jobs))

    table: dict[str, dict[int, float]] = {}
    failures: list[str] = []
    for method, n in keys:
        mine = [(o[2], v) for o, v in zip(owners, values) if o[:2] == (method, n)]
        radius, problems = summarise(f"{method} N={n}", mine, s)
        table.setdefault(method, {})[n] = radius
        failures += problems
    if failures:
        raise CalibrationError("; ".join(failures))
    if above:
        scale = s["imposed_radius_scale"]
        for radii in table.values():
            for n in (n for n in protocol.flock_sizes if n > above):
                radii[n] = scale * radii[above] * math.sqrt(n / above)
    return table
