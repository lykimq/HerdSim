"""Default parameters for obstacle-aware Collect/Drive herding.

Strombom sheep and Collect/Drive switch; Drive stand-off is deflected around
blocking obstacles or toward a narrow-gate gap when present.
"""

from algorithms.strombom.config import STROMBOM_DEFAULTS

OBSTACLE_AWARE_DEFAULTS = {
    **STROMBOM_DEFAULTS,
    "n_shepherds": 1,
    # Extra clearance beyond obstacle half-extent when offsetting Pd
    "obstacle_clearance": 5.0,
}
