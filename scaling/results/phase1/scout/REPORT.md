# Protocol report: `phase1_scout`

## Summary

SCOUT completed: 3000/3000 trials in ~73 min (WORKERS=16). Package A and F written. Map is highly successful on compact + strombom_multi (overall R=0.983). D_min is 2 for N in {5,10} and 1 for N>=25. No overcrowding regime on this export. Bootstrap CI on D_min is one grid step wide for every N (no 200-seed raise needed before claim). Ready for claim-plan.

## Intent

- Phase / RQ: Phase 1 / RQ2
- Focus: Size (reliability map for claim windows)
- Claims touched (C1a-C7b): none (SCOUT; planning only)
- Grade: SCOUT

## Setup

- Protocol: `scaling_v2`
- Task / success rule: herd into goal within T0
- Method(s): strombom_multi
- Layout(s) X0: compact
- N grid: 5, 10, 25, 50, 75, 100, 150, 200, 300, 400
- D grid: 1, 2, 3, 4, 6, 10, 15, 20, 25, 35
- Seeds (scout / claim): 30 (scout)
- T0 (and T1 if used): 10000 (T0 only)
- Theta: 0.90
- Command: `make -C scaling scaling-scout WORKERS=16`
- Output: `scaling/results/phase1/scout/`
- Host: gwen (Ultra 7 165H, 61 GiB)
- WORKERS / CPU governor: 16 / performance

## Completeness

- Planned cells: 3000
- Done: 3000
- `status.json` complete? yes
- Resume notes: first full run; elapsed ~4359 s; timeseries stored; analyse A+F succeeded

## Results

- Success pattern: R=1.0 for all N>=25; lower only at N=5 (0.903) and N=10 (0.927), driven by D=1 under-resourcing
- D_min / frontier (by N / layout): compact D_min=2 (N=5,10), D_min=1 (N>=25); d_max=35; no D_overcrowd
- Regimes: wasteful_overspend 88, efficient_operation 10, under_resourced_failure 2
- Surprises: no overcrowding at theta=0.9 on this scout; failures are oscillation/stuck at small N; ticks usually short (median 182) with rare 10000 caps
- Bootstrap: d_min_ci_low == d_min_ci_high for every N (no multi-step CI)
- Package F (auto): best_model=piecewise by leave-one-N RMSE; prefers_piecewise_or_state=True (SCOUT only; not for Claims)

## Figures

From `packages/*/figures/` (tick what you looked at):

- [x] Reliability heatmap R(N, D)
- [x] Frontier D_min(N) (+ D_overcrowd / D_max if present)
- [x] Regime counts
- [ ] Other (Phase 2+):

## Interpretation

On compact X0, one dog is enough for N>=25 under T0; small flocks need D>=2. High D mostly looks wasteful rather than overcrowded. Claim windows will concentrate on the D_min neighborhood (and overcrowding only if plan finds consecutive sub-theta cells; scout suggests that may be empty).

## Limits

SCOUT: 30 seeds, one method, one layout. Not for Claims. No overcrowding / hard-failure signal to cite. Package F fits are diagnostic only until claim-grade merge.

## Claims update

CLAIM grade only. Skipped for SCOUT.

| Claim | Verdict | Evidence |
|-------|---------|----------|
| | | |

## Next

- `make -C scaling scaling-claim-plan` (writes `boundary_cells.csv`)
- Then `make -C scaling scaling-claim-reseed WORKERS=16`
- Tracker: step 2 DONE; step 3 next

## Links

- Package A: `packages/a/package_a.md`
- Package F: `packages/f/package_f.md`
- `status.json`, `provenance.json`, `protocol.yaml`, `trials.csv`
