# Kha nang chan dat tap the: Ke hoach scaling chinh

Giao thuc: `scaling_v2`.

Tai lieu nay la ke hoach khoa hoc. Tai lieu dinh nghia muc tieu nghien cuu, quan he phu thuoc giua cac phase, cau hoi nghien cuu, tieu chi claim, cap bang chung, ngan sach, cong quyet dinh, va gioi han nghien cuu. Tai lieu khong lap lai ly do thiet lap, giai thich bo dieu khien, quyen so huu trien khai, muc tu vung, hay lenh chay.

Tai lieu canonical ho tro:

- [Chuong trinh nghien cuu](herdsim_research_program.md)
- [Muc luc thiet lap va tham chieu](setup/README_vi.md)
- [Thiet lap thi nghiem](setup/experiment_setup_vi.md)
- [Tham chieu tham so](setup/parameter_reference_vi.md)
- [Bang thuat ngu](setup/glossary_vi.md)
- [Huong dan method](methods/README_vi.md)
- [Do tin cay va so sanh](credibility/README_vi.md)
- [Chien luoc chay](experiment_run_strategy.md)
- [Huong dan chay](setup/run_guide_vi.md)
- [Tracker tien do](progress_tracker.md)
- [Phu luc du lieu](../results/summary/data/README_vi.md)

## 1. Muc tieu nghien cuu

Chuong trinh hoi can bao nhieu kiem soat ben ngoai de dan mot tap the mot cach dang tin cay khi kich thuoc dan va cau truc ban dau thay doi, nhung qua trinh nao giai thich nhu cau do, va nhung mau nao chuyen giao giua cac method chan dat.

Dai luong chinh cua nhu cau kiem soat la mien so shepherd kha dung quanh `D_min` va bien overcrowding neu quan sat duoc, trong mot nhiem vu, nguong tin cay, ngan sach thoi gian, bo cuc, method, va dieu kien thong tin co dinh. `D_min` khong phai thuoc tinh noi tai cua mot dan.

Don vi cong bo nho nhat la RQ1, RQ2, RQ3, va giao thuc dong bang. RQ4 lap lai ca ban do kich thuoc va doi sanh cau truc cho cac method transfer bat buoc. RQ5 va RQ7 la nghien cuu tiep theo. RQ6 dung cac ban do bien da hoan tat va khong duoc quyet dinh luoi theo du lieu sau khi chay.

## 2. Ban do cong viec va quan he phu thuoc

| Phase | Vai tro nghien cuu | RQ | Package | Phu thuoc | Dieu kien hoan tat trong ke hoach |
|---|---|---|---|---|---|
| 0 | Dong bang giao thuc chung | S8 | all | Khong | YAML canonical va ke hoach khoa hoc thong nhat |
| 1 | Ban do kich thuoc va regime baseline | RQ2 | A | Phase 0 | Bien baseline da merge, regime, va quyet dinh T1 co dieu kien |
| 2 | Cau truc tai N co dinh | RQ1 | B | Quy tac scout va cua so claim cua Phase 1 | Bien theo bo cuc da merge va so sanh predictor |
| 3 | Doi sanh co che | RQ3 | C | Cell efficient va overcrowding phu hop tu Phase 1 hoac 2 | Kiem dinh trong cung N da dinh truoc, hoac trang thai undefined ro rang |
| 4 | Transfer giua cac method | RQ4 | D | Thiet ke Phase 1 va 2 da co dinh | Ban do kich thuoc va cau truc cho moi method bat buoc |
| 5 | Thay the thong tin | RQ5 | E | Baseline method on dinh va pipeline phan tang | Bien cua cac ladder observation, range, va communication |
| 6 | Fit scaling | RQ6 | F | Ban do bien cap CLAIM | So sanh curve bang leave-one-N-out |
| 7 | Canh bao som | RQ7 | G | Trajectory cap CLAIM co timeseries can thiet | Danh gia AUROC va lead time tren tap holdout |

Quy tac phu thuoc:

1. Phase 0 dung truoc moi run khoa hoc.
2. Phase 1, 2, va 4 dung ban do scout truoc khi reseed claim.
3. Phase 3 la phan tich cac cell doi sanh da thu thap. Phase nay undefined neu regime can thiet khong ton tai.
4. Claim cau truc cua Phase 4 doi ban do cau truc tu moi method bat buoc.
5. Phase 5 gom ba ladder rieng, khong phai tich Descartes.
6. Phase 6 chi fit sau khi co bien.
7. Phase 7 can timeseries cap CLAIM va holdout toan bo N.

## 3. Hop dong ke hoach chung

Gia tri may-doc nam trong [`canonical_grid.yaml`](../configs/canonical_grid.yaml). Y nghia va ly do cua tham so nam trong [tham chieu tham so](setup/parameter_reference_vi.md) va [thiet lap thi nghiem](setup/experiment_setup_vi.md).

Ke hoach khoa cac rang buoc sau:

- Nhiem vu: `drive_to_goal`, chi thanh cong khi moi sheep den dich truoc deadline.
- Nguong tin cay chinh: `theta = 0.90`; cung bao cao 0.50 va 0.70.
- Method baseline: `strombom_multi`.
- Tap transfer bat buoc: `strombom_multi`, `kubo`, va `fat`.
- Method transfer khuyen nghi nhung khong nam trong tap toi thieu: `communication_free`.
- Luoi kich thuoc dan: `{5, 10, 25, 50, 75, 100, 150, 200, 300, 400}`.
- Luoi so shepherd: `{1, 2, 3, 4, 6, 10, 15, 20, 25, 35}`.
- Bo cuc: `compact`, `wide`, `split`, va `outlier_rich`.
- Kich thuoc cau truc: `{50, 100, 200}`.
- Kich thuoc thong tin: `{100, 200}`.
- Deadline: `T0 = 10000`; `T1 = 20000` co dieu kien.
- Danh sach seed khoa tu master seed 2026.
- Do sau scout: 30 seed moi cell duoc chon.
- Do sau claim: thong thuong 100 seed moi cell duoc chon.
- Bootstrap: 1000 lan resample seed.

Hieu ung theo so dog duoc do bang buoc cuc bo cua luoi. Nghien cuu khong phan giai duoc chenh lech nho hon mot buoc cuc bo cua luoi D da thu.

### Quy tac bien va regime

Dat `R(m, tau, N, D, T, X0, I)` la xac suat thanh cong tren cac seed da khoa.

| Dai luong | Dinh nghia ke hoach |
|---|---|
| `D_min` | D nho nhat da thu voi `R >= theta` |
| `D_overcrowd` | D nho nhat sau `D_min` ma D do va D ke tiep trong luoi deu thap hon theta |
| `D_max` | D tin cay lon nhat duoi `D_overcrowd`; khi khong co overcrowding, la D tin cay lon nhat da thu va co the chi la tran luoi |
| `B*` | `(D, T)` tin cay co trung vi duong di shepherd nho nhat; neu bang nhau, chon D nho hon roi thoi gian thanh cong nhanh hon |
| Hard failure | Khong co D da thu nao dat theta |
| Under-resourced failure | `R < theta` duoi `D_overcrowd` |
| Efficient operation | `R >= theta` va trung vi duong di duoi nguong wasteful |
| Wasteful overspend | `R >= theta` va trung vi duong di cao hon `B*` it nhat 20 phan tram; cung bao cao 10 va 30 phan tram |
| Overcrowding collapse | `R < theta` tai hoac tren `D_overcrowd` |

`D_max` bang 35 khi khong co `D_overcrowd` la tran luoi da thu, khong phai diem collapse da do.

## 4. Cap bang chung va ngan sach du kien

