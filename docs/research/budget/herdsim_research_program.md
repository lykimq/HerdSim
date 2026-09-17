# HerdSim Research Program

> **Generated from:** `master_prompt.md` (Deep Research Prompt — Designing a New Scientific Research Program Around HerdSim)
> **Status:** Active — single source of truth
> **Supersedes:** `main_shepherding_budget_plan.md` (draft, 2026-09-17)
> **Last updated:** 2026-09-17

---

## 1. Scientific Vision

This project addresses a fundamental, open problem in the science of collective systems:

> **How can an external controller reliably influence a large collective without directly controlling its individual members — and what determines the limits of that controllability?**

This problem sits at the intersection of collective behaviour science, control theory, and complex adaptive systems. It is broader than any single shepherding algorithm. It matters whenever a relatively small number of external agents must reliably steer a population whose emergent dynamics they cannot directly programme.

HerdSim provides a controlled model system in which this general problem can be experimentally decomposed, its mechanisms exposed, and its boundaries mapped — in a way that is reproducible, quantitative, and honest about the gap between simulation and real-world systems.

The draft paper ("How many dogs do I need to herd sheep?", 2025) explored a specific instance of this problem — the scaling of required shepherd count with flock size, and its correlation with flock spread. That work is treated here as **preliminary evidence**, not as the scientific foundation. The new program asks: why do those scaling relationships exist, when do they break, what governs them, and are the governing principles transferable?

---

## 2. Real-World Motivation

The general problem — indirect collective control — appears in the following real-world systems:

| Domain | Real-world challenge | Why indirect control is relevant |
|--------|---------------------|----------------------------------|
| Livestock robotics | Robotic dogs must herd sheep flocks of varying size and cohesion | Individual-level control of each sheep is infeasible |
| Drone-swarm escort | Small number of shepherd drones must keep a larger swarm on-path | Direct communication/control of all swarm members is bandwidth-limited |
| Crowd guidance | Emergency responders must move crowds without physical contact | Individual commands cannot be issued at scale |
| Search and rescue | A small robot team must herd survivors or disoriented individuals to a collection point | Survivors may not be individually controllable |
| Environmental robotics | Robots must move animals away from protected zones | Physical density of controlled robots is limited |
| Collective transport | Simple robots collectively transport large objects via local rules | Central control of each robot is not scalable |

For each domain, what is currently missing is not "a better algorithm" but scientific understanding of:
- What collective-state properties determine how much control capacity is needed
- What causes additional controllers to saturate, interfere, or become harmful
- What information (sensing, communication) can substitute for physical control agents
- How predictive signals of control failure can be detected in advance

The present program provides scientific knowledge that could eventually inform real-system design — while being honest that simulation cannot establish real-world effectiveness.

---

## 3. State of the Field

### Established

- **Collective movement from local rules:** Vicsek (1995), Reynolds (1987), Stromboem (2011) show that simple local interaction rules produce coherent group motion.
- **Single-shepherd scaling limits:** Strombom et al. (2014) demonstrated one shepherd can herd ~50–100 sheep, with performance deteriorating thereafter.
- **Collect-or-drive algorithms:** Well-characterised for single-agent settings (Strombom 2014, Kubo 2022, FAT).
- **Overcrowding as a qualitative observation:** The draft paper (2025) and Jadhav et al. provide empirical evidence that adding shepherds beyond a point reduces reliability.
- **Flock spread as a predictor:** The draft paper (2025) found strong correlation between mean-spread and required shepherd count at fixed flock size.

### Partially understood

- **Mechanistic cause of overcrowding:** Why adding shepherds reduces success is unexplained. Interference between shepherd trajectories and coverage saturation are candidate explanations, but relative contributions are not established.
- **Cross-method generality:** Whether scaling laws and overcrowding hold across different herding architectures is untested systematically.
- **Initial collective-state dependence:** Spread correlates with required shepherds, but causal manipulation of initial collective state has not been performed.

### Contested

- **Whether spread is a sufficient predictor:** The draft paper's N→spread→D_min chain is correlational. Whether cohesion, fragmentation, and outlier density independently predict herdability beyond spread is unknown.
- **Scaling regime structure:** Whether shepherd scaling follows a single power law or piecewise regimes is undetermined.

### Underexplored

- **Information–shepherd substitution:** Whether better sensing or communication can reduce the required number of physical shepherds at fixed reliability is almost entirely unstudied.
- **Early warning of herding failure:** Whether measurable collective-state trajectories can predict imminent failure has not been studied in shepherding systems.
- **Controllability phase transitions:** Whether there are sharp transitions between controllable and uncontrollable collective-state regimes has not been characterised.

### Unknown

- What combination of collective-state variables forms a minimal sufficient statistic for herdability beyond N and mean-spread.
- What makes the overcrowding-to-failure transition sharp or gradual — and whether this depends on the herding architecture.
- Whether herdability principles established in one simulated domain transfer across control architectures.

---

## 4. Genuine Research Gap

> **We do not know what governs operational herdability of collective systems under limited indirect control — beyond flock size. We cannot predict when extra controllers help, when they become redundant, when they become harmful, or when control will fail — from measurable collective-state variables.**

This gap is:
- **Not filled by the existing draft paper**, which established correlational scaling at fixed collective-state and did not manipulate initial state, test mechanisms, or study multi-instrument generality.
- **Not filled by prior literature**, which either studied single-shepherd settings, treated shepherd count as the only variable, or analysed specific algorithms without systematic comparison.
- **Not an incremental gap** — closing it would change how collective-control systems are designed and operated.

