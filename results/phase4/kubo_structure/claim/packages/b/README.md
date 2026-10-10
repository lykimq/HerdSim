# Package B: phase4_kubo_structure_claim

Auto tables and figures for this package. Read `../../README.md` for interpretation.

Current frontiers (`frontier_by_layout.csv`):

| Layout | N | D_min | hard_failure |
|--------|--:|------:|:------------:|
| compact / split | 50,100,200 | 1 | no |
| outlier_rich | 50,100 | 1 | no |
| outlier_rich | 200 | 20 | no |
| wide | 50,100,200 | none | yes |

Outlier_rich N=200 detail: `../../outlier_rich_n200_window.json` (200 seeds on D in {1,2,3,4,6,10,15,20,25}; bootstrap [2, 20]; no overcrowding).

Predictor prefers_state=True nd_nll=0.42182883865301374 state_nll=0.3462265531932712

Artefacts:
- frontier_by_layout: frontier_by_layout.csv
- predictor_comparison: predictor_comparison.csv
