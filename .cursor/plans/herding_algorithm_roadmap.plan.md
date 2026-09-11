---
name: Herding Algorithm Roadmap
overview: "Progress: Must polish of the original five, shared config ownership, param_groups, and Should algorithms (v_formation, heterogeneous, obstacle_aware) are done. Remaining: Later CBF/RL (deferred), and good-to-have tool features (inspect, video, failure taxonomy, Single export, Analytics polish)."
todos:
  - id: polish-current
    content: "Must: polish paper fidelity, presets, docs, and fair-comparison caveats for the original five algorithms."
    status: completed
  - id: shared-config-ownership
    content: "Platform: shared world defaults + algorithm-only configs composed in resolve_experiment_config; info.json param_groups in UI."
    status: completed
  - id: multi-dog-baseline
    content: "Should: V-formation multi-shepherd (Fujioka/Hayashi-style) under BaseAlgorithm."
    status: completed
  - id: heterogeneous-sheep
    content: "Should: heterogeneous sheep (responsive vs stubborn) with metadata and docs."
    status: completed
  - id: obstacle-aware-heuristic
    content: "Should: obstacle/clutter-aware Collect/Drive heuristic using existing scenarios."
    status: completed
  - id: classic-teaching-baseline
    content: "Should (optional teaching): folded into v_formation (classic contrast); no second classic port."
    status: completed
  - id: defer-cbf-rl
    content: "Later: design extension hooks only when ready for CBF/optimization and RL policies (do not force into current step loop yet)."
    status: pending
  - id: tool-features
    content: "Good-to-have: agent inspect, video/GIF export, failure taxonomy, Single-run export UI, Analytics multi-algo polish."
    status: pending
isProject: false
---

# Herding Algorithm Roadmap

## Progress (as of 2026-09-08)

### Done

- Must polish for the original five (`strombom`, `strombom_noise`, `strombom_multi`, `kubo`, `flocking_dog`): research docs under `docs/research/algorithms/`, presets, fidelity notes.
- Config ownership: `core/shared_defaults.py` + `resolve_experiment_config` compose shared world -> algorithm behavior -> scenario overlay. Algorithm `config.py` files declare agent counts + algorithm-specific params only.
- UI param groups via `info.json` `param_groups` (wired in control panel).
- Should algorithms shipped and registered:
  - `v_formation` (classic multi-shepherd contrast; teaching baseline folded here)
  - `heterogeneous` (responsive vs stubborn sheep)
  - `obstacle_aware` (rule-based drive around obstacles / toward gate)
- Guide tab + topic docs tree (`docs/user/`, `docs/research/`, `docs/developer/`); `docs/papers/` kept.
- Revised Phase B research features (`gcm_goal`, history/report, sweeps, assignment viz) -- see NetLogo / Phase B plans.

### Remain

- **Later:** CBF / optimization / RL -- design note only until a concrete research need; do not force into interactive `step()`.
- **Good-to-have tool features:** agent inspect; video/GIF export; failure taxonomy; Single-run export/download UI; further Analytics scaling / multi-algorithm sweep polish; optional stronger Algorithm vs World panel split if param_groups is not enough.
- **Optional next papers (not started):** Zhang et al. 2024 outmost-push; other Long et al. 2020 ports -- only after checklist below.

## Goal

Keep HerdSim a focused herding simulation tool: reproducible algorithms, shared scenarios, shared metrics, Arena/Analytics comparison. Do not try to replace NetLogo, Mesa, or general robotics stacks.

Primary question this plan answers: if we add more herding algorithms later, does the current design fit, which papers matter, and what is good to have?

Documentation, tone, and the in-app Guide tab are planned separately in [documentation_and_guide_tab.plan.md](documentation_and_guide_tab.plan.md) (execution complete; keep docs in sync when algorithms change).

## Current Suite (baseline to protect)

| ID | Paper / basis | Status |
|----|---------------|--------|
| `strombom` | Strombom et al. 2014, J R Soc Interface | In repo; Must polish done |
| `strombom_noise` | Strombom variant (robustness preset) | In repo |
| `strombom_multi` | Strombom multi-dog extension (HerdSim) | In repo |
| `kubo` | Kubo et al. 2022 (+ MATLAB ref) | In repo |
| `flocking_dog` | Jadhav et al. 2024, Communications Biology | In repo |
| `v_formation` | Fujioka/Hayashi-style V-formation | Should done |
| `heterogeneous` | Responsive vs stubborn sheep (Strombom base) | Should done |
| `obstacle_aware` | Obstacle/gate-aware Collect/Drive | Should done |

Entry survey for newcomers: Long et al. 2020, *A Comprehensive Review of Shepherding as a Bio-Inspired Swarm-Robotics Guidance Approach* (IEEE TETCI).

