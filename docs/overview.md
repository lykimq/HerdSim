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
| Strombom 2014 | 50 sheep, 1 shepherd; if flock is spread, Collect the farthest straggler, else Drive from behind the flock toward the goal |
| Strombom Multi-Dog | Same sheep rules; 3 dogs share Collect / Drive assignments instead of stacking |
| Strombom Noise | Same as Strombom 2014 (50 sheep, 1 shepherd) but noise_strength 0.9 (vs 0.3) |
| Heterogeneous Sheep | Strombom Collect / Drive (50 sheep, 1 shepherd); 20% stubborn sheep (weaker dog response) |
| V-Formation | Strombom sheep; 2 dogs drive on a V-arc behind the flock (no classic Collect switch) |
| Obstacle-Aware | Strombom Collect / Drive (50 sheep, 1 shepherd); Drive target bends around obstacles / gates |
| Kubo 2022 | Force-based sheep and dogs (not Collect / Drive); defaults 40 sheep, 4 dogs |
| Flocking Dog 2024 | Jadhav neighbour sheep + Collect / Drive; small flock default (14 sheep, 1 dog) |
| FAT | Strombom sheep; 2 dogs each chase the farthest sheep they can see (local sensing) |
| Communication-Free | Strombom sheep; 3 dogs; each dog Collect/Drives only from sheep it can see (no team assignment, no shared GCM/target) |
| Adaptive | Strombom sheep; 2 dogs; switch by outlier count: Collect if some stragglers, Recover (stand back at 2*r_a behind flock) if many, Lead/Drive if cohesive |

Open **Instruments** in this Guide for the full write-up of each one.

## How a run works

Each tick:

```text
environment -> sheep motion -> observation -> dog decisions
  -> constraints / walls -> metrics
```

You choose an **instrument**, a **scenario**, a **seed**, and optional **factors**. Same instrument + scenario + seed replays the same way. Metrics use the same definitions across instruments so Compare and Experiments stay meaningful.

## Fixed conditions (always on)

These apply in Simulate, Compare, and Experiments. They are not optional instrument settings.

**Bounded arena.** Every run is inside a rectangular world. Agents that hit a wall bounce back (position and velocity are reflected). This differs from some papers that use an open field with no walls. Usual starting scenario **Drive to Goal**: arena **150 x 150**, circular goal of radius **15** near a corner (centre near `(15, 15)`). **Wide Field** uses **250 x 250** and goal radius **20**. Other scenarios keep 150 x 150 unless you override world settings in Custom.

**Obstacles are solid.** If the scenario places obstacles or a gate, agents cannot pass through them; they are pushed to the edge. Most instruments still aim as if obstacles were not there; only Obstacle-Aware bends its Drive target around them.

**Tick limit (timeout).** A trial stops at the scenario's `max_ticks` if success has not been reached:

| Scenario | Default max ticks | Default success rule |
|----------|-------------------|----------------------|
| Drive to Goal | 3000 | All sheep in goal (`success_fraction` 1.0) |
| Containment | 2000 | >= 95% in pen for 200 continuous ticks |
| Obstacle Course | 4000 | All sheep in goal |
| Split Flock | 4000 | >= 95% in goal |
| Narrow Gate | 4500 | All sheep in goal |
| Wide Field | 6000 | All sheep in goal |

**Success vs live occupancy.** Scenario success is the boolean win condition above. The live **Success Rate** metric is only the current fraction of sheep inside the goal (0-1); it can be high without the trial having succeeded yet (and the reverse under Containment).

**Seeded randomness.** Same instrument + scenario + seed + settings => same replay.

Paper defaults for sheep and dog counts are starting values only. Custom mode can change counts, factors, and (when exposed) world overrides; it does not remove walls. Full layout detail: **Environment** and **Scenarios** in this Guide.

## Core ideas

**Instrument.** The named method package you select (for example Strombom 2014 or Kubo 2022).

**Scenario.** The task and world layout (for example Drive to Goal or Obstacle Course), including how success is judged.

**Seed.** The random draw for initial positions and stochastic bits. Same instrument + scenario + seed means the same replay; different seeds are independent trials.

**Experimental factors.** Conditions around the instrument: observation mode, sensing range, noise, stubborn fraction, shepherd failure, goal motion, sheep/dog counts, and similar knobs.

**Settings source.** Instrument (paper-style defaults), Scenario (task defaults), or Custom (you lock counts and factors). Use Custom for a fair head-to-head ranking.

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
