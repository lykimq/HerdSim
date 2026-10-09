# Package B (pilot_state)

This folder is **auto-generated** by the analysis package export (from the parent stage's `trials.csv` or `merged_trials.csv` after the stage make run). Do not edit these files by hand.

Layout contrast tables for the RQ1 smoke run: fewest dogs and path cost by `initial_layout` x N, plus a state vs (N, D) predictor comparison.

## Artefacts

```
.
|-- artefacts.json
|-- frontier_by_layout.csv
`-- predictor_comparison.csv
```

**Auto-generated (analysis)**
- `artefacts.json`: Index of paths written by the analysis package export.
- `frontier_by_layout.csv`: Fewest dogs / overcrowding / B* by layout x N.
- `predictor_comparison.csv`: Leave-one-N NLL for early-state vs (N, D) predictors; prefers_state flag.

## Numbers

Smoke grid (5 seeds). `prefers_state=True` on this reduced map (`nd_nll` ≈ 0.153, `state_nll` ≈ 0.130). `D_min` is still 1 for N >= 25 on all four layouts; wide and outlier_rich raise B* effort.

Predictor summary fields in `predictor_comparison.csv` (C1b):

- `nd_nll`: leave-one-N negative log-likelihood of a logistic model that uses only `(N, D)`.
- `state_nll`: same CV NLL when early flock/dog state (and layout) is added.
- `prefers_state`: true when `state_nll` is lower than `nd_nll` (early state predicts success better than `(N, D)` alone).
