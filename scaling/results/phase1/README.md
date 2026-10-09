# Phase 1: flock size map

Question in plain terms: on a tight (compact) start with the baseline dog rule, how many dogs do we need as the flock gets larger?

Baseline method: `strombom_multi`. Protocol: `scaling_v2`. Cross-phase context: [main scaling plan](../../docs/main_scaling_plan.md).

## Folders

| Folder | Grade | Role |
|--------|-------|------|
| [pilot/](pilot/) | SMOKE | Pipeline check (150 trials) |
| [scout/](scout/) | SCOUT | Cheap full N x D map (3,000 trials) |
| [claim/](claim/) | CLAIM | Careful reseed near the fewest-dogs edge (2,200 trials; merge 4,540) |
| [t1/](t1/) | plan only | Longer deadline for overcrowding (0 cells; no sims) |

## Runtime

Sum of each protocol `status.json` `elapsed_seconds`:

| Protocol | Elapsed | Source |
|----------|---------|--------|
| pilot | 43 s (0h 0m 43s) | `pilot/status.json` |
| scout | 4,359 s (1h 12m 39s) | `scout/status.json` |
| claim | 3,451 s (0h 57m 31s) | `claim/status.json` (resumed completion run) |
| t1 | n/a (plan only) | no sim grid |
| **Phase 1 sim total** | **7,853 s (2h 10m 53s)** | sum of rows above |

## Files and folders

| Path | Meaning |
|------|---------|
| `README.md` | Phase index (this file) |
| `pilot/` | SMOKE protocol folder (see `pilot/README.md`) |
| `scout/` | SCOUT protocol folder (see `scout/README.md`) |
| `claim/` | CLAIM protocol folder + merge + packages (see `claim/README.md`) |
| `t1/` | T1 overcrowding plan only (see `t1/README.md`) |

### Common files inside each protocol folder

| File | Meaning |
|------|---------|
| `protocol.yaml` | Frozen run config |
| `provenance.json` | Git/host stamp |
| `status.json` | Progress + `elapsed_seconds` |
| `manifest.jsonl` | Resume ledger |
| `trials.csv` | One row per trial |
| `packages/` | Analyse exports (A/F/...) |
| `timeseries/` | Optional parquet trajectories (kept only under `claim/` here) |

Claim-only extras: `boundary_*.csv/json`, `merged_trials.csv`, `*dmin_bootstrap.csv`.

## Claim-grade takeaways

Cited in [claim/README.md](claim/README.md) and packages under `claim/packages/`:

- Merge overall R = 0.963 (4,371 / 4,540) in `claim/merged_trials.csv` (R = share of repeats that succeed)
- Fewest dogs (`D_min`) = 2 for N in {5, 10}; `D_min` = 1 for N >= 25; no overcrowding (`D_overcrowd`) at the 90% bar (theta = 0.90)
- C2a REJECTED; C2b SKIPPED; C6a EVALUATED (weak) via Package F

## Cross-phase

- Final report: [../../docs/final_report.md](../../docs/final_report.md)
- Main scaling plan: [../../docs/main_scaling_plan.md](../../docs/main_scaling_plan.md)
- Tracker: [../../docs/progress_tracker.md](../../docs/progress_tracker.md)
