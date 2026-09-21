# Collective Herdability Under Shepherding

Status note: Section 8 protocol frozen (`scaling_v1`). Caps I1-I14 built. Claim-grade phases: tracker.

Domain terms (`N`, `D`, `D_min`, control demand, ...): research program Terms table.

| Abbreviation | Meaning |
|--------------|---------|
| *method* | Dog algorithm; code id may still be `dog_controller` |
| *R* / *theta* | Success rate; reliability threshold |
| *I_dir* | Shepherd interference index |
| *C* | Shepherd coverage of peripheral sheep |
| `B*` | Best (D, T) at target R with least effort |
| *AIC* / *BIC* | Model-comparison scores (lower is better; Package F) |
| *Delta AIC* / *Delta BIC* | Difference between two fitted models |
| *AUROC* | Ranking quality for early warning (Package G) |
| *GCM* | Flock global centre of mass |
| *RMS* | Root-mean-square |
| *S_bar* | Mean-spread (variance of distances to centroid) |
| *lead time* | Ticks between a warning and actual failure |

---

## Work map

| Phase | Focus | RQ | Package | Depends on | Done when |
|-------|-------|----|---------|------------|-----------|
| 0 | Freeze protocol | S8 | all | n/a | Section 8 rows frozen |
| 1 | Size map: R(N, D), frontier, regimes (baseline) | RQ2 | A | 0 | Package A: frontier + regimes + reliability map |
| 2 | Structure: vary X_0 at fixed N; compare D_min | RQ1 | B | 1 | Package B: verified X_0 families; D_min(N, X_0) comparable |
| 3 | Mechanism: I_dir / C / fragmentation on contrast cells | RQ3 | C | 1 | Package C: I_dir and C series for contrast cells |
| 4 | Generality: other methods; transfer table | RQ4 | D | 1-3 | Transfer table for >= 3 methods |
| 5 | Follow-on: information vs shepherd count | RQ5 | E | 1 | Package E on methods that consume I factors |
| 6 | Scaling fits (uses Phase 1-2 data) | RQ6 | F | 1-2 | Package F model-comparison table |
| 7 | Follow-on: early warning from trajectories | RQ7 | G | 1-3 | Package G: AUROC + lead-time distribution |

Smallest publishable unit: **RQ1 + RQ2 + RQ3 + S8**. RQ4-RQ7 reuse the same protocol afterward.

| Package | Must contain |
|---------|--------------|
| A | R(N, D) maps; D_min, D_overcrowd, D_max, B*; regime labels; provenance |
| B | Per-(N, X_0, D) reliability; D_min(N, X_0); predictor comparison |
| C | Per-trial I_dir(t), C(t); regime-paired rank tests; mechanism verdicts |
| D | Transfer table: property x method -> shared / shifted / absent |
| E | D_min(N, I); Delta D_min/Delta I; method-conditional notes |
| F | Power-law / piecewise / state-conditioned fits; Delta AIC/BIC |
| G | AUROC; lead-time distributions; feature-importance ranks |

---

## How we measure

### Notation

**Herdability / R.** How often a fixed setup (method, task, N, D, T, X_0, I) reaches the goal under locked seeds. Herdable at `theta` when `R >= theta`.

```text
R(m, tau, N, D, T, X_0, I) = P(success | locked seeds)
```

Default theta = 0.90; also report 0.50 and 0.70. Mechanism metrics explain patterns; they do not replace R.

| Kind | Symbol | Meaning |
|------|--------|---------|
| Input | D | Shepherd count |
| Input | T | Time limit (ticks) |
| Outcome | S | Success (binary) |
| Outcome | t_s | Time to success (if successful) |
| Outcome | E | Realised effort: total shepherd path length |
| Outcome | X(t) | Collective-state trajectory |
| Context | N | Flock size |
| Context | m | Herding method |
| Context | tau | Task; tau_0 = `drive_to_goal` |
| Context | X_0 | Initial state family |
| Context | I | Information condition |

### Collective state and mechanism metrics

