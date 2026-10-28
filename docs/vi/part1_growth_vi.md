# Mức tăng của đội nhỏ nhất theo quy mô bầy, bố cục và thời hạn

Phần 1 của báo cáo HerdSim về quy mô đội. [Phần tổng quan](d_min_report_vi.md) gồm tóm tắt, các câu hỏi nghiên cứu, [quy tắc quyết định](d_min_report_vi.md#2-quy-tắc-quyết-định) định nghĩa $D_{\min}$, khoảng và cận dưới của nó, phần thảo luận và [tài liệu tham khảo](d_min_report_vi.md#tài-liệu-tham-khảo). Các thuật ngữ được định nghĩa trong [bảng thuật ngữ](glossary_vi.md).

## 3.1 RQ1: D_min tăng thế nào theo N?

Bầy lớn hơn cần thêm bao nhiêu chó? Không nhiều, khi có đủ thời gian: bầy tập trung cần một chó ở mọi quy mô và mọi thời hạn, và ở thời hạn thong thả 12 lần thời gian lùa, một bầy phân tán 400 con cần 2 hoặc 3 chó (ý 1 đến 3). Khi ít thời gian thì cần nhiều hơn ([mục 3.3](#33-rq3-thời-hạn-làm-d_min-thay-đổi-thế-nào)). Tốc độ tăng của đội được đo bên dưới bằng độ dốc của $D_{\min}$ theo $N$ trên trục log-log; độ dốc 0,5 nghĩa là bầy lớn gấp bốn cần gấp đôi số chó, và ở 12 lần thời gian lùa các bầy phân tán đều ở dưới mức đó.

Hình 1 vẽ $D_{\min}$ theo $N$ cho mọi bố cục và thời hạn, và Bảng 1 liệt kê cùng các ô đó.

1. Bầy tập trung cần một chó.  
   $D_{\min} = 1$ ở mọi quy mô bầy từ 25 đến 400 và mọi thời hạn. Thêm chó không rút ngắn thời gian lùa: trung vị thời gian hoàn thành giữ ở 1,44–1,74 lần thời gian lùa với mọi $D$ từ 1 đến 24.  
   Vì sao: trong mô hình Strömbom, một con cừu phản ứng với chó luôn đi với 1 m/s, và lực đẩy của nhiều chó được chuẩn hóa về độ lớn lực đẩy của một chó. Chó phía sau một bầy tập trung đổi hướng bầy nhưng không làm bầy nhanh hơn. Trong mô hình Kubo, nơi cừu tăng tốc khi bị đẩy mạnh hơn, thời gian hoàn thành có giảm theo $D$: từ 115 s với một chó xuống 29 s với mười chó ở $N = 100$ (Hình 2).

2. Đến $N = 50$, một chó là đủ trên mọi bố cục.  
   Trên các bố cục phân tán cũng vậy, $D_{\min} = 1$ với $N \le 50$ ở mọi thời hạn.  
   Một lý do khả dĩ: các bố cục phân tán được định cỡ theo khoảng cách gom $r_a N^{2/3}$, nên ở $N = 50$ con cừu xa nhất xuất phát cách tâm bầy nhiều nhất khoảng 45 m, trong phạm vi 65 m mà cừu phản ứng với chó. Một chó phía sau bầy đã tác động lên gần như mọi con cừu ngay từ đầu.

3. Trên bầy phân tán, $D_{\min}$ tăng chậm hơn $N$.  
   Với $N \ge 100$ trên các bố cục phân tán, $D_{\min}$ có tăng nhưng chậm: với thời hạn thong thả nó chỉ đạt 2 hoặc 3 chó ở $N = 400$. Trên thang log-log, độ dốc là 0,20 đến 0,42 ở 12 lần thời gian lùa (Hình 1), dưới mức 0,5 mà Lama và di Bernardo (2024) công bố cho mục tiêu không gắn kết.

Bảng 1 cho $D_{\min}$ ở mọi ô chính (nghiêm ngặt / 99%):

**Bảng 1: $D_{\min}$ ở mọi ô chính, quy tắc nghiêm ngặt / quy tắc 99%.**

| Thời hạn | Bố cục | $N = 25$ | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 12× | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| 12× | `wide` | 1 / 1 | 1 / 1 | 1 / 1 | 2 / 1–2 | 3 / 2 |
| 12× | `split` | 1 / 1 | 1 / 1 | 1 / 1 | 1–2 / 1 | 3 / 2 |
| 12× | `outlier_rich` | 1 / 1 | 1 / 1 | 1–3 / 1–2 | 2 / 2 | 3 / 2 |
| 6× | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| 6× | `wide` | 1 / 1 | 1 / 1 | 1 / 1 | 3 / 2 | [9] / 2–3 |
| 6× | `split` | 1 / 1 | 1 / 1 | 1 / 1 | none / [1] | none / [5] |
| 6× | `outlier_rich` | 1 / 1 | 1 / 1 | 3 / 2 | [12] / 2–3 | none / 3 |
| 3× | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| 3× | `wide` | 1 / 1 | 1 / 1 | 3 / 2 | none / 3 | none / 5–6 |
| 3× | `split` | 1 / 1 | 1 / 1 | 1 / 1 | none / none | none / none |
| 3× | `outlier_rich` | 1 / 1 | 1 / 1 | 3–8 / 2 | none / 4–10 | none / [6] |

*Dữ liệu:* [results_tables.md: strict success](../report/results_tables.md#d_min-by-layout-and-n-strict-success) (`dmin_m12`, `dmin_m6`, `dmin_m3`) và [results_tables.md: success at 99 percent](../report/results_tables.md#d_min-by-layout-and-n-success-at-99-percent) (`dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3`).

![D_min theo quy mô bầy N](../figures/fig20_dmin_vs_n.png)

**Hình 1: $D_{\min}$ theo quy mô bầy $N$ qua các thời hạn và bố cục.** Bầy tập trung giữ ở 1 chó; bầy phân tán tăng chậm ở thời hạn thong thả và nhanh hơn nhiều dưới quy tắc nghiêm ngặt khi $N \ge 100$.

- Ký hiệu: mỗi điểm là $D_{\min}$ của một đường cong (một bố cục và một $N$ dưới một quy tắc), theo các dạng ở [mục 2.1](d_min_report_vi.md#21-khi-nào-một-đội-là-tin-cậy). Màu là bố cục; đường liền với hình tròn là quy tắc nghiêm ngặt, đường đứt với hình vuông là quy tắc 99%. Thanh tô màu là các khoảng còn mở ở 200 lượt, tam giác rỗng là cận dưới, và dấu chéo nghĩa là không có đội tin cậy đến 24. Điểm của mỗi quy tắc và bố cục được dịch ngang một chút để không che nhau.
- Các khung: ba thời hạn, 12, 6 và 3 lần thời gian lùa từ trái sang phải, trên trục log-log.

*Dữ liệu:* [results_tables.md: strict success](../report/results_tables.md#d_min-by-layout-and-n-strict-success), [results_tables.md: success at 99 percent](../report/results_tables.md#d_min-by-layout-and-n-success-at-99-percent), và các quy mô thêm $N = 71, 141, 283, 566$.

![Thời gian hoàn thành trên bầy tập trung](../figures/fig31_compact.png)

**Hình 2: Thời gian hoàn thành theo quy mô đội trên bầy tập trung, cừu Strömbom so với cừu Kubo.** Thêm chó không làm cừu Strömbom nhanh hơn; với cừu Kubo thì có.

- Trái: cừu Strömbom với quy tắc đội `strombom_multi`, $N = 25$ đến 400. Trung vị thời gian hoàn thành được chia cho thời gian lùa của mỗi $N$ (thời gian một con cừu đi thẳng với 1 m/s cần để hết quãng đường lùa, xem [thiết kế nhiệm vụ](task_design_vi.md)), để mọi quy mô dùng chung một trục. Nó phẳng theo $D$, vì một con cừu đang phản ứng đi với 1 m/s bất kể chó làm gì.
- Phải: cừu Kubo, $N = 25, 50, 100$, trung vị thời gian hoàn thành tính bằng giây. Cừu Kubo tăng tốc khi bị đẩy mạnh hơn, đến 5 m/s, nên nhiều chó xong sớm hơn, từ 115 s với một chó xuống 29 s với mười chó ở $N = 100$.

*Dữ liệu:* các lượt thành công trên bầy tập trung trong `results/dmin_m6` và `results/dmin_kubo`; $D_{\min}$ của Kubo trong [results_tables.md: Kubo (compact, strict)](../report/results_tables.md#kubo-compact-strict).

Bảng 2 cho độ dốc của $\log_2 D_{\min}$ theo $\log_2 N$ trên năm quy mô gốc (các lưới 99% ở 12 và 6 lần thời gian lùa sau đó được mở rộng, [mục 3.8](#38-rq8-mức-tăng-theo-n-trên-lưới-dày-hơn-d_sat-và-hình-dạng-đường-cong)):

**Bảng 2: Độ dốc của $\log_2 D_{\min}$ theo $\log_2 N$ trên năm quy mô gốc.**

| Quy tắc | Thời hạn | `wide` | `split` | `outlier_rich` |
| :--- | :---: | :---: | :---: | :---: |
| Nghiêm ngặt | $12\times$ | 0,42 | 0,32 đến 0,42 | 0,42 |
| Nghiêm ngặt | $6\times$ | 0,48 ($N \le 200$) | phẳng ($N \le 100$) | 0,79 ($N \le 100$) |
| Nghiêm ngặt | $3\times$ | 0,79 ($N \le 100$) | phẳng ($N \le 100$) | 0,79 đến 1,50 ($N \le 100$) |
| 99% | $12\times$ | 0,20 đến 0,30 | 0,20 | 0,30 |
| 99% | $6\times$ | 0,30 đến 0,42 | phẳng ($N \le 100$) | 0,42 đến 0,48 |
| 99% | $3\times$ | 0,62 đến 0,68 | phẳng ($N \le 100$) | 0,70 đến 1,10 ($N \le 200$) |

Một khoảng là tập các độ dốc mà các khoảng $D_{\min}$ cho phép; "$N \le 100$" nghĩa là các quy mô lớn hơn chưa có $D_{\min}$ được quyết định.  
*Dữ liệu:* [results_tables.md: Growth with N, strict](../report/results_tables.md#growth-with-n-strict) và [results_tables.md: Growth with N, 99 percent](../report/results_tables.md#growth-with-n-99-percent).

Điều gì quyết định độ dốc:
1. Độ gắn kết có lẽ giữ nó thấp: với mục tiêu không gắn kết, Lama và di Bernardo công bố độ dốc 0,5. Với bầy Strömbom ở thời hạn thong thả, nó là 0,20 đến 0,30 dưới quy tắc 99% trên năm quy mô gốc (0,27 đến 0,38 với bốn quy mô thêm vào, [mục 3.8](#38-rq8-mức-tăng-theo-n-trên-lưới-dày-hơn-d_sat-và-hình-dạng-đường-cong)). Mỗi con cừu bị hút về cả bầy ($c = 1{,}05$, cả $N - 1$ hàng xóm), nên con cừu lạc mà chó lùa quay lại sẽ tự đi về bầy, và chó không phải đi bắt từng con. [Mục 3.11](part6_square_root_law_vi.md#311-rq11-độ-gắn-kết-và-mức-tăng-của-d_min) ủng hộ điều này với một bầy gắn kết yếu hơn trên `wide`, có độ dốc tăng lên 0,40–0,70; bản thân cơ chế chưa được kiểm chứng.
2. Thời hạn gấp làm nó tăng: ở 3 lần thời gian lùa, độ dốc là 0,62–0,68 trên `wide` và 0,70–1,10 trên `outlier_rich` ($N \le 200$) theo quy tắc 99%, và đến 1,50 theo quy tắc nghiêm ngặt ($N \le 100$). [Mục 3.3](#33-rq3-thời-hạn-làm-d_min-thay-đổi-thế-nào) cho thấy các lượt thất bại ở những đội nào khi có 3 lần thời gian lùa và $N = 400$.

## 3.2 RQ2: Bố cục hay quy mô bầy làm D_min thay đổi nhiều hơn?

Người định cỡ một đội chó hay robot sẽ muốn biết nên nhìn trước vào số con vật hay vào mức độ phân tán của chúng. Số con vật quan trọng ít nhất là ngang bằng: ở mọi hàng của Bảng 3, $D_{\min}$ thay đổi theo quy mô bầy ít nhất bằng theo bố cục. Phép so sánh bỏ ra các đường cong không có đội tin cậy, nên nó không tính các trường hợp bố cục quyết định giữa có đội tin cậy và không có, như ở 3 lần thời gian lùa và $N \ge 200$, nơi `split` không có đội tin cậy theo cả hai quy tắc (Bảng 1).

Để so một yếu tố dạng số ($N$) với một yếu tố dạng loại (bố cục), chúng tôi đo cả hai bằng **số lần gấp đôi** của $D_{\min}$:

$$
\text{độ trải (lần gấp đôi)} = \log_2 \left( \frac{D_{\min} \text{ lớn nhất}}{D_{\min} \text{ nhỏ nhất}} \right)
$$

Vậy đi từ 1 chó lên 2 là một lần gấp đôi, từ 1 lên 3 là 1,58, và không đổi là 0. Độ trải theo bố cục được lấy ở từng $N$ rồi lấy trung bình qua các $N$; độ trải theo $N$ được lấy ở từng bố cục rồi lấy trung bình qua các bố cục. Một khoảng được tính tại trung bình nhân của hai đầu khoảng, và các đường cong không có $D$ tin cậy bị bỏ ra.

Bảng 3 cho độ trải trên năm quy mô gốc:

**Bảng 3: Độ trải của $D_{\min}$ theo bố cục và theo $N$ (số lần gấp đôi), năm quy mô gốc.**

| Quy tắc | Thời hạn | Độ trải theo bố cục ($N$ cố định) | Độ trải theo $N$ (bố cục cố định) |
| :--- | :---: | :---: | :---: |
| Nghiêm ngặt | $12\times$ | 0,68 | 1,19 |
| Nghiêm ngặt | $6\times$ | 1,67 | 1,69 |
| Nghiêm ngặt | $3\times$ | 0,76 | 0,97 |
| 99% | $12\times$ | 0,50 | 0,75 |
| 99% | $6\times$ | 0,92 | 1,30 |
| 99% | $3\times$ | 1,25 | 1,28 |

*Dữ liệu:* tính từ các tóm tắt lần gấp đôi trong [Growth with N, strict](../report/results_tables.md#growth-with-n-strict) và [Growth with N, 99 percent](../report/results_tables.md#growth-with-n-99-percent).

Bảng cho thấy gì:
1. Quy mô bầy làm $D_{\min}$ thay đổi nhiều hơn một chút. Ở mọi hàng, độ trải theo $N$ ít nhất bằng độ trải theo bố cục; ở thời hạn 6 lần nghiêm ngặt và 3 lần 99%, hai giá trị gần bằng nhau.
2. Tập trung so với phân tán là một phần của tác động bố cục, không phải toàn bộ. Bầy tập trung giữ $D_{\min} = 1$ ở mọi nơi. Dưới quy tắc 99% ở 12 lần thời gian lùa, `wide` và `outlier_rich` hiếm khi khác nhau quá một chó. Dưới quy tắc nghiêm ngặt ở 6 lần, chúng khác nhau nhiều (3 so với [12] ở $N = 200$), và theo quy tắc 99% ở 3 lần thời gian lùa và $N = 200$, `split` không có đội tin cậy nào trong khi `wide` cần 3 chó và `outlier_rich` 4–10.

## 3.3 RQ3: Thời hạn làm D_min thay đổi thế nào?

Ít thời gian hơn có cần nhiều chó hơn không? Với bầy lớn thì có. Theo quy tắc 99% trên `wide` và `outlier_rich` đến $N = 400$, bước từ 6 xuống 3 lần thời gian lùa lớn hơn nhiều so với từ 12 xuống 6: 12 lần thời gian lùa thay vì 6 tiết kiệm nhiều nhất một chó. Đi từ 6 xuống 3 tốn nhiều nhất một chó ở $N = 100$, nhưng ở $N = 400$ tốn 2 đến 4 chó trên `wide` (từ 2–3 lên 5–6) và ít nhất 3 chó trên `outlier_rich` (từ 3 lên [6]; Hình 3). Mục 2 cho thấy bước nhảy này đến từ đâu ở $N = 400$.

1. Thay đổi đột ngột, không từ từ.  
   Dưới quy tắc 99% trên `wide` và `outlier_rich`, đi từ 6 lên 12 lần thời gian lùa tiết kiệm nhiều nhất một chó đến $N = 400$ (Hình 3; ở 566 các khoảng của Bảng 4 để ngỏ điều này). Đi từ 6 xuống 3 lần tốn hơn nhiều: trên `wide` $N = 400$, $D_{\min}$ từ 2–3 lên 5–6 (trên `split` $N \ge 200$ không đội nào được quyết định là tin cậy ở cả hai thời hạn: cận dưới [1] và [5] ở 6 lần thời gian lùa, không có ở 3 lần).

2. Ở $N = 400$, giới hạn 3 lần thời gian lùa, tức 621 s, cắt bỏ các lượt chậm, với lý do khác nhau trên mỗi bố cục.  
   Trên `wide`, tỉ lệ thành công ở 3 lần thời gian lùa tăng theo đội: 2 trong 10 lượt với 3 chó, 45 trong 60 với 4, 189 trong 200 với 5 (chưa quyết định) và 79 trong 80 với 6, tin cậy từ đó trở lên, nên $D_{\min}$ là 5–6. Vì sao đội nhỏ mất nhiều thời gian như vậy thì chưa được kiểm chứng. Một lý do khả dĩ là đội nhỏ đưa từng con lạc về lần lượt rồi mới lùa bầy, còn đội lớn hơn gom ở nhiều phía cùng lúc; muốn kiểm chứng cần chạy lại các lượt và ghi lại lúc nào đội đang gom và từng chó ở đâu, điều mà các lượt đã lưu không có.  
   Trên `outlier_rich`, tỉ lệ thành công chững lại ở 0,60–0,86 từ 5 chó trở lên và không đội nào đến 24 là tin cậy, nên có cận dưới [6]. Từ 6 chó, tỉ lệ thất bại ở 3 lần thời gian lùa (14%, 17%, 40%, 26% và 23% ở 6, 8, 12, 16 và 24 chó) gần với tỉ lệ lượt ở 12 lần thời gian lùa mà 9% cuối của bầy vào đích muộn hơn 90% đầu quá một phút (14%, 17%, 40%, 23% và 22%; hai lần chạy có số hạt giống khác nhau ở mỗi đội). Những thất bại này có lẽ là các con về muộn của [mục 3.7](part3_beyond_dmin_vi.md#37-rq7-vượt-quá-d_min-đủ-chó-chi-phí-và-áp-lực-lên-bầy), điều mà thêm chó không loại bỏ được, chứ không phải do thiếu chó.

3. Thời hạn ngắn hơn chỉ cắt ngắn cùng một lượt chạy.  
   Mọi lượt chạy mà hai thời hạn có chung (cùng ô và hạt giống: 26.620 lượt giữa 12 và 6 lần thời gian lùa, 10.760 lượt giữa 6 và 3 lần và 10.360 lượt giữa 12 và 3 lần theo quy tắc 99%, 10.500 lượt giữa 12 và 6 lần theo quy tắc nghiêm ngặt) thành công ở thời hạn ngắn hơn đúng khi nó đã xong trong giới hạn đó ở thời hạn dài hơn, và xong ở cùng một giây. Vì vậy $D_{\min}$ ở mọi thời hạn đến 12 lần thời gian lùa có thể đọc từ các lượt 12 lần, trong phạm vi các hạt giống của chúng. $D_{\mathrm{sat}}$, đội mà vượt quá nó thêm chó không còn làm việc lùa nhanh hơn ([mục 3.7](part3_beyond_dmin_vi.md#1-khi-nào-thêm-chó-không-còn-giúp-d_sat)), ở 12 và 6 lần là như nhau trên mọi đường cong có $D_{\min}$ ở cả hai (`outlier_rich` $N = 566$ cho hai khoảng chồng nhau, 8–24 và 8–12). Trên `wide` ở $N \ge 100$, $D_{\min}$ chỉ chạm $D_{\mathrm{sat}}$ ở 3 lần thời gian lùa: ở $N = 100$, 200 và 400, $D_{\mathrm{sat}}$ là 2, 3 và 6 so với $D_{\min}$ 2, 3 và 5–6, nên khi ít thời gian, đội tin cậy nhỏ nhất đã gần như là đội nhanh nhất. Trên các bố cục tản mát khác thì ở 3 lần không như vậy (`outlier_rich` $N = 100$: $D_{\min}$ 2 so với $D_{\mathrm{sat}}$ 3; `split` $N = 100$: 1 so với 4), và trên `compact` cả hai là 1 ở mọi thời hạn ([bảng theo từng lượt](../report/results_tables.md#single-trials-and-curves-across-folders)).

![Tác động của thời hạn lên đường cong thành công](../figures/fig29_deadline.png)

**Hình 3: Tỷ lệ thành công theo quy mô đội ở ba thời hạn.** Thời hạn gấp hơn đẩy các đường về phía đội lớn hơn, và bước từ 6 xuống 3 lần thời gian lùa lớn hơn nhiều so với từ 12 xuống 6.

- Trái và giữa: tỷ lệ thành công theo quy tắc 99% theo $D$ trên `wide` $N = 400$ (trái) và `outlier_rich` $N = 200$ (giữa), mỗi điểm kèm khoảng Clopper–Pearson 99%. Xanh nhạt, xanh vừa và xanh đậm là 12, 6 và 3 lần thời gian lùa; đường chấm là $\theta = 0{,}90$.
- Phải: $D_{\min}$ theo thời hạn cho `wide` và `outlier_rich` ở $N = 200$ (liền, hình tròn) và $N = 400$ (đứt, hình vuông). Thanh tô màu là khoảng và điểm rỗng là cận dưới.

*Dữ liệu:* `results/dmin_f99_m12`, `dmin_f99_m6` và `dmin_f99_m3`; giá trị trong [results_tables.md: D_min by layout and N, success at 99 percent](../report/results_tables.md#d_min-by-layout-and-n-success-at-99-percent).

## 3.8 RQ8: Mức tăng theo N trên lưới dày hơn, D_sat, và hình dạng đường cong

Khi bầy lớn mãi lên, đội có tiếp tục tăng, hay chững lại ở một đội lớn nhất? Dữ liệu chưa trả lời được. Theo quy tắc 99% đến $N = 566$, một đường cong tăng mãi (luật lũy thừa) và một đường cong chững lại ở mức trần $D_\infty$ khớp $D_{\min}$ trên `wide` và `outlier_rich` tốt như nhau (ý 3, Hình 4); đến 566 các đội vẫn còn nhỏ và một số là khoảng rộng (Bảng 4). Bầy lớn hơn có thể phân biệt được hai dạng, nhưng trên khoảng 600 con chính mô hình đặt ra giới hạn, được mô tả ở [mục 3.13](#313-rq13-bầy-rất-lớn-và-một-giới-hạn-của-quy-tắc-lùa) với các lượt chạy đến 3200 con.

Để xác định hình dạng của $D_{\min}(N)$, các lưới 99% ở 12 và 6 lần thời gian lùa được thêm bốn quy mô bầy: $N = 71, 141, 283$ (trung điểm trên thang log giữa 50 và 400) và $N = 566 = 400\sqrt{2}$.

Các quy mô thêm vào tăng theo bước $\sqrt{2}$, cho mọi quy mô cùng trọng số trong một phép khớp log-log, và dừng ở 566, bước cuối dưới [giới hạn hiệu chỉnh](glossary_vi.md#nhiệm-vụ-lùa): trên khoảng 600 (ranh giới nằm giữa 600 và 630), một bầy xuất phát lỏng giữ lại một phần kích thước của nó, nên một bán kính $R_f(N)$ duy nhất không còn mô tả được nó ([quy mô bầy](task_design_vi.md#quy-mô-bầy)).

1. Các độ dốc hẹp lại.  
   Trên chín quy mô, độ dốc của $D_{\min}$ theo $N$ là 0,27 đến 0,38 trên `wide` và 0,28 đến 0,38 trên `outlier_rich` ở 12 lần thời gian lùa, và 0,38 đến 0,61 trên `wide` và 0,40 đến 0,58 trên `outlier_rich` ở 6 lần. Ở thời hạn thong thả nó vẫn dưới 0,5.

2. $D_{\mathrm{sat}}$ tăng nhanh gấp khoảng 1,6 lần $D_{\min}$ trên `wide` ở 6 lần thời gian lùa (tỷ số tại trung điểm; 1,15 đến 2,4 lần theo hai đầu khoảng).  
   Trên `wide` ở 6 lần thời gian lùa, $D_{\mathrm{sat}}$ là 1, 1, 1, 2, 3, 3, 4, 5 chó từ $N = 25$ đến 400, và 7–24 ở 566 (độ dốc 0,70 đến 0,91). Khoảng cách giữa đội tin cậy và đội nhanh nhất rộng ra khi bầy lớn lên.

3. Tăng đều và đường cong chững lại khớp như nhau.  
   Đến $N = 566$, dữ liệu khớp một luật lũy thừa $D = c N^b$ và một đường cong bão hòa $D = 1 + (D_\infty - 1) N / (N + K)$ như nhau (log odds 0,0; Hình 4). Ở $N = 1600$, các đường cong khớp được cho phép 1,5 đến 6,7 chó ở 12 lần thời gian lùa (3,1 đến 10,4 ở 6 lần). Để phân biệt chúng cần bầy lớn hơn, mà mô hình không hiệu chỉnh được ([mục 3.13](#313-rq13-bầy-rất-lớn-và-một-giới-hạn-của-quy-tắc-lùa)). Số mũ luật lũy thừa khớp được là 0,29 (`wide`) và 0,22 (`outlier_rich`) ở 12 lần thời gian lùa và 0,34 cho cả hai ở 6 lần, còn các đường cong bão hòa dừng ở $D_\infty$ = 2,6, 2,0, 7,4 và 8,0. Các lượt chạy bầy lớn, trong một thiết lập khác (điểm lùa bị giới hạn, $R_f$ áp đặt), cần nhiều hơn mức các phép khớp ở 12 lần cho phép trên `wide`: không đội nào đến 12 chó tin cậy ở $N = 1600$.

Bảng 4 cho $D_{\min}$ và $D_{\mathrm{sat}}$ trên chín quy mô bầy (quy tắc 99%):

**Bảng 4: $D_{\min}$ và $D_{\mathrm{sat}}$ trên chín quy mô bầy, quy tắc 99%.**

| $N$ | 25 | 50 | 71 | 100 | 141 | 200 | 283 | 400 | 566 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `wide`, $12\times$ | 1 | 1 | 1 | 1 | 2 | 1–2 | 2 | 2 | 2–3 |
| `outlier_rich`, $12\times$ | 1 | 1 | 1 | 1–2 | 2 | 2 | 2 | 2 | 2–3 |
| `wide`, $6\times$ | 1 | 1 | 1 | 1 | 2 | 2 | 2–3 | 2–3 | 3–7 |
| `outlier_rich`, $6\times$ | 1 | 1 | 1 | 2 | 2 | 2–3 | 2–3 | 3 | 3–6 |
| $D_{\mathrm{sat}}$ `wide`, $6\times$ | 1 | 1 | 1 | 2 | 3 | 3 | 4 | 5 | 7–24 |

*Dữ liệu:* [results_tables.md: Finish-time top-up, densified N, independent shepherds, Kubo to D = 24, 99 percent](../report/results_tables.md#finish-time-top-up-densified-n-independent-shepherds-kubo-to-d--24-99-percent).

![D_min trên chín quy mô và phạm vi của hai dạng đường cong](../figures/fig35_growth_fits.png)

**Hình 4: $D_{\min}$ trên chín quy mô bầy, và mỗi dạng đường cong có thể đi đến đâu.** Luật lũy thừa và đường cong bão hòa đều khớp dữ liệu đến $N = 566$; vượt qua đó, các vùng tô cho thấy mỗi dạng có thể đi đến đâu.

- Ký hiệu: `wide` hình tròn và `outlier_rich` hình vuông trên trục log-log. Mỗi điểm là $D_{\min}$ ở đội tin cậy, và một thanh kéo xuống $D_{\min,\mathrm{low}}$ ở nơi một đội nhỏ hơn còn mở (một khoảng, [mục 2.1](d_min_report_vi.md#21-khi-nào-một-đội-là-tin-cậy)). Đường dọc đánh dấu giới hạn hiệu chỉnh ($N \approx 600$); bên phải nó, các vùng tô cho thấy các luật lũy thừa (cạnh trên đứt) và các đường cong bão hòa (cạnh trên chấm) khớp dữ liệu có thể nằm ở đâu.
- Các khung: 12 lần thời gian lùa (trái) và 6 lần (phải).

*Dữ liệu:* [results_tables.md: D_min, dmin_f99_m12](../report/results_tables.md#d_min-dmin_f99_m12), [results_tables.md: D_min, dmin_f99_m6](../report/results_tables.md#d_min-dmin_f99_m6), và [results_tables.md: fits dmin_f99_m12](../report/results_tables.md#fits-dmin_f99_m12-d_minn-power-law-against-saturating-curve).

## 3.13 RQ13: Bầy rất lớn và một giới hạn của quy tắc lùa

Điều gì xảy ra với các bầy lớn hơn hẳn các bầy của lưới chính, và ở đó có hiện ra một đội lớn nhất không? Các lượt chạy này không cho thấy đội lớn nhất nào, nhưng chưa đủ để kết luận. Trên $N \approx 1056$, quy tắc lùa của Strömbom không còn hoạt động (ý 1). Khi giới hạn điểm lùa, đội nhỏ nhất trên `wide` tiếp tục tăng và vượt 12 chó ở $N = 1600$ (ý 2, Bảng 5). Các lượt chạy này khác lưới chính ở bán kính bầy áp đặt, điểm lùa bị giới hạn và đội dừng ở 12 chó, nên chúng không phải phần nối tiếp của các đường cong ở [mục 3.8](#38-rq8-mức-tăng-theo-n-trên-lưới-dày-hơn-d_sat-và-hình-dạng-đường-cong).

Chúng tôi chạy các bầy 800 đến 3200 con ở 12 lần thời gian lùa. Trên khoảng 600 con, một bán kính không còn mô tả được bầy của mô hình ([mục 3.8](#38-rq8-mức-tăng-theo-n-trên-lưới-dày-hơn-d_sat-và-hình-dạng-đường-cong)), nên trên $N = 566$, $R_f$ được đặt để giữ mật độ của bầy 566: $R_f(N) = R_f(566)\sqrt{N/566}$.

### 1. Trên N ≈ 1056, điểm lùa nằm ngoài tầm của cừu
Trong quy tắc của Strömbom, chó lùa đứng phía sau tâm bầy $r_a \sqrt{N} = 2\sqrt{N}$ m, và một con cừu chỉ phản ứng với chó trong vòng $r_s = 65$ m, nên trên $N \approx 1056$ chó đứng ở nơi ít hoặc không con cừu nào phản ứng và bầy không được lùa ([quy tắc lùa và giới hạn của nó](models_vi.md#3-lùa-và-giới-hạn-của-nó-với-bầy-lớn)). Ở $N = 1131$, không đội nào đến 12 chó thành công trong bất kỳ lượt nào trong 10 lượt, trên cả `compact` lẫn `wide`.

### 2. Giới hạn điểm lùa khôi phục việc lùa
Khi giới hạn khoảng lùa ở $r_s - r_a = 63$ m (`dmin_f99_big_cap`), một biến thể HerdSim của quy tắc bài báo:
- Compact: một chó lùa được bầy 800 và 1131, cần hai chó ở 1600. Ở 3200, mọi đội từ 3 đến 12 chó thành công trong cả 42 lượt đã chạy.
- Wide: 3 chó ở $N = 800$, 5–9 ở 1131 và hơn 12 ở 1600. Một bầy phân tán lớn cần nhiều chó để giữ các phía của nó lại với nhau.
- Bầy tập trung không còn bão hòa ở một chó: $D_{\mathrm{sat}}$ là 2 ở $N = 800$ và 6 ở 1131 và 1600. Một chó ở 1131 là tin cậy nhưng cần trung vị 3838 s, so với 1255–1367 s khi có 2 đến 12 chó.
- Câu trả lời phụ thuộc vào mật độ áp đặt: `wide` $N = 800$ cần 4–5 chó khi $R_f$ được đặt cho một bầy dày hơn ($1/\sqrt{2}$ bán kính gốc), so với 3 ở thiết lập gốc và thiết lập thưa hơn. Ở 566 cả ba cho 2–3, nhưng đó không phải phép kiểm tra về mật độ, vì bán kính áp đặt chỉ áp dụng trên 566 và ba lượt chạy là cùng một nhiệm vụ ở đó. Nguyên nhân chưa được kiểm chứng.

Bảng 5 cho kết quả với điểm lùa bị giới hạn (quy tắc 99%, 12 lần thời gian lùa):

**Bảng 5: $D_{\min}$ khi điểm lùa bị giới hạn ở 63 m, quy tắc 99%, 12 lần thời gian lùa.**

| Giới hạn ở 63 m, 99%, $12\times$ | $N = 800$ | $N = 1131$ | $N = 1600$ | $N = 3200$ (một phần) |
| :--- | :---: | :---: | :---: | :---: |
| `compact` | 1 | 1 | 2 | 42 / 42 lượt thành công ở $D = 3$–12 ($D = 1, 2$ không chạy) |
| `wide` | 3 | 5–9 | none đến 12 | none (0 / 58 ở $D = 2$–12) |

*Dữ liệu:* [results_tables.md: dmin_f99_big_cap](../report/results_tables.md#dmin_f99_big_cap); cột $N = 3200$ từ `results/dmin_f99_big_cap` (100 lượt, dừng sớm). Kết quả không giới hạn trong [results_tables.md: D_min, dmin_f99_big](../report/results_tables.md#d_min-dmin_f99_big).

Hoạt ảnh 6 trong [mô hình](models_vi.md#3-lùa-và-giới-hạn-của-nó-với-bầy-lớn) chạy lại một chó ở $N = 1131$ không và có giới hạn: không giới hạn thì chó chỉ chạm tới phần sau của bầy, có giới hạn thì nó lùa được bầy vào.
