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

That is the same basic problem as the draft sheep-scaling paper (dog count vs flock size, and whether spread helps explain difficulty). This report keeps that problem, but tries to be more careful:

- say clearly what "how much control" means,
- separate size from shape / state,
- ask why a pattern shows up, not only that it does,
- check whether it still shows up under a different herding method.

We are not starting from a claimed universal scaling law. We start from questions we can actually run.

HerdSim is the experimental platform for that program: a few dogs (or shepherds) guide a larger flock to a goal under conditions you can control and repeat. For this study it is a model system for measuring control demand, not an attempt to copy real farms in full.

Herding is a good fit because control is indirect:

> A small number of external controllers tries to steer a larger group whose members are not commanded one by one.

The point of the platform is fairness and comparison. You can pick a method setup (how the sheep move plus how the dogs decide), put it in a scenario, fix a random seed, and measure what happens with shared metrics. That way you can see when herding works, when it fails, and how methods compare when flock size, sensing, and other settings are held fair.

HerdSim has 2 goals on one shared engine:

a. **Simulation + frontend**: interactive UI - Simulate, Compare, Experiments, NetLogo, Guide.
b. **Scaling**: CLI protocols that answer the scaling/control-demand research questions.

### Methods

A method is a ready-made sheep plus dog package with paper-style defaults.

Here are the methods currently in the platform:

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

