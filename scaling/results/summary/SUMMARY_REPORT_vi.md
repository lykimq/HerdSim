# Mot dan cuu can bao nhieu cho?

## 1. Pham vi va tinh trang

Bao cao nay chi gom ket qua thuc nghiem cua cac Giai doan **1**, **2**, va **4** da hoan tat trong `scaling_v2`.

| Cau hoi | Bang chung da hoan tat |
|---|---|
| Dan lon hon thi can bao nhieu cho? | Giai doan 1, co so `strombom_multi` tren xuat phat `compact` |
| Cau truc xuat phat co doi cau tra loi khong? | Giai doan 2, co so tren bon bo cuc |
| Ket qua co chuyen sang luat cho khac khong? | Giai doan 4, ban do kich thuoc va cau truc cua `kubo` va `fat` |

| Danh gia | Phat hien | So chinh |
|---|---|---|
| D_min = 1 | Tren luat co so voi xuat phat compact, dan tu 25 den 400 cuu thanh cong tin cay voi mot cho. | Dan 5 va 10 cuu can 2 cho. Tai mot cho, R la 0.07 va 0.24. |
| Lang phi | Khi xuat phat compact da chay duoc, them cho khong giup xong nhanh hon; cho chi di nhieu hon. | Thoi gian xong dien hinh khoang 183 tick; duong moi cho khoang 148 voi N >= 25. Trong 100 o kich thuoc nhan so cho, 88 o lang phi. |
| Khong tai hien | Duong tang manh ve so cho can trong ban thao 2025 khong xuat hien o day. | Ban thao bao khoang 20 den 35 cho voi N >= 200. O day mot cho xong N = 400 trong trung vi 168 tick. |
| Chi doi chi phi | Bo cuc xuat phat tren co so doi thoi gian va duong di, nhung khong doi D_min. | Xuat phat wide ton khoang 11x den 20x thoi gian va 19x den 36x duong so voi compact. Tai N = 200, `outlier_rich` dat khoang 6x thoi gian va 11x duong. |
| Chuyen giao mot phan | Kubo va FAT khong chuyen deu tu co so. | Kubo gan khop co so tren compact nhung chi dat R = 0.47 den 0.54 tren wide. FAT chi dat R >= 0.90 voi N <= 10. |

| Giai doan | Cau hoi | Phuong phap | Bo cuc | Pilot | Scout | Claim |
|---|---|---|---|---:|---:|---:|
| 1 | Ban do kich thuoc | strombom_multi | compact | 150 | 3,000 | 2,200 |
| 2 | Cau truc | strombom_multi | 4 bo cuc | 600 | 3,600 | 2,400 |
| 4a | Chuyen giao: kich thuoc | kubo | compact | khong co | 3,000 | 2,100 |
| 4a | Chuyen giao: kich thuoc | fat | compact | khong co | 3,000 | 2,000 |
| 4b | Chuyen giao: cau truc | kubo | 4 bo cuc | khong co | 3,600 | 4,000 |
| 4b | Chuyen giao: cau truc | fat | 4 bo cuc | khong co | 3,600 | 2,400 |
|  | **Tong mo phong** |  |  |  |  | **35,650** |

Ban merge claim co 30,670 dong. Cac tang pilot, scout va claim da chay co 35,650 dong; o duoc gieo lai bo dong scout khoi merge claim. Claim cau truc Kubo co 4,000 dong, gom 200 seed tai `outlier_rich`, N = 200 voi D trong {1, 2, 3, 4, 6, 10, 15, 20, 25}. Xem [so cai chay](data/run_ledger_vi.md).

Tai lieu chinh tac:

- [Ke hoach nghien cuu](../../docs/main_scaling_plan.md)
- [Thiet lap va tham chieu tham so](../../docs/setup/README_vi.md)
- [Huong dan phuong phap](../../docs/methods/README_vi.md)
- [Do tin cay va doi chieu ban thao](../../docs/credibility/README_vi.md)
- [Phu luc du lieu tao tu dong](data/README_vi.md)

## 2. Giai doan 1: kich thuoc dan

Bang chung: `../phase1/claim/README.md`, `../phase1/claim/packages/a/`, va `../phase1/claim/packages/f/`.

![Hinh 1. Mat ti le thanh cong cua ba bo dieu khien tren xuat phat compact.](figures/f1_reliability_heatmaps.png)

