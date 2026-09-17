# HerdSim Research Program

## Scaling of Collective Control

This document is a research plan for a multi-stage program. It is not a claim that one final law already exists, and it is not a single-paper checklist.

The plan is meant to do two jobs:

1. State the scientific problem in clear questions.
2. Guide what HerdSim should implement so those questions can be tested fairly.

---

# 0. The Problem in Plain Language

Imagine a large group that moves together: sheep, robots, drones, or people. Often we do not control every member of the group. Instead, a few outside agents try to guide the whole group. In sheep herding, those outside agents are dogs. In other settings they might be robots, drones, or human operators.

The basic practical question is simple:

> If the group gets larger, or more spread out, how many guides do I need to finish the task reliably?

A draft study already looked at one version of this question for sheep and dogs in simulation. It asked how the number of dogs should grow with flock size, and whether flock "spread" helps explain the difficulty.

That draft is a useful starting point. This program keeps the same problem, but treats it more carefully:

* define "how much control is needed" in a clear and reusable way,
* separate group size from group shape,
* ask why the pattern appears,
* and check whether the pattern still holds when the guiding method changes.

We do not start by claiming a universal scaling law. We start by asking questions that experiments can answer.

### What we hope to achieve

By the end of the core program, we want to be able to say, with evidence:

* how control need changes as the group grows,
* whether the shape of the group matters beyond size,
* which processes help explain that pattern,
* and which parts of the pattern look shared across guiding methods, versus method-specific.

If a simple predictive rule appears, that is a strong success. If the pattern turns out to depend heavily on the method, that is also a useful scientific result.

---

# 1. Scientific Goal

HerdSim studies how much external control is needed to reliably steer a collective system.

Central question:

> How does the amount of control needed to reliably steer a collective scale with the size and structure of the collective?

Follow-up question:

> Which parts of this scaling remain consistent when the control method changes?

HerdSim uses herding as a controlled model system. The main goal is not to invent the best herding algorithm. The main goal is to understand how group size and group structure shape control demand.

A longer-term hope is that the relationship can be described by simple, testable scaling rules. That hope is an outcome to test, not an assumption.

---

# 2. Terms Used in This Plan

These terms are used throughout the document.

### Collective

A group of many individuals that interact and move together. In HerdSim, the collective is usually a flock of sheep.

### Controller / shepherd / dog

An external agent that tries to guide the collective. The individuals in the collective are not commanded one by one. The controllers influence them indirectly.

### Task

What success means in an experiment. Example: gather the flock and move it into a goal region within a time limit.

### Reliability

How often the task succeeds across repeated runs. Example: succeed in at least 90% of trials under the same conditions.

### Control demand

How much external control is needed to reach a chosen reliability. In this plan, the main measure of control demand is the minimum number of controllers.

### `N`

Number of individuals in the collective. Example: number of sheep.

### `D`

Number of external controllers. Example: number of dogs.

### `D_min`

The smallest number of controllers that still meets the reliability target, under fixed experimental conditions.

Important: `D_min` is not a universal property of a flock. It depends on the task, time limit, information available to the controllers, success rule, and other fixed settings.

### Structure (`X`)

The spatial organization of the collective, not only how many members it has. Examples:

* spread: how widely members are distributed,
* density: how tightly packed they are,
* fragmentation: whether the group is one piece or several separated pieces,
* elongation: whether the group is long and thin rather than round,
* clustering: whether members form local clumps,
* outliers: whether some individuals are far from the rest.

### Scaling

How a quantity changes when the system gets larger or changes in structure. Here, scaling mainly means how `D_min` changes when `N` or `X` changes.

### Control method / instrument

The specific rules used by the controllers (and, when relevant, by the flock). In HerdSim, a named method package is called an instrument.

### Model system

A simplified setting that is useful for studying a broader question. Sheep herding is used here as a model of indirect collective control, not as a full replica of real farms.

### Mechanism

A process that helps explain why a scaling pattern appears. Example: a fragmented flock may need more controllers because several subgroups must be handled at once.

### Generality / transfer

Whether a finding still holds when something important changes, especially when the control method changes.

### Protocol

The fixed rules of an experiment: task, success rule, reliability target, time budget, information setting, and how `D_min` is measured.

---

# 3. Central Concept

Consider a collective with `N` individuals and `D` external controllers.