| Variable | Definition | Source |
|----------|------------|--------|
| Cohesion | Mean distance of sheep to GCM | `plugins/metrics/cohesion.py` |
| Fragmentation | Largest connected-component fraction under measurement radius | `plugins/metrics/fragmentation.py` |
| Outlier count | Sheep beyond lost-distance threshold | `plugins/metrics/outlier_count.py` |
| Spread | Variance of distances to centroid (S_bar) | `plugins/metrics/mean_spread.py` |
| Extent | Radius of gyration (RMS to centroid) | `plugins/metrics/extent.py` |

Secondary (only if primary predictors fail): cluster count, velocity variance, shape elongation.

| Metric | Definition | Reading |
|--------|------------|---------|
| I_dir(t) | `1 - \|\|sum_i u_hat_i(t)\|\| / M_active` for moving shepherds | 0 = coherent; 1 = maximal conflict |
| C(t) | Fraction of peripheral sheep in at least one shepherd influence radius | Low = under-covered; plateau = coverage saturation |

Peripheral sheep: distance to GCM above the median. Influence radius: `r_s` from `state.metadata` (default 2.0).

**I_dir stationary rule.** Speed below 1e-6: exclude from numerator and M_active. If none move, I_dir(t) = 0.

**I_dir caveat.** Compute from realised velocities (`state.shepherd_velocities`). Wall reflections can inflate I_dir near boundaries. If that confounds RQ3, add intended velocities (exception E1 under Caps).

### Frontiers, D_min procedure, regimes

| Quantity | Definition |
|----------|------------|
| D_min(N, X_0) | Smallest D with R >= theta |
| D_overcrowd(N, X_0) | Smallest D > D_min where R stays below theta for >= 2 consecutive *ordered D-grid* entries |
| D_max(N, X_0) | Largest D still with R >= theta (if overcrowding occurs) |
| B*(N, X_0) | (D, T) with R >= theta at minimum median E; ties: smaller D, then faster t_s |

**D_min procedure**

1. Scout: 30 seeds per cell on the full (N, D) grid
2. Boundary cells: first D (grid order) with R > 0.80 and first with R < 0.95
3. Rerun boundaries with 100 seeds
4. D_min = smallest D with 100-seed R >= theta
5. Bootstrap 95% CI on D_min (1,000 resamples of the 100 seeds)

| Regime | Definition |
|--------|------------|
| Under-resourced failure | R < theta |
| Efficient operation | R >= theta, D at or near D_min, effort competitive |
| Wasteful overspend | R >= theta, median E >= 20% above efficient with no reliability gain (sensitivity 10%/30%) |
| Overcrowding collapse | R < theta for D > D_overcrowd |
| Hard failure | No tested D reaches R >= theta within T |

---

## How we run each RQ

### RQ1: Structure (Package B, Phase 2)

Does the same N have different herdability under different X_0?

- Fix N in {50, 100, 200}
- X_0: compact, wide, split, outlier_rich (layout contract under Caps)
- Sweep D from the frozen D grid
- Compare D_min(N, X_0); fit R ~ f(N, D, state) vs R ~ f(N, D); OOS log-likelihood and Delta AIC

### RQ2: Size boundary and regimes (Package A, Phase 1)

Where does reliable herding end as D grows, and how sharp is the boundary?

- R(N, D) at T_0; label regimes
- Transition width in D-grid steps (efficient to overcrowding)
- T_1 hard-ceiling check on overcrowding cells

### RQ3: Mechanism (Package C, Phase 3)

Why do extra shepherds stop helping?

| Hypothesis | Expected signature |
|------------|-------------------|
| Interference | I_dir rises with D *before* R falls |
| Coverage saturation | C plateaus while E keeps rising |
| Induced fragmentation | Fragmentation higher in overcrowding vs efficient |
| Redundant effort | E rises, R flat, I_dir not necessarily high |

Compare overcrowding vs efficient cells at the same N (median I_dir / fragmentation, rank tests; temporal order).