*Hinh 1. Giai doan 1 la bang trai; Kubo va FAT thuoc Giai doan 4. Nguon: `../phase1/claim/packages/a/reliability.csv` va `../phase4/{kubo,fat}_size/claim/packages/a/reliability.csv`.*

| Kich thuoc dan N | D_min | D_max | D_overcrowd | Y nghia |
|---|---|---|---|---|
| 5, 10 | 2 | 35 (tran luoi) | khong | Mot cho khong du tin cay; D = 2 den D = 35 van tin cay |
| 25 den 400 | 1 | 35 (tran luoi) | khong | Mot cho dat R >= 0.90; van tren nguong den D = 35 |

Khoang bootstrap cua moi D_min co so co do rong 0. Nguon: `../phase1/claim/packages/a/frontier.csv`.

| Su kien D_max | Cach doc |
|---|---|
| D_max = 35 voi moi N | Khong quan sat thay overcrowding tren co so |
| Vi sao la 35? | Day la gia tri lon nhat da thu trong {1, 2, 3, 4, 6, 10, 15, 20, 25, 35} |
| 35 khong phai gi | Khong phai diem sup da do hay gioi han tren chung |
| Hard failure? | Khong co o hard failure trong Giai doan 1 co so |

Ti le thanh cong tong tren merge Giai doan 1 la 0.963, voi 169 that bai trong 4,540 dong. That bai tap trung tai mot cho tren hai dan nho nhat.

| O | R tai D = 1 | R tai D = 2 | Nhan that bai chinh |
|---|---:|---:|---|
| N = 5 | 0.07 | 1.00 | oscillation: 93 |
| N = 10 | 0.24 | 1.00 | stuck: 58, oscillation: 18 |

| Che do | So o | Cach doc |
|---|---:|---|
| Lang phi qua muc | 88 | Da tin cay; them cho chi tang duong |
| Hieu qua | 10 | Gan D huu ich |
| Thieu nguon luc | 2 | N = 5 va N = 10 tai D = 1 |

![Hinh 2. Chi phi theo D.](figures/f3_cost_vs_d.png)

*Hinh 2. Thoi gian xong phang trong khi tong duong ti le voi D. Nguon: `../phase1/claim/merged_trials.csv`.*

Thoi gian xong trung vi la 183 tick (p90 = 198). Neu chi tinh luot thanh cong, trung vi la 182 va p90 la 195. Voi N >= 25, duong trung vi moi cho khoang 148 don vi the gioi.

![Hinh 3. D_min theo N, co ban thao 2025 de doi chieu.](figures/f2_dmin_vs_n.png)

*Hinh 3. Nguon: `../phase1/claim/packages/a/frontier.csv`, `../phase4/*/size/claim/packages/a/frontier.csv`, va Bang A3 cua ban thao.*

| N | Strombom | Kubo | FAT | Ban thao 2025 |
|---:|---:|---:|---:|---:|
| 5 | 2 | 3 | 1 | 1 |
| 10 | 2 | 1 | 1 | 1 |
| 25 | 1 | 1 | khong <= 35 | 1 |
| 50 | 1 | 1 | khong <= 35 | 1 |
| 75 | 1 | 1 | khong <= 35 | khong co |
| 100 | 1 | 1 | khong <= 35 | 1 |
| 150 | 1 | 1 | khong <= 35 | 3 |
| 200 | 1 | 1 | khong <= 35 | 20 |
| 300 | 1 | 1 | khong <= 35 | 20 |
| 400 | 1 | 1 | khong <= 35 | 35 |

*D_min tai theta = 0.90 tren xuat phat compact. Kubo tai N = 5 co bootstrap [1, 3]; R la 0.77 tai D = 1, 0.71 tai D = 2, va 0.97 tai D = 6. Nguon: cac tep frontier va `dmin_bootstrap.csv` neu tren.*

D_min co so quan sat chi co hai muc: 2 voi N trong {5, 10}, va 1 voi N >= 25.

| Mo hinh | RMSE leave-one-N-out | Cach doc |
|---|---:|---|
| Hang | 0.44 | Mot D_min phang |
| Tuyen tinh | 0.44 | Duong thang theo N |
| Luy thua | 0.25 | Duong cong log-log muot |
| Tung manh | 0.13 | Hai muc, diem gay tai N = 10 |

![Hinh 4. RMSE leave-one-N-out theo mo hinh.](figures/f8_scaling_rmse_vi.svg)

