# HerdSim

**HerdSim** is a reproducible experimental platform for investigating the
limits, robustness, generalization, and information requirements of multi-agent
shepherding.

Herding -- where a small group of shepherds guides a larger flock to a target --
is studied here through orthogonal experimental factors rather than algorithm
catalogues alone. Named **instruments** are factor bundles over
`sheep_model` x `dog_controller`. Controllers are instruments for measuring
herdability; metrics stay algorithm-agnostic.

## Motivation

- **Herdability:** when is a flock controllable under given N_sheep, N_dogs, and density?
- **Information:** how does performance change under global, local, bearing, or noisy sensing?
- **Heterogeneity:** how do outcomes change when sheep or dogs differ in response or capability?
- **Generalization:** do rankings reverse under distribution shift?

## Architecture

Each tick runs:

```text
environment updates -> sheep dynamics -> observation -> dog controller
-> constraints -> obstacles/walls -> metrics
```

See [docs/architecture.md](docs/architecture.md) for the factor-based plugin layout.

## Research docs

- [Compare (fair comparison)](docs/research/comparison_framework.md)
- [Experiments](docs/experiments.md)
- [Metrics](docs/research/metrics.md)
- [Related work](docs/research/related_work.md)
- [Architecture](docs/architecture.md)
- [Instruments](docs/research/algorithms/README.md)

## Getting Started

1. `make install`
2. `make dev`
3. Open http://localhost:5173

UI tabs: **Simulate** (single run + inspect + run report), **Compare** (Arena A/B),
**Experiments** (fair compare / factor grid + CSV/JSON export), **NetLogo** (desktop twins),
**Guide** (same docs as this tree).

Batch studies run in the **Experiments** tab; see [Experiments](docs/experiments.md).
Live A/B watching is in **Compare**; see [Compare](docs/research/comparison_framework.md).
