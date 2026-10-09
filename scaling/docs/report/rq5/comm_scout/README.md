# phase5_comm_scout

## Purpose

SCOUT communication ladder. Used to plan communication claim windows. Not claim-grade by itself.

## Setup

- Protocol: `scaling_v2` (`phase5_comm_scout`)
- Depends on: none for running. Starts the communication ladder. Writes `trials.csv`.
- Method: `strombom_multi`
- Layout: compact
- N: {100, 200}
- D: {1, 2, 3, 4, 6, 10}
- Seeds: 30
- Communications: none, neighbour_broadcast, global_shared
- Package export: E
- Command: `make -C scaling scaling-phase5-comm-scout WORKERS=18`

## Completeness

1,080 / 1,080 trials (`status.json` complete).

## Runtime

Started:  8 Oct 2026, 10:37 UTC
Finished: 8 Oct 2026, 11:56 UTC
Total:    1h 18m

## Results

Scout map for planning only. Claim-grade frontiers live in `../comm_claim/`.

## Files in this folder

### Dependencies

```mermaid
flowchart LR
  proto["protocol.yaml"] -->|"run"| trials["trials.csv"]
  trials --> status["status.json / manifest.jsonl"]
  trials --> pkgs["packages/e/"]
```

```
.
|-- manifest.jsonl
|-- protocol.yaml
|-- status.json
|-- trials.csv
`-- packages/
    `-- e/
```

**Config**
- `protocol.yaml`: Run settings (method, layouts, N/D grid, seeds, grade).

**Auto-generated (run)**
- `manifest.jsonl`: Per-cell progress log; enables resume without re-running ok cells.
- `status.json`: Planned vs done counts, complete flag, start/finish, elapsed.
- `trials.csv`: One row per seed (success, ticks, path/effort, layout, N, D, ...).

**Auto-generated (analysis packages)**
- `packages/e/`: Package E (substitution / ladder tables).

Trajectory parquet written during the run is not retained here.

## Limits

SCOUT (30 seeds). Not for claims.
