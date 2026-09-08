# Algorithms

| ID | Family | Paper / basis | Page |
|----|--------|---------------|------|
| `strombom` | Collect/Drive | Strombom et al. 2014 | [strombom_2014.md](strombom_2014.md) |
| `strombom_noise` | Collect/Drive | Strombom + elevated noise | [strombom_noise.md](strombom_noise.md) |
| `strombom_multi` | Collect/Drive multi-dog | Strombom multi-dog extension | [strombom_multi.md](strombom_multi.md) |
| `kubo` | Force-based multi-dog | Kubo et al. 2022 | [kubo_2022.md](kubo_2022.md) |
| `flocking_dog` | Topological flocking + dog | Jadhav et al. 2024 | [flocking_dog_2024.md](flocking_dog_2024.md) |
| `v_formation` | V-formation drive | Fujioka / Hayashi line | [v_formation.md](v_formation.md) |
| `heterogeneous` | Collect/Drive + sheep types | Heterogeneous response variant | [heterogeneous.md](heterogeneous.md) |
| `obstacle_aware` | Collect/Drive + obstacle drive | Clutter-aware heuristic | [obstacle_aware.md](obstacle_aware.md) |

MATLAB companion for Kubo: [force_based_matlab.md](force_based_matlab.md).

PDF sources: [../../papers/](../../papers/).

## Fidelity notes (current suite)

- Collect/Drive Strombom family shares `f(N)` and `collect_threshold_scale` (including `strombom_multi`).
- Strict `time_to_goal` vs scenario success / `first_success_tick` documented in [../metrics.md](../metrics.md).
- Tick vs Kubo `dt` caveats in [../environment.md](../environment.md) and Analytics exports.
- NetLogo twins: Drive-to-Goal behavioural comparison only ([../netlogo.md](../netlogo.md)).