### RQ4: Generality (Package D, Phase 4)

Which patterns transfer across methods under locked task, seeds, and metrics?

- Required: `strombom_multi`, `kubo`, `fat`
- Recommended: `communication_free`
- Optional: `v_formation`, `adaptive`

| Property | shared | shifted | absent |
|----------|--------|---------|--------|
| State-dependent D_min (RQ1) | same pattern, abs(Delta D_min) <= 2 | same direction, abs(Delta D_min) > 2 | no significant effect |
| Overcrowding (RQ2) | exists at D/N within 1.5x | exists at very different D | not observed |
| I_dir signature (RQ3) | r(I_dir, R) < -0.3 in both | present, magnitude differs | not significant |
| Coverage saturation; RQ5 / RQ7 patterns | analogous thresholds | magnitude/threshold differs | not observed |

### RQ5: Information vs shepherds (Package E, Phase 5)

Can better sensing or communication cut D_min at fixed reliability?

- N in {100, 200}, theta = 0.90
- Ladders: obs (bearing_only -> local_positions -> global); range (x0.5 -> x1 -> x1.5 -> x2); comm (none -> neighbour_broadcast -> global_shared)
- D_min(N, I_k); first and second step Delta D_min

### RQ6: Scaling fits (Package F, Phase 6)

How does required resource grow with N and state?

- D_min(N, X_0) on the frozen N grid
- Fit power-law, piecewise, state-conditioned; AIC/BIC + CV
- Cross-method after RQ4 data exist

### RQ7: Early warning (Package G, Phase 7)

Can state predict failure before timeout?

- Windowed X(t), I_dir(t), C(t) -> P(failure within k | features at t)
- Baseline: logistic on (N, D); leave-one-N-out CV
- Frozen: k = 500; w = 200; evaluate every 200 ticks from 1,000 to 8,000

---

## Protocol freeze (Section 8)

Machine-readable: [../configs/canonical_grid.yaml](../configs/canonical_grid.yaml).  
Subsets: [../configs/protocols/](../configs/protocols/). Every override needs a WHY comment (`protocols/README.md`).

Frozen:

| Item | Default |
|------|---------|
| Task tau_0 | `drive_to_goal` |
| Reliability theta | 0.90 (also report 0.50, 0.70) |
| Baseline method | `strombom_multi` |
| Transfer methods | `strombom_multi`, `kubo`, `fat`, `communication_free` |
| N | {5, 10, 25, 50, 75, 100, 150, 200, 300, 400} |
| D | {1, 2, 3, 4, 6, 10, 15, 20, 25, 35} |
| X_0 | compact, wide, split, outlier_rich |
| T_0 | 10,000 ticks |
| T_1 | 20,000 ticks (hard-ceiling vs timeout) |
| Scout / claim seeds | 30 / 100 on boundary cells |
| RQ5 factors | obs mode, sensing range, communication |
| RQ7 k / w | 500 / 200 ticks |
| Master seed | 2026 |

Changing a frozen default needs a tracker protocol exception and usually a new `protocol_id`. Code follows the protocol; do not rewrite the science to match whatever the code already supports.

### 8.1 Why these defaults

Longer notes: comments in `canonical_grid.yaml`.

| Choice | Why |
|--------|-----|
| `drive_to_goal` | Shared operational herdability task |
| theta = 0.90 | Reliable band (SR >= 90%); sensitivity at 0.50/0.70 |
| `strombom_multi` | Coordinated Collect/Drive multi-dog baseline |
| Transfer set | Distinct architectures (force / local FAT / no shared targets) |
| N grid | Scale ladder; floor N=5 (8.1.1); 5-10 = hard small flock; 75/150 resolve ~100; 300/400 large-N |
| D grid | Fine at low D; ceiling 35 practical cap |
| X_0 | Causal axes for RQ1 (spread, fragmentation, outliers) |
| T_0 = 10000 | Failures reflect control limits, not a short default clock |
| T_1 = 20000 | Hard-ceiling vs timeout only |
| Scout 30 / claim 100 | Cheap map then precise D_min CI |
| Master seed 2026 | Reproducible base |
| RQ7 k/w | 5% of T_0; fixed feature window |
| Wasteful 20% | Default effort tolerance; sensitivity 10%/30% |

