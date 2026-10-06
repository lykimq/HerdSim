# Collective Herdability Under Shepherding: Main Scaling Plan

Protocol: `scaling_v2`.

This document is the scientific plan. It defines the research objective, phase dependencies, research questions, claim criteria, evidence grades, budgets, decision gates, and study boundaries. It does not duplicate setup rationale, controller explanations, implementation ownership, glossary entries, or run commands.

Canonical supporting documents:

- [Research program](herdsim_research_program.md)
- [Setup and reference index](setup/README.md)
- [Experiment setup](setup/experiment_setup.md)
- [Parameter reference](setup/parameter_reference.md)
- [Glossary](setup/glossary.md)
- [Method guides](methods/README.md)
- [Credibility and comparison](credibility/README.md)
- [Run strategy](experiment_run_strategy.md)
- [Run guide](setup/run_guide.md)
- [Progress tracker](progress_tracker.md)
- [Data appendices](../results/summary/data/README.md)

## 1. Research objective

The program asks how much external control is needed to guide a collective reliably as flock size and initial structure change, which processes explain that demand, and which patterns transfer across shepherding methods.

The primary control-demand quantity is the viable shepherd range around `D_min` and any observed overcrowding boundary under a fixed task, reliability threshold, time budget, layout, method, and information condition. `D_min` is not an intrinsic property of a flock.

The smallest publishable unit is RQ1, RQ2, RQ3, and the frozen protocol. RQ4 repeats both the size map and structure contrast for the required transfer methods. RQ5 and RQ7 are follow-on studies. RQ6 uses completed frontier maps and must not determine the grid retrospectively.

## 2. Work map and dependencies

| Phase | Research role | RQ | Package | Depends on | Planning completion condition |
|---|---|---|---|---|---|
| 0 | Freeze shared protocol | S8 | all | none | Canonical YAML and scientific plan agree |
| 1 | Baseline size and regime map | RQ2 | A | Phase 0 | Merged baseline frontiers, regimes, and conditional T1 decision |
| 2 | Structure at fixed N | RQ1 | B | Phase 1 scout and claim-window rules | Merged layout frontiers and predictor comparison |
| 3 | Mechanism contrasts | RQ3 | C | Matching efficient and overcrowding cells from Phases 1 or 2 | Prespecified within-N tests, or an explicit undefined status |
| 4 | Transfer across methods | RQ4 | D | Phases 1 and 2 design fixed | Size and structure maps for all required methods |
| 5 | Information substitution | RQ5 | E | Stable method baseline and staged-run pipeline | Observation, range, and communication ladder frontiers |
| 6 | Scaling fits | RQ6 | F | Claim-grade frontier maps | Leave-one-N-out comparison of candidate curves |
| 7 | Early warning | RQ7 | G | Claim trajectories with required timeseries | Held-out AUROC and lead-time evaluation |

Dependency rules:

1. Phase 0 precedes every scientific run.
2. Phases 1, 2, and 4 use scout maps before claim reseeding.
3. Phase 3 is analysis of collected contrast cells. It is undefined if the required regimes do not exist.
4. Phase 4 structure claims wait for structure maps from every required method.
5. Phase 5 is three separate ladders, not a Cartesian product.
6. Phase 6 is fitted only after frontiers exist.
7. Phase 7 requires stored claim-grade timeseries and whole-N holdout.

## 3. Shared planning contract

The machine-readable values are in [`canonical_grid.yaml`](../configs/canonical_grid.yaml). Parameter meanings and rationale are in [parameter reference](setup/parameter_reference.md) and [experiment setup](setup/experiment_setup.md).

The plan locks these constraints:

- Task: `drive_to_goal`, with success only when every sheep reaches the goal by the deadline.
- Primary reliability threshold: `theta = 0.90`; also report 0.50 and 0.70.
- Baseline method: `strombom_multi`.
- Required transfer set: `strombom_multi`, `kubo`, and `fat`.
- Recommended, non-minimum transfer method: `communication_free`.
- Flock-size grid: `{5, 10, 25, 50, 75, 100, 150, 200, 300, 400}`.
- Shepherd-count grid: `{1, 2, 3, 4, 6, 10, 15, 20, 25, 35}`.
- Layouts: `compact`, `wide`, `split`, and `outlier_rich`.
- Structure sizes: `{50, 100, 200}`.
- Information sizes: `{100, 200}`.
- Deadlines: `T0 = 10000`; conditional `T1 = 20000`.
- Locked seed list from master seed 2026.
- Scout depth: 30 seeds per selected cell.
- Claim depth: normally 100 seeds per selected cell.
- Bootstrap: 1000 seed resamples.

