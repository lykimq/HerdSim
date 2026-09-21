# Reference: sheep-scaling paper (2025 draft)

Source PDF: [../../docs/papers/sheep-scaling_paper2025.pdf](../../docs/papers/sheep-scaling_paper2025.pdf)

Title: *Collective Nudging that Scales. How many dogs do I need to herd sheep?*
Status: draft (~2025); placeholder author lines in the PDF.
Platform in that work: NetLogo 7.0.3 ABM (not HerdSim).

This note is a **reference summary** of what that draft did (methods, experiment, results). It is not a substitute for the PDF. Use it when comparing HerdSim scaling protocol choices to prior work.

HerdSim program: [herdsim_research_program.md](herdsim_research_program.md)
HerdSim how: [main_scaling_plan.md](main_scaling_plan.md)

---

## Purpose and questions

**Claimed gap.** Many collective-nudging papers treat scale as an application quality issue. A general empirical study of how shepherd count must grow with flock size (and why) was missing.

**Questions (paper RQ1 to RQ3)**

1. How does the viable dog interval `[Dmin, Dmax]` for the herding task vary with sheep count N?
2. Can required dog count be correlated with a **flock macro-measure** (spread) rather than only micro behaviours?
3. How can sheep keep global flock coherence (GCM attraction) from **local** information only?

**Contributions claimed**

1. Herding scalability study (D vs N).
2. Link scaling to mean-spread.
3. Sheep model extension: density-gradient proxy for GCM (local sectors).

---

## Methods (model)

### Task (three phases)

Dogs must:

1. **Collect** dispersed sheep into a compact flock toward a containment zone.
2. **Hold** the flock in that zone for **800 ticks** (with escape limits).
3. **Exit**: drive the flock through a pen gate.

Success: all sheep through the gate within **10,000 ticks**. Otherwise fail.

### World and agents

| Item | Value |
|------|-------|
| World | Non-toroidal grid **101 x 71** patches |
| Containment | Circle at centre; radius `rc = clamp(2.5 * sqrt(N), 23, 27)` |
| Exit gate | 6 patches, middle of right wall |
| Sheep modes | grazing / fleeing |
| Dog modes | targeting / driving / patrolling |
| Sheep neighbours | topological `ntopo = 7` |
| Sheep vision | ~360 deg (assumed); range 30 patches |
| Density gradient | 8 angular sectors of 45 deg; move toward densest |

**Assumptions (high level).** Dogs see flock GCM and outliers; sheep are local only; homogeneous agents; no fatigue; uniform world (no obstacles/relief); dogs self-partition sectors by id.

**Sheep forces.** Weighted sum (repulsion, local cohesion, wall, persistence/alignment when grazing; dog avoidance + global density cohesion when fleeing; gate pull in exit). Max turn 40 deg/tick. Full parameter table: PDF Table A1.

**Dogs.** Collect-or-drive extended to multi-dog: target lost sheep behind relative to GCM; drive in 90 deg arc behind flock; patrol containment sectors during hold. Inter-dog repulsion, sheep/wall avoidance, speed modulation, stuck detection.

**Mean-spread** (paper eq. 1): time-averaged variance of sheep distances to GCM. Compact often `S_bar ≈ 15` or lower; sparse often `S_bar ≈ 50` or higher.

This is **not** claimed as a realistic farm model; it is a fixed flocking + shepherding scheme for measuring scaling.

---

## Experiment design

### Factors (full factorial)

| Factor | Levels |
|--------|--------|
| D | `{1, 2, 3, 4, 6, 10, 15, 20, 25, 35}` |
| N | `{5, 10, 25, 50, 100, 150, 200, 250, 300, 350, 400}` |

- Conditions: **10 x 11 = 110**
- Runs per cell: **100** (flat; no scout/claim split)
- Total simulations: **11,000**
- Timeout: **10,000** ticks
- Other parameters: fixed (Table A1)

### Metrics (per run)

- Success (boolean)
- Ticks to success (if success)
- Phase at end
- Sheep in zone / holding time
- Mean-spread `S_bar`
- Total dog path distance
- Lost sheep / enclosed sheep

### Frontier definitions (Fig. 4 caption)

For SR >= 90%:

| Quantity | Definition |
|----------|------------|
| Dmin | Smallest D with SR >= 90% |
| Dovercrowd | Smallest D > Dmin where SR starts decreasing |
| Dmax | Smallest D > Dmin with SR < 90% (only where observed; else ceiling D=35) |

### Statistics used

- Spearman correlations over the **110 condition aggregates** (`scipy.stats.spearmanr`)
- Exhaustive threshold search for classifiers predicting SR bands
- **No** binomial CI on SR; **no** bootstrap on Dmin

### Extra analyses (not the main grid)

- Failure breakdown by phase and by `S_bar` (Table VIII)
- Sensitivity: lower sheep repulsion `Rrep` 3.0 -> 2.5 on four hard cells (Table IX)
- Density-gradient accuracy vs true GCM direction (~80M observations; Table X)

---

## Results (what they reported)

### Success-rate surface (Table III, % of 100 runs)

Bands in the paper: >= 90% / 15-90% / < 15%.

