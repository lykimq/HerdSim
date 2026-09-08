"""Default parameters for heterogeneous (responsive vs stubborn) sheep herding.

Strombom Collect/Drive base with a fraction of stubborn sheep that feel weaker
shepherd repulsion (scaled rs_weight).
"""

from algorithms.strombom.config import STROMBOM_DEFAULTS

HETEROGENEOUS_DEFAULTS = {
    **STROMBOM_DEFAULTS,
    "n_shepherds": 1,
    # Fraction of sheep assigned stubborn response on first step
    "stubborn_fraction": 0.2,
    # Multiplier on rs_weight for stubborn sheep (in (0, 1])
    "stubborn_rs_scale": 0.25,
}
