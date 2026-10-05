# Phase 4: Controller Generality & Transfer

## Question
Do the scaling frontiers observed on the baseline `strombom_multi` controller generalize to other canonical shepherding algorithms (`kubo` and `fat`) across both flock size and initial structure?

## Results Summary
- **Tested**: `kubo` and `fat` across 10 flock sizes ($N \in [5, 400]$) and 4 layout families ($N \in \{50, 100, 200\}$) on $D \in [1, 35]$.
- **Kubo Controller**:
  - For $N \ge 25$ through 400, $D_{\min} = 1$ is **shared** with the baseline.
  - At small sizes, minor boundary shifts: $N=5$ requires 3 dogs; $N=10$ requires 1 dog.
  - Structure grid: $D_{\min} = 1$ across all four layouts.
  - Overcrowding: None observed.
- **FAT Controller (Potential Fields)**:
  - Works on small flocks ($N \le 10$ with $D_{\min} = 1$).
  - Experiences **hard failure** for $N \ge 25$ through 400: fails to reach $\theta = 0.90$ reliability within 10,000 ticks, regardless of shepherd count ($D$ up to 35).
  - FAT's attractive/repulsive force fields circle or disperse large flocks without completing the pen drive.

```text
Flock Size N      Strombom (Baseline)   Kubo             FAT
N = 5             D_min = 2             D_min = 3        D_min = 1
N = 10            D_min = 2             D_min = 1        D_min = 1
N = 25 .. 400     D_min = 1             D_min = 1        Hard Failure (R < 0.90)
Overcrowding      None                  None             None
```

## Claims Verdict
- **C4 (Shared $D_{\min}$ / Overcrowding)**: **Supported (partial)**. Strombom and Kubo share $D_{\min} = 1$ and the absence of overcrowding for $N \ge 25$. FAT does not transfer due to large-flock failure.

## Discussion
Shepherding scaling laws depend strongly on controller architecture. Reactive collect-and-drive algorithms (Strombom, Kubo) maintain flat scaling frontiers ($D_{\min} \approx 1$) up to 400 sheep, whereas potential-field controllers (FAT) suffer severe scalability breakdown on open-field drive tasks.
