# HerdSim Research Program

## Scaling of Collective Control

Parent framing for the shepherding-budget program. It states the scientific problem in plain language and the build priorities that follow from it.

Execution detail (formal RQ1--RQ7, claims, Caps, protocol freeze, phases) lives in:

[main_shepherding_budget_plan.md](main_shepherding_budget_plan.md)

Live status and campaigns live in:

[progress_tracker.md](progress_tracker.md)

If anything conflicts, the main plan wins on scientific content; the tracker wins on current status.

---

## Central question

> When a few shepherds guide a larger flock, how much control do we actually need as the flock gets bigger or more spread out?

A draft sheep-scaling study asked how dog count should grow with flock size, and whether flock "spread" helps explain difficulty. This program keeps that problem, but treats it more carefully:

- define "how much control is needed" in a reusable way,
- separate group size from group shape,
- ask why the pattern appears,
- and check whether the pattern still holds when the guiding method changes.

We do not start by claiming a universal scaling law. We start with questions experiments can answer.

### What success looks like

By the end of the core program, evidence should show:

- how control need changes as the group grows,
- whether the shape of the group matters beyond size,
- which processes help explain that pattern,
- and which parts look shared across guiding methods versus method-specific.

A simple predictive rule would be a strong success. Strong method dependence would also be a useful result.

---

## HerdSim

HerdSim is a reproducible experimental platform for multi-agent sheep herding: a small number of shepherds (dogs) guides a larger flock toward a goal under controlled conditions. It is the experimental workbench for this program -- a controlled model system for measuring collective control demand, not a full replica of real farms.

Herding is useful because it captures indirect control:

> A small number of external controllers tries to steer a larger group whose members are not commanded one by one.

---

## Shared protocol (idea)

Before RQ-specific studies, experiments share one frozen protocol so comparisons stay fair. In practice that means locking:

- the herding task,
- what counts as success,
- a reliability target (for example succeed in at least 90% of runs),
- a time budget,
- flock sizes and shepherd counts to sweep,
- a baseline herding method and the methods compared against it,
- and a common way to estimate the viable shepherd range (minimum needed for reliable success, and where adding more stops helping or starts hurting).

Full frozen defaults are in the main plan, Section 8.

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
| Control method / instrument | Named herding rules used by the shepherds |
| Mechanism | Process that helps explain a scaling pattern |
| Protocol | Frozen experimental rules for fair comparison |

`D_min` is not a universal property of a flock. It depends on task, time limit, information, success rule, and other fixed settings.

---

## Core research questions

Each question has three parts: what we want to know, how we study it, and what we may find. We do not pre-commit to one preferred result.

Formal IDs used in the main plan are noted in parentheses.

### 1. Size -- how does the viable shepherd range change with collective size? (RQ2, RQ6)

**Question.** As flock size grows, how does the viable shepherd range change: the minimum needed for reliable herding, and the point where adding more stops helping or starts hurting?

**Approach.** Freeze a protocol. Vary `N` while holding other conditions as constant as possible. For each `N`, find the smallest `D` that meets the reliability target, and record whether larger `D` keeps helping, saturates, or hurts. Fit scaling candidates only after real frontiers exist.

**Possible results.** Linear, sublinear, or superlinear growth; different regimes at different sizes; saturation or thresholds; or no simple relationship. Also: clear operating regimes (too few / efficient / wasteful / overcrowding).

### 2. Structure -- does shape/state change control demand at fixed size? (RQ1)

**Question.** At the same flock size, does flock shape/state (spread, fragmentation, outliers, etc.) change how much control we need?

**Approach.** Keep `N` fixed in matched comparisons. Vary initial structure in a controlled way. Measure candidate structural properties. Compare how much variation is explained by size alone versus size plus structure.

**Possible results.** Size is almost enough; one or a few structural measures explain remaining variation; or different properties matter in different size ranges.

### 3. Mechanism -- what produces the observed pattern? (RQ3)

**Question.** Why does that pattern appear (for example interference, coverage limits, fragmentation)?

**Approach.** Candidate mechanisms include spatial demand, fragmentation, controller interference, redundant control, and local instability. Measure run-level quantities linked to these ideas, check which track control demand, and intervene where possible. Correlation alone is not treated as causation.

**Possible results.** One dominant mechanism; several mechanisms in different regimes; or a pattern that resists a single simple explanation.

### 4. Generality -- which parts transfer across herding methods? (RQ4)

**Question.** Which parts of the pattern still hold when we change the herding method?

**Approach.** Repeat core size and structure experiments under more than one method. Compare scaling shape and regime labels, not only raw success rates. Separate shared features from method-specific ones.

**Possible results.** Method-specific scaling; shared form with different magnitude; or shared form with method-dependent thresholds and slopes. Strong method dependence bounds how far scaling can be separated from the controller.

---

## Follow-on questions

These come after the core four. They should not redefine the first scientific question.

| Topic | Formal ID | Question in brief |
|-------|-----------|-------------------|
| Information vs shepherds | RQ5 | Can better sensing or communication reduce required shepherd count at fixed reliability? |
| Early warning | RQ7 | Can flock-state signals warn of failure before a run times out? |
| Time as a resource | (protocol T₀/T₁) | How does a tighter or looser time limit change control demand? |
| Other systems | later | Do similar patterns appear outside sheep-herding simulations? |

Operating regimes (too few / efficient / wasteful / overcrowding) are part of the Size question and Package A, not a separate RQ.

---

## Short approach

1. Freeze the shared HerdSim protocol.
2. Sweep flock size and shepherd count with the baseline method; map viable control range and regimes.
3. Hold size fixed and vary initial flock structure to separate size from shape/state.
4. Use run logs to test candidate mechanisms.
5. Repeat measurements across other herding methods to see what transfers.
6. Later: information substitution and early-warning tests.

Suggested HerdSim build order matches that progression: protocol and `D_min` pipeline first; then size maps; then structure metrics and matched comparisons; then mechanism logging; then cross-method comparison; only later information/time and stronger normalized summaries.

Implementation rule: every major HerdSim change should map to a clearer protocol definition, a core or follow-on RQ, a validation need, or a clearly marked later extension.

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
- immediately claiming results for every collective system
- building a real-time failure prediction product

Those can become later applications after the core scaling questions are clearer.

---

## Scientific contribution

The intended contribution is a clearer, evidence-based understanding of how collective properties shape the amount of external control needed for reliable steering.

Compared with a single-method scaling study, this program aims to:

- define control demand in a reusable way,
- separate size effects from structure effects,
- test mechanisms rather than stop at correlation,
- and check which scaling features survive method change.

Claim only what the evidence supports. Formal claims, Cap IDs, and phase done-when criteria are in the main plan.
