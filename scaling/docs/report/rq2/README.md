# RQ2: flock size map

Question: on a tight (compact) start with the baseline dog rule, how many dogs do we need as the flock gets larger?

Baseline method: `strombom_multi`. Protocol: `scaling_v2`.

Story and numbers: [short report](../short_report.html). Frozen defaults: [../protocol/canonical_grid.yaml](../protocol/canonical_grid.yaml).

## Folders

| Folder | Grade | Role |
|--------|-------|------|
| [pilot/](pilot/) | SMOKE | Pipeline check (150 trials) |
| [scout/](scout/) | SCOUT | Cheap full N x D map (3,000 trials) |
| [claim/](claim/) | CLAIM | Careful reseed near the fewest-dogs edge (2,200 trials; merge 4,540) |
| [t1/](t1/) | plan only | Longer deadline for overcrowding (0 cells; no sims) |

Scaling-fit tables (RQ6) and early-warning tables (RQ7) live in sibling folders [`../rq6/`](../rq6/) and [`../rq7/`](../rq7/), not under claim/packages here.

## Common files inside each protocol folder

| File | Meaning |
|------|---------|
| `README.md` | Human note for that run |
| `protocol.yaml` | Frozen settings for that run |
| `provenance.json` | Host, timestamps, protocol hash |
| `status.json` | Progress and whether the run finished |
| `manifest.jsonl` | Resume ledger |
| `trials.csv` | One row per simulation |
| `packages/` | Analysis exports (Package A under claim) |

Claim-only extras: `boundary_*.csv/json`, `merged_trials.csv`, `*dmin_bootstrap.csv`.

Trajectory parquet files (`timeseries/`) are not included in this package.

## Takeaway

`D_min = 2` for N in {5, 10}; `D_min = 1` for N >= 25. No overcrowding inside D <= 35. Extra dogs mostly add walking (waste), not failure. Claim C2a REJECTED; C2b SKIPPED.
