# Chan dan dua tren luc Kubo

## Cam hung tu cong bo

Kubo va cong su (2022) mo hinh hoa cuu va nhieu cho bang tong luc lien tuc, khong dung chuyen Collect/Drive roi rac. Cuu ket hop luc day lang gieng, can huong van toc, ket dinh, va day khoi cho. Moi cho nham con cuu trong tam xa dich nhat, trong khi luc day khoi muc tieu, day khoi dich, va day giua cac cho tao chuyen dong. Luc day giua cho co the xoe doi hinh o sau dan.

Tai lieu: M. Kubo, M. Tashiro, H. Sato, va cong su, "Herd guidance by multiple sheepdog agents with repulsive force," Artificial Life and Robotics 27, 416-427, 2022. DOI: `10.1007/s10015-021-00726-7`.

## Hien thuc HerdSim chinh xac

Bundle `kubo` ket hop:

- `sheep_model=kubo`;
- `dog_controller=kubo_forces`;
- mac dinh 40 cuu va 4 cho khi khong co ghi de thi nghiem.

Phuong phap nay khong dung cuu Strombom va khong co trang thai Collect/Drive.

### Buoc luc cua cuu

Voi moi con cuu, HerdSim tim cuu va cho trong `radius = 60`. Hien thuc tinh:

- trung binh luc day cuu nghich dao binh phuong;
- trung binh huong van toc don vi cua lang gieng dang chay;
- trung binh luc hut don vi ve cuu lang gieng;
- trung binh luc day khoi cho nghich dao lap phuong.

Van toc co trong so dung `K_s1..K_s4 = 10, 0.5, 2, 5000`. Do lon bi chan tai `sheep_speed_max = 5`, va vi tri tang `dt * velocity` voi `dt = 0.05`.

### Buoc luc cua cho

Voi moi cho dang hoat dong co quan sat khong rong:

1. Tao trang thai cuc bo bi gioi han boi quan sat.
2. Giu cuu trong `radius`.
3. Chon con trong tam xa dich nhat.
4. Ket hop luc hut ve muc tieu, day nghich dao lap phuong khoi muc tieu, day khoi dich, va day nghich dao lap phuong khoi cho khac trong tam.
5. Dung `K_f1..K_f4 = 10, 200, 8, 3000`.
6. Chan toc do tai `dog_speed_max = 10` va tang vi tri `dt * velocity`.

Neu quan sat khong co cuu, bo dieu khien de cho dung yen trong tick do. Cuu cap nhat truoc cho trong buoc mo phong. HerdSim con ap dung dich cua scenario, hanh vi bien san, he so dap ung va ket dinh tung ca the, cung pipeline quan sat quanh cac luc nay.

Bang chung hien thuc:

- [`../../../core/methods.py`](../../../core/methods.py)
- [`../../../methods/kubo/config.py`](../../../methods/kubo/config.py)
- [`../../../methods/kubo/forces.py`](../../../methods/kubo/forces.py)
- [`../../../plugins/sheep/kubo.py`](../../../plugins/sheep/kubo.py)
- [`../../../plugins/dogs/kubo_forces.py`](../../../plugins/dogs/kubo_forces.py)

## Thiet lap `scaling_v2`

Kubo la phuong phap chuyen giao Giai doan 4, duoc so sanh voi co so `strombom_multi` tren cung hinh hoc nhiem vu.

- Ban do kich thuoc: compact tren toan luoi `N` va `D`.
- Ban do cau truc: bon bo cuc tai `N = {50, 100, 200}`.
- Quan sat: global.
- Han: `T0 = 10000`.
- Nguong tin cay: `R >= 0.90`.
- Phan tang: 30 seed scout, sau do 100 seed claim trong cua so da chon.
- Do chinh xac bo sung: `outlier_rich`, `N = 200`, `D` trong `{1, 2, 3, 4, 6, 10, 15, 20, 25}` duoc tang len 200 seed. `D = 35` giu 30 seed scout.

Thi nghiem ghi de so ca the mac dinh theo tung o `(N, D)`. Cac gain luc Kubo khong duoc tinh chinh lai theo kich thuoc hay bo cuc.

Bang chung cau hinh:

- [`../../configs/canonical_grid.yaml`](../../configs/canonical_grid.yaml)
- [`../../configs/protocols/phase4_kubo_size_claim.yaml`](../../configs/protocols/phase4_kubo_size_claim.yaml)
- [`../../configs/protocols/phase4_kubo_structure_claim.yaml`](../../configs/protocols/phase4_kubo_structure_claim.yaml)

## Ket qua hoan tat da quan sat

### Ban do kich thuoc compact

- `D_min = 3` tai `N = 5`.
- `D_min = 1` tai moi kich thuoc da thu tu `N = 10` den 400.
- `D_max = 35` la tran luoi trong moi o kich thuoc.
- Khong quan sat thay overcrowding.
- Thanh cong toan merge kich thuoc Kubo la 0.991, va moi that bai duoc ghi la timeout.

Vi vay Kubo chia se bien compact voi co so tai `N >= 25`, nhung khong chia se moi ket qua dan nho.

### Cau truc ban dau

- Compact va split: `D_min = 1` tai `N = 50, 100, 200`.
- `outlier_rich`: `D_min = 1` tai `N = 50, 100`.
- `outlier_rich`, `N = 200`: uoc luong diem `D_min = 20`.
- Wide: hard failure o ca ba kich thuoc. Do tin cay tot nhat tren luoi cho khoang 0.47 den 0.54, duoi 0.90.

Voi `outlier_rich`, `N = 200`, cac o 200 seed cho `R = 0.935` tai `D = 20` va `R = 0.910` tai `D = 25`. Khoang bootstrap cua `D_min` la `[2, 20]` vi vai muc cho thap nam gan nguong. Uoc luong diem phai luon duoc bao cung khoang rong nay.

Bang chung:

- [`../../results/phase4/kubo_size/claim/packages/a/frontier.csv`](../../results/phase4/kubo_size/claim/packages/a/frontier.csv)
- [`../../results/phase4/kubo_structure/claim/packages/b/frontier_by_layout.csv`](../../results/phase4/kubo_structure/claim/packages/b/frontier_by_layout.csv)
- [`../../results/phase4/kubo_structure/claim/merged_dmin_bootstrap.csv`](../../results/phase4/kubo_structure/claim/merged_dmin_bootstrap.csv)
- [`../../results/phase4/kubo_structure/claim/outlier_rich_n200_window.json`](../../results/phase4/kubo_structure/claim/outlier_rich_n200_window.json)
- [`../../results/phase4/package_d/structure/frontier_by_method_layout.csv`](../../results/phase4/package_d/structure/frontier_by_method_layout.csv)

## Hinh da co lien quan

- [Heatmap compact cua ba phuong phap](../../results/phase4/guides/assets/figures/f1_reliability_heatmaps.png)
- [Duong do tin cay theo bo cuc](../../results/phase4/guides/assets/figures/f5_layout_reliability_curves.png)
- [So sanh kieu that bai](../../results/phase4/guides/assets/figures/f6_failure_modes.png)
- [Kubo `outlier_rich`, `N = 200`](../../results/phase4/guides/assets/figures/f9_kubo_outlier_rich_n200.png)

## Gioi han va dieu khong khang dinh

- Cung `D_min` tren compact khong co nghia la chuyen giao toan bo. Kubo khong dat 90% trong moi o wide va dich manh tai `outlier_rich`, `N = 200`.
- Khoang bootstrap `[2, 20]` lam bien `D_min = 20` bat dinh ve phia thap.
- Hard failure tren wide nghia la khong `D <= 35` nao dat nguong. No khong chung minh them cho luon lam Kubo te hon.
- Tick Kubo khong so sanh vat ly truc tiep voi tick ho Strombom vi Kubo dung tich phan `dt`.
- San co bien, hinh hoc sinh, dia dich, va so ca the cua HerdSim la lua chon nghien cuu, khong phai khang dinh ve thiet lap chinh xac cua bai bao.
- Twin NetLogo Kubo co trong registry, nhung bao cao scaling hoan tat khong co ket qua parity dinh luong. Registry: [`../../../integrations/netlogo/twins.json`](../../../integrations/netlogo/twins.json).
- Ket qua khong tai tao cac bang so cua bai bao va khong chung minh hieu nang ngoai nhiem vu mo phong nay.
