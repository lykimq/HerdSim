# Tham chieu tham so

Gia tri o day den tu [`scaling/configs/canonical_grid.yaml`](../../configs/canonical_grid.yaml) hoac mac dinh controller trong cac module cau hinh duoc lien ket. Protocol YAML co the chon tap con nhung khong duoc ngam dinh nghia lai canonical protocol.

## Protocol cot loi

| Tham so | Gia tri | Y nghia va ly do |
|---|---|---|
| `protocol_id` | `scaling_v2` | ID provenance cua bo quy tac khoa |
| `frozen_on` | `2026-09-22` | Ngay dong bang |
| `task` | `drive_to_goal` | Moi cuu vao dia dich truoc deadline |
| `world_width`, `world_height` | 500, 500 | San vuong du cho wide va outlier-rich |
| tam dan | `(250, 250)` | Tam san |
| `goal_center` | `(370, 250)` | Cach tam dan 120 theo phuong ngang |
| `drive_length` | 120 | Quang duong task co dinh |
| `goal_radius_at_n50` | 15 | Ban kinh dich tai N = 50 |
| ban kinh dich | `15 * sqrt(N/50)` | Giu dien tich dich tren moi cuu khong doi |
| `initial_spread` | 30 | Scale co so cho layout |
| `measurement_radius` | 5 | Ban kinh lien thong cua fragmentation |
| `reliability_theta` | 0.90 | Nguong tin cay chinh |
| `reliability_sensitivity` | 0.50, 0.70 | Nguong bao cao them, khong phai bar D_min |
| `baseline_method` | `strombom_multi` | Controller baseline |
| `transfer_methods` | baseline, `kubo`, `fat`, `communication_free` | Danh sach transfer day du |
| `required_transfer_methods` | baseline, `kubo`, `fat` | Tap claim toi thieu |
| `flock_sizes` | 5, 10, 25, 50, 75, 100, 150, 200, 300, 400 | Luoi N |
| `shepherd_counts` | 1, 2, 3, 4, 6, 10, 15, 20, 25, 35 | Luoi D |
| `structure_flock_sizes` | 50, 100, 200 | N cho structure |
| `rq5_flock_sizes` | 100, 200 | N cho information |
| `x0_families` | compact, wide, split, outlier_rich | Factor layout |
| `time_limit_t0` | 10,000 | Deadline chinh |
| `time_limit_t1` | 20,000 | Deadline dai chi cho overcrowding |
| `scout_seeds` | 30 | Do sau map rong |
| `claim_grade_seeds` | 100 | Do sau cua so claim |
| `master_seed` | 2026 | Goc danh sach seed co dinh |
| `bootstrap_resamples` | 1,000 | So lan resample seed |
| `predictor_window_ticks` | 100 | Cua so feature dau trial |
| `wasteful_effort_tolerance` | 0.20 | Bar path du thua mac dinh |
| `wasteful_effort_sensitivity` | 0.10, 0.30 | Bar sensitivity |

Tai R = 0.90, 30 seed co standard error khoang 0.055 va 100 seed khoang 0.03. Interval xap xi cua R tai 100 seed la cong tru 0.06. Day la uncertainty cua R, khong truc tiep la uncertainty cua D_min.

## Layout

| Tham so | Gia tri | Y nghia |
|---|---:|---|
| compact sigma | 9 | `0.3 * initial_spread` |
| wide sigma | 60 | `2.0 * initial_spread` |
| so split cluster | 2 neu N < 12, nguoc lai 3 | Tranh nhom ba qua nho |
| split gap toi thieu | 10 | `2 * measurement_radius` |
| outlier core | khoang 80 phan tram | Dan chinh |
| outlier | khoang 20 phan tram | Ngoai `r_a * N^(2/3)` |

Diem ngoai san hoac trong dich duoc draw lai.

## `strombom_multi`

| Tham so | Gia tri | Y nghia |
|---|---:|---|
| `r_a` | 2 | Do dai tuong tac cuu, cung dung trong collect threshold |
| `r_s` | 65 | Khoang cach cuu phan ung voi cho; base sensing range |
| `sheep_speed` | 1.0 | Dich chuyen cuu moi tick |
| `shepherd_speed` | 1.5 | Dich chuyen cho moi tick |
| `noise_strength` | 0.3 | Do manh angular process noise |
| `inertia` | 0.5 | Trong so huong truoc cua cuu |
| collect threshold | `r_a * N^(2/3)` | Ban kinh chuyen collect sang drive |

Coverage radius la `sensing_range` neu factor da set, neu khong la `r_s` cua method. No khong phai sheep-sheep repulsion distance.

## `kubo`

| Tham so | Gia tri | Y nghia |
|---|---:|---|
| `radius` | 60 | Local sensing radius |
| `K_s1` | 10 | Sheep-sheep repulsion gain |
| `K_s2` | 0.5 | Alignment gain cua cuu |
| `K_s3` | 2 | Cohesion gain cua cuu |
| `K_s4` | 5000 | Sheep-dog repulsion gain |
| `K_f1` | 10 | Cho hut ve target sheep |
| `K_f2` | 200 | Cho day khoi target sheep |
| `K_f3` | 8 | Cho day khoi goal |
| `K_f4` | 3000 | Dog-dog repulsion gain |
| `dt` | 0.05 | Buoc tich phan force |
| `sheep_speed_max` | 5 | Speed clamp cua cuu |
| `dog_speed_max` | 10 | Speed clamp cua cho |

