# Simulation environment

## Integration (tick vs `dt`)

Each tick, algorithms compute new velocities, then update positions. Semantics differ by family:

| Family | Position update | Speed meaning |
|--------|-----------------|---------------|
| Strombom / Flocking Dog / Strombom variants | `p <- p + v` | `sheep_speed` / `shepherd_speed` are **displacement per tick** (world `dt` not applied) |
| Kubo | `p <- p + dt * v` | `dt` from **algorithm config** (default 0.05). Scenario `World.dt` does not integrate Kubo |

Cross-algorithm path length and speed comparisons are therefore not physically time-normalized. Analytics CSV/JSON exports list this caveat.

## Shared world model

`core/world.py`:

- Rectangular arena (`width`, `height`)
- Optional circular `GoalZone` (also used as the containment pen)
- Optional rectangular `Obstacle` list

## Boundary handling

1. `reflect_positions` -- mirror overshoot back into the arena
2. `reflect_velocities` -- flip velocity components at edges
3. `resolve_obstacles` -- push agents from obstacle interiors to the nearest edge (applied in `SimulationRunner` for all algorithms after the algorithm step)

## Shared sheep helpers

`core/agents/sheep.py` provides building blocks used by Strombom-family algorithms (local centroid, attraction, neighbour repulsion, shepherd repulsion, noise). Kubo uses MATLAB-faithful forces in `algorithms/kubo/forces.py`.

## Scenarios

See [scenarios.md](scenarios.md) for success criteria. Summary:

| ID | Objective |
|----|-----------|
| `drive_to_goal` | Herd sheep into a corner goal circle |
| `containment` | Keep sheep inside a central pen for a minimum duration |
| `obstacle_course` | Reach a goal while avoiding rectangular obstacles |
| `split_flock` | Collect / recovery from 2-3 initial clusters |
| `narrow_gate` | Pass a choke point then reach the goal |
| `wide_field` | Long drive on a larger arena |

## Reproducibility

`SimulationRunner` creates `numpy.random.default_rng(seed)` on `SimulationState.rng`. All stochastic terms must use `state.rng`.
