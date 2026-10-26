# HerdSim architecture

This document explains how HerdSim is put together and why it's built that way. For what the project does, see the [README](../../README.md); for how to configure a run and what it writes, the [configuration guide](../guides/configuration.md); for the commands, the [CLI reference](../guides/cli_reference.md).

## What the design has to serve

HerdSim isn't a general-purpose simulator. It exists to run controlled experiments: thousands of short simulations whose results get compared against each other and turned into claims. Most of the design follows from that:

- Comparisons have to be fair. Two cells that differ only in dog count must differ only in dog count: same field, same parameters, same start flocks.
- Results have to be traceable. Months later you should be able to tell exactly what produced a number, even after the code and configs have moved on.
- Campaigns are long. A grid is thousands of trials and can run for days. Runs get stopped, crash or need a restart, and none of that should cost finished work.
- Methods and tasks keep changing. We swap dog rules, sheep models and tasks, and that shouldn't mean rewriting the engine or the campaign code each time.
- Analysis keeps changing too. Thresholds and summaries get redefined long after the simulations have run.

## The big picture

```mermaid
flowchart LR
    subgraph define["Define"]
        P["protocol YAML<br/>+ canonical defaults"]
    end
    subgraph execute["Execute"]
        C["campaign runner<br/>calibration, rounds,<br/>workers, resume"]
        E["engine<br/>one trial, tick by tick"]
        K["packaging<br/>trial -> one table row"]
    end
    subgraph evidence["Evidence"]
        R["results folder<br/>frozen protocol, trials,<br/>provenance, status"]
    end
    subgraph decide["Decide"]
        A["frontier rules<br/>reliability, comparisons,<br/>D values, zones"]
    end

    P --> C
    C --> E
    E --> K
    K --> R
    R --> A
    A -. "which cells need seeds" .-> C
```

There are four stages:

1. Define. An experiment is a YAML file, not code.
2. Execute. The campaign runner turns the protocol into D curves, cells and seeds, hands each trial to the engine, and packages the outcome as one row.
3. Evidence. Everything lands in a results folder that holds enough to audit the run on its own.
4. Decide. The frontier rules read the rows and say, per curve, which values are decided and which cells still need seeds.

The loop back from the rules to the runner is the adaptive part: the runner keeps adding seeds, and dog counts between neighbours, until the rules have nothing left to decide. It also stops when every open cell has reached the seed cap, or when the time budget of the run is spent. The budget counts from the start of each run, after calibration, so a resumed run gets a new one; it bounds one sitting, not the campaign.

## Design principles

### The protocol is the experiment

An experiment is described entirely by data: a protocol YAML layered over a shared set of canonical defaults. The grid, the methods, the factors, the task and the output folder all live there. When a run starts, the merged protocol and every method parameter it runs with are copied into the results folder, and everything that changes a trial's outcome is hashed.

*Why:* configs drift. If the experiment lived in code or in a file that keeps getting edited, an old result could no longer be tied to what produced it. A frozen copy next to the data makes every results folder self-describing.

