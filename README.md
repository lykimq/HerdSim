# HerdSim

HerdSim is a research platform for multi-agent sheep herding. A few dogs (or shepherds) try to guide a larger flock toward a goal, under conditions you can control and repeat.

The point of the platform is fairness and comparison. You pick a named setup (an instrument: how the sheep move plus how the dogs decide), put it in a scenario, fix a random seed, and measure what happens with shared metrics. That way you can see when herding works, when it fails, and how methods compare when flock size, sensing, and other settings are held fair.

## Getting started

You need [uv](https://docs.astral.sh/uv/) and Node.js.

```bash
make install   # Python environment via uv, plus frontend dependencies
make dev       # API and Vite together
```

Then open http://localhost:5173 in your browser.

Other useful targets: `make test` and `make help`.

## What you can do

The web app has several tabs:

- **Simulate.** Run one instrument live. Scrub through history, inspect agents, and download a run report.
- **Compare.** Run two setups side by side. You can keep settings matched (fair A/B) or let each side differ. Metric deltas update as the runs go.
- **Experiments.** Run multi-seed batches and factor grids. Look at charts, then export CSV, JSON, or Markdown.
- **NetLogo.** For instruments that have a desktop twin, open the NetLogo model from here.
- **Guide.** In-app documentation: overview, instruments, scenarios, metrics, and how-tos.

Larger claim-oriented shepherding-budget campaigns live outside the Experiments tab. They use the CLI (`make budget-help`) and write under `results/budget/`.

## Instruments

An instrument is a ready-made sheep plus dog package with paper-style defaults. You pick one in Simulate, Compare, or Experiments. Around that package you can still change sensing, counts, noise, and other factors.

For the glossary (Collect, Drive, inertia, arena, timeout, and more), open the in-app Guide, Overview, then Terms.

Here are the instruments currently in the catalog:

- **`strombom` (Strombom 2014).** Defaults: 50 sheep and 1 shepherd. If the flock is spread out, Collect the farthest straggler. If it is tight, Drive from behind toward the goal.
- **`strombom_multi` (Strombom Multi-Dog).** Same sheep rules as Strombom 2014, but with 3 dogs. The dogs share the work (who Collects which sheep, where to Drive) so they do not all pile on the same spot.
- **`strombom_noise` (Strombom Noise).** Same rules and counts as Strombom 2014, but stress-tested: heading noise is tripled (0.9 instead of 0.3) and inertia is lowered (0.3 instead of 0.5). Agents keep less memory of their previous facing, jitter more, and smooth the wobble less.
- **`heterogeneous` (Heterogeneous Sheep).** Same Collect / Drive as Strombom 2014 (50 sheep, 1 shepherd). At the start of the run, 20% of sheep are marked stubborn and then feel only about 25% of the usual push from the dog for the whole trial. The shepherd does not know which sheep those are.
- **`v_formation` (V-Formation).** Strombom sheep with 2 dogs. Dogs stay on a V-shaped arc behind the flock and Drive. They do not switch into classic Collect of a single straggler.
- **`obstacle_aware` (Obstacle-Aware).** Same Collect / Drive as Strombom 2014 (50 sheep, 1 shepherd), but when Driving the aim point bends around walls, obstacles, or a gate instead of pointing straight through them.
- **`kubo` (Kubo 2022).** Different physics. Sheep and dogs move by continuous forces (attraction, repulsion, goal pull), not Collect / Drive modes. Defaults: 40 sheep and 4 dogs.
- **`flocking_dog` (Flocking Dog 2024).** Smaller default flock (14 sheep, 1 dog). Sheep use neighbour-based flocking. The dog still uses Collect / Drive and slows when already inside the group.
- **`fat` (FAT).** Strombom sheep with 2 dogs. Each dog only uses sheep it can see locally, and always heads for the farthest visible sheep (no Collect / Drive mode switch).
- **`communication_free` (Communication-Free).** Strombom sheep with 3 dogs. Each dog runs Collect / Drive using only the sheep it can see. Dogs do not share a common target or tell each other who is Collecting what.
- **`adaptive` (Adaptive).** Strombom sheep with 2 dogs. Each tick counts how many sheep are far from the group centre. A few stragglers: Collect. Many stragglers: Recover (stand farther back behind the whole flock to press it together). Tight flock: Lead ahead toward the goal, or Drive from behind if leading is off.

### Adding an instrument

Most new instruments reuse existing sheep and dog plugins. You package defaults and metadata, then register one catalog entry. Only new behaviours need a plugin implementation and a registry hook first.

Flow in short:

1. Sheep and dog plugins live under `plugins/sheep/` and `plugins/dogs/`. Register new ones in `core/plugin_registry.py`.
2. Those plugins are packaged as `instruments/<id>/` with `info.json` and paper defaults.
3. Add a `_bundle(...)` entry to `INSTRUMENTS` in `core/instruments.py`.
4. The catalog then shows up in Simulate, Compare, and Experiments.

More detail: [docs/architecture.md](docs/architecture.md).

## How a run works

Each tick follows the same loop:

```text
environment -> sheep motion -> observation -> dog decisions
  -> constraints / walls -> metrics
```

You choose an instrument, a scenario, a seed, and optional factors. Same instrument, scenario, and seed replay the same way.

Hard conditions that always apply:

- A rectangular arena with wall bounce. Drive to Goal defaults to 150 x 150 with goal radius 15 (not an open field).
- Solid obstacles when the scenario has them.
- A max-tick timeout (3000 on Drive to Goal; other scenarios differ).
- Scenario-defined success.

Details live in the in-app Guide under Overview and Environment.

## Project layout

- `core/`: simulation engine, factors, observation, instrument catalog
- `plugins/`: sheep, dogs, scenarios, metrics
- `instruments/`: named packages (`info.json`, paper defaults, helpers)
- `api/`: HTTP and WebSocket API for the UI
- `services/`: Experiments engine (`services/experiments/`) and budget campaign runners (`services/budget/`)
- `analysis/`: failure taxonomy helpers and budget analysis packages (`analysis/budget/`)
- `frontend/`: Vite app (Simulate, Compare, Experiments, NetLogo, Guide)
- `docs/`: architecture, in-app Guide pages, and research notes under `docs/research/`
- `integrations/`: NetLogo models and MATLAB reference code
- `scripts/`: local `dev.sh` and budget CLIs under `scripts/budget/`
- `configs/budget/`: frozen protocol and campaign YAML subsets
- `results/budget/`: campaign outputs (`phase{k}/{slug}/`; see `results/budget/README.md`)
- `tests/`: backend pytest and frontend node tests
- `Makefile` / `Makefile.budget`: project targets and budget campaign targets

## Shepherding-budget campaigns

```bash
make budget-help
# or: make -f Makefile.budget help
```
