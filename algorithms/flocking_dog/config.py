"""Default parameters for the Flocking Dog 2024 herding model.

Mapped from Jadhav et al., Communications Biology 2024 (Methods / Fig. 7)
and the authors' reference MATLAB `model/herding_model.m` + `simulation_hm.m`.

World / layout keys are shared (see core.shared_defaults); this module declares
paper agent counts and Flocking Dog-specific behavior only.
"""

FLOCKING_DOG_DEFAULTS = {
    "n_sheep": 14,
    "n_shepherds": 1,
    # Sheep social / dog interaction radii
    "r_a": 2.0,  # rad_rep_s / Ra: sheep-sheep repulsion distance
    "r_s": 12.0,  # rad_rep_dog / Rd: dog interaction distance
    # Topological neighbourhood (paper: k, nAtt, nAli)
    "k_neighbors": 10,  # K_atr: nearest neighbours perceived
    "n_attraction": 5,  # nAtt / k_atr: random attraction subset
    "n_alignment": 1,  # nAli / k_alg: random alignment subset
    # Force weights
    "inertia": 0.5,  # h / alpha
    "sheep_repulsion_weight": 2.0,  # rho_a / wRep
    "dog_repulsion_weight": 1.0,  # rho_d / wDog
    "attraction_weight": 1.5,  # c / wAtt
    "alignment_weight": 1.3,  # alg_str / wAli
    "noise_strength": 0.5,  # e
    # Speeds
    "sheep_speed": 1.0,  # vS
    "shepherd_speed": 1.5,  # vDog
    "shepherd_close_speed": 0.05,  # slow when within r_a of any sheep
    # Collect/Drive (paper uses Strombom-style f(N), pd, pc)
    # f(N) = r_a * N^(2/3); pd = r_a * sqrt(N); pc = r_a
    "collect_threshold_scale": 1.0,
}
