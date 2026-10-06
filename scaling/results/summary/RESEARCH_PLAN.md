# What this research is about

## 1. The main question

> If a few dogs have to move a flock of sheep into a goal area, how many dogs do we need when the flock gets larger, or when the sheep start more scattered?

In plain terms: we want a clear number for **how many dogs are enough**, and we want to know whether that number grows with flock size, changes when the sheep start in a different shape, and stays the same if we swap the dog "brain" (controller).

| What we try to measure | Symbol | Everyday meaning |
|------------------------|--------|------------------|
| Fewest dogs that usually work | `D_min` | Smallest dog count that succeeds in at least 90% of repeats |
| Most dogs that still usually work | `D_max` | Highest dog count that still stays at >= 90%. If nothing ever collapses, this number is just **35** (the largest count we ran), not "35 is the true limit" |
| Where more dogs start to hurt | `D_overcrowd` | The place on our dog-count list where too many dogs push the win rate under 90% (see the example below) |
| Best cheap setup that still works | `B*` | Among setups that hit 90%, the one with the least total dog walking |
| Helpful vs wasteful extra dogs | regimes | Extra dogs may only walk more (waste), or may actually make the win rate drop (overcrowding) |

**The dog counts we actually test.** We do not run every integer (5 dogs, 7 dogs, ...). We only run this fixed list:

`1, 2, 3, 4, 6, 10, 15, 20, 25, 35`

"Top of the tested list" / "grid ceiling" = **35**: the last number on that list. If even 35 dogs still wins >= 90%, we write `D_max = 35` and leave `D_overcrowd` empty. That means we never saw a collapse inside the range we ran; it does not prove 36 or 50 dogs would still work, and it does not prove 35 is where things start to break.

**Why stop at 35.** Same cap as the 2025 draft (the "few shepherds" range), and packing many more high-D points blows up the trial budget. That is **not** a forever refusal of larger dog counts: asking what happens at 50+ dogs is a **different question**, outside this map, for a later stage if we still need to hunt an upper collapse.

**Overcrowding and `D_overcrowd` (example + figure).**

- **Waste:** 1 dog already wins about 100% of repeats. 10 dogs also win about 100%, but dogs walk more. The win rate is still fine; only travel cost rises.
- **Overcrowding:** there was a good working band (say 1 through 15 dogs all >= 90%), then when we try still more dogs on the list, the win rate **falls under 90% again**. "Fails the bar" means R (the share of winning repeats) drops.
- **How we set `D_overcrowd`:** we need **two steps in a row on the list** both under 90%. Toy example: 15 dogs OK, then 20 dogs R = 0.80 and 25 dogs R = 0.70. Then `D_overcrowd = 20`, `D_max = 15`. If only 20 dogs dips and 25 dogs is OK again, that is not overcrowding.

![Toy example: waste, D_max, D_overcrowd.](figures/schematics/en/overcrowd_example.svg)

*Green bars: still win >= 90% (working or waste). Red bars: R under 90%. We need two red bars in a row to set D_overcrowd.*

We study the same kind of problem as a 2025 NetLogo draft (dogs vs flock size), but we are stricter: we keep size and starting shape separate, we check other dog controllers, and we do not treat "two numbers move together" as proof of a cause. HerdSim is a **lab simulation**, not a full farm copy.

### What we can already say

| Topic | Current answer (baseline unless noted) |
|-------|----------------------------------------|
| How many dogs as the flock grows (tight start) | Tiny flocks (5 or 10 sheep) need 2 dogs; from 25 sheep up, 1 dog is enough |
| Does a messier start need more dogs? | On the baseline dog rule: no. Still 1 dog. It does take longer and more walking |
| Do extra dogs help once it already works? | Mostly no: time stays flat; dogs just walk more |
| Do other dog rules behave the same? | Only partly. On a tight start, Kubo often matches; FAT and wide starts often fail; some hard Kubo layouts need more dogs |

### What we are **not** answering (yet, or on purpose)

| Not answered | Why |
|--------------|-----|
| "Too many dogs make it fail" as a real upper limit | On the baseline map, from 1 through 35 dogs stays >= 90%. `D_max = 35` only says "still fine at the largest count we ran." Going past 35 is a later-stage question |
| Why overcrowding happens | Needs cases where more dogs actually break success; baseline has none |
| Can better sensing or dog-to-dog talk cut the dog count? | Phase 5 not run yet |
| Can we warn early that a run will fail? | Phase 7 not run yet |
| A rule for real farms or for the NetLogo draft task | We only claim results for this one simulated task |
| Differences finer than our dog-count steps | We only test a fixed list of dog counts |