| Cap | Muc dich | Do sau du kien | Duoc dung cho claim |
|---|---|---:|---|
| SMOKE hoac Pilot | Kiem tra path, metric, host, va resume | Luoi chan doan nho, thong thuong 5 seed | Khong |
| SCOUT | Lap ban do rong va chon cua so chinh xac | 30 seed | Chi lap ke hoach va chan doan |
| CLAIM | Uoc luong bien da chon va dai luong claim | Thong thuong 100 seed | Co, sau khi kiem tra provenance va tai lieu run |
| T1 | Thu deadline dai hon tren cell overcrowding da phat hien | 100 seed | Co, chi khi trigger ton tai |

Voi moi method, bo cuc, va N, ke hoach claim chon:

1. `D_min` tu scout, cung D truoc va sau trong luoi.
2. Khi hai gia tri D lien tiep xac lap mot onset overcrowding ung vien, chon hai gia tri do va D tin cay cuoi.
3. Neu khong D nao dat theta, chon hai gia tri D lon nhat da thu.

Dong claim thay dong scout trong cell da reseed. Khong bao gio cong chong dong scout va claim cua cung cell. Cell khong duoc chon giu do sau scout. Bootstrap resample seed trong moi D; lan lay mau khong co `D_min` van bi censor ben phai tren luoi da thu. Neu khoang `D_min` trai qua hon mot buoc luoi D, nang cua so do len 200 seed truoc khi dung cho claim cau truc.

### Uoc luong theo ke hoach

Nhung so nay la uoc luong ngan sach, khong phai so da thuc thi:

| Campaign | Uoc luong scout | Uoc luong claim | Ghi chu ke hoach |
|---|---:|---:|---|
| Mot ban do kich thuoc | Khoang 3000 | Toi da khoang 6000 | Uoc luong claim gia dinh toi da sau gia tri D moi N |
| Mot doi sanh cau truc | Khoang 3600 | Toi da khoang 7200 | Ba N, bon bo cuc, toan bo luoi D cho scout |
| Core baseline | Khoang 20000 tong cong | Da tinh ben trong | Kich thuoc, T1 co dieu kien, va cau truc, lam tron de lap ke hoach |
| Moi method transfer bat buoc | Lap lai ngan sach kich thuoc va cau truc | Tinh lai sau scout | Cua so claim phu thuoc scout cua method do |

Cong viec thuc te phai doc tu artifact status va provenance, khong suy ra tu cac uoc luong nay.

## 5. Cau hoi nghien cuu va phep thu du kien

### RQ1: Cau truc

`D_min` co thay doi giua cac bo cuc ban dau tai N co dinh khong?

Dung N trong `{50, 100, 200}`, ca bon bo cuc, va toan bo luoi D. So sanh `D_min` theo buoc luoi. So sanh model `(N, D)` voi model dung them bo cuc va state chi do trong 100 tick dau. Holdout toan bo N. Khong dung thong ke toan trial lam predictor.

### RQ2: Kich thuoc va regime van hanh

Bien shepherd tin cay va regime van hanh thay doi theo N nhu the nao?

Lap ban do `R(N, D)` tai T0 cho method baseline va bo cuc compact. Uoc luong bien va nhan regime theo quy tac chung. Chi chay T1 cho cell duoc chon boi trigger overcrowding quan sat tu scout hoac claim.

### RQ3: Co che

Chu ky co che nao da dinh truoc phan biet cell efficient va overcrowding tai cung N?

Dung mot trung vi moi cell `(N, D)`, kiem dinh rank, va hieu chinh Holm tren cac gia thuyet.

| Gia thuyet | Chu ky bat buoc |
|---|---|
| Interference | Trung vi `I_dir` cao hon trong cell overcrowding |
| Induced fragmentation | Ti le thanh phan lien thong lon nhat thap hon trong cell overcrowding |
| Coverage saturation | Trong cell tin cay, trung vi coverage tren 0.5, mien theo D duoi 0.1, va trung vi path tang; curve gan 0 khong phai saturation |
| Redundant effort | Trung vi path cao hon ma reliability khong tang |

RQ3 khong them luoi moi. Neu mot method khong co nhan overcrowding, doi sanh co che undefined cho method do.

