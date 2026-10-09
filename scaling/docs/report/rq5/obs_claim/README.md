# phase5_obs_claim

## Purpose

CLAIM reseed for the observation information ladder. Tests whether richer obs modes lower `D_min` at N in {100, 200}.

## Setup

- Protocol: `scaling_v2` (`phase5_obs_claim`); upstream `phase5_factor_sweep`
- Depends on: Observation scout.
  - Reads (plan): `../factor_sweep/trials.csv`
  - Writes: `boundary_cells.csv`, `boundary_plan.json`, then `trials.csv`
  - Merge: `merged_trials.csv` = claim `trials.csv` + non-window `../factor_sweep/trials.csv`
- Method: `strombom_multi`
- Layout: compact
- N: {100, 200}
- D: claim windows (12 cells in `boundary_cells.csv`)
- Seeds: 100 on window cells
- Obs modes: bearing_only, local_positions, global
- Theta: 0.90
- T0: 10000
- Package export: E
- Commands (run in this order):
  1. Plan: `make -C scaling scaling-phase5-obs-claim-plan`
     Must run after this method's scout. Chooses scout cells near the reliability edge and writes `boundary_cells.csv` / `boundary_plan.json` (no claim sims yet).
  2. Reseed: `make -C scaling scaling-phase5-obs-claim-reseed WORKERS=18`
     Runs the claim sims (100 seeds) on those planned cells.

## Completeness

1,200 / 1,200 claim trials (`status.json` complete). Merge 1,920 rows (12 x 100 + 24 x 30). Mid-run pause left orphan manifest rows that were stripped before finishing.

## Runtime

Started:  7 Oct 2026, 12:46 UTC

Finished: 8 Oct 2026, 15:48 UTC

Total:    1d 3h 1m

## Results

Columns are obs mode (config). Rows are N.

| N | obs bearing_only | obs local_positions | obs global |
|---|------------------|---------------------|------------|
| 100 | hard failure | D_min = 1 | D_min = 1 |
| 200 | hard failure | D_min = 1 | D_min = 1 |

Package E summary (from `packages/e/substitution_summary_obs.csv`):

- `n_compared = 2`: number of N values with at least two defined `D_min` levels to compare.
- `median_delta_dmin = 0`: median over N of (`D_min` at richest obs mode minus `D_min` at poorest defined mode). Negative would mean richer obs needs fewer dogs.
- `supports_substitution = False`: C5a flag; true only when that median is negative.
- `supports_diminishing_returns = False`: C5b flag; true only when the first ladder step saves dogs and the second step saves fewer.

## Interpretation

Bearing-only cannot reach the 90% bar on the tested D band. Local positions already sit on the `D_min` = 1 floor; global observation does not reduce dog count further.

## Claims update

| Claim | What it asks (supported when) | Verdict | Evidence |
|-------|-------------------------------|---------|----------|
| C5a | One ladder step lowers `D_min` by at least one D-grid step at N in {100, 200} | REJECTED | no ladder step lowers a defined `D_min` by a grid step; `supports_substitution=False` |
| C5b | The second ladder step saves fewer dogs than the first | INCONCLUSIVE | no first-step dog saving among defined frontiers |

## Files in this folder

### Dependencies

```mermaid
flowchart LR
  scout["../factor_sweep/trials.csv"] -->|"plan"| plan["boundary_cells.csv<br/>boundary_plan.json"]
  plan -->|"reseed"| trials["trials.csv"]
  scout -->|"merge: non-window"| merge["merged_trials.csv"]
  trials -->|"merge: window"| merge
  merge --> pkgs["packages/e/"]
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
|-- scout_dmin_bootstrap_preview.csv
|-- status.json
|-- trials.csv
`-- packages/
    `-- e/
```

**Config**
- `protocol.yaml`: Run settings (method, layouts, N/D grid, seeds, grade).

**Planning (auto before claim / T1)**
- `boundary_cells.csv`: Cells chosen for 100-seed claim reseed (from scout).
- `boundary_plan.json`: Planner metadata for the claim window (theta, params).
- `scout_dmin_bootstrap_preview.csv`: Scout-side D_min bootstrap preview used while planning.

**Auto-generated (run)**
- `manifest.jsonl`: Per-cell progress log; enables resume without re-running ok cells.
- `merged_trials.csv`: Claim-window 100-seed rows + non-window scout 30-seed rows.
- `status.json`: Planned vs done counts, complete flag, start/finish, elapsed.
- `trials.csv`: One row per seed (success, ticks, path/effort, layout, N, D, ...).

**Auto-generated (analysis)**
- `dmin_bootstrap.csv`: Bootstrap of D_min / CI from claim trials only.
- `merged_dmin_bootstrap.csv`: Same bootstrap schema on merged_trials.csv.

**Auto-generated (analysis packages)**
- `packages/e/`: Package E (substitution / ladder tables).

Trajectory parquet written during the run is not retained here.

## Limits

Baseline method and compact layout only. Low-D band only. Hard failure under bearing_only is not scored as a numeric `D_min` decrease under C5a.
