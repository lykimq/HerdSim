---
name: Shepherding Budget Research
overview: "Execution tracker for collective herdability research. Scientific source of truth: docs/research/budget/main_shepherding_budget_plan.md. Live status: docs/research/budget/progress_tracker.md. Do not edit research content here."
todos:
  - id: freeze-protocol
    content: "Phase 0: freeze Section 8 protocol (DONE 2026-09-17)"
    status: completed
  - id: phase1-maps
    content: "Phase 1: Package A / RQ2 — herdability maps (IN PROGRESS; compact still easy)"
    status: in_progress
  - id: phase2-state
    content: "Phase 2: Package B / RQ1 — collective-state manipulation"
    status: pending
  - id: phase3-mechanism
    content: "Phase 3: Package C / RQ3 — overcrowding mechanism"
    status: pending
  - id: phase4-transfer
    content: "Phase 4: Package D / RQ4 — cross-method transfer"
    status: pending
  - id: phase5-substitution
    content: "Phase 5: Package E / RQ5 — information substitution"
    status: pending
  - id: phase6-scaling
    content: "Phase 6: Package F / RQ6 — scaling fits (SMOKE only so far)"
    status: pending
  - id: phase7-early-warning
    content: "Phase 7: Package G / RQ7 — early warning"
    status: pending
isProject: true
---

# Shepherding Controllability -- Cursor execution pointer

## Sources of truth

- Science, claims, Caps, protocol: [docs/research/budget/main_shepherding_budget_plan.md](../../docs/research/budget/main_shepherding_budget_plan.md)
- Plain-language framing: [docs/research/budget/herdsim_research_program.md](../../docs/research/budget/herdsim_research_program.md)
- Live status / next actions: [docs/research/budget/progress_tracker.md](../../docs/research/budget/progress_tracker.md)

If anything conflicts, update the docs above -- not research content in this Cursor plan.

## Implementation rule

Only modify HerdSim when the change maps to a Cap ID (I1--I14), RQ, or result package in the main plan. Phase done-when = claim-evaluability, not "code exists."

## Current phase

See progress tracker Section 1. As of 2026-09-18: Phase 1 in progress; Caps built; claims unevaluated; recommended next is harder X0 (Phase 2) if compact remains too easy.

## Decision log (Cursor-local)

- 2026-09-17: Canonical content consolidated into `main_shepherding_budget_plan.md`
- 2026-09-18: Docs rewritten for clearer framing; this plan re-synced to real phase status (not all completed)
- 2026-09-18: Results layout cleanup (`phase{k}/{slug}/`, campaign YAMLs, `packages/{a-g}/`)
