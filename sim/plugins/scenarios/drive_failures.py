"""Why a failed drive trial failed, read from its metric history after the run.

These are the drive task's rules (``Scenario.classify_failure``): progress is
the flock centre's distance to the goal (``gcm_goal``). A task with other
stages brings its own rules and may reuse the flock and dog ones here.

Most rules look at the second half of the trial (the late window); FLOCK_ESCAPED
compares that window with the start, and OSCILLATION and STUCK compare the two
halves. Lengths are relative to the trial's own goal radius and flock radius, and
time windows are in model seconds (converted with the method's dt), so the
labels mean the same thing at every N, D and method. When several rules match, the
first in ``PRIORITY`` is the label; all matches are kept as hints.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

NONE = "none"
DOGS_OUT_OF_RANGE = "dogs_out_of_range"  # dogs too far for the sheep to react
FLOCK_ESCAPED = "flock_escaped"  # flock ended farther from the goal than it started
SPLIT = "split"  # flock broke into groups
SCATTER = "scatter"  # flock stayed spread out
OSCILLATION = "oscillation"  # flock swung toward and away from the goal
STUCK = "stuck"  # flock barely moved relative to the goal
TIMEOUT = "timeout"  # none of the above

PRIORITY = (
    DOGS_OUT_OF_RANGE,
    FLOCK_ESCAPED,
    SPLIT,
    SCATTER,
    OSCILLATION,
    STUCK,
)

# Rule thresholds.
# Coverage below this means the dogs are out of the sheep's reach. 0.1 suits Strombom,
# where a working drive has coverage 1.0 (measured, N = 100, four layouts). A working
# Kubo drive sits at 0.1-0.2 (measured, N = 25-100): the flee term K_s4 / d^2 is 12.5 at
# d = 20, above the sheep speed cap 5, so sheep keep the dogs at the edge of the 20-unit
# view. Kubo therefore sets its own value (config key low_coverage), and for it the
# dogs_out_of_range label is a weak hint.
LOW_COVERAGE = 0.1
SPLIT_FRACTION = 0.55
SCATTER_FLOCK_RADII = 2.0
SMOOTH_SECONDS = 200.0  # HerdSim choice; 200 Strombom ticks, 4000 Kubo ticks
MIN_SWINGS = 3


@dataclass(frozen=True)
class Failure:
    mode: str
    hints: tuple[str, ...]


def smooth_window(dt: float) -> int:
    """Ticks in the smoothing window of the oscillation rule: SMOOTH_SECONDS of model time."""
    return max(1, round(SMOOTH_SECONDS / dt))


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


def classify_failure(history: pd.DataFrame, *, success: bool, config: dict[str, Any]) -> Failure:
    if success:
        return Failure(NONE, ())
    goal_radius = float(config["goal_radius"])
    late = history.iloc[len(history) // 2 :]
    early = history.iloc[: len(history) // 2]
    gcm = history["gcm_goal"].to_numpy(dtype=float)
    progress = float(early["gcm_goal"].mean() - late["gcm_goal"].mean())

    matched: list[str] = []
    low_coverage = float(config.get("low_coverage", LOW_COVERAGE))
    if late["coverage"].mean() < low_coverage and late["lost_sheep"].mean() < 1.0:
        matched.append(DOGS_OUT_OF_RANGE)
    if late["gcm_goal"].mean() > gcm[0]:
        matched.append(FLOCK_ESCAPED)
    if late["fragmentation"].mean() < SPLIT_FRACTION:
        matched.append(SPLIT)
    if late["extent"].mean() > SCATTER_FLOCK_RADII * float(config["flock_radius"]):
        matched.append(SCATTER)
    smooth = (
        pd.Series(gcm).rolling(smooth_window(float(config["dt"])), min_periods=1).mean().to_numpy()
    )
    if swings(smooth, goal_radius) >= MIN_SWINGS and abs(progress) < goal_radius:
        matched.append(OSCILLATION)
    if abs(progress) < goal_radius:
        matched.append(STUCK)

    mode = next((label for label in PRIORITY if label in matched), TIMEOUT)
    return Failure(mode, tuple(matched))