Effects in dog count are measured in local grid steps. The study cannot resolve a difference smaller than one local step of the tested D grid.

### Frontier and regime rules

Let `R(m, tau, N, D, T, X0, I)` be success probability over locked seeds.

| Quantity | Planning definition |
|---|---|
| `D_min` | Smallest tested D with `R >= theta` |
| `D_overcrowd` | Smallest D after `D_min` for which that D and the next tested D are both below theta |
| `D_max` | Largest reliable D below `D_overcrowd`; without overcrowding, the largest tested reliable D, which may only be a grid ceiling |
| `B*` | Reliable `(D, T)` with minimum median shepherd path; ties use smaller D, then faster median success time |
| Hard failure | No tested D reaches theta |
| Under-resourced failure | `R < theta` below `D_overcrowd` |
| Efficient operation | `R >= theta` and median path is below the wasteful threshold |
| Wasteful overspend | `R >= theta` and median path is at least 20 percent above `B*`; also report 10 and 30 percent |
| Overcrowding collapse | `R < theta` at or above `D_overcrowd` |

A `D_max` at 35 with no `D_overcrowd` is a tested-grid ceiling, not a measured collapse point.

## 4. Evidence grades and planned budgets

| Grade | Purpose | Planned depth | Permitted claim use |
|---|---|---:|---|
| SMOKE or Pilot | Check paths, metrics, host, and resume behavior | Small diagnostic grid, normally 5 seeds | None |
| SCOUT | Map the broad grid and select precision windows | 30 seeds | Planning and diagnostics only |
| CLAIM | Estimate selected frontiers and claim quantities | Normally 100 seeds | Yes, after provenance and run documentation checks |
| T1 | Test the longer deadline on detected overcrowding cells | 100 seeds | Yes, only when the trigger exists |

For each method, layout, and N, claim planning selects:

1. Scout `D_min`, plus the previous and next tested D.
2. When two consecutive D values establish a candidate overcrowding onset, those two values and the last reliable D.
3. If no D reaches theta, the two largest tested D values.

Claim rows replace scout rows for reseeded cells. They are never stacked with scout rows from the same cell. Unselected cells retain scout depth. Bootstrap resamples seeds within D; undefined `D_min` draws remain right-censored above the tested grid. If a `D_min` interval spans more than one D-grid step, raise that window to 200 seeds before using it for a structure claim.

### Planned estimates

These figures are budget estimates, not executed counts:

| Campaign | Scout estimate | Claim estimate | Planning note |
|---|---:|---:|---|
| One size map | About 3000 | Up to about 6000 | Claim estimate assumes up to six D values per N |
| One structure contrast | About 3600 | Up to about 7200 | Three N values, four layouts, full scout D grid |
| Baseline core | About 20000 total | Included | Size, conditional T1, and structure, rounded for planning |
| Each required transfer method | Repeat size and structure budgets | Recompute after scout | Claim windows depend on that method's scout |

Actual work must be read from status and provenance artifacts, not inferred from these estimates.

## 5. Research questions and planned tests

### RQ1: Structure

Does `D_min` change across initial layouts at fixed N?

Use N in `{50, 100, 200}`, all four layouts, and the full D grid. Compare `D_min` in grid steps. Compare an `(N, D)` model against a model that also uses layout and state measured only in the first 100 ticks. Hold out whole N values. Full-trial summaries are not predictors.

### RQ2: Size and operating regimes

How do the reliable shepherd frontier and operating regimes change with N?

Map `R(N, D)` at T0 for the baseline method and compact layout. Estimate frontiers and regime labels under the shared rules. Run T1 only for cells selected by an observed scout or claim overcrowding trigger.

### RQ3: Mechanism

Which prespecified mechanism signatures distinguish efficient and overcrowding cells at the same N?

Use one median per `(N, D)` cell, rank tests, and Holm correction across hypotheses.

| Hypothesis | Required signature |
|---|---|
| Interference | Higher median `I_dir` in overcrowding cells |
| Induced fragmentation | Lower largest-component fraction in overcrowding cells |
| Coverage saturation | Among reliable cells, median coverage remains above 0.5, its range across D is below 0.1, and median path rises; a near-zero curve is not saturation |
| Redundant effort | Higher median path without a reliability gain |

No new grid is introduced for RQ3. If a method has no overcrowding label, the mechanism contrast is undefined for that method.

### RQ4: Generality across methods

