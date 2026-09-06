"""Default parameters for the Strombom 2014 herding algorithm.

Reference: Strombom et al., J. Royal Soc. Interface, 2014, Table 1.
Parameter names follow the paper's notation where practical.
"""

STROMBOM_DEFAULTS = {
    # Agent counts
    "n_sheep": 50,
    "n_shepherds": 1,
    # Sheep behaviour (paper Table 1)
    "r_a": 2.0,  # sheep-sheep repulsion distance; also weight ra
    "r_s": 65.0,  # shepherd detection distance
    "rs_weight": 1.0,  # relative strength of shepherd repulsion (paper rs)
    "n_neighbors": -1,  # topological LCM; -1 => N-1 (global case)
    "c": 1.05,  # attraction strength toward LCM of n nearest neighbours
    "noise_strength": 0.3,  # angular noise e
    "sheep_speed": 1.0,  # agent displacement d per time step
    "inertia": 0.5,  # previous-heading weight h
    "graze_move_prob": 0.05,  # p: move while grazing when dog beyond r_s
    # Shepherd behaviour
    "shepherd_speed": 1.5,  # shepherd displacement ds per time step
    "shepherd_stop_multiple": 3.0,  # stop when within this * r_a of any sheep
    # Switching threshold: f(N) = r_a * N^(2/3)
    # Extension (not in Strombom 2014): scenarios may supply
    # collect_threshold_scale > 1.0 to widen the threshold.
    "collect_threshold_scale": 1.0,
    # World
    "world_width": 150.0,
    "world_height": 150.0,
    "goal_center": [15.0, 15.0],
    "goal_radius": 15.0,
    "max_ticks": 3000,
}
