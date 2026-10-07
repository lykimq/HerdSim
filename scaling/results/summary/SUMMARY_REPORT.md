# How many dogs does a flock need?

## 1. Scope and status

This report contains only empirical results from completed Phases **1**, **2**, and **4** of `scaling_v2`.

![Phases covered in this report.](figures/schematics/en/phase_roadmap.svg)

*Phases with claim-grade numbers here: 1, 2, and 4. Setup and method diagrams live in the linked docs below.*

![Five main results from Phases 1, 2, and 4.](figures/schematics/en/summary_at_a_glance.svg)

| Question | Completed evidence |
|---|---|
| As flock size grows, how many dogs are needed? | Phase 1, baseline `strombom_multi` on `compact` starts |
| Does starting structure change that answer? | Phase 2, baseline across four layouts |
| Do the findings transfer to other dog rules? | Phase 4, `kubo` and `fat` size and structure maps |

| Verdict | Finding | Key numbers |
|---|---|---|
| D_min = 1 | On the baseline rule with a compact start, flocks from 25 to 400 sheep succeed reliably with one dog. | Flocks of 5 and 10 need 2 dogs. At one dog, R is 0.07 and 0.24. |
| Waste | Once compact-start runs work, more dogs do not finish faster; they walk more. | Typical finish is about 183 ticks; path per dog is about 148 for N >= 25. Of 100 size by dog-count cells, 88 are wasteful. |
| Not reproduced | The steep rise in dog need reported by the 2025 draft does not appear here. | The draft reported about 20 to 35 dogs for N >= 200. Here one dog finishes N = 400 in a typical 168 ticks. |
| Cost only | Baseline start shape changes time and path, but not D_min. | Wide starts take about 11x to 20x more time and 19x to 36x more path than compact starts. At N = 200, `outlier_rich` reaches about 6x time and 11x path. |
| Partial transfer | Kubo and FAT do not transfer evenly from baseline. | Kubo roughly matches baseline on compact starts but reaches only R = 0.47 to 0.54 on wide starts. FAT reaches R >= 0.90 only for N <= 10. |

| Phase | Question | Method | Layout | Pilot | Scout | Claim |
|---|---|---|---|---:|---:|---:|
| 1 | Size map | strombom_multi | compact | 150 | 3,000 | 2,200 |
| 2 | Structure | strombom_multi | 4 layouts | 600 | 3,600 | 2,400 |
| 4a | Transfer: size | kubo | compact | n/a | 3,000 | 2,100 |
| 4a | Transfer: size | fat | compact | n/a | 3,000 | 2,000 |
| 4b | Transfer: structure | kubo | 4 layouts | n/a | 3,600 | 4,000 |
| 4b | Transfer: structure | fat | 4 layouts | n/a | 3,600 | 2,400 |
|  | **Total simulations** |  |  |  |  | **35,650** |

The claim merges contain 30,670 rows. The executed pilot, scout, and claim stages contain 35,650 rows; reseeded cells drop their scout rows from the claim merge. Kubo structure claim has 4,000 rows, including 200 seeds at `outlier_rich`, N = 200 for D in {1, 2, 3, 4, 6, 10, 15, 20, 25}. See the [run ledger](data/run_ledger.md).

Canonical background:

- [Research plan](../../docs/main_scaling_plan.md)
- [Setup and parameter reference](../../docs/setup/README.md)
- [Method guides](../../docs/methods/README.md)
- [Credibility and draft comparison](../../docs/credibility/README.md)
- [Generated data appendices](data/README.md)

## 2. Phase 1: flock size

Evidence: `../phase1/claim/README.md`, `../phase1/claim/packages/a/`, and `../phase1/claim/packages/f/`.

![Figure 1. Success-rate surface for the three controllers on the compact start.](figures/f1_reliability_heatmaps.png)

*Figure 1. Phase 1 is the left panel; Kubo and FAT are Phase 4. Sources: `../phase1/claim/packages/a/reliability.csv` and `../phase4/{kubo,fat}_size/claim/packages/a/reliability.csv`.*

| Flock size N | D_min | D_max | D_overcrowd | Meaning |
|---|---|---|---|---|
| 5, 10 | 2 | 35 (grid ceiling) | none | One dog is not reliable; D = 2 through D = 35 remain reliable |
| 25 to 400 | 1 | 35 (grid ceiling) | none | One dog reaches R >= 0.90; reliability remains above the bar through D = 35 |

Bootstrap intervals on every baseline D_min have width zero. Source: `../phase1/claim/packages/a/frontier.csv`.

| D_max fact | Reading |
|---|---|
| D_max = 35 for every N | No baseline overcrowding was observed |
| Why 35? | It is the largest tested value in {1, 2, 3, 4, 6, 10, 15, 20, 25, 35} |
| What 35 is not | It is not a measured collapse or a general upper limit |
| Hard failure? | No baseline Phase 1 cell is a hard failure |

