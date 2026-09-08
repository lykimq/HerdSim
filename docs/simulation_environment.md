# Simulation Environment

## Integration

Each tick, algorithms compute new velocities, then positions are updated. Semantics differ by algorithm family:

- Strombom / Flocking Dog: `p <- p + v` where `sheep_speed` / `shepherd_speed` are **displacement per tick** (world `dt` is not applied to those steps).
- Kubo: `p <- p + dt * v` with `dt` from **algorithm config** (default 0.05). Scenario `World.dt` is separate and does not drive Kubo integration.

Cross-algorithm path length and speed comparisons are therefore not time-normalized. Analytics CSV/JSON exports list this caveat.

## Shared World Model
`core/world.py` defines:
- Rectangular arena (`width`, `height`)
- Optional circular `GoalZone` (also reused as the containment pen)
- Optional rectangular `Obstacle` list

## Boundary Handling
1. `reflect_positions`: mirror overshoot back into the arena
2. `reflect_velocities`: flip velocity components at edges
3. `resolve_obstacles`: push agents from obstacle interiors to the nearest edge (applied in `SimulationRunner` for all algorithms)

## Sheep Flocking Vectors (shared helpers)
`core/agents/sheep.py` provides reusable building blocks used by Strombom:
- local centroid
- attraction
- neighbour repulsion
- shepherd repulsion
- noise

Kubo uses its own MATLAB-faithful force terms in `algorithms/kubo/forces.py`.

## Scenarios

See [`scenarios.md`](scenarios.md) for the full list and success criteria. Summary:

| ID | Objective |
|----|-----------|
| `drive_to_goal` | Herd sheep into a corner goal circle |
| `containment` | Keep sheep inside a central pen for a minimum duration |
| `obstacle_course` | Reach a goal while avoiding rectangular obstacles |
| `split_flock` | Collect / recovery from 2-3 initial clusters |
| `narrow_gate` | Pass a choke point then reach the goal |
| `wide_field` | Long drive on a larger arena |

## Reproducibility
`SimulationRunner` creates `numpy.random.default_rng(seed)` and stores it on `SimulationState.rng`. All stochastic terms must use `state.rng`.
