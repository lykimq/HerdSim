# phase4_fat_structure_claim

## Purpose

CLAIM reseed for the FAT four-layout structure map.

## Setup

- Protocol: `scaling_v2` (`phase4_fat_structure_claim`)
- Depends on: FAT structure scout (not blocked on RQ1/RQ2/RQ3).
  - Reads (plan): `../scout/trials.csv`
  - Writes: `boundary_cells.csv`, `boundary_plan.json`, then `trials.csv`
  - Merge: `merged_trials.csv` = claim `trials.csv` + non-window `../scout/trials.csv`
  - Later: `package_d/structure/` also needs RQ1 and Kubo claim merges
- Method: `fat`
- Layouts: compact, wide, split, outlier_rich
- N: {50, 100, 200}
- D: claim reliability window (see `boundary_cells.csv`)
- Seeds: 100
- Package export: B
- Commands (run in this order):
  1. Plan: `make -C scaling scaling-transfer-structure-claim-plan TRANSFER_METHOD=fat`
     Must run after this method's scout. Chooses scout cells near the reliability edge and writes `boundary_cells.csv` / `boundary_plan.json` (no claim sims yet).
  2. Reseed: `make -C scaling scaling-transfer-structure-claim-reseed TRANSFER_METHOD=fat WORKERS=16`
     Runs the claim sims (100 seeds) on those planned cells.

## Completeness

2,400 / 2,400 trials (`status.json` complete). Merge has 5,280 rows.

## Runtime

Started:  1 Oct 2026, 05:38 UTC
Finished: 2 Oct 2026, 05:16 UTC
Total:    23h 37m

## Results

Hard failure on all four layouts at N in {50, 100, 200} (no cell clears theta through D = 35).

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

CLAIM grade. Baseline transfer contrast for this method only.
