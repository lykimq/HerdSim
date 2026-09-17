# Shepherding Budget Analysis -- Research Backbone

Status: active draft (protocol not frozen)  
Audience: researchers and implementers working on HerdSim  
Role: canonical research specification; all later simulations, experiments, tool changes, and analyses should serve this document

Related execution tracker: `.cursor/plans/shepherding_budget_research.plan.md`

---

## 0. How to use this document

This file is the backbone for the research program. It defines:

1. the scientific goal and thesis
2. the field gaps this program addresses
3. the contributions we aim to deliver
4. formal definitions (budget, reliability, regimes, frontiers)
5. concrete research questions and what counts as an answer
6. the experimental protocol
7. HerdSim capabilities required to produce those answers
8. phased work from protocol freeze to results

Implementation rule:

- Do not add simulations, metrics, UI, or analysis features "in general."
- Add them only when they are required to answer a question in this document.
- If a proposed change does not map to a question, contribution, or protocol need below, it is out of scope until this document is revised.

---

## 1. Scientific goal

### 1.1 Goal statement

Establish multi-resource shepherding-budget frontiers for cohesive flocks, and determine which frontier properties and predictors transfer across herding methods.

### 1.2 Thesis

Shepherding scalability is better understood as a multi-resource budget problem than as a single-variable staffing question. The field needs:

- **comparative frontiers** that expose tradeoffs among shepherd count, time, and effort;
- **a regime taxonomy** that formalises overcrowding, underspend, and other non-obvious failure modes;
- **cross-method transfer tests** that separate flock-control principles from algorithm artifacts.

### 1.3 Primary object of study

The shepherding budget and the performance frontier it induces.

Shepherd count `D` is one input to the budget. It is not the whole research object.

### 1.4 What success looks like

We can claim success if we deliver at least one of:

- a comparative regime taxonomy supported by multi-method evidence
- a transfer result identifying which frontier properties are method-invariant vs method-specific
- quantified substitution rates between sensing/coordination quality and shepherd headcount
- a cross-method predictor of required budget, with documented failure cases

and we can reproduce those claims from locked seeds, scenarios, metrics, and exports.

---

## 2. Field gap this program addresses

### 2.1 Current state of the field

- Many papers propose herding controllers, but each is evaluated in its own simulator with its own metrics.
- A smaller set studies scaling limits — how performance changes with flock size `N` or shepherd count `D`.
- Very few studies treat herding as a multi-resource problem involving time, effort, and information in addition to headcount.
- Almost no shared protocol exists for making comparative scaling claims across methods.
- The overcrowding effect (performance degradation from excess shepherds) is observed but not formalised.

### 2.2 Specific gaps we target

| Gap ID | Missing piece in the field | Our response |
|--------|----------------------------|--------------|
| G1 | Object of study is usually dog count alone | Multi-resource budget vector `(D, T)` with effort as a measured outcome |
| G2 | Overcrowding and overspend are reported anecdotally | Operationalised regime taxonomy with boundary criteria |
| G3 | Unknown what transfers across methods | Comparative transfer tests under locked protocols |
| G4 | No resource-substitution analysis | Sensing/coordination vs `D` substitution curves |
| G5 | Predictors are validated within a single model only | Cross-method predictor evaluation with failure-case documentation |
| G6 | No reusable reporting standard for frontier claims | Reproducible protocol with provenance exports |

### 2.3 Non-goals

- Inventing a new herding controller as the primary contribution.
- Claiming a universal closed-form `D = f(N)` from a single method.
- Expanding the budget definition to every possible factor before v1 frontiers exist.
- Treating methods with incompatible motion conventions as directly comparable without caveats.

---

## 3. Contributions to the field

Each contribution must map to at least one research question in Section 5.

### Contribution A -- Multi-resource budget framing (conceptual)

Reframe flock guidance as a multi-resource budget problem:

- **reliability** = success rate over stochastic seeds at a stated threshold
- **cost** = budget inputs (shepherd count `D`, time limit `T`) and measured outcome (realised effort `E`)
- **frontier** = the set of budget configurations that achieve reliable herding at minimum cost

Conceptual value: provides shared language for scalability claims across the collective-control literature.  
Application value: operators can reason about tradeoffs — fewer robots vs more time, better sensing vs more headcount.

### Contribution B -- Regime taxonomy (empirical)

Define and measure distinct regimes in the relationship between budget and performance:

