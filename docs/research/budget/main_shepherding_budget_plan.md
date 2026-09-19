# Collective Herdability Under Shepherding

Status: active (Section 8 protocol frozen 2026-09-17)  
Role: detailed research plan and HerdSim implementation contract for this program  
Program overview: [herdsim_research_program.md](herdsim_research_program.md)  
Status / campaigns / run plan: [progress_tracker.md](progress_tracker.md)  
Results layout: [results/budget/README.md](../../../results/budget/README.md)

This is the detailed plan: scientific questions and claims, the frozen protocol, and
what HerdSim has to provide so we can evaluate those claims. A code change belongs
here only if it serves an RQ, contribution, Cap, or evidence package below. Phase
status and campaign outcomes stay in the progress tracker -- keep them out of this
file so we do not maintain two status boards.

**Terminology.** *Herdability* here means operational reliability of shepherding a
collective to a goal. It is not control-theoretic *controllability*. In prose we say
*herding method* or *instrument* for the dog algorithm; the code may still use
`dog_controller` for compatibility.

---

## At a glance

### Central question

> When a few shepherds guide a larger flock, how much control do we actually need as the flock gets bigger or more spread out?

Same starting point as the sheep-scaling draft (dog count vs flock size, and
correlation with spread). We want to test that idea carefully, without assuming
one scaling law up front.

### HerdSim

HerdSim is the experimental platform we use for multi-agent sheep herding: a few
shepherds (dogs) guide a larger flock to a goal under controlled conditions. It
gives us shared scenarios, metrics, and a fair way to compare herding methods.

### Shared protocol (summary)

One frozen experimental setup reused across comparisons (full freeze: Section 8).
If the protocol stays fixed, differences we see can be attributed to flock size,
flock structure, or herding method -- not to quietly changing the experiment.

It includes:

- herding task: `drive_to_goal`
- success rule and reliability target (default θ = 0.90; also report 0.50, 0.70)
- time budget per run (T₀ = 10,000; T₁ = 20,000 for hard-ceiling tests)
- flock sizes N and shepherd counts D to sweep
- baseline herding method: `strombom_multi` -- coordinated multi-dog collect-or-drive (gather strays, then drive toward the goal)
- transfer methods compared against that baseline:
  - `kubo` -- force-based multi-dog herding, no explicit collect/drive switch
  - `fat` -- each dog targets the farthest sheep it can see under local sensing
  - `communication_free` -- decentralised collect/drive; dogs do not share targets
- a common way to estimate the viable shepherd range: minimum needed for reliable success, and where adding more stops helping or starts hurting
- operating regimes (not only min/max): too few / efficient / wasteful / overcrowding / hard failure

### Core questions (reader view)

These four questions carry the program. Formal IDs RQ1--RQ7 (phases, Caps, claims)
map onto them in the table below.

1. **Size.** As flock size grows, how does the viable shepherd range change: the minimum needed for reliable herding, and the point where adding more stops helping or starts hurting?
2. **Structure.** At the same flock size, does flock shape/state (spread, fragmentation, outliers, etc.) change how much control we need?
3. **Mechanism.** Why does that pattern appear (for example interference, coverage limits, fragmentation)?
4. **Generality.** Which parts of the pattern still hold when we change the herding method?

Beyond those four, the plan also covers **information--shepherd tradeoffs** and
**early failure warning** as follow-ons, and we report operating regimes, not only
a min/max shepherd count.

### Short approach

1. Freeze the shared HerdSim protocol (Section 8).
2. Sweep flock size and shepherd count with the `strombom_multi` baseline; map viable control range and regimes from repeated runs.
3. Hold flock size fixed and vary initial structure (compact, wide, split, outlier-rich) to separate size from shape/state.
4. Use run logs to test candidate mechanisms (interference vs coverage vs fragmentation).
5. Repeat the same measurements with `kubo`, `fat`, and `communication_free` to see what transfers.
6. Later: test whether better information reduces needed shepherd count, and whether flock-state signals warn of failure before timeout.

