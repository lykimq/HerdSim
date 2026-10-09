# Protocol note: `phase5_comm_scout`

## Summary

Communication scout finished: 1080/1080 trials. Modes none / neighbour_broadcast / global_shared at N in {100, 200} and D in {1, 2, 3, 4, 6, 10}, 30 seeds, compact `strombom_multi`. Package E written. Planning only.

## Intent

- RQ: RQ5
- Focus: Communication ladder (scout)
- Claims touched: none (SCOUT)
- Grade: SCOUT

## Setup

- Protocol: `scaling_v2`
- Method(s): strombom_multi
- Layout(s) X0: compact
- N grid: {100, 200}
- D grid: {1, 2, 3, 4, 6, 10}
- Seeds: 30
- Communications: none, neighbour_broadcast, global_shared
- Command: `make -C scaling scaling-phase5-comm-scout WORKERS=18`
- Output: `rq5/ (package) / live tree phase5/comm_scout/`
- Host: gwen; WORKERS=18 / performance

## Completeness

- Planned / done: 1080 / 1080
- `status.json` complete? yes

## Runtime

| Field | Value |
|-------|-------|
| Elapsed | 4,726 s (1h 18m 46s) |
| Started (UTC) | 2026-10-08T10:37:51Z |
| Updated (UTC) | 2026-10-08T11:56:38Z |

## Limits

SCOUT only. Not for Claims.

## Next

- Claim reseed in `../comm_claim/`
