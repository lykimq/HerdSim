# Validation, NetLogo, and claim boundaries

## Keep the layers separate

**NetLogo platform.** NetLogo is a general agent-based modelling environment. Its presence does not validate a particular model or HerdSim result.

**Bundled twins.** `integrations/netlogo/twins.json` registers selected desktop `.nlogo` counterparts. The HerdSim UI can list and open them. They are intended for behavior-oriented inspection under similar settings.

**2025 draft.** The draft used NetLogo, but its collect, hold, and gate-exit model is not a bundled twin. It was not rerun.

**HerdSim claim stack.** Current scaling claims come from Python `scaling_v2` protocols, frozen grids, staged seeds, claim merges, bootstrap analysis, provenance, and exported CSVs. They do not derive from the NetLogo twins.

![NetLogo and HerdSim serve different roles.](../../results/summary/figures/schematics/en/netlogo_vs_herdsim.svg)

## Twin registry and claim use

The registry currently contains five counterparts:

| HerdSim method | Registry model | Claim-grade in current scaling report | Boundary |
|---|---|---|---|
| `strombom` | `strombom.nlogo` | No direct scaling claim package | Counterpart exists; no parity score |
| `strombom_noise` | `strombom_noise.nlogo` | No | Counterpart exists; no parity score |
| `strombom_multi` | `strombom_multi.nlogo` | Yes, HerdSim Phases 1 and 2 | Claim evidence is Python output, not twin output |
| `kubo` | `kubo.nlogo` | Yes, HerdSim Phase 4 | Claim evidence is Python output; time conventions differ across method families |
| `flocking_dog` | `flocking_dog.nlogo` | No current scaling claim package | Counterpart exists; no parity score |
| `fat` | none | Yes, HerdSim Phase 4 | HerdSim only in this comparison |

The 2025 draft model is absent from the registry.

## What the twins support

The NetLogo guide describes counterparts with similar herding behavior for Drive to Goal, settings that can be matched manually, live metrics, and visual inspection. This supports qualitative checks such as whether a method gathers, drives, spreads dogs, stalls, or fragments in a broadly similar way.

Exact paths and finish ticks are not expected to match because Python and NetLogo use different random number generators and may update agents in a different order. Kubo is particularly sensitive to discrete integration differences. A shared numeric seed does not create a shared random stream.

The twins therefore support a behavioral cross-check. They do not, by their existence alone, support numerical equivalence.

## What the tests establish

| Test area | What it verifies | What it does not verify |
|---|---|---|
| Twin API | The five registry methods and expected model filenames are returned | Model behavior or cross-engine parity |
| Model library API | Bundled models can be listed; uploads are constrained | Scientific validity |
| Desktop open API | The configured NetLogo launcher receives a model path | A successful scientific run |
| Path helpers | Repository model paths resolve; local NetLogo may be detected | Matching trajectories |
| HerdSim determinism | Repeated HerdSim runs with one configuration and seed can match | Matching NetLogo randomness |
| Controller and metric tests | Selected formulas, configurations, and invariants behave as coded | Agreement with an external implementation over a study grid |
| Scaling stack tests | Protocol fields and analysis functions follow expected rules | The truth of external draft results |

Relevant files:

- [Twin registry](../../../integrations/netlogo/twins.json)
- [NetLogo API tests](../../../tests/backend/api/test_netlogo_api.py)
- [NetLogo bridge tests](../../../tests/backend/test_netlogo.py)
- [HerdSim correctness tests](../../../tests/backend/correctness/)
- [HerdSim good-path tests](../../../tests/backend/goodpath/)

## HerdSim claim evidence

The strongest current evidence is internal reproducibility under a frozen protocol:

1. `scaling_v2` fixes the task, world, N and D grids, layouts, theta, deadlines, methods, and master seed.
2. Scout runs map the grid with 30 seeds per cell and are used for planning.
3. Claim runs reseed selected frontier windows, normally with 100 seeds.
4. Claim analysis uses claim rows where present and scout rows elsewhere.
5. D_min uncertainty is estimated with 1,000 seed bootstraps.
6. CSV outputs, status files, protocol snapshots, and provenance records remain inspectable.