Overall Phase 1 merge success is 0.963, with 169 failures in 4,540 rows. Failures are concentrated at one dog for the two smallest flocks.

| Cell | R at D = 1 | R at D = 2 | Main failure labels |
|---|---:|---:|---|
| N = 5 | 0.07 | 1.00 | oscillation: 93 |
| N = 10 | 0.24 | 1.00 | stuck: 58, oscillation: 18 |

| Regime | Cells | Reading |
|---|---:|---|
| Wasteful overspend | 88 | Already reliable; more dogs only add path |
| Efficient | 10 | Near the useful D |
| Under-resourced | 2 | N = 5 and N = 10 at D = 1 |

![Figure 2. Cost against D.](figures/f3_cost_vs_d.png)

*Figure 2. Finish time is flat while total path is proportional to D. Source: `../phase1/claim/merged_trials.csv`.*

Median finish time is 183 ticks (p90 = 198). On successful trials, median is 182 and p90 is 195. For N >= 25, median path per dog is about 148 world units.

![Figure 3. D_min against N, with the 2025 draft for contrast.](figures/f2_dmin_vs_n.png)

*Figure 3. Sources: `../phase1/claim/packages/a/frontier.csv`, `../phase4/*/size/claim/packages/a/frontier.csv`, and draft Table A3.*

| N | Strombom | Kubo | FAT | 2025 draft |
|---:|---:|---:|---:|---:|
| 5 | 2 | 3 | 1 | 1 |
| 10 | 2 | 1 | 1 | 1 |
| 25 | 1 | 1 | none <= 35 | 1 |
| 50 | 1 | 1 | none <= 35 | 1 |
| 75 | 1 | 1 | none <= 35 | n/a |
| 100 | 1 | 1 | none <= 35 | 1 |
| 150 | 1 | 1 | none <= 35 | 3 |
| 200 | 1 | 1 | none <= 35 | 20 |
| 300 | 1 | 1 | none <= 35 | 20 |
| 400 | 1 | 1 | none <= 35 | 35 |

*D_min at theta = 0.90 on compact starts. Kubo at N = 5 has bootstrap [1, 3]; R is 0.77 at D = 1, 0.71 at D = 2, and 0.97 at D = 6. Sources: the frontier and `dmin_bootstrap.csv` files above.*

Observed baseline D_min has only two levels: 2 for N in {5, 10}, and 1 for N >= 25.

| Model | Leave-one-N-out RMSE | Reading |
|---|---:|---|
| Constant | 0.44 | One flat D_min |
| Linear | 0.44 | Straight line in N |
| Power law | 0.25 | Smooth log-log curve |
| Piecewise | 0.13 | Two levels with a break at N = 10 |

![Figure 4. Leave-one-N-out RMSE by model.](figures/f8_scaling_rmse.svg)

*Figure 4. The piecewise fit benefits from encoding the observed step. Source: `../phase1/claim/packages/f/scaling_cv.csv`. C6b cannot be tested because there is no growth band to fit.*

## 3. Phase 2: starting structure

Evidence: `../phase2/claim/README.md` and `../phase2/claim/packages/b/`.

![Four starting layouts.](figures/schematics/en/four_layouts.svg)

*Structure contrast holds N fixed and changes only the start shape.*

D_min = 1 for all 12 layout by N cells, and every bootstrap interval has width zero. At D = 1, every cell has R = 1.00. D_max = 35 is the grid ceiling in every cell, with no D_overcrowd.

![Figure 5. Median total path at D = 1 by layout.](figures/f4_layout_cost.png)

*Figure 5. Source: `../phase2/claim/merged_trials.csv` at D = 1.*

| Layout | N | R at D = 1 | Median ticks | vs compact | Median path | vs compact |
|---|---:|---:|---:|---:|---:|---:|
| compact | 50 | 1.00 | 195 | 1.0x | 157 | 1.0x |
| compact | 100 | 1.00 | 204 | 1.0x | 161 | 1.0x |
| compact | 200 | 1.00 | 191 | 1.0x | 144 | 1.0x |
| split | 50 | 1.00 | 195 | 1.0x | 158 | 1.0x |
| split | 100 | 1.00 | 205 | 1.0x | 162 | 1.0x |
| split | 200 | 1.00 | 193 | 1.0x | 144 | 1.0x |
| outlier_rich | 50 | 1.00 | 224 | 1.1x | 209 | 1.3x |
| outlier_rich | 100 | 1.00 | 501 | 2.5x | 554 | 3.4x |
| outlier_rich | 200 | 1.00 | 1,228 | 6.4x | 1,647 | 11.4x |
| wide | 50 | 1.00 | 2,138 | 11.0x | 2,925 | 18.6x |
| wide | 100 | 1.00 | 3,074 | 15.1x | 4,319 | 26.8x |
| wide | 200 | 1.00 | 3,870 | 20.3x | 5,213 | 36.2x |

