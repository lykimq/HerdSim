# Co so Strombom Collect/Drive

## Cam hung tu cong bo

Strombom va cong su (2014) mo ta mot nguoi chan chuyen giua hai hanh dong. O che do Collect, nguoi chan di ra sau con cuu xa tam dan nhat va day no vao trong. O che do Drive, nguoi chan di ra sau tam dan theo huong nguoc dich va day dan da ket dinh tien ve dich.

Quy tac chuyen che do dung:

```text
f(N) = r_a * N^(2/3)
```

Neu co cuu cach tam khoi luong toan dan xa hon `f(N)`, dan duoc xem la dang trai va nguoi chan Collect. Neu khong, nguoi chan Drive. Mo hinh cong bo cung la co so cho cac quy tac hut, day, quan tinh, an co, nhieu, va dung cua cuu Strombom trong HerdSim.

Tai lieu: D. Strombom va cong su, "Solving the shepherding problem: heuristics for herding autonomous, interacting agents," Journal of The Royal Society Interface 11(100), 2014. DOI: `10.1098/rsif.2014.0719`.

## Hien thuc HerdSim chinh xac

HerdSim tach dong luc cuu va bo dieu khien cho.

Preset `strombom` ket hop:

- `sheep_model=strombom`;
- `dog_controller=collect_drive`;
- mac dinh mot nguoi chan.

Nghien cuu scaling hoan tat khong dung preset nay. Nghien cuu dung `strombom_multi`, van dung cuu Strombom nhung ghep voi `dog_controller=collect_drive_multi`.

### Cuu

Khi moi cho dang hoat dong deu cach xa hon `r_s`, cuu an co. Cuu thuong dung yen va buoc ngau nhien voi xac suat `graze_move_prob`. Khi co cho trong `r_s`, cuu ket hop huong truoc, luc hut ve tam lang gieng, luc day cuu o tam ngan, luc day khoi cho dang hoat dong, va nhieu ngau nhien. Sau do cuu di `sheep_speed`.

Mac dinh cua bundle gom `r_a = 2`, `r_s = 65`, `c = 1.05`, `inertia = 0.5`, `noise_strength = 0.3`, `sheep_speed = 1.0`, va `shepherd_speed = 1.5`.

### Bo dieu khien nhieu cho

Trong quan sat global cua cac giai doan scaling hoan tat, moi cho thay toan dan va tinh cung tam cung nguong.

Trong Collect:

- cuu ngoai `f(N)` duoc sap theo khoang cach den tam;
- cho `i` nhan ca the lac `i mod k`, voi `k` la so ca the lac;
- dich co so nam sau ca the duoc gan mot khoang `r_a` theo huong ra xa tam;
- lech tiep tuyen `2 * r_a` moi slot tach cac cho cung tiep can mot ca the.

Trong Drive:

- dich co so nam sau tam dan mot khoang `r_a * sqrt(N)` theo huong nguoc dich;
- cac cho nam o goc cach deu tren duong tron ban kinh `4 * r_a` quanh dich co so.

Moi cho dung khi gan hon `shepherd_stop_multiple * r_a` voi bat ky cuu nao trong view dang dung. Gia tri mac dinh cua multiple la 3. Chuyen dong cho co nhieu goc Strombom.

Gan ca the lac, lech tiep tuyen trong Collect, va duong tron Drive la phan bo sung cua HerdSim. Chung khong nam trong thuat toan mot nguoi chan nam 2014 va khong duoc khang dinh la ban port cua mot bo dieu khien nhieu nguoi chan da cong bo khac.

Bang chung hien thuc:

- [`../../../core/methods.py`](../../../core/methods.py)
- [`../../../plugins/sheep/strombom.py`](../../../plugins/sheep/strombom.py)
- [`../../../plugins/dogs/collect_drive_multi.py`](../../../plugins/dogs/collect_drive_multi.py)
- [`../../../methods/strombom/heuristics.py`](../../../methods/strombom/heuristics.py)
- [`../../../methods/strombom/config.py`](../../../methods/strombom/config.py)

## Thiet lap `scaling_v2`

`strombom_multi` la bo dieu khien co so trong giao thuc dong bang.

