# Overview

HerdSim is a research platform for **multi-agent sheep herding**: a few dogs (or shepherds) guide a larger flock toward a goal under controlled, repeatable conditions. Named **instruments** (sheep + dog setups) and shared **metrics** let you measure when herding works, when it fails, and how methods compare when flock size, sensing, scenario, and seeds are held fair.

## What you can do

| Feature | What it is for |
|---------|----------------|
| **Simulate** | Run one instrument live; scrub history; inspect agents; download a run report |
| **Compare** | Side-by-side A/B runs (fair shared settings, or independent) with live metric deltas |
| **Experiments** | Multi-seed batches and factor grids; charts; CSV / JSON / Markdown export |
| **NetLogo** | Open desktop NetLogo twins for instruments that have a counterpart |
| **Guide** | This documentation: overview, instruments, scenarios, metrics, and how-tos |

## Instruments

An instrument is a ready-made herding setup: how sheep move plus how dogs decide where to go, with sensible defaults. Pick one in Simulate, Compare, or Experiments; you can still change sensing, counts, noise, and other factors around it.

| Name | Role |
|------|------|
| Strombom 2014 | Classic Collect / Drive, one shepherd |
| Strombom Multi-Dog | Strombom variant: shared Collect / Drive across several dogs |
| Strombom Noise | Strombom variant: elevated process noise |
| Heterogeneous Sheep | Strombom variant: stubborn sheep fraction (harder finish) |
| V-Formation | Strombom variant: multi-dog drive on a V-arc behind the flock |
| Obstacle-Aware | Strombom variant: drive deflected around obstacles / gates |
| Kubo 2022 | Force-based multi-dog herding |
| Flocking Dog 2024 | Neighbour-based sheep motion + Collect / Drive |
| FAT | Strombom variant: farthest-agent targeting under local observations |
| Communication-Free | Strombom variant: independent Collect / Drive, no shared targets |
| Adaptive | Strombom variant: collect / drive / recover / lead mode switcher |

Open **Instruments** in this Guide for the full write-up of each one.

## How a run works

Each tick:

```text
environment -> sheep motion -> observation -> dog decisions
  -> constraints / walls -> metrics
```

You choose an **instrument**, a **scenario**, a **seed**, and optional **factors**. Same instrument + scenario + seed replays the same way. Metrics use the same definitions across instruments so Compare and Experiments stay meaningful.

## Core ideas

**Instrument.** The named method package you select (for example Strombom 2014 or Kubo 2022).

**Scenario.** The task and world layout (for example Drive to Goal or Obstacle Course), including how success is judged.

**Seed.** The random draw for initial positions and stochastic bits. Same instrument + scenario + seed means the same replay; different seeds are independent trials.

**Experimental factors.** Conditions around the instrument: observation mode, sensing range, noise, stubborn fraction, shepherd failure, goal motion, sheep/dog counts, and similar knobs.

**Settings source.** Instrument (paper-style defaults), Scenario (task defaults), or Custom (you lock counts and factors). Use Custom for a fair head-to-head ranking.

## Map of the app

| Tab | Use it to... |
|-----|----------------|
| Simulate | Watch one run, scrub, inspect, download a run report |
| Compare | Watch two instruments matched or independently |
| Experiments | Rank methods over seeds, sweep factors, export results |
| NetLogo | Open a desktop twin beside HerdSim |
| Guide | Read this overview and the reference pages |

## First minutes in Simulate

1. Open **Simulate**.
2. Pick an **instrument** (Strombom 2014 is a good first choice) and a **scenario** (Drive to Goal).
3. Note the seed and agent counts; switch to **Custom** if you plan to change factors.
4. Click **Initialize New Run**, then **Play**.
5. Pause to **scrub** the timeline, read live metrics, and open **Inspect** for mode and model details.
6. When the run ends, read the **run report** (and download Markdown if you want notes).

When you want two methods side by side, open **Compare**. When you need many seeds and a table, open **Experiments**.

## Frequently asked questions

**Is HerdSim a single algorithm demo?**
No. It is a platform: shared scenarios, seeds, factors, and metrics around many instruments.

**What is an instrument vs a factor?**
An instrument is the method you select by name. A factor is a condition you vary around it (sensing, stubborn sheep, failure, counts). You can keep one instrument and still run a factor study.

**How do I compare methods fairly?**
Lock the same scenario, sheep count, dog count, seed list, and success rule. In Compare, use Fair compare. In Experiments, use Compare instruments with Custom counts. Paper presets keep each method's published counts; that is replication, not a matched ranking.

**Why do path lengths look odd across Kubo and Strombom-style methods?**
They do not advance motion the same way. Kubo uses a continuous time step; many Strombom-family controllers move by a fixed step per tick. Treat path length carefully; Experiments exports note this caveat.

**Can I reproduce a paper's agent counts?**
Yes: use Instrument (paper) settings. Say clearly that those runs are paper-default replication, not locked-count fair compare.

**Where do batch results go?**
Use the **Experiments** tab to download CSV, JSON, or Markdown from the browser. Live Compare is for watching; Experiments is for downloadable trial tables.

**Is NetLogo inside the browser sim?**
No. HerdSim runs its own engine in Simulate, Compare, and Experiments. The NetLogo tab opens desktop models that mirror selected instruments for a visual cross-check.

**Where should I read next?**

- Method details: **Instruments**
- Task layouts: **Scenarios**
- Score definitions: **Metrics**
- World and timing: **Environment**
- Live A/B: **Compare**
- Batch studies: **Experiments**
- Desktop twins: **NetLogo**
