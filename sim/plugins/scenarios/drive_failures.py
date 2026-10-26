"""Drive failure classification based on trial metric history.

Evaluates late-window metrics relative to goal and flock geometry. When multiple
failure conditions trigger, the first in `PRIORITY` is assigned as the primary mode,
while all matching conditions are preserved in `Failure.hints`.
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

# Coverage threshold below which dogs are considered disconnected from the flock.
# Kubo overrides this via `low_coverage` because its stronger flee force keeps dogs further.
LOW_COVERAGE = 0.1
SPLIT_FRACTION = 0.55
SCATTER_FLOCK_RADII = 2.0
# Rolling window duration (in simulation seconds) for trajectory oscillation detection.
SMOOTH_SECONDS = 200.0
MIN_SWINGS = 3


def smooth_window(dt: float, stride: int = 1) -> int:
    """Number of history rows corresponding to SMOOTH_SECONDS given dt and metrics stride."""
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
        pd.Series(gcm)
        .rolling(smooth_window(float(config["dt"]), int(config["metrics_stride"])), min_periods=1)
        .mean()
        .to_numpy()
    )
    if swings(smooth, goal_radius) >= MIN_SWINGS and abs(progress) < goal_radius:
        matched.append(OSCILLATION)
    if abs(progress) < goal_radius:
        matched.append(STUCK)

    mode = next((label for label in PRIORITY if label in matched), TIMEOUT)
    return Failure(mode, tuple(matched))


STRUCTURAL_GATHER = "structural_gather"
BOUNDARY_TEMPORAL = "boundary_temporal"


def classify_failure_regime(
    history: pd.DataFrame, *, success: bool, config: dict[str, Any]
) -> str:
    """Classifies a failed trial into Structural Gathering vs Boundary/Temporal failure.

    - Structural Gather: The flock stalled during collection or early transit, ending far
      from the goal (> 2x goal_radius). Extending the deadline cannot rescue the trial.
    - Boundary/Temporal: The flock reached the goal vicinity (<= 2x goal_radius) with the
      majority contained, failing due to deadline expiry or marginal stragglers.
    """
    if success or history.empty:
        return "none"
    goal_radius = float(config.get("goal_radius", 10.0))
    final_dist = float(history["gcm_goal"].iloc[-1])
    return BOUNDARY_TEMPORAL if final_dist <= 2.0 * goal_radius else STRUCTURAL_GATHER

