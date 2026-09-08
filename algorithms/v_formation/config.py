"""Default parameters for Fujioka/Hayashi-style V-formation herding.

Sheep dynamics follow Strombom 2014 defaults. Shepherd drive targets lie on a
V-shaped arc behind the flock GCM relative to the goal; Collect falls back to
Strombom multi-dog outlier assignment when the flock is dispersed.
"""

from algorithms.strombom.config import STROMBOM_DEFAULTS

V_FORMATION_DEFAULTS = {
    **STROMBOM_DEFAULTS,
    "n_shepherds": 2,
    # Angle between adjacent V-arc slots (degrees)
    "v_angle_deg": 35.0,
    # Optional override: when omitted, arc radius is r_a * sqrt(N)
}
