# Protocol note: `phase5_range_scout`

## Summary

Sensing-range scout finished: 1440/1440 trials. Four ranges (32.5, 65, 97.5, 130) at N in {100, 200} and D in {1, 2, 3, 4, 6, 10}, 30 seeds, compact `strombom_multi`. Package E written. Planning only.

## Intent

- Phase / RQ: Phase 5 / RQ5
- Focus: Sensing-range ladder (scout)
- Claims touched: none (SCOUT)
- Grade: SCOUT

## Setup

- Protocol: `scaling_v2`
- Method(s): strombom_multi
- Layout(s) X0: compact
- N grid: {100, 200}
- D grid: {1, 2, 3, 4, 6, 10}
- Seeds: 30
- Sensing ranges: 32.5, 65.0, 97.5, 130.0
- Command: `make -C scaling scaling-phase5-range-scout WORKERS=18`
- Output: `scaling/results/phase5/range_scout/`
- Host: gwen; WORKERS=18 / performance

## Completeness

- Planned / done: 1440 / 1440
- `status.json` complete? yes

## Runtime

| Field | Value |
|-------|-------|
| Elapsed | 1,495 s (0h 24m 55s) |
| Started (UTC) | 2026-10-08T09:42:13Z |
| Updated (UTC) | 2026-10-08T10:07:08Z |

## Limits

SCOUT only. Not for Claims.

## Next

- Claim reseed in `../range_claim/`
