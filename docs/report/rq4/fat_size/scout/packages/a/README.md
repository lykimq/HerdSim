# Package A (fat size scout)

This folder is **auto-generated** by the analysis package export (from the parent stage's `trials.csv` or `merged_trials.csv` after the stage make run). Do not edit these files by hand.

Size-map tables for the FAT compact scout: reliability, frontier, and regimes.

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
- `trials.csv`: Simulator output: one row per seed (success, ticks, path/effort, layout, N, D, ...). 3,000 rows here.

## Numbers

`D_min` = 1 for N in {5, 10}. Hard failure for every N >= 25 (nothing clears theta through D = 35).
