---
name: Shepherding Budget Research
overview: "Execution tracker for collective controllability research. Single source of truth: docs/research/budget/main_shepherding_budget_plan.md (RQ1-RQ7 + Cap I1-I13 + HerdSim implementation). Do not edit research content here."
todos:
  - id: freeze-protocol
    content: Freeze Part IV protocol defaults (Section 8) in main_shepherding_budget_plan.md
    status: completed
  - id: phase1-maps
    content: "Phase 1: Caps I1-I4, I13; Package A; RQ2 claims evaluable"
    status: completed
  - id: phase2-state
    content: "Phase 2: Caps I5-I6; Package B; RQ1 claims evaluable"
    status: completed
  - id: phase3-mechanism
    content: "Phase 3: Caps I7-I8; Package C; RQ3 claims evaluable"
    status: completed
  - id: phase4-transfer
    content: "Phase 4: Cap I9; Package D; RQ4 claim evaluable"
    status: completed
  - id: phase5-substitution
    content: "Phase 5: Cap I10; Package E; RQ5 claims evaluable"
    status: completed
  - id: phase6-scaling
    content: "Phase 6: Cap I11; Package F; RQ6 claims evaluable"
    status: completed
  - id: phase7-early-warning
    content: "Phase 7: Cap I12; Package G; RQ7 claims evaluable"
    status: completed
isProject: true
---

# Shepherding Controllability -- Execution Tracker

## Single source of truth

All research content (goal, scientific value of RQs, definitions, contributions, protocol, Cap I1-I13, HerdSim implementation) lives in:

[docs/research/budget/main_shepherding_budget_plan.md](../../docs/research/budget/main_shepherding_budget_plan.md)

This plan only tracks execution status. If anything conflicts, update this tracker.

## Implementation rule

Only modify HerdSim when the change maps to a Cap ID (I1-I13), RQ, or result package in the main document. Phase done-when criteria are claim-evaluability, not "code exists."

## Current phase

Phase 0 -- protocol freeze (pending Section 8 confirmation). Minimum publishable unit: RQ1+RQ2+RQ3+S8.

## Decision log

- 2026-09-17: Canonical content consolidated into `main_shepherding_budget_plan.md`
- 2026-09-17: Scientific-value justification, operational controllability definition, Cap traceability I1-I13 added
- 2026-09-17: Removed redirect stubs; budget folder keeps the source-of-truth file
