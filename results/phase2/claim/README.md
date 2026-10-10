# Protocol note: `phase2_claim`

## Summary

Careful reseed finished: 2400 claim trials on 24 reliability-window cells; the merge has 5280 rows. Package B written on `merged_trials.csv`. Fewest dogs (`D_min`) = 1 on all four layouts at N in {50, 100, 200}; bootstrap band is one dog-list step everywhere. Cost (`B*` path / time at D=1) rises sharply on wide and outlier_rich, but success does not fall below the 90% bar. C1a rejected; C1b inconclusive (no `D_min` shift to explain).

## Intent

- Phase / RQ: Phase 2 / RQ1
- Focus: Structure (`D_min` and cost across initial_layout)
- Claims touched (C1a-C7b): C1a, C1b
- Grade: CLAIM

## Setup

- Protocol: `scaling_v2`
- Task / success rule: herd every sheep into the goal before the deadline (T0)
- Method(s): strombom_multi
- Layout(s) X0: compact, split, outlier_rich, wide
- N grid: {50, 100, 200}
- D grid: reliability window (24 cells; see boundary_cells.csv)
- Seeds (scout / claim): 30 scout elsewhere / 100 on window cells
- T0 (and T1 if used): 10000 (T0 only)
- Theta: 0.90 (90% success bar)
- Command: `make -C scaling scaling-phase2-claim-reseed WORKERS=16`
- Output: `scaling/results/phase2/claim/`
- Host: gwen (Ultra 7 165H, 61 GiB)
- WORKERS / CPU governor: 16 / performance

## Completeness

- Planned cells: 2400 claim trials
- Done: 2400 (`status.json` complete)
- `status.json` complete? yes
- Resume notes: finished in one session; merge 5280 rows; overall success 1.0 on the merge

## Runtime

From `status.json` (`elapsed_seconds`):

| Field | Value |
|-------|-------|
| Elapsed | 10,757 s (2h 59m 17s) |
| Started (UTC) | 2026-09-25T12:40:20Z |
| Updated (UTC) | 2026-09-25T15:39:37Z |

## Results

- Success pattern: R = 1.0 at D = 1 for every layout x N cell on the claim windows
- Fewest dogs / frontier: `D_min` = 1 for compact, split, outlier_rich, wide at N in {50, 100, 200}; no `D_overcrowd`; `d_max` = 35
- Cheap good setup (`B*`) effort (from `packages/b/frontier_by_layout.csv`):
  - compact / split: about 144 to 162 path units at B*_d = 1
  - outlier_rich: 209 (N=50) to 1647 (N=200) at B*_d = 1
  - wide: 2337 to 3694 path units; B*_d shifts to 2 (cost minimum), while `D_min` stays 1
- Bootstrap: `d_min_ci_low` == `d_min_ci_high` for all layout x N at 100 seeds
- Predictor (Package B auto): prefers_state=False; NLL comparison not informative when `D_min` is flat

## Interpretation

Start shape changes work (walking and time), not dog count, on this baseline controller and T0. Wide and outlier_rich starts stretch path length and time by an order of magnitude, but a single dog still clears theta=0.90. That rejects C1a (layout-driven `D_min` shift) under the frozen protocol. C1b stays inconclusive: with no `D_min` movement, state predictors have nothing extra to explain.

## Limits

Baseline method only (`strombom_multi`). Split looks cost-similar to compact; confirm the generator creates separated clusters at t=0 if that layout is used as a mechanism contrast. No overcrowding cells, so Phase 3 Package C remains blocked on this map. Timeseries parquet from this claim are not retained.

## Claims update

CLAIM grade. Aligned with `scaling/docs/progress_tracker.md`:

| Claim | Verdict | Evidence |
|-------|---------|----------|
| C1a | REJECTED | `packages/b/frontier_by_layout.csv`: `D_min` = 1 on all 4 layouts at N in {50, 100, 200} |
| C1b | INCONCLUSIVE | no `D_min` shift; state vs (N, D) predictor comparison not decisive |

## Next

- Tracker steps 7-8 DONE
- Optional: verify split X0 at t=0; transfer maps in Phase 4 for C4
- Final report: [../../../docs/final_report.md](../../../docs/final_report.md)
- Main scaling plan: [../../../docs/main_scaling_plan.md](../../../docs/main_scaling_plan.md)

## Files in this folder

| Path | Meaning | Contents |
|------|---------|----------|
| `README.md` | This protocol note | Setup, runtime, results, claims, file map |
| `protocol.yaml` | Frozen config used for the run | Method, layouts, seeds, theta, T0 |
| `provenance.json` | Reproducibility stamp | Protocol id, git commit, host/platform, timestamps |
| `status.json` | Run progress | `n_planned`, `n_done`, `complete`, `elapsed_seconds` |
| `manifest.jsonl` | Resume ledger | One JSON line per cell; completed cells skipped on re-run |
| `trials.csv` | Claim-window trials only | 2,400 rows at 100 seeds on planned cells |
| `merged_trials.csv` | Claim-grade merge | Window 100-seed rows plus non-window scout 30-seed rows (5,280 total) |
| `boundary_cells.csv` | Claim window plan | Layout x N x D cells selected for reseed |
| `boundary_plan.json` | Plan metadata | Theta / planning parameters |
| `dmin_bootstrap.csv` | Bootstrap on claim trials | D_min and CI by layout x N |
| `merged_dmin_bootstrap.csv` | Bootstrap on merge | Same schema on the merge |
| `packages/b/` | Package B export | Structure evidence package |
| `timeseries/` | (not retained) | Parquet removed |

### `packages/b/` detail

| Path | Meaning |
|------|---------|
| `README.md` | Auto package summary |
| `frontier_by_layout.csv` | D_min, B*, effort by layout x N |
| `predictor_comparison.csv` | State vs (N, D) predictor NLL comparison |
| `artefacts.json` / `provenance.json` | Paths and run stamp for the package |

## Links

- Package B: `packages/b/README.md`
- Final report: `../../../docs/final_report.md`
- `merged_trials.csv`, `status.json`, `provenance.json`, `protocol.yaml`, `boundary_cells.csv`
- Phase index: `../README.md`
