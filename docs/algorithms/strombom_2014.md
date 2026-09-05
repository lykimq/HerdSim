# Strombom et al. (2014) -- Implementation Spec

## Paper Reference
- D. Strombom, R. P. Mann, A. M. Wilson, S. Hailes, A. J. Morton, D. J. T. Sumpter, A. J. King
- "Solving the shepherding problem: heuristics for herding autonomous, interacting agents"
- Journal of The Royal Society Interface, 11(100), 20140719, 2014
- DOI: https://doi.org/10.1098/rsif.2014.0719

## Overview
A single shepherd switches between Collect (recover stragglers) and Drive (push a cohesive flock toward a goal). Sheep are reactive agents driven by local attraction, neighbour repulsion, shepherd repulsion, inertia, and noise.

## Agents

| Type | Count | State |
|------|-------|-------|
| Sheep | N (default 50) | position (x,y), velocity (vx,vy) |
| Shepherd | 1 (paper); UI may set M but logic is single-target | position, velocity |

## Parameters

| Symbol | Code key | Default | Meaning |
|--------|----------|---------|---------|
| r_a | `r_a` | 2.0 | Sheep-sheep repulsion radius; also Collect/Drive stand-off |
| r_s | `r_s` | 65.0 | Shepherd threat radius for sheep |
| r_n | `r_n` | 50.0 | Neighbourhood radius for local centre of mass |
| c | `c` | 1.05 | Attraction weight toward LCM |
| h | `inertia` | 0.5 | Previous-velocity blend weight |
| e | `noise_strength` | 0.3 | Noise magnitude |
| delta_sheep | `sheep_speed` | 1.5 | Sheep step length |
| rho_s | `shepherd_speed` | 2.0 | Shepherd step length |

## Sheep Dynamics
For each sheep i each tick:
1. Compute LCM of neighbours within `r_n`.
2. Attraction `A_i`: unit vector toward LCM.
3. Neighbour repulsion `R_a,i` within `r_a` (inverse-distance weighted).
4. Shepherd repulsion `R_s,i` within `r_s`.
5. Add noise `e_i`.
6. Desired direction: `c * A_i + R_a,i + R_s,i + e_i`.
7. Blend with inertia: `h * v_prev + (1-h) * desired`, normalise, scale by `sheep_speed`.
8. Integrate position and reflect at world boundaries.

## Shepherd Dynamics
1. Compute flock GCM.
2. If `max_i ||p_i - GCM|| > f(N) = r_a * N^(2/3)` -> Collect, else Drive.
3. Collect target: point behind furthest sheep relative to GCM, offset by `r_a` (code: `collect_drive_offset`, default equals `r_a`).
4. Drive target: point behind GCM relative to goal, same offset.
5. Move toward target at `shepherd_speed`.

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
- Drive uses `state.world.goal.center` when available (not a stale config copy).
- Multi-shepherd values share the same Collect/Drive target; this algorithm is defined for one shepherd. Use Kubo for coordinated multi-dog herding.
- Paper variable mapping: `e` -> `noise_strength`, `h` -> `inertia`, `delta`/`v` -> `sheep_speed`, shepherd speed -> `shepherd_speed`.
