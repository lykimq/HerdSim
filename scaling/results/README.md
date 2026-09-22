# Scaling experiment results

Protocol outputs for the scaling work live here. Run data under
`scaling/results/` is kept in git (trials, packages, provenance, timeseries, etc.)
so a finished campaign stays available for analysis and claims.

Science and protocol: `scaling/docs/main_scaling_plan.md`  
Status / run plan / hardware: `scaling/docs/progress_tracker.md`  
Protocol subsets: `scaling/configs/protocols/`  
Report template: `scaling/docs/REPORT_TEMPLATE.md`

## Layout

```text
scaling/results/
  README.md
  phase1/
    pilot/                 # make scaling-pilot
    scout/                 # make scaling-scout
    claim/                 # make scaling-claim-plan / scaling-claim-reseed
  phase2/
    pilot_state/           # make scaling-pilot-state
  phase5/
    factor_sweep/          # make scaling-factor-sweep
```

Each protocol folder:

```text
phase{k}/{protocol_slug}/
  protocol.yaml            # copy of the protocol subset used
  manifest.jsonl           # resume ledger (do not delete)
  provenance.json          # protocol stamp
  status.json              # planned / done counts; started_at / updated_at /
                           # finished_at / elapsed_seconds / running (clock only)
  trials.csv               # one row per completed trial
  timeseries/              # stem == cell key (includes method)
  packages/
    a/ ... g/              # auto analysis (Package A-G)
  REPORT.md                # hand-written note (from REPORT_TEMPLATE.md)
```

## Conventions

1. Path = `phase{k}/{protocol_slug}/`.
2. `protocol_id` in provenance matches the protocol YAML (e.g. `phase1_scout`).
3. Resume ledger is only `manifest.jsonl`. Package path maps are `artefacts.json`.
4. Trial table is always `trials.csv` (not `summary.csv`).
5. Timeseries stem matches the resume cell key, e.g.
   `N50_D2_Lcompact_S2026_Mstrombom_multi.parquet`.
6. Auto analysis goes under `packages/{letter}/` (tables + `package_*.md` +
   `figures/` when generated). `REPORT.md` is the hand-written note
   (template: `scaling/docs/REPORT_TEMPLATE.md`).
7. Frozen Section 8 defaults live in `scaling/configs/canonical_grid.yaml`
   (each field has a WHY comment; see also main plan Section 8.1).
   Per-run subsets live in `scaling/configs/protocols/*.yaml` with the same
   rule. New protocols: follow `scaling/configs/protocols/README.md`.

### Package A auto report contents

After `scaling-analyse PACKAGE=A` (or pilot/scout), expect:

```text
packages/a/
  package_a.md           # setup, diagnostics, claim stubs, tables, figure links
  trials.csv reliability.csv frontier.csv regimes.csv
  provenance.json artefacts.json
  figures/
    reliability_heatmap.png   # or reliability_heatmap_<layout>.png
    frontier_dmin.png
    regime_counts.png
```

`REPORT.md` at the protocol root is where you write what you make of those files.

## Operator commands

```bash
make help                              # basic project targets
make -C scaling help           # scaling protocols (or: make scaling-help)

make -C scaling scaling-test
make -C scaling scaling-pilot SCALING_MAX_TICKS=3000 WORKERS=1
make -C scaling scaling-pilot-state
make -C scaling scaling-scout WORKERS=16
make -C scaling scaling-claim-plan SCOUT_TRIALS=results/phase1/scout/trials.csv
make -C scaling scaling-claim-reseed WORKERS=8
make -C scaling scaling-factor-sweep
make -C scaling scaling-analyse PACKAGE=A TRIALS=results/phase1/scout/trials.csv
```

The root `Makefile` still forwards `make budget-*` into `scaling/`.

## Resume rules

- Keep `manifest.jsonl` and reuse the same `--output` / make target.
- Do not delete the protocol folder mid-run unless you intend a full rerun
  (`--no-resume`).
- After a stop, re-run the same target; completed `status=ok` cells are skipped.
- Re-analyse without resimulating: `make scaling-analyse ...`.

## What to commit

After a protocol (or a useful partial run), commit the protocol folder under
`scaling/results/phase{k}/{slug}/` so the run stays with the repo:

- `protocol.yaml`, `provenance.json`, `status.json`, `manifest.jsonl`
- `trials.csv`
- `timeseries/` (needed for mechanism / early-warning work)
- `packages/`
- `REPORT.md` when you have written it

Point the tracker at that path and the grade (SMOKE / SCOUT / CLAIM) when citing
a claim.

Note: full claim-grade grids with timeseries can get large. Prefer one protocol
folder per commit (or per logical batch) rather than mixing unfinished scratch
runs with claim data.