---

## 5. Position of Our Existing Work

### What the draft paper contributes

The 2025 draft paper established:
1. Non-linear, quasi-monotonically increasing scaling of minimum shepherd count with flock size (one herding algorithm, one task, one environment)
2. Diminishing returns and overcrowding at fixed flock size as shepherd count increases
3. Correlation between required shepherd count and flock mean-spread

### Why the new program is broader

The draft paper:
- Used a single herding algorithm (Strombom multi-dog)
- Used a fixed initial collective state (single compact cluster)
- Observed spread as a correlate, not a causally manipulated variable
- Did not test mechanisms (interference, coverage saturation)
- Did not study information substitution, early warning, or cross-method transfer
- Was built on NetLogo; the new program uses HerdSim (Python) enabling reproducible, code-auditable experiments

The new program asks the question the draft paper *motivates* but does not *answer*: **What governs herdability — and which governing principles are general?**

---

## 6. Central Scientific Question

> **What determines the operational limits of reliability when a fixed set of external controllers attempts to steer a collective system that they cannot individually control — and how do those limits depend on the collective's internal state, the controllers' capacity, and their information?**

---

## 7. Central Hypothesis

> **Operational herdability is not determined by collective size alone. It is governed by the interaction between the collective's measurable state (cohesion, fragmentation, spread, outlier density), the effective control capacity (number of controllers, their coordination, and interference), and the information available to controllers. Specific transitions between controllable and uncontrollable regimes exist, and some governing mechanisms are shared across different control architectures.**

**Notation:**

```
R(m, tau, N, D, T, X0, I) = P(success | locked seeds) >= theta

where:
  R    = herdability (operational reliability)
  m    = herding method (instrument)
  tau  = task (scenario + success rule)
  N    = collective size
  D    = shepherd count
  T    = time budget (ticks)
  X0   = initial collective state family
  I    = information condition
  theta = reliability threshold (default 0.90)
```

**Terminology note:** *Herdability* = operational reliability R >= theta, NOT control-theoretic controllability (Gramian/rank-based). The shepherd algorithm is called the *herding method* or *instrument*, not "controller," to avoid conflation.

---

## 8. Major Research Questions

### RQ1 — Collective state as a predictor of herdability

**Question:** Does the initial collective state (beyond flock size N) causally determine herdability? Do equal-sized flocks with different initial states (compact vs. wide vs. fragmented vs. outlier-rich) require systematically different minimum shepherd counts?

**Why it matters:** If true, N is not a sufficient statistic for sizing a shepherding force. Operators must use collective-state measurements, not headcounts, to plan capacity.

**What is already known:** Spread correlates with required shepherd count (draft paper, 2025) — correlational, not causal.

**What is unknown:** Whether manipulating initial collective state (holding N fixed) causes systematic changes in D_min.

**Hypotheses:**
- H1a: D_min differs by >= 2 shepherds across initial-state families at fixed N (at least one N value)
- H1b: A model including collective-state features predicts trial-level reliability better than (N, D) alone (ΔAIC > 4, out-of-sample log-likelihood)

**Falsification:** If D_min does not differ across X0 families after causal manipulation, N-only sizing remains adequate.

**Contribution level:** Level 2 (mechanism) — establishes collective state as independent determinant.

---

### RQ2 — Herdability regimes and regime boundaries

**Question:** As shepherd count increases beyond the minimum required, what distinct reliability regimes emerge — and how sharp are the transitions?

**Why it matters:** Without regime taxonomy, "add more shepherds" is an untested heuristic.

**Regimes:**

| Regime | Operational definition |
|--------|----------------------|
| Under-budget failure | R < theta |
| Efficient operation | R >= theta, D near D_min, effort competitive |
| Wasteful overspend | R >= theta, median effort 20%+ above efficient level without reliability gain |
| Overcrowding collapse | R drops below theta for D > D_overcrowd |
| Hard failure | No tested D achieves R >= theta within T |

**Hypotheses:**
- H2a: Overcrowding (sustained R decline with increasing D) appears for >= 2 herding methods at theta = 0.90
- H2b: For at least one (N, X0), D > D_overcrowd remains unreliable (R < theta) even at T1 = 20,000 ticks (hard ceiling, not timeout artefact)

**Falsification:** If R always recovers with extended T, overcrowding is a timeout artefact.

**Contribution level:** Level 1–2 (empirical characterisation of regimes).

---

### RQ3 — Mechanism of diminishing and negative returns

**Question:** Why do additional shepherds eventually stop helping and start hurting?

**Why it matters:** Phenomenology alone cannot guide design. Mechanism identification tells operators what to fix.

**Candidate mechanisms:**

| Mechanism | Predicted signature |
|-----------|---------------------|
| Shepherd interference | I_dir rises with D before reliability falls |
| Coverage saturation | Coverage C plateaus while effort keeps rising |
| Induced fragmentation | Flock fragmentation increases in overcrowding cells |
| Redundant effort | Effort rises, reliability flat, I_dir not necessarily elevated |

**Interference index:**
```
I_dir(t) = 1 - ||sum_i u_hat_i(t)|| / M_active

  u_hat_i = shepherd i's unit velocity
  M_active = count of moving shepherds (speed > 1e-6 world-units/tick)
  If M_active = 0: I_dir = 0
```

