---
name: Extension implementation plan
overview: Clean-cut near-term HerdSim redesign for herdability, sensing, and heterogeneity experiments, plus sequenced future phases that complete the full extension.md research programme (communication, adaptive control, RL, empirical validation, robot constraints).
todos:
  - id: evaluate-extension
    content: Treat extension.md as research requirements and select the feasible first research question
    status: completed
  - id: factor-config
    content: Implement ExperimentalFactors and factor-based config resolver
    status: completed
  - id: core-contracts
    content: Replace BaseAlgorithm with SheepDynamics, ObservationModel, and DogController
    status: completed
  - id: migrate-models
    content: Migrate Strombom, Kubo, Jadhav, V-formation, and obstacle-aware controllers; delete duplicated variants
    status: completed
  - id: observation
    content: Implement global, local, bearing-only, noisy-bearing, and intermittent observation modes
    status: completed
  - id: agent-factors
    content: Add structured sheep/shepherd attributes for heterogeneity and dog failure
    status: completed
  - id: factor-grid
    content: Replace two-param sweep with factor-grid experiments and provenance
    status: completed
  - id: api-frontend
    content: Align API and frontend controls with factor bundles
    status: completed
  - id: docs-tests
    content: Rewrite docs and tests to match the new architecture; remove old API references
    status: completed
  - id: first-study
    content: Run herdability, sensing, and heterogeneity grids as the first supported research study
    status: completed
  - id: future-comm-fat
    content: "Future: communication factor + FAT / communication-free controllers"
    status: completed
  - id: future-env-cohesion
    content: "Future: cohesion spectrum, dynamic goals/paths, richer obstacle environments"
    status: completed
  - id: future-adaptive
    content: "Future: context-aware adaptive controller and lead/herd switching"
    status: completed
  - id: future-generalization
    content: "Future: train/test domain split and generalization-gap reporting"
    status: completed
  - id: future-rl
    content: "Future: RL/imitation train-eval harness as a DogController backend"
    status: completed
  - id: future-empirical
    content: "Future: Jadhav empirical calibration and information-propagation metrics"
    status: completed
  - id: future-behavioural
    content: "Future: behavioural event sequences and transition-matrix validation"
    status: completed
  - id: future-robot
    content: "Future: robot kinematics, latency, and predictive/MPC-style constraints"
    status: completed
  - id: future-universality
    content: "Future: dimensionless predictors and cross-controller herdability laws"
    status: completed
isProject: false
---

# HerdSim extension implementation plan

## Evaluation of extension.md

The analysis in [`.cursor/plans/extension.md`](.cursor/plans/extension.md) is directionally correct: HerdSim should move from "algorithm comparison" toward controlled experiments about herdability, information, robustness, heterogeneity, and generalization. It correctly identifies the main research opportunity: vary assumptions independently while holding tasks, seeds, metrics, and analysis constant.

The document is too broad to implement directly. It mixes near-term platform requirements with long-term research themes: RL, empirical calibration, physical robot constraints, behavioural validation, field theory, adaptive leading/herding, and 2026 robotics work. Those are valuable as research context, but the next build should target the smallest architecture that makes those questions possible later.

The current implementation confirms this gap:

- [`core/simulation_runner.py`](core/simulation_runner.py) still calls one monolithic algorithm object with full global state.
- [`core/base_algorithm.py`](core/base_algorithm.py) defines `step(state, config)`, which prevents real observation-limited experiments.
- [`algorithms/registry.py`](algorithms/registry.py) registers full algorithm bundles, including variants that should become factors (`strombom_noise`, `heterogeneous`).
- [`api/benchmark_sweep.py`](api/benchmark_sweep.py) supports only a two-parameter sweep, which is not enough for herdability phase diagrams.
- [`metrics/registry.py`](metrics/registry.py) already has useful model-independent metrics, so metrics should be extended but not redesigned first.

The implementation plan should therefore meet the goal of `extension.md` by building a clean factor-based architecture first, then using it to run a focused research programme: **minimum dog requirement under heterogeneity and sensing limits**.

## Chosen implementation goal

### Near-term (Phases 1-9)

Implement a clean HerdSim architecture that can answer this first concrete research question:

> How does the minimum number of shepherds required for successful herding change with flock size, sheep responsiveness, and sensing quality?

This covers the highest-value near-term parts of `extension.md`:

