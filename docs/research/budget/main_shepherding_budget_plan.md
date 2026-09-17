# Collective Herdability Under Shepherding

Status: active (Section 8 protocol frozen 2026-09-17)  
Role: single source of truth for the research program and HerdSim implementation  
Execution ledger (phases, Caps, campaigns, claim verdicts): [progress_tracker.md](progress_tracker.md)

This document defines (1) what must be scientifically established, (2) how each research question earns its place, and (3) what HerdSim must implement so the experiments can actually answer those questions. An implementation step is in scope only if it maps to an RQ, contribution, or evidence package below.

**Terminology convention.** Throughout this plan, *herdability* denotes the operational reliability of shepherding a collective to a goal. This is deliberately distinct from control-theoretic *controllability* (rank conditions, Gramian reachability) to avoid confusion. When referring to the shepherding algorithm that drives the dogs, this plan uses *herding method* or *instrument*, not "controller," to prevent conflation with the herdability concept. Code-level identifiers (`dog_controller`, `BaseDogController`) retain their current names for backward compatibility.

---

## Part I — Problem, Goal, and Contributions

### 1. Problem

Shepherding and related collective-nudging work usually asks: how many shepherds are needed for a flock of size N? That framing is too narrow for both science and operations. It treats flock size as the sole predictor and shepherd count as the sole resource, and therefore cannot answer the decisions operators actually face:

| Decision | What N-only sizing cannot answer |
|----------|----------------------------------|
| Force sizing | Two flocks of equal N can be easy or hard depending on cohesion, fragmentation, and spread |
| Adding robots | Extra shepherds can waste effort or reduce reliability; without regimes, "more is better" is untested |
| Sensor vs robot spend | Sensing and communication may substitute for headcount; the rate is unknown |
| Live monitoring | Failure is often recognised only at timeout; early state signals are unused |
| Method choice | Limits found on one herding method may or may not transfer |

The same decisions appear in livestock robotics, drone escort, crowd guidance, and autonomous convoy routing. The scientific gap is not "another herding heuristic." It is a missing account of what makes a collective *operationally herdable* under indirect shepherd influence.

### 1.1 Operational definition (keeps claims scientific)

In this program, **herdability** means the measured probability that a shepherding configuration drives the flock to its goal within the time and resource budget. This is deliberately *not* classical control-theoretic controllability (e.g., Kalman rank tests or Gramian-based reachability).

```text
A configuration is herdable at threshold θ when
R(m, τ, N, D, T, X₀, I) = P(success | locked seeds) >= θ.
```

| Term | Meaning in this plan |
|------|---------------------|
| Herdability | Operational reliability R ≥ θ of shepherding a flock to goal |
| Herding method / instrument | The shepherding algorithm that drives the dogs (e.g., `strombom_multi`, `kubo`) |
| Shepherd / dog | A physical or simulated agent that exerts repulsive influence on sheep |
| `dog_controller` | HerdSim code identifier for the herding-method plugin — retained for backward compatibility |

Claims are valuable only if they change this reliability, the minimum budget that achieves it, or the ability to anticipate its loss. Mechanism metrics (interference, coverage) are supporting explanations, not substitutes for R.

### 2. Goal

Determine what governs operational herdability of a cohesive collective under indirect shepherd influence.

Central hypothesis:

```text
Herdability = f(collective state, shepherding resources, information quality, interference, task)
```

Herdability is not determined by flock size alone. It depends on the interaction between the flock's measurable state and the effective shepherding capacity — a capacity limited by inter-shepherd interference, information, and coordination.

### 2.1 Why the research questions are scientifically valuable

Each RQ is kept only if it (a) closes a decision gap above, (b) has a falsifiable claim, and (c) produces an evidence package that HerdSim can emit. Rejection of a claim is still a scientific result: it bounds where N-only or D-only rules remain adequate.

Task τ₀ refers to `drive_to_goal`, the default shepherding scenario confirmed in Section 8.

| RQ | Scientific value (why ask) | What changes if supported | What changes if rejected |
|----|----------------------------|---------------------------|-----------------------|
| RQ1 | Tests whether N is a sufficient statistic | Force sizing must use flock state | N-only sizing remains adequate in the tested domain |
| RQ2 | Makes "works / fails / hurts" operational | Capacity planning uses regimes, not a single D | Monotonic "more dogs help" survives; no overcrowding taxonomy needed |
| RQ3 | Separates mechanism from phenomenology | Explains *why* returns diminish; guides herding-method or spacing rules | Overcrowding exists but is not interference/coverage-driven; revise mechanism |
| RQ4 | Prevents method-local overgeneralisation | States which limits are architecture-invariant | Treat results as instrument-specific |
| RQ5 | Quantifies sensor/robot substitution | Procurement can trade I for D at fixed R | Physical headcount dominates; information upgrades do not buy shepherds |
| RQ6 | Replaces anecdotal scale-up with fitted laws | Capacity scales with N and state | Simple global scaling (or N-only) remains competitive |
| RQ7 | Moves from post-hoc failure to anticipation | Live ops can act before timeout | State features add no lead time over (N, D) |

Minimum publishable scientific unit (first paper-scale cut): **RQ1 + RQ2 + RQ3 + S8**. RQ4–RQ7 are staged extensions that reuse the same protocol; they are not required to justify starting Phase 1.

### 3. Research questions

| ID | Question | Core contribution | Evidence package |
|----|----------|-------------------|------------------|
| RQ1 | Does collective state (cohesion, fragmentation, spread) change herdability at fixed N? | S1 | B |
| RQ2 | Where is the boundary between reliable and unreliable herding, and how sharp is it? | S2 | A |
| RQ3 | Why does adding shepherds eventually stop helping or start hurting? | S3 | C |
| RQ4 | Which herdability mechanisms are general across herding methods? | S4 | D |
| RQ5 | Can better information substitute for additional physical shepherds? | S5 | E |
| RQ6 | How does required shepherding resource scale with flock size and collective state? | S6 | F |
| RQ7 | Can current collective state predict imminent herding failure? | S7 | G |

### 3.1 Evidence packages

Each evidence package is an exportable dataset that enables the matching claims to be evaluated.

