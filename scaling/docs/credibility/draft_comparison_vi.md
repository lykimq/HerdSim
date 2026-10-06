# Doi chieu ban thao 2025 va HerdSim

## Trang thai doi chieu

Ban thao 2025, *Collective Nudging that Scales. How many dogs do I need to herd sheep?*, bao cao mot nghien cuu NetLogo 7.0.3. HerdSim `scaling_v2` la mot nghien cuu mo phong Python rieng. Hai nghien cuu chia se cau hoi rong, luoi so cho, han 10,000 tick, va nguong tin cay 90%. Chung khong chia se cung nhiem vu, san, khoi tao, bo dieu khien, hoac dinh nghia bien.

Ban thao khong duoc chay lai trong HerdSim hoac NetLogo trong chuong trinh hien tai. Gia tri ban thao ben duoi duoc chep tu PDF va ghi chu trong kho. Gia tri HerdSim den tu du lieu tang claim. Day la doi chieu ket qua giua hai giao thuc, khong phai kiem tra tai lap.

![Ban thao gom, giu, ra cong so voi HerdSim lua vao dich.](../../results/summary/figures/schematics/vi/draft_vs_herdsim.svg)

## Doi chieu giao thuc

| Muc | Ban thao 2025 | HerdSim `scaling_v2` |
|---|---|---|
| Dong co | NetLogo 7.0.3 tren luoi patch | HerdSim trong khong gian lien tuc voi tick roi rac |
| Nhiem vu | Gom, giu 800 tick, roi dua qua cong | `drive_to_goal`, moi cuu nam trong dia dich |
| Thanh cong | Moi cuu qua cong truoc 10,000 tick | Ti le trong dia dich dat 1.0 truoc T0 = 10,000 |
| San | 101 x 71 patch, vung giu o tam, cong tren tuong phai | San 500 x 500, dan tai (250, 250), dich tai (370, 250) |
| Vung giu hoac dich | `rc = clamp(2.5 * sqrt(N), 23, 27)` | Ban kinh `15 * sqrt(N/50)` |
| Khoi tao cuu | Rai ngau nhien, co dem voi tuong va cho | Cac ho `compact`, `wide`, `split`, va `outlier_rich` duoc kiem soat |
| Khoi tao cho | Luoi tai goc tren trai | Sau dan, doi dien dich, lech 50 voi nhieu `+/-5` |
| Bo dieu khien | Mot ho NetLogo gom, lua, va tuan tra | Co so `strombom_multi`; chuyen giao `kubo` va `fat` |
| Luoi D | `{1, 2, 3, 4, 6, 10, 15, 20, 25, 35}` | Giong |
| Luoi N | `{5, 10, 25, 50, 100, 150, 200, 250, 300, 350, 400}` | `{5, 10, 25, 50, 75, 100, 150, 200, 300, 400}` |
| Lay mau | 100 lan moi o, tong 11,000 | Scout 30 moi o; claim thuong gieo lai 100 tren cua so da chon |
| Seed | Seed goc khong neu trong ghi chu | Seed goc 2026; seed thu nghiem `2026 + i` |
| Tin cay | SR >= 90% | R >= theta, voi theta = 0.90 cho bien claim |
| D_min | D nho nhat co SR >= 90% | D da thu nho nhat co R >= theta |
| D_overcrowd | D dau tien tren D_min noi SR bat dau giam | Dau cua hai D lien tiep duoi theta sau D_min |
| D_max | D dau tien tren D_min co SR < 90%, neu khong thi tran | D tin cay lon nhat truoc D_overcrowd; neu khong thi tran luoi 35 |
| Bat dinh | Khong bao cao khoang nhi thuc hoac bootstrap D_min | 1,000 bootstrap seed cho D_min |
| Cau truc | Do rai phat sinh, tom tat bang `S_bar` | Bo cuc khoi tao kiem soat, cohesion, fragmentation, va mean spread |
| Chi so | Thanh cong, tick, pha, spread, path, va cuu lac | Thanh cong, tick, path, cohesion, fragmentation, spread, interference, va nhan that bai |

![Cac pha nhiem vu ban thao duoc bao cao.](../../results/summary/figures/schematics/vi/draft_task_phases.svg)

## Ket qua ban thao duoc bao cao

Tai SR >= 90%, Bang A3 cua ban thao bao cao:

| N | D_min ban thao | D_max ban thao | SR toi da |
|---|---:|---:|---:|
| 5 | 1 | chua dat | 100% |
| 10 | 1 | 15 | 100% |
| 25 | 1 | 25 | 100% |
| 50 | 1 | 25 | 100% |
| 100 | 1 | chua dat | 100% |
| 150 | 3 | chua dat | 99% |
| 200 | 20 | 35 | 94% |
| 250 | 25 | chua dat | 93% |
| 300 | 20 | chua dat | 93% |
| 350 | 35 | chua dat | 91% |
| 400 | 35 | chua dat | 91% |

