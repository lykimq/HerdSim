# Quy mô đội để lùa một bầy cừu mô phỏng: Tối thiểu, đủ và quá nhiều chó

*Báo cáo nghiên cứu HerdSim*  
*39 giao thức và 367.150 lượt chạy, không có lỗi mô phỏng nào: 23 giao thức của nghiên cứu đầu (164.740 lượt), 14 giao thức tiếp theo và ba lượt chạy tiếp (162.130 lượt), và hai giao thức của mô hình mục tiêu không gắn kết của Lama và di Bernardo (2024) (40.280 lượt).*  
*Các mô hình và quy tắc đội được mô tả ở [docs/methods/models_vi.md](../methods/models_vi.md), hình học nhiệm vụ và cách lấy mẫu ở [docs/experiments/task_design_vi.md](../experiments/task_design_vi.md). Báo cáo này trình bày kết quả.*

---

## Tóm tắt

Cần bao nhiêu chó ($D$) để gom một bầy $N$ con cừu và lùa vào đích trước thời hạn? Chúng tôi hỏi ba điều: ít nhất là bao nhiêu ($D_{\min}$), bao nhiêu là đủ trước khi thêm chó không còn giúp gì ($D_{\mathrm{sat}}$), và khi nào thêm chó lại làm tệ đi. $D_{\min}$ là đội nhỏ nhất có tỷ lệ thành công ít nhất 0,90 với độ tin cậy 99% (khoảng Clopper–Pearson chính xác). Một bộ chạy thích ứng chỉ thêm lượt chạy cho những ô chưa có câu trả lời, tối đa 200 lượt mỗi ô.

23 giao thức đầu bao phủ các quy mô bầy $N = 25$ đến 400, bốn bố cục xuất phát (`compact`, `wide`, `split`, `outlier_rich`) và ba thời hạn (12, 6 và 3 lần thời gian lùa), mỗi thứ dưới hai quy tắc thành công: mọi con cừu vào đích (nghiêm ngặt) và 99% số cừu vào đích. Các giao thức tiếp theo chỉ dùng quy tắc 99%. Chúng thêm $D_{\mathrm{sat}}$, bốn quy mô bầy nữa đến $N = 566$, các quy tắc đội khác, giữ bầy trong đích, chó chiếm chỗ, độ gắn kết, tầm cảm nhận giới hạn, và bầy đến $N = 3200$. Hai giao thức cuối chạy mô hình mục tiêu không gắn kết của Lama và di Bernardo (2024) trên nhiệm vụ của chính họ.

Kết quả chính:

1. **Bầy tập trung cần một chó.** $D_{\min} = 1$ ở mọi quy mô bầy và mọi thời hạn, và thêm chó không rút ngắn thời gian lùa.
2. **Bầy phân tán chỉ cần thêm ít.** $D_{\min} = 1$ đến $N = 50$ và chỉ 2 hoặc 3 chó ở $N = 400$ với thời hạn thong thả. Trên thang log-log, độ dốc tăng là 0,20–0,42 ở 12 lần thời gian lùa và 0,30–0,79 ở 6 lần (năm quy mô bầy; 0,27–0,38 và 0,38–0,61 trên chín quy mô, mục 8).
3. **Thời hạn quan trọng hơn quy mô bầy.** Rút từ 12 xuống 3 lần thời gian lùa làm $D_{\min}$ trên `wide` $N = 400$ tăng từ 2 lên 5–6, nhiều hơn khi đi từ $N = 100$ lên 400.
4. **Dưới quy tắc nghiêm ngặt, con cừu cuối cùng quyết định.** Trong 97% số lượt thất bại nghiêm ngặt với 6 chó trở lên (lượt chạy cơ sở của phần độ nhạy), 99% bầy đã từng ở trong đích. Với chó chậm hơn (1,15 m/s thay vì 1,5), $D_{\min}$ nghiêm ngặt trên `outlier_rich` $N = 400$ giảm từ không có trên lưới xuống 6.
5. **Quy tắc 99% ổn định trước các lựa chọn thiết lập.** Dưới quy tắc này, $D_{\min}$ thay đổi nhiều nhất khoảng một chó khi đổi vị trí thả chó, khoảng cách xuất phát, tốc độ chó hay tham số cừu; chỉ đích nhỏ hơn làm nó tăng nhiều hơn. Dưới quy tắc nghiêm ngặt, cùng những thay đổi đó thường đẩy nó thành "không có trên lưới".
6. **Chó không có quy tắc đội thì không mở rộng được.** Với FAT, mọi chó đuổi cùng một con cừu, nên không đội nào tin cậy ở $N \ge 200$ trên bất kỳ bố cục phân tán nào, kể cả bầy tập trung $N = 400$.
7. **Vượt $D_{\mathrm{sat}}$, thêm chó tốn kém nhưng không gây hại** (mục 3.7). Thời gian hoàn thành ở mức 0,96–1,01 lần thời gian tại $D_{\mathrm{sat}}$, trong khi thời gian chó tăng theo $D$, và thời gian mỗi con cừu chạy trốn không tăng. Dưới quy tắc 99%, không đội nào đến 24 chó làm nhiệm vụ thất bại trên năm quy mô ban đầu (một chỗ trũng trên lưới dày hơn); thêm chó chủ yếu làm chậm bầy `split`.
8. **Lưới dày hơn** (mục 3.8): trên chín quy mô bầy, $D_{\min}$ tăng với độ dốc 0,27–0,38 ở 12 lần thời gian lùa và 0,38–0,61 ở 6 lần, còn $D_{\mathrm{sat}}$ tăng nhanh gấp khoảng đôi. Đến $N = 566$, một luật lũy thừa và một đường cong chững lại khớp dữ liệu như nhau.
9. **Phần nào của quy tắc đội quan trọng** (mục 3.9): riêng công tắc gom/lùa của bài báo đã đưa một đội chó độc lập đến $N = 200$; ở $N = 400$ cần đến tầng đội.
10. **Quá nhiều chó** (mục 3.10): khi chó giữ cách nhau 2 m, `outlier_rich` $N = 400$ thất bại từ $D = 9$ trở lên; chó dạng điểm không có thất bại như vậy đến 24.
11. **Độ gắn kết và tầm cảm nhận** (mục 3.11, 3.12): gắn kết yếu hơn làm $D_{\min}$ tăng nhanh hơn, về phía 0,5 của mục tiêu không gắn kết; tầm nhìn cục bộ tốn khoảng một chó ở $N = 200$, và chia sẻ những gì mọi chó thấy bù lại được.
12. **Một giới hạn của quy tắc lùa** (mục 3.13): trên $N \approx 1056$, điểm lùa của bài báo nằm ngoài khoảng cách mà cừu phản ứng với chó, và không đội nào đến 12 chó lùa được bầy. Khi giới hạn điểm lùa trong tầm, một bầy phân tán cần 3 chó ở $N = 800$, 5–9 ở 1131 và hơn 12 ở 1600.
13. **Mục tiêu không gắn kết** (mục 3.14): HerdSim cho lại ngưỡng mà Lama và di Bernardo công bố trong Bảng I của họ, và bản đồ của HerdSim có cùng hình dạng với bản đồ của họ. Khi thấy mọi thứ, đội nhỏ nhất tăng theo căn bậc hai của số mục tiêu (số mũ 0,52–0,53) theo cả thống kê của bài báo lẫn của HerdSim. Với bán kính cảm nhận 10, hai cách tách nhau gần ngưỡng: ở 144 mục tiêu, trung bình của bài báo đạt 0,99 với 11 người chăn, trong khi 17 đến 25 người chăn vẫn sót một mục tiêu trong khoảng một lượt trên mười.

---

## 1. Câu hỏi nghiên cứu

Các nghiên cứu trước về nhiều chó chăn khảo sát các đội có quy mô cố định hoặc các mục tiêu không tụ bầy (Pierson và Schwager 2015; Kubo et al. 2022; Lama và di Bernardo 2024). Nghiên cứu này hỏi đội tối thiểu tăng thế nào khi cừu tụ bầy, khi thời hạn gấp và khi bầy xuất phát phân tán. Nghiên cứu đầu có bảy câu hỏi:

- **RQ1 (quy mô bầy):** $D_{\min}$ tăng thế nào theo $N$ từ 25 đến 400, qua các bố cục và thời hạn? Độ gắn kết có làm thay đổi mức tăng $\sqrt{N}$ thấy ở mục tiêu không gắn kết không?
- **RQ2 (bố cục so với quy mô):** ở cùng một thời hạn, bố cục xuất phát hay $N$ làm $D_{\min}$ thay đổi nhiều hơn?
- **RQ3 (thời hạn):** $D_{\min}$ thay đổi thế nào từ 12 xuống 6 rồi 3 lần thời gian lùa, và thay đổi đó từ từ hay đột ngột?
- **RQ4 (quy tắc thành công):** quy tắc nghiêm ngặt và quy tắc 99% khác nhau thế nào, và vì sao các đội lớn thất bại dưới quy tắc nghiêm ngặt?
- **RQ5 (lựa chọn thiết lập):** kết quả có giữ nguyên khi đổi các lựa chọn không có giá trị thực tế không (vị trí thả chó, khoảng cách xuất phát, bán kính đích, tham số cừu, tốc độ chó)?
- **RQ6 (phối hợp):** các chó không phối hợp có đạt được $D_{\min}$ hữu hạn trên bầy lớn không?
- **RQ7 (đủ và quá nhiều):** từ đội $D_{\mathrm{sat}}$ nào thì thêm một chó không còn rút ngắn thời gian lùa, mỗi chó vượt quá tốn bao nhiêu, nó có thêm áp lực lên cừu không, và có đội nào làm nhiệm vụ thất bại không? (Đọc từ các lượt chạy 99% sẵn có.)

Các lượt chạy tiếp theo (quy tắc 99% xuyên suốt) thêm bảy câu hỏi:

- **RQ8 (lưới dày hơn):** trên chín quy mô bầy đến $N = 566$, $D_{\min}$ và $D_{\mathrm{sat}}$ tăng nhanh thế nào, và có phân biệt được tăng đều với một đường cong chững lại không?
- **RQ9 (các phần của quy tắc):** công tắc gom/lùa và tầng đội mỗi phần thêm gì, và một mô hình mà thời gian hoàn thành giảm theo $D$ (Kubo) bão hòa ra sao?
- **RQ10 (quá nhiều chó):** giữ bầy trong đích, hay chó chiếm chỗ, có làm thêm chó trở nên có hại không?
- **RQ11 (độ gắn kết):** mức tăng của $D_{\min}$ thay đổi thế nào theo độ mạnh của sự gắn kết?
- **RQ12 (chó thấy gì):** tầm cảm nhận giới hạn tốn bao nhiêu chó, và chia sẻ những gì các chó thấy có bù lại được không?
- **RQ13 (N lớn):** điều gì xảy ra trên quy mô mà bầy của mô hình còn có kích thước riêng?
- **RQ14 (mục tiêu không gắn kết):** HerdSim có cho lại kết quả của Lama và di Bernardo (2024) không, và quy luật căn bậc hai của họ có đúng dưới quy tắc tin cậy của HerdSim cũng như dưới thống kê của họ không?

---

## 2. Quy tắc quyết định

