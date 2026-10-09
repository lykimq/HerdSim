# Scaling Report

How many dogs does it take to herd a flock reliably, and does that number change when the flock gets bigger, starts more spread out, or is herded by a different set of dog rules? This report collects everything the HerdSim scaling campaign measured to answer that, what it could not answer, and why.

## Contents

- [The short version](#the-short-version)
- [1. HerdSim overview](#1-herdsim-overview)
  - [Why these three methods](#why-these-three-methods)
  - [Method tracks: transfer vs draft](#method-tracks-transfer-vs-draft)
  - [Does this answer the central question?](#does-this-answer-the-central-question)
- [2. Prior draft paper](#2-prior-draft-paper)
  - [Result of the paper](#result-of-the-paper)
  - [If we rerun a draft-style method](#if-we-rerun-a-draft-style-method)
- [3. Research questions](#3-research-questions)
  - [What we want from the program](#what-we-want-from-the-program)
  - [Core questions](#core-questions)
  - [Follow-on questions](#follow-on-questions)
  - [Scope](#scope)
- [4. Shared protocol](#4-shared-protocol)
  - [Core protocol](#core-protocol)
  - [Initial layouts](#initial-layouts)
  - [Frontier, regimes, and failure labels](#frontier-regimes-and-failure-labels)
- [5. Campaign design](#5-campaign-design)
  - [Grades](#grades)
  - [Shared pipeline](#shared-pipeline)
  - [Claim windows and merge](#claim-windows-and-merge)
  - [How each phase uses the pipeline](#how-each-phase-uses-the-pipeline)
  - [Trial counts by run](#trial-counts-by-run)
  - [Trust audit](#trust-audit)
- [6. Methods and results](#6-methods-and-results)
  - [`strombom_multi`](#strombom_multi)
  - [`kubo`](#kubo)
  - [`fat`](#fat)
- [7. Findings synthesis](#7-findings-synthesis)
  - [At a glance](#at-a-glance)
  - [Contrast with the 2025 draft](#contrast-with-the-2025-draft)
  - [Baseline cost and regimes](#baseline-cost-and-regimes)
  - [Upper frontier status](#upper-frontier-status)
  - [Future work: measuring collapse beyond D = 35](#future-work-measuring-collapse-beyond-d--35)
- [8. Answers to research questions](#8-answers-to-research-questions)
- [9. Cross-method transfer](#9-cross-method-transfer)
- [10. Scaling fits](#10-scaling-fits)
- [11. Claims](#11-claims)
- [12. Limits and threats](#12-limits-and-threats)
- [13. Information ladders](#13-information-ladders)
- [14. Outcomes and state metrics](#14-outcomes-and-state-metrics)
- [15. Prediction and early warning](#15-prediction-and-early-warning)
- [16. Commands run](#16-commands-run)

---

## The short version

All planned simulation campaigns are finished: 43,250 trials across Phases 1, 2, 4 and 5, plus the analysis-only Phases 6 and 7. Here is what they tell us.

1. **On the baseline controller, one dog is enough.** With `strombom_multi` and a tight starting clump, a single dog herds anywhere from 25 to 400 sheep into the goal in at least 90% of runs. Only the tiny flocks (5 and 10 sheep) need two.
2. **Extra dogs don't break anything, they just walk more.** Up to 35 dogs, success never drops. Finish time stays at about 183 ticks; total dog path grows with every dog added.
3. **Starting shape changes the cost, not the dog count** (on the baseline). Wide or straggler-heavy starts take far longer, but one dog still gets there.
4. **This only partly carries over to other controllers.** Kubo behaves like the baseline on tight starts but cannot herd wide starts reliably. FAT only works for flocks of 10 or fewer.
5. **The 2025 draft's "big flocks need 20 to 35 dogs" does not show up here.** The two studies use different tasks, so this is a contrast, not a refutation.
6. **The information experiments (Phase 5) did not really test what they were meant to test.** Local sensing works as well as a full view, which is useful. But the bearing-only, sensing-range and communication runs each hit a setup problem (explained in [Information ladders](#13-information-ladders)). We can't yet say whether better information saves dogs.
7. **Early warning (Phase 7) had almost nothing to work with.** Successful runs finish in about 180 ticks, and the warning checks only start at tick 1,000. By then there was no "healthy" run left to compare failures against.

![Five main results at a glance.](../results/summary/figures/schematics/en/summary_at_a_glance.svg)

*Headline results from Phases 1, 2 and 4. Phase 5 and 7 outcomes are in sections 13 and 15.*

---

## 1. HerdSim overview

> When a few shepherds guide a larger flock, how much control do we actually need as the flock gets bigger or more spread out?

Put simply: if the flock grows, or starts more scattered, do you need more dogs?

An earlier 2025 draft paper on sheep scaling asked the same thing. We keep that question, but try to be more careful about it:

- define "how much control" precisely, so it can be measured,
- treat flock *size* and flock *shape at the start* as separate factors,
- ask *why* a pattern appears, not only whether it does,
- check whether the pattern survives a change of herding method.

We don't assume there is one universal scaling law. We start from questions we can actually run in simulation.

**HerdSim** is the platform we use. A few dogs guide a larger flock to a goal, with every setting fixed and repeatable. For this study it is a model system for measuring *control demand*: how much dog effort it takes to succeed reliably. It is not meant to copy a real farm.

Herding is a good test case because the control is *indirect*:

> A small number of external controllers tries to steer a larger group whose members are not commanded one by one.

The platform is built for fair comparison. You pick a method (how sheep move and how dogs decide), put it in a scenario, fix a random seed, and score the run with the same metrics as every other run. That lets you see when herding works, when it fails, and how methods compare when everything else is held equal.

HerdSim does two jobs on one engine:

a. **Simulation + frontend**: an interactive UI (Simulate, Compare, Experiments, NetLogo, Guide).
b. **Scaling**: command-line protocols that run the control-demand experiments in this report.

### Methods

A **method** is a ready-made package: a sheep model plus a dog controller, with defaults taken from the source paper.

Methods currently in the platform:

- `strombom`: Strombom 2014, 50 sheep, 1 shepherd
- `strombom_multi`: Strombom Multi-Dog, 50 sheep, 3 dogs
- `strombom_noise`: Strombom Noise, 50 sheep, noisier motion, 1 shepherd
- `heterogeneous`: Heterogeneous Sheep, 50 sheep, 1 shepherd
- `v_formation`: V-Formation, Strombom sheep, 2 dogs
- `obstacle_aware`: Obstacle-Aware, 50 sheep, 1 shepherd
- `fat`: FAT, Strombom sheep, 2 dogs
- `communication_free`: Communication-Free, Strombom sheep, 3 dogs
- `adaptive`: Adaptive, Strombom sheep, 2 dogs
- `kubo`: Kubo 2022, 40 sheep, 4 dogs
- `flocking_dog`: Flocking Dog 2024, 14 sheep, 1 dog

This study uses three of them: `strombom_multi` (the baseline), `kubo` and `fat`. Controller details and results are in [Methods and results](#6-methods-and-results).

#### Why these three methods

The plan fixes one baseline and two comparison methods so we can ask: "If we change only the dog rules, does the size and structure story stay the same?" That is research question RQ4.

| Method | Role | How the dogs behave |
|--------|------|---------------------|
| `strombom_multi` | Baseline | Dogs gather stragglers (Collect), then push the flock toward the goal (Drive) |
| `kubo` | Required comparison | Continuous "force" rules, no Collect/Drive switch; each dog pushes the sheep farthest from the goal among those it can sense |
| `fat` | Required comparison | Each dog chases the sheep farthest from *itself*; no Collect/Drive switch; dogs don't space themselves apart |

What matters is having genuinely different *kinds* of controller on the **same** task (`drive_to_goal`), rather than three small variations of Collect/Drive. These three are the minimum set needed for transfer claims. `communication_free` is the recommended next addition but sits outside that minimum. The other presets exist in the UI but are not part of the claims here.

If all three methods show the same pattern (say, the same smallest reliable dog count), that pattern is more likely to belong to the task than to one controller. If Kubo or FAT breaks the pattern, we learn how far the result can be generalised. Three methods obviously don't cover every herding idea out there.

#### Method tracks: transfer vs draft

We approach the same broad question ("how much control as size and spread change?") in two ways:

| Track | What changes | Why | Linked RQs |
|-------|--------------|-----|------------|
| Same-task transfer (`strombom_multi`, `kubo`, `fat`; next: `communication_free`) | Only the dog/sheep rules; task and grids stay fixed | See which patterns survive a controller change (RQ4) | RQ1 to RQ7 |
| Draft-style method in HerdSim (planned) | Task, arena, starts, and usually the controller family (collect, hold, gate) | The 2025 draft used a collect-hold-gate task; porting it lets us ask the same RQs there | Same central question; not a substitute for RQ4 |

The draft track is described under [Prior draft paper](#2-prior-draft-paper). It is not a fourth transfer method alongside Kubo and FAT.

We use `drive_to_goal` as the main task because it is the frozen HerdSim protocol for comparing methods fairly. That choice doesn't mean the draft's task is wrong. When we later say the compact baseline looks "easy" (one dog is often enough), that is something we measured, not a reason we picked the task.

#### Does this answer the central question?

Here, "how much control" means the useful range of dog counts under fixed rules:

- **`D_min`**: the smallest dog count that succeeds in at least 90% of runs,
- what happens beyond that: do extra dogs help, waste effort walking, or make things worse (overcrowding)?
- all under a fixed time limit.

Which RQ covers what: size is RQ2 (with curve fits in RQ6); starting shape is RQ1; "why" is RQ3, which needs overcrowding cases to compare; method transfer is RQ4; information and early warning are RQ5 and RQ7.

The program answers the question by *bounding* it inside this protocol: where dog need stays low, where cost rises without needing more dogs, and where transfer to other controllers fails. The results are in [Findings synthesis](#7-findings-synthesis), with one answer per question in [Answers to research questions](#8-answers-to-research-questions).

This study does **not** claim a universal farm law, that the draft's rising dog counts are wrong on the draft's own task, or that every method needs only one dog up to D = 35.

---

## 2. Prior draft paper

The 2025 draft, "Collective Nudging that Scales", asked a simple question: how many dogs do I need to herd sheep?

It was run in **NetLogo**, not HerdSim, and differs from our main study in several important ways:

- **Task**: gather the flock, hold it for 800 ticks, then push it out through a gate (not our open-field `drive_to_goal`).
- **Success**: every sheep through the gate by 10,000 ticks.
- **Arena**: patch grid of 101 x 71, with a central hold zone and a gate on the right wall.
- **Starts**: sheep scattered at random; dogs start in a grid at the top left.
- **Controller**: a single NetLogo collect / drive / patrol family.
- **Same reliability idea**: succeed in at least 90% of runs; `D_min` is the smallest dog count that reaches that.
- **Grids**: up to 35 dogs and up to 400 sheep (details below).

Setup details:

- NetLogo 7.0.3 on a patch grid.
- Containment radius: `rc = clamp (2.5 * sqrt (N), 23, 27)`.
- D grid: `{1, 2, 3, 4, 6, 10, 15, 20, 25, 35}`.
- N grid: `{5, 10, 25, 50, 100, 150, 200, 250, 300, 350, 400}`.
- Sampling: 100 runs per cell (11,000 in total).
- Seed: the master seed is not stated in the note.
- `D_overcrowd` / `D_max`: the draft's definitions differ slightly from ours.
- Structure: emergent spread summarised by `S_bar`.
- Metrics: success, ticks, phase, spread, path, lost sheep.

![2025 draft task phases.](../results/summary/figures/schematics/en/draft_task_phases.svg)

*Draft task: collect, hold, then exit through a gate (NetLogo patch arena).*

![2025 draft experiment design.](../results/summary/figures/schematics/en/draft_experiment_design.svg)

*Draft design: containment zone, gate, and run budgets.*

### Result of the paper

Small flocks usually needed one dog. Large flocks needed many more: tens of dogs at N around 200 to 400.

At a success rate (SR) of at least 90%, draft Table A3 reports:

| N   | D_min | D_max     | Maximum SR |
|-----|-------|-----------|------------|
| 5   | 1     | not reached | 100%     |
| 10  | 1     | 15        | 100%       |
| 25  | 1     | 25        | 100%       |
| 50  | 1     | 25        | 100%       |
| 100 | 1     | not reached | 100%     |
| 150 | 3     | not reached | 99%      |
| 200 | 20    | 35        | 94%        |
| 250 | 25    | not reached | 93%      |
| 300 | 20    | not reached | 93%      |
| 350 | 35    | not reached | 91%      |
| 400 | 35    | not reached | 91%      |

"Not reached" means no upper failure point was found up to D = 35.

The draft also found that more spread went with lower success (Spearman `rho = -0.701` for mean spread `S_bar` vs SR, and `rho = -0.828` for `S_bar * N` vs SR, over 110 condition aggregates).

![2025 draft main results sketch.](../results/summary/figures/schematics/en/draft_main_results.svg)

*Draft Table A3 pattern: D_min stays low for small N, then jumps for large flocks.*

### If we rerun a draft-style method

We did **not** rerun the draft in this campaign. The plan is to port the collect / hold / gate task (and its controller family) into **HerdSim** rather than rerun NetLogo.

The point would be to ask the same research questions on that harder task. That is a different exercise from adding another dog rule to the current task.

| What the HerdSim draft rerun would ask | Planned RQ |
|----------------------------------------|------------|
| As flock size grows on collect-hold-gate, how many dogs are needed, and do extra dogs help, plateau, or hurt? | RQ2 (size and regimes); RQ6 once frontiers exist |
| At the same flock size, does starting shape or hold-phase state change how many dogs are needed? | RQ1 (structure), using draft-style state such as `S_bar` where useful |
| If too many dogs start to hurt, what separates good cells from overcrowded ones? | RQ3 (mechanism), only if those contrasts appear |
| On a frozen draft-style task, which patterns hold when only the controller changes? | RQ4 (transfer), once that task is frozen |
| On that task, can better sensing or communication reduce the dog count? | RQ5 |
| On that task, can recent flock state warn of failure better than N and D alone? | RQ7 |

---

## 3. Research questions

The program asks how many dogs are needed for reliable herding as the flock gets bigger or more spread out, why that demand appears, and whether the answer depends on the herding method.

For each core question below we give what we want to know, how we study it, and what kinds of answer would count. We did not pick a preferred outcome in advance.

### What we want from the program

After the core runs, we should be able to say something concrete about:

- how dog need changes as the group grows,
- whether starting shape matters beyond size,
- which processes seem to drive the pattern,
- what is shared across methods and what is method-specific.

A simple predictive rule would be useful. Strong method dependence would also be useful, because it tells us how far results can be generalised. Compared with a single-method scaling study, the program defines control demand in a reusable way, separates size from structure, tests mechanisms instead of stopping at correlation, and checks which features survive a method change.

### Core questions

#### Size and operating regimes (RQ2, with curve fits in RQ6)

**Question.** As flock size grows, how does the useful dog range change? That means both the minimum needed for reliable herding, and whether adding more dogs still helps, mostly wastes walking, or starts to hurt.

RQ6 is the follow-up modelling step: once we have `D_min` for each N, which simple curve best predicts a flock size it hasn't seen? Is one power law enough?

**Approach.** Freeze the protocol. Vary flock size `N` and keep everything else fixed. For each `N`, find the smallest dog count `D` that hits the reliability target, then check whether larger `D` helps, plateaus, or hurts. Fit curves only after those frontiers exist.

**Possible results.** Dog need could grow smoothly, grow in steps, stay flat, or look messy. We also label operating regimes: too few dogs, efficient, wasteful (succeeds, but with a lot of walking), or overcrowded (success falls at high D).

#### Structure (RQ1)

**Question.** At the same flock size, does starting shape (spread, split, outliers) change how many dogs are needed?

As a claim: does `D_min` change across initial layouts at fixed N?

**Approach.** Hold `N` fixed and change only the starting layout. Measure a few shape properties and see how much difficulty is left that size alone can't explain.

**Possible results.** Size may be nearly enough on its own; a few shape measures may explain the rest; or different properties may matter at different sizes.

#### Mechanism (RQ3)

**Question.** Why does the pattern appear? For example: dogs getting in each other's way, the flock splitting, or limited coverage.

As a claim: which pre-chosen signatures separate efficient cells from overcrowded cells at the same N?

**Approach.** Candidates include spatial demand, fragmentation, dog interference, redundant control and local instability. We log quantities tied to each and compare them. Correlation alone is not treated as proof of cause.

**Possible results.** One main mechanism, several mechanisms in different regimes, or a pattern that doesn't reduce to one clean story.

#### Generality across methods (RQ4)

**Question.** If we switch herding method, which parts of the pattern stay the same?

**Approach.** Rerun the core size and structure maps with `strombom_multi`, `kubo` and `fat`. Compare frontiers and regime labels, not just raw success rates, and mark what is shared versus method-specific.

**Possible results.** Fully method-specific; same shape at a different scale; or same shape with different thresholds. Strong method dependence limits how much we can say about "scaling" separately from the controller.

### Follow-on questions

These come after the core four and should not change the original scientific question.

| Topic | ID | Question |
|-------|----|----------|
| Information vs shepherds | RQ5 | Can better sensing or communication reduce the dog count at the same reliability? |
| Early warning | RQ7 | Can recent flock state warn of failure better than knowing only N and D? |
| Time as a resource | protocol `T0`/`T1` | Does a tighter or looser deadline change how many dogs are needed? |
| Collapse beyond D = 35 | RQ2 upper band (extension) | With more than 35 dogs, does success eventually fall, or does only wasted walking keep rising? See [Future work](#future-work-measuring-collapse-beyond-d--35). |
| Other systems | later | Do similar patterns appear outside sheep-herding simulations? |

RQ6 (curve fitting) belongs with the size question: fit only once solid frontiers exist. The regimes (too few / efficient / wasteful / overcrowded) also belong with size rather than being a separate RQ.

### Scope

**In scope for the core program**

- flock size and starting structure
- how much external control is needed for reliable success
- scaling relationships and mechanisms
- whether results transfer across control methods
- a reproducible protocol

**Not primary goals**

- finding the single "best" herding algorithm
- copying every detail of real livestock
- optimising one controller design
- claiming results for every collective system at once
- shipping a real-time failure-prediction product

Those can wait until the core scaling questions are clearer. We only claim what the evidence supports.

---

## 4. Shared protocol

| Term | Meaning |
|------|---------|
| `N` | Number of sheep |
| `D` | Number of dogs |
| `R` | Success rate: fraction of repeated runs that finish in time |
| `theta` | Reliability bar (0.90 here: succeed in at least 90% of runs) |
| `D_min` | Smallest tested D with `R >= theta` |
| Compact start | Sheep begin in a tight clump |

### Core protocol

- `task`: `drive_to_goal`: every sheep must be inside the goal disk before the deadline.
- `world_width`, `world_height`: (500, 500): a square field big enough for wide and outlier-rich starts.
- Flock centre: (250, 250): centre of the field.
- `goal_center`: (370, 250): on the midline, 120 units right of the flock.
- `drive_length`: 120: fixed centre-to-centre distance.
- `goal_radius_at_n50`: 15: goal size at N = 50.
- Goal radius: `15 * sqrt (N/50)`: keeps goal area per sheep constant.
- `initial_spread`: 30: base scale for all layout generators.
- `measurement_radius`: 5: connectivity radius used for fragmentation.
- `reliability_theta`: 0.90: main reliability threshold.
- `reliability_sensitivity`: 0.5, 0.7: also reported, but not used for `D_min`.
- `baseline_method`: `strombom_multi`: baseline collect-and-drive controller.
- `transfer_method`: baseline, `kubo`, `fat`, `communication_free`: full planned transfer list.
- `required_transfer_methods`: baseline, `kubo`, `fat`: minimum set for transfer claims.
- `flock_size` grid: `{5, 10, 25, 50, 75, 100, 150, 200, 300, 400}`.
- `shepherd_counts` grid: `{1, 2, 3, 4, 6, 10, 15, 20, 25, 35}`.
- `structure_flock_sizes`: `{50, 100, 200}`.
- `rq5_flock_sizes`: `{100, 200}`: flock sizes for the information experiments.
- `X0_families`: compact, wide, split, outlier_rich: the starting-layout factor.
- `time_limit_t0`: 10,000: main deadline, roughly 80 straight 120-unit crossings at speed 1.
- `time_limit_t1`: 20,000: longer deadline, only for overcrowded cells.
- `scout_seeds`: 30: depth for the broad first map.
- `master_seeds`: 2026: base of a shared, deterministic seed list.
- `bootstrap_resamples`: 1,000: seed resamples for frontier uncertainty.
- `predictor_window_ticks`: 100: initial-state feature window, shorter than a straight drive.
- `wasteful_effort_tolerance`: 0.2: default excess-path threshold.
- `wasteful_effort_sensitivity`: 0.1, 0.3: also reported.

#### Why the setup looks like this

These choices were fixed in the plan before any results came in.

##### Field

A 500 by 500 square leaves room to spare for wide and outlier-rich starts. A much smaller field (150) can't hold them, a 400 field is tight on the wide start, and a 1000 field mostly adds empty space.

The goal sits on the horizontal midline so the top and bottom margins are equal.

![Field and arena overview.](../results/summary/figures/schematics/en/arena_overview.svg)

*500 by 500 field, flock centre, goal on the midline, and room for wide starts.*

The flock has to travel 120 units from its centre to the goal. That's far enough that a tight start isn't already "in" the goal, but not so far that the goal ends up against the far wall.

![Compact drive geometry.](../results/summary/figures/schematics/en/arena_compact.svg)

*A 120-unit drive from flock centre to goal along the midline.*

##### Radius

At N = 50 the goal radius is 15: large enough that sheep aren't jammed into a tiny disk, small enough that the task isn't trivial. The radius grows with `sqrt(N)` so the goal *area per sheep* stays roughly the same; a fixed radius would squeeze large flocks. We deliberately do **not** reuse the Strombom Collect radius as the goal size, since that rule belongs to one controller.

![Goal radius scaling.](../results/summary/figures/schematics/en/goal_radius.svg)

*Goal radius `15 * sqrt(N/50)` keeps goal area per sheep roughly constant.*

##### Flock-size and dog-count grids

**Flock sizes (N):** N = 5 is the smallest size where the collective measures still make sense. The grid is denser around N = 100, includes 300 and 400 for large flocks, and skips 250 and 350 because every extra N needs a full sweep over dog counts.

**Dog counts (D):** fine steps at low D, where the minimum usually sits, then bigger jumps to see whether many more dogs help or hurt. The list stops at 35 because the question is about a *few* shepherds. That is a ceiling for this study, not a physical limit, and it doesn't prove overcrowding can't happen above 35 ([Future work](#future-work-measuring-collapse-beyond-d--35)).

![Frozen N and D grids.](../results/summary/figures/schematics/en/design_nd_grids.svg)

*N is denser near 100; D goes in single steps at low counts, then larger steps up to 35.*

![Reliability threshold theta.](../results/summary/figures/schematics/en/design_theta.svg)

*Main bar: R >= 0.90. Thresholds of 0.50 and 0.70 are reported but don't define D_min.*

##### Methods and claim sizes

Method choice and tracks: [Why these three methods](#why-these-three-methods) and [Method tracks: transfer vs draft](#method-tracks-transfer-vs-draft).

Structure experiments use `structure_flock_sizes` and all four starting layouts. These sizes are big enough for split clusters and outliers to actually look like structure.

Below N = 12 the split layout only has two clusters, and tiny compact flocks are already covered by Phase 1.

N = 300 and N = 400 could be added after the three-size structure map, mainly if every layout stayed at the `D_min` floor.

Information experiments use `rq5_flock_sizes`. N = 50 is left out because a `D_min` already at 1 can't go any lower.

### Initial layouts

Flock size stays fixed; only the starting positions change:

| Layout | What it looks like | How it's generated |
|--------|--------------------|--------------------|
| `compact` | Tight clump | Narrow Gaussian (sigma 9) |
| `wide` | Very spread out | Wide Gaussian (sigma 60) |
| `split` | Two or three separate clumps | Gaps of at least 10 units |
| `outlier_rich` | Main flock plus far stragglers | About 80% core, 20% far outliers |

Sanity checks: compact should be tighter than wide, split more broken up than compact, and outlier_rich should have more outliers than compact. Points that land outside the field or inside the goal are redrawn rather than pinned to the wall.

A connectivity radius of 5 links close neighbours in a compact flock but doesn't bridge the gaps in a split one.

![Four initial layouts.](../results/summary/figures/schematics/en/four_layouts.svg)

*Compact, wide, split and outlier_rich at the same N.*

### Frontier, regimes, and failure labels

**Control demand** means: how many dogs do you need for herding to succeed often enough? We measure it mainly through the useful dog range around `D_min`, and whether too many dogs start to hurt.

`D_min` isn't a natural property of sheep. It depends on the task, time limit, sensing, success rule and the other frozen settings.

We only test the dog counts on the frozen list, not every integer.

Success rate `R` is estimated over a fixed set of random seeds for a given method, protocol, N, D, time limit, starting layout and information setting.

| Label | Meaning |
|-------|---------|
| `D_min` | Smallest tested dog count with `R >= 0.90` |
| `D_overcrowd` | After a reliable band, the first point where two consecutive tested D fall below 0.90 |
| `D_max` | Largest reliable D before overcrowding; if there's no overcrowding, just the top of the tested list (a ceiling) |
| `B*` | Among reliable choices, the one with the shortest median dog path (ties: fewer dogs, then faster finish) |
| Hard failure | No tested D reaches 0.90 |
| Under-resourced | Too few dogs; `R` below 0.90 |
| Efficient | Reliable, and path not much above `B*` |
| Wasteful | Reliable, but dogs walk a lot more than at `B*` (default 20% more; 10% and 30% also reported) |
| Overcrowding | After a reliable band, success falls again at high D |

**Waste vs overcrowding:**

- **Waste:** runs still succeed, but the extra dogs mostly add walking.
- **Overcrowding:** after a reliable band, success drops below 90% for two dog counts in a row.

If there's no overcrowding, `D_max = 35` only means "still fine at the largest D we tried", not "collapse starts at 35". More on this in [Upper frontier status](#upper-frontier-status).

![Waste versus overcrowding.](../results/summary/figures/schematics/en/overcrowd_example.svg)

*Waste: R stays at or above theta while path grows. Overcrowding: after a reliable band, R drops below theta for two consecutive tested D.*

![Frontier quantities.](../results/summary/figures/schematics/en/design_frontier.svg)

*`D_min`, the reliable band, `D_overcrowd`, `D_max`, and `B*` (the reliable choice with the least walking).*

![Regimes along D at fixed N.](../results/summary/figures/schematics/en/regimes.svg)

*Under-resourced, efficient, wasteful and overcrowded regimes along the tested D grid.*

Failure labels:

- Stacking: dogs pile up on one spot.
- Split: the flock stays in pieces.
- Scatter: cohesion distances stay high.
- Oscillation: the flock centre flips back and forth with little progress.
- Stuck: the flock centre barely moves toward the goal.
- Timeout: still unfinished at T0.

![Failure-label families.](../results/summary/figures/schematics/en/design_failures.svg)

*How failed trials are labelled from flock and dog state (stacking, split, scatter, oscillation, stuck).*

![Timeout as a failure label.](../results/summary/figures/schematics/en/design_timeout.svg)

*Timeout: the run is still unfinished at T0. Other labels can also apply to a run that fails earlier.*

---

## 5. Campaign design

We need accurate success rates near the edges that matter: where `D_min` sits, and where overcrowding might start. Running *every* cell at 100 seeds would waste most of the budget, because cells that always succeed or always fail tell us little at that depth.

So we work in stages: cheap seeds everywhere first (scout), find the cells that matter, then spend the expensive seeds only there (claim). Size, structure, transfer and information experiments all follow this pattern.

![Phase roadmap.](../results/summary/figures/schematics/en/phase_roadmap.svg)

*Which phases produce claim-grade maps and which are analysis-only or follow-on work.*

![Staged scout and claim pipeline.](../results/summary/figures/schematics/en/pipeline.svg)

*Smoke, scout, claim plan, claim reseed, analyse, and conditional T1.*

### Grades

| Grade | Role | Typical seeds | Usable for claims? |
|-------|------|---------------|--------------------|
| SMOKE | Pipeline check (paths, resume, metrics) | tiny grid | No |
| SCOUT | Broad map; choose claim windows | 30 | No (planning and diagnostics only) |
| CLAIM | Precision on selected cells | 100 | Yes |

A SCOUT result is never promoted to a claim verdict.

### Shared pipeline

Every simulation campaign goes through the same steps:

1. Pilot (SMOKE): check host, paths, metrics and resume on a small grid.
2. Scout (SCOUT): run the full (or factor) grid at 30 seeds to build a reliability map.
3. Claim plan: no new simulations; list the frontier cells to reseed.
4. Claim reseed (CLAIM): run those cells at 100 seeds and merge them with the scout.
5. Analyse: build packages and figures from the merge.
6. T1 (only if needed): claim-depth runs at `T = 20,000` on overcrowded cells.

If the scout map is broken, the grid needs changing, or the bootstrap interval is too wide, we stop after the scout, fix the protocol, then carry on.

![One cell and seed depth.](../results/summary/figures/schematics/en/one_cell_seeds.svg)

*A single (N, D) cell at scout depth versus claim depth.*

![Scout reliability map idea.](../results/summary/figures/schematics/en/scout_grid.svg)

*The broad 30-seed map over the N by D grid shows roughly where reliability lies before precision reseeding.*

![Claim window selection.](../results/summary/figures/schematics/en/claim_window.svg)

*Reseed D_min and its neighbours; add overcrowding onset cells only if the scout shows them.*

### Claim windows and merge

After the scout, we only reseed the cells that matter:

- Around the scout's `D_min`: that D, plus the previous and next dog counts on the list.
- If overcrowding seems to start (two dog counts in a row below 0.90): those two D values and the last reliable one.
- If nothing reaches 0.90: the two largest D values tested.

For a reseeded cell, the analysis uses only its claim rows. Every other cell keeps its scout rows. Scout and claim rows are never mixed within one cell. If the bootstrap interval on `D_min` is wider than one dog-count step, that window is raised to 200 seeds before a structure claim (next subsection).

### Bootstrap on `D_min` (analysis, then maybe more seeds)

The bootstrap is not a campaign phase and doesn't involve 1,000 new simulations. Once scout and claim rows are locked, we resample those existing seeds with replacement 1,000 times, recompute `D_min` each time, and take the 2.5% and 97.5% percentiles as the interval. A resample that never clears theta is treated as "above the tested grid". An interval of width zero means every resample gave the same `D_min`.

What happens next is a separate rule:

1. Run the bootstrap on the locked claim (or scout) seeds.
2. If the interval spans more than one step on the D grid, raise that claim window to 200 real simulation seeds.
3. Bootstrap again on the larger seed set.
4. Report the point `D_min` with the new interval. More seeds reduce noise, but they can't turn a gradual edge into a sharp one.

Worked example (Phase 4, Kubo): `outlier_rich` at `N = 200` had a wide interval, so those D cells were raised to 200 seeds. With the deeper set, the point estimate is still `D_min = 20` and the interval is still `[2, 20]`. Details under [`kubo`](#kubo).

![Bootstrap on D_min, then raise to 200 seeds when the interval is wide.](../results/summary/figures/schematics/en/design_bootstrap.svg)

*Top: resample locked seeds (analysis only). Bottom: a wide interval triggers new simulations at 200 seeds, then a second bootstrap. The interval can stay wide.*

### How each phase uses the pipeline

| Phase | RQ | What's specific | Scout asks | Claim spends seeds on |
|-------|----|-----------------|------------|------------------------|
| 1 | RQ2 | Baseline size map (`strombom_multi`, compact) | Where does `R(N, D)` sit on the frozen grids? | Frontiers and hard-failure cells |
| 2 | RQ1 | Four layouts at `N` in `{50, 100, 200}` | How does starting layout move `D_min` and cost? | Structure windows at those three sizes |
| 3 | RQ3 | Analysis only | (none) | Needs matched efficient vs overcrowded cells from Phase 1 or 2 |
| 4 | RQ4 | Repeat size and structure for `kubo` and `fat` | Same maps per transfer method | Same window rules per method |
| 5 | RQ5 | Three separate ladders (observation, range, communication) | Does a ladder step lower `D_min`? | Windows on each ladder at `N` in `{100, 200}` |
| 6 | RQ6 | Analysis only | (none) | Needs claim-grade frontier maps |
| 7 | RQ7 | Analysis only | (none) | Needs claim-grade timeseries |

Notes per phase:

- Phase 1: full frozen `N` x `D` grids. T1 skipped because no overcrowded cells appeared.
- Phase 2: structure scout and claim only; no new size grid.
- Phase 3: skipped, because Phase 1 produced no overcrowded cells to compare.
- Phase 4: size then structure, once per transfer method (`kubo`, then `fat`).
- Phase 5: observation ladder first, then range, then communication, all on the low dog band `{1, 2, 3, 4, 6, 10}` ([Information ladders](#13-information-ladders)).
- Phases 6 and 7: no new simulations. They reuse the Phase 1 claim merge (and, for Phase 7, its timeseries).

### Trial counts by run

Counts are completed simulation trials taken from each protocol folder (`status.json`, checked against `trials.csv`). Claim rows are the reseed trials only, not the merged table. Analysis-only phases have no trials of their own.

| Phase | Run | Grade | Method / focus | Trials | Status |
|-------|-----|-------|----------------|-------:|--------|
| 1 | Pilot | SMOKE | `strombom_multi` | 150 | DONE |
| 1 | Scout | SCOUT | size map, compact | 3,000 | DONE |
| 1 | Claim reseed | CLAIM | size frontiers | 2,200 | DONE |
| 1 | T1 | CLAIM | overcrowding at `T = 20,000` | 0 | SKIPPED |
| 2 | Pilot (state) | SMOKE | structure smoke | 600 | DONE |
| 2 | Scout | SCOUT | 4 layouts | 3,600 | DONE |
| 2 | Claim reseed | CLAIM | structure windows | 2,400 | DONE |
| 3 | Mechanism | CLAIM | Package C (analysis) | n/a | SKIPPED |
| 4 | Kubo size scout | SCOUT | `kubo` compact | 3,000 | DONE |
| 4 | Kubo size claim | CLAIM | `kubo` size windows | 2,100 | DONE |
| 4 | Kubo structure scout | SCOUT | `kubo` 4 layouts | 3,600 | DONE |
| 4 | Kubo structure claim | CLAIM | `kubo` structure windows | 4,000 | DONE |
| 4 | FAT size scout | SCOUT | `fat` compact | 3,000 | DONE |
| 4 | FAT size claim | CLAIM | `fat` size windows | 2,000 | DONE |
| 4 | FAT structure scout | SCOUT | `fat` 4 layouts | 3,600 | DONE |
| 4 | FAT structure claim | CLAIM | `fat` structure windows | 2,400 | DONE |
| 5 | Observation scout (`factor_sweep`) | SCOUT | observation ladder | 1,080 | DONE |
| 5 | Observation claim | CLAIM | observation windows (12 cells) | 1,200 | DONE |
| 5 | Range scout | SCOUT | sensing-range ladder | 1,440 | DONE |
| 5 | Range claim | CLAIM | range windows (16 cells) | 1,600 | DONE |
| 5 | Communication scout | SCOUT | communication ladder | 1,080 | DONE |
| 5 | Communication claim | CLAIM | communication windows (12 cells) | 1,200 | DONE |
| 6 | Scaling fits | CLAIM | Package F (analysis) | n/a | DONE |
| 7 | Early warning | CLAIM | Package G (analysis) | n/a | DONE |
| | **Total simulations** | | | **43,250** | |

The claim merges used for analysis hold 37,070 rows. That's fewer than the total because a reseeded cell drops its scout rows from the merge.

Phase 5 wall-clock time, from each `status.json`: the observation scout and claim each took about 21 hours, but both include an overnight pause. The range and communication runs were continuous and took between 22 and 79 minutes each.

### Trust audit

On 2026-10-09 we cross-checked the run records before writing this report (full notes in [`TRUST_AUDIT.md`](../results/TRUST_AUDIT.md)):

- For every pilot, scout and claim folder in Phases 1, 2, 4 and 5, the completed count in `status.json`, the rows in `trials.csv` and the `ok` entries in `manifest.jsonl` agree.
- Every audited provenance file carries the same protocol hash (`54dfb46837e3971a`), so all runs used the same frozen settings.
- `make -C scaling scaling-test` passes (19 tests).
- The Phase 5 observation claim was paused mid-run, which left 128 manifest entries with no matching row in `trials.csv`. Those orphan keys were removed and the missing trials rerun. The final claim has 1,200 trials and a merge of 1,920 rows (12 cells at 100 seeds, 24 at 30). The runner now writes `trials.csv` after each finished cell so this can't happen again.
- One known quirk: an older status field for the Phase 4 Kubo structure claim says 600 planned trials, while 4,000 were completed (the extra comes from the 200-seed raise). This is noted in the run ledger.

The full Phase 1, 2 and 4 grids were not rerun for the audit; spot counts and hashes matched the existing claim files.

---

## 6. Methods and results

The shared rules (field, grids, 90% bar, scout/claim staging) are defined once in [Shared protocol](#4-shared-protocol) and [Campaign design](#5-campaign-design). This section goes through each controller and then its results. Each figure has a short **What this shows** note underneath.

"Farthest" means something different for each controller:

- **Strombom Collect:** the sheep farthest from the *flock centre*
- **Kubo:** the sheep farthest from the *goal* (among those the dog can sense)
- **FAT:** the sheep farthest from the *dog itself*

### `strombom_multi`

Dogs first gather stragglers (Collect), then push the whole flock toward the goal (Drive). They switch based on a radius that grows with flock size (`r_a * N^(2/3)`). That Collect radius is wider than the goal disk, so a Strombom failure shouldn't be read as sheep failing to pack into the goal.

![strombom_multi collect and drive.](../results/summary/figures/schematics/en/alg_strombom_multi.svg)

*Multi-dog Collect assigns outliers to dogs; Drive places dogs on an arc behind the flock, facing the goal.*

**Published inspiration**

Strombom et al. (2014) describe a single shepherd that alternates between two actions. In Collect, it moves behind the sheep farthest from the flock centre and pushes that outlier inward. In Drive, it moves behind the flock centre (relative to the goal) and pushes the whole group forward.

The switch uses:

```
f(N) = r_a * N^(2/3)
```

If any sheep is farther than `f(N)` from the flock's centre of mass, the flock counts as spread out and the shepherd collects. Otherwise it drives. The paper also provides the sheep rules (attraction, repulsion, inertia, grazing, noise) and the shepherd stop rule that HerdSim's Strombom sheep are based on.

Ref: paper

**HerdSim implementation**

HerdSim keeps sheep dynamics separate from the dog controller.

The named `strombom` preset combines:

- `sheep_model=strombom`;
- `dog_controller=collect_drive`;
- one shepherd by default.

The scaling study did not use that preset. It used `strombom_multi`, which pairs the same Strombom sheep with `dog_controller=collect_drive_multi`.

**Sheep**

When every active dog is farther away than `r_s`, a sheep grazes: it mostly stays still and takes a random step with probability `graze_move_prob`. When a dog comes within `r_s`, the sheep combines its previous heading, attraction to nearby sheep, short-range repulsion from other sheep, repulsion from dogs, and random noise, then moves by `sheep_speed`.

Defaults in the method bundle include:

- `r_a = 2`: sheep interaction length, used in packing and the Collect threshold.
- `r_s = 65`: distance at which sheep react to a shepherd; also the base sensing range.
- `sheep_speed = 1.0`: sheep displacement per tick.
- `shepherd_speed = 1.5`: shepherd displacement per tick.
- `noise_strength = 0.3`: random angular jitter added when a sheep updates its heading. Higher values make paths wobble more; 0.3 is the Strombom-style default.
- `inertia = 0.5`: weight on the sheep's previous heading when forming the new direction. At 0.5, half of each update keeps the old heading, which smooths turns.
- Collect threshold: `r_a * N^(2/3)`: the radius that switches between Collect and Drive.

The coverage radius is `sensing_range` when an information setting provides one, and the method's `r_s` otherwise. It is not the sheep-to-sheep repulsion distance.

**Multi-dog controller**

With the global observation used in Phases 1, 2 and 4, every active dog sees the whole flock and computes the same centre and threshold.

In Collect:

- sheep beyond `f(N)` are sorted by distance from the centre;
- dog `i` is assigned outlier `i mod k`, where `k` is the number of outliers;
- its target is `r_a` behind that sheep, relative to the centre;
- a sideways offset of `2 * r_a` per slot spreads out dogs heading for the same outlier.

In Drive:

- the target is `r_a * sqrt(N)` behind the centre, relative to the goal;
- dogs are spaced at equal angles on a circle of radius `4 * r_a` around that point.

A dog stops when it gets closer than `shepherd_stop_multiple * r_a` to any sheep it can see. The default `shepherd_stop_multiple = 3` gives a stop distance of `3 * r_a = 6`. Dog motion includes the Strombom angular noise.

The outlier assignment, the sideways Collect spacing (4 units per slot) and the Drive circle (radius 8) are HerdSim additions. They're not part of the 2014 single-shepherd algorithm, and we don't claim they reproduce any other published multi-shepherd controller.

`strombom_multi` is the baseline. It was run on the Phase 1 size map (compact) and the Phase 2 structure map, both with global observation. The experiment overrides the preset dog count as it sweeps `D` but keeps the controller equations and defaults listed above.

#### Results

**Compact size map**

At the 90% reliability threshold:

- `D_min = 2` for `N = 5` and `N = 10`;
- `D_min = 1` for every tested `N` from 25 to 400;
- no overcrowding anywhere; `D_max = 35` is just the top of the grid ([Upper frontier status](#upper-frontier-status)).

![`strombom_multi` compact reliability heatmap.](../results/phase1/claim/packages/a/figures/reliability_heatmap.png)

*Success rate R(N, D) for `strombom_multi`, compact starts only.*

What this shows: almost the entire N by D surface sits at or near R = 1.00. The only weak spot is N = 5 and N = 10 with one dog (R about 0.07 and 0.24). From D = 2 upward, every size clears the bar. So the size story here is a floor, not a rising curve.

![`strombom_multi` frontier D_min(N).](../results/phase1/claim/packages/a/figures/frontier_dmin.png)

*`D_min` (and the ceiling `D_max`) on the compact size map. No overcrowding curve appears.*

What this shows: `D_min` drops from 2 to 1 at N = 25 and stays there up to N = 400. `D_max` sits at the top of the grid (35) for every N because success never falls. This is a lower frontier plus a ceiling label, not a measured upper collapse.

![`strombom_multi` cost against D.](../results/phase1/claim/packages/a/figures/cost_vs_d.png)

*Finish time stays roughly flat once runs succeed; total path grows with D.*

What this shows: median finish time is about 183 ticks (90th percentile about 198) and barely changes as D grows. Total dog path rises with D; for N >= 25 the median path per dog is about 148. Extra dogs buy almost no time and mostly add walking, which is the waste pattern.

![`strombom_multi` size-map outcomes.](../results/phase1/claim/packages/a/figures/failure_modes.png)

*How trials end in the compact size claim merge (4,540 rows).*

What this shows: overall success is about 0.963 (169 failures). All failures are in the two under-resourced cells, N = 5 and N = 10 with one dog: 111 labelled oscillation and 58 labelled stuck. Every other cell succeeds.

![`strombom_multi` regime counts.](../results/phase1/claim/packages/a/figures/regime_counts.png)

*Regime labels on the 100 size-by-dog cells.*

What this shows: 88 wasteful, 10 efficient, 2 under-resourced (N = 5 and N = 10 at D = 1), 0 overcrowded. Most of the reliable band is already past `B*`: more dogs keep R high but add walking.

**Starting structure**

At `N = 50, 100, 200`, all four layouts have `D_min = 1`, with a bootstrap interval of width zero. Starting shape changed the cost, not the minimum dog count:

- wide starts took about 11 to 20 times longer than compact and needed about 19 to 36 times the dog path, with one dog;
- `outlier_rich` at `N = 200` took a median 1,228 ticks and a path of 1,647 with one dog;
- on wide starts, the least-walking reliable choice `B*` was 2 dogs at all three sizes.

![`strombom_multi` layout cost at D = 1.](../results/phase2/claim/packages/b/figures/layout_cost_d1.png)

*Median total path by layout with one dog. Wide and large outlier_rich starts are the expensive ones.*

What this shows: compact and split are almost identical. Wide is the expensive start (path about 2,900 to 5,200). `outlier_rich` grows quickly with N (path about 209 at N = 50, about 1,647 at N = 200). On the baseline, structure affects cost, not `D_min`.

![`strombom_multi` R vs D by layout at N = 50, 100, 200.](../results/phase2/claim/packages/b/figures/layout_reliability_by_n.png)

*Success rate R(D) for each layout at the three structure sizes. Curves are nudged vertically so they don't hide each other; true values are R = 1.00 where marked.*

What this shows: at N = 50, 100 and 200, all four layouts reach R = 1.00 with one dog and stay above the bar up to D = 35. Without the vertical nudge the four curves would sit on top of each other. Layout doesn't open any reliability gap on the baseline; it just makes runs slower and longer.

![Wide starts: path at D = 1 versus D = 2.](../results/summary/figures/f10_wide_bstar_path.png)

*On wide starts `B*` = 2: a second dog shortens the median path while staying reliable.*

What this shows: for wide starts at N = 50, 100 and 200, median total path falls from about 2,925 to 2,337, from 4,319 to 3,003, and from 5,213 to 3,694 when going from one dog to two, with R still above the bar. The second dog makes the job more efficient; it isn't needed for reliability.

**Limitations and non-claims**

- The claim-grade baseline is HerdSim's `strombom_multi`, not the unmodified single-shepherd algorithm from the paper.
- The compact task is easy enough to create a ceiling effect. One dog succeeds for every `N >= 25`, so these data can't support a growing dog-count law. For what `D_max = 35` does and doesn't mean, see [Upper frontier status](#upper-frontier-status).
- The split layout behaved almost exactly like compact (matching medians for ticks and path at D = 1). Mean fragmentation stays near 1.0, so the intended separation barely shows up in the recorded state. We make no claim about split starts until the generator's separation is confirmed.

Compact-start frontier (Phase 1 claim merge):

| N | D_min | D_max | D_overcrowd |
|---:|---:|---:|---|
| 5 | 2 | 35 (ceiling) | none |
| 10 | 2 | 35 (ceiling) | none |
| 25-400 | 1 | 35 (ceiling) | none |

Every baseline `D_min` above has a bootstrap interval of width zero. Source files: `scaling/results/phase1/claim/`.

### `kubo`

There's no Collect/Drive switch. Sheep and dogs move under continuous forces (push, align, pull) with local sensing and speed limits. Each dog targets the sheep farthest from the goal among those it can sense, and dogs push each other apart so they don't pile onto one spot.

![Kubo force-based control.](../results/summary/figures/schematics/en/alg_kubo.svg)

*Continuous forces; each dog presses the in-range sheep farthest from the goal, and dog-dog repulsion spreads the team out.*

**Published inspiration**

Kubo et al. (2022) model sheep and multiple dogs as sums of continuous forces rather than a Collect/Drive switch. Sheep combine repulsion from neighbours, velocity alignment, cohesion and repulsion from dogs. Each dog targets an in-range sheep farthest from the goal, and its motion is shaped by repulsion from that sheep, from the goal and from other dogs. Dog-dog repulsion can spread the team behind the flock.

Ref: paper

**HerdSim implementation**

The `kubo` method bundle combines:

- `sheep_model=kubo`;
- `dog_controller=kubo_forces`;
- 40 sheep and 4 dogs by default, outside experiment overrides.

It does not use Strombom sheep and has no Collect/Drive state.

**Sheep force step**

For each sheep, HerdSim finds the sheep and dogs within `radius` and computes:

- mean inverse-square repulsion from other sheep;
- mean unit velocity of moving neighbours;
- mean unit attraction toward neighbouring sheep;
- mean inverse-cube repulsion from dogs.

These are weighted by sheep gains `K_s1..K_s4` (defaults below), carried over from the Kubo-style model and not retuned per N or layout. The resulting speed is capped at `sheep_speed_max` so one force spike can't produce a huge step. Position advances by `dt * velocity` with `dt = 0.05`, so a Kubo tick is a fixed integration step, not a unit move as with Strombom-family sheep.

**Dog force step**

For each active dog that can see at least one sheep:

- Build its local, observation-limited view.
- Keep only sheep inside `radius`.
- Pick the in-range sheep farthest from the goal.
- Combine attraction to that sheep, inverse-cube repulsion from it, repulsion from the goal, and inverse-cube repulsion from other in-range dogs.
- Weight these with dog gains `K_f1..K_f4` (defaults below), again not retuned per cell.
- Cap speed at `dog_speed_max` and advance by `dt * velocity`.

A dog that sees no sheep stays put for that tick. Sheep update before dogs within each step. HerdSim adds its own goal, arena walls, per-agent response and cohesion factors, and observation pipeline around these forces.

Defaults in the method bundle:

- `radius = 60`: local sensing radius.
- `K_s1 = 10`: sheep-sheep repulsion.
- `K_s2 = 0.5`: sheep velocity alignment.
- `K_s3 = 2`: sheep cohesion.
- `K_s4 = 5000`: sheep repulsion from dogs.
- `K_f1 = 10`: dog attraction to its target sheep.
- `K_f2 = 200`: dog repulsion from its target sheep.
- `K_f3 = 8`: dog repulsion from the goal.
- `K_f4 = 3000`: dog-dog repulsion.
- `dt = 0.05`: integration step.
- `sheep_speed_max = 5`: sheep speed cap.
- `dog_speed_max = 10`: dog speed cap.

Kubo is a Phase 4 transfer method, run on the same size and structure maps as the baseline (global observation, scout then claim). One window got extra precision: `outlier_rich`, `N = 200`, `D` in `{1, 2, 3, 4, 6, 10, 15, 20, 25}` was raised to 200 seeds; `D = 35` stayed at 30 scout seeds.

The experiment sets the counts for each `(N, D)` cell but does not retune Kubo's force gains for each flock size or layout.

#### Results

**Compact size map**

- `D_min = 3` at `N = 5` (bootstrap `[1, 3]`); `D_min = 1` from `N = 10` to 400.
- No overcrowding; `D_max = 35` is the grid ceiling ([Upper frontier status](#upper-frontier-status)).
- Overall success in the Kubo size claim merge is 0.991 (4,428 successes, 42 failures, 4,470 rows). Every failure is a timeout; there are no oscillation or stuck labels.

![`kubo` compact reliability heatmap.](../results/phase4/kubo_size/claim/packages/a/figures/reliability_heatmap.png)

*Success rate R(N, D) for `kubo`, compact starts only.*

What this shows: like the baseline, most of the compact surface is high. The weak corner is the smallest flock at low D: at N = 5, R is about 0.77 with one dog and 0.71 with two, before clearing the bar at three. From N = 10 upward, one dog is already reliable.

![`kubo` frontier D_min(N).](../results/phase4/kubo_size/claim/packages/a/figures/frontier_dmin.png)

*`D_min(N)` on compact starts; `D_max` sits at the grid top where there's no overcrowding.*

What this shows: after N = 5 (`D_min = 3`), the frontier stays at 1 up to N = 400. There's no overcrowding curve; `D_max = 35` is the grid ceiling everywhere. On tight starts with N >= 10, Kubo and the baseline share the same lower frontier.

![`kubo` cost against D.](../results/phase4/kubo_size/claim/packages/a/figures/cost_vs_d.png)

*Finish time and path against dog count on the Kubo compact size map.*

What this shows: once cells are reliable, adding dogs doesn't cause a collapse. Path still tends to rise with D while finish time stays in the successful range, the same waste pattern as the baseline. (Kubo ticks are not the same physical time as Strombom ticks.)

![`kubo` size-map outcomes.](../results/phase4/kubo_size/claim/packages/a/figures/failure_modes.png)

*How trials end in the Kubo compact size claim merge (4,470 rows).*

What this shows: 42 failures, all timeouts; overall success about 0.991. Failures are rare and come from running out of time, not from the oscillation that dominates FAT.

![`kubo` regime counts.](../results/phase4/kubo_size/claim/packages/a/figures/regime_counts.png)

*Regime labels on the 100 Kubo size-by-dog cells.*

What this shows: 87 wasteful, 11 efficient, 2 under-resourced, 0 overcrowded. Almost the same mix as the baseline: most reliable cells already have more dogs than they need.

**Starting structure**

- Compact and split: `D_min = 1` at `N = 50, 100, 200`.
- `outlier_rich`: `D_min = 1` at `N = 50` and `100`.
- `outlier_rich`, `N = 200`: point estimate `D_min = 20`.
- Wide: hard failure at all three sizes. The best success rate over all tested dog counts is about 0.47 to 0.54. Failures are mostly timeout or scatter: the flock stays too spread out for the local-force dogs to finish by T0. More dogs push R up toward about 0.5, but never past 0.90 within D <= 35, so the label is hard failure, not overcrowding.

![`kubo` R vs D by layout at N = 50, 100, 200.](../results/phase4/kubo_structure/claim/packages/b/figures/layout_reliability_by_n.png)

*Success rate R(D) for each layout at the three structure sizes.*

What this shows: compact and split stay above the bar at every D and all three sizes. Wide stays stuck in the middle (best R about 0.47 to 0.54) and never reaches 0.90, so transfer fails on spread-out starts. `outlier_rich` keeps `D_min = 1` at N = 50 and 100, but at N = 200 it only clears the bar at high D (next figures). Sharing the baseline's compact `D_min` doesn't extend to every layout.

![`kubo` layout cost at D = 1.](../results/phase4/kubo_structure/claim/packages/b/figures/layout_cost_d1.png)

*Median path (and related cost) by layout with one dog.*

What this shows: where one dog is already reliable (compact, split), cost is the only difference. Wide and large `outlier_rich` are the expensive or unreliable starts. For wide, the cost at D = 1 isn't a success story, because those cells never reach the bar at any D.

For `outlier_rich`, `N = 200`, the raise-to-200 rule kicked in ([Bootstrap on `D_min`](#bootstrap-on-d_min-analysis-then-maybe-more-seeds)): those D cells were rerun at 200 seeds and the bootstrap repeated. At that depth, `R = 0.935` at `D = 20` and `R = 0.910` at `D = 25`. The bootstrap interval is still `[2, 20]`, because several smaller D values sit just under the bar and resampling can pull the estimate down. So we report `D_min = 20` with interval `[2, 20]`. More seeds did not sharpen this edge.

![Kubo outlier_rich, N = 200.](../results/summary/figures/f9_kubo_outlier_rich_n200.png)

*R(D) with Wilson 95% intervals. D_min = 20 is the first count to clear the bar; after 200 seeds the bootstrap interval is still [2, 20].*

What this shows: R climbs slowly (0.745 at one dog, 0.86 to 0.89 between 4 and 10 dogs) and first clears 0.90 at D = 20 (0.935). It stays above at D = 25 (0.910) and D = 35 (0.967, scout depth of 30). Because several lower counts are so close to the bar, the interval stays wide even at 200 seeds. Treat `D_min = 20` as a point estimate with real uncertainty below it, not a sharp cliff.

**Limitations and non-claims**

- Sharing the compact `D_min` doesn't mean full transfer. Kubo failed the 90% bar on every wide cell and shifted sharply at `outlier_rich`, `N = 200`.
- The `[2, 20]` interval makes the lower side of `D_min = 20` uncertain.
- Hard failure on wide means no tested `D <= 35` reached the bar. It is not evidence that more dogs make Kubo worse.
- Kubo ticks are not comparable to Strombom-family ticks, because Kubo uses `dt` integration.
- HerdSim's walled arena, spawn geometry, goal disk and dog counts are choices made for this study, not a reproduction of the paper's exact setup.

### `fat`

Sheep still follow the Strombom model, but the dogs use a much simpler rule. Each dog looks at the sheep it can see, picks the one farthest from itself, and moves behind that sheep on the side away from the goal. There's no Collect/Drive switch and no spacing between dogs.

![FAT farthest-agent targeting.](../results/summary/figures/schematics/en/alg_fat.svg)

*Each dog independently presses the visible sheep farthest from itself; no Collect/Drive switch and no dog-dog spacing.*

**Published inspiration**

FAT is inspired by the local-camera shepherding rule discussed by Tsunoda et al. (2018): act on the farthest agent in the herder's field of view, without needing global flock coordinates.

HerdSim doesn't implement that paper's camera model, position-error handling, sheep dynamics, navigation law or calibration. The paper inspired the target-selection rule; we don't claim to reproduce the full model.

Ref: paper

**HerdSim implementation**

The `fat` method bundle combines:

- `sheep_model=strombom`
- `dog_controller=fat`
- 2 dogs by default, outside experiment overrides.

So the sheep use HerdSim's Strombom grazing, flocking, repulsion and fixed-step movement. The dog controller has no Collect/Drive switch and no check on how tight the flock is.

For each active dog on each tick:

- Read that dog's observation after observation-mode and sensing filters.
- If it sees no sheep, it stays still.
- Pick the visible sheep farthest from the dog.
- Set a target `r_a` behind that sheep, on the line from the goal through the sheep.
- Move toward the target at `shepherd_speed`, with Strombom angular noise.
- Stop if any visible sheep is closer than `shepherd_stop_multiple * r_a`.

Every dog decides on its own. There's no dog-dog repulsion, no negotiation over targets and no explicit spacing.

**Experiment scope**

FAT is a Phase 4 transfer method on the same size and structure maps (global observation, scout then claim). No coordination is added.

The global observation setting matters here. The FAT idea comes from local sensing, but in Phases 1, 2 and 4 each FAT dog could see the whole flock. These results therefore say nothing about the local-camera limitation. Phase 5's information ladders were only run on the baseline, not on FAT.

**Results**

**Compact size map**

- `D_min = 1` at `N = 5` and `N = 10`.
- For every `N >= 25`, no dog count up to 35 reached `R >= 0.90`.
- Those larger sizes are hard failures: `D_min` and `D_max` are undefined (not zero, and not 35).
- The best success rate for `N = 50` to 400 was about 0.40 to 0.53.
- About half of all FAT size trials failed: about 39% of trials by oscillation and 7% by getting stuck.

![`fat` compact reliability heatmap.](../results/phase4/fat_size/claim/packages/a/figures/reliability_heatmap.png)

*Success rate R(N, D) for `fat`, compact starts only.*

What this shows: only the smallest flocks have a reliable band (N = 5 and 10 clear the bar with one dog). For N >= 25 the whole surface stays below 0.90; the best R per size for N = 50 to 400 is about 0.40 to 0.53, and some cells drop to about 0.17. Adding dogs doesn't create a reliable band.

![`fat` frontier D_min(N).](../results/phase4/fat_size/claim/packages/a/figures/frontier_dmin.png)

*Where no D reaches the bar, `D_min` is undefined (hard failure), not zero.*

What this shows: `D_min = 1` only at N = 5 and 10. For every larger N there's no frontier at all, and no `D_max` to draw. That's the opposite of the baseline and Kubo, which sit at one dog.

![`fat` cost against D.](../results/phase4/fat_size/claim/packages/a/figures/cost_vs_d.png)

*Finish time and path against dog count on the FAT compact size map.*

What this shows: on the hard-failure sizes these costs aren't an efficiency story. Many runs never succeed, so path and time describe failed or mixed cells. Rising path here is not the same "waste after `D_min`" pattern seen for Strombom and Kubo.

![`fat` size-map outcomes.](../results/phase4/fat_size/claim/packages/a/figures/failure_modes.png)

*How trials end in the FAT compact size claim merge (4,400 rows).*

What this shows: 2,206 failures, about half of all trials. Most are labelled oscillation (1,707, about 39% of all trials), then stuck (295, about 7%), then timeout (204). FAT doesn't just run out of time; it mostly goes back and forth without making progress.

![`fat` regime counts.](../results/phase4/fat_size/claim/packages/a/figures/regime_counts.png)

*Regime labels on the 100 FAT size-by-dog cells.*

What this shows: 80 hard failure, 17 wasteful, 3 efficient, 0 overcrowded. The map is dominated by cells that never reach the bar.

**Starting structure**

FAT didn't reach 90% in any structure cell at `N = 50, 100, 200`.

- Compact best `R`: 0.47, 0.40, 0.47 for `N = 50, 100, 200`.
- Split best `R`: 0.50, 0.47, 0.40.
- `outlier_rich` best `R`: 0.10, 0.00, 0.00.
- Wide best `R`: 0.00 at all three sizes.

![`fat` R vs D by layout at N = 50, 100, 200.](../results/phase4/fat_structure/claim/packages/b/figures/layout_reliability_by_n.png)

*Success rate R(D) for each layout at the three structure sizes.*

What this shows: at every size, every layout stays below the bar for every D. Compact and split top out around 0.40 to 0.50; `outlier_rich` and wide stay near zero, especially at larger N. A different starting shape doesn't rescue FAT.

![`fat` layout cost at D = 1.](../results/phase4/fat_structure/claim/packages/b/figures/layout_cost_d1.png)

*Path (and related cost) by layout with one dog.*

What this shows: with R far below the bar, these costs mostly describe failed runs. How the layouts rank matters much less than the fact that none of them works.

The size merge also shows a strong negative link between FAT dog interference and success: Pearson `r` about `-0.87`. This is an observed correlation. It doesn't prove interference causes the failures.

![`fat` interference against D.](../results/phase4/fat_size/claim/packages/a/figures/interference_vs_d.png)

*Median mean I_dir on the FAT compact size map. Pearson r(I_dir, success) on that merge is about -0.87 (correlation only).*

What this shows: FAT dogs interfere with each other far more than baseline or Kubo dogs (mean `I_dir` about 0.40 at N = 100, against about 0.05 and 0.10). That makes interference a good candidate to test in future mechanism work, but this is not a completed RQ3 test.

**Limitations and non-claims**

- This is a minimal FAT controller on Strombom sheep, not the full Tsunoda et al. model.
- The results use global observation. They don't measure camera occlusion, bearing-only control, position error or recovering lost sheep.
- Hard failure means no tested count reached the 90% bar before `T0`. It doesn't prove FAT can never work at larger `D`, with a longer deadline, or on another task.
- More dogs didn't rescue larger flocks on this grid. That alone doesn't identify why.
- The interference correlation is not a controlled causal test.

---

## 7. Findings synthesis

Everything planned has now been run. The firm claims come from Phases 1, 2 and 4 (baseline size and structure, plus Kubo and FAT). Phase 6 fits the Phase 1 frontier. Phase 5 (information) and Phase 7 (early warning) are complete, but for reasons explained in sections 13 and 15 they don't support strong conclusions. Phase 3 (mechanism) was skipped because no overcrowding appeared.

### At a glance

| Verdict | Finding | Key numbers |
|---------|---------|-------------|
| Lower frontier (`D_min`) | With the baseline and a tight start, one dog is enough for 25 to 400 sheep. | N = 5 and 10 need two dogs; with one dog their success rates are only about 0.07 and 0.24. |
| Upper frontier (more dogs) | Adding dogs past the minimum never breaks success on this map; it mainly adds walking. `D_max = 35` is "top of our list", not a measured collapse. | 88 of 100 cells are wasteful, 0 overcrowded. Typical finish about 183 ticks; path per dog about 148 for N >= 25. |
| Structure is cost, not dog count | Messier starts take longer and need more walking, but one dog still succeeds on the baseline. | Wide starts take about 11x to 20x the time and 19x to 36x the path of compact starts with one dog. For wide starts the cheapest reliable choice is two dogs (`B* = 2`). |
| Partial transfer | Kubo and FAT don't copy the baseline everywhere. | Kubo matches the baseline on tight starts but fails on wide ones (best R about 0.47 to 0.54). FAT only reaches 90% for N <= 10. |
| Draft pattern not seen | The draft's "large flocks need many dogs" doesn't appear on the compact baseline map. | Draft: about 20 to 35 dogs for N >= 200. Here: one dog herds 400 sheep in a median 168 ticks. |
| Information (Phase 5) | Local sensing (radius 65) works as well as a full view on compact N = 100 and 200. The other ladder steps didn't test what they were meant to. | Local and global both have `D_min = 1`. Bearing-only dogs never moved; range settings had no effect; communication runs fed duplicated sheep lists to the controller. |
| Early warning (Phase 7) | Not testable on this data. | At tick 1,000 (first check), only 5 of 2,031 successful runs are still going; AUROC couldn't be computed. |

### Contrast with the 2025 draft

![Draft versus this HerdSim protocol.](../results/summary/figures/schematics/en/draft_vs_herdsim.svg)

*Same broad question and 90% bar, but a different task, arena and controller family. This is a contrast, not a matched replication.*

Smallest reliable dog count (`D_min`) on compact starts at the 90% bar:

| N | Baseline (`strombom_multi`) | Kubo | FAT | 2025 draft |
|---:|---:|---:|---:|---:|
| 5 | 2 | 3 | 1 | 1 |
| 10 | 2 | 1 | 1 | 1 |
| 25 | 1 | 1 | none <= 35 | 1 |
| 50 | 1 | 1 | none <= 35 | 1 |
| 75 | 1 | 1 | none <= 35 | not tested |
| 100 | 1 | 1 | none <= 35 | 1 |
| 150 | 1 | 1 | none <= 35 | 3 |
| 200 | 1 | 1 | none <= 35 | 20 |
| 300 | 1 | 1 | none <= 35 | 20 |
| 400 | 1 | 1 | none <= 35 | 35 |

`none <= 35` means no tested dog count reached 90% success. On *this* protocol, the steep rise the draft saw for large N doesn't appear on the baseline compact map. Since the draft used a harder gather-hold-gate task, this tells us the rise is not a general property of herding; it doesn't tell us the draft was wrong about its own task.

### Baseline cost and regimes

Headline numbers are in [At a glance](#at-a-glance) and per-method plots in [Methods and results](#6-methods-and-results). The figure below puts the frontiers side by side, with the draft for comparison:

![D_min against N, with 2025 draft contrast.](../results/summary/figures/f2_dmin_vs_n.png)

*Baseline and Kubo stay at about one dog for large compact flocks; the draft rises sharply. FAT has no D_min for N >= 25.*

### Upper frontier status

RQ2 also asks: once you *already* have enough dogs, does adding more help, do nothing useful, or start to hurt? (Definitions in [Frontier, regimes, and failure labels](#frontier-regimes-and-failure-labels).) Up to D = 35:

| Method | Compact `D_min` | Overcrowding? | What `D_max` means here | Do extra dogs hurt success? |
|--------|----------------:|---------------|-------------------------|-----------------------------|
| `strombom_multi` | 2 at N = 5, 10; otherwise 1 | no | 35 = top of tested list | No: success stays high; extra dogs mostly walk more |
| `kubo` | 3 at N = 5; otherwise 1 | no | 35 = top of tested list | Not on compact. Structure is a different story (wide fails; large outlier_rich needs many dogs) |
| `fat` | 1 only at N = 5, 10; undefined for N >= 25 | no | undefined when nothing reaches 90% | Not an overcrowding story: large N never reaches 90% at any D |

So `D_max = 35` means "still fine at the largest D we tried", **not** "collapse begins at 35".

The only place in the whole program where success *fell* as dogs were added is in the Phase 5 communication ladder: at N = 200 with neighbour or global sharing, all 30 runs at D = 10 failed while D = 6 succeeded. That cell is scout-grade (30 seeds), only one tested D failed (overcrowding needs two in a row), and it is most likely caused by how shared sheep lists are combined in the controller rather than by dogs crowding each other (see [Information ladders](#13-information-ladders)). We don't count it as overcrowding.

### Future work: measuring collapse beyond D = 35

Not run. This extension would allow more than 35 dogs and check whether success eventually falls (a real upper collapse), or whether wasted walking simply keeps rising.

| Question | Why it matters | How we'd run it |
|----------|----------------|-----------------|
| After a reliable band, does success fall for some D > 35? | Turns the ceiling into a measured collapse point | Extend the dog-count list past 35 for selected N |
| If success stays high, does wasted walking keep rising? | Shows a waste-only upper band even with many dogs | Same extended sweep; report path and regimes |
| Does a longer deadline (T1) rescue high-D failures at T0? | Separates "too slow" from "truly overcrowded" | T1 only on candidate overcrowded cells |
| Do efficient and overcrowded cells differ in interference or splitting? | Makes RQ3 possible | Matched comparisons at the same N |
| Does the upper-band story transfer across methods? | RQ4 for the upper band | Repeat with Kubo / FAT (later `communication_free`) |

Another option that doesn't raise the dog cap: port the harder draft-style task and see whether overcrowding appears within D <= 35 ([If we rerun a draft-style method](#if-we-rerun-a-draft-style-method)). Not scheduled; there are no claim-grade D > 35 cells in this report.

---

## 8. Answers to research questions

One table for all the research questions. Details and figures are in the method sections; formal claim codes are in [Claims](#11-claims).

| RQ | Question | Status | What we found |
|----|----------|--------|---------------|
| RQ1 | At the same flock size, does starting shape change how many dogs you need? | Answered on baseline | Not for dog count: all four layouts need only one dog at N = 50, 100, 200. Shape changes time and walking, not `D_min`. On Kubo, shape does matter (wide fails; large outlier_rich needs about 20). (C1a rejected; C1b inconclusive.) |
| RQ2 | As N grows, how does the useful dog range change? | Answered within D <= 35 | Lower end: from N = 25 up, the baseline needs one dog on compact starts. Upper end: extra dogs waste walking; no overcrowding; `D_max = 35` is a list ceiling ([Upper frontier](#upper-frontier-status)). D > 35 not tested ([Future work](#future-work-measuring-collapse-beyond-d--35)). |
| RQ3 | Why do efficient and overcrowded cells differ? | Not answerable | No overcrowding appeared on the baseline, so there's nothing to compare. |
| RQ4 | Do the patterns transfer to Kubo and FAT? | Partly | On tight starts, Strombom and Kubo both need one dog for N >= 25; FAT never reaches the bar there. Wide starts break Kubo; FAT fails on every structure cell. |
| RQ5 | Can better information reduce the dog count? | Not answered | Local sensing works as well as a full view (both `D_min = 1`), so less information didn't cost dogs. Whether *more* information saves dogs can't be judged: the baseline is already at one dog, and the bearing-only, range and communication runs each had a setup problem ([Information ladders](#13-information-ladders)). |
| RQ6 | Which curve best predicts an unseen N? | Weak answer | A two-level step fits best, simply because `D_min` only takes the values 2 and 1. Not a meaningful scaling law. |
| RQ7 | Can recent state warn of failure better than N and D? | Not answerable on this data | By the first check at tick 1,000, almost every successful run had already finished, so there was nothing to compare failures against ([Prediction and early warning](#15-prediction-and-early-warning)). |

---

## 9. Cross-method transfer

Same grids and layouts for every method. For each feature we ask: does it match the baseline, shift, or disappear?

### Compact size map

| Case | What we see |
|------|-------------|
| Shared | Strombom and Kubo both need one dog for N >= 25 (Kubo needs three at N = 5, then one from N = 10). |
| Absent (FAT) | For every N >= 25, FAT never reaches 90% with any D <= 35. Best R is about 0.40 to 0.53. |
| Ceiling, not collapse | Strombom and Kubo show no overcrowding on compact starts; `D_max = 35` is the list ceiling ([Upper frontier](#upper-frontier-status)). |

The automatic Package D comparison labels the size-map features as 8 shared, 7 shifted and 29 absent. Most of the "absent" count comes from overcrowding rows, simply because no controller overcrowds on compact starts.

### Structure map (`D_min` at theta 0.90)

| Layout | N | Strombom | Kubo | FAT |
|--------|---:|---:|---:|---:|
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

`none` means no dog count up to 35 reached 90% success.

What this shows: sharing `D_min = 1` on compact starts does **not** mean full transfer. Wide starts and large outlier-rich starts are where the methods part ways, and FAT clears no structure cell at all. The Kubo `outlier_rich`, N = 200 detail (point `D_min = 20`, interval `[2, 20]`) is under [`kubo`](#kubo).

![Transfer sketch.](../results/summary/figures/schematics/en/transfer_sketch.svg)

*Same grids and layouts; each frontier feature is labelled shared, shifted, or absent.*

![Cross-method layout reliability curves.](../results/summary/figures/f5_layout_reliability_curves.png)

*Success curves at N = 200 for every method and layout. Per-method structure plots are in each method section.*

---

## 10. Scaling fits

Once we have `D_min` for each flock size, RQ6 asks which simple formula best predicts a flock size left out of the fit.

On the baseline compact map, `D_min` takes only two values: 2 for N = 5 and 10, and 1 for everything larger. The error below is leave-one-N-out RMSE (lower is better):

| Model | RMSE | What it assumes |
|-------|-----:|-----------------|
| Constant | 0.44 | One flat dog count |
| Linear | 0.44 | A straight line in N |
| Power law | 0.25 | A smooth curve on log-log axes |
| Piecewise | 0.13 | Two levels with a break near N = 10 |

The piecewise model wins because it matches that single step, not because we found a rich growth law. The fitted power-law slope is slightly negative (about -0.17), and across N = 25 to 400 the frontier is completely flat. Both formal RQ6 claims (C6a and C6b) technically pass on this data, but with only two distinct `D_min` values neither says much about how dog need scales. These fits are not a general scaling law.

![Leave-one-N-out RMSE by model.](../results/summary/figures/f8_scaling_rmse.svg)

*Source: `phase1/claim/packages/f/scaling_cv.csv`.*

---

## 11. Claims

Verdicts use claim-grade evidence only. The labels mean:

- **SUPPORTED**: the stated condition holds within this protocol
- **REJECTED**: we checked and it doesn't hold
- **INCONCLUSIVE**: we can't decide (usually the needed contrast is missing)
- **SKIPPED**: the trigger for the test never appeared

The "Recorded verdict" column is what the [progress tracker](progress_tracker.md) and claim packages report, applying each claim's rule as written. The last column is our reading of how much that verdict actually tells us.

![Claims scorecard.](../results/summary/figures/schematics/en/claims_scorecard.svg)

*Visual summary of the recorded verdicts. Detail in the table below.*

| Claim | RQ | What the claim says | Recorded verdict | Evidence | How much weight it carries |
|-------|----|---------------------|------------------|----------|----------------------------|
| C1a | RQ1 | `D_min` changes across layouts at fixed N | REJECTED | Baseline: `D_min = 1` for all four layouts at N = 50, 100, 200; bootstrap width 0 | Solid for the baseline. Not true for Kubo, where layout does shift `D_min`. |
| C1b | RQ1 | State features predict better than (N, D) | INCONCLUSIVE | No baseline `D_min` shift, so there's nothing to predict | Untestable here. Cost still depends strongly on layout. |
| C2a | RQ2 | Overcrowding appears on the size map | REJECTED | 0 overcrowded cells at theta 0.90 | Solid up to D = 35. Above 35 is untested. |
| C2b | RQ2 | Overcrowding survives a longer deadline | SKIPPED | No overcrowded cell to rerun at T = 20,000 | n/a |
| C3 | RQ3 | Pre-chosen signatures separate efficient from overcrowded cells | INCONCLUSIVE | No overcrowded cells to compare | n/a |
| C4 | RQ4 | Frontier features transfer across controllers | SUPPORTED (partial) | Strombom and Kubo share compact `D_min` for N >= 25; FAT absent for N >= 25; Kubo wide absent; Kubo `outlier_rich`, N = 200 shifts to `D_min = 20` (interval `[2, 20]`) | Solid. Transfer is conditional on controller and starting shape. |
| C5a | RQ5 | One ladder step lowers `D_min` by at least one grid step at N = 100, 200 | REJECTED | Package E: no step lowers a defined `D_min`; local and global both at 1; range and communication flat at 1; bearing-only hard-fails | Weak. The baseline is already at one dog, so a reduction was impossible, and three of the four comparisons had setup problems (section 13). Better read as "not tested". |
| C5b | RQ5 | The second ladder step saves fewer dogs than the first | INCONCLUSIVE | No first-step saving to compare (`median_first_step_delta = 0` on every ladder) | n/a |
| C6a | RQ6 | A power law fits worse than piecewise | SUPPORTED | Leave-one-N-out RMSE: power 0.247, piecewise 0.132 | Technically true, but there are only two `D_min` levels to fit. |
| C6b | RQ6 | The log-log slope of `D_min` on N is below 1 in a stated band | SUPPORTED | Compact N = 25 to 400: `D_min = 1` throughout, slope 0 | Technically true, but a flat line trivially has slope 0. |
| C7a | RQ7 | State-based warning beats an (N, D) baseline on held-out N | INCONCLUSIVE | Package G: held-out AUROC could not be computed (folds empty) | Untestable on this data (section 15). |
| C7b | RQ7 | At least 30% of failures are flagged 500+ ticks ahead | REJECTED | Package G: 14 of 169 failures (8.3%) have a measured lead time of at least 500 ticks | Weak. The test design and this failure pattern don't fit together well (section 15). |

These verdicts only hold within the tested protocol. They don't support a universal law, an untested task, real-farm performance, or a dog-count difference smaller than one step on our D list.

---

## 12. Limits and threats

What this report can and can't say:

| Limit | How we handle it |
|-------|------------------|
| One simulated task | Results apply to `drive_to_goal` under the frozen protocol only. |
| Method dependence | We check transfer (RQ4) before generalising; transfer is only partial. |
| Shape could be confused with size | N is matched and layouts are fixed; on the baseline, `D_min` didn't move with layout. |
| Discrete dog-count list | We can't resolve differences smaller than one step on that list. |
| Gradual reliability edges | Fixed seeds, claim windows, bootstrap, and 200 seeds where uncertainty is wide. Some edges stay gradual. |
| Conditional analyses | If the trigger never appears, we mark the test skipped or inconclusive, not "proven null". |
| Time across methods | Kubo ticks are not the same physical time as Strombom-family ticks. |
| Collect switch wider than the goal | A Strombom failure doesn't mean sheep couldn't pack into the goal. |
| Simulated controllers | No claim about real farms or animal behaviour. |
| Grid ceiling | `D_max = 35` is the top of our list, not a measured collapse ([Upper frontier](#upper-frontier-status); [Future work](#future-work-measuring-collapse-beyond-d--35)). |
| Easy compact map | Most baseline cells succeed with one dog at R near 1.00, which makes any rising dog-count law hard to see. It also left no room for information to save dogs (RQ5) and too few failures for early warning (RQ7). |
| Split layout | Behaves like compact so far; the generator's separation still needs checking. |
| Interference correlation | FAT's `I_dir` link to failure is a correlation, not a controlled test. |
| Phase 5 setup | Bearing-only input froze the dogs; range settings had no effect under global observation; communication duplicated sheep in the controller's input. See [Information ladders](#13-information-ladders). |
| Phase 7 timing | Warning checks start after almost every successful run has finished. See [Prediction and early warning](#15-prediction-and-early-warning). |

---

## 13. Information ladders

Status: **all six runs complete** (three scouts, three claims; 7,600 trials). The results are recorded faithfully below, but they answer RQ5 only in a narrow way.

RQ5 asks whether better information can replace dogs: if the dogs sense more, see farther, or share what they see, does the same reliability need fewer dogs? We test three separate ladders rather than every combination:

- **Observation content:** bearing only → local positions → global view
- **Sensing range:** 32.5, 65, 97.5, 130 (0.5x, 1x, 1.5x and 2x Strombom's `r_s` of 65)
- **Communication:** none → share with nearby dogs (`neighbour_broadcast`) → share everything any dog senses (`global_shared`)

All three ladders use the baseline `strombom_multi`, compact starts, N = 100 and 200, and the low dog band `{1, 2, 3, 4, 6, 10}`, since that's where saving even one dog would show up. Each scout uses 30 seeds per cell. Each claim reseeds its windows at 100 seeds: D = 1 and 2 wherever `D_min = 1`, and the two largest D (6 and 10) wherever nothing reached the bar.

### What the runs recorded

| Ladder | N = 100 | N = 200 | Package E summary |
|--------|---------|---------|-------------------|
| Observation | bearing only: hard failure; local: `D_min = 1`; global: `D_min = 1` | same | No defined `D_min` was lowered |
| Range | `D_min = 1` at all four ranges | same | `median_delta_dmin = 0` |
| Communication | `D_min = 1` for none, neighbour and global sharing | same | `median_delta_dmin = 0` |

On paper, then: information decides *whether* herding works at all (bearing-only never succeeds), but beyond local sensing nothing reduces the dog count. That's what the tracker recorded as C5a rejected and C5b inconclusive.

When we looked at the trial data underneath those tables, though, three of the four comparisons turned out not to test what they were designed to test.

![Phase 5 information ladders.](../results/summary/figures/f11_phase5_ladders.png)

*A: success rate per observation mode. B: median dog path at N = 200 for the four sensing ranges (the four curves lie exactly on top of each other). C: success rate at N = 200 per communication mode. Built from the three claim merges by `results/summary/_gen_phase57_figures.py`.*

### Local positions vs global view: a real result

This is the one clean comparison. With dogs limited to sheep within 65 units, results are practically identical to giving every dog the full flock: R = 1.00 in every cell, `D_min = 1` at both sizes, and median dog path within about 1% of the global case (for example 161.6 vs 161.4 at N = 100, D = 1). On tight starts at these flock sizes, a local view costs nothing. This doesn't tell us about wide or outlier-rich starts, where sheep may sit beyond a dog's range.

### Bearing-only: the dogs never moved

Every one of the 640 bearing-only trials in the claim merge has a dog path of exactly 0. The dogs never left their starting spots, and every run timed out (all labelled oscillation).

The cause is in how bearing-only input reaches the controller. The bearing-only observation replaces each visible sheep with a point one unit away from the dog in that sheep's direction (direction is kept, distance is thrown away). `strombom_multi` then applies its normal stop rule: stay still if any sheep is closer than `3 * r_a = 6` units. Every "sheep" is now one unit away, so the dog always stops.

So this result says "the position-based Collect/Drive controller can't use bearing-only input", not "bearing-only information is too poor to herd with". A real bearing-only test needs a controller written for bearings.

### Sensing range: the setting had no effect

All four ranges produced *identical* trials. Across all 640 matched seed-cells, the dog path is the same to the last decimal whichever range is set (panel B).

The range runs didn't specify an observation mode, so they ran with the method default: global observation. Under global observation every dog sees every sheep regardless of range. In `strombom_multi`, the range value is only used to decide which dogs count as neighbours for `neighbour_broadcast`, which is switched off in this ladder. In effect the range ladder ran the same experiment four times.

To test sensing range properly, it needs to be paired with `local_positions` observation.

### Communication: sharing changed the controller's input, not its information

Communication runs also used global observation, so sharing couldn't add any information: each dog already saw everything. Even so, sharing *did* change behaviour (panel C):

- `neighbour_broadcast` and `global_shared` produced identical trials in all 640 matched cases.
- Both gave somewhat shorter dog paths than `none` at D >= 2 (for example 245 vs 268 at N = 200, D = 2).
- At N = 200, D = 10, all 30 runs failed (oscillation) with either sharing mode, while `none` succeeded in all 30. At D = 6 the sharing runs still succeeded, but more slowly (median 240 vs 181 ticks).

Reading the controller code points to a likely reason. When lists are shared, the controller stacks every dog's list of sheep positions without removing duplicates. Under global observation that means each dog works with D copies of the flock. The flock centre doesn't change, but two quantities that depend on the sheep *count* do: the Collect threshold `r_a * count^(2/3)` and the Drive stand-off `r_a * sqrt(count)`. At N = 200 and D = 10 the controller thinks it has 2,000 sheep, so it places itself about 89 units behind the flock. That's farther than the 65-unit distance at which sheep react to a dog. We haven't confirmed this with a fixed rerun, so treat it as a probable explanation rather than a proven one.

Two more things to keep in mind about the D = 10 failure: those cells are scout-grade (30 seeds, outside the claim windows), and the drop is a single dog count, not the two-in-a-row the overcrowding rule needs.

### What Phase 5 does and doesn't tell us

- **It does show** that on compact starts at N = 100 and 200, the baseline herds just as reliably with a 65-unit local view as with a full view.
- **It can't show** that better information saves dogs. The baseline is already at one dog in every working configuration, so there was no room for a saving. The bearing-only, range and communication steps also had the setup problems above.
- **C5a (REJECTED)** follows the rule as written, but it's better read as "not tested" than as evidence that information can't replace dogs.

To give RQ5 a fair test, a rerun would need: (1) range paired with `local_positions`; (2) shared sheep lists merged by sheep identity, so each sheep is counted once; (3) a bearing-aware controller for the bearing-only step; and ideally (4) a harder starting layout (wide, outlier-rich) or controller where more than one dog is needed, so there's a dog count to reduce.

---

## 14. Outcomes and state metrics

What we record on each run:

- **Success:** did every sheep reach the goal in time? (yes/no)
- **Finish time (`t_s`):** the first tick at which that happens
- **Dog path:** total distance walked by all dogs; also path per dog
- **Cohesion:** how tightly the sheep cluster around the flock centre
- **Fragmentation:** size of the largest connected group of sheep, divided by N
- **Outliers / spread / extent / hull size / density / aspect ratio:** other summaries of the flock's shape
- **`I_dir` (interference):** near 0 if dogs move in the same direction; near 1 if their headings cancel out (they're pushing against each other)
- **Coverage:** fraction of the outer sheep that are within a dog's influence range

Technical notes: if no dog moves, `I_dir = 0`. Velocities include wall effects. A missing coverage radius gives NaN.

![Tick and path cost metrics.](../results/summary/figures/schematics/en/metrics_tick_path.svg)

![Reliability R.](../results/summary/figures/schematics/en/metrics_reliability.svg)

![Interference I_dir.](../results/summary/figures/schematics/en/metrics_idir.svg)

---

## 15. Prediction and early warning

Status: **run** (Package G, on the Phase 1 claim timeseries). The results exist but can't answer RQ7, for reasons that come down to timing.

RQ7 asks whether recent flock and dog state can warn that a run is about to fail, better than a baseline that only knows flock size and dog count.

**How it was set up** (fixed in the plan): at check times from tick 1,000 to 8,000 in steps of 200, look only at the last 200 ticks of state. Predict whether the run fails within the next 500 ticks. Train on some flock sizes and test on a left-out one (leave-one-N-out), and compare against a model that only knows N and D. Two claims follow: C7a (state beats N and D on held-out AUROC) and C7b (at least 30% of failures get a warning 500 or more ticks ahead).

**What came out:**

| Quantity | Value |
|----------|------:|
| Trials with timeseries | 2,200 |
| Failures | 169 |
| Held-out AUROC, state model | not computed |
| Held-out AUROC, (N, D) model | not computed |
| Leave-one-N-out folds | empty |
| Failures with a measured lead time | 14 of 169 |
| Median lead time (those 14) | 9,288.5 ticks |
| Share of failures with lead time >= 500 | 8.3% (bar: 30%) |

So C7a is INCONCLUSIVE (no AUROC to compare) and C7b is REJECTED (8.3% is below 30%).

**Why the test had so little to work with.** The figure below shows when each of the 2,200 runs ended.

![Early warning: run end times versus the check window.](../results/summary/figures/f12_early_warning_timing.png)

*Successful runs (blue) finish around 180 ticks. Failed runs (red) all run to the 10,000-tick deadline. The shaded band is where the warning checks happen.*

- Successful runs finish in about 183 ticks (median). Only 5 of the 2,031 successes are still running at tick 1,000, the first check time.
- All 169 failures run all the way to the 10,000-tick deadline. They are all N = 5 or N = 10 with a single dog (93 oscillation at N = 5; 58 stuck and 18 oscillation at N = 10).

At every check time, then, the runs still going are almost all failures. There are hardly any successful runs left to compare them against, and when a flock size with no failures is held out, its test fold has nothing to score. That is very likely why the folds came back empty. The lead-time numbers are also hard to interpret: every failure is a run that just never finishes, and a failure is only declared at tick 10,000, so long lead times are expected and don't by themselves show a useful warning.

**What it would take to test RQ7.** Data where failures and successes overlap in time: a harder layout or controller (for example Kubo on wide starts, or FAT, where about half the runs fail), or check times that start inside the first few hundred ticks. With the current Phase 1 data, RQ7 is open.

---

## 16. Commands run

Commands used for the completed campaigns (from the repo root; set `WORKERS` to suit the host):

```bash
make -C scaling scaling-test
make -C scaling scaling-pilot WORKERS=16
make -C scaling scaling-scout WORKERS=16
make -C scaling scaling-claim-plan
make -C scaling scaling-claim-reseed WORKERS=16
make -C scaling scaling-analyse PACKAGE=A TRIALS=results/phase1/claim/merged_trials.csv OUT=results/phase1/claim/packages/a
make -C scaling scaling-analyse PACKAGE=F TRIALS=results/phase1/claim/merged_trials.csv OUT=results/phase1/claim/packages/f
# T1 and Package C skipped: no overcrowding cells on the baseline map
make -C scaling scaling-phase2-scout WORKERS=16
make -C scaling scaling-phase2-claim-reseed WORKERS=16
make -C scaling scaling-transfer-size-scout TRANSFER_METHOD=kubo WORKERS=16
# then claim-reseed; repeat with TRANSFER_METHOD=fat
make -C scaling scaling-transfer-structure-scout TRANSFER_METHOD=kubo WORKERS=16
# then claim-reseed; repeat with TRANSFER_METHOD=fat
make -C scaling scaling-analyse PACKAGE=D TRIALS=... --trials-by-method ...
# Phase 5: all three ladders, scout then claim, via the orchestrator
bash scaling/results/phase5/run_all_ladders.sh            # WORKERS=18
#   which runs, in order:
#   make -C scaling scaling-factor-sweep WORKERS=18
#   make -C scaling scaling-phase5-obs-claim-reseed WORKERS=18
#   make -C scaling scaling-phase5-range-scout WORKERS=18
#   make -C scaling scaling-phase5-range-claim-reseed WORKERS=18
#   make -C scaling scaling-phase5-comm-scout WORKERS=18
#   make -C scaling scaling-phase5-comm-claim-reseed WORKERS=18
make -C scaling scaling-analyse PACKAGE=G TRIALS=results/phase1/claim/merged_trials.csv OUT=results/phase1/claim/packages/g
# Summary figures for Phases 5 and 7
.venv/bin/python scaling/results/summary/_gen_phase57_figures.py
```
