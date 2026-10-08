# Scaling Report

## Contents

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

## 1. HerdSim overview

> When a few shepherds guide a larger flock, how much control do we actually need as the flock gets bigger or more spread out?

If the flock gets bigger, or starts more spread out, do you need more dogs?

That is the same basic problem as an earlier 2025 draft paper on sheep scaling. This report keeps that problem, but tries to be more careful:

- say clearly what "how much control" means (not just a vibe),
- separate flock *size* from flock *shape* at the start,
- ask *why* a pattern shows up, not only that it does,
- check whether the pattern still appears under a different herding method.

We are not assuming there is one universal scaling law. We start from questions we can actually run in simulation.

**HerdSim** is the platform we use for that. A few dogs guide a larger flock to a goal, under settings you can fix and repeat. For this study it is a model system for measuring *control demand* (how much dog effort you need for reliable success). It is not meant to copy a real farm in full.

Herding is a good test case because control is *indirect*:

> A small number of external controllers tries to steer a larger group whose members are not commanded one by one.

The platform is built for fair comparison. You pick a method (how sheep move and how dogs decide), put it in a scenario, fix a random seed, and score runs with the same metrics. Then you can see when herding works, when it fails, and how methods compare when size and other settings are held equal.

HerdSim has two roles on one engine:

a. **Simulation + frontend**: interactive UI (Simulate, Compare, Experiments, NetLogo, Guide).
b. **Scaling**: command-line protocols that answer the control-demand research questions.

### Methods

A **method** is a ready-made package: a sheep model plus a dog controller, with paper-style defaults.

Methods currently in the platform:

- `strombom`: Strombom 2014, 50 sheep, 1 shepherd
- `strombom_multi`: Strombom Multi-Dog, 50 sheep, 3 dogs
- `strombom_noise`: Strombom Noise, 50 sheep, noisier motion, 1 shepherd
- `heterogeneous`: Heterogeneous Sheep, 50 sheep, 1 shepherd
- `v_formation`: V-Formation, Strombom sheep, 2 dogs
- `obstacle_aware`: Obstacle-Aware, 50 sheep, 1 shepherd
- `fat`: FAT, strombom sheep, 2 dogs
- `communication_free`: Communication-Free, strombom sheep, 3 dogs
- `adaptive`: Adaptive, strombom sheep, 2 dogs
- `kubo`: Kubo 2022, 40 sheep, 4 dogs
- `flocking_dog`: Flocking Dog 2024, 14 sheep, 1 dog