**Coverage:** Fraction of peripheral sheep (distance > median distance to centroid) within >= 1 shepherd's influence radius r_s.

**Hypothesis:**
- H3: Overcrowding cells have significantly higher median I_dir and/or fragmentation than efficient cells at same N (rank test p < 0.05, Holm-Bonferroni corrected)

**Falsification:** If I_dir and fragmentation do not differ, interference is not the mechanism.

**Contribution level:** Level 2 (mechanism).

---

### RQ4 — Cross-method generality

**Question:** Which herdability mechanisms are shared across different herding architectures?

**Why it matters:** Mechanism findings on one instrument are not scientific laws.

**Herding methods:**
- Required: `strombom_multi`, `kubo`, `fat`
- Recommended: `communication_free`
- Optional: `v_formation`, `adaptive`

**Transfer labels per property:**

| Property | shared | shifted | absent |
|----------|--------|---------|--------|
| State-dependent D_min | same direction, |DeltaD_min| <= 2 | same direction, |DeltaD_min| > 2 | no significant effect |
| Overcrowding existence | comparable D/N ratio (within 1.5x) | exists but different D | not observed |
| Interference signature | I_dir-reliability correlation r < -0.3 in both | present but magnitude differs | not significant |
| Coverage saturation | analogous thresholds | present but different level | not observed |

**Hypothesis:**
- H4: At least one core mechanism receives **shared** label across >= 3 of the 4 required+recommended herding methods

**Falsification:** If all mechanisms are shifted/absent, results are instrument-specific only.

**Contribution level:** Level 3 (general principle) if confirmed.

---

### RQ5 — Information–shepherd substitution

**Question:** Can better sensing or communication reduce the minimum required shepherd count at fixed reliability?

**Why it matters:** If yes, the control budget is multi-dimensional (D, I), not D-only.

**Information ladder:**

| Factor | Levels |
|--------|--------|
| Observation mode | bearing_only → local_positions → global |
| Sensing range | x0.5 → x1.0 → x1.5 → x2.0 of default |
| Communication | none → neighbour_broadcast → global_shared |

**Hypotheses:**
- H5a: At least one step up the information ladder reduces D_min by >= 1 at N in {100, 200} while R >= theta
- H5b: The second step saves fewer shepherds than the first (diminishing returns)

**Falsification:** If no information upgrade reduces D_min, physical headcount dominates.

**Contribution level:** Level 1–2.

---

### RQ6 — Scaling laws conditioned on collective state

**Question:** How does the minimum required shepherd count grow with N — and does the scaling law depend on initial collective state?

**Why it matters:** Operators need growth laws for planning.

**Hypotheses:**
- H6a: A single global power law is rejected in favour of piecewise or state-conditioned models (ΔAIC > 10), OR
- H6b: A stable sublinear scaling regime (exponent alpha < 1) exists within a stated domain

**Falsification:** If global power law is not rejected, N-only scaling is adequate; report the single-law exponent.

**Contribution level:** Level 2–3.

---

## 9. Scientific Breakpoints

Primary targets — each represents a mechanistically meaningful regime change:

```
controllable → uncontrollable
(reliable herding at D_min) → (no D achieves R >= theta)

beneficial → redundant → harmful controllers
(D < D_min) → (D_min <= D < D_overcrowd) → (D > D_overcrowd)

local information sufficient → information insufficient
(bearing_only achieves R >= theta) → (bearing_only fails; global needed)

cohesive collective → fragmented collective
(flock navigates as unit) → (splits; shepherd tasks conflict)

sublinear scaling → superlinear scaling
(each additional sheep costs less than one shepherd) → (costs more)
```

| Transition | Status |
|-----------|--------|
| Controllable → uncontrollable | Partially known (qualitative); boundaries uncharacterised |
| Beneficial → harmful controllers | Underexplored (mechanism unknown) |
| Information sufficiency → insufficiency | Unknown |
| Cohesive → fragmented (shepherd-induced) | Unknown |
| Scaling regime changes | Partially known (draft paper observed non-linearity; piecewise fit not done) |

---

## 10. Experimental Program

### Stage A — Exploration: herdability maps (Phase 1)

**Goal:** Build reliability maps R(N, D) under baseline method; identify existence of regimes (RQ2).

| Parameter | Value |
|-----------|-------|
| Herding method | `strombom_multi` |
| Flock sizes N | {25, 50, 75, 100, 150, 200, 300, 400} |
| Shepherd counts D | {1, 2, 3, 4, 6, 10, 15, 20, 25, 35} |
| Initial state X0 | compact (fixed) |
| Time limit T0 | 10,000 ticks |
| Scout seeds | 30 per (N, D) cell |
| Claim seeds | 100 on boundary cells |
| Master seed | 2026 |

**Decision criteria:** C2 claims (H2a, H2b) evaluable; frontier and regimes exported.

### Stage B — Collective-state manipulation (Phase 2)

**Goal:** Test whether initial state causally determines herdability (RQ1).

| Parameter | Value |
|-----------|-------|
| X0 families | compact, wide, split, outlier_rich |
| N | {50, 100, 200} |
| D sweep | same grid as Stage A |

**Decision criteria:** H1a and H1b evaluable; X0 families verified by metric stats.

### Stage C — Mechanism testing (Phase 3)

**Goal:** Identify causal mechanism of overcrowding collapse (RQ3).

