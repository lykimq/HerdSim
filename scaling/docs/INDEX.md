# Scaling documentation index

This is the main reading map for `scaling_v2`. Each document has one primary responsibility. English and Vietnamese versions are paired where the document is intended for readers.

## Start here

| Need | Canonical document |
|---|---|
| Understand what is planned | [Main scaling plan](main_scaling_plan.md) |
| Understand the controllers | [Methods index](methods/README.md) |
| Understand parameters and simulation setup | [Setup and reference](setup/README.md) |
| Run, resume, or analyse a campaign | [Run guide](setup/run_guide.md) |
| Read completed findings | [Results report](../results/summary/SUMMARY_REPORT.md) |
| Inspect readable evidence tables | [Data appendices](../results/summary/data/README.md) |
| Compare with the 2025 draft and NetLogo | [Credibility and comparison](credibility/README.md) |
| Check current implementation and claim status | [Progress tracker](progress_tracker.md) |

Vietnamese index: [INDEX_vi.md](INDEX_vi.md).

## Document ownership

| Area | Owns | Does not own |
|---|---|---|
| Plan | Research questions, dependencies, claim criteria, budgets, decision gates | Executed numerical findings |
| Methods | Published basis, HerdSim implementation, method-specific setup and limits | Cross-phase verdicts |
| Setup | Parameters, rationale, definitions, staging, commands, outputs, provenance | Scientific interpretation |
| Results | Completed Phase 1, 2, and 4 observations, uncertainty, limits | Protocol rationale or method tutorials |
| Credibility | Draft comparison, NetLogo scope, validation evidence, non-claims | New parity claims |
| Data appendices | Generated tables, run ledger, schemas, direct evidence links | Hand-entered interpretation |
| Tracker | Current implementation, run, and verdict status | Stable explanatory narrative |

## Reader paths

### First reading

1. [Main scaling plan](main_scaling_plan.md)
2. [Experiment setup](setup/experiment_setup.md)
3. [Methods index](methods/README.md)
4. [Results report](../results/summary/SUMMARY_REPORT.md)
5. [Credibility and comparison](credibility/README.md)

### Reproduce or audit a result

1. [Run guide](setup/run_guide.md)
2. [Run ledger](../results/summary/data/run_ledger.md)
3. [Phase data tables](../results/summary/data/README.md)
4. The linked `protocol.yaml`, `provenance.json`, `manifest.jsonl`, `status.json`, and CSV artifacts

### Look up a term or value

- [Glossary](setup/glossary.md)
- [Parameter reference](setup/parameter_reference.md)
- [Experiment setup and rationale](setup/experiment_setup.md)

## Methods

- [Strombom Collect/Drive](methods/strombom.md)
- [Kubo force model](methods/kubo.md)
- [FAT](methods/fat.md)

## Results and evidence

- [Cross-phase results](../results/summary/SUMMARY_REPORT.md)
- [Phase 1 readable tables](../results/summary/data/phase1_tables.md)
- [Phase 2 readable tables](../results/summary/data/phase2_tables.md)
- [Phase 4 readable tables](../results/summary/data/phase4_tables.md)
- [Phase 1 run folders](../results/phase1/)
- [Phase 2 run folders](../results/phase2/)
- [Phase 4 run folders](../results/phase4/)

## Supporting and historical notes

The files under [`discuss/`](discuss/) are concise phase discussion notes. The files under [`notes/`](notes/) capture related work and the 2025 draft reference. They remain useful evidence, but the focused documents above are the maintained reader-facing sources.

The former research-plan paths under `results/summary/RESEARCH_PLAN*` are compatibility landing pages. They point to this reorganized document set and should not become a second source of protocol or result prose.
