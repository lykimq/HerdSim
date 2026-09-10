# HerdSim

**HerdSim** is an interactive agent-based research platform for simulating,
visualizing, and comparing sheep herding models under shared scenarios and
metrics.

Herding -- where a small group of shepherds guides a larger flock to a target --
is a complex problem in robotics and collective behaviour. HerdSim provides a
standardized experimental stack so different models can be evaluated under
equivalent conditions.

## Motivation

- **Visualization:** watch algorithms in real time.
- **Standardization:** same scenarios, metrics, and seeds across models.
- **Extensibility:** plug in algorithms, scenarios, and metrics without rewriting the engine.

Core comparison families: Strombom 2014, Kubo 2022, and Jadhav 2024 (`flocking_dog`).

## Research docs

- [Comparison framework](docs/research/comparison_framework.md) -- fair protocol and reporting
- [Metrics](docs/research/metrics.md) -- taxonomy, trajectory aggregates, provenance
- [Related work](docs/research/related_work.md) -- situating the three model families
- [Architecture](docs/architecture.md) -- tick lifecycle and plugins
- [Algorithms](docs/research/algorithms/README.md) -- suite map

Fair comparison CLI: `python scripts/run_fair_compare.py` (shared N/M, default 30 seeds).

## Getting Started

You need Python and Node.js.

1. **Install dependencies:**
   ```bash
   make install
   ```
2. **Start the simulation server and visual interface:**
   ```bash
   make dev
   ```

Open **http://localhost:5173** to start simulating.
