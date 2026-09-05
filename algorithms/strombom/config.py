"""Default parameters for the Strömbom 2014 herding algorithm.

Reference: Strömbom et al., J. Royal Soc. Interface, 2014.
Parameter names follow the paper's notation.
"""

STROMBOM_DEFAULTS = {
    # Agent counts
    "n_sheep": 50,
    "n_shepherds": 1,
    # Sheep behaviour
    "r_a": 2.0,  # sheep-sheep repulsion distance
    "r_s": 65.0,  # shepherd detection range for sheep
    "r_n": 50.0,  # neighbour radius for local centroid
    "c": 1.05,  # attraction strength toward local centroid
    "noise_strength": 0.3,  # random movement noise (paper e)
    "sheep_speed": 1.5,  # max sheep step size per tick
    "inertia": 0.5,  # weight of previous velocity
    # Shepherd behaviour
    "shepherd_speed": 2.0,  # shepherd step size per tick
    # Paper uses r_a as collect/drive stand-off; kept as explicit override.
    "collect_drive_offset": 2.0,
    # Switching threshold: f(N) = r_a * N^(2/3)
    # Computed dynamically from r_a and n_sheep, not a static param.
    #
    # Extension (not in Strombom 2014): a scenario may supply
    # collect_threshold_scale > 1.0 to widen the threshold, reducing
    # collect interruptions when initial clusters are far from the goal.
    # Default 1.0 reproduces the original paper behaviour.
    "collect_threshold_scale": 1.0,
    # World
    "world_width": 150.0,
    "world_height": 150.0,
    "goal_center": [15.0, 15.0],
    "goal_radius": 15.0,
    "max_ticks": 3000,
}
