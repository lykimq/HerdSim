# Package G (RQ7)

Analysis CSVs here are **auto-generated** by the analysis package export (analysis-only RQ; no new simulations). `CLAIM_NOTE.md` is Config.

Early-warning tables: whether early flock/dog state predicts later failure better than (N, D) alone, and how often lead time is at least 500 ticks.

## Depends on

- Reads: `../../../rq2/claim/merged_trials.csv` (outcomes / cell keys)
- Reads: RQ2 claim trajectory parquet (outside this report tree; state features)

## Artefacts

```
.
|-- CLAIM_NOTE.md
|-- artefacts.json
|-- early_warning_campaign.csv
|-- early_warning_folds.csv
`-- early_warning_summary.csv
```

**Config**
- `CLAIM_NOTE.md`: Claim note (C7a / C7b verdicts and limits).

**Auto-generated (analysis)**
- `artefacts.json`: Index of paths written by the analysis package export.
- `early_warning_campaign.csv`: Campaign settings and AUROC vs (N, D) baseline.
- `early_warning_folds.csv`: Per-fold AUROC detail (may be empty).
- `early_warning_summary.csv`: Lead-time and coverage summary across failure trials.

## Numbers

2,200 trials; 169 failures. state and (N, D) AUROC means are null; beats_nd_baseline = False. 14 / 169 failures have a scored lead time; frac_lead_ge_500 ≈ 0.083; median_lead_time among those 14 is 9288.5 ticks.

Summary fields:

- `beats_nd_baseline`: C7a flag; true when held-out state AUROC beats the held-out `(N, D)` baseline.
- AUROC null here: almost every success has already finished by the first check tick, so there is no usable late window to score.
- `frac_lead_ge_500`: C7b; fraction of failure trials with lead time of at least 500 ticks (threshold 0.30).
- `median_lead_time`: median lead time among failures that have a scored lead time.
