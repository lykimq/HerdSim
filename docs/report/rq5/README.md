# RQ5: information vs shepherds

Can richer observation, sensing range, or communication lower the fewest-dogs answer at the same reliability?

## Status

NOT RUN YET. No claim-grade results are published for this question.

Earlier Phase 5 ladder runs were removed after shared observation and communication bugs were found (bearing-only freeze, range under global observation, duplicated shared sheep lists). Those runs are not evidence. Protocols remain under `scaling/configs/protocols/phase5_*.yaml` for a future rerun after the sim fixes.

## This folder

This folder is only a note. There is no `trials.csv`, run ledger, or package tree.

## Planned design (not executed here)

Method: `strombom_multi`. Layout: compact. N in {100, 200}. Three separate ladders (observation, sensing range, communication). Scout then claim as in the Phase 5 protocols.

```bash
WORKERS=18 bash scaling/results/phase5/run_all_ladders.sh
```

## Claims

| Claim | What it asks (supported when) | Verdict |
|-------|-------------------------------|---------|
| C5a | One ladder step lowers `D_min` by at least one D-grid step at N in {100, 200} | NOT RUN |
| C5b | The second ladder step saves fewer dogs than the first | NOT RUN |