- **under-budget failure**: reliability below threshold
- **efficient operation**: reliability above threshold with competitive effort and time
- **wasteful overspend**: reliability remains high, but effort or time worsens without reliability gain
- **overcrowding collapse**: reliability itself declines as shepherd count increases
- **hard failure / unherdable ceiling**: no tested budget achieves the reliability threshold (if observed)

Empirical value: structures scaling behaviour beyond monotone "more shepherds = better" assumptions.  
Application value: warns practitioners against naive over-provisioning.

### Contribution C -- Cross-method transfer analysis (empirical)

Determine which frontier properties are:

- **method-invariant** (shared across herding algorithms), or
- **method-specific** (artifacts of a particular algorithm)

Either finding is scientifically valuable: universals reveal flock-control principles; method-specifics reveal algorithm design constraints.

Empirical value: separates flock physics from algorithm design.  
Application value: tells practitioners when method choice changes the required budget.

### Contribution D -- Resource substitution analysis (empirical + applied)

Quantify how improvements in sensing quality or coordination capacity substitute for shepherd headcount at fixed reliability.

Empirical value: connects information-theoretic assumptions (observation range, noise, communication) to operational cost.  
Application value: better sensors or communication may reduce the number of robots needed.

### Contribution E -- Cross-method herdability predictors (empirical + applied)

Identify flock-level macro-measures (e.g., cohesion, spread, fragmentation) that predict required budget across methods, and document where those predictors fail.

Empirical value: identifies predictive herdability indicators and their domain of validity.  
Application value: enables real-time monitors for under-budgeted flock states.

### Contribution F -- Reproducible experimental standard (infrastructure)

A reusable experimental standard comprising: locked tasks, seed lists, metric definitions, frontier extraction procedures, regime labels, failure taxonomy, and export provenance.

Value: future studies can report frontier shifts relative to a shared baseline, rather than presenting isolated demos.

---

## 4. Formal definitions

Freeze these before claim-grade experiments. The candidates below are the working defaults.

### 4.1 Agents and task

| Symbol | Meaning |
|--------|---------|
| `N` | Number of sheep (flock size) |
| `D` | Number of shepherds (dogs/robots) |
| `m` | Herding method (instrument) |
| `τ` | Task: scenario definition + success rule |
| `seed` | Random seed controlling initialisation and stochasticity |

### 4.2 Shepherding budget (v1)

The budget has two layers: **inputs** (what the operator chooses) and **outcomes** (what is measured).

**Budget inputs:**

```text
B = (D, T)
```

| Symbol | Meaning | Operationalisation in HerdSim |
|--------|---------|-------------------------------|
| `D` | Shepherd count | `n_shepherds` parameter |
| `T` | Time limit | `max_ticks` (upper bound on simulation duration) |

**Measured outcomes per trial:**

| Symbol | Meaning | Operationalisation in HerdSim |
|--------|---------|-------------------------------|
| `E` | Realised effort | Total shepherd path length (sum of distances travelled by all shepherds) |
| `t_s` | Time to success | Ticks elapsed at task completion (if successful) |
| `S` | Success | Binary: did the trial meet the task's success rule? |

**Design rationale:**

- `D` and `T` are **inputs** because the operator sets them before a trial begins.
- `E` and `t_s` are **outcomes** because they depend on the trial's dynamics; they are not set in advance.
- Effort `E` is used in Pareto/efficiency analysis (which budget inputs achieve reliable success at lowest cost?) but is not itself a constraint in v1. A future version may impose effort caps.
- Information quality (sensing range, noise, communication) and coordination capacity are treated as **frontier-shifting factors** in v1 — experimental conditions that move the frontier, not coordinates of the budget vector.

### 4.3 Trial success and reliability

- **Trial success**: `S ∈ {0, 1}` — determined by the scenario's `is_success` rule at termination.
- **Reliability** of an experimental cell `c = (m, τ, N, D, T, factors)` over a seed set `Seeds`:

```text
R(c) = (1 / |Seeds|) × Σ_{seed ∈ Seeds} S(c, seed)
```

- **Reliable cell**: `R(c) ≥ θ`
- Working default: `θ = 0.90`
- Sensitivity reporting: always also report results at `θ ∈ {0.50, 0.70}` for key claims.

### 4.4 Frontier quantities

For fixed `(m, τ, N, factors)` under baseline time limit `T₀`:

