# Phase 2: start-shape map

Question in plain terms: if flock size is fixed, does a different sheep layout at the start change how many dogs we need?

Baseline method: `strombom_multi`. Layouts: compact, wide, split, outlier_rich. Protocol: `scaling_v2`. Cross-phase context: [main scaling plan](../../docs/main_scaling_plan.html) and [results summary](../summary/SUMMARY_REPORT.html).

## Folders

| Folder | Grade | Role |
|--------|-------|------|
| [pilot_state/](pilot_state/) | SMOKE | Layout / metrics smoke (600 trials) |
| [scout/](scout/) | SCOUT | Cheap 3 N x 4 layouts x D map (3,600 trials) |
| [claim/](claim/) | CLAIM | Careful reseed near edges (2,400 trials; merge 5,280) |
| [guides/](guides/) | reader | `REPORT_en.html`, `REPORT_vi.html`, shared `assets/` |

## Runtime

Sum of each protocol `status.json` `elapsed_seconds`:

| Protocol | Elapsed | Source |
|----------|---------|--------|
| pilot_state | 421 s (0h 7m 1s) | `pilot_state/status.json` |
| scout | 11,633 s (3h 13m 53s) | `scout/status.json` |
| claim | 10,757 s (2h 59m 17s) | `claim/status.json` |
| **Phase 2 sim total** | **22,811 s (6h 20m 11s)** | sum of rows above |

## Files and folders

| Path | Meaning |
|------|---------|
| `README.md` | Phase index (this file) |
| `pilot_state/` | SMOKE protocol folder (see `pilot_state/README.md`) |
| `scout/` | SCOUT protocol folder (see `scout/README.md`) |
| `claim/` | CLAIM protocol folder + merge + Package B (see `claim/README.md`) |
| `guides/` | Reader HTML: `REPORT_en.html`, `REPORT_vi.html`, shared `assets/` (`figures/`, `layouts/`) |

### Common files inside each protocol folder

| File | Meaning |
|------|---------|
| `protocol.yaml` | Frozen run config |
| `provenance.json` | Git/host stamp |
| `status.json` | Progress + `elapsed_seconds` |
| `manifest.jsonl` | Resume ledger |
| `trials.csv` | One row per trial |
| `packages/` | Analyse exports (Package B) |
| `timeseries/` | Not retained in this phase after cleanup |

Claim-only extras: `boundary_*.csv/json`, `merged_trials.csv`, `*dmin_bootstrap.csv`.

## Claim-grade takeaways

Cited in [claim/README.md](claim/README.md) and `claim/packages/b/`:

- Fewest dogs (`D_min`) = 1 on compact, split, outlier_rich, and wide at N in {50, 100, 200}
- Cost rises on wide and outlier_rich; on wide, the cheap good setup (`B*`) = 2 while `D_min` stays 1
- C1a REJECTED; C1b INCONCLUSIVE

## Cross-phase

- Main scaling plan: [../../docs/main_scaling_plan.html](../../docs/main_scaling_plan.html)
- Results summary: [../summary/SUMMARY_REPORT.html](../summary/SUMMARY_REPORT.html)
- Documentation: [index](../../docs/INDEX.html), [methods](../../docs/methods/README.html), [setup](../../docs/setup/README.html), [credibility](../../docs/credibility/README.html)
- Data appendices: [Phase 2 tables](../summary/data/phase2_tables.html), [run ledger](../summary/data/run_ledger.html)
- Tracker: [../../docs/progress_tracker.md](../../docs/progress_tracker.md)