- herdability phase diagrams
- limited information experiments
- heterogeneous sheep
- robustness/generalization groundwork
- model-independent metrics
- reproducible factor grids

### Full programme (Future Phases 10-18)

After the platform is stable, continue until HerdSim can support the overarching `extension.md` question:

> How do agent heterogeneity, information constraints, environmental complexity, and controller architecture determine the herdability, robustness, and generalization of multi-agent shepherding systems?

That requires the future phases for communication/FAT, cohesion and dynamic environments, adaptive control, generalization benchmarks, RL, empirical calibration, behavioural validation, robot constraints, and dimensionless herdability analysis.
## Target architecture

Replace the current single algorithm pipeline with a clean, factor-driven pipeline:

```text
ExperimentalFactors
  -> ExperimentConfig
  -> Scenario initial state
  -> SheepDynamics
  -> ObservationModel
  -> DogController
  -> Environment constraints
  -> Metrics
  -> FactorGrid analysis
```

The engine contract after this implementation:

```text
state(t)
  -> apply environment updates
  -> sheep_dynamics.step(state, config)
  -> observation_model.observe(state, shepherd_index, config)
  -> dog_controller.step(state, observations, config)
  -> resolve obstacles and walls
  -> metrics(state(t+1))
```

No backward-compatibility adapter will remain. Existing behaviour is preserved through migrated implementations and regression tests, not through old code paths.

## Phase 1: Core factor model

Create [`core/experimental_factors.py`](core/experimental_factors.py) as the only high-level experiment specification.

Factor groups:

- `FlockFactors`: `n_sheep`, `initial_layout`, `initial_spread`, `cohesion_scale`, `stubborn_fraction`, `stubborn_response_scale`
- `ShepherdFactors`: `n_shepherds`, `speed_scale`, `failure_mode`, `failure_tick`
- `ObservationFactors`: `mode`, `sensing_range`, `noise_sigma`, `observation_frequency`
- `EnvironmentFactors`: current world keys plus `goal_mode`, `goal_velocity`
- `ModelFactors`: `sheep_model`, `dog_controller`, `scenario`, `preset`

Update [`core/experiment_config.py`](core/experiment_config.py) so `resolve_experiment_config` accepts factors and returns one resolved config for runner/API/reporting. Remove parallel flat config ownership after API migration is complete.

Why: this turns the research variables in `extension.md` into the software contract, so HerdSim can run condition-based experiments instead of hand-coded algorithm comparisons.

## Phase 2: Replace algorithm bundles

Replace [`core/base_algorithm.py`](core/base_algorithm.py) with three interfaces:

- [`core/sheep_dynamics.py`](core/sheep_dynamics.py): `BaseSheepDynamics.step(state, config)`
- [`core/observation.py`](core/observation.py): `BaseObservationModel.observe(state, shepherd_index, config)`
- [`core/dog_controller.py`](core/dog_controller.py): `BaseDogController.step(state, observations, config)`

Create registries for sheep dynamics, observation models, and dog controllers. Remove [`algorithms/registry.py`](algorithms/registry.py) as the engine selector after migration.

Migrate the existing models as combinations:

- Strombom: `sheep_model=strombom`, `dog_controller=collect_drive`
- Strombom multi: `sheep_model=strombom`, `dog_controller=collect_drive_multi`
- Kubo: `sheep_model=kubo`, `dog_controller=kubo_forces`
- Jadhav/Flocking Dog: `sheep_model=jadhav`, `dog_controller=collect_drive`
- V-formation: `sheep_model=strombom`, `dog_controller=v_formation`
- Obstacle-aware: `sheep_model=strombom`, `dog_controller=obstacle_aware_drive`

Delete standalone duplicate variants after migration:

- `strombom_noise` becomes a noise factor/preset.
- `heterogeneous` becomes flock responsiveness factors.

Why: `extension.md` depends on independent variation of model, sensing, environment, and controller. That is impossible while sheep and dog behaviour are locked inside one algorithm plugin.

## Phase 3: Observation modes

Implement observation models used by all dog controllers:

- `global`: complete state, represented as a `ShepherdObservation` object
- `local_positions`: sheep and dog positions filtered by `sensing_range`
- `bearing_only`: bearing angles without distance
- `noisy_bearing`: bearing angles with `noise_sigma`
- `intermittent`: cached observations updated every `observation_frequency` ticks

