"""Flock radius R_f(N) per method: the size of a flock while one dog drives it.

The goal radius, the compact spread and the lost-sheep radius are multiples of
R_f, so they follow the real flock instead of an assumed packing. One dog drives
a compact flock toward a goal it cannot reach, for ``calibration_seconds``
(ticks x dt, so slow-clock methods run as long); R_f = sqrt(2) x RMS radius (the
radius of a uniform disk with that RMS), averaged over the last window, median
over seeds and start sizes.

R_f is the size of the flock driven by one dog: calibration always uses a single dog and no
factor, whatever the protocol sweeps, so every factor level of a method is compared on a
task sized to that one reference flock. A method with ``calibrate_as`` is calibrated with
the single dog of the named method (FAT with the paper shepherd of strombom_multi), so the
two methods are compared on the same task rather than each on its own flock size.

Calibration always runs the drive task (``CALIBRATION_TASK``), whatever task
the protocol runs: R_f is a property of the sheep model under a driving dog,
and any task sizes itself from it. It runs in its own field, sized for a
compact start, one dog and its long drive.

R_f is only a property of the model where the flock settles to one size whatever
size it starts from. ``calibrate`` checks both conditions and raises where they fail. For
Strombom sheep they hold up to N = 600 (measured 2026-10-23); from about 630 a loose start
keeps part of its size, and from 800 the check fails.

Above that edge a protocol may impose the radius instead (``impose_radius_above`` = N_cal):
N_cal is calibrated as usual, and every flock size above it gets
R_f(N) = imposed_radius_scale x R_f(N_cal) x sqrt(N / N_cal), the density of the N_cal flock
held constant (scaled for a sweep). Those sizes are not calibrated, since a calibration there
would average two start-dependent sizes. Results at them are results at that imposed density.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np

from sim.core.config.experiment import build_config
from sim.core.simulation_runner import run_trial

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
    """Length of the calibration drive: DRIVE_SPEED_MARGIN x top sheep speed x seconds."""
    params = method_spec(protocol, method).params
    seconds = float(protocol.settings["calibration_seconds"])
    return DRIVE_SPEED_MARGIN * sheep_speed_per_second(method, params) * seconds


def calibration_config(
    protocol: Protocol, method: str, n_sheep: int, spacing: float
) -> dict[str, Any]:
    """One global dog, a compact start of ``spacing``, a goal of radius 0 too far to reach.

    The protocol's factors are not applied; the drive is set in units through
    both drive terms so the task's max() rule returns exactly ``calibration_drive``.
    With ``calibrate_as`` the dog of that method drives, on this method's parameters
    (``_methods`` allows it only between methods with the same sheep and parameter names).
    """
    spec = method_spec(protocol, method)
    driver = spec.calibrate_as or method
    s = protocol.settings
    radius = start_radius(spacing, n_sheep)
    drive = calibration_drive(protocol, method)
    far = {
        **s,
        # R_f is the flock driven by the paper's one dog, which sees every sheep: the settings of
        # the team rule and the task that a protocol changes are set back for calibration.
        **PAPER_DOG,
        "task": CALIBRATION_TASK,
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
    setup["max_ticks"] = math.ceil(float(s["calibration_seconds"]) / method_dt(method, spec.params))
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
    """(R_f over the last window, R_f over the window before) from one calibration trial.

    Raises CalibrationError when the flock centre came within
    GOAL_CLEARANCE_RADII x the measured radius of the goal during either window:
    the run then measured a flock at the goal, not a driven one.
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
    """(R_f, problems) from the runs of one flock size: (start spacing, (late, early)) each."""
    starts = sorted({spacing for spacing, _ in runs})
    late = float(np.median([v[0] for _, v in runs]))
    early = float(np.median([v[1] for _, v in runs]))
    by_start = [float(np.median([v[0] for sp, v in runs if sp == x])) for x in starts]
    drift = abs(late - early) / early
    spread = (max(by_start) - min(by_start)) / late
    problems = []
    if drift > float(settings["settled_tolerance"]):
        problems.append(f"{label}: radius still changing ({drift:.0%} between windows)")
    if spread > float(settings["start_agreement"]):
        problems.append(f"{label}: radius depends on the start size ({spread:.0%})")
    return late, problems


def calibrate(protocol: Protocol, workers: int) -> dict[str, dict[int, float]]:
    """R_f for every method and flock size; raises where a calibrated size is not settled.

    With ``impose_radius_above`` the sizes above it are imposed from N_cal (module docstring),
    and the table also holds N_cal itself, the size they are imposed from.
    """
    s = protocol.settings
    seeds = [int(s["master_seed"]) + i for i in range(int(s["calibration_seeds"]))]
    starts = [float(x) for x in s["calibration_starts"]]
    above = int(s["impose_radius_above"])
    measured = sorted(
        {n for n in protocol.flock_sizes if not above or n <= above} | ({above} if above else set())
    )
    keys = [(m.name, n) for m in protocol.methods for n in measured]
    jobs, owners = [], []
    for method, n in keys:
        window = round(
            float(s["calibration_window_seconds"])
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
        scale = float(s["imposed_radius_scale"])
        for radii in table.values():
            for n in (n for n in protocol.flock_sizes if n > above):
                radii[n] = scale * radii[above] * math.sqrt(n / above)
    return table
