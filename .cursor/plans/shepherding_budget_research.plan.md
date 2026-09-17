---
name: Shepherding Budget Research
overview: "Execution tracker for the shepherding-budget controllability program. Canonical research backbone: docs/research/shepherding_budget_agenda.md. Implement HerdSim changes only to answer questions in that document."
todos:
  - id: freeze-definitions
    content: "Freeze protocol in agenda Section 6.1 (task, theta, instruments, seeds, B definition)."
    status: pending
  - id: q1-frontier-protocol
    content: "Phase 1: run/implement support for budget-frontier grids (agenda Q1, requirements R1-R4)."
    status: pending
  - id: q2-regime-maps
    content: "Phase 1: extract and export regime maps (agenda Q2, R2-R3)."
    status: pending
  - id: q3-method-transfer
    content: "Phase 2: multi-instrument transfer tests under locked protocol (agenda Q3)."
    status: pending
  - id: q4-scaling-hypotheses
    content: "Phase 2: scaling-shape summary for D_min(N) and B*(N) (agenda Q4)."
    status: pending
  - id: q5-substitution
    content: "Phase 3: sensing/coordination substitution curves (agenda Q5, R7)."
    status: pending
  - id: q6-predictors
    content: "Phase 3: cross-method budget predictors (agenda Q6, R8-R9)."
    status: pending
  - id: robustness-later
    content: "Phase 4: robust budget inflation (agenda Q7, R10-R11)."
    status: pending
isProject: true
---

# Shepherding Budget Research -- Execution Tracker

## Canonical document

All scientific definitions, questions, contributions, protocol, and HerdSim requirements live in:

[docs/research/shepherding_budget_agenda.md](../../docs/research/shepherding_budget_agenda.md)

This plan only tracks execution. If the agenda and this plan disagree, update this plan.

## Implementation rule

Do not modify HerdSim "in general."

Only add simulation, experiment, metric, analysis, or UI support that maps to:

- a research question in the agenda, or
- a requirement ID in agenda Section 7, or
- a result package in agenda Section 9

## Current phase

Phase 0 -- protocol freeze (not started)

Pending user confirmations from agenda Section 11:

1. Canonical task (Drive to Goal?)
2. theta = 0.90?
3. Transfer instruments (`strombom_multi`, `kubo`, `fat`, `communication_free`?)
4. Information outside B for v1?

## Phase checklist

### Phase 0

- [ ] Confirm agenda Section 6.1
- [ ] Mark agenda protocol frozen
- [ ] Mark `freeze-definitions` completed

### Phase 1 (Q1-Q2)

- [ ] Ensure R1-R6 support as needed
- [ ] Produce Package P1 (frontier dossier)

### Phase 2 (Q3-Q4)

- [ ] Multi-method locked campaigns
- [ ] Produce Package P2 (transfer dossier)

### Phase 3 (Q5-Q6)

- [ ] Ensure R7-R9 as needed
- [ ] Produce Package P3 (mechanism dossier)

### Phase 4 (Q7)

- [ ] Ensure R10-R11 as needed
- [ ] Produce Package P4 (robustness dossier)

## Decision log

- 2026-09-16: Canonical backbone created at `docs/research/shepherding_budget_agenda.md`
- 2026-09-16: This file demoted to execution tracker