### Mapping: reader questions to formal RQs

| Reader question | Formal IDs | Phase focus | Evidence package |
|-----------------|------------|-------------|------------------|
| Size (viable range + scaling) | RQ2, RQ6 | Phase 1, 6 | A, F |
| Structure (state beyond N) | RQ1 | Phase 2 | B |
| Mechanism | RQ3 | Phase 3 | C |
| Generality (method transfer) | RQ4 | Phase 4 | D |
| Information vs shepherds | RQ5 | Phase 5 | E |
| Early warning | RQ7 | Phase 7 | G |
| Reproducible protocol | S8 | Phase 0 | all |

Smallest unit we would treat as scientifically publishable: **RQ1 + RQ2 + RQ3 + S8**.
RQ4--RQ7 reuse the same protocol and come in stages after that.

---

## Part I — Problem, Goal, and Contributions

### 1. Problem

Shepherding and related collective-nudging work often asks: how many shepherds are
needed for a flock of size N? That is too narrow. It treats flock size as the only
predictor and shepherd count as the only resource, so it cannot answer decisions
operators actually face:

| Decision | What N-only sizing cannot answer |
|----------|----------------------------------|
| Force sizing | Two flocks of equal N can be easy or hard depending on cohesion, fragmentation, and spread |
| Adding robots | Extra shepherds can waste effort or reduce reliability; without regimes, "more is better" is untested |
| Sensor vs robot spend | Sensing and communication may substitute for headcount; the rate is unknown |
| Live monitoring | Failure is often recognised only at timeout; early state signals are unused |
| Method choice | Limits found on one herding method may or may not transfer |

Similar decisions show up in livestock robotics, drone escort, crowd guidance, and
autonomous convoy routing. What is missing is not "another herding heuristic," but
a clearer account of what makes a collective *operationally herdable* under
indirect shepherd influence.

### 1.1 Operational definition

**Herdability** is the measured probability that a shepherding configuration drives the flock to its goal within the time and resource budget. It is not classical control-theoretic controllability.

```text
A configuration is herdable at threshold θ when
R(m, τ, N, D, T, X₀, I) = P(success | locked seeds) >= θ.
```

| Term | Meaning in this plan |
|------|---------------------|
| Herdability | Operational reliability R ≥ θ of shepherding a flock to goal |
| Herding method / instrument | The shepherding algorithm that drives the dogs (e.g., `strombom_multi`, `kubo`) |
| Shepherd / dog | A physical or simulated agent that exerts repulsive influence on sheep |
| `dog_controller` | HerdSim code identifier for the herding-method plugin -- retained for compatibility |

Claims only matter if they change this reliability, the budget needed to hit it, or
our ability to see failure coming. Mechanism metrics (interference, coverage) help
explain patterns; they do not replace R.

### 2. Goal

Figure out what actually governs operational herdability of a cohesive collective
under indirect shepherd influence.

Working hypothesis:

```text
Herdability = f(collective state, shepherding resources, information quality, interference, task)
```

Flock size alone is not enough. Herdability depends on how the flock's measurable
state interacts with effective shepherding capacity -- limited by interference,
information, and coordination.

### 2.1 Why each formal RQ is kept

Keep an RQ only if it (a) closes a decision gap above, (b) has a claim we can
falsify, and (c) produces an evidence package HerdSim can emit. Rejecting a claim
still counts as a result: it bounds where N-only or D-only rules are enough.

Task τ₀ = `drive_to_goal` (Section 8).