*Hinh 4. Fit tung manh huong loi vi ma hoa buoc nhay quan sat. Nguon: `../phase1/claim/packages/f/scaling_cv.csv`. Khong the kiem C6b vi khong co dai tang truong de fit.*

## 3. Giai doan 2: cau truc xuat phat

Bang chung: `../phase2/claim/README.md` va `../phase2/claim/packages/b/`.

D_min = 1 cho ca 12 o bo cuc nhan N, va moi khoang bootstrap co do rong 0. Tai D = 1, moi o co R = 1.00. D_max = 35 la tran luoi trong moi o, khong co D_overcrowd.

![Hinh 5. Tong duong trung vi tai D = 1 theo bo cuc.](figures/f4_layout_cost.png)

*Hinh 5. Nguon: `../phase2/claim/merged_trials.csv` tai D = 1.*

| Bo cuc | N | R tai D = 1 | Tick trung vi | so voi compact | Duong trung vi | so voi compact |
|---|---:|---:|---:|---:|---:|---:|
| compact | 50 | 1.00 | 195 | 1.0x | 157 | 1.0x |
| compact | 100 | 1.00 | 204 | 1.0x | 161 | 1.0x |
| compact | 200 | 1.00 | 191 | 1.0x | 144 | 1.0x |
| split | 50 | 1.00 | 195 | 1.0x | 158 | 1.0x |
| split | 100 | 1.00 | 205 | 1.0x | 162 | 1.0x |
| split | 200 | 1.00 | 193 | 1.0x | 144 | 1.0x |
| outlier_rich | 50 | 1.00 | 224 | 1.1x | 209 | 1.3x |
| outlier_rich | 100 | 1.00 | 501 | 2.5x | 554 | 3.4x |
| outlier_rich | 200 | 1.00 | 1,228 | 6.4x | 1,647 | 11.4x |
| wide | 50 | 1.00 | 2,138 | 11.0x | 2,925 | 18.6x |
| wide | 100 | 1.00 | 3,074 | 15.1x | 4,319 | 26.8x |
| wide | 200 | 1.00 | 3,870 | 20.3x | 5,213 | 36.2x |

| Bo cuc | Cach doc thuc nghiem |
|---|---|
| wide | 11x den 20x tick va 19x den 36x duong so voi compact |
| outlier_rich | Tai N = 200, 6.4x tick va 11.4x duong so voi compact |
| split | Trung vi khop compact; fragmentation trung binh khoang 0.99, nen coi la kiem tra thay vi phat hien |
| compact | Moc tham chieu |

Voi xuat phat wide, B* = 2 tai N = 50, 100, va 200. Tong duong trung vi giam tu 2,925 xuong 2,337, tu 4,319 xuong 3,003, va tu 5,213 xuong 3,694. Nguon: `../phase2/claim/packages/b/frontier_by_layout.csv`.

![Hinh 6. Xuat phat wide: duong trung vi tai D = 1 so voi D = 2.](figures/f10_wide_bstar_path_vi.png)

*Hinh 6. Nguon: `../phase2/claim/merged_trials.csv`, bo cuc wide.*

## 4. Giai doan 4: chuyen giao bo dieu khien

Bang chung: `../phase4/README.md`, `../phase4/kubo_structure/claim/README.md`, `../phase4/package_d/`, va `../phase4/kubo_structure/claim/outlier_rich_n200_window.json`.

### Ban do kich thuoc compact

Kubo co D_min = 3 tai N = 5 va D_min = 1 tu N = 10 den 400. D_max = 35 la tran luoi cho moi o kich thuoc, khong co overcrowding. Ti le thanh cong tong la 0.991, va moi that bai deu la timeout.

FAT co D_min = 1 tai N trong {5, 10}; hai o deu co D_max = 35 nhu tran luoi. Voi N >= 25, khong D <= 35 nao dat R >= 0.90, nen D_min va D_max khong xac dinh. Voi N = 50 den 400, R tot nhat theo N la 0.40 den 0.53, con R cua tung o xuong toi khoang 0.17. Khoang mot nua luot FAT kich thuoc that bai: 39% do oscillation va 7% do stuck.

