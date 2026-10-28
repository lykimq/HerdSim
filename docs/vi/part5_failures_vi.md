# Vì sao các lượt thất bại: bố cục `split` và cách các lượt thất bại kết thúc

Phần 5 của báo cáo HerdSim về quy mô đội. [Phần tổng quan](d_min_report_vi.md) gồm tóm tắt, các câu hỏi nghiên cứu, [quy tắc quyết định](d_min_report_vi.md#2-quy-tắc-quyết-định) định nghĩa $D_{\min}$, khoảng và cận dưới của nó, phần thảo luận và [tài liệu tham khảo](d_min_report_vi.md#tài-liệu-tham-khảo). Các thuật ngữ được định nghĩa trong [bảng thuật ngữ](glossary_vi.md).

## 4. Xem kỹ hơn: bố cục `split` và các số đo theo từng bước

### 4.1 Vì sao thêm chó không giúp trên `split`
Vì sao thêm chó không giúp khi bầy xuất phát thành các cụm tách rời (`split`)? Các lượt chạy lại 12 hạt giống đã lưu mỗi ô ở $N = 200$ chỉ ra hai nguyên nhân, cách quy tắc đội phân công các chó đang gom và các chó bị quy tắc dừng của Strömbom giữ đứng yên (chó dừng khi có một con cừu trong vòng 6 m); ở 6 lần thời gian lùa, mỗi thay đổi đều làm lượt lùa nhanh hơn trong các lượt chạy lại (ý 1 và 2).

Trên bầy `split` ở $N \ge 200$, thêm chó không làm tăng tỷ lệ thành công: ở 6 lần thời gian lùa dưới quy tắc 99%, nó nằm trong khoảng 0,60 đến 0,92 với mọi $D \ge 4$ ở $N = 200$ và 400 (0,10–0,76 dưới quy tắc nghiêm ngặt), và ở 3 lần thời gian lùa nó giảm về gần không (Hình 1).

Hai số đo trên mọi lượt đã lưu cho thấy thời gian đi đâu ([bảng theo từng lượt](../report/results_tables.md#single-trials-and-curves-across-folders)):
- Bầy vào đích thành hai đợt. Ở 6 lần thời gian lùa trên `split` $N = 200$, một hoặc hai chó cần trung vị 7 s từ 90% đến 99% bầy trong đích; 3 chó và các đội từ 6 chó trở lên cần 249 đến 418 s, 43% đến 60% thời gian hoàn thành của chúng (4 chó cần 22 s, nhưng chỉ trên 38 lượt thành công). Ở $N = 283$ và 400, các đội từ 3 chó cần 274 đến 480 s, và ở $N = 566$ các đội từ 4 chó cần 474 đến 540 s.
- Các quy tắc đơn giản hơn làm tốt hơn quy tắc đội. Trên `split` $N = 200$ (6 lần thời gian lùa, quy tắc 99%), quy tắc đội ở mức 0,60–0,95 với trung vị thời gian hoàn thành 341–703 s, và chia sẻ với cả đội thất bại từ 4 chó. Chó chăn độc lập tin cậy từ 3 chó (trung vị 265–299 s), và chó nhìn xa 30 đến 65 m không chia sẻ thành công cả 60 lượt ở mọi đội từ 3 đến 16 chó (trung vị 237–350 s). Chó chăn độc lập cũng lập kế hoạch trên cả bầy, nên cái chúng thiếu là tầng đội, tức việc phân công và cung. Vì sao điều đó giúp ích trên `split` thì chưa được kiểm chứng; điều này khớp với nguyên nhân thứ nhất dưới đây.

Chạy lại các lượt đã lưu (`cli/diagnostics/split_diagnostic.py`, 12 hạt giống mỗi ô, $N = 200$) chỉ ra hai nguyên nhân:

1. Mọi chó đi gom dồn về một cụm ($D = 4$).  
   Quy tắc đội phân công chó cho các con lạc theo tổng quãng đường đi ngắn nhất. Cách đó bỏ qua việc con lạc thuộc cụm nào, nên khi bầy tách thành nhiều cụm, cụm gần hơn hoặc tản hơn có thể lấy hết chó trong khi cụm khác trôi đi. Khi buộc các chó đi gom chọn những con lạc cách nhau ít nhất $f(N) = r_a N^{2/3}$, trung vị thời gian hoàn thành ở $D = 4$ giảm từ 631 s xuống 318 s (6 lần thời gian lùa).

2. Nhiều chó đứng yên vì quy tắc dừng ($D \ge 4$).  
   Chó của Strömbom dừng lại khi có con cừu nào trong vòng $3 r_a = 6$ m. Trên `wide` và `outlier_rich`, điều đó giữ 1% đến 7% số chó đứng yên. Trên `split`, khoảng 25% số chó đứng yên, bị giữ lại cạnh một cụm trên đường sang cụm khác. Khi rút khoảng cách dừng xuống $r_a = 2$ m, lượt lùa nhanh hơn 21–24% ở $D = 8$ và 16, và $D = 16$ thành công ở cả 12 hạt giống.  
   Ở 3 lần thời gian lùa, không thay đổi nào làm `split` trở nên tin cậy trong các lượt chạy lại này, nơi ở 4, 8 và 16 chó không phiên bản nào thành công quá 7 trong 12 hạt giống, đủ ít để khoảng 99% loại trừ độ tin cậy.

![Đường cong split và các số đo](../figures/fig23_split_curves.png)

**Hình 1: Tỷ lệ thành công trên bầy `split` theo quy mô đội (6 lần thời gian lùa).** Trên `wide` tỷ lệ thành công tăng lên 1; trên `split` ở $N = 200$ và 400 nó đi ngang dưới ngưỡng, còn $N = 100$ tin cậy dưới cả hai quy tắc.

- Ký hiệu: hình tròn xanh là quy tắc nghiêm ngặt và hình vuông cam là quy tắc 99%, mỗi điểm kèm khoảng Clopper–Pearson 99%, theo $D$ trên thang log. Đường chấm là $\theta = 0{,}90$.
- Các khung: `split` ở $N = 100$, 200 và 400, và `wide` ở $N = 400$ để so sánh.

*Dữ liệu:* `results/dmin_m6` và `results/dmin_f99_m6`; giá trị trong [results_tables.md: dmin_m6](../report/results_tables.md#dmin_m6) và [results_tables.md: dmin_f99_m6](../report/results_tables.md#dmin_f99_m6).

![Hoạt ảnh hai hạt giống của một ô split](../gifs/split.gif)

**Hoạt ảnh 1: Hai hạt giống của một ô `split`, chạy lại ($N = 200$, 16 chó, quy tắc 99%, 6 lần thời gian lùa).** Cùng một đội thành công với bầy xuất phát này và thất bại với bầy khác. Mỗi lượt chạy lại khớp với lượt đã lưu.

- Trái: hạt giống 4 gom các cụm lại và thành công ở 283 s.
- Phải: hạt giống 8 hết giờ khi bầy còn chưa tới đích.

### 4.2 Các số đo theo từng bước
Hai số đo được ghi ở mọi bước, tức mỗi bước mô phỏng, của mọi lượt chạy:

- Độ trải của bầy và tỷ lệ thành công: trên các ô có ít nhất 20 hạt giống ở 6 lần thời gian lùa, tương quan hạng (Spearman) giữa độ trải trung bình của bầy (khoảng cách RMS đến tâm) và tỷ lệ thành công là $-0{,}76$ dưới quy tắc nghiêm ngặt và $-0{,}71$ dưới quy tắc 99% ($-0{,}57$ đến $-0{,}68$ ở 3 lần thời gian lùa; Hình 2). Độ trải được lấy trung bình trên cả lượt và các lượt thất bại kết thúc khi bầy còn tản ra, nên tương quan này không cho biết điều nào có trước.
- Các chó đến gần nhau bao nhiêu: với `strombom_multi` trên `wide`, không chó nào có chó khác trong vòng 2 m đến $D = 6$; ở $D = 16$ tỷ lệ là 0,45–0,59 trên các bố cục phân tán. Với FAT nó là 0,45–0,66 ở $D = 2$ và 0,72–0,90 ở $D = 16$ (trung vị qua mọi $N$), đúng như khi mọi chó đuổi cùng một con cừu.

![Các số đo từng lượt](../figures/fig27_metrics.png)

**Hình 2: Các số đo theo từng bước ở 6 lần thời gian lùa.** Các ô có bầy trải rộng hơn thì thành công ít hơn, và trên `split` khoảng một phần tư số chó đứng yên vì quy tắc dừng 6 m.

- Trái (a): độ trải trung bình của bầy trong lượt (khoảng cách RMS đến tâm) so với tỷ lệ thành công, mỗi ô có ít nhất 20 hạt giống một điểm, tô màu theo bố cục, hình tròn cho quy tắc nghiêm ngặt và hình vuông cho quy tắc 99%. Tương quan hạng là $-0{,}76$ với quy tắc nghiêm ngặt và $-0{,}71$ ở 99%.
- Giữa (b): trung vị tỷ lệ chó đứng yên theo $D$ ở $N = 200$ (quy tắc 99%) cho `wide`, `split` và `outlier_rich`.
- Phải (c): trung vị tỷ lệ chó có một chó khác trong vòng 2 m theo $D$, cho cùng các ô.

*Dữ liệu:* `results/dmin_m6` và `results/dmin_f99_m6`.

## 5.2 Các lượt thất bại kết thúc thế nào, và độ trải lúc xuất phát

Các lượt thất bại kết thúc thế nào: bầy đã ở gần đích nhưng quá muộn, hay bầy vẫn còn xa đích? Phần lớn là còn xa đích (ý 1, Bảng 1). Mức độ trải của bầy lúc xuất phát tách được xuất phát tập trung với xuất phát phân tán nhưng không xếp thứ tự được các bố cục phân tán (ý 2, Bảng 2).

1. Hai loại lượt thất bại.  
   Chúng tôi chia các lượt lùa thất bại theo nơi bầy dừng lại. Một lượt là gần đích khi tâm bầy kết thúc trong vòng hai bán kính đích quanh tâm đích: bầy đã đến đó nhưng trễ hạn hoặc còn sót cừu bên ngoài. Nó là xa đích khi tâm bầy kết thúc xa hơn: bầy không tới được đích. Phần lớn thất bại là xa đích (Bảng 1):

   **Bảng 1: Các lượt lùa thất bại theo nơi bầy kết thúc.**

   | Giao thức | Quy tắc | Lượt thất bại | Xa đích | Gần đích | Tỷ lệ xa |
   | :--- | :--- | :---: | :---: | :---: | :---: |
   | `dmin_m12` | nghiêm ngặt, 12× | 235 | 180 | 55 | 76,6% |
   | `dmin_m6` | nghiêm ngặt, 6× | 889 | 639 | 250 | 71,9% |
   | `dmin_m3` | nghiêm ngặt, 3× | 710 | 571 | 139 | 80,4% |
   | `dmin_f99_m12` | 99%, 12× | 235 | 213 | 22 | 90,6% |
   | `dmin_f99_m6` | 99%, 6× | 1511 | 1067 | 444 | 70,6% |
   | `dmin_f99_m3` | 99%, 3× | 584 | 457 | 127 | 78,3% |

   Trong 70% đến 91% số lượt thất bại, bầy kết thúc xa đích, nên phần lớn thất bại đến từ việc gom và lùa, không phải từ mấy mét cuối. Cách chia này chỉ dùng nơi bầy kết thúc; nó không cho biết thêm thời gian có cứu được lượt chạy hay không. Các nhãn thất bại của nhiệm vụ, là các quy tắc kinh nghiệm đọc từ lịch sử của mỗi lượt (`flock_escaped`, `stuck`, `scatter` và các nhãn khác), thêm được ít: ở 6 lần thời gian lùa theo quy tắc 99%, 1049 trong 1511 lượt thất bại không khớp mẫu nào và chỉ là hết giờ, và trên `split` 207 trong 1015 là `stuck`; ở 12 lần, nhãn thường gặp nhất là `flock_escaped` (105 trong 235).  
   *Dữ liệu:* `uv run cli/dmin_tables.py dispersion`, trên sáu giao thức chính.

2. Độ trải lúc xuất phát nhân $N$.  
   Tích của độ trải lúc xuất phát $S_0$ (bán kính RMS của bầy lúc xuất phát) và $N$ đo lượng công gom mà một bố cục đòi hỏi. Ở $N = 400$, nó lớn gấp 8 đến 13 lần trên các bố cục phân tán so với `compact`, và tỷ lệ thành công ở 6 lần thời gian lùa (trên mọi $D$) giảm khi nó tăng (Bảng 2):

   **Bảng 2: Độ trải xuất phát, đại lượng $S_0 \times N$ và tỷ lệ thành công ở 6 lần thời gian lùa.**

   | Bố cục | $N$ | Độ trải xuất phát $S_0$ | $S_0 \times N$ | Tỷ lệ thành công (mọi $D$) |
   | :--- | :---: | :---: | :---: | :---: |
   | `compact` | 25 | 4,8 m | 119 | 100,0% |
   | `compact` | 100 | 6,7 m | 665 | 100,0% |
   | `compact` | 400 | 8,3 m | 3316 | 100,0% |
   | `wide` | 400 | 74,8 m | 29.931 | 83,8% |
   | `outlier_rich` | 400 | 66,2 m | 26.496 | 55,3% |
   | `split` | 400 | 108,8 m | 43.507 | 21,1% |

   Đại lượng này tách bầy tập trung khỏi bầy phân tán, nhưng không xếp thứ tự được các bố cục phân tán: `outlier_rich` có giá trị nhỏ hơn `wide` nhưng tỷ lệ thành công thấp hơn. Các con lạc nằm ở đâu cũng quan trọng như chúng xa đến đâu.  
   *Dữ liệu:* `uv run cli/dmin_tables.py dispersion` trên `dmin_m6`; $S_0$ là trung bình của `max_extent` (bán kính RMS lớn nhất của bầy trong một lượt, tức lúc xuất phát).
