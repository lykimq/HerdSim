"""Why a failed drive trial failed, read from its metric history after the run.

These are the drive task's rules (``Scenario.classify_failure``): progress is the flock
centre's distance to the goal (``gcm_goal``). Most rules look at the second half of the
trial (the late window); FLOCK_ESCAPED compares that window with the start, OSCILLATION and
STUCK compare the two halves. Lengths are relative to the trial's own goal radius and flock
radius, and time windows are in model seconds (converted with the method's dt), so the
labels mean the same thing at every N, D and method. When several rules match, the first
in ``PRIORITY`` is the label; all matches are kept as hints.

``classify_failure_regime`` is a coarser, two-way reading used by analysis/dispersion_burden.py:
did the flock get near the goal at all.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from .failures import NONE, TIMEOUT, Failure

DOGS_OUT_OF_RANGE = "dogs_out_of_range"  # dogs too far for the sheep to react
FLOCK_ESCAPED = "flock_escaped"  # flock ended farther from the goal than it started
SPLIT = "split"  # flock broke into groups
SCATTER = "scatter"  # flock stayed spread out
OSCILLATION = "oscillation"  # flock swung toward and away from the goal
STUCK = "stuck"  # flock barely moved relative to the goal

PRIORITY = (
    DOGS_OUT_OF_RANGE,
    FLOCK_ESCAPED,
    SPLIT,
    SCATTER,
    OSCILLATION,
    STUCK,
)

# Coverage below this means the dogs are out of the sheep's reach. 0.1 suits Strombom,
# where a working drive has coverage 1.0. A working Kubo drive sits at 0.1 to 0.2 (the
# sheep hold the dogs at the edge of their view), so Kubo sets its own value with the
# config key low_coverage, and for it the label is a weak hint.
LOW_COVERAGE = 0.1
SPLIT_FRACTION = 0.55
SCATTER_FLOCK_RADII = 2.0
SMOOTH_SECONDS = 200.0  # smoothing window of the oscillation rule, in model seconds
MIN_SWINGS = 3

# Regimes of classify_failure_regime: a flock that ended within this many goal radii of the
# goal centre got there and lost on time or stragglers; one farther away never arrived.
NEAR_GOAL_RADII = 2.0
STRUCTURAL_GATHER = "structural_gather"
BOUNDARY_TEMPORAL = "boundary_temporal"


def smooth_window(dt: float, stride: int = 1) -> int:
    """Rows in the smoothing window: SMOOTH_SECONDS of model time, one row per ``stride``
    ticks of ``dt``."""
    return max(1, round(SMOOTH_SECONDS / (dt * stride)))


def swings(series: np.ndarray, amplitude: float) -> int:
    """Number of direction reversals of ``series`` whose swing exceeds ``amplitude``."""
    count = 0
    anchor = series[0]
    direction = 0
    for value in series[1:]:
        move = value - anchor
        if direction >= 0 and move < -amplitude:
            count += direction > 0
            direction, anchor = -1, value
        elif direction <= 0 and move > amplitude:
            count += direction < 0
            direction, anchor = 1, value
        elif (direction > 0 and value > anchor) or (direction < 0 and value < anchor):
            anchor = value
    return count


def _oscillates(gcm: np.ndarray, goal_radius: float, config: dict[str, Any]) -> bool:
    """At least MIN_SWINGS swings of a goal radius in the smoothed distance to the goal."""
    window = smooth_window(float(config["dt"]), int(config["metrics_stride"]))
    smooth = pd.Series(gcm).rolling(window, min_periods=1).mean().to_numpy()
    return swings(smooth, goal_radius) >= MIN_SWINGS


def classify_failure(history: pd.DataFrame, *, success: bool, config: dict[str, Any]) -> Failure:
    if success:
        return Failure(NONE, ())
    goal_radius = float(config["goal_radius"])
    half = len(history) // 2
    early, late = history.iloc[:half], history.iloc[half:]
    gcm = history["gcm_goal"].to_numpy(dtype=float)
    progress = float(early["gcm_goal"].mean() - late["gcm_goal"].mean())
    low_coverage = float(config.get("low_coverage", LOW_COVERAGE))

    matched: list[str] = []
    if late["coverage"].mean() < low_coverage and late["lost_sheep"].mean() < 1.0:
        matched.append(DOGS_OUT_OF_RANGE)
    if late["gcm_goal"].mean() > gcm[0]:
        matched.append(FLOCK_ESCAPED)
    if late["fragmentation"].mean() < SPLIT_FRACTION:
        matched.append(SPLIT)
    if late["extent"].mean() > SCATTER_FLOCK_RADII * float(config["flock_radius"]):
        matched.append(SCATTER)
    if abs(progress) < goal_radius:
        if _oscillates(gcm, goal_radius, config):
            matched.append(OSCILLATION)
        matched.append(STUCK)

    mode = next((label for label in PRIORITY if label in matched), TIMEOUT)
    return Failure(mode, tuple(matched))


def classify_failure_regime(history: pd.DataFrame, *, success: bool, config: dict[str, Any]) -> str:
    """BOUNDARY_TEMPORAL when the flock ended within NEAR_GOAL_RADII goal radii of the goal
    centre (more time or a looser share might have rescued it), STRUCTURAL_GATHER when it
    ended farther away (it was never gathered and driven there); "none" for a success."""
    if success or history.empty:
        return "none"
    final = float(history["gcm_goal"].iloc[-1])
    near = final <= NEAR_GOAL_RADII * float(config["goal_radius"])
    return BOUNDARY_TEMPORAL if near else STRUCTURAL_GATHER
