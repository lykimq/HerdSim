# Protocol note: `phase5_obs_claim`

## Summary

Observation claim reseed finished: 1200 claim trials on 12 reliability-window cells; merge written. Package E on the merge. At N in {100, 200}, `bearing_only` is a hard failure (no `D_min`); `local_positions` and `global` both have `D_min` = 1. No defined `D_min` falls by a grid step when moving up the ladder, so C5a is rejected on this ladder. C5b is inconclusive: there is no first-step dog saving among defined frontiers to test diminishing returns.

## Intent

- Phase / RQ: Phase 5 / RQ5
- Focus: Observation information ladder
- Claims touched (C1a-C7b): C5a, C5b
- Grade: CLAIM

## Setup

- Protocol: `scaling_v2`
- Task / success rule: herd every sheep into the goal before the deadline (T0)
- Method(s): strombom_multi
- Layout(s) X0: compact
- N grid: {100, 200}
- D grid: claim windows from obs scout (12 cells; see `boundary_cells.csv`)
- Seeds (scout / claim): 30 scout elsewhere / 100 on window cells
- Obs modes: bearing_only, local_positions, global
- T0: 10000
- Theta: 0.90
- Command: `make -C scaling scaling-phase5-obs-claim-reseed WORKERS=18`
- Output: `scaling/results/phase5/obs_claim/`
- Host: gwen (Ultra 7 165H, 61 GiB)
- WORKERS / CPU governor: 18 / performance

## Completeness

- Planned cells: 1200 claim trials
- Done: 1200 (`status.json` complete)
- `status.json` complete? yes
- Resume notes: paused mid-run left 128 manifest-ok rows without `trials.csv` flush; orphan keys stripped and reseeding completed 2026-10-08; final trials=1200, merge=1920 (12x100 + 24x30)

## Runtime

From `status.json` (`elapsed_seconds`):

| Field | Value |
|-------|-------|
| Elapsed | 75,342 s (20h 55m 42s) |
| Started (UTC) | 2026-10-07T12:46:28Z |
| Updated (UTC) | 2026-10-08T09:42:09Z |

Note: elapsed spans the overnight pause gap in wall clock.

## Results

From `packages/e/substitution_curves_obs.csv` and `substitution_summary_obs.csv`:

| N | bearing_only | local_positions | global |
|---|--------------|-----------------|--------|
| 100 | hard failure | D_min = 1 | D_min = 1 |
| 200 | hard failure | D_min = 1 | D_min = 1 |

- Package E summary: n_compared = 2; median_delta_dmin = 0; supports_substitution = False; supports_diminishing_returns = False
- Qualitative note: moving from bearing_only (no frontier) to local_positions establishes reliability at one dog, but that is not a one-grid-step lowering of two defined `D_min` values

## Interpretation

On compact Strombom starts at N in {100, 200}, bearing-only sensing cannot reach the 90% bar on the tested D band. Local positions already sit on the `D_min` = 1 floor; global observation does not reduce dog count further. Information quality matters for whether a frontier exists, but richer observation does not buy fewer dogs once local sensing works.

## Limits

Baseline method and compact layout only. Low-D band only. Claim windows follow scout selection. Hard failure under bearing_only is not scored as a numeric `D_min` decrease under C5a.

## Claims update

CLAIM grade. Aligned with `scaling/docs/progress_tracker.md`:

| Claim | Verdict | Evidence |
|-------|---------|----------|
| C5a | REJECTED | `packages/e/substitution_curves_obs.csv`: no ladder step lowers a defined `D_min` by a grid step at N in {100, 200}; Package E `supports_substitution=False` |
| C5b | INCONCLUSIVE | No first-step dog saving among defined frontiers (`median_first_step_delta=0`; `supports_diminishing_returns=False`) |

## Next

- Range and communication ladders under `../range_claim/` and `../comm_claim/`
- Tracker steps 14 DONE; C5a/C5b updated from all three ladders
- Phase index: `../README.md`

## Files in this folder

| Path | Meaning |
|------|---------|
| `README.md` | This protocol note |
| `protocol.yaml` | Frozen config |
| `provenance.json` | Reproducibility stamp |
| `status.json` | Progress + elapsed |
| `manifest.jsonl` | Resume ledger |
| `trials.csv` | Claim-window trials |
| `merged_trials.csv` | Claim-grade merge |
| `boundary_cells.csv` | Claim window plan |
| `packages/e/` | Package E substitution tables |

## Links

- Package E: `packages/e/README.md`
- Upstream scout: `../factor_sweep/`
- Main scaling plan: [../../../docs/main_scaling_plan.md](../../../docs/main_scaling_plan.md)
