# Flocking Dog (2024) -- Implementation Spec

## Paper Reference
- Collective responses of flocking sheep (Ovis aries) to a herding dog (border collie)
- Communications Biology, 2024
- DOI: https://doi.org/10.1038/s42003-024-07245-8

## Overview
Runnable HerdSim model inspired by empirical dog-sheep coupling: sheep combine classic flocking with reciprocal dog interaction and a front-biased response; the dog uses Collect/Drive positioning with a mild pull toward the flock front.

## Agents

| Type | Count | State |
|------|-------|-------|
| Sheep | N (default 40) | position, velocity |
| Shepherd dog | 1 (default) | position, velocity |

## Parameters

| Code key | Default | Meaning |
|----------|---------|---------|
| `r_n` | 25 | Neighbourhood radius |
| `r_a` | 3 | Sheep-sheep repulsion radius |
| `alignment_weight` | 0.8 | Alignment gain |
| `r_s` | 40 | Dog interaction radius |
| `dog_repulsion` | 2.2 | Sheep escape gain from dog |
| `sheep_attraction_to_dog` | 0.15 | Reciprocal pull toward dog |
| `front_bias` | 0.35 | Extra weight when dog is ahead of sheep heading |
| `shepherd_speed` | 2.2 | Dog step length |

## Sheep Dynamics
1. Attraction to local centroid
2. Neighbour repulsion
3. Velocity alignment
4. Dog repulsion within `r_s`
5. Front-biased reciprocal coupling toward dog
6. Noise + inertia blend, scaled by `sheep_speed`

## Shepherd Dynamics
1. Collect if furthest sheep exceeds `r_a * N^(2/3)` from GCM, else Drive
2. Move toward Collect/Drive target
3. Add small reciprocal pull toward flock centroid / front

## Known Simplifications
- Not a replay of UWB trajectories from the paper
- Discrete Collect/Drive retained for goal-directed herding tasks in HerdSim
- Single primary interaction radius rather than full empirical kernel fits

## Implementation Notes
- Code: `algorithms/flocking_dog/algorithm.py`, `dynamics.py`, `config.py`
- Reuses Strombom Collect/Drive target helpers for goal scenarios
