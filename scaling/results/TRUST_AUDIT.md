# Trust audit (scaling_v2)

Date: 2026-10-09. Host: gwen. Protocol hash: `54dfb46837e3971a` on all audited provenance files.

## What was checked

1. Count triangulation: `status.n_done` vs `trials.csv` vs `manifest.jsonl` for every pilot/scout/claim folder under `scaling/results/phase{1,2,4,5}/`.
2. Protocol hash lock across those provenance files.
3. Claim merge depth math for Phase 5 obs/range/comm.
4. Phase 5 obs pause/resume repair (orphan manifest keys without CSV rows).
5. Package E / F / G claim rows vs tracker.
6. Run ledger rebuild to include Phase 5.
7. SUMMARY_REPORT scope sync for Phases 5 and 7.
8. `make -C scaling scaling-test` (19 passed).

## Integrity result

All audited folders: OK (status/trials/manifest match when complete).

Known caveat retained: Phase 4 Kubo structure claim `n_planned` in an older status field is 600 while completed claim rows are 4,000 (documented in the run ledger).

Phase 5 obs claim after repair:

| Field | Value |
|-------|------:|
| trials.csv | 1200 |
| manifest ok | 1200 |
| merged_trials.csv | 1920 |
| claim-depth cells | 12 at 100 seeds |
| scout-depth cells on merge | 24 at 30 seeds |

Repair notes: `phase5/obs_claim/ORPHAN_MANIFEST_KEYS.json` and `manifest.jsonl.bak_*`.

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

Full Phase 1/2/4 grids were not regenerated. Spot counts and hashes matched existing claim artifacts.

## Follow-ups completed

- Runner now flushes `trials.csv` after each finished cell (`scaling/services/scaling/runner.py`).
- SUMMARY_REPORT (EN/VI) includes Phase 5 and Phase 7 narrative plus updated claim snapshot.
- HTML mirrors rebuilt via `results/summary/_rebuild_html.py`.