![Phases covered by current results.](figures/schematics/en/phase_roadmap.svg)

*Phases with solid numbers in the results report today: 1 (flock size), 2 (starting shape), 4 (other dog rules). Phase 3 needs overcrowding cases; Phases 5 and 7 are still open.*

## 2. The detailed questions and where they stand

| ID | In everyday words | Phase / package | Status now |
|----|-------------------|-----------------|------------|
| RQ2 | As the flock gets bigger, how many dogs do we need, and what happens if we add more? | Phase 1 / A | **Done**. Baseline: 1 dog from 25 sheep up; no overcrowding |
| RQ6 | Is there a simple curve for "dogs vs flock size"? | Phase 1 / F | **Checked, weak**: the answer is almost flat, so there is little curve to fit |
| RQ1 | If flock size is fixed, does a different start shape change how many dogs we need? | Phase 2 / B | **Done**. Baseline: still 1 dog; time and walking change a lot |
| RQ3 | When more dogs hurt, do interference or flock breakup look different? | Phase 3 / C | **Skipped / unclear**: baseline never shows "more dogs hurt" |
| RQ4 | Do the same answers show up with other dog rules (Kubo, FAT)? | Phase 4 / D | **Partial**: tight starts often match for Strombom/Kubo; wide and FAT often fail; Kubo outlier_rich at 200 sheep shifts to D_min = 20 (200 seeds; bootstrap [2, 20]) |
| RQ5 | Can better sensing or communication let us use fewer dogs? | Phase 5 / E | **Not run** |
| RQ7 | Can flock signals warn us before a run times out? | Phase 7 / G | **Not run** |

The smallest core we wanted was: freeze the rules, answer size, answer start shape, then explain overcrowding. Overcrowding never appeared on the baseline map, so that middle step could not run as planned. Checking other dog rules (Phase 4) is done for the required methods.

## 3. How we decide "it worked" and "how many dogs"

One **run** is one simulation with its own random seed. One **cell** is one fixed recipe (flock size, dog count, start shape, dog rule) repeated many times.

![Reliability is a fraction of seeds.](figures/schematics/en/metrics_reliability.svg)

*We call R the share of repeats that finish before the deadline. For official answers we usually require R at least 0.90 (90%).*

| Word | Meaning here |
|------|----------------|
| Success | Every sheep is inside the goal circle before the deadline |
| R | How often that happens across repeats |
| theta | The bar we use for "reliable enough" (0.90 by default) |
| D_min | Fewest dogs on our list that clear that bar |
| B* | Among setups that clear the bar, the one with the least dog walking |
| Wasteful | Already reliable (R >= 0.90), but dogs walk much more than the cheap good setup |
| Overcrowding | After a working band, R falls under 0.90 for two steps in a row on the list (see section 1) |

![Frontier labels on an R(D) curve.](figures/schematics/en/design_frontier.svg)

*Picture of fewest dogs, overcrowding, most dogs still OK, and the cheap good point. Steps on the axis are values from the tested list, not every integer.*

For time and walking distance, see also [SUMMARY_REPORT.html](SUMMARY_REPORT.html) Appendix B (ticks, path, interference).

![Ticks measure time; path measures dog travel.](figures/schematics/en/metrics_tick_path.svg)

## 4. The fixed task and field

Every official comparison uses the **same** task rules, so size, start shape, and dog-rule checks stay fair.

| Setting | Value |
|---------|-------|
| Task | Drive every sheep into a goal circle |
| Field | 500 by 500; flock starts at the centre; goal centre at (370, 250) |
| How far to the goal | 120 units (same for every flock size) |
| Goal size | Grows with flock size: `15 * sqrt(N/50)` (15 at 50 sheep; about 42 at 400) |
| Deadline | 10,000 time steps (a longer 20,000 only if overcrowding shows up) |
| Main dog rule | `strombom_multi` |
| Other dog rules we check | `kubo`, `fat` |
| Flock sizes we test | 5, 10, 25, 50, 75, 100, 150, 200, 300, 400 |
| Dog counts we test | 1, 2, 3, 4, 6, 10, 15, 20, 25, 35 |
| Start-shape check sizes | 50, 100, 200 sheep on four layouts |

