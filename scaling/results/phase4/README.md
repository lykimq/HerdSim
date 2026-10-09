# Protocol note: Phase 4 transfer (Package D)

## Summary

Question in plain terms: do the same fewest-dogs answers show up with other dog rules (Kubo, FAT), or are they special to the baseline?

Claim-grade size and structure maps for `kubo` and `fat`, compared to baseline `strombom_multi`. Size map: Kubo shares `D_min` = 1 with the baseline for N >= 25; FAT hard-fails for N >= 25. Structure map: Kubo matches on compact and split; hard-fails on wide; outlier_rich N=200 shifts to `D_min` = 20 (200 seeds on D in {1,2,3,4,6,10,15,20,25}; bootstrap [2, 20]). FAT hard-fails on every structure cell. C4 supported only in part.

Cross-phase context: [main scaling plan](../../docs/main_scaling_plan.md).

## Intent

- Phase / RQ: Phase 4 / RQ4
- Focus: Generality / transfer across controllers
- Claims touched (C1a-C7b): C4
- Grade: CLAIM

## Setup

- Protocol: `scaling_v2`
- Task / success rule: herd every sheep into the goal before the deadline (T0)
- Method(s): strombom_multi (baseline), kubo, fat
- Layout(s) X0: compact (size); compact, split, outlier_rich, wide (structure)
- N grid: size {5..400}; structure {50, 100, 200}
- D grid: [1, 35] scout; claim windows reseeds
- Seeds (scout / claim): 30 scout / 100 claim; Kubo outlier_rich N=200 uses 200 seeds on D in {1,2,3,4,6,10,15,20,25}
- T0: 10000
- Theta: 0.90 (90% success bar)
- Commands: `make -C scaling scaling-transfer-size-*` and `scaling-transfer-structure-*` with `TRANSFER_METHOD=kubo` then `fat`
- Output: `scaling/results/phase4/`
- Host: gwen (Ultra 7 165H, 61 GiB)

## Completeness

| Protocol folder | Claim trials | Merged rows | Complete |
|-----------------|-------------:|------------:|----------|
| `kubo_size/claim` | 2100 | 4470 | yes |
| `fat_size/claim` | 2000 | 4400 | yes |
| `kubo_structure/claim` | 4000 | 6670 | yes |
| `fat_structure/claim` | 2400 | 5280 | yes |

Package D tables: `package_d/size/`, `package_d/structure/`. Kubo outlier_rich N=200 window snapshot: `kubo_structure/claim/outlier_rich_n200_window.json`.

## Runtime

Elapsed values are `elapsed_seconds` from each protocol `status.json` (process timer; may include resume wall time). Snapshot below was read when this README was written; re-check `status.json` if a run is still marked `running`.

| Protocol | Elapsed | Human |
|----------|--------:|-------|
| kubo_size/scout | 19,897 s | 5h 31m 36s |
| kubo_size/claim | 16,069 s | 4h 27m 48s |
| kubo_structure/scout | 59,977 s | 16h 39m 36s |
| kubo_structure/claim | 835,308 s | 9d 16h 1m 48s |
| fat_size/scout | 140,772 s | 1d 15h 6m 11s |
| fat_size/claim | 448,955 s | 5d 4h 42m 34s |
| fat_structure/scout | 122,406 s | 1d 10h 0m 5s |
| fat_structure/claim | 85,049 s | 23h 37m 29s |
| **Phase 4 sim total** | **1,728,431 s** | **20d 0h 7m 11s** |

## Results

### Size map (compact)

- Kubo: `D_min` = 3 at N=5; `D_min` = 1 at N=10 and for N >= 25 through 400; no overcrowding
- FAT: `D_min` = 1 at N <= 10; hard failure for N >= 25 through 400 (R never reaches 0.90 for any D <= 35)
- Strombom baseline (Phase 1): `D_min` = 2 at N in {5,10}, `D_min` = 1 for N >= 25

### Structure map (N in {50, 100, 200})

From `package_d/structure/frontier_by_method_layout.csv`:

| Layout | Strombom | Kubo | FAT |
|--------|----------|------|-----|
| compact | D_min = 1 | D_min = 1 | hard failure |
| split | D_min = 1 | D_min = 1 | hard failure |
| outlier_rich | D_min = 1 | D_min = 1 at N=50,100; D_min = 20 at N=200 | hard failure |
| wide | D_min = 1 | hard failure (best R about 0.47 to 0.54) | hard failure (R = 0) |

