"""Default parameters for the Kubo 2022 force-based herding algorithm.

Mapped from the MATLAB reference implementation
(PatrickHup/Force-Based-Sheep-Herding-Algorithm) and Kubo et al. 2022.

World / layout keys are shared (see core.shared_defaults); this module declares
paper agent counts and Kubo-specific behavior only.
"""

KUBO_DEFAULTS = {
    "n_sheep": 40,
    "n_shepherds": 4,
    # Interaction radius (MATLAB: radius)
    "radius": 60.0,
    # Sheep gains (MATLAB: K_s1..K_s4)
    "K_s1": 10.0,  # sheep-sheep repulsion
    "K_s2": 0.5,  # velocity alignment
    "K_s3": 2.0,  # cohesion
    "K_s4": 5000.0,  # sheep-dog repulsion
    # Dog gains (MATLAB: K_f1..K_f4)
    "K_f1": 10.0,  # attraction to target sheep
    "K_f2": 200.0,  # repulsion from target sheep
    "K_f3": 8.0,  # repulsion from goal
    "K_f4": 3000.0,  # dog-dog repulsion
    # Integration / speed limits
    "dt": 0.05,
    "sheep_speed_max": 5.0,
    "dog_speed_max": 10.0,
    "r_a": 2.0,  # used by generic outlier metric
}