**How to picture the field.** Sheep start outside the goal, inside the field. The clickable app still has its own smaller corner-goal world; the scaling study does **not** use that for claims. Success means every sheep is inside the scaling goal circle.

**Two distances that are easy to mix up (Strombom).** The study uses two different lengths. They answer different questions.

| Length | Formula (typical) | Question it answers |
|--------|-------------------|---------------------|
| Goal circle (success) | `15 * sqrt(N/50)` (15 at 50 sheep; about 42 at 400) | Did every sheep enter our win region before the deadline? |
| Strombom gather/drive switch | `f(N) = r_a * N^(2/3)` (about 27 at 50 sheep; about 109 at 400, with `r_a = 2`) | Is the flock tight enough for this dog rule to stop gathering and start pushing? |

`f(N)` is an internal rule of the Strombom dog "brain." It is **not** the size of the pen. The goal circle is always smaller. We keep that on purpose: if we opened the pen to match `f(N)`, large flocks would get an easier win criterion tied to one controller, and every method would inherit that bias. So if Strombom fails on this task, we read "did not get every sheep into the smaller goal in time," **not** "the sheep could not physically fit in the pen."

![Compact start on the scaling field.](figures/schematics/en/arena_compact.svg)

*Dogs start behind the flock, facing the goal. Not the draft paper's corner start.*

![Goal radius grows with sqrt(N).](figures/schematics/en/goal_radius.svg)

![Field, drive length, and timeout budget.](figures/schematics/en/design_timeout.svg)

![N and D grids denser near likely frontiers.](figures/schematics/en/design_nd_grids.svg)

### Why we chose these numbers

Each row: what we locked in, what we turned down, and why. These are design reasons from the protocol plan, not numbers fitted after seeing the results.

#### Goal size and distance

| What we chose | What we turned down | Why |
|---------------|---------------------|-----|
| Goal radius 15 at 50 sheep | A tight packed radius (~8), or a huge "pasture" radius (30) | 15 matches the app's usual goal. Too small jams the flock. Too big makes the job easier and can fake a lower dog need |
| Grow radius with `sqrt(N/50)` | Same radius for every flock size; or use Strombom's gather distance as the pen | Keeps space per sheep roughly steady. A fixed radius jams large flocks. Using one dog rule's gather distance as the pen would favour large flocks for every method |
| Drive distance 120 | 80 or 200 | At sheep speed 1, a straight walk takes 120 steps. Shorter sits inside a wide start. Longer pushes the far side of the goal into the wall |

#### Field

| What we chose | What we turned down | Why |
|---------------|---------------------|-----|
| Field 500 x 500, goal at (370, 250) | App field 150; field 400; field 1000 | Big enough for wide and straggler starts with margin. 150 is too small. 400 is tight. 1000 is mostly empty space. Goal on the midline keeps top and bottom margins even |

#### Which flock sizes and dog counts

| What we chose | What we turned down | Why |
|---------------|---------------------|-----|
| Smallest flock 5 (keep 5 and 10) | Start at 20, or at 1 | Below 5 there is barely a "flock." Tiny flocks are interesting, not noise |
| Ten flock sizes, denser near 100; skip 250 and 350 | Every 50 from 50 to 400 | The draft expected a change near 100. Extra sizes each need a full dog sweep, so we dropped 250 and 350 |
| Dog steps 1 to 4, then bigger jumps; stop at 35 | Every integer up to 35 | The fewest-dogs answer usually sits at 1 to 4. Later we care whether a **big** jump helps or hurts. Testing every integer would make the cheap map about three times more expensive |

#### How sure, how long, how many repeats

| What we chose | What we turned down | Why |
|---------------|---------------------|-----|
| 90% success bar | 50% as the main bar; 99% at 100 repeats | Same "usually works" bar as the draft. 50% is too loose for "enough dogs." 99% at 100 repeats is harsh on stable cells |
| Deadline 10,000 steps | Default scenario 3,000 | Long enough that "timed out" means the dogs lost control, not that a slow success was cut off |
| Cheap map 30 repeats; careful map 100; raise to 200 if unsure | Only 10; or 100 everywhere | 30 is enough to spot broken vs solid cells. 100 is for the important edges. 200 is for when the fewest-dogs answer is still blurry |
| Resample 1,000 times for uncertainty | Only 100 resamples | Gives a stabler uncertainty band on the fewest-dogs answer |