All dog controllers consume observation objects only. Do not pass raw full `SimulationState` into controllers.

Why: this implements the information axis from `extension.md` and enables experiments like success probability versus sensing quality.

## Phase 4: Heterogeneity and failure factors

Move sheep response variation into typed state attributes rather than algorithm-specific metadata.

Add structured agent attributes to [`core/simulation_state.py`](core/simulation_state.py):

- per-sheep response scale
- per-sheep cohesion scale
- per-dog speed scale
- per-dog active mask
- per-dog sensing scale

Implement failure modes:

- `none`
- `inactive_after_tick`
- `reduced_speed_after_tick`
- `blind_after_tick`

Why: this supports the robustness and heterogeneous-population claims in `extension.md` without duplicating controllers.

## Phase 5: Factor-grid experiments

Replace the two-param sweep path in [`api/benchmark_sweep.py`](api/benchmark_sweep.py) with a factor-grid runner.

Create [`scripts/run_factor_grid.py`](scripts/run_factor_grid.py) using the same trial loop as API benchmarks.

Required first grids:

- `n_sheep x n_shepherds` for herdability phase diagrams
- `observation.mode x sensing_range x noise_sigma` for information curves
- `stubborn_fraction x n_shepherds` for heterogeneity thresholds

Every trial row must include:

- factor values
- resolved config
- seed
- scenario
- sheep model
- dog controller
- success
- total ticks
- current trajectory aggregates from [`api/benchmark_aggregates.py`](api/benchmark_aggregates.py)

Why: this turns the research programme in `extension.md` into executable, reproducible experiments.

## Phase 6: Metrics and analysis outputs

Keep existing metrics as the core layer:

- success rate
- time to goal
- GCM to goal
- cohesion
- fragmentation
- polarization
- outlier count
- shepherd path

Add only the metrics needed for the first research question:

- final herdability label per trial: success/fail under threshold
- estimated `required_shepherds` per factor cell
- degradation slope for sensing/noise sweeps
- recovery time after dog failure

Do not implement information propagation, behavioural sequence validation, or empirical-data metrics yet.

Why: `extension.md` proposes many useful metrics, but implementing all of them now would delay the architecture needed to run the first scientific study.

## Phase 7: API and frontend alignment

Update the API to expose presets as factor bundles instead of algorithm-only presets.

Update frontend parameter plumbing so Arena/Analytics can select:

- preset/instrument
- scenario
- sheep model
- dog controller
- observation mode
- key factor overrides

Keep the first UI small: expose the factor axes needed for herdability, sensing, and heterogeneity experiments. Hide not-yet-supported frontier topics.

Why: implementation and docs must reflect the same model. A clean backend with an old algorithm-only UI would create confusion and dead code.

## Phase 8: Docs alignment

Rewrite existing docs, not a separate long markdown summary.

Update:

- [`README.md`](README.md): HerdSim as factor-based herdability lab
- [`docs/architecture.md`](docs/architecture.md): new tick pipeline, interfaces, factors
- [`docs/research/comparison_framework.md`](docs/research/comparison_framework.md): fair compare as one use case of factor grids
- [`docs/research/related_work.md`](docs/research/related_work.md): align with the strongest `extension.md` themes: herdability, information, heterogeneity, generalization
- [`docs/research/metrics.md`](docs/research/metrics.md): existing metrics plus first factor-derived outputs
- [`docs/research/algorithms/README.md`](docs/research/algorithms/README.md): replace algorithm list with sheep-model x dog-controller mapping
- developer/user guide pages that mention `BaseAlgorithm`, algorithm-only presets, or two-param sweeps

All documentation should be ASCII-only and describe current implementation only. Do not copy the entire literature analysis into docs.

Why: the user-facing claim must match what the code can actually do.

## Phase 9: Tests and cleanup

Replace tests for removed APIs with tests for the new contracts.

Required tests:

- factor validation and resolved config determinism
- `SimulationRunner` tick order with sheep dynamics, observation, dog controller, constraints, metrics
- observation filtering for global/local/bearing/noisy modes
- responsiveness factor creates expected sheep attributes deterministically
- dog failure factors change active/sensing/speed state as expected
- migrated Strombom/Kubo/Jadhav smoke tests produce finite trajectories and preserve rough baseline behaviour under `global`
- factor-grid runner emits complete provenance and expected number of trial rows
- API smoke tests create and step a factor-based simulation