| Package | Contents | Produced by |
|---------|----------|-------------|
| A | Reliability maps R(N, D), frontier curves (D_min, D_overcrowd, D_max, B*), regime labels, provenance stamp | Phase 1 grid campaign |
| B | Per-(N, X₀, D) reliability, D_min(N, X₀) comparisons, predictor-comparison tables | Phase 2 X₀-manipulation campaign |
| C | Per-trial I_dir(t) and C(t) time series, regime-paired rank tests, mechanism-hypothesis verdicts | Phase 3 mechanism campaign |
| D | Transfer table: property × method → shared / shifted / absent | Phase 4 multi-instrument campaign |
| E | D_min(N, I) curves, substitution rates ΔD_min/ΔI, instrument-conditional notes | Phase 5 factor sweep |
| F | Scaling model fits (power-law, piecewise, state-conditioned), ΔAIC/BIC tables | Phase 6 analysis |
| G | AUROC, lead-time distributions, feature-importance ranks | Phase 7 early-warning analysis |

### 4. Contributions

**Scientific contributions:**

| ID | Contribution | Type | Valuable because |
|----|-------------|------|------------------|
| S1 | Collective-state principle: herdability depends on measurable flock state beyond N | Empirical | Falsifies N-only sufficiency |
| S2 | Herdability regimes: taxonomy with operationalised boundaries | Empirical | Turns reliability maps into actionable capacity bands |
| S3 | Interference–coverage mechanism: explains non-monotonic returns to shepherd count | Empirical + mechanistic | Distinguishes waste, conflict, and hard failure |
| S4 | Cross-method transfer: identifies which mechanisms are method-invariant | Empirical | Bounds external validity |
| S5 | Information–shepherding substitution: quantified tradeoff between sensing and headcount | Empirical + applied | Links I to D_min at fixed R |
| S6 | State-conditioned scaling: scaling laws that depend on collective state, not N alone | Empirical | Supports growth planning |
| S7 | Early warning: predictive indicators of impending herding failure | Empirical + applied | Tests anticipatory value of X(t) |
| S8 | Reproducible protocol: locked tasks, seeds, metrics, and provenance on HerdSim | Infrastructure | Makes S1–S7 auditable and repeatable |

**Practical contributions:**

| ID | Application | Depends on |
|----|-------------|------------|
| P1 | Size a shepherding force by flock state, not only by N | S1, S6 |
| P2 | Detect when extra shepherds waste effort or reduce reliability | S2, S3 |
| P3 | Trade sensors and communication against extra robots | S5 |
| P4 | Monitor operations for early loss-of-herding signals | S7 |
| P5 | Know which operational limits depend on the herding method | S4 |
| P6 | Plan capacity as flocks grow, using state-conditioned scaling | S6 |

**Target claim (to be supported or refuted):**

Equal-sized collectives can differ in herdability; extra shepherds can saturate and interfere; information can substitute for physical shepherds within bounds; scaling depends on collective state; and loss of herding can be anticipated from measurable state.

This compound claim is the program-level thesis. Individual papers or phases may support only a subset; each subset must still map to falsifiable claims C1a–C7b.

---

## Part II — Measurement Framework

### 5. Notation and budget structure

**Reliability (herdability score):**

```text
R(m, τ, N, D, T, X₀, I) = P(success | locked seeds)
```

A setting is herdable at threshold θ when R ≥ θ.  
Default: θ = 0.90. Sensitivity: also report at θ ∈ {0.50, 0.70}.

**Budget inputs** (set before a trial begins):

| Symbol | Meaning |
|--------|---------|
| D | Shepherd count |
| T | Time limit (ticks) |

**Measured outcomes** (observed after a trial):

| Symbol | Meaning |
|--------|---------|
| S | Success (binary) |
| t_s | Time to success (ticks, if successful) |
| E | Realised effort: total shepherd path length |
| X(t) | Collective-state trajectory over time |

**Context variables** (experimental conditions, not optimised):

| Symbol | Meaning |
|--------|---------|
| N | Flock size |
| m | Herding method (instrument) |
| τ | Task (scenario + success rule); τ₀ = `drive_to_goal` |
| X₀ | Initial collective-state family (compact, wide, split, outlier-rich) |
| I | Information condition (observation mode, sensing range, communication) |

### 6. Collective state and mechanism metrics

**Collective-state variables X(t):**

| Variable | Definition | HerdSim source |
|----------|-----------|----------------|
| Cohesion | Mean Euclidean distance of sheep to flock centroid (GCM) | `metrics/cohesion.py` — exists |
| Fragmentation | Largest connected-component fraction under measurement radius | `metrics/fragmentation.py` — exists |
| Outlier count | Sheep beyond the lost-distance threshold | `metrics/outlier_count.py` — exists |
| Spread | Variance of sheep distances to centroid (mean-spread S̄) | `metrics/mean_spread.py` — **to add** |
| Extent | Radius of gyration: RMS distance to centroid | `metrics/extent.py` — **to add** |

Secondary (add only if primary variables are insufficient as predictors):

- Cluster count (DBSCAN)
- Velocity variance
- Shape elongation (ratio of principal component eigenvalues)

**Mechanism metrics (for RQ3 and RQ7):**

| Metric | Definition | Interpretation |
|--------|-----------|----------------|
| Interference index I_dir(t) | `1 − ‖Σᵢ ûᵢ(t)‖ / M_active` where ûᵢ is shepherd i's unit velocity direction and M_active is the count of moving shepherds | 0 = all moving shepherds are coherent; 1 = maximal conflict |
| Coverage C(t) | Fraction of peripheral sheep within at least one shepherd's influence radius | Low C = under-covered flock; plateau in C suggests coverage saturation |

Peripheral sheep = sheep whose distance to centroid exceeds the median distance.

**I_dir stationary-shepherd rule:** A shepherd with speed below ε = 1 × 10⁻⁶ world-units/tick is classified as *stationary* and excluded from both the numerator sum and M_active. If all shepherds are stationary in a tick, I_dir(t) = 0 by convention (no conflict is possible when nobody moves). This prevents division by zero and avoids inflating interference when a shepherd pauses to switch between collect and drive phases.

