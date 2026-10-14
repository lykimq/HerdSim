# HerdSim scaling study: results

This is the results write-up for the scaling study. It covers what the claim-grade runs found, what each finding means, and where the evidence is thin.

It assumes you've read the [main README](../../README.md). That's where the setup lives: arena, grids, methods, how a campaign runs, what each metric means. All numbers below come from the claim merges (`merged_trials.csv`) unless a section says otherwise.

## Summary

- **One dog is enough far earlier than we expected.** On the baseline (`strombom_multi`, compact start), every flock from 25 to 400 sheep is herded reliably by a single dog. Only the tiny flocks (N = 5 and 10) need two.
- **Extra dogs don't hurt, they just walk.** We never saw overcrowding up to 35 dogs. Every dog past the first adds path and almost nothing else. Control efficiency falls almost exactly as 1/D.
- **Start shape changes the bill, not the headcount.** Wide and outlier-rich starts take 10x to 30x more time and path, but one dog still gets there.
- **The story is method-specific.** Kubo matches the baseline on compact starts and falls apart on wide ones. FAT never clears the bar past N = 10. Its dogs work against each other, and the interference metric shows it clearly.
- **Sensing range is the one information knob that moved the answer.** Halving it from 65 to 32.5 costs 1 to 2 extra dogs. Going above 65 buys nothing.
- **The easy compact map limits everything downstream.** With `D_min` stuck at 1, scaling fits, mechanism contrasts and early warning have little signal to work with.

## How much we ran

| Question | What | Scout | Claim | Status |
|----------|------|------:|------:|--------|
| RQ2 size | baseline, compact, 10 x 10 grid | 3,000 | 2,200 | done |
| RQ1 structure | baseline, 4 layouts, N = 50/100/200 | 3,600 | 2,400 | done |
| RQ4 transfer | Kubo and FAT, size + structure | 13,200 | 10,500 | done |
| RQ5 information | obs / range / comm ladders | 3,600 | 4,100 | done |
| RQ3 mechanism | needs overcrowding cells | - | - | skipped |
| RQ6 fits, RQ7 early warning | analysis on RQ2 claim data | - | - | done |
| Phase 8 | collect-hold-gate size map | 2,062 / 3,000 | - | scout running |

That's about 43,000 trials for Phases 1 to 5, including 750 smoke runs. Claim reseeds go only to the cells near `D_min`, so most of the claim budget lands where the answer is decided.

---

## 1. Flock size: one dog goes a long way (RQ2)

The baseline size map is almost all success. The only real failures are N = 5 and N = 10 with a single dog, at R = 0.07 and 0.24. Give them a second dog and both go to R = 1.00.

![Reliability heatmaps for the three methods on compact starts.](../figures/f1_reliability_heatmaps.png)

*Success rate R(N, D) on compact starts. The baseline (left) is solid apart from the two tiny-flock cells at D = 1. Kubo looks similar; FAT has no reliable band past N = 10.*

| N | 5 | 10 | 25 | 50 | 75 | 100 | 150 | 200 | 300 | 400 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `D_min` | 2 | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

The bootstrap interval on every one of these is zero width. With 100 seeds near the boundary, the answer doesn't move.

The failed tiny-flock runs are labelled `oscillation` (111) or `stuck` (58): the flock goes back and forth or stops making progress, then runs out the clock. We haven't pinned down why five or ten sheep are harder for one dog than fifty. A likely factor is that a handful of sheep has less mutual attraction holding it together, so the dog keeps switching between collecting and driving. That's a guess, not something we tested.

### What happens past `D_min`

We were looking for overcrowding: a point where adding dogs makes success drop again. Up to 35 dogs it never happened. So `D_max = 35` here only means "top of the grid", not "this is where it breaks".

What extra dogs do instead is waste effort. Of the 100 (N, D) cells, 88 are `wasteful_overspend`, 10 are `efficient_operation` and 2 are `under_resourced_failure`. Finish time stays flat at about 183 ticks whatever D is, while total dog path grows with every dog.

Control efficiency (distance the flock gains toward the goal, divided by dog path) makes this very plain:

![Control efficiency against dog count.](../figures/report/r1_control_efficiency.png)

*Median control efficiency on compact starts, N >= 25. The baseline sits on the 1/D line: two dogs do exactly the work of one at twice the walking.*

For `strombom_multi`, efficiency drops from 0.72 at D = 1 to 0.021 at D = 35. That's 0.72 / 35, almost to the decimal. In plain terms, the flock makes the same progress whether it has 1 dog or 35. Every extra dog adds its own path and contributes nothing. Kubo loses a bit less on the first few dogs (0.89 to 0.53 going from 1 to 2 dogs), but from about D = 10 its curve falls at the same 1/D rate.