#### Start shapes and related cuts

| What we chose | What we turned down | Why |
|---------------|---------------------|-----|
| Tight vs wide spreads that still fit the field | An ultra-wide start that spills out | Wide should be clearly more spread, but still on the field |
| Split into 2 groups if under 12 sheep, else 3; gap at least 10 | Always 3 tiny groups; tiny gaps | Tiny "groups" are not real sub-flocks. Gaps must stay visibly separate |
| About 20% stragglers | 50% or 5% | 50% is basically a second flock; 5% is not even one sheep at size 5 |
| "Wasteful" if walking is 20% above the cheap good setup | Only 10%, or only 50% | 10% is noise; 50% only catches extremes |

#### Which sizes for the start-shape check, and where we spend careful repeats

| What we chose | What we turned down | Why |
|---------------|---------------------|-----|
| Start-shape check at 50, 100, 200 sheep | Also 5, 10, 25 first; or jump to 300, 400 first | Those middle sizes already need only 1 dog on a tight start. They are large enough for split and straggler layouts to mean something. Tiny sizes are already covered in Phase 1 |
| Careful repeats only near the fewest-dogs edge | One cell only; or careful repeats on every cell | One thin cell can misplace the edge. Careful repeats everywhere waste budget on cells that never change the answer |
| Overcrowding needs two bad steps in a row | One bad blip; or "the whole upper grid must stay bad" | One blip can be noise. Demanding the whole upper grid stay bad can miss a real drop that later recovers |

#### Planned later (not run yet)

| Choice | Why (when Phases 5 / 7 run) |
|--------|----------------------------|
| Look at only the first 100 time steps for early predictors | Shorter than a straight drive, so an easy win is not already baked into the features |
| Early-warning checks from step 1,000 to 8,000 | Start after the layout settles; stop while there is still room before the deadline |
| Information steps relative to each dog rule's sensing range | Same ladder for different dog rules |

The machine-readable settings live in `scaling/configs/canonical_grid.yaml`. Number tables are also in SUMMARY_REPORT Appendix A.

## 5. What "start shape" means

Here we ask: if flock size is the same, does a different sheep layout at the start change how many dogs we need?

| Layout | What it looks like | Quick check |
|--------|--------------------|-------------|
| compact | Tight cloud | Tighter than wide |
| wide | Same centre, much more spread | More spread than compact |
| split | Two or three separate clumps | More broken apart than compact |
| outlier_rich | Tight core plus about 20% far sheep | More stragglers than compact |

If a random draw would put a sheep off the field or inside the goal, we redraw it (we do not glue it to the wall).

![Four starting layouts.](figures/schematics/en/four_layouts.svg)

*On the baseline dog rule, fewest dogs stayed at 1 for all of these. Time and walking did not.*

## 6. How we spend simulation budget

We do **not** run every recipe at full careful depth. Cheap repeats map the whole grid; careful repeats go only near the edges that decide the answer.

![Staging pipeline.](figures/schematics/en/pipeline.svg)

| Stage | Typical repeats | OK to quote as a solid answer? |
|-------|-----------------|--------------------------------|
| Smoke check | tiny | No |
| Cheap map (scout) | 30 on every cell | No (for planning only) |
| Careful map (claim) | 100 on chosen edges | Yes |
| Extra care | 200 if the fewest-dogs answer is still blurry | Yes, for that edge |
| Long deadline (T1) | 100 at 20,000 steps on overcrowding dog counts | Yes, when it runs |

![Scout covers the full grid cheaply.](figures/schematics/en/scout_grid.svg)

![Claim reseeds a window around the frontier.](figures/schematics/en/claim_window.svg)

Merge rule: if a cell has careful repeats, we analyse those only. Other cells keep the cheap repeats. We also resample within each dog count (1,000 times) to see how stable the fewest-dogs answer is.

## 7. Other dog rules (transfer)

Transfer asks: which findings are about **this herding task**, and which are about **one dog rule**?

![Transfer idea.](figures/schematics/en/transfer_sketch.svg)

We compare three dog rules. Same task, same field, same win rule. Only the dog "brain" changes.