Selected facts:

- **D=1:** near-perfect SR up to N=100, then collapse at N=150 (SR ~1%). Breakpoint ~100 sheep per dog in this setup.
- Larger D shifts the reliable region to larger N, with **wider transition zones**.
- **Diminishing returns:** e.g. 1 dog for N=100 (SR>90%); 3 dogs for N=150; ~20 dogs for N=200; 35 dogs for N=400 at SR>90%.
- **Overcrowding:** e.g. N=10, D>=20 worse than fewer dogs.

### Viable range at SR >= 90% (Table A3)

| N | Dmin | Dmax | Max SR |
|---|------|------|--------|
| 5 | 1 | not reached | 100% |
| 10 | 1 | 15 | 100% |
| 25 | 1 | 25 | 100% |
| 50 | 1 | 25 | 100% |
| 100 | 1 | not reached | 100% |
| 150 | 3 | not reached | 99% |
| 200 | 20 | 35 | 94% |
| 250 | 25 | not reached | 93% |
| 300 | 20 | not reached | 93% |
| 350 | 35 | not reached | 91% |
| 400 | 35 | not reached | 91% |

"Not reached" means D=35 still had SR >= 90%, so true Dmax (if any) is above the experimental ceiling.

### Spread vs success

- High `S_bar` (>= 30) associated with losing control / failure.
- For fixed N, adding dogs often lowers `S_bar` and raises SR until overcrowding reverses that.
- Spearman over 110 cells: `S_bar` vs SR, **rho = -0.701**.
- Best composite: `S_bar * N`, **rho = -0.828** (then `S_bar * sqrt(N)`, -0.819). Predictors that fold in D do worse (D already affects `S_bar`).

Classifier example (Appendix): threshold on `S_bar * N` for predicting SR >= 90% (confusion matrix Table A2).

### Time and effort

- Mean ticks to success rise with N and fall with D on successful runs (Table VI / Fig. 6); near timeout at breakpoints.
- Total dog distance rises with D and saturates near breakpoints (Table VII).
- Small flocks can also be slow (less compression / overcrowding).

### Failures (3,089 / 11,000)

| Slice | Count | Mostly stall in |
|-------|-------|-----------------|
| `S_bar` > 25 (no control) | 2,161 | Collect 97% |
| `S_bar` <= 25 (some control) | 928 | Collect 74%; hold 9%; exit 18% |
| All failures | 3,089 | Collect 90% |

Interpretation in paper: most failures never compress the flock; a minority might need more than 10,000 ticks.

### Sensitivity (Table IX)

Reducing `Rrep` 3.0 -> 2.5 (tighter flocking) sharply raises SR on hard cells, e.g. (D=6, N=400) 0% -> 92%; (D=3, N=250) 5% -> 100%. Used to argue that micro params that change `S_bar` move the same macro story.

### Density gradient (RQ3)

For N >= 100, mean angular error to true GCM ~18-22 deg; correct sector often >= 65%; correct or adjacent >= 87%. Worse for very small or very large N (sparse signal / vision limits).

---

## Discussion takeaways (paper)

- Scaling of Dmin with N is **quasi-monotonic, non-linear**, with slope changing by N band.
- Extra dogs help then **saturate / overcrowding** for fixed N.
- **Spread** is a useful macro correlate of difficulty; `S_bar * N` improves prediction vs `S_bar` alone.
- Efficacy of a given nudging setup is bounded to a **scale interval** (case by case).
- Limits: one flocking/shepherding scheme; homogeneous agents; no obstacles; NetLogo ABM; D ceiling 35; no uncertainty on Dmin.

---

## How this maps to HerdSim (quick compare)

| Item | 2025 draft | HerdSim scaling freeze (`scaling_v1`) |
|------|------------|--------------------------------------|
| Engine | NetLogo | HerdSim |
| Task | Collect + hold 800 + gate exit | `drive_to_goal` (no hold/gate phase stack) |
| D grid | same set to 35 | same |
| N grid | includes 250, 350; no 75 | includes 75; drops 250, 350 |
| Seeds | 100 every cell | scout 30; claim 100 on boundaries |
| Reliability | SR >= 90% | theta = 0.90 (also 0.50, 0.70) |
| Timeout | 10,000 | T0 = 10,000; T1 = 20,000 for hard-ceiling |
| Dmin uncertainty | none | plan: bootstrap CI (implement when claiming) |
| Methods | one NetLogo collect/drive family | baseline `strombom_multi` + transfer set |
| Structure | emergent spread; correlate `S_bar` | also **manipulate** X0 families (RQ1) |
| Mechanism | mostly correlate + failure phase | I_dir / coverage tests (RQ3) |

Reuse from the draft: reliability band, D grid shape, timeout scale, mean-spread idea, vocabulary (Dmin / overcrowding / viable range). Do **not** expect numerical Dmin(N) to copy across engines or tasks.

---

## Pointers in-repo

- Protocol comments that cite the draft: `scaling/configs/canonical_grid.yaml`
- Mean-spread metric note: `plugins/metrics/mean_spread.py`
- Related themes (not this protocol dump): `scaling/docs/related_work.md`
