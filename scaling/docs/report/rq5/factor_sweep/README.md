# Protocol note: `phase5_factor_sweep`

## Summary

Observation-ladder scout finished: 1080/1080 trials on compact starts with `strombom_multi`. Three obs modes (bearing_only, local_positions, global) at N in {100, 200} and D in {1, 2, 3, 4, 6, 10}, 30 seeds. Package E written. Planning only: not for claims. Claim windows reseeds live in `../obs_claim/`.

## Intent

- RQ: RQ5
- Focus: Observation information ladder (scout map)
- Claims touched (C1a-C7b): none (SCOUT)
- Grade: SCOUT

## Setup

- Protocol: `scaling_v2`
- Task / success rule: herd every sheep into the goal before the deadline (T0)
- Method(s): strombom_multi
- Layout(s) X0: compact
- N grid: {100, 200}
- D grid: {1, 2, 3, 4, 6, 10}
- Seeds (scout / claim): 30 (scout)
- Obs modes: bearing_only, local_positions, global
- T0: 10000
- Theta: 0.90
- Command: `make -C scaling scaling-factor-sweep WORKERS=18`
- Output: `rq5/ (package) / live tree phase5/factor_sweep/`
- Host: gwen (Ultra 7 165H, 61 GiB)
- WORKERS / CPU governor: 18 / performance

## Completeness

- Planned cells: 1080
- Done: 1080
- `status.json` complete? yes
- Resume notes: paused overnight once; resume skipped finished manifest rows

## Runtime

From `status.json` (`elapsed_seconds`):

| Field | Value |
|-------|-------|
| Elapsed | 78,955 s (21h 55m 55s) |
| Started (UTC) | 2026-10-07T07:46:49Z |
| Updated (UTC) | 2026-10-08T05:42:44Z |

Note: elapsed spans the overnight pause gap in wall clock.

## Results

- Scout map used only to plan obs claim windows
- Claim-grade frontiers: see `../obs_claim/packages/e/`

## Limits

SCOUT: 30 seeds. Not for Claims.

## Claims update

Skipped for SCOUT.

## Next

- Claim reseed in `../obs_claim/`
- Phase index: `../README.md`

## Files in this folder

| Path | Meaning |
|------|---------|
| `README.md` | This protocol note |
| `protocol.yaml` | Frozen config |
| `provenance.json` | Reproducibility stamp |
| `status.json` | Progress + elapsed |
| `manifest.jsonl` | Resume ledger |
| `trials.csv` | 1,080 scout rows |
| `packages/e/` | Package E scout export |
