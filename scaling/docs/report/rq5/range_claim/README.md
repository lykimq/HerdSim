# Protocol note: `phase5_range_claim`

## Summary

Range claim reseed finished: 1600 claim trials on 16 window cells; merge 2560 rows. Package E: `D_min` = 1 at every sensing range for N in {100, 200}. No grid-step lowering of `D_min` along the range ladder. Supports C5a rejection and leaves C5b without a first-step dog saving.

## Intent

- RQ: RQ5
- Focus: Sensing-range information ladder
- Claims touched (C1a-C7b): C5a, C5b
- Grade: CLAIM

## Setup

- Protocol: `scaling_v2`
- Task / success rule: herd every sheep into the goal before the deadline (T0)
- Method(s): strombom_multi
- Layout(s) X0: compact
- N grid: {100, 200}
- D grid: claim windows from range scout (16 cells)
- Seeds: 30 scout elsewhere / 100 on windows
- Sensing ranges: 32.5, 65.0, 97.5, 130.0
- T0: 10000; Theta: 0.90
- Command: `make -C scaling scaling-phase5-range-claim-reseed WORKERS=18`
- Output: `rq5/ (package) / live tree phase5/range_claim/`
- Host: gwen; WORKERS=18 / performance

## Completeness

- Planned / done: 1600 / 1600
- `status.json` complete? yes
- Merge rows: 2560

## Runtime

| Field | Value |
|-------|-------|
| Elapsed | 1,834 s (0h 30m 34s) |
| Started (UTC) | 2026-10-08T10:07:13Z |
| Updated (UTC) | 2026-10-08T10:37:47Z |

## Results

From `packages/e/substitution_curves_range.csv`:

| N | 32.5 | 65.0 | 97.5 | 130.0 |
|---|------|------|------|-------|
| 100 | D_min = 1 | D_min = 1 | D_min = 1 | D_min = 1 |
| 200 | D_min = 1 | D_min = 1 | D_min = 1 | D_min = 1 |

- Package E: median_delta_dmin = 0; supports_substitution = False; supports_diminishing_returns = False

## Interpretation

Within 0.5x to 2x of Strombom `r_s`, sensing range does not change the fewest-dogs answer on this compact baseline task: one dog already clears theta.

## Limits

Baseline method, compact only, low-D band. Does not test observation-mode limits (those are the obs ladder).

## Claims update

| Claim | Verdict | Evidence |
|-------|---------|----------|
| C5a | REJECTED | `packages/e/substitution_curves_range.csv`: flat `D_min` = 1 across ranges |
| C5b | INCONCLUSIVE | No first-step dog saving (`median_first_step_delta=0`) |

## Next

- Communication ladder: `../comm_claim/`
- Package E: `packages/e/README.md`
