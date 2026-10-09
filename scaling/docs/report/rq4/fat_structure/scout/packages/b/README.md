# Package B (fat structure scout)

This folder is **auto-generated** by the analysis package export (from the parent stage's `trials.csv` or `merged_trials.csv` after the stage make run). Do not edit these files by hand.

Layout contrast tables for the FAT structure scout: fewest dogs and path cost by `initial_layout` x N.

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

Hard failure on all four layouts at N in {50, 100, 200} (no cell clears theta through D = 35).

Predictor summary fields in `predictor_comparison.csv` (C1b):

- `nd_nll`: leave-one-N negative log-likelihood of a logistic model that uses only `(N, D)`.
- `state_nll`: same CV NLL when early flock/dog state (and layout) is added.
- `prefers_state`: true when `state_nll` is lower than `nd_nll` (early state predicts success better than `(N, D)` alone).
