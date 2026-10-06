# Thiet lap va tham chieu scaling

Thu muc nay la tai lieu van hanh cho giao thuc `scaling_v2`. Tai lieu giai thich thiet lap dong bang, tham so, thuat ngu, va lenh campaign ma khong thay doi ke hoach nghien cuu.

## Thu tu doc

1. [Thiet lap thi nghiem](experiment_setup_vi.md): nhiem vu, san, bo cuc, phan tang, ly do, cap trien khai, va gioi han nghien cuu.
2. [Tham chieu tham so](parameter_reference_vi.md): gia tri dong bang, mac dinh bo dieu khien, metric, bien, va phan tich.
3. [Huong dan chay](run_guide_vi.md): test, chay, tiep tuc, lap ke hoach, gieo lai, T1, phan tich, dau ra, va provenance.
4. [Bang thuat ngu](glossary_vi.md): ky hieu va dinh nghia van hanh.

Ban tieng Anh:

- [Experiment setup](experiment_setup.md)
- [Parameter reference](parameter_reference.md)
- [Run guide](run_guide.md)
- [Glossary](glossary.md)

## Thu tu uu tien nguon

1. [`scaling/configs/canonical_grid.yaml`](../../configs/canonical_grid.yaml) la nguon co tham quyen cho mac dinh may-doc cua `scaling_v2`.
2. YAML da resolve trong [`scaling/configs/protocols/`](../../configs/protocols/) dinh nghia mot campaign cu the va co the thu hep luoi canonical.
3. `protocol.yaml` trong thu muc ket qua ghi dung recipe da dung.
4. [`scaling/docs/main_scaling_plan.md`](../main_scaling_plan.md) dinh nghia cau hoi nghien cuu, dependency, quy tac bien va regime, tieu chi claim, ngan sach, va cong quyet dinh.
5. [`scaling/docs/experiment_run_strategy.md`](../experiment_run_strategy.md) dinh nghia phan tang va muc dich van hanh.
6. [`scaling/Makefile`](../../Makefile) va `uv run scaling/scripts/campaign.py help` dinh nghia lenh hien tai.
7. [`scaling/results/README.md`](../../results/README.md) va bao cao tong hop mo ta artifact va trang thai thuc te. Ket qua khong dinh nghia lai giao thuc dong bang.

Bang tham so va dinh nghia dai luong truoc day nam trong Phu luc A va B cua Summary Report hien duoc duy tri tai [tham chieu tham so](parameter_reference_vi.md) va [bang thuat ngu](glossary_vi.md).

Neu tai lieu ke hoach khac voi protocol da copy cua mot run, dung `protocol.yaml`, `provenance.json`, `manifest.jsonl`, va `status.json` cua run do. Khong sua ngam gia tri dong bang.

## So do

- [Tong quan san](../../results/summary/figures/schematics/vi/arena_overview.svg)
- [San voi bo cuc compact](../../results/summary/figures/schematics/vi/arena_compact.svg)
- [Quy tac ban kinh dich](../../results/summary/figures/schematics/vi/goal_radius.svg)
- [Bon bo cuc](../../results/summary/figures/schematics/vi/four_layouts.svg)
- [Pipeline phan tang](../../results/summary/figures/schematics/vi/pipeline.svg)
- [Mot cell va cac seed](../../results/summary/figures/schematics/vi/one_cell_seeds.svg)
- [Luoi scout](../../results/summary/figures/schematics/vi/scout_grid.svg)
- [Cua so claim](../../results/summary/figures/schematics/vi/claim_window.svg)
- [Cac regime](../../results/summary/figures/schematics/vi/regimes.svg)

## Pham vi

Tai lieu nay chi mo ta thiet lap va van hanh. Verdict cua claim nam trong tracker va bao cao cap CLAIM. Ket luan chi ap dung cho mo phong, nhiem vu, luoi da thu, va do phan giai tick nay. Tai lieu khong khang dinh quy luat chung cho nhiem vu khac hay nong trai that, va khong phan giai duoc chenh lech nho hon mot buoc cuc bo cua luoi D.
