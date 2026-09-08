# Metrics

All metrics implement `BaseMetric` and are algorithm-agnostic unless noted.

| ID | Name | Definition |
|----|------|------------|
| `cohesion` | Flock Cohesion | Mean distance of sheep to GCM |
| `gcm_goal` | GCM to Goal | Euclidean distance from flock GCM to goal centre |
| `time_to_goal` | Time to Goal | Current tick if **all** sheep are in the goal, else -1 (strict all-in-goal) |
| `shepherd_path` | Shepherd Path Length | Cumulative distance traveled by all shepherds |
| `success_rate` | Success Rate | Fraction of sheep currently inside the goal (occupancy) |
| `sheep_in_goal` | Sheep in Goal | Integer count of sheep currently inside the goal |
| `polarization` | Flock Polarisation | `\|\|mean(unit velocities)\|\|` in [0, 1] |
| `outlier_count` | Outlier Count | Count of sheep with distance to GCM > effective collect threshold |
| `min_separation` | Min Separation | Minimum pairwise sheep distance |

## Semantic notes

- `shepherd_path` is stateful; `HistoryRecorder.reset()` clears it between runs.
- `outlier_count` reads `state.metadata["r_a"]` and optional `collect_threshold_scale`. The threshold form `f(N) = r_a * N^(2/3)` is Strombom-shaped; algorithms that publish `r_a` remain comparable.
- `success_rate` / `sheep_in_goal` measure occupancy. Scenario **success** may use `success_fraction` < 1.0.
- Benchmark `first_success_tick` follows scenario success, not `time_to_goal`.
- Cross-algorithm path length and speed are not time-normalized when mixing displacement-per-tick families with Kubo `dt` (see [environment.md](environment.md)).

## Exports

- Session: `GET /api/metrics/export/{session_id}?format=json|csv|md`
- Analytics: `GET /api/benchmarks/export?format=csv|json|md` (CSV/JSON preferred for analysis)

## Code

- Implementations: `metrics/<id>.py`
- Registry: `metrics/registry.py`
- Tests: `tests/backend/correctness/test_metrics_formulas.py` and related