Which frontier, regime, and structure patterns transfer across the three required methods?

Repeat the size map and structure contrast for `kubo` and `fat`, then compare them with `strombom_multi`.

| Property | Shared | Shifted | Absent |
|---|---|---|---|
| `D_min` | Same tested D | Different tested D | One side has no `D_min` |
| Overcrowding | Present on both and D/N is within a factor of 1.5 | Present on both with a wider gap | Not present on both |
| `I_dir` | `r(I_dir, success) < -0.3` on both | Sign pattern agrees but magnitude differs | Required significant pattern is missing |
| Coverage saturation | Saturation rule holds on both | Holds on one | Holds on neither |

The state-dependent transfer row is filled only when every compared method has the required structure runs.

### RQ5: Information versus shepherd count

Can richer observation, sensing range, or communication lower `D_min` at fixed reliability?

Use N in `{100, 200}`. Test the observation ladder `bearing_only`, `local_positions`, `global`; range multipliers `0.5, 1, 1.5, 2` times method `r_s`; and communication ladder `none`, `neighbour_broadcast`, `global_shared`. For `strombom_multi`, shared information is the union of sensed sheep, not privileged simulator truth.

### RQ6: Scaling fits

Which planned curve best predicts held-out N, and is a single power law adequate?

Compare constant, linear, power `A * N^alpha`, and two-piece linear candidates in dog-count units. Select by leave-one-N-out RMSE. Report any log slope only within an explicit N and layout band.

### RQ7: Early warning

Can recent state predict a later failure better than N and D alone?

At ticks 1000 through 8000 in steps of 200, use features only from `(t - 200, t]`. Label failure within the next 500 ticks only where the horizon remains inside T0. Train on other N values. Lead time is measured from first crossing of the training threshold to failure and may exceed 500 ticks.

## 6. Claim support criteria

Verdicts are `UNEVALUATED`, `SUPPORTED`, `REJECTED`, or `INCONCLUSIVE`. A conditional analysis that cannot run because its trigger is absent is marked `SKIPPED` in run status and explained in the tracker. Verdicts may be assigned only from claim-grade evidence.

| Claim | RQ | Supported when |
|---|---|---|
| C1a | RQ1 | For at least one N, `D_min` differs by at least one D-grid step across layouts at theta 0.90 |
| C1b | RQ1 | The state model has lower leave-one-N-out negative log-likelihood than the `(N, D)` model |
| C2a | RQ2 | The baseline method has `D_overcrowd` at theta 0.90 for at least one N |
| C2b | RQ2 | At least one D above `D_overcrowd` remains below theta at T = 20000 |
| C3 | RQ3 | At fixed N, overcrowding and efficient cells differ in `I_dir` and/or fragmentation with rank `p < 0.05` after Holm correction |
| C4 | RQ4 | `D_min` or overcrowding is shared across the three required methods; the structure row additionally requires all structure runs |
| C5a | RQ5 | One ladder step lowers `D_min` by at least one D-grid step at N in `{100, 200}` |
| C5b | RQ5 | The second ladder step saves fewer dogs than the first |
| C6a | RQ6 | Power has higher leave-one-N-out RMSE than piecewise or per-layout curves |
| C6b | RQ6 | The slope of log `D_min` on log N is below 1 in a stated N and layout band |
| C7a | RQ7 | Held-out state AUROC exceeds the held-out `(N, D)` baseline |
| C7b | RQ7 | At least 30 percent of failure trials have lead time of at least 500 ticks |

These criteria support statements inside the tested protocol only. They do not support a universal law, an untested task, field performance, or a dog-count gap below one grid step.

## 7. Execution status, not scientific results

This section records whether planned work ran. It does not state effect sizes, frontier values, or scientific interpretations. The [progress tracker](progress_tracker.md) owns current run and verdict status. The [run ledger](../results/summary/data/run_ledger.md) owns executed counts and provenance.

Status as recorded on 2026-10-06:

| Phase | Run status | Executed-count note |
|---|---|---|
| 0 | DONE | Protocol frozen |
| 1 | DONE; conditional T1 SKIPPED | Scout 3000 rows; claim reseed 2200 rows; T1 not run because its trigger selected zero cells |
| 2 | DONE | Scout 3600 rows; claim reseed 2400 rows |
| 3 | SKIPPED | Conditional mechanism analysis had no eligible overcrowding contrast |
| 4 | DONE for required Kubo and FAT size and structure campaigns | Exact scout, claim, and merge counts are in the run ledger |
| 5 | TODO | No completed information-ladder campaign is claimed |
| 6 | DONE for the planned baseline fit package | Analysis status only |
| 7 | TODO | Early-warning analysis has not run |

