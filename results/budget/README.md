# Budget experiment results

This directory holds shepherding-budget campaign outputs. Heavy artefacts are
gitignored; this README is tracked so the layout stays documented.

Science and protocol: `docs/research/budget/main_shepherding_budget_plan.md`  
Live status: `docs/research/budget/progress_tracker.md`  
Campaign subsets: `configs/budget/campaigns/`  
Human report template: `docs/research/budget/REPORT_TEMPLATE.md`

## Layout

```text
results/budget/
  README.md
  phase1/
    pilot/                 # make budget-pilot
    scout/                 # make budget-scout
  phase2/
    pilot_state/           # make budget-pilot-state
  phase5/
    factor_sweep/          # make budget-factor-sweep
```

Each campaign folder:

```text
phase{k}/{campaign_slug}/
  campaign.yaml            # copy of the campaign subset used
  manifest.jsonl           # resume ledger (do not delete)
  provenance.json          # campaign stamp
  status.json              # planned / done counts
  trials.csv               # one row per completed trial
  timeseries/              # stem == cell key (includes instrument)
  packages/
    a/ ... g/              # auto analysis (Package A-G)
  REPORT.md                # human narrative only (optional, may be committed)
```

## Conventions

1. Path = `phase{k}/{campaign_slug}/`.
2. `campaign_id` in provenance matches the campaign YAML (e.g. `phase1_scout`).
3. Resume ledger is only `manifest.jsonl`. Package path maps are `artefacts.json`.
4. Trial table is always `trials.csv` (not `summary.csv`).
5. Timeseries stem matches the resume cell key, e.g.
   `N50_D2_Lcompact_S2026_Istrombom_multi.parquet`.
6. Auto analysis goes under `packages/{letter}/` (tables + `package_*.md` +
   `figures/` when generated). Reserve `REPORT.md` for human narrative
   (template: `docs/research/budget/REPORT_TEMPLATE.md`).
7. Frozen Section 8 defaults live in `configs/budget/canonical_grid.yaml`
   (each field has a WHY comment; see also main plan Section 8.1).
   Per-run subsets live in `configs/budget/campaigns/*.yaml` with the same
   rule. New campaigns: follow `configs/budget/campaigns/README.md`.

### Package A auto report contents

After `budget-analyse PACKAGE=A` (or pilot/scout), expect:

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

Human `REPORT.md` at the campaign root interprets those artefacts.

## Operator commands

```bash
make help                              # basic project targets
make -f Makefile.budget help           # budget campaigns (or: make budget-help)

make -f Makefile.budget budget-test
make -f Makefile.budget budget-pilot BUDGET_MAX_TICKS=3000 WORKERS=1
make -f Makefile.budget budget-pilot-state
make -f Makefile.budget budget-scout WORKERS=16
make -f Makefile.budget budget-factor-sweep
make -f Makefile.budget budget-analyse PACKAGE=A TRIALS=results/budget/phase1/scout/trials.csv
```

The main `Makefile` still forwards `make budget-*` to `Makefile.budget`, so existing habits keep working.

## Resume rules

- Keep `manifest.jsonl` and reuse the same `--output` / make target.
- Do not delete the campaign folder mid-run unless you intend a full rerun
  (`--no-resume`).
- After a stop, re-run the same target; completed `status=ok` cells are skipped.
- Re-analyse without resimulating: `make budget-analyse ...`.

## What to commit

- Tracked: this README; optional `REPORT.md` files under campaigns.
- Ignored: `trials.csv`, parquet timeseries, package CSVs, manifests (local only
  unless you choose otherwise).

When citing a claim, point the tracker at the campaign `REPORT.md` and the
matching `packages/` exports, and record grade (SMOKE / SCOUT / CLAIM).
