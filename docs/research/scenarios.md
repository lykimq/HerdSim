# Scenarios

A scenario defines the task, the world layout, and the success criterion for a simulation run. Any algorithm can run in any scenario; scenarios and algorithms are fully independent.

## Scenario index

| Scenario | Task | Success criterion |
|----------|------|-------------------|
| **Drive to Goal** | Herd the entire flock into a corner goal zone. | Fraction of sheep inside the goal >= `success_fraction` (default: all sheep). |
| **Containment** | Keep the flock inside a central pen for a sustained period. | Pen occupancy >= `containment_fraction` held continuously for `containment_min_ticks`. |
| **Obstacle Course** | Reach the goal while navigating around rectangular obstacles placed in the arena. | Fraction in goal >= `success_fraction`. |
| **Split Flock** | Collect and drive a flock that starts in two or three separated clusters. | Fraction in goal >= `success_fraction` (default 0.95). |
| **Narrow Gate** | Pass the flock through a choke point before reaching the goal. | Fraction in goal >= `success_fraction`. |
| **Wide Field** | Long-distance drive on a larger arena. Tests efficiency at scale. | Fraction in goal >= `success_fraction`. |

## Presets

Each scenario has a recommended configuration accessible via the **scenario** preset. This sets flock size, shepherd count, and world layout to values suited to the task. The **paper** preset overrides agent counts with the algorithm's published defaults while keeping the scenario's world layout.

## What scenarios control

Scenarios own the world geometry: arena dimensions, goal or pen position and radius, obstacle placement, gate parameters (position, width, wall thickness), and containment thresholds. Algorithms run inside the world the scenario defines.

## Success, occupancy, and time

Three related quantities appear in the metrics panel and run report:

**Success rate** (live metric) is the fraction of sheep currently inside the goal zone. This updates every tick and ranges from 0 to 1.

**Sheep in goal** (live metric) is the integer count of sheep inside the goal zone.

**Scenario success** is declared when the scenario's specific criterion first holds -- for example, all sheep inside the goal, or the pen occupancy threshold sustained for enough ticks. Success is a boolean event, not a continuous metric.

**Time to goal** is a strict metric: it reports the current tick only when every single sheep is simultaneously inside the goal. If any sheep is outside, it returns -1. This can differ from the first success tick under scenarios where `success_fraction` is less than 1.

**First success tick** (in run reports and Analytics exports) is the tick at which the scenario success criterion first held. This is the primary outcome measure for comparing algorithms on a given scenario.

## Collect threshold and scenario tuning

Some scenarios, particularly Split Flock, benefit from raising `collect_threshold_scale` above 1.0 in the scenario preset. This widens the Collect / Drive switch boundary so that a shepherd does not attempt to drive before the separated sub-flocks are sufficiently merged. The scenario preset manages this automatically.
