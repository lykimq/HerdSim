# phase4_kubo_size_scout

## Purpose

SCOUT Kubo compact size map. Used to plan claim windows. Not claim-grade by itself.

## Setup

- Protocol: `scaling_v2` (`phase4_kubo_size_scout`)
- Depends on: none for running. Starts the Kubo size chain. Writes `trials.csv`.
- Method: `kubo`
- Layout: compact
- N: {5, 10, 25, 50, 75, 100, 150, 200, 300, 400}
- D: {1, 2, 3, 4, 6, 10, 15, 20, 25, 35}
- Seeds: 30
- Package export: A, D, F
- Command: `make -C scaling scaling-transfer-size-scout TRANSFER_METHOD=kubo WORKERS=16`

## Completeness

3,000 / 3,000 trials (`status.json` complete).

## Runtime

Started:  25 Sep 2026, 16:12 UTC
Finished: 25 Sep 2026, 21:43 UTC
Total:    5h 31m

## Results

Scout size map on compact Kubo. Claim-grade frontiers live in the claim folder.

## Files in this folder

### Dependencies

```mermaid
flowchart LR
  proto["protocol.yaml"] -->|"run"| trials["trials.csv"]
  trials --> status["status.json / manifest.jsonl"]
  trials --> pkgs["packages/a+f/"]
```

```
.
|-- manifest.jsonl
|-- protocol.yaml
|-- status.json
|-- trials.csv
`-- packages/
    |-- a/
    `-- f/
```

**Config**
- `protocol.yaml`: Run settings (method, layouts, N/D grid, seeds, grade).

**Auto-generated (run)**
- `manifest.jsonl`: Per-cell progress log; enables resume without re-running ok cells.
- `status.json`: Planned vs done counts, complete flag, start/finish, elapsed.
- `trials.csv`: One row per seed (success, ticks, path/effort, layout, N, D, ...).

**Auto-generated (analysis packages)**
- `packages/a/`: Package A (size-map tables).
- `packages/f/`: Package F (scaling-fit tables).

Trajectory parquet written during the run is not retained here.

## Limits

SCOUT (30 seeds). Not for claims.