- Giai doan 1: bo cuc compact, luoi kich thuoc `N = {5, 10, 25, 50, 75, 100, 150, 200, 300, 400}`.
- Giai doan 2: `compact`, `wide`, `split`, va `outlier_rich` tai `N = {50, 100, 200}`.
- Luoi cho: `{1, 2, 3, 4, 6, 10, 15, 20, 25, 35}`.
- Che do quan sat trong so sanh hoan tat: global.
- Nguong tin cay: `R >= 0.90`.
- Scout: 30 seed moi o tren toan luoi.
- Claim: 100 seed trong cua so bien da len ke hoach.

Thi nghiem ghi de so cho mac dinh khi quet `D`. Cac phuong trinh dieu khien va mac dinh Strombom o tren duoc giu.

Bang chung cau hinh:

- [`../../configs/canonical_grid.yaml`](../../configs/canonical_grid.yaml)
- [`../../configs/protocols/phase1_claim.yaml`](../../configs/protocols/phase1_claim.yaml)
- [`../../configs/protocols/phase2_claim.yaml`](../../configs/protocols/phase2_claim.yaml)

## Ket qua hoan tat da quan sat

### Ban do kich thuoc compact

Tai nguong tin cay 90%:

- `D_min = 2` voi `N = 5` va `N = 10`;
- `D_min = 1` voi moi `N` da thu tu 25 den 400;
- khong quan sat thay overcrowding;
- `D_max = 35` la tran luoi cho moi kich thuoc, khong phai diem sup da do.

Ban merge claim Giai doan 1 co 4,540 dong va `R = 0.963` toan bo. Phan lon 169 lan that bai tap trung o mot cho voi hai dan nho nhat. Thoi gian hoan thanh trung vi tren merge la 183 tick. Voi `N >= 25`, duong trung vi moi cho khoang 148 don vi.

### Cau truc ban dau

Tai `N = 50, 100, 200`, ca bon bo cuc deu co `D_min = 1`, voi do rong bootstrap bang 0. Cau truc doi chi phi, khong doi so cho tin cay toi thieu:

- wide can khoang 11 den 20 lan thoi gian compact va 19 den 36 lan duong compact o mot cho;
- `outlier_rich`, `N = 200` co trung vi 1,228 tick va duong 1,647 o mot cho;
- tren wide, lua chon tin cay co duong nho nhat `B*` la hai cho o ca ba kich thuoc.

Bang chung:

- [`../../results/phase1/claim/packages/a/frontier.csv`](../../results/phase1/claim/packages/a/frontier.csv)
- [`../../results/phase1/claim/merged_trials.csv`](../../results/phase1/claim/merged_trials.csv)
- [`../../results/phase2/claim/packages/b/frontier_by_layout.csv`](../../results/phase2/claim/packages/b/frontier_by_layout.csv)
- [`../../results/phase2/claim/merged_trials.csv`](../../results/phase2/claim/merged_trials.csv)

## Hinh da co lien quan

- [Heatmap do tin cay compact](../../results/phase1/guides/assets/figures/reliability_heatmap.png)
- [`D_min` theo kich thuoc dan](../../results/phase1/guides/assets/figures/f2_dmin_vs_n.png)
- [Chi phi theo so cho](../../results/phase1/guides/assets/figures/f3_cost_vs_d.png)
- [So sanh chi phi bo cuc](../../results/phase2/guides/assets/figures/f4_layout_cost.png)
- [Duong wide voi mot va hai cho](../../results/phase2/guides/assets/figures/f10_wide_bstar_path.png)

## Gioi han va dieu khong khang dinh

- Co so cap claim la `strombom_multi` cua HerdSim, khong phai thuat toan mot nguoi chan da cong bo ma khong sua doi.
- Nhiem vu compact de tao hieu ung tran. Mot cho thanh cong voi moi `N >= 25`, nen du lieu nay khong ho tro mot quy luat so cho tang theo scaling.
- `D_max = 35` nghia la chua thay sup trong luoi da thu. No khong phai gioi han sinh hoc hay van hanh.
- Bo cuc split hoat dong gan giong compact trong phan tich hoan tat. Bao cao tong hop danh dau viec tach cum ban dau can duoc xac nhan them trong generator, nen khong dua ra ket luan co che manh cho split.
- Twin NetLogo duoc dang ky chi cho thay co ban doi, khong chung minh bang nhau tung tick. Registry: [`../../../integrations/netlogo/twins.json`](../../../integrations/netlogo/twins.json).
- Ket qua khong chung minh hieu nang cho that va khong tai tao ket qua dinh luong cua bai bao 2014.
