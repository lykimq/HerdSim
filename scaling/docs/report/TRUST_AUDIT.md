# Trust audit (scaling_v2)

Package note: this audit was written against the live tree under `scaling/results/`. In this email package the same run folders are renamed by research question (phase1 -> rq2, phase2 -> rq1, phase4 -> rq4, phase5 -> rq5). Timeseries parquet files are not included here.


Date: 2026-10-09. Host: gwen. Protocol hash: `54dfb46837e3971a` on all audited provenance files.

## What was checked

1. Count triangulation: `status.n_done` vs `trials.csv` vs `manifest.jsonl` for every pilot/scout/claim folder under `scaling/results/phase{1,2,4,5}/`.
2. Protocol hash lock across those provenance files (stored hash, rehash of embedded protocol, and current `canonical_grid.yaml`).
3. Claim merge depth math for Phase 1/2/4/5 claim folders (recompute `merge_scout_and_claim`).
4. Phase 5 obs pause/resume repair (orphan manifest keys without CSV rows).
5. Package E / F / G claim rows vs tracker.
6. Run ledger rebuild to include Phase 5.
7. Final report scope sync for Phases 5 and 7.
8. `make -C scaling scaling-test` (20 passed after resume-key contract test).
9. Offline CLI/code audit (no phase re-runs): seed list = `master_seed + i`; manifest/trials join on resume identity; grid / factor / claim boundary expansion vs completed rows.

## Integrity result

All audited folders: OK (status/trials/manifest match when complete; protocol hash locked; claim merges recompute to stored row counts; seeds match formula).

`make -C scaling scaling-test`: 20 passed.

Known caveats retained:

- Phase 4 Kubo structure claim `n_planned` in status is 600 while completed claim rows are 4,000 (documented in the run ledger).
- Same folder: protocol `seeds: 100`, but 9 `outlier_rich` N=200 cells were intentionally oversampled to 200 seeds (22 cells x 100 + 9 cells x 200 = 4,000). Boundary CSV has 31 cells; a naive re-expand at 100 seeds yields 3,100. Existing trials and merge depths are consistent; re-seeding would need the 200-seed oversample recorded per cell.
- Resume keys for grid scouts omit `O*` / `R*` / `C*` when those `ScalingCell` fields were unset, while `trials.csv` may still store resolved config `obs_mode` (usually `global`). Analysis and D_min use CSV columns, not key strings. Documented on `_cell_key` in `scaling/services/scaling/runner.py`.

Phase 5 obs claim after repair:

| Field | Value |
|-------|------:|
| trials.csv | 1200 |
| manifest ok | 1200 |
| merged_trials.csv | 1920 |
| claim-depth cells | 12 at 100 seeds |
| scout-depth cells on merge | 24 at 30 seeds |

Repair notes: obs claim orphan keys were stripped and reseeding completed 2026-10-08; temporary repair ledgers and backups were removed after audit. Current `manifest.jsonl` and `trials.csv` are authoritative.

## Claims after audit

| Claim | Verdict |
|-------|---------|
| C5a | REJECTED (unchanged after obs repair; Package E still flat / bearing hard-fail) |
| C5b | INCONCLUSIVE (unchanged) |
| C6a | SUPPORTED |
| C6b | SUPPORTED (compact N in {25..400}, slope 0 < 1) |
| C7a | INCONCLUSIVE |
| C7b | REJECTED |

## Not re-run

Full Phase 1/2/4/5 grids were not regenerated. Spot counts, hashes, merges, and CLI expansion checks matched existing claim artifacts.

## Follow-ups completed

- Runner now flushes `trials.csv` after each finished cell (`scaling/services/scaling/runner.py`).
- Final report includes Phase 5 and Phase 7 narrative plus updated claim snapshot.
- Resume-key contract covered by `test_resume_keys_omit_unset_info_factors`.

## Optional follow-up (not done)

- Record per-cell seed depth for Kubo structure claim oversample (or bump those 9 cells in protocol notes) so a future claim-reseed cannot silently drop to 100 seeds.
- Refresh Kubo structure claim `status.n_planned` from 600 to 4000 (metadata only).