This study focuses on three methods: `strombom_multi` (baseline), `kubo`, and `fat`.
Controller detail and results are in [Methods and results](#6-methods-and-results).

#### Why these three methods

The frozen plan locks a baseline and a minimum transfer set for RQ4 (repeat size and structure maps under more than one herding method, then compare):

| Method | Role in the plan | What it is in HerdSim (documented contrast) |
|--------|------------------|-----------------------------------------------|
| `strombom_multi` | Baseline | Multi-dog Collect/Drive on Strombom sheep (coordinated gather then drive) |
| `kubo` | Required transfer | Continuous force model; no Collect/Drive switch; dogs press the sensed sheep farthest from the goal |
| `fat` | Required transfer | Farthest-from-self targeting on Strombom sheep; no Collect/Drive switch; no dog-dog spacing |

Reason for that set: RQ4 needs controller change on one frozen task (`drive_to_goal`), not three near-copies of Collect/Drive. The three entries above are the locked minimum claim set. `communication_free` is the recommended next transfer method, outside that minimum. Other catalogue presets are available in the platform but are not part of the current transfer claim unless a later decision adds them.

What a shared vs broken pattern means: if the same `D_min` / regime story appears in all three, the pattern is not only a baseline quirk; if it fails for Kubo or FAT, that bounds how far we can generalise. That is the RQ4 meaning, not a claim that these three exhaust all herding methods.

#### Method tracks: transfer vs draft

Two different experiment purposes, same broad control-demand question:

| Track | What the plan changes | Why that track exists | Linked RQs |
|-------|----------------------|------------------------|------------|
| Same-protocol transfer (`strombom_multi`, `kubo`, `fat`; next: `communication_free`) | Dog/sheep rules only; task and grids stay frozen | Answer RQ4: which patterns survive a controller change | RQ1 to RQ4 now; RQ5 to RQ7 follow-on |
| Draft-style method / protocol (HerdSim port) | Task, arena, starts, and often the controller family (collect, hold, gate) | Credibility / task sensitivity: the 2025 draft used a different hard task; planned as a HerdSim rerun, not done yet | Same central question; not a substitute for RQ4 |

The draft method is therefore under [Prior draft paper](#2-prior-draft-paper), not a fourth row in the required transfer set. Choosing `drive_to_goal` as the main task is the frozen HerdSim protocol choice for fair method comparison. It is not a claim that the draft task is wrong, and "easy compact floor" is a measured outcome under that protocol, not the reason the task was chosen.

#### Does this answer the central question?

"How much control" here means the viable shepherd range (`D_min`, waste vs overcrowding / `D_max`) under a frozen reliability bar and deadline. RQ2 / RQ6 cover size; RQ1 structure; RQ3 mechanism when overcrowding contrasts exist; RQ4 method transfer; RQ5 and RQ7 follow-on.

The program answers by bounding the question inside this protocol: where dog need is stable, where cost rises without `D_min` rising, where transfer fails, and later whether information or early state can substitute for dogs. Completed findings and per-RQ answers are in [Findings synthesis](#7-findings-synthesis) and [Answers to research questions](#8-answers-to-research-questions). This study does not claim a universal farm law, that the draft's rising `D_min` is wrong on its own task, or that every method needs one dog within D <= 35.

---

## 2. Prior draft paper

The 2025 draft paper "Collective Nudging that Scales".

- Question: How many dogs do I need to herd sheep?
- NetLogo: 7.0.3 on a patch grid.
- Task: Collect, hold for 800 ticks, then exit through a gate.
- Success: All sheep pass through the gate by 10,000 ticks.
- Arena: 101 x 71 patches, central containment zone, right-wall gate.
- Containment or goal: `rc = clamp (2.5 * sqrt (N), 23, 27)`
- Sheep start: Random scatter with wall and dog buffers.
- Dog start: Top-left corner grid.
- Control scope: One NetLogo collect, drive, and patrol family.
- D grid: `{1, 2, 3, 4, 6, 10, 15, 20, 25, 35}`.
- N grid: `{5, 10, 25, 50, 100, 150, 200, 250, 300, 350, 400}`.
- Sampling: 100 runs in every cell, 11,000 total.
- Seed definition: Master seed not stated in the note.
- Reliability: SR >= 90%.
- D_min: Smallest D with SR >= 90%.
- D_overcrowd: First D above D_min where SR starts decreasing.
- D_max: First D above D_min with SR >= 90%, otherwise ceiling.
- Structure: Emergent spread summarized by `S_bar`.
- Metrics: Success, ticks, phase, spread, path and lost sheep.

![2025 draft task phases.](../results/summary/figures/schematics/en/draft_task_phases.svg)

*Draft task: collect, hold, then exit through a gate (NetLogo patch arena).*

![2025 draft experiment design.](../results/summary/figures/schematics/en/draft_experiment_design.svg)

*Draft design sketch: containment zone, gate, and run budgets.*

### Result of the paper

At SR >= 90%, draft Table A3 reports:

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

Here "not reach" means the upper failure boundary was not found by D = 35.

It also reports a negative association between mean spread and success, including Spearman `rho = -0.701` for `S_bar` against SR and `rho = -0.828` for `S_bar * N` against SR over 110 condition aggregates.

![2025 draft main results sketch.](../results/summary/figures/schematics/en/draft_main_results.svg)

*Draft Table A3 pattern: D_min stays low at small N, then rises sharply for large flocks.*

### If we rerun a draft-style method

The draft method was not rerun here. The planned rerun is in HerdSim: bring the draft collect / hold / gate task and controller family into HerdSim (not a NetLogo rerun). The point is to ask the same control-demand questions on that task, together with the planned RQs, not to treat the draft as one more controller on `drive_to_goal`.

| Question the draft rerun would ask | Planned RQ it answers with |
|------------------------------------|----------------------------|
| As flock size grows on the collect-hold-gate task, how does the viable dog range change (`D_min`, and whether more dogs help, plateau, or hurt)? | RQ2 (size and regimes), and RQ6 once frontiers exist |
| At fixed N on that task, does start shape or hold-phase state change how many dogs we need? | RQ1 (structure), using draft-style state such as spread / `S_bar` where relevant |
| If overcrowding cells appear, which mechanisms separate efficient from overcrowding runs? | RQ3 (mechanism), only when those contrasts exist |
| On a frozen draft-style task, which patterns still hold when we change only the controller? | RQ4 (transfer), after the draft task is frozen first |
| On that task, can richer information lower `D_min` at fixed reliability? | RQ5 (information ladders) |
| On that task, can recent state warn of failure better than N and D alone? | RQ7 (early warning) |

Together: the planned RQs stay the program's questions; the HerdSim draft-style rerun asks them again under that task and method. Track placement: [Method tracks: transfer vs draft](#method-tracks-transfer-vs-draft).

---

## 3. Research questions

The program asks how much external control is needed to guide a collective reliably as flock size and initial structure change, which processes explain that demand, and which patterns transfer across shepherding methods.

For each core question below: what we want to know, how we study it, and what kinds of answers would count. We are not locking in a preferred outcome ahead of time.

### What we want from the program

After the core runs, we should be able to say something concrete about how control need changes with group size, whether shape / state matters beyond size, which processes drive the pattern, and what looks shared across methods versus method-specific. A simple predictive rule would be useful; strong method dependence would also be useful, because it bounds how far we can generalise. Relative to a single-method scaling study, that means defining control demand in a reusable way, separating size from structure, testing mechanisms instead of stopping at correlation, and checking which features survive a method change.

### Core questions

#### Size and operating regimes (RQ2, with fits in RQ6)

**Question.** As flock size grows, how does the viable shepherd range change: the minimum needed for reliable herding, and the point where adding more stops helping or starts hurting? RQ6 asks which planned curve best predicts held-out N, and whether a single power law is adequate.

**Approach.** Freeze the protocol. Vary `N`, keep other settings as fixed as we can. For each `N`, find the smallest `D` that hits the reliability target, and note whether larger `D` still helps, plateaus, or hurts. Only fit scaling models once we have real frontiers.

**Possible results.** Linear, sublinear, or superlinear growth; different behaviour in different size bands; saturation or thresholds; or nothing simple. We also care about operating regimes (too few / efficient / wasteful / overcrowding).

#### Structure (RQ1)

**Question.** At the same flock size, does flock shape/state (spread, fragmentation, outliers, etc.) change how much control we need? In the claim form: does `D_min` change across initial layout at fixed N?

**Approach.** Hold `N` fixed in matched comparisons. Change initial structure on purpose. Measure a few structural properties and see how much of the leftover variation size alone cannot explain.

**Possible results.** Size is almost enough; one or a few structure measures pick up the rest; or different properties matter at different sizes.

#### Mechanism (RQ3)

**Question.** Why does that pattern appear (for example interference, coverage limits, fragmentation)? Which prespecified mechanism signatures distinguish efficient and overcrowding cells at the same N?

**Approach.** Candidates include spatial demand, fragmentation, controller interference, redundant control, and local instability. Log run-level quantities tied to those ideas, see which track control demand, and intervene when we can. Correlation by itself is not treated as causation.

**Possible results.** One main mechanism; several mechanisms in different regimes; or a pattern that does not reduce to one clean story.

#### Generality across methods (RQ4)

**Question.** Which frontier, regime, and structure patterns transfer across the three required methods?

**Approach.** Rerun the core size and structure experiments under more than one method. Compare scaling shape and regime labels, not only raw success rates. Mark what looks shared vs method-specific.

**Possible results.** Fully method-specific scaling; same shape with different magnitude; or same shape with method-dependent thresholds and slopes. Strong method dependence would limit how far we can talk about "scaling" apart from the controller.

### Follow-on questions

These sit after the core four. They should not rewrite the first scientific question.

| Topic | ID | Question in brief |
|-------|----|-------------------|
| Information vs shepherds | RQ5 | Can richer observation, sensing range, or communication lower `D_min` at fixed reliability? |
| Early warning | RQ7 | Can recent state predict a later failure better than N and D alone? |
| Time as a resource | protocol `T0`/`T1` | How does a tighter or looser time limit change control demand? |
| Collapse beyond D = 35 | RQ2 upper band (extension) | Does reliability fall for D > 35, or only path waste continue? See [Future work: measuring collapse beyond D = 35](#future-work-measuring-collapse-beyond-d--35). |
| Other systems | later | Do similar patterns appear outside sheep-herding simulations? |

RQ6 (scaling fits) stays with the size question above: fit curves only after claim-grade frontiers exist. Operating regimes (too few / efficient / wasteful / overcrowding) belong with the size question, not a separate RQ.

### Scope

**In scope for the core program**

- collective size and structure
- external control demand and viable shepherd range
- scaling relationships and mechanisms
- generality across control methods
- reproducible protocol

**Not primary goals**

- finding the single best herding algorithm
- reproducing every detail of real livestock behaviour
- optimizing one controller architecture
- claiming results for every collective system out of the gate
- shipping a real-time failure-prediction product

Those can wait until the core scaling questions are clearer. Only claim what the evidence supports.

---

## 4. Shared protocol

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

These are the locked protocol reasons (field size, goal, grids, layouts), not post-hoc stories from the results.

##### Field

The square 500 field accommodates a wide three-sigma draw with reach 180 and the approximate N = 400 outlier reach of 174 while leaving about 70 units of margin.

A 150 field cannot contain those starts, a 400 field leaves only about 20 units on the wide draw, and a 1000 field adds unused space.

The midline goal keeps vertical margin equal.

![Field and arena overview.](../results/summary/figures/schematics/en/arena_overview.svg)

*500 by 500 field, flock centre, midline goal, and margin for wide starts.*

The 120-unit drive is outside the compact start and past one wide sigma even at the large goal; 80 would sit inside the wide cloud, while 200 would put the far goal edge on the wall.

![Compact drive geometry.](../results/summary/figures/schematics/en/arena_compact.svg)

*Centre-to-goal drive of 120 units on the midline.*

##### Radius

At N=50 the radius is 15, matching the application goal and exceeding the approximate packed radius of 8. A radius of 8 risks jamming and 30 makes the target much easier. Square-root scaling keeps goal area per sheep constant.

A fixed radius would jam large flocks. The Strombom collect switch `r_a * N^(2/3)` is controller-specific and is not used as the goal radius.

![Goal radius scaling.](../results/summary/figures/schematics/en/goal_radius.svg)

*Goal radius `15 * sqrt(N/50)` keeps goal area per sheep roughly constant.*

##### Flock-size and dog-count grid

Why these N values: N=5 is the floor because smaller groups do not support the same collective quantities. The grid is denser near 100, includes 300 and 400 for large-N behavior, and omits 250 and 350 because every extra N requires a complete dog-count sweep.

Why these D values: unit steps cover the likely low-D frontier; larger steps test whether large additions help or hurt. The cap of 35 matches the program's "few shepherds" scope (central question). It is a tested-grid ceiling for that scope, not a physical or farm limit, and not a claim that overcrowding cannot appear above 35 ([Future work: measuring collapse beyond D = 35](#future-work-measuring-collapse-beyond-d--35)).

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

| Layout         | Construction                                                                           | Validation gate                                      |
|----------------|----------------------------------------------------------------------------------------|------------------------------------------------------|
| `compact`      | Gaussian with sigma `0.3 * initial_spread = 9`                                         | Lower cohesion distance than `wide`                  |
| `wide`         | Gaussian with sigma `2.0 * initial_spread = 60`                                        | Higher cohesion distance than `compact`              |
| `split`        | Two clusters below N=12, otherwise three; gap at least `2 * measurement_radius = 10` | Lower largest-component fraction than `compact`      |
| `outlier_rich` | Core about 80%; about 20% beyond `r_a * N^(2/3)`                                       | Higher outlier count than `compact`                  |

- Compact sigma 9 approximates a packed N = 50 flock.
- Wide sigma 60 creates a clear cohesion contrast while fitting the field. A sigma of 120 would not fit.
- Split avoids 3 implausibly tiny subflocks below N=12.
- 20% outliers creates a real minority without becoming a second flock. Points outside the field or inside the goal are redrawn, not clipped to a boundary.

The measurement radius is 5. It links compact neighbors normally separated by about 2 to 4 units, but does not bridge split gaps of at least 10.

![Four initial layouts.](../results/summary/figures/schematics/en/four_layouts.svg)

*Compact, wide, split, and outlier_rich at the same N.*

### Frontier, regimes, and failure labels

Control demand is how much external control is needed for a chosen reliability. The primary measure is the viable shepherd range around `D_min` and overcrowding. `D_min` is not a universal property of a flock: it depends on task, time limit, information, success rule, and other fixed settings.

Dog counts come from the frozen `shepherd_counts` grid (not every integer).

Let `R(m, tau, N, D, T, X0, I)` be the probability of success estimated over locked seeds for method `m`, protocol `tau`, flock size `N`, shepherd count `D`, deadline `T`, layout `X0`, and information condition `I`.

- `D_min`: Smallest tested D with `R >= theta`.
- `D_overcrowd`: Smallest D after `D_min` for which that D and the next tested D are both below theta.
- `D_max`: Largest reliable D below `D_overcrowd`; without overcrowding, the largest tested reliable D, which can only be a grid ceiling.
- `B*`: Reliable `(D, T)` with minimum median shepherd path; ties use smaller D, then faster median success time.
- Hard failure: No tested D reaches theta.
- Under-resourced failure: `R < theta` below `D_overcrowd`.
- Efficient operation: `R >= theta` and median path is below the wasteful threshold.
- Wasteful overspend: `R >= theta` and median path is at least 20% above `B*`; also report 10% and 30%.
- Overcrowding collapse: `R < theta` at or above `D_overcrowd`.

Waste: R stays at or above theta while path grows. Overcrowding: after a reliable band, R falls below theta for two consecutive tested D. Without overcrowding, reported `D_max` at the grid top is a ceiling only (empirical meaning: [Upper frontier status](#upper-frontier-status)).

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

Claim-grade maps need precise success rates near frontiers (`D_min`, overcrowding). Running every cell at 100 seeds wastes budget: interior cells that always succeed or always fail teach little at that depth. The staged pipeline spends cheap seeds everywhere, learns which cells matter, then spends expensive seeds only on those cells. The same pattern applies to size, structure, transfer, and information ladders. One flat 100-seed full grid would buy little extra science on obvious cells and burn the budget before later phases.

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

For each method, layout, and N (or each factor level in a ladder), the claim planner selects:

- Reliability window: scout `D_min`, plus the previous and next grid `D`.
- Overcrowding window (only if two consecutive `D` after that candidate stay below theta): those two `D` and the last `D` still at or above theta.
- If no `D` reaches theta: the two largest tested `D`.

On a cell that received claim seeds, analysis uses those claim rows only. Other cells keep scout rows. Scout and claim rows are not stacked on the same cell. If the bootstrap CI on `D_min` spans more than one grid step, raise that window to 200 seeds before the structure claim.

![Bootstrap on D_min.](../results/summary/figures/schematics/en/design_bootstrap.svg)

Bootstrap resamples the locked seed list within each D (1,000 resamples). For each resample, recompute success rates and the resulting D_min on the tested grid. The reported interval is the spread of those resampled D_min values. If that interval spans more than one grid step, raise the claim window to 200 seeds before using the cell in a structure claim. Undefined D_min draws (no D reaches theta) stay right-censored above the tested grid.

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

Shared grids, reliability, deadlines, and staging are defined once in [Shared protocol](#4-shared-protocol) and [Campaign design](#5-campaign-design). This section covers controller detail, method-specific run notes, and results. Each method keeps its own controller schematic and result plots (no shared three-panel repeats here).

"Farthest" differs by controller: Strombom Collect uses farthest from the flock centre; Kubo uses farthest from the goal among in-range sheep; FAT uses farthest from the dog among observed sheep.

### `strombom_multi`

`strombom_multi` is a coordinated collect-and-drive controller. Its collect switch is `r_a * N^(2/3)`. This switch is wider than the goal, so a Strombom failure is not interpreted as a packing failure.

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

`kubo` uses continuous force terms, local sensing, `dt` integration, and speed clamps. It has no collect-and-drive switch. Dogs press the sensed sheep farthest from the goal, and dog-dog repulsion spreads them.

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

For `outlier_rich`, `N=200`, the 200-seed cells gave `R=0.935` at `D=20` and `R=0.910` at `D=25`. The bootstrap interval for `D_min` is `[2, 20]`: several D below 20 have R near theta, so resamples can pull the estimate downward even when the full-depth point estimate is 20. Report `D_min = 20` with `[2, 20]`.

![Kubo outlier_rich, N = 200.](../results/summary/figures/f9_kubo_outlier_rich_n200.png)

*R(D) with Wilson 95% intervals. Point D_min = 20 clears theta; the bootstrap lower edge remains uncertain.*

Meaning: R climbs through the teens and first clears 0.90 at D = 20 (R = 0.935), then stays above at D = 25 (0.910) and D = 35 (0.967 at scout depth 30). Several lower D sit near the bar, which is why the bootstrap interval is wide. Treat `D_min = 20` as a point estimate with that uncertainty, not a sharp cliff.

**Limitations and non-claims**

- Shared compact `D_min` does not imply full transfer. Kubo failed the 90% criterion on every wide cell and shifted sharply at `outlier_rich`, `N=200`.
- The `[2, 20]` bootstrap interval makes the `D_min=20` boundary uncertain on its lower side.
- Hard failure on wide means no tested `D <= 35` reached the reliability threshold. It is not evidence that more dogs always make Kubo worse.
- Kubo ticks are not physically comparable with Strombom-family ticks because Kubo uses `dt` integration.
- HerdSim's bounded arena, spawn geometry, goal disk, and experiment counts are study choices, not claims about the paper's exact setup.

### `fat`

`fat` retains the Strombom sheep model. Each dog independently selects the observed sheep farthest from itself and stands off behind that sheep toward the goal.

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

Claim-grade evidence below covers Phases 1, 2, and 4 (baseline size and structure; Kubo and FAT size and structure). Phase 5 is in progress and not claimed here. Phases 3 and 7 are not claimed (Phase 3 skipped for lack of overcrowding contrast; Phase 7 not run).

### At a glance

![Five main results at a glance.](../results/summary/figures/schematics/en/summary_at_a_glance.svg)

| Verdict | Finding | Key numbers |
|---------|---------|-------------|
| Lower frontier (`D_min`) | On baseline `strombom_multi` with compact starts, flocks from 25 to 400 sheep succeed reliably with one dog. | N=5 and N=10 need `D_min=2`. At one dog, R is about 0.07 and 0.24 for those two sizes. |
| Upper frontier (more dogs) | Extra dogs waste path; no overcrowding on the baseline compact map (`D_max=35` = grid ceiling). Detail: [Upper frontier status](#upper-frontier-status). | 88 of 100 cells wasteful; 0 overcrowding. Typical finish about 183 ticks; path per dog about 148 for N >= 25. |
| Structure is cost, not `D_min` | Baseline start shape changes time and path, but not `D_min`, at N in `{50, 100, 200}`. | Wide starts take about 11x to 20x more time and 19x to 36x more path than compact at 1 dog. For wide, `B*=2`. |
| Partial transfer | Kubo and FAT do not transfer evenly from baseline. | Kubo roughly matches baseline on compact starts but hard-fails wide (best R about 0.47 to 0.54). FAT reaches R >= 0.90 only for N <= 10. |
| Draft not reproduced | The steep rise in dog need reported by the 2025 draft does not appear on this compact baseline map. | Draft: about 20 to 35 dogs for large N. Here: one dog finishes N=400 with typical finish near 168 to 183 ticks. |

### Contrast with the 2025 draft

![Draft versus this HerdSim protocol.](../results/summary/figures/schematics/en/draft_vs_herdsim.svg)

*Same broad question and 90% bar; different task, arena, and controller family. Not a matched replication.*

Compact-start `D_min` at theta 0.90:

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

`none <= 35` means no tested dog count reached R >= 0.90. On this protocol, the draft's large-N rise in required dogs does not appear on the baseline compact size map.

### Baseline cost and regimes

Headline numbers are in [At a glance](#at-a-glance). Per-method reliability, cost, frontier, and regime plots are in [Methods and results](#6-methods-and-results). The figure below is the cross-method frontier contrast only:

![D_min against N, with 2025 draft contrast.](../results/summary/figures/f2_dmin_vs_n.png)

*Baseline and Kubo stay near one dog for large compact flocks; the draft rises sharply. FAT has no D_min for N >= 25.*

### Upper frontier status

RQ2 asks whether larger D still helps, plateaus, or starts to hurt (regime definitions: [Frontier, regimes, and failure labels](#frontier-regimes-and-failure-labels)). Inside the frozen grid through D = 35:

| Method | Compact size: `D_min` | `D_overcrowd` | `D_max` meaning | Does adding more dogs hurt reliability? |
|--------|----------------------:|--------------:|-----------------|-----------------------------------------|
| `strombom_multi` | 2 at N=5,10; else 1 | none | 35 = tested-grid ceiling | No: R stays high; extra dogs mainly add path (waste). |
| `kubo` | 3 at N=5; else 1 | none | 35 = tested-grid ceiling | No on compact. Structure differs (wide hard-fails; large outlier_rich shifts). |
| `fat` | 1 only for N=5,10; undefined for N>=25 | none | undefined when hard failure | Not overcrowding: large-N cells never reach theta at any tested D. |

`D_max = 35` means still reliable at the largest tested D, not that collapse begins at 35. Headline counts are in [At a glance](#at-a-glance). Claim verdicts C2a / C2b and RQ3 status are in [Answers to research questions](#8-answers-to-research-questions) and [Claims](#11-claims).

### Future work: measuring collapse beyond D = 35

Not run. Extend the RQ2 upper band past the few-shepherd cap to find a measured `D_overcrowd` / `D_max` if one exists (the protocol capped D at 35 on purpose; this does not rule out overcrowding for all D).

| Question | Why it matters | How it would be answered |
|----------|----------------|--------------------------|
| Does R fall below theta for some D > 35 after a reliable band? | Turns ceiling into a real `D_overcrowd` / measured `D_max` | Extend `shepherd_counts` past 35 on selected N; same theta and T0 |
| If R stays high as D grows, does path waste keep rising without collapse? | Waste-only upper band outside the few-shepherd range | Same extended D sweep; report path and regimes |
| Does T1 rescue high-D cells that fail at T0? | Separates slow success from true overcrowding | T1 only on candidate overcrowding cells |
| Do efficient vs overcrowding cells differ in interference or fragmentation? | Unlocks RQ3 | Matched within-N tests (Package C) |
| Does the upper story transfer across methods? | RQ4 for the upper band | Repeat under `kubo` / `fat` (later `communication_free`) |

Without raising the D cap, a draft-style harder task could create overcrowding inside D <= 35 ([If we rerun a draft-style method](#if-we-rerun-a-draft-style-method)). Status: not scheduled; no claim-grade D > 35 cells here.

---

## 8. Answers to research questions

This section answers each RQ in one place. Detail and figures stay in the method and claims sections; claims criteria are in [Claims](#11-claims).

| RQ | Question (short) | Status | Answer in this study |
|----|------------------|--------|----------------------|
| RQ1 | Does `D_min` change across initial layout at fixed N? | Answered (baseline) | No on baseline: `D_min=1` for all four layouts at N in `{50, 100, 200}`. Structure changes cost (time and path), not the minimum reliable dog count. C1a rejected; C1b inconclusive. |
| RQ2 | How do the reliable frontier and regimes change with N? | Answered inside D <= 35 (baseline; transfer partial) | Lower: `D_min=1` for N>=25 on baseline compact. Upper: waste, not overcrowding; `D_max=35` is a grid ceiling ([Upper frontier status](#upper-frontier-status)). Collapse for D > 35 not tested ([Future work](#future-work-measuring-collapse-beyond-d--35)). C2a rejected; C2b skipped. |
| RQ3 | Which mechanisms distinguish efficient vs overcrowding cells? | Not answerable yet | No overcrowding cells on the baseline size map, so the prespecified contrast is undefined. C3 inconclusive. |
| RQ4 | Which patterns transfer across `strombom_multi`, `kubo`, `fat`? | Answered (partial) | Compact `D_min` for N>=25 is shared by Strombom and Kubo, not by FAT. Wide and large outlier-rich starts break transfer for Kubo; FAT fails the 90% bar on structure cells. C4 supported only partially. |
| RQ5 | Can richer information lower `D_min` at fixed reliability? | Not yet | Observation / range / communication ladders are not claim-complete. C5a/C5b unevaluated. |
| RQ6 | Which curve predicts held-out N; is one power law enough? | Weak answer | Piecewise (two-level) RMSE beats power law, but only because observed `D_min` is almost flat ({2,1}). Not evidence for a rich scaling law. C6a evaluated weak; C6b unevaluated. |
| RQ7 | Can recent state warn of failure better than N and D? | Not yet | Package G not run. C7a/C7b unevaluated. |

Unanswered RQ5 to RQ7 and a draft-style task rerun would tighten the same bounds; they do not change the program's purpose ([Does this answer the central question?](#does-this-answer-the-central-question)).

---

## 9. Cross-method transfer

Same grids and layouts; label each frontier feature shared, shifted, or absent relative to the baseline.

### Compact size map

| Case | Empirical meaning |
|------|-------------------|
| Shared | Strombom and Kubo both reach `D_min=1` for N >= 25 (Kubo needs 3 at N=5, then 1 from N=10). |
| Absent (FAT) | For every tested N >= 25, FAT has no D <= 35 with R >= 0.90 (`D_min` / `D_max` undefined). Best R by size is about 0.40 to 0.53. |
| Ceiling, not collapse | Strombom and Kubo: no overcrowding on compact starts; `D_max=35` is the grid ceiling ([Upper frontier status](#upper-frontier-status)). |

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

`none` means no D <= 35 reaches R = 0.90.

Meaning: compact `D_min` sharing does not imply full transfer. Wide and large outlier-rich starts expose method dependence; FAT clears no structure cell at these sizes. Kubo `outlier_rich`, N=200 detail (point `D_min=20`, bootstrap `[2, 20]`) is under [`kubo`](#kubo).

![Transfer sketch.](../results/summary/figures/schematics/en/transfer_sketch.svg)

![Cross-method layout reliability curves.](../results/summary/figures/f5_layout_reliability_curves.png)

*Side-by-side R(D) at N = 200 across methods and layouts. Per-method structure plots are in each method section above.*

---

## 10. Scaling fits

Leave-one-N-out RMSE on the baseline compact frontier (`D_min` levels only 2 for N in `{5, 10}` and 1 for N >= 25):

| Model | Leave-one-N-out RMSE | Meaning |
|-------|---------------------:|---------|
| Constant | 0.44 | One flat `D_min` |
| Linear | 0.44 | Straight line in N |
| Power law | 0.25 | Smooth log-log curve |
| Piecewise | 0.13 | Two levels with a break near N=10 |

The piecewise model wins because it encodes the observed step, not because a rich growth law was measured. C6b (log-log slope below 1 on a stated growth band) cannot be tested here: there is no growing `D_min` band to fit. These fits are not a claim of a universal scaling law.

![Leave-one-N-out RMSE by model.](../results/summary/figures/f8_scaling_rmse.svg)

---

## 11. Claims

Verdicts use claim-grade evidence only. Criteria: supported when the stated condition holds inside this protocol; otherwise rejected, inconclusive, skipped (trigger absent), or unevaluated.

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

These criteria support statements inside the tested protocol only. They do not support a universal law, an untested task, field performance, or a dog-count gap below one grid step.

---

## 12. Limits and threats

| Threat or boundary | Response in this report |
|--------------------|-------------------------|
| One simulated task | Conclusions limited to `drive_to_goal` under the frozen protocol. |
| Method dependence | RQ4 before method-general statements; transfer is partial. |
| Layout and state confounding | Matched N and prespecified layouts; baseline `D_min` did not move. |
| Discrete D grid | Effects in local grid steps; unresolved below one step. |
| Soft reliability frontier | Locked seeds, claim windows, bootstrap; raise to 200 seeds when the interval spans more than one step. |
| Conditional analyses | Absent-trigger work is skipped or inconclusive, not a measured null at an unrun condition. |
| Time across methods | Avoid treating Kubo ticks as physically comparable to Strombom-family ticks. |
| Collect switch wider than the goal | Do not read Strombom failure as packing failure. |
| Simulated controllers | No field, farm, or biological-validity claim. |
| Grid ceiling | `D_max=35` is a tested-grid ceiling, not a measured collapse ([Upper frontier status](#upper-frontier-status); [Future work](#future-work-measuring-collapse-beyond-d--35)). |
| Ceiling effect on easy compact | R near 1.00 at D=1 on many baseline cells limits visible dog-count scaling. |
| Split layout | Behaves like compact in completed analysis; generator separation still needs confirmation. |
| Observational interference | FAT `I_dir` association is not a controlled causal test. |

---

## 13. Information ladders

Status: not claim-complete. Observation scout is done; observation claim was running when this section was written. Range and communication scout/claim are not finished. Do not treat any Phase 5 figure as a claim verdict yet.

- `obs_mode`: `bearing_only`, `local_positions`, `global` - Increasing observation content.
- `sensing_range`: 32.5, 65, 97.5, 130 - 0.5, 1.5, and 2 times Strombom `r_s`.
- `communication`: `none`, `neighbour_broadcast`, `global_shared` - Own observation, neighbour union, or globally shared sensed union.

For `strombom_multi`, `global_shared` means each dog may act on the union of sheep that any communicating dog currently senses. It is still filtered by sensing range and observation mode. It is not a free look at the full simulator state: sheep outside every dog's sensor remain unseen.

Phase 5 scout protocols use D in `{1, 2, 3, 4, 6, 10}` because this low-D band is where a one-step saving can appear.

---

## 14. Outcomes and state metrics

- Success: Binary indicator that all sheep enter the goal by the deadline.
- `t_s` or finish time: First tick at which success is met.
- `shepherd_path`: Sum of Euclidean step lengths of all dogs, in arena units.
- Path per dog: `shepherd_path/D`
- Cohesion: Mean sheep distance to the flock centre of mass.
- Fragmentation: Largest connected-component size divided by N, using radius 5.
- Outlier count: Sheep beyond `r_a * N^(2/3)`.
- Spread: Variance of sheep distances to the centroid.
- Extent: Root-mean-square distance to the centroid.
- Perimeter: Convex-hull perimeter.
- Hull area: Convex-hull area.
- Flock density: N divided by hull area; zero for degenerate area.
- Aspect ratio: Fit a 2D principal-component ellipse to sheep positions. The ratio of the major-axis length to the minor-axis length is 1 for a round flock and larger when the flock is elongated.
- `I_dir`: Directional interference among dogs. Take each active dog with speed above `1e-6`, form its unit velocity, sum those units, and set `I_dir = 1 - ||sum|| / M_active`. Near 0 means dogs move in a common direction; near 1 means headings cancel (pushing against each other).
- Coverage C: Fraction of peripheral sheep, those above median GCM distance, within the influence radius.

If no dog moves, `I_dir = 0`. It uses realized velocities, so constraints such as wall reflections are included. Missing coverage radius produces NaN.

![Tick and path cost metrics.](../results/summary/figures/schematics/en/metrics_tick_path.svg)

![Reliability R.](../results/summary/figures/schematics/en/metrics_reliability.svg)

![Interference I_dir.](../results/summary/figures/schematics/en/metrics_idir.svg)

---

## 15. Prediction and early warning

Status: not run. No AUROC or lead-time claim yet.

RQ7 uses horizon `k=500`, feature window `w=200`, and evaluation ticks 1000 through 8000 in steps of 200. Features use only `(t - 200, t]`.

At each evaluation tick t, the predictor may use only flock and dog state from the open window `(t - w, t]` with `w = 200`. It must not peek at future ticks. The label is whether a failure occurs within the next `k = 500` ticks. Evaluation sweeps t from 1000 to 8000 in steps of 200 so early transient and late timeout regimes are both sampled. The planned test is whether these recent-state features beat a baseline that knows only N and D (held-out AUROC and lead time). Package G has not been run yet, so no AUROC or lead-time numbers are claimed here.

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
