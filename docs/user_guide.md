# Overview

HerdSim is an interactive research workbench for **multi-agent sheep herding**: a small number of shepherds (dogs) guides a larger flock toward a goal under controlled conditions.

The point is not only to demo one clever controller. It is to ask measurable questions about when herding works, when it fails, and how methods compare when the world, flock size, sensing, and randomness are held fair.

## Purpose and goals

HerdSim helps you:

- **Run** named herding methods (instruments) in shared scenarios
- **Vary** experimental factors (sensing, heterogeneity, failure, counts) without rewriting the engine
- **Compare** methods live (side by side) or in batch (many seeds, exports)
- **Report** outcomes with shared metrics and reproducible seeds

Typical research themes:

| Theme | Example question |
|-------|------------------|
| Herdability | How many dogs does a flock of size N need? |
| Information | Does performance collapse under local or noisy sensing? |
| Heterogeneity | What happens when some sheep barely respond to the dog? |
| Robustness | Can the team finish if a shepherd fails mid-run? |
| Generalization | Does the ranking of methods flip on a harder scenario or seed set? |
| Method contrast | Collect/Drive vs force-based vs local farthest-sheep targeting |

## What you get (features)

- **Simulate:** one live run with scrub history, metrics, inspect panel, and a run report
- **Compare:** Fair or Independent A/B arenas with live metric deltas
- **Experiments:** multi-seed instrument ranking, factor grids, charts, CSV/JSON/Markdown export
- **NetLogo:** open desktop twins for instruments that have a NetLogo counterpart
- **Guide:** this documentation set (overview, how-to pages, and reference)

Under the hood, every tick follows the same pipeline: environment updates, sheep dynamics, observation, dog control, constraints and walls, then metrics. Metrics are shared across instruments so numbers mean the same thing on every side of a comparison.

## Core ideas in plain language

**Instrument.** A ready-made method package: how sheep move plus how dogs decide where to go (for example Strombom 2014, Kubo 2022, FAT). Pick it from a list; you do not assemble plugins by hand for normal use.

**Scenario.** The task and layout (for example Drive to Goal, Obstacle Course). Success rules and world shape live here.

**Seed.** The random draw for initial positions and stochastic bits. Same instrument + scenario + seed => same replay. Different seeds => independent trials.

**Experimental factors.** Knobs around the instrument: observation mode, sensing range, noise, stubborn fraction, shepherd failure, goal motion, sheep/dog counts, and more. Change conditions without switching the named method.

**Settings source.** Instrument (paper-style defaults), Scenario (task defaults), or Custom (you lock counts and factors). Use Custom when you want a fair head-to-head ranking.

## Map of the app

Open the app at `http://localhost:5173` after `make install` and `make dev` (see the project README).

| Tab | Use it to... | Full how-to |
|-----|--------------|-------------|
| Simulate | Watch one run, scrub, inspect, download a run report | Short start below |
| Compare | Watch two instruments matched or independently | **Compare** in this Guide |
| Experiments | Rank methods over seeds, sweep factors, export | **Experiments** in this Guide |
| NetLogo | Open a desktop twin beside HerdSim | **NetLogo** in this Guide |
| Guide | Read overview and reference | You are here |

Reference pages (Instruments, Scenarios, Metrics, Environment) explain the scientific objects. Architecture is for developers extending the stack.

## First minutes in Simulate

1. Open **Simulate**.
2. Pick an **instrument** (Strombom 2014 is a good first choice) and a **scenario** (Drive to Goal).
3. Note the seed and agent counts; switch to **Custom** if you plan to change factors.
4. Click **Initialize New Run**, then **Play**.
5. Pause to **scrub** the timeline, read live metrics, and open **Inspect** for mode and model metadata.
6. When the run ends, read the **run report** (and download Markdown if you want notes).

When you are ready to compare two methods visually, switch to **Compare**. When you need many seeds and a table, switch to **Experiments**.

## Questions researchers often ask

**Is HerdSim a single algorithm demo?**
No. It is a platform: shared scenarios, seeds, factors, and metrics around many instruments.

**What is an instrument vs a factor?**
An instrument is the method bundle you select by name. A factor is a condition you vary around it (sensing, stubborn sheep, failure, counts). You can keep one instrument and still run a factor study.

**How do I compare methods fairly?**
Lock the same scenario, sheep count, dog count, seed list, and success rule. In Compare, use Fair compare. In Experiments, use Compare instruments with Custom counts. Paper presets keep each method's published counts; that is replication, not a matched ranking.

**Why do path lengths look odd across Kubo and Strombom-style methods?**
They do not advance motion the same way. Kubo uses a continuous time step (`dt`); many Strombom-family controllers move by displacement per tick. Treat path length carefully; Experiments exports call out this caveat.

**Can I reproduce a paper's agent counts?**
Yes: use Instrument (paper) settings. Say clearly that those runs are paper-default replication, not locked-count fair compare.

**Where do batch results and provenance go?**
Experiments exports (CSV, JSON, Markdown) carry trial outcomes, trajectory summaries, failure labels, design, and resolved config. Live Compare is for watching; Experiments is for evidence you can cite.

**Is NetLogo inside the browser sim?**
No. HerdSim runs the Python engine in Simulate, Compare, and Experiments. The NetLogo tab opens desktop models that mirror selected instruments for visual cross-check.

**Where should I read next?**

- Method details: **Instruments**
- Task layouts: **Scenarios**
- Score definitions: **Metrics**
- World and timing conventions: **Environment**
- Live A/B UI: **Compare**
- Batch studies: **Experiments**
- Desktop twins: **NetLogo**
