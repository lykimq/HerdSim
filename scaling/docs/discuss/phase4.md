# Phase 4: Controller Generality & Transfer

## Question
Do the scaling frontiers observed on the baseline `strombom_multi` controller generalize to other canonical shepherding algorithms (`kubo` and `fat`) across both flock size and initial structure?

## Results Summary
- **Tested**: `kubo` and `fat` across 10 flock sizes (N in [5, 400]) and 4 layout families (N in {50, 100, 200}) on D in [1, 35].
- Sources: `scaling/results/phase4/package_d/size/`, `scaling/results/phase4/package_d/structure/frontier_by_method_layout.csv`, `phase4/kubo_structure/claim/outlier_rich_n200_window.json`, and the per-method claim packages under `phase4/{kubo,fat}_{size,structure}/claim/`.

### Size map (compact start)

- **Kubo**:
  - For N >= 25 through 400, D_min = 1 is **shared** with the baseline.
  - At small sizes: N = 5 has D_min = 3 (R = 0.77 at D = 1, 0.71 at D = 2, 0.97 at D = 6); N = 10 has D_min = 1.
  - No overcrowding on the compact size map.
- **FAT** (farthest-agent targeting on Strombom sheep; not a potential-field controller):
  - Works on small flocks (N <= 10 with D_min = 1).
  - Hard failure for N >= 25 through 400: never reaches theta = 0.90 for any D up to 35.
  - Extra dogs do not help; failures are mostly oscillation and stuck under global observation.

```text
Flock Size N      Strombom (Baseline)   Kubo             FAT
N = 5             D_min = 2             D_min = 3        D_min = 1
N = 10            D_min = 2             D_min = 1        D_min = 1
N = 25 .. 400     D_min = 1             D_min = 1        Hard Failure (R < 0.90)
Overcrowding      None                  None (size map)  None
```

### Structure map (N in {50, 100, 200})

| Layout | Strombom | Kubo | FAT |
|--------|----------|------|-----|
| compact | D_min = 1 | D_min = 1 | hard failure (best R about 0.3 to 0.5) |
| split | D_min = 1 | D_min = 1 | hard failure |
| outlier_rich | D_min = 1 | D_min = 1 at N = 50, 100; at N = 200, D_min = 20 (200 seeds; D = 1 to 15 below 0.90) | hard failure (near 0) |
| wide | D_min = 1 | **hard failure at every N** (best R about 0.42 to 0.54) | hard failure (R = 0) |

- Kubo on **wide** never reaches R >= 0.90: timeouts and scatter; more dogs raise R slowly but stay below the bar.
- Kubo on **outlier_rich N = 200**: D = 1 to 15 stay below theta at 200 seeds (R about 0.75 to 0.89). D_min = 20 at 200 seeds (R = 0.935); D = 25 also at 200 seeds (R = 0.910). Bootstrap interval [2, 20]. No overcrowding. Snapshot: `kubo_structure/claim/outlier_rich_n200_window.json` (claim README: `kubo_structure/claim/README.md`).
- FAT fails on every structure cell at these N.

## Claims Verdict
- **C4 (Shared D_min / Overcrowding)**: **Supported (partial)**.
  - Shared on the compact size map for N >= 25 (Strombom and Kubo both D_min = 1; no overcrowding).
  - Structure transfer is **shifted / absent** for Kubo: wide has no D_min; outlier_rich N = 200 shifts to D_min = 20 at 200 seeds (bootstrap [2, 20]).
  - FAT does not transfer (absent D_min for N >= 25 on size; hard failure on structure).

## Discussion
Shepherding scaling on this task depends on controller architecture **and** starting structure. Reactive collect-and-drive (Strombom) keeps D_min = 1 across the four layouts; Kubo matches that on compact and split starts but fails to collect wide flocks and needs more dogs (or fails the bar) on large outlier_rich flocks. FAT (local farthest-agent targeting) breaks down for N >= 25 regardless of dog count under the Phase 4 observation setting (`obs_mode=global`).

Controller architecture matters more than shepherd count once the method cannot collect or finish the drive. Size-map transfer alone would overstate generality; the structure map is where Kubo and FAT diverge from the baseline.
