# Package E (factor_sweep)

This folder is **auto-generated** by the analysis package export (from the parent stage's `trials.csv` or `merged_trials.csv` after the stage make run). Do not edit these files by hand.

## Config

- Factor: obs mode
- Levels: bearing_only, local_positions, global
- N: {100, 200}

## Artefacts

```
.
|-- artefacts.json
|-- substitution_curves_obs.csv
`-- substitution_summary_obs.csv
```

**Auto-generated (analysis)**
- `artefacts.json`: Index of paths written by the analysis package export.
- `substitution_curves_obs.csv`: D_min by N and observation mode along the obs ladder.
- `substitution_summary_obs.csv`: Aggregate deltas and support flags for the observation ladder.

## Numbers

Scout (30 seeds). n_compared = 2; median_delta_dmin = 0; supports_substitution = False; supports_diminishing_returns = False.

Summary fields in `substitution_summary_obs.csv`:

- `n_compared`: N values with at least two defined `D_min` levels to compare.
- `median_delta_dmin`: median over N of (richest-level `D_min` minus poorest-level `D_min`). Negative means richer info needs fewer dogs.
- `supports_substitution`: true when that median is negative (C5a).
- `supports_diminishing_returns`: true when the first ladder step saves dogs and the second saves fewer (C5b).