### 8.1.1 Why N floor is 5

Science choice about indirect control of a *collective*, not an implementation limit.

Below N=5 the quantities stop meaning the same thing: no sheep-sheep collective at N=1; outlier_rich (majority core + minority outliers) is not the same factor at N=2-4; periphery-by-median for C is nearly tautological at N=2-3; Collect/Drive relative to a flock GCM becomes individual chase. N=5 is the smallest size where structure, mechanism metrics, and the herding task still match the larger-N object. N=5 and 10 stay in the freeze for the hard small-flock regime.

N=1-4 would need a separate individual-pursuit protocol, not a mix into this freeze.

---

## Caps (HerdSim capabilities)

Principles: additive modules; analysis is DataFrame in/out; provenance on every campaign; phase-gated tooling; no Cap without a row below.

| Cap | Serves | Capability | Location | Status | Package |
|-----|--------|------------|----------|--------|---------|
| I1 | RQ2, RQ6 | N x D x seed grid runner + resume + provenance | `scaling/services/scaling/runner.py`, `analysis/scaling/provenance.py` | built | A, F |
| I2 | RQ2 | Frontier D_min, D_overcrowd, D_max, B* | `analysis/scaling/frontier.py` | built | A |
| I3 | RQ2 | Regime labelling | `analysis/scaling/regimes.py` | built | A |
| I4 | RQ1, RQ6, RQ7 | Mean-spread, extent | `plugins/metrics/mean_spread.py`, `extent.py` | built | B, F, G |
| I5 | RQ1 | X_0 generators + scenario wiring | `core/x0_generators.py` | built | B |
| I6 | RQ1 | State vs (N, D) predictors | `analysis/scaling/predictors.py` | built | B |
| I7 | RQ3, RQ7 | I_dir, C | `plugins/metrics/shepherd_interference.py`, `shepherd_coverage.py` | built | C, G |
| I8 | RQ3 | Mechanism tests | `analysis/scaling/mechanism.py` | built | C |
| I9 | RQ4 | Multi-method + transfer table | `analysis/scaling/transfer.py` | built | D |
| I10 | RQ5 | Factor sweeps + substitution | `scaling/scripts/run_factor_sweep.py`, `analysis/scaling/substitution.py` | built | E |
| I11 | RQ6 | Scaling fits | `analysis/scaling/fits.py` | built | F |
| I12 | RQ7 | Early-warning eval | `analysis/scaling/early_warning.py` | built | G |
| I13 | S8 | Canonical config + dossier export | `scaling/configs/canonical_grid.yaml`, `analysis/scaling/export.py` | built | all |
| I14 | RQ3, RQ7 | Per-trial Parquet timeseries | runner write path | built | C, G |

Already available (do not rebuild): cohesion, fragmentation, outlier_count; `iter_one_trial`; obs/communication factors; RQ4 method presets.

**Acceptance.** A phase answers its RQ only when matching Caps are built and unit-tested *and* Work map "Done when" is met.

### Layout contract (X_0) and RQ1 gate

| Layout | Definition | Gate metric |
|--------|------------|-------------|
| compact | Single Gaussian, sigma = 0.3 x default spread | Low cohesion distance |
| wide | Single Gaussian, sigma = 2.0 x default | High cohesion distance |
| split | 2-3 subclusters at distance >= 2x interaction radius | Low fragmentation index |
| outlier_rich | Core ~80% + outliers ~20% beyond lost threshold | High outlier count |

Wired via `INITIAL_LAYOUTS` and `DriveToGoalScenario` -> `x0_generators.generate_initial_positions()`.

**RQ1 gate:** unit tests must show sampled layouts differ on the intended metric before claim-grade Package B.

### Timeseries and operator paths

