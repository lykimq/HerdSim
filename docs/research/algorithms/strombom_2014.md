# Strombom et al. (2014)

## Paper reference

- D. Strombom, R. P. Mann, A. M. Wilson, S. Hailes, A. J. Morton, D. J. T. Sumpter, A. J. King
- "Solving the shepherding problem: heuristics for herding autonomous, interacting agents"
- Journal of The Royal Society Interface, 11(100):20140719, 2014
- DOI: https://doi.org/10.1098/rsif.2014.0719
- PDF: [../../papers/Strombom_et_al.pdf](../../papers/Strombom_et_al.pdf)

## Problem the paper solves

One shepherd must aggregate interacting agents (sheep) and drive them to a predetermined destination. Success in the paper is transporting the flock to the target under local attraction-repulsion sheep dynamics. The published heuristic switches between Collect (recover stragglers) and Drive (push a cohesive flock toward the goal).

## Algorithm (written out)

### Sheep (each tick)

1. If distance to nearest shepherd > `r_s`: **graze** -- remain still, or with probability `p` take a random step of length `d`.
2. Else (threatened):
   - Compute LCM of `n` nearest neighbours (`n_neighbors`; default all other sheep).
   - Attraction unit `C_hat` toward LCM.
   - Neighbour repulsion: sum unit vectors `(A_i - A_j)/|A_i-A_j|` for neighbours within `r_a`, then unit `R_a_hat` (paper eq. 4.1).
   - Shepherd repulsion unit `R_s_hat` within `r_s`.
   - Angular noise `e * e_hat`.
   - Heading (eq. 4.2): `H' = h H_hat + c C_hat + ra R_a_hat + rs R_s_hat + e e_hat`.
   - Normalise `H'`, displace by `d` (eq. 4.3).
3. Reflect at world boundaries.

### Shepherd (each tick)

1. Compute flock GCM.
2. If `max_i ||p_i - GCM|| > f(N) = r_a * N^(2/3)` (optionally times `collect_threshold_scale`) -> **Collect**, else **Drive**.
3. Collect target `Pc`: point behind the furthest sheep relative to GCM, offset `r_a` (or `collect_offset`).
4. Drive target `Pd`: point behind GCM relative to goal, offset `r_a * sqrt(N)` (or `drive_offset`).
5. If within `3 * r_a` of any sheep: speed = 0.
6. Otherwise move toward the target at `ds`, with angular noise `e`.

### Switching

```
if max_distance_to_GCM > r_a * N^(2/3) * collect_threshold_scale:
    mode = Collect
else:
    mode = Drive
```

## Agents

| Type | Paper default | State |
|------|---------------|-------|
| Sheep | N = 50 | position, velocity |
| Shepherd | M = 1 | position, velocity |

UI may set M > 1; base `strombom` still uses per-dog Collect/Drive toward shared-style targets without multi-dog assignment. Use `strombom_multi`, `kubo`, or `v_formation` for coordinated multi-dog behaviour.

## Paper parameters (full accounts)

### `r_a` (paper `r_a`, default 2.0)

Sheep-sheep repulsion distance and force weight `ra`. Enters Collect/Drive threshold `f(N) = r_a * N^(2/3)` and default collect/drive offsets. Paper Table 1. Code: sheep repulsion helpers; `compute_threshold` in `algorithms/strombom/heuristics.py`. Increase -> stronger/longer-range sheep repulsion and a larger cohesion threshold (Collect more often). Decrease -> tighter flocks and earlier Drive.

### `r_s` (paper `r_s`, default 65.0)

Shepherd detection distance for sheep. Beyond `r_s`, sheep graze. Paper Table 1. Code: sheep threat test in `algorithms/strombom/algorithm.py`. Increase -> sheep react from farther away; decrease -> larger graze region, less continuous pressure.

### `rs_weight` (paper `rs`, default 1.0)

Relative strength of shepherd repulsion in the sheep heading sum. Paper Table 1. Code: `compose_strombom_heading` / sheep step. Increase -> stronger flight from the dog; decrease -> weaker evasion (harder herding).

### `n_neighbors` (paper `n`, default -1)

Topological LCM size. `-1` means N-1 (global). Paper discusses locality of attraction. Code: `compute_local_centroid_knn`. Smaller `n` -> more local flocking, higher split risk.

### `c` (paper `c`, default 1.05)

Attraction weight toward LCM. Paper Table 1. Increase -> stronger clustering toward local centre; decrease -> weaker cohesion under threat.

### `inertia` (paper `h`, default 0.5)

Previous-heading weight. Paper Table 1. Higher -> smoother trajectories; lower -> snappier heading changes.

### `noise_strength` (paper `e`, default 0.3)

Angular noise magnitude for sheep and shepherd. Paper Table 1. Higher -> more jitter, more failed collects; lower -> more deterministic paths.

### `sheep_speed` (paper `d`, default 1.0)

Sheep displacement per tick (not meters/second). Paper Table 1. Scales how far sheep move each step.

### `graze_move_prob` (paper `p`, default 0.05)

Probability of a random step while grazing. Paper Table 1. Higher -> more drift when the dog is far.

### `shepherd_speed` (paper `ds`, default 1.5)

Shepherd displacement per tick. Paper Table 1. Higher -> dog closes targets faster relative to sheep step `d`.

### `shepherd_stop_multiple` (default 3.0)

Stop when within this multiple of `r_a` of any sheep (paper uses 3). Code: shepherd step. Lower -> dog approaches closer before stopping.

### HerdSim extensions

| Key | Default | Role |
|-----|---------|------|
| `collect_threshold_scale` | 1.0 | Multiplies `f(N)`; scenarios may widen Collect |
| `collect_offset` / `drive_offset` | derived | Optional overrides of Pc/Pd stand-off |
| `ra_weight` | = `r_a` | Optional separate weight from distance `r_a` |

## Paper preset in HerdSim

Preset **paper** loads `STROMBOM_DEFAULTS` (N=50, M=1, Table 1 behaviour). World/layout come from the selected scenario. Under `drive_to_goal` with paper defaults, expect Collect episodes while the flock is spread, then Drive toward the goal with the dog stopping near the flock; success when the scenario fraction is in the goal (default all-in-goal).

## Fidelity notes

- Matches paper Collect/Drive switch, sheep heading composition, and stop distance 3*`r_a`.
- Drive uses `state.world.goal.center` (scenario goal), not a fixed paper origin.
- Elastic wall reflection is applied (paper open-field emphasis differs).
- `collect_threshold_scale` is an intentional HerdSim extension.

## Code

- `algorithms/strombom/algorithm.py`, `heuristics.py`, `config.py`
- Shared: `core/agents/sheep.py` (`compose_strombom_heading`, `compute_local_centroid_knn`)

## Tests

- `tests/backend/correctness/test_strombom_heuristics.py`
- `tests/backend/correctness/test_algorithm_variants.py` (family behaviour)

## Related scenarios / metrics

Scenarios: `drive_to_goal`, `split_flock`, `wide_field`. Metrics: `cohesion`, `outlier_count`, `gcm_goal`, `time_to_goal`, `shepherd_path`, `success_rate`.