*Cost:* the YAML merge is deliberately simple (a child key replaces the parent's whole value), so a protocol has to spell out a list in full to change one entry.

### A results folder belongs to one protocol and one physics

The hash covers the task, every setting that changes a trial, each method's full parameter set and time limit, and the set of layouts and the largest dog count, because the dog start arcs must hold every dog of the largest team and so place the field and goal of every cell on the curve. It leaves out the strategy settings (theta, seed depth, budget) and the flock sizes and smaller dog counts. A folder records its protocol and hash, and refuses to be reused by another protocol or under different physics.

*Why:* a campaign can then grow (more seeds, more flock sizes, intermediate dog counts) and still resume into the same folder, but a change that would make old and new trials incomparable cannot slip in.

*Cost:* changing anything physical, even a small change to one default, needs a new folder. A setting added later is left out of the hash while it sits at its neutral value (the value that reproduces the old behaviour), so the folders written before it keep their hash and can still resume.

### The engine knows nothing about campaigns

The engine runs exactly one trial: one flock, one set of dogs, one seed, until success or the time limit. It doesn't know about grids, seed lists, workers, resume or tables. All of that sits in the campaign layer above it.

*Why:* it keeps the engine small and easy to test on its own, and lets the campaign side change without touching the simulation. A single trial can be pulled out and run by hand for debugging.

### Layers depend only downward

The code has three layers under the tools. The engine runs one trial. Above it sit two layers side by side: the campaign layer, which runs things (protocols, calibration, rounds, and replays of stored trials), and the analysis layer, which reads finished results folders and turns them into decisions and tables and never runs the model; the campaign layer also reads the frontier rules from the analysis layer to decide cells. The command-line tools sit on top; each one parses its arguments, calls the layers below and prints. Imports point only down this order, and no tool imports another tool. These rules are kept by convention; nothing checks them automatically.

*Why:* each piece can then be removed, replaced or extended on its own. Deleting a tool breaks nothing else, the analysis can be rerun without a simulation, and a rule that several tools need (how a results folder is read, how a replay is checked against its stored trial) lives in one place below them.

*Cost:* a helper that two tools share has to move down into a layer, even when it is small.

### Everything that varies is a plugin chosen by name

Sheep behaviour, dog behaviour, the task and every metric are separate plugins, listed under string ids. A method is a named pairing of a sheep model and a dog controller, plus their default parameters. A protocol picks methods and the task by name.

Each plugin owns what is specific to it. A sheep model checks its own parameters and derives the values it needs from them. A task owns its setup, its success rule, the metrics that only make sense for it, the columns it adds to a trial row, and the rules that label a failed trial. The engine, the packaging and the campaign layer call these through the task's interface and never name a task or a method themselves. The catalog of methods is checked when it is loaded, so a method that names a missing plugin or leaves out a setting the engine reads fails before any run starts.

*Why:* the research questions are about swapping one thing at a time: a different dog rule, less information, a harder task. If each is a plugin that carries its own checks and outputs, a new comparison is a new YAML file or one new module, and the rest of the system stays the same between the two arms of the comparison.

*Cost:* plugins share one flat set of settings. Unknown keys are refused when a protocol loads and when a config is built, but the set has no schema, so a plugin can still read a key no one set and fail only when it runs.

### Each setting has one source

Task setup comes only from the protocol and the canonical defaults. Behaviour parameters come only from the method definition. Plugins keep no fallback copies of either, apart from two zero defaults that mean off, and every canonical value carries a note saying where its number comes from.

*Why:* when the same number lives in several places, changing it means finding every copy, and a missed copy changes results without anyone noticing. With one source, a protocol that leaves out a setting fails at the start of the run instead of quietly picking up an old default.

### Lengths follow the measured flock

Goal size, start spread, lost-sheep distance and drive length are multiples of the flock radius, measured per method and flock size by a short calibration: one all-seeing dog drives a compact flock for a fixed time, and the settled radius is the scale. The calibration runs when a campaign first needs a method and flock size, and is stored in the results folder and reused after that. Calibration refuses a flock size whose radius has not settled or depends on its start. It always drives a compact flock with the paper's single all-seeing dog, whatever task or dog settings the protocol runs, so protocols that share a method share its radii and differ only in what they set.

*Why:* fixed lengths make the task easier or harder as N grows for reasons that have nothing to do with the dogs. Tying them to the real flock keeps "every sheep in the goal" meaning the same thing at every N and for every sheep model.

*Cost:* by default each method gets a task sized to its own flock, so methods are compared on equivalent tasks, not on one shared field. That is wrong for two methods that differ only in their dog rule, because the flock one rule settles differs from the other's and so would the goal and the drive. For such a pair, one method can be calibrated with the other's dog, so both run exactly the same task.

Above the largest size at which the flock settles to a radius of its own, a protocol may impose the radius instead, at the density of a calibrated size. Settings that act only through calibration hold for the whole protocol and cannot be swept as factors, because calibration runs once per protocol and a factor level would never reach it.

A task may instead size itself from its own settings and skip calibration. The gather task does: its targets do not flock, so a driven flock has no radius to measure, and the paper it comes from sizes everything by the radius of the disc the agents start on. That radius then stands in for the flock radius in the rows and the generic metrics, which is exact for a uniform disc (the flock radius is defined as the radius of the uniform disc with the flock's RMS spread). The settings such a task owns are hashed only when that task runs, so adding a task leaves every existing folder's hash as it was.

### The field is open and the deadline scales with the task

The papers the sheep and dog rules come from have no boundary, so HerdSim has none: agents may leave the field, and the field rectangle only places the start. A reflecting wall was tried and measured. It rescued trials that would time out, mostly in the hardest cells, so it lowered the dog count for a reason that has nothing to do with the dogs.

The time allowed is a multiple of the drive time, the drive length over the top sheep speed. With unlimited time one dog eventually herds almost any flock, so the number of dogs only has content once time is bounded. Writing the bound as a multiple of the drive time asks the same of every flock size.

*Why:* a result about the number of dogs should come from the dogs, the flock and the deadline, and from nothing else in the setup.

*Cost:* a bounded paddock, a fence or an obstacle is a different question. It needs a fence model that acts on sheep the way a real fence does, and it would be added as its own setting.

### Every added dog has its own work

A dog count is only worth simulating if the extra dog can change something. So the default multi-dog rule gives every dog its own target while another is open: in the base setup dogs start at their own stations spread over the half circle behind the flock, collecting dogs are matched one to one with the farthest outliers by distance, dogs left over drive the core, and driving dogs share out the flock's back edge. A per-tick measure records how often two dogs still end up on top of each other, so a wasted dog shows in the data, not only in a finish time that didn't improve.

*Why:* with identical dogs aimed at one point, a curve over D measures the same trial again at every D, and the campaign pays for it. Giving each dog distinct work makes the D axis a real experimental axis, and the overlap measure separates "the dogs had nothing more to do" from "the dogs got in each other's way".

*Cost:* the team rule is HerdSim's, not the paper's, so multi-dog results are results about this rule. Dogs use each other's positions to share out the work, which is a form of coordination, so the results describe a team that knows where its members are, not independent dogs. Dogs are points by default and may stand on top of each other; a protocol can give them room instead, so that no dog steps closer than a set distance to another, which is how crowding can be tested at all.

A second dog rule is kept on purpose as a baseline. In it every dog aims at the sheep farthest from the goal and nothing shares out the work, so all dogs choose the same sheep and become copies once they meet. Run on the same task, it shows what the D axis looks like when added dogs repeat each other's work, and the overlap measure shows it in the data. A third rule gives every dog the paper's single-dog decision on its own, with no team layer. It has the paper's switch between collecting and driving, which the farthest-sheep baseline lacks, so the two controls together separate what the switch contributes from what the team layer contributes.

### Success is stated, and both readings are kept

The source papers do not agree on when a trial is won: Strombom counts every sheep inside the goal, Kubo states that aim but measures the flock centre and a circle round the flock, and Lama and di Bernardo end the task when the herders are inside the goal and read the share of targets inside at that moment. HerdSim keeps the every-sheep rule as the default and adds a reading in which a share of the sheep, 99 percent for example, is enough. The two readings are separate protocols with their own folders, run on the same grid and the same seeds, so they can be compared cell by cell.

*Why:* with an open goal, the last one or two sheep can decide a trial after the flock has arrived, and the reading used changes the dog count a result reports. Keeping both shows how much of a result belongs to the herding and how much to the definition of success.

*Cost:* every question that has to hold under both readings is asked twice, which doubles the runs.

A third reading asks the flock to stay: the goal counts only after the required share has been inside without a break for a set time. It is off by default, so it changes nothing unless a protocol sets it, and it comes with a step in which the dogs back off, because a dog that only stops still keeps a sheep in flight.

### Conventions are tested

Some setup choices have no rule behind them in the source papers or in field data: where the dogs stand at the start, how roomy the goal is, how fast a dog is compared with a sheep. HerdSim picks a value for each and writes down that it is a convention. The campaign then repeats one small grid with one such choice changed at a time, next to a reference run on the same seeds, under each reading of success, and a conclusion counts only where the reference and the variants agree. Where the source papers offer a second parameter set that was matched to a real flock, it is one of the variants.

*Why:* a result about the number of dogs should not depend on a choice nobody can defend. Testing the choice is cheaper and more honest than arguing for it.

*Cost:* the sensitivity grid is small, so a claim that rests on it is limited to the layouts and flock sizes it covers. It also adds runs.

### Separate random streams, shared seeds

Every trial draws its start layout, its sheep noise and its dog noise from three streams spawned from its seed. Seed i is the same number in every cell of a campaign.

*Why:* a trial's result then depends only on its cell and seed, whichever worker ran it and in whatever order. Because the layout and sheep streams don't depend on the dog count, cells at different D start from the same flocks and see the same sheep draws until the dogs change what the sheep do. That pairs the finish-time comparisons, which is what lets small differences be decided with few seeds.

*Cost:* the dynamics are chaotic, so results are bit-identical only on the same machine with the same library versions. Across machines they agree within a tolerance, which is what the regression tests check.

### Spend seeds where the answer is still open

There is no fixed seed depth. Every cell starts with one batch, and after each round the frontier rules decide which cells get another:

- A cell gets another batch while its reliability is undecided, or while a finish-time comparison that could still move one of the curve's values is undecided. Comparisons that cannot change any value never ask for seeds.
- Where the zone changes between two dog counts that are far apart, the count halfway between is added, so the boundary is found without testing every count.
- When a cell has reached the seed cap still undecided, the dog count between it and its nearest decided neighbour is added, so that the undecided stretch has a decided cell on each side. A cell below the cap is not bracketed yet, because it may still decide on its own.
- A protocol can switch the finish-time comparisons off when only the minimum team is asked for; the values that rest on them are then reported as undecided.
- Above a confirmed saturation, dog counts whose dogs were measured to be copies of each other get no more seeds, because they repeat the cell below them. A dog count that is slower or failing is always kept, because that is a measured harm.

*Why:* most cells always fail, which one batch settles, or always succeed, which a few batches settle; only cells near the threshold need many. Precision only matters near the boundaries, so that's where the budget goes, and the stop rule is "nothing left to decide" instead of a depth fixed before anyone saw the data.

*Cost:* a cell whose true rate sits right at theta stays undecided up to the seed cap. That is by design, but it means some values are reported as a range, from the largest dog count known to be too small to the smallest one decided reliable, or as a lower bound when no larger count is decided yet.

### Survive interruption

Only the parent process writes files, and a folder lock keeps a second campaign out. Each finished trial is appended as one line the moment it returns; a kill can at worst cut the last line, which is dropped on the next start and rerun. Seed counts stay on whole batches across restarts, so a resumed run seeds every cell as an uninterrupted one would. A worker that dies takes its in-flight trials with it, and they are rerun on resume rather than logged as errors.

*Why:* long campaigns get killed, crash or need a reboot. With append-only rows, an interruption costs at most the trials in flight, and a restart just continues.

### An error stops its cell

A trial that raises is logged, its cell gets no further seeds, and that cell is never marked reliable. The run reports which cells had errors.

*Why:* the simulation is deterministic, so an exception will happen again on the same seed. Averaging it away as noise, or counting it as a plain failure, would hide a bug inside a result.

### Failure labels are computed afterwards

A trial stops on success, on the time limit, or when the task itself says the trial is over. The drive task never says so, so its failures run to the limit. The gather task ends a trial once every dog is inside the goal and none senses a target outside it, because its source paper stops there and reads the outcome at that moment; a trial ended that way is a failure unless the success rule holds at the same tick. Why a trial failed (dogs out of range, flock escaped, split, scatter, oscillation, stuck; targets lost, outnumbered) is worked out afterwards from the metric history, by rules the task provides.

*Why:* the stopping rule is fixed per task and the same for every method, so trial lengths are comparable within a task. Failure categories are an interpretation, and they can be refined later without re-running anything.

### Results are evidence; the rules only read them

The campaign layer writes results. The frontier rules never run the simulation, they only read rows. Every generated text file carries a notice saying it is machine-written, so that no one edits a table the next run will overwrite.

Metrics are recorded every tick by default; a protocol may record every k-th tick for a method whose time step is small, where the metrics would otherwise cost more than the model. The stop checks run every tick whatever the stride, and the last tick is always recorded, so outcomes do not depend on it; only the per-tick history and what is read from it (first arrivals, summaries) are coarser.

*Why:* thresholds and comparisons can then be redone in seconds without re-simulating, and the rules can never silently produce new data.

## A trial, conceptually

```mermaid
flowchart LR
    S["sheep react<br/>to flock + dogs"] --> D["dogs decide<br/>and move"]
    D --> M["metrics recorded"]
    M --> T{"task done<br/>or out of time?"}
    T -- no --> S
```

Sheep move first, reacting to where the dogs were. Then the dogs decide and move. By default each dog knows every sheep and every other dog; a protocol can limit each dog to the sheep within a range of it, and say whether dogs share what they see. Metrics are recorded on the resulting state, and the task decides whether it is done.

## A campaign, conceptually

```mermaid
flowchart TB
    PR["protocol"] --> CAL["calibrate flock radius<br/>per method and N"]
    CAL --> EX["expand into D curves and cells"]
    EX --> PL["plan the round:<br/>new cells, open cells, midpoints"]
    PL --> POOL["worker pool<br/>one trial per task"]
    POOL --> PAR["parent appends each row"]
    PAR --> FR["frontier rules"]
    FR --> PL
```

Workers get a small description of one trial, run it and send back its row. Because workers share nothing, the pool can be any size, and a one-worker run gives the same rows, which is how we debug.

## Trade-offs we accepted

| Choice | What we gave up | Why it's acceptable for now |
|--------|----------------|-----------------------------|
| Flat config dict, no schema | Type and presence checks happen per plugin, not in one schema | Keeps plugins independent. Unknown keys are refused at load, and the folder records every parameter that ran |
| Tables rewritten after each round | Write cost grows with campaign size | The append-only trial log is the source of truth; the tables are views of it |
| Layering by convention | Nothing stops a bad import | Small codebase, and the type checker flags import cycles |
| Regression tests use tolerances | Small drifts go unnoticed | Bit-exact comparisons break across machines because the dynamics are chaotic |
| Every metric recorded on every trial | Some compute per tick | Metrics we didn't plan to use have explained results before. Recording them is cheap insurance |
| Calibration always on the drive task | A task with its own flock behaviour can't calibrate its own scale | The flock radius is a property of the sheep model under a driving dog; a task whose agents do not flock sizes itself from its own settings instead, as the gather task does |
| Imposed radius above the calibration edge | Results there are conditional on a chosen density | The model gives no flock size of its own there; the choice is a setting, swept in its own protocols, and the flock's real size is reported beside it |

## How it's meant to grow

The extension points follow the plugin boundaries:

- A new dog rule or sheep model is a new plugin plus a method entry that pairs them.
- A new task is one module with its setup, checks, success rule, metrics, row columns and failure rules, and one entry in the task table.
- A new measurement is a new metric. Every later run picks it up, along with its trial-row summaries.
- A new experiment on existing settings is a new protocol file. Any canonical setting that changes a trial can be swept as a factor, so most new axes need no code.

Some things the current design doesn't handle yet, and would need real changes:

- The world has one circular goal. The drive task's layouts, field sizing and dog start arcs assume a single drive from a start toward that goal, and the gather task's assume a disc round it. Holding the flock in that goal exists; a gate, a pen or several stages still need a more general world and its own start geometry.
- The multi-dog collect/drive controller reads the flock's start position from the task setup, and its dogs share out the work using each other's positions. Roles beyond collect, drive and back off (flanking, holding a gap) would be new jobs in that layer.
- The paper's drive point lies r_a sqrt(N) behind the flock, which passes the sheep's reaction distance near N = 1056; above that the drive rule itself stops working, and only a capped drive point (a labelled variant) drives such flocks.
- The sheep models and dog rules have only been run in their own pairings: the Strombom and Kubo dogs on their own flocks in the drive task, the Lama herders on Lama targets in the gather task. Crossing them (a flocking dog rule on targets that do not flock, or the other way round) needs each rule's assumptions about the other side checked first. The team rule reads a flock start and a collect distance that mean nothing without cohesion, and the herders read distances from the goal centre, which in the drive task is far from the flock.
- Much larger flocks would need the per-dog loops in the controllers vectorised.

## Where to look in the code

| Concern | Location |
|---------|----------|
| Single trial, tick loop | `sim/core/simulation_runner.py` |
| State, world, start layouts | `sim/core/simulation_state.py`, `sim/core/world/` |
| Method catalog and paper parameters | `sim/core/methods.py`, `sim/methods/` (`strombom/`, `kubo/`, `lama/`) |
| The tasks and what they share | `sim/plugins/scenarios/drive_to_goal.py`, `gather.py`; shared `goal.py`, `failures.py`, `team_settings.py` |
| How a trial's config is assembled and checked | `sim/core/config/experiment.py` |
| Plugins | `sim/plugins/{sheep,dogs,scenarios,metrics}/` |
| Canonical defaults and the protocol files | `protocols/configs/` |
| Protocol loading and checks | `services/protocol.py` |
| Groups, cells, run configs | `services/cells.py` |
| Calibration of the flock radius | `services/calibration.py` |
| Adaptive rounds, worker batches, results folder | `services/adaptive.py`, `services/runner.py`, `services/pool.py`, `services/store.py` |
| Trial row, provenance | `protocols/packaging/` |
| Frontier rules | `analysis/frontier.py` |
| Reading a results folder, Markdown tables | `analysis/results.py` |
| D_min of a finished run, and its tables | `analysis/dmin.py`, `analysis/dmin_tables.py` |
| Growth-shape fits of D_min against N | `analysis/growth_fits.py` |
| The gather task read the paper's way, beside D_min | `analysis/herdability.py` |
| Start spread times N, and where failed drives ended | `analysis/dispersion_burden.py` |
| Replays of stored trials, checked against the stored outcome | `services/replay.py` |
| Pressure on the flock in a replay | `analysis/pressure.py`, `cli/diagnostics/pressure_replay.py` |
| Diagnostic replays of the split layout | `cli/diagnostics/split_diagnostic.py` |
| Local estimate of the flock centre on start layouts | `cli/diagnostics/gradient_validation.py` |
| Command-line entry points | `cli/` (see `cli/README.md`) |
| Regression tests | `tests/sim/test_golden.py` |
