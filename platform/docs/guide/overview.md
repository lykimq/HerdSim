# Overview

HerdSim is a research platform for multi-agent sheep herding. A few dogs (or shepherds) try to guide a larger flock toward a goal, under conditions you can control and repeat.

The platform is built around named methods (a sheep model plus a dog controller, with paper-style defaults) and shared metrics. That combination lets you measure when herding works, when it fails, and how methods compare when flock size, sensing, scenario, and seeds are held fair.

## What you can do

- **Simulate.** Run one method live. Scrub history, inspect agents, and download a run report.
- **Compare.** Watch two runs side by side. Keep settings matched (fair A/B) or let each side differ. Metric deltas update as the runs go.
- **Experiments.** Run multi-seed batches and factor grids. Look at charts, then export CSV, JSON, or Markdown.
- **NetLogo.** For methods that have a desktop twin, open the NetLogo model from here. That twin is not the browser simulation.
- **Guide.** This documentation: overview, methods, scenarios, metrics, and how-tos.

## Terms

### Core setup

- **Method:** a named ready-made package (how sheep move plus how dogs decide), with paper-style defaults.
- **Scenario:** the task and world layout (arena, goal or pen, obstacles, success rule). Examples: Drive to Goal, Obstacle Course.
- **Seed:** the random draw for start positions and chance events. Same method, scenario, seed, and settings give the same replay.
- **Experimental factors:** knobs around a method (sensing, noise, stubborn fraction, dog failure, goal motion, sheep/dog counts, and similar).
- **Mode / settings source:** how defaults are locked in the UI. **Paper original** uses paper counts and parameters on Drive to Goal. **Scenarios** uses the scenario-recommended setup. **Custom** lets you lock counts and factors for a fair compare.
- **Paper defaults:** published-style sheep and dog counts and parameters for a method. Good for replication. Not always a fair head-to-head.
- **Fair compare:** same scenario, sheep count, dog count, seed(s), and success rule across methods so rankings are matched.
- **Trial / run:** one simulation from initialize until success or timeout.
- **Metric:** a number computed each tick or summarised over a trial. Definitions are shared across methods.

### Agents and flock

- **Sheep:** flock agents that move, graze, and usually flee dogs.
- **Shepherd / dog:** the herding agent. Naming differs by method, but the role in the UI is the same.
- **Flock:** the set of sheep in the run.
- **Straggler:** a sheep that has drifted far from the rest of the flock.
- **Group centre (GCM):** average position of the sheep in the current flock view. Metrics often label this GCM.
- **Stubborn sheep:** sheep marked at the start of a Heterogeneous run that react much less to a nearby dog (harder to push). Default: 20% of the flock feel about 25% of the usual push.
- **Neighbour-based flocking:** sheep update from nearby sheep (used by Flocking Dog), not only the classic Strombom sheep rules.
- **Force-based motion:** Kubo-style continuous push and pull forces instead of Collect / Drive modes.

### Dog behaviours

- **Collect:** move to gather a sheep that has drifted away from the group.
- **Drive:** stand behind the group and push it toward the goal.
- **Recover:** Adaptive only. When many sheep are far out, stand farther back behind the whole flock and press it together. This is not chasing one straggler.
- **Lead:** Adaptive only. When the flock is tight, move ahead of the group toward the goal. Sheep still only flee dogs. They do not follow a leader.
- **V-formation:** multi-dog Drive on a V-shaped arc behind the flock. No classic Collect of one straggler.
- **FAT:** each dog always heads for the farthest sheep it can see. No Collect / Drive switch.
- **Communication-Free:** each dog Collects / Drives from its own view only. No shared team target or assignment.
- **Assignment:** coordinated Multi-Dog sharing of who Collects which sheep and where to Drive so dogs do not stack.

### Sensing and variation

