# HerdSim

**HerdSim** is a reproducible experimental platform for investigating the
limits, robustness, generalization, and information requirements of multi-agent
shepherding.

Herding -- where a small group of shepherds guides a larger flock to a target --
is studied here through orthogonal experimental factors rather than algorithm
catalogues alone. Controllers are instruments for measuring herdability.

## Motivation

- **Herdability:** when is a flock controllable under given N_sheep, N_dogs, and density?
- **Information:** how does performance change under global, local, bearing, or noisy sensing?
- **Heterogeneity:** how robust are strategies when sheep or dogs are not identical?
- **Generalization:** do rankings reverse under distribution shift?

## Architecture

Each tick runs:

```text
environment updates -> sheep dynamics -> observation -> dog controller
-> constraints -> obstacles/walls -> metrics
```

Named instruments (e.g. `strombom`, `kubo`, `flocking_dog`) are factor bundles
over `sheep_model` x `dog_controller`.

## Research docs

- [Comparison framework](docs/research/comparison_framework.md)
- [Metrics](docs/research/metrics.md)
- [Related work](docs/research/related_work.md)
- [Architecture](docs/architecture.md)
- [Instruments](docs/research/algorithms/README.md)

Fair comparison: `python scripts/run_fair_compare.py`

Factor grids: `python scripts/run_factor_grid.py --grid 'n_sheep=20,50;n_shepherds=1,2' --seeds 1,2,3`

## Getting Started

1. `make install`
2. `make dev`
3. Open http://localhost:5173
