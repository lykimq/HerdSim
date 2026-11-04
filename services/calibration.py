"""Flock radius R_f(N) per method: the size of a flock while one dog drives it.

The goal radius, compact spread and lost-sheep radius are multiples of R_f. One dog drives
a compact flock toward a goal it cannot reach for ``calibration_seconds``; R_f = sqrt(2) x
RMS radius over the last window, median over seeds and start sizes. One dog is used for
every team size, so all are compared on a task sized to the same reference flock.

``calibrate`` raises where the radius is not settled or depends on the start size; with the
canonical tolerances and 3 seeds per start it holds for Strombom sheep at every tested size up
to N = 600 and fails at every tested size from 630 (results/diagnostics/).
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np

from sim.trial import build_config, run_trial
from sim.vectors import FLOCK_RADIUS_FACTOR

from .cells import method_spec, setup_for
from .pool import worker_pool
from .protocol import Protocol, method_dt, sheep_speed_per_second

# The calibration goal lies this many times farther than the sheep could travel at their
# top speed during the whole run, so no flock reaches it: a flock that reaches the goal is
# measured turning at it, not being driven.
DRIVE_SPEED_MARGIN = 1.5
# measure() raises when the flock centre comes closer to the goal than this many measured
# radii inside the measured windows, for the same reason.
GOAL_CLEARANCE_RADII = 2.0


class CalibrationError(RuntimeError):
    """A flock size has no settled radius that is independent of the start."""


def start_radius(spacing: float, n_sheep: int) -> float:
    """Radius of the calibration start flock: spacing x sqrt(N / pi)."""
    return spacing * math.sqrt(n_sheep / math.pi)


def calibration_drive(protocol: Protocol, method: str) -> float:
    """Length of the calibration drive: DRIVE_SPEED_MARGIN x top sheep speed x seconds."""
    params = method_spec(protocol, method).params
    seconds = protocol.settings["calibration_seconds"]
    return DRIVE_SPEED_MARGIN * sheep_speed_per_second(params) * seconds


def calibration_config(
    protocol: Protocol, method: str, n_sheep: int, spacing: float
) -> dict[str, Any]:
    """One dog, a compact start of ``spacing``, a goal of radius 0 too far to reach.

    The drive is set through both drive terms so the task's max() rule returns exactly
    ``calibration_drive``.
    """
    spec = method_spec(protocol, method)
    s = protocol.settings
    radius = start_radius(spacing, n_sheep)
    drive = calibration_drive(protocol, method)
    far = {
        **s,
        "drive_distance_multiple": drive / radius,
        "drive_distance_min": drive,
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
    setup["max_ticks"] = math.ceil(s["calibration_seconds"] / method_dt(spec.params))
    return build_config(
        method=method,
        params=dict(spec.params),
        setup=setup,
        n_sheep=n_sheep,
        n_shepherds=1,
        initial_layout="compact",
    )


def measure(job: tuple[dict[str, Any], int, int]) -> tuple[float, float]:
    """(R_f over the last window, R_f over the window before) from one calibration trial.

    Raises CalibrationError when the flock centre came within GOAL_CLEARANCE_RADII x the
    measured radius of the goal during either window: the run then measured a flock at the
    goal, not a driven one.
    """
    config, seed, window = job
    history = run_trial(config, seed).history
    extent = history["extent"].to_numpy()
    late = FLOCK_RADIUS_FACTOR * extent[-window:].mean()
    early = FLOCK_RADIUS_FACTOR * extent[-2 * window : -window].mean()
    closest = float(history["gcm_goal"].to_numpy()[-2 * window :].min())
    if closest < GOAL_CLEARANCE_RADII * late:
        who = f"{config['method']} N={config['n_sheep']} seed {seed}"
        how = f"came within {closest:.1f} of the goal (R_f {late:.1f})"
        raise CalibrationError(f"{who}: the flock centre {how} during the measured windows")
    return float(late), float(early)


def settle(runs: list[tuple[float, tuple[float, float]]]) -> tuple[float, float, float]:
    """(R_f, drift, spread) from the runs of one flock size: (start spacing, (late, early)).

    R_f is the median of the late windows; drift the change between the two windows' medians;
    spread the range of the per-start medians, both relative.
    """
    starts = sorted({spacing for spacing, _ in runs})
    late = float(np.median([v[0] for _, v in runs]))
    early = float(np.median([v[1] for _, v in runs]))
    by_start = [float(np.median([v[0] for sp, v in runs if sp == x])) for x in starts]
    drift = abs(late - early) / early if early > 0.0 else 0.0
    spread = (max(by_start) - min(by_start)) / late if late > 0.0 else 0.0
    return late, drift, spread


def summarise(
    label: str, runs: list[tuple[float, tuple[float, float]]], settings: dict[str, Any]
) -> tuple[float, list[str]]:
    """(R_f, problems) from the runs of one flock size: (start spacing, (late, early)) each.

    A problem is a drift above ``settled_tolerance`` or a spread above ``start_agreement``.
    """
    late, drift, spread = settle(runs)
    problems = []
    if drift > settings["settled_tolerance"]:
        problems.append(f"{label}: radius still changing ({drift:.0%} between windows)")
    if spread > settings["start_agreement"]:
        problems.append(f"{label}: radius depends on the start size ({spread:.0%})")
    return late, problems


def measure_sizes(
    protocol: Protocol, sizes: list[tuple[str, int]], workers: int
) -> dict[tuple[str, int], list[tuple[float, tuple[float, float]]]]:
    """Every start spacing and seed of every (method, N) in ``sizes``, measured in parallel.

    The result maps each (method, N) to its (start spacing, (late, early)) runs.
    """
    s = protocol.settings
    seeds = [s["master_seed"] + i for i in range(s["calibration_seeds"])]
    owners: list[tuple[str, int, float]] = []
    jobs = []
    for method, n in sizes:
        window = round(
            s["calibration_window_seconds"] / method_dt(method_spec(protocol, method).params)
        )
        for spacing in s["calibration_starts"]:
            config = calibration_config(protocol, method, n, spacing)
            for seed in seeds:
                owners.append((method, n, spacing))
                jobs.append((config, seed, window))
    with worker_pool(workers) as pool:
        values = list(pool.map(measure, jobs))
    runs: dict[tuple[str, int], list[tuple[float, tuple[float, float]]]] = {}
    for (method, n, spacing), value in zip(owners, values, strict=True):
        runs.setdefault((method, n), []).append((spacing, value))
    return runs


def calibrate(
    protocol: Protocol, workers: int, existing: dict[str, dict[int, float]] | None = None
) -> dict[str, dict[int, float]]:
    """R_f for every method and flock size; raises where a size is not settled.

    Sizes already in ``existing`` are kept as they are; only the missing ones are measured.
    """
    table = {method: dict(radii) for method, radii in (existing or {}).items()}
    missing = [
        (m.name, n)
        for m in protocol.methods
        for n in sorted(protocol.flock_sizes)
        if n not in table.get(m.name, {})
    ]
    if not missing:
        return table
    runs = measure_sizes(protocol, missing, workers)
    failures: list[str] = []
    for method, n in missing:
        radius, problems = summarise(f"{method} N={n}", runs[method, n], protocol.settings)
        table.setdefault(method, {})[n] = radius
        failures += problems
    if failures:
        raise CalibrationError("; ".join(failures))
    return table
