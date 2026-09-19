# HerdSim

HerdSim is a research platform for **multi-agent sheep herding**: a few dogs (or shepherds) guide a larger flock toward a goal under controlled, repeatable conditions. Named **instruments** (sheep + dog setups) and shared **metrics** let you measure when herding works, when it fails, and how methods compare when flock size, sensing, scenario, and seeds are held fair.

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
| **Guide** | In-app docs: overview, instruments, scenarios, metrics, how-tos |

Larger claim-oriented **shepherding-budget** campaigns use the CLI (`make budget-help`) and `results/budget/`, separate from the Experiments tab.

## Instruments

An instrument is a ready-made sheep + dog setup with paper-style defaults. Pick one in Simulate, Compare, or Experiments; you can still change sensing, counts, noise, and other factors around it.

Full plain-language glossary (Collect, Drive, inertia, arena, timeout, and more): in-app Guide **Overview** -> **Terms**.

| Id | Name | Role |
|----|------|------|
| `strombom` | Strombom 2014 | Defaults 50 sheep and 1 shepherd. If the flock is spread out, Collect the farthest straggler; if it is tight, Drive from behind toward the goal. |
| `strombom_multi` | Strombom Multi-Dog | Same sheep rules as Strombom 2014, but with 3 dogs. The dogs share the work (who Collects which sheep, where to Drive) so they do not all pile on the same spot. |
| `strombom_noise` | Strombom Noise | Same rules and counts as Strombom 2014, but stress-tested: heading noise is tripled (0.9 instead of 0.3) and inertia is lowered (0.3 instead of 0.5), so agents have less memory of their previous facing, jitter more, and smooth the wobble less. |
| `heterogeneous` | Heterogeneous Sheep | Same Collect / Drive as Strombom 2014 (50 sheep, 1 shepherd). At the start of the run, 20% of sheep are marked stubborn and then feel only about 25% of the usual push from the dog for the whole trial. The shepherd does not know which sheep those are. |
| `v_formation` | V-Formation | Strombom sheep with 2 dogs. Dogs stay on a V-shaped arc behind the flock and Drive; they do not switch into classic Collect of a single straggler. |
| `obstacle_aware` | Obstacle-Aware | Same Collect / Drive as Strombom 2014 (50 sheep, 1 shepherd), but when Driving the aim point bends around walls, obstacles, or a gate instead of pointing straight through them. |
| `kubo` | Kubo 2022 | Different physics: sheep and dogs move by continuous forces (attraction, repulsion, goal pull), not Collect / Drive modes. Defaults 40 sheep and 4 dogs. |
| `flocking_dog` | Flocking Dog 2024 | Smaller default flock (14 sheep, 1 dog). Sheep use neighbour-based flocking; the dog still uses Collect / Drive and slows when already inside the group. |
| `fat` | FAT | Strombom sheep with 2 dogs. Each dog only uses sheep it can see locally, and always heads for the farthest visible sheep (no Collect / Drive mode switch). |
| `communication_free` | Communication-Free | Strombom sheep with 3 dogs. Each dog runs Collect / Drive using only the sheep it can see. Dogs do not share a common target or tell each other who is Collecting what. |
| `adaptive` | Adaptive | Strombom sheep with 2 dogs. Each tick counts how many sheep are far from the group centre: a few stragglers -> Collect; many stragglers -> Recover (stand farther back behind the whole flock to press it together); tight flock -> Lead ahead toward the goal, or Drive from behind if leading is off. |

### Adding an instrument

Most new instruments reuse existing sheep and dog plugins. You package defaults and metadata, then register one catalog entry; only new behaviours need a plugin implementation and registry hook first.

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

1. Reuse or implement plugins under `plugins/sheep/` and `plugins/dogs/`, then register them in `core/plugin_registry.py` if they are new.
2. Add `instruments/<id>/` with `info.json` and paper defaults.
3. Add a `_bundle(...)` entry to `INSTRUMENTS` in `core/instruments.py`.

Details: [docs/architecture.md](docs/architecture.md).

## How a run works

Each tick:

```text
environment -> sheep motion -> observation -> dog decisions
  -> constraints / walls -> metrics
```

You choose an **instrument**, a **scenario**, a **seed**, and optional **factors**. Same instrument + scenario + seed replays the same way.

Hard conditions that always apply: rectangular arena with wall bounce (Drive to Goal default 150 x 150, goal radius 15; not an open field), solid obstacles when the scenario has them, a max-tick timeout (3000 on Drive to Goal; other scenarios differ), and scenario-defined success. Details: in-app Guide under Overview and Environment.

## Project layout

- `core/`: engine, factors, instrument catalog
- `plugins/`: sheep, dogs, scenarios, metrics
- `instruments/`: named packages (`info.json`, paper defaults)
- `api/`: HTTP and WebSocket for the UI
- `services/`: Experiments engine and budget campaign runners
- `frontend/`: Vite app
- `docs/`: architecture and Guide pages
- `integrations/`: NetLogo and MATLAB references
- `configs/budget/`, `scripts/budget/`, `results/budget/`: budget campaigns

## Shepherding-budget campaigns

```bash
make budget-help
# or: make -f Makefile.budget help
```
