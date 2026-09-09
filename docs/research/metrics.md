# Metrics

Metrics are computed at every tick and are algorithm-agnostic unless noted. They appear in the live metrics panel during Single and Arena runs, in the scrub history, and in Analytics exports.

## Metric definitions

| Metric | Definition |
|--------|------------|
| **Cohesion** | Mean Euclidean distance of all sheep from the flock global centre of mass (GCM). Lower values indicate a tighter, more aggregated flock. |
| **GCM to Goal** | Euclidean distance from the GCM to the goal centre. Decreasing values indicate the flock is progressing toward the goal. |
| **Success Rate** | Fraction of sheep currently inside the goal zone, from 0.0 to 1.0. This is an instantaneous occupancy measure, not a scenario success flag. |
| **Sheep in Goal** | Integer count of sheep currently inside the goal zone. |
| **Time to Goal** | Current tick number if all sheep are simultaneously inside the goal; -1 otherwise. This is a strict all-in-goal measure. |
| **Shepherd Path** | Cumulative Euclidean distance travelled by all shepherds combined since the session was last reset. Reflects total shepherd effort. |
| **Polarisation** | Mean of the unit velocity vectors of all sheep, reported as a scalar magnitude between 0 and 1. A value near 1 means all sheep are moving in nearly the same direction (high alignment); near 0 means movement directions are dispersed. |
| **Outlier Count** | Number of sheep whose distance from the GCM exceeds the shared threshold f(N) = `r_a` * N^(2/3) (optionally scaled by `collect_threshold_scale`). Same formula for every algorithm. |
| **Min Separation** | Minimum pairwise distance between any two sheep. A proxy for collision risk and crowding. |

## Notes on specific metrics

**Shepherd Path** is cumulative within a session. Resetting the session (Create / Reset) clears the accumulated path.

**Outlier Count** always uses that Strombom-shaped threshold so Arena and Analytics can compare flock spread on one scale. For Collect / Drive algorithms (Strombom family, Flocking Dog), this is also the Collect switch boundary. For algorithms without that switch (such as Kubo), the count is still a valid spread score under the same definition; it does not drive the controller. Kubo keeps an `r_a` value so the threshold can be evaluated. This metric is **not** “sheep outside the goal” -- use **Sheep in Goal** or **Success Rate** for goal occupancy.

**Time to Goal** is intentionally strict. It is useful for measuring clean success -- a run where every sheep entered the goal at the same time -- but will remain at -1 for runs where `success_fraction` < 1.0 allows the scenario to succeed with a few sheep still outside.

**Polarisation** can transiently peak during Drive when dogs push the flock coherently in one direction, and drop during Collect when the flock is fragmented.

## Comparing across algorithms

**Cohesion, GCM to Goal, Success Rate, Sheep in Goal, Outlier Count, Min Separation,** and **Polarisation** use the same definitions for every algorithm, so you can compare them directly on a shared seed and scenario. Outlier Count shares one threshold shape; interpret it as flock spread, and use goal metrics when you care about sheep in the goal.

**Shepherd Path** is comparable across algorithms only when they share the same time-step convention. Strombom-family algorithms advance agents by a fixed displacement per tick; Kubo integrates over a continuous dt. A Kubo run with the same number of ticks represents a different physical duration, so path lengths are not directly comparable to Strombom without normalising by the integration step.

**Time to Goal** and **First Success Tick** are directly comparable for the same scenario and flock size, but carry the same caveat about tick-step conventions across families.

## Analytics exports

The Analytics tab exports all metric values alongside the resolved algorithm configuration, scenario, seed, and outcome for each trial. CSV format contains one row per trial. JSON format includes full provenance, metric definitions, and notes on time-step conventions. These caveats are documented inside the export files themselves.