## `fat`

FAT dung tham so cuu Strombom. Moi cho chon con cuu quan sat xa no nhat va dung cach `r_a` phia sau con cuu theo huong ra xa dich. Phase 1, 2, 4 dung observation `global`.

## Information ladder

| Factor | Gia tri | Y nghia |
|---|---|---|
| `obs_mode` | `bearing_only`, `local_positions`, `global` | Muc thong tin quan sat tang dan |
| `sensing_range` | 32.5, 65, 97.5, 130 | 0.5, 1, 1.5, 2 lan `r_s` |
| `communication` | `none`, `neighbour_broadcast`, `global_shared` | Rieng, hop neighbor, hoac hop toan cuc cua cuu da sense |

Voi `strombom_multi`, `global_shared` dung hop cua cuu da sense, khong dung true position dac quyen tu simulator. Scout Phase 5 dung D trong `{1, 2, 3, 4, 6, 10}` vi saving mot buoc co the xuat hien o vung D thap.

## Field cua protocol recipe

| Field | Y nghia |
|---|---|
| `protocol_id` | ID resolve trong `scaling/configs/protocols/` va ghi vao output |
| `phase` | So phase nghien cuu |
| `grade` | Grade SMOKE, SCOUT, hoac CLAIM |
| `canonical` | Path toi mac dinh dong bang |
| `extends` | Parent YAML duoc ke thua |
| `output` | Dich trong `scaling/results/` |
| `methods` hoac `method` | Danh sach controller hoac controller cua factor run |
| `layouts` | Tap con layout |
| `flock_sizes` | Tap con N |
| `shepherd_counts` | Tap con D |
| `seeds` | So seed moi cell da chon |
| `seed_mode` | Y nghia stage nhu scout hoac claim |
| `runner` | Execution path grid hoac factor |
| `upstream_protocol` | Protocol scout hoac claim dung de lap ke hoach |
| `store_timeseries` | Co ghi Parquet history moi trial hay khong |
| `packages` | Package phan tich export sau run |
| `obs_modes`, `sensing_ranges`, `communications` | Gia tri cua mot information ladder |

`canonical` import mac dinh; `extends` ke thua recipe day du. `protocol.yaml` da resolve duoc copy vao result directory de co the kiem tra ca gia tri ke thua.

## Outcome va state metric

| Dai luong | Dinh nghia |
|---|---|
| success | Moi cuu vao dich truoc deadline |
| `t_s` | Tick dau tien dat success |
| `shepherd_path` | Tong Euclidean step length cua moi cho |
| path moi cho | `shepherd_path / D` |
| cohesion | Trung binh khoang cach cuu toi GCM |
| fragmentation | Largest connected component chia N, radius 5 |
| outlier count | So cuu ngoai `r_a * N^(2/3)` |
| spread | Variance cua khoang cach toi centroid |
| extent | RMS distance toi centroid |
| perimeter | Chu vi convex hull |
| hull area | Dien tich convex hull |
| flock density | N chia hull area; 0 neu area suy bien |
| aspect ratio | Ti so PCA major/minor; 1 la tron |
| `I_dir` | `1 - ||sum unit_velocity|| / M_active`, voi speed tren `1e-6` |
| coverage C | Ti le cuu ngoai median GCM distance nam trong influence radius |

Neu khong cho nao di chuyen, `I_dir = 0`. Metric dung realized velocity, gom ca anh huong constraint. Khong co coverage radius thi gia tri la NaN.

## Reliability, frontier, regime

`R(m, tau, N, D, T, X0, I)` la xac suat success uoc luong tren seed khoa, voi method m, protocol tau, N, D, deadline T, layout X0, va information I.

| Dai luong | Dinh nghia |
|---|---|
| D_min | D nho nhat da thu co R >= theta |
| D_overcrowd | D dau tien sau D_min ma no va D luoi ke tiep deu co R < theta |
| D_max | D tin cay lon nhat truoc overcrowding; neu khong co collapse thi la D tin cay lon nhat da thu |
| B* | `(D, T)` tin cay co median path nho nhat; hoa thi chon D nho, roi finish nhanh |
| hard failure | Khong D nao dat theta; frontier de trong |
| under-resourced | R duoi theta truoc D_overcrowd |
| efficient | R dat theta va path duoi wasteful bar |
| wasteful | Tin cay nhung median path cao hon B* it nhat 20 phan tram; cung bao cao 10 va 30 |
| overcrowding collapse | R duoi theta tai hoac sau D_overcrowd |

Effect frontier tinh theo buoc cuc bo cua luoi D. D_max = 35 va D_overcrowd trong nghia la chua thay collapse den tran da thu, khong co nghia collapse bat dau tai 35.

Bootstrap resample seed trong moi D 1,000 lan. Mau khong co D_min van duoc giu nhu right-censored tren D lon nhat. Percentile 2.5 va 97.5 la gia tri luoi hoac `above grid`.

## Prediction va early warning

RQ7 dung horizon `k = 500`, feature window `w = 200`, va tick danh gia 1,000 den 8,000, buoc 200. Feature chi dung `(t - 200, t]`; label la failure trong 500 tick tiep theo khi horizon van nam trong T0.

State model va N,D model hold out toan bo N. Candidate fit gom constant, linear, power `A * N^alpha`, va two-piece linear. Chon bang leave-one-N-out RMSE.