The words `DONE`, `SKIPPED`, and `TODO` describe execution status only. A completed phase can yield a rejected or inconclusive claim. A skipped conditional phase means its prespecified trigger was absent, not that a scientific outcome was observed at the unrun condition.

## 8. Future decision gates

| Gate | Evidence checked | Decision |
|---|---|---|
| G1 Protocol consistency | Canonical YAML, resolved protocol, and plan | Stop if frozen values disagree; version any deliberate protocol change |
| G2 Scout quality | Completion, reliability map, and provenance | Stop and repair a broken map before claim planning |
| G3 Claim-window precision | Bootstrap interval for `D_min` | Raise selected windows to 200 seeds when the interval spans more than one D-grid step |
| G4 T1 trigger | Two consecutive post-frontier D values below theta | Run T1 only on selected overcrowding cells; otherwise record `SKIPPED` |
| G5 Mechanism eligibility | Efficient and overcrowding cells at the same N | Run RQ3 only where the matched contrast exists |
| G6 Transfer completeness | Size and structure maps for all required methods | Do not fill the full structure-transfer claim before all maps exist |
| G7 Structure extension | Three-size structure claim map | Add N = 300 and 400 mainly if all four layouts remain at the `D_min` floor; otherwise the extension is optional |
| G8 Information campaign | Stable baseline and separate ladder protocol | Run observation, range, and communication as separate staged campaigns |
| G9 Early warning | Claim-grade timeseries and both outcome classes | Do not report AUROC or lead time without held-out eligible data |
| G10 Intended velocity E1 | Claim-grade evidence of wall-driven `I_dir` spikes | Keep E1 unbuilt unless that diagnostic need is demonstrated |
| G11 External parity | Matched cross-engine protocol and prespecified tolerances | Make no numerical NetLogo parity claim until the credibility requirements are met |

## 9. Scope and threats

| Threat or boundary | Planning response |
|---|---|
| One simulated task | Limit conclusions to `drive_to_goal`; a second task is later work |
| Method dependence | Require RQ4 before making method-general statements |
| Layout and state confounding | Use matched N and prespecified layout contrasts |
| Discrete D grid | Express effects in local grid steps and preserve censoring above the grid |
| Soft reliability frontier | Use locked seeds, claim windows, bootstrap intervals, and the 200-seed precision gate |
| Conditional analyses | Mark absent-trigger work as undefined or skipped, never as a measured null at an unrun condition |
| Time conventions across methods | Avoid direct physical interpretation of raw tick counts across controller families |
| Strombom collect switch wider than the goal | Do not interpret its failure as a packing failure |
| Simulated controllers | Make no field, farm, or biological-validity claim |
| NetLogo twins and 2025 draft | Treat them as separate evidence layers; follow the credibility documents |
| Grid ceiling | Do not interpret D = 35 as a physical upper limit |
| Selective precision | Preserve cell grade after merges and never stack scout and claim rows |

The application default arena, sheep models, and dog force laws are outside this protocol's modification scope. Detailed boundaries and validation limits are in [credibility and comparison](credibility/README.md).

## 10. Source precedence and document ownership

When sources differ, use this order:

1. [`canonical_grid.yaml`](../configs/canonical_grid.yaml) defines frozen machine-readable `scaling_v2` defaults.
2. A resolved YAML in [`configs/protocols/`](../configs/protocols/) defines a campaign subset.
3. A run's copied `protocol.yaml`, `provenance.json`, `manifest.jsonl`, and `status.json` define what actually executed.
4. This plan defines research questions, dependencies, claim criteria, evidence grades, budgets, gates, and scope.
5. [Setup documents](setup/README.md) define parameter rationale, glossary, implementation caps, and operational reference.
6. [Method guides](methods/README.md) define controller interpretation and method-specific limits.
7. [Credibility documents](credibility/README.md) define comparison and validation boundaries.
8. [Run strategy](experiment_run_strategy.md) and [run guide](setup/run_guide.md) define staging intent and commands.
9. [Progress tracker](progress_tracker.md) defines current code, run, and claim status.
10. [Data appendices](../results/summary/data/README.md) and their direct artifacts define executed counts and reported evidence.

Results never redefine the frozen plan. If a planning estimate differs from a run artifact, retain the estimate as a plan and report the artifact as executed. If a copied run protocol differs from generic prose, the copied protocol and provenance control interpretation of that run.
