# Package A (claim)

This folder is **auto-generated** by the analysis package export (from the parent stage's `trials.csv` or `merged_trials.csv` after the stage make run). Do not edit these files by hand.

Size-map tables for the RQ2 claim merge: reliability R(N, D), fewest dogs / overcrowding frontier, and regime labels.

## Artefacts

```
.
|-- artefacts.json
|-- dmin_bootstrap.csv
|-- frontier.csv
|-- regimes.csv
|-- reliability.csv
`-- trials.csv
```

**Auto-generated (analysis)**
- `artefacts.json`: Index of paths written by the analysis package export.
- `dmin_bootstrap.csv`: Bootstrap of D_min and confidence interval from claim trials only.
- `frontier.csv`: Fewest dogs / overcrowding / B* by N.
- `regimes.csv`: Regime label per cell (efficient, wasteful, under-resourced, overcrowding).
- `reliability.csv`: Success rate R by layout x N x D.
- `trials.csv`: Simulator output: one row per seed (success, ticks, path/effort, layout, N, D, ...). 4,540 rows here.

## Numbers

Overall success 0.963. `D_min` = 2 for N in {5, 10}; `D_min` = 1 for N >= 25; `d_max` = 35. Regimes: wasteful_overspend 88, efficient_operation 10, under_resourced_failure 2. No overcrowding. Failures: oscillation 111, stuck 58.
