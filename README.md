# HerdSim

**HerdSim** is a reproducible experimental platform for investigating the
limits, robustness, generalization, and information requirements of multi-agent
shepherding.

Herding, where a small group of shepherds guides a larger flock to a target --
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

## Getting Started

1. `make install`
2. `make dev`
3. Open http://localhost:5173
