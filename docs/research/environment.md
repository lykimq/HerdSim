# Simulation Environment

## Arena

All simulations run inside a rectangular arena with configurable width and height. The arena is defined by the selected scenario. Walls are hard boundaries: agents that would overshoot a wall are reflected back into the arena. Both position and velocity components are reflected, so agents bounce off walls rather than clipping through them.

## Goal zone

The goal zone is a circular region within the arena. Its centre and radius are set by the scenario. Sheep are counted as inside the goal if their position falls within this circle. In the Containment scenario the same circular zone serves as the pen.

## Obstacles

Scenarios that include obstacles place one or more rectangular regions inside the arena. Agents that collide with an obstacle boundary are pushed to the nearest edge. The Obstacle-Aware algorithm uses the positions and extents of these rectangles to deflect its Drive target around them. Other algorithms do not reason about obstacles explicitly; they still respect the obstacle boundaries through the environment's collision resolution, but their Drive targets may point through obstacles.

## Time step conventions

HerdSim supports two time-step conventions, and algorithms choose one at implementation.

**Displacement-per-tick (Strombom family).** On each tick, an agent advances by a fixed displacement d in the direction of its heading:

```
p  <-  p  +  d * heading_unit
```

The parameters `sheep_speed` and `shepherd_speed` are this displacement in world units per tick. World time `dt` has no effect on these algorithms.

**Continuous integration (Kubo).** On each tick, an agent integrates a velocity field using a configurable time step `dt`:

```
p  <-  p  +  dt * v
```

The parameter `dt` is part of the algorithm configuration. Speed parameters are velocities (world units per unit time), and the effective displacement per tick is `dt * v`.

These two conventions are not interchangeable. The number of ticks to complete a scenario, and the cumulative shepherd path length, are not physically equivalent between families even at the same tick count. Analytics exports document which convention each algorithm uses, and this caveat appears in exported CSV and JSON files.

## Reproducibility

Every stochastic element in a run -- initial sheep positions, heading noise, random grazing steps, stubborn sheep assignment -- is drawn from a single seeded random number generator. Given the same seed, algorithm, scenario, and parameter values, a run is fully deterministic and reproducible. Different seeds produce statistically independent runs, which is what the Analytics multi-seed mode exploits.

## Experimental measurement radius

`measurement_radius` (shared default, overridable) is used only by the fragmentation metric: sheep within that distance are treated as connected. It is an experimental measurement parameter, not Kubo sensing `radius` and not Strombom `r_a`.

## Tick order and environment constraints

Each tick applies algorithm movement, then obstacle and wall resolution, then metrics on the constrained state. Metrics therefore describe positions after environment constraints.
