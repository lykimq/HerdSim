# Flocking Dog (2024) -- Implementation Spec

## Paper Reference
- V. Jadhav et al.
- Collective responses of flocking sheep (Ovis aries) to a herding dog (border collie)
- Communications Biology, 2024
- DOI: https://doi.org/10.1038/s42003-024-07245-8
- Author MATLAB: https://github.com/tee-lab/collective-responses-of-flocking-sheep-to-herding-dog (`model/herding_model.m`)

## Overview
Sheep combine topological attraction/alignment with short-range repulsion and dog repulsion. Beyond dog range they graze (stationary). The dog uses Collect/Drive positioning (Strombom-style `f(N)`, `pc`, `pd`) and slows to `0.05` when within `r_a` of any sheep.

## Agents

| Type | Count | State |
|------|-------|-------|
| Sheep | N (default 14) | position, velocity |
| Shepherd dog | 1 | position, velocity |

## Parameters (Methods / Fig. 7 / `simulation_hm.m`)

| Symbol | Code key | Default | Meaning |
|--------|----------|---------|---------|
| Ra / rad_rep_s | `r_a` | 2 | Sheep-sheep repulsion distance |
| Rd / rad_rep_dog | `r_s` | 12 | Dog interaction distance |
| k / K_atr | `k_neighbors` | 10 | Nearest neighbours perceived |
| nAtt / k_atr | `n_attraction` | 5 | Random attraction subset size |
| nAli / k_alg | `n_alignment` | 1 | Random alignment subset size |
| alpha / h | `inertia` | 0.5 | Previous-heading weight |
| wRep / rho_a | `sheep_repulsion_weight` | 2.0 | Sheep-sheep repulsion weight |
| wDog / rho_d | `dog_repulsion_weight` | 1.0 | Dog repulsion weight |
| wAtt / c | `attraction_weight` | 1.5 | Attraction weight |
| wAli / alg_str | `alignment_weight` | 1.3 | Alignment weight |
| e | `noise_strength` | 0.5 | Angular noise |
| vS | `sheep_speed` | 1.0 | Sheep step length |
| vDog | `shepherd_speed` | 1.5 | Dog step length |
| - | `shepherd_close_speed` | 0.05 | Dog speed when within `r_a` |

Collect threshold `f(N) = r_a * N^(2/3)`, collect offset `pc = r_a`, drive offset `pd = r_a * sqrt(N)`.

## Sheep Dynamics
1. If dog distance > `r_s`: graze (velocity = 0).
2. Else:
   - Perceive `k` nearest neighbours; sample `nAtt` for attraction, `nAli` of those for alignment.
   - Short-range repulsion within `r_a`.
   - Unit repulsion from dog.
   - Heading: `h H_hat + rho_a Rep + rho_d Dog + c Att + alg Ali + e e_hat`, normalise, step `vS`.

## Shepherd Dynamics
1. If within `r_a` of any sheep: continue previous heading at speed `0.05`.
2. Else if furthest sheep > `f(N)` from GCM: Collect behind that sheep (offset `pc`).
3. Else Drive behind GCM relative to goal (offset `pd`).
4. Add angular noise `e`, move at `vDog`.

## Known Environment Adaptation
- Paper MATLAB drives toward the origin; HerdSim Drive uses `state.world.goal.center`.
- World edge reflection is applied as in other HerdSim algorithms.

## Implementation Notes
- Code: `algorithms/flocking_dog/algorithm.py`, `dynamics.py`, `config.py`
- Reuses `compute_threshold` from Strombom heuristics for `f(N)`.