| Parameter | Value |
|-----------|-------|
| Cells | overcrowding and efficient cells from Stage A |
| Metrics added | I_dir(t), coverage C(t) per tick |
| Analysis | Temporal ordering of I_dir and fragmentation relative to reliability drop |

**Decision criteria:** H3 evaluable; mechanism time series stored as Parquet.

### Stage D — Robustness: Cross-method transfer (Phase 4)

**Goal:** Test whether RQ1–RQ3 mechanisms generalise (RQ4).

| Parameter | Value |
|-----------|-------|
| Methods | strombom_multi, kubo, fat, communication_free |
| Protocol | identical task, seeds, metrics as Stages A–C |

**Decision criteria:** H4 evaluable; transfer table filled for >= 3 methods.

### Stage E — Information substitution (Phase 5)

**Goal:** Measure information–shepherd substitution rate (RQ5).

| Parameter | Value |
|-----------|-------|
| N | {100, 200} |
| I factors | observation mode, sensing range, communication |

**Decision criteria:** H5a and H5b evaluable.

### Stage F — Scaling analysis (Phase 6)

**Goal:** Fit and compare scaling laws (RQ6). Reuses Packages A/B — no new campaign.

**Decision criteria:** H6a or H6b decided with model comparison table.

### Stage G — Early warning (Phase 7)

**Goal:** Test predictive value of state trajectories for failure (RQ7). Reuses trial histories from Stages A–C.

| Parameter | Value |
|-----------|-------|
| Prediction horizon k | 500 ticks |
| Feature window w | 200 ticks |
| Evaluation points | every 200 ticks, tick 1,000–8,000 |
| Baseline | logistic on (N, D) |
| Validation | leave-one-N-out cross-validation |

**Decision criteria:** AUROC(state-based) vs AUROC(N,D baseline); lead-time distribution reported.

---

## 11. Required HerdSim Capabilities

Every capability maps to at least one RQ. No feature is in scope unless it appears here.

| Cap | Serves | Capability | Target location | Status |
|-----|--------|------------|-----------------|--------|
| I1 | RQ2, RQ6 | N x D x seed grid runner (parallel, resumable, provenance) | `api/budget_runner.py` | to build |
| I2 | RQ2 | Frontier extraction: D_min, D_overcrowd, D_max, B* | `analysis/budget/frontier.py` | to build |
| I3 | RQ2 | Regime labelling | `analysis/budget/regimes.py` | to build |
| I4 | RQ1, RQ6, RQ7 | Mean-spread and extent metrics | `metrics/mean_spread.py`, `metrics/extent.py` | to build |
| I5 | RQ1 | X0 generators + scenario wiring | `core/x0_generators.py`; update `drive_to_goal` | to build |
| I6 | RQ1 | State vs (N,D) predictor comparison | `analysis/budget/predictors.py` | to build |
| I7 | RQ3, RQ7 | Interference I_dir and coverage C metrics | `metrics/shepherd_interference.py`, `metrics/shepherd_coverage.py` | to build |
| I8 | RQ3 | Mechanism hypothesis tests | `analysis/budget/mechanism.py` | to build |
| I9 | RQ4 | Locked multi-instrument campaigns + transfer table | `analysis/budget/transfer.py` | to build |
| I10 | RQ5 | Factor sweeps + substitution curves | `scripts/budget/run_factor_sweep.py`, `analysis/budget/substitution.py` | to build |
| I11 | RQ6 | Scaling model fits | `analysis/budget/scaling.py` | to build |
| I12 | RQ7 | Early-warning features and evaluation | `analysis/budget/early_warning.py` | to build |
| I13 | S8 | Canonical protocol config + dossier export | `configs/budget/canonical_grid.yaml`, `analysis/budget/export.py` | to build |
| I14 | RQ3, RQ7 | Per-trial time-series storage (Parquet) | `api/budget_runner.py` (write path) | to build |

**Already available (do not rebuild):** cohesion, fragmentation, outlier_count metrics; `iter_one_trial()` / Experiments path; observation modes and communication factor injection; instrument presets.

---

## 12. HerdSim Architecture

```
Scientific Question
        |
        v
Experiment Definition  (canonical_grid.yaml, ExperimentalFactors)
        |
        v
Scenario               (drive_to_goal, initial_layout via x0_generators)
        |
        v
Collective Model       (sheep dynamics -- unchanged)
        |
        v
Controller / Instrument (herding method -- studied as-is, not modified)
        |
        v
Simulation             (simulation_runner.py -- wrapped, not modified)
        |
        v
Instrumentation        (metrics: cohesion, fragmentation, mean_spread, extent, I_dir, coverage)
        |
        v
Telemetry              (HistoryRecorder -> Parquet per trial)
        |
        v
Trial Results          (manifest.jsonl, summary.csv)
        |
        v
Statistical Analysis   (frontier.py, regimes.py, predictors.py, mechanism.py, ...)
        |
        v
Scientific Conclusion  (evidence packages A-G)
```

### Module layout

