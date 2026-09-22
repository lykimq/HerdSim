# Protocol report: `phase1_pilot`

## Summary

SMOKE pilot completed on host `gwen` with WORKERS=16. Pipeline (run, resume artifacts, Package A, figures) is healthy. Map is easy on this reduced grid: overall success 0.947; failures only at small N with D=1. Ready for Phase 1 scout.

## Intent

- Phase / RQ: Phase 1 / RQ2 (smoke of size map path)
- Focus: Size (pipeline check only)
- Claims touched (C1a-C7b): none (SMOKE; do not update Claims)
- Grade: SMOKE

## Setup

- Protocol: `scaling_v2`
- Task / success rule: herd into goal within T0
- Method(s): strombom_multi
- Layout(s) X0: compact
- N grid: 5, 10, 25, 50, 100
- D grid: 1, 2, 3, 4, 6, 10
- Seeds (scout / claim): 5 (scout mode)
- T0 (and T1 if used): 10000 (T0 only)
- Theta: 0.90
- Command: `make -C scaling scaling-pilot WORKERS=16`
- Output: `scaling/results/phase1/pilot/`
- Host: gwen (Ultra 7 165H, 61 GiB)
- WORKERS / CPU governor: 16 / performance

## Completeness

- Planned cells: 150
- Done: 150
- `status.json` complete? yes
- Resume notes: first run; elapsed ~43 s; 150 timeseries files written

## Results

- Success pattern: almost all cells R=1.0; only under-resourced cells are N=5 D=1 (R=0.0) and N=10 D=1 (R=0.4)
- D_min / frontier (by N / layout): compact D_min = 2 for N in {5,10}; D_min = 1 for N in {25,50,100}. No D_overcrowd on this export
- Regimes: wasteful_overspend 23, efficient_operation 5, under_resourced_failure 2
- Surprises: none for smoke; ticks mostly short (median 185, p90 201); a few oscillation/stuck failures

## Figures

From `packages/*/figures/` (tick what you looked at):

- [x] Reliability heatmap R(N, D)
- [x] Frontier D_min(N) (+ D_overcrowd / D_max if present)
- [x] Regime counts
- [ ] Other (Phase 2+):

## Interpretation

Pipeline and Package A behave as expected on a compact low-D band. Failures concentrate where D is too small for small flocks. High success and no overcrowding here do not predict the full freeze grid; scout will add larger N/D and more seeds.

## Limits

SMOKE only: 5 seeds, reduced N/D, one method, one layout. Not for Claims. Do not treat D_min or regimes as claim-grade.

## Claims update

CLAIM grade only. Skipped for SMOKE.

| Claim | Verdict | Evidence |
|-------|---------|----------|
| | | |

## Next

- Run Phase 1 scout (`make -C scaling scaling-scout WORKERS=16`)
- Tracker: step 1 DONE; step 2 next

## Links

- Package A: `packages/a/package_a.md`
- Other packages: none
- `status.json`, `provenance.json`, `protocol.yaml`, `trials.csv`
