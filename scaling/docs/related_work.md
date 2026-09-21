# Related work

Agent-based shepherding models differ mainly in how sheep move and how dogs choose targets. HerdSim keeps scenarios and metrics shared so you can vary sensing, heterogeneity, environment, and controller architecture in controlled experiments.

## Methods in HerdSim

### Strombom et al. 2014

Heuristic Collect/Drive shepherding. Method: `strombom` (`sheep_model=strombom`, `dog_controller=collect_drive`).

### Kubo et al. 2022

Force-based multi-sheepdog guidance. Method: `kubo`.

### Jadhav et al. 2024

Empirically informed flocking sheep responses. Method: `flocking_dog` (`sheep_model=jadhav`).

### Tsunoda et al. 2018 (FAT)

Farthest-agent targeting under local observations. Method: `fat` (Strombom sheep, FAT dog controller).

### Li et al. 2023 (Communication-Free)

Decentralised Collect / Drive without shared dog targets. Method: `communication_free`.

### Adaptive (HerdSim)

Mode switcher (collect, drive, recover, lead) inspired by context-aware and lead-herd literature. Method: `adaptive`. Not tied to one paper implementation.

## Research themes HerdSim targets

- **Herdability limits:** minimum dogs vs flock size/density.
- **Collective controllability / scalings:** state, regimes, interference, information substitution, scaling, early warning -- see [main_scaling_plan.md](main_scaling_plan.md) (single source of truth).
- **Information requirements:** global, local, bearing-only, noisy sensing.
- **Heterogeneity and failure:** stubborn sheep, dog dropout/degradation.
- **Generalization:** ranking stability under distribution shift.
- **Adaptive control:** context-aware collect/drive/recover/lead.
- **Reality gap:** idealized vs Jadhav sheep; optional kinematic constraints.

Representative background includes Lien et al., El-Fiqi et al., Li et al. (communication-free), Lama & di Bernardo (herdability), and Tsunoda et al. (FAT / local sensing).

## What HerdSim emphasizes

Many papers propose a new controller. Fewer define a reusable factor, metric, and scenario stack. HerdSim's contribution is that stack: shared engine, factors, seeds, and provenance for discovering when shepherding succeeds or fails.