Kubo outlier_rich N=200 rates: D1 0.745, D2 0.855, D3 0.835, D4 0.860, D6 0.890, D10 0.875, D15 0.855, D20 0.935, D25 0.910 (all 200 seeds); D35 0.967 (30 seeds). Bootstrap on D_min: [2, 20]. No overcrowding.

We label each comparison **shared** (same answer), **shifted** (different dog count), or **absent** (one side never reaches 90% success).

## Interpretation

Transfer is not automatic. Kubo shares the compact size frontier for mid/large N, but structure breaks generality: wide never clears the 90% bar, and large outlier_rich needs more dogs (`D_min` = 20). FAT does not transfer under `obs_mode=global` for N >= 25. Size-only transfer would overstate C4; the structure map is the binding contrast.

## Limits

Kubo outlier_rich N=200 D_min bootstrap stays wide ([2, 20]) because several D < 20 sit near theta. D = 35 on that row remains at 30 seeds. No overcrowding cells for any method/layout in these maps. Observation mode fixed to global (Phase 5 ladders not run). Phase 4 timeseries parquet are not retained.

## Claims update

CLAIM grade. Aligned with `scaling/docs/progress_tracker.md`:

| Claim | Verdict | Evidence |
|-------|---------|----------|
| C4 | SUPPORTED (partial) | Measured CSVs only (not docs): `package_d/size/transfer_summary.csv`, `package_d/structure/frontier_by_method_layout.csv`, kubo/fat size+structure claim Package A / merges. Shared on compact N>=25 (Strombom/Kubo); Kubo wide absent; Kubo outlier_rich N=200 shifted to D_min=20; FAT absent for N>=25. Partial because transfer is mixed, not universal. |

## Next

- Tracker steps 11-13 DONE; Phase 5 still TODO
- Final report: [../../docs/final_report.md](../../docs/final_report.md)

## Files and folders

| Path | Meaning |
|------|---------|
| `README.md` | This phase note (setup, runtime, results, claims) |
| `kubo_size/` | Kubo size scout + claim protocol trees |
| `kubo_structure/` | Kubo structure scout + claim (`claim/README.md`, `scout/README.md`) |
| `fat_size/` | FAT size scout + claim |
| `fat_structure/` | FAT structure scout + claim |
| `package_d/` | Package D transfer tables (`size/`, `structure/`) |

### Inside each `{method}_{size|structure}/{scout|claim}/` folder

| Path | Meaning | Contents |
|------|---------|----------|
| `README.md` | Protocol note (when present) | Current numbers for that scout/claim tree |
| `protocol.yaml` | Frozen config | Method, grids, seeds, theta |
| `provenance.json` | Reproducibility stamp | Commit, host, timestamps |
| `status.json` | Run progress | Counts, `complete`, `elapsed_seconds` |
| `manifest.jsonl` | Resume ledger | One line per cell |
| `trials.csv` | Trials for that stage | One row per seed |
| `merged_trials.csv` | Claim merge (claim folders) | Claim + scout rows for analysis |
| `boundary_cells.csv` / `boundary_plan.json` | Claim window plan | Cells chosen for denser reseed |
| `*dmin_bootstrap.csv` | Bootstrap frontiers | Point D_min and CI |
| `packages/` | Package A or B exports | Frontiers, reliability, figures |
| `timeseries/` | (not retained) | Parquet removed after Phase 4 cleanup |

### Kubo structure claim extras

| Path | Meaning |
|------|---------|
| `outlier_rich_n200_window.json` | Current rates, D_min, and bootstrap for outlier_rich N=200 |

### `package_d/` detail

| Path | Meaning |
|------|---------|
| `size/README.md` | Size-transfer package note (auto) |
| `size/transfer_table.csv` / `transfer_summary.csv` | Shared / shifted / absent on size map |
| `size/{strombom_multi,kubo,fat}_trials.csv` | Method trial tables used for transfer |
| `structure/README.md` | Structure-transfer package note |
| `structure/frontier_by_method_layout.csv` | D_min / hard_failure by method x layout x N |
| `structure/transfer_*.csv` | Per-layout transfer slices (`compact`, `wide`, ...) |

## Links

- Package D size: `package_d/size/README.md`
- Package D structure: `package_d/structure/` (`frontier_by_method_layout.csv`, `transfer_*.csv`)
- Per-method Package A/B: `{kubo,fat}_{size,structure}/claim/packages/`
- Window snapshot: `kubo_structure/claim/outlier_rich_n200_window.json`
- Final report: [../../docs/final_report.md](../../docs/final_report.md)
- Main scaling plan: [../../docs/main_scaling_plan.md](../../docs/main_scaling_plan.md)
- Tracker: [../../docs/progress_tracker.md](../../docs/progress_tracker.md)