*(Bộ chạy thích ứng, các khoảng tin cậy và hạt giống dùng chung được mô tả ở [task_design_vi.md: lấy mẫu thích ứng](../experiments/task_design_vi.md#3-động-cơ-lấy-mẫu-thích-ứng-tuần-tự-adaptive-sequential-sampling).)*

### 2.1 Khi nào một đội là tin cậy
Một **ô** là một tổ hợp phương pháp, bố cục, $N$, thời hạn và $D$. Mỗi lượt chạy thành công hoặc thất bại. Với $n$ lượt và $k$ lượt thành công, $[L, U]$ là khoảng Clopper–Pearson hai phía 99% chính xác cho tỷ lệ thành công thật $p$:

$$
L = B\left(\frac{\alpha}{2}, k, n - k + 1\right), \quad U = B\left(1 - \frac{\alpha}{2}, k + 1, n - k\right)
$$

trong đó $B(q, a, b)$ là phân vị $q$ của phân phối Beta với tham số $a$ và $b$, $\alpha = 0{,}01$, và $n$ từ 10 đến 200 lượt mỗi ô.

Với ngưỡng $\theta = 0{,}90$:
- **Tin cậy:** $L \ge 0{,}90$. Cần ít nhất 51 lượt thành công liên tiếp không thất bại, tức 60 lượt theo lô 10.
- **Không tin cậy:** $U < 0{,}90$. Thường được quyết định sau 10 đến 20 lượt, và ô không nhận thêm lượt nào.
- **Chưa quyết định:** $L < 0{,}90 \le U$. Ô nhận thêm một lô 10 lượt, đến tối đa 200.

Với một đường cong các số chó đã thử ở cùng phương pháp, bố cục, $N$ và thời hạn:

$$
D_{\min} = \min \lbrace D \mid \text{ô } D \text{ tin cậy} \rbrace, \qquad
D_{\min,\mathrm{low}} = \min \lbrace D \mid U(D) \ge \theta \rbrace
$$

Các bảng ghi $D_{\min}$ theo bốn dạng:
- **Một giá trị (`3`):** mọi $D$ nhỏ hơn đều không tin cậy.
- **Một khoảng (`3-8`):** $D = 8$ tin cậy nhưng một $D$ nhỏ hơn từ 3 trở lên vẫn chưa quyết định ở 200 lượt.
- **Một cận dưới (`[5]`):** chưa $D$ nào tin cậy, và $D_{\min}$ ít nhất là 5.
- **`none`:** mọi $D$ đã thử đến đỉnh lưới (24 ở các lượt chạy chính) đều không tin cậy.

### 2.2 Các giao thức
Nghiên cứu đầu có 23 giao thức (164.740 lượt, 20 worker, không lỗi):
- **Lưới chính (6 lượt chạy):** 5 quy mô bầy, 4 bố cục và 3 thời hạn, mỗi thứ dưới quy tắc nghiêm ngặt và quy tắc 99%.
- **Đối chứng FAT (2 lượt chạy):** `dmin_fat` và `dmin_f99_fat` ở 6 lần thời gian lùa.
- **Mô hình Kubo (1 lượt chạy):** `dmin_kubo` trên bầy tập trung 25 đến 100.
- **Độ nhạy (14 lượt chạy):** ở 6 lần thời gian lùa, một cơ sở và sáu biến thể (thả chó từ một điểm, chó trên vòng tròn, khoảng cách xuất phát 15 và 60 thay vì 30, bán kính đích $1{,}5 R_f$, bộ tham số cừu khớp thực địa, tốc độ chó 1,15), mỗi thứ dưới cả hai quy tắc.

Phần tiếp theo thêm 14 giao thức và chạy tiếp ba lưới 99% (162.130 lượt, không lỗi, chỉ quy tắc 99%); chúng được liệt kê cùng RQ8–RQ13 và trong phụ lục. Hai giao thức của mô hình Lama và di Bernardo (40.280 lượt, không lỗi) trả lời RQ14.

---

## 3. Kết quả

### 3.1 RQ1: $D_{\min}$ tăng thế nào theo $N$?

1. **Bầy tập trung cần một chó.**  
   $D_{\min} = 1$ ở mọi quy mô bầy từ 25 đến 400 và mọi thời hạn. Thêm chó không rút ngắn thời gian lùa: trung vị thời gian hoàn thành giữ ở 1,44–1,74 lần thời gian lùa với mọi $D$ từ 1 đến 24.  
   *Vì sao:* trong mô hình Strömbom, một con cừu phản ứng với chó luôn đi với 1 m/s, và lực đẩy của nhiều chó được chuẩn hóa về độ lớn lực đẩy của một chó. Chó phía sau một bầy tập trung đổi hướng bầy nhưng không làm bầy nhanh hơn. Trong mô hình Kubo, nơi cừu tăng tốc khi bị đẩy mạnh hơn, thời gian hoàn thành có giảm theo $D$: từ 115 s với một chó xuống 29 s với mười chó ở $N = 100$ (Hình 2).

2. **Đến $N = 50$, một chó là đủ trên mọi bố cục.**  
   Trên các bố cục phân tán cũng vậy, $D_{\min} = 1$ với $N \le 50$ ở mọi thời hạn.  
   *Một lý do khả dĩ:* các bố cục phân tán được định cỡ theo khoảng cách gom $r_a N^{2/3}$, nên ở $N = 50$ con cừu xa nhất xuất phát cách tâm bầy nhiều nhất khoảng 45 m, trong phạm vi 65 m mà cừu phản ứng với chó. Một chó phía sau bầy đã tác động lên gần như mọi con cừu ngay từ đầu.

3. **Trên bầy phân tán, $D_{\min}$ tăng chậm hơn $N$.**  
   Với $N \ge 100$ trên các bố cục phân tán, $D_{\min}$ có tăng nhưng chậm: với thời hạn thong thả nó chỉ đạt 2 hoặc 3 chó ở $N = 400$. Trên thang log-log, độ dốc là **0,20 đến 0,42** ở 12 lần thời gian lùa, dưới mức 0,5 mà Lama và di Bernardo (2024) công bố cho mục tiêu không gắn kết.

Bảng 1 cho $D_{\min}$ ở mọi ô chính (nghiêm ngặt / 99%):

| Thời hạn | Bố cục | $N = 25$ | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **12&times;** | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| **12&times;** | `wide` | 1 / 1 | 1 / 1 | 1 / 1 | 2 / 1–2 | 3 / 2 |
| **12&times;** | `split` | 1 / 1 | 1 / 1 | 1 / 1 | 1–2 / 1 | 3 / 2 |
| **12&times;** | `outlier_rich` | 1 / 1 | 1 / 1 | 1–3 / 1–2 | 2 / 2 | 3 / 2 |
| **6&times;** | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| **6&times;** | `wide` | 1 / 1 | 1 / 1 | 1 / 1 | 3 / 2 | [9] / 2–3 |
| **6&times;** | `split` | 1 / 1 | 1 / 1 | 1 / 1 | none / [1] | none / [5] |
| **6&times;** | `outlier_rich` | 1 / 1 | 1 / 1 | 3 / 2 | [12] / 2–3 | none / 3 |
| **3&times;** | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| **3&times;** | `wide` | 1 / 1 | 1 / 1 | 3 / 2 | none / 3 | none / 5–6 |
| **3&times;** | `split` | 1 / 1 | 1 / 1 | 1 / 1 | none / none | none / none |
| **3&times;** | `outlier_rich` | 1 / 1 | 1 / 1 | 3–8 / 2 | none / 4–10 | none / [6] |

*Dữ liệu:* [results_tables.md: strict success](results_tables.md#d_min-by-layout-and-n-strict-success) (`dmin_m12`, `dmin_m6`, `dmin_m3`) và [results_tables.md: success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent) (`dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3`).

![D_min theo quy mô bầy N](../figures/fig20_dmin_vs_n.png)

**Hình 1: $D_{\min}$ theo quy mô bầy $N$ qua các thời hạn và bố cục.**  
Ba khung là ba thời hạn (12, 6 và 3 lần thời gian lùa), trên trục log-log. Đường liền với hình tròn là quy tắc nghiêm ngặt; đường đứt với hình vuông là quy tắc 99%. Thanh tô màu là các khoảng còn mở ở 200 lượt; tam giác rỗng là cận dưới; dấu chéo nghĩa là không có đội tin cậy đến 24. Bầy tập trung giữ ở 1; bầy phân tán tăng chậm ở thời hạn thong thả và nhanh hơn nhiều dưới quy tắc nghiêm ngặt khi $N \ge 100$.  
*Dữ liệu:* [results_tables.md: strict success](results_tables.md#d_min-by-layout-and-n-strict-success), [results_tables.md: success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent), và các quy mô thêm $N = 71, 141, 283, 566$.

![Thời gian hoàn thành trên bầy tập trung](../figures/fig31_compact.png)

**Hình 2: Thời gian hoàn thành theo quy mô đội trên bầy tập trung, cừu Strömbom so với cừu Kubo.**  
*(Trái)* Cừu Strömbom với quy tắc đội `strombom_multi` ($N = 25$ đến 400): thời gian hoàn thành phẳng theo $D$, vì một con cừu đang phản ứng đi với 1 m/s bất kể chó làm gì.  
*(Phải)* Cừu Kubo ($N = 25, 50, 100$): cừu tăng tốc khi bị đẩy mạnh hơn, đến 5 m/s, nên nhiều chó xong sớm hơn: từ 115 s với một chó xuống 29 s với mười chó ở $N = 100$.  
*Dữ liệu:* các lượt thành công trên bầy tập trung trong `results/dmin_m6` và `results/dmin_kubo`; $D_{\min}$ của Kubo trong [results_tables.md: Kubo (compact, strict)](results_tables.md#kubo-compact-strict).

Bảng 2 cho độ dốc của $\log_2 D_{\min}$ theo $\log_2 N$:

| Quy tắc | Thời hạn | `wide` | `split` | `outlier_rich` |
| :--- | :---: | :---: | :---: | :---: |
| **Nghiêm ngặt** | $12\times$ | 0,42 | 0,32 đến 0,42 | 0,42 |
| **Nghiêm ngặt** | $6\times$ | 0,48 ($N \le 200$) | phẳng ($N \le 100$) | 0,79 ($N \le 100$) |
| **Nghiêm ngặt** | $3\times$ | 0,79 ($N \le 100$) | phẳng ($N \le 100$) | 0,79 đến 1,50 ($N \le 100$) |
| **99%** | $12\times$ | 0,20 đến 0,30 | 0,20 | 0,30 |
| **99%** | $6\times$ | 0,30 đến 0,42 | phẳng ($N \le 100$) | 0,42 đến 0,48 |
| **99%** | $3\times$ | 0,62 đến 0,68 | phẳng ($N \le 100$) | 0,70 đến 1,10 ($N \le 200$) |

Một khoảng là tập các độ dốc mà các khoảng $D_{\min}$ cho phép; "$N \le 100$" nghĩa là các quy mô lớn hơn chưa có $D_{\min}$ được quyết định.  
*Dữ liệu:* [results_tables.md: Growth with N, strict](results_tables.md#growth-with-n-strict) và [results_tables.md: Growth with N, 99 percent](results_tables.md#growth-with-n-99-percent).

**Điều gì quyết định độ dốc.**
1. **Độ gắn kết giữ nó thấp.** Với mục tiêu không gắn kết, Lama và di Bernardo công bố độ dốc 0,5. Với bầy Strömbom ở thời hạn thong thả, nó là 0,20 đến 0,30 dưới quy tắc 99%. Mỗi con cừu bị hút về cả bầy ($c = 1{,}05$, cả $N - 1$ hàng xóm), nên con cừu lạc mà chó lùa quay lại sẽ tự đi về bầy, và chó không phải đi bắt từng con.
2. **Thời hạn gấp làm nó tăng.** Ở 3 lần thời gian lùa, độ dốc tăng lên 0,62–1,50. Không đủ thời gian để một chó đưa từng con lạc về lần lượt, nên cả đội phải làm việc ở nhiều phía của bầy cùng lúc.

---

### 3.2 RQ2: Bố cục hay quy mô bầy làm $D_{\min}$ thay đổi nhiều hơn?

Người định cỡ một đội chó hay robot sẽ muốn biết nên nhìn trước vào số con vật hay vào mức độ phân tán của chúng.

Để so một yếu tố dạng số ($N$) với một yếu tố dạng loại (bố cục), chúng tôi đo cả hai bằng **số lần gấp đôi** của $D_{\min}$:

$$
\text{độ trải (lần gấp đôi)} = \log_2 \left( \frac{D_{\min} \text{ lớn nhất}}{D_{\min} \text{ nhỏ nhất}} \right)
$$

Vậy đi từ 1 chó lên 2 là một lần gấp đôi, từ 1 lên 3 là 1,58, và không đổi là 0. Độ trải theo bố cục được lấy ở từng $N$ rồi lấy trung bình qua các $N$; độ trải theo $N$ được lấy ở từng bố cục rồi lấy trung bình qua các bố cục. Một khoảng được tính tại trung điểm nhân của nó, và các đường cong không có $D$ tin cậy bị bỏ ra.

Bảng 3:

| Quy tắc | Thời hạn | Độ trải theo bố cục ($N$ cố định) | Độ trải theo $N$ (bố cục cố định) |
| :--- | :---: | :---: | :---: |
| **Nghiêm ngặt** | $12\times$ | 0,68 | 1,19 |
| **Nghiêm ngặt** | $6\times$ | 1,67 | 1,69 |
| **Nghiêm ngặt** | $3\times$ | 0,76 | 0,97 |
| **99%** | $12\times$ | 0,50 | 0,75 |
| **99%** | $6\times$ | 0,92 | 1,30 |
| **99%** | $3\times$ | 1,25 | 1,28 |

*Dữ liệu:* tính từ các tóm tắt lần gấp đôi trong [Growth with N, strict](results_tables.md#growth-with-n-strict) và [Growth with N, 99 percent](results_tables.md#growth-with-n-99-percent).

**Bảng cho thấy gì.**
1. **Quy mô bầy làm $D_{\min}$ thay đổi nhiều hơn một chút.** Ở mọi hàng, độ trải theo $N$ ít nhất bằng độ trải theo bố cục; ở thời hạn 6 lần nghiêm ngặt và 3 lần 99%, hai giá trị gần bằng nhau.
2. **Tác động của bố cục chủ yếu là tập trung so với phân tán.** Bầy tập trung giữ $D_{\min} = 1$ ở mọi nơi. Dưới quy tắc 99% ở 12 lần thời gian lùa, `wide` và `outlier_rich` hiếm khi khác nhau quá một chó. Dưới quy tắc nghiêm ngặt ở 6 lần, chúng khác nhau nhiều (3 so với [12] ở $N = 200$), và `split` có thể thất bại hẳn ở nơi hai bố cục kia có $D_{\min}$.

---

### 3.3 RQ3: Thời hạn làm $D_{\min}$ thay đổi thế nào?

1. **Thay đổi đột ngột, không từ từ.**  
   Dưới quy tắc 99% trên `wide` và `outlier_rich`, đi từ 6 lên 12 lần thời gian lùa tiết kiệm nhiều nhất một chó. Đi từ 6 xuống 3 lần tốn hơn nhiều: trên `wide` $N = 400$, $D_{\min}$ từ 2–3 lên 5–6, và trên `split` $N \ge 200$ không đội nào đến 24 là tin cậy.

2. **Vì sao.**  
   Cừu đi 1 m/s và chó chạy 1,5 m/s. Với 12 lần thời gian lùa, có đủ thời gian để một chó đưa từng con lạc về trước khi lùa cả bầy. Với 3 lần, trình tự đó không còn vừa, nên nhiều chó phải làm việc ở các phía khác nhau của bầy cùng lúc.

![Tác động của thời hạn lên đường cong thành công](../figures/fig29_deadline.png)

**Hình 3: Tỷ lệ thành công theo quy mô đội ở ba thời hạn.**  
*(Trái và giữa)* Tỷ lệ thành công với khoảng Clopper–Pearson 99% theo $D$ trên `wide` $N = 400$ (trái) và `outlier_rich` $N = 200$ (giữa), ở 12 (xanh nhạt), 6 (xanh vừa) và 3 (xanh đậm) lần thời gian lùa; đường chấm là $\theta = 0{,}90$.  
*(Phải)* $D_{\min}$ theo thời hạn cho `wide` và `outlier_rich` ở $N = 200$ (liền, hình tròn) và $N = 400$ (đứt, hình vuông); điểm rỗng là cận dưới. Thời hạn gấp hơn đẩy các đường về phía đội lớn hơn, và bước từ 6 xuống 3 lớn hơn nhiều so với từ 12 xuống 6.  
*Dữ liệu:* `results/dmin_f99_m12`, `dmin_f99_m6` và `dmin_f99_m3`; giá trị trong [results_tables.md: D_min by layout and N, success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent).

---

### 3.4 RQ4: Quy tắc thành công và con cừu cuối cùng

1. **Quy tắc 99% không bao giờ cần nhiều chó hơn.**  
   Ở cả 34 ô phân tán mà cả hai quy tắc đều có đội tin cậy, quy tắc 99% cần bằng hoặc ít chó hơn. Ở những ô cả hai đều đã quyết định, nó tiết kiệm đúng một chó (từ 3 xuống 2 chẳng hạn); trên `outlier_rich` $N = 100$ ở 3 lần thời gian lùa, $D_{\min}$ đi từ khoảng 3–8 xuống 2. Sáu ô bầy lớn thất bại dưới quy tắc nghiêm ngặt (bốn `none`, hai còn mở ở 200 lượt) có đội tin cậy dưới quy tắc 99% (hai đã quyết định, bốn khoảng hẹp).

2. **Vì sao đội lớn thất bại dưới quy tắc nghiêm ngặt.**  
   Trong **97% số lượt thất bại nghiêm ngặt** với 6 chó trở lên ở lượt chạy cơ sở của phần độ nhạy (`dmin_s_base`; 91% ở `dmin_m6`), 99% bầy đã từng ở trong đích trước thời hạn. Một hai con cừu cuối cùng quyết định lượt chạy. Trong một lượt mẫu (`wide` $N = 400$, 16 chó, hạt giống 2), các chó đuổi theo con lạc cuối cùng, đứng vào giữa bầy và đích, và lùa bầy đã vào đích ra ngoài trở lại, hai lần (Hình 5).

3. **Chó chậm hơn tránh được điều đó.**  
   Với chó 1,15 m/s thay vì 1,5 (`dmin_s_dogspeed`), $D_{\min}$ nghiêm ngặt trên `outlier_rich` $N = 400$ giảm từ không có trên lưới xuống 6, và trên `wide` $N = 400$ từ [9] xuống 5. Vậy những thất bại nghiêm ngặt này đến từ những gì xảy ra ở đích, không phải từ một đội quá nhỏ để gom bầy.

![Thành công nghiêm ngặt so với 99%](../figures/fig30_strict_vs_99.png)

**Hình 4: Thành công nghiêm ngặt so với 99%, từng ô, trên cùng các hạt giống.**  
Mỗi khung một thời hạn (12, 6, 3), các bố cục phân tán ở $N \ge 100$ (80, 57 và 33 ô chung có ít nhất 20 hạt giống). Trục hoành: tỷ lệ thành công nghiêm ngặt; trục tung: tỷ lệ thành công 99%; đường chéo là $y = x$. Vùng tô ở góc trên trái chứa 40 ô (31 ở $N \ge 200$) tin cậy dưới quy tắc 99% nhưng không dưới quy tắc nghiêm ngặt. Ở đó, con cừu cuối cùng có vào được hay không quyết định kết quả nghiêm ngặt.  
*Dữ liệu:* `results/dmin_m12`, `dmin_m6` và `dmin_m3`; giá trị trong [results_tables.md: strict success](results_tables.md#d_min-by-layout-and-n-strict-success) và [results_tables.md: success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent).

![Con cừu cuối cùng](../figures/fig22_straggler.png)

**Hình 5: Con cừu cuối cùng quyết định.**  
*(Trái)* Tỷ lệ các lượt có 6 chó trở lên mà mọi con cừu đều vào (xanh đậm), mà 99% số cừu đã ở trong đích tại một thời điểm nào đó (gạch chéo), và mà mọi con cừu đều vào khi chó chậm hơn (cam). Với chó 1,5 m/s, hai cột đầu chênh nhau đến khoảng 30 điểm; với chó 1,15 m/s, gần như mọi lượt đưa được mọi con cừu vào.  
*(Phải)* Một lượt chạy (`wide` $N = 400$, 16 chó, hạt giống 2): trên, khoảng cách từ tâm bầy đến đích; dưới, số cừu ngoài đích (thang symlog). Chó nhanh (xanh) đưa 399 con vào, rồi lùa bầy ra ngoài hai lần khi đuổi con cuối cùng. Chó chậm hơn (cam) xong trong một lượt.  
*Dữ liệu:* `results/dmin_s_base` và `results/dmin_s_dogspeed`; giá trị trong [results_tables.md: Sensitivity, strict: base / variant](results_tables.md#sensitivity-strict-base--variant).

---

### 3.5 RQ5: Kết quả nào giữ nguyên khi đổi thiết lập?

14 giao thức độ nhạy ở 6 lần thời gian lùa mỗi lần đổi một lựa chọn thiết lập.

1. **Dưới quy tắc 99%, $D_{\min}$ hầu như không đổi.**  
   Thả chó từ một điểm hoặc từ vòng tròn, đổi khoảng cách xuất phát (15, 30, 60 m), cho chó chậm hơn (1,15 m/s) hay dùng bộ tham số cừu khớp thực địa làm $D_{\min}$ thay đổi nhiều nhất khoảng một chó. Thay đổi lớn nhất là bộ cừu khớp thực địa trên `outlier_rich` $N = 200$, từ 2–3 xuống 1.

2. **Dưới quy tắc nghiêm ngặt, nó thay đổi nhiều.**  
   Cùng những thay đổi đó thường biến một $D_{\min}$ hữu hạn thành "không có trên lưới" (chẳng hạn `wide` $N = 200$ từ 3 thành none với bộ cừu khớp thực địa, hoặc thành cận dưới [3] với khoảng cách 15). Thay đổi nhỏ ở vị trí xuất phát của chó làm thay đổi cách con cừu cuối cùng đi vào.

3. **Kích thước đích là thiết lập duy nhất có tác động dưới cả hai quy tắc.**  
   Với bán kính đích $1{,}5 R_f$ thay vì $1{,}9 R_f$, $D_{\min}$ tăng dưới cả hai quy tắc: dưới quy tắc 99%, `wide` $N = 400$ từ 2–3 lên 5–6 chó, và `outlier_rich` $N = 400$ từ 3 thành none. Một bầy đã ổn định chỉ vừa khít trong đích nhỏ hơn.

![Bản đồ nhiệt độ nhạy](../figures/fig24_sensitivity.png)

**Hình 6: $D_{\min}$ cho từng thay đổi thiết lập ở 6 lần thời gian lùa.**  
Nửa trên: quy tắc nghiêm ngặt; nửa dưới: quy tắc 99%. Các hàng là các thay đổi: vị trí thả chó (`handler`, `ring`), khoảng cách xuất phát (15, 60), bán kính đích $1{,}5 R_f$, tốc độ chó 1,15 và bộ cừu khớp thực địa. Các cột là bố cục và quy mô bầy ($N = 100, 200, 400$). Màu thể hiện $D_{\min}$; ô gạch ghi "none" không có đội tin cậy. Dưới quy tắc 99%, phần lớn các hàng khớp cơ sở trong vòng một chó; dưới quy tắc nghiêm ngặt, nhiều hàng thì không.  
*Dữ liệu:* [results_tables.md: Sensitivity, strict: base / variant](results_tables.md#sensitivity-strict-base--variant) và [results_tables.md: Sensitivity, 99 percent: base / variant](results_tables.md#sensitivity-99-percent-base--variant).

---

### 3.6 RQ6: Chó không có quy tắc đội có đạt $D_{\min}$ hữu hạn không?

FAT (nhắm con xa nhất) là một đối chứng không phối hợp: mỗi chó đứng sau con cừu xa đích nhất.

1. **FAT thất bại trên bầy lớn.**  
   FAT tin cậy trên bầy nhỏ ($N \le 100$) nhưng không có đội tin cậy nào ở $N \ge 200$ trên bất kỳ bố cục phân tán nào, và cũng không có trên bầy tập trung $N = 400$, nơi quy tắc đội chỉ cần một chó. Thêm chó không giúp gì.

2. **Vì sao.**  
   Mọi chó thấy mọi con cừu và chọn theo cùng một quy tắc, nên cả $D$ chó đuổi cùng một con cừu. Chúng dồn cục: ở $N \ge 200$, trung vị tỷ lệ chó có một chó khác trong vòng 2 m là 0,86 trên `compact` và 0,79 trên `split` (0,46 trên `wide`, 0,30 trên `outlier_rich`). Một đội FAT lớn hơn chỉ là một đám đông lớn hơn sau một con cừu trong khi phần còn lại của bầy tản ra.  
   Các chó chăn độc lập ở mục 3.9 cũng không có tầng đội, nhưng chúng giữ công tắc gom/lùa của Strömbom, và đạt $D_{\min}$ hữu hạn đến $N = 200$. FAT thất bại vì nó không có cả tầng đội lẫn công tắc.

Bảng 5 so FAT với `strombom_multi` ở 6 lần thời gian lùa (FAT nghiêm ngặt / 99%, `strombom_multi` trong ngoặc):

| Bố cục | $N = 25$ | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `compact` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / [12] (1 / 1) |
| `wide` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / none (3 / 2) | none / none ([9] / 2–3) |
| `split` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / none (none / [1]) | none / none (none / [5]) |
| `outlier_rich` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 2 / 2 (3 / 2) | none / none ([12] / 2–3) | none / none (none / 3) |

*Dữ liệu:* [results_tables.md: FAT dog rule, deadline 6](results_tables.md#fat-dog-rule-deadline-6-strict-then-99-percent) (`dmin_fat`, `dmin_f99_fat`); `strombom_multi` trong [results_tables.md: strict success](results_tables.md#d_min-by-layout-and-n-strict-success) và [results_tables.md: success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent).

![FAT so với quy tắc đội](../figures/fig26_fat.png)

**Hình 7: Tỷ lệ thành công theo quy mô đội cho `strombom_multi` (xanh) và FAT (cam) ở 6 lần thời gian lùa.**  
Năm khung: `compact` $N = 400$, `wide` $N = 200$ và 400, `outlier_rich` $N = 200$, và `split` $N = 200$. Đường liền: quy tắc nghiêm ngặt; đứt: quy tắc 99%; chấm: $\theta = 0{,}90$. Quá hai chó, FAT ở dưới khoảng 0,55, trong khi `strombom_multi` trở nên tin cậy trên `wide` và `outlier_rich`.  
*Dữ liệu:* `results/dmin_fat`, `dmin_f99_fat`, `dmin_m6` và `dmin_f99_m6`.

---

### 3.7 RQ7: Vượt quá $D_{\min}$: đủ chó, chi phí, và áp lực lên bầy

Biết đội tin cậy nhỏ nhất vẫn để lại những câu hỏi thực tế. Thêm chó có lùa nhanh hơn không? Mỗi chó thêm tốn bao nhiêu? Thêm chó có làm cừu căng thẳng hơn không? Chúng tôi đọc các câu trả lời từ các lượt chạy 99% (11 giao thức), và chạy lại 164 lượt đã lưu để đo thời gian mỗi con cừu chạy trốn (mọi lượt chạy lại đều cho đúng lượt đã lưu).

#### 1. Khi nào thêm chó không còn giúp ($D_{\mathrm{sat}}$)
$D_{\mathrm{sat}}$ là đội tin cậy nhỏ nhất mà không đội tin cậy lớn hơn nào nhanh hơn.
- **Bầy tập trung và $N \le 50$:** $D_{\mathrm{sat}} = 1$ (trừ `outlier_rich` $N = 50$, khoảng 1–24). Một chó đã giữ bầy đi với 1 m/s.
- **Bầy phân tán ở 6 lần thời gian lùa:** $D_{\mathrm{sat}}$ là 2 đến 6 ở $N = 100$ đến 400 (`outlier_rich` $N = 100$: 3; `wide` $N = 400$: 5).
- Sau các lượt chạy bổ sung thời gian hoàn thành (mục 3.8), $D_{\mathrm{sat}}$ trên `wide` là 1, 1, 1, 2, 3, 3, 4, 5 từ $N = 25$ đến 400.

#### 2. Chó vượt $D_{\mathrm{sat}}$ tốn bao nhiêu
- Ở cả 189 ô tin cậy trên một $D_{\mathrm{sat}}$ đã quyết định ở 6 lần thời gian lùa, thời gian hoàn thành bằng 0,96 đến 1,01 lần thời gian tại $D_{\mathrm{sat}}$: nhanh hơn nhiều nhất 4%, đôi khi chậm hơn 1%.
- Thời gian chó ($D$ nhân thời gian hoàn thành) tăng theo $D / D_{\mathrm{sat}}$. Trên một bầy tập trung 50 con, 24 chó mất đúng 154 s như một chó, với thời gian chó gấp 24 lần.

Bảng 6 so gấp đôi $D_{\mathrm{sat}}$ và $D = 24$ với ô $D_{\mathrm{sat}}$ (bầy phân tán, 6 lần thời gian lùa):

| Bố cục, $N$ | $D_{\mathrm{sat}}$ | Tại $2 D_{\mathrm{sat}}$: thời gian hoàn thành / thời gian chó | Tại $D = 24$: thời gian hoàn thành / thời gian chó |
| :--- | :---: | :---: | :---: |
| `wide`, $N = 200$ | 3 | 0,97 / 1,94 | 0,96 / 7,70 |
| `wide`, $N = 400$ | 5 | 0,97 / 2,32 (tại $D = 12$) | 0,96 / 4,61 |
| `outlier_rich`, $N = 100$ | 3 | 0,99 / 1,98 | 0,98 / 7,85 |
| `outlier_rich`, $N = 400$ | 6–24 | 0,96 / 1,91 | 0,94 / 3,74 |
| `split`, $N = 100$ | 4 | 0,99 / 1,98 | 0,99 / 5,91 |

Tại $D = 24$, việc lùa nhanh hơn 1% đến 6% so với tại $D_{\mathrm{sat}}$, với thời gian chó gấp 3,7 đến 7,9 lần.  
*Dữ liệu:* [results_tables.md: Effort, dmin_f99_m6](results_tables.md#effort-dmin_f99_m6-cost-of-dogs-beyond-d_sat-relative-to-the-d_sat-cell-1) và [results_tables.md: D_sat, dmin_f99_m6](results_tables.md#d_sat-dmin_f99_m6-d_sat-1).

#### 3. Áp lực lên cừu
Một con cừu chạy trốn khi có chó trong vòng 65 m ($r_s$). Các lượt chạy lại đo khoảng thời gian đó.
- **Mỗi con cừu chạy trốn ít hơn, cho đến $D_{\mathrm{sat}}$.** Nhiều chó gom bầy sớm hơn, nên lượt lùa ngắn hơn. Trên `wide` $N = 400$, trung vị thời gian chạy trốn mỗi con giảm từ 485 s ở $D = 3$ xuống 359 s ở $D = 6$, rồi giữ ở đó (361 s ở $D = 12$).
- **Nhiều cừu chạy trốn cùng lúc hơn.** Một đội lớn hơn trải trên một vòng cung rộng hơn: trung vị tỷ lệ bầy đang chạy trốn tại một thời điểm tăng từ 68% ở $D = 3$ lên 84% ở $D = 12$. Vì lượt lùa xong sớm hơn, tổng thời gian mỗi con cừu chạy trốn không tăng.
- **Chó không áp sát cừu.** Thời gian một con cừu ở trong vòng 6 m ($3 r_a$, khoảng cách dừng của chó) quanh một chó dưới 1,3 s mỗi con (trung vị) ở mọi quy mô đội.

#### 4. Không quy mô đội nào làm nhiệm vụ thất bại
Dưới quy tắc 99%, trên năm quy mô bầy ban đầu và đến 24 chó, không đường cong nào trở lại không tin cậy sau khi đã tin cậy. Vậy chó dạng điểm không gây thất bại do quá đông. Trên lưới dày hơn có một chỗ trũng (`split` $N = 141$, $D = 4$, thành công 0,80). Thêm chó có làm chậm một số bầy: trên `split` $N = 400$ ở 12 lần thời gian lùa, trung vị thời gian hoàn thành là 950–1040 s với $D \ge 9$ so với 839 s ở $D = 5$, dù nhiệm vụ vẫn thành công.

![Chi phí của chó vượt D_sat](../figures/fig33_effort.png)

**Hình 8: Chi phí của chó vượt $D_{\mathrm{sat}}$ (6 lần thời gian lùa, quy tắc 99%).**  
*(Trái)* Thời gian hoàn thành so với ô $D_{\mathrm{sat}}$ theo $D / D_{\mathrm{sat}}$ (thang log). Mọi đường đều nằm trong 0,96 đến 1,01.  
*(Phải)* Thời gian chó ($D$ nhân thời gian hoàn thành) so với ô $D_{\mathrm{sat}}$; các đường đi theo đường chéo $y = x$, nên thời gian chó tăng tỷ lệ với đội.  
*Dữ liệu:* [results_tables.md: Effort, dmin_f99_m6](results_tables.md#effort-dmin_f99_m6-cost-of-dogs-beyond-d_sat-relative-to-the-d_sat-cell-1).

![Áp lực lên bầy](../figures/fig34_pressure.png)

**Hình 9: Thời gian cừu chạy trốn theo quy mô đội (6 lần thời gian lùa, quy tắc 99%).**  
Trung vị trên các lượt thành công cho $N = 100$ (hình tròn, chấm) và $N = 400$ (hình vuông, liền).  
*(Trái)* Số giây mỗi con cừu có chó trong vòng 65 m. Từ $D_{\min}$ đến $D_{\mathrm{sat}}$ nó giảm, vì bầy được gom sớm hơn; vượt $D_{\mathrm{sat}}$ nó đi ngang.  
*(Phải)* Tỷ lệ bầy đang chạy trốn tại một thời điểm. Đội lớn hơn làm nhiều cừu chạy cùng lúc hơn, trong thời gian ngắn hơn.  
*Dữ liệu:* [results_tables.md: Pressure, dmin_f99_m6](results_tables.md#pressure-dmin_f99_m6-replay-of-12-stored-seeds-per-cell-every-replay-reproduced-its-stored-trial).

---

### 3.8 RQ8: Mức tăng theo $N$ trên lưới dày hơn, $D_{\mathrm{sat}}$, và hình dạng đường cong

Để xác định hình dạng của $D_{\min}(N)$, các lưới 99% ở 12 và 6 lần thời gian lùa được thêm bốn quy mô bầy: $N = 71, 141, 283$ (trung điểm trên thang log giữa 50 và 400) và $N = 566 = 400\sqrt{2}$.

**Vì sao các bước $\sqrt{2}$, và vì sao dừng ở 566.** Các bước $\sqrt{2}$ cho mọi quy mô cùng trọng số trong một phép khớp log-log. 566 là bước cuối như vậy dưới quy mô mà bầy của mô hình không còn ổn định: dưới khoảng 600, một bầy bị lùa ổn định về một bán kính $R_f(N)$ bất kể nó xuất phát lớn hay nhỏ. Ở $N = 630$, một bầy xuất phát lỏng vẫn lớn hơn 17% so với bầy xuất phát chặt, và ở 800 việc hiệu chỉnh thất bại.

1. **Các độ dốc hẹp lại.**  
   Trên chín quy mô, độ dốc của $D_{\min}$ theo $N$ là **0,27 đến 0,38** trên `wide` và **0,28 đến 0,38** trên `outlier_rich` ở 12 lần thời gian lùa, và **0,38 đến 0,61** ở 6 lần. Ở thời hạn thong thả nó vẫn dưới 0,5.

2. **$D_{\mathrm{sat}}$ tăng nhanh gấp khoảng đôi $D_{\min}$.**  
   Trên `wide` ở 6 lần thời gian lùa, $D_{\mathrm{sat}}$ là 1, 1, 1, 2, 3, 3, 4, 5 chó từ $N = 25$ đến 400, và 7–24 ở 566 (độ dốc **0,70 đến 0,91**). Khoảng cách giữa đội tin cậy và đội nhanh nhất rộng ra khi bầy lớn lên.

3. **Tăng đều và đường cong chững lại khớp như nhau.**  
   Đến $N = 566$, dữ liệu khớp một luật lũy thừa $D = c N^b$ và một đường cong bão hòa $D = 1 + (D_\infty - 1) N / (N + K)$ như nhau (log odds 0,0). Ở $N = 1600$, các đường cong khớp được cho phép 1,5 đến 6,7 chó ở 12 lần thời gian lùa (3,1 đến 10,4 ở 6 lần). Để phân biệt chúng cần bầy lớn hơn, mà mô hình không hiệu chỉnh được (mục 3.13).

Bảng 7, chín quy mô bầy (quy tắc 99%):

| $N$ | 25 | 50 | 71 | 100 | 141 | 200 | 283 | 400 | 566 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `wide`, $12\times$ | 1 | 1 | 1 | 1 | 2 | 1–2 | 2 | 2 | 2–3 |
| `outlier_rich`, $12\times$ | 1 | 1 | 1 | 1–2 | 2 | 2 | 2 | 2 | 2–3 |
| `wide`, $6\times$ | 1 | 1 | 1 | 1 | 2 | 2 | 2–3 | 2–3 | 3–7 |
| `outlier_rich`, $6\times$ | 1 | 1 | 1 | 2 | 2 | 2–3 | 2–3 | 3 | 3–6 |
| $D_{\mathrm{sat}}$ `wide`, $6\times$ | 1 | 1 | 1 | 2 | 3 | 3 | 4 | 5 | 7–24 |

*Dữ liệu:* [results_tables.md: Finish-time top-up, densified N, independent shepherds, Kubo to D = 24, 99 percent](results_tables.md#finish-time-top-up-densified-n-independent-shepherds-kubo-to-d--24-99-percent).

![D_min trên chín quy mô và phạm vi của hai dạng đường cong](../figures/fig35_growth_fits.png)

**Hình 10: $D_{\min}$ trên chín quy mô bầy, và mỗi dạng đường cong có thể đi đến đâu.**  
Trái: 12 lần thời gian lùa; phải: 6 lần (log-log; `wide` hình tròn, `outlier_rich` hình vuông). Thanh là các khoảng; đường dọc đánh dấu giới hạn hiệu chỉnh ($N \approx 600$). Bên phải, các vùng tô cho thấy các luật lũy thừa (cạnh trên đứt) và các đường cong bão hòa (cạnh trên chấm) khớp dữ liệu có thể nằm ở đâu. Cả hai khớp đến $N = 566$.  
*Dữ liệu:* [results_tables.md: D_min, dmin_f99_m12](results_tables.md#d_min-dmin_f99_m12), [results_tables.md: D_min, dmin_f99_m6](results_tables.md#d_min-dmin_f99_m6), và [results_tables.md: fits dmin_f99_m12](results_tables.md#fits-dmin_f99_m12-d_minn-power-law-against-saturating-curve).

---

### 3.9 RQ9: Phần nào của quy tắc đội quan trọng?

FAT (mục 3.6) thiếu hai thứ mà quy tắc đội có: (1) công tắc của Strömbom giữa gom cừu lạc và lùa cả bầy, và (2) tầng đội, phân công chó cho các con lạc (phép gán Hungarian) và trải chó trên một vòng cung sau bầy theo thứ tự góc.

Để tách hai phần, `dmin_f99_indep` chạy một đội **chó chăn độc lập theo bài báo**: mỗi chó chạy quy tắc một chó của Strömbom trên cả bầy, không phân công, không vòng cung.

1. **Riêng công tắc đã đủ đến $N = 200$.**  
   Các chó chăn độc lập tin cậy trên mọi bố cục phân tán đến $N = 200$, nơi FAT thất bại: 2–3 chó trên `wide`, 3 trên `outlier_rich`. Ngay cả khi chúng đuổi cùng một con lạc, việc chuyển sang lùa khi bầy đã gom lại vẫn giữ bầy liền.

2. **Ở $N = 400$ cần đến tầng đội.**  
   Chó chăn độc lập không có đội tin cậy nào đến 24 chó ở $N = 400$. Quy tắc đội cần 2–3 chó trên `wide` và 3 trên `outlier_rich`. Không có phân công, các chó cứ đuổi theo cùng những con cừu trong khi các phần khác của một bầy lớn tản ra.

3. **Trong mô hình Kubo, thêm chó vẫn giúp, nhưng lợi ích giảm dần.**  
   Với cừu Kubo (`dmin_f99_kubo`), một chó là đủ trên bầy tập trung 25 đến 100. Khác cừu Strömbom, cừu Kubo đi nhanh hơn khi bị đẩy mạnh hơn (đến 5 m/s), nên thêm chó rút ngắn lượt lùa: ở $N = 100$, trung vị thời gian hoàn thành giảm từ 115 s với một chó xuống 29 s với mười chó, và 25 s với 24 chó. Mười chó đã cho 95% lợi ích của 24 chó.

Bảng 8 so ba quy tắc ở 6 lần thời gian lùa (quy tắc 99%):

| `strombom_multi` / `independent` / `fat` | $N = 200$ | $N = 400$ |
| :--- | :---: | :---: |
| `wide` | 2 / 2–3 / none | 2–3 / none / none |
| `outlier_rich` | 2–3 / 3 / none | 3 / none / none |
| `split` | [1] / 1–3 / none | [5] / none / none |

*Dữ liệu:* [results_tables.md: Methods at 99 percent, 6 drive times](results_tables.md#methods-at-99-percent-6-drive-times-team-rule-independent-paper-shepherds-fat) và [results_tables.md: Kubo, compact, D to 24](results_tables.md#kubo-compact-d-to-24-99-percent); thời gian hoàn thành của Kubo từ `results/dmin_f99_kubo`.

---

### 3.10 RQ10: Khi nào thêm chó gây hại? Giữ bầy, và chó chiếm chỗ

Khi lùa ngoài trời dưới quy tắc 99%, thêm chó dạng điểm chưa bao giờ làm nhiệm vụ thất bại. Hai giao thức thử những tình huống mà chó thêm có thể cản nhau:

1. **Giữ bầy (`dmin_f99_hold`):** một lượt chỉ thành công khi 99% bầy đã ở trong đích suốt một lần thời gian lùa. Trong lúc bầy ở trong đích, chó lùi ra $r_s + r_a = 67$ m sau con cừu xa nhất, để không con cừu nào phản ứng với chúng và bầy gặm cỏ.
2. **Chó chiếm chỗ (`dmin_f99_hold_spacing`):** cùng nhiệm vụ, nhưng không chó nào được đến gần chó khác dưới 2 m. Vòng cung sau bầy khi đó chỉ có chỗ cho một số chó nhất định, khoảng $D_{\mathrm{cap}} = 7, 9, 10, 11, 12$ ở $N = 25$ đến 400.

#### Kết quả

1. **Giữ bầy thất bại trên bầy nhỏ vì lý do hình học.**  
   Trên bầy lớn hơn ($N \ge 100$), giữ bầy thành công trên `wide` và `compact`, với $D_{\min}$ bằng lúc lùa ngoài trời hoặc thêm một (1, 2 và 3 chó trên `wide` ở $N = 100$, 200, 400).  
   Trên bầy nhỏ ($N \le 50$), không đội nào giữ được bầy. Đích ở đó chỉ có bán kính 12–14 m, trong khi chó phải lùi ra 67 m. Khi chó đi xa, cừu gặm cỏ lang thang ra khỏi cái đích nhỏ trước khi hết thời gian giữ. Thất bại đến từ kích thước đích, không phải từ việc thiếu chó.

2. **Chó chiếm chỗ làm chó thêm trở nên có hại trên `outlier_rich` $N = 400$.**  
   - Với 3 đến 6 chó, tỷ lệ thành công là 0,925–0,94, chưa quyết định.  
   - Từ $D = 9$ trở lên, mọi đội đến 24 đều được quyết định là không tin cậy: thành công 0,77 ở $D = 9$, 0,65 ở $D = 12$, 0,50 ở $D = 16$.  
   - *Một lý do khả dĩ:* vòng cung sau bầy chứa khoảng 12 chó cách nhau 2 m. Khi nhiều chó hơn thế, chúng đẩy nhau ra khỏi chỗ trên vòng cung và không thể rời vòng cung để bắt một con cừu tách ra.  
   - Trên `wide` và `compact`, những chó thừa không vừa vòng cung đứng phía sau mà không cản đường, và nhiệm vụ vẫn tin cậy đến 24 chó. Vậy thêm chó có gây hại hay không còn tùy bố cục, chứ không chỉ tùy khoảng chỗ mỗi chó chiếm.

![Giữ bầy với chó dạng điểm và chó cách nhau 2 m](../figures/fig36_spacing.png)

**Hình 11: Giữ bầy ở $N = 400$, chó dạng điểm so với chó giữ cách nhau 2 m.**  
Trái: `wide`; phải: `outlier_rich`; tỷ lệ thành công theo $D$ (thang log). Chấm xám: chó dạng điểm; liền xanh: chó cách nhau 2 m; dải cam: sức chứa vòng cung ($D_{\mathrm{cap}} \approx 10$–12); đường đứt: $\theta = 0{,}90$. Trên `wide`, các chó thừa đứng phía sau và thành công giữ nguyên; trên `outlier_rich`, nó giảm từ $D = 9$.  
*Dữ liệu:* [results_tables.md: D_min, dmin_f99_hold](results_tables.md#d_min-dmin_f99_hold) và [results_tables.md: D_min, dmin_f99_hold_spacing](results_tables.md#d_min-dmin_f99_hold_spacing).

---

### 3.11 RQ11: Độ gắn kết và mức tăng của $D_{\min}$

Lama và di Bernardo (2024) công bố rằng đội tăng theo $\sqrt{N}$ với các mục tiêu không tụ bầy. Để nối trường hợp của họ với bầy Strömbom, chúng tôi đổi độ gắn kết theo hai cách: (1) trọng số hút $c$, tăng từ 1,05 của bài báo lên 1,3, 1,6 và 2,0, và (2) số hàng xóm mỗi con cừu bị hút về, giảm từ cả $N - 1$ xuống một nửa bầy ($n = 0{,}5N$).

1. **Gắn kết mạnh hơn thay đổi ít.**  
   Với $c = 1{,}3$, 1,6 hay 2,0, độ dốc trên `wide` là 0,20, và $D_{\min}$ giảm nhiều nhất một chó ở mọi quy mô. Với $c = 1{,}05$ của bài báo và mỗi con cừu bị hút về cả bầy, bầy đã giữ liền; kéo nó chặt hơn không giúp gì cho chó lùa.

2. **Gắn kết yếu hơn làm $D_{\min}$ tăng nhanh hơn, về phía quy luật căn bậc hai.**  
   Với $n = 0{,}5N$, độ dốc trên `wide` thành **0,40 đến 0,70**, một khoảng chứa 0,5 của mục tiêu không gắn kết.  
   Trên `split`, bầy yếu hơn tách ra dưới một chó: $D_{\min}$ từ 1 lên 3–4 ở $N = 200$ và từ 2 lên 4–5 ở $N = 400$. Mức tăng chậm của $D_{\min}$ ở bầy Strömbom phụ thuộc vào việc mỗi con cừu bị hút về cả bầy.

Bảng 9, các mức gắn kết (`wide`, quy tắc 99%, 12 lần thời gian lùa):

| Độ gắn kết (`wide`, 99%, $12\times$) | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ | Độ dốc |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Yếu hơn ($n = 0{,}5N$)** | 1 | 1 | 2 | 2–4 | **0,40 đến 0,70** |
| **Bài báo ($c = 1{,}05$)** | 1 | 1 | 1–2 | 2 | **0,20 đến 0,30** |
| **Mạnh hơn ($c = 1{,}3; 1{,}6; 2{,}0$)** | 1 | 1 | 1 | 2 | **0,20** |

*Dữ liệu:* hàng bài báo từ [results_tables.md: dmin_f99_m12](results_tables.md#dmin_f99_m12) và [results_tables.md: Growth with N, 99 percent](results_tables.md#growth-with-n-99-percent); các lượt chạy gắn kết từ [results_tables.md: D_min, dmin_f99_c1.3](results_tables.md#d_min-dmin_f99_c13), [dmin_f99_c1.6](results_tables.md#d_min-dmin_f99_c16), [dmin_f99_c2.0](results_tables.md#d_min-dmin_f99_c20) và [dmin_f99_k05](results_tables.md#d_min-dmin_f99_k05); độ dốc từ [results_tables.md: dmin_f99_c1.3](results_tables.md#dmin_f99_c13), [dmin_f99_c1.6](results_tables.md#dmin_f99_c16), [dmin_f99_c2.0](results_tables.md#dmin_f99_c20) và [dmin_f99_k05](results_tables.md#dmin_f99_k05) (growth).

---

### 3.12 RQ12: Chó thấy gì, và chia sẻ điều đó

Chó, robot và drone thật không thấy cả cánh đồng. Ở đây mỗi chó chỉ thấy những con cừu trong một tầm cảm nhận (15, 30, 45, 65 hoặc 100 m), và các chó chia sẻ những gì chúng thấy theo một trong ba cách: không chia sẻ (`none`), chia sẻ với các chó trong tầm (`neighbour`), hoặc với cả đội (`shared`).

1. **Một tầm thực tế tốn khoảng một chó.**  
   Trên `wide` $N = 200$, chó thấy mọi thứ cần 2 con. Với tầm 30 đến 65 m chúng cần 3 (3–4 ở 45 m). Trên bầy 100 con trở xuống, tầm cảm nhận không tốn gì, vì cả bầy phân tán nằm gọn trong 65 m.

2. **Dưới 30 m chó mất dấu bầy.**  
   Với tầm 15 m trên `wide`, không đội nào đến 16 là tin cậy ở $N = 50$, và ở $N = 100$ cần ít nhất 6 chó. Khi tầm ngắn hơn khoảng cách giữa các con lạc, chó không còn thấy những con cừu ở rìa.

3. **Chia sẻ với cả đội lấy lại được một chó.**  
   Ở 65 m trên `wide` $N = 200$, chó không chia sẻ cần 3 con. Chia sẻ với cả đội đưa $D_{\min}$ về 2, như khi thấy mọi thứ. Chỉ chia sẻ với các chó trong tầm thì không giúp (vẫn 3): một chó ở xa cần biết về một con lạc mà nó không thấy. Trên `split` $N = 200$, chia sẻ cũng không giúp (3, so với [1] khi thấy mọi thứ).

![D_min theo tầm cảm nhận, và việc chia sẻ](../figures/fig37_view.png)

**Hình 12: $D_{\min}$ theo tầm cảm nhận, và tác dụng của chia sẻ.**  
Trái: $D_{\min}$ theo tầm cho `wide` (hình tròn) và `split` (hình vuông) ở $N = 100$ (nhạt) và $N = 200$; đường đứt đánh dấu 65 m, khoảng cách mà cừu phản ứng. Dưới 30 m, `wide` thất bại.  
Phải: tỷ lệ thành công theo $D$ trên `wide` $N = 200$ ở tầm 65 m: không chia sẻ (chấm xanh), chia sẻ với chó trong tầm (đứt xanh), chia sẻ với cả đội (liền xanh), và thấy mọi thứ (liền đen). Chia sẻ với cả đội bằng với thấy mọi thứ.  
*Dữ liệu:* [results_tables.md: Views: sensing range](results_tables.md#views-sensing-range-no-sharing-base-row--range-0-global) và [results_tables.md: Views: sharing at range 65](results_tables.md#views-sharing-at-range-65-beside-the-no-sharing-rows-of-dmin_f99_view_range).

---

### 3.13 RQ13: Bầy rất lớn và một giới hạn của quy tắc lùa

Chúng tôi chạy các bầy 800 đến 3200 con ở 12 lần thời gian lùa. Trên $N = 566$, bầy của mô hình không có kích thước ổn định, nên $R_f$ được đặt để giữ mật độ của bầy 566: $R_f(N) = R_f(566)\sqrt{N/566}$.

#### 1. Trên $N \approx 1056$, điểm lùa nằm ngoài tầm của cừu
Trong quy tắc của Strömbom, chó lùa nhắm tới một điểm sau tâm bầy, ở phía xa đích:
$$
\mathbf{P}_d = \mathrm{GCM} - r_a \sqrt{N} \, \hat{\mathbf{e}}_{\mathrm{GCM} \to \mathrm{đích}}
$$
với $r_a = 2$ m, nên chó đứng cách tâm $2\sqrt{N}$ m. Một con cừu chỉ phản ứng với chó trong vòng $r_s = 65$ m. Điểm lùa nằm ngoài tầm của mọi con cừu khi
$$
r_a \sqrt{N} > r_s \iff 2\sqrt{N} > 65 \iff N > 1056
$$
Trên quy mô đó, chó đứng ở nơi ít hoặc không con cừu nào phản ứng, và bầy không được lùa. Ở $N = 1131$, không đội nào đến 12 chó thành công trong bất kỳ lượt nào trong 10 lượt, trên cả `compact` lẫn `wide`.

#### 2. Giới hạn điểm lùa đưa bầy trở lại
Khi giới hạn khoảng lùa ở $r_s - r_a = 63$ m (`dmin_f99_big_cap`), một biến thể HerdSim của quy tắc bài báo:
- **Compact:** một chó lùa được bầy 800 và 1131, cần hai chó ở 1600. Ở 3200, mọi đội từ 3 đến 12 chó thành công trong cả 42 lượt đã chạy.
- **Wide:** 3 chó ở $N = 800$, 5–9 ở 1131 và hơn 12 ở 1600. Một bầy phân tán lớn cần nhiều chó để giữ các phía của nó lại với nhau.

Bảng 10, điểm lùa bị giới hạn (quy tắc 99%, 12 lần thời gian lùa):

| Giới hạn ở 63 m, 99%, $12\times$ | $N = 800$ | $N = 1131$ | $N = 1600$ | $N = 3200$ (một phần) |
| :--- | :---: | :---: | :---: | :---: |
| `compact` | 1 | 1 | 2 | 42 / 42 lượt thành công ở $D = 3$–12 ($D = 1, 2$ không chạy) |
| `wide` | 3 | 5–9 | none đến 12 | **none** (0 / 58 ở $D = 2$–12) |

*Dữ liệu:* [results_tables.md: dmin_f99_big_cap](results_tables.md#dmin_f99_big_cap); cột $N = 3200$ từ `results/dmin_f99_big_cap` (100 lượt, dừng sớm). Kết quả không giới hạn trong [results_tables.md: D_min, dmin_f99_big](results_tables.md#d_min-dmin_f99_big).

---

### 3.14 RQ14: Mục tiêu không gắn kết: quy luật căn bậc hai của Lama và di Bernardo (2024)

Để so bầy Strömbom với các mục tiêu không tụ bầy, chúng tôi chạy mô hình của Lama và di Bernardo (2024) trong HerdSim với phương pháp `lama` trên nhiệm vụ `gather` ([mô hình](../methods/models_vi.md#mô-hình-mục-tiêu-brownian-không-liên-kết-lama-2024), [nhiệm vụ](../experiments/task_design_vi.md#6-nhiệm-vụ-gom-lama-và-di-bernardo-2024)). Mỗi mục tiêu đi lang thang ngẫu nhiên và bị người chăn trong vòng $\lambda = 2{,}5$ đẩy ra xa; mỗi người chăn đuổi mục tiêu xa đích nhất trong số những mục tiêu nó cảm nhận được. Mục tiêu và người chăn xuất phát đều trên một hình tròn bán kính $R = 50$ quanh một đích bán kính $R/5$, và một lượt kéo dài tối đa 5000 s.

#### 1. Hai cách gọi một đội là đủ
Cùng các lượt chạy được đọc theo hai cách:
- **Thống kê của bài báo:** một đội là đủ khi tỷ lệ mục tiêu trong đích lúc kết thúc, lấy trung bình qua các lượt, ít nhất 0,99.
- **Quy tắc của HerdSim:** một đội là đủ khi tỷ lệ số lượt kết thúc với 99% mục tiêu trong đích ít nhất 0,90 với độ tin cậy 99%.

#### 2. Kết quả
1. **HerdSim cho lại kết quả của bài báo.**  
   Bài báo công bố bằng số một kết quả là ngưỡng trong Bảng I: với bán kính cảm nhận 10, đội nhỏ nhất chỉ theo quy luật căn bậc hai từ $\sqrt{N} = 8$, 9 và 11 trở lên, ứng với mức 90%, 95% và 99%. HerdSim cho 8, 9 và 12. Các kết quả còn lại của bài báo là bản đồ màu ([Hình 2](https://doi.org/10.1103/PhysRevResearch.6.L032012)). Đặt cạnh nhau (Hình 13), bản đồ của HerdSim và của bài báo có cùng hình dạng: với bán kính 10, khi ít mục tiêu thì không đội nào đến 25 đạt được, rồi có một ngưỡng rõ, và trên ngưỡng là một dải đội tăng theo căn bậc hai của số mục tiêu; khi thấy mọi thứ, dải đó kéo dài suốt cả khoảng. Có hai khác biệt nhỏ: với bán kính 10 và ít mục tiêu, HerdSim gom được ít hơn bài báo một chút, và đường 0,99 của HerdSim quay lên ở khoảng $\sqrt{N} = 12$, còn của bài báo ở khoảng 10 đến 11.

   ![Hình 2 của bài báo cạnh bản đồ của HerdSim](../figures/fig39_lama_maps.png)

   **Hình 13: Bản đồ của bài báo phía trên bản đồ của HerdSim.** Mỗi ô là tỷ lệ mục tiêu trong đích lúc kết thúc, lấy trung bình qua các lượt, cho một số mục tiêu (trục hoành, theo căn bậc hai) và một số người chăn (trục tung); đường trắng đánh dấu mức 0,99. Trái: thấy mọi thứ; phải: bán kính cảm nhận 10. Lưới của HerdSim dừng ở 400 mục tiêu ($\sqrt{N} = 20$), nên dải xám từ 21 đến 25 trên trục của bài báo không có dữ liệu. Phạm vi đã chạy đã chứa ngưỡng và đoạn tăng theo căn bậc hai phía trên ngưỡng, đủ để kiểm tra, nên năm quy mô lớn hơn không được chạy; chạy thêm sẽ làm thời gian chạy tăng gần gấp đôi. Lưới có 10 đến 200 lượt mỗi ô, bài báo có 50.  
   *Trên: Hình 2 của Lama và di Bernardo (2024), Phys. Rev. Research 6, L032012, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), đã cắt. Dưới: `lama_r50_inf` và `lama_r50`.*

2. **Khi thấy mọi thứ, cả hai cách đều cho quy luật căn bậc hai.**  
   Hai cách cho cùng đội nhỏ nhất ở gần như mọi quy mô (8 người chăn cho 100 mục tiêu, 13 cho 225, 17 cho 400). Số mũ khớp được là **0,52** (thống kê của bài báo) và **0,53** (quy tắc của HerdSim).

3. **Với bán kính cảm nhận 10, hai cách tách nhau gần ngưỡng.**  
   Với 81 mục tiêu trở xuống, không đội nào đến 25 người chăn là tin cậy; mọi thất bại ở đó kết thúc với các mục tiêu không người chăn nào thấy được.  
   Ngay trên ngưỡng, từ 100 đến 196 mục tiêu, hai cách tách nhau:
   - Ở 144 mục tiêu, 11 người chăn gom trung bình 99,2% mục tiêu, nên thống kê của bài báo chấp nhận. Nhưng chỉ 70% số lượt của họ kết thúc với 99% mục tiêu trong đích. Các lượt mất hai trên 144 mục tiêu (98,6%) trộn với các lượt không mất gì vẫn cho trung bình trên 0,99.
   - Quy tắc của HerdSim không chấp nhận 11 người chăn; $D_{\min}$ của nó là khoảng 17–25.
   - Một mức trung bình có thể che đi những lượt thất bại. Đếm từng lượt thì không, nên gần ngưỡng hai câu trả lời chênh nhau 6 đến 14 người chăn.

![Mô hình Lama và di Bernardo trong HerdSim](../figures/fig38_lama.png)

**Hình 14: Đội nhỏ nhất theo số mục tiêu trong mô hình của Lama và di Bernardo (2024).**  
Trái: bán kính cảm nhận 10 (vùng ngưỡng tô xám); phải: thấy mọi thứ. Hình vuông là đội của bài báo như thể hiện trên Hình 2 của bài báo; hình tròn là thống kê của bài báo áp dụng lên các lượt của HerdSim; hình thoi là $D_{\min}$ của HerdSim (thanh là khoảng, tam giác là cận dưới, dấu chéo là không có đội tin cậy đến 25). Khi thấy mọi thứ, hai thống kê trùng nhau. Gần ngưỡng ở bán kính 10, trung bình chấp nhận 11 người chăn ở 144 mục tiêu, trong khi quy tắc của HerdSim cần 17–25.  
*Dữ liệu:* [results_tables.md: Lama and di Bernardo (2024): gather task](results_tables.md#lama-and-di-bernardo-2024-gather-task).

---

## 4. Xem kỹ hơn: bố cục `split` và các số đo theo từng bước

### 4.1 Vì sao thêm chó không giúp trên `split`
Trên bầy `split` ở $N \ge 200$, thêm chó không làm tăng tỷ lệ thành công: ở 6 lần thời gian lùa dưới quy tắc 99%, nó nằm trong khoảng 0,60 đến 0,92 với mọi $D \ge 4$ (0,10–0,76 dưới quy tắc nghiêm ngặt), và ở 3 lần thời gian lùa nó giảm về gần không.

Chạy lại các lượt đã lưu (`cli/diagnostics/split_diagnostic.py`, 12 hạt giống mỗi ô, $N = 200$) chỉ ra hai nguyên nhân:

1. **Mọi chó đi gom dồn về một cụm ($D = 4$).**  
   Quy tắc đội phân công chó cho các con lạc theo tổng quãng đường đi ngắn nhất. Cách đó bỏ qua việc con lạc thuộc cụm nào, nên khi bầy tách thành nhiều cụm, cụm gần hơn hoặc tản hơn có thể lấy hết chó trong khi cụm khác trôi đi. Khi buộc các chó đi gom chọn những con lạc cách nhau ít nhất $f(N) = r_a N^{2/3}$, trung vị thời gian hoàn thành ở $D = 4$ giảm từ 631 s xuống 318 s (6 lần thời gian lùa).

2. **Nhiều chó đứng yên vì quy tắc dừng ($D \ge 4$).**  
   Chó của Strömbom dừng lại khi có con cừu nào trong vòng $3 r_a = 6$ m. Trên `wide` và `outlier_rich`, điều đó giữ 1% đến 7% số chó đứng yên. Trên `split`, khoảng 25% số chó đứng yên, bị giữ lại cạnh một cụm trên đường sang cụm khác. Khi rút khoảng cách dừng xuống $r_a = 2$ m, lượt lùa nhanh hơn 21–24% ở $D = 8$ và 16, và $D = 16$ thành công ở cả 12 hạt giống.  
   Ở 3 lần thời gian lùa, không thay đổi nào làm `split` trở nên tin cậy: đổi quy tắc của từng chó không giải quyết được việc một đội phải phục vụ nhiều cụm.

![Đường cong split và các số đo](../figures/fig23_split_curves.png)

**Hình 15: Tỷ lệ thành công trên bầy `split` theo quy mô đội (6 lần thời gian lùa).**  
Các khung cho `split` ở $N = 100$, 200 và 400, và `wide` ở $N = 400$ để so sánh, với khoảng Clopper–Pearson 99% theo $D$ (thang log). Hình tròn xanh: quy tắc nghiêm ngặt; hình vuông cam: quy tắc 99%; đường chấm: $\theta = 0{,}90$. Trên `wide` tỷ lệ thành công tăng lên 1; trên `split` nó đi ngang dưới ngưỡng.  
*Dữ liệu:* `results/dmin_m6` và `results/dmin_f99_m6`; giá trị trong [results_tables.md: dmin_m6](results_tables.md#dmin_m6) và [results_tables.md: dmin_f99_m6](results_tables.md#dmin_f99_m6).

### 4.2 Các số đo theo từng bước
- **Bầy tản ra thất bại nhiều hơn.**  
  Trên các ô có ít nhất 20 hạt giống ở 6 lần thời gian lùa, tương quan hạng (Spearman) giữa độ trải trung bình của bầy (khoảng cách RMS đến tâm) và tỷ lệ thành công là $-0{,}76$ dưới quy tắc nghiêm ngặt và $-0{,}71$ dưới quy tắc 99% ($-0{,}57$ đến $-0{,}68$ ở 3 lần thời gian lùa).
- **Các chó đến gần nhau bao nhiêu.**  
  Với `strombom_multi` trên `wide`, không chó nào có chó khác trong vòng 2 m đến $D = 6$; ở $D = 16$ tỷ lệ là 0,45–0,59 trên các bố cục phân tán. Với FAT nó là 0,56–0,82 từ $D = 2$, vì mọi chó đuổi cùng một con cừu.

![Các số đo từng lượt](../figures/fig27_metrics.png)

**Hình 16: Các số đo theo từng bước ở 6 lần thời gian lùa.**  
(a) Độ trải trung bình của bầy (khoảng cách RMS đến tâm) so với tỷ lệ thành công, mỗi ô một điểm (tương quan hạng $-0{,}76$ nghiêm ngặt, $-0{,}71$ ở 99%).  
(b) Trung vị tỷ lệ chó đứng yên theo $D$ ở $N = 200$ (quy tắc 99%) cho `wide`, `split` và `outlier_rich`. Trên `split`, khoảng một phần tư số chó đứng yên vì quy tắc dừng 6 m.  
(c) Trung vị tỷ lệ chó có một chó khác trong vòng 2 m theo $D$.  
*Dữ liệu:* `results/dmin_m6` và `results/dmin_f99_m6`.

---

## 5. Thảo luận

### 5.1 So với quy luật căn bậc hai
Độ dốc của chúng tôi (0,20–0,42 ở 12 lần thời gian lùa trên năm quy mô; 0,27–0,38 trên chín, mục 3.8) thấp hơn mức tăng $\sqrt{N}$ (độ dốc 0,5) mà Lama và di Bernardo (2024) công bố cho mục tiêu không tụ bầy. Một cách đọc hợp lý: không có gắn kết, người chăn phải đi bắt từng mục tiêu; trong một bầy gắn kết, mỗi con cừu bị hút về cả bầy ($n = N - 1$), nên khi chó đã lùa một con lạc quay lại, nó tự nhập lại bầy.

Các lượt chạy về độ gắn kết (mục 3.11) kiểm tra cách đọc này. Một bầy gắn kết hơn bầy của bài báo hầu như không đổi độ dốc (0,20 trên `wide`, so với 0,20–0,30), trong khi bầy yếu hơn duy nhất mà mô hình tạo được (mỗi con cừu bị hút về một nửa bầy) nâng nó lên 0,40–0,70, một khoảng chứa 0,5. Thời hạn cũng vậy: ở 6 lần thời gian lùa, độ dốc là 0,38–0,61. Độ gắn kết và áp lực thời gian cùng nhau quyết định một bầy nằm ở phía nào của quy luật căn bậc hai.

Mục 3.14 cho phía không gắn kết ngay trong HerdSim. Mô hình của bài báo cho lại quy luật của chính nó: số mũ 0,52–0,53 khi thấy mọi thứ và 0,41–0,42 trên ngưỡng với bán kính cảm nhận 10, theo cả hai thống kê. Cả hai đều cao hơn 0,27–0,38 của bầy Strömbom ở 12 lần thời gian lùa, đúng như cách đọc trên. Hai loạt chạy còn khác nhau về nhiệm vụ và quy tắc người chăn, nên phần chênh lệch do độ gắn kết chưa được đo.

### 5.2 Các lượt thất bại kết thúc thế nào, và độ trải lúc xuất phát

1. **Hai loại lượt thất bại.**  
   Chúng tôi chia các lượt lùa thất bại theo nơi bầy dừng lại. Một lượt là **gần đích** khi tâm bầy kết thúc trong vòng hai bán kính đích quanh tâm đích: bầy đã đến đó nhưng trễ hạn hoặc còn sót cừu bên ngoài. Nó là **xa đích** khi tâm bầy kết thúc xa hơn: bầy chưa bao giờ được gom và lùa đến đích. Phần lớn thất bại là xa đích:

   | Giao thức | Quy tắc | Lượt thất bại | Xa đích | Gần đích | Tỷ lệ xa |
   | :--- | :--- | :---: | :---: | :---: | :---: |
   | `dmin_m12` | nghiêm ngặt, 12× | 235 | 180 | 55 | **76,6%** |
   | `dmin_m6` | nghiêm ngặt, 6× | 889 | 639 | 250 | **71,9%** |
   | `dmin_m3` | nghiêm ngặt, 3× | 710 | 571 | 139 | **80,4%** |
   | `dmin_f99_m12` | 99%, 12× | 235 | 213 | 22 | **90,6%** |
   | `dmin_f99_m6` | 99%, 6× | 1.511 | 1.067 | 444 | **70,6%** |
   | `dmin_f99_m3` | 99%, 3× | 584 | 457 | 127 | **78,3%** |

   Trong 70% đến 91% số lượt thất bại, bầy kết thúc xa đích, nên phần lớn thất bại đến từ việc gom và lùa, không phải từ mấy mét cuối. Cách chia này chỉ dùng nơi bầy kết thúc; nó không cho biết thêm thời gian có cứu được lượt chạy hay không.  
   *Dữ liệu:* `python -m analysis.dispersion_burden`, trên sáu giao thức chính.

2. **Độ trải lúc xuất phát nhân $N$.**  
   Tích của độ trải lúc xuất phát $S_0$ (bán kính RMS của bầy lúc xuất phát) và $N$ đo lượng công gom mà một bố cục đòi hỏi. Ở $N = 400$, nó lớn gấp 8 đến 13 lần trên các bố cục phân tán so với `compact`, và tỷ lệ thành công ở 6 lần thời gian lùa (trên mọi $D$) giảm khi nó tăng:

   | Bố cục | $N$ | Độ trải xuất phát $S_0$ | $S_0 \times N$ | Tỷ lệ thành công (mọi $D$) |
   | :--- | :---: | :---: | :---: | :---: |
   | `compact` | 25 | 4,8 m | 119 | 100,0% |
   | `compact` | 100 | 6,7 m | 665 | 100,0% |
   | `compact` | 400 | 8,3 m | 3.316 | 100,0% |
   | `wide` | 400 | 74,8 m | 29.931 | 83,8% |
   | `outlier_rich` | 400 | 66,2 m | 26.496 | 55,3% |
   | `split` | 400 | 108,8 m | 43.507 | 21,1% |

   Đại lượng này tách bầy tập trung khỏi bầy phân tán, nhưng không xếp thứ tự được các bố cục phân tán: `outlier_rich` có giá trị nhỏ hơn `wide` nhưng tỷ lệ thành công thấp hơn. Các con lạc nằm ở đâu cũng quan trọng như chúng xa đến đâu.  
   *Dữ liệu:* `python -m analysis.dispersion_burden` trên `dmin_m6`; $S_0$ là trung bình của `max_extent` (bán kính RMS lớn nhất của bầy trong một lượt, tức lúc xuất phát).

### 5.3 Nghiên cứu này thêm được gì

1. **Một bản đồ quy mô đội đã quyết định.** $D_{\min}$ và $D_{\mathrm{sat}}$ qua các quy mô bầy ($N \le 566$, với các lượt chạy đến 3200), bố cục và thời hạn, mỗi ô được quyết định với độ tin cậy 99% hoặc báo cáo dưới dạng khoảng.
2. **Quy tắc thành công thay đổi câu trả lời.** Dưới quy tắc nghiêm ngặt, con cừu cuối cùng thường quyết định một lượt; quy tắc 99% đo những gì cả đội làm được với bầy.
3. **Đội tin cậy và đội nhanh là hai đội khác nhau.** Đội nhanh nhất tăng theo $N$ nhanh gấp khoảng đôi đội tin cậy nhỏ nhất, và chó vượt quá nó chỉ thêm chi phí mà không thêm tốc độ.
4. **Phần nào của quy tắc đội quan trọng.** Công tắc gom/lùa đưa một đội không phối hợp đến $N = 200$; ở $N = 400$ cần phân công.
5. **Khi nào thêm chó gây hại.** Chó dạng điểm chưa bao giờ làm nhiệm vụ thất bại; chó giữ cách nhau 2 m thì có, trên `outlier_rich` $N = 400$ từ khoảng 9 chó.
6. **Độ gắn kết và quy luật căn bậc hai.** Bầy Strömbom tăng chậm hơn $\sqrt{N}$ ở thời hạn thong thả, và gắn kết yếu hơn đẩy nó về phía 0,5.
7. **Một giới hạn của quy tắc lùa.** Trên $N \approx 1056$, điểm lùa của Strömbom nằm ngoài khoảng cách phản ứng của cừu; giới hạn nó lại làm việc lùa hoạt động trở lại.
8. **Cảm nhận và chia sẻ.** Tầm nhìn cục bộ tốn khoảng một chó ở $N = 200$, và chia sẻ với cả đội lấy lại được trên `wide` (không trên `split`).
9. **Các thất bại kết thúc thế nào.** Phần lớn các lượt lùa thất bại kết thúc xa đích.
10. **Một bộ mô phỏng tái lập được.** Mọi lượt có thể chạy lại từ cấu hình và hạt giống của nó; 932 lượt chạy lại chẩn đoán cho đúng các lượt đã lưu.

### 5.4 Ứng dụng khả dĩ

Ứng dụng trực tiếp là chăn dắt bằng robot và drone, nơi phải chọn quy mô đội trước khi chạy. Với người chăn cừu thực thụ, các con số chỉ mang tính gián tiếp: họ quyết định bằng kinh nghiệm và tự điều khiển chó, và cừu của mô hình khác cừu thật (bầy lỏng hơn, một khoảng cách phản ứng cố định).

Dưới đây, một *đơn vị* là một thành viên của đội: một chó, một robot hay một drone. Số đơn vị chính là quy mô đội $D$, nên "một đến ba đơn vị" nghĩa là $D = 1$ đến 3.

- **Định cỡ một đội.** Ở thời hạn thong thả, một đến ba đơn vị xử lý được một bầy phân tán đến 400 con, và một bầy tập trung cần một đơn vị đến $N = 1131$ (hai ở 1600, với điểm lùa bị giới hạn). Thời hạn làm thay đổi câu trả lời gần bằng một bầy lớn gấp bốn, nên hãy chốt thời gian có được trước khi chọn quy mô đội.
- **Tốc độ tốn hơn độ tin cậy.** Trên `wide` và `outlier_rich`, đội nhanh nhất lớn gấp rưỡi đến hai lần rưỡi đội tối thiểu (nhiều hơn trên `split`), và các đơn vị vượt quá nó chỉ thêm thời gian chạy mà không thêm lợi ích (Bảng 6).
- **Chỗ mỗi đơn vị chiếm giới hạn đội hữu ích.** Các đơn vị không thể đến gần nhau dưới 2 m làm chật vòng cung sau một bầy `outlier_rich` từ khoảng 9 đơn vị ở $N = 400$.
- **Chia sẻ bản đồ trước khi thêm đơn vị.** Tầm nhìn cục bộ tốn khoảng một đơn vị ở $N = 200$, và chia sẻ những gì mọi đơn vị thấy đã lấy lại được trên `wide` (không trên `split`).
- **Lùi ra để giữ bầy.** Các đơn vị phải lùi ra ngoài khoảng cách chạy trốn của con vật để giữ bầy tại chỗ; các đơn vị chỉ dừng lại thì vẫn làm bầy di chuyển.
- **Bầy lớn cần điểm lùa gần hơn.** Một bộ điều khiển dùng quy tắc lùa của Strömbom phải giới hạn khoảng đứng ở khoảng cách chạy trốn với bầy trên khoảng một nghìn con.
- **Phúc lợi động vật.** Trong mô hình, thời gian mỗi con cừu chạy trốn không tăng khi thêm đơn vị. Đây là một giả thuyết để thử ngoài thực địa theo tinh thần của Yaxley et al. (2021), không phải một phát hiện về động vật.

---

## 6. Hạn chế

1. **Cơ thể đơn giản.** Cừu và chó là các điểm, quay hướng tức thì và không mệt.
2. **Không có hàng rào.** Cánh đồng thật có hàng rào giúp chó giữ các con lạc; mô hình không có.
3. **Các khoảng.** Các ô có tỷ lệ thành công thật gần 0,90 vẫn chưa quyết định ở 200 lượt, nên một số câu trả lời là khoảng.
4. **Thấy mọi thứ ở phần lớn lượt chạy.** Ngoài mục 3.12, chó biết vị trí của mọi con cừu. Mục 3.12 giới hạn tầm nhưng vẫn cho vị trí chính xác trong tầm; việc chỉ cảm nhận hướng không được mô hình hóa.
5. **Các lựa chọn của HerdSim ở phần tiếp theo.** Quy tắc lùi ra khi giữ bầy, khoảng cách 2 m giữa các chó và điểm lùa bị giới hạn là lựa chọn của HerdSim, không phải quan sát từ chó thật.
6. **Giới hạn hiệu chỉnh.** Trên khoảng $N = 600$, bầy Strömbom không ổn định về một kích thước, nên kết quả ở $N$ lớn hơn là ở một mật độ được áp đặt. Ở $N = 800$ đến 1131, bầy tập trung trong một lượt chỉ bằng 0,5–0,8 lần bán kính áp đặt (`cli/dmin_tables.py extent`).
7. **Mẫu chẩn đoán nhỏ.** Các lượt chạy lại về áp lực và về `split` dùng 12 hạt giống mỗi ô. Chúng cho thấy xu hướng, không phải cận chặt.
8. **Nhiều chó cùng đẩy một con cừu.** Mô hình của Strömbom định nghĩa lực đẩy của một chó. HerdSim chuẩn hóa tổng lực đẩy của mọi chó trong vòng 65 m về độ lớn lực đẩy của một chó. Nếu cộng mà không chuẩn hóa, hai chó cách nhau dưới 116° sẽ đẩy mạnh hơn lực hút của bầy ($c = 1{,}05$) và xé bầy từ $D = 2$ trở lên. Đây là một lựa chọn mô hình; liệu cừu thật có chạy mạnh hơn khi gặp nhiều chó không là câu hỏi cho dữ liệu thực địa.
9. **Tốc độ cừu.** Một con cừu Strömbom đang phản ứng luôn đi với 1 m/s, nên thời gian hoàn thành phẳng sau $D_{\mathrm{sat}}$ là hệ quả của mô hình. Cừu Kubo tăng tốc khi bị đẩy mạnh hơn (đến 5 m/s), vì thế thêm chó Kubo vẫn tiếp tục rút ngắn lượt lùa.
10. **Tái lập trên máy khác.** Chạy lại cho kết quả chính xác trên cùng một máy, với các phiên bản phụ thuộc đã khóa (`uv.lock`) và một luồng BLAS mỗi tiến trình. Trên CPU khác, các bit cuối của phép tính dấu phẩy động có thể khác, có thể làm đổi kết quả của những lượt hiếm kết thúc sát thời hạn.
11. **Xem kết quả giữa các lô.** Độ tin cậy được quyết định sau mỗi lô 10 hạt giống. Khoảng Clopper–Pearson thận trọng và một ô tin cậy cần ít nhất 51 lượt thành công liên tiếp, nhưng việc xem nhiều lần không được hiệu chỉnh, nên độ tin cậy 99% của một quyết định chỉ là gần đúng.
12. **Mô hình Lama và di Bernardo được dựng lại từ văn bản bài báo**; không có mã nguồn công bố. Ở những chỗ văn bản không nói, HerdSim chọn và ghi rõ (lực đẩy hướng ra xa người chăn; một lượt kết thúc khi mọi người chăn ở trong đích và không ai thấy mục tiêu nào bên ngoài; mục tiêu và người chăn được di chuyển từ cùng một trạng thái). Mục 3.14 chỉ so bằng số với Bảng I của bài báo và so phần còn lại với hình của bài báo bằng cách đặt cạnh nhau.

---

## 7. Kết luận và hướng tiếp theo

Qua 367.150 lượt trong 39 giao thức, HerdSim lập bản đồ đội tin cậy nhỏ nhất $D_{\min}$, đội mà vượt quá nó thêm chó không còn giúp ($D_{\mathrm{sat}}$), và những tình huống mà thêm chó gây hại. Một bầy tập trung cần một chó đến $N = 1131$ (với điểm lùa bị giới hạn trên 1056). Trên bầy phân tán, đội nhỏ nhất tăng chậm hơn bầy, với độ dốc 0,27–0,38 ở 12 lần thời gian lùa và 0,38–0,61 ở 6 lần, trong khi đội nhanh nhất tăng nhanh gấp khoảng đôi. Dưới quy tắc nghiêm ngặt, con cừu cuối cùng quyết định; dưới quy tắc 99%, câu trả lời giữ nguyên khi đổi thiết lập. Phối hợp quan trọng ở bầy lớn. Thêm chó dạng điểm chưa bao giờ làm nhiệm vụ thất bại trên `wide` hay `outlier_rich` nhưng làm chậm `split`, còn chó chiếm chỗ thì có gây thất bại. Bản thân quy tắc lùa của Strömbom ngừng hoạt động trên khoảng một nghìn con. Chạy trong cùng bộ mô phỏng, các mục tiêu không gắn kết của Lama và di Bernardo theo đúng quy luật căn bậc hai của họ, cả dưới quy tắc tin cậy của HerdSim, trừ gần ngưỡng của họ, nơi một mức trung bình 0,99 che đi những lượt sót mục tiêu.

### Hướng tiếp theo

1. **Phân công có nhìn thấy cụm.** Trên `split`, phân công chó sao cho mỗi cụm đều có chó, thay vì chỉ theo tổng quãng đường.
2. **Giữ bầy có cổng.** Thử giữ bầy trong một chuồng đóng thay vì cho chó lùi ra ngoài trời, xem bầy nhỏ có giữ được không.
3. **Chỉ cảm nhận hướng.** Cho chó cảm nhận hướng tới một con cừu mà không biết khoảng cách, như một camera trên drone.
4. **Ghép chéo hai mô hình trên một nhiệm vụ.** Chạy quy tắc đội của Strömbom trên các mục tiêu của Lama trong nhiệm vụ gom, và người chăn của Lama trên cừu Strömbom, để tách chênh lệch số mũ ở mục 3.14 thành phần do độ gắn kết và phần do quy tắc người chăn và nhiệm vụ. Mỗi quy tắc đọc những đại lượng mà phía kia không có (quy tắc đội đọc khoảng cách gom, vô nghĩa khi không có gắn kết; người chăn đọc khoảng cách đến một đích mà trong nhiệm vụ lùa nằm xa bầy), nên mỗi cách ghép cần thiết kế riêng trước.
5. **Dữ liệu thực địa với nhiều chó.** Hợp tác với các nhà nghiên cứu chăn nuôi để thu dữ liệu GPS khi chăn bằng nhiều chó hoặc drone, nhằm kiểm tra cừu thật có chạy mạnh hơn khi gặp nhiều chó không.
6. **Ước lượng cục bộ tâm bầy.** Thay việc cừu biết tâm của cả bầy bằng hướng về các hàng xóm gần nhất. `cli/diagnostics/gradient_validation.py` đo hướng đó lệch bao nhiêu trên các bố cục xuất phát; ở $N = 400$ với 15 hàng xóm, sai số trung bình vẫn khoảng 30°.

---

## Dữ liệu và mã

Mọi lượt chạy và quyết định của từng ô được lưu trong `results/<protocol>/`. Các bảng chứa số liệu của báo cáo này nằm trong [results_tables.md](results_tables.md); mỗi khối ghi lệnh đã tạo ra nó. Cách chạy lại nghiên cứu và tạo lại các bảng: xem [cli/README.md](../../cli/README.md) và [tài liệu tham chiếu CLI](../guides/cli_reference.md).

---

## Tài liệu tham khảo

- Auletta F, Fiore D, Richardson MJ, di Bernardo M (2021). Herding stochastic autonomous agents via local control rules and online global target selection strategies. *arXiv:2010.00386*.
- Brown D, Garrity T, Perkins D, Hunter D, Pochman W (2025). Optimal control strategies for multi-agent sheep herding. *arXiv:2510.25115*.
- di Bernardo M (2026). Multi-scale control of large agent populations: from density dynamics to individual actuation. *arXiv:2603.15160*.
- Green T, et al. (2022). A minimalist solution to the multi-robot barrier coverage problem. *Towards Autonomous Robotic Systems (TAROS 2021)*, LNCS 13054.
- Jadhav V, Pasqua R, Zanon C, Roy M, Tredan G, Bon R, Guttal V, Theraulaz G (2024). Collective responses of flocking sheep (*Ovis aries*) to a herding dog (border collie). *Communications Biology* 7: 1543.
- Kubo M, Tashiro M, Sato H, Yamaguchi A (2022). Herd guidance by multiple sheepdog agents with repulsive force. *Artificial Life and Robotics* 27: 416–427.
- Lama A, di Bernardo M (2024). Shepherding control and herdability in complex multiagent systems. *Physical Review Research* 6: L032012.
- Li A, Ogura M, Wakamiya N (2025). Swarm shepherding using bearing-only measurements. *Philosophical Transactions of the Royal Society A* 383: 20240145.
- Pierson A, Schwager M (2015). Bio-inspired non-cooperative multi-robot herding. *IEEE International Conference on Robotics and Automation (ICRA)*.
- Ranganathan A, et al. Emergent strategies for shepherding a flock. *arXiv:2211.04352*.
- Strömbom D, Mann RP, Wilson AM, Hailes S, Morton AJ, Sumpter DJT, King AJ (2014). Solving the shepherding problem: heuristics for herding autonomous, interacting agents. *Journal of the Royal Society Interface* 11(100): 20140719.
- Yaxley KJ, Joiner KF, Abbass H (2021). Drone approach parameters leading to lower stress sheep flocking and movement: sky shepherding. *Scientific Reports* 11: 7803.

---

## Phụ lục A: Nhật ký chạy giao thức

| Giao thức | Lượt | Ô | Đã quyết định | Còn mở ở 200 lượt | Lỗi | Giờ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `dmin_m12` | 17.220 | 183 | 179 | 4 | 0 | 1,24 |
| `dmin_m6` | 13.470 | 191 | 170 | 21 | 0 | 0,28 |
| `dmin_m3` | 9.530 | 183 | 178 | 5 | 0 | 0,17 |
| `dmin_f99_m12` | 11.100 | 180 | 178 | 2 | 0 | 0,41 |
| `dmin_f99_m6` | 14.240 | 191 | 174 | 17 | 0 | 0,49 |
| `dmin_f99_m3` | 11.140 | 185 | 177 | 8 | 0 | 0,27 |
| `dmin_fat` | 8.660 | 181 | 179 | 2 | 0 | 0,22 |
| `dmin_f99_fat` | 8.670 | 184 | 183 | 1 | 0 | 0,23 |
| `dmin_kubo` | 1.080 | 18 | 18 | 0 | 0 | 0,08 |
| Các giao thức độ nhạy (14 lượt chạy) | 69.630 | 921 | 800 | 121 | 0 | 3,27 |
| **Tổng** | **164.740** | **2.417** | **2.236** | **181** | **0** | **khoảng 6,7** |

Các lượt chạy tiếp theo (quy tắc 99%; giờ với 20 worker):

| Giao thức | Lượt | Ô | Còn mở ở 200 lượt | Lỗi | Giờ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3` (chạy tiếp với lượt cho thời gian hoàn thành; thêm $N$ 71, 141, 283, 566 vào hai cái đầu) | +38.770 | | | 0 | 4,0 |
| `dmin_f99_indep` | 12.990 | 181 | 18 | 0 | 0,30 |
| `dmin_f99_kubo` | 3.260 | 38 | 6 | 0 | 0,18 |
| `dmin_f99_hold` | 14.280 | 280 | 18 | 0 | 0,74 |
| `dmin_f99_hold_spacing` (chạy lại với quy tắc giãn cách cứng) | 13.930 | 283 | 19 | 0 | 0,70 |
| `dmin_f99_c1.3`, `_c1.6`, `_c2.0` | 10.800 / 10.830 / 10.780 | 180 mỗi giao thức | 1 / 0 / 0 | 0 | 0,31 / 0,29 / 0,41 |
| `dmin_f99_k05` | 11.630 | 149 | 14 | 0 | 2,29 |
| `dmin_f99_view_range` | 21.040 | 293 | 27 | 0 | 0,53 |
| `dmin_f99_view_comm` | 6.890 | 102 | 3 | 0 | 0,20 |
| `dmin_f99_big` | 2.230 | 84 | 1 | 0 | 3,12 |
| `dmin_f99_big_dense`, `_loose` | 1.320 / 830 | 15 / 14 | 2 / 1 | 0 | 0,73 / 0,26 |
| `dmin_f99_big_cap` | 2.550 (+100 ở $N = 3200$, không tính) | 45 | 3 | 0 | 5,5 (7,6 tính cả $N = 3200$) |
| `lama_r50` (nhiệm vụ gom, bán kính cảm nhận 10) | 17.660 | 500 | 23 | 0 | 6,53 |
| `lama_r50_inf` (nhiệm vụ gom, thấy mọi thứ) | 22.620 | 500 | 1 | 0 | 6,47 |

Chạy lại chẩn đoán: 164 lượt về áp lực và 768 lượt về `split`, mọi lượt chạy lại không đổi đều giống hệt lượt đã lưu. Hai lượt kiểm chứng mô hình Lama (8.200 lượt, thư mục nháp không giữ) chạy trước `lama_r50`; lượt thứ hai sửa thứ tự di chuyển người chăn và mục tiêu (mục 6, ý 12).

---

## Phụ lục B: Các khẳng định và bằng chứng

| # | Khẳng định | Loại | Bằng chứng | Giới hạn |
| :-: | :--- | :--- | :--- | :--- |
| 1 | Một bầy tập trung cần một chó ($D_{\min} = 1$) đến $N = 1131$. | Đo được | `dmin_m12`, `dmin_m6`, `dmin_m3`, `dmin_f99_*` đến $N = 566$; `dmin_f99_big_cap` ở 800 và 1131. | Trên 1056 chỉ khi giới hạn điểm lùa. |
| 2 | Đến $N = 50$, một chó là đủ trên mọi bố cục và thời hạn. | Đo được | Mọi ô $N \le 50$ của 23 giao thức cơ sở được quyết định ở $D = 1$. | Lý do nêu ở mục 3.1 là khả dĩ, chưa được kiểm tra. |
| 3 | Trên bầy phân tán, $D_{\min}$ tăng với độ dốc 0,27–0,38 ở 12 lần thời gian lùa và 0,38–0,61 ở 6 lần. | Đo được | Khoảng độ dốc qua các khoảng $D_{\min}$ của chín quy mô ($N = 25$–566), `dmin_f99_m12`, `dmin_f99_m6`. | Chỉ đến giới hạn hiệu chỉnh. |
| 4 | Dưới quy tắc nghiêm ngặt, các đội lớn thất bại vì con cừu cuối cùng. | Đo được | 97% số lượt thất bại nghiêm ngặt với $D \ge 6$ đã có 99% bầy trong đích (`dmin_s_base`); với chó chậm hơn (`dmin_s_dogspeed`), $D_{\min}$ nghiêm ngặt trên `outlier_rich` $N = 400$ từ none xuống 6. | Áp dụng cho quy tắc nghiêm ngặt với đích mở. |
| 5 | Trên `split`, các chó đi gom dồn về một cụm và nhiều chó đứng yên. | Đo trong các lượt chạy lại | Các lượt chạy lại `split_diagnostic`: trải các con lạc ra làm thời gian hoàn thành giảm một nửa ở $D = 4$; rút khoảng cách dừng làm lượt lùa nhanh hơn 21–24% ở $D = 8$, 16. | 12 hạt giống mỗi ô; không thay đổi nào sửa được 3 lần thời gian lùa. |
| 6 | Gắn kết yếu hơn làm $D_{\min}$ tăng nhanh hơn, về phía 0,5. | Đo được | `dmin_f99_k05` độ dốc 0,40–0,70 trên `wide`; `dmin_f99_c*` 0,20. | Chỉ một mức yếu hơn; bầy yếu hơn nữa không hiệu chỉnh được. |
| 7 | Trên $N \approx 1056$, điểm lùa của Strömbom nằm ngoài khoảng cách phản ứng của cừu. | Suy ra và đo được | $2\sqrt{N} > 65$; không giới hạn, 0 trên 10 lượt thành công ở $N = 1131$ với mọi $D$; có giới hạn, bầy tập trung thành công ở 800, 1131, 1600 và 42 trên 42 ở 3200. | Giả định khoảng cách phản ứng $r_s = 65$ m. |
| 8 | Chó giữ cách nhau 2 m làm chó thêm trở nên có hại trên `outlier_rich` $N = 400$. | Đo được | `dmin_f99_hold_spacing`: thành công 0,94 ở $D = 6$, 0,77 ở 9, 0,50 ở 16; mọi $D \ge 9$ không tin cậy. | Không thấy trên `wide` hay `compact`. |
| 9 | Tầm nhìn cục bộ tốn khoảng một chó ở $N = 200$; chia sẻ với cả đội lấy lại được. | Đo được | `dmin_f99_view_range`, `dmin_f99_view_comm`. | Việc chia sẻ trong mô hình là tức thời và không lỗi. |
| 10 | Gần ngưỡng, một mức trung bình 0,99 chấp nhận những đội thất bại một lượt trên ba. | Đo được | `lama_r50`: ở 144 mục tiêu, 11 người chăn đạt trung bình 0,992 nhưng thành công ở 70% số lượt; $D_{\min}$ của HerdSim là 17–25. | Mục tiêu không gắn kết trên một hình tròn. |

---

## Phụ lục C: Khả năng tái lập

| Hạng mục | Ở đâu |
| :--- | :--- |
| Mã nguồn | Kho `HerdSim`, nhánh `scaling-cli-d-min-max`. |
| Môi trường | `uv`, Python 3.11 trở lên; các phiên bản khóa trong `pyproject.toml` và `uv.lock`. |
| Bố cục xuất phát | `sim/core/world/layouts.py` (`compact`, `wide`, `split`, `outlier_rich`). |
| Dòng ngẫu nhiên | Hạt giống $i$ của mọi ô là `master_seed + i`; mỗi lượt có các dòng riêng cho bố cục xuất phát, cho cừu và cho chó, nên các ô cùng hạt giống xuất phát từ cùng một bầy. |
| Phần cứng | Máy trạm Linux, 20 worker (`--workers 20`). |
| Dữ liệu thô | 367.150 dòng lượt chạy trong `results/<protocol>/trials.jsonl`, kèm bản `trials.csv`. |
| Chạy nghiên cứu | `uv run cli/campaign.py run --protocol <id>` và `uv run cli/run_queue.py`. |
| Các bảng | `cli/dmin_tables.py` dựng [results_tables.md](results_tables.md) từ các thư mục kết quả. |
| Kiểm thử | `make test` chạy 330 kiểm thử đơn vị, bất biến và hồi quy; `make bench` chạy 23 chiến dịch thu nhỏ. |
| Chạy lại | `services/replay.py`; 932 lượt chạy lại chẩn đoán cho đúng các lượt đã lưu. |