This is claim-grade for the simulated HerdSim task and tested range. It is not field validation, external replication, or cross-engine validation.

![The staged claim pipeline.](../../results/summary/figures/schematics/en/pipeline.svg)

![One reliability cell contains independent seeds.](../../results/summary/figures/schematics/en/one_cell_seeds.svg)

## Claim and non-claim table

| Supported statement | Unsupported stronger statement |
|---|---|
| HerdSim reuses paper-informed controller ideas | HerdSim reproduces every cited paper protocol |
| Some methods have bundled NetLogo counterparts | Every HerdSim method has a NetLogo twin |
| Twins permit visual and metric-oriented cross-checks | Twins are quantitatively equivalent to HerdSim |
| Frozen HerdSim runs support the current scaling results | NetLogo independently reproduced those results |
| Current results cover one simulated task, tested grids, and theta = 0.90 | Results establish a universal farm or biological scaling law |
| D_max = 35 is a grid ceiling where no collapse was seen | 35 is a measured physical upper limit |
| FAT fails to reach theta in specified HerdSim cells | FAT cannot herd larger flocks in general |
| Draft outcomes differ from HerdSim outcomes | The draft was disproved |

![Claim and non-claim layers.](../../results/summary/figures/schematics/en/trust_herdsim.svg)

## Missing parity evidence

No repository artifact currently provides all of the following:

- A frozen, matched Python and NetLogo protocol for each twin
- A documented mapping for every parameter, initialization rule, update order, and boundary rule
- Cross-engine runs over the same condition grid
- A seed strategy that accounts for different random number generators
- Prespecified parity metrics and tolerances
- Distributional comparisons with uncertainty across many runs
- Versioned parity result tables and provenance
- A pass or fail decision for each twin

Without these items, no quantitative parity score should be reported. A useful future parity study would compare distributions rather than tick-for-tick traces, using outcomes such as success probability, completion-time distribution under compatible time units, final goal distance, cohesion, fragmentation, and controller-specific qualitative invariants.

## Comparison guidance

Live Compare is exploratory evidence for a matched HerdSim pair. Experiments provides multi-seed HerdSim evidence and exports. NetLogo runs in a separate desktop application. These three workflows should not be pooled without a predeclared protocol.

For cross-method HerdSim comparisons, lock scenario, sheep count, dog count, success rule, time budget, and seed list. Paper presets answer a different question because methods may declare different default counts. Shepherd path and tick count also require care across Kubo and Strombom-style families because their integration conventions differ.

## Citations

- D. Strombom et al. "Solving the shepherding problem: heuristics for herding autonomous, interacting agents." *Journal of the Royal Society Interface* 11(100):20140719, 2014. DOI: `10.1098/rsif.2014.0719`.
- M. Kubo et al. "Herd guidance by multiple sheepdog agents with repulsive force." *Artificial Life and Robotics* 27:416-427, 2022. DOI: `10.1007/s10015-021-00726-7`.
- V. Jadhav et al. "Collective responses of flocking sheep (Ovis aries) to a herding dog (border collie)." *Communications Biology*, 2024. DOI: `10.1038/s42003-024-07245-8`.
- Z. Li et al. "Communication-free shepherding navigation with multiple steering agents." *Frontiers in Control Engineering* 4, 2023. DOI: `10.3389/fcteg.2023.989232`.
- 2025 draft: [repository PDF](../../../docs/papers/sheep-scaling_paper2025.pdf). Draft status and placeholder author lines must be retained when citing it.

Additional context: [related work](../notes/related_work.md), [NetLogo guide](../../../platform/docs/guide/netlogo.md), [Compare guide](../../../platform/docs/guide/compare.md), [Experiments guide](../../../platform/docs/guide/experiments.md), and [draft comparison](draft_comparison.md).