```
HerdSim/
├── analysis/budget/
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
│   ├── benchmark_runner.py    [UNCHANGED]
│   └── budget_runner.py       [NEW]
├── configs/budget/
│   └── canonical_grid.yaml    [NEW]
├── core/
│   ├── x0_generators.py       [NEW]
│   └── ...                    [existing files unchanged; see E1]
├── metrics/
│   ├── mean_spread.py         [NEW -- Phase 1]
│   ├── extent.py              [NEW -- Phase 1]
│   ├── shepherd_interference.py [NEW -- Phase 3]
│   ├── shepherd_coverage.py   [NEW -- Phase 3]
│   └── ...                    [existing metrics unchanged]
├── scripts/budget/
│   ├── run_grid.py            [NEW]
│   ├── run_factor_sweep.py    [NEW]
│   └── analyse.py             [NEW]
└── results/budget/            [NEW -- gitignored]
    └── <campaign_id>/
        ├── manifest.jsonl
        ├── summary.csv
        └── timeseries/
```

### Design principles

1. **Additive, not invasive.** New modules over core rewrites. Extend BaseMetric; wrap `iter_one_trial()`.
2. **Composable analysis.** Every analysis function is `DataFrame -> DataFrame`. No hidden state.
3. **Reproducible by default.** Every campaign exports a provenance stamp (git hash, config hash, seed list, metric versions).
4. **Phase-gated.** Build and test each phase before running experiments.
5. **Traceability gate.** Do not merge HerdSim work unless it maps to a row in Section 15.

### Minimal changes to existing files

- `core/experimental_factors.py`: update `INITIAL_LAYOUTS` to `("compact", "wide", "split", "outlier_rich")`; accept `"cluster"` as alias for `"compact"` before validation
- `scenarios/drive_to_goal.py`: call `x0_generators.generate_initial_positions()` when `initial_layout` is set
- `metrics/registry.py`: register new metric classes

### Exception E1 — conditional core change

If RQ3 mechanism analysis reveals wall reflections inflate I_dir confoundingly: add `shepherd_intended_velocities: np.ndarray | None = None` to `SimulationState`. This is the **only permitted core-module change**, gated behind an empirical finding.

---

## 13. Telemetry and Metrics

### Collective-state variables X(t)

| Variable | Definition | Status |
|----------|-----------|--------|
| Cohesion | Mean distance of sheep to flock centroid | exists |
| Fragmentation | Largest connected-component fraction | exists |
| Outlier count | Sheep beyond lost-distance threshold | exists |
| Mean spread | Variance of sheep distances to centroid | to build |
| Extent | Radius of gyration: RMS distance to centroid | to build |

**Secondary (add only if primary variables insufficient):** cluster count (DBSCAN), velocity variance, shape elongation.

### Mechanism metrics

| Metric | Definition | Interpretation |
|--------|-----------|----------------|
| I_dir(t) | `1 - ||sum_i u_hat_i|| / M_active` | 0 = coherent; 1 = maximal conflict |
| Coverage C(t) | Fraction of peripheral sheep within >= 1 shepherd's influence radius | Low C = under-covered |

**I_dir stationary rule:** speed < 1e-6 world-units/tick → excluded from sum and M_active. If M_active = 0: I_dir = 0.

### Frontier quantities

| Quantity | Definition |
|----------|-----------|
| D_min(N, X0) | Smallest D with R >= theta |
| D_overcrowd(N, X0) | Smallest D > D_min at which R drops below theta for >= 2 consecutive D grid steps |
| D_max(N, X0) | Largest D still achieving R >= theta (if overcrowding occurs) |
| B*(N, X0) | Budget (D, T) achieving R >= theta at minimum median effort E |

### D_min identification procedure

1. Scout sweep: 30 seeds per (N, D) cell
2. Identify boundary cells: first D where R > 0.80 and first D where R < 0.95
3. Rerun boundary cells with 100 seeds
4. D_min = smallest D where 100-seed R >= theta
5. Report bootstrap 95% CI on D_min (1,000 iterations)

### Per-trial time-series storage

- Format: Apache Parquet, one file per trial
- Path: `results/budget/<campaign_id>/timeseries/N{n}_D{d}_seed{s}.parquet`
- Phase 1 columns: `tick, cohesion, fragmentation, outlier_count, mean_spread, extent`
- Phase 3 additions: `+ i_dir, coverage`
- Storage budget: ~130 KB per trial (Parquet-compressed); full scout sweep ~1.2 GB

---

## 14. Statistical Design

All statistical decisions are made **before** experiments run. No post-hoc threshold selection.

### Replication and confidence

- Scout phase: 30 seeds per (N, D) cell
- Claim phase: 100 seeds on boundary cells — bootstrap 95% CI on R ~= ±0.06 at R = 0.90
- Default theta: 0.90; also report at theta in {0.50, 0.70}

### Hypothesis tests

| Test | Method |
|------|--------|
| D_min difference across X0 (H1a) | Bootstrap CI comparison |
| Predictor improvement (H1b) | ΔAIC > 4 and out-of-sample log-likelihood |
| Overcrowding existence (H2a) | Sustained R < theta for >= 2 D-grid steps |
| Hard ceiling (H2b) | R < theta even at T1 = 20,000 ticks |
| Mechanism signal (H3) | Wilcoxon rank test, p < 0.05, Holm-Bonferroni corrected |
| Transfer labels (H4) | Quantitative thresholds per property (see RQ4) |
| Information substitution (H5a/b) | DeltaD_min/DeltaI curves; CI on substitution rate |
| Scaling model selection (H6a/b) | ΔAIC > 10; model comparison table |
| Early warning (H7) | AUROC, leave-one-N-out CV; lead-time distribution |

### Breakpoint detection

