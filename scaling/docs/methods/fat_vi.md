# FAT: nham ca the xa nhat

## Cam hung tu cong bo

FAT duoc truyen cam hung boi quy tac chan dan voi camera cuc bo trong Tsunoda va cong su (2018): tac dong len ca the xa nhat trong tap ma nguoi chan nhin thay, khong can toa do toan dan.

HerdSim khong hien thuc day du mo hinh camera, xu ly sai so vi tri, dong luc cuu, luat dieu huong, hay hieu chinh thi nghiem cua bai bao. Vi vay phan cong bo chi la cam hung cho cach chon muc tieu, khong phai khang dinh tai tao toan bo mo hinh.

Tai lieu: Y. Tsunoda va cong su, "Analysis of local-camera-based shepherding navigation," Advanced Robotics 32(23), 2018. DOI: `10.1080/01691864.2018.1539410`.

## Hien thuc HerdSim chinh xac

Bundle `fat` ket hop:

- `sheep_model=strombom`;
- `dog_controller=fat`;
- mac dinh hai cho khi khong co ghi de thi nghiem.

Cuu dung quy tac an co, tao dan, day, va dich chuyen co dinh cua Strombom trong HerdSim. Bo dieu khien cho khong co chuyen Collect/Drive va khong kiem tra ket dinh toan dan.

Voi moi cho dang hoat dong trong moi tick:

1. Doc quan sat cua cho sau cac bo loc che do quan sat va cam bien.
2. Neu khong thay cuu, de cho dung yen.
3. Chon con cuu quan sat duoc xa chinh con cho nhat.
4. Dat dich cach `r_a` sau con cuu tren tia di tu dich qua cuu.
5. Di ve dich do voi `shepherd_speed` va nhieu goc Strombom.
6. Dung neu co cuu trong view dang dung gan hon `shepherd_stop_multiple * r_a`.

Moi cho chon doc lap. FAT khong co luc day giua cho, dam phan gan muc tieu, hay khoang cach doi hinh ro rang. "Xa nhat" la xa con cho nhat, khac Collect Strombom (xa tam dan nhat) va Kubo (xa dich nhat).

Bang chung hien thuc:

- [`../../../core/methods.py`](../../../core/methods.py)
- [`../../../plugins/dogs/fat.py`](../../../plugins/dogs/fat.py)
- [`../../../plugins/sheep/strombom.py`](../../../plugins/sheep/strombom.py)
- [`../../../methods/strombom/heuristics.py`](../../../methods/strombom/heuristics.py)
- [`../../../methods/strombom/config.py`](../../../methods/strombom/config.py)

## Thiet lap `scaling_v2`

FAT la phuong phap chuyen giao Giai doan 4 tren cung nhiem vu va luoi voi Kubo va co so.

- Ban do kich thuoc: compact tren toan luoi kich thuoc va so cho.
- Ban do cau truc: bon bo cuc tai `N = {50, 100, 200}`.
- Quan sat: global.
- Giao tiep: bo dieu khien FAT khong them phoi hop.
- Han: `T0 = 10000`.
- Nguong tin cay: `R >= 0.90`.
- Phan tang: 30 seed scout, sau do 100 seed claim trong cua so da chon.

Thiet lap global rat quan trong. Du y tuong chon muc tieu den tu cam bien cuc bo, cac Giai doan 1, 2, va 4 hoan tat cho moi cho FAT thay toan dan. Cac ket qua nay khong kiem tra gioi han thong tin camera cuc bo. Thi nghiem che do quan sat duoc lap ke hoach cho Giai doan 5 nhung chua chay.

Bang chung cau hinh:

- [`../../configs/canonical_grid.yaml`](../../configs/canonical_grid.yaml)
- [`../../configs/protocols/phase4_fat_size_claim.yaml`](../../configs/protocols/phase4_fat_size_claim.yaml)
- [`../../configs/protocols/phase4_fat_structure_claim.yaml`](../../configs/protocols/phase4_fat_structure_claim.yaml)

## Ket qua hoan tat da quan sat

### Ban do kich thuoc compact

- `D_min = 1` tai `N = 5` va `N = 10`.
- Voi moi `N >= 25`, khong so cho nao den 35 dat `R >= 0.90`.
- Cac o nay la hard failure: `D_min` va `D_max` khong xac dinh, khong phai 0 va cung khong phai 35.
- Do tin cay tot nhat theo kich thuoc voi `N = 50` den 400 khoang 0.40 den 0.53.
- Khoang nua cac lan chay kich thuoc FAT that bai. Bao cao tong hop gan khoang 39% toan bo trial cho oscillation va 7% cho stuck.

### Cau truc ban dau

FAT khong dat 90% trong bat ky o cau truc nao tai `N = 50, 100, 200`.

- Compact co `R` tot nhat: 0.47, 0.40, 0.47 voi `N = 50, 100, 200`.
- Split co `R` tot nhat: 0.50, 0.47, 0.40.
- `outlier_rich` co `R` tot nhat: 0.10, 0.00, 0.00.
- Wide co `R` tot nhat: 0.00 o ca ba kich thuoc.

Bao cao tong hop cung ghi nhan lien he am manh giua nhiu huong FAT va thanh cong tren merge kich thuoc, voi Pearson `r` khoang `-0.87`. Day la quan sat, khong chung minh nhiu la nguyen nhan that bai.

Bang chung:

- [`../../results/phase4/fat_size/claim/packages/a/frontier.csv`](../../results/phase4/fat_size/claim/packages/a/frontier.csv)
- [`../../results/phase4/fat_size/claim/merged_trials.csv`](../../results/phase4/fat_size/claim/merged_trials.csv)
- [`../../results/phase4/fat_structure/claim/merged_trials.csv`](../../results/phase4/fat_structure/claim/merged_trials.csv)
- [`../../results/phase4/package_d/structure/frontier_by_method_layout.csv`](../../results/phase4/package_d/structure/frontier_by_method_layout.csv)

## Hinh da co lien quan

- [Heatmap compact cua ba phuong phap](../../results/phase4/guides/assets/figures/f1_reliability_heatmaps.png)
- [Duong do tin cay theo bo cuc](../../results/phase4/guides/assets/figures/f5_layout_reliability_curves.png)
- [So sanh kieu that bai](../../results/phase4/guides/assets/figures/f6_failure_modes.png)
- [Nhiu huong theo so cho](../../results/summary/figures/f7_interference.png)

## Gioi han va dieu khong khang dinh

- Day la bo dieu khien FAT toi gian cua HerdSim tren cuu Strombom, khong phai mo hinh day du cua Tsunoda va cong su.
- Ket qua hoan tat dung quan sat global. Chung khong do che khuat camera, dieu khien chi co goc, sai so vi tri, hay phuc hoi khi mat dau vet.
- Hard failure nghia la khong so cho da thu nao dat thanh 90% truoc `T0`. No khong chung minh FAT khong the hoat dong voi `D` lon hon, timeout khac, hay nhiem vu khac.
- Tang so cho khong cuu duoc dan lon tren luoi nay. Quan sat do khong tach duoc co che nhan qua.
- Tuong quan nhiu khong phai phep thu nhan qua co kiem soat.
- FAT khong co twin NetLogo trong registry: [`../../../integrations/netlogo/twins.json`](../../../integrations/netlogo/twins.json).
- Ket qua khong chung minh hieu nang ngoai dong va khong tai tao ket qua dinh luong cua bai bao 2018.