Cleanup checks:

- no subclass of removed `BaseAlgorithm`
- no registry entry for deleted algorithm variants
- no unused config keys such as inactive vision flags
- no duplicate Collect/Drive helper logic
- no docs referencing old contracts

Why: the clean-cut plan only works if tests guard against partial migration and stale compatibility code.

## Deferred scope (now sequenced as future phases)

The items below were previously deferred. They are now explicit future implementation phases that complete the `extension.md` intention after Phases 1-9 are stable. Do not start them until the clean factor platform and first herdability study work.

## Future Phase 10: Communication and local-information controllers

Goal: answer **RQ2 / SQ4** from `extension.md` -- how much communication is necessary?

Implement:

- Communication factor: `none` | `neighbour_broadcast` | `global_shared`
- Message-passing hook between dog controllers (typed messages, not shared mutable state)
- `fat` dog controller (farthest-agent targeting under local observation)
- `communication_free` multi-dog controller (Li-style local decision without inter-dog messages)

Experiments:

- communication level x observation mode x n_shepherds
- ranking reversal under local vs global information

Deliverable: information-sharing curves and a second controller family beyond Collect/Drive and Kubo forces.

## Future Phase 11: Cohesion spectrum and richer environments

Goal: answer non-cohesive flock and environmental complexity themes (Families F/G).

Implement:

- `cohesion_scale` continuum from strong flocking to independent agents
- dynamic goal / corridor / dynamic-path scenarios
- denser obstacle and gate layouts as environment factors, not new algorithm forks
- optional density packing helpers for herdability density studies

Experiments:

- P(success) vs cohesion_scale across controllers
- phase boundary vs obstacle density and dog count (El-Fiqi-style)

Deliverable: environment/cohesion phase diagrams on the same factor runner.

## Future Phase 12: Adaptive and context-aware control

Goal: answer **RQ4 / SQ5** -- does adaptation improve robustness under distribution shift?

Implement:

- flock-state classifier (dispersed / cohesive / fragmented) from observations
- `adaptive` dog controller that selects from a behaviour library (collect, drive, recover, later lead)
- optional lead/herd switching (Strombom 2026 style) as a behaviour library entry once sheep attraction/repulsion modes exist

Experiments:

- fixed vs adaptive under held-out scenarios (obstacles, noise, heterogeneous sheep)
- generalization gap G = P_train - P_test

Deliverable: adaptive vs fixed robustness comparison without claiming a universal best algorithm.

## Future Phase 13: Generalization benchmark suite

Goal: make generalization a first-class product (Family I framing, not only RL).

Implement:

- named train domains and held-out test domains as factor manifests
- `scripts/run_generalization.py` wrapping the factor-grid runner
- report templates for ranking reversal and generalization gap

Train domain example:

- open field, homogeneous sheep, global sensing, low noise

Test domains:

- obstacles, heterogeneous sheep, local/bearing sensing, high noise, dog failure

Deliverable: standardized generalization reports for every controller family.

## Future Phase 14: Learning-based controllers

Goal: answer whether learned policies generalize better than hand-designed ones.

Implement only after observation + factor manifests exist:

- offline train/eval CLI separate from live Arena tick loop
- `DogController` backend that loads a frozen policy
- curriculum and domain-randomization configs as factor manifests
- no interactive training inside WebSocket step by default

Experiments:

- train on easy domain, evaluate on generalization suite
- compare RL vs Collect/Drive vs Kubo vs adaptive on the same held-out grids

Deliverable: RL as another instrument in the factor lab, not a separate product.

## Future Phase 15: Empirical sheep realism and information metrics

Goal: answer **RQ5 / SQ6** -- reality gap under Jadhav-calibrated dynamics.

Implement:

- parameter fitting / calibration path from public Jadhav trajectories into `sheep_model=jadhav`
- trajectory replay and model-vs-data residual reports
- information-propagation metrics (velocity correlation delays, directional influence proxies)

Experiments:

- algorithm ranking under idealized vs calibrated sheep
- model-validity map across realism ladder levels 0-4

Deliverable: evidence that conclusions survive (or reverse) under empirical sheep dynamics.

## Future Phase 16: Behavioural validation module

