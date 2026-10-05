# How many shepherds does a flock need?

HerdSim scaling_v2: summary of Phases 1 (size), 2 (structure) and 4 (transfer).
An HTML version with embedded figures is in `SUMMARY_REPORT.html`. Vietnamese version: `SUMMARY_REPORT_vi.md`.

## Summary

We asked how many shepherds a flock needs as the flock grows, and whether the answer depends on the controller and on how the flock starts. This report covers the three phases that are finished at claim grade: **Phase 1** (size map, baseline), **Phase 2** (starting structure, baseline) and **Phase 4** (transfer to Kubo and FAT).

- **On this task, one dog is enough for the baseline from N = 25 up to N = 400.** Only N = 5 and 10 need two dogs, because a single dog oscillates on a tiny flock (success 7% and 24% at D = 1).
- **Extra dogs buy nothing and cost a lot.** Median time to finish stays near 183 ticks for every D; total path grows by about 146 units per added dog. 88 of the 100 (N, D) cells are labelled wasteful overspend.
- **The 2025 draft's steep D_min(N) curve and its overcrowding are not reproduced.** The draft needs 20 to 35 dogs at N >= 200. Here one dog finishes N = 400 in a median of 168 ticks. The tasks differ (collect + hold 800 ticks + exit through a gate, versus a 120-unit drive into a goal disk), so this is a statement about the task, not a refutation (section 6).
- **Starting structure changes cost, not D_min (baseline).** A wide start needs 11x to 20x more ticks and 19x to 36x more path than a compact start with the same one dog; outlier_rich grows with N (up to 6x ticks, 11x path at N = 200).
- **Controllers differ sharply.** Kubo matches the baseline on compact starts but fails on wide starts (R <= 0.54 for any D) and is borderline on outlier_rich at N = 200. FAT reaches R >= 0.90 only for N <= 10.
- **Caveat on every positive claim:** a ceiling effect. R = 1.00 at D = 1 leaves nothing to measure, so the benchmark cannot yet show how collective difficulty scales. Section 8 lists ways to make it informative.

## 1. Why we ran this and how it relates to the draft paper

The 2025 draft (`docs/papers/sheep-scaling_paper2025.pdf`) swept shepherd count D and flock size N in a NetLogo model and reported a reliable band of D for every N. It found that one dog handles up to about 100 sheep, that larger flocks need many more dogs with diminishing returns, and that too many dogs can hurt. It had no uncertainty on D_min and used a flat 100 seeds per cell.

HerdSim (`scaling_v2`, [main_scaling_plan.md](../../docs/main_scaling_plan.md)) re-asks the question with a frozen protocol: the same D grid, a bootstrap interval on D_min, a cheap scout followed by a 100-seed claim reseed near the frontier, a structure factor (starting layout), and a transfer test across controllers. The research questions are RQ1 structure, RQ2 size, RQ3 mechanism, RQ4 transfer, RQ5 information, RQ6 fits and RQ7 early warning. Phases 1, 2 and 4 cover RQ2, RQ1 and RQ4.

|  | 2025 draft | HerdSim `scaling_v2` |
|---|---|---|
| Task | Collect, hold 800 ticks, exit through gate | `drive_to_goal`: every sheep inside a goal disk |
| Arena | 101 x 71 patches, pen at centre | 500 x 500, goal at (370, 250), radius 15 * sqrt(N / 50) |
| Timeout | 10,000 ticks | T0 = 10,000 (T1 = 20,000 for overcrowding cells) |
| Grid | 11 N x 10 D, 100 seeds each | 10 N x 10 D; 30 seeds, then 100 on frontier windows |
| D_min uncertainty | none | bootstrap over seeds (1,000 resamples) |
| Factors beyond N and D | none | layout X0, controller, information (later phases) |

*Table 1. Draft versus current protocol.*

## 2. How the experiments were run

Every protocol goes through three grades. **Pilot** (smoke): a handful of cells to check that the code runs. **Scout**: 30 seeds on every (N, D) cell. **Claim**: for each (method, layout, N) the cells that decide D_min (the scout D_min and its grid neighbours, plus any overcrowding window) are re-run at 100 seeds with fresh seeds. The claim analysis then uses 100 seeds on those cells and 30 elsewhere. A trial succeeds when every sheep is inside the goal disk before the time limit.

