# Metrics Guide

All metrics implement `BaseMetric` and are algorithm-agnostic.

| ID | Name | Definition |
|----|------|------------|
| `cohesion` | Flock Cohesion | Mean distance of sheep to GCM |
| `gcm_goal` | GCM to Goal | Euclidean distance from flock GCM to goal centre |
| `time_to_goal` | Time to Goal | Current tick if all sheep in goal, else -1 |
| `shepherd_path` | Shepherd Path Length | Cumulative distance traveled by all shepherds |
| `success_rate` | Success Rate | Fraction of sheep currently inside the goal |
| `polarization` | Flock Polarisation | `||mean(unit velocities)||` in [0,1] |
| `outlier_count` | Outlier Count | Count of sheep with distance to GCM > `r_a * N^(2/3)` |
| `min_separation` | Min Separation | Minimum pairwise sheep distance |

## Notes
- `shepherd_path` is stateful; `HistoryRecorder.reset()` clears it between runs.
- `outlier_count` reads `state.metadata["r_a"]` (set by the runner/algorithms).
- Export endpoints: `GET /api/metrics/export/{session_id}?format=json|csv|md`.
