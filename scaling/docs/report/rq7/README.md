# RQ7: early warning

Question: can recent flock and dog state warn of a later failure better than knowing only N and D?

## Status

DONE as analysis only, but not answerable cleanly on this data. No new simulations. Package G used claim-grade trajectories from the RQ2 size map. Those trajectory parquet files are not included in this package; the summary tables below are.

Story and numbers: [short report](../short_report.html). Source size map: [`../rq2/`](../rq2/).

## Files in this folder

| File | Meaning |
|------|---------|
| `README.md` | This note |
| `CLAIM_NOTE.md` | Short claim note from the analysis run |
| `early_warning_summary.csv` | Lead-time and coverage summary |
| `early_warning_campaign.csv` | Campaign-level AUROC / fold summary |
| `early_warning_folds.csv` | Per-fold detail (empty folds here) |
| `artefacts.json` | Index of package outputs |
| `provenance.json` | Analysis stamp |

## Takeaway

By the first check at tick 1,000, almost every successful RQ2 size-map run has already finished, so there is no late window left to warn. Claim C7a INCONCLUSIVE; C7b REJECTED.
