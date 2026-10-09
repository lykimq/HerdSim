# phase2_claim

## Purpose

CLAIM reseed on reliability-window cells for RQ1 start shape. Measures fewest dogs (`D_min`) and path/time cost across the four layouts at N in {50, 100, 200}.

## Setup

- Protocol: `scaling_v2` (`phase2_claim`); upstream scout `phase2_scout`
- Depends on: RQ1 scout.
  - Reads (plan): `../scout/trials.csv`
  - Writes: `boundary_cells.csv`, `boundary_plan.json`, then `trials.csv`
  - Merge: `merged_trials.csv` = claim-window rows from `trials.csv` + non-window rows from `../scout/trials.csv`
- Method: `strombom_multi`
- Layouts: compact, wide, split, outlier_rich
- N: {50, 100, 200}
- D: reliability window (24 cells in `boundary_cells.csv`)
- Seeds: 100 on window cells
- Theta: 0.90
- T0: 10000
- Package export: B (on `merged_trials.csv`)
- Commands (run in this order):
  1. Plan: `make -C scaling scaling-phase2-claim-plan`
     Must run after this method's scout. Chooses scout cells near the reliability edge and writes `boundary_cells.csv` / `boundary_plan.json` (no claim sims yet).
  2. Reseed: `make -C scaling scaling-phase2-claim-reseed WORKERS=16`
     Runs the claim sims (100 seeds) on those planned cells.

## Completeness

2,400 / 2,400 claim trials (`status.json` complete). Merge has 5,280 rows. Overall success 1.0 on the merge.

## Runtime

Started:  25 Sep 2026, 12:40 UTC
Finished: 25 Sep 2026, 15:39 UTC
Total:    2h 59m

## Results

- Success: R = 1.0 at D = 1 for every layout x N cell on the claim windows
- `D_min` = 1 for compact, split, outlier_rich, wide at N in {50, 100, 200}; no overcrowding; `d_max` = 35
- Cheap good setup (`B*`) effort from `packages/b/frontier_by_layout.csv`:
  - compact / split: about 144 to 162 path units at B*_d = 1
  - outlier_rich: 209 (N=50) to 1647 (N=200) at B*_d = 1
  - wide: 2337 to 3694 path units; B*_d shifts to 2 (cost minimum), while `D_min` stays 1
- Bootstrap: `d_min_ci_low` == `d_min_ci_high` for all layout x N at 100 seeds
- Predictor (Package B): `prefers_state=False` (`state_nll` is not lower than `nd_nll`; early state does not beat `(N, D)` on leave-one-N NLL). NLL comparison is not informative when `D_min` is flat

## Interpretation

Start shape changes work (walking and time), not dog count, on this baseline controller and T0. Wide and outlier_rich starts stretch path length and time by an order of magnitude, but a single dog still clears theta=0.90. That rejects C1a (layout-driven `D_min` shift). C1b stays inconclusive: with no `D_min` movement, state predictors have nothing extra to explain.

## Claims update

| Claim | What it asks (supported when) | Verdict | Evidence |
|-------|-------------------------------|---------|----------|
| C1a | For at least one N, `D_min` differs by at least one D-grid step across layouts at theta 0.90 | REJECTED | `packages/b/frontier_by_layout.csv`: `D_min` = 1 on all 4 layouts at N in {50, 100, 200} |
| C1b | The early-state model has lower leave-one-N-out NLL than the `(N, D)` model | INCONCLUSIVE | no `D_min` shift; state vs (N, D) predictor comparison not decisive |

## Files in this folder

### Dependencies

```mermaid
flowchart LR
  scout["../scout/trials.csv"] -->|"plan"| plan["boundary_cells.csv<br/>boundary_plan.json"]
  plan -->|"reseed"| trials["trials.csv"]
  scout -->|"merge: non-window"| merge["merged_trials.csv"]
  trials -->|"merge: window"| merge
  merge --> pkgs["packages/b/"]
```

```
.
|-- boundary_cells.csv
|-- boundary_plan.json
|-- dmin_bootstrap.csv
|-- manifest.jsonl
|-- merged_dmin_bootstrap.csv
|-- merged_trials.csv
|-- protocol.yaml
|-- status.json
|-- trials.csv
`-- packages/
    `-- b/
```

**Config**
- `protocol.yaml`: Run settings (method, layouts, N/D grid, seeds, grade).

**Planning (auto before claim / T1)**
- `boundary_cells.csv`: Cells chosen for 100-seed claim reseed (from scout).
- `boundary_plan.json`: Planner metadata for the claim window (theta, params).

**Auto-generated (run)**
- `manifest.jsonl`: Per-cell progress log; enables resume without re-running ok cells.
- `merged_trials.csv`: Claim-window 100-seed rows + non-window scout 30-seed rows.
- `status.json`: Planned vs done counts, complete flag, start/finish, elapsed.
- `trials.csv`: One row per seed (success, ticks, path/effort, layout, N, D, ...).

**Auto-generated (analysis)**
- `dmin_bootstrap.csv`: Bootstrap of D_min / CI from claim trials only.
- `merged_dmin_bootstrap.csv`: Same bootstrap schema on merged_trials.csv.

**Auto-generated (analysis packages)**
- `packages/b/`: Package B (structure / layout tables).

Trajectory parquet written during the run is not retained here.

## Limits

Baseline method only (`strombom_multi`). No overcrowding cells on this map. Split looks cost-similar to compact.