- **Observation / sensing:** what each dog is allowed to know about sheep (and sometimes other dogs) on a tick.
- **Local sensing:** a dog only sees sheep within its sensing setup, not the whole flock.
- **Global sensing:** a dog can use the full flock picture.
- **Heading noise:** random wobble in which way an agent faces each tick. Higher means twitchier paths.
- **Inertia:** how much an agent keeps its previous facing / memory of the last heading. Higher means smoother. Lower means less memory, so noise shows more.
- **Shepherd failure:** a factor that can disable a dog mid-run.
- **Goal motion:** a factor where the goal moves over time instead of staying fixed.

### World and success

- **Arena:** rectangular world from the scenario. Agents that hit a wall bounce back. This is not an open field.
- **Wall bounce / reflection:** leaving the arena flips the agent back inside and reverses that velocity component.
- **Goal / goal zone:** circular target region. Sheep inside it count toward occupancy and usually toward success.
- **Pen:** Containment scenario's hold-inside region. Same idea as a goal zone, different success rule.
- **Obstacle:** solid rectangle agents cannot pass through. They are pushed to the edge.
- **Gate:** narrow opening between walls (Narrow Gate scenario).
- **Open field:** unbounded world with no walls (some papers). HerdSim does not use this. Arenas are bounded.
- **Scenario success:** boolean win for the trial (the scenario rule first holds).
- **Success Rate (live metric):** current fraction of sheep inside the goal (0 to 1). Not the same as scenario success.
- **Timeout:** trial ends because max ticks were reached without success.
- **Max ticks:** tick limit for the scenario (for example Drive to Goal default 3000).

### Timing and motion

- **Tick:** one simulation step (environment, sheep, observation, dog decisions, walls/obstacles, metrics).
- **Displacement-per-tick:** Strombom-family motion. Fixed step length per tick along heading.
- **Continuous time step (dt):** Kubo-style motion. Position updates with velocity times `dt`. Path lengths are not directly comparable across the two conventions.
- **Scrub:** drag the history slider to replay a past tick in Simulate or Compare.
- **Run report:** end-of-run summary in Simulate (download Markdown or JSON).

## Methods

A method is a ready-made herding setup: how sheep move plus how dogs decide where to go, with sensible defaults. Pick one in Simulate, Compare, or Experiments. You can still change sensing, counts, noise, and other factors around it. The terms above apply to the list below.

- **Strombom 2014.** Defaults: 50 sheep and 1 shepherd. If the flock is spread out, Collect the farthest straggler. If it is tight, Drive from behind toward the goal.
- **Strombom Multi-Dog.** Same sheep rules as Strombom 2014, but with 3 dogs. The dogs share the work (who Collects which sheep, where to Drive) so they do not all pile on the same spot.
- **Strombom Noise.** Same rules and counts as Strombom 2014, but stress-tested: heading noise is tripled (0.9 instead of 0.3) and inertia is lowered (0.3 instead of 0.5). Agents keep less memory of their previous facing, jitter more, and smooth the wobble less.
- **Heterogeneous Sheep.** Same Collect / Drive as Strombom 2014 (50 sheep, 1 shepherd). At the start of the run, 20% of sheep are marked stubborn and then feel only about 25% of the usual push from the dog for the whole trial. The shepherd does not know which sheep those are.
- **V-Formation.** Strombom sheep with 2 dogs. Dogs stay on a V-shaped arc behind the flock and Drive. They do not switch into classic Collect of a single straggler.
- **Obstacle-Aware.** Same Collect / Drive as Strombom 2014 (50 sheep, 1 shepherd), but when Driving the aim point bends around walls, obstacles, or a gate instead of pointing straight through them.
- **Kubo 2022.** Different physics. Sheep and dogs move by continuous forces (attraction, repulsion, goal pull), not Collect / Drive modes. Defaults: 40 sheep and 4 dogs.
- **Flocking Dog 2024.** Smaller default flock (14 sheep, 1 dog). Sheep use neighbour-based flocking. The dog still uses Collect / Drive and slows when already inside the group.
- **FAT.** Strombom sheep with 2 dogs. Each dog only uses sheep it can see locally, and always heads for the farthest visible sheep (no Collect / Drive mode switch).
- **Communication-Free.** Strombom sheep with 3 dogs. Each dog runs Collect / Drive using only the sheep it can see. Dogs do not share a common target or tell each other who is Collecting what.
- **Adaptive.** Strombom sheep with 2 dogs. Each tick counts how many sheep are far from the group centre. A few stragglers: Collect. Many stragglers: Recover (stand farther back behind the whole flock to press it together). Tight flock: Lead ahead toward the goal, or Drive from behind if leading is off.

