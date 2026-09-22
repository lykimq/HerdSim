# Protocol report: `phase1_claim`

## Summary

CLAIM reseed completed (resumed from 73/2200 after an earlier abort). 2200 claim trials on 22 reliability-window cells; merge has 4467 rows. Packages A and F written on `merged_trials.csv`. Frontier matches scout: D_min=2 for N in {5,10}, D_min=1 for N>=25. No overcrowding. Bootstrap CI on D_min is one grid step for every N. Ready for Claims review on C1/C2a (size map) and Package F diagnostics; T1 still needed only if overcrowding cells appear (none here).

## Intent

- Phase / RQ: Phase 1 / RQ2
- Focus: Size (claim-grade D_min / regimes)
- Claims touched (C1a-C7b): C1a/C1b candidates; C2a unevaluable (no overcrowding); C6 pending careful F read
- Grade: CLAIM

## Setup

- Protocol: `scaling_v2`
- Task / success rule: herd into goal within T0
- Method(s): strombom_multi
- Layout(s) X0: compact
- N grid: full freeze (claim windows only)
- D grid: reliability window only (22 cells; see boundary_cells.csv)
- Seeds (scout / claim): 30 scout elsewhere / 100 on window cells
- T0 (and T1 if used): 10000 (T0 only)
- Theta: 0.90
- Command: `make -C scaling scaling-claim-reseed WORKERS=16` (resume)
- Output: `scaling/results/phase1/claim/`
- Host: gwen (Ultra 7 165H, 61 GiB)
- WORKERS / CPU governor: 16 / performance

## Completeness

- Planned cells: 2200 claim trials
- Done: 2200 (`status.json` complete)
- `status.json` complete? yes
- Resume notes: first attempt stopped at 73; second run resumed (`n_pending_at_start` 2127); elapsed clock ~3451 s across sessions; merge 4467 rows

## Results

- Success pattern: merged overall success 0.977; under-resource failures still at small N with D=1
- D_min / frontier (by N / layout): compact D_min=2 (N=5,10), D_min=1 (N>=25); no D_overcrowd; d_max=35
- Regimes: wasteful_overspend 88, efficient_operation 10, under_resourced_failure 2
- Surprises: still no overcrowding at theta=0.9 on compact+strombom_multi; stuck/oscillation dominate the rare failures
- Bootstrap: d_min_ci_low == d_min_ci_high for all N at 100 seeds
- Package F (auto): best_model=piecewise; prefers_piecewise_or_state=True

## Figures

From `packages/*/figures/` (tick what you looked at):

- [x] Reliability heatmap R(N, D)
- [x] Frontier D_min(N) (+ D_overcrowd / D_max if present)
- [x] Regime counts
- [ ] Other (Phase 2+):

## Interpretation

Claim-grade map confirms the scout story: one dog is enough for N>=25 on compact X0 under T0; N=5 and N=10 need D>=2. High D is wasteful rather than overcrowded, so C2a is not supported by this size map (and T1 has no overcrowding cells to run). Scaling fits lean piecewise (Package F); treat C6 only after reading fit tables against claim criteria.

## Limits

Single method, single layout. No overcrowding window, so no T1 overcrowding campaign from this plan. Merge mixes 100-seed claim cells with 30-seed scout cells elsewhere (by design). Claims that need structure, transfer, or information ladders wait on later phases.

## Claims update

CLAIM grade. Copy into tracker after you agree:

| Claim | Verdict | Evidence |
|-------|---------|----------|
| C1a | SUPPORTED (provisional) | `packages/a/` frontier D_min(N) exists and is stable (bootstrap one step) |
| C1b | INCONCLUSIVE / check criteria | regimes show under-resourced and wasteful; no overcrowding band |
| C2a | UNEVALUABLE / REJECTED on this map | no D_overcrowd / overcrowding regime |
| C2b | UNEVALUATED | needs T1; no overcrowding cells |
| C6a/C6b | UNEVALUATED pending F criteria | `packages/f/` piecewise preferred |

## Next

- Update Claims table in progress_tracker.md for C1/C2a
- Skip T1 unless you redefine overcrowding cells (tracker step 6)
- Or continue Phase 2 structure scout
- Tracker: steps 4-5 DONE

## Links

- Package A: `packages/a/package_a.md`
- Package F: `packages/f/package_f.md`
- `merged_trials.csv`, `status.json`, `provenance.json`, `protocol.yaml`, `boundary_cells.csv`