| Quantity | Definition |
|----------|------------|
| `D_min(N)` | Smallest `D` such that `R ≥ θ` |
| `D_overcrowd(N)` | Smallest `D > D_min` at which `R` begins a sustained decline (≥ 2 consecutive D-steps with lower R) |
| `D_max(N)` | Largest `D` that still maintains `R ≥ θ` (meaningful only if overcrowding decline is observed) |
| `B*(N)` | Efficient reliable budget: the `(D, T)` pair achieving `R ≥ θ` at minimum median effort `E`, with ties broken by smaller `D`, then smaller median `t_s` |

Any alternative cost order used to define `B*` must be documented explicitly before it appears in claims.

### 4.5 Performance regimes

For fixed `(m, τ, N)` as shepherd count `D` increases (at baseline `T₀`):

| Regime | Operational definition | Key indicator |
|--------|------------------------|---------------|
| Under-budget failure | `R(c) < θ` | Reliability below threshold |
| Efficient operation | `R(c) ≥ θ` and `D` is at or near `D_min`; effort and time are competitive | Reliability high, effort near minimum |
| Wasteful overspend | `R(c) ≥ θ` but median `E` exceeds the efficient level by ≥ 20% without reliability improvement | Reliability flat, effort rising |
| Overcrowding collapse | `R(c)` drops below `θ` for `D > D_overcrowd` | Reliability declining with more shepherds |
| Hard failure | No tested `D` achieves `R ≥ θ` within `T₀` | Candidate unherdable ceiling for this `(m, τ, N)` |

Notes:

- The 20% effort threshold for "wasteful overspend" is a working default; sensitivity analysis should test thresholds at 10% and 30%.
- A cell can transition through multiple regimes as `D` increases: under-budget → efficient → wasteful → overcrowding.
- Regime labelling is applied per method and per flock size; it is not a global label.

### 4.6 Primary measurements (every trial)

Required for all trials:

| Measurement | Description |
|-------------|-------------|
| Success `S` | Binary task completion |
| Time to success `t_s` | Ticks at success (if successful); `T₀` if failed |
| Realised effort `E` | Total shepherd path length |
| Cohesion | Mean distance of sheep to flock centroid (GCM), averaged over time |
| Fragmentation index | Fraction of simulation time the flock is split into ≥ 2 clusters |
| Outlier count | Number of sheep beyond the "lost" threshold at termination |
| Terminal reason | Why the trial ended (success, timeout, other) |

Optional (add when needed for specific questions):

- Variance-based spread (as used in mean-spread `S̄` measures)
- Flock convex-hull area or perimeter
- Number of distinct clusters at termination

### 4.7 Fair comparison rules

When comparing methods:

1. Lock `τ`, `N`, seed list, success rule, and factor settings.
2. Sweep the same `D` values for each method (fair compare); do not use method-specific default counts.
3. Compare reliability and regime structure first. Compare effort across methods only with documented motion-convention caveats (step size, speed, tick semantics).
4. Export full provenance: instrument identifier, resolved configuration, seed list, metric definitions, code version.

---

## 5. Research questions

### 5.1 Spine questions (first results package)

#### Q1 -- Multi-resource budget frontier

**Question:** For a fixed task `τ₀` and reliability threshold `θ`, which budget configurations `(D, T)` achieve reliable herding as flock size `N` grows? What is the Pareto relationship among reliability, effort, and time across the reliable region?

**Hypothesis:** The set of reliable budgets forms a connected region in `(D, T)` space that shifts and potentially narrows as `N` increases. Within this region, effort `E` and time `t_s` trade off: faster completions require more effort (more aggressive shepherding).

**What counts as an answer:**

- Reliability heatmaps over `(N, D)` at fixed `T₀`
- Median effort and median time-to-success for each reliable cell
- `D_min(N)` curve with confidence bands
- `B*(N)` curve identifying the most efficient reliable budget at each `N`
- Pareto front of `(E, t_s)` within the reliable region for selected `N` values

**Contribution:** A (framing), and data for B (regimes).

---

#### Q2 -- Regime structure

**Question:** As shepherd count `D` increases at fixed flock size `N`, does performance pass through distinct regimes — under-budget failure, efficient operation, wasteful overspend, and overcrowding collapse? Where are the regime boundaries, and do they shift predictably with `N`?

**Hypothesis:** The overcrowding regime is not merely noise at high `D`; it reflects interference among shepherds (conflicting repulsion forces on the flock). The onset `D_overcrowd` grows with `N` but at a slower rate than `D_min`.