| RQ | Scientific value (why ask) | If supported | If rejected |
|----|----------------------------|--------------|-------------|
| RQ1 | Tests whether N is a sufficient statistic | Force sizing must use flock state | N-only sizing adequate in tested domain |
| RQ2 | Makes "works / fails / hurts" operational | Capacity planning uses regimes | Monotonic "more dogs help" survives |
| RQ3 | Separates mechanism from phenomenology | Explains diminishing returns | Overcrowding not interference/coverage-driven |
| RQ4 | Prevents method-local overgeneralisation | States which limits are method-invariant | Treat results as instrument-specific |
| RQ5 | Quantifies sensor/robot substitution | Can trade I for D at fixed R | Headcount dominates; info does not buy shepherds |
| RQ6 | Replaces anecdotal scale-up with fitted laws | Capacity scales with N and state | Global or N-only scaling remains competitive |
| RQ7 | Moves from post-hoc failure to anticipation | Live ops can act before timeout | State features add no lead time over (N, D) |

### 3. Formal research questions

| ID | Question | Contribution | Package |
|----|----------|--------------|---------|
| RQ1 | Does collective state (cohesion, fragmentation, spread) change herdability at fixed N? | S1 | B |
| RQ2 | Where is the boundary between reliable and unreliable herding, and how sharp is it? | S2 | A |
| RQ3 | Why does adding shepherds eventually stop helping or start hurting? | S3 | C |
| RQ4 | Which herdability mechanisms are general across herding methods? | S4 | D |
| RQ5 | Can better information substitute for additional physical shepherds? | S5 | E |
| RQ6 | How does required shepherding resource scale with flock size and collective state? | S6 | F |
| RQ7 | Can current collective state predict imminent herding failure? | S7 | G |

### 3.1 Evidence packages

Each package is an exportable dataset used to evaluate the matching claims.

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

That is the overall thesis for the program. A paper or phase may only cover part of
it; whatever subset we claim still has to land on the falsifiable claims C1a–C7b.

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
| Spread | Variance of sheep distances to centroid (mean-spread S̄) | `metrics/mean_spread.py` — built (Cap I4) |
| Extent | Radius of gyration: RMS distance to centroid | `metrics/extent.py` — built (Cap I4) |

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

Formal IDs below are what phases, Caps, and claims use. The reader labels (Size /
Structure / Mechanism / Generality) are in **At a glance**.

### RQ1 — Structure: collective state beyond N

**Reader question:** At the same flock size, does flock shape/state change how much control we need?

**Formal question:** Does the same flock size have different herdability under different initial collective states?

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

### RQ2 — Size (part): herdability boundary and regimes

**Reader question:** As flock size grows, how does the viable shepherd range change (minimum needed, and where more stops helping or starts hurting)?

**Formal question:** Where does reliable herding end as D increases, and how sharp is that boundary?

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

### RQ3 — Mechanism: diminishing and negative returns

**Reader question:** Why does the size/structure pattern appear (interference, coverage limits, fragmentation)?

**Formal question:** Why do extra shepherds stop helping? What causes overcrowding collapse?

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

### RQ4 — Generality: cross-method transfer

**Reader question:** Which parts of the pattern still hold when we change the herding method?

**Formal question:** Which herdability mechanisms are shared across herding architectures?

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

### RQ5 — Follow-on: information versus physical shepherding

**Reader question:** Can better information reduce the needed shepherd count at fixed reliability?

**Formal question:** Can better sensing or communication reduce the required shepherd count at fixed reliability?

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

### RQ6 — Size (part): scaling regimes

**Reader question:** How does required shepherding resource grow with flock size and collective state?

**Formal question:** How does required shepherding resource grow with N and collective state?

**Why this RQ is valuable:** Operators need growth laws, not single-N anecdotes. State-conditioned scaling is only justified if RQ1 holds; otherwise report N-only scaling and stop.

**Approach:**
- Compute D_min(N, X₀) for each X₀ family across N in {5, 10, 25, 50, 75, 100, 150, 200, 300, 400}
- Fit power-law, piecewise-linear, and state-conditioned candidates; compare with AIC/BIC and cross-validation
- Test across herding methods after RQ4 data exist

**Falsifiable claims:**
- **C6a:** A single global power law is rejected in favour of piecewise or state-conditioned models (ΔAIC > 10), OR
- **C6b:** A stable sublinear regime (α < 1) exists within a stated domain of N and X₀

