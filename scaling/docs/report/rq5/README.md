# RQ5: information vs shepherds

Question: can richer observation, sensing range, or communication lower the fewest-dogs answer at the same reliability?

Baseline method: `strombom_multi`. Layout: compact. N in {100, 200}. Three separate ladders (not every combination at once). Protocol: `scaling_v2`.

Story and numbers: [short report](../short_report.html). Frozen defaults: [../protocol/canonical_grid.yaml](../protocol/canonical_grid.yaml).

## Folders

| Folder | Grade | Role |
|--------|-------|------|
| [factor_sweep/](factor_sweep/) | SCOUT | Observation ladder scout |
| [obs_claim/](obs_claim/) | CLAIM | Observation claim windows |
| [range_scout/](range_scout/) | SCOUT | Sensing-range ladder scout |
| [range_claim/](range_claim/) | CLAIM | Range claim windows |
| [comm_scout/](comm_scout/) | SCOUT | Communication ladder scout |
| [comm_claim/](comm_claim/) | CLAIM | Communication claim windows |
| `run_all_ladders.sh` | helper | Sequential scout then claim for all three ladders |

## Common files inside each protocol folder

| File | Meaning |
|------|---------|
| `README.md` | Human note for that run |
| `protocol.yaml` | Frozen settings |
| `provenance.json` | Host, timestamps, protocol hash |
| `status.json` | Progress and completion |
| `manifest.jsonl` | Resume ledger |
| `trials.csv` | One row per simulation |
| `merged_trials.csv` | Claim merge (claim folders) |
| `packages/e/` | Package E substitution tables |

## Takeaway

Local sensing (radius 65) matches a full global view: both have `D_min = 1` at N = 100 and 200. Bearing-only, range, and communication ladders had setup problems that blocked a fair "does better information save dogs?" test. Claim C5a REJECTED; C5b INCONCLUSIVE.