| Layout | Empirical reading |
|---|---|
| wide | 11x to 20x the ticks and 19x to 36x the path of compact |
| outlier_rich | At N = 200, 6.4x the ticks and 11.4x the path of compact |
| split | Medians match compact; mean fragmentation is about 0.99, so treat this as a check rather than a finding |
| compact | Reference |

For wide starts, B* = 2 at N = 50, 100, and 200. Median total path falls from 2,925 to 2,337, from 4,319 to 3,003, and from 5,213 to 3,694. Source: `../phase2/claim/packages/b/frontier_by_layout.csv`.

![Figure 6. Wide starts: median path at D = 1 versus D = 2.](figures/f10_wide_bstar_path.png)

*Figure 6. Source: `../phase2/claim/merged_trials.csv`, wide layout.*

## 4. Phase 4: controller transfer

Evidence: `../phase4/README.md`, `../phase4/kubo_structure/claim/README.md`, `../phase4/package_d/`, and `../phase4/kubo_structure/claim/outlier_rich_n200_window.json`.

![Transfer idea across methods.](figures/schematics/en/transfer_sketch.svg)

*Same grids and layouts; label each frontier feature shared, shifted, or absent.*

### Compact size map

Kubo has D_min = 3 at N = 5 and D_min = 1 from N = 10 through 400. D_max = 35 is the grid ceiling for every size cell, with no overcrowding. Overall success is 0.991, and all failures are timeouts.

FAT has D_min = 1 at N in {5, 10}; both cells have D_max = 35 as a grid ceiling. For N >= 25, no D <= 35 reaches R >= 0.90, so D_min and D_max are undefined. For N = 50 through 400, best R by N is 0.40 to 0.53, while individual cell R reaches as low as about 0.17. About half of FAT size trials fail: 39% by oscillation and 7% by stuck behavior.

| Case | Frontier fields | Empirical reading |
|---|---|---|
| D_max = 35, no D_overcrowd | D_min present | Reliable at the grid ceiling; upper collapse not measured |
| Hard failure | D_min and D_max empty | No tested D reaches theta |
| True overcrowding | D_overcrowd present and D_max below 35 | Not observed in completed phases |

Package D size labels are 8 shared, 7 shifted, and 29 absent. The absent count is dominated by overcrowding rows because no controller overcrowds on compact starts. Source: `../phase4/package_d/size/transfer_summary.csv`.

![Figure 7. How trials end on the size maps.](figures/f6_failure_modes.png)

*Figure 7. Source: `failure_mode` in claim `merged_trials.csv` for Phase 1, Kubo size, and FAT size.*

### Structure map

| Layout | N | Strombom | Kubo | FAT |
|---|---:|---:|---:|---:|
| compact | 50 | 1 | 1 | none (best R = 0.47) |
| compact | 100 | 1 | 1 | none (best R = 0.40) |
| compact | 200 | 1 | 1 | none (best R = 0.47) |
| split | 50 | 1 | 1 | none (best R = 0.50) |
| split | 100 | 1 | 1 | none (best R = 0.47) |
| split | 200 | 1 | 1 | none (best R = 0.40) |
| outlier_rich | 50 | 1 | 1 | none (best R = 0.10) |
| outlier_rich | 100 | 1 | 1 | none (best R = 0.00) |
| outlier_rich | 200 | 1 | 20 | none (best R = 0.00) |
| wide | 50 | 1 | none (best R = 0.49) | none (best R = 0.00) |
| wide | 100 | 1 | none (best R = 0.54) | none (best R = 0.00) |
| wide | 200 | 1 | none (best R = 0.47) | none (best R = 0.00) |

*D_min by layout and controller. `none` means no D <= 35 reaches R = 0.90. Source: `../phase4/package_d/structure/frontier_by_method_layout.csv`.*

![Figure 8. R against D at N = 200 by layout.](figures/f5_layout_reliability_curves.png)

*Figure 8. Source: structure claim `merged_trials.csv` files.*

| D | Seeds | R | R >= 0.90? |
|---:|---:|---:|:---:|
| 1 | 200 | 0.745 | no |
| 2 | 200 | 0.855 | no |
| 3 | 200 | 0.835 | no |
| 4 | 200 | 0.860 | no |
| 6 | 200 | 0.890 | no |
| 10 | 200 | 0.875 | no |
| 15 | 200 | 0.855 | no |
| 20 | 200 | 0.935 | yes |
| 25 | 200 | 0.910 | yes |
| 35 | 30 | 0.967 | yes |

