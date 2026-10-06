# Bang thuat ngu

| Thuat ngu | Dinh nghia |
|---|---|
| B* | `(D, T)` tin cay co median tong path cua cho nho nhat; hoa thi D nho hon, roi finish nhanh hon |
| C, coverage | Ti le cuu peripheral nam trong influence radius |
| cell | Mot to hop co dinh cua method, layout, N, D, va information factor, lap qua cac seed |
| CLAIM | Grade chinh xac, thuong 100 seed tai cell da lap ke hoach |
| cohesion | Trung binh khoang cach cuu toi GCM |
| D | So cho hoac shepherd |
| luoi D | `{1, 2, 3, 4, 6, 10, 15, 20, 25, 35}` |
| D_max | D tin cay cuoi truoc overcrowding, hoac tran luoi khi chua thay collapse |
| D_min | D nho nhat co R dat theta |
| D_overcrowd | Phan tu dau cua hai D lien tiep sau D_min deu duoi theta |
| efficient | Cell tin cay co median path duoi wasteful threshold |
| extent | RMS distance cua cuu toi centroid |
| finish time, `t_s` | Tick dau tien moi cuu nam trong dich |
| fragmentation | Largest connected component radius 5 chia N |
| GCM | Tam khoi hinh hoc cua dan |
| grade | Cap evidence: SMOKE, SCOUT, CLAIM, hoac T1 co dieu kien |
| grid ceiling | D = 35, gia tri lon nhat da thu; khong phai gioi han vat ly |
| hard failure | Khong D nao tren luoi dat theta |
| hull area | Dien tich convex hull cua cuu |
| I | Information condition |
| `I_dir` | Xung dot huong cua cho dang di; 0 cung huong, 1 triet tieu |
| layout, X0 | Bo tri ban dau: compact, wide, split, outlier-rich |
| m, method | Controller cua cho |
| manifest | `manifest.jsonl`, ledger dung de bo qua trial key da xong khi resume |
| mean spread | Diem spread export cho layout va prediction |
| merged trials | Row claim tai cell gieo lai cong row scout tai cell con lai |
| N | So cuu |
| luoi N | `{5, 10, 25, 50, 75, 100, 150, 200, 300, 400}` |
| overcrowding collapse | Cell khong tin cay tai hoac sau D_overcrowd |
| path, `shepherd_path` | Tong Euclidean travel cua moi cho |
| path moi cho | Tong path chia D |
| perimeter | Chu vi convex hull |
| Pilot, SMOKE | Kiem tra pipeline nho, khong dung cho claim |
| protocol | Recipe da resolve cho factor, seed, grade, output, va canonical setting |
| provenance | Record may-doc cua protocol, seed, code state, host, metric, timestamp |
| R | Ti le seed thanh cong truoc deadline |
| regime | under-resourced, efficient, wasteful, overcrowding, hoac hard failure |
| SCOUT | Map rong 30 seed chi dung lap ke hoach va chan doan |
| seed | Mot lan lap ngau nhien doc lap; danh sach goc bat dau tu 2026 |
| success | Moi cuu vao dia dich truoc deadline |
| T0 | Deadline chinh 10,000 tick |
| T1 | Deadline 20,000 tick chi cho overcrowding |
| theta | Nguong reliability 0.90; sensitivity 0.50 va 0.70 |
| tick | Mot update roi rac, khong phai giay dong ho |
| timeseries | Lich su Parquet theo trial cho trajectory va early warning |
| under-resourced | R duoi theta truoc working band |
| wasteful | Cell tin cay co median path vuot B* theo tolerance |
| X0 | Ho layout ban dau |

## Failure label

Trial that bai co the nhan label phan tich `stacking`, `split`, `scatter`, `oscillation`, `stuck`, hoac `timeout`. Label heuristic nay khong thay doi success nhi phan.

## Ten controller

| Ten | Mo ta ngan |
|---|---|
| `strombom_multi` | Baseline collect/drive nhieu cho co phoi hop |
| `kubo` | Controller force cuc bo co sensing va tich phan |
| `fat` | Cuu Strombom va target xa tung cho nhat |
| `communication_free` | Controller transfer khuyen nghi, ngoai tap bat buoc ba method |
