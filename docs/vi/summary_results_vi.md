# Tổng quan kết quả: mọi giao thức trong một cái nhìn

Đội tin cậy nhỏ nhất cho mọi đường cong của 41 giao thức HerdSim, chỉ gồm bảng. Phần diễn giải nằm trong [báo cáo](d_min_report_vi.md) và các thuật ngữ trong [bảng thuật ngữ](glossary_vi.md).

## Mục lục

- [Cách đọc các bảng](#cách-đọc-các-bảng)
- [1. Quy tắc nghiêm ngặt](#1-quy-tắc-nghiêm-ngặt)
- [2. Quy tắc 99 phần trăm](#2-quy-tắc-99-phần-trăm)
- [3. Giữ bầy ở 95 và 90 phần trăm](#3-giữ-bầy-ở-95-và-90-phần-trăm)
- [4. Các lệnh](#4-các-lệnh)

## Cách đọc các bảng

Mỗi hàng là một giao thức, bố cục xuất phát và biến thể; mỗi cột là một quy mô bầy $N$. Mỗi ô là $D_{\min}$, số chó nhỏ nhất có tỷ lệ thành công ít nhất 0,90 với độ tin cậy 99% ([quy tắc quyết định](d_min_report_vi.md#21-khi-nào-một-đội-là-tin-cậy)):

- `3`: đã quyết định. `2-3`: 3 chó là tin cậy, 2 chó còn chưa quyết định sau 200 lượt. `[5]`: chưa đội nào tin cậy, và cần ít nhất 5. `none`: mọi đội đã thử đều không tin cậy. Ô trống: $N$ đó không được chạy.
- `(max 6)`: đội tin cậy lớn nhất, $D_{\max}$, khi nó nhỏ hơn đội lớn nhất đã thử. Một ô tin cậy không có ghi chú thì vẫn tin cậy tới đội lớn nhất đã thử.
- `(over 9)`: $D_{\mathrm{overcrowd}}$, quy mô đầu tiên trong hai quy mô đội liên tiếp đều không tin cậy, tìm ở phía trên $D_{\min}$.

Quy tắc nghiêm ngặt cần mọi con cừu ở trong đích, quy tắc 99 phần trăm cần ít nhất 99% số cừu; không bảng nào trộn hai quy tắc. Một giao thức có `f99` trong tên có cùng thiết lập với giao thức nghiêm ngặt cùng tên, ngoài quy tắc thành công.

## 1. Quy tắc nghiêm ngặt

`dmin_m12`, `dmin_m6` và `dmin_m3` có thời hạn 12, 6 và 3 lần thời gian lùa. Các lượt `dmin_s_*` ở 6 lần thời gian lùa, gồm một lượt cơ sở và mỗi lượt một thay đổi: `matched` bộ cừu khớp thực địa, `handler` mọi chó xuất phát ở một điểm, `ring` chó xuất phát trên một vòng tròn đầy đủ, `goal` đích bán kính $1{,}5 R_f$, `dogspeed` chó đi 1,15 m/s, `gap` khoảng cách xuất phát. `dmin_fat` dùng chó FAT và `dmin_kubo` dùng mô hình Kubo với giới hạn 500 s (Bảng 1).

**Bảng 1: Đội tin cậy nhỏ nhất, quy tắc nghiêm ngặt.**

| protocol | layout | variant | N=25 | N=50 | N=100 | N=200 | N=400 |
|---|---|---|---|---|---|---|---|
| dmin_m12 | compact |  | 1 | 1 | 1 | 1 | 1 |
| dmin_m12 | wide |  | 1 | 1 | 1 | 2 | 3 |
| dmin_m12 | split |  | 1 | 1 | 1 | 1-2 | 3 |
| dmin_m12 | outlier_rich |  | 1 | 1 | 1-3 | 2 | 3 |
| dmin_m6 | compact |  | 1 | 1 | 1 | 1 | 1 |
| dmin_m6 | wide |  | 1 | 1 | 1 | 3 (max 16) | [9] |
| dmin_m6 | split |  | 1 | 1 | 1 | none | none |
| dmin_m6 | outlier_rich |  | 1 | 1 | 3 | [12] | none |
| dmin_m3 | compact |  | 1 | 1 | 1 | 1 | 1 |
| dmin_m3 | wide |  | 1 | 1 | 3 | none | none |
| dmin_m3 | split |  | 1 | 1 | 1 (max 1, over 2) | none | none |
| dmin_m3 | outlier_rich |  | 1 | 1 | 3-8 | none | none |
| dmin_s_base | wide |  |  |  | 1 | 3 | [9] |
| dmin_s_base | outlier_rich |  |  |  | 3 | [12] | none |
| dmin_s_matched | wide |  |  |  | 1-6 (max 6) | none | none |
| dmin_s_matched | outlier_rich |  |  |  | [1] | none | none |
| dmin_s_handler | wide |  |  |  | 1 | 3 | none |
| dmin_s_handler | outlier_rich |  |  |  | 2 | [3] (over 4) | none |
| dmin_s_ring | wide |  |  |  | 1 | 3-5 | [8] |
| dmin_s_ring | outlier_rich |  |  |  | 2-7 | [5] | none |
| dmin_s_goal | wide |  |  |  | 1-3 | none | none |
| dmin_s_goal | outlier_rich |  |  |  | 3 (max 15) | none | none |
| dmin_s_dogspeed | wide |  |  |  | 1 | 3 | 5 |
| dmin_s_dogspeed | outlier_rich |  |  |  | 2-3 | 4 | 6 |
| dmin_s_gap | wide | gap 15 m |  |  | 1 (max 15) | [3] (over 4) | none |
| dmin_s_gap | wide | gap 30 m |  |  | 1 | 3 | [9] |
| dmin_s_gap | wide | gap 60 m |  |  | 1 | 3-4 | 6-7 |
| dmin_s_gap | outlier_rich | gap 15 m |  |  | [1] (over 4) | none | none |
| dmin_s_gap | outlier_rich | gap 30 m |  |  | 3 | [12] | none |
| dmin_s_gap | outlier_rich | gap 60 m |  |  | 3 | 5 | [12] |
| dmin_fat | compact |  | 1 | 1 | 1 | 1 (max 16) | none |
| dmin_fat | wide |  | 1 | 1 | 1 | none | none |
| dmin_fat | split |  | 1 | 1 | 1 | none | none |
| dmin_fat | outlier_rich |  | 1 | 1 | 2 | none | none |
| dmin_kubo | compact |  | 1 | 1 | 1 |  |  |

Bảng 2 ghi $D_{\mathrm{sat}}$, đội tin cậy nhỏ nhất mà không đội tin cậy lớn hơn nào nhanh hơn quá 5% thời gian hoàn thành với độ tin cậy 99%, cho `dmin_m12`, lượt nghiêm ngặt duy nhất có thêm hạt giống để quyết định thời gian hoàn thành. `5-24` nghĩa là một đội lớn hơn vẫn có thể nhanh hơn, `-` là không đội nào tin cậy.

**Bảng 2: Đội mà vượt quá nó thêm chó không còn giúp, quy tắc nghiêm ngặt, 12 lần thời gian lùa.**

| protocol | layout | N=25 | N=50 | N=100 | N=200 | N=400 |
|---|---|---|---|---|---|---|
| dmin_m12 | compact | 1 | 1 | 1 | 1 | 1 |
| dmin_m12 | wide | 1 | 1 | 2 | 3-24 | 6-24 |
| dmin_m12 | split | 1 | 1 | 4 | 3-24 | 3-24 |
| dmin_m12 | outlier_rich | 1 | 1-24 | 3 | 5-24 | 6-24 |

## 2. Quy tắc 99 phần trăm

### 2.1 Các lưới chính

Các lưới chính ở 12, 6 và 3 lần thời gian lùa (Bảng 3), và $D_{\mathrm{sat}}$ cho năm lượt 99 phần trăm có quyết định thời gian hoàn thành (Bảng 4).

**Bảng 3: Đội tin cậy nhỏ nhất trên các lưới chính, quy tắc 99 phần trăm.**

| protocol | layout | N=25 | N=50 | N=71 | N=100 | N=141 | N=200 | N=283 | N=400 | N=566 |
|---|---|---|---|---|---|---|---|---|---|---|
| dmin_f99_m12 | compact | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| dmin_f99_m12 | wide | 1 | 1 | 1 | 1 | 2 | 1-2 | 2 | 2 | 2-3 |
| dmin_f99_m12 | split | 1 | 1 | 1 | 1 | 1 | 1 | 2 | 2 | 3 |
| dmin_f99_m12 | outlier_rich | 1 | 1 | 1 | 1-2 | 2 | 2 | 2 | 2 | 2-3 |
| dmin_f99_m6 | compact | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| dmin_f99_m6 | wide | 1 | 1 | 1 | 1 | 2 | 2 | 2-3 | 2-3 | 3-7 |
| dmin_f99_m6 | split | 1 | 1 | 1 | 1 | 1 | [1] (over 4) | [5] (over 15) | [5] (over 10) | none |
| dmin_f99_m6 | outlier_rich | 1 | 1 | 1 | 2 | 2 | 2-3 | 2-3 | 3 | 3-6 (max 12) |
| dmin_f99_m3 | compact | 1 | 1 |  | 1 |  | 1 |  | 1 |  |
| dmin_f99_m3 | wide | 1 | 1 |  | 2 |  | 3 |  | 5-6 |  |
| dmin_f99_m3 | split | 1 | 1 |  | 1 |  | none |  | none |  |
| dmin_f99_m3 | outlier_rich | 1 | 1 |  | 2 |  | 4-10 |  | [6] (over 7) |  |

**Bảng 4: Đội mà vượt quá nó thêm chó không còn giúp, quy tắc 99 phần trăm.**

| protocol | layout | N=25 | N=50 | N=71 | N=100 | N=141 | N=200 | N=283 | N=400 | N=566 |
|---|---|---|---|---|---|---|---|---|---|---|
| dmin_f99_m12 | compact | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| dmin_f99_m12 | wide | 1 | 1 | 1 | 2 | 3 | 3 | 4 | 5 | 7-24 |
| dmin_f99_m12 | split | 1 | 1 | 1 | 4 | 7 | 2-24 | 2-24 | 4-24 | 3-24 |
| dmin_f99_m12 | outlier_rich | 1 | 1-24 | 2 | 3 | 3 | 4 | 5-24 | 6-24 | 8-24 |
| dmin_f99_m6 | compact | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| dmin_f99_m6 | wide | 1 | 1 | 1 | 2 | 3 | 3 | 4 | 5 | 7-24 |
| dmin_f99_m6 | split | 1 | 1 | 1 | 4 | 7 | - | - | - | - |
| dmin_f99_m6 | outlier_rich | 1 | 1-24 | 2 | 3 | 3 | 4 | 5-24 | 6-24 | 8-12 |
| dmin_f99_m3 | compact | 1 | 1 |  | 1 |  | 1 |  | 1 |  |
| dmin_f99_m3 | wide | 1 | 1 |  | 2 |  | 3 |  | 6 |  |
| dmin_f99_m3 | split | 1 | 1 |  | 4 |  | - |  | - |  |
| dmin_f99_m3 | outlier_rich | 1 | 1-24 |  | 3 |  | 10 |  | - |  |
| dmin_f99_indep | compact | 1 | 1 |  | 1 |  | 1 |  | 1 |  |
| dmin_f99_indep | wide | 1 | 1 |  | 2 |  | 3 |  | - |  |
| dmin_f99_indep | split | 1 | 1 |  | 2 |  | 5-24 |  | - |  |
| dmin_f99_indep | outlier_rich | 1 | 1 |  | 2-24 |  | 4-24 |  | - |  |
| dmin_f99_kubo | compact | 16-24 | 17-24 |  | 16-24 |  |  |  |  |  |

### 2.2 Các quy tắc chó khác

Chó FAT, chó độc lập (mỗi chó chạy quy tắc một chó của Strömbom, không có tầng đội) ở 6 lần thời gian lùa, và mô hình Kubo với giới hạn 500 s (Bảng 5).

**Bảng 5: Đội tin cậy nhỏ nhất với FAT, chó độc lập và Kubo, quy tắc 99 phần trăm.**

| protocol | layout | N=25 | N=50 | N=100 | N=200 | N=400 |
|---|---|---|---|---|---|---|
| dmin_f99_fat | compact | 1 | 1 | 1 | 1 | [12] (over 13) |
| dmin_f99_fat | wide | 1 | 1 | 1 | none | none |
| dmin_f99_fat | split | 1 | 1 | 1 | none | none |
| dmin_f99_fat | outlier_rich | 1 | 1 | 2 | none | none |
| dmin_f99_indep | compact | 1 | 1 | 1 | 1 | 1 |
| dmin_f99_indep | wide | 1 | 1 | 1 | 2-3 | none |
| dmin_f99_indep | split | 1 | 1 | 1 | 1-3 | none |
| dmin_f99_indep | outlier_rich | 1 | 1 | 2 | 3 | none |
| dmin_f99_kubo | compact | 1 | 1 | 1 |  |  |

### 2.3 Thay đổi thiết lập

Các lượt chạy độ nhạy ở 6 lần thời gian lùa, với các thay đổi đã liệt kê ở [mục 1](#1-quy-tắc-nghiêm-ngặt) (Bảng 6).

**Bảng 6: Đội tin cậy nhỏ nhất trong các lượt chạy độ nhạy, quy tắc 99 phần trăm.**

| protocol | layout | variant | N=100 | N=200 | N=400 |
|---|---|---|---|---|---|
| dmin_f99_s_base | wide |  | 1 | 2 | 2-3 |
| dmin_f99_s_base | outlier_rich |  | 2 | 2-3 | 3 |
| dmin_f99_s_matched | wide |  | 1 | 1 | 2 |
| dmin_f99_s_matched | outlier_rich |  | 1 | 1 | 2-3 |
| dmin_f99_s_handler | wide |  | 1 | 2-3 | 2-3 |
| dmin_f99_s_handler | outlier_rich |  | 2 | 2-3 | 3 (max 5) |
| dmin_f99_s_ring | wide |  | 1 | 2-3 | 3 |
| dmin_f99_s_ring | outlier_rich |  | 2 | 2 | 3 |
| dmin_f99_s_goal | wide |  | 1 | 2 | 5-6 |
| dmin_f99_s_goal | outlier_rich |  | 2 | 2-3 | none |
| dmin_f99_s_dogspeed | wide |  | 1 | 2-3 | 2-3 |
| dmin_f99_s_dogspeed | outlier_rich |  | 2 | 2-3 | 3 |
| dmin_f99_s_gap | wide | gap 15 m | 1 | 2 | 2-3 |
| dmin_f99_s_gap | wide | gap 30 m | 1 | 2 | 2-3 |
| dmin_f99_s_gap | wide | gap 60 m | 1 | 2-3 | 2-3 |
| dmin_f99_s_gap | outlier_rich | gap 15 m | 1-2 | 2 (max 13) | 3 (max 12) |
| dmin_f99_s_gap | outlier_rich | gap 30 m | 2 | 2-3 | 3 |
| dmin_f99_s_gap | outlier_rich | gap 60 m | 2 | 2-3 | 3 |

### 2.4 Giữ bầy

Nhiệm vụ giữ bầy ([giữ bầy](glossary_vi.md#thành-công-và-độ-tin-cậy)): 99% bầy phải ở lại trong đích suốt một lần thời gian lùa trong lúc chó lùi ra. `dmin_f99_hold_spacing` giữ chó cách nhau 2 m; biến thể là bán kính đích tính theo bán kính bầy $R_f$ (Bảng 7).

**Bảng 7: Đội tin cậy nhỏ nhất để giữ bầy, quy tắc 99 phần trăm.**

| protocol | layout | variant | N=25 | N=50 | N=100 | N=200 | N=400 |
|---|---|---|---|---|---|---|---|
| dmin_f99_hold | compact |  | none | none | 1 | 1 | 1 |
| dmin_f99_hold | wide |  | none | none | 1 | 2 | 3 |
| dmin_f99_hold | split |  | none | none | 1 | [2] (over 3) | none |
| dmin_f99_hold | outlier_rich |  | none | none | 3 | 3 | 3-4 (max 6) |
| dmin_f99_hold_spacing | compact |  | none | none | 1 | 1 | 1 |
| dmin_f99_hold_spacing | wide |  | none | none | 1 | 2 | 3 |
| dmin_f99_hold_spacing | split |  | none | none | 1 | [2] (over 3) | none |
| dmin_f99_hold_spacing | outlier_rich |  | none | none | 2-3 | 3 | [3] (over 9) |
| dmin_f99_hold_goal | compact | goal 1.9 R_f | none | none | 1 |  |  |
| dmin_f99_hold_goal | compact | goal 2.5 R_f | 1 (max 3) | 1 | 1 |  |  |
| dmin_f99_hold_goal | compact | goal 3 R_f | 1 | 1 | 1 |  |  |
| dmin_f99_hold_goal | wide | goal 1.9 R_f | none | none | 1 |  |  |
| dmin_f99_hold_goal | wide | goal 2.5 R_f | 1-2 (max 4) | 1 | 1 |  |  |
| dmin_f99_hold_goal | wide | goal 3 R_f | 1 | 1 | 1 |  |  |
| dmin_f99_hold_goal | split | goal 1.9 R_f | none | none | 1 |  |  |
| dmin_f99_hold_goal | split | goal 2.5 R_f | 1 (max 3) | 1 | 1 |  |  |
| dmin_f99_hold_goal | split | goal 3 R_f | 1 | 1 | 1 |  |  |
| dmin_f99_hold_goal | outlier_rich | goal 1.9 R_f | none | none | 3 |  |  |
| dmin_f99_hold_goal | outlier_rich | goal 2.5 R_f | 1-3 (max 6) | 1 | 2 |  |  |
| dmin_f99_hold_goal | outlier_rich | goal 3 R_f | 1 | 1 | 2 |  |  |
| dmin_f99_hold_share | compact | goal 1.9 R_f | none | none | 1 |  |  |
| dmin_f99_hold_share | compact | goal 2.1 R_f | none | [1] | 1 |  |  |
| dmin_f99_hold_share | compact | goal 2.3 R_f | none | 1 | 1 |  |  |
| dmin_f99_hold_share | compact | goal 2.5 R_f | 1 (max 1) | 1 | 1 |  |  |
| dmin_f99_hold_share | wide | goal 1.9 R_f | none | none | 1 |  |  |
| dmin_f99_hold_share | wide | goal 2.1 R_f | none | [1] | 1 |  |  |
| dmin_f99_hold_share | wide | goal 2.3 R_f | none | 1 | 1 |  |  |
| dmin_f99_hold_share | wide | goal 2.5 R_f | 1-2 (max 4) | 1 | 1 |  |  |
| dmin_f99_hold_share | split | goal 1.9 R_f | none | none | 1 |  |  |
| dmin_f99_hold_share | split | goal 2.1 R_f | none | [1] | 1 |  |  |
| dmin_f99_hold_share | split | goal 2.3 R_f | none | 1 | 1 |  |  |
| dmin_f99_hold_share | split | goal 2.5 R_f | 1 (max 3) | 1 | 1 |  |  |
| dmin_f99_hold_share | outlier_rich | goal 1.9 R_f | none | none | 3 |  |  |
| dmin_f99_hold_share | outlier_rich | goal 2.1 R_f | none | [1] | 2 |  |  |
| dmin_f99_hold_share | outlier_rich | goal 2.3 R_f | none | 1 | 2 |  |  |
| dmin_f99_hold_share | outlier_rich | goal 2.5 R_f | 1-3 (max 6) | 1 | 2 |  |  |

### 2.5 Sự gắn kết

Ở 12 lần thời gian lùa: trọng số hút $c$ tăng từ 1,05 của Strömbom et al. (2014) lên 1,3, 1,6 và 2,0, và mỗi con cừu bị hút về nửa bầy thay vì cả bầy (`dmin_f99_k05`) (Bảng 8).

**Bảng 8: Đội tin cậy nhỏ nhất khi thay đổi sự gắn kết, quy tắc 99 phần trăm.**

| protocol | layout | N=25 | N=50 | N=100 | N=200 | N=400 |
|---|---|---|---|---|---|---|
| dmin_f99_c1.3 | compact | 1 | 1 | 1 | 1 | 1 |
| dmin_f99_c1.3 | wide | 1 | 1 | 1 | 1 | 2 |
| dmin_f99_c1.3 | split | 1 | 1 | 1 | 1 | 1-2 |
| dmin_f99_c1.3 | outlier_rich | 1 | 1 | 1 | 2 | 2 |
| dmin_f99_c1.6 | compact | 1 | 1 | 1 | 1 | 1 |
| dmin_f99_c1.6 | wide | 1 | 1 | 1 | 1 | 2 |
| dmin_f99_c1.6 | split | 1 | 1 | 1 | 1 | 1 |
| dmin_f99_c1.6 | outlier_rich | 1 | 1 | 1 | 1 | 2 |
| dmin_f99_c2.0 | compact | 1 | 1 | 1 | 1 | 1 |
| dmin_f99_c2.0 | wide | 1 | 1 | 1 | 1 | 2 |
| dmin_f99_c2.0 | split | 1 | 1 | 1 | 1 | 2 |
| dmin_f99_c2.0 | outlier_rich | 1 | 1 | 1 | 1 | 2 |
| dmin_f99_k05 | compact |  | 1 | 1 | 1 | 1 |
| dmin_f99_k05 | wide |  | 1 | 1 | 2 | 2-4 |
| dmin_f99_k05 | split |  | 1-4 | 1-2 (max 7) | 3-4 (max 20) | 4-5 |
| dmin_f99_k05 | outlier_rich |  | 1 | 2 | 2 | 2 |

### 2.6 Cảm nhận hạn chế

Ở 6 lần thời gian lùa: chó chỉ thấy các con cừu trong một tầm (`range 0 m` là tầm nhìn đầy đủ), và ở 65 m, chia sẻ những gì chúng thấy với các chó trong tầm (`neighbour`) hoặc với cả đội (`shared`) (Bảng 9).

**Bảng 9: Đội tin cậy nhỏ nhất khi tầm nhìn bị giới hạn, quy tắc 99 phần trăm.**

| protocol | layout | variant | N=50 | N=100 | N=200 |
|---|---|---|---|---|---|
| dmin_f99_view_range | wide | range 0 m | 1 | 1 | 2 |
| dmin_f99_view_range | wide | range 15 m | none | [6] | [7] |
| dmin_f99_view_range | wide | range 30 m | 1 | 1 | 3 |
| dmin_f99_view_range | wide | range 45 m | 1 | 1 | 3-4 |
| dmin_f99_view_range | wide | range 65 m | 1 | 1 | 3 |
| dmin_f99_view_range | wide | range 100 m | 1 | 1 | 2-3 |
| dmin_f99_view_range | split | range 0 m | 1 | 1 | [1] (over 8) |
| dmin_f99_view_range | split | range 15 m | 1 | 1 | [3] |
| dmin_f99_view_range | split | range 30 m | 1 | 1 | 2-3 |
| dmin_f99_view_range | split | range 45 m | 1 | 1 | 3 |
| dmin_f99_view_range | split | range 65 m | 1 | 1 | 3 |
| dmin_f99_view_range | split | range 100 m | 1 | 1 | 1-5 |
| dmin_f99_view_comm | wide | neighbour | 1 | 1 | 3 |
| dmin_f99_view_comm | wide | shared | 1 | 1 | 2 |
| dmin_f99_view_comm | split | neighbour | 1 | 1 | 3 |
| dmin_f99_view_comm | split | shared | 1 | 1 | 3 (max 3, over 4) |

### 2.7 Bầy lớn

Ở 12 lần thời gian lùa, với $R_f$ được áp trên $N = 566$ theo mật độ của bầy 566 con. `dmin_f99_big_dense` và `_loose` nhân bán kính được áp với $1/\sqrt{2}$ và $\sqrt{2}$ (từ $N = 800$; các hàng $N = 566$ của chúng chạy cùng bầy với `dmin_f99_big`). `dmin_f99_big_cap` giới hạn điểm lùa ở 63 m sau bầy (Bảng 10).

**Bảng 10: Đội tin cậy nhỏ nhất cho bầy lớn, quy tắc 99 phần trăm.**

| protocol | layout | N=566 | N=800 | N=1131 | N=1600 | N=2263 | N=3200 |
|---|---|---|---|---|---|---|---|
| dmin_f99_big | compact | 1 | 1 | none | none | none | none |
| dmin_f99_big | wide | 2-3 | 3 | none | none | none | none |
| dmin_f99_big_dense | wide | 2-3 | 4-5 |  |  |  |  |
| dmin_f99_big_loose | wide | 2-3 | 3 |  |  |  |  |
| dmin_f99_big_cap | compact |  | 1 | 1 | 2 |  |  |
| dmin_f99_big_cap | wide |  | 3 | 5-9 | none |  |  |

### 2.8 Mục tiêu không gắn kết

Nhiệm vụ gom của Lama và di Bernardo (2024) ([nhiệm vụ gom](glossary_vi.md#nhiệm-vụ-gom)): $N$ là số mục tiêu và mỗi ô là số người chăn tin cậy nhỏ nhất, với bán kính cảm nhận 10 (`lama_r50`) và cảm nhận vô hạn (`lama_r50_inf`). Thành công còn cần mọi người chăn ở trong đích (Bảng 11).

**Bảng 11: Số người chăn tin cậy nhỏ nhất cho nhiệm vụ gom, quy tắc 99 phần trăm.**

| N | lama_r50 | lama_r50_inf |
|---|---|---|
| 1 | none | 1 |
| 4 | none | 1 |
| 9 | none | 2 |
| 16 | none | 3 |
| 25 | none | 3 |
| 36 | none | 4 |
| 49 | none | 5 |
| 64 | none | 6 |
| 81 | none | 7 |
| 100 | none | 8 |
| 121 | [20] | 9 |
| 144 | 17-25 | 10 |
| 169 | 14-20 | 11 |
| 196 | 13-15 | 12 |
| 225 | 13 | 13 |
| 256 | 14 | 14 |
| 289 | 15 | 14-15 |
| 324 | 15 | 15 |
| 361 | 16 | 16 |
| 400 | 17 | 17 |

## 3. Giữ bầy ở 95 và 90 phần trăm

`dmin_f99_hold_share` cũng chạy nhiệm vụ giữ bầy khi chỉ cần 95% và 90% bầy ở trong đích; ở $N = 25$ điều đó cho phép một và hai con cừu ở ngoài (Bảng 12 và 13).

**Bảng 12: Đội tin cậy nhỏ nhất để giữ bầy, quy tắc 95 phần trăm.**

| protocol | layout | variant | N=25 | N=50 | N=100 |
|---|---|---|---|---|---|
| dmin_f99_hold_share | compact | goal 1.9 R_f | none | 1 | 1 |
| dmin_f99_hold_share | compact | goal 2.1 R_f | none | 1 | 1 |
| dmin_f99_hold_share | compact | goal 2.3 R_f | 1 | 1 | 1 |
| dmin_f99_hold_share | compact | goal 2.5 R_f | 1 | 1 | 1 |
| dmin_f99_hold_share | wide | goal 1.9 R_f | none | 1 | 1 |
| dmin_f99_hold_share | wide | goal 2.1 R_f | none | 1 | 1 |
| dmin_f99_hold_share | wide | goal 2.3 R_f | 1 | 1 | 1 |
| dmin_f99_hold_share | wide | goal 2.5 R_f | 1 | 1 | 1 |
| dmin_f99_hold_share | split | goal 1.9 R_f | none | 1 | 1 |
| dmin_f99_hold_share | split | goal 2.1 R_f | none | 1 | 1 |
| dmin_f99_hold_share | split | goal 2.3 R_f | 1 (max 19) | 1 | 1 |
| dmin_f99_hold_share | split | goal 2.5 R_f | 1 | 1 | 1 |
| dmin_f99_hold_share | outlier_rich | goal 1.9 R_f | none | 1 | 2 |
| dmin_f99_hold_share | outlier_rich | goal 2.1 R_f | none | 1 | 2 |
| dmin_f99_hold_share | outlier_rich | goal 2.3 R_f | 1 | 1 | 2 |
| dmin_f99_hold_share | outlier_rich | goal 2.5 R_f | 1 | 1 | 2 |

**Bảng 13: Đội tin cậy nhỏ nhất để giữ bầy, quy tắc 90 phần trăm.**

| protocol | layout | variant | N=25 | N=50 | N=100 |
|---|---|---|---|---|---|
| dmin_f99_hold_share | compact | goal 1.9 R_f | none | 1 | 1 |
| dmin_f99_hold_share | compact | goal 2.1 R_f | [1] (over 4) | 1 | 1 |
| dmin_f99_hold_share | compact | goal 2.3 R_f | 1 | 1 | 1 |
| dmin_f99_hold_share | compact | goal 2.5 R_f | 1 | 1 | 1 |
| dmin_f99_hold_share | wide | goal 1.9 R_f | none | 1 | 1 |
| dmin_f99_hold_share | wide | goal 2.1 R_f | [1] (over 3) | 1 | 1 |
| dmin_f99_hold_share | wide | goal 2.3 R_f | 1 | 1 | 1 |
| dmin_f99_hold_share | wide | goal 2.5 R_f | 1 | 1 | 1 |
| dmin_f99_hold_share | split | goal 1.9 R_f | none | 1 | 1 |
| dmin_f99_hold_share | split | goal 2.1 R_f | 1 (max 1, over 7) | 1 | 1 |
| dmin_f99_hold_share | split | goal 2.3 R_f | 1 | 1 | 1 |
| dmin_f99_hold_share | split | goal 2.5 R_f | 1 | 1 | 1 |
| dmin_f99_hold_share | outlier_rich | goal 1.9 R_f | none | 1 | 2 |
| dmin_f99_hold_share | outlier_rich | goal 2.1 R_f | 1 (max 1, over 5) | 1 | 2 |
| dmin_f99_hold_share | outlier_rich | goal 2.3 R_f | 1 | 1 | 2 |
| dmin_f99_hold_share | outlier_rich | goal 2.5 R_f | 1 | 1 | 2 |

## 4. Các lệnh

Các bảng được in bởi `cli/dmin_tables.py overview` từ các lượt chạy đã lưu trong `results/` (sinh ngày 2026-10-28); đừng sửa chúng bằng tay. Mỗi lệnh in một bảng cho mỗi quy tắc thành công; lệnh có `dmin_f99_hold_share` in thêm Bảng 12 và 13:

```bash
uv run cli/dmin_tables.py overview dmin_m12 dmin_m6 dmin_m3 dmin_s_base dmin_s_matched dmin_s_handler dmin_s_ring dmin_s_goal dmin_s_dogspeed dmin_s_gap dmin_fat dmin_kubo
uv run cli/dmin_tables.py overview dmin_m12 --value d_sat
uv run cli/dmin_tables.py overview dmin_f99_m12 dmin_f99_m6 dmin_f99_m3
uv run cli/dmin_tables.py overview dmin_f99_m12 dmin_f99_m6 dmin_f99_m3 dmin_f99_indep dmin_f99_kubo --value d_sat
uv run cli/dmin_tables.py overview dmin_f99_fat dmin_f99_indep dmin_f99_kubo
uv run cli/dmin_tables.py overview dmin_f99_s_base dmin_f99_s_matched dmin_f99_s_handler dmin_f99_s_ring dmin_f99_s_goal dmin_f99_s_dogspeed dmin_f99_s_gap
uv run cli/dmin_tables.py overview dmin_f99_hold dmin_f99_hold_spacing dmin_f99_hold_goal dmin_f99_hold_share
uv run cli/dmin_tables.py overview dmin_f99_c1.3 dmin_f99_c1.6 dmin_f99_c2.0 dmin_f99_k05
uv run cli/dmin_tables.py overview dmin_f99_view_range dmin_f99_view_comm
uv run cli/dmin_tables.py overview dmin_f99_big dmin_f99_big_dense dmin_f99_big_loose dmin_f99_big_cap
uv run cli/dmin_tables.py overview lama_r50 lama_r50_inf --transpose
```
