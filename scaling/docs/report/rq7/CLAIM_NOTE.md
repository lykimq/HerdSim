# Package G claim note (Phase 7 / RQ7)

Hand note on top of the auto `README.md`. Criteria: main scaling plan C7a / C7b.

## Inputs

- Trials: `../../merged_trials.csv` (4,540 merge; Package G loaded 2,200 claim-window rows with timeseries)
- Timeseries: `../../timeseries/` (parquet per claim trial)
- Horizon k = 500; feature window w = 200; eval ticks 1000..8000 step 200

## Results

From `early_warning_summary.csv` and `early_warning_campaign.csv`:

| Quantity | Value |
|----------|------:|
| n_trials | 2200 |
| n_failures | 169 |
| state AUROC (mean) | null |
| (N, D) AUROC (mean) | null |
| beats_nd_baseline | False |
| n_with_lead_time | 14 |
| median_lead_time (among those 14) | 9288.5 ticks |
| frac_lead_ge_500 | 0.083 |

Leave-one-N fold table is empty (`early_warning_folds.csv`).

## Claims

| Claim | Verdict | Reading |
|-------|---------|---------|
| C7a | INCONCLUSIVE | Held-out AUROC for state vs (N, D) could not be scored (null means / empty folds), so superiority is not established |
| C7b | REJECTED | Only about 8.3% of failure trials have lead time >= 500 ticks; need at least 30% |

## Limits

Failures on this map are concentrated at tiny flocks with one dog. Whole-N holdout and sparse failure trajectories limit AUROC scoring. Lead-time fraction uses all failure trials in the denominator (n_failures = 169).
