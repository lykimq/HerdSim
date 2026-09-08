# V-Formation (Fujioka / Hayashi line)

## Paper reference

- K. Fujioka, S. Hayashi
- Effective herding with V-formation control (shepherding / V-formation literature)
- Mechanism adapted in HerdSim under id `v_formation` with Strombom sheep dynamics

## Problem

Multiple dogs should drive a cohesive flock without stacking on a single Drive point. V-formation places shepherds on an angular arc behind the GCM relative to the goal.

## Algorithm (written out)

### Sheep

Identical to [strombom_2014.md](strombom_2014.md).

### Shepherds

1. Compute threshold `f(N) = r_a * N^(2/3) * collect_threshold_scale`.
2. **If outliers exist:** Collect -- assign dogs to distinct furthest outliers with tangential spacing (same idea as `strombom_multi`).
3. **Else Drive:** place dog `i` at `GCM + R(behind_unit, angle_i) * offset` where `angle_i = (i - (M-1)/2) * v_angle_deg` (radians) and `offset` is `v_arc_offset` or `r_a * sqrt(N)`.
4. Step toward targets with Strombom stop distance and noise.

Metadata: `herding_mode`, `assignment_lines`.

## Parameters

Strombom paper params apply. Additions:

| Key | Default | Purpose / effect |
|-----|---------|------------------|
| `v_angle_deg` | 35 | Angular spacing between V-arc slots. Larger -> wider V. |
| `v_arc_offset` | (optional) | Arc radius; default `r_a*sqrt(N)`. Larger -> dogs stand farther behind. |
| `n_shepherds` | 2 | Number of V slots |

## Fidelity notes

- Sheep = Strombom 2014.
- V-arc geometry is a HerdSim implementation of the V-formation *idea* for fair multi-dog Drive contrast; not a line-by-line port of every Fujioka experiment setting.
- Scenario goal and wall reflection as elsewhere in HerdSim.

## Code / tests

- `algorithms/v_formation/`
- `tests/backend/correctness/test_v_formation.py`
