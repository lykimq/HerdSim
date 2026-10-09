# Protocol note: `phase5_comm_claim`

## Summary

Communication claim reseed finished: 1200 claim trials on 12 window cells; merge 1920 rows. Package E: `D_min` = 1 at none, neighbour_broadcast, and global_shared for N in {100, 200}. No grid-step lowering of `D_min` along the communication ladder.

## Intent

- Phase / RQ: Phase 5 / RQ5
- Focus: Communication information ladder
- Claims touched (C1a-C7b): C5a, C5b
- Grade: CLAIM

## Setup

- Protocol: `scaling_v2`
- Task / success rule: herd every sheep into the goal before the deadline (T0)
- Method(s): strombom_multi
- Layout(s) X0: compact
- N grid: {100, 200}
- D grid: claim windows from comm scout (12 cells)
- Seeds: 30 scout elsewhere / 100 on windows
- Communications: none, neighbour_broadcast, global_shared
- T0: 10000; Theta: 0.90
- Command: `make -C scaling scaling-phase5-comm-claim-reseed WORKERS=18`
- Output: `scaling/results/phase5/comm_claim/`
- Host: gwen; WORKERS=18 / performance

## Completeness

- Planned / done: 1200 / 1200
- `status.json` complete? yes
- Merge rows: 1920

## Runtime

| Field | Value |
|-------|-------|
| Elapsed | 1,295 s (0h 21m 35s) |
| Started (UTC) | 2026-10-08T11:56:42Z |
| Updated (UTC) | 2026-10-08T12:18:17Z |

## Results

From `packages/e/substitution_curves_comm.csv`:

| N | none | neighbour_broadcast | global_shared |
|---|------|---------------------|---------------|
| 100 | D_min = 1 | D_min = 1 | D_min = 1 |
| 200 | D_min = 1 | D_min = 1 | D_min = 1 |

- Package E: median_delta_dmin = 0; supports_substitution = False; supports_diminishing_returns = False

## Interpretation

Sharing sensed sheep among dogs does not reduce the fewest-dogs answer when the baseline already reaches `D_min` = 1 with no communication on this compact task.

## Limits

Baseline method, compact only, low-D band. For Strombom, `global_shared` is union of sensed sheep, not privileged simulator truth.

## Claims update

| Claim | Verdict | Evidence |
|-------|---------|----------|
| C5a | REJECTED | `packages/e/substitution_curves_comm.csv`: flat `D_min` = 1 across communication modes |
| C5b | INCONCLUSIVE | No first-step dog saving (`median_first_step_delta=0`) |

## Next

- Tracker C5a/C5b from all three ladders
- Phase 7 Package G on Phase 1 claim timeseries
- Package E: `packages/e/README.md`