| Phase | Question | Method | Layout | Pilot | Scout | Claim |
|---|---|---|---|---|---|---|
| 1 | Size map | strombom_multi | compact | 150 | 3,000 | 2,200 |
| 2 | Structure | strombom_multi | 4 layouts | 600 | 3,600 | 2,400 |
| 4a | Transfer: size | kubo | compact | - | 3,000 | 2,100 |
| 4a | Transfer: size | fat | compact | - | 3,000 | 2,000 |
| 4b | Transfer: structure | kubo | 4 layouts | - | 3,600 | 2,800 |
| 4b | Transfer: structure | fat | 4 layouts | - | 3,600 | 2,400 |
|  | **Total simulations** |  |  |  |  | **34,450** |

*Table 2. Trials per stage (rows of `trials.csv`; merged analysis files are slightly larger).*

Reading a heatmap: rows are flock size, columns are shepherd count, and each cell is the percentage of seeds that succeeded. D_min is the first column in a row that reaches 90%.

## 3. Phase 1: how many dogs does a flock of size N need?

Goal: map the success rate R(N, D) for the baseline `strombom_multi` controller on a compact start, and from it D_min, D_overcrowd, D_max and the cheapest reliable D.

![Figure 1. Success-rate surface for the three controllers on the compact start. Phase 1 is the left panel; the other two are Phase 4 (section 5).](figures/f1_reliability_heatmaps.png)

*Figure 1. Success-rate surface for the three controllers on the compact start. Phase 1 is the left panel; the other two are Phase 4 (section 5).*

### What we see (baseline)

- **D_min = 1 for N >= 25, D_min = 2 for N = 5 and 10.** The bootstrap interval on D_min has width zero for every N.
- **No overcrowding.** R stays at or above 0.90 up to D = 35 for every N, so D_overcrowd is undefined and D_max is the grid ceiling.
- **Failures are rare and only at D = 1 on tiny flocks.** Overall success is 96%; of the 169 failures 93 are oscillation at N = 5, and 18 oscillation plus 58 stuck at N = 10. These cells have R = 0.07 and 0.24 at D = 1 and 1.00 at D = 2.
- **Regime labels over the 100 (N, D) cells:** 88 wasteful overspend, 10 efficient operation, 2 under-resourced failure.

![Figure 2. Cost against D (log-log). Time to finish is flat: the task is a 120-unit drive at speed 1, so about 120 ticks are unavoidable and more dogs cannot shorten them. Path is proportional to D.](figures/f3_cost_vs_d.png)

*Figure 2. Cost against D (log-log). Time to finish is flat: the task is a 120-unit drive at speed 1, so about 120 ticks are unavoidable and more dogs cannot shorten them. Path is proportional to D.*

### Why

Time is flat because collection and drive are already fast with one dog (median 183 ticks, p90 198, against a 10,000-tick budget). Path grows with D because every dog walks for the whole trial: about 146 units per dog for N >= 25. That is why almost every cell is wasteful: only the first dog does useful work.

Why N = 5 and 10 need two dogs is not tested here. A plausible reading, which the data are consistent with but do not prove, is that one dog on a flock of a few sheep alternates between collecting and driving and never settles (the dominant failure label is `oscillation`). A second dog removes the alternation.

![Figure 3. D_min against N. The grey line is the 2025 draft (Table A3). The draft needs many dogs from N = 150 upward; the HerdSim baseline stays at one. FAT has no D_min for N >= 25.](figures/f2_dmin_vs_n.png)

*Figure 3. D_min against N. The grey line is the 2025 draft (Table A3). The draft needs many dogs from N = 150 upward; the HerdSim baseline stays at one. FAT has no D_min for N >= 25.*

| N | Strombom | Kubo | FAT | 2025 draft |
|---|---|---|---|---|
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

*Table 3. D_min at theta = 0.90 by flock size (compact start). Draft values from its Table A3.*

### Scaling fits (Package F)

