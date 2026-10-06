# Protocol note: `phase2_scout`

## Summary

Cheap start-shape map: 3,600 trials across N in {50,100,200}, four layouts, and the dog-count grid. Used to plan claim windows. Not claim-grade by itself.

## Intent

- Phase / RQ: Phase 2 / RQ1
- Focus: Structure reliability map for claim windows
- Claims touched: none (SCOUT)
- Grade: SCOUT

## Setup

- Protocol: `scaling_v2`
- Method(s): strombom_multi
- Layout(s) X0: compact, split, outlier_rich, wide
- N grid: {50, 100, 200}
- Seeds: 30
- Theta: 0.90 (90% success bar)
- T0: 10000
- Output: `scaling/results/phase2/scout/`

## Completeness

- Planned / done: 3,600 / 3,600 (`status.json` complete)

## Runtime

From `status.json` (`elapsed_seconds`):

| Field | Value |
|-------|-------|
| Elapsed | 11,633 s (3h 13m 53s) |
| Started (UTC) | 2026-09-25T09:25:40Z |
| Updated (UTC) | 2026-09-25T12:39:33Z |

## Results

Scout-grade layout map that feeds `boundary_cells.csv` in `../claim/`. Claim-grade fewest-dogs and cost numbers live in the claim merge and Package B.

## Files in this folder

| Path | Meaning | Contents |
|------|---------|----------|
| `README.md` | This protocol note | Setup, runtime, file map |
| `protocol.yaml` | Frozen config used for the run | Method, layouts, N/D grids, seeds |
| `provenance.json` | Reproducibility stamp | Protocol id, git commit, host/platform |
| `status.json` | Run progress | Counts, `complete`, `elapsed_seconds` |
| `manifest.jsonl` | Resume ledger | One JSON line per cell |
| `trials.csv` | Trial-level results | One row per seed across layouts and D |
| `packages/` | Analysis exports | Package B scout export (`frontier_by_layout`, predictors) |
| `timeseries/` | (not retained) | Parquet removed after analysis |

## Limits

SCOUT: 30 seeds. Not for Claims.

## Links

- Claim stage: `../claim/`
- Phase index: `../README.md`
- Main scaling plan: [../../../docs/main_scaling_plan.html](../../../docs/main_scaling_plan.html)
