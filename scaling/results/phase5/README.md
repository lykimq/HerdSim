# Phase 5: information ladders

Question in plain terms: can richer observation, sensing range, or communication lower the fewest-dogs answer at fixed reliability?

Baseline method: `strombom_multi`. Layout: compact. Protocol: `scaling_v2`. Cross-phase context: [main scaling plan](../../docs/main_scaling_plan.html) and [results summary](../summary/SUMMARY_REPORT.html).

Three separate ladders (not a Cartesian product). Host: gwen. Workers: 18. CPU governor: performance.

## Folders

| Folder | Grade | Role | Status |
|--------|-------|------|--------|
| [factor_sweep/](factor_sweep/) | SCOUT | Observation ladder scout (bearing / local / global) | DONE |
| [obs_claim/](obs_claim/) | CLAIM | Observation claim windows | DONE |
| [range_scout/](range_scout/) | SCOUT | Sensing-range ladder scout | DONE |
| [range_claim/](range_claim/) | CLAIM | Range claim windows | DONE |
| [comm_scout/](comm_scout/) | SCOUT | Communication ladder scout | DONE |
| [comm_claim/](comm_claim/) | CLAIM | Communication claim windows | DONE |

## Runtime

Elapsed values are `elapsed_seconds` from each protocol `status.json`. Obs scout/claim elapsed spans an overnight pause/resume gap; range and comm are continuous.

| Protocol | Elapsed | Human |
|----------|--------:|-------|
| factor_sweep (obs scout) | 78,955 s | 21h 55m 55s (includes pause gap) |
| obs_claim | 75,342 s | 20h 55m 42s (includes pause gap) |
| range_scout | 1,495 s | 0h 24m 55s |
| range_claim | 1,834 s | 0h 30m 34s |
| comm_scout | 4,726 s | 1h 18m 46s |
| comm_claim | 1,295 s | 0h 21m 35s |
| **Phase 5 status.json sum** | **163,647 s** | **1d 21h 27m 27s** |

## Setup snapshot

- N: {100, 200}
- D (low band): {1, 2, 3, 4, 6, 10}
- Seeds: 30 scout / 100 claim
- Observation modes: bearing_only, local_positions, global
- Sensing ranges: 32.5, 65.0, 97.5, 130.0 (0.5x to 2x r_s)
- Communications: none, neighbour_broadcast, global_shared
- Orchestrator: `bash scaling/results/phase5/run_all_ladders.sh` with `WORKERS=18`

## Claim-grade takeaways

Cited in claim-folder READMEs and Package E under each `*_claim/packages/e/`:

- Observation: `bearing_only` hard-fails at N in {100, 200}; `local_positions` and `global` both have `D_min` = 1
- Range: `D_min` = 1 at every tested sensing range for both N
- Communication: `D_min` = 1 at none / neighbour_broadcast / global_shared for both N
- C5a REJECTED: no ladder step lowers a defined `D_min` by a D-grid step
- C5b INCONCLUSIVE: no first-step dog saving to test diminishing returns

## Files and folders

| Path | Meaning |
|------|---------|
| `README.md` | Phase index (this file) |
| `run_all_ladders.sh` | Sequential scout then claim for all three ladders |
| `factor_sweep/` | Observation SCOUT |
| `obs_claim/` | Observation CLAIM |
| `range_scout/` | Range SCOUT |
| `range_claim/` | Range CLAIM |
| `comm_scout/` | Communication SCOUT |
| `comm_claim/` | Communication CLAIM |

### Common files inside each protocol folder

| File | Meaning |
|------|---------|
| `README.md` | Protocol note |
| `protocol.yaml` | Frozen run config |
| `provenance.json` | Git/host stamp |
| `status.json` | Progress + `elapsed_seconds` |
| `manifest.jsonl` | Resume ledger |
| `trials.csv` | One row per trial |
| `packages/e/` | Package E substitution tables |
| `merged_trials.csv` | Claim merge (claim folders only) |

## Cross-phase

- Main scaling plan: [../../docs/main_scaling_plan.html](../../docs/main_scaling_plan.html)
- Results summary: [../summary/SUMMARY_REPORT.html](../summary/SUMMARY_REPORT.html)
- Tracker: [../../docs/progress_tracker.md](../../docs/progress_tracker.md)
- Run guide: [../../docs/setup/run_guide.html](../../docs/setup/run_guide.html)