### RQ4: Tinh tong quat giua cac method

Nhung mau bien, regime, va cau truc nao chuyen giao giua ba method bat buoc?

Lap lai ban do kich thuoc va doi sanh cau truc cho `kubo` va `fat`, roi so sanh voi `strombom_multi`.

| Thuoc tinh | Shared | Shifted | Absent |
|---|---|---|---|
| `D_min` | Cung D da thu | D da thu khac | Mot ben khong co `D_min` |
| Overcrowding | Co o ca hai va D/N trong he so 1.5 | Co o ca hai voi khoang cach lon hon | Khong co o ca hai |
| `I_dir` | `r(I_dir, success) < -0.3` o ca hai | Mau dau cung huong nhung do lon khac | Thieu mau co y nghia bat buoc |
| Coverage saturation | Quy tac saturation dung o ca hai | Dung o mot ben | Khong dung o ca hai |

Chi dien dong transfer phu thuoc state khi moi method duoc so sanh co run cau truc bat buoc.

### RQ5: Thong tin so voi so shepherd

Observation, sensing range, hoac communication phong phu hon co lam giam `D_min` tai reliability co dinh khong?

Dung N trong `{100, 200}`. Thu ladder observation `bearing_only`, `local_positions`, `global`; he so range `0.5, 1, 1.5, 2` lan `r_s` cua method; va ladder communication `none`, `neighbour_broadcast`, `global_shared`. Voi `strombom_multi`, thong tin chia se la hop cua sheep duoc cam nhan, khong phai ground truth uu tien tu simulator.

### RQ6: Fit scaling

Curve du kien nao du doan N holdout tot nhat, va mot power law duy nhat co du khong?

So sanh cac ung vien constant, linear, power `A * N^alpha`, va two-piece linear theo don vi so dog. Chon bang RMSE leave-one-N-out. Chi bao cao log slope trong mot mien N va bo cuc duoc noi ro.

### RQ7: Canh bao som

State gan day co du doan failure sau nay tot hon chi N va D khong?

Tai tick 1000 den 8000, buoc 200, chi dung feature tu `(t - 200, t]`. Gan nhan failure trong 500 tick tiep theo chi khi horizon van nam trong T0. Train tren cac N khac. Lead time duoc do tu lan vuot nguong training dau den failure va co the lon hon 500 tick.

## 6. Tieu chi ho tro claim

Verdict la `UNEVALUATED`, `SUPPORTED`, `REJECTED`, hoac `INCONCLUSIVE`. Mot phan tich co dieu kien khong the chay vi trigger vang mat duoc danh dau `SKIPPED` trong trang thai run va giai thich trong tracker. Chi duoc gan verdict tu bang chung cap CLAIM.

| Claim | RQ | Duoc ho tro khi |
|---|---|---|
| C1a | RQ1 | Voi it nhat mot N, `D_min` khac it nhat mot buoc luoi D giua cac bo cuc tai theta 0.90 |
| C1b | RQ1 | Model state co negative log-likelihood leave-one-N-out thap hon model `(N, D)` |
| C2a | RQ2 | Method baseline co `D_overcrowd` tai theta 0.90 cho it nhat mot N |
| C2b | RQ2 | It nhat mot D tren `D_overcrowd` van duoi theta tai T = 20000 |
| C3 | RQ3 | Tai N co dinh, cell overcrowding va efficient khac nhau ve `I_dir` va/hoac fragmentation voi rank `p < 0.05` sau hieu chinh Holm |
| C4 | RQ4 | `D_min` hoac overcrowding shared tren ba method bat buoc; dong cau truc can them tat ca run cau truc |
| C5a | RQ5 | Mot buoc ladder lam giam `D_min` it nhat mot buoc luoi D tai N trong `{100, 200}` |
| C5b | RQ5 | Buoc ladder thu hai tiet kiem it dog hon buoc dau |
| C6a | RQ6 | Power co RMSE leave-one-N-out cao hon piecewise hoac curve rieng theo bo cuc |
| C6b | RQ6 | Slope cua log `D_min` theo log N duoi 1 trong mien N va bo cuc da neu |
| C7a | RQ7 | AUROC state holdout cao hon baseline `(N, D)` holdout |
| C7b | RQ7 | It nhat 30 phan tram trial failure co lead time it nhat 500 tick |

