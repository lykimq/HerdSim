"""Default parameters for the Flocking Dog 2024 inspired model.

Simplified reciprocal dog-sheep interaction model inspired by:
Fujioka et al., Communications Biology, 2024.
"""

FLOCKING_DOG_DEFAULTS = {
    "n_sheep": 40,
    "n_shepherds": 1,
    # Sheep flocking
    "r_n": 25.0,
    "r_a": 3.0,
    "c": 1.1,
    "alignment_weight": 0.8,
    "sheep_speed": 1.4,
    "inertia": 0.45,
    "noise_strength": 0.2,
    # Reciprocal dog <-> sheep interaction
    "r_s": 40.0,
    "dog_repulsion": 2.2,
    "sheep_attraction_to_dog": 0.15,  # mild front-biased coupling
    "front_bias": 0.35,
    # Dog control
    "shepherd_speed": 2.2,
    "collect_drive_offset": 4.0,
    "drive_gain": 1.0,
    # World
    "world_width": 150.0,
    "world_height": 150.0,
    "goal_center": [15.0, 15.0],
    "goal_radius": 15.0,
    "max_ticks": 3000,
}