**What counts as an answer:**

- Regime map: for each `(N, D)` cell, a regime label assigned by the operational definitions in Section 4.5
- Boundary estimates: `D_min(N)`, `D_overcrowd(N)`, and `D_max(N)` where observable
- Failure-mode characterisation at regime boundaries (e.g., fragmentation-driven failure vs timeout-driven failure)
- Sensitivity: regime maps at `θ ∈ {0.50, 0.70, 0.90}`

**Contribution:** B.

---

#### Q3 -- Cross-method transfer

**Question:** Under locked tasks and seeds, which frontier and regime properties are shared across herding methods, and which are method-specific?

**Hypothesis:** Qualitative regime structure (the existence of overcrowding, the ordering of regimes) transfers across methods, even when the exact `D_min(N)` values differ. The viable-range width `D_max - D_min` may be method-specific because it depends on how shepherds coordinate.

**What counts as an answer:**

- Transfer table: for each property (regime existence, regime ordering, `D_min` scaling exponent, overcrowding onset, Pareto shape), label it as **shared** (present in all methods), **shifted** (present but with different parameters), or **absent** (not observed in some methods)
- Ranking stability: does the method with the smallest `D_min` at a given `N` also achieve the lowest effort? If rankings change, document the crossover points.

**Contribution:** C.

---

#### Q4 -- Scaling shape

**Question:** How does `D_min(N)` scale with flock size? Is the relationship sublinear (e.g., `D_min ∝ N^α, α < 1`), piecewise with breakpoints, or strongly method-dependent?

**Hypothesis:** For cohesive flocks, `D_min(N)` grows sublinearly because flock cohesion makes larger flocks partially self-organising. The exponent `α` is expected to be smaller than the `√N` found by Lama & di Bernardo (2024) for non-cohesive targets, because cohesion reduces the herder's burden.

**What counts as an answer:**

- Fitted scaling models (power law, piecewise linear, log-linear) per method, with goodness-of-fit comparison
- Residual analysis and breakpoint detection
- Statement of which scaling hypotheses remain plausible and which are rejected
- Cross-method comparison: is `α` consistent across methods?

**Contribution:** C (and supports A).

---

### 5.2 Amplifier questions (second results package)

#### Q5 -- Resource substitution

**Question:** At fixed flock size `N` and reliability threshold `θ`, how much can improved sensing range or coordination capacity reduce the required shepherd count `D`? What happens to effort `E` and time `t_s` when shepherds are replaced by better information?

**Hypothesis:** Increasing sensing range has diminishing returns — doubling range from baseline saves more shepherds than doubling it again. There exists a sensing-range threshold below which no `D` achieves reliable herding (information floor).

**What counts as an answer:**

- Substitution curves: `D_min` as a function of sensing-range factor (and/or coordination factor) at fixed `N`
- Iso-reliability contours in `(D, sensing-range)` space
- Effort and time tradeoffs: does fewer-shepherds-with-better-sensing produce lower or higher total effort?

**Contribution:** D.

---

#### Q6 -- Predictive macro-measures

**Question:** Which flock-level macro-measures (cohesion, spread, fragmentation, cluster count) predict the required budget across methods? Where do those predictors break down?

**Hypothesis:** Mean-spread (or a spread-derived composite) predicts `D_min` within a single method, but its predictive power degrades across methods that use different cohesion mechanisms. No single macro-measure achieves > 85% accuracy across all methods and flock sizes.

**What counts as an answer:**

- Predictor ranking by accuracy (correlation with `D_min` and/or classification of reliable vs unreliable cells)
- Per-method vs cross-method accuracy comparison
- Failure-case catalogue: conditions where the best predictor is wrong (e.g., small `N`, highly fragmented flocks, scenarios with obstacles)

**Contribution:** E.

---

### 5.3 Deferred question

#### Q7 -- Budget under perturbation

**Question:** How much does the required budget inflate under heterogeneous flock composition, shepherd failure (dropout during task), or harder environmental conditions (obstacles, multiple goals)?

**Hypothesis:** Budget inflation is superlinear in perturbation severity — small disturbances are absorbed, but beyond a tipping point the required `D` increases sharply.

Run only after Q1–Q4 exist as baselines.

**Contribution:** extends B and C to robust settings.

---

## 6. Experimental protocol