Use functional modelling (logistic curve fit to R vs D), not the first cell where R changes on a coarse grid. Report breakpoint location with uncertainty (bootstrap). Sensitivity: test with/without boundary cells.

### Overclaiming prevention

All claims are labelled:
- **Simulation result:** observed within HerdSim parameter domain
- **Empirical mechanism:** causal pathway supported by time-series evidence
- **General principle:** mechanism shared across >= 3 instruments (requires Stage D)
- **Real-world implication:** cautious, qualified by scope conditions

Use hedged language: "within the tested parameter domain", "consistent with", "supports the hypothesis that", "provides evidence for."

---

## 15. Research-to-Code Traceability

| RQ | Central claim | Evidence package | HerdSim capabilities | Experiment stage | Decision criterion |
|----|--------------|-----------------|---------------------|-----------------|-------------------|
| RQ1 | Collective state determines herdability beyond N | B | I4, I5, I6 | Stage B | H1a: D_min differs >= 2; H1b: ΔAIC > 4 |
| RQ2 | Herdability regimes exist and have measurable boundaries | A | I1, I2, I3, I13, I14 | Stage A | H2a: overcrowding at >= 2 methods; H2b: hard ceiling confirmed |
| RQ3 | Interference/coverage saturation drive overcrowding | C | I7, I8, I14 | Stage C | H3: I_dir/fragmentation higher in overcrowding cells, p < 0.05 corrected |
| RQ4 | Core mechanisms shared across herding architectures | D | I9 | Stage D | H4: >= 1 mechanism shared across >= 3 methods |
| RQ5 | Information substitutes for physical shepherds | E | I10 | Stage E | H5a: DeltaD_min >= 1; H5b: diminishing returns |
| RQ6 | State-conditioned scaling law (not N alone) | F | I11 | Stage F | H6a: ΔAIC > 10; or H6b: stable sublinear regime |
| RQ7 | State trajectory predicts imminent failure | G | I12 | Stage G | H7a: AUROC(state) > AUROC(N,D); H7b: >= 30% failures with >= 500-tick lead time |
| S8 | Reproducible protocol | all | I1, I13 | Phase 0 | Protocol frozen; provenance on all packages |

**Minimum publishable scientific unit:** RQ1 + RQ2 + RQ3 + S8 (Stages A–C + Phase 0).

---

## 16. Expected Contributions

### Empirical
- **S1:** Collective-state principle — herdability depends on measurable flock state beyond N
- **S2:** Herdability regimes — taxonomy with operationalised boundaries and frontier quantities
- **S3:** Interference–coverage mechanism — explains non-monotonic returns
- **S4:** Cross-method transfer — identifies method-invariant vs instrument-specific mechanisms
- **S5:** Information–shepherding substitution — quantified trade-off
- **S6:** State-conditioned scaling — scaling laws conditioned on collective state
- **S7:** Early warning — predictive indicators of impending failure

### Mechanistic
- Identification of I_dir and coverage saturation as drivers of overcrowding collapse (S3)
- Causal manipulation evidence for collective state as predictor (S1)

### Theoretical (conditional on evidence)
- If RQ4 confirms shared mechanisms: candidate general principle of collective-control limits
- If RQ6 confirms state-conditioned scaling: functional form for capacity planning

### Methodological
- **S8:** Reproducible protocol — locked tasks, seeds, metrics, provenance on HerdSim
- Per-trial time-series telemetry framework
- Traceability architecture: every module maps to a research question

### Applied

| ID | Application | Depends on |
|----|-------------|------------|
| P1 | Size a shepherding force by flock state, not only N | S1, S6 |
| P2 | Detect when extra shepherds waste effort or reduce reliability | S2, S3 |
| P3 | Trade sensors and communication against extra robots | S5 |
| P4 | Monitor operations for early loss-of-herding signals | S7 |
| P5 | Know which operational limits depend on the herding method | S4 |
| P6 | Plan capacity as flocks grow, using state-conditioned scaling | S6 |

---

## 17. Possible Outcomes

| Outcome | What it would mean |
|---------|-------------------|
| H1a and H1b both supported | Collective state is an independent determinant; N-only planning is insufficient |
| H1a supported, H1b not | State shifts minimum resource but does not improve trial-level prediction; use for coarse planning only |
| H1a not supported | N is a sufficient statistic; spread correlation in draft paper was emergent, not causal |
| H2a and H2b both supported | Overcrowding is a genuine hard failure; collective-control regimes with no recovery exist |
| H2a supported, H2b not | Overcrowding is a timeout artefact; no hard ceiling in tested domain |
| H3 supported | Interference and/or coverage saturation are the mechanism; spacing/assignment rules are the design lever |
| H3 not supported | Overcrowding mechanism is not interference-driven; alternative must be investigated |
| H4: mechanisms shared | Findings generalise beyond one algorithm; general principle candidate established |
| H4: all shifted/absent | Results are instrument-specific; external validity claims bounded to tested methods |
| H5a supported | Multi-resource budget confirmed; information and physical capacity are substitutable |
| H5a not supported | Physical headcount dominates; information upgrades do not reduce D_min in tested domain |
| H6a supported | State-conditioned scaling is better than global power law; state matters for growth planning |
| H6a not supported | N-only scaling adequate in tested domain; report single exponent |
| H7 supported | Anticipatory monitoring has operational value; failure can be anticipated |
| H7 not supported | State trajectory adds no predictive value beyond (N, D) |

---

