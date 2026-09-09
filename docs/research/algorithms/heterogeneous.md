# Heterogeneous Sheep

## What it is

HerdSim variant of **Strombom 2014**. Collect / Drive is unchanged; a fraction of sheep have weaker shepherd repulsion for the whole run. Inspired by heterogeneous shepherding literature (e.g. Hiraoka / Sueoka / Osuka). Not a single-paper twin.

## Reference

Base paper:
D. Strombom, R. P. Mann, A. M. Wilson, S. Hailes, A. J. Morton, D. J. T. Sumpter, A. J. King.
"Solving the shepherding problem: heuristics for herding autonomous, interacting agents."
Journal of The Royal Society Interface, 11(100):20140719, 2014.
DOI: 10.1098/rsif.2014.0719

## Why

Strombom 2014 assumes every sheep responds the same way to the shepherd. Real flocks are mixed: some animals are easy to push, others resist, so residual outliers can remain even when Collect looks correct.

## Goal

Compared with homogeneous Strombom 2014, expect slower aggregation, more residual outliers, and lower success under the same tick budget as `stubborn_fraction` rises or `stubborn_rs_scale` falls. The point of a run is to quantify that difficulty, not to guarantee a cleaner herding path.

## What changes

| Aspect | Strombom 2014 | Heterogeneous |
|--------|---------------|---------------|
| Shepherd | Collect / Drive | Unchanged; shepherd does not know who is stubborn |
| Sheep response | Same `rs_weight` for all | Fraction `stubborn_fraction` use `stubborn_rs_scale` on shepherd repulsion |
| Extra params | -- | `stubborn_fraction`, `stubborn_rs_scale` |

At `stubborn_fraction` = 0 the algorithm is equivalent to Strombom 2014.

## How (idea)

```mermaid
flowchart TD
  startNode(["Start run"])
  assign["Mark a fraction of<br/>sheep as stubborn"]
  tick(["Start tick"])
  sheep["Stubborn sheep react<br/>less to the shepherd"]
  shep["Shepherd uses normal<br/>Collect / Drive"]
  done(["End tick"])

  startNode --> assign
  assign --> tick
  tick --> sheep
  sheep --> shep
  shep --> done

  classDef domain fill:#c8e6c9,stroke:#2e7d32,color:#000000
  classDef wiring fill:#e1bee7,stroke:#7b1fa2,color:#000000
  classDef start fill:#eceff1,stroke:#546e7a,color:#000000

  class startNode,tick,done start
  class shep domain
  class assign,sheep wiring
```

Legend: grey = start/end, green = shared Strombom shepherding, purple = heterogeneous sheep.

## How (rules)

Shepherd algorithm is standard Strombom 2014 Collect / Drive. Read **Strombom 2014** for that part.

The heading update follows Strombom 2014 with one modification: each sheep has an individual response factor `r_i` assigned at initialisation.

**Response assignment.** At the start of each run, a fraction `stubborn_fraction` of sheep are drawn uniformly at random and assigned the response factor `stubborn_rs_scale`. All other sheep receive a response factor of `1.0`.

**Individual heading update:**

```
H'_i = inertia * H_i
     + c * C_i
     + r_a * R_a_i
     + (rs_weight * r_i) * R_s_i
     + noise_strength * epsilon_i
```

The shepherd repulsion weight for sheep `i` is scaled by `r_i`. A stubborn sheep with `stubborn_rs_scale` = 0.25 feels only 25% of the shepherd repulsion that a normal sheep would, making it significantly harder to move.

All other terms -- LCM attraction, neighbour repulsion, `inertia`, and `noise_strength` -- are unchanged.

## Knobs

Default N = 50 sheep, M = 1 shepherd, as in Strombom 2014. All Strombom 2014 parameters apply. Additional parameters:

| Parameter | Default | Meaning |
|-----------|---------|---------|
| `stubborn_fraction` | 0.2 | Fraction of sheep assigned reduced shepherd response. At 0.0 the algorithm is equivalent to Strombom 2014. |
| `stubborn_rs_scale` | 0.25 | Response multiplier for stubborn sheep. Lower values make those sheep harder to push; at 0.0 they ignore the shepherd entirely. |

## How to read a run

- As `stubborn_fraction` increases, expect slower aggregation, more outlier ticks, and lower success under a fixed tick budget.
- Raising `stubborn_rs_scale` toward 1.0 weakens the effect; lowering it toward 0.0 approaches a permanent unresponsive sub-population.
- Stubborn assignment is fixed for the run and drawn from the simulation seed; the same seed always produces the same stubborn sub-population.

## Limits

Shepherd geometry matches Strombom 2014. Heterogeneous response is a HerdSim model of population variation, not a claim to reproduce one specific published flock.