| Kubo `outlier_rich`, N = 200 | Value |
|---|---|
| D_min | 20 |
| Bootstrap interval | [2, 20] from `merged_dmin_bootstrap.csv`, `n_seeds_ref = 200` |
| Overcrowding | none |
| Uncertainty | Several D < 20 lie near 0.90, so bootstrap resamples can place D_min below 20 |

![Figure 9. Kubo outlier_rich N = 200 with Wilson 95% CI.](figures/f9_kubo_outlier_rich_n200.png)

*Figure 9. Sources: `../phase4/kubo_structure/claim/merged_trials.csv`, `merged_dmin_bootstrap.csv`, and `outlier_rich_n200_window.json`.*

| Finding | Empirical reading |
|---|---|
| Kubo + wide | Best R is 0.47 to 0.54; failures are timeout or scatter; more dogs raise R toward about 0.5 but not 0.90 |
| Kubo + outlier_rich, N = 200 | Shifted to D_min = 20, with bootstrap [2, 20] |
| FAT structure | No layout at N >= 50 reaches R = 0.90 |

| Controller | Mean I_dir at D = 35, N = 100 | Mean I_dir over all D at N = 100 |
|---|---:|---:|
| Baseline (`strombom_multi`) | about 0.09 | about 0.05 |
| Kubo | about 0.15 | about 0.10 |
| FAT | about 0.48 | about 0.40 |

| Association check | Value | Reading |
|---|---:|---|
| Pearson r(I_dir, success), FAT size merge | about -0.87 | Strong negative association |
| Causal claim | no | Observational association, not a controlled mechanism experiment |

![Figure 10. Interference index against D.](figures/f7_interference.png)

*Figure 10. Source: `mean_i_dir` in claim `merged_trials.csv` files.*

## 5. Synthesis and claim snapshot

![Claims scorecard from progress tracker and claim packages.](figures/schematics/en/claims_scorecard.svg)

*Verdict colours match the table below. Live verdicts: `../../docs/progress_tracker.md`.*

| Claim | Verdict | Evidence | Reading |
|---|---|---|---|
| C1a | REJECTED | Phase 2 Package B: D_min = 1 for all four layouts at N = 50, 100, 200; bootstrap width 0 | Baseline only; Kubo structure shifts |
| C1b | INCONCLUSIVE | No baseline D_min shift; Package B reports NaN likelihoods | Cost still depends strongly on layout |
| C2a | REJECTED | Phase 1 Package A: 0 overcrowding cells at theta = 0.90 | None in Phase 4 either |
| C2b | SKIPPED | No overcrowding cell for T = 20,000 | No T1 run |
| C3 | INCONCLUSIVE | Baseline mechanism contrast requires overcrowding | Kubo contrast cells exist but Package C was not completed |
| C4 | SUPPORTED, partial | Strombom and Kubo share compact D_min for N >= 25; FAT is absent; Kubo wide is absent; Kubo `outlier_rich`, N = 200 shifts | Controller transfer is conditional |
| C6a | EVALUATED, weak | Piecewise RMSE 0.13 versus power-law RMSE 0.25 | The fit uses only observed levels {2, 1}; it is not a scaling law |
| C5a/b, C6b, C7a/b | UNEVALUATED | Phases 5 and 7 not run; C6b has no stated growth band | No result claim |

## 6. Uncertainty, limits, and phases not run

| Status | Topic | Current limit |
|---|---|---|
| Ceiling effect | Baseline reliability | R = 1.00 at D = 1 on almost every baseline cell, limiting visible scaling |
| Grid ceiling | D_max = 35 | No upper collapse was measured; behavior above 35 is unknown |
| Hard failure | FAT and Kubo wide | Empty D_min and D_max mean no tested D reaches 0.90, not that an upper frontier was found |
| Wide interval | Kubo `outlier_rich`, N = 200 | Point D_min = 20 at 200 seeds, R = 0.935, but bootstrap is [2, 20] |
| Weak fit | C6a | Two observed D_min levels do not support a general scaling law |
| Observational only | I_dir | r about -0.87 does not establish interference as a cause |
| Unverified generator behavior | `split` layout | Cost and D_min match compact; separation at t = 0 still needs confirmation |
| One simulated task | External validity | Results do not establish field performance, biological realism, or a universal farm rule |
| Discrete D grid | Resolution | Differences finer than the tested dog-count steps are unresolved |

Phases not run:

- Phase 3 and C2b were skipped because baseline produced zero overcrowding cells.
- Phase 5 sensing, range, and communication experiments were not run.
- Phase 7 early-warning Package G was not run.
- The 2025 draft was not rerun, and quantitative NetLogo parity was not established.

For the removed setup, method, draft, NetLogo, provenance, and glossary material, use the canonical documents linked in section 1. Generated empirical tables and their source paths are indexed in [data/README.md](data/README.md).
