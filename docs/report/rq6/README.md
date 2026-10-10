# RQ6: scaling fits

Once we have `D_min` vs flock size from the baseline size map, which simple curve best predicts a held-out N, and is one power law enough?

## Status

DONE as analysis only. No new simulations. Fits use the claim-grade frontier from the RQ2 size map (`strombom_multi`, compact).

## Dependencies

```mermaid
flowchart LR
  rq2merge["../rq2/claim/merged_trials.csv"]
  frontier["frontier.csv"]
  fits["scaling_fits.csv<br/>scaling_cv.csv<br/>delta_aic_vs_power.csv"]

  rq2merge -->|"frontier"| frontier
  frontier -->|"fits"| fits
```

| Input | Role |
|-------|------|
| `../rq2/claim/merged_trials.csv` | Claim-grade size map used to build the frontier |
| `frontier.csv` (this folder) | `D_min` / overcrowding / B* by N fed into the fits |

No scout/claim reseed here. Re-running RQ6 is analysis export only after RQ2 claim merge exists.

## This folder

Analysis CSVs live at the top level and are mirrored under `packages/`.

```
.
|-- artefacts.json
|-- delta_aic_vs_power.csv
|-- frontier.csv
|-- scaling_cv.csv
|-- scaling_fits.csv
`-- packages/
    `-- f/
```

**Auto-generated (analysis)**
- `artefacts.json`: Index of paths written by the analysis package export.
- `delta_aic_vs_power.csv`: AIC gap of each model versus the power law.
- `frontier.csv`: Fewest dogs / overcrowding / B* by N.
- `scaling_cv.csv`: Leave-one-N-out RMSE by model.
- `scaling_fits.csv`: Fitted D_min-vs-N models with params, RMSE, AIC, BIC.

**Auto-generated (analysis packages)**
- `packages/f/`: Package F (scaling-fit tables; mirrors the CSVs above).

## Takeaway

Piecewise (two levels: 2 then 1) has the lowest leave-one-N RMSE (0.132 vs power 0.247) because `D_min` is almost flat. That is not a rich scaling law.

## Claims

| Claim | What it asks (supported when) | Verdict |
|-------|-------------------------------|---------|
| C6a | Power has higher leave-one-N-out RMSE than piecewise or per-layout curves | SUPPORTED |
| C6b | The slope of log `D_min` on log N is below 1 in a stated N and layout band | SUPPORTED |