**HerdSim must provide:** scaling fit module consuming Packages A/B; no new simulator physics.

### RQ7 — Follow-on: early warning of herding failure

**Reader question:** Can flock-state signals warn of failure before a run times out?

**Formal question:** Can measurable collective state predict impending failure before the trial ends?

**Why this RQ is valuable:** Post-hoc failure labels do not help live operations. Predictive lead time from X(t), I_dir, and C is the scientific test of anticipatory value. Only run after RQ1--RQ3 metrics exist and failure trajectories are plentiful.

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

Machine-readable freeze: [configs/budget/canonical_grid.yaml](../../../configs/budget/canonical_grid.yaml)  
Campaign subsets (with per-field rationale): [configs/budget/campaigns/](../../../configs/budget/campaigns/)  
New campaign rule: every override needs a WHY comment -- see `campaigns/README.md`.

| Item | Default | Status |
|------|---------|--------|
| Task τ₀ | `drive_to_goal` | frozen |
| Reliability θ | 0.90 (also report 0.50, 0.70) | frozen |
| Baseline herding method | `strombom_multi` | frozen |
| Transfer herding methods | `strombom_multi`, `kubo`, `fat`, `communication_free` | frozen |
| Flock sizes N | {5, 10, 25, 50, 75, 100, 150, 200, 300, 400} | frozen |
| Shepherd counts D | {1, 2, 3, 4, 6, 10, 15, 20, 25, 35} | frozen |
| X₀ families | compact, wide, split, outlier_rich | frozen |
| Time limit T₀ | 10,000 ticks (overrides scenario default 3,000) | frozen |
| Extended time limit T₁ | 20,000 ticks (for C2b hard-ceiling test) | frozen |
| Scout seeds | 30 per cell | frozen |
| Claim-grade seeds | 100 on boundary cells | frozen |
| RQ5 factors | obs mode, sensing range, communication mode | frozen |
| RQ7 prediction horizon k | 500 ticks | frozen |
| Master seed | 2026 | frozen |

### 8.1 Protocol rationale (why these values)

These defaults are deliberate, not arbitrary. Short version below; longer notes are
in comments in `canonical_grid.yaml`:

| Choice | Why |
|--------|-----|
| `drive_to_goal` | Shared HerdSim task; matches operational herdability (goal under time budget) |
| θ = 0.90 | Aligns with sheep-scaling "reliable" band (SR ≥ 90%); sensitivity at 0.50/0.70 |
| `strombom_multi` baseline | Coordinated Collect/Drive multi-dog baseline in HerdSim |
| Transfer set | Distinct architectures (force / local FAT / no shared targets), not near-duplicates |
| N grid | Full scale ladder; floor N=5 (see Section 8.1.1); 5-10 = hard small-flock regime; 75/150 resolve ~100 breakpoint; 300/400 probe large-N growth |
| D grid | Fine steps at low D, coarser at high D; ceiling 35 as practical experimental cap |
| X₀ families | Causal structure axes for RQ1 (spread, fragmentation, outliers) |
| T₀ = 10000 | Per-trial horizon so failures reflect control limits, not a short default clock; overrides scenario 3000 |
| T₁ = 20000 | C2b only: hard ceiling vs timeout |
| Scout 30 / claim 100 | Cheap map then precise boundary CI (D_min procedure) |
| Master seed 2026 | Fixed reproducible seed base |
| RQ7 k=500, w=200 | 5% of T₀ horizon; fixed feature window from Phase 0 |
| Wasteful 20% | Default effort tolerance; analyse sensitivity at 10%/30% |

**Future experiments:** any new `configs/budget/campaigns/*.yaml` must say why each
subset differs from this freeze. Changing a frozen default needs a tracker protocol
exception (and usually a new `protocol_id`). Code follows the protocol -- we do not
rewrite the science to match whatever the code already supports.

#### 8.1.1 Why the N floor is 5 (not 1, 2, or 4)

