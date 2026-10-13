# Phase 1: flock size map

How many dogs do we need as the flock gets larger, on a compact start with `strombom_multi`?

We ran pilot first (N in {5, 10, 25, 50, 100}, D in {1, 2, 3, 4, 6, 10}, 5 seeds, 150 trials, 43 s), then scout (full N x D, 30 seeds, 3,000 trials, 1h 12m 39s), then claim (22 window cells at 100 seeds, 2,200 trials, merge 4,540, 57m 31s). Sim total about **2h 11m**. T1 was skipped (no overcrowding cells; no `t1/` results folder).

Claim-grade merge success is 0.963. `D_min` = 2 for N in {5, 10}, and 1 for N >= 25. No overcrowding at theta = 0.90.

- **C2a** (at theta 0.90 the baseline has overcrowding for at least one N, i.e. a `D_overcrowd`): **REJECTED**. We found none.
- **C2b** (at least one D above `D_overcrowd` still fails at T = 20,000): **SKIPPED**. No overcrowding cells to extend.
- **C6a** (a power law fits `D_min` vs N worse than piecewise / per-layout curves): **SUPPORTED (weak)**. Only two observed `D_min` levels.
- **C6b** (log `D_min` vs log N has slope below 1 on a stated band): **SUPPORTED**. Flat `D_min` = 1 on compact N in {25...400}.
- **C7a** (held-out state AUROC beats the `(N, D)` baseline): **INCONCLUSIVE**. Package G folds empty. AUROC = Area Under the ROC Curve, a 0-to-1 score for how well a model ranks likely failures vs successes (0.5 = chance, 1.0 = perfect); here it asks whether flock-state features predict failure better than knowing only `(N, D)` on held-out data.
- **C7b** (at least 30% of failure trials have lead time >= 500 ticks): **REJECTED**. Only 8.3% meet that bar.

## How we get this

- pilot: 150 trials

`run --protocol phase1_pilot --workers 16`

- scout: 3000 trials

`run --protocol phase1_scout --workers 16`

- claim: 2200 trials

`claim-reseed --protocol phase1_claim --workers 16`

## Files from this run

Machine-written outputs in this folder (do not edit by hand):

`protocol.yaml`, `provenance.json`, `status.json`, `manifest.jsonl`, `trials.csv`, `packages/`.
Claim also has merge / boundary / bootstrap files and `timeseries/`.