**Implementation note on I_dir:** HerdSim stores realised velocities (post-constraint) in [SimulationState](file:///home/quyen/HerdSim/core/simulation_state.py). The herding method's *intended* direction is not separately recorded. For v1, compute I_dir from realised velocities and document the caveat that wall reflections can inflate I_dir near boundaries. If RQ3 analysis shows wall effects confound the mechanism signal, add `shepherd_intended_velocities` to SimulationState (see Section 13, exception E1).

**Frontier quantities (computed from trial aggregates):**

| Quantity | Definition |
|----------|-----------:|
| D_min(N, X₀) | Smallest D with R ≥ θ |
| D_overcrowd(N, X₀) | Smallest D > D_min at which R begins a sustained decline: R drops below θ for ≥ 2 consecutive entries in the *ordered D grid* (e.g., if the grid is {1,2,3,4,6,10,…}, then D=10 and D=15 are consecutive even though they differ by 5) |
| D_max(N, X₀) | Largest D still achieving R ≥ θ (if overcrowding occurs) |
| B*(N, X₀) | Budget (D, T) achieving R ≥ θ at minimum median effort E; ties by smaller D, then faster t_s |

**D_min identification procedure:**
1. Scout sweep: 30 seeds per cell across the full (N, D) grid
2. Identify boundary cells: the first D (in grid order) where R > 0.80 and the first D where R < 0.95
3. Rerun boundary cells with 100 seeds
4. D_min = smallest D where 100-seed R ≥ θ
5. Report bootstrap 95% CI on D_min (resample the 100 seeds, 1,000 iterations)

**Herdability regimes:**

| Regime | Operational definition |
|--------|----------------------|
| Under-budget failure | R(c) < θ (insufficient resources) |
| Efficient operation | R(c) ≥ θ, D at or near D_min, effort competitive |
| Wasteful overspend | R(c) ≥ θ, but median E exceeds efficient level by ≥ 20% without reliability gain |
| Overcrowding collapse | R(c) drops below θ for D > D_overcrowd |
| Hard failure | No tested D achieves R ≥ θ within T |

Wasteful-overspend threshold: default 20%; sensitivity at 10% and 30%.

---

## Part III — Research Questions in Detail

### RQ1 — Collective state beyond N

**Question:** Does the same flock size have different herdability under different initial collective states?

**Why this RQ is valuable:** If true, N is not a sufficient statistic for herdability. That is the core scientific justification for measuring X(t) at all. Causal manipulation of X₀ (not only correlating emergent spread with success) is required so state is an independent factor, not a by-product of D or failure.

**Approach:**
- Fix N in {50, 100, 200}
- Generate X₀ families: compact, wide, split, outlier-rich (see Section 11.1)
- Sweep D in {1, 2, 3, 4, 6, 10, 15, 20, 25, 35} for each (N, X₀) pair
- Compare D_min(N, X₀) across X₀ families
- Fit R ~ f(N, D, cohesion, fragmentation, outliers) and compare out-of-sample log-likelihood (and ΔAIC) against R ~ f(N, D) alone

**Falsifiable claims:**
- **C1a:** For at least one N, D_min differs by ≥ 2 shepherds across X₀ families at θ = 0.90
- **C1b:** A model including collective-state features predicts trial reliability better (out-of-sample log-likelihood and ΔAIC > 4) than (N, D) alone

**HerdSim must provide:** X₀ generators wired into the locked scenario; cohesion, fragmentation, outlier, mean-spread (and extent) metrics; frontier extraction of D_min; predictor comparison module.

### RQ2 — Herdability boundary and regimes

**Question:** Where does reliable herding end as D increases, and how sharp is that boundary?

**Why this RQ is valuable:** Without operational regimes, "add more shepherds" remains an untested heuristic. Mapping R(N, D) into under-budget / efficient / wasteful / overcrowding / hard-failure makes capacity decisions scientific rather than anecdotal.

**Approach:**
- Build reliability maps over (N, D) at fixed T₀ = 10,000 ticks
- Label regimes using the definitions in Section 6
- Measure transition width: how many D-steps (in grid order) the efficient-to-overcrowding transition spans
- Test whether increasing T beyond T₀ restores herding in overcrowding cells

**Falsifiable claims:**
- **C2a:** Overcrowding (reliability decline with increasing D) appears for at least two herding methods at θ = 0.90
- **C2b:** For at least one (N, X₀), there exists a D > D_overcrowd that remains unreliable (R < θ) even when T is extended to T₁ = 20,000 ticks (a hard ceiling on herdability for that configuration, not merely a timeout artefact)

**HerdSim must provide:** budget grid runner with provenance; frontier (D_min, D_overcrowd, D_max, B*); regime labelling; Package A export.

### RQ3 — Mechanism of diminishing and negative returns

**Question:** Why do extra shepherds stop helping? What causes overcrowding collapse?

**Why this RQ is valuable:** Phenomenology (RQ2) alone does not tell operators or designers what to change. Mechanism tests decide whether the fix is spacing/assignment (interference), peripheral coverage, fragmentation management, or simply stopping overspend.

**Tested hypotheses:**

| Hypothesis | Expected signature |
|------------|-------------------|
| Interference | I_dir rises with D *before* reliability falls |
| Coverage saturation | C plateaus while effort E keeps rising |
| Induced fragmentation | Fragmentation rises in overcrowding cells vs efficient cells |
| Redundant effort | Effort rises, reliability flat, I_dir not necessarily high |

**Approach:**
- For overcrowding and efficient cells at the same N, compute per-trial I_dir and C time series
- Compare median I_dir (and fragmentation) with rank tests
- Trace temporal order: does I_dir or fragmentation rise before the reliability drop?

**Expected causal pathway:**

```text
More shepherds -> coverage saturation + interference
              -> flock fragmentation or oscillation
              -> reliability drop
```

**Falsifiable claim:**
- **C3:** Overcrowding cells have significantly higher median I_dir and/or fragmentation than efficient cells at the same N (rank test p < 0.05, multiple-comparison corrected)

**HerdSim must provide:** shepherd_interference and shepherd_coverage metrics; mechanism hypothesis tests; caveat documented if I_dir uses realised velocities.

### RQ4 — Cross-method generality

**Question:** Which herdability mechanisms are shared across herding architectures?

**Why this RQ is valuable:** Results on one instrument are not scientific laws. Transfer labels (shared / shifted / absent) bound external validity and stop overclaiming.

**Herding methods under locked task, seeds, and metrics:**
- Required: `strombom_multi`, `kubo`, `fat`
- Recommended: `communication_free`
- Optional: `v_formation`, `adaptive`

**Properties to compare:**

| Property | Transfer labels |
|----------|----------------|
| State-dependent D_min (RQ1 effect) | **shared**: same qualitative pattern with |ΔD_min| ≤ 2; **shifted**: same direction but |ΔD_min| > 2; **absent**: no significant effect |
| Overcrowding regime (RQ2 existence) | **shared**: overcrowding at comparable D/N ratio (within factor 1.5×); **shifted**: overcrowding exists but at substantially different D; **absent**: no overcrowding observed |
| Interference signature (RQ3 I_dir pattern) | **shared**: I_dir–reliability correlation r < −0.3 in both; **shifted**: correlation present but magnitude differs; **absent**: no significant correlation |
| Coverage saturation (RQ3 C plateau) | shared / shifted / absent (analogous thresholds) |
| Information substitution (RQ5 pattern) | shared / shifted / absent |
| Early-warning features (RQ7 predictors) | shared / shifted / absent |

**Falsifiable claim:**
- **C4:** At least one core mechanism (overcrowding, interference, or coverage saturation) receives the **shared** label across ≥ 3 of the 4 required+recommended herding methods

**HerdSim must provide:** multi-instrument grid runs under identical τ, seeds, metrics; transfer table builder.

### RQ5 — Information versus physical shepherding

**Question:** Can better sensing or communication reduce the required shepherd count at fixed reliability?

**Why this RQ is valuable:** If information substitutes for dogs at fixed R, the budget is multi-resource, not D-only. That is the scientific basis for P3. Substitution must be measured as ΔD_min / ΔI, and only for instruments that consume the varied observation/communication factors.

**Approach:**
- Fix N in {100, 200}, θ = 0.90
- Define the information ladder (ordered from least to most informative):
  - Observation mode: bearing_only → local_positions → global (3 ordinal levels)
  - Sensing range: ×0.5 → ×1.0 → ×1.5 → ×2.0 of default (4 ordinal levels)
  - Communication: none → neighbour_broadcast → global_shared (3 ordinal levels)
- For each information level I_k, compute D_min(N, I_k)
- "First improvement" = the D_min change from the lowest to the second level on each ladder
- "Second improvement" = the D_min change from the second to the third level
- Estimate substitution rate ΔD_min / ΔI_level

**Falsifiable claims:**
- **C5a:** At least one step up the information ladder reduces D_min by ≥ 1 at N ∈ {100, 200} while R ≥ θ
- **C5b:** The second step up the same ladder saves fewer shepherds than the first step (diminishing returns along the information axis)

**HerdSim must provide:** factor-sweep runner over existing observation/communication factors; substitution curves; instrument-conditional reporting when a factor is ignored by a herding method.

### RQ6 — Scaling regimes

**Question:** How does required shepherding resource grow with N and collective state?

**Why this RQ is valuable:** Operators need growth laws, not single-N anecdotes. State-conditioned scaling is only justified if RQ1 holds; otherwise report N-only scaling and stop.

**Approach:**
- Compute D_min(N, X₀) for each X₀ family across N in {25, 50, 75, 100, 150, 200, 300, 400}
- Fit power-law, piecewise-linear, and state-conditioned candidates; compare with AIC/BIC and cross-validation
- Test across herding methods after RQ4 data exist

**Falsifiable claims:**
- **C6a:** A single global power law is rejected in favour of piecewise or state-conditioned models (ΔAIC > 10), OR
- **C6b:** A stable sublinear regime (α < 1) exists within a stated domain of N and X₀

**HerdSim must provide:** scaling fit module consuming Packages A/B; no new simulator physics.

### RQ7 — Early warning of herding failure

**Question:** Can measurable collective state predict impending failure before the trial ends?

**Why this RQ is valuable:** Post-hoc failure labels do not help live operations. Predictive lead time from X(t), I_dir, and C is the scientific test of anticipatory value. Only run after RQ1–RQ3 metrics exist and failure trajectories are plentiful.

**Approach:**
- At time t, extract windowed features of X(t), I_dir(t), C(t)
- Predict P(failure within k ticks | features at t); baseline = logistic on (N, D)
- Evaluate with leave-one-N-out cross-validation

**Design parameters** (freeze in Phase 0):
- Prediction horizon k: 500 ticks (5% of T₀)
- Feature window w: 200 ticks
- Evaluation points: every 200 ticks from tick 1,000 to tick 8,000

**Falsifiable claims:**
- **C7a:** State-based warning achieves higher AUROC than (N, D)-only prediction on held-out trials
- **C7b:** Useful warning lead time (≥ 500 ticks before failure) exists on ≥ 30% of failure trajectories

**HerdSim must provide:** early-warning feature export from trial histories; prediction and lead-time evaluation module.

---

## Part IV — Experimental Protocol

### 8. Protocol defaults (freeze in Phase 0)

| Item | Default | Status |
|------|---------|--------|
| Task τ₀ | `drive_to_goal` | frozen |
| Reliability θ | 0.90 (also report 0.50, 0.70) | frozen |
| Baseline herding method | `strombom_multi` | frozen |
| Transfer herding methods | `strombom_multi`, `kubo`, `fat`, `communication_free` | frozen |
| Flock sizes N | {25, 50, 75, 100, 150, 200, 300, 400} | frozen |
| Shepherd counts D | {1, 2, 3, 4, 6, 10, 15, 20, 25, 35} | frozen |
| X₀ families | compact, wide, split, outlier_rich | frozen |
| Time limit T₀ | 10,000 ticks (overrides scenario default 3,000) | frozen |
| Extended time limit T₁ | 20,000 ticks (for C2b hard-ceiling test) | frozen |
| Scout seeds | 30 per cell | frozen |
| Claim-grade seeds | 100 on boundary cells | frozen |
| RQ5 factors | obs mode, sensing range, communication mode | frozen |
| RQ7 prediction horizon k | 500 ticks | frozen |
| Master seed | 2026 | frozen |

### 9. Phase plan

| Phase | Focus | Questions | Output | Depends on | Phase done when |
|-------|-------|-----------|--------|------------|-----------------|
| 0 | Freeze protocol | -- | Confirmed Section 8 | -- | All rows in Section 8 marked frozen |
| 1 | Herdability maps (baseline) | RQ2, data for RQ6 | Package A | Phase 0 | C2 claims evaluable on baseline method; frontier+regimes exported |
| 2 | Collective-state manipulation | RQ1 | Package B | Phase 1 | C1a/C1b evaluable; X₀ families verified by metric stats |
| 3 | Overcrowding mechanism | RQ3 | Package C | Phase 1 | C3 evaluable; I_dir and C time series stored |
| 4 | Cross-method transfer | RQ4 | Package D | Phases 1–3 | Transfer table filled for ≥ 3 herding methods |
| 5 | Information substitution | RQ5 | Package E | Phase 1 | C5a/C5b evaluable on instruments that consume I factors |
| 6 | Scaling regimes | RQ6 | Package F | Phases 1–2 | C6a or C6b decided with model comparison table |
| 7 | Early warning | RQ7 | Package G | Phases 1–3 | C7a/C7b evaluable with reported lead-time distribution |

---

## Part V — HerdSim Implementation Guide

### 10. Design principles

1. **Additive, not invasive.** New modules over core rewrites. Extend BaseMetric and wrap `iter_one_trial()`.
2. **Composable analysis.** Every analysis function is `DataFrame -> DataFrame`. No hidden state.
3. **Reproducible by default.** Every campaign exports a provenance stamp (git hash, config hash, seed list, metric versions).
4. **Phase-gated.** Build and test each phase's tooling before running experiments. Do not pre-build later phases.
5. **Traceability gate.** Do not merge HerdSim work unless it maps to a row in Section 10.1. Orphan tooling is out of scope.

### 10.1 Traceability: RQ to HerdSim capability (implementation must meet the plan)

HerdSim meets this plan when every required capability below exists, is tested, and is used by the matching evidence package. Status is relative to the current codebase at plan time.

| Cap | Serves | Capability | HerdSim location | Status | Package |
|-----|--------|------------|------------------|--------|---------|
| I1 | RQ2, RQ6 | N × D × seed grid runner with resume + provenance | `api/budget_runner.py`, `analysis/budget/provenance.py` | built | A, F |
| I2 | RQ2 | Frontier extraction D_min, D_overcrowd, D_max, B* | `analysis/budget/frontier.py` | built | A |
| I3 | RQ2 | Regime labelling | `analysis/budget/regimes.py` | built | A |
| I4 | RQ1, RQ6, RQ7 | Mean-spread and extent metrics | `metrics/mean_spread.py`, `metrics/extent.py` | built | B, F, G |
| I5 | RQ1 | X₀ generators + scenario wiring | `core/x0_generators.py`; update `drive_to_goal` + `INITIAL_LAYOUTS` | built | B |
| I6 | RQ1 | State vs (N, D) predictor comparison | `analysis/budget/predictors.py` | built | B |
| I7 | RQ3, RQ7 | Interference I_dir and coverage C metrics | `metrics/shepherd_interference.py`, `metrics/shepherd_coverage.py` | built | C, G |
| I8 | RQ3 | Mechanism hypothesis tests | `analysis/budget/mechanism.py` | built | C |
| I9 | RQ4 | Locked multi-instrument campaigns + transfer table | `analysis/budget/transfer.py` | built | D |
| I10 | RQ5 | Factor sweeps (obs, range, communication) + substitution curves | `scripts/budget/run_factor_sweep.py`, `analysis/budget/substitution.py` | built | E |
| I11 | RQ6 | Scaling model fits | `analysis/budget/scaling.py` | built | F |
| I12 | RQ7 | Early-warning features and evaluation | `analysis/budget/early_warning.py` | built | G |
| I13 | S8 | Canonical protocol config + dossier export | `configs/budget/canonical_grid.yaml`, `analysis/budget/export.py` | built | all |
| I14 | RQ3, RQ7 | Per-trial time-series storage (Parquet) | `api/budget_runner.py` (write path) | built | C, G |

**Already available (do not rebuild):** cohesion, fragmentation, outlier_count metrics; `iter_one_trial` / Experiments path; observation modes and communication factor injection in the simulation runner; instrument presets listed in RQ4; failure taxonomy via benchmark runner.

**Acceptance rule:** Phase k implementation is complete only when its Cap row(s) are built, unit-tested, and the phase "done when" criterion in Section 9 is met. Running campaigns without the matching Cap does not count as answering the RQ.

### 11. What to build

#### 11.1 X₀ generators (Phase 2, but spec needed at Phase 0)

**File:** `core/x0_generators.py` [NEW]  
**Capability:** I5 (required for RQ1)

The `initial_layout` factor in [ExperimentalFactors](file:///home/quyen/HerdSim/core/experimental_factors.py#L34) is declared but **not implemented** — [DriveToGoalScenario.initial_positions()](file:///home/quyen/HerdSim/scenarios/drive_to_goal.py#L58-L77) always generates a single cluster regardless of the layout value. This must be fixed for RQ1.

**Design:** Create a standalone generator that scenarios call, rather than embedding layout logic in each scenario.

```python
def generate_initial_positions(
    n_sheep: int,
    layout: str,         # "compact" | "wide" | "split" | "outlier_rich"
    center: np.ndarray,
    rng: np.random.Generator,
    **kwargs,
) -> np.ndarray:
    """Generate sheep positions for a named X₀ family."""
```

| Layout (plan) | Factor value stored | Definition | Key parameter |
|---------------|---------------------|------------|---------------|
| `compact` | `compact` (alias: legacy `cluster` → `compact`) | Single Gaussian cluster, σ = 0.3 × default spread | Low cohesion distance |
| `wide` | `wide` | Single Gaussian cluster, σ = 2.0 × default spread | High cohesion distance |
| `split` | `split` | 2–3 separated subclusters at distance ≥ 2× interaction radius | Low fragmentation index |
| `outlier_rich` | `outlier_rich` | Core cluster (80%) + outliers (20%) beyond lost threshold | High outlier count |

Update `INITIAL_LAYOUTS` in [experimental_factors.py](file:///home/quyen/HerdSim/core/experimental_factors.py) to `("compact", "wide", "split", "outlier_rich")` and accept legacy `"cluster"` as an alias for `"compact"`. The `validate()` method checks membership in the `INITIAL_LAYOUTS` tuple, so updating the tuple is sufficient — no separate validation change is needed, but verify that existing configs using `"cluster"` still pass by mapping the alias before validation. Update `DriveToGoalScenario.initial_positions()` to call this generator when `initial_layout` is set.

**RQ1 gate:** unit tests must verify that sampled layouts differ on the intended metric (cohesion for compact/wide; fragmentation for split; outlier_count for outlier_rich) before any claim-grade campaign.

#### 11.2 New metrics (Phase 1–3)

| Metric | File | Phase | Cap | Serves |
|--------|------|-------|-----|--------|
| Mean spread (variance of distances to centroid) | `metrics/mean_spread.py` [NEW] | 1 | I4 | RQ1, RQ6, RQ7 |
| Extent (radius of gyration: RMS distance to centroid) | `metrics/extent.py` [NEW] | 1 | I4 | RQ1, RQ6 |
| Shepherd interference I_dir | `metrics/shepherd_interference.py` [NEW] | 3 | I7 | RQ3, RQ7 |
| Shepherd coverage C | `metrics/shepherd_coverage.py` [NEW] | 3 | I7 | RQ3, RQ7 |

**Conditional** (add only if primary state variables are insufficient as predictors):
- Cluster count (DBSCAN)
- Convex hull area
- Velocity variance

Register all new metrics in [metrics/registry.py](file:///home/quyen/HerdSim/metrics/registry.py).

**I_dir implementation specification:**

```python
def compute(self, state: SimulationState) -> float:
    vels = state.shepherd_velocities                    # shape (M, 2)
    speeds = np.linalg.norm(vels, axis=1)               # shape (M,)
    moving = speeds > 1e-6                              # stationary threshold
    m_active = int(moving.sum())
    if m_active == 0:
        return 0.0                                      # no conflict when nobody moves
    unit_vecs = vels[moving] / speeds[moving, np.newaxis]
    resultant = np.linalg.norm(unit_vecs.sum(axis=0))
    return 1.0 - resultant / m_active
```

Compute from `state.shepherd_velocities` (realised, post-constraint). Document caveat: wall reflections ([simulation_runner.py L176-178](file:///home/quyen/HerdSim/core/simulation_runner.py#L176-L178)) may inflate I_dir near boundaries. If RQ3 analysis shows this is a confound, upgrade by recording intended velocities in SimulationState (see Section 13, exception E1).

**Coverage implementation note:** "Peripheral sheep" = sheep whose distance to centroid exceeds the median distance. Influence radius = `r_s` read from `state.metadata.get("r_s", 2.0)` (populated by [SimulationRunner.initialize()](file:///home/quyen/HerdSim/core/simulation_runner.py#L85)), not from the scenario config.

#### 11.3 Campaign infrastructure (Phase 1)

| Component | File | Purpose |
|-----------|------|---------|
| Canonical grid config | `configs/budget/canonical_grid.yaml` [NEW] | Machine-readable protocol defaults |
| Budget grid runner | `api/budget_runner.py` [NEW] | N×D×seed campaigns with resumability and provenance |
| Provenance stamps | `analysis/budget/provenance.py` [NEW] | Git hash, config hash, seed list, timestamps |
| Frontier extraction | `analysis/budget/frontier.py` [NEW] | D_min, D_overcrowd, D_max, B* |
| Regime labelling | `analysis/budget/regimes.py` [NEW] | Assigns regime labels to (N, D) cells |
| Export / dossier | `analysis/budget/export.py` [NEW] | CSV + markdown report per package |

The grid runner wraps [iter_one_trial()](file:///home/quyen/HerdSim/api/benchmark_runner.py#L77) from the existing benchmark runner. It does NOT modify the benchmark runner.

**Resumability:** On startup, scan `output_dir` for completed `(N, D, seed)` tuples and skip them. Critical because a full grid (8 × 10 × 30 = 2,400 trials) can take hours. Implement a JSON manifest (e.g., `output_dir/manifest.jsonl`) that appends one line per completed trial with keys `{N, D, seed, status, timestamp}`. On resume, load the manifest and skip listed triples.

**T₀ override:** The canonical grid config MUST set `max_ticks: 10000` to override the scenario default of 3,000 ([drive_to_goal.py L41](file:///home/quyen/HerdSim/scenarios/drive_to_goal.py#L41)). The override flows through `algorithm_params` → `resolve_experiment_config`. Verify this path in a smoke test before any campaign: run one trial with the canonical config and assert `result.total_ticks <= 10000` and `result.total_ticks > 3000` (for a trial that runs to timeout).

#### 11.4 Per-trial time-series storage (Phase 1, extended in Phase 3)

**Capability:** I14

RQ3 and RQ7 require per-tick mechanism metrics (I_dir, C) and collective-state trajectories, not just scalar summaries. The grid runner must store per-trial time-series data.

**Format:** Apache Parquet, one file per trial.

```
results/budget/<campaign_id>/timeseries/N{n}_D{d}_seed{s}.parquet
```

**Columns (Phase 1):** `tick, cohesion, fragmentation, outlier_count, mean_spread, extent`

**Columns (Phase 3, added when I7 is built):** `+ i_dir, coverage`

**Storage budget:** ~10,000 ticks × 8 columns × 8 bytes ≈ 640 KB per trial (Parquet compresses ~5×, so ~130 KB). Full scout sweep (9,600 trials): ~1.2 GB. Manageable.

**Implementation:** After `iter_one_trial()` yields the final `"trial"` event, extract `result.history` (the [HistoryRecorder](file:///home/quyen/HerdSim/core/history_recorder.py) DataFrame) and write it to Parquet. The recorder already stores all registered metrics per tick.

#### 11.5 Analysis modules (Phases 2–7)

| Module | File | Phase | Serves |
|--------|------|-------|--------|
| Transfer table builder | `analysis/budget/transfer.py` [NEW] | 4 | RQ4 |
| Mechanism hypothesis tests | `analysis/budget/mechanism.py` [NEW] | 3 | RQ3 |
| Substitution curves | `analysis/budget/substitution.py` [NEW] | 5 | RQ5 |
| Scaling model fitting | `analysis/budget/scaling.py` [NEW] | 6 | RQ6 |
| Early-warning models | `analysis/budget/early_warning.py` [NEW] | 7 | RQ7 |
| Predictor evaluation | `analysis/budget/predictors.py` [NEW] | 2 | RQ1, RQ6 |

#### 11.6 Parallelisation strategy

A full scout sweep for one herding method is 8 (N) × 10 (D) × 4 (X₀) × 30 (seeds) = 9,600 trials. At T₀ = 10,000 ticks each, single-core execution is infeasible.

**Design:** The budget grid runner uses `concurrent.futures.ProcessPoolExecutor` with configurable `max_workers` (default: `os.cpu_count() - 1`).

- Each worker calls `iter_one_trial()` for one `(N, D, X₀, seed)` tuple — this function is self-contained and process-safe (its own RNG seeded by the trial seed).
- The main process collects results, appends to the manifest, and writes Parquet files.
- Resumability interacts cleanly: the manifest is append-only and flushed after each trial.
- For cluster execution, provide a `scripts/budget/submit_slurm.py` template that partitions the grid into array-job tasks. This is optional and not gated by any Phase; add it when a cluster is available.

**Thread safety note:** `iter_one_trial()` creates its own `SimulationRunner` with a per-trial RNG. No shared mutable state exists. Verified: [simulation_runner.py](file:///home/quyen/HerdSim/core/simulation_runner.py) uses only instance variables.

#### 11.7 Diagnostic visualisation (Phase 1, extended per phase)

| Plot | Module | Phase | Serves |
|------|--------|-------|--------|
| Reliability heatmap R(N, D) | `analysis/budget/plots.py` | 1 | RQ2, debugging |
| Frontier overlay D_min(N) with CI | `analysis/budget/plots.py` | 1 | RQ2, RQ6 |
| I_dir time-series overlay (efficient vs overcrowding) | `analysis/budget/plots.py` | 3 | RQ3 |
| Substitution curve D_min vs I_level | `analysis/budget/plots.py` | 5 | RQ5 |
| Scaling fits (data + candidate curves) | `analysis/budget/plots.py` | 6 | RQ6 |
| ROC curves (state-based vs baseline) | `analysis/budget/plots.py` | 7 | RQ7 |

These are diagnostic and paper-ready. Build each plot when the matching phase data exists.

#### 11.8 CLI entry points

| Script | Purpose |
|--------|---------|
| `scripts/budget/run_grid.py` | Run single or multi-instrument N×D campaigns |
| `scripts/budget/run_factor_sweep.py` | Sensing/communication sweeps for RQ5 |
| `scripts/budget/analyse.py` | Extract frontiers, regimes, transfer tables from completed campaigns |

### 12. Module layout

```
HerdSim/
├── analysis/budget/           [NEW — all budget-specific analysis]
│   ├── __init__.py
│   ├── provenance.py          Phase 0
│   ├── frontier.py            Phase 1
│   ├── regimes.py             Phase 1
│   ├── export.py              Phase 1
│   ├── plots.py               Phase 1+
│   ├── mechanism.py           Phase 3
│   ├── transfer.py            Phase 4
│   ├── substitution.py        Phase 5
│   ├── scaling.py             Phase 6
│   ├── predictors.py          Phase 2
│   └── early_warning.py       Phase 7
├── api/
│   ├── benchmark_runner.py    [UNCHANGED — wrapped, not modified]
│   └── budget_runner.py       [NEW]
├── configs/budget/            [NEW]
│   └── canonical_grid.yaml
├── core/
│   ├── x0_generators.py       [NEW — X₀ family generation]
│   └── ...                    [existing files unchanged; see Section 13 exception E1]
├── metrics/
│   ├── mean_spread.py         [NEW — Phase 1]
│   ├── extent.py              [NEW — Phase 1]
│   ├── shepherd_interference.py [NEW — Phase 3]
│   ├── shepherd_coverage.py   [NEW — Phase 3]
│   └── ...                    [existing metrics unchanged]
├── scripts/budget/            [NEW]
│   ├── run_grid.py
│   ├── run_factor_sweep.py
│   └── analyse.py
├── results/budget/            [NEW — gitignored output]
│   └── <campaign_id>/
│       ├── manifest.jsonl
│       ├── summary.csv
│       └── timeseries/        [per-trial Parquet files]
└── tests/
    ├── test_budget_frontier.py [NEW]
    ├── test_budget_regimes.py  [NEW]
    ├── test_budget_runner.py   [NEW]
    ├── test_x0_generators.py   [NEW]
    └── test_budget_smoke.py    [NEW]
```

### 13. What is NOT modified

| Module | Reason |
|--------|--------|
| `core/simulation_runner.py` | Grid runner wraps it |
| `core/experiment_config.py` | Config resolution is already flexible |
| `analysis/herdability.py` | Superseded by frontier.py but kept for backward compatibility |
| `analysis/failure_taxonomy.py` | Already integrated via benchmark_runner |
| `algorithms/*` | We study existing instruments as-is |
| `dynamics/*` | No sheep/dog model changes |

**Minimal changes to existing files:**
- `core/experimental_factors.py`: update `INITIAL_LAYOUTS` to `("compact", "wide", "split", "outlier_rich")`; add alias mapping so `"cluster"` is accepted and silently mapped to `"compact"` before validation
- `scenarios/drive_to_goal.py`: call `x0_generators.generate_initial_positions()` when `initial_layout` is set
- `metrics/registry.py`: register new metric classes

**Exception E1 — conditional core change (shepherd intended velocities):**

If RQ3 mechanism analysis reveals that wall reflections inflate I_dir to the point of confounding the interference signal (assessed visually and with a boundary-distance correlation test), then add an optional field `shepherd_intended_velocities: np.ndarray | None = None` to [SimulationState](file:///home/quyen/HerdSim/core/simulation_state.py). This field would be populated by the herding-method plugin *before* constraint application and wall reflection. The interference metric would then use intended velocities instead of realised ones.

This is the *only* permitted core-module change. It is gated behind an empirical finding and must not be pre-built.

### 14. Build order

| Step | What | Caps | Tests | Phase |
|------|------|------|-------|-------|
| 0.1 | `canonical_grid.yaml` | I13 | Manual review | 0 |
| 0.2 | `provenance.py` | I1, I13 | Unit test | 0 |
| 1.1 | `mean_spread.py`, `extent.py` + registry | I4 | Unit tests | 1 |
| 1.2 | `budget_runner.py` (single instrument, with parallelisation + manifest) | I1, I14 | Integration test (tiny grid) | 1 |
| 1.3 | `frontier.py` | I2 | Unit test with synthetic data | 1 |
| 1.4 | `regimes.py` | I3 | Unit test with synthetic data | 1 |
| 1.5 | `export.py` (Package A) + `plots.py` (heatmap, frontier) | I13 | Integration test | 1 |
| 1.6 | CLI scripts | I1 | Smoke test (verify T₀ override: assert max_ticks = 10,000) | 1 |
| 1.7 | **Run Phase 1 campaign** | -- | C2 evaluable | 1 |
| 2.1 | `x0_generators.py` + scenario integration + alias mapping | I5 | Unit test (layout metric gates) | 2 |
| 2.2 | `predictors.py` | I6 | Unit test | 2 |
| 2.3 | **Run Phase 2 campaign** | -- | C1a/C1b evaluable | 2 |
| 3.1 | `shepherd_interference.py`, `shepherd_coverage.py` | I7 | Unit tests (include stationary-shepherd edge case) | 3 |
| 3.2 | `mechanism.py` | I8 | Unit test | 3 |
| 3.3 | **Run Phase 3 campaign** | -- | C3 evaluable | 3 |
| 4.1 | Multi-instrument grid runner | I9 | Integration test | 4 |
| 4.2 | `transfer.py` | I9 | Unit test | 4 |
| 4.3 | **Run Phase 4 campaign** | -- | C4 evaluable | 4 |
| 5.1 | Factor-sweep runner | I10 | Integration test | 5 |
| 5.2 | `substitution.py` | I10 | Unit test | 5 |
| 5.3 | **Run Phase 5 campaign** | -- | C5a/C5b evaluable | 5 |
| 6.1 | `scaling.py` | I11 | Unit test | 6 |
| 6.2 | **Run Phase 6 analysis** | -- | C6a or C6b decided | 6 |
| 7.1 | `early_warning.py` | I12 | Unit test | 7 |
| 7.2 | **Run Phase 7 campaign** | -- | C7a/C7b evaluable | 7 |

### 15. Non-goals for HerdSim work

- Inventing a new herding method as the research goal
- Rewriting the simulator into a general multi-agent platform
- Claiming single-method results as universal without RQ4 transfer tests
- Pre-building Phase 3+ tooling before Phase 1 experiments complete
- Building analysis modules that do not map to a Cap ID in Section 10.1
- Expanding scope beyond answering C1a–C7b for the locked protocol

---

## Part VI — Validity, Decisions, and Open Items

### 16. Threats to validity

| Threat | Scope | Mitigation |
|--------|-------|------------|
| **Single-task bias** | All experiments use `drive_to_goal` (τ₀). Patterns (overcrowding, scaling) may not generalise to containment, evasion, or multi-goal tasks. | RQ4 provides partial mitigation by varying the herding method. After the minimum publishable unit (RQ1–RQ3), consider a robustness check with a second task (e.g., `narrow_gate`) but this is not required for the first paper. |
| **Single-scenario geometry** | The world is a fixed 150×150 rectangle with a corner goal. Boundary effects may influence shepherd paths and I_dir. | Document boundary proximity in all campaigns. If wall effects are significant, test a larger world or a centred goal as a robustness appendix. |
| **Discrete-time artefacts** | The simulation is tick-based (dt = 0.1). Very fast events (collisions, direction reversals) may be under-resolved. | The dt = 0.1 default is standard in Strömbom-family models. Report dt and note that results apply to this time resolution. |
| **Herding-method fidelity** | Simulated instruments may not capture all phenomena of physical robots (communication latency, actuator noise, GPS error). | Scope claims to the simulated domain. RQ5 partially tests information degradation. Physical validation is out of scope for this program. |
| **Statistical power** | 30 scout seeds and 100 claim-grade seeds are heuristics, not formally powered. | For C1a (detecting ΔD_min ≥ 2): with 100 seeds per cell, the binomial 95% CI on R is ±0.06 at R = 0.90. A 2-shepherd shift moves R by ~0.15–0.30 in practice (based on preliminary runs), which is well above the CI width. If preliminary Phase 1 data suggest narrower effects, increase to 200 seeds on boundary cells before Phase 2. |

### 17. Decision log

| Date | Decision |
|------|----------|
| 2026-09-16 | Research object reframed from dog count to multi-resource budget |
| 2026-09-16 | Budget inputs B = (D, T); effort E as measured outcome |
| 2026-09-17 | RQs restructured: RQ1 (state), RQ2 (boundary), RQ3 (mechanism), RQ4 (transfer), RQ5 (information), RQ6 (scaling), RQ7 (early warning) |
| 2026-09-17 | Mechanism metrics added: I_dir (interference), C (coverage) |
| 2026-09-17 | X₀ families defined: compact, wide, split, outlier_rich |
| 2026-09-17 | N grid expanded to 8 points for scaling fits |
| 2026-09-17 | Plan polished: falsifiable claims, HerdSim gaps, implementation grounded in codebase audit |
| 2026-09-17 | Scientific-value table added for each RQ; operational definition framed as herdability |
| 2026-09-17 | Minimum publishable unit set to RQ1+RQ2+RQ3+S8; RQ4–RQ7 staged |
| 2026-09-17 | Traceability matrix Cap I1–I14 added; phase done-when criteria tied to claims |
| 2026-09-17 | Terminology de-risked: "herdability" replaces "controllability"; "herding method" / "instrument" replaces "controller" in prose |
| 2026-09-17 | I_dir stationary-shepherd rule specified (speed < 1e-6 → excluded) |
| 2026-09-17 | C2b hard-ceiling test clarified: T₁ = 20,000 ticks |
| 2026-09-17 | D_overcrowd defined over grid-ordered D-steps (not arithmetic spacing) |
| 2026-09-17 | C4 transfer labels operationalised with quantitative thresholds |
| 2026-09-17 | C5 information-ladder ordinal levels defined |
| 2026-09-17 | Parallelisation strategy added (ProcessPoolExecutor) |
| 2026-09-17 | Per-trial time-series storage format specified (Parquet) |
| 2026-09-17 | Exception E1 documented: conditional `shepherd_intended_velocities` addition to SimulationState |
| 2026-09-17 | Threats-to-validity section added |
| 2026-09-17 | Evidence-package dictionary (Section 3.1) added |
| 2026-09-17 | Diagnostic visualisation module added |
| 2026-09-17 | Freeze protocol (Section 8) — all defaults confirmed |

### 18. Protocol freeze (Phase 0 complete)

Section 8 defaults are **frozen** as of 2026-09-17. Confirmed choices:

1. Task τ₀ = `drive_to_goal` (optional later robustness: `narrow_gate`).
2. Reliability θ = 0.90 (also report 0.50, 0.70).
3. Transfer instruments: strombom_multi, kubo, fat, communication_free.
4. Flock sizes N = {25, 50, 75, 100, 150, 200, 300, 400}.
5. Time limits T₀ = 10,000; T₁ = 20,000 for C2b.
6. X₀ families: compact, wide, split, outlier_rich.
7. RQ7 horizons: k = 500 ticks (prediction), w = 200 ticks (feature window).
8. Public term: herdability / operational herdability.
9. Minimum publishable unit: RQ1+RQ2+RQ3+S8.

Phase 1 implementation targets Caps I1–I4, I13, and I14.

- 2026-09-17: Caps I1-I14 implemented in HerdSim (metrics, analysis/budget, api/budget_runner, configs/budget, scripts/budget). Phase done-when = claim-evaluable tooling + unit tests; full scout campaigns remain operator runs.
