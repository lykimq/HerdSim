# RQ5: information vs shepherds

Can better observation, sensing range, or communication reduce how many dogs we need at the same reliability bar (theta = 0.90)?

Claim-grade evidence lives under `results/phase5/` (obs / range / comm scout+claim). Short-report write-up: [../short_report.md](../short_report.md) (RQ5 section). Tracker: [../../science/progress_tracker.md](../../science/progress_tracker.md).

## Verdicts

| Claim | Criterion | Verdict |
|-------|-----------|---------|
| C5a | One ladder step lowers `D_min` by at least one D-grid step at N in {100, 200} | SUPPORTED (range: sensing_range 32.5 -> 65) |
| C5b | The second ladder step saves fewer dogs than the first | SUPPORTED (further range steps save 0 more) |

## Key numbers (claim merges)

| Ladder | N | Factor | D_min |
|--------|--:|--------|------:|
| Obs | 100, 200 | bearing_only | none (hard failure) |
| Obs | 100, 200 | local_positions / global | 1 |
| Range | 100 | sensing_range 32.5 | 3 |
| Range | 200 | sensing_range 32.5 | 2 |
| Range | 100, 200 | sensing_range 65 / 97.5 / 130 | 1 |
| Comm | 100, 200 | none / neighbour_broadcast / global_shared | 1 |

Figures: `docs/figures/f13_rq5_ladder_dmin.png`, `f14_rq5_range_reliability.png`, `f15_rq5_obs_reliability.png`.