This is a science choice about what we are studying (indirect control of a
collective). It is not justified by current implementation limits: if the science
needed N<5, we would change the generators/metrics, not the other way around.

Below N=5, the quantities this program asks about stop meaning the same thing:

1. **Collective interaction.** Herdability here is control of a group whose members interact with each other. At N=1 there are no sheep-sheep interactions, so "collective structure" and interaction-driven cohesion are undefined as group phenomena. Spread-as-variance around a GCM is trivially zero for a single agent.

2. **Structure as an independent factor (RQ1).** Structure families such as `outlier_rich` are defined as a *majority core plus a minority of outliers* (about 80%/20%). That definition needs enough agents for both parts to coexist as roles in one flock. At N=2-4, "20% outliers" cannot describe a minority subpopulation in the same sense (one sheep is already a huge fraction of the group), so the X0 contrast is no longer the same experimental factor.

3. **Mechanism metrics.** Coverage defines periphery as farther from the GCM than the median. At N=2-3 that split is nearly tautological: a large share of agents are "peripheral" by construction. Interference/coverage comparisons then do not mean the same thing as in larger flocks.

4. **Task semantics.** The herding task is: gather a dispersed group into a flock, then drive that flock to a goal (Collect then Drive relative to a flock GCM / size-dependent cohesion rule). With only a few sheep, the same controller mostly reduces to chasing individuals. That is a different control problem than indirect nudging of a collective.

5. **Question scope.** The central question is how much control a *few* shepherds need for a *larger* group. Studying N in {1,2,3,4} on a D grid up to 35 mainly measures over-actuated individual pursuit, not collective control demand.

Therefore N=5 is the smallest size where (a) sheep-sheep collective structure is still
present, (b) majority-core / minority-outlier structure can be defined as intended, and
(c) the herding task is still the same object as at larger N. N=5 and 10 stay in the
freeze so we can study the hard *small-flock* regime without leaving that object.

If we later want N=1-4, run a separate control campaign (individual-pursuit baseline)
with its own rationale -- and implement whatever generators/metrics that campaign
needs -- rather than mixing it into the collective scaling freeze.
### 9. Phase plan

Live status for each phase: [progress_tracker.md](progress_tracker.md). This table is
the planned phase contract only (not a status board).

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

1. **Additive, not invasive.** Prefer new modules over rewriting the core. Extend BaseMetric and wrap `iter_one_trial()`.
2. **Composable analysis.** Analysis functions take a `DataFrame` and return a `DataFrame`. No hidden global state.
3. **Reproducible by default.** Every campaign exports a provenance stamp (git hash, config hash, seed list, metric versions).
4. **Phase-gated.** Build and test the tooling for a phase before running its experiments. Do not pre-build later phases "just in case."
5. **Traceability.** Do not merge HerdSim work unless it maps to a row in Section 10.1. Orphan tooling is out of scope.

### 10.1 Traceability: RQ to HerdSim capability (implementation must meet the plan)

The plan is met when each capability below exists, is tested, and is used by the
matching evidence package. Status below was relative to the codebase when the plan
was written.

| Cap | Serves | Capability | HerdSim location | Status | Package |
|-----|--------|------------|------------------|--------|---------|
| I1 | RQ2, RQ6 | N × D × seed grid runner with resume + provenance | `services/budget/runner.py`, `analysis/budget/provenance.py` | built | A, F |
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
| I14 | RQ3, RQ7 | Per-trial time-series storage (Parquet) | `services/budget/runner.py` (write path) | built | C, G |

**Already available (do not rebuild):** cohesion, fragmentation, outlier_count metrics; `iter_one_trial` / Experiments path; observation modes and communication factor injection in the simulation runner; instrument presets listed in RQ4; failure taxonomy via benchmark runner.

**Acceptance rule:** Phase k is done on the implementation side only when its Cap
row(s) are built, unit-tested, and the Section 9 "done when" criterion is met.
Running campaigns without the matching Cap does not count as answering the RQ.

### 11. What to build

#### 11.1 X₀ generators (Phase 2, but spec needed at Phase 0)

