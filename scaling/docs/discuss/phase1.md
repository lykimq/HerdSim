# Phase 1: Size Scaling (Baseline)

## Question
Does the minimum shepherd count $D_{\min}$ scale with flock size $N$ under the baseline `strombom_multi` controller on a compact initial layout? Do we observe an overcrowding collapse at high dog counts?

## Results Summary
- **Tested**: $N \in [5, 400]$, $D \in [1, 35]$, $\theta = 0.90$.
- **$D_{\min}$ Frontier**:
  - $N \in \{5, 10\}$: $D_{\min} = 2$.
  - $N \ge 25$: $D_{\min} = 1$ across all sizes up to $N = 400$.
- **Overcrowding**: 0 overcrowding cells found. Adding more shepherds up to $D = 35$ did not cause task failure. High dog counts simply produce wasteful path effort ($B^*$ remains at 1 dog).
- **T1 Evaluation**: Skipped because there were no overcrowding candidates to test at $T_1 = 20,000$ ticks.
- **Scaling Fits (Package F)**: Leave-one-$N$-out cross-validation favors a piecewise model over a power law, primarily due to the transition between small flocks ($N \le 10$, $D_{\min}=2$) and larger flocks ($D_{\min}=1$).

## Claims Verdict
- **C2a (Overcrowding)**: **Rejected**. No overcrowding onset observed at $\theta = 0.90$.
- **C2b ($T_1$ Overcrowding Persistence)**: **Skipped**. No overcrowding cells to extend.

## Discussion & Contrast with Literature
Earlier draft findings in NetLogo reported that $D_{\min}$ scaled upwards with flock size and showed overcrowding. In HerdSim's open-interior drive task with Strombom dynamics, one dog is sufficient once the flock exceeds 10 sheep. Extra dogs increase path interference but do not disrupt collection into the goal pen.
