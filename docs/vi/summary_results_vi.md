# Tổng quan kết quả: mọi giao thức trong một cái nhìn

Trang này liệt kê 41 giao thức của nghiên cứu và các quyết định đã lưu cho từng đường cong của chúng, không kèm diễn giải, dành cho người đọc muốn thấy mọi lượt chạy cùng lúc trước khi đọc [báo cáo](d_min_report_vi.md). Các bảng đứng sau các hình của báo cáo nằm trong [results_tables.md](../report/results_tables.md), các thiết lập trong [hướng dẫn cấu hình](../guides/configuration.md), và mọi thuật ngữ trong [bảng thuật ngữ](glossary_vi.md).

## Mục lục

- [1. Cách đọc các bảng](#1-cách-đọc-các-bảng)
- [2. Quy tắc nghiêm ngặt: mọi con cừu trong đích](#2-quy-tắc-nghiêm-ngặt-mọi-con-cừu-trong-đích)
- [3. Quy tắc 99 phần trăm](#3-quy-tắc-99-phần-trăm)
- [4. Giữ bầy ở 95 và 90 phần trăm](#4-giữ-bầy-ở-95-và-90-phần-trăm)
- [5. Tạo lại các bảng](#5-tạo-lại-các-bảng)

## 1. Cách đọc các bảng

Một giao thức là một thí nghiệm, một tệp YAML cố định quy tắc chó, các bố cục xuất phát, các quy mô bầy $N$, các quy mô đội $D$ (số chó), quy tắc thành công và thời hạn ([bảng thuật ngữ](glossary_vi.md#lượt-chạy-và-thí-nghiệm)). Một đường cong là một quy tắc chó, bố cục, mức thiết lập và $N$ qua các quy mô đội đã thử. Một đội là tin cậy khi khoảng Clopper–Pearson 99% của tỷ lệ thành công nằm từ 0,90 trở lên, và $D_{\min}$ là đội tin cậy nhỏ nhất trên một đường cong ([quy tắc quyết định](d_min_report_vi.md#21-khi-nào-một-đội-là-tin-cậy)).

Mọi bảng trên trang này là đầu ra của `uv run cli/dmin_tables.py overview <folders>` trên các lượt chạy đã lưu trong `results/`, sinh ngày 2026-10-28; [mục 5](#5-tạo-lại-các-bảng) ghi các lệnh. Bảng giữ nguyên tên cột và dấu chấm thập phân của công cụ. Đừng sửa bảng bằng tay; hãy chạy lại các lệnh. Các bảng được tách theo quy tắc thành công, để không bảng nào trộn hai quy tắc:

- Quy tắc nghiêm ngặt ([mục 2](#2-quy-tắc-nghiêm-ngặt-mọi-con-cừu-trong-đích)): mọi con cừu ở trong đích tại một bước; 12 giao thức.
- Quy tắc 99 phần trăm ([mục 3](#3-quy-tắc-99-phần-trăm)): ít nhất $\lceil 0{,}99\,N \rceil$ con cừu ở trong đích tại một bước; 29 giao thức, trong các bảng theo chủ đề. $\lceil 0{,}99\,N \rceil = N$ với mọi $N$ dưới 100, nên ở $N$ = 25, 50 và 71 hai quy tắc trùng nhau. Các giao thức giữ bầy còn cần tỷ lệ đó ở lại trong đích suốt một lần thời gian lùa ([giữ bầy](glossary_vi.md#thành-công-và-độ-tin-cậy)), và nhiệm vụ gom còn cần mọi người chăn ở trong đích ([nhiệm vụ gom](task_design_vi.md#6-nhiệm-vụ-gom-lama-và-di-bernardo-2024)).
- 95 và 90 phần trăm ([mục 4](#4-giữ-bầy-ở-95-và-90-phần-trăm)): hai tỷ lệ khác mà `dmin_f99_hold_share` quét, để ngoài các bảng 99 phần trăm.

Một giao thức có `f99` trong tên và giao thức nghiêm ngặt có tên còn lại giống hệt (như `dmin_f99_m6` và `dmin_m6`) có cùng thiết lập ngoài quy tắc thành công, trừ việc các lưới 99 phần trăm ở 12 và 6 lần thời gian lùa thêm $N$ = 71, 141, 283 và 566 và `dmin_f99_kubo` chạy đội tới 24. Mục 2 và 3 bắt đầu bằng một bảng giao thức, với các cột:

- folder: tên giao thức, cũng là thư mục của nó trong `results/` ([tên giao thức](glossary_vi.md#lượt-chạy-và-thí-nghiệm)).
- method: quy tắc chó; `strombom_multi` là quy tắc đội của HerdSim, `independent` là quy tắc một chó của Strömbom do từng chó chạy, `fat` là nhắm con xa nhất (FAT), `kubo` là mô hình Kubo và `lama` là người chăn của Lama và di Bernardo (2024) ([mô hình cừu và quy tắc chó](glossary_vi.md#mô-hình-cừu-và-quy-tắc-chó)).
- task: `drive_to_goal`, nhiệm vụ lùa, hoặc `gather`, nhiệm vụ gom của Lama và di Bernardo (2024) ([nhiệm vụ gom](glossary_vi.md#nhiệm-vụ-gom)). Trong nhiệm vụ gom, $N$ là số mục tiêu và $D$ là số người chăn.
- rule: quy tắc thành công; `swept` khi giao thức chạy nhiều tỷ lệ như một yếu tố.
- deadline: giới hạn thời gian như tệp giao thức ghi, theo số lần thời gian lùa ([thời hạn](glossary_vi.md#nhiệm-vụ-lùa)), giây hoặc bước.
- changed: các thiết lập làm thay đổi một lượt mà giao thức đặt khác giá trị mặc định trong `protocols/configs/canonical.yaml`, và các tham số phương pháp mà nó đặt (ví dụ `drive_offset_cap=63`, điểm lùa bị giới hạn; `dog_spacing=2`, chó giữ cách nhau 2 m; `c=1.3`, trọng số hút). `metrics_stride`, chỉ quy định bao lâu ghi lịch sử theo bước một lần, được bỏ ra; hai lượt `lama_r50` đặt nó bằng 10. Các thiết lập được mô tả trong [hướng dẫn cấu hình](../guides/configuration.md#2-settings-added-by-the-follow-up-campaigns) và [bảng thuật ngữ](glossary_vi.md#biến-thể).
- swept: các yếu tố, những thiết lập được chạy ở nhiều giá trị; mỗi giá trị là một đường cong riêng và hiện trong bảng đường cong ở cột variant.

Các bảng đường cong có một hàng cho mỗi phương pháp, bố cục và biến thể, với các cột:

- layout: bố cục xuất phát (`compact`, `wide`, `split`, `outlier_rich`, hoặc `uniform` trong nhiệm vụ gom; [bố cục xuất phát](glossary_vi.md#bố-cục-xuất-phát-và-vị-trí-xuất-phát-của-chó)).
- N: các quy mô bầy của hàng. Bốn cột giá trị sau D tested ghi một mục cho mỗi $N$, theo cùng thứ tự.
- D tested: mọi quy mô đội có ít nhất một lượt ở một $N$ nào đó của hàng. Bộ chạy thích nghi thêm một quy mô đội ở giữa hai quy mô đã thử có quyết định khác nhau, nên các quy mô đội đã chạy khác nhau từ $N$ này sang $N$ khác.
- D_min: `3` đã quyết định, `3-8` một khoảng (8 là tin cậy, một đội nhỏ hơn từ 3 trở lên còn chưa quyết định sau 200 lượt), `[5]` một cận dưới (chưa đội nào tin cậy), `none on grid` khi mọi đội đã thử đều không tin cậy.
- D_sat: đội tin cậy nhỏ nhất mà không đội tin cậy lớn hơn nào dưới D_overcrowd nhanh hơn quá 5% thời gian hoàn thành với độ tin cậy 99%: `5` đã quyết định, `5-24` khi một đội lớn hơn vẫn có thể nhanh hơn, `[24]` khi đường cong vẫn còn nhanh lên ở đỉnh lưới.
- D_max: đội tin cậy lớn nhất dưới D_overcrowd, hoặc đội tin cậy lớn nhất. Ở đỉnh lưới nó là một cận dưới: chưa tìm thấy giới hạn trên.
- D_overcrowd: đội đầu tiên mà từ đó hai quy mô đội đã thử liên tiếp đều không tin cậy, tìm ở phía trên D_min (phía trên đội nhỏ nhất có khoảng tin cậy còn chạm 0,90, trên đường cong chưa có đội tin cậy; [quy mô đội](glossary_vi.md#quy-mô-đội)).

Dấu `-` trong một danh sách đánh dấu một $N$ không có giá trị; một dấu `-` duy nhất nghĩa là không $N$ nào của hàng có giá trị. D_sat chỉ được quyết định với hạt giống bổ sung cho các so sánh thời gian hoàn thành trong `dmin_m12` (tệp giao thức của nó ghi điều này), `dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3`, `dmin_f99_indep` và `dmin_f99_kubo`; ở các lượt chạy khác nó được đọc từ các hạt giống dùng để quyết định độ tin cậy, nên khoảng của nó có thể rộng hơn. Các thư mục kết quả không lưu thiết lập này, nên bảng không thể hiện được.

Các thiết lập lấy từ các tệp giao thức hiện tại; các quy mô bầy và quy mô đội lấy từ các quyết định đã lưu, vì `protocol.yaml` lưu trong thư mục chỉ giữ các quy mô của đợt chạy đầu. Ba thư mục trong `results/` không thuộc 41 giao thức và được bỏ ra: `dmin_pilot`, `dmin_s_ring_dog_in_goal` và `dmin_f99_hold_spacing_soft`; `results/diagnostics/` chứa các CSV của các công cụ chạy lại ([results_tables.md: Runs](../report/results_tables.md#runs)).

## 2. Quy tắc nghiêm ngặt: mọi con cừu trong đích

Bảng 1 liệt kê 12 giao thức nghiêm ngặt: ba lưới chính, bảy lượt chạy độ nhạy và hai đối chứng FAT và Kubo.

**Bảng 1: Các giao thức nghiêm ngặt.**

| folder | method | task | rule | deadline | changed | swept |
|---|---|---|---|---|---|---|
| dmin_m12 | strombom_multi | drive_to_goal | strict | 12x drive time | - | - |
| dmin_m6 | strombom_multi | drive_to_goal | strict | 6x drive time | - | - |
| dmin_m3 | strombom_multi | drive_to_goal | strict | 3x drive time | - | - |
| dmin_s_base | strombom_multi | drive_to_goal | strict | 6x drive time | - | - |
| dmin_s_matched | strombom_multi | drive_to_goal | strict | 6x drive time | separation_scale=1; dog_overlap_distance=1; r_a=1; noise_strength=0.1; r_s=75 | - |
| dmin_s_handler | strombom_multi | drive_to_goal | strict | 6x drive time | dog_start=handler | - |
| dmin_s_ring | strombom_multi | drive_to_goal | strict | 6x drive time | dog_start=ring | - |
| dmin_s_goal | strombom_multi | drive_to_goal | strict | 6x drive time | goal_radius_multiple=1.5 | - |
| dmin_s_dogspeed | strombom_multi | drive_to_goal | strict | 6x drive time | shepherd_speed=1.15 | - |
| dmin_s_gap | strombom_multi | drive_to_goal | strict | 6x drive time | - | dog_start_gap: 15, 30, 60 |
| dmin_fat | fat | drive_to_goal | strict | 6x drive time | calibrate_as=strombom_multi | - |
| dmin_kubo | kubo | drive_to_goal | strict | 500 s | - | - |

Bảng 2 ghi quy mô đội của mọi đường cong nghiêm ngặt:

**Bảng 2: Quy mô đội theo quy tắc nghiêm ngặt.**

| folder | method | layout | variant | N | D tested | D_min | D_sat | D_max | D_overcrowd |
|---|---|---|---|---|---|---|---|---|---|
| dmin_m12 | strombom_multi | compact | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1 | 24, 24, 24, 24, 24 | - |
| dmin_m12 | strombom_multi | wide | - | 25, 50, 100, 200, 400 | 1-6, 8, 12, 16, 24 | 1, 1, 1, 2, 3 | 1, 1, 2, 3-24, 6-24 | 24, 24, 24, 24, 24 | - |
| dmin_m12 | strombom_multi | split | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1-2, 3 | 1, 1, 4, 3-24, 3-24 | 24, 24, 24, 24, 24 | - |
| dmin_m12 | strombom_multi | outlier_rich | - | 25, 50, 100, 200, 400 | 1-6, 8, 12, 16, 24 | 1, 1, 1-3, 2, 3 | 1, 1-24, 3, 5-24, 6-24 | 24, 24, 24, 24, 24 | - |
| dmin_m6 | strombom_multi | compact | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1 | 24, 24, 24, 24, 24 | - |
| dmin_m6 | strombom_multi | wide | - | 25, 50, 100, 200, 400 | 1-4, 6, 8-10, 12, 14-18, 20, 24 | 1, 1, 1, 3, [9] | 1, 1, 1-24, 3-16, - | 24, 24, 24, 16, - | - |
| dmin_m6 | strombom_multi | split | - | 25, 50, 100, 200, 400 | 1-6, 8, 12, 16, 24 | 1, 1, 1, none on grid, none on grid | 1, 1, 5, -, - | 24, 24, 24, -, - | - |
| dmin_m6 | strombom_multi | outlier_rich | - | 25, 50, 100, 200, 400 | 1-6, 8, 10-12, 16, 24 | 1, 1, 3, [12], none on grid | 1, 1-24, 3, -, - | 24, 24, 24, -, - | - |
| dmin_m3 | strombom_multi | compact | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1 | 24, 24, 24, 24, 24 | - |
| dmin_m3 | strombom_multi | wide | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 3, none on grid, none on grid | 1, 1, 3, -, - | 24, 24, 24, -, - | - |
| dmin_m3 | strombom_multi | split | - | 25, 50, 100, 200, 400 | 1-6, 8, 12, 16, 24 | 1, 1, 1, none on grid, none on grid | 1, 1, 1, -, - | 24, 24, 1, -, - | -, -, 2, -, - |
| dmin_m3 | strombom_multi | outlier_rich | - | 25, 50, 100, 200, 400 | 1-8, 12, 16, 24 | 1, 1, 3-8, none on grid, none on grid | 1, 1-24, 8, -, - | 24, 24, 24, -, - | - |
| dmin_s_base | strombom_multi | wide | - | 100, 200, 400 | 1-4, 6, 8-10, 12, 14-16 | 1, 3, [9] | 1-16, 3-16, - | 16, 16, - | - |
| dmin_s_base | strombom_multi | outlier_rich | - | 100, 200, 400 | 1-6, 8, 10-12, 16 | 3, [12], none on grid | 3, -, - | 16, -, - | - |
| dmin_s_matched | strombom_multi | wide | - | 100, 200, 400 | 1-8, 12, 16 | 1-6, none on grid, none on grid | 6, -, - | 6, -, - | - |
| dmin_s_matched | strombom_multi | outlier_rich | - | 100, 200, 400 | 1-4, 6, 8, 12, 16 | [1], none on grid, none on grid | - | - | - |
| dmin_s_handler | strombom_multi | wide | - | 100, 200, 400 | 1-6, 8, 12, 16 | 1, 3, none on grid | 2, 3-16, - | 16, 16, - | - |
| dmin_s_handler | strombom_multi | outlier_rich | - | 100, 200, 400 | 1-4, 6, 8, 12, 16 | 2, [3], none on grid | 2-16, -, - | 16, -, - | -, 4, - |
| dmin_s_ring | strombom_multi | wide | - | 100, 200, 400 | 1-8, 12, 16 | 1, 3-5, [8] | 1-16, 5, - | 16, 16, - | - |
| dmin_s_ring | strombom_multi | outlier_rich | - | 100, 200, 400 | 1-8, 12, 16 | 2-7, [5], none on grid | 7, -, - | 16, -, - | - |
| dmin_s_goal | strombom_multi | wide | - | 100, 200, 400 | 1-4, 6, 8, 12, 16 | 1-3, none on grid, none on grid | 3, -, - | 16, -, - | - |
| dmin_s_goal | strombom_multi | outlier_rich | - | 100, 200, 400 | 1-6, 8, 12, 14-16 | 3, none on grid, none on grid | 3, -, - | 15, -, - | - |
| dmin_s_dogspeed | strombom_multi | wide | - | 100, 200, 400 | 1-6, 8, 12, 16 | 1, 3, 5 | 2, 3, 5 | 16, 16, 16 | - |
| dmin_s_dogspeed | strombom_multi | outlier_rich | - | 100, 200, 400 | 1-6, 8, 12, 16 | 2-3, 4, 6 | 3, 4, 6 | 16, 16, 16 | - |
| dmin_s_gap | strombom_multi | wide | dog_start_gap=15.0 | 100, 200, 400 | 1-4, 6, 8, 12, 14-16 | 1, [3], none on grid | 1-15, -, - | 15, -, - | -, 4, - |
| dmin_s_gap | strombom_multi | wide | dog_start_gap=30.0 | 100, 200, 400 | 1-4, 6, 8-10, 12, 14-16 | 1, 3, [9] | 1-16, 3-16, - | 16, 16, - | - |
| dmin_s_gap | strombom_multi | wide | dog_start_gap=60.0 | 100, 200, 400 | 1-8, 12, 16 | 1, 3-4, 6-7 | 3, 4, 7 | 16, 16, 16 | - |
| dmin_s_gap | strombom_multi | outlier_rich | dog_start_gap=15.0 | 100, 200, 400 | 1-4, 6-8, 12, 16 | [1], none on grid, none on grid | - | - | 4, -, - |
| dmin_s_gap | strombom_multi | outlier_rich | dog_start_gap=30.0 | 100, 200, 400 | 1-6, 8, 10-12, 16 | 3, [12], none on grid | 3, -, - | 16, -, - | - |
| dmin_s_gap | strombom_multi | outlier_rich | dog_start_gap=60.0 | 100, 200, 400 | 1-6, 8, 10-12, 16 | 3, 5, [12] | 3, 5, - | 16, 16, - | - |
| dmin_fat | fat | compact | - | 25, 50, 100, 200, 400 | 1-6, 8, 12, 16, 24 | 1, 1, 1, 1, none on grid | 1, 1, 1, 1, - | 24, 24, 24, 16, - | - |
| dmin_fat | fat | wide | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, none on grid, none on grid | 1, 1, 1, -, - | 24, 24, 24, -, - | - |
| dmin_fat | fat | split | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, none on grid, none on grid | 1, 1, 1-24, -, - | 24, 24, 24, -, - | - |
| dmin_fat | fat | outlier_rich | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 2, none on grid, none on grid | 1, 1, 2-24, -, - | 24, 24, 24, -, - | - |
| dmin_kubo | kubo | compact | - | 25, 50, 100 | 1-4, 6, 10 | 1, 1, 1 | [10], [10], [10] | 10, 10, 10 | - |

## 3. Quy tắc 99 phần trăm

Bảng 3 liệt kê 29 giao thức chạy theo quy tắc 99 phần trăm. `dmin_f99_hold_share` quét tỷ lệ như một yếu tố; mục này chỉ có các đường cong 99 phần trăm của nó.

**Bảng 3: Các giao thức theo quy tắc 99 phần trăm.**

| folder | method | task | rule | deadline | changed | swept |
|---|---|---|---|---|---|---|
| dmin_f99_m12 | strombom_multi | drive_to_goal | 99 percent | 12x drive time | - | - |
| dmin_f99_m6 | strombom_multi | drive_to_goal | 99 percent | 6x drive time | - | - |
| dmin_f99_m3 | strombom_multi | drive_to_goal | 99 percent | 3x drive time | - | - |
| dmin_f99_fat | fat | drive_to_goal | 99 percent | 6x drive time | calibrate_as=strombom_multi | - |
| dmin_f99_indep | independent | drive_to_goal | 99 percent | 6x drive time | calibrate_as=strombom_multi | - |
| dmin_f99_kubo | kubo | drive_to_goal | 99 percent | 500 s | - | - |
| dmin_f99_s_base | strombom_multi | drive_to_goal | 99 percent | 6x drive time | - | - |
| dmin_f99_s_matched | strombom_multi | drive_to_goal | 99 percent | 6x drive time | separation_scale=1; dog_overlap_distance=1; r_a=1; noise_strength=0.1; r_s=75 | - |
| dmin_f99_s_handler | strombom_multi | drive_to_goal | 99 percent | 6x drive time | dog_start=handler | - |
| dmin_f99_s_ring | strombom_multi | drive_to_goal | 99 percent | 6x drive time | dog_start=ring | - |
| dmin_f99_s_goal | strombom_multi | drive_to_goal | 99 percent | 6x drive time | goal_radius_multiple=1.5 | - |
| dmin_f99_s_dogspeed | strombom_multi | drive_to_goal | 99 percent | 6x drive time | shepherd_speed=1.15 | - |
| dmin_f99_s_gap | strombom_multi | drive_to_goal | 99 percent | 6x drive time | - | dog_start_gap: 15, 30, 60 |
| dmin_f99_hold | strombom_multi | drive_to_goal | 99 percent | 6x drive time | hold_drive_multiple=1; hold_withdraw=True | - |
| dmin_f99_hold_spacing | strombom_multi | drive_to_goal | 99 percent | 6x drive time | hold_drive_multiple=1; hold_withdraw=True; dog_spacing=2 | - |
| dmin_f99_hold_goal | strombom_multi | drive_to_goal | 99 percent | 6x drive time | hold_drive_multiple=1; hold_withdraw=True | goal_radius_multiple: 1.9, 2.5, 3 |
| dmin_f99_hold_share | strombom_multi | drive_to_goal | swept | 6x drive time | hold_drive_multiple=1; hold_withdraw=True | goal_radius_multiple: 1.9, 2.1, 2.3, 2.5; success_fraction: 0.9, 0.95, 0.99 |
| dmin_f99_c1.3 | strombom_multi | drive_to_goal | 99 percent | 12x drive time | c=1.3 | - |
| dmin_f99_c1.6 | strombom_multi | drive_to_goal | 99 percent | 12x drive time | c=1.6 | - |
| dmin_f99_c2.0 | strombom_multi | drive_to_goal | 99 percent | 12x drive time | c=2 | - |
| dmin_f99_k05 | strombom_multi | drive_to_goal | 99 percent | 12x drive time | n_neighbors=0.5N | - |
| dmin_f99_view_range | strombom_multi | drive_to_goal | 99 percent | 6x drive time | - | sensing_range: 0, 15, 30, 45, 65, 100 |
| dmin_f99_view_comm | strombom_multi | drive_to_goal | 99 percent | 6x drive time | sensing_range=65 | communication: neighbour, shared |
| dmin_f99_big | strombom_multi | drive_to_goal | 99 percent | 12x drive time | impose_radius_above=566 | - |
| dmin_f99_big_dense | strombom_multi | drive_to_goal | 99 percent | 12x drive time | impose_radius_above=566; imposed_radius_scale=0.707107 | - |
| dmin_f99_big_loose | strombom_multi | drive_to_goal | 99 percent | 12x drive time | impose_radius_above=566; imposed_radius_scale=1.41421 | - |
| dmin_f99_big_cap | strombom_multi | drive_to_goal | 99 percent | 12x drive time | drive_offset_cap=63; impose_radius_above=566 | - |
| lama_r50 | lama | gather | 99 percent | 166667 ticks | - | - |
| lama_r50_inf | lama | gather | 99 percent | 166667 ticks | sensing_radius=inf | - |

### 3.1 Các lưới chính

Bảng 4 ghi ba lưới chính ở 12, 6 và 3 lần thời gian lùa; các lưới ở 12 và 6 lần thời gian lùa chạy chín quy mô bầy tới 566.

**Bảng 4: Quy mô đội trên các lưới chính, quy tắc 99 phần trăm.**

| folder | method | layout | variant | N | D tested | D_min | D_sat | D_max | D_overcrowd |
|---|---|---|---|---|---|---|---|---|---|
| dmin_f99_m12 | strombom_multi | compact | - | 25, 50, 71, 100, 141, 200, 283, 400, 566 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1, 1, 1, 1, 1 | 24, 24, 24, 24, 24, 24, 24, 24, 24 | - |
| dmin_f99_m12 | strombom_multi | wide | - | 25, 50, 71, 100, 141, 200, 283, 400, 566 | 1-8, 12, 16, 24 | 1, 1, 1, 1, 2, 1-2, 2, 2, 2-3 | 1, 1, 1, 2, 3, 3, 4, 5, 7-24 | 24, 24, 24, 24, 24, 24, 24, 24, 24 | - |
| dmin_f99_m12 | strombom_multi | split | - | 25, 50, 71, 100, 141, 200, 283, 400, 566 | 1-10, 12-16, 20-24 | 1, 1, 1, 1, 1, 1, 2, 2, 3 | 1, 1, 1, 4, 7, 2-24, 2-24, 4-24, 3-24 | 24, 24, 24, 24, 24, 24, 24, 24, 24 | - |
| dmin_f99_m12 | strombom_multi | outlier_rich | - | 25, 50, 71, 100, 141, 200, 283, 400, 566 | 1-8, 10-12, 14-16, 24 | 1, 1, 1, 1-2, 2, 2, 2, 2, 2-3 | 1, 1-24, 2, 3, 3, 4, 5-24, 6-24, 8-24 | 24, 24, 24, 24, 24, 24, 24, 24, 24 | - |
| dmin_f99_m6 | strombom_multi | compact | - | 25, 50, 71, 100, 141, 200, 283, 400, 566 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1, 1, 1, 1, 1 | 24, 24, 24, 24, 24, 24, 24, 24, 24 | - |
| dmin_f99_m6 | strombom_multi | wide | - | 25, 50, 71, 100, 141, 200, 283, 400, 566 | 1-8, 12, 16, 24 | 1, 1, 1, 1, 2, 2, 2-3, 2-3, 3-7 | 1, 1, 1, 2, 3, 3, 4, 5, 7-24 | 24, 24, 24, 24, 24, 24, 24, 24, 24 | - |
| dmin_f99_m6 | strombom_multi | split | - | 25, 50, 71, 100, 141, 200, 283, 400, 566 | 1-12, 14-16, 18-20, 22-24 | 1, 1, 1, 1, 1, [1], [5], [5], none on grid | 1, 1, 1, 4, 7, -, -, -, - | 24, 24, 24, 24, 24, -, -, -, - | -, -, -, -, -, 4, 15, 10, - |
| dmin_f99_m6 | strombom_multi | outlier_rich | - | 25, 50, 71, 100, 141, 200, 283, 400, 566 | 1-8, 10-12, 16, 24 | 1, 1, 1, 2, 2, 2-3, 2-3, 3, 3-6 | 1, 1-24, 2, 3, 3, 4, 5-24, 6-24, 8-12 | 24, 24, 24, 24, 24, 24, 24, 24, 12 | - |
| dmin_f99_m3 | strombom_multi | compact | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1 | 24, 24, 24, 24, 24 | - |
| dmin_f99_m3 | strombom_multi | wide | - | 25, 50, 100, 200, 400 | 1-6, 8, 12, 16, 24 | 1, 1, 2, 3, 5-6 | 1, 1, 2, 3, 6 | 24, 24, 24, 24, 24 | - |
| dmin_f99_m3 | strombom_multi | split | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, none on grid, none on grid | 1, 1, 4, -, - | 24, 24, 24, -, - | - |
| dmin_f99_m3 | strombom_multi | outlier_rich | - | 25, 50, 100, 200, 400 | 1-10, 12, 16, 24 | 1, 1, 2, 4-10, [6] | 1, 1-24, 3, 10, - | 24, 24, 24, 24, - | -, -, -, -, 7 |

### 3.2 Các quy tắc chó khác

Bảng 5 ghi các quy tắc chó ngoài quy tắc đội, tất cả ở 6 lần thời gian lùa trừ Kubo (500 s, chỉ `compact`).

**Bảng 5: Quy mô đội với FAT, chó độc lập và Kubo, quy tắc 99 phần trăm.**

| folder | method | layout | variant | N | D tested | D_min | D_sat | D_max | D_overcrowd |
|---|---|---|---|---|---|---|---|---|---|
| dmin_f99_fat | fat | compact | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 10-14, 16, 24 | 1, 1, 1, 1, [12] | 1, 1, 1, 1, - | 24, 24, 24, 24, - | -, -, -, -, 13 |
| dmin_f99_fat | fat | wide | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, none on grid, none on grid | 1, 1, 1, -, - | 24, 24, 24, -, - | - |
| dmin_f99_fat | fat | split | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, none on grid, none on grid | 1, 1, 1-24, -, - | 24, 24, 24, -, - | - |
| dmin_f99_fat | fat | outlier_rich | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 2, none on grid, none on grid | 1, 1, 2-24, -, - | 24, 24, 24, -, - | - |
| dmin_f99_indep | independent | compact | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1 | 24, 24, 24, 24, 24 | - |
| dmin_f99_indep | independent | wide | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 2-3, none on grid | 1, 1, 2, 3, - | 24, 24, 24, 24, - | - |
| dmin_f99_indep | independent | split | - | 25, 50, 100, 200, 400 | 1-6, 8, 12, 16, 24 | 1, 1, 1, 1-3, none on grid | 1, 1, 2, 5-24, - | 24, 24, 24, 24, - | - |
| dmin_f99_indep | independent | outlier_rich | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 2, 3, none on grid | 1, 1, 2-24, 4-24, - | 24, 24, 24, 24, - | - |
| dmin_f99_kubo | kubo | compact | - | 25, 50, 100 | 1-4, 6, 8, 10, 12, 14-18, 20, 24 | 1, 1, 1 | 16-24, 17-24, 16-24 | 24, 24, 24 | - |

### 3.3 Thay đổi thiết lập

Bảng 6 ghi bảy lượt chạy độ nhạy ở 6 lần thời gian lùa: lượt cơ sở và sáu biến thể của nó, trên `wide` và `outlier_rich`.

**Bảng 6: Quy mô đội trong các lượt chạy độ nhạy, quy tắc 99 phần trăm.**

| folder | method | layout | variant | N | D tested | D_min | D_sat | D_max | D_overcrowd |
|---|---|---|---|---|---|---|---|---|---|
| dmin_f99_s_base | strombom_multi | wide | - | 100, 200, 400 | 1-4, 6, 8, 12, 16 | 1, 2, 2-3 | 1-16, 3-16, 6 | 16, 16, 16 | - |
| dmin_f99_s_base | strombom_multi | outlier_rich | - | 100, 200, 400 | 1-4, 6, 8, 12, 16 | 2, 2-3, 3 | 3, 4, 6-16 | 16, 16, 16 | - |
| dmin_f99_s_matched | strombom_multi | wide | - | 100, 200, 400 | 1-4, 6, 8, 12, 16 | 1, 1, 2 | 1, 1, 2-16 | 16, 16, 16 | - |
| dmin_f99_s_matched | strombom_multi | outlier_rich | - | 100, 200, 400 | 1-4, 6, 8-10, 12, 16 | 1, 1, 2-3 | 1, 1-16, 3-16 | 16, 16, 16 | - |
| dmin_f99_s_handler | strombom_multi | wide | - | 100, 200, 400 | 1-8, 10-12, 16 | 1, 2-3, 2-3 | 2, 4-16, 3-16 | 16, 16, 16 | - |
| dmin_f99_s_handler | strombom_multi | outlier_rich | - | 100, 200, 400 | 1-8, 12, 16 | 2, 2-3, 3 | 2-16, 7, 3-5 | 16, 16, 5 | - |
| dmin_f99_s_ring | strombom_multi | wide | - | 100, 200, 400 | 1-4, 6, 8, 12, 16 | 1, 2-3, 3 | 1-16, 6, 8 | 16, 16, 16 | - |
| dmin_f99_s_ring | strombom_multi | outlier_rich | - | 100, 200, 400 | 1-4, 6, 8, 12, 16 | 2, 2, 3 | 6, 6, 8-16 | 16, 16, 16 | - |
| dmin_f99_s_goal | strombom_multi | wide | - | 100, 200, 400 | 1-10, 12, 16 | 1, 2, 5-6 | 2, 3-16, 6 | 16, 16, 16 | - |
| dmin_f99_s_goal | strombom_multi | outlier_rich | - | 100, 200, 400 | 1-4, 6, 8-10, 12, 16 | 2, 2-3, none on grid | 3, 9, - | 16, 16, - | - |
| dmin_f99_s_dogspeed | strombom_multi | wide | - | 100, 200, 400 | 1-4, 6, 8, 12, 16 | 1, 2-3, 2-3 | 2, 3, 6 | 16, 16, 16 | - |
| dmin_f99_s_dogspeed | strombom_multi | outlier_rich | - | 100, 200, 400 | 1-4, 6, 8, 12, 16 | 2, 2-3, 3 | 2-16, 3-16, 6 | 16, 16, 16 | - |
| dmin_f99_s_gap | strombom_multi | wide | dog_start_gap=15.0 | 100, 200, 400 | 1-4, 6, 8, 12, 16 | 1, 2, 2-3 | 2-16, 3-16, 6 | 16, 16, 16 | - |
| dmin_f99_s_gap | strombom_multi | wide | dog_start_gap=30.0 | 100, 200, 400 | 1-4, 6, 8, 12, 16 | 1, 2, 2-3 | 1-16, 3-16, 6 | 16, 16, 16 | - |
| dmin_f99_s_gap | strombom_multi | wide | dog_start_gap=60.0 | 100, 200, 400 | 1-4, 6, 8, 12, 16 | 1, 2-3, 2-3 | 2-16, 3-16, 6 | 16, 16, 16 | - |
| dmin_f99_s_gap | strombom_multi | outlier_rich | dog_start_gap=15.0 | 100, 200, 400 | 1-6, 8, 10-14, 16 | 1-2, 2, 3 | 3, 3-13, 6-12 | 16, 13, 12 | - |
| dmin_f99_s_gap | strombom_multi | outlier_rich | dog_start_gap=30.0 | 100, 200, 400 | 1-4, 6, 8, 12, 16 | 2, 2-3, 3 | 3, 4, 6-16 | 16, 16, 16 | - |
| dmin_f99_s_gap | strombom_multi | outlier_rich | dog_start_gap=60.0 | 100, 200, 400 | 1-4, 6, 8, 12, 16 | 2, 2-3, 3 | 3, 4, 8 | 16, 16, 16 | - |

### 3.4 Giữ bầy và chó chiếm chỗ

Bảng 7 ghi nhiệm vụ giữ bầy ([giữ bầy](glossary_vi.md#thành-công-và-độ-tin-cậy)), với chó dạng điểm (`dmin_f99_hold`), với chó giữ cách nhau 2 m (`dmin_f99_hold_spacing`), và với đích lớn hơn (`dmin_f99_hold_goal`, cùng các đường cong 99 phần trăm của `dmin_f99_hold_share`). Bán kính đích tính theo bán kính bầy $R_f$.

**Bảng 7: Quy mô đội để giữ bầy, quy tắc 99 phần trăm.**

| folder | method | layout | variant | N | D tested | D_min | D_sat | D_max | D_overcrowd |
|---|---|---|---|---|---|---|---|---|---|
| dmin_f99_hold | strombom_multi | compact | - | 25, 50, 100, 200, 400 | 1-4, 6-13, 16, 24 | none on grid, none on grid, 1, 1, 1 | -, -, 1, 1, 1 | -, -, 24, 24, 24 | - |
| dmin_f99_hold | strombom_multi | wide | - | 25, 50, 100, 200, 400 | 1-4, 6-13, 16, 24 | none on grid, none on grid, 1, 2, 3 | -, -, 1-24, 3, 6 | -, -, 24, 24, 24 | - |
| dmin_f99_hold | strombom_multi | split | - | 25, 50, 100, 200, 400 | 1-4, 6-13, 16, 24 | none on grid, none on grid, 1, [2], none on grid | -, -, 4, -, - | -, -, 24, -, - | -, -, -, 3, - |
| dmin_f99_hold | strombom_multi | outlier_rich | - | 25, 50, 100, 200, 400 | 1-4, 6-13, 16, 24 | none on grid, none on grid, 3, 3, 3-4 | -, -, 3, 10, 6 | -, -, 24, 24, 6 | - |
| dmin_f99_hold_spacing | strombom_multi | compact | - | 25, 50, 100, 200, 400 | 1-4, 6-13, 16, 24 | none on grid, none on grid, 1, 1, 1 | -, -, 1, 1, 1 | -, -, 24, 24, 24 | - |
| dmin_f99_hold_spacing | strombom_multi | wide | - | 25, 50, 100, 200, 400 | 1-13, 16, 24 | none on grid, none on grid, 1, 2, 3 | -, -, 1-24, 3, 6 | -, -, 24, 24, 24 | - |
| dmin_f99_hold_spacing | strombom_multi | split | - | 25, 50, 100, 200, 400 | 1-4, 6-13, 16, 24 | none on grid, none on grid, 1, [2], none on grid | -, -, 4, -, - | -, -, 24, -, - | -, -, -, 3, - |
| dmin_f99_hold_spacing | strombom_multi | outlier_rich | - | 25, 50, 100, 200, 400 | 1-13, 16, 24 | none on grid, none on grid, 2-3, 3, [3] | -, -, 3, 12, - | -, -, 24, 24, - | -, -, -, -, 9 |
| dmin_f99_hold_goal | strombom_multi | compact | goal_radius_multiple=1.9 | 25, 50, 100 | 1-4, 6, 8, 12, 16, 24 | none on grid, none on grid, 1 | -, -, 1 | -, -, 24 | - |
| dmin_f99_hold_goal | strombom_multi | compact | goal_radius_multiple=2.5 | 25, 50, 100 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1 | 1, 1, 1 | 3, 24, 24 | - |
| dmin_f99_hold_goal | strombom_multi | compact | goal_radius_multiple=3.0 | 25, 50, 100 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1 | 1, 1, 1 | 24, 24, 24 | - |
| dmin_f99_hold_goal | strombom_multi | wide | goal_radius_multiple=1.9 | 25, 50, 100 | 1-4, 6, 8, 12, 16, 24 | none on grid, none on grid, 1 | -, -, 1-24 | -, -, 24 | - |
| dmin_f99_hold_goal | strombom_multi | wide | goal_radius_multiple=2.5 | 25, 50, 100 | 1-6, 8, 12, 16, 24 | 1-2, 1, 1 | 2, 1, 1-24 | 4, 24, 24 | - |
| dmin_f99_hold_goal | strombom_multi | wide | goal_radius_multiple=3.0 | 25, 50, 100 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1 | 1, 1, 1-24 | 24, 24, 24 | - |
| dmin_f99_hold_goal | strombom_multi | split | goal_radius_multiple=1.9 | 25, 50, 100 | 1-4, 6, 8, 12, 16, 24 | none on grid, none on grid, 1 | -, -, 4 | -, -, 24 | - |
| dmin_f99_hold_goal | strombom_multi | split | goal_radius_multiple=2.5 | 25, 50, 100 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1 | 1, 1, 2-24 | 3, 24, 24 | - |
| dmin_f99_hold_goal | strombom_multi | split | goal_radius_multiple=3.0 | 25, 50, 100 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1 | 1, 1, 2-24 | 24, 24, 24 | - |
| dmin_f99_hold_goal | strombom_multi | outlier_rich | goal_radius_multiple=1.9 | 25, 50, 100 | 1-4, 6, 8, 12, 16, 24 | none on grid, none on grid, 3 | -, -, 3 | -, -, 24 | - |
| dmin_f99_hold_goal | strombom_multi | outlier_rich | goal_radius_multiple=2.5 | 25, 50, 100 | 1-4, 6-8, 12, 16, 24 | 1-3, 1, 2 | 3, 1, 3 | 6, 24, 24 | - |
| dmin_f99_hold_goal | strombom_multi | outlier_rich | goal_radius_multiple=3.0 | 25, 50, 100 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 2 | 1, 1, 3 | 24, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | compact | goal_radius_multiple=1.9 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, none on grid, 1 | -, -, 1 | -, -, 24 | - |
| dmin_f99_hold_share | strombom_multi | compact | goal_radius_multiple=2.1 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, [1], 1 | -, -, 1 | -, -, 24 | - |
| dmin_f99_hold_share | strombom_multi | compact | goal_radius_multiple=2.3 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 1 | -, 1, 1 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | compact | goal_radius_multiple=2.5 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 1 | 1, 1, 1 | 1, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | wide | goal_radius_multiple=1.9 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, none on grid, 1 | -, -, 1-24 | -, -, 24 | - |
| dmin_f99_hold_share | strombom_multi | wide | goal_radius_multiple=2.1 | 25, 50, 100 | 1-6, 8, 24 | none on grid, [1], 1 | -, -, 1-24 | -, -, 24 | - |
| dmin_f99_hold_share | strombom_multi | wide | goal_radius_multiple=2.3 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 1 | -, 1, 1-24 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | wide | goal_radius_multiple=2.5 | 25, 50, 100 | 1-2, 4-6, 8, 24 | 1-2, 1, 1 | 2, 1, 1-24 | 4, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | split | goal_radius_multiple=1.9 | 25, 50, 100 | 1-4, 8, 24 | none on grid, none on grid, 1 | -, -, 4 | -, -, 24 | - |
| dmin_f99_hold_share | strombom_multi | split | goal_radius_multiple=2.1 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, [1], 1 | -, -, 2-24 | -, -, 24 | - |
| dmin_f99_hold_share | strombom_multi | split | goal_radius_multiple=2.3 | 25, 50, 100 | 1-4, 8, 24 | none on grid, 1, 1 | -, 1, 2-24 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | split | goal_radius_multiple=2.5 | 25, 50, 100 | 1-4, 8, 24 | 1, 1, 1 | 1, 1, 2-24 | 3, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | outlier_rich | goal_radius_multiple=1.9 | 25, 50, 100 | 1-4, 8, 24 | none on grid, none on grid, 3 | -, -, 3 | -, -, 24 | - |
| dmin_f99_hold_share | strombom_multi | outlier_rich | goal_radius_multiple=2.1 | 25, 50, 100 | 1-6, 8, 24 | none on grid, [1], 2 | -, -, 4 | -, -, 24 | - |
| dmin_f99_hold_share | strombom_multi | outlier_rich | goal_radius_multiple=2.3 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 2 | -, 1, 4 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | outlier_rich | goal_radius_multiple=2.5 | 25, 50, 100 | 1-4, 6-8, 24 | 1-3, 1, 2 | 3, 1, 4 | 6, 24, 24 | - |

### 3.5 Sự gắn kết

Bảng 8 ghi các lượt chạy gắn kết ở 12 lần thời gian lùa: trọng số hút $c$ tăng từ 1,05 của Strömbom et al. (2014) lên 1,3, 1,6 và 2,0 (`dmin_f99_c*`), và số hàng xóm mà mỗi con cừu bị hút về giảm từ cả $N - 1$ xuống nửa bầy (`dmin_f99_k05`, `n_neighbors=0.5N`).

**Bảng 8: Quy mô đội khi thay đổi sự gắn kết, quy tắc 99 phần trăm.**

| folder | method | layout | variant | N | D tested | D_min | D_sat | D_max | D_overcrowd |
|---|---|---|---|---|---|---|---|---|---|
| dmin_f99_c1.3 | strombom_multi | compact | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1 | 24, 24, 24, 24, 24 | - |
| dmin_f99_c1.3 | strombom_multi | wide | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 2 | 1, 1, 2, 3, 6 | 24, 24, 24, 24, 24 | - |
| dmin_f99_c1.3 | strombom_multi | split | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 1-2 | 1, 1, 1, 3-24, 6 | 24, 24, 24, 24, 24 | - |
| dmin_f99_c1.3 | strombom_multi | outlier_rich | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 2, 2 | 1, 1-24, 2, 3-24, 6 | 24, 24, 24, 24, 24 | - |
| dmin_f99_c1.6 | strombom_multi | compact | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1 | 24, 24, 24, 24, 24 | - |
| dmin_f99_c1.6 | strombom_multi | wide | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 2 | 1, 1, 2, 3, 6 | 24, 24, 24, 24, 24 | - |
| dmin_f99_c1.6 | strombom_multi | split | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 1 | 1, 1, 1-24, 3, 6 | 24, 24, 24, 24, 24 | - |
| dmin_f99_c1.6 | strombom_multi | outlier_rich | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 2 | 1, 1-24, 2-24, 3-24, 6 | 24, 24, 24, 24, 24 | - |
| dmin_f99_c2.0 | strombom_multi | compact | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 1 | 1, 1, 1, 1, 1 | 24, 24, 24, 24, 24 | - |
| dmin_f99_c2.0 | strombom_multi | wide | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 2 | 1, 1, 2, 3, 6 | 24, 24, 24, 24, 24 | - |
| dmin_f99_c2.0 | strombom_multi | split | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 2 | 1, 1, 1, 3, 3 | 24, 24, 24, 24, 24 | - |
| dmin_f99_c2.0 | strombom_multi | outlier_rich | - | 25, 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1, 2 | 1, 1-24, 1-24, 2-24, 4 | 24, 24, 24, 24, 24 | - |
| dmin_f99_k05 | strombom_multi | compact | - | 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 1, 1 | 1, 1, 1, 1 | 24, 24, 24, 24 | - |
| dmin_f99_k05 | strombom_multi | wide | - | 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 1, 2, 2-4 | 1, 2, 3-24, 6 | 24, 24, 24, 24 | - |
| dmin_f99_k05 | strombom_multi | split | - | 50, 100, 200, 400 | 1-8, 12, 16, 20-22, 24 | 1-4, 1-2, 3-4, 4-5 | 4-24, 2-7, 4-20, 5-24 | 24, 7, 20, 24 | - |
| dmin_f99_k05 | strombom_multi | outlier_rich | - | 50, 100, 200, 400 | 1-4, 6, 8, 12, 16, 24 | 1, 2, 2, 2 | 1-24, 3, 4-24, 6-24 | 24, 24, 24, 24 | - |

### 3.6 Cảm nhận hạn chế

Bảng 9 ghi các lượt chạy về cảm nhận ở 6 lần thời gian lùa ([tầm cảm nhận và chia sẻ](glossary_vi.md#biến-thể)): tầm cảm nhận từ 15 tới 100 m không chia sẻ, bên cạnh tầm nhìn đầy đủ (`sensing_range=0.0`, biết mọi con cừu), và ở 65 m, chia sẻ với các chó trong tầm (`neighbour`) hoặc với cả đội (`shared`).

**Bảng 9: Quy mô đội khi tầm nhìn bị giới hạn, quy tắc 99 phần trăm.**

| folder | method | layout | variant | N | D tested | D_min | D_sat | D_max | D_overcrowd |
|---|---|---|---|---|---|---|---|---|---|
| dmin_f99_view_range | strombom_multi | wide | sensing_range=0.0 | 50, 100, 200 | 1-4, 6, 8, 12, 16 | 1, 1, 2 | 1, 1-16, 3-16 | 16, 16, 16 | - |
| dmin_f99_view_range | strombom_multi | wide | sensing_range=15.0 | 50, 100, 200 | 1-8, 12, 16 | none on grid, [6], [7] | - | - | - |
| dmin_f99_view_range | strombom_multi | wide | sensing_range=30.0 | 50, 100, 200 | 1-4, 6, 8, 12, 16 | 1, 1, 3 | 1, 1, 3 | 16, 16, 16 | - |
| dmin_f99_view_range | strombom_multi | wide | sensing_range=45.0 | 50, 100, 200 | 1-4, 6, 8, 12, 16 | 1, 1, 3-4 | 1, 1, 4 | 16, 16, 16 | - |
| dmin_f99_view_range | strombom_multi | wide | sensing_range=65.0 | 50, 100, 200 | 1-4, 6, 8, 12, 16 | 1, 1, 3 | 1, 2, 3 | 16, 16, 16 | - |
| dmin_f99_view_range | strombom_multi | wide | sensing_range=100.0 | 50, 100, 200 | 1-4, 6, 8, 12, 16 | 1, 1, 2-3 | 1, 2, 3 | 16, 16, 16 | - |
| dmin_f99_view_range | strombom_multi | split | sensing_range=0.0 | 50, 100, 200 | 1-8, 12, 16 | 1, 1, [1] | 1, 2-16, - | 16, 16, - | -, -, 8 |
| dmin_f99_view_range | strombom_multi | split | sensing_range=15.0 | 50, 100, 200 | 1-4, 6, 8, 12, 16 | 1, 1, [3] | 1, 1-16, - | 16, 16, - | - |
| dmin_f99_view_range | strombom_multi | split | sensing_range=30.0 | 50, 100, 200 | 1-4, 6, 8, 12, 16 | 1, 1, 2-3 | 1, 1-16, 4-16 | 16, 16, 16 | - |
| dmin_f99_view_range | strombom_multi | split | sensing_range=45.0 | 50, 100, 200 | 1-4, 6, 8, 12, 16 | 1, 1, 3 | 1, 1-16, 3-16 | 16, 16, 16 | - |
| dmin_f99_view_range | strombom_multi | split | sensing_range=65.0 | 50, 100, 200 | 1-4, 6, 8, 12, 16 | 1, 1, 3 | 1, 1, 3 | 16, 16, 16 | - |
| dmin_f99_view_range | strombom_multi | split | sensing_range=100.0 | 50, 100, 200 | 1-6, 8, 12, 16 | 1, 1, 1-5 | 1, 1-16, 5 | 16, 16, 16 | - |
| dmin_f99_view_comm | strombom_multi | wide | communication=neighbour | 50, 100, 200 | 1-4, 6, 8, 12, 16 | 1, 1, 3 | 1, 2, 3 | 16, 16, 16 | - |
| dmin_f99_view_comm | strombom_multi | wide | communication=shared | 50, 100, 200 | 1-4, 6, 8, 12, 16 | 1, 1, 2 | 1, 2, 3 | 16, 16, 16 | - |
| dmin_f99_view_comm | strombom_multi | split | communication=neighbour | 50, 100, 200 | 1-8, 12, 16 | 1, 1, 3 | 1, 1, 4-16 | 16, 16, 16 | - |
| dmin_f99_view_comm | strombom_multi | split | communication=shared | 50, 100, 200 | 1-4, 6, 8-10, 12-14, 16 | 1, 1, 3 | 1-16, 1, 3 | 16, 16, 3 | -, -, 4 |

### 3.7 Bầy lớn

Bảng 10 ghi các lượt chạy trên giới hạn hiệu chỉnh ở 12 lần thời gian lùa, nơi $R_f$ được áp theo mật độ của bầy 566 con ([giới hạn hiệu chỉnh](glossary_vi.md#nhiệm-vụ-lùa)): ở mật độ đó (`dmin_f99_big`), ở một bầy dày hơn và một bầy thưa hơn (`imposed_radius_scale` $1/\sqrt{2}$ và $\sqrt{2}$), và với điểm lùa bị giới hạn (`dmin_f99_big_cap`). Ở $N = 566$, dưới giới hạn, $R_f$ được hiệu chỉnh và hệ số mật độ không tác động, nên ba hàng $N = 566$ chạy cùng một bầy. 100 lượt của `dmin_f99_big_cap` ở $N = 3200$ không nằm trong các quyết định đã lưu của nó nên không có trong bảng.

**Bảng 10: Quy mô đội cho bầy lớn, quy tắc 99 phần trăm.**

| folder | method | layout | variant | N | D tested | D_min | D_sat | D_max | D_overcrowd |
|---|---|---|---|---|---|---|---|---|---|
| dmin_f99_big | strombom_multi | compact | - | 566, 800, 1131, 1600, 2263, 3200 | 1-4, 6, 8, 12 | 1, 1, none on grid, none on grid, none on grid, none on grid | 1, 2, -, -, -, - | 12, 12, -, -, -, - | - |
| dmin_f99_big | strombom_multi | wide | - | 566, 800, 1131, 1600, 2263, 3200 | 1-4, 6, 8, 12 | 2-3, 3, none on grid, none on grid, none on grid, none on grid | 8, [12], -, -, -, - | 12, 12, -, -, -, - | - |
| dmin_f99_big_dense | strombom_multi | wide | - | 566, 800 | 1-6, 8, 12 | 2-3, 4-5 | 8, 8-12 | 12, 12 | - |
| dmin_f99_big_loose | strombom_multi | wide | - | 566, 800 | 1-4, 6, 8, 12 | 2-3, 3 | 8, [12] | 12, 12 | - |
| dmin_f99_big_cap | strombom_multi | compact | - | 800, 1131, 1600 | 1-4, 6, 8, 12 | 1, 1, 2 | 2, 6, 6 | 12, 12, 12 | - |
| dmin_f99_big_cap | strombom_multi | wide | - | 800, 1131, 1600 | 1-6, 8-10, 12 | 3, 5-9, none on grid | [12], 10-12, - | 12, 12, - | - |

### 3.8 Mục tiêu không gắn kết

Bảng 11 ghi nhiệm vụ gom của Lama và di Bernardo (2024), với bán kính cảm nhận 10 (`lama_r50`) và cảm nhận vô hạn (`lama_r50_inf`). Ở đây N là số mục tiêu và các cột D đếm người chăn. Đây chỉ là các quyết định của HerdSim; thống kê riêng của bài báo nằm trong [results_tables.md](../report/results_tables.md#lama-and-di-bernardo-2024-gather-task).

**Bảng 11: Số người chăn cho nhiệm vụ gom, quy tắc 99 phần trăm.**

| folder | method | layout | variant | N | D tested | D_min | D_sat | D_max | D_overcrowd |
|---|---|---|---|---|---|---|---|---|---|
| lama_r50 | lama | uniform | - | 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361, 400 | 1-25 | none on grid, none on grid, none on grid, none on grid, none on grid, none on grid, none on grid, none on grid, none on grid, none on grid, [20], 17-25, 14-20, 13-15, 13, 14, 15, 15, 16, 17 | -, -, -, -, -, -, -, -, -, -, -, 25, 24-25, [25], [25], [25], [25], [25], [25], [25] | -, -, -, -, -, -, -, -, -, -, -, 25, 25, 25, 25, 25, 25, 25, 25, 25 | - |
| lama_r50_inf | lama | uniform | - | 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361, 400 | 1-25 | 1, 1, 2, 3, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 14-15, 15, 16, 17 | 4-25, 6-25, 11-25, 12-25, 13-25, 15-25, 16-25, 20-25, 23-25, 24-25, 24-25, 24-25, [25], [25], [25], [25], [25], [25], [25], [25] | 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25 | - |

## 4. Giữ bầy ở 95 và 90 phần trăm

`dmin_f99_hold_share` cũng chạy nhiệm vụ giữ bầy khi chỉ cần 95% và 90% bầy ở lại trong đích (ở $N = 25$, một và hai con cừu được phép ở ngoài). Bảng 12 và 13 ghi các đường cong đó; giao thức được liệt kê ở [Bảng 3](#3-quy-tắc-99-phần-trăm) và các đường cong 99 phần trăm của nó ở [Bảng 7](#34-giữ-bầy-và-chó-chiếm-chỗ).

**Bảng 12: Quy mô đội để giữ bầy, quy tắc 95 phần trăm.**

| folder | method | layout | variant | N | D tested | D_min | D_sat | D_max | D_overcrowd |
|---|---|---|---|---|---|---|---|---|---|
| dmin_f99_hold_share | strombom_multi | compact | goal_radius_multiple=1.9 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 1 | -, 1, 1 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | compact | goal_radius_multiple=2.1 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 1 | -, 1, 1 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | compact | goal_radius_multiple=2.3 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 1 | 1, 1, 1 | 24, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | compact | goal_radius_multiple=2.5 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 1 | 1, 1, 1 | 24, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | wide | goal_radius_multiple=1.9 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 1 | -, 1, 1-24 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | wide | goal_radius_multiple=2.1 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 1 | -, 1, 1-24 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | wide | goal_radius_multiple=2.3 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 1 | 1, 1, 1-24 | 24, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | wide | goal_radius_multiple=2.5 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 1 | 1, 1, 1-24 | 24, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | split | goal_radius_multiple=1.9 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 1 | -, 1, 2-24 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | split | goal_radius_multiple=2.1 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 1 | -, 1, 2-24 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | split | goal_radius_multiple=2.3 | 25, 50, 100 | 1-2, 4, 8, 16, 18-20, 24 | 1, 1, 1 | 1, 1, 2-24 | 19, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | split | goal_radius_multiple=2.5 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 1 | 1, 1, 2-24 | 24, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | outlier_rich | goal_radius_multiple=1.9 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 2 | -, 1, 4 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | outlier_rich | goal_radius_multiple=2.1 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 2 | -, 1, 4 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | outlier_rich | goal_radius_multiple=2.3 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 2 | 1, 1, 4 | 24, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | outlier_rich | goal_radius_multiple=2.5 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 2 | 1, 1, 4 | 24, 24, 24 | - |

**Bảng 13: Quy mô đội để giữ bầy, quy tắc 90 phần trăm.**

| folder | method | layout | variant | N | D tested | D_min | D_sat | D_max | D_overcrowd |
|---|---|---|---|---|---|---|---|---|---|
| dmin_f99_hold_share | strombom_multi | compact | goal_radius_multiple=1.9 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 1 | -, 1, 1 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | compact | goal_radius_multiple=2.1 | 25, 50, 100 | 1-4, 8, 24 | [1], 1, 1 | -, 1, 1 | -, 24, 24 | 4, -, - |
| dmin_f99_hold_share | strombom_multi | compact | goal_radius_multiple=2.3 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 1 | 1, 1, 1 | 24, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | compact | goal_radius_multiple=2.5 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 1 | 1, 1, 1 | 24, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | wide | goal_radius_multiple=1.9 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 1 | -, 1, 1-24 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | wide | goal_radius_multiple=2.1 | 25, 50, 100 | 1-4, 8, 24 | [1], 1, 1 | -, 1, 1-24 | -, 24, 24 | 3, -, - |
| dmin_f99_hold_share | strombom_multi | wide | goal_radius_multiple=2.3 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 1 | 1, 1, 1-24 | 24, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | wide | goal_radius_multiple=2.5 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 1 | 1, 1, 1-24 | 24, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | split | goal_radius_multiple=1.9 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 1 | -, 1, 2 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | split | goal_radius_multiple=2.1 | 25, 50, 100 | 1-2, 4, 6-8, 24 | 1, 1, 1 | 1, 1, 1-24 | 1, 24, 24 | 7, -, - |
| dmin_f99_hold_share | strombom_multi | split | goal_radius_multiple=2.3 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 1 | 1, 1, 2-24 | 24, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | split | goal_radius_multiple=2.5 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 1 | 1, 1, 2-24 | 24, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | outlier_rich | goal_radius_multiple=1.9 | 25, 50, 100 | 1-2, 4, 8, 24 | none on grid, 1, 2 | -, 1, 4 | -, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | outlier_rich | goal_radius_multiple=2.1 | 25, 50, 100 | 1-2, 4-6, 8, 24 | 1, 1, 2 | 1, 1, 4 | 1, 24, 24 | 5, -, - |
| dmin_f99_hold_share | strombom_multi | outlier_rich | goal_radius_multiple=2.3 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 2 | 1, 1, 4 | 24, 24, 24 | - |
| dmin_f99_hold_share | strombom_multi | outlier_rich | goal_radius_multiple=2.5 | 25, 50, 100 | 1-2, 4, 8, 24 | 1, 1, 2 | 1, 1, 4 | 24, 24, 24 | - |

## 5. Tạo lại các bảng

Mỗi lệnh in một bảng giao thức rồi một bảng đường cong cho mỗi quy tắc thành công. Mục 2 lấy từ lệnh thứ nhất. Lệnh thứ hai chỉ dùng cho bảng giao thức (Bảng 3), còn lệnh thứ ba tới thứ mười chỉ dùng cho các bảng đường cong (Bảng 4 tới 11, và Bảng 12 và 13 từ lệnh thứ sáu):

```bash
uv run cli/dmin_tables.py overview dmin_m12 dmin_m6 dmin_m3 dmin_s_base dmin_s_matched dmin_s_handler dmin_s_ring dmin_s_goal dmin_s_dogspeed dmin_s_gap dmin_fat dmin_kubo
uv run cli/dmin_tables.py overview dmin_f99_m12 dmin_f99_m6 dmin_f99_m3 dmin_f99_fat dmin_f99_indep dmin_f99_kubo dmin_f99_s_base dmin_f99_s_matched dmin_f99_s_handler dmin_f99_s_ring dmin_f99_s_goal dmin_f99_s_dogspeed dmin_f99_s_gap dmin_f99_hold dmin_f99_hold_spacing dmin_f99_hold_goal dmin_f99_hold_share dmin_f99_c1.3 dmin_f99_c1.6 dmin_f99_c2.0 dmin_f99_k05 dmin_f99_view_range dmin_f99_view_comm dmin_f99_big dmin_f99_big_dense dmin_f99_big_loose dmin_f99_big_cap lama_r50 lama_r50_inf
uv run cli/dmin_tables.py overview dmin_f99_m12 dmin_f99_m6 dmin_f99_m3
uv run cli/dmin_tables.py overview dmin_f99_fat dmin_f99_indep dmin_f99_kubo
uv run cli/dmin_tables.py overview dmin_f99_s_base dmin_f99_s_matched dmin_f99_s_handler dmin_f99_s_ring dmin_f99_s_goal dmin_f99_s_dogspeed dmin_f99_s_gap
uv run cli/dmin_tables.py overview dmin_f99_hold dmin_f99_hold_spacing dmin_f99_hold_goal dmin_f99_hold_share
uv run cli/dmin_tables.py overview dmin_f99_c1.3 dmin_f99_c1.6 dmin_f99_c2.0 dmin_f99_k05
uv run cli/dmin_tables.py overview dmin_f99_view_range dmin_f99_view_comm
uv run cli/dmin_tables.py overview dmin_f99_big dmin_f99_big_dense dmin_f99_big_loose dmin_f99_big_cap
uv run cli/dmin_tables.py overview lama_r50 lama_r50_inf
```
