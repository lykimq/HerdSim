# Package E (obs_claim)

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

bearing_only hard failure; local_positions and global both `D_min` = 1 at N in {100, 200}.

Summary fields in `substitution_summary_obs.csv`:

- `n_compared`: N values with at least two defined `D_min` levels. Here 2.
- `median_delta_dmin`: median over N of (richest-level `D_min` minus poorest defined-level `D_min`). Here 0.
- `supports_substitution`: true when that median is negative (C5a). Here False.
- `supports_diminishing_returns`: true when the first step saves dogs and the second saves fewer (C5b). Here False.