| Truong hop | Truong bien | Cach doc thuc nghiem |
|---|---|---|
| D_max = 35, khong D_overcrowd | Co D_min | Tin cay tai tran luoi; chua do duoc diem sup tren |
| Hard failure | D_min va D_max trong | Khong D da thu nao dat theta |
| Overcrowding that | Co D_overcrowd va D_max duoi 35 | Khong quan sat thay trong cac giai doan da hoan tat |

Nhan Package D kich thuoc gom 8 chia se, 7 dich, va 29 vang. So vang chu yeu den tu cac dong overcrowding vi khong bo dieu khien nao overcrowd tren compact. Nguon: `../phase4/package_d/size/transfer_summary.csv`.

![Hinh 7. Cach cac luot ket thuc tren ban do kich thuoc.](figures/f6_failure_modes_vi.png)

*Hinh 7. Nguon: `failure_mode` trong `merged_trials.csv` claim cua Giai doan 1, Kubo kich thuoc, va FAT kich thuoc.*

### Ban do cau truc

| Bo cuc | N | Strombom | Kubo | FAT |
|---|---:|---:|---:|---:|
| compact | 50 | 1 | 1 | khong (R tot nhat = 0.47) |
| compact | 100 | 1 | 1 | khong (R tot nhat = 0.40) |
| compact | 200 | 1 | 1 | khong (R tot nhat = 0.47) |
| split | 50 | 1 | 1 | khong (R tot nhat = 0.50) |
| split | 100 | 1 | 1 | khong (R tot nhat = 0.47) |
| split | 200 | 1 | 1 | khong (R tot nhat = 0.40) |
| outlier_rich | 50 | 1 | 1 | khong (R tot nhat = 0.10) |
| outlier_rich | 100 | 1 | 1 | khong (R tot nhat = 0.00) |
| outlier_rich | 200 | 1 | 20 | khong (R tot nhat = 0.00) |
| wide | 50 | 1 | khong (R tot nhat = 0.49) | khong (R tot nhat = 0.00) |
| wide | 100 | 1 | khong (R tot nhat = 0.54) | khong (R tot nhat = 0.00) |
| wide | 200 | 1 | khong (R tot nhat = 0.47) | khong (R tot nhat = 0.00) |

*D_min theo bo cuc va bo dieu khien. `khong` nghia la khong D <= 35 nao dat R = 0.90. Nguon: `../phase4/package_d/structure/frontier_by_method_layout.csv`.*

![Hinh 8. R theo D tai N = 200 theo bo cuc.](figures/f5_layout_reliability_curves_vi.png)

*Hinh 8. Nguon: cac tep `merged_trials.csv` claim cau truc.*

| D | So seed | R | R >= 0.90? |
|---:|---:|---:|:---:|
| 1 | 200 | 0.745 | khong |
| 2 | 200 | 0.855 | khong |
| 3 | 200 | 0.835 | khong |
| 4 | 200 | 0.860 | khong |
| 6 | 200 | 0.890 | khong |
| 10 | 200 | 0.875 | khong |
| 15 | 200 | 0.855 | khong |
| 20 | 200 | 0.935 | co |
| 25 | 200 | 0.910 | co |
| 35 | 30 | 0.967 | co |

| Kubo `outlier_rich`, N = 200 | Gia tri |
|---|---|
| D_min | 20 |
| Khoang bootstrap | [2, 20] tu `merged_dmin_bootstrap.csv`, `n_seeds_ref = 200` |
| Overcrowding | khong |
| Bat dinh | Vao D < 20 nam gan 0.90, nen bootstrap co the dat D_min duoi 20 |

![Hinh 9. Kubo outlier_rich N = 200 voi khoang Wilson 95%.](figures/f9_kubo_outlier_rich_n200_vi.png)

*Hinh 9. Nguon: `../phase4/kubo_structure/claim/merged_trials.csv`, `merged_dmin_bootstrap.csv`, va `outlier_rich_n200_window.json`.*

| Phat hien | Cach doc thuc nghiem |
|---|---|
| Kubo + wide | R tot nhat la 0.47 den 0.54; that bai la timeout hoac scatter; them cho nang R ve khoang 0.5 nhung khong toi 0.90 |
| Kubo + outlier_rich, N = 200 | Dich sang D_min = 20, bootstrap [2, 20] |
| Cau truc FAT | Khong bo cuc nao tai N >= 50 dat R = 0.90 |

