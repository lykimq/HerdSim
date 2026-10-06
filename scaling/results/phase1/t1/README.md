# Protocol note: `phase1_t1`

## Summary

T1 asks: if more dogs start to hurt at the usual deadline, does that still hold when we allow 20,000 steps? The planner ran against the Phase 1 claim merge and selected **0 overcrowding cells**. No T1 simulations were executed. Make exited non-zero by design when the cell list is empty. That is the expected outcome given claim Package A (no `D_overcrowd`). C2b cannot be evaluated from T1 on this map; C2a has no overcrowding onset to cite.

## Intent

- Phase / RQ: Phase 1 / RQ2 (C2b hard ceiling at long budget)
- Focus: Size / overcrowding under T1=20000
- Claims touched: C2a, C2b
- Grade: CLAIM (plan only; no sims)

## Setup

- Protocol: `scaling_v2`
- Upstream: `phase1_claim` `merged_trials.csv`
- Command: `make -C scaling scaling-t1 WORKERS=16`
- Output: `scaling/results/phase1/t1/`
- Host: gwen; governor performance
- Theta: 0.90 (90% success bar)
- Max ticks: 20000

## Completeness

- Planned T1 cells: 0
- Done: n/a (nothing to run)
- `t1_plan.json`: `n_t1_cells=0`, `max_ticks=20000`
- `t1_cells.csv`: empty

## Runtime

No simulation runtime. Planner only; no `status.json` with `elapsed_seconds` for a T1 grid.

## Results

- No overcrowding window on compact + strombom_multi at theta=0.90 in the claim merge.
- Message from planner: "No overcrowding cells found; T1 has nothing to run (C2a may be false)"

## Figures

None (no Package A/C run).

## Interpretation

The size map does not show two consecutive sub-theta dog counts after `D_min`, so the T1 overcrowding protocol has no cells. That is evidence against overcrowding on this method/layout/task, not a pipeline failure.

## Limits

Single method and layout. Structure or transfer maps might still show overcrowding later.

## Claims update

| Claim | Verdict | Evidence |
|-------|---------|----------|
| C2a | REJECTED on this map | no `D_overcrowd`; empty T1 plan |
| C2b | SKIPPED | no T1 cells to reseed |

## Next

- Tracker step 6 SKIPPED
- Continue with Phase 2 structure when that campaign is next
- Main scaling plan: [../../../docs/main_scaling_plan.html](../../../docs/main_scaling_plan.html)

## Files in this folder

| Path | Meaning | Contents |
|------|---------|----------|
| `README.md` | This protocol note | Why T1 did not run; claim impact |
| `t1_plan.json` | Planner output | `n_t1_cells`, theta, max_ticks, path to upstream merge |
| `t1_cells.csv` | Cells to reseed at T1 | Empty here (header only / no rows): no overcrowding window |

## Links

- `t1_plan.json`, `t1_cells.csv`
- Upstream: `../claim/merged_trials.csv`, `../claim/packages/a/`
- Phase index: `../README.md`
