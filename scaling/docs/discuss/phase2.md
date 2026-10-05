# Phase 2: Initial Spatial Structure

## Question
Does initial spatial geometry $X_0$ alter the minimum number of shepherds $D_{\min}$ required to drive the flock at fixed flock sizes $N \in \{50, 100, 200\}$?

## Results Summary
- **Tested**: Layouts `compact`, `wide`, `split`, and `outlier_rich` across $N \in \{50, 100, 200\}$ and $D \in [1, 35]$.
- **$D_{\min}$ Invariance**: $D_{\min} = 1$ across all four layout families at all three sizes. Even an elongated or split flock does not require additional dogs to achieve $\ge 90\%$ reliability given $T_0 = 10,000$ ticks.
- **Effort ($B^*$ Path Length)**:
  - `compact` and `split` require ~150 path units.
  - `wide` requires ~3,000 to ~3,700 path units (a 20-fold increase in movement). Its best operational point $B^*$ shifts to **2 dogs** to minimize overall path.
  - `outlier_rich` effort increases rapidly with flock size (from 209 units at $N=50$ to 1,647 units at $N=200$).

```text
Layout        N    D_min   B* Dogs   B* Path Effort
compact       50   1       1         157.5
compact       100  1       1         161.4
compact       200  1       1         144.2

split         50   1       1         157.5
split         100  1       1         162.0
split         200  1       1         144.4

outlier_rich  50   1       1         209.2
outlier_rich  100  1       1         553.9
outlier_rich  200  1       1         1646.7

wide          50   1       2         2336.8
wide          100  1       2         3003.2
wide          200  1       2         3693.7
```

## Claims Verdict
- **C1a ($D_{\min}$ shifts across layouts)**: **Rejected**. $D_{\min} = 1$ for all tested layouts.
- **C1b (State predictor vs $(N, D)$)**: **Inconclusive**. Because $D_{\min}$ does not shift, state-based metrics do not improve over the $(N, D)$ baseline.

## Discussion
Dispersed and wide layouts do not cause herd failure for single shepherds, but they drastically increase task completion time and movement cost. The single shepherd reliably rounds up distant sheep before completing the drive.
