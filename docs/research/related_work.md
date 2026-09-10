# Related work

HerdSim sits among agent-based shepherding models that guide interacting
followers with steering agents. The platform emphasizes controlled variation of
assumptions: sensing, heterogeneity, environment, and controller architecture.

## Instruments in HerdSim

### Strombom et al. 2014

Heuristic Collect/Drive shepherding. Instrument: `strombom`
(`sheep_model=strombom`, `dog_controller=collect_drive`).

### Kubo et al. 2022

Force-based multi-sheepdog guidance. Instrument: `kubo`.

### Jadhav et al. 2024

Empirically informed flocking sheep responses. Instrument: `flocking_dog`
(`sheep_model=jadhav`).

## Research themes HerdSim targets

- **Herdability limits:** minimum dogs vs flock size/density.
- **Information requirements:** global, local, bearing-only, noisy sensing.
- **Heterogeneity and failure:** stubborn sheep, dog dropout/degradation.
- **Generalization:** ranking stability under distribution shift.
- **Adaptive control:** context-aware collect/drive/recover/lead.
- **Reality gap:** idealized vs Jadhav sheep; optional kinematic constraints.

Representative background includes Lien et al., El-Fiqi et al., Li et al.
(communication-free), Lama & di Bernardo (herdability), and Tsunoda et al. (FAT /
local sensing).

## What HerdSim emphasizes

Many papers propose a new controller. Fewer define a reusable factor, metric,
and scenario stack. HerdSim's contribution is that stack: shared engine, factors,
seeds, and provenance for discovering when shepherding succeeds or fails.