### 6.1 Canonical settings (working defaults; freeze in Phase 0)

| Item | Working default | Status |
|------|-----------------|--------|
| Canonical task `τ₀` | Drive to Goal | pending confirm |
| Reliability threshold `θ` | 0.90 (also report 0.50, 0.70) | pending confirm |
| Baseline instrument | `strombom_multi` (or `strombom` for D=1 slice) | pending confirm |
| Transfer instrument set | `strombom_multi`, `kubo`, `fat`, `communication_free` | pending confirm |
| Secondary contrasts (optional) | `v_formation`, `adaptive` | optional |
| Flock sizes `N` | {10, 25, 50, 100, 150, 200, 250, 300, 400} | pending confirm |
| Shepherd counts `D` | {1, 2, 3, 4, 6, 10, 15, 20, 25, 35} | pending confirm |
| Scout seeds (initial sweeps) | ≥ 30 per cell | pending confirm |
| Claim-grade seeds (boundary cells) | ≥ 100 per cell | pending confirm |
| Time limit `T₀` | 10,000 ticks | pending confirm |
| Information in `B`? | No for v1 (treated as frontier-shifting factor) | pending confirm |

### 6.2 Phase plan

#### Phase 0 -- Freeze protocol

Deliverables:

- Confirmed and locked table in Section 6.1
- Metric and export checklist (which measurements, which formats)
- Analysis definitions for `D_min`, `D_overcrowd`, `B*`, regime labelling

Exit criterion: this section marked **frozen**; no further changes without a decision-log entry.

#### Phase 1 -- Single-method frontier (Q1, Q2)

Steps:

1. Run baseline instrument over the full `N × D` grid with scout seeds
2. Identify boundary cells and rerun with claim-grade seeds
3. Compute reliability, effort, time for every cell
4. Extract `D_min(N)`, `B*(N)`, and regime map
5. Characterise failure modes at regime boundaries

Exit criterion: one complete frontier + regime map with provenance export.

#### Phase 2 -- Comparative transfer (Q3, Q4)

Steps:

1. Repeat Phase 1 for each instrument in the transfer set
2. Ensure locked task, seed list, and metric definitions across all methods
3. Build transfer table and scaling-shape summary
4. Document motion-convention caveats for effort comparison

Exit criterion: multi-method transfer claims ready for drafting.

#### Phase 3 -- Substitution and predictors (Q5, Q6)

Steps:

1. Factor sweeps on sensing range and coordination parameters
2. Compute substitution curves and iso-reliability contours
3. Evaluate predictor accuracy within and across methods

Exit criterion: substitution + predictor result packages.

#### Phase 4 -- Robustness (Q7)

Steps:

1. Introduce perturbations (heterogeneity, shepherd dropout, obstacles) against frozen Phase 1–2 baselines
2. Measure budget inflation relative to nominal frontiers

Exit criterion: robustness dossier.

---

## 7. HerdSim requirements (implementation backlog derived from questions)

This section bridges research questions to tool work. Implement only what the active phase needs.

### 7.1 Already usable

- Multiple instruments (`strombom`, `strombom_multi`, `kubo`, `fat`, `communication_free`)
- Shared scenarios and seed control
- Factor sweeps and experiment exports
- Metrics: success, time-related signals, shepherd path length, cohesion, fragmentation
- Basic herdability helper for minimum shepherds from trial tables

### 7.2 Required for Phase 1–2 (must have)

| Req ID | Need | Serves |
|--------|------|--------|
| R1 | Reliable multi-seed `(N, D)` grid runner with provenance export | Q1–Q4 |
| R2 | Analysis to compute `D_min`, `D_overcrowd`, `D_max` from reliability tables | Q1, Q2 |
| R3 | Regime labelling from reliability and effort curves | Q2 |
| R4 | Efficient-budget / Pareto summary (`B*`) extraction | Q1 |
| R5 | Motion-convention documentation and effort-normalisation caveats | Q3 fair comparison |
| R6 | Failure labels and terminal-reason export | Q2 regime/failure interpretation |

### 7.3 Required for Phase 3 (should have)

| Req ID | Need | Serves |
|--------|------|--------|
| R7 | Clean sensing-range and noise parameter sweeps | Q5 |
| R8 | Predictor evaluation pipeline (macro-measures → required budget prediction) | Q6 |
| R9 | Additional flock macro-measures if cohesion/fragmentation are insufficient | Q6 |