![Cost against dog count on the baseline.](../figures/f3_cost_vs_d.png)

*Finish time stays flat; path climbs with D. Waste, not collapse.*

## 2. Start shape: it changes the cost, not the dog count (RQ1)

At N = 50, 100 and 200, all four layouts have `D_min = 1` on the baseline. Start shape never changed how many dogs we needed. It changed how long the job took and how far the dog walked:

| Layout | N = 50 ticks / path | N = 100 ticks / path | N = 200 ticks / path |
|--------|--------------------:|---------------------:|---------------------:|
| compact | 195 / 158 | 204 / 161 | 191 / 144 |
| split | 195 / 158 | 205 / 162 | 193 / 144 |
| outlier_rich | 224 / 209 | 501 / 554 | 1,228 / 1,647 |
| wide | 2,138 / 2,925 | 3,074 / 4,319 | 3,870 / 5,213 |

*Median over successful runs at D = 1. Success is 1.00 in every cell.*

![Layout cost at one dog.](../figures/f4_layout_cost.png)

Wide starts cost 11x to 20x more time and 19x to 36x more path than compact. On wide, the cheapest reliable setup is two dogs (`B* = 2`). The second dog cuts median path (for example 5,213 to 3,694 at N = 200) while keeping R at 1.00. So it's an efficiency choice, not a rescue.

![Wide starts: path at D = 1 vs D = 2.](../figures/f10_wide_bstar_path.png)

The flock-shape metrics show what's going on under the hood:

![Fragmentation and cohesion by layout.](../figures/report/r3_layout_shape.png)

*Fragmentation is the share of the flock in the largest connected group, so 1.0 means one group. Cohesion is the mean distance of a sheep to the flock centre.*

- **Wide** flocks spend most of the run in pieces. Fragmentation is 0.64, so on average a third of the sheep are outside the main group. Cohesion is four times the compact value. The dog spends the run collecting, which is where the path goes.
- **Outlier-rich** sits in between (0.92). The core is tight, and the outliers cost one collect trip each.
- **Split** is indistinguishable from compact on every metric (0.99 fragmentation, same ticks, same path). The clusters are placed close enough that they merge before the dog arrives. That makes split a weak contrast in the current generator, and it's worth fixing before anyone leans on split results.

Since `D_min` never moved, we couldn't test the follow-up question (C1b): whether early flock state predicts difficulty better than N and D alone.

## 3. Other dog rules: partial transfer (RQ4)

We ran the same size and structure maps with Kubo and FAT. The point was to see which parts of the baseline story belong to the task and which belong to the controller.

`D_min` at theta = 0.90 ("-" means no D up to 35 reached it):

| Map | N | strombom_multi | kubo | fat |
|-----|---|---:|---:|---:|
| compact size | 5 | 2 | 3 | 1 |
| compact size | 10 | 2 | 1 | 1 |
| compact size | 25 to 400 | 1 | 1 | - |
| split | 50, 100, 200 | 1 | 1 | - |
| outlier_rich | 50, 100 | 1 | 1 | - |
| outlier_rich | 200 | 1 | 20 | - |
| wide | 50, 100, 200 | 1 | - | - |

![D_min against N across methods.](../figures/f2_dmin_vs_n.png)

*Baseline and Kubo stay on the one-dog floor for compact flocks. FAT has no `D_min` past N = 10. The steep curve is a 2025 NetLogo draft on a harder collect-hold-gate task, shown for contrast only; it was not rerun here.*

**Kubo** shares the compact floor exactly. It breaks on structure: on wide starts its best R is only 0.47 to 0.54, and on outlier_rich at N = 200 the point estimate jumps to 20 dogs. That last one is a soft edge. Even at 200 seeds the bootstrap interval is [2, 20], so it's best read as "somewhere between 2 and 20".

![Kubo outlier_rich at N = 200.](../figures/f9_kubo_outlier_rich_n200.png)

**FAT** is a different story. It clears the bar only at N = 5 and 10. Above that, best R sits between 0.40 and 0.53 on compact, and drops to near 0 on outlier_rich and wide. Adding dogs doesn't help.

The interference metric `I_dir` explains a lot of this. It is near 0 when the dogs move the same way and near 1 when their headings cancel out:

![Dog interference against dog count.](../figures/report/r2_interference.png)

*Median I_dir per trial, compact, N >= 25.*