```text
scaling/results/phase{k}/{protocol_slug}/timeseries/<cell_key>.parquet
```

Phase 1 columns: `tick, cohesion, fragmentation, outlier_count, mean_spread, extent`. Phase 3+: `i_dir, coverage`.

Runner: ProcessPoolExecutor; resume via append-only `manifest.jsonl`. T_0 via `max_ticks: 10000` in canonical config.

CLI: `make -C scaling help` (`scaling-pilot`, `scaling-scout`, `scaling-pilot-state`, `scaling-factor-sweep`, `scaling-analyse`).

```text
analysis/scaling/     # Caps analysis (packages A-G)
services/scaling/     # runner + layout helpers
scaling/configs/      # canonical_grid.yaml + protocols/
scaling/scripts/      # run_grid, run_factor_sweep, analyse
scaling/results/      # phase{k}/{protocol}/ + packages/{a-g}/ + REPORT.md
```

### Do not modify (and exception E1)

Leave alone: `core/simulation_runner.py`, `core/experiment_config.py`, `analysis/failure_taxonomy.py`, `methods/*`, sheep/dog plugins.

Allowed touch: `INITIAL_LAYOUTS`; DriveToGoal initial positions; metric registry.

**E1 (conditional only):** if wall reflections confound I_dir, add optional `shepherd_intended_velocities` on `SimulationState`, filled before constraints. Do not pre-build.

### Non-goals for HerdSim work

- New herding method as the research goal
- Rewriting the simulator into a general multi-agent platform
- Single-method results claimed as universal without RQ4
- Pre-building later-phase tooling before earlier claim-grade runs need it
- Analysis modules with no Cap ID
- Scope beyond locked-protocol RQs and Packages A-G

---

## Threats to validity

| Threat | Mitigation |
|--------|------------|
| Single task (`drive_to_goal`) | RQ4 varies method; second task is optional after RQ1-RQ3, not required for first paper |
| Fixed 150x150 corner-goal geometry | Document boundary proximity; larger world / centred goal only if walls confound |
| Discrete time dt = 0.1 | Report dt; results apply at this resolution |
| Simulated method fidelity | Scope claims to simulation; physical validation out of scope |
| Scout 30 / claim 100 not formally powered | At R=0.90, 100 seeds give ~+/-0.06 CI on R; Delta D_min >= 2 is the detection target. If Phase 1 shows narrower effects, raise boundary cells to 200 seeds before Phase 2 |

---

## Claims

Canonical support criteria. Tracker holds verdicts. Reports cite evidence paths. Fill claims only at **CLAIM** grade after reading `packages/*/`.

| Claim | RQ | Supported when |
|-------|----|----------------|
| C1a | RQ1 | For at least one N, D_min differs by >= 2 across X_0 at theta = 0.90 |
| C1b | RQ1 | State features beat (N, D) on OOS log-likelihood and Delta AIC > 4 |
| C2a | RQ2 | Overcrowding for at least two methods at theta = 0.90 |
| C2b | RQ2 | Some D > D_overcrowd still has R < theta at T_1 = 20,000 |
| C3 | RQ3 | Overcrowding cells higher median I_dir and/or fragmentation vs efficient (rank p < 0.05, corrected) |
| C4 | RQ4 | At least one core mechanism shared across >= 3 of 4 required+recommended methods |
| C5a | RQ5 | One ladder step reduces D_min by >= 1 at N in {100, 200} with R >= theta |
| C5b | RQ5 | Second ladder step saves fewer shepherds than the first |
| C6a | RQ6 | Global power law rejected vs piecewise/state (Delta AIC > 10) |
| C6b | RQ6 | Stable sublinear regime (alpha < 1) in a stated N, X_0 domain |
| C7a | RQ7 | State-based warning AUROC > (N, D)-only baseline on held-out trials |
| C7b | RQ7 | Lead time >= 500 ticks on >= 30% of failure trajectories |

Verdicts: UNEVALUATED / SUPPORTED / REJECTED / INCONCLUSIVE.