**File:** `core/x0_generators.py` [NEW]  
**Capability:** I5 (required for RQ1)

Cap I5 is **built**: `core/x0_generators.py` plus scenario wiring. Spec below remains the design contract for RQ1 (verify layout metric gates before claim-grade Package B).

**Design:** Standalone generator that scenarios call, rather than embedding layout logic in each scenario.

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
| `compact` | `compact` | Single Gaussian cluster, σ = 0.3 × default spread | Low cohesion distance |
| `wide` | `wide` | Single Gaussian cluster, σ = 2.0 × default spread | High cohesion distance |
| `split` | `split` | 2–3 separated subclusters at distance ≥ 2× interaction radius | Low fragmentation index |
| `outlier_rich` | `outlier_rich` | Core cluster (80%) + outliers (20%) beyond lost threshold | High outlier count |

`INITIAL_LAYOUTS` in `core/experimental_factors.py` is `("compact", "wide", "split", "outlier_rich")`. `DriveToGoalScenario.initial_positions()` calls `x0_generators.generate_initial_positions()` when `initial_layout` is set.

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
| Budget grid runner | `services/budget/runner.py` [NEW] | N×D×seed campaigns with resumability and provenance |
| Provenance stamps | `analysis/budget/provenance.py` [NEW] | Git hash, config hash, seed list, timestamps |
| Frontier extraction | `analysis/budget/frontier.py` [NEW] | D_min, D_overcrowd, D_max, B* |
| Regime labelling | `analysis/budget/regimes.py` [NEW] | Assigns regime labels to (N, D) cells |
| Export / dossier | `analysis/budget/export.py` [NEW] | CSV + markdown report per package |