For a fixed protocol, define:

`D_min(N, X)`

as the smallest number of controllers needed to reach the chosen reliability, where `X` describes collective structure.

The research begins with size only:

`D_min(N)`

and then asks whether structure is also needed:

`D_min(N, X)`.

We do not assume the mathematical form in advance. A power-law form such as

`D_min ∝ N^α`

is one possible outcome. Other possibilities include linear growth, slower-than-linear growth, faster-than-linear growth, different regions at different sizes, saturation, thresholds, or no simple pattern.

The goal is to discover and test how control demand changes with size and structure, not to force one formula.

---

# 4. What Scaling Means Here

Scaling, in this plan, means answering questions such as:

* If the group doubles in size, how many more controllers are needed?
* Does a compact group need less control than a dispersed group of the same size?
* Does fragmentation create extra control demand?
* Does adding controllers eventually stop helping, or even start hurting?
* Does the same pattern appear when a different control method is used?

So scaling is more than fitting one exponent. It is about identifying what drives control demand and what remains stable.

---

# 5. Why Structure Matters

Two groups can have the same size and still be very different to control.

One group may be compact and connected. Another may be spread out, elongated, broken into pieces, or full of outliers. Those differences change how hard the controllers must work.

Basic question:

> Is group size enough to explain control demand, or does group structure add important information?

We will not assume in advance which structural properties matter. Experiments will show which measurable properties explain systematic changes in control demand.

---

# 6. Core Research Questions

Each question below has three parts:

* Question: what we want to know,
* Approach: how we will study it,
* Possible results: what we may find.

We do not pre-commit to one preferred result.

---

## RQ1 -- How does control demand scale with collective size?

### Question

> How does the minimum control required for reliable steering change as the collective becomes larger?

### Approach

1. Freeze a protocol: task, success rule, reliability target, time budget, and information setting.
2. Vary collective size `N` while keeping other conditions as constant as possible.
3. For each `N`, find the smallest controller count `D_min(N)` that meets the reliability target.
4. Also record what happens when more controllers are added: improvement, saturation, or interference.

### Possible results

* roughly linear growth of control demand with size,
* slower-than-linear growth,
* faster-than-linear growth,
* different behavior in different size ranges,
* saturation or thresholds,
* or no simple relationship.

A useful outcome is a clear empirical map of `D_min(N)`, including breakpoints and diminishing returns. Any fitted relationship should also be checked on sizes not used to estimate it.

---

## RQ2 -- How does collective structure change control demand?

### Question

> At the same collective size, how does internal structure affect the amount of control required?

### Approach

1. Keep `N` fixed in matched comparisons.
2. Vary structure `X` in a controlled way when possible.
3. Measure candidate structural properties such as spread, density, fragmentation, elongation, clustering, and outliers.
4. Compare how much of the variation in control demand is explained by size alone versus size plus structure.

This extends the study from:

`D_min(N)`

to:

`D_min(N, X)`.

### Possible results

* size is almost enough, and structure adds little,
* one or a few structural measures explain most remaining variation,
* or different structural properties matter in different size ranges.

A useful outcome is evidence for whether control demand is mainly a size effect or a size-plus-structure effect.

---

## RQ3 -- What produces the observed scaling?

### Question

> What mechanisms help explain the observed relationship between collective structure and control demand?

### Approach

Candidate mechanisms include:

* Spatial demand: larger or more dispersed groups need influence over a wider area.
* Fragmentation: separated subgroups may need to be handled at the same time.
* Controller interference: extra controllers may conflict with each other.
* Redundant control: after enough control is present, extra controllers add little benefit.
* Local instability: some configurations are hard to recover once they start failing.

These are hypotheses to test, not assumptions.

Working method:

1. Measure run-level quantities linked to these ideas.
2. Check which quantities track control demand.
3. Where possible, intervene on the suspected mechanism and test whether control demand or the scaling pattern changes.

Correlation alone is not treated as proof of causation.

### Possible results

* one dominant mechanism explains most of the pattern,
* several mechanisms matter in different regimes,
* or the pattern remains hard to reduce to one simple mechanism.

A useful outcome is a tested explanation of why `D_min` rises, saturates, or breaks down, not only a curve fit.

---

## RQ4 -- Which parts of the scaling generalize across control methods?

### Question

> Does the relationship between collective properties and control demand remain similar when the control method changes?

