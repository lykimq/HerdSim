# phase2_scout

## Purpose

SCOUT map of start-shape reliability: three flock sizes, four layouts, and the dog-count grid. Used to choose claim reseed windows. Not claim-grade by itself.

## Setup

- Protocol: `scaling_v2` (`phase2_scout`)
- Depends on: none required for running (pilot_state is smoke only). Writes `trials.csv`.
- Method: `strombom_multi`
- Layouts: compact, wide, split, outlier_rich
- N: {50, 100, 200}
- D: {1, 2, 3, 4, 6, 10, 15, 20, 25, 35}
- Seeds: 30
- Theta: 0.90
- T0: 10000
- Package export: B
- Command: `make -C scaling scaling-phase2-scout WORKERS=16`

## Completeness

3,600 / 3,600 trials (`status.json` complete).

## Runtime

Started:  25 Sep 2026, 09:25 UTC
Finished: 25 Sep 2026, 12:39 UTC
Total:    3h 13m

## Results

Scout-grade layout map. On this grid, `D_min = 1` for every layout x N cell; path effort rises sharply on wide and outlier_rich. Claim-grade fewest-dogs and bootstrap numbers live in `../claim/`.

## Files in this folder

### Dependencies

```mermaid
flowchart LR
  proto["protocol.yaml"] -->|"run"| trials["trials.csv"]
  trials --> status["status.json / manifest.jsonl"]
  trials --> pkgs["packages/b/"]
```

```
.
|-- manifest.jsonl
|-- protocol.yaml
|-- status.json
|-- trials.csv
`-- packages/
    `-- b/
```

**Config**
- `protocol.yaml`: Run settings (method, layouts, N/D grid, seeds, grade).

**Auto-generated (run)**
- `manifest.jsonl`: Per-cell progress log; enables resume without re-running ok cells.
- `status.json`: Planned vs done counts, complete flag, start/finish, elapsed.
- `trials.csv`: One row per seed (success, ticks, path/effort, layout, N, D, ...).

**Auto-generated (analysis packages)**
- `packages/b/`: Package B (structure / layout tables).

Trajectory parquet written during the run is not retained here.

## Limits

SCOUT (30 seeds). Not for claims.