## 18. Limitations

| Limitation | Scope | Mitigation |
|-----------|-------|------------|
| **Single-task bias** | All experiments use `drive_to_goal` (tau_0) | RQ4 partially mitigates; optional robustness check with second task after minimum publishable unit |
| **Single-scenario geometry** | Fixed 150x150 world, corner goal | Document boundary proximity; test larger world or centred goal if wall effects are significant |
| **Discrete-time artefacts** | Tick-based simulation (dt = 0.1) | Report dt; standard in Strombom-family models |
| **Simulation-to-reality gap** | No actuator noise, latency, or GPS error | Scope all claims to simulated domain; physical validation out of scope |
| **Statistical power heuristic** | 30 scout/100 claim seeds are heuristics | CI at 100 seeds ~= ±0.06 at R = 0.90; increase to 200 if Phase 1 shows narrower effects |
| **Herding method coverage** | 3–4 methods tested | Transfer labels bound claims to tested set |
| **No biological validity** | Agent models are abstractions | Do not claim findings predict biological sheep/dog behaviour |

**What this program cannot conclude:**
- Universal laws governing all collective systems
- Real-world effectiveness of any herding strategy
- Biological validity of any mechanism
- Theoretical impossibility in regimes not tested

---

## 19. Implementation Roadmap

| Step | What | Caps | Tests | Phase |
|------|------|------|-------|-------|
| 0.1 | `canonical_grid.yaml` | I13 | Manual review | 0 |
| 0.2 | `provenance.py` | I1, I13 | Unit test | 0 |
| 1.1 | `mean_spread.py`, `extent.py` + registry | I4 | Unit tests | 1 |
| 1.2 | `budget_runner.py` (parallel + manifest + Parquet) | I1, I14 | Integration test (tiny grid) | 1 |
| 1.3 | `frontier.py` | I2 | Unit test with synthetic data | 1 |
| 1.4 | `regimes.py` | I3 | Unit test with synthetic data | 1 |
| 1.5 | `export.py` (Package A) + `plots.py` (heatmap, frontier) | I13 | Integration test | 1 |
| 1.6 | CLI scripts (`run_grid.py`, `analyse.py`) | I1 | Smoke test: assert T0 override (max_ticks = 10,000) | 1 |
| **1.7** | **Run Stage A campaign** | -- | C2 evaluable; frontier + regimes exported | 1 |
| 2.1 | `x0_generators.py` + scenario integration + alias mapping | I5 | Unit test (layout metric gates) | 2 |
| 2.2 | `predictors.py` | I6 | Unit test | 2 |
| **2.3** | **Run Stage B campaign** | -- | H1a/H1b evaluable | 2 |
| 3.1 | `shepherd_interference.py`, `shepherd_coverage.py` | I7 | Unit tests (stationary-shepherd edge case) | 3 |
| 3.2 | `mechanism.py` | I8 | Unit test | 3 |
| **3.3** | **Run Stage C campaign** | -- | H3 evaluable | 3 |
| 4.1 | Multi-instrument grid runner extension | I9 | Integration test | 4 |
| 4.2 | `transfer.py` | I9 | Unit test | 4 |
| **4.3** | **Run Stage D campaign** | -- | H4 evaluable | 4 |
| 5.1 | Factor-sweep runner (`run_factor_sweep.py`) | I10 | Integration test | 5 |
| 5.2 | `substitution.py` | I10 | Unit test | 5 |
| **5.3** | **Run Stage E campaign** | -- | H5a/H5b evaluable | 5 |
| 6.1 | `scaling.py` | I11 | Unit test with synthetic data | 6 |
| **6.2** | **Stage F analysis** (reuses Packages A/B) | -- | H6a or H6b decided | 6 |
| 7.1 | `early_warning.py` | I12 | Unit test | 7 |
| **7.2** | **Stage G analysis** (reuses trial histories from Stages A–C) | -- | H7a/H7b evaluable | 7 |

---

## 20. Experimental Roadmap

```
Phase 0:  Protocol freeze
          -> confirm Section: Protocol Defaults (task, theta, methods, N, D, seeds, master seed)
          -> mark all rows in canonical_grid.yaml as frozen

Phase 1:  Stage A -- herdability maps (baseline method, compact X0)
          -> Package A: reliability maps, frontier, regimes
          -> gate: H2a/H2b evaluable

Phase 2:  Stage B -- collective-state manipulation (all X0 families)
          -> Package B: D_min comparisons across X0, predictor comparison
          -> gate: H1a/H1b evaluable

Phase 3:  Stage C -- mechanism (I_dir and C time series, overcrowding cells)
          -> Package C: mechanism hypothesis verdicts
          -> gate: H3 evaluable
          *** MINIMUM PUBLISHABLE UNIT: Phases 0-3 + S8 ***

Phase 4:  Stage D -- cross-method transfer
          -> Package D: transfer table
          -> gate: H4 evaluable

Phase 5:  Stage E -- information substitution
          -> Package E: substitution curves
          -> gate: H5a/H5b evaluable

Phase 6:  Stage F -- scaling analysis (reuses Packages A/B)
          -> Package F: scaling model fits
          -> gate: H6a or H6b decided

Phase 7:  Stage G -- early warning (reuses trial histories from Stages A-C)
          -> Package G: AUROC, lead-time distributions
          -> gate: H7a/H7b evaluable
```

---

## 21. Publication / Contribution Strategy

