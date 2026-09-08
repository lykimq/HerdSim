# Strombom et al. (2014) -- Implementation Spec

## Paper Reference
- D. Strombom, R. P. Mann, A. M. Wilson, S. Hailes, A. J. Morton, D. J. T. Sumpter, A. J. King
- "Solving the shepherding problem: heuristics for herding autonomous, interacting agents"
- Journal of The Royal Society Interface, 11(100), 20140719, 2014
- DOI: https://doi.org/10.1098/rsif.2014.0719

## Overview
A single shepherd switches between Collect (recover stragglers) and Drive (push a cohesive flock toward a goal). Sheep are reactive agents driven by local attraction to the LCM of their `n` nearest neighbours, neighbour repulsion, shepherd repulsion, inertia, and noise. Beyond detection range they graze.

## Agents

| Type | Count | State |
|------|-------|-------|
| Sheep | N (default 50) | position (x,y), velocity (vx,vy) |
| Shepherd | 1 (paper); UI may set M but logic is single-target | position, velocity |

## Parameters (paper Table 1)

| Symbol | Code key | Default | Meaning |
|--------|----------|---------|---------|
| r_a | `r_a` | 2.0 | Sheep-sheep repulsion distance; also force weight ra |
| r_s | `r_s` | 65.0 | Shepherd detection distance for sheep |
| rs (weight) | `rs_weight` | 1.0 | Relative strength of shepherd repulsion |
| n | `n_neighbors` | -1 | Topological LCM size; -1 means N-1 (global) |
| c | `c` | 1.05 | Attraction weight toward LCM |
| h | `inertia` | 0.5 | Previous-heading weight |
| e | `noise_strength` | 0.3 | Angular noise magnitude |
| d | `sheep_speed` | 1.0 | Sheep step length |
| p | `graze_move_prob` | 0.05 | Probability of moving while grazing |
| ds | `shepherd_speed` | 1.5 | Shepherd step length |
| - | `shepherd_stop_multiple` | 3.0 | Stop when within this * r_a of any sheep |

## Sheep Dynamics
For each sheep i each tick:
1. If distance to shepherd > `r_s`: graze -- stay still, or with probability `p` take a random step of length `d`.
2. Else (threatened):
   - LCM of `n` nearest neighbours (`n_neighbors`; default all other sheep).
   - Attraction `C_hat`: unit vector toward LCM.
   - Neighbour repulsion `R_a` within `r_a` (eq. 4.1: sum of unit vectors
     `(A_i - A_j) / |A_i - A_j|`), then unit `R_a_hat`.
   - Shepherd repulsion unit `R_s_hat` within `r_s`.
   - Noise `e * e_hat`.
   - Heading (eq. 4.2): `H' = h H_hat + c C_hat + ra R_a_hat + rs R_s_hat + e e_hat`.
   - Normalise `H'`, move distance `d` (eq. 4.3).
3. Reflect at world boundaries.

## Shepherd Dynamics
1. Compute flock GCM.
2. If `max_i ||p_i - GCM|| > f(N) = r_a * N^(2/3)` -> Collect, else Drive.
3. Collect target Pc: point behind furthest sheep relative to GCM, offset `r_a`.
4. Drive target Pd: point behind GCM relative to goal, offset `r_a * sqrt(N)`.
5. If within `3 * r_a` of any sheep: speed = 0.
6. Otherwise move toward target at `ds`, with the same angular noise `e` as sheep.

## Switching / Decision Logic
```
if max_distance_to_GCM > r_a * N^(2/3):
    mode = Collect
else:
    mode = Drive
```

## Boundary Conditions
Elastic reflection on world edges (`World.reflect_positions` + `reflect_velocities`).

## Success Condition
Typical scenario `drive_to_goal`: fraction of sheep inside goal circle >= `success_fraction` (default 1.0).

## Implementation Notes
- Code lives in `algorithms/strombom/` (`algorithm.py`, `heuristics.py`, `config.py`).
- Shared helpers: `core/agents/sheep.py` (`compose_strombom_heading`, `compute_local_centroid_knn`).
- Drive uses `state.world.goal.center` when available.
- Multi-shepherd UI values share Collect/Drive logic per dog; the paper defines one shepherd. Use Kubo or `strombom_multi` for coordinated multi-dog herding. `strombom_multi` keeps the paper 3*r_a stop and shepherd noise while assigning distinct Collect/Drive targets.
- Optional overrides: `collect_offset`, `drive_offset`, `ra_weight` (defaults to `r_a`).
- Extension (not in paper): `collect_threshold_scale` may widen f(N) for some scenarios.