Nhung tieu chi nay chi ho tro phat bieu trong giao thuc da thu. Chung khong ho tro quy luat pho quat, nhiem vu chua thu, hieu qua ngoai thuc dia, hay chenh lech so dog duoi mot buoc luoi.

## 7. Trang thai thuc thi, khong phai ket qua khoa hoc

Muc nay ghi cong viec du kien da chay hay chua. Muc nay khong neu effect size, gia tri bien, hay dien giai khoa hoc. [Tracker tien do](progress_tracker.md) quan ly trang thai run va verdict hien tai. [Run ledger](../results/summary/data/run_ledger_vi.md) quan ly so da thuc thi va provenance.

Trang thai duoc ghi vao ngay 2026-10-06:

| Phase | Trang thai run | Ghi chu so da thuc thi |
|---|---|---|
| 0 | DONE | Giao thuc da dong bang |
| 1 | DONE; T1 co dieu kien SKIPPED | Scout 3000 dong; claim reseed 2200 dong; T1 khong chay vi trigger chon zero cell |
| 2 | DONE | Scout 3600 dong; claim reseed 2400 dong |
| 3 | SKIPPED | Phan tich co che co dieu kien khong co doi sanh overcrowding du dieu kien |
| 4 | DONE cho campaign kich thuoc va cau truc bat buoc cua Kubo va FAT | So scout, claim, va merge chinh xac nam trong run ledger |
| 5 | TODO | Khong claim campaign information-ladder da hoan tat |
| 6 | DONE cho package fit baseline da du kien | Chi la trang thai phan tich |
| 7 | TODO | Phan tich canh bao som chua chay |

`DONE`, `SKIPPED`, va `TODO` chi mo ta trang thai thuc thi. Phase hoan tat co the cho claim bi reject hoac inconclusive. Phase co dieu kien bi skip co nghia trigger dinh truoc vang mat, khong co nghia da quan sat mot ket qua khoa hoc tai dieu kien khong chay.

## 8. Cong quyet dinh tuong lai

| Cong | Bang chung kiem tra | Quyet dinh |
|---|---|---|
| G1 Tinh nhat quan giao thuc | YAML canonical, protocol da resolve, va ke hoach | Dung neu gia tri dong bang khac nhau; tao version cho thay doi giao thuc co chu dich |
| G2 Chat luong scout | Hoan tat, ban do reliability, va provenance | Dung va sua ban do hong truoc khi lap ke hoach claim |
| G3 Do chinh xac cua so claim | Khoang bootstrap cua `D_min` | Nang cua so da chon len 200 seed khi khoang trai qua hon mot buoc luoi D |
| G4 Trigger T1 | Hai D lien tiep sau bien duoi theta | Chi chay T1 tren cell overcrowding da chon; neu khong, ghi `SKIPPED` |
| G5 Dieu kien co che | Cell efficient va overcrowding tai cung N | Chi chay RQ3 noi doi sanh matched ton tai |
| G6 Day du transfer | Ban do kich thuoc va cau truc cho moi method bat buoc | Khong dien claim transfer cau truc day du truoc khi moi ban do ton tai |
| G7 Mo rong cau truc | Ban do claim cau truc ba kich thuoc | Them N = 300 va 400 chu yeu neu ca bon bo cuc van o san `D_min`; neu khong, mo rong la tuy chon |
| G8 Campaign thong tin | Baseline on dinh va protocol ladder rieng | Chay observation, range, va communication thanh cac campaign phan tang rieng |
| G9 Canh bao som | Timeseries cap CLAIM va ca hai lop outcome | Khong bao cao AUROC hoac lead time neu khong co du lieu holdout du dieu kien |
| G10 Intended velocity E1 | Bang chung cap CLAIM ve spike `I_dir` do wall | Giu E1 chua xay dung tru khi nhu cau chan doan duoc chung minh |
| G11 Parity ben ngoai | Giao thuc matched giua engine va tolerance dinh truoc | Khong claim parity NetLogo dinh luong truoc khi dat yeu cau credibility |

