# Package F (kubo size claim)

This folder is **auto-generated** by the analysis package export (from the parent stage's `trials.csv` or `merged_trials.csv` after the stage make run). Do not edit these files by hand.

Scaling-curve fits on the Kubo compact claim frontier (`D_min` vs N).

## Artefacts

```
.
|-- artefacts.json
|-- delta_aic_vs_power.csv
|-- frontier.csv
|-- scaling_cv.csv
`-- scaling_fits.csv
```

**Auto-generated (analysis)**
- `artefacts.json`: Index of paths written by the analysis package export.
- `delta_aic_vs_power.csv`: AIC gap of each model versus the power law.
- `frontier.csv`: Fewest dogs / overcrowding / B* by N.
- `scaling_cv.csv`: Leave-one-N-out RMSE by model.
- `scaling_fits.csv`: Fitted D_min-vs-N models with params, RMSE, AIC, BIC.

## Numbers

Piecewise (break at N=10: 3 then 1) has near-zero RMSE. Power RMSE ≈ 0.42.

Summary fields:

- `best_model`: model with lowest leave-one-N-out RMSE on `D_min` vs N (C6a compares power vs piecewise / separate curves).
- leave-one-N RMSE values: how wrong each model is when one flock size is held out.
- `prefers_piecewise_or_state`: true when piecewise or per-layout curves beat power on that CV (C6a).
- `log_log_slope` (power): slope of log `D_min` on log N; C6b asks whether this is below 1 in the stated band.
- `delta_aic_vs_power`: AIC of each model minus AIC of power (negative means better than power on in-sample AIC).

