# Thiet lap thi nghiem

Giao thuc: `scaling_v2`. Gia tri dong bang nam trong [`scaling/configs/canonical_grid.yaml`](../../configs/canonical_grid.yaml). Quy tac khoa hoc va ly do nam trong [`scaling/docs/main_scaling_plan.md`](../main_scaling_plan.md).

![San scaling](../../results/summary/figures/schematics/vi/arena_overview.svg)

## Nhiem vu va san

Nhiem vu la `drive_to_goal`. Mot trial thanh cong khi moi con cuu nam trong dia dich truoc time limit.

- San lien tuc: 500 x 500 world unit.
- Tam dan luc dau: `(250, 250)`.
- Tam dich: `(370, 250)`.
- Quang duong tam-den-tam: 120 cho moi N.
- Ban kinh dich: `15 * sqrt(N/50)`.
- T0: 10,000 tick roi rac.
- T1 co dieu kien: 20,000 tick.

San vuong 500 chua duoc wide draw 3-sigma co tam voi 180 va tam voi outlier xap xi 174 tai N = 400, con khoang 70 unit. San 150 khong du, san 400 chi con khoang 20 unit, san 1000 them khoang trong khong can thiet. Dich tren duong giua giu le tren va duoi bang nhau. Quang duong 120 nam ngoai compact va qua mot wide sigma. Quang 80 nam trong wide cloud; quang 200 dua mep xa cua dich toi tuong.

Tai N = 50, ban kinh 15 bang dich cua ung dung va lon hon packed radius xap xi 8. Ban kinh 8 co nguy co ket, con 30 lam bai toan de hon. Scale theo can bac hai giu dien tich dich tren moi con cuu khong doi. Switch collect cua Strombom la `r_a * N^(2/3)`, chi thuoc bo dieu khien va khong phai ban kinh dich.

Mac dinh ung dung voi san 150 va dich goc khong thay doi. Protocol scaling chi override san cho cac thi nghiem nay.

![Ban kinh dich](../../results/summary/figures/schematics/vi/goal_radius.svg)

## Factor thi nghiem

Luoi N la `{5, 10, 25, 50, 75, 100, 150, 200, 300, 400}`. N = 5 la san vi nhom nho hon khong co cung dai luong tap the. Luoi day hon gan 100 va co 300, 400 de quan sat vung N lon. Bo 250 va 350 vi moi N them vao can ca mot sweep D.

Luoi D la `{1, 2, 3, 4, 6, 10, 15, 20, 25, 35}`. Buoc mot phu vung frontier D thap; buoc rong hon kiem tra viec them nhieu cho co loi hay co hai. D = 35 la tran luoi da thu, khong phai gioi han vat ly hay nong trai.

Baseline la `strombom_multi`. Tap transfer bat buoc gom `strombom_multi`, `kubo`, va `fat`. `communication_free` duoc khuyen nghi nhung khong thuoc claim toi thieu.

Thi nghiem structure dung N trong `{50, 100, 200}` va bon bo cuc. Cac N nay du lon de split cluster va outlier la cau truc dan co nghia. N duoi 12 chi dung hai split cluster. N = 300 va 400 chi nen them sau map claim ba kich thuoc, chu yeu khi tat ca bo cuc van o san D_min.

Thi nghiem information dung N trong `{100, 200}`. Bo N = 50 vi D_min = 1 khong the giam them mot buoc luoi.

## Bo cuc ban dau

Moi bo cuc dung `initial_spread = 30`.

| Bo cuc | Cach tao | Gate kiem tra |
|---|---|---|
| `compact` | Gaussian, sigma `0.3 * spread = 9` | Cohesion distance thap hon `wide` |
| `wide` | Gaussian, sigma `2.0 * spread = 60` | Cohesion distance cao hon `compact` |
| `split` | Hai cluster neu N < 12, nguoc lai ba; gap it nhat 10 | Largest-component fraction thap hon `compact` |
| `outlier_rich` | Core khoang 80 phan tram; outlier khoang 20 phan tram ngoai `r_a * N^(2/3)` | Outlier count cao hon `compact` |

Compact sigma 9 gan packed flock N = 50. Wide sigma 60 tao contrast cohesion ro va van vua san; sigma 120 khong vua. Split tranh ba subflock qua nho khi N < 12. Ti le outlier 20 phan tram tao nhom thieu so that ma khong thanh dan thu hai. Diem ngoai san hoac trong dich duoc draw lai, khong bi ep len bien.

Measurement radius la 5. No noi neighbor compact thuong cach 2 den 4, nhung khong noi gap split it nhat 10.

![Bon bo cuc](../../results/summary/figures/schematics/vi/four_layouts.svg)

## Bo dieu khien

`strombom_multi` phoi hop collect va drive. Switch collect dung `r_a * N^(2/3)`. Switch rong hon dich, vi vay failure Strombom khong duoc doc nhu packing failure.

`kubo` dung force lien tuc, sensing cuc bo, tich phan `dt`, va speed clamp. Khong co switch collect/drive. Moi cho ep con cuu trong tam nhin xa dich nhat; dog-dog repulsion trai cac cho ra.

