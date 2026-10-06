# Huong dan chay

Chay lenh tu `/home/gwen/HerdSim`. Makefile dat `PYTHONPATH` va goi `scaling/scripts/campaign.py`.

## Xem help va test

```bash
make -C scaling help
uv run scaling/scripts/campaign.py help
make -C scaling scaling-test
```

Target correctness chay:

```bash
uv run pytest tests/backend/correctness/test_scaling_stack.py -q
```

So worker mac dinh la 18 cho host ghi trong `scaling/Makefile`. Tren may nho hon, override nhu `WORKERS=4`.

## Phase 1: baseline size

```bash
make -C scaling scaling-pilot
make -C scaling scaling-scout
make -C scaling scaling-claim-plan
make -C scaling scaling-claim-reseed
make -C scaling scaling-analyse PROTOCOL=phase1_claim PACKAGE=A
make -C scaling scaling-t1-plan
make -C scaling scaling-t1
```

Chay theo thu tu nay. Pilot la smoke check. Scout map luoi day du. Claim plan ghi cell selection nhung khong chay simulation. Claim reseed chay cac cell va tao merged claim data. T1 chi chay neu planner thay overcrowding.

Baseline da hoan thanh khong co overcrowding cell, nen Phase 1 T1 khong chay. Khong chay T1 chi de lap thu muc neu planner khong co cell.

## Phase 2: structure

```bash
make -C scaling scaling-pilot-state
make -C scaling scaling-phase2-scout
make -C scaling scaling-phase2-claim-plan
make -C scaling scaling-phase2-claim-reseed
make -C scaling scaling-analyse PROTOCOL=phase2_claim PACKAGE=B
```

Moi layout va N co cua so frontier rieng.

## Phase 4: transfer controller

Chay size va structure rieng cho Kubo:

```bash
make -C scaling scaling-transfer-size-scout TRANSFER_METHOD=kubo
make -C scaling scaling-transfer-size-claim-plan TRANSFER_METHOD=kubo
make -C scaling scaling-transfer-size-claim-reseed TRANSFER_METHOD=kubo
make -C scaling scaling-transfer-structure-scout TRANSFER_METHOD=kubo
make -C scaling scaling-transfer-structure-claim-plan TRANSFER_METHOD=kubo
make -C scaling scaling-transfer-structure-claim-reseed TRANSFER_METHOD=kubo
```

Lap lai voi `TRANSFER_METHOD=fat`. Package D chi tong hop sau khi du map bat buoc.

## Phase 5: information ladder

Observation:

```bash
make -C scaling scaling-factor-sweep
make -C scaling scaling-phase5-obs-claim-plan
make -C scaling scaling-phase5-obs-claim-reseed
```

Sensing range:

```bash
make -C scaling scaling-phase5-range-scout
make -C scaling scaling-phase5-range-claim-plan
make -C scaling scaling-phase5-range-claim-reseed
```

Communication:

```bash
make -C scaling scaling-phase5-comm-scout
make -C scaling scaling-phase5-comm-claim-plan
make -C scaling scaling-phase5-comm-claim-reseed
```

Ba ladder la campaign rieng, khong phai Cartesian product.

## Lenh campaign truc tiep

Dang chung:

```bash
uv run scaling/scripts/campaign.py VERB --protocol PROTOCOL_ID [OPTIONS]
```

Verb gom `run`, `claim-plan`, `claim-reseed`, `t1-plan`, `t1`, va `analyse`. Protocol ID duoc resolve trong `scaling/configs/protocols/`.

```bash
uv run scaling/scripts/campaign.py run --protocol phase1_scout --workers 8
uv run scaling/scripts/campaign.py claim-plan --protocol phase1_claim
uv run scaling/scripts/campaign.py claim-reseed --protocol phase1_claim --workers 8
uv run scaling/scripts/campaign.py analyse --protocol phase1_claim --package A
```

Option gom `--output`, `--workers`, `--upstream-trials`, `--no-analyse`, `--package`, `--trials`, `--methods`, `--layouts`, `--n`, `--d`, `--seeds`, `--max-ticks`, `--no-timeseries`, va `--no-resume`.

Make variable map toi filter:

```bash
make -C scaling scaling-scout WORKERS=4 SCALING_N=100 SCALING_D=1 SCALING_SEEDS=2
make -C scaling scaling-analyse PROTOCOL=phase1_claim PACKAGE=F \
  TRIALS=scaling/results/phase1/claim/merged_trials.csv
```

Filter va seed override dung cho chan doan. Run da filter khong phai campaign dong bang day du va khong duoc trinh bay nhu campaign day du.

## Resume

Resume bat mac dinh. Chay lai cung lenh voi cung output directory. Runner doc `manifest.jsonl` va bo trial key co `status=ok`. Key gom N, D, seed, layout, method, va factor observation, range, communication neu co.

```bash
make -C scaling scaling-scout
```

Kiem tra `status.json` truoc va sau resume. File ghi so planned, done, pending tai luc bat dau, running, va timestamp. Tranh `--no-resume` tru khi co chu y chay moi, vi option nay tat skip key da xong.

## Phan tich trial co san

```bash
make -C scaling scaling-analyse \
  PROTOCOL=phase1_claim \
  PACKAGE=A \
  TRIALS=scaling/results/phase1/claim/merged_trials.csv
```

`TRIALS` va `OUT` la Make variable tuy chon. Neu analyse truc tiep khong co protocol, can ca `--trials` va `--output`.

Package:

- A: baseline size frontier va reliability.
- B: structure.
- C: mechanism.
- D: transfer.
- E: information substitution.
- F: scaling fit.
- G: early warning.

Package C, F, G chu yeu phan tich data da thu. G can timeseries. Scout protocol thuong dat `store_timeseries: false` de giam disk I/O; claim protocol dat true cho boundary trajectory.

## Dau ra

| Artifact | Y nghia |
|---|---|
| `protocol.yaml` | Recipe da resolve |
| `provenance.json` | Protocol stamp, seed list, code va host metadata, metric ID, timestamp |
| `manifest.jsonl` | Resume ledger voi `status=ok` |
| `status.json` | So planned, done va timestamp |
| `trials.csv` | Mot row moi simulation |
| `boundary_cells.csv` | Cell do claim planner chon |
| `merged_trials.csv` | Claim row thay scout row tai cell gieo lai |
| `timeseries/*.parquet` | Trajectory moi trial neu bat |
| `packages/` | Bang va hinh export |
| `README.md` | Ghi chu run va link |

Path thuong gap:

```text
scaling/results/phase1/pilot/
scaling/results/phase1/scout/
scaling/results/phase1/claim/
scaling/results/phase1/t1/
scaling/results/phase2/{pilot_state,scout,claim}/
scaling/results/phase4/{kubo,fat}_{size,structure}/{scout,claim}/
scaling/results/phase5/
```

## Provenance va cach doc

Truoc khi trich ket qua:

1. Xac nhan `status.json` da hoan thanh.
2. Xac nhan `protocol.yaml` co dung protocol, grade, factor, seed count.
3. Giu `provenance.json` va `manifest.jsonl`.
4. Dung `merged_trials.csv` cho claim, khong tu noi CSV.
5. Xac nhan bao cao ghi grade CLAIM.
6. Doc D = 35 la grid ceiling khi D_overcrowd trong.
7. Ghi ro phase co dieu kien bi skip va trigger cua no.

Hinh SCOUT chi dung lap ke hoach, khong duoc nang thanh verdict. Thu muc protocol la don vi provenance; recipe va record may-doc cua no uu tien hon vi du tong quat trong van ban.