The leave-one-N-out RMSE of D_min is 0.44 for a constant, 0.44 linear, 0.25 power law and 0.13 piecewise. Read this carefully: D_min takes only the values 2 (N <= 10) and 1 (N >= 25), so the piecewise model fits it perfectly by construction (break at N = 10). It does not show a scaling law, and it cannot test claim C6b (log-log slope below 1 in an N band) because there is no growth to fit.

## 4. Phase 2: does the starting structure change the answer?

Goal: hold N fixed at 50, 100 and 200 and change only the starting layout. **compact**: tight Gaussian blob. **wide**: Gaussian with 6.7x the width, so sheep are far from each other. **split**: three clusters. **outlier_rich**: a core with about 20% outliers beyond the controller's collect radius. The test is whether D_min moves by at least one grid step across layouts (claim C1a).

**Result for D_min: no.** D_min = 1 for all 12 (layout, N) cells and the bootstrap interval has width zero. Every cell at D = 1 reaches R = 1.00, so D_min cannot drop and the structure effect on D_min is not measurable with this controller and task (a floor effect).

**Result for cost: yes, large.** Success at D = 1 is 100% everywhere, but the work needed to get there differs by an order of magnitude:

![Figure 4. Median total path at D = 1 by layout. Success rate is printed on each bar.](figures/f4_layout_cost.png)

*Figure 4. Median total path at D = 1 by layout. Success rate is printed on each bar.*

| Layout | N | R at D=1 | Median ticks | vs compact | Median path | vs compact |
|---|---|---|---|---|---|---|
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

*Table 4. Baseline cost of one dog by layout (100 seeds per cell).*

- **wide** costs 11x to 20x more ticks and 19x to 36x more path than compact. The cost gap grows with N (path ratio 19x, 27x, 36x), because the flock must first be collected from a larger area.
- **outlier_rich** is cheap at N = 50 (about 1.1x ticks) and expensive at N = 200 (6.4x ticks, 11x path): the number of stragglers grows with N, each needing its own collection trip.
- **split looks the same as compact** (identical medians at N = 50). The three clusters are gathered almost immediately (mean fragmentation over the trial is 0.98 for both). Treat this as a result to double-check, not as a finding: the layout may not be creating a hard sub-flock problem for this controller.
- **More dogs do help on wide starts.** The cheapest reliable D (B*) is 2, not 1, on wide layouts (path 2,337 at N = 50 against 2,925 at D = 1). This is the only place in the baseline data where a second dog pays for itself.

Interpretation: starting structure acts through effort and time long before it moves the reliability frontier. A frontier-only analysis would miss it. We recommend reporting path and ticks next to D_min whenever structure is varied.

## 5. Phase 4: do the findings transfer to other controllers?

Goal: repeat the size map and the structure contrast with **Kubo** and **FAT** (potential-field), and compare with the baseline. A feature is **shared** if both controllers have the same D_min, **shifted** if different, **absent** if one side has none.

### Size map

- **Kubo** has D_min = 1 for N from 10 to 400, like the baseline, and D_min = 3 at N = 5 (success 77% at D = 1, 71% at D = 2, then 100%). Overall success 99%; all failures are timeouts.
- **FAT** has D_min = 1 for N = 5 and 10 but never reaches 0.90 for N >= 25 with any D up to 35: R is 0.6 to 0.8 at N = 25, 0.2 to 0.5 beyond. More dogs do not help. Half of all FAT trials fail, mostly by oscillation (39% of trials) and getting stuck (7%).
- Package D size table: 8 shared D_min entries, 7 shifted, 29 absent. The 29 absent are mostly overcrowding entries (no controller overcrowds on compact starts), so the count is not a measure of disagreement.

![Figure 5. How trials end. FAT dominates the failure mass; the baseline barely fails.](figures/f6_failure_modes.png)

*Figure 5. How trials end. FAT dominates the failure mass; the baseline barely fails.*

### Structure at N = 50, 100, 200