### Useful result (minimum threshold for contribution)

Any single evidence package that:
- Reports a reproducible, falsifiable finding with locked seeds and provenance
- Evaluates at least one claim (H1–H7) with stated CI and effect size
- Clearly distinguishes simulation-domain results from general claims

### Strong scientific contribution (Phases 0–3, Packages A + B + C)

> "Operational herdability of collective systems under indirect control depends on measurable collective state, exhibits distinct reliability regimes, and is mechanistically explained by shepherd interference and coverage saturation — findings reproducible under locked seeds across multiple flock sizes."

This is a **Level 2 contribution** (mechanism) — a new scientific account of when and why collective-control systems fail.

### Potentially broader contribution to collective-control science (Phases 0–4, Packages A–D)

> "We discovered and experimentally characterised a previously unresolved principle governing how collective systems can be controlled through limited external agents: herdability is governed by the interaction between collective state, effective controller capacity, and controller interference — mechanisms shared across multiple independent control architectures."

This would be a **Level 3 contribution** (general principle), contingent on:
- Shared transfer labels across >= 3 herding methods (H4 confirmed)
- Mechanism confirmed at Level 2 (H3 confirmed)
- State-conditioned scaling replaces N-only model (H6 confirmed)

**Only pursue the Level 3 claim if the evidence actually supports it.**

---

## Protocol Defaults (to be frozen in Phase 0)

| Item | Default | Status |
|------|---------|--------|
| Task tau_0 | `drive_to_goal` | pending confirm |
| Reliability theta | 0.90 (also report 0.50, 0.70) | pending confirm |
| Baseline herding method | `strombom_multi` | pending confirm |
| Transfer herding methods | `strombom_multi`, `kubo`, `fat`, `communication_free` | pending confirm |
| Flock sizes N | {25, 50, 75, 100, 150, 200, 300, 400} | pending confirm |
| Shepherd counts D | {1, 2, 3, 4, 6, 10, 15, 20, 25, 35} | pending confirm |
| X0 families | compact, wide, split, outlier_rich | pending confirm |
| Time limit T0 | 10,000 ticks (overrides scenario default 3,000) | pending confirm |
| Extended time limit T1 | 20,000 ticks (for H2b hard-ceiling test) | pending confirm |
| Scout seeds | 30 per cell | pending confirm |
| Claim-grade seeds | 100 on boundary cells | pending confirm |
| RQ5 factors | obs mode, sensing range, communication mode | pending confirm |
| RQ7 prediction horizon k | 500 ticks | pending confirm |
| Master seed | 2026 | pending confirm |

> When confirmed, update all rows to **frozen** and begin Phase 1 implementation (Caps I1–I4, I13, I14 only). Cap I5 added when starting Phase 2.

---

## Open Decisions Before Protocol Freeze

1. **Task:** Confirm `drive_to_goal` as tau_0. Optional robustness task `narrow_gate` not required for minimum publishable unit.
2. **Reliability threshold:** theta = 0.90?
3. **Transfer instrument set:** strombom_multi, kubo, fat, communication_free?
4. **Flock sizes:** {25, 50, 75, 100, 150, 200, 300, 400}?
5. **Time limits:** T0 = 10,000 ticks? T1 = 20,000 ticks for H2b?
6. **X0 families:** compact, wide, split, outlier_rich -- sufficient for H1a?
7. **RQ7 parameters:** k = 500 ticks, w = 200 ticks?
8. **Term in titles/abstracts:** use "herdability"; avoid bare "controllability" in public prose.
9. **First cut:** confirm minimum publishable unit = RQ1+RQ2+RQ3+S8 before building Phase 4+ tooling.

---

## Decision Log

| Date | Decision |
|------|----------|
| 2026-09-16 | Research object reframed from dog count to multi-resource budget |
| 2026-09-16 | Budget inputs B = (D, T); effort E as measured outcome |
| 2026-09-17 | RQs restructured: RQ1 (state), RQ2 (boundary), RQ3 (mechanism), RQ4 (transfer), RQ5 (information), RQ6 (scaling), RQ7 (early warning) |
| 2026-09-17 | Mechanism metrics added: I_dir (interference), C (coverage) |
| 2026-09-17 | X0 families defined: compact, wide, split, outlier_rich |
| 2026-09-17 | N grid expanded to 8 points for scaling fits |
| 2026-09-17 | Minimum publishable unit: RQ1+RQ2+RQ3+S8 |
| 2026-09-17 | Traceability matrix I1-I14 added; phase done-when criteria tied to claims |
| 2026-09-17 | Herdability replaces controllability in prose |
| 2026-09-17 | I_dir stationary-shepherd rule specified (speed < 1e-6 -> excluded) |
| 2026-09-17 | C2b hard-ceiling test: T1 = 20,000 ticks |
| 2026-09-17 | D_overcrowd defined over grid-ordered D-steps |
| 2026-09-17 | Transfer labels operationalised with quantitative thresholds |
| 2026-09-17 | Information-ladder ordinal levels defined |
| 2026-09-17 | Parallelisation strategy: ProcessPoolExecutor |
| 2026-09-17 | Per-trial time-series format: Parquet |
| 2026-09-17 | Exception E1: conditional shepherd_intended_velocities |
| 2026-09-17 | Program generated from master_prompt.md; supersedes main_shepherding_budget_plan.md draft |
| pending | Protocol freeze (Section: Protocol Defaults) |