### 7.4 Required for Phase 4 (later)

| Req ID | Need | Serves |
|--------|------|--------|
| R10 | Heterogeneity and shepherd-failure scenario campaigns | Q7 |
| R11 | Multi-scenario frontier-shift reports | Q7 generalisation |

### 7.5 Explicitly not required to start

- A new herding algorithm
- Full biological redesign of sheep or dog models
- Expanding HerdSim into a general multi-agent platform beyond shepherding needs

---

## 8. Claims we aim to support

These are targets, not yet results. Each will be accepted, refined, or rejected based on evidence from the corresponding questions.

### 8.1 Empirical claims

1. Herding performance for cohesive flocks is characterised by a multi-resource budget frontier over `(D, T)`, not by a single staffing number. *(Q1)*
2. Reliability is not monotone in shepherd count: an overcrowding regime exists in which adding shepherds reduces performance. *(Q2)*
3. Qualitative regime structure (existence and ordering of regimes) transfers across herding methods, even when exact `D_min(N)` values do not. *(Q3)*
4. `D_min(N)` grows sublinearly for cohesive flocks, and the scaling exponent is broadly consistent across methods. *(Q4)*
5. Improved sensing and coordination substitute for shepherd headcount within measurable bounds, with diminishing returns. *(Q5)*
6. Flock macro-state carries predictive information about required budget beyond `N` alone, but no single predictor is universally accurate across methods. *(Q6)*

### 8.2 Applied claims

1. Operators can choose among multiple reliable budgets under time and effort constraints. *(Q1)*
2. Adding shepherds past the efficient point wastes effort or actively reduces reliability. *(Q2)*
3. Better sensing or coordination can reduce robot-staffing requirements for a given reliability target. *(Q5)*
4. Method evaluation should report frontier shifts and regime maps, not only success on a default `(N, D)` pair. *(Contribution F)*

---

## 9. Result packages (deliverables)

### Package P1 -- Frontier dossier (from Q1, Q2)

- Protocol stamp (frozen settings, code version)
- Reliability / effort / time tables for all `(N, D)` cells
- `D_min(N)` and `B*(N)` curves with confidence bands
- Regime map with boundary estimates
- Failure-mode characterisation at boundaries

### Package P2 -- Transfer dossier (from Q3, Q4)

- Multi-method frontiers under locked protocol
- Transfer table (property × method: shared / shifted / absent)
- Scaling-shape summary with cross-method comparison
- Ranking stability analysis
- Motion-convention caveats

### Package P3 -- Substitution and predictor dossier (from Q5, Q6)

- Substitution curves and iso-reliability contours
- Predictor accuracy leaderboard (within-method and cross-method)
- Predictor failure-case catalogue

### Package P4 -- Robustness dossier (from Q7)

- Budget inflation tables under perturbations
- Regime-shift analysis relative to nominal baselines

These packages are the scientific outputs. HerdSim changes exist to make these packages reproducible.

---

## 10. Decision log

| Date | Decision |
|------|----------|
| 2026-09-16 | Research object reframed from dog count to multi-resource shepherding budget |
| 2026-09-16 | Spine questions set to Q1–Q4; Q5–Q6 amplifiers; Q7 deferred |
| 2026-09-16 | v1 budget inputs set to `B = (D, T)`; effort `E` treated as measured outcome |
| 2026-09-16 | Information quality kept as frontier-shifting factor, not a budget coordinate |
| 2026-09-16 | Agenda refined: terminology corrected, regime definitions operationalised, hypotheses added to all questions |
| pending | Freeze canonical task, θ, seed policy, instrument set (Section 6.1) |

---

## 11. Open decisions before protocol freeze

Confirm or revise:

1. **Canonical v1 task:** Drive to Goal?
2. **Reliability threshold:** `θ = 0.90` (with sensitivity at 0.50, 0.70)?
3. **Transfer instrument set:** `strombom_multi`, `kubo`, `fat`, `communication_free`?
4. **Flock sizes and shepherd counts:** `N ∈ {10, 25, 50, 100, 150, 200, 250, 300, 400}`, `D ∈ {1, 2, 3, 4, 6, 10, 15, 20, 25, 35}`?
5. **Time limit:** `T₀ = 10,000` ticks?
6. **Keep information outside `B` for v1?**

When confirmed, update Section 6.1 to status **frozen** and proceed to Phase 1 execution.
