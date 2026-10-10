# Trust audit (scaling_v2)

Date: 2026-10-09. Host: gwen. Protocol hash: `54dfb46837e3971a` on all audited provenance files.

## What was checked

1. Count triangulation: `status.n_done` vs `trials.csv` vs `manifest.jsonl` for every pilot/scout/claim folder under `results/phase{1,2,4}/` (Phase 5 excluded; see below).
2. Protocol hash lock across those provenance files (stored hash, rehash of embedded protocol, and current `canonical_grid.yaml`).
3. Claim merge depth math for Phase 1/2/4 claim folders (recompute `merge_scout_and_claim`).
4. Package F / G claim rows vs tracker.
5. Run ledger rebuild for Phases 1/2/4.
6. `make -C run scaling-test` (passed after resume-key contract test).
7. Offline CLI/code audit (no phase re-runs): seed list = `master_seed + i`; manifest/trials join on resume identity; grid / factor / claim boundary expansion vs completed rows.

## Integrity result

Audited Phase 1/2/4 folders: OK (status/trials/manifest match when complete; protocol hash locked; claim merges recompute to stored row counts; seeds match formula).

`make -C run scaling-test`: passed.

Known caveats retained:

- Phase 4 Kubo structure claim `n_planned` in status is 600 while completed claim rows are 4,000 (documented in the run ledger).
- Same folder: protocol `seeds: 100`, but 9 `outlier_rich` N=200 cells were intentionally oversampled to 200 seeds (22 cells x 100 + 9 cells x 200 = 4,000). Boundary CSV has 31 cells; a naive re-expand at 100 seeds yields 3,100. Existing trials and merge depths are consistent; re-seeding would need the 200-seed oversample recorded per cell.
- Resume keys for grid scouts omit `O*` / `R*` / `C*` when those `ScalingCell` fields were unset, while `trials.csv` may still store resolved config `obs_mode` (usually `global`). Analysis and D_min use CSV columns, not key strings. Documented on `_cell_key` in `run/services/scaling/runner.py`.

## Phase 5 / RQ5

NOT RUN YET for claim-grade reporting. Prior Phase 5 scout/claim trees were removed after shared sim bugs invalidated those ladders (bearing-only freeze, range under global observation, communication list stacking). Protocols remain; rerun with `bash results/phase5/run_all_ladders.sh` after the fixes. C5a and C5b are marked NOT RUN.

## Claims after audit

| Claim | Verdict |
|-------|---------|
| C5a | NOT RUN |
| C5b | NOT RUN |
| C6a | SUPPORTED |
| C6b | SUPPORTED (compact N in {25..400}, slope 0 < 1) |
| C7a | INCONCLUSIVE |
| C7b | REJECTED |

## Not re-run

Full Phase 1/2/4 grids were not regenerated for this audit. Spot counts, hashes, merges, and CLI expansion checks matched existing claim artifacts. Phase 5 awaits a clean rerun.

## Optional follow-up (not done)

- Record per-cell seed depth for Kubo structure claim oversample (or bump those 9 cells in protocol notes) so a future claim-reseed cannot silently drop to 100 seeds.
- Refresh Kubo structure claim `status.n_planned` from 600 to 4000 (metadata only).
- Rerun Phase 5 ladders and refresh C5a/C5b.
