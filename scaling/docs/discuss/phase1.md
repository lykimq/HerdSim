# Phase 1 discussion note (high level)

Audience: email / meeting. Detail lives in the plan, tracker, and run `REPORT.md` files.
Protocol: `scaling_v2`. Date context: runs completed 2026-09-22 on host `gwen`.

Meeting backlog: [notice-meeting.md](../notice-meeting.md).
Full how: [main_scaling_plan.md](../main_scaling_plan.md).
Run staging: [experiment_run_strategy.md](../experiment_run_strategy.md).
Status: [progress_tracker.md](../progress_tracker.md).

---

## 1. Question (what Phase 1 asks)

**RQ2 / Package A (size map).** For the baseline method on a fixed compact start: how does reliability R(N, D) change with flock size N and dog count D? Where is D_min? Do we see overcrowding?

This is the HerdSim analogue of the draft paper’s “how many dogs for N sheep?” question, on our open-interior drive-to-goal task (not collect–hold–gate).

Claims this phase can speak to: mainly **C2a / C2b** (overcrowding), size-map evidence for regimes, and diagnostic **C6** fits. **C1a** (structure across layouts) needs Phase 2.

---

## 2. Design (what we froze)

| Choice | Setting |
|--------|---------|
| Task | Drive flock into goal disk; success = all sheep in goal |
| Arena | 500×500; flock center; goal offset; radius `15 * sqrt(N/50)` |
| Method | `strombom_multi` only |
| Layout X0 | `compact` only |
| N grid | 5 … 400 (10 values) |
| D grid | 1 … 35 (10 values) |
| Theta | 0.90 |
| T0 / T1 | 10,000 / 20,000 (T1 only on overcrowding cells) |
| Seeds | Scout 30; claim window 100 |
| Staging | Pilot → scout → claim-plan → claim-reseed → analyse → T1 if needed |

Not in Phase 1: other layouts, other methods, gate task, NetLogo twin (meeting items 2–4).

---

## 3. Plan vs what we ran

| Step | Intent | Status |
|------|--------|--------|
| Sanity tests | Pipeline correctness | DONE |
| Pilot (SMOKE) | Tiny grid, prove paths/Package A | DONE |
| Scout (SCOUT) | Full N×D at 30 seeds (~3,000 trials) | DONE (~73 min) |
| Claim plan | Choose D_min ± neighbors (and overcrowding if any) | DONE (22 cells; no overcrowding window) |
| Claim reseed | 100 seeds on those cells; merge | DONE (2,200 claim trials; merge 4,467 rows) |
| Analyse A + F | Frontiers, regimes, scaling fits | DONE (auto with reseed) |
| T1 | Long budget on overcrowding D | SKIPPED (0 cells to run) |

Artifacts: `scaling/results/phase1/{pilot,scout,claim,t1}/` with `REPORT.md` where written.

---

## 4. Implementation (code ready for this phase)

Before/during runs: campaign CLI, scout/claim/T1 protocols, Package A/F, bootstrap, merge rule, WORKERS=16 defaults, typecheck in CI.

After Phase 1 runs (not required to re-run Phase 1): shape metrics for **future** campaigns: perimeter, hull_area, flock_density, aspect_ratio (meeting item 1). Phase 1 claims do not depend on them.

---

## 5. Results (claim-grade picture)

- Overall success on merge ≈ **0.98**.
- **D_min = 2** for N ∈ {5, 10}; **D_min = 1** for all N ≥ 25 through 400.
- Bootstrap CI on D_min is **one grid step** everywhere (no 200-seed raise needed before structure).
- Regimes: mostly **wasteful** at high D; a few **under-resourced** at small N with D=1; **no overcrowding**.
- T1 empty by design: no D_overcrowd → nothing to reseed at 20,000 ticks.
- Package F (auto): prefers **piecewise** over a single power law (diagnostic only until Claims wording is locked).

**Working reading.** On compact + Strombom + this goal task, one dog is enough once the flock is not tiny. Extra dogs add path cost more than they cause collapse. The interesting story is not “D_min grows with N” on this baseline.

---

## 6. Report / Claims (discussion stance)

Per-run narratives: `scaling/results/phase1/*/REPORT.md`.

Suggested Phase 1 Claims posture (tracker table still UNEVALUATED until you promote):

| Claim | Suggested verdict on this map | Why |
|-------|-------------------------------|-----|
| C2a | Rejected / not supported | No overcrowding onset |
| C2b | Not applicable | No T1 cells |
| C6 | Open | Fits lean piecewise; need criteria pass |
| C1a | Out of scope here | Needs Phase 2 layouts |

---

## 7. Draft paper: what we can and cannot say

Same family of question (dogs vs N, SR ≥ 90%, similar D grid, 10k-tick scale). **Not the same experiment:** NetLogo vs HerdSim, different controller/sheep, different task (hold+gate vs open goal).

Draft reported **rising D_min with N** and some **overcrowding**. Our Phase 1 baseline shows **flat D_min ≈ 1** and **no overcrowding**.

Fair message for discussion: Phase 1 is a real result for this system, and a useful **contrast** with the draft, not a replication of their D_min table. Whether hard scaling is method/task-specific is exactly what Phase 2 (structure) and Phase 4 (other methods) test next.

Do **not** re-run Phase 1 only for the new shape metrics.

---

## 8. Before Phase 2 (checklist for the meeting)

1. Agree Phase 1 Claims wording (especially C2a).
2. Keep Phase 1 results as the size baseline; no re-run required for science.
3. Phase 2 scout: N ∈ {50,100,200} × 4 layouts × full D × 30 seeds (~3,600 trials; ~1 h order of magnitude). New shape metrics will be logged automatically.
4. Meeting backlog still open: gate task / method mix (item 2), draft-in-HerdSim twin (item 3), NetLogo extension twin (item 4). Those are parallel tracks, not Phase 2 blockers.

---

## 9. Pointers (if someone wants one click deeper)

| Layer | Where |
|-------|--------|
| Why / RQs | [herdsim_research_program.md](../herdsim_research_program.md) |
| Draft reference | [sheep-scaling_paper2025.md](../sheep-scaling_paper2025.md) |
| Claim report | `scaling/results/phase1/claim/REPORT.md` |
| Figures | `scaling/results/phase1/claim/packages/a/figures/` |
| Next make target | `make -C scaling scaling-phase2-scout WORKERS=16` |
