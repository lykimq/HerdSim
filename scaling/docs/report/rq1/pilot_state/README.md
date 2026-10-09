# Protocol note: `phase2_pilot_state`

## Summary

Smoke check for the Phase 2 start-shape path (layouts and state metrics). 600 trials completed. Pipeline check only. Not for claims.

## Intent

- RQ: RQ1 (smoke)
- Focus: Structure pipeline check
- Claims touched: none (SMOKE)
- Grade: SMOKE

## Setup

- Protocol: `scaling_v2`
- Method(s): strombom_multi
- Layout(s) X0: compact, split, outlier_rich, wide (reduced smoke grid)
- Output: `rq1/ (package) / live tree phase2/pilot_state/`

## Completeness

- Planned / done: 600 / 600 (`status.json` complete)

## Runtime

From `status.json` (`elapsed_seconds`):

| Field | Value |
|-------|-------|
| Elapsed | 421 s (0h 7m 1s) |
| Started (UTC) | 2026-09-25T09:18:26Z |
| Updated (UTC) | 2026-09-25T09:25:27Z |

## Results

Smoke-only. Use `packages/b/` if present for a first look at layout contrasts; do not update Claims from this folder.

## Files in this folder

| Path | Meaning | Contents |
|------|---------|----------|
| `README.md` | This protocol note | Setup, runtime, file map |
| `protocol.yaml` | Frozen config used for the run | Method, layouts, seeds, theta, T0 |
| `provenance.json` | Reproducibility stamp | Protocol id, git commit, host/platform |
| `status.json` | Run progress | Counts, `complete`, `elapsed_seconds` |
| `manifest.jsonl` | Resume ledger | One JSON line per cell |
| `trials.csv` | Trial-level results | One row per seed (success, ticks, shape/cost metrics) |
| `packages/` | Analysis exports | Package B smoke export if written |
| `timeseries/` | (not retained) | Parquet removed after analysis |

## Limits

SMOKE only. Not for Claims.

## Links

- Next: `../scout/`, then `../claim/`
- Phase index: `../README.md`
- Main scaling plan: ../../../docs/main_scaling_plan.md (frozen protocol in ../protocol/ or package protocol/)
