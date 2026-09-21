# HerdSim Research Program

## Scaling of Collective Control

Formal RQs, claims, Caps, protocol freeze, and phases:

[main_scaling_plan.md](main_scaling_plan.md)

Where we are and what to run next:

[progress_tracker.md](progress_tracker.md)

If the docs disagree: the main plan wins on science; the tracker wins on status.

---

## Central question

> When a few shepherds guide a larger flock, how much control do we actually need as the flock gets bigger or more spread out?

That is the same basic problem as the draft sheep-scaling paper (dog count vs flock
size, and whether "spread" helps explain difficulty). We keep it, but we try to be
more careful:

- say clearly what "how much control" means,
- separate size from shape / state,
- ask why a pattern shows up, not only that it does,
- check whether it still shows up under a different herding method.

We are not starting from a claimed universal scaling law. We start from questions
we can actually run.

### What we want out of the core program

After the core runs, we should be able to say something concrete about:

- how control need changes as the group grows,
- whether shape / state matters beyond size,
- which processes look like they drive the pattern,
- and what looks shared across methods vs method-specific.

A simple predictive rule would be great. Finding that the pattern is strongly
method-dependent would also be useful -- that still bounds how far you can
generalise.

---

## HerdSim

HerdSim is our experimental platform for multi-agent sheep herding: a few shepherds
(dogs) guide a larger flock to a goal under controlled settings. For this program it
is the workbench -- a model system for measuring control demand -- not an attempt to
copy real farms in full.

Herding is a good fit because control is indirect:

> A small number of external controllers tries to steer a larger group whose members are not commanded one by one.

---

## Shared protocol (idea)

Before diving into RQ-specific grids, we freeze one shared protocol so later
comparisons are fair. That means locking at least:

- the herding task,
- what counts as success,
- a reliability target (e.g. succeed in at least 90% of runs),
- a time budget,
- which flock sizes and shepherd counts we sweep,
- a baseline method and the methods we compare against it,
- how we estimate the viable shepherd range (minimum for reliable success, and
  where adding more stops helping or starts hurting).

Frozen defaults: main plan, Section 8.

---

## Terms

| Term | Meaning |
|------|---------|
| Collective | Group of interacting individuals (usually sheep) |
| Shepherd / dog | External agent that guides the collective indirectly |
| Task | What success means (e.g. drive flock into a goal in time) |
| Reliability | How often the task succeeds across repeated runs |
| Control demand | How much external control is needed for a chosen reliability; primary measure is the viable shepherd range around `D_min` / overcrowding |
| `N` | Collective size |
| `D` | Shepherd count |
| `D_min` | Smallest `D` that meets the reliability target under a fixed protocol |
| Structure (`X`) | Spatial organization beyond size: spread, density, fragmentation, elongation, clustering, outliers |
| Control method / method | Named herding rules used by the shepherds |
| Mechanism | Process that helps explain a scaling pattern |
| Protocol | Frozen experimental rules for fair comparison |

`D_min` is not a universal property of a flock. It depends on task, time limit, information, success rule, and other fixed settings.

---

## Core research questions

For each question: what we want to know, how we plan to study it, and what kinds of
answers would count. We are not locking in a preferred outcome ahead of time.

Formal IDs from the main plan are in parentheses.

### 1. Size -- how does the viable shepherd range change with collective size? (RQ2, RQ6)

**Question.** As flock size grows, how does the viable shepherd range change: the minimum needed for reliable herding, and the point where adding more stops helping or starts hurting?

**Approach.** Freeze the protocol. Vary `N`, keep other settings as fixed as we can. For each `N`, find the smallest `D` that hits the reliability target, and note whether larger `D` still helps, plateaus, or hurts. Only fit scaling models once we have real frontiers.

**Possible results.** Linear, sublinear, or superlinear growth; different behaviour in different size bands; saturation or thresholds; or nothing simple. We also care about operating regimes (too few / efficient / wasteful / overcrowding).

### 2. Structure -- does shape/state change control demand at fixed size? (RQ1)

**Question.** At the same flock size, does flock shape/state (spread, fragmentation, outliers, etc.) change how much control we need?

**Approach.** Hold `N` fixed in matched comparisons. Change initial structure on purpose. Measure a few structural properties and see how much of the leftover variation size alone cannot explain.

**Possible results.** Size is almost enough; one or a few structure measures pick up the rest; or different properties matter at different sizes.

### 3. Mechanism -- what produces the observed pattern? (RQ3)

**Question.** Why does that pattern appear (for example interference, coverage limits, fragmentation)?

**Approach.** Candidates include spatial demand, fragmentation, controller interference, redundant control, and local instability. Log run-level quantities tied to those ideas, see which track control demand, and intervene when we can. Correlation by itself is not treated as causation.

**Possible results.** One main mechanism; several mechanisms in different regimes; or a pattern that does not reduce to one clean story.

### 4. Generality -- which parts transfer across herding methods? (RQ4)

**Question.** Which parts of the pattern still hold when we change the herding method?

**Approach.** Rerun the core size and structure experiments under more than one method. Compare scaling shape and regime labels, not only raw success rates. Mark what looks shared vs method-specific.

**Possible results.** Fully method-specific scaling; same shape with different magnitude; or same shape with method-dependent thresholds and slopes. Strong method dependence would limit how far we can talk about "scaling" apart from the controller.

---

## Follow-on questions

These sit after the core four. They should not rewrite the first scientific question.

| Topic | Formal ID | Question in brief |
|-------|-----------|-------------------|
| Information vs shepherds | RQ5 | Can better sensing or communication reduce required shepherd count at fixed reliability? |
| Early warning | RQ7 | Can flock-state signals warn of failure before a run times out? |
| Time as a resource | (protocol T₀/T₁) | How does a tighter or looser time limit change control demand? |
| Other systems | later | Do similar patterns appear outside sheep-herding simulations? |

Operating regimes (too few / efficient / wasteful / overcrowding) belong with the Size question and Package A -- not a separate RQ.

---

## Short approach

1. Freeze the shared HerdSim protocol.
2. Sweep flock size and shepherd count with the baseline method; map viable range and regimes.
3. Hold size fixed and vary initial flock structure so we can separate size from shape / state.
4. Use run logs to pressure-test candidate mechanisms.
5. Repeat the same measurements on other herding methods and see what transfers.
6. Later: information substitution and early-warning tests.

Build order should follow that: protocol + `D_min` pipeline first, then size maps, then structure metrics and matched comparisons, then mechanism logging, then cross-method work. Information / time and heavier summary analysis come later.

Rule of thumb for HerdSim changes: if a change does not clarify the protocol, serve a core or follow-on RQ, support validation, or is explicitly marked as later work, it probably does not belong in this program yet.

---

## Scope

### In scope for the core program

- collective size and structure
- external control demand and viable shepherd range
- scaling relationships and mechanisms
- generality across control methods
- reproducible protocol (S8)

### Not primary goals

- finding the single best herding algorithm
- reproducing every detail of real livestock behaviour
- optimizing one controller architecture
- claiming results for every collective system out of the gate
- shipping a real-time failure-prediction product

Those can wait until the core scaling questions are clearer.

---

## Scientific contribution

What we are aiming for is a clearer, evidence-backed account of how collective
properties change how much external control you need for reliable steering.

Relative to a single-method scaling study, that means:

- defining control demand in a reusable way,
- separating size effects from structure effects,
- testing mechanisms instead of stopping at correlation,
- checking which scaling features survive a method change.

Only claim what the evidence supports. Formal claims, Cap IDs, and phase
done-when criteria live in the main plan.
