# Simulation Environment

## Integration
Each tick, algorithms compute new velocities, then positions are updated:
- Strombom: `p <- p + v` (unit step already scaled by speed)
- Kubo: `p <- p + dt * v` with `dt` from config (default 0.05)

## Shared World Model
`core/world.py` defines:
- Rectangular arena (`width`, `height`)
- Optional circular `GoalZone`
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
| ID | Objective |
|----|-----------|
| `drive_to_goal` | Herd sheep into a corner goal circle |
| `containment` | Keep sheep inside a central pen for a minimum duration |
| `obstacle_course` | Reach a goal while avoiding rectangular obstacles |

## Reproducibility
`SimulationRunner` creates `numpy.random.default_rng(seed)` and stores it on `SimulationState.rng`. All stochastic terms must use `state.rng`.
