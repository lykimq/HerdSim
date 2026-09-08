# Flocking Dog (Jadhav et al. 2024)

## Paper reference

- V. Jadhav et al.
- "Collective responses of flocking sheep (Ovis aries) to a herding dog (border collie)"
- Communications Biology, 2024
- DOI: https://doi.org/10.1038/s42003-024-07245-8
- PDF: [../../papers/Jadhav_et_al.pdf](../../papers/Jadhav_et_al.pdf)
- Author MATLAB: `model/herding_model.m` (tee-lab GitHub)

## Problem the paper solves

Model flocking sheep responding to a herding dog with topological attraction/alignment, short-range repulsion, and dog repulsion; dog uses Collect/Drive geometry.

## Algorithm (written out)

### Sheep

1. If dog distance > `r_s`: graze (velocity = 0).
2. Else: perceive `k` nearest neighbours; sample `nAtt` for attraction and `nAli` for alignment; short-range repulsion within `r_a`; unit dog repulsion; heading `h H + rho_a Rep + rho_d Dog + c Att + alg Ali + e noise`; step `vS`.

### Dog

1. If within `r_a` of any sheep: continue previous heading at absolute speed `shepherd_close_speed` (0.05; MATLAB absolute, not 0.05*`vDog`).
2. Else if furthest sheep > `f(N)=r_a*N^(2/3)` from GCM: Collect behind that sheep (offset `pc=r_a`).
3. Else Drive behind GCM relative to goal (offset `pd=r_a*sqrt(N)`).
4. Add angular noise `e`, move at `vDog`.

## Agents

Default N=14, M=1.

## Paper parameters (accounts)

| Key | Default | Purpose / effect |
|-----|---------|------------------|
| `r_a` | 2 | Sheep-sheep repulsion distance; enters `f(N)` and close-dog test |
| `r_s` | 12 | Dog interaction range; beyond = graze |
| `k_neighbors` | 10 | Neighbourhood size for perception |
| `n_attraction` / `n_alignment` | 5 / 1 | Random topological subsets |
| `inertia` | 0.5 | Previous-heading weight |
| `sheep_repulsion_weight` | 2.0 | Weight on sheep-sheep repulsion |
| `dog_repulsion_weight` | 1.0 | Weight on dog repulsion |
| `attraction_weight` / `alignment_weight` | 1.5 / 1.3 | Flocking weights |
| `noise_strength` | 0.5 | Angular noise |
| `sheep_speed` / `shepherd_speed` | 1.0 / 1.5 | Displacement per tick |
| `shepherd_close_speed` | 0.05 | Slow dog near flock |

Code: `algorithms/flocking_dog/`; threshold via Strombom `compute_threshold`.

## Fidelity notes

- Paper MATLAB Drive often toward origin; HerdSim Drive uses scenario goal.
- Wall reflection applied as in other HerdSim algorithms.
- Close-dog speed follows author MATLAB absolute 0.05.

## Code / tests

- `algorithms/flocking_dog/`
- Backend correctness tests for dynamics / determinism