- Baseline dogs settle around 0.09. They fan out behind the flock and mostly push the same way.
- Kubo plateaus around 0.15.
- FAT climbs from 0.27 at two dogs to about 0.6 at 15 or more. Each FAT dog chases the sheep farthest from itself, so dogs end up on opposite sides of the flock pushing it back and forth.

Within FAT, the split between outcomes is stark. Failed runs have a median `I_dir` of 0.63, successful ones 0.01, and the correlation with success is -0.83 (N >= 25). Failed FAT runs also have low coverage: 0.27 of the outer sheep are within a dog's reach, against 1.00 in the runs that succeed. This is a correlation, not a controlled test, but it's the clearest mechanism signal we have anywhere in the study.

How runs fail is just as method-specific (claim merges, size and structure maps combined):

| Method | Trials | none | oscillation | split | scatter | stuck | timeout |
|--------|------:|-----:|------------:|------:|--------:|------:|--------:|
| strombom_multi | 9,820 | 9,651 | 111 | 0 | 0 | 58 | 0 |
| kubo | 11,140 | 10,107 | 0 | 0 | 320 | 13 | 700 |
| fat | 9,680 | 3,100 | 3,721 | 1,298 | 474 | 581 | 506 |

The baseline only ever fails on tiny flocks with one dog. Kubo's failures are mostly wide starts (742 of 1,033) that run out the clock or scatter, and most of the rest are outlier_rich. FAT fails in every way the taxonomy has, and most of all by oscillating, which fits the tug-of-war picture above.

![Layout reliability across methods at N = 200.](../figures/f5_layout_reliability_curves.png)

So C4 holds only in part. The compact size floor transfers between Strombom and Kubo, but structure effects and the FAT results don't.

## 4. Information: can sensing replace dogs? (RQ5)

All three ladders ran on the baseline, compact starts, N = 100 and 200, and D in {1, 2, 3, 4, 6, 10}.

![D_min across the three information ladders.](../figures/f13_rq5_ladder_dmin.png)

*Crosses mark levels that never reach theta. Where N = 100 and N = 200 share a value, the markers overlap.*

**Sensing range is the clean result.**

| Sensing range | 32.5 | 65 | 97.5 | 130 |
|---------------|-----:|---:|-----:|----:|
| `D_min` at N = 100 | 3 | 1 | 1 | 1 |
| `D_min` at N = 200 | 2 | 1 | 1 | 1 |

Going from 32.5 to 65 saves 2 dogs at N = 100 and 1 at N = 200 (C5a). Past 65 there's nothing left to save (C5b).

Coverage shows why:

![Coverage and success at range 32.5 vs 65.](../figures/report/r4_range_coverage.png)

*Left: share of outer sheep within some dog's sensing range. Right: success. Solid lines are N = 100, dotted are N = 200.*

At range 65, coverage is already 1.00 with one dog, because one dog sees the whole flock. At 32.5, a single dog sees only 59% of the outer sheep at N = 100, so stragglers drift off unseen. Each added dog pushes coverage up (0.74, 0.82, 0.87), and success follows it over the 0.90 line at D = 3. So more dogs here are standing in for eyesight. N = 200 needs fewer extra dogs than N = 100, likely because the bigger flock is denser and its edge sits closer to the dog.

**Observation mode.** `global` and `local_positions` both have `D_min = 1`. `bearing_only` never reaches the bar at any D, with merge success about 0.22. Under bearing only, the dogs walk 10,000 to 78,000 units per run with control efficiency near 0. They move constantly and get the flock nowhere. That's a hard failure, not a graded dog saving.

**Communication.** All three modes have `D_min = 1` and R = 1.00. One dog already clears the bar, so there was nothing for sharing to save.

![Success against D by sensing range.](../figures/f14_rq5_range_reliability.png)

![Success against D by observation mode.](../figures/f15_rq5_obs_reliability.png)

## 5. Scaling fits (RQ6)

With `D_min` taking only two values (2, then 1), the fits don't have much to describe. Leave-one-N-out RMSE, lower is better:

| Model | Constant | Linear | Power law | Piecewise |
|-------|---------:|-------:|----------:|----------:|
| RMSE | 0.44 | 0.44 | 0.25 | 0.13 |

![Leave-one-N-out RMSE by model.](../figures/f8_scaling_rmse.svg)

Piecewise wins because its automatic break lands at N = 10, right on the step. The fitted power law has a slightly negative exponent (about -0.2), so if anything it says larger flocks need fewer dogs. Neither result is a growth law. We record C6a as weakly supported and C6b as supported (log-log slope 0 on N = 25 to 400). The honest summary is that this map has no scaling curve to fit.

## 6. Early warning (RQ7)

