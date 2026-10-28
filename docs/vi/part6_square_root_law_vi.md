# Độ gắn kết và quy luật căn bậc hai

Phần 6 của báo cáo HerdSim về quy mô đội. [Phần tổng quan](d_min_report_vi.md) gồm tóm tắt, các câu hỏi nghiên cứu, [quy tắc quyết định](d_min_report_vi.md#2-quy-tắc-quyết-định) định nghĩa $D_{\min}$, khoảng và cận dưới của nó, phần thảo luận và [tài liệu tham khảo](d_min_report_vi.md#tài-liệu-tham-khảo). Các thuật ngữ được định nghĩa trong [bảng thuật ngữ](glossary_vi.md).

## 3.11 RQ11: Độ gắn kết và mức tăng của D_min

Lama và di Bernardo (2024) công bố rằng đội tăng theo $\sqrt{N}$ với các mục tiêu không tụ bầy. Để nối trường hợp của họ với bầy Strömbom, chúng tôi đổi độ gắn kết theo hai cách: (1) trọng số hút $c$, tăng từ 1,05 của bài báo lên 1,3, 1,6 và 2,0, và (2) số hàng xóm mỗi con cừu bị hút về, giảm từ cả $N - 1$ xuống một nửa bầy ($n = 0{,}5N$).

Độ mạnh của sự gắn kết có thay đổi tốc độ tăng của đội không? Trên `wide`, gắn kết yếu hơn đẩy độ dốc về phía 0,5 của mục tiêu không gắn kết, còn gắn kết mạnh hơn thì không (ý 1 và 2, Bảng 1). Trên `outlier_rich`, bầy gắn kết yếu hơn giữ độ dốc ở 0,30, bằng dòng của bài báo ([các bảng kết quả](../report/results_tables.md#dmin_f99_k05)). Bầy gắn kết yếu hơn được chạy trên bốn quy mô (50 đến 400) và dòng của bài báo trên năm (25 đến 400), nên hai độ dốc không được khớp trên cùng các quy mô. Chỉ một mức yếu hơn được chạy, vì các bầy yếu hơn không hiệu chỉnh được ([phụ lục B](appendix_run_record_vi.md#phụ-lục-b-các-khẳng-định-và-bằng-chứng), khẳng định 6).

1. Gắn kết mạnh hơn thay đổi ít.  
   Với $c = 1{,}3$, 1,6 hay 2,0, độ dốc trên `wide` là 0,20, và $D_{\min}$ giảm nhiều nhất một chó ở mọi quy mô. Với $c = 1{,}05$ của Strömbom và mỗi con cừu bị hút về cả bầy, bầy đã giữ liền; kéo nó chặt hơn không giúp gì cho chó lùa. Nhưng nó làm các đội lớn chậm hơn trên `outlier_rich`: với $c = 2{,}0$ ở 12 lần thời gian lùa, trung vị thời gian hoàn thành là 406 s với 2 chó và 499–530 s với 6 đến 24 chó ở $N = 200$, và 517 s với 4 chó và 674–726 s với 6 đến 24 chó ở $N = 400$, nên $D_{\mathrm{crowd}} = 6$ ở cả hai.

2. Gắn kết yếu hơn làm $D_{\min}$ tăng nhanh hơn, về phía quy luật căn bậc hai.  
   Với $n = 0{,}5N$, độ dốc trên `wide` thành 0,40 đến 0,70, một khoảng chứa 0,5 của mục tiêu không gắn kết.  
   Trên `split`, bầy yếu hơn tách ra dưới một chó: $D_{\min}$ từ 1 lên 3–4 ở $N = 200$ và từ 2 lên 4–5 ở $N = 400$. Trên `wide`, mức yếu hơn duy nhất này gợi ý rằng mức tăng chậm của $D_{\min}$ phụ thuộc vào việc mỗi con cừu bị hút về cả bầy; trên `outlier_rich` nó không làm độ dốc thay đổi, nên sự phụ thuộc này không đúng chung.

Bảng 1 cho các mức gắn kết (`wide`, quy tắc 99%, 12 lần thời gian lùa):

**Bảng 1: $D_{\min}$ và độ dốc của nó ở ba mức gắn kết trên `wide`, quy tắc 99%, 12 lần thời gian lùa.**

| Độ gắn kết (`wide`, 99%, $12\times$) | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ | Độ dốc |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Yếu hơn ($n = 0{,}5N$) | 1 | 1 | 2 | 2–4 | 0,40 đến 0,70 |
| Bài báo ($c = 1{,}05$) | 1 | 1 | 1–2 | 2 | 0,20 đến 0,30 |
| Mạnh hơn ($c = 1{,}3; 1{,}6; 2{,}0$) | 1 | 1 | 1 | 2 | 0,20 |

*Dữ liệu:* hàng bài báo từ [results_tables.md: dmin_f99_m12](../report/results_tables.md#dmin_f99_m12) và [results_tables.md: Growth with N, 99 percent](../report/results_tables.md#growth-with-n-99-percent); các lượt chạy gắn kết từ [results_tables.md: D_min, dmin_f99_c1.3](../report/results_tables.md#d_min-dmin_f99_c13), [dmin_f99_c1.6](../report/results_tables.md#d_min-dmin_f99_c16), [dmin_f99_c2.0](../report/results_tables.md#d_min-dmin_f99_c20) và [dmin_f99_k05](../report/results_tables.md#d_min-dmin_f99_k05); độ dốc từ [results_tables.md: dmin_f99_c1.3](../report/results_tables.md#dmin_f99_c13), [dmin_f99_c1.6](../report/results_tables.md#dmin_f99_c16), [dmin_f99_c2.0](../report/results_tables.md#dmin_f99_c20) và [dmin_f99_k05](../report/results_tables.md#dmin_f99_k05) (growth).

## 3.14 RQ14: Mục tiêu không gắn kết: quy luật căn bậc hai của Lama và di Bernardo (2024)

Để so bầy Strömbom với các mục tiêu không tụ bầy, chúng tôi chạy mô hình của Lama và di Bernardo (2024) trong HerdSim với phương pháp `lama` trên nhiệm vụ `gather` ([mô hình](models_vi.md#mô-hình-mục-tiêu-brownian-không-liên-kết-lama-2024), [nhiệm vụ](task_design_vi.md#6-nhiệm-vụ-gom-lama-và-di-bernardo-2024)). Một lượt kéo dài tối đa 5000 s, là thời gian tối đa mà Hình S8 trong phần bổ sung của bài báo ghi cho $R = 50$ và bán kính cảm nhận 10; phần chính của bài báo chạy mỗi trường hợp tới khi tỉ lệ trong đích ổn định.

Các mục tiêu không tụ bầy có theo quy luật căn bậc hai cả trong HerdSim không, và quy luật có giữ được dưới cách HerdSim coi một đội là đủ, vốn chặt hơn ([hai cách tính](#1-hai-cách-gọi-một-đội-là-đủ)), không? Với tầm cảm nhận vô hạn thì có, theo cả hai cách tính (kết quả 2). HerdSim cho kết quả gần với ngưỡng của bài báo cho $R = 50$ và bán kính cảm nhận 10, dòng duy nhất trong Bảng I của phần bổ sung được so sánh ở đây, và khi đặt cạnh nhau, các bản đồ của nó có cùng hình dạng với bản đồ của bài báo (kết quả 1, Hình 1). Với bán kính cảm nhận 10, hai cách tính tách nhau ngay trên ngưỡng của bài báo (kết quả 3, Hình 2).

### 1. Hai cách gọi một đội là đủ
Cùng các lượt chạy được đọc theo hai cách ([hai thống kê](task_design_vi.md#hai-thống-kê)): thống kê của bài báo coi một đội là đủ khi tỷ lệ mục tiêu trong đích lúc kết thúc, lấy trung bình qua các lượt, ít nhất 0,99; quy tắc của HerdSim coi là đủ khi ít nhất 90% số lượt kết thúc với 99% mục tiêu trong đích, với độ tin cậy 99%.

### 2. Kết quả
1. HerdSim cho kết quả gần với bài báo.  
   Bài báo nêu ngưỡng của nó dưới dạng số trong Bảng I của phần tài liệu bổ sung; ở dòng được so sánh ở đây, $R = 50$ và bán kính cảm nhận 10, đội nhỏ nhất chỉ theo quy luật căn bậc hai từ $\sqrt{N} = 8$, 9 và 11 trở lên, ứng với mức 90%, 95% và 99%. HerdSim cho 8, 9 và 12, đọc ngưỡng là $\sqrt{N}$ đầu tiên mà từ đó đội nhỏ nhất nhập vào dải căn bậc hai. Các kết quả còn lại của bài báo là bản đồ màu ([Hình 2](https://doi.org/10.1103/PhysRevResearch.6.L032012)). Đặt cạnh nhau (Hình 1), bản đồ của HerdSim và của bài báo có cùng hình dạng: với bán kính 10, khi ít mục tiêu thì không đội nào đến 25 đạt được, rồi có một ngưỡng rõ, và trên ngưỡng là một dải đội tăng theo căn bậc hai của số mục tiêu; khi thấy mọi thứ, dải đó kéo dài suốt cả khoảng. Có hai khác biệt nhỏ: với bán kính 10 và ít mục tiêu, HerdSim gom được ít hơn bài báo một chút, và đường 0,99 của HerdSim quay lên hơi xa hơn về bên phải so với của bài báo.

   ![Hình 2 của bài báo cạnh bản đồ của HerdSim](../figures/fig39_lama_maps.png)

   **Hình 1: Bản đồ của bài báo phía trên bản đồ của HerdSim.** Bản đồ của HerdSim có cùng hình dạng với bản đồ của bài báo.

   - Ký hiệu: mỗi ô là tỷ lệ mục tiêu trong đích lúc kết thúc, lấy trung bình qua các lượt, cho một số mục tiêu (trục hoành, theo căn bậc hai) và một số người chăn (trục tung). Đường trắng đánh dấu mức 0,99. Lưới của HerdSim có 10 đến 200 lượt mỗi ô, bài báo có 50.
   - Các khung: Hình 2 của bài báo ở trên và HerdSim ở dưới, với thấy mọi thứ ở bên trái và bán kính cảm nhận 10 ở bên phải.
   - Dải xám: lưới của HerdSim dừng ở 400 mục tiêu ($\sqrt{N} = 20$), nên đoạn 21 đến 25 trên trục của bài báo không có dữ liệu ([vì sao](task_design_vi.md#quy-mô-bầy)).

   *Dữ liệu:* trên, Hình 2 của Lama và di Bernardo (2024), Phys. Rev. Research 6, L032012, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), đã cắt; dưới, `lama_r50_inf` và `lama_r50`.

2. Khi thấy mọi thứ, cả hai cách đều cho quy luật căn bậc hai.  
   Hai cách cho cùng đội nhỏ nhất ở gần như mọi quy mô (8 người chăn cho 100 mục tiêu, 13 cho 225, 17 cho 400). Số mũ khớp được là 0,52 (thống kê của bài báo) và 0,53 (quy tắc của HerdSim). Khác bầy Strömbom, việc gom tiếp tục nhanh hơn khi thêm người chăn: ở 400 mục tiêu, trung vị thời gian là 1232 s với 17 người chăn, 451 s với 20 và 222 s với 25, và từ 169 mục tiêu $D_{\mathrm{sat}}$ ít nhất là 25, đỉnh của lưới.

3. Với bán kính cảm nhận 10, hai cách tách nhau gần ngưỡng.  
   Với 100 mục tiêu trở xuống, không đội nào đến 25 người chăn là tin cậy; đến 81 mục tiêu, mọi thất bại kết thúc với các mục tiêu không người chăn nào thấy được.  
   Ngay trên ngưỡng, từ 100 đến 196 mục tiêu, hai cách tách nhau (Hình 2):
   - Ở 144 mục tiêu, 11 người chăn gom trung bình 99,2% mục tiêu, nên thống kê của bài báo chấp nhận. Nhưng chỉ 21 trên 30 lượt của họ kết thúc với 99% mục tiêu trong đích (khoảng 99% là 0,45–0,89). Chín lượt thất bại mất từ hai đến bốn trên 144 mục tiêu; trộn với các lượt mất một hoặc không mất gì, trung bình vẫn trên 0,99.
   - Quy tắc của HerdSim không chấp nhận 11 người chăn; $D_{\min}$ của nó là khoảng 17–25.
   - Một mức trung bình có thể che đi những lượt thất bại. Đếm từng lượt thì không, nên gần ngưỡng hai câu trả lời chênh nhau, 6 đến 14 người chăn ở 144 mục tiêu và ít hơn ở các mức trên.

![Mô hình Lama và di Bernardo trong HerdSim](../figures/fig38_lama.png)

**Hình 2: Đội nhỏ nhất theo số mục tiêu trong mô hình của Lama và di Bernardo (2024).** Khi thấy mọi thứ, hai thống kê trùng nhau; gần ngưỡng ở bán kính 10, trung bình chấp nhận 11 người chăn ở 144 mục tiêu, trong khi quy tắc của HerdSim cần 17–25.

- Ký hiệu: hình tròn là thống kê của bài báo áp dụng lên các lượt của HerdSim; hình thoi là $D_{\min}$ của HerdSim, với thanh cho khoảng, tam giác cho cận dưới và dấu chéo cho không có đội tin cậy đến 25.
- Các khung: bán kính cảm nhận 10 với vùng ngưỡng tô xám (trái), và thấy mọi thứ (phải).

*Dữ liệu:* [results_tables.md: Lama and di Bernardo (2024): gather task](../report/results_tables.md#lama-and-di-bernardo-2024-gather-task).

Hoạt ảnh 5 trong [thiết kế nhiệm vụ](task_design_vi.md#khi-nào-một-lượt-kết-thúc-và-thế-nào-là-thành-công) chạy lại hai lượt của ô này, 144 mục tiêu và 11 người chăn: hạt giống 0 thành công, còn hạt giống 1 kết thúc với hai mục tiêu nằm ngoài tầm của mọi người chăn.

## 5.1 So với quy luật căn bậc hai
Vì sao bầy Strömbom cần thêm ít chó hơn khi lớn lên so với mức mà quy luật căn bậc hai của mục tiêu không gắn kết đưa ra? Độ dốc của chúng tôi theo quy tắc 99% ở 12 lần thời gian lùa (0,20–0,30 trên năm quy mô; 0,27–0,38 trên chín, [mục 3.8](part1_growth_vi.md#38-rq8-mức-tăng-theo-n-trên-lưới-dày-hơn-d_sat-và-hình-dạng-đường-cong)) thấp hơn mức tăng $\sqrt{N}$ (độ dốc 0,5) mà Lama và di Bernardo (2024) công bố cho mục tiêu không tụ bầy. Một cách đọc hợp lý: không có gắn kết, người chăn phải đi bắt từng mục tiêu; trong một bầy gắn kết, mỗi con cừu bị hút về cả bầy ($n = N - 1$), nên khi chó đã lùa một con lạc quay lại, nó tự nhập lại bầy.

Các lượt chạy về độ gắn kết ([mục 3.11](#311-rq11-độ-gắn-kết-và-mức-tăng-của-d_min)) kiểm tra cách đọc này, với kết quả không đồng nhất. Một bầy gắn kết hơn bầy của bài báo hầu như không đổi độ dốc (0,20 trên `wide`, so với 0,20–0,30), trong khi bầy yếu hơn duy nhất mà mô hình tạo được (mỗi con cừu bị hút về một nửa bầy) nâng nó lên 0,40–0,70, một khoảng chứa 0,5. Thời hạn cũng vậy: ở 6 lần thời gian lùa, độ dốc là 0,38–0,61. Trên `wide`, cả gắn kết yếu hơn lẫn áp lực thời gian đều đẩy độ dốc về phía 0,5; hai độ dốc được khớp trên số quy mô khác nhau (bốn và chín).

[Mục 3.14](#314-rq14-mục-tiêu-không-gắn-kết-quy-luật-căn-bậc-hai-của-lama-và-di-bernardo-2024) cho phía không gắn kết ngay trong HerdSim. Mô hình của bài báo cho lại quy luật của chính nó: số mũ 0,52–0,53 khi thấy mọi thứ ($N \ge 100$) và 0,41–0,42 với bán kính cảm nhận 10 cho $N \ge 225$, theo cả hai thống kê (gần ngưỡng hơn thì hai thống kê không trùng nhau, như [mục 3.14](#314-rq14-mục-tiêu-không-gắn-kết-quy-luật-căn-bậc-hai-của-lama-và-di-bernardo-2024) cho thấy). Cả hai đều cao hơn 0,27–0,38 của bầy Strömbom ở 12 lần thời gian lùa, đúng như cách đọc trên. Hai loạt chạy còn khác nhau về nhiệm vụ và quy tắc người chăn, nên phần chênh lệch do độ gắn kết chưa được đo.