This study focuses on three of them: `strombom_multi` (our baseline), `kubo`, and `fat`.
Full controller detail and results: [Methods and results](#6-methods-and-results).

#### Why these three methods

The plan freezes one baseline and two other methods so we can ask: "If we change only the dog rules, does the size/structure story stay the same?" That is research question RQ4.

| Method | Role | Description |
|--------|------|-------------------|
| `strombom_multi` | Baseline | Dogs gather stragglers (Collect), then push the flock toward the goal (Drive) |
| `kubo` | Required comparison | Continuous "force" rules; no Collect/Drive switch; each dog pushes the sheep farthest from the goal (among those it senses) |
| `fat` | Required comparison | Each dog chases the sheep farthest from *itself*; no Collect/Drive switch; dogs do not space themselves apart |

We need different *kinds* of controllers on the **same** task (`drive_to_goal`), not three tiny variants of Collect/Drive. Those three are the locked minimum set for claims. `communication_free` is recommended next, but outside that minimum. Other presets exist in the UI; they are not part of the current claim set unless we add them later.

If all three methods show the same pattern (for example the same smallest reliable dog count), that pattern is more likely a real feature of the task, not a quirk of one controller. If Kubo or FAT breaks the pattern, we learn how far we can generalise. That is what RQ4 is for. It does *not* mean these three methods cover every herding idea in the world.

#### Method tracks: transfer vs draft

We pursue the same broad question ("how much control as size and spread change?") in two different ways:

| Track | What we change | Why | Linked RQs |
|-------|----------------|-----|------------|
| Same-task transfer (`strombom_multi`, `kubo`, `fat`; next: `communication_free`) | Only dog/sheep rules; task and grids stay fixed | See which patterns survive a controller change (RQ4) | RQ1 to RQ4 now; RQ5 to RQ7 later |
| Draft-style method in HerdSim (planned) | Task, arena, starts, and often the controller family (collect, hold, gate) | The 2025 draft used a collect-hold-gate task; planned as a HerdSim port to ask the same RQs there | Same central question; not a substitute for RQ4 |

The draft track lives under [Prior draft paper](#2-prior-draft-paper). It is not a fourth transfer method beside Kubo and FAT.

We use `drive_to_goal` as the main task because that is the frozen HerdSim protocol for fair method comparison. That choice does *not* say the draft task is wrong. When we later say the compact baseline looks "easy" (often one dog is enough), that is a measured outcome, not the reason we picked the task.

#### Does this answer the central question?

Here, "how much control" means the useful dog range under fixed rules:

- **`D_min`**: smallest dog count that still succeeds often enough (at least 90% of runs),
- what happens if you add more dogs: useful, wasteful walking, or real overcrowding collapse,
- all under a fixed time limit.

Which RQ covers which piece: size is RQ2 (and curve fits in RQ6); start shape is RQ1; "why" is RQ3 when we have overcrowding contrasts; method transfer is RQ4; information and early warning are RQ5 and RQ7.

The program answers by *bounding* the question inside this protocol: where dog need stays low, where cost rises without needing more dogs, where transfer fails, and later whether better sensing can replace dogs. Completed findings: [Findings synthesis](#7-findings-synthesis). Per-question answers: [Answers to research questions](#8-answers-to-research-questions).

This study does **not** claim a universal farm law, that the draft's rising dog counts are wrong on the draft's own task, or that every method needs only one dog for D up to 35.

---

## 2. Prior draft paper

The 2025 draft is titled "Collective Nudging that Scales". It asked a simple question: how many dogs do I need to herd sheep?

It was run in **NetLogo** (not HerdSim). The important differences from our main study:

- **Task**: gather the flock, hold it for 800 ticks, then push it out through a gate (not our open-field `drive_to_goal`).
- **Success**: every sheep through the gate by 10,000 ticks.
- **Arena**: patch grid 101 x 71, with a central hold zone and a gate on the right wall.
- **Starts**: sheep scattered at random; dogs start in a top-left grid.
- **Controller**: one NetLogo collect / drive / patrol family.
- **Same idea of reliability**: succeed in at least 90% of runs; `D_min` is the smallest dog count that hits that bar.
- **Grids**: dog counts up to 35; flock sizes up to 400 (details in the list below).

Full setup notes:

- NetLogo: 7.0.3 on a patch grid.
- Containment radius: `rc = clamp (2.5 * sqrt (N), 23, 27)`.
- D grid: `{1, 2, 3, 4, 6, 10, 15, 20, 25, 35}`.
- N grid: `{5, 10, 25, 50, 100, 150, 200, 250, 300, 350, 400}`.
- Sampling: 100 runs in every cell (11,000 total).
- Seed: master seed not stated in the note.
- `D_overcrowd` / `D_max`: draft definitions differ slightly from ours (see comparison figures later).
- Structure: emergent spread summarized by `S_bar`.
- Metrics: success, ticks, phase, spread, path, lost sheep.

![2025 draft task phases.](../results/summary/figures/schematics/en/draft_task_phases.svg)

*Draft task: collect, hold, then exit through a gate (NetLogo patch arena).*

![2025 draft experiment design.](../results/summary/figures/schematics/en/draft_experiment_design.svg)

*Draft design sketch: containment zone, gate, and run budgets.*

### Result of the paper

For small flocks one dog often worked; for large flocks the draft needed many more dogs (tens of dogs at N around 200 to 400).

At success rate (SR) >= 90%, draft Table A3 reports:

| N   | D_min | D_max     | Maximum SR |
|-----|-------|-----------|------------|
| 5   | 1     | not reach | 100%       |
| 10  | 1     | 15        | 100%       |
| 25  | 1     | 25        | 100%       |
| 50  | 1     | 25        | 100%       |
| 100 | 1     | not reach | 100%       |
| 150 | 3     | not reach | 99%        |
| 200 | 20    | 35        | 94%        |
| 250 | 25    | not reach | 93%        |
| 300 | 20    | not reach | 93%        |
| 350 | 35    | not reach | 91%        |
| 400 | 35    | not reach | 91%        |

Here "not reach" means they never found an upper failure point before D = 35.

The draft also found that more spread tended to go with worse success (Spearman `rho = -0.701` for mean spread `S_bar` vs SR, and `rho = -0.828` for `S_bar * N` vs SR, over 110 condition aggregates).

![2025 draft main results sketch.](../results/summary/figures/schematics/en/draft_main_results.svg)

*Draft Table A3 pattern: D_min stays low at small N, then rises sharply for large flocks.*

### If we rerun a draft-style method

We did **not** rerun the draft in this campaign. The plan is to port that collect / hold / gate task (and its controller family) into **HerdSim**, not to rerun NetLogo.

The aim is to ask the same research questions on that collect-hold-gate task, alongside the questions already asked on `drive_to_goal`. It is not equivalent to adding one more dog rule on the current task.

| Question the HerdSim draft rerun would ask | Planned RQ |
|--------------------------------------------------|--------------------------|
| As flock size grows on collect-hold-gate, how many dogs do you need, and do extra dogs help, plateau, or hurt? | RQ2 (size and regimes); RQ6 after we have frontiers |
| At the same flock size, does start shape or hold-phase state change how many dogs you need? | RQ1 (structure), using draft-style state such as spread / `S_bar` where useful |
| If too many dogs start to hurt success, what mechanisms separate "good" cells from overcrowded ones? | RQ3 (mechanism), only if those contrasts appear |
| On a frozen draft-style task, which patterns still hold when we change only the controller? | RQ4 (transfer), after that task is frozen first |
| On that task, can better sensing or communication reduce the dog count at the same reliability? | RQ5 |
| On that task, can recent flock state warn of failure better than knowing only N and D? | RQ7 |

The planned RQs stay the program's questions; the draft-style HerdSim run asks them again under that task. Track placement: [Method tracks: transfer vs draft](#method-tracks-transfer-vs-draft).

---

## 3. Research questions

The program asks how many dogs are needed for reliable herding as the flock gets bigger or more spread out, why that demand appears, and whether the answer depends on which herding method you use.

For each core question below: what we want to know, how we study it, and what kinds of answers would count. We do not lock in a preferred outcome ahead of time.

### What we want from the program

After the core runs, we should be able to say something concrete about:

- how dog need changes as the group grows,
- whether start shape matters beyond size,
- which processes seem to drive the pattern,
- what looks shared across methods versus method-specific.

A simple predictive rule would be useful. Strong method dependence would also be useful: that still bounds how far results can be generalised. Relative to a single-method scaling study, the program defines control demand in a reusable way, separates size from structure, tests mechanisms instead of stopping at correlation, and checks which features survive a method change.

### Core questions

#### Size and operating regimes (RQ2, with curve fits in RQ6)

**Question.** As flock size grows, how does the useful dog range change: the minimum needed for reliable herding, and whether adding more still helps, mostly wastes path, or starts to hurt?

RQ6 is the follow-on modeling step: once we have those minimums (`D_min` vs N), which simple curve best predicts a held-out flock size, and is one power law enough?

**Approach.** Freeze the protocol. Change flock size `N`, keep other settings fixed. For each `N`, find the smallest dog count `D` that hits the reliability target, and check whether larger `D` still helps, plateaus, or hurts. Only fit curves after those frontiers exist.

**Possible results.** Dog need may grow smoothly, grow in steps, stay flat, or look messy. We also label operating regimes: too few dogs, efficient, wasteful (success but lots of walking), or overcrowding (success falls when D is high).

#### Structure (RQ1)

**Question.** At the same flock size, does start shape (spread, split, outliers) change how many dogs are needed?

In claim form: does `D_min` change across initial layouts at fixed N?

**Approach.** Hold `N` fixed. Change only the starting layout on purpose. Measure a few shape properties and see how much leftover difficulty size alone cannot explain.

**Possible results.** Size may be almost enough; a few structure measures may explain the rest; or different properties may matter at different sizes.

#### Mechanism (RQ3)

**Question.** Why does the pattern appear (for example dog interference, flock splitting, coverage limits)?

In claim form: which prechosen signatures separate efficient cells from overcrowding cells at the same N?

**Approach.** Candidates include spatial demand, fragmentation, dog interference, redundant control, and local instability. We log quantities tied to those ideas and compare. Correlation alone is not treated as proof of cause.

**Possible results.** One main mechanism; several mechanisms in different regimes; or a pattern that does not reduce to one clean story.

#### Generality across methods (RQ4)

**Question.** If we switch herding method, which parts of the pattern stay the same?

**Approach.** Rerun the core size and structure maps under `strombom_multi`, `kubo`, and `fat`. Compare frontiers and regime labels, not only raw success rates. Mark what is shared vs method-specific.

**Possible results.** Fully method-specific; same shape with different magnitude; or same shape with different thresholds. Strong method dependence limits how far we can talk about "scaling" apart from the controller.

### Follow-on questions

These come after the core four. They should not rewrite the first scientific question.

| Topic | ID | Question |
|-------|----|----------------|
| Information vs shepherds | RQ5 | Can better sensing or communication reduce the dog count at the same reliability? |
| Early warning | RQ7 | Can recent flock state warn of failure better than knowing only N and D? |
| Time as a resource | protocol `T0`/`T1` | Does a tighter or looser deadline change how many dogs you need? |
| Collapse beyond D = 35 | RQ2 upper band (extension) | If we allow more than 35 dogs, does success eventually fall, or only path waste keep rising? See [Future work](#future-work-measuring-collapse-beyond-d--35). |
| Other systems | later | Do similar patterns appear outside sheep-herding simulations? |

RQ6 (curve fitting) stays with the size question: fit only after solid frontiers exist. Regimes (too few / efficient / wasteful / overcrowding) also belong with size, not as a separate RQ.

### Scope

**In scope for the core program**

- flock size and start structure
- how much external control you need for reliable success
- scaling relationships and mechanisms
- whether results transfer across control methods
- a reproducible protocol

**Not primary goals**

- finding the single "best" herding algorithm
- copying every detail of real livestock
- optimizing one controller architecture
- claiming results for every collective system at once
- shipping a real-time failure-prediction product

Those can wait until the core scaling questions are clearer. Only claim what the evidence supports.

---

## 4. Shared protocol

| Term | Meaning |
|------|---------|
| `N` | Number of sheep |
| `D` | Number of dogs |
| `R` | Success rate: fraction of repeated runs that finish in time |
| `theta` | Reliability bar (here 0.90: succeed in at least 90% of runs) |
| `D_min` | Smallest tested D with `R >= theta` |
| Compact start | Sheep begin in a tight clump |

### Core protocol

- `task`: `drive_to_goal`: Every sheep must enter the goal disk before the deadline.
- `world_width`, `world_height`: (500, 500) - Square field large enough for wide and outlier-rich starts.
- Flock centre: (250, 250) - Field centre.
- `goal_center`: (370, 250) - Midline point 120 units right of the flock.
- `drive_length`: 120 - Fixed centre-to-centre task distance.
- `goal_radius_at_n50`: 15 - Application-scale target at N=50.
- Goal radius: `15 * sqrt (N/50)` - Keep target area per sheep constant.
- `initial_spread`: 30 - Base scale used by all layout generators.
- `measurement_radius`: 5 - Connectivity radius for fragmentation.
- `reliability_theta`: 0.90 - Primary reliable-band threshold.
- `reliability_sensitivity`: 0.5, 0.7 - Additional reported threshold, not the D_min bar.
- `baseline_method`: `strombom_multi` - Baseline collect-and-drive controller.
- `transfer_method`: baseline method, `kubo`, `fat`, `communication_free` - Full planned transfer list.
- `required_transfer_methods`: baseline method, `kubo`, `fat` - Minimum transfer claim set.
- `flock_size` grid: `{5, 10, 25, 50, 75, 100, 150, 200, 300, 400}` - Frozen N grid.
- `shepherd_counts` grid: `{1, 2, 3, 4, 6, 10, 15, 20, 25, 35}` - Frozen D grid.
- `structure_flock_sizes`: `{50, 100, 200}`.
- `rq5_flock_sizes`: `{100, 200}` - Information-ladder claim sizes.
- `X0_families`: compact, wide, split, outlier_rich - Initial layout factor.
- `time_limit_t0`: 10,000 - Main deadline, about 80 straight 120-unit crossings at speed 1.
- `time_limit_t1`: 20,000 - Long deadline only for overcrowding cells.
- `scout_seeds`: 30 - Broad-map depth.
- `master_seeds`: 2026 - Base for a shared deterministic seed list.
- `bootstrap_resamples`: 1,000 - Seed resamples for frontier uncertainty.
- `predictor_window_ticks`: 100 - Initial-state feature window, shorter than a straight drive.
- `wasteful_effort_tolerance`: 0.2 - Default excess-path bar.
- `wasteful_effort_sensitivity`: 0.1, 0.3 - Reported sensitivity bar.

#### Some reasons for the setup

These reasons were locked in the plan (field, goal, grids, layouts). They are not stories made up after seeing the results.

##### Field

We use a 500 by 500 square so wide and outlier-rich starts still fit with room to spare. A much smaller field (150) cannot hold those starts. A 400 field is tight on the wide start. A 1000 field mostly adds empty space.

The goal sits on the horizontal midline so top and bottom margins stay equal.

![Field and arena overview.](../results/summary/figures/schematics/en/arena_overview.svg)

*500 by 500 field, flock centre, midline goal, and margin for wide starts.*

The flock must travel 120 units from centre to goal. That is far enough that a tight start is not already "in" the goal, but not so far that the goal sits against the far wall.

![Compact drive geometry.](../results/summary/figures/schematics/en/arena_compact.svg)

*Centre-to-goal drive of 120 units on the midline.*

##### Radius

At N = 50 the goal radius is 15: big enough that sheep are not jammed into a tiny disk, but not so big that the task becomes trivial. We grow the radius with `sqrt(N)` so goal *area per sheep* stays roughly constant. A fixed radius would squeeze large flocks. We do **not** reuse the Strombom Collect radius as the goal size (that Collect rule is controller-specific).

![Goal radius scaling.](../results/summary/figures/schematics/en/goal_radius.svg)

*Goal radius `15 * sqrt(N/50)` keeps goal area per sheep roughly constant.*

##### Flock-size and dog-count grid

**Why these flock sizes (N):** N = 5 is the smallest size where the same collective measures still make sense. We sample more densely around N = 100, include 300 and 400 for large flocks, and skip 250 and 350 because each extra N needs a full sweep over dog counts.

**Why these dog counts (D):** fine steps at low D (where the minimum usually sits), then larger jumps to see whether "many more dogs" help or hurt. The top of the list is 35 because the central question is about a *few* shepherds. That is a grid ceiling for this study, not a physical farm limit, and not proof that overcrowding cannot appear above 35 ([Future work](#future-work-measuring-collapse-beyond-d--35)).

![Frozen N and D grids.](../results/summary/figures/schematics/en/design_nd_grids.svg)

*N denser near 100; D unit steps at low counts, then larger steps up to 35.*

![Reliability threshold theta.](../results/summary/figures/schematics/en/design_theta.svg)

*Primary bar: R >= 0.90. Sensitivity thresholds 0.50 and 0.70 are reported but do not define D_min.*

##### Methods and claim sizes

Required methods and tracks: [Why these three methods](#why-these-three-methods) and [Method tracks: transfer vs draft](#method-tracks-transfer-vs-draft).

Structure experiments use `structure_flock_sizes` and all 4 initial layouts. These sizes are large enough for split clusters and outliers to represent flock structure.

N below 12 uses only two split clusters, and tiny compact flocks are already covered by phase 1.

N = 300 and N = 400 may be added only after the 3-size claim map, mainly if every layout remains at the D_min floor.

Information experiments use `rq5_flock_sizes`. N=50 is omitted because a D_min already at one cannot decrease by a grid step.

### Initial layouts

We hold flock size fixed and change only how sheep are placed at the start:

| Layout | Picture | How we build it |
|--------|---------------|-------------------------|
| `compact` | Tight clump | Narrow Gaussian (sigma 9) |
| `wide` | Very spread out | Wide Gaussian (sigma 60) |
| `split` | Two or three separate clumps | Gaps of at least 10 units |
| `outlier_rich` | Main flock plus far stragglers | About 80% core, 20% far outliers |

Checks: compact should look tighter than wide; split should look more broken than compact; outlier_rich should show more outliers than compact. Points that land outside the field or inside the goal are redrawn (not stuck on the wall).

A connectivity radius of 5 links nearby compact neighbors but does not bridge the split gaps.

![Four initial layouts.](../results/summary/figures/schematics/en/four_layouts.svg)

*Compact, wide, split, and outlier_rich at the same N.*

### Frontier, regimes, and failure labels

**Control demand** means: how many dogs do you need so that herding succeeds often enough? We measure that mainly with the useful dog range around `D_min`, and with whether too many dogs start to hurt.

`D_min` is not a property of sheep in nature. It depends on the task, time limit, sensing, success rule, and other frozen settings.

We only test the dog counts on the frozen list (not every integer).

Success rate `R` is estimated over locked random seeds for a given method, protocol, N, D, time limit, start layout, and information setting.

| Label | Meaning |
|-------|----------------|
| `D_min` | Smallest tested dog count with `R >= 0.90` |
| `D_overcrowd` | After a good band, the first place where two steps in a row fall below 0.90 |
| `D_max` | Largest still-reliable D before overcrowding; if there is no overcrowding, this is just the top of the tested list (a ceiling) |
| `B*` | Among reliable choices, the one with the shortest median dog walking distance (ties: fewer dogs, then faster finish) |
| Hard failure | No tested D reaches 0.90 |
| Under-resourced | Too few dogs; `R` below 0.90 |
| Efficient | Reliable and path is not much above `B*` |
| Wasteful | Reliable, but dogs walk a lot more than at `B*` (default: 20% more path; we also report 10% and 30%) |
| Overcrowding | After a reliable band, success falls again when D is high |

**Waste vs overcrowding:**

- **Waste:** still succeed often, but extra dogs mostly walk more.
- **Overcrowding:** after a good winning band, success falls under 90% again for two steps in a row.

If there is no overcrowding, a reported `D_max = 35` only means "still OK at the largest D we tested," not "collapse begins at 35." Detail: [Upper frontier status](#upper-frontier-status).

![Waste versus overcrowding.](../results/summary/figures/schematics/en/overcrowd_example.svg)

*Waste: R stays at or above theta while path grows. Overcrowding: after a reliable band, R falls below theta for two consecutive tested D.*

![Frontier quantities.](../results/summary/figures/schematics/en/design_frontier.svg)

*`D_min`, reliable band, `D_overcrowd`, `D_max`, and `B*` (minimum-path reliable choice).*

![Regimes along D at fixed N.](../results/summary/figures/schematics/en/regimes.svg)

*Under-resourced, efficient, wasteful, and overcrowding regimes on the tested D grid.*

Failure labels:

- Stacking: Dogs pile on one point.
- Split: Flock stays in pieces.
- Scatter: Cohesion distances high.
- Oscillation: GCM flips, little progress.
- Stuck: GCM barely moves to goal.
- Timeout: still unfinished at T0.

![Failure-label families.](../results/summary/figures/schematics/en/design_failures.svg)

*How failed trials are labelled from flock and dog state (stacking, split, scatter, oscillation, stuck).*

![Timeout as a failure label.](../results/summary/figures/schematics/en/design_timeout.svg)

*Timeout: the run is still unfinished at T0; other labels can appear on early failure too.*

---

## 5. Campaign design

We need accurate success rates near the important edges (where `D_min` sits, and where overcrowding might start). Running *every* cell at 100 random seeds would waste budget: cells that always succeed or always fail teach little at that depth.

So we use a staged pipeline: cheap seeds everywhere first (scout), learn which cells matter, then spend expensive seeds only there (claim). The same idea is used for size, structure, transfer, and later information ladders.

![Phase roadmap.](../results/summary/figures/schematics/en/phase_roadmap.svg)

*Which phases produce claim-grade maps versus analyse-only or follow-on work.*

![Staged scout and claim pipeline.](../results/summary/figures/schematics/en/pipeline.svg)

*Smoke, scout, claim plan, claim reseed, analyse, and conditional T1.*

### Grades

| Grade | Role | Typical seeds | Cite for claims? |
|-------|------|---------------|------------------|
| SMOKE | Pipeline check (paths, resume, metrics) | tiny grid | No |
| SCOUT | Broad map; choose claim windows | 30 | No (planning / diagnostics only) |
| CLAIM | Precision on planned cells | 100 | Yes |

Do not promote a SCOUT figure to a claim verdict.

### Shared pipeline

Every simulation campaign follows the same steps:

1. Pilot (SMOKE): confirm host, paths, metrics, and resume on a small grid.
2. Scout (SCOUT): run the full (or factor) grid at 30 seeds to build a reliability map.
3. Claim plan: no new sims; write the frontier cells to reseed.
4. Claim reseed (CLAIM): run those cells at 100 seeds and merge with scout.
5. Analyse: build packages and figures from the merge.
6. T1 (when needed): claim-depth runs at `T=20,000` only on overcrowding cells.

Stop after scout if the map is broken, the grid must change, or the bootstrap interval is too wide. Fix the protocol, then continue.

![One cell and seed depth.](../results/summary/figures/schematics/en/one_cell_seeds.svg)

*A single (N, D) cell: scout depth versus claim depth.*

![Scout reliability map idea.](../results/summary/figures/schematics/en/scout_grid.svg)

*Broad 30-seed map over the N by D grid; dark or light cells show where reliability lives before precision reseeding.*

![Claim window selection.](../results/summary/figures/schematics/en/claim_window.svg)

*Reseed D_min and its neighbors; add overcrowding onset cells only when the scout shows them.*

### Claim windows and merge

After the scout map, we only reseed the cells that matter:

- Around the scout's `D_min`: that D, plus the previous and next dog counts on the list.
- If overcrowding seems to start (two steps in a row below 0.90): those two D values and the last still-reliable D.
- If nothing reaches 0.90: the two largest D values we tested.

For a cell that got claim seeds, we use only those claim rows in the analysis. Other cells keep their scout rows. We never mix scout and claim rows in the same cell. If the bootstrap interval on `D_min` is wider than one dog-count step, that window is raised to 200 seeds before a structure claim (next subsection).

### Bootstrap on `D_min` (analysis, then maybe more seeds)

Bootstrap is not a campaign phase and not 1,000 new simulations. After scout/claim rows are locked, we reshuffle those existing seeds with replacement 1,000 times, recompute `D_min` each time, and take the 2.5% and 97.5% percentiles as the interval. If a resample never clears theta, that draw stays right-censored above the tested grid. Width zero means every resample gave the same `D_min`.

The rule that follows is separate from the bootstrap itself:

1. Run bootstrap on the locked claim (or scout) seeds.
2. If the interval spans more than one dog-count step on the frozen D grid, raise that claim window to 200 real simulation seeds.
3. Bootstrap again on the new seed bag.
4. Report the point `D_min` with the new interval. More seeds can shrink noise, but they do not guarantee a one-step cliff: soft edges stay soft.

Worked case (Phase 4 Kubo): `outlier_rich`, `N=200` hit a wide interval, so those D cells were raised to 200 seeds. After the deeper bag, the point estimate is still `D_min=20` and the bootstrap interval is still `[2, 20]`. Details under [`kubo`](#kubo).

![Bootstrap on D_min, then raise to 200 seeds when the interval is wide.](../results/summary/figures/schematics/en/design_bootstrap.svg)

*Top: resample locked seeds (analysis only). Bottom: wide interval triggers new sims at 200 seeds, then bootstrap again; the interval can remain wide.*

### How each phase uses the pipeline

| Phase | RQ | What is specific | Scout asks | Claim spends seeds on |
|-------|----|------------------|------------|------------------------|
| 1 | RQ2 | Baseline size map (`strombom_multi`, compact) | Where does `R(N, D)` live on the frozen grids? | Frontiers and hard-failure cells |
| 2 | RQ1 | Four layouts at `N` in `{50, 100, 200}` | How does `X0` move `D_min` and cost? | Structure windows at those three sizes |
| 3 | RQ3 | Analyse only | (none) | Needs matched efficient vs overcrowding cells from Phases 1 or 2 |
| 4 | RQ4 | Repeat size and structure for `kubo` and `fat` | Same maps per transfer method | Same window logic per method |
| 5 | RQ5 | Three separate ladders (obs, range, comm), not a product | Does a ladder step lower `D_min`? | Windows on each ladder at `N` in `{100, 200}` |
| 6 | RQ6 | Analyse only | (none) | Needs claim-grade frontier maps |
| 7 | RQ7 | Analyse only | (none) | Needs claim-grade timeseries |

Phase-specific notes:

- Phase 1: full frozen `N` x `D` grids; T1 skipped here because no overcrowding cells appeared.
- Phase 2: structure scout and claim only; no new size grid.
- Phase 3: skipped for the baseline because Phase 1 found no overcrowding cells to contrast.
- Phase 4: size then structure, once per transfer method (`kubo`, then `fat`).
- Phase 5: observation scout/claim first, then range, then communication; low-D band as in [Information ladders](#13-information-ladders).
- Phases 6 and 7: no new simulation campaigns; they consume earlier merges (and timeseries for Phase 7).

### Trial counts by run

Counts are completed simulation trials from each protocol folder (`status.json` / `trials.csv`). Claim rows are reseed trials only, not the merged table. Analyse-only phases have no new trials. Blank cells are for runs not finished yet.

| Phase | Run | Grade | Method / focus | Trials | Status |
|-------|-----|-------|----------------|--------|--------|
| 1 | Pilot | SMOKE | `strombom_multi` | 150 | DONE |
| 1 | Scout | SCOUT | size map, compact | 3000 | DONE |
| 1 | Claim reseed | CLAIM | size frontiers | 2200 | DONE |
| 1 | T1 | CLAIM | overcrowding at `T=20,000` | 0 | SKIPPED |
| 2 | Pilot (state) | SMOKE | structure smoke | 600 | DONE |
| 2 | Scout | SCOUT | 4 layouts | 3600 | DONE |
| 2 | Claim reseed | CLAIM | structure windows | 2400 | DONE |
| 3 | Mechanism | CLAIM | Package C (analyse) | n/a | SKIPPED |
| 4 | Kubo size scout | SCOUT | `kubo` compact | 3000 | DONE |
| 4 | Kubo size claim | CLAIM | `kubo` size windows | 2100 | DONE |
| 4 | Kubo structure scout | SCOUT | `kubo` 4 layouts | 3600 | DONE |
| 4 | Kubo structure claim | CLAIM | `kubo` structure windows | 4000 | DONE |
| 4 | FAT size scout | SCOUT | `fat` compact | 3000 | DONE |
| 4 | FAT size claim | CLAIM | `fat` size windows | 2000 | DONE |
| 4 | FAT structure scout | SCOUT | `fat` 4 layouts | 3600 | DONE |
| 4 | FAT structure claim | CLAIM | `fat` structure windows | 2400 | DONE |
| 5 | Obs scout (`factor_sweep`) | SCOUT | observation ladder | 1080 | DONE |
| 5 | Obs claim | CLAIM | observation windows |  | RUNNING |
| 5 | Range scout | SCOUT | sensing-range ladder |  | TODO |
| 5 | Range claim | CLAIM | range windows |  | TODO |
| 5 | Comm scout | SCOUT | communication ladder |  | TODO |
| 5 | Comm claim | CLAIM | communication windows |  | TODO |
| 6 | Scaling fits | CLAIM | Package F (analyse) | n/a | DONE |
| 7 | Early warning | CLAIM | Package G (analyse) | n/a | TODO |

Planned Phase 5 scout sizes (for later fill-in): observation 1080 (done); range about 1440; communication about 1080. Claim trial totals depend on the planned windows after each scout.

---

## 6. Methods and results

The shared rules (field, grids, 90% bar, scout/claim staging) are defined once in [Shared protocol](#4-shared-protocol) and [Campaign design](#5-campaign-design). This section covers each controller, then its results, with a short **Meaning** under each figure.

"Farthest" differs by controller:

- **Strombom Collect:** sheep farthest from the *flock centre*
- **Kubo:** sheep farthest from the *goal* (among those the dog can sense)
- **FAT:** sheep farthest from the *dog itself*

### `strombom_multi`

Dogs first gather stragglers (Collect), then push the whole flock toward the goal (Drive). They switch using a radius that grows with flock size (`r_a * N^(2/3)`). That Collect radius is wider than the goal disk, so a Strombom failure is not read as sheep failing to pack into the goal.

![strombom_multi collect and drive.](../results/summary/figures/schematics/en/alg_strombom_multi.svg)

*Multi-dog Collect assigns outliers; Drive places dogs on an arc behind the flock toward the goal.*

**Published inspiration**

Strombom et al. (2014) describe a single shepherd that alternates between 2 actions. In Collect, it moves behind the sheep farthest from the flock center and pushes that outlier inward. In Drive, it moves behind the flock center relative to the goal and pushes the cohesive flock forward.

The switch uses:

```
f(N) = r_a * N^(2/3)
```

If any sheep is farther than `f(N)` from the global center of mass, the flock is treated as spread and the shepherd collects. Otherwise it drives. The published model also supplies the sheep attraction, repulsion, inertia, grazing, noise, and shepherd stop rules used as a basis of HerdSim's Strombom sheep.

Ref: paper

**HerdSim Implementation**

HerdSim separates sheep dynamics from the dog controller.

The named `strombom` preset combines:

- `sheep_model=strombom`;
- `dog_controller=collect_drive`;
- one shepherd by default.

The completed scaling study did not use that preset. It used `strombom_multi`, which combines the same Strombom sheep with `dog_controller=collect_drive_multi`.

**Sheep**

When every active dog is farther than `r_s`, a sheep grazes. It normally stays still and takes a random step with probability `graze_move_prob`. When a dog is within `r_s`, the sheep combines previous heading, attraction to a neighbor center, short-range sheep repulsion, repulsion from active dogs, and random noise, then moves by `sheep_speed`.

Defaults used by the method bundle include:

- `r_a = 2`: Sheep interaction length used in packing and collect threshold calculations.
- `r_s = 65`: Distance within which sheep react to a shepherd; base sensing range.
- `sheep_speed = 1.0`: Sheep displacement per tick.
- `shepherd_speed = 1.5`: Shepherd displacement per tick.
- `noise_strength = 0.3`: Strength of random angular jitter added when a sheep updates its heading. Higher values make paths wobble more; 0.3 is the Strombom-style default used in this bundle.
- `inertia = 0.5`: Weight on the sheep's previous heading when forming the new direction (the rest comes from attraction, repulsion, dog push, and noise). At 0.5, half of the update keeps the prior facing, which smooths turns.
- Collect threshold: `r_a * N^(2/3)` - Radius switch between collect and drive.

The coverage radius is `sensing_range` when an information factor sets it, otherwise the method's `r_s`. It is not the sheep-sheep repulsion distance.

**Multi-dog controller**

Under the global observations used in the completed scaling phases, each active dog sees the full flock and computes the same centroid and threshold.

In Collect:

- sheep beyond `f(N)` are sorted by distance from the centroid;
- dog `i` is assigned outlier `i mod k`, where `k` is the number of outliers;
- its base target is `r_a` behind that sheep relative to the centroid;
- a tangential offset of `2 * r_a` per slot spreads dogs that approach the same outlier.

In Drive:

- the base target is `r_a * sqrt(N)` behind the centroid relative to the goal;
- dogs are placed at equal angles on a circle of radius `4 * r_a` around that base target.

Each dog stops when it is closer than `shepherd_stop_multiple * r_a` to any sheep in its working view. The default is `shepherd_stop_multiple = 3`, so the stop distance is `3 * r_a = 6` with `r_a = 2`. Dog motion includes the Strombom angular noise.

The outlier assignment, tangential Collect spacing (`2 * r_a = 4` per slot), and Drive circle (radius `4 * r_a = 8` around the base drive target) are HerdSim additions. They are not part of the single-shepherd 2014 algorithm and are not claimed as a port of another published multi-shepherd controller.

`strombom_multi` is the baseline controller. It uses the [shared protocol](#4-shared-protocol) and [campaign design](#5-campaign-design): Phase 1 size map (compact) and Phase 2 structure map. Observation mode in the completed comparison: global. The experiment overrides the preset dog count as it sweeps `D`. It keeps the controller equations and the Strombom defaults listed above.

#### Results

**Compact size map**

At the 90% reliability threshold:

- `D_min = 2` for `N=5` and `N=10`;
- `D_min = 1` for every tested `N` from 25 through 400;
- no overcrowding; `D_max=35` is the grid ceiling (meaning: [Upper frontier status](#upper-frontier-status)).

![`strombom_multi` compact reliability heatmap.](../results/phase1/claim/packages/a/figures/reliability_heatmap.png)

*Success-rate surface R(N, D) for `strombom_multi` on compact starts only.*

Meaning: almost the whole N by D surface is at or near R = 1.00. The clear low-R band is only N = 5 and N = 10 at D = 1 (R about 0.07 and 0.24). Once D >= 2, every tested size clears theta. That is why the size story here is a floor, not a rising dog-count curve.

![`strombom_multi` frontier D_min(N).](../results/phase1/claim/packages/a/figures/frontier_dmin.png)

*`D_min` (and ceiling `D_max`) on the compact size map. No overcrowding curve appears.*

Meaning: `D_min` steps from 2 down to 1 at N = 25 and stays at 1 through N = 400. `D_max` sits on the top of the grid (35) for every N because no overcrowding pair appears. The plot is a lower frontier plus a ceiling label, not a measured upper collapse.

![`strombom_multi` cost against D.](../results/phase1/claim/packages/a/figures/cost_vs_d.png)

*Finish time stays roughly flat once runs succeed; total path grows with D.*

Meaning: median finish time is about 183 ticks (p90 about 198) and does not fall much as D grows. Total shepherd path rises with D; for N >= 25, median path per dog is about 148. Extra dogs therefore buy little time and mainly add walking: the waste pattern.

![`strombom_multi` size-map outcomes.](../results/phase1/claim/packages/a/figures/failure_modes.png)

*How trials end on the compact size claim merge (4,540 rows).*

Meaning: overall success is about 0.963 (169 failures). Failures concentrate at the two under-resourced cells: oscillation (111) and stuck (58), mainly N = 5 / N = 10 at D = 1. Successful cells dominate the rest of the map.

![`strombom_multi` regime counts.](../results/phase1/claim/packages/a/figures/regime_counts.png)

*Regime labels on the 100 size-by-dog cells.*

Meaning: 88 wasteful overspend, 10 efficient, 2 under-resourced (N = 5 and N = 10 at D = 1), 0 overcrowding. Most of the reliable band is already past `B*`: more dogs keep R high but raise path.

**Starting structure**

At `N=50, 100, 200`, all four layouts have `D_min=1`, with bootstrap width zero. Structure changed cost rather than the minimum reliable dog count:

- wide starts took about 11 to 20 times the compact completion time and about 19 to 36 times the compact path at 1 dog;
- `outlier_rich`, `N=200` took a median 1,228 ticks and path 1,647 at 1 dog;
- on wide starts, the minimum-path reliable choice `B*` was 2 dogs for all 3 tested sizes.

![`strombom_multi` layout cost at D = 1.](../results/phase2/claim/packages/b/figures/layout_cost_d1.png)

*Median total path by layout at one dog. Wide and large outlier_rich starts dominate cost.*

Meaning: compact and split sit near each other (split is not a hard contrast in these medians). Wide is the expensive start (path about 2,900 to 5,200). `outlier_rich` grows sharply with N (path about 209 at N = 50 to about 1,647 at N = 200). Structure here is a cost factor, not a `D_min` factor.

![`strombom_multi` R vs D by layout at N = 50, 100, 200.](../results/phase2/claim/packages/b/figures/layout_reliability_by_n.png)

*Success rate R(D) for each layout at the three structure sizes. Markers and a small vertical dodge separate stacked curves; true values are still R = 1.00 where noted.*

Meaning: at N = 50, 100, and 200, all four layouts (compact, split, outlier_rich, wide) have `D_min = 1` and R = 1.00 already at D = 1, and stay at or above theta through D = 35. On the raw values the four curves coincide, which is why an undodged plot looked like a single line. Layout does not open a reliability gap on the baseline at any of these sizes; the structure effect is delayed finish and longer path, not failure to hit 90%.

![Wide starts: path at D = 1 versus D = 2.](../results/summary/figures/f10_wide_bstar_path.png)

*On wide starts, `B*` = 2: the second dog cuts median path while staying reliable.*

Meaning: for wide at N = 50, 100, and 200, median total path falls from about 2,925 to 2,337, 4,319 to 3,003, and 5,213 to 3,694 when D goes from 1 to 2, with R still at or above theta. The second dog is an efficiency choice (`B*`), not a reliability rescue.

**Limitations and non-claims**

- The claim-grade baseline is HerdSim's `strombom_multi`, not the published single-shepherd algorithm without modification.
- The easy compact task produces a ceiling effect. One dog succeeds for all tested `N>=25`, so these data do not support a growing dog-count scaling law. Upper-frontier meaning (grid ceiling vs collapse): [Upper frontier status](#upper-frontier-status).
- The split layout behaved much like compact in the completed analysis (matched medians for ticks and path at D = 1). Mean fragmentation stays near 1.0, so the intended initial separation is weakly expressed in the recorded state. No strong split-layout mechanism claim is made until the generator separation is confirmed.

Compact-start frontier (baseline Phase 1 claim merge):

| N | D_min | D_max | D_overcrowd |
|---:|---:|---:|---|
| 5 | 2 | 35 (ceiling) | none |
| 10 | 2 | 35 (ceiling) | none |
| 25-400 | 1 | 35 (ceiling) | none |

Bootstrap width on every baseline D_min above is zero. Artefacts: Phase 1 claim frontier and merged trials under `scaling/results/phase1/claim/`.

### `kubo`

There is no Collect/Drive switch. Sheep and dogs move under continuous forces (push, align, pull) with local sensing and speed limits. Each dog focuses on the sheep farthest from the goal among those it can sense. Dogs also push each other apart so they do not stack on one spot.

![Kubo force-based control.](../results/summary/figures/schematics/en/alg_kubo.svg)

*Continuous forces; each dog presses the in-range sheep farthest from the goal, with dog-dog repulsion spreading the team.*

**Published inspiration**

Kubo et al. (2022) model sheep and multiple dogs through continuous force sums rather than a discrete Collect/Drive switch. Sheep combine neighbor repulsion, velocity alignment, cohesion, and dog repulsion. Each dog targets an in-range sheep farthest from the goal, while target repulsion, goal repulsion, and dog-dog repulsion shape its motion. Dog-dog repulsion can spread the team behind the flock.

Ref. paper.

**HerdSim implementation**

The `kubo` method bundle combines:

- `sheep_model=kubo`;
- `dog_controller=kubo_forces`;
- default counts of 40 sheep and 4 dogs outside experiment overrides.

It does not use Strombom sheep and has no Collect/Drive state.

**Sheep force step**

For each sheep, HerdSim finds sheep and dogs within `radius`. It computes:

- mean inverse-square sheep repulsion;
- mean unit velocity of moving neighbors;
- mean unit attraction toward neighboring sheep;
- mean inverse-cube repulsion from dogs.

The weighted velocity uses sheep gains `K_s1..K_s4` (defaults below). These are the method-bundle force gains carried from the Kubo-style continuous model; this study does not retune them per N or layout. Magnitude is clamped to `sheep_speed_max` so a single force spike cannot produce an unbounded step. Position advances by `dt * velocity` with `dt = 0.05`, so one simulation tick is a fixed integration step rather than a unit displacement as in Strombom-family sheep.

**Dog force step**

For each active dog with a nonempty observation:

- Build the observation-limited local state.
- Keep sheep inside `radius`.
- Select the in-range sheep farthest from the goal.
- Combine attraction to that target, inverse-cube repulsion from it, repulsion from the goal, and inverse-cube repulsion from other in-range dogs.
- Weight the terms with dog gains `K_f1..K_f4` (defaults below). Same rule as the sheep gains: published-style bundle defaults, not re-optimized for each cell.
- Clamp speed to `dog_speed_max` and advance by `dt * velocity`.

If the observation contains no sheep, the controller leaves that dog stationary for the tick. Sheep update before dogs in the simulation step. HerdSim also applies its scenario goal, bounded arena behavior, per-agent response and cohesion factors, and observation pipeline around these forces.

Defaults used by the method bundle:

- `radius = 60`: Local sensing radius.
- `K_s1 = 10`: Sheep-sheep repulsion gain.
- `K_s2 = 0.5`: Sheep velocity-alignment gain.
- `K_s3 = 2`: Sheep cohesion gain.
- `K_s4 = 5000`: Sheep repulsion from dogs.
- `K_f1 = 10`: Dog attraction to the target sheep.
- `K_f2 = 200`: Dog repulsion from the target sheep.
- `K_f3 = 8`: Dog repulsion from the goal.
- `K_f4 = 3000`: Dog-dog repulsion.
- `dt = 0.05`: Force-integration time step.
- `sheep_speed_max = 5`: Sheep speed clamp.
- `dog_speed_max = 10`: Dog speed clamp.

Kubo is a Phase 4 transfer method on the [shared protocol](#4-shared-protocol) size and structure maps (global observation, staged scout/claim). Method-specific precision: `outlier_rich`, `N=200`, `D` in `{1, 2, 3, 4, 6, 10, 15, 20, 25}` was raised to 200 seeds; `D=35` remained at 30 scout seeds.

The experiment overrides the preset counts with each tested `(N, D)` cell. It does not retune Kubo's force gains for each flock size or layout.

#### Results

**Compact size map**

- `D_min=3` at `N=5`; `D_min=1` from `N=10` through 400
- no overcrowding; `D_max=35` is the grid ceiling ([Upper frontier status](#upper-frontier-status))
- Overall success in the Kubo size claim merge was 0.991 (4428 successes and 42 failures in 4470 rows). Every failure has `failure_mode = timeout`; no oscillation or stuck labels appear in that merge.

![`kubo` compact reliability heatmap.](../results/phase4/kubo_size/claim/packages/a/figures/reliability_heatmap.png)

*Success-rate surface R(N, D) for `kubo` on compact starts only.*

Meaning: like the baseline, most of the compact surface is high R. The weak corner is small N at low D (N = 5 needs D_min = 3; at D = 1 and D = 2, R is about 0.77 and 0.71 before clearing at higher D). From N = 10 upward the map is already reliable at D = 1.

![`kubo` frontier D_min(N).](../results/phase4/kubo_size/claim/packages/a/figures/frontier_dmin.png)

*`D_min(N)` on compact starts; `D_max` at the grid top where no overcrowding appears.*

Meaning: after N = 5 (`D_min = 3`), the frontier sits at 1 through N = 400. No overcrowding curve is drawn: `D_max = 35` is the tested-grid ceiling for every size cell. Compact-size transfer with the baseline is shared on that lower frontier for N >= 10.

![`kubo` cost against D.](../results/phase4/kubo_size/claim/packages/a/figures/cost_vs_d.png)

*Finish time and path against dog count on the Kubo compact size map.*

Meaning: once cells are reliable, adding dogs does not create an overcrowding collapse on this map. Path still tends to grow with D while finish time stays in a successful band, matching the waste pattern used for the baseline upper frontier (Kubo ticks are not physically comparable to Strombom-family ticks).

![`kubo` size-map outcomes.](../results/phase4/kubo_size/claim/packages/a/figures/failure_modes.png)

*How trials end on the Kubo compact size claim merge (4,470 rows).*

Meaning: 42 failures, all labelled timeout; no oscillation or stuck labels in that merge. Overall success is about 0.991. Failures are rare and time-budget limited, not oscillation-dominated as on FAT.

![`kubo` regime counts.](../results/phase4/kubo_size/claim/packages/a/figures/regime_counts.png)

*Regime labels on the 100 Kubo size-by-dog cells.*

Meaning: 87 wasteful overspend, 11 efficient, 2 under-resourced, 0 overcrowding. Same qualitative mix as the baseline compact map: most reliable cells are past the useful dog count on path.

**Scaling structure**

- Compact and split: `D_min=1` at `N=50, 100, 200`
- `outlier_rich`: `D_min=1` at `N=50, 100`.
- `outlier_rich`, `N=200`: point estimate `D_min=20`.
- Wide: hard failure at all 3 sizes. Best reliability over tested dog counts is about 0.47 to 0.54, below 0.90. Failures are mainly timeout or scatter: the flock stays too spread for the local-force dogs to finish by T0. Adding dogs raises R toward about 0.5 but does not cross the 0.90 bar inside D <= 35, so the label is hard failure, not overcrowding.

![`kubo` R vs D by layout at N = 50, 100, 200.](../results/phase4/kubo_structure/claim/packages/b/figures/layout_reliability_by_n.png)

*Success rate R(D) for each layout at the three structure sizes.*

Meaning: compact and split stay above theta across D at all three N. Wide stays in a mid band (best R about 0.47 to 0.54) and never clears 0.90 at N = 50, 100, or 200, so transfer fails on spread-out starts. `outlier_rich` stays at `D_min = 1` for N = 50 and 100, then only clears theta at high D when N = 200 (see next figures). Compact `D_min` sharing with the baseline therefore does not extend to every layout.

![`kubo` layout cost at D = 1.](../results/phase4/kubo_structure/claim/packages/b/figures/layout_cost_d1.png)

*Median path (and related cost) by layout at one dog.*

Meaning: where R is already high at D = 1 (compact / split), cost is the secondary contrast. Wide and large `outlier_rich` are the expensive or unreliable starts; for wide, cost at D = 1 is not a success story because those cells never reach theta at any tested D.

For `outlier_rich`, `N=200`, the shared raise-to-200 rule applied ([Bootstrap on D_min](#bootstrap-on-d_min-analysis-then-maybe-more-seeds)): those D cells were reseeded at 200 simulation seeds, then bootstrap was run again on that deeper bag. The 200-seed cells gave `R=0.935` at `D=20` and `R=0.910` at `D=25`. The bootstrap interval for `D_min` is still `[2, 20]`: several D below 20 have R near theta, so resamples can pull the estimate downward even when the full-depth point estimate is 20. Report `D_min = 20` with `[2, 20]`. Deeper seeding did not collapse the soft edge to a one-step cliff.

![Kubo outlier_rich, N = 200.](../results/summary/figures/f9_kubo_outlier_rich_n200.png)

*R(D) with Wilson 95% intervals. Point D_min = 20 clears theta; after 200 seeds the bootstrap lower edge remains [2, 20].*

Meaning: R climbs through the teens and first clears 0.90 at D = 20 (R = 0.935), then stays above at D = 25 (0.910) and D = 35 (0.967 at scout depth 30). Several lower D sit near the bar, which is why the bootstrap interval stays wide even at 200 seeds. Treat `D_min = 20` as a point estimate with that uncertainty, not a sharp cliff.

**Limitations and non-claims**

- Shared compact `D_min` does not imply full transfer. Kubo failed the 90% criterion on every wide cell and shifted sharply at `outlier_rich`, `N=200`.
- The `[2, 20]` bootstrap interval makes the `D_min=20` boundary uncertain on its lower side.
- Hard failure on wide means no tested `D <= 35` reached the reliability threshold. It is not evidence that more dogs always make Kubo worse.
- Kubo ticks are not physically comparable with Strombom-family ticks because Kubo uses `dt` integration.
- HerdSim's bounded arena, spawn geometry, goal disk, and experiment counts are study choices, not claims about the paper's exact setup.

### `fat`

Sheep still use the Strombom sheep model, but dogs have a simpler rule. Each dog looks at the sheep it can see, picks the one farthest from itself, and stands behind that sheep toward the goal. Dogs do not switch Collect/Drive, and they do not actively space themselves apart.

![FAT farthest-agent targeting.](../results/summary/figures/schematics/en/alg_fat.svg)

*Each dog independently presses the observed sheep farthest from itself; no Collect/Drive switch and no dog-dog spacing rule.*

**Published inspiration**

FAT is inspired by the local-camera shepherding rule discussed by Tsunoda et al. (2018): act on the farthest agent in the herder's visible set without requiring global flock coordinates.

HerdSim does not implement that paper's complete camera model, positional-error treatment, sheep dynamics, navigation law, or experimental calibration. The published contribution is therefore inspiration for target selection, not a claim of full model reproduction.

Ref paper.

**HerdSim implementation**

The `fat` method bundle combines:

- `sheep_model=strombom`
- `dog_controller=fat`
- 2 dogs by default outside experiment overrides.

Sheep therefore use HerdSim's Strombom grazing, flocking, repulsion, and fixed-displacement update. The dog controller has no Collect/Drive switch and no flock-cohesion test.

For each active dog on each tick:

- Read that dog's observation after observation-mode and sensing filters.
- If no sheep are visible, leave the dog stationary.
- Choose the observed sheep farthest from the dog itself.
- Place a target `r_a` behind that sheep on the ray from the goal through the sheep.
- Move toward that target at `shepherd_speed`, with Strombom angular noise.
- Stop if any sheep in the dog's working view is closer than `shepherd_stop_multiple * r_a`.

Each dog makes this choice independently. FAT has no dog-dog repulsion, assignment negotiation, or explicit spacing. "Farthest" means farthest from the dog, which differs from Strombom Collect (farthest from the flock center) and Kubo (farthest from the goal).

**Experiment scope**

FAT is a Phase 4 transfer method on the [shared protocol](#4-shared-protocol) size and structure maps (global observation, staged scout/claim). No coordination is added by the FAT controller.

The global observation setting is important. Although the target-selection idea is motivated by local sensing, completed Phase 1, 2 and 4 gave each FAT dog the full flock view. Those results do not test the local-camera information limit. Observation-mode experiments were planned for Phase 5 ([Information ladders](#13-information-ladders)).

**Results**

**Compact size map**

- `D_min=1` at `N=5` and `N=10`.
- For every tested `N>=25`, no dog count through 35 reached `R >= 0.90`.
- The latter cells are hard failures: `D_min` and `D_max` are undefined, not zero and not 35.
- Best reliability by size for `N=50` through 400 was about 0.40 to 0.53.
- About half of FAT size trials failed. The summary attributes about 39% of all trials to oscillation failures and 7% to stuck failures.

![`fat` compact reliability heatmap.](../results/phase4/fat_size/claim/packages/a/figures/reliability_heatmap.png)

*Success-rate surface R(N, D) for `fat` on compact starts only.*

Meaning: only the smallest flocks show a high-R band (N = 5 and N = 10 reach theta at D = 1). For N >= 25 the surface stays below 0.90 across the whole D grid; best R by size for N = 50 through 400 is about 0.40 to 0.53, with some cells as low as about 0.17. Adding dogs does not paint a reliable band on this compact map.

![`fat` frontier D_min(N).](../results/phase4/fat_size/claim/packages/a/figures/frontier_dmin.png)

*Where no D reaches theta, `D_min` is undefined (hard failure), not zero.*

Meaning: `D_min = 1` only at N = 5 and N = 10. For every larger N the frontier is empty (hard failure): there is no `D_min` and no `D_max` to plot as a collapse. That is the opposite of the baseline/Kubo compact floor.

![`fat` cost against D.](../results/phase4/fat_size/claim/packages/a/figures/cost_vs_d.png)

*Finish time and path against dog count on the FAT compact size map.*

Meaning: cost curves on hard-failure sizes are not an efficiency story. Many runs never succeed, so path and time describe failed or mixed cells rather than a wasteful reliable band. Do not read rising path here as the same "waste after D_min" pattern used for Strombom and Kubo.

![`fat` size-map outcomes.](../results/phase4/fat_size/claim/packages/a/figures/failure_modes.png)

*How trials end on the FAT compact size claim merge (4,400 rows).*

Meaning: 2,206 failures (about half of trials). Labels are mostly oscillation (1,707; about 39% of all trials), then stuck (295; about 7%), then timeout (204). Failure mode is not "ran out of time only"; oscillation dominates.

![`fat` regime counts.](../results/phase4/fat_size/claim/packages/a/figures/regime_counts.png)

*Regime labels on the 100 FAT size-by-dog cells.*

Meaning: 80 hard failure, 17 wasteful overspend, 3 efficient, 0 overcrowding. The map is dominated by cells that never reach theta, not by a long reliable waste band.

**Starting structure**

FAT did not reach 90% reliability in any structure cell at `N=50, 100, 200`.

- Compact best `R`: 0.47, 0.40, 0.47 for `N=50, 100, 200`.
- Split best `R`: 0.50, 0.47, 0.40.
- `outlier_rich` best `R`: 0.10, 0.00, 0.00.
- Wide best `R`: 0.00 at all three sizes.

![`fat` R vs D by layout at N = 50, 100, 200.](../results/phase4/fat_structure/claim/packages/b/figures/layout_reliability_by_n.png)

*Success rate R(D) for each layout at the three structure sizes.*

Meaning: at N = 50, 100, and 200, every layout stays below theta for all tested D. Compact/split best R is about 0.40 to 0.50; `outlier_rich` and wide stay near 0 (especially at larger N). Structure does not rescue FAT here; the size-map hard failure continues across starts and sizes.

![`fat` layout cost at D = 1.](../results/phase4/fat_structure/claim/packages/b/figures/layout_cost_d1.png)

*Path (and related cost) by layout at one dog.*

Meaning: with R far below theta, these costs are mainly failed or unreliable runs. Layout ranking is secondary to the fact that no structure cell at these sizes clears the reliability bar.

The completed summary also reports a strong negative association between FAT trial interference and success on the size merge, with Pearson `r` about `-0.87`. This is observational. It does not establish interference as the cause of failure.

![`fat` interference against D.](../results/phase4/fat_size/claim/packages/a/figures/interference_vs_d.png)

*Median mean I_dir on the FAT compact size map. Pearson r(I_dir, success) on that merge is about -0.87 (observational only).*

Meaning: FAT mean I_dir is much higher than baseline or Kubo on the size maps (about 0.40 overall at N = 100 versus about 0.05 and 0.10). The plot tracks interference against D; the association with failure is correlational only, so it is a candidate signature for later mechanism work, not a completed RQ3 contrast.

**Limitations and non-claims**

- This is a minimal HerdSim FAT controller on Strombom sheep, not the full Tsunoda et al. model.
- The completed results use global observations. They do not measure camera occlusion bearing-only control, position error, or lost-track recovery.
- Hard failure means no tested count reached the study's 90% bar before `T0`. It does not prove FAT can never work at larger `D`, under another timeout, or on another task.
- Increasing dog count did not rescue larger flocks on this grid. That observation does not isolate a causal mechanism.
- The interference correlation is not a controlled causal test.

---

## 7. Findings synthesis

What we can claim so far comes from Phases 1, 2, and 4: baseline size and structure, plus Kubo and FAT size and structure. Phase 5 (information) is in progress and not claimed here. Phase 3 (mechanism) was skipped because we never saw overcrowding on the baseline. Phase 7 (early warning) has not been run.

### At a glance

![Five main results at a glance.](../results/summary/figures/schematics/en/summary_at_a_glance.svg)

| Verdict | Finding | Key numbers |
|----------|----------------|-------------|
| Lower frontier (`D_min`) | On the baseline with a tight start, one dog is enough from 25 to 400 sheep. | Tiny flocks N = 5 and 10 need 2 dogs. At one dog their success rates are only about 0.07 and 0.24. |
| Upper frontier (more dogs) | Adding dogs past the minimum does not break success on that map; it mostly adds walking. `D_max = 35` is "top of our list," not a measured collapse. | 88 of 100 cells are wasteful; 0 overcrowding. Typical finish about 183 ticks; path per dog about 148 for N >= 25. |
| Structure is cost, not dog count | Messy starts make the run slower and longer, but still succeed with one dog on the baseline. | Wide starts take about 11x to 20x more time and 19x to 36x more path than compact at 1 dog. For wide, the cheapest reliable choice is 2 dogs (`B* = 2`). |
| Partial transfer | Kubo and FAT do not copy the baseline story everywhere. | Kubo looks like baseline on tight starts, but fails on wide starts (best R about 0.47 to 0.54). FAT hits 90% only for N <= 10. |
| Draft not reproduced | The draft's "large flocks need many dogs" pattern does not show up on this compact baseline map. | Draft: about 20 to 35 dogs for large N. Here: one dog finishes N = 400 in roughly 168 to 183 ticks. |

### Contrast with the 2025 draft

![Draft versus this HerdSim protocol.](../results/summary/figures/schematics/en/draft_vs_herdsim.svg)

*Same broad question and 90% bar; different task, arena, and controller family. This is a contrast, not a matched replication.*

Smallest reliable dog count (`D_min`) on compact starts at the 90% bar:

| N | Baseline (`strombom_multi`) | Kubo | FAT | 2025 draft |
|---:|---:|---:|---:|---:|
| 5 | 2 | 3 | 1 | 1 |
| 10 | 2 | 1 | 1 | 1 |
| 25 | 1 | 1 | none <= 35 | 1 |
| 50 | 1 | 1 | none <= 35 | 1 |
| 100 | 1 | 1 | none <= 35 | 1 |
| 150 | 1 | 1 | none <= 35 | 3 |
| 200 | 1 | 1 | none <= 35 | 20 |
| 300 | 1 | 1 | none <= 35 | 20 |
| 400 | 1 | 1 | none <= 35 | 35 |

`none <= 35` means: no dog count we tested reached 90% success. On *this* protocol, the draft's "large N needs many dogs" story does not appear on the baseline compact size map.

### Baseline cost and regimes

Headline numbers are in [At a glance](#at-a-glance). Per-method plots are in [Methods and results](#6-methods-and-results). The figure below only compares frontiers across methods (and the draft):

![D_min against N, with 2025 draft contrast.](../results/summary/figures/f2_dmin_vs_n.png)

*Baseline and Kubo stay near one dog for large compact flocks; the draft rises sharply. FAT has no D_min for N >= 25.*

### Upper frontier status

RQ2 also asks: if you *already* have enough dogs, does adding more still help, do nothing useful, or start to hurt? (Definitions: [Frontier, regimes, and failure labels](#frontier-regimes-and-failure-labels).) Inside our list through D = 35:

| Method | Compact `D_min` | Overcrowding? | What `D_max` means here | Do extra dogs hurt success? |
|--------|----------------:|---------------|-------------------------|-----------------------------|
| `strombom_multi` | 2 at N=5,10; else 1 | no | 35 = top of tested list | No: success stays high; extra dogs mainly walk more (waste) |
| `kubo` | 3 at N=5; else 1 | no | 35 = top of tested list | No on compact. Structure is different (wide fails; large outlier_rich needs many dogs) |
| `fat` | 1 only for N=5,10; undefined for N>=25 | no | undefined when nothing reaches 90% | Not an overcrowding story: large N never reaches 90% at any tested D |

So `D_max = 35` means "still OK at the largest D we tried," **not** "collapse begins at 35." Claim codes C2a / C2b and RQ3 status: [Answers to research questions](#8-answers-to-research-questions) and [Claims](#11-claims).

### Future work: measuring collapse beyond D = 35

Not run. This extension would allow more than 35 dogs and test whether success eventually falls (a real upper collapse), or whether path waste keeps rising without collapse.

| Question | Why it matters | How we would run it |
|----------------|------------|---------------------|
| After a good band, does success fall for some D > 35? | Turns "ceiling" into a measured collapse point | Extend the dog-count list past 35 on selected N |
| If success stays high, does path waste keep rising? | Shows a waste-only upper band even with many dogs | Same extended sweep; report path and regimes |
| Does a longer deadline (T1) rescue high-D failures at T0? | Separates "too slow" from "true overcrowding" | T1 only on candidate overcrowding cells |
| Do efficient and overcrowding cells differ in interference or splitting? | Unlocks RQ3 | Matched tests at the same N |
| Does that upper story transfer across methods? | RQ4 for the upper band | Repeat under Kubo / FAT (later `communication_free`) |

Another path without raising the dog cap: port the draft-style harder task and see whether overcrowding appears inside D <= 35 ([If we rerun a draft-style method](#if-we-rerun-a-draft-style-method)). Status: not scheduled; no claim-grade D > 35 cells in this report.

---

## 8. Answers to research questions

One table for all research questions. Details and figures stay in the method sections; formal claim codes are in [Claims](#11-claims).

| RQ | Question | Status | Answer in this study |
|----|----------------|--------|-------------------|
| RQ1 | At the same flock size, does start shape change how many dogs you need? | Answered on baseline | No for dog count: all four layouts still need only 1 dog at N = 50, 100, 200. Shape changes time and walking, not `D_min`. (C1a rejected; C1b inconclusive.) |
| RQ2 | As N grows, how does the useful dog range change? | Answered inside D <= 35 | Lower: from N = 25 up, baseline compact needs 1 dog. Upper: extra dogs waste path; no overcrowding; `D_max = 35` is a list ceiling ([Upper frontier](#upper-frontier-status)). We did not test D > 35 ([Future work](#future-work-measuring-collapse-beyond-d--35)). |
| RQ3 | Why do efficient vs overcrowding cells differ? | Not answerable yet | We never saw overcrowding on the baseline size map, so the planned contrast does not exist. |
| RQ4 | Do the patterns transfer to Kubo and FAT? | Partial | On tight starts, Strombom and Kubo share `D_min = 1` for N >= 25; FAT does not. Wide starts break Kubo; FAT fails the 90% bar on structure cells. |
| RQ5 | Can better information reduce dog count? | Not yet | Observation / range / communication ladders are not claim-complete. |
| RQ6 | Which curve predicts held-out N? | Weak | A two-level step fits best, only because `D_min` is almost flat ({2, then 1}). Not a rich scaling law. |
| RQ7 | Can recent state warn of failure better than N and D? | Not yet | Early-warning package not run. |

RQ5 to RQ7 and a draft-style HerdSim rerun would tighten the same story; they do not change what the program is for ([central question](#does-this-answer-the-central-question)).

---

## 9. Cross-method transfer

Same grids and layouts. For each feature we ask: does it look like the baseline, shift, or disappear?

### Compact size map

| Case | What we see |
|------|-------------|
| Shared | Strombom and Kubo both need only 1 dog for N >= 25 (Kubo needs 3 at N = 5, then 1 from N = 10). |
| Absent (FAT) | For every N >= 25, FAT never reaches 90% success with any D <= 35. Best R is about 0.40 to 0.53. |
| Ceiling, not collapse | Strombom and Kubo: no overcrowding on compact starts; `D_max = 35` is the list ceiling ([Upper frontier](#upper-frontier-status)). |

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

Meaning: sharing `D_min = 1` on compact starts does **not** mean full transfer. Wide starts and large outlier-rich starts show method dependence. FAT clears no structure cell at these sizes. Kubo `outlier_rich`, N = 200 detail (point `D_min = 20`, bootstrap `[2, 20]`) is under [`kubo`](#kubo).

![Transfer sketch.](../results/summary/figures/schematics/en/transfer_sketch.svg)

![Cross-method layout reliability curves.](../results/summary/figures/f5_layout_reliability_curves.png)

*Side-by-side success curves at N = 200 across methods and layouts. Per-method structure plots are in each method section above.*

---

## 10. Scaling fits

After we have `D_min` for each flock size, RQ6 asks which simple formula best predicts a left-out N.

On the baseline compact map, `D_min` is almost only two values: 2 for N = 5 and 10, and 1 for everything larger. Error below is leave-one-N-out RMSE (lower is better):

| Model | RMSE | Meaning |
|-------|-----:|---------------|
| Constant | 0.44 | Pretend one flat dog count |
| Linear | 0.44 | Straight line in N |
| Power law | 0.25 | Smooth curve on log-log axes |
| Piecewise | 0.13 | Two levels with a break near N = 10 |

The piecewise model wins because it matches that step, not because we measured a rich growth law. We cannot test "slope below 1 on a growth band" (C6b): there is no rising `D_min` band to fit. These fits are not a universal scaling law.

![Leave-one-N-out RMSE by model.](../results/summary/figures/f8_scaling_rmse.svg)

---

## 11. Claims

Verdicts use claim-grade evidence only. Labels:

- **SUPPORTED**: the stated condition holds inside this protocol
- **REJECTED**: we looked and it does not hold
- **INCONCLUSIVE**: we cannot decide (often the needed contrast is missing)
- **SKIPPED**: the trigger to run the test never appeared
- **UNEVALUATED**: not run yet

![Claims scorecard.](../results/summary/figures/schematics/en/claims_scorecard.svg)

*Visual summary of claim verdicts. Detail in the table below.*

| Claim | RQ | Verdict | Evidence meaning |
|-------|----|---------|------------------|
| C1a | RQ1 | REJECTED | Baseline structure: `D_min=1` for all four layouts at N in `{50, 100, 200}`; bootstrap width 0. |
| C1b | RQ1 | INCONCLUSIVE | No baseline `D_min` shift across layouts, so state-vs-(N, D) predictor superiority is not evaluable. Cost still depends strongly on layout. |
| C2a | RQ2 | REJECTED | Baseline size map: 0 overcrowding cells at theta 0.90. |
| C2b | RQ2 | SKIPPED | No overcrowding cell to extend to T=20,000. |
| C3 | RQ3 | INCONCLUSIVE | Baseline mechanism contrast undefined without overcrowding cells. |
| C4 | RQ4 | SUPPORTED (partial) | Strombom and Kubo share compact `D_min` for N >= 25; FAT absent for N >= 25; Kubo wide absent; Kubo `outlier_rich`, N=200 shifts to point `D_min=20` with bootstrap `[2, 20]`. |
| C5a | RQ5 | UNEVALUATED | Information ladders not claim-complete. |
| C5b | RQ5 | UNEVALUATED | Information ladders not claim-complete. |
| C6a | RQ6 | EVALUATED (weak) | Piecewise RMSE 0.13 beats power-law RMSE 0.25; only two observed `D_min` levels. |
| C6b | RQ6 | UNEVALUATED | No stated growth band (baseline `D_min` does not rise with N). |
| C7a | RQ7 | UNEVALUATED | Early-warning analysis not run. |
| C7b | RQ7 | UNEVALUATED | Early-warning analysis not run. |

These checks only support statements inside the tested protocol. They do not support a universal law, an untested task, real-farm performance, or a dog-count difference smaller than one step on our D list.

---

## 12. Limits and threats

Limits of what this report can say:

| Limit | How we treat it |
|-------|-----------------|
| One simulated task | Results are for `drive_to_goal` under the frozen protocol only. |
| Method dependence | We check transfer (RQ4) before general claims; transfer is only partial. |
| Start shape can confuse size | We match N and use fixed layouts; on baseline, `D_min` did not move with layout. |
| Discrete dog-count list | We cannot resolve effects finer than one step on that list. |
| Soft reliability edges | Locked seeds, claim windows, bootstrap; raise to 200 seeds when uncertainty is wide. |
| Conditional analyses | If the trigger never appears, we mark skipped/inconclusive (not "proven null"). |
| Time across methods | Do not treat Kubo ticks as the same physical time as Strombom-family ticks. |
| Collect switch wider than the goal | Do not read a Strombom failure as "sheep could not pack into the goal." |
| Simulated controllers | No farm or biology validity claim. |
| Grid ceiling | `D_max = 35` is the top of our list, not a measured collapse ([Upper frontier](#upper-frontier-status); [Future work](#future-work-measuring-collapse-beyond-d--35)). |
| Easy compact map | Many baseline cells succeed at D = 1 with R near 1.00, so rising dog-count laws are hard to see. |
| Split layout | Behaves like compact so far; the generator's separation still needs a hard check. |
| Interference correlation | FAT `I_dir` link to failure is observational, not a controlled cause test. |

---

## 13. Information ladders

Status: **not claim-complete**. Observation scout is done; observation claim was still running when this section was written. Range and communication ladders are not finished. Do not treat Phase 5 figures as final claims yet.

RQ5 asks whether better sensing can replace some dogs while keeping the same reliability. We test three separate ladders (not every combination at once):

- **Observation content:** bearing only → local positions → global view
- **Sensing range:** about 0.5×, 1×, 1.5×, 2× Strombom's usual sense radius
- **Communication:** no sharing → share with neighbors → share the union of what any dog senses

For `strombom_multi`, "global shared" still only includes sheep that *some* dog currently senses. It is not a free look at the whole simulator. Sheep outside every sensor stay unseen.

Scout runs for Phase 5 use low dog counts `{1, 2, 3, 4, 6, 10}` because that is where saving even one dog would show up.

---

## 14. Outcomes and state metrics

What we record on each run:

- **Success:** did every sheep reach the goal in time? (yes/no)
- **Finish time (`t_s`):** first tick when that happens
- **Dog path:** total distance all dogs walked; also path per dog
- **Cohesion:** how tightly sheep sit around the flock centre
- **Fragmentation:** size of the largest connected sheep group, divided by N
- **Outliers / spread / extent / hull size / density / aspect ratio:** other shape summaries of the flock
- **`I_dir` (interference):** near 0 if dogs move the same way; near 1 if their headings cancel (push against each other)
- **Coverage:** fraction of outer sheep that sit within dog influence range

Technical notes: if no dog moves, `I_dir = 0`. Velocities include wall effects. Missing coverage radius yields NaN.

![Tick and path cost metrics.](../results/summary/figures/schematics/en/metrics_tick_path.svg)

![Reliability R.](../results/summary/figures/schematics/en/metrics_reliability.svg)

![Interference I_dir.](../results/summary/figures/schematics/en/metrics_idir.svg)

---

## 15. Prediction and early warning

Status: **not run**. No accuracy or lead-time numbers yet.

RQ7 asks whether recent flock and dog state can warn that a run is about to fail, better than a baseline that knows only flock size and dog count.

Planned setup: at time t, use only the last 200 ticks of state (no peeking into the future). Ask whether a failure happens in the next 500 ticks. Sweep many times t during the run. Compare against a simple baseline that knows only N and D. Package G has not been run, so nothing is claimed here.

---

## 16. Commands run

Commands used for the completed and queued campaigns (from the repo root; set `WORKERS` to match the host):

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
# then claim-reseed; repeat TRANSFER_METHOD=fat
make -C scaling scaling-transfer-structure-scout TRANSFER_METHOD=kubo WORKERS=16
# then claim-reseed; repeat TRANSFER_METHOD=fat
make -C scaling scaling-analyse PACKAGE=D TRIALS=... --trials-by-method ...
make -C scaling scaling-factor-sweep WORKERS=18
make -C scaling scaling-phase5-obs-claim-reseed WORKERS=18
# then range and communication scout/claim
# Phase 7 (Package G) not run yet
```
