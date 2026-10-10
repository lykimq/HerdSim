# Protocol note: `phase1_scout`

## Summary

Cheap full size map finished: 3000/3000 trials. Packages A and F written. On compact starts with `strombom_multi`, overall success is high (R=0.983). Fewest dogs (`D_min`) is 2 for N in {5,10} and 1 for N>=25. No overcrowding regime on this export. The bootstrap band on `D_min` is only one dog-list step for every N, so we do not need a 200-seed raise before claim. Planning only: not for claims.

## Intent

- Phase / RQ: Phase 1 / RQ2
- Focus: Size (reliability map used to pick claim windows)
- Claims touched (C1a-C7b): none (SCOUT; planning only)
- Grade: SCOUT

## Setup

- Protocol: `scaling_v2`
- Task / success rule: herd every sheep into the goal before the deadline (T0)
- Method(s): strombom_multi
- Layout(s) X0: compact
- N grid: 5, 10, 25, 50, 75, 100, 150, 200, 300, 400
- D grid: 1, 2, 3, 4, 6, 10, 15, 20, 25, 35
- Seeds (scout / claim): 30 (scout)
- T0 (and T1 if used): 10000 (T0 only)
- Theta: 0.90 (90% success bar)
- Command: `make -C scaling scaling-scout WORKERS=16`
- Output: `scaling/results/phase1/scout/`
- Host: gwen (Ultra 7 165H, 61 GiB)
- WORKERS / CPU governor: 16 / performance

## Completeness

- Planned cells: 3000
- Done: 3000
- `status.json` complete? yes
- Resume notes: first full run; analyse A+F succeeded

## Runtime

From `status.json` (`elapsed_seconds`):

| Field | Value |
|-------|-------|
| Elapsed | 4,359 s (1h 12m 39s) |
| Started (UTC) | 2026-09-22T10:50:18Z |
| Updated (UTC) | 2026-09-22T12:02:57Z |

## Results

- Success pattern: R=1.0 for all N>=25; lower only at N=5 (0.903) and N=10 (0.927), driven by D=1 under-resourcing
- Fewest dogs / frontier (by N / layout): compact `D_min`=2 (N=5,10), `D_min`=1 (N>=25); `d_max`=35; no `D_overcrowd`
- Regimes: wasteful_overspend 88, efficient_operation 10, under_resourced_failure 2
- Surprises: no overcrowding at theta=0.9 on this scout; failures are oscillation/stuck at small N; ticks usually short (median 182) with rare 10000 caps
- Bootstrap: `d_min_ci_low` == `d_min_ci_high` for every N (no multi-step CI)
- Package F (auto): best_model=piecewise by leave-one-N RMSE; prefers_piecewise_or_state=True (SCOUT only; not for Claims)

## Interpretation

On a compact start, one dog is enough for N>=25 under T0; tiny flocks need at least 2 dogs. High dog counts mostly look wasteful (more walking) rather than overcrowded (success drops). Claim windows should sit around the fewest-dogs edge.

## Limits

SCOUT: 30 seeds, one method, one layout. Not for Claims. Timeseries parquet from this scout are not retained.

## Claims update

CLAIM grade only. Skipped for SCOUT.

## Next

- Claim plan + reseed in `../claim/`
- Phase index: `../README.md`
- Main scaling plan: [../../../docs/main_scaling_plan.md](../../../docs/main_scaling_plan.md)

## Files in this folder

| Path | Meaning | Contents |
|------|---------|----------|
| `README.md` | This protocol note | Setup, runtime, results, claims, file map |
| `protocol.yaml` | Frozen config used for the run | Method, grids, seeds, theta, T0, timeseries flag |
| `provenance.json` | Reproducibility stamp | Protocol id, git commit, host/platform, timestamps |
| `status.json` | Run progress | `n_planned`, `n_done`, `complete`, `elapsed_seconds`, start/update times |
| `manifest.jsonl` | Resume ledger | One JSON line per cell; `status=ok` rows are skipped on re-run |
| `trials.csv` | Trial-level results | One row per seed: N, D, layout, success, ticks, path/effort metrics, failure tags, etc. |
| `packages/` | Analysis exports | Auto tables from `scaling-analyse` (figures under `docs/figures/packages/`) (Package A/B/F/...); see `packages/*/README.md` |
| `timeseries/` | (not retained) | Parquet trajectories were removed after analysis to save disk; CSV/packages remain |

Packages: `packages/a/` (size map), `packages/f/` (scaling-fit diagnostics on scout frontiers).

## Links

- Package A: `packages/a/README.md`
- Package F: `packages/f/README.md`
- `status.json`, `provenance.json`, `protocol.yaml`, `trials.csv`
