# Nhật ký chạy, các khẳng định và khả năng tái lập

Phụ lục của báo cáo HerdSim về quy mô đội. [Phần tổng quan](d_min_report_vi.md) gồm tóm tắt, các câu hỏi nghiên cứu, [quy tắc quyết định](d_min_report_vi.md#2-quy-tắc-quyết-định) định nghĩa $D_{\min}$, khoảng và cận dưới của nó, phần thảo luận và [tài liệu tham khảo](d_min_report_vi.md#tài-liệu-tham-khảo). Các thuật ngữ được định nghĩa trong [bảng thuật ngữ](glossary_vi.md).

## Phụ lục A: Nhật ký chạy giao thức

Bảng 1 liệt kê các giao thức của nghiên cứu đầu. Lượt, ô và quyết định là tổng hiện tại của các thư mục; giờ là của lượt chạy đầu của mỗi giao thức (giờ chạy tiếp được liệt kê dưới bảng).

**Bảng 1: Nhật ký chạy của các giao thức nghiên cứu đầu.**

| Giao thức | Lượt | Ô | Đã quyết định | Còn mở ở 200 lượt | Lỗi | Giờ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `dmin_m12` | 17.220 | 183 | 179 | 4 | 0 | 1,24 |
| `dmin_m6` | 13.470 | 191 | 170 | 21 | 0 | 0,28 |
| `dmin_m3` | 9530 | 183 | 178 | 5 | 0 | 0,17 |
| `dmin_f99_m12` | 11.100 | 180 | 178 | 2 | 0 | 0,41 |
| `dmin_f99_m6` | 14.240 | 191 | 174 | 17 | 0 | 0,49 |
| `dmin_f99_m3` | 11.140 | 185 | 177 | 8 | 0 | 0,27 |
| `dmin_fat` | 8660 | 181 | 179 | 2 | 0 | 0,22 |
| `dmin_f99_fat` | 8670 | 184 | 183 | 1 | 0 | 0,23 |
| `dmin_kubo` | 1080 | 18 | 18 | 0 | 0 | 0,08 |
| Các giao thức độ nhạy (14 lượt chạy) | 69.630 | 921 | 800 | 121 | 0 | 3,27 |
| Tổng | 164.740 | 2417 | 2236 | 181 | 0 | khoảng 6,7 |

Bảng 2 liệt kê các lượt chạy tiếp theo (quy tắc 99%; giờ với 20 worker):

**Bảng 2: Nhật ký chạy của các giao thức tiếp theo.**

| Giao thức | Lượt | Ô | Còn mở ở 200 lượt | Lỗi | Giờ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3` (chạy tiếp với lượt cho thời gian hoàn thành; thêm $N$ 71, 141, 283, 566 vào hai cái đầu) | +38.770 | | | 0 | 4,0 |
| `dmin_f99_indep` | 12.990 | 181 | 18 | 0 | 0,30 |
| `dmin_f99_kubo` | 3260 | 38 | 6 | 0 | 0,18 |
| `dmin_f99_hold` | 14.280 | 280 | 18 | 0 | 0,74 |
| `dmin_f99_hold_spacing` (chạy lại với quy tắc giãn cách cứng) | 13.930 | 283 | 19 | 0 | 0,70 |
| `dmin_f99_hold_goal` (giữ bầy, đích 1,9; 2,5; 3,0 $R_f$, $N \le 100$) | 21.800 | 326 | 30 | 0 | 0,36 |
| `dmin_f99_hold_share` (giữ bầy, đích 1,9 đến 2,5 $R_f$ × tỷ lệ 90, 95, 99%) | 50.170 | 746 | 57 | 0 | 0,91 |
| `dmin_f99_c1.3`, `_c1.6`, `_c2.0` | 10.800 / 10.830 / 10.780 | 180 mỗi giao thức | 1 / 0 / 0 | 0 | 0,31 / 0,29 / 0,41 |
| `dmin_f99_k05` | 11.630 | 149 | 14 | 0 | 2,29 |
| `dmin_f99_view_range` | 21.040 | 293 | 27 | 0 | 0,53 |
| `dmin_f99_view_comm` | 6890 | 102 | 3 | 0 | 0,20 |
| `dmin_f99_big` | 2230 | 84 | 1 | 0 | 3,12 |
| `dmin_f99_big_dense`, `_loose` | 1320 / 830 | 15 / 14 | 2 / 1 | 0 | 0,73 / 0,26 |
| `dmin_f99_big_cap` | 2550 (+100 ở $N = 3200$, không tính) | 45 | 3 | 0 | 5,5 (7,6 tính cả $N = 3200$) |
| `lama_r50` (nhiệm vụ gom, bán kính cảm nhận 10) | 17.660 | 500 | 23 | 0 | 6,53 |
| `lama_r50_inf` (nhiệm vụ gom, thấy mọi thứ) | 22.620 | 500 | 1 | 0 | 6,47 |

Chạy lại chẩn đoán: 164 lượt về áp lực, 768 lượt về `split` và 240 lượt đo quãng đi khi giữ bầy, mọi lượt chạy lại không đổi đều giống hệt lượt đã lưu. Hai lượt kiểm chứng mô hình Lama (8200 lượt, thư mục nháp không giữ) chạy trước `lama_r50`; lượt thứ hai sửa thứ tự di chuyển người chăn và mục tiêu ([mục 6](d_min_report_vi.md#6-hạn-chế), ý 12).

## Phụ lục B: Các khẳng định và bằng chứng

Bảng 3 liệt kê từng khẳng định cùng bằng chứng và giới hạn của nó.

**Bảng 3: Các khẳng định và bằng chứng.**

| # | Khẳng định | Loại | Bằng chứng | Giới hạn |
| :---: | :--- | :--- | :--- | :--- |
| 1 | Một bầy tập trung cần một chó ($D_{\min} = 1$) đến $N = 1131$. | Đo được | `dmin_m12`, `dmin_m6`, `dmin_m3`, `dmin_f99_*` đến $N = 566$; `dmin_f99_big_cap` ở 800 và 1131. | Trên 1056 chỉ khi giới hạn điểm lùa. |
| 2 | Đến $N = 50$, một chó là đủ trên mọi bố cục và thời hạn. | Đo được | Mọi ô $N \le 50$ của 23 giao thức cơ sở được quyết định ở $D = 1$. | Lý do nêu ở [mục 3.1](part1_growth_vi.md#31-rq1-d_min-tăng-thế-nào-theo-n) là khả dĩ, chưa được kiểm tra. |
| 3 | Trên bầy phân tán, $D_{\min}$ tăng với độ dốc 0,27–0,38 ở 12 lần thời gian lùa và 0,38–0,61 ở 6 lần. | Đo được | Khoảng độ dốc qua các khoảng $D_{\min}$ của chín quy mô ($N = 25$–566), `dmin_f99_m12`, `dmin_f99_m6`. | Chỉ đến giới hạn hiệu chỉnh. |
| 4 | Dưới quy tắc nghiêm ngặt, các đội lớn thất bại vì con cừu cuối cùng. | Đo được | 97% số lượt thất bại nghiêm ngặt với $D \ge 6$ đã có 99% bầy trong đích (`dmin_s_base`); với chó chậm hơn (`dmin_s_dogspeed`), $D_{\min}$ nghiêm ngặt trên `outlier_rich` $N = 400$ từ none xuống 6. | Áp dụng cho quy tắc nghiêm ngặt với đích mở. |
| 5 | Trên `split`, các chó đi gom dồn về một cụm và nhiều chó đứng yên. | Đo trong các lượt chạy lại | Các lượt chạy lại `split_diagnostic`: trải các con lạc ra làm thời gian hoàn thành giảm một nửa ở $D = 4$; rút khoảng cách dừng làm lượt lùa nhanh hơn 21–24% ở $D = 8$, 16. | 12 hạt giống mỗi ô; không thay đổi nào sửa được 3 lần thời gian lùa. |
| 6 | Gắn kết yếu hơn làm $D_{\min}$ tăng nhanh hơn, về phía 0,5. | Đo được | `dmin_f99_k05` độ dốc 0,40–0,70 trên `wide`; `dmin_f99_c*` 0,20. | Chỉ một mức yếu hơn; bầy yếu hơn nữa không hiệu chỉnh được. |
| 7 | Trên $N \approx 1056$, điểm lùa của Strömbom nằm ngoài khoảng cách phản ứng của cừu. | Suy ra và đo được | $2\sqrt{N} > 65$; không giới hạn, 0 trên 10 lượt thành công ở $N = 1131$ với mọi $D$; có giới hạn, bầy tập trung thành công ở 800, 1131, 1600 và 42 trên 42 ở 3200. | Giả định khoảng cách phản ứng $r_s = 65$ m. |
| 8 | Chó giữ cách nhau 2 m làm chó thêm trở nên có hại trên `outlier_rich` $N = 400$. | Đo được | `dmin_f99_hold_spacing`: thành công 0,94 ở $D = 6$, 0,77 ở 9, 0,50 ở 16; mọi $D \ge 9$ không tin cậy. | Không thấy trên `wide` hay `compact`. |
| 9 | Trên `wide` $N = 200$ tầm nhìn cục bộ tốn khoảng một chó và chia sẻ với cả đội lấy lại được; trên `split` $N = 200$ tầm nhìn cục bộ 30 đến 65 m tốt hơn thấy mọi thứ. | Đo được | `dmin_f99_view_range`, `dmin_f99_view_comm`. | Việc chia sẻ trong mô hình là tức thời và không lỗi. |
| 10 | Gần ngưỡng, một mức trung bình 0,99 chấp nhận những đội thất bại 9 trên 30 lượt. | Đo được | `lama_r50`: ở 144 mục tiêu, 11 người chăn đạt trung bình 0,992 nhưng thành công ở 21 trên 30 lượt (khoảng 99% là 0,45–0,89); $D_{\min}$ của HerdSim là 17–25. | Mục tiêu không gắn kết trên một hình tròn. |
| 11 | Giữ bầy nhỏ thất bại ở đích mặc định; một đích khoảng 16 đến 19 m giữ được chúng với một chó. Quãng đi của bầy trong lúc chó lùi ra là nguyên nhân khả dĩ. | Ngưỡng và quãng đi đo được; nguyên nhân phù hợp, chưa được thử | `dmin_f99_hold_goal`, `dmin_f99_hold_share`: một chó được kết luận tin cậy trên mọi bố cục từ 18,6 m ($N = 25$) và 17,5 m ($N = 50$) ở 99%, với các khoảng xuống tới 15,5 và 16,0 m. Chạy lại bằng `hold_walk`: tâm bầy đi trung vị 17, 15 và 13 m ở $N = 25$, 50, 100. | Các mức đích cách nhau $0{,}2 R_f$; gắn với quy tắc lùi ra; quãng đi không được thay đổi trực tiếp. |

## Phụ lục C: Khả năng tái lập

Bảng 4 liệt kê những gì cần để chạy lại nghiên cứu.

**Bảng 4: Các hạng mục tái lập.**

| Hạng mục | Ở đâu |
| :--- | :--- |
| Mã nguồn | Kho `HerdSim`, nhánh `scaling-cli-d-min-max`. |
| Môi trường | `uv`, Python 3.11 trở lên; các phiên bản khóa trong `pyproject.toml` và `uv.lock`. |
| Bố cục xuất phát | `sim/core/world/layouts.py` (`compact`, `wide`, `split`, `outlier_rich`). |
| Dòng ngẫu nhiên | Các ô cùng hạt giống xuất phát từ cùng một bầy ([dòng ngẫu nhiên ghép cặp](task_design_vi.md#dòng-ngẫu-nhiên-ghép-cặp)). |
| Phần cứng | Máy trạm Linux, 20 worker (`--workers 20`). |
| Dữ liệu thô | 439.120 dòng lượt chạy trong `results/<protocol>/trials.csv`; `trials.jsonl` (trong git là `trials.jsonl.gz`) giữ cùng các dòng đó cộng thêm 100 lượt $N = 3200$ không được tính của `dmin_f99_big_cap`. |
| Chạy nghiên cứu | `uv run cli/campaign.py run --protocol <id>` và `uv run cli/run_queue.py`. |
| Các bảng | `cli/dmin_tables.py` dựng [results_tables.md](../report/results_tables.md) từ các thư mục kết quả. |
| Kiểm thử | `make test` chạy 332 kiểm thử đơn vị, bất biến và hồi quy; `make bench` chạy 23 kiểm thử benchmark trên sáu chiến dịch thu nhỏ. |
| Chạy lại | `services/replay.py`; 1172 lượt chạy lại chẩn đoán cho đúng các lượt đã lưu. |
