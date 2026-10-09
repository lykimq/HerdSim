# RQ6: scaling fits

Question: once we have `D_min` vs flock size from the baseline size map, which simple curve best predicts a held-out N, and is one power law enough?

## Status

DONE as analysis only. No new simulations. Fits use the claim-grade frontier from the RQ2 size map (`strombom_multi`, compact).

Story and numbers: [short report](../short_report.html). Source size map: [`../rq2/`](../rq2/).

## Files in this folder

| File | Meaning |
|------|---------|
| `README.md` | This note |
| `frontier.csv` | `D_min` (and related) by N used for fitting |
| `scaling_fits.csv` | Fitted models and slopes |
| `scaling_cv.csv` | Leave-one-N-out RMSE by model |
| `delta_aic_vs_power.csv` | Model comparison helper |
| `artefacts.json` | Index of package outputs |
| `provenance.json` | Analysis stamp |

## Takeaway

Piecewise (two levels: 2 then 1) has the lowest leave-one-N RMSE because `D_min` is almost flat. That is not a rich scaling law. Claims C6a and C6b SUPPORTED on that narrow reading.