| Bo dieu khien | I_dir trung binh tai D = 35, N = 100 | I_dir trung binh tren moi D tai N = 100 |
|---|---:|---:|
| Co so (`strombom_multi`) | khoang 0.09 | khoang 0.05 |
| Kubo | khoang 0.15 | khoang 0.10 |
| FAT | khoang 0.48 | khoang 0.40 |

| Kiem tra lien he | Gia tri | Cach doc |
|---|---:|---|
| Pearson r(I_dir, success), merge FAT kich thuoc | khoang -0.87 | Lien he am manh |
| Ket luan nhan qua | khong | Lien he quan sat, khong phai thi nghiem co che co kiem soat |

![Hinh 10. Chi so interference theo D.](figures/f7_interference_vi.png)

*Hinh 10. Nguon: `mean_i_dir` trong cac tep `merged_trials.csv` claim.*

## 5. Tong hop va anh chup claim

| Claim | Phan quyet | Bang chung | Cach doc |
|---|---|---|---|
| C1a | BI BAC BO | Giai doan 2 Package B: D_min = 1 cho bon bo cuc tai N = 50, 100, 200; bootstrap rong 0 | Chi cho co so; cau truc Kubo co dich |
| C1b | KHONG RO | Khong co dich D_min tren co so; Package B bao likelihood NaN | Chi phi van phu thuoc manh vao bo cuc |
| C2a | BI BAC BO | Giai doan 1 Package A: 0 o overcrowding tai theta = 0.90 | Giai doan 4 cung khong co |
| C2b | BO QUA | Khong co o overcrowding de chay T = 20,000 | Khong chay T1 |
| C3 | KHONG RO | Doi chieu co che co so can overcrowding | Co o doi chieu Kubo nhung Package C chua hoan tat |
| C4 | DUOC UNG HO, mot phan | Strombom va Kubo chia se D_min compact voi N >= 25; FAT vang; Kubo wide vang; Kubo `outlier_rich`, N = 200 dich | Chuyen giao phu thuoc dieu kien |
| C6a | DA DANH GIA, yeu | RMSE tung manh 0.13 so voi luy thua 0.25 | Fit chi dung hai muc quan sat {2, 1}; khong phai quy luat scaling |
| C5a/b, C6b, C7a/b | CHUA DANH GIA | Giai doan 5 va 7 chua chay; C6b khong co dai tang truong da neu | Khong co ket luan ket qua |

## 6. Bat dinh, gioi han, va giai doan chua chay

| Tinh trang | Chu de | Gioi han hien tai |
|---|---|---|
| Hieu ung tran | Do tin cay co so | R = 1.00 tai D = 1 tren gan moi o co so, nen kho thay scaling |
| Tran luoi | D_max = 35 | Chua do diem sup tren; hanh vi tren 35 chua biet |
| Hard failure | FAT va Kubo wide | D_min va D_max trong nghia la khong D da thu nao dat 0.90, khong phai da tim thay bien tren |
| Khoang rong | Kubo `outlier_rich`, N = 200 | Uoc diem D_min = 20 tai 200 seed, R = 0.935, nhung bootstrap la [2, 20] |
| Fit yeu | C6a | Hai muc D_min quan sat khong ho tro quy luat scaling chung |
| Chi quan sat | I_dir | r khoang -0.87 khong chung minh interference gay that bai |
| Hanh vi bo sinh chua xac minh | Bo cuc `split` | Chi phi va D_min khop compact; van can xac nhan tach cum tai t = 0 |
| Mot nhiem vu mo phong | Gia tri ben ngoai | Ket qua khong chung minh hieu nang ngoai dong, do trung thuc sinh hoc, hay quy tac nong trai chung |
| Luoi D roi rac | Do phan giai | Khong phan giai duoc khac biet nho hon cac buoc so cho da thu |

Giai doan chua chay:

- Giai doan 3 va C2b bi bo qua vi co so co 0 o overcrowding.
- Giai doan 5 ve cam bien, tam, va giao tiep chua chay.
- Giai doan 7 va Package G ve canh bao som chua chay.
- Ban thao 2025 khong duoc chay lai, va parity dinh luong voi NetLogo chua duoc xac lap.

Noi dung thiet lap, phuong phap, ban thao, NetLogo, provenance, va thuat ngu da bo khoi bao cao nay nam trong cac tai lieu chinh tac lien ket o muc 1. Cac bang thuc nghiem tao tu dong va duong dan nguon nam trong [data/README_vi.md](data/README_vi.md).
