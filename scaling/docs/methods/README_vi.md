# Cac phuong phap trong `scaling_v2`

Thu muc nay giai thich ba ho bo dieu khien da duoc danh gia trong nghien cuu scaling hoan tat. Moi huong dan tach ro bon lop:

1. y tuong da cong bo truyen cam hung cho phuong phap;
2. bo dieu khien va mo hinh cuu chinh xac trong HerdSim;
3. thiet lap thi nghiem dong bang `scaling_v2`;
4. ket qua da quan sat tu cac lan chay hoan tat.

Viec tach cac lop nay la can thiet. Nghien cuu so sanh cac bo dieu khien mo phong tren nhiem vu `drive_to_goal` cua HerdSim. Nghien cuu khong tai tao toan bo thi nghiem hay ket qua dinh luong cua cac bai bao duoc trich.

## Huong dan

| Huong dan | Co so cong bo | Phuong phap HerdSim trong `scaling_v2` |
|---|---|---|
| [Strombom Collect/Drive](strombom_vi.md) | Strombom va cong su (2014) | `strombom_multi`, khong phai preset mot nguoi chan `strombom` |
| [Mo hinh luc Kubo](kubo_vi.md) | Kubo va cong su (2022) | `kubo` |
| [FAT](fat_vi.md) | Y tuong ca the nhin thay xa nhat cua Tsunoda va cong su (2018) | `fat`, dung cuu Strombom |

Ban tieng Anh: [README.md](README.md), [strombom.md](strombom.md), [kubo.md](kubo.md), va [fat.md](fat.md).

## Thiet lap chung cua `scaling_v2`

Tat ca so sanh hoan tat dung cung nhiem vu va dinh nghia bien:

- nhiem vu: dua moi con cuu vao dia dich truoc `T0 = 10000` tick;
- san: 500 x 500 don vi khong gian lien tuc;
- tam dan: `(250, 250)`;
- tam dich: `(370, 250)`;
- ban kinh dich: `15 * sqrt(N / 50)`;
- so cuu cho ban do kich thuoc: `{5, 10, 25, 50, 75, 100, 150, 200, 300, 400}`;
- so cho: `{1, 2, 3, 4, 6, 10, 15, 20, 25, 35}`;
- so cuu cho ban do cau truc: `N` trong `{50, 100, 200}`;
- bo cuc: `compact`, `wide`, `split`, va `outlier_rich`;
- do tin cay: `R`, ty le seed doc lap thanh cong truoc `T0`;
- bien: `D_min`, so cho nho nhat da thu co `R >= 0.90`;
- phan tang: 30 seed scout tren toan luoi, sau do 100 seed claim trong cua so da chon, voi ngoai le 200 seed cho Kubo `outlier_rich`, `N = 200`.

Ban merge claim thay cac dong scout tai o duoc chay lai va giu dong scout o cac o con lai. `D_max = 35` khi khong co overcrowding chi la dinh luoi da thu, khong phai nguong that bai da do.

Cau hinh dong bang: [`../../configs/canonical_grid.yaml`](../../configs/canonical_grid.yaml).

## Bang chung hoan tat

So sanh dat cap claim gom:

- kich thuoc va cau truc co so: `strombom_multi`, Giai doan 1 va 2;
- kich thuoc va cau truc chuyen giao: `kubo` va `fat`, Giai doan 4.

Bang chung chinh:

- [`../../results/phase1/claim/`](../../results/phase1/claim/)
- [`../../results/phase2/claim/`](../../results/phase2/claim/)
- [`../../results/phase4/`](../../results/phase4/)
- [`../../results/summary/SUMMARY_REPORT_vi.md`](../../results/summary/SUMMARY_REPORT_vi.md)

Huong dan phuong phap giup dien giai, nhung ket luan dinh luong nen trich CSV da do.

## Gioi han chung

- Ket qua chi ap dung cho mot nhiem vu mo phong, mot hinh hoc dong bang, mot timeout, va mot nguong tin cay chinh.
- Khong nen so sanh vat ly so tick giua Kubo va ho Strombom. Kubo tich phan van toc voi `dt = 0.05`, con ho Strombom dich chuyen co dinh moi tick.
- Registry NetLogo co twin cho `strombom_multi` va `kubo`, nhung bao cao hoan tat khong khang dinh parity tung tick hay diem parity dinh luong da cong bo.
- FAT khong co twin NetLogo trong registry.
- Khong co ket qua hoan tat nao chung minh hieu nang ngoai dong, do trung thuc sinh hoc, hay quy luat scaling pho quat.