`fat` giu mo hinh cuu Strombom. Moi cho doc lap chon con cuu quan sat xa no nhat va dung lui sau con cuu theo huong ve dich. Phase 1, 2, 4 dung observation `global`.

Hang so va y nghia nam trong [parameter_reference_vi.md](parameter_reference_vi.md).

## Phan tang

![Pipeline phan tang](../../results/summary/figures/schematics/vi/pipeline.svg)

Phan tang danh do chinh xac vao vung gan D_min va overcrowding co the co, thay vi ton 100 seed cho moi cell noi suy.

| Grade | Muc dich | Seed thuong dung | Dung cho claim |
|---|---|---:|---|
| SMOKE hay Pilot | Kiem tra host, path, metric, resume | Luoi nho, thuong 5 | Khong |
| SCOUT | Map toan bo luoi hoac factor | 30 | Chi lap ke hoach va chan doan |
| CLAIM | Gieo lai cua so frontier | 100 | Co, sau tai lieu run |
| T1 | Thu cell overcrowding tai 20,000 tick | 100 | Co, neu co cell |

![Cua so claim](../../results/summary/figures/schematics/vi/claim_window.svg)

Voi moi method, layout, N, planner chon:

1. D_min cua scout va neighbor truoc, sau tren luoi D.
2. Neu hai D lien tiep sau candidate deu duoi theta, chon hai D do va D cuoi van dat theta.
3. Neu khong D nao dat theta, chon hai D lon nhat.

Tai cell duoc gieo lai, row claim thay row scout; khong cong chong. Cell khac giu row scout. Neu bootstrap interval cua D_min rong hon mot buoc luoi, tang cua so do len 200 seed truoc structure claim.

Uoc luong Phase 1 la 3,000 scout trial va toi da khoang 6,000 claim trial. Structure contrast la khoang 3,600 scout va 7,200 claim. Day la so lap ke hoach, can tinh lai sau scout.

## Phase va dependency

| Phase | Muc dich | Dependency |
|---|---|---|
| 0 | Dong bang protocol | Canonical YAML va plan phu hop |
| 1 | Baseline size map | Pilot, scout, claim, T1 tuy dieu kien |
| 2 | Structure ban dau | Scout va claim tai N 50, 100, 200 |
| 3 | Mechanism | Phan tich contrast cell da thu |
| 4 | Transfer controller | Size va structure map cho Kubo, FAT |
| 5 | Information ladder | Observation, range, communication |
| 6 | Scaling fit | Phan tich merged claim map |
| 7 | Early warning | Phan tich can claim timeseries |

Phase 3, 6, 7 chu yeu la phan tich va bi chan cho den khi co merged claim data. Phase 7 con can timeseries. Phase 5 la campaign sau theo cung mau scout/claim.

Ket qua baseline khong co overcrowding cell, nen Phase 1 T1 da duoc lap ke hoach nhung khong chay. Xem [`scaling/results/phase1/t1/README.md`](../../results/phase1/t1/README.md). Khong co T1 nghia la trigger khong xuat hien, khong phai da quan sat ket qua 20,000 tick.

## Cap trien khai va path

| Cap | Trach nhiem | Path |
|---|---|---|
| I1 | Grid run, resume, provenance | `scaling/services/scaling/runner.py` |
| I2 | Frontier, claim window, bootstrap | `analysis/scaling/frontier.py` |
| I3 | Regime | `analysis/scaling/regimes.py` |
| I4 | Metric hinh hoc va spread | `plugins/metrics/` |
| I5 | Generator X0 | `core/x0_generators.py` |
| I6 | State model so voi N,D | `analysis/scaling/predictors.py` |
| I7 | I_dir va coverage | `plugins/metrics/shepherd_interference.py`, `plugins/metrics/shepherd_coverage.py` |
| I8 | Mechanism test | `analysis/scaling/mechanism.py` |
| I9 | Transfer table | `analysis/scaling/transfer.py` |
| I10 | Factor sweep | `scaling/scripts/run_factor_sweep.py`, `analysis/scaling/substitution.py` |
| I11 | Fit | `analysis/scaling/fits.py` |
| I12 | Early warning | `analysis/scaling/early_warning.py` |
| I13 | Canonical config, export | `scaling/configs/canonical_grid.yaml`, `analysis/scaling/export.py` |
| I14 | Parquet timeseries | Output path cua runner |

Thu muc chinh: `analysis/scaling/`, `scaling/services/scaling/`, `scaling/configs/`, `scaling/scripts/`, va `scaling/results/phase{k}/{protocol}/`.

## Gioi han

Khong thay mac dinh san ung dung, mo hinh cuu, hay force law cua cho trong protocol nay. Extension E1 cho intended velocity chua xay cho den khi map cap CLAIM cho thay spike I_dir chi o tuong.

Baseline mot minh khong tao duoc quy luat chung cho moi method. Ket qua thuoc mot nhiem vu mo phong, do phan giai tick roi rac, va luoi da thu.