### Approach

For each control method `m`, measure:

`D_min,m(N, X)`.

1. Repeat the core size and structure experiments with more than one method.
2. Compare the shape of the scaling, not only raw success rates.
3. Separate features that look shared from features that look method-specific.

The point is not mainly to crown a best algorithm. The point is to learn which findings look like properties of the collective, and which depend on the controller.

### Possible results

* Method-specific scaling: different methods give different relationships.
* Shared form with different magnitude: similar pattern, but different absolute control need.
* Shared form with method-dependent details: similar pattern, but different thresholds or slopes.

Any of these outcomes is scientifically useful. Strong method dependence would show a limit on how far scaling can be separated from the controller.

---

# 7. Control Boundaries and Diminishing Returns

As controller count increases, performance may pass through several regions:

1. too little control: the task often fails,
2. useful extra control: reliability rises strongly,
3. diminishing returns: extra controllers help little,
4. possible overcrowding: too many controllers interfere and can hurt performance.

These regions are not separate research goals. They are features that may appear while we study how `N`, `X`, and `D` relate. We will look for them in the data rather than assume their exact shape in advance.

---

# 8. Extensions After the Core Program

These topics come later. They should not redefine the first scientific question.

### Information

Can better sensing or communication reduce the number of physical controllers needed?

Written as: `D_min(N, X, I)`.

### Time

How does a tighter or looser time limit change control demand?

Written as: `D_min(N, X, I, T)`.

### Early warning

Can changes in group state signal that the system is approaching a control limit?

### Other systems

Do similar patterns appear outside sheep-herding simulations?

### More general description

Can different experiments be summarized by a shared normalized quantity, conceptually:

`available control / required control`?

That would be a strong later result if evidence supports it. It is not assumed.

---

# 9. Validation and Prediction

A useful relationship should do more than describe the experiments used to fit it. It should also make predictions for new conditions.

Where appropriate, validation includes:

* unseen collective sizes,
* unseen structures,
* new initial layouts,
* new controller setups,
* and different control methods.

A strong test is:

> Can a relationship learned from one set of experiments predict control demand in another set without being refitted?

---

# 10. Research Progression

### Core program

1. Size scaling: measure `D_min(N)`.
2. Structure: test whether `D_min(N, X)` is needed.
3. Mechanism: test explanations of the observed pattern.
4. Method transfer: check what remains when the control method changes.

### Later extensions

5. Information and time as extra resources.
6. Search for a more general normalized description, only if evidence supports it.

### Throughout

7. Validate on conditions not used to build the relationship.

---

# 11. Possible Scientific Outcomes

The program does not require one preferred outcome. Possible useful outcomes include:

* a clear size-scaling map for control demand,
* evidence that structure matters beyond size,
* a tested mechanistic explanation,
* evidence that some scaling features transfer across methods,
* or evidence that scaling is strongly method-dependent.

The project should claim only what the evidence supports.

---

# 12. Role of HerdSim

HerdSim is the experimental workbench for this program.

It lets us vary group size, structure-related conditions, controller number, control method, information, and other settings under shared tasks and shared metrics.

HerdSim is not meant to copy every detail of real livestock. It is meant to provide a controlled model system where collective control demand can be measured.

Herding is useful because it captures a key feature of indirect control:

> A small number of external controllers tries to steer a larger group whose members are not directly commanded one by one.

---

# 13. Scope

### In scope for the core program

* collective size,
* collective structure,
* external control demand,
* scaling relationships,
* mechanisms behind those relationships,
* generality across control methods.

### Not primary goals

* finding the single best herding algorithm,
* reproducing every detail of real livestock behavior,
* optimizing one controller architecture,
* immediately claiming results for every collective system,
* building a real-time failure prediction product.

Those can become later applications after the core scaling questions are clearer.

---

# 14. Implementation Guidance for HerdSim

This section turns the research questions into build priorities. The rule is simple:

> Implement what is needed to answer the questions. Do not build features that only support a preferred claim.

## 14.1 Shared protocol layer (needed first)

Before RQ-specific studies, HerdSim should make the experimental protocol explicit and reusable:

* fixed task / scenario definition,
* clear success rule,
* chosen reliability target (for example success rate across seeds),
* time budget,
* information setting,
* reproducible seeds,
* shared metrics across methods,
* a standard way to estimate `D_min` from a sweep over controller count `D`.

