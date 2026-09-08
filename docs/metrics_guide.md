# Metrics Guide

All metrics implement `BaseMetric` and are algorithm-agnostic.

| ID | Name | Definition |
|----|------|------------|
| `cohesion` | Flock Cohesion | Mean distance of sheep to GCM |
| `gcm_goal` | GCM to Goal | Euclidean distance from flock GCM to goal centre |
| `time_to_goal` | Time to Goal | Current tick if **all** sheep are in the goal, else -1 (strict) |
| `shepherd_path` | Shepherd Path Length | Cumulative distance traveled by all shepherds |
| `success_rate` | Success Rate | Fraction of sheep currently inside the goal (occupancy) |
| `sheep_in_goal` | Sheep in Goal | Integer count of sheep currently inside the goal |
| `polarization` | Flock Polarisation | `||mean(unit velocities)||` in [0,1] |
| `outlier_count` | Outlier Count | Count of sheep with distance to GCM > effective collect threshold |
| `min_separation` | Min Separation | Minimum pairwise sheep distance |

## Notes
- `shepherd_path` is stateful; `HistoryRecorder.reset()` clears it between runs.
- `outlier_count` reads `state.metadata["r_a"]` and optional `collect_threshold_scale`.
- `success_rate` / `sheep_in_goal` measure occupancy. Scenario **success** may use a lower `success_fraction` than 1.0.
- Benchmark column `first_success_tick` is when the scenario criterion was met; it can differ from `time_to_goal`.
- Session export: `GET /api/metrics/export/{session_id}?format=json|csv|md`.
- Analytics export: `GET /api/benchmarks/export?format=csv|json|md` (CSV/JSON preferred for analysis).
