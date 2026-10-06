# Phu luc du lieu

Thu muc nay la muc luc tai tao duoc cho bang chung cua Giai doan 1, 2 va 4. Cac bang duoc tao truc tiep tu CSV, JSON, status va provenance chinh tac. Khong co so nao duoc nhap tay.

## Cach doc

* [So cai chay](run_ledger_vi.md): cap pilot, scout, claim; so dong; hash protocol; lien ket provenance.
* [Bang Giai doan 1](phase1_tables_vi.md): bien kich thuoc, che do, fit scaling va tom tat merge.
* [Bang Giai doan 2](phase2_tables_vi.md): bien theo bo cuc, chi phi mot cho, predictor va tom tat merge.
* [Bang Giai doan 4](phase4_tables_vi.md): transfer Kubo va FAT, hard failure, cua so Kubo kho va tom tat merge.
* [English index](README.md).

## Quy uoc bang chung

Scout la ban do 30 seed dung de chon cua so. Claim la bang chung chinh xac, thuong 100 seed, va la cap dung cho ket luan. Merge claim thay dong scout tai cac o da gieo lai claim va giu scout tai cac o con lai. Vi vay moi ket luan phai giu ro cap cua tung o.

`D_max = 35` voi `D_overcrowd` trong chi co nghia la thanh cong van dat nguong tai dinh luoi da thu. Neu `hard_failure = True`, khong D nao trong luoi dat R = 0.90, nen khong duoc dien mot `D_max` gia.

## Tai tao

Chay `python3 build_tables.py` trong thu muc nay. Chay `python3 build_tables.py --check` de xac nhan cac tep da tao trung khop voi nguon hien tai. Script chi ghi 10 tep Markdown trong thu muc nay.