**`strombom_multi` (baseline).** Dogs share one mode for the whole team: **gather** stragglers, or **drive** the flock toward the goal. The switch uses `f(N)` from section 4 (wider than our goal circle; we do not enlarge the goal to match it). With several dogs, HerdSim assigns different outliers in gather mode and spaces dogs behind the flock in drive mode so they do not all stack on one point. Sheep use the Strombom 2014 rules.

**`kubo`.** No gather/drive switch. Sheep and dogs move from continuous force sums inside a sensing radius (`dt` integration, not one fixed step per tick like Strombom). Each dog presses the in-range sheep that is **farthest from the goal**; dog-dog repulsion fans the dogs into an arc. Sheep are Kubo sheep, not Strombom sheep.

**`fat`.** Also no gather/drive switch. Sheep stay Strombom 2014. Each dog independently presses the sheep **farthest from itself** (not from the goal, not from the flock centre), then stands off behind that sheep toward the goal. In Phases 1, 2, and 4 here, every dog sees the full flock (`obs_mode=global`).

| Dog rule | Role in this study |
|----------|--------------------|
| `strombom_multi` | Main baseline |
| `kubo` | Force-based check |
| `fat` | Simple "press the farthest sheep from me" check |

![Baseline gather / drive.](figures/schematics/en/alg_strombom_multi.svg)

![Kubo force-based herding.](figures/schematics/en/alg_kubo.svg)

![FAT farthest-from-dog targeting.](figures/schematics/en/alg_fat.svg)

![What "farthest" means for each rule.](figures/schematics/en/alg_farthest_compare.svg)

*The word "farthest" points at three different sheep depending on the dog rule.*

We label each comparison **shared** (same answer), **shifted** (different dog count), or **absent** (one side never reaches 90% success, or never shows overcrowding). Today: tight starts often match for Strombom and Kubo; FAT and wide starts often fail; Kubo outlier_rich at N = 200 shifts to D_min = 20 at 200 seeds (bootstrap [2, 20]; no overcrowding). Numbers: [SUMMARY_REPORT.html](SUMMARY_REPORT.html) section 5; window snapshot `../phase4/kubo_structure/claim/outlier_rich_n200_window.json`.

## 8. What we are allowed to claim

A "claim" is a yes/no scientific statement with a fixed rule for support. We only update the verdict after careful-grade evidence.

| Claim | Topic in plain words | Verdict now |
|-------|----------------------|-------------|
| C1a | Start shape changes fewest dogs by at least one step on our list | REJECTED (baseline) |
| C1b | Flock state predicts better than size+dogs when fewest dogs moves | INCONCLUSIVE |
| C2a | Baseline shows overcrowding at 90% success | REJECTED |
| C2b | Overcrowding still shows at a longer deadline | SKIPPED |
| C3 | Overcrowding cells look different on interference / breakup | INCONCLUSIVE |
| C4 | Fewest dogs or overcrowding is shared across the three dog rules | SUPPORTED (partial) |
| C5a / C5b | Better information cuts fewest dogs | UNEVALUATED |
| C6a | A simple power curve loses to a broken-line or per-layout fit | EVALUATED (weak fit) |
| C6b | Growth of dogs with flock size is slower than linear (in a stated band) | UNEVALUATED |
| C7a / C7b | Early warning quality and lead time | UNEVALUATED |

![Claims scorecard schematic.](figures/schematics/en/claims_scorecard.svg)

*Colours match the results scorecard.*

## 9. What this budget can and cannot support

Rough core cost: baseline size map plus start-shape map is on the order of 20,000 simulations; each other dog rule repeats both maps.

| This budget can support | It cannot support by itself |
|-------------------------|-----------------------------|
| Solid fewest-dogs answers and waste/overcrowd labels on our grids | A law for every dog rule from the baseline alone |
| Start-shape checks at 50, 100, 200 sheep | A universal farm rule or NetLogo-task rule |
| Mechanism checks **when** we have contrast cells | Dog-count differences finer than our list steps |
| Side-by-side tables for the required dog rules | "Interference caused failure" from correlation alone |

### Limits we keep in view

| Limit | How we treat it |
|-------|-----------------|
| One task only | We change dog rules in Phase 4; a second task is optional later |
| Strombom gather distance wider than the goal | Section 4 table; failure is not read as packing |
| Discrete time steps, sheep speed 1 | Results are at this resolution |
| Simulated dog rules | Claims stay inside the simulation |
| Soft fewest-dogs edge | If uncertainty spans more than one dog step, we raise that edge to 200 repeats |
