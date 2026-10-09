# RQ1: start shape (structure)

Question: at the same flock size, does the starting layout of the sheep change how many dogs you need?

Baseline method: `strombom_multi`. Layouts: compact, wide, split, outlier_rich. Protocol: `scaling_v2`.

Story and numbers: [short report](../short_report.html). Frozen defaults: [../protocol/canonical_grid.yaml](../protocol/canonical_grid.yaml).

## Folders

| Folder | Grade | Role |
|--------|-------|------|
| [pilot_state/](pilot_state/) | SMOKE | Layout / metrics smoke check (600 trials) |
| [scout/](scout/) | SCOUT | Cheap 3 N x 4 layouts x D map (3,600 trials) |
| [claim/](claim/) | CLAIM | Careful reseed near edges (2,400 trials; merge 5,280) |

## Common files inside each protocol folder

| File | Meaning |
|------|---------|
| `README.md` | Human note for that run (setup, counts, takeaways) |
| `protocol.yaml` | Frozen settings for that run |
| `provenance.json` | Host, timestamps, protocol hash |
| `status.json` | Progress and whether the run finished |
| `manifest.jsonl` | Resume ledger (finished trials are skipped on re-run) |
| `trials.csv` | One row per simulation |
| `packages/` | Analysis tables (Package B under claim) |

Claim-only extras: `boundary_*.csv/json`, `merged_trials.csv`, `*dmin_bootstrap.csv`.

## Takeaway

On the baseline, `D_min = 1` for all four layouts at N in {50, 100, 200}. Start shape changes time and path cost, not the fewest-dogs answer at the 90% bar. Claim C1a REJECTED; C1b INCONCLUSIVE.
