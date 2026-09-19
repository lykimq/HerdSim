# HerdSim

HerdSim is a research platform for **multi-agent sheep herding**: a few dogs
(or shepherds) guide a larger flock toward a goal under controlled, repeatable
conditions. Named **instruments** (sheep + dog setups) and shared **metrics**
let you measure when herding works, when it fails, and how methods compare when
flock size, sensing, scenario, and seeds are held fair.

## Getting started

Requires [uv](https://docs.astral.sh/uv/) and Node.js.

```bash
make install   # Python venv via uv + frontend deps
make dev       # API + Vite together
```

Open http://localhost:5173

Useful targets: `make test`, `make help`.

## What you can do

| Feature | What it is for |
|---------|----------------|
| **Simulate** | Run one instrument live; scrub history; inspect agents; download a run report |
| **Compare** | Side-by-side A/B runs (fair shared settings, or independent) with live metric deltas |
| **Experiments** | Multi-seed batches and factor grids; charts; CSV / JSON / Markdown export |
| **NetLogo** | Open desktop NetLogo twins for instruments that have a counterpart |
| **Guide** | In-app docs: overview, instruments, scenarios, metrics, architecture |

Larger claim-oriented **shepherding-budget** campaigns use the CLI
(`make budget-help`) and `results/budget/`, separate from the Experiments tab.

## Instruments

An instrument is a ready-made `sheep_model` x `dog_controller` bundle with
paper-style defaults. Pick one in Simulate, Compare, or Experiments; vary
sensing, counts, noise, and other factors around it without changing the method.

| Id | Name | Role |
|----|------|------|
| `strombom` | Strombom 2014 | Classic Collect / Drive, one shepherd |
| `strombom_multi` | Strombom Multi-Dog | Strombom variant: shared Collect / Drive across several dogs |
| `strombom_noise` | Strombom Noise | Strombom variant: elevated process noise |
| `heterogeneous` | Heterogeneous Sheep | Strombom variant: stubborn sheep fraction (harder finish) |
| `v_formation` | V-Formation | Strombom variant: multi-dog drive on a V-arc behind the flock |
| `obstacle_aware` | Obstacle-Aware | Strombom variant: drive deflected around obstacles / gates |
| `kubo` | Kubo 2022 | Force-based multi-dog herding |
| `flocking_dog` | Flocking Dog 2024 | Jadhav sheep + Collect / Drive |
| `fat` | FAT | Strombom variant: farthest-agent targeting under local observations |
| `communication_free` | Communication-Free | Strombom variant: independent Collect / Drive, no shared targets |
| `adaptive` | Adaptive | Strombom variant: collect / drive / recover / lead mode switcher |

Guide write-ups: [docs/research/instruments/](docs/research/instruments/).

### Adding an instrument

Most new instruments reuse existing sheep and dog plugins. You package defaults
and metadata, then register one catalog entry; only new behaviours need a
plugin implementation and registry hook first.

```mermaid
flowchart LR
  plugins["Sheep / dog plugins"]
  registry["plugin_registry"]
  package["instruments/id package"]
  catalog["core/instruments.py"]
  ui(["Simulate Compare Experiments"])

  plugins --> registry
  registry --> package
  package --> catalog
  catalog --> ui
```

1. Reuse or implement plugins under `plugins/sheep/` and `plugins/dogs/`, then
   register them in `core/plugin_registry.py` if they are new.
2. Add `instruments/<id>/` with `info.json` and paper defaults.
3. Add a `_bundle(...)` entry to `INSTRUMENTS` in `core/instruments.py`.

Details: [docs/architecture.md](docs/architecture.md).

## How a run works

Each tick:

```text
environment -> sheep motion -> observation -> dog decisions
  -> constraints / walls -> metrics
```

You choose an **instrument**, a **scenario**, a **seed**, and optional
**factors**. Same instrument + scenario + seed replays the same way.

## Project layout

- `core/` -- engine, factors, instrument catalog
- `plugins/` -- sheep, dogs, scenarios, metrics
- `instruments/` -- named packages (`info.json`, paper defaults)
- `api/` -- HTTP and WebSocket for the UI
- `services/` -- Experiments engine and budget campaign runners
- `frontend/` -- Vite app
- `docs/` -- architecture and Guide pages
- `integrations/` -- NetLogo and MATLAB references
- `configs/budget/`, `scripts/budget/`, `results/budget/` -- budget campaigns

## Shepherding-budget campaigns

```bash
make budget-help
# or: make -f Makefile.budget help
```