The setup asks whether the last 200 ticks of flock state can predict a failure 500 ticks ahead, with checks starting at tick 1,000. On the baseline size map that's too late. Successful runs finish in a median of 183 ticks, and only 5 of 2,031 are still going at tick 1,000. The 169 failures are all N = 5 or 10 with one dog, and they run to the 10,000-tick deadline.

![Run end times versus the warning window.](../figures/f12_early_warning_timing.png)

So at every check there's essentially nothing but failures left. The held-out AUROC folds came out empty (C7a inconclusive), and only 14 of 169 failures had a lead time of 500 ticks or more (8.3%, against a 30% bar: C7b rejected). A fair test needs successes and failures running side by side for a while, like FAT or Kubo-wide runs.

---

## Claims scorecard

| Claim | Question | Verdict | Why |
|-------|----------|---------|-----|
| C1a | RQ1 | rejected | Layout never moved `D_min` on the baseline |
| C1b | RQ1 | inconclusive | No `D_min` shift, so the state-vs-(N, D) test couldn't run |
| C2a | RQ2 | rejected | 0 overcrowding cells up to D = 35 |
| C2b | RQ2 | skipped | No overcrowding cell to extend to T = 20,000 |
| C3 | RQ3 | inconclusive | No overcrowding cells to contrast against |
| C4 | RQ4 | supported (partial) | Compact floor shared by Strombom and Kubo; FAT, Kubo-wide and Kubo outlier_rich N = 200 break it |
| C5a | RQ5 | supported | Range 32.5 to 65 lowers `D_min` by 2 (N = 100) and 1 (N = 200) |
| C5b | RQ5 | supported | Further range steps save 0 more dogs |
| C6a | RQ6 | supported (weak) | Piecewise beats power law on held-out N, but there are only two `D_min` levels |
| C6b | RQ6 | supported | `D_min` flat at 1 for N = 25 to 400, slope 0 |
| C7a | RQ7 | inconclusive | Held-out AUROC not computable |
| C7b | RQ7 | rejected | 8.3% of failures have lead time >= 500 ticks (bar: 30%) |

These hold inside this protocol only. They say nothing about other tasks, real farms, or differences smaller than one step on the D grid.

## Metrics worth keeping an eye on

The claim packages are built on success, ticks and path. Going back through the other per-trial columns, these turned out to carry real information:

| Metric | What it told us |
|--------|-----------------|
| `control_efficiency` | The cleanest way to show waste. On the baseline it's exactly 1-dog efficiency / D |
| `mean_i_dir` | Separates the methods (0.09 / 0.15 / 0.6) and tracks FAT failure (r = -0.83) |
| `mean_coverage` | Explains the range result, and drops to 0.27 in failed FAT runs |
| `mean_fragmentation`, `mean_cohesion` | Explain the layout costs, and expose that split starts don't really split |
| `failure_mode` | Shows each method failing in its own way |

Two others were less useful. `mean_polarization` mostly reflects the sheep model (about 0.99 under Kubo, 0.55 under Strombom), so it can't be compared across methods. `mean_coverage` is also misleading under `bearing_only`: it reads 1.00 even though the dogs are plainly lost, so it measures who is in range, not what the dog actually knows.

## Limits

- **One easy task.** Most of this is `drive_to_goal` on a compact start, where one dog already clears the bar. That ceiling is why RQ3, RQ6 and RQ7 came out thin.
- **The D grid tops out at 35.** No overcrowding up to 35 is not the same as no overcrowding.
- **Grid resolution.** We can't see effects smaller than one step on the D list.
- **Soft edges.** Kubo outlier_rich at N = 200 is still a wide interval after 200 seeds.
- **Split layout** behaves like compact, so it isn't a real structure contrast yet.
- **Method time.** Kubo ticks aren't the same physical time as Strombom ticks, so don't compare finish times across methods.
- **Correlations only.** The `I_dir` and coverage links to FAT failure are observational.
- **Simulation.** No claim about real dogs or real sheep.

## What's next

- **Phase 8 (collect-hold-gate)** is the harder task, and the scout is running now. If overcrowding shows up anywhere inside D <= 35, it should be here. That would finally give RQ3 its contrast and test C2a again.
- **Push D past 35** on a few N values, to tell a true ceiling from a collapse we haven't reached yet.
- **Rerun RQ5 and RQ7 where `D_min` > 1.** Wide starts, Kubo outlier_rich or FAT are the obvious candidates. Communication and early warning both need a map where the answer can move.
- **Fix the split generator** so the clusters actually start apart.
- **Tighten Kubo outlier_rich at N = 200**, and give FAT a fairer local-sensing setup before drawing firm conclusions about it.
