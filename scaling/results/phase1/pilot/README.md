# Protocol note: `phase1_pilot`

## Summary

Smoke check for the Phase 1 size map. 150 trials finished on host `gwen` with WORKERS=16. The run, resume files, Package A, and figures all look healthy. On this small grid, overall success is 0.947; failures only show up at tiny flocks with one dog. Safe to move on to scout. Not for claims.

## Intent

- Phase / RQ: Phase 1 / RQ2 (smoke of the size-map path)
- Focus: Size (pipeline check only)
- Claims touched (C1a-C7b): none (SMOKE; do not update Claims)
- Grade: SMOKE

## Setup

- Protocol: `scaling_v2`
- Task / success rule: herd every sheep into the goal before the deadline (T0)
- Method(s): strombom_multi
- Layout(s) X0: compact
- N grid: 5, 10, 25, 50, 100
- D grid: 1, 2, 3, 4, 6, 10
- Seeds (scout / claim): 5 (scout mode)
- T0 (and T1 if used): 10000 (T0 only)
- Theta: 0.90 (90% success bar)
- Command: `make -C scaling scaling-pilot WORKERS=16`
- Output: `scaling/results/phase1/pilot/`
- Host: gwen (Ultra 7 165H, 61 GiB)
- WORKERS / CPU governor: 16 / performance

## Completeness

- Planned cells: 150
- Done: 150
- `status.json` complete? yes
- Resume notes: first run; 150 trials written

## Runtime

From `status.json` (`elapsed_seconds`):

| Field | Value |
|-------|-------|
| Elapsed | 43 s (0h 0m 43s) |
| Started (UTC) | 2026-09-22T10:45:41Z |
| Updated (UTC) | 2026-09-22T10:46:24Z |

## Results

- Success pattern: almost all cells R=1.0; only weak cells are N=5 D=1 (R=0.0) and N=10 D=1 (R=0.4)
- Fewest dogs / frontier (by N / layout): compact `D_min` = 2 for N in {5,10}; `D_min` = 1 for N in {25,50,100}. No overcrowding on this export
- Regimes: wasteful_overspend 23, efficient_operation 5, under_resourced_failure 2
- Surprises: none for smoke; ticks mostly short (median 185, p90 201); a few oscillation/stuck failures

## Figures

From `packages/*/figures/`:

- [x] Reliability heatmap R(N, D)
- [x] Frontier D_min(N)
- [x] Regime counts

## Interpretation

The pipeline and Package A behave as expected on a compact low-D band. Failures sit where one dog is too few for a tiny flock. High success and no overcrowding here do not predict the full freeze grid; scout adds larger N/D and more seeds.

## Limits

SMOKE only: 5 seeds, reduced N/D, one method, one layout. Not for Claims. Do not treat `D_min` or regimes as claim-grade. Timeseries parquet from this smoke run are not retained.

## Claims update

CLAIM grade only. Skipped for SMOKE.

## Next

- Phase 1 scout (`../scout/`), then claim (`../claim/`)
- Phase index: `../README.md`
- Research plan: [../../summary/RESEARCH_PLAN.html](../../summary/RESEARCH_PLAN.html)

## Files in this folder

| Path | Meaning | Contents |
|------|---------|----------|
| `README.md` | This protocol note | Setup, runtime, results, claims, file map |
| `protocol.yaml` | Frozen config used for the run | Method, grids, seeds, theta, T0, timeseries flag |
| `provenance.json` | Reproducibility stamp | Protocol id, git commit, host/platform, timestamps |
| `status.json` | Run progress | `n_planned`, `n_done`, `complete`, `elapsed_seconds`, start/update times |
| `manifest.jsonl` | Resume ledger | One JSON line per cell; `status=ok` rows are skipped on re-run |
| `trials.csv` | Trial-level results | One row per seed: N, D, layout, success, ticks, path/effort metrics, failure tags, etc. |
| `packages/` | Analysis exports | Auto tables/figures from `scaling-analyse` (Package A/B/F/...); see `packages/*/README.md` |
| `timeseries/` | (not retained) | Parquet trajectories were removed after analysis to save disk; CSV/packages remain |

Package A lives under `packages/a/` (`reliability.csv`, `frontier.csv`, `regimes.csv`, `figures/`).

## Links

- Package A: `packages/a/README.md`
- `status.json`, `provenance.json`, `protocol.yaml`, `trials.csv`
