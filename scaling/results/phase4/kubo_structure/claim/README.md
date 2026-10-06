# Protocol note: `phase4_kubo_structure_claim`

## Summary

Kubo structure claim (4 layouts x N in {50,100,200}). Claim trials: 4,000 rows. Merge: 6,670 rows. Compact and split keep `D_min` = 1. Wide is hard failure. Outlier_rich N=200 has `D_min` = 20 at 200 seeds on D in {1,2,3,4,6,10,15,20,25} (bootstrap [2, 20]; no overcrowding). Snapshot: `outlier_rich_n200_window.json`.

## Intent

- Phase / RQ: Phase 4 / RQ4
- Focus: Structure transfer for `kubo` vs Phase 2 baseline
- Claims touched: C4
- Grade: CLAIM

## Setup

- Protocol: `scaling_v2`
- Method(s): kubo
- Layout(s) X0: compact, split, outlier_rich, wide
- N grid: {50, 100, 200}
- Seeds: 100 on standard claim windows; 200 on outlier_rich N=200 for D in {1,2,3,4,6,10,15,20,25}; D=35 stays at 30 (scout)
- Theta: 0.90
- T0: 10000
- obs_mode: global
- Output: `scaling/results/phase4/kubo_structure/claim/`

## Completeness

| Field | Value |
|-------|------:|
| Claim trials (`trials.csv`) | 4000 |
| Merged rows | 6670 |
| `status.json` complete | yes |

## Runtime

From `status.json` (`elapsed_seconds`):

| Field | Value |
|-------|-------|
| Elapsed | 835,308 s (9d 16h 1m 47s) |
| Finished (UTC) | 2026-10-06T10:54:32Z |

## Results

From `packages/b/frontier_by_layout.csv` and `merged_dmin_bootstrap.csv`:

| Layout | N | D_min | Notes |
|--------|--:|------:|-------|
| compact / split | 50,100,200 | 1 | shared with baseline |
| outlier_rich | 50,100 | 1 | shared |
| outlier_rich | 200 | 20 | 200 seeds; R(20)=0.935, R(25)=0.910; CI [2, 20] |
| wide | 50,100,200 | none | hard failure (best R about 0.47 to 0.54) |

Outlier_rich N=200 rates (see `outlier_rich_n200_window.json`): D1 0.745, D2 0.855, D3 0.835, D4 0.860, D6 0.890, D10 0.875, D15 0.855, D20 0.935, D25 0.910 (n=200); D35 0.967 (n=30).

## Limits

Scout-only Package B under `../scout/packages/b/` is not the claim answer for outlier_rich N=200. Use this claim merge and `outlier_rich_n200_window.json`. Bootstrap on that D_min stays wide because several D < 20 sit near theta.

## Claims update

| Claim | Verdict | Evidence |
|-------|---------|----------|
| C4 | SUPPORTED (partial) | This merge + `../../package_d/structure/`; shifted on outlier_rich N=200; absent on wide |

## Links

- Phase note: `../../README.md`
- Package B: `packages/b/`
- Package D structure: `../../package_d/structure/`
- Guides: `../../guides/REPORT_en.html`, `../../guides/REPORT_vi.html`
- Summary: `../../../summary/SUMMARY_REPORT.html`