Without this layer, results from different experiments are hard to compare.

### Practical meaning of `D_min` in software

For a frozen protocol and a chosen size/structure condition:

1. run multiple seeds for each controller count `D`,
2. compute success rate,
3. find the smallest `D` that meets the reliability target,
4. store that value as `D_min` for that condition.

Also store nearby information, such as whether larger `D` keeps helping, saturates, or starts to hurt.

## 14.2 What to build for each core RQ

### For RQ1 (size scaling)

Build and keep stable:

* sweeps over collective size `N`,
* sweeps over controller count `D`,
* batch multi-seed experiments,
* export of success rates and estimated `D_min(N)`,
* plots or tables of control demand versus size.

Question this answers: how does required control change as the group grows?

### For RQ2 (structure)

Build and keep stable:

* measurable structure metrics during and/or at the start of a run (spread, density, fragmentation, elongation, clustering, outliers),
* ways to create or select different structures at similar `N`,
* matched comparisons where size is fixed and structure varies,
* analysis that separates size effects from structure effects.

Question this answers: at the same size, does group shape change control demand?

### For RQ3 (mechanisms)

Build and keep stable:

* trajectory and event logs that can support mechanism tests,
* quantities linked to candidate mechanisms (for example dispersion over time, number of separated subgroups, signs of controller conflict, recovery after disturbance),
* optional intervention experiments that change one suspected factor at a time.

Question this answers: why does the observed scaling pattern appear?

### For RQ4 (method transfer)

Build and keep stable:

* multiple control methods (instruments) under the same scenario and metrics,
* fair comparison settings: same task, same `N`, same seed list, same success rule,
* repeated `D_min` estimation across methods,
* comparison of scaling shape across methods, not only single-score ranking.

Question this answers: which parts of the scaling look shared, and which look method-specific?

## 14.3 Build order

Suggested order for HerdSim work:

1. Protocol freeze and `D_min` estimation pipeline.
2. RQ1 size sweeps and reporting.
3. Structure metrics and RQ2 controlled comparisons.
4. Mechanism logging and targeted interventions for RQ3.
5. Cross-method `D_min` comparisons for RQ4.
6. Only later: information/time extensions and stronger normalized summaries.

## 14.4 Implementation rule

Every major HerdSim change should map to one of:

* a clearer protocol definition,
* a core RQ,
* a validation need,
* or a clearly marked later extension.

If a feature does not help answer a stated question, it should wait.

## 14.5 How claims stay weak during implementation

When implementing and reporting:

* prefer "measure whether" over "prove that",
* report possible outcomes, not one expected victory condition,
* treat negative or mixed results as valid scientific progress,
* keep method comparison focused on transfer of scaling features, not on crowning a winner.

---

# 15. Scientific Contribution

The intended contribution is a clearer, evidence-based understanding of how collective properties shape the amount of external control needed for reliable steering.

Compared with a single-method scaling study, this program aims to:

* define control demand in a reusable way,
* separate size effects from structure effects,
* test mechanisms rather than stop at correlation,
* and check which scaling features survive method change.

The work moves through three increasingly broad questions:

> How does control demand scale with collective size?

> How does collective structure modify that scaling?

> Which parts of the resulting relationship are independent of the specific control method?

If successful, the program can provide more than results for one herding algorithm. It can provide a practical empirical framework for studying scaling in indirect control of collective systems.

A simple predictive relationship would be a strong outcome. It is not assumed at the start.

---

# 16. Summary

### Problem

When a few external controllers guide a larger group, how does the needed amount of control change as the group grows or changes shape?

### Core questions

1. Size: how does `D_min` change with `N`?
2. Structure: does `X` matter beyond size?
3. Mechanism: what processes explain the pattern?
4. Generality: which parts remain when the method changes?

### Approach

Use HerdSim as a controlled experimental workbench. Freeze a protocol, measure `D_min`, vary size and structure, test explanations, then compare across methods.

### What success looks like

Not one forced claim. Success means the questions are answerable with clear evidence, and HerdSim has the protocol, metrics, and experiment tools needed to produce that evidence.

### Overall goal

> Discover how the control required to reliably steer a collective scales with collective size and structure, understand the mechanisms behind that scaling, and determine which aspects of that scaling generalize across control methods.
