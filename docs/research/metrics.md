# Metrics

Metrics are computed at every tick from observable simulation state and are
algorithm-agnostic unless noted. They appear in the live metrics panel during
Single and Arena runs, in the scrub history, and in Analytics exports.

Per-tick plugins write into history. Analytics **trial** and **summary** exports
use an outcome + trajectory schema (mean/min/max/auc over the run), not bare
final-tick metric ids.

## Metric taxonomy

### A. Effectiveness (task and goal progress)

| Metric | Definition |
|--------|------------|
| **Success Rate** (per-tick) | Fraction of sheep currently inside the goal zone (0-1). Instantaneous occupancy, not the trial success flag. |
| **Sheep in Goal** | Integer count of sheep currently inside the goal zone. |
| **Time to Goal** | Current tick if all sheep are simultaneously inside the goal; -1 otherwise. |
| **GCM to Goal** | Euclidean distance from the flock GCM to the goal centre. |

**Task success** is the scenario criterion (`is_success`), exported as trial column `success`. It is separate from occupancy metrics.

### B. Efficiency (control effort)

| Metric | Definition |
|--------|------------|
| **Shepherd Path** | Cumulative Euclidean distance travelled by all shepherds since reset. |
| **Control efficiency** (trial) | `(gcm_goal at start - gcm_goal at end) / shepherd_path`. 0 if path is 0. |

### C. Flock integrity

| Metric | Definition |
|--------|------------|
| **Cohesion** | Mean Euclidean distance of sheep to the GCM (dispersion). Lower is tighter. |
| **Fragmentation** | Size of the largest connected component / N, with edges when pairwise distance <= `measurement_radius`. 1.0 is one connected flock. |
| **Min Separation** | Minimum pairwise sheep distance. |

`measurement_radius` is an **experimental** shared default (see Environment), not Kubo `radius` or Strombom `r_a`.

### D. Collective behaviour

| Metric | Definition |
|--------|------------|
| **Polarisation** | Magnitude of the mean of sheep unit velocity vectors (0-1). |

### E. Spread (shared experimental threshold)

| Metric | Definition |
|--------|------------|
| **Outlier Count** | Number of sheep beyond f(N) = `r_a` * N^(2/3) (optionally scaled by `collect_threshold_scale`) from the GCM. Same formula for every algorithm so Arena/Analytics share one spread scale. For Collect/Drive controllers this matches the mode switch; for Kubo it is a report score only. Not "sheep outside the goal." |

## Outcome vs trajectory (Analytics)

| Kind | Examples |
|------|----------|
| Outcome / task | `success`, `total_ticks`, `first_success_tick`, `time_to_goal`, `final_*`, `shepherd_path` |
| Trajectory | `mean_*`, `min_*`, `max_*`, `auc_*` for cohesion, gcm_goal, polarization, fragmentation, outlier_count |
| Derived | `control_efficiency` |

`auc_*` is the mean of the metric over ticks in that trial. Summary tables average these trial fields across seeds (plus success/failure rates and tick IQR).

## Notes on specific metrics

**Shepherd Path** is cumulative within a session. Resetting the session (Create / Reset) clears the accumulated path.

**Time to Goal** is intentionally strict. It can remain -1 when `success_fraction` < 1.0 allows scenario success with a few sheep outside.

**Polarisation** can peak during Drive and drop during Collect when the flock is fragmented.

## Comparing across algorithms

Cohesion, GCM to Goal, Success Rate, Sheep in Goal, Fragmentation, Outlier Count, Min Separation, and Polarisation use the same definitions for every algorithm on a shared seed and scenario.

**Shepherd Path** and tick counts are comparable across algorithms only when they share the same time-step convention. Strombom-family algorithms advance by a fixed displacement per tick; Kubo integrates over continuous `dt`. Path lengths are not directly comparable without normalising by the integration step.

For fair comparison, lock the same `n_sheep`, `n_shepherds`, scenario, and seeds (custom preset). Do not use paper preset when comparing models that declare different paper agent counts. See `docs/research/comparison_framework.md`.

## Factor-derived analysis outputs

Trial tables from factor grids also support:

- `required_shepherds` estimates via `analysis.herdability.required_shepherds`
- sensing/noise degradation slopes via `analysis.herdability.degradation_slope`
- dimensionless predictors (`pi_speed`, `pi_dogs`, `pi_sensing`, `pi_density`)
- behavioural event transitions via `analysis.behavioural`
- velocity-correlation delay proxies via `analysis.propagation`

These are analysis-layer outputs, not per-tick metric plugins.

JSON packages include `herdsim_version`, best-effort `git_commit`, `python_version`, experiment design, `resolved_config` (from a trial), metric definitions, summary, trial rows, and caveats. CSV includes the same preamble facts; nested `resolved_config` is omitted from CSV cells and kept in JSON.