| Layout | N | Strombom | Kubo | FAT |
|---|---|---|---|---|
| compact | 50 | 1 | 1 | none (best R=0.47) |
| compact | 100 | 1 | 1 | none (best R=0.40) |
| compact | 200 | 1 | 1 | none (best R=0.47) |
| split | 50 | 1 | 1 | none (best R=0.50) |
| split | 100 | 1 | 1 | none (best R=0.47) |
| split | 200 | 1 | 1 | none (best R=0.40) |
| outlier_rich | 50 | 1 | 1 | none (best R=0.10) |
| outlier_rich | 100 | 1 | 1 | none (best R=0.00) |
| outlier_rich | 200 | 1 | 4, overcrowd at 10 | none (best R=0.00) |
| wide | 50 | 1 | none (best R=0.49) | none (best R=0.00) |
| wide | 100 | 1 | none (best R=0.54) | none (best R=0.00) |
| wide | 200 | 1 | none (best R=0.47) | none (best R=0.00) |

*Table 5. D_min by layout and controller. 'none' = no D <= 35 reaches 0.90; best R over D in brackets.*

![Figure 6. R against D at N = 200 by layout (on the baseline all four curves sit on R = 1.00 and overlap). Kubo's wide start plateaus near 0.4 to 0.5 and its outlier_rich curve hovers around the 0.90 line; FAT never gets near it.](figures/f5_layout_reliability_curves.png)

*Figure 6. R against D at N = 200 by layout (on the baseline all four curves sit on R = 1.00 and overlap). Kubo's wide start plateaus near 0.4 to 0.5 and its outlier_rich curve hovers around the 0.90 line; FAT never gets near it.*

- **Kubo on wide starts fails** at every N (pooled R about 0.42 to 0.48, best single D 0.54). The failures are timeouts and scatter: the flock is not collected within 10,000 ticks. More dogs raise R slowly (0.2 at D = 1 to about 0.5), without reaching the bar.
- **Kubo on outlier_rich at N = 200** has D_min = 4 and is labelled overcrowded at D = 10. The curve (0.70, 0.84, 0.86, 0.93, 0.91, 0.85, 0.87, 0.93 ...) is a noisy band around 0.90, not a collapse. Treat it as a soft frontier: with 100 seeds the 0.06 interval on R spans the whole band.
- **FAT**: nothing reaches the bar on any layout at N >= 50. wide and outlier_rich are close to zero; compact and split are at about 0.3.
- **Interference.** Mean I_dir saturates with D (about 0.09 baseline, 0.15 Kubo, 0.48 FAT at N = 100). It is zero at D = 1 by construction, so its link with success is confounded with D; the Package D value r(I_dir, success) = -0.87 for FAT may mostly reflect that FAT fails at large D with high I_dir, not a tested mechanism.

![Figure 7. Interference index against D. It rises from zero at one dog and levels off.](figures/f7_interference.png)

*Figure 7. Interference index against D. It rises from zero at one dog and levels off.*

Interpretation: controller architecture matters more than the number of dogs. Reactive collect-and-drive controllers (Strombom, Kubo) are limited by how the flock starts; the potential-field controller is limited by its own dynamics and no dog count rescues it on this task.

## 6. Comparison with the 2025 draft

| Draft finding | HerdSim here | Comment |
|---|---|---|
| One dog suffices up to N ~ 100, then collapses (N = 150, D = 1: SR ~ 1%) | One dog suffices up to N = 400 (R = 1.00 at N = 150 and 400) | Not reproduced. Different task and arena. |
| D_min rises to 20 to 35 for N >= 200 | D_min = 1 | Not reproduced. |
| Overcrowding (e.g. N = 10, D >= 20 worse than fewer) | R = 1.00 at D = 35 for N = 5 to 400 (baseline) | Not reproduced for the baseline; soft evidence for Kubo outlier_rich. |
| Time falls with D and rises with N; distance saturates | Time flat in D and N; path linear in D | Different shape: no saturation here. |
| Spread correlates with failure (rho = -0.70; S_bar * N: -0.83) | Not tested (Phase 3 needs overcrowding cells) | Cohesion/spread metrics are recorded and can be analysed on existing trials. |
| Single scheme, no uncertainty on D_min | Bootstrap interval, three controllers, four layouts | New: width-zero intervals; structure and controller effects. |

*Table 6. Which draft findings carry over.*

Why the outcomes diverge: the draft's collapse comes from the **collect and hold** phases, where the flock has to be compacted and kept inside a containment circle for 800 ticks and 90% of its failures stall in collection. `drive_to_goal` removes holding and exit entirely, uses a goal radius that scales with N, and a flock that starts at the centre of a 500-unit field with 120 units to cover. The baseline finishes in about 183 of 10,000 ticks, so the time budget (the thing that makes extra dogs necessary in the draft) is never binding. This is my reading of the protocol; it has not been tested by changing the task.

## 7. Claims scorecard

| Claim | Verdict | Evidence | Comment |
|---|---|---|---|
| C1a | REJECTED | Baseline: D_min = 1 for all 4 layouts at N = 50, 100, 200 (bootstrap interval has width 0). | True for the baseline. Not true for Kubo: D_min = 4 on outlier_rich N = 200 and no D_min on wide (Phase 4). |
| C1b | INCONCLUSIVE | No D_min shift on the baseline, so the state-vs-(N, D) comparison has nothing to explain. | Package B reports NaN likelihoods. Cost (path, ticks) does depend on layout, see section 4. |
| C2a | REJECTED | Baseline: no overcrowding cell on the compact map (R >= 0.90 up to D = 35). | Overcrowding appears only for Kubo outlier_rich N = 200 (D_overcrowd = 10), and it is a soft effect. |
| C2b | SKIPPED | No overcrowding cell to extend to T = 20,000. |  |
| C3 | INCONCLUSIVE | Mechanism contrast needs an overcrowding cell; none on the baseline. | Kubo outlier_rich N = 200 is a candidate cell that already exists in the data. |
| C4 | SUPPORTED (partial) | Baseline and Kubo share D_min = 1 for N >= 25; FAT does not transfer. | The tracker says SUPPORTED, discuss/phase4.md says partial. Partial is the accurate wording. |
| C6a | EVALUATED, weak | Piecewise beats power law on leave-one-N-out RMSE (0.13 vs 0.25). | The 'piecewise' fit is just the two levels {2, 1} with a break at N = 10. It is not a scaling law. |
| C5a/b, C6b, C7a/b | UNEVALUATED | Phases 5 and 7 not run; C6b has no stated N band yet. |  |

## 8. Limits and suggested next steps

- **Ceiling effect.** R = 1.00 at D = 1 for almost every baseline cell. The surface is flat, so C1 to C3 cannot be supported or rejected informatively. A harder setting is needed before further phases add value. Candidate knobs (not tried): shorter T0, longer drive, smaller goal, a hold phase, noisy or limited observation (Phase 5).
- **Documentation mismatch.** `docs/discuss/phase4.md` states Kubo has D_min = 1 across all four layouts and no overcrowding; the data (Table 5) show no D_min on wide and D_min = 4 with overcrowding at 10 on outlier_rich N = 200.
- **Tracker wording.** C4 reads SUPPORTED where the discussion says partial; C6a reads EVALUATED but the fit is degenerate.
- **Soft frontiers.** Kubo outlier_rich N = 200 sits inside the +/-0.06 interval of R. Following the plan rule, raise that window to 200 seeds before treating D_overcrowd = 10 as real.
- **A usable mechanism test exists.** C3 was marked inconclusive for lack of overcrowding cells, but Kubo outlier_rich N = 200 (and Kubo wide, where success does not improve with D) could serve as contrast cells.
- **Split layout.** Confirm the generator produces separated clusters at the start and not only a lower mean fragmentation index; the results are indistinguishable from compact.
- **Scope.** One task, simulated controllers, one theta; results are statements about this simulation only.

## 9. Where the numbers come from

| Item | Source |
|---|---|
| Trial rows | `scaling/results/phase*/**/merged_trials.csv` |
| D_min, regimes | `phase1/claim/packages/a/`, `phase4/*_size/claim/packages/a/` |
| Structure frontier | `phase2/claim/packages/b/`, `phase4/package_d/structure/frontier_by_method_layout.csv` |
| Transfer tables | `phase4/package_d/` |
| Fits | `phase1/claim/packages/f/` |
| Draft values | `scaling/docs/notes/sheep-scaling_paper2025.md` (from the PDF's Table A3) |

*Table 7. Provenance.*