Goal: validate sequences of dog-sheep events, not only geometric success (Early et al.).

Implement:

- event detectors (approach, flock compress, turn, chase, escape proxies)
- behaviour sequence extraction
- transition-matrix comparison between simulation and empirical reference sequences

Deliverable: behavioural similarity scores alongside task metrics.

## Future Phase 17: Physical robot constraints

Goal: answer **SQ7** -- do rankings change under realistic dog dynamics?

Implement:

- dog dynamics factors: `v_max`, `a_max`, `omega_max`, `latency`
- kinematic integration layer after controller actions
- optional short-horizon predictive controller backend later (MPC-style), without forcing solvers into the default stack

Experiments:

- ideal point-mass dogs vs constrained dogs on the same grids
- ranking reversal under latency and turning limits

Deliverable: robot-constraint sensitivity curves; full hardware remains optional and out of core HerdSim.

## Future Phase 18: Universality and dimensionless predictors

Goal: pursue the ambitious `extension.md` claim that success may depend on system ratios more than controller identity.

Implement:

- derived dimensionless features: speed ratio, sensing/flock-size ratio, dog/sheep ratio, interaction/mean-spacing
- analysis scripts that fit herdability boundaries against these predictors across controllers
- optional connectivity / herdability-graph summaries inspired by Lama & di Bernardo (empirical, not formal certificates)

Deliverable: cross-controller scaling plots and candidate universal predictors, documented as experimental findings.

## Mapping future phases to extension.md research questions

| extension.md focus | Near-term (1-9) | Future phase |
|--------------------|-----------------|--------------|
| RQ1 Herdability | first N x M study | 11 density/cohesion, 18 scaling laws |
| RQ2 Information | observation modes | 10 communication + FAT |
| RQ3 Heterogeneity / failure | stubborn + dog failure | 12 lead/herd mixed behaviour |
| RQ4 Generalization | groundwork via factors | 12 adaptive, 13 suite, 14 RL |
| RQ5 Reality gap | Jadhav as sheep_model | 15 calibration, 16 behaviour, 17 robots |
| Scientific outputs (surfaces, curves, frontiers) | basic grids | 13-18 analysis products |

## Implementation order

Near-term:

1. Factor schema and config resolver.
2. New dynamics/observation/controller interfaces and registries.
3. Runner migration using Strombom vertical slice.
4. Migrate Kubo and Jadhav.
5. Consolidate/delete noise and heterogeneous algorithm variants.
6. Implement observation modes.
7. Add agent attributes and failure factors.
8. Replace sweep with factor-grid runner.
9. Update API/frontend to factors.
10. Rewrite docs and tests throughout each phase.
11. Run first herdability, sensing, and heterogeneity grids.

Future (after near-term success criteria):

12. Communication factor + FAT / communication-free controllers.
13. Cohesion spectrum + dynamic environments.
14. Adaptive / lead-herd controllers.
15. Generalization benchmark suite.
16. RL train-eval harness.
17. Empirical Jadhav calibration + propagation metrics.
18. Behavioural sequence validation.
19. Robot kinematic constraints (+ optional predictive control).
20. Dimensionless herdability analysis.

## Success criteria

### Near-term (Phases 1-9)

HerdSim can run this study without custom code per experiment:

```text
for sheep_model in strombom,kubo,jadhav
for dog_controller in collect_drive,kubo_forces,v_formation
for n_sheep in 20,50,100,200
for n_shepherds in 1,2,4,8
for obs_mode in global,local_positions,bearing_only,noisy_bearing
for stubborn_fraction in 0.0,0.25,0.5,0.75
run seeds 1..30
report P(success), median ticks, fragmentation, path, required_shepherds
```

### Full extension.md intention (through Phase 18)

HerdSim can systematically produce the scientific outputs named in `extension.md`:

- success surfaces and herdability boundaries
- information-performance and communication curves
- heterogeneity and failure robustness curves
- fixed vs adaptive generalization gaps
- idealized vs empirical vs robot-constrained model-validity maps
- candidate dimensionless predictors across controller families

At that point HerdSim is a complete experimental platform for the programme:

> How do agent heterogeneity, information constraints, environmental complexity, and controller architecture determine the herdability, robustness, and generalization of multi-agent shepherding systems?

Near-term delivery makes that programme possible. Future phases 10-18 are what fully fulfil it.