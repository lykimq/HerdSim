# Instruments

An instrument is a ready-made herding setup you pick in Simulate, Compare, or Experiments. Each one pairs a sheep behaviour with a dog (or shepherd) strategy, plus sensible defaults for counts and parameters.

You do not need to assemble plugins by hand. Choose an instrument, pick a scenario, then run. Open a named page in this Guide section when you want the story behind one instrument, its rules, and its limits.

## How to use them

1. In the left setup panel, open **Instrument** and pick a name (for example Strombom 2014 or Kubo 2022).
2. Choose a **Scenario** such as Drive to Goal or Obstacle Course.
3. Leave **Settings source** on Instrument when you want the paper-style defaults, or switch to Custom to change counts and factors.
4. Initialize a run and watch how that instrument gathers and drives the flock.

The same instrument list appears in Compare and Experiments, so you can put two setups side by side or run batch trials under the same seeds.

## Main instruments

- **Strombom 2014:** Classic Collect / Drive with one shepherd. Good starting point for open-field Drive to Goal.
- **Strombom Multi-Dog:** Same sheep rules, several dogs that share Collect and Drive work instead of stacking on one spot.
- **Strombom Noise:** Same as Strombom 2014, but noisier defaults. Useful when you want to see how brittle a run is.
- **V-Formation:** Multi-dog Drive on a V-shaped arc behind the flock.
- **Heterogeneous:** Some sheep respond weakly to the shepherd, so the flock is harder to finish.
- **Obstacle-Aware:** Drive bends around obstacles or through a gate instead of aiming straight through walls.
- **Kubo 2022:** Force-based multi-dog herding without an explicit Collect / Drive switch.
- **Flocking Dog:** Smaller flocks with neighbour-based sheep motion and a dog that slows when it is already inside the group.
- **FAT:** Each dog aims at the farthest sheep it can see. Handy for limited sensing studies.
- **Communication-Free:** Each dog decides from its own view only, with no shared targets.
- **Adaptive:** Picks collect, drive, recover, or lead from the current flock state.

Use the pages under Instruments in the left Guide list for the full write-up of each one.

## What you can change without switching instrument

You can keep the same instrument and still vary:

- How much each dog can see (global view, local range, noisy bearings, and similar options)
- How stubborn a fraction of the flock is
- Whether a shepherd fails mid-run
- Whether the goal stays fixed or moves
- Sheep and dog counts, and the random seed

Those knobs live under experimental factors and Custom settings. Changing them does not replace the instrument; it changes the conditions around it.

## Where to go next

- Start with **Strombom 2014** if you are new to the app.
- Use **Kubo 2022** or **Flocking Dog** when you want a different herding style to compare.
- Open **Scenarios** and **Metrics** in this Guide when you are ready to judge success and read the live numbers.
- See **Comparison Framework** for fair side-by-side experiments across instruments.