## 9. Pham vi va nguy co

| Nguy co hoac gioi han | Phan hoi trong ke hoach |
|---|---|
| Mot nhiem vu mo phong | Gioi han ket luan trong `drive_to_goal`; nhiem vu thu hai la cong viec sau |
| Phu thuoc method | Yeu cau RQ4 truoc phat bieu tong quat cho method |
| Confounding bo cuc va state | Dung N matched va doi sanh bo cuc dinh truoc |
| Luoi D roi rac | Bieu dien hieu ung theo buoc luoi cuc bo va giu censor tren luoi |
| Bien reliability mem | Dung seed khoa, cua so claim, khoang bootstrap, va cong chinh xac 200 seed |
| Phan tich co dieu kien | Danh dau cong viec thieu trigger la undefined hoac skipped, khong coi la null do duoc tai dieu kien khong chay |
| Quy uoc thoi gian giua method | Tranh dien giai vat ly truc tiep cua tick tho giua cac ho controller |
| Collect switch Strombom rong hon dich | Khong dien giai failure cua no la packing failure |
| Bo dieu khien mo phong | Khong claim ngoai thuc dia, nong trai, hay gia tri sinh hoc |
| Twin NetLogo va ban nhap 2025 | Coi la lop bang chung rieng; theo tai lieu credibility |
| Tran luoi | Khong dien giai D = 35 la gioi han vat ly |
| Do chinh xac chon loc | Giu cap cua cell sau merge va khong cong chong dong scout va claim |

San mac dinh cua ung dung, sheep model, va dog force law nam ngoai pham vi sua doi cua giao thuc nay. Gioi han chi tiet va bien validation nam trong [do tin cay va so sanh](credibility/README_vi.md).

## 10. Thu tu uu tien nguon va quyen so huu tai lieu

Khi cac nguon khac nhau, dung thu tu sau:

1. [`canonical_grid.yaml`](../configs/canonical_grid.yaml) dinh nghia mac dinh may-doc dong bang cua `scaling_v2`.
2. YAML da resolve trong [`configs/protocols/`](../configs/protocols/) dinh nghia subset cua mot campaign.
3. `protocol.yaml`, `provenance.json`, `manifest.jsonl`, va `status.json` da copy cua run dinh nghia dieu da thuc thi.
4. Ke hoach nay dinh nghia cau hoi nghien cuu, quan he phu thuoc, tieu chi claim, cap bang chung, ngan sach, cong, va pham vi.
5. [Tai lieu thiet lap](setup/README_vi.md) dinh nghia ly do tham so, glossary, cap trien khai, va tham chieu van hanh.
6. [Huong dan method](methods/README_vi.md) dinh nghia dien giai bo dieu khien va gioi han rieng cua method.
7. [Tai lieu credibility](credibility/README_vi.md) dinh nghia bien so sanh va validation.
8. [Chien luoc chay](experiment_run_strategy.md) va [huong dan chay](setup/run_guide_vi.md) dinh nghia muc dich phan tang va lenh.
9. [Tracker tien do](progress_tracker.md) dinh nghia trang thai code, run, va claim hien tai.
10. [Phu luc du lieu](../results/summary/data/README_vi.md) va artifact truc tiep dinh nghia so da thuc thi va bang chung da bao cao.

Ket qua khong bao gio dinh nghia lai ke hoach dong bang. Neu uoc luong ke hoach khac artifact run, giu uoc luong la ke hoach va bao cao artifact la da thuc thi. Neu protocol da copy cua run khac van ban tong quat, protocol da copy va provenance chi phoi dien giai run do.