The grid runner wraps [iter_one_trial()](file:///home/quyen/HerdSim/services/experiments/runner.py#L77) from the existing benchmark runner. It does NOT modify the benchmark runner.

**Resumability:** On startup, scan `output_dir` for completed `(N, D, seed)` tuples and skip them. Critical because a full grid (8 × 10 × 30 = 2,400 trials) can take hours. Implement a JSON manifest (e.g., `output_dir/manifest.jsonl`) that appends one line per completed trial with keys `{N, D, seed, status, timestamp}`. On resume, load the manifest and skip listed triples.

**T₀ override:** The canonical grid config MUST set `max_ticks: 10000` to override the scenario default of 3,000 ([drive_to_goal.py L41](file:///home/quyen/HerdSim/scenarios/drive_to_goal.py#L41)). The override flows through `algorithm_params` → `resolve_experiment_config`. Verify this path in a smoke test before any campaign: run one trial with the canonical config and assert `result.total_ticks <= 10000` and `result.total_ticks > 3000` (for a trial that runs to timeout).

#### 11.4 Per-trial time-series storage (Phase 1, extended in Phase 3)

**Capability:** I14

RQ3 and RQ7 require per-tick mechanism metrics (I_dir, C) and collective-state trajectories, not just scalar summaries. The grid runner must store per-trial time-series data.

**Format:** Apache Parquet, one file per trial. Filename stem equals the resume cell key
(includes N, D, layout, seed, instrument, and any info-factor suffixes).

```
results/budget/phase{k}/{campaign_slug}/timeseries/<cell_key>.parquet
```

Example: `N50_D2_Lcompact_S2026_Istrombom_multi.parquet`

**Columns (Phase 1):** `tick, cohesion, fragmentation, outlier_count, mean_spread, extent`

**Columns (Phase 3, added when I7 is built):** `+ i_dir, coverage`

**Storage budget:** ~10,000 ticks × 8 columns × 8 bytes ≈ 640 KB per trial (Parquet compresses ~5×, so ~130 KB). Full scout sweep (9,600 trials): ~1.2 GB. Manageable.

**Implementation:** After each trial completes, write `result.history` to Parquet under `timeseries/`. Also write `status.json` with planned/done counts. Campaign subset YAML is copied to `campaign.yaml` in the output folder.

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
├── analysis/budget/           # Caps analysis (packages A-G)
│   ├── provenance.py
│   ├── frontier.py
│   ├── regimes.py
│   ├── export.py
│   ├── plots.py
│   ├── mechanism.py
│   ├── transfer.py
│   ├── substitution.py
│   ├── scaling.py
│   ├── predictors.py
│   └── early_warning.py
├── api/
│   ├── budget_runner.py       # grid expand + resume + timeseries
│   └── budget_layout.py       # path conventions + campaign helpers
├── configs/budget/
│   ├── canonical_grid.yaml    # frozen Section 8 protocol
│   └── campaigns/             # per-run subsets (pilot, scout, state, ...)
├── scripts/budget/
│   ├── run_grid.py
│   ├── run_factor_sweep.py
│   └── analyse.py
├── results/budget/            # campaign run data (kept in git)
│   ├── README.md
│   └── phase{k}/{campaign}/
│       ├── campaign.yaml
│       ├── manifest.jsonl
│       ├── provenance.json
│       ├── status.json
│       ├── trials.csv
│       ├── timeseries/
│       ├── packages/{a-g}/
│       └── REPORT.md          # human narrative (optional)
└── tests/backend/correctness/
    └── test_budget_stack.py
```

Operator facade: `Makefile.budget` (`make -f Makefile.budget help`, or `make budget-help`). Targets: `budget-pilot`, `budget-scout`, `budget-pilot-state`, `budget-factor-sweep`, `budget-analyse`.
### 13. What is NOT modified

| Module | Reason |
|--------|--------|
| `core/simulation_runner.py` | Grid runner wraps it |
| `core/experiment_config.py` | Config resolution is already flexible |
| `analysis/failure_taxonomy.py` | Already integrated via benchmark_runner |
| `instruments/*` | We study existing instruments as-is |
| `dynamics/*` | No sheep/dog model changes |

**Minimal changes to existing files:**
- `core/experimental_factors.py`: `INITIAL_LAYOUTS = ("compact", "wide", "split", "outlier_rich")`
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
| 2026-09-18 | Front matter rewritten for plain-language "At a glance" (central question, protocol summary, reader RQs, short approach, mapping to formal RQ1--RQ7); parent framing and progress tracker slimmed to remove status/definition duplication |
| 2026-09-18 | Results layout cleanup: `phase{k}/{slug}/`, `packages/{a-g}/`, campaign YAMLs, `status.json`, timeseries stem = cell key, `artefacts.json`, tracked `results/budget/README.md` |
| 2026-09-18 | Protocol rationale added: comments on all budget YAML fields + main plan Section 8.1; campaigns/README checklist for future experiments |
| 2026-09-18 | N grid includes 5 and 10 (full small-N regime); framed as general scale test, not paper exclusion |

### 18. Protocol freeze (Phase 0 complete)

Section 8 defaults are **frozen** as of 2026-09-17. Confirmed choices:

1. Task τ₀ = `drive_to_goal` (optional later robustness: `narrow_gate`).
2. Reliability θ = 0.90 (also report 0.50, 0.70).
3. Transfer instruments: strombom_multi, kubo, fat, communication_free.
4. Flock sizes N = {5, 10, 25, 50, 75, 100, 150, 200, 300, 400}.
5. Time limits T₀ = 10,000; T₁ = 20,000 for C2b.
6. X₀ families: compact, wide, split, outlier_rich.
7. RQ7 horizons: k = 500 ticks (prediction), w = 200 ticks (feature window).
8. Public term: herdability / operational herdability.
9. Minimum publishable unit: RQ1+RQ2+RQ3+S8.

Phase 1 implementation targets Caps I1–I4, I13, and I14.

- 2026-09-17: Caps I1-I14 implemented in HerdSim (metrics, analysis/budget, api/budget_runner, configs/budget, scripts/budget). Phase done-when = claim-evaluable tooling + unit tests; full scout campaigns remain operator runs.