## Architecture Fit (unchanged contract)

A new algorithm fits the current design if it can:

1. Live under `algorithms/<id>/` with `BaseAlgorithm` (`id`, `name`, `default_config`, `step`).
2. Update only sheep + shepherd position/velocity arrays each tick.
3. Use `state.rng`, `state.world.goal`, and world reflect/obstacle helpers.
4. Ship `info.json` (optional `param_groups`), paper/scenario/custom presets, docs under `docs/research/algorithms/`, and tests.
5. Stay meaningful under existing scenarios and algorithm-agnostic metrics.
6. Declare **only** agent counts + algorithm-specific params in `config.py` (no world/layout keys; see `core/shared_defaults.py`).

Register in [`algorithms/registry.py`](algorithms/registry.py). Config composition: [`core/shared_defaults.py`](core/shared_defaults.py) + [`core/experiment_config.py`](core/experiment_config.py).

What still strains as count grows:

- Divergent sheep physics and tick/`dt` conventions (document in exports/caveats)
- Strombom-shaped overlays/metrics on non-collect/drive methods
- Manual registry (acceptable until auto-discovery is needed)

## Must (near term) -- DONE

Paper fidelity, presets, export caveats, and NetLogo as behavioral comparison only are done for the original five. Keep updating docs when behavior changes; do not reopen as a greenfield Must phase.

## Should -- DONE (fixed order completed)

1. V-formation multi-shepherd -- done (`v_formation`)
2. Heterogeneous flock -- done (`heterogeneous`)
3. Obstacle/clutter-aware heuristic -- done (`obstacle_aware`)
4. Classic teaching baseline -- folded into `v_formation` (no separate port)

## Later (different runtime or larger design)

Do not force these into the current `step()` loop until hooks exist.

| Family | Examples | Why later | What would be needed |
|--------|----------|-----------|----------------------|
| Optimization / CBF / CLF | Multi-robot CBF herding, backstepping CBF | QP/solver per tick | Optional solver dependency, safety metrics |
| Distributed consensus herding | ADMM / dual-decomposition dog teams | Messaging inside a tick | Communication model or inner-loop API |
| Learning policies | RL / imitation nets | Training harness | Train/eval CLI separate from live sim |
| Full 3D / GIS / heterogeneous robots | Beyond sheep+dog point agents | Breaks agent schema | New agent kinds and renderer |

Rule: when a Later algorithm is requested, first decide "plugin with heavier step" vs "separate experiment backend."

## Good-to-have tool features (remain)

These make HerdSim more useful while staying unique vs NetLogo/Mesa:

- Agent inspect (selected sheep/dog state, mode, assignment)
- Video / GIF export of a run
- Failure taxonomy (timeout, split, stuck at gate, oscillation)
- Single-run session export / Run Report download UI (deferred from Revised Phase B)
- Further multi-algorithm Analytics polish beyond current compare + 1-2 param sweep
- Stronger batch/HPC path via existing `scripts/run_batch.py` + JSON provenance

## Explicit non-goals

- Becoming a general ABM language or NetLogo replacement
- Shipping every paper named in Long et al. 2020
- Adding algorithms without paper preset, docs, and tests
- Silent changes to tick/`dt` semantics without export caveats

## Suggested sequence (updated)

1. Must polish original five -- **done**
2. Shared config ownership + param_groups -- **done**
3. Should: v_formation, heterogeneous, obstacle_aware -- **done**
4. Platform good-to-haves (inspect, export UI, failure taxonomy, Analytics polish) -- **remain**
5. Later: CBF/RL design spike only if a concrete research need appears -- **remain**

## Decision checklist for any new algorithm

Before implementing, answer:

1. Which paper (DOI) and which figures/settings are the target?
2. Does it fit sheep+shepherd `step()` without a solver or trainer?
3. Which existing scenarios and metrics remain valid?
4. What adaptations will we document (goal, walls, dt)?
5. What is the paper preset and success criterion?
6. How will Arena/Analytics compare it fairly to Strombom/Kubo?
7. Config declares only algorithm-specific + agent keys (world from shared/scenario)?

If any answer is unclear, keep it out until scoped.

## References (starter set)

- Strombom et al. 2014 -- collect/drive heuristic baseline
- Long et al. 2020 -- shepherding survey (roadmap context)
- Kubo et al. 2022 -- multi-dog repulsive forces (in repo)
- Jadhav et al. 2024 -- flocking sheep + herding dog (in repo)
- Fujioka / Hayashi -- V-formation shepherding (in repo as `v_formation`)
- Zhang et al. 2024 -- outmost-push multi-robot herding (candidate, not started)
- Heterogeneous flocking/shepherding overview -- arXiv:2304.03951 (HerdSim minimal variant in repo)
- CBF multi-robot herding line -- defer (Later)