Open **Methods** in this Guide for the full write-up of each one.

## How a run works

Each tick follows the same loop:

```text
environment -> sheep motion -> observation -> dog decisions
  -> constraints / walls -> metrics
```

You choose a method, a scenario, a seed, and optional factors. Same method, scenario, and seed replay the same way. Metrics use the same definitions across methods so Compare and Experiments stay meaningful.

## Fixed conditions (always on)

These apply in Simulate, Compare, and Experiments. They are not optional method settings.

**Bounded arena.** Every run is inside a rectangular world. Agents that hit a wall bounce back (position and velocity are reflected). This differs from some papers that use an open field with no walls. Usual starting scenario **Drive to Goal**: arena **150 x 150**, circular goal of radius **15** near a corner (centre near `(15, 15)`). **Wide Field** uses **250 x 250** and goal radius **20**. Other scenarios keep 150 x 150 unless you override world settings in Custom.

**Obstacles are solid.** If the scenario places obstacles or a gate, agents cannot pass through them. They are pushed to the edge. Most methods still aim as if obstacles were not there. Only Obstacle-Aware bends its Drive target around them.

**Tick limit (timeout).** A trial stops at the scenario's max ticks if success has not been reached:

| Scenario | Default max ticks | Default success rule |
|----------|-------------------|----------------------|
| Drive to Goal | 3000 | All sheep in goal (success fraction 1.0) |
| Containment | 2000 | At least 95% in pen for 200 continuous ticks |
| Obstacle Course | 4000 | All sheep in goal |
| Split Flock | 4000 | At least 95% in goal |
| Narrow Gate | 4500 | All sheep in goal |
| Wide Field | 6000 | All sheep in goal |

**Success vs live occupancy.** Scenario success is the boolean win condition above. The live Success Rate metric is only the current fraction of sheep inside the goal (0 to 1). It can be high without the trial having succeeded yet (and the reverse under Containment).

**Seeded randomness.** Same method, scenario, seed, and settings give the same replay.

Paper defaults for sheep and dog counts are starting values only. Custom mode can change counts, factors, and (when exposed) world overrides. It does not remove walls. Full layout detail: **Environment** and **Scenarios** in this Guide.

## Frequently asked questions

**Is HerdSim a single algorithm demo?**
No. It is a platform: shared scenarios, seeds, factors, and metrics around many methods.

**What is a method vs a factor?**
A method is the method you select by name. A factor is a condition you vary around it (sensing, stubborn sheep, failure, counts). You can keep one method and still run a factor study.

**How do I compare methods fairly?**
Lock the same scenario, sheep count, dog count, seed list, and success rule. In Compare, use Fair compare. In Experiments, use Compare methods with Custom counts. Paper presets keep each method's published counts. That is replication, not a matched ranking.

**Why do path lengths look odd across Kubo and Strombom-style methods?**
They do not advance motion the same way. Kubo uses a continuous time step. Many Strombom-family controllers move by a fixed step per tick. Treat path length carefully. Experiments exports note this caveat.

**Can I reproduce a paper's agent counts?**
Yes: use Method (paper) settings. Say clearly that those runs are paper-default replication, not locked-count fair compare.

**Where do batch results go?**
Use the **Experiments** tab to download CSV, JSON, or Markdown from the browser. Live Compare is for watching. Experiments is for downloadable trial tables.

**Is NetLogo inside the browser sim?**
No. HerdSim runs its own engine in Simulate, Compare, and Experiments. The NetLogo tab opens desktop models that mirror selected methods for a visual cross-check.
