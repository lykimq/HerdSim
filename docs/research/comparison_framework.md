# Compare

This page covers the **Compare** tab only: live side-by-side runs of Setup A and Setup B. For batch tables, charts, and CSV/JSON exports, use the **Experiments** page in this Guide.

## What Compare is for

Use Compare when you want to **watch** two instruments at the same time, scrub both timelines, and read live metric deltas (A minus B).

It answers questions like: on this seed and layout, does method A gather faster, stay tighter, or reach the goal sooner than method B?

It does not replace Experiments. One matched pair you watch is insight. Many seeds you export is evidence.

## Fair compare (default)

Fair compare keeps the two sides matched so differences are mostly about the instruments.

**Shared bar (top):**

- Scenario
- Seed
- Sheep count
- Dog count

**On each side (Setup A / Setup B):**

- Choose the **instrument** (and display options)
- Shared fields and per-side Initialize / play controls stay inactive or hidden so you do not desync the runs

**Run both sides together:**

1. Set the shared scenario, seed, and counts.
2. Pick an instrument on A and on B.
3. Click **Init Both** (agents are placed; nothing plays yet).
4. Click **Play Both** to run. Use **Pause Both** or **Reset Both** as needed.

If the shared counts or seed change after init, initialize again so both sides stay aligned.

## Independent mode

Independent unlocks a full setup on each side: its own scenario, seed, counts, and Initialize / play controls.

Use it to explore freely (for example different scenarios, or one side as a sandbox). Do not treat Independent runs as a matched fair trial when you write results down.

Switching back to Fair compare restores the shared bar and locks the duplicate side controls again.

## Live deltas

The header shows **Live deltas (A - B)** on key metrics while both sides run.

- Positive values favor side A.
- Time to goal stays unavailable until both sides have a finished outcome to compare.
- Shepherd path needs care across instrument families. Kubo advances with a time step (`dt`); Strombom-style controllers move by displacement per tick. Path length is not always directly comparable.

Scrub each side when paused to inspect how the flocks diverged.

## Reading a fair live compare

While you watch, look for:

- Who reaches the goal (or gets closer) first on this seed
- Whether one flock stays more cohesive or fragments more
- Whether one side spends longer collecting outliers before driving
- How the dogs move (stacking, spreading, stalling)

Remember this is one seed unless you change the shared seed and run again. For rates and spreads across many seeds, open the **Experiments** tab.

## Paper counts vs locked counts

On Fair compare, sheep and dog counts come from the shared bar, so both sides see the same N and M. That is the live fair setup.

If you only want to see each method with its own published defaults, use **Independent** and set counts per side, or open Simulate. Say clearly that those runs are not locked-count fair compares.

## Quick checklist (Compare tab)

| Goal | Mode | What to do |
|------|------|------------|
| Matched live A/B | Fair compare | Shared scenario, seed, N, M; instruments on A and B; Init Both, Play Both |
| Free exploration | Independent | Full setup per side |
| Many seeds / export | (leave Compare) | Use the Experiments tab |

## Related pages

- Overview: purpose, features, and researcher Q&A
- Experiments: batch ranking, factor grids, charts, and exports
- Metrics: what each live score means
- Scenarios: task layouts and success rules
- Instruments: what each method package contains
