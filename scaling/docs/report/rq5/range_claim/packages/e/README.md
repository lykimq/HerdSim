# Package E (range_claim)

This folder is **auto-generated** by the analysis package export (from the parent stage's `trials.csv` or `merged_trials.csv` after the stage make run). Do not edit these files by hand.

## Config

- Factor: sensing range
- Levels: 32.5, 65.0, 97.5, 130.0
- N: {100, 200}

## Artefacts

```
.
|-- artefacts.json
|-- substitution_curves_obs.csv
|-- substitution_curves_range.csv
|-- substitution_summary_obs.csv
`-- substitution_summary_range.csv
```

**Auto-generated (analysis)**
- `artefacts.json`: Index of paths written by the analysis package export.
- `substitution_curves_obs.csv`: D_min by N and observation mode along the obs ladder.
- `substitution_curves_range.csv`: D_min by N and sensing range along the range ladder.
- `substitution_summary_obs.csv`: Aggregate deltas and support flags for the observation ladder.
- `substitution_summary_range.csv`: Aggregate deltas and support flags for the range ladder.

## Numbers

`D_min` = 1 at every sensing range for N in {100, 200}.

Summary fields in `substitution_summary_range.csv`:

- `median_delta_dmin`: median over N of (richest-level `D_min` minus poorest-level `D_min`). Here 0 (flat ladder).
- `supports_substitution`: true when that median is negative (C5a). Here False.
- `supports_diminishing_returns`: true when the first step saves dogs and the second saves fewer (C5b). Here False.
