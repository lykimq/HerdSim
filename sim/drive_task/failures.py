"""Drive-task failure labels from a finished trial's metric history.

Progress is ``gcm_goal``. First match in ``PRIORITY`` is the label; all matches
are hints. Lengths scale with goal/flock radius; windows use model seconds.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

NONE = "none"  # the trial succeeded
TIMEOUT = "timeout"  # none of the rules matched

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

# Coverage below this means the dogs are out of the sheep's reach; a working drive has
# coverage 1.0.
LOW_COVERAGE = 0.1
SPLIT_FRACTION = 0.55
SCATTER_FLOCK_RADII = 2.0
SMOOTH_SECONDS = 200.0  # smoothing window of the oscillation rule, in model seconds
MIN_SWINGS = 3


@dataclass(frozen=True)
class Failure:
    mode: str
    hints: tuple[str, ...]  # every rule that matched, the first in PRIORITY is the mode


def smooth_window(dt: float) -> int:
    """Rows in the smoothing window: SMOOTH_SECONDS of model time, one row per tick of ``dt``."""
    return max(1, round(SMOOTH_SECONDS / dt))


def swings(series: np.ndarray, amplitude: float) -> int:
    """Number of direction reversals of ``series`` whose swing exceeds ``amplitude``.

    ``anchor`` is the last turning point, then the furthest value reached in the current
    direction; a move of more than ``amplitude`` back from it turns the direction. The first
    turn only sets the direction, so it is not counted.
    """
    count = 0
    anchor = series[0]
    direction = 0  # 1 rising, -1 falling, 0 not known yet
    for value in series[1:]:
        move = value - anchor
        if direction >= 0 and move < -amplitude:
            if direction > 0:
                count += 1
            direction, anchor = -1, value
        elif direction <= 0 and move > amplitude:
            if direction < 0:
                count += 1
            direction, anchor = 1, value
        elif (direction > 0 and value > anchor) or (direction < 0 and value < anchor):
            anchor = value
    return count


def _oscillates(gcm: np.ndarray, goal_radius: float, config: dict[str, Any]) -> bool:
    """At least MIN_SWINGS swings of a goal radius in the smoothed distance to the goal."""
    window = smooth_window(float(config["dt"]))
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

    matched: list[str] = []
    if late["coverage"].mean() < LOW_COVERAGE and late["lost_sheep"].mean() < 1.0:
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
