# Protocol note: `rq2_claim`

## Summary

Careful reseed finished (resumed from 73/2200 after an earlier abort). 2200 claim trials on 22 reliability-window cells; the merge has 4540 rows (22 x 100 claim + 78 x 30 scout). Packages A and F written on `merged_trials.csv`. Frontier matches scout: fewest dogs (`D_min`)=2 for N in {5,10}, `D_min`=1 for N>=25. No overcrowding. Bootstrap band on `D_min` is one dog-list step for every N. This is the claim-grade size map for C2a (rejected: no overcrowding) and Package F diagnostics; T1 has no overcrowding cells.

## Intent

- RQ: RQ2
- Focus: Size (claim-grade `D_min` / regimes)
- Claims touched (C1a-C7b): C2a on this size map; C6a via Package F; C1a/C1b wait on RQ1 structure
- Grade: CLAIM

## Setup

- Protocol: `scaling_v2`
- Task / success rule: herd every sheep into the goal before the deadline (T0)
- Method(s): strombom_multi
- Layout(s) X0: compact
- N grid: full freeze (claim windows only)
- D grid: reliability window only (22 cells; see boundary_cells.csv)
- Seeds (scout / claim): 30 scout elsewhere / 100 on window cells
- T0 (and T1 if used): 10000 (T0 only)
- Theta: 0.90 (90% success bar)
- Command: `make -C scaling scaling-claim-reseed WORKERS=16` (resume)
- Output (this package): `rq2/claim/`
- Host: gwen (Ultra 7 165H, 61 GiB)
- WORKERS / CPU governor: 16 / performance

## Completeness

- Planned cells: 2200 claim trials
- Done: 2200 (`status.json` complete)
- `status.json` complete? yes
- Resume notes: first attempt stopped at 73; second run resumed (`n_pending_at_start` 2127); merge 4540 rows

## Runtime

From `status.json` (`elapsed_seconds` for the completed claim process that finished the grid):

| Field | Value |
|-------|-------|
| Elapsed | 3,451 s (0h 57m 31s) |
| Started (UTC) | 2026-09-22T12:07:52Z |
| Updated (UTC) | 2026-09-22T13:05:23Z |

Note: elapsed covers the resumed run that completed the remaining trials, not a sum of the aborted first attempt.

## Results

- Success pattern: merged overall success 0.963 (4371 wins / 4540); under-resource failures still at small N with D=1; rare failures are oscillation (111) or stuck (58)
- Fewest dogs / frontier (by N / layout): compact `D_min`=2 (N=5,10), `D_min`=1 (N>=25); no `D_overcrowd`; `d_max`=35
- Regimes: wasteful_overspend 88, efficient_operation 10, under_resourced_failure 2
- Surprises: still no overcrowding at theta=0.9 on compact+strombom_multi
- Bootstrap: `d_min_ci_low` == `d_min_ci_high` for all N at 100 seeds
- Package F (auto): best_model=piecewise; prefers_piecewise_or_state=True (degenerate two-level fit {2, 1} with break at N=10)

## Interpretation

The careful map confirms the scout story: one dog is enough for N>=25 on a compact start under T0; N=5 and N=10 need at least 2 dogs. High dog counts are wasteful rather than overcrowded, so C2a is rejected on this size map (and T1 has no overcrowding cells to run). Scaling fits lean piecewise (Package F); treat C6a as evaluated but weak (not a real scaling law).

## Limits

Single method, single layout. No overcrowding window, so no T1 overcrowding campaign from this plan. Merge mixes 100-seed claim cells with 30-seed scout cells elsewhere (by design). Layout-shift claims (C1a/C1b) need RQ1; transfer claims need RQ4. Timeseries parquet are not included in this package; RQ7 summary tables are under ../rq7/.

## Claims update

CLAIM grade. Verdict summary is in `../../short_report.md` (Claims section).

| Claim | Verdict | Evidence |
|-------|---------|----------|
| C2a | REJECTED | `packages/a/`: 0 overcrowding cells / no `D_overcrowd` at theta=0.90 |
| C2b | SKIPPED | needs T1; no overcrowding cells |
| C6a | SUPPORTED | `packages/f/scaling_cv.csv`: leave-one-N RMSE power 0.247 > piecewise 0.132 |
| C6b | SUPPORTED | compact N in {25..400}: D_min=1 flat (slope 0 < 1); `scaling_fits.csv` power log_log_slope = -0.165 |
| C7a | INCONCLUSIVE | `packages/g/`: held-out state and (N, D) AUROC are null; folds empty; `beats_nd_baseline=False` |
| C7b | REJECTED | `packages/g/early_warning_summary.csv`: frac_lead_ge_500 = 0.083 (< 0.30); 14/169 failures have lead time |

## Next

- T1 (long-deadline follow-up) was skipped because no overcrowding cells were found: see `../t1/README.md`.
- Scaling fits (RQ6) live in `../../rq6/`.
- Early warning (RQ7) lives in `../../rq7/`.

## Files in this folder

| Path | Meaning | Contents |
|------|---------|----------|
| `README.md` | This protocol note | Setup, runtime, results, claims, file map |
| `protocol.yaml` | Frozen config used for the run | Method, grids, seeds, theta, T0, timeseries flag |
| `provenance.json` | Reproducibility stamp | Protocol id, git commit, host/platform, timestamps |
| `status.json` | Run progress | `n_planned`, `n_done`, `complete`, `elapsed_seconds`, start/update times |
| `manifest.jsonl` | Resume ledger | One JSON line per cell; `status=ok` rows are skipped on re-run |
| `trials.csv` | Trial-level results | One row per seed: N, D, layout, success, ticks, path/effort metrics, failure tags, etc. |
| `packages/` | Analysis exports | Auto tables from `scaling-analyse` (derived figures are not included in this email package); see `packages/*/README.md` |

| `boundary_cells.csv` | Claim window plan | Cells selected for 100-seed reseed (`n_sheep`, `n_shepherds`, role, scout reliability) |
| `boundary_plan.json` | Plan metadata | How the boundary list was produced (theta, source scout, counts) |
| `merged_trials.csv` | Claim-grade merge | Window cells at 100 seeds plus non-window scout rows at 30 seeds (same columns as `trials.csv`) |
| `dmin_bootstrap.csv` | Bootstrap on claim trials | Point `d_min` and CI per N (and layout if present) |
| `merged_dmin_bootstrap.csv` | Bootstrap on merge | Same schema on `merged_trials.csv` |
| `timeseries/` | Per-trial trajectories | Not included in this email package |

### `packages/` detail

| Path | Meaning |
|------|---------|
| `packages/a/README.md` | Package A summary (auto) |
| `packages/a/reliability.csv` | R(N, D) rates |
| `packages/a/frontier.csv` | D_min / D_overcrowd / D_max |
| `packages/a/regimes.csv` | Regime labels per cell |
| `packages/a/dmin_bootstrap.csv` | Bootstrap copy used by the package |
| `packages/` | Package exports | This folder contains Package A for the RQ2 size map |

## Links

- Package A: `packages/a/README.md`
- `merged_trials.csv`, `status.json`, `provenance.json`, `protocol.yaml`, `boundary_cells.csv`
- Phase index: `../README.md`