"Chua dat" nghia la bien that bai phia tren chua duoc tim thay tai D = 35. Day la gia tri ban thao bao cao, khong phai ket qua duoc tao lai boi kho nay.

Ban thao cung bao cao lien he am giua mean spread va thanh cong, gom Spearman rho = -0.701 cho `S_bar` voi SR va rho = -0.828 cho `S_bar * N` voi SR tren 110 tong hop dieu kien. Phan tich nhay cam va density gradient khong duoc chay lai o day.

![Tom tat truc quan chep tu Bang A3 cua ban thao.](../../results/summary/figures/schematics/vi/draft_main_results.svg)

## Ket qua HerdSim dung de doi chieu

Voi co so `strombom_multi` tren xuat phat compact, du lieu claim cho D_min = 2 tai N trong `{5, 10}` va D_min = 1 tu N = 25 den 400. D_max = 35 la tran luoi da thu trong moi o Giai doan 1 vi khong thay cap overcrowding. No khong phai diem sup phia tren da do.

Doi bo cuc khoi tao khong doi D_min co so tai N trong `{50, 100, 200}`, nhung doi chi phi ro ret. Kubo gan khop co so compact, trong khi Kubo tren wide va FAT tren dan lon thuong khong dat R = 0.90 tai bat ky D nao trong luoi. Day la ket qua chuyen giao HerdSim, khong phai ket qua parity voi ban thao hoac NetLogo.

| Phat hien ban thao | Ket qua HerdSim theo giao thuc cua no | Trang thai |
|---|---|---|
| Mot cho du den khoang N = 100 roi sup | Mot cho dat R >= 0.90 den N = 400 tren co so compact | Khong tai hien |
| D_min tang len 20 den 35 khi N >= 200 | D_min co so van la 1 | Khong tai hien |
| D cao co the gay overcrowding cho dan nho | Khong co cap overcrowding co so den D = 35 | Khong tai hien |
| Thoi gian giam theo D; quang duong bao hoa | Thoi gian co so gan phang; tong duong cho tang theo D | Hinh dang do khac |
| Spread du doan that bai | Chua co phan tich doi ung co kiem soat o muc claim | Chua kiem parity |
| Mot bo dieu khien, khong bat dinh D_min | Ba bo dieu khien HerdSim, bon bo cuc, va bootstrap | Bang chung HerdSim bo sung |

![Cac phan tich ban thao khong duoc chay lai.](../../results/summary/figures/schematics/vi/draft_extra_analyses.svg)

## Vi sao ket qua co the khac

Khac biet co the den tu pha giu va qua cong, cuu rai luc dau, cho xuat phat o goc, hinh hoc vung giu, va chi tiet bo dieu khien cua ban thao. HerdSim dung duong lua noi bo ngan hon voi cho da o sau dan. Day chi la dien giai. Khong co thi nghiem thay tung thanh phan de tach mot nguyen nhan.

Vi vay, "khong tai hien" nghia la ket qua khong xuat hien duoi giao thuc HerdSim khac. No khong chung minh ket qua ban thao sai.

## Da chay va chua chay lai

| Muc | Trang thai |
|---|---|
| Du lieu claim HerdSim Giai doan 1, 2, va 4 | Da chay va dung cho ket luan hien tai |
| Thi nghiem 11,000 lan cua ban thao 2025 | Khong chay lai |
| Cac o nhay cam cua ban thao | Khong chay lai |
| Phan tich density gradient cua ban thao | Khong chay lai |
| Bo phan loai va tuong quan spread cua ban thao | Khong chay lai |
| Mo hinh ban thao nhu mot twin di kem | Khong, khong co trong `twins.json` |
| Thay giao thuc co kiem soat giua ban thao va HerdSim | Chua chay |

## Trich dan va nguon goc

Nguon ban thao chinh:

*Collective Nudging that Scales. How many dogs do I need to herd sheep?* Ban thao, khoang 2025, dong tac gia tam. Ban trong kho: [PDF](../../../docs/papers/sheep-scaling_paper2025.pdf).

Tai lieu ho tro dien giai:

- [Ghi chu tham chieu ban thao](../notes/sheep-scaling_paper2025.md)
- [Bao cao tong hop tieng Anh](../../results/summary/SUMMARY_REPORT.md)
- [Bao cao tong hop tieng Viet](../../results/summary/SUMMARY_REPORT_vi.md)
- [Ranh gioi xac thuc va NetLogo](validation_and_netlogo_vi.md)
