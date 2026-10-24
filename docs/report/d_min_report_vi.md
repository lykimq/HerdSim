# Quy mô đội để lùa một bầy cừu mô phỏng: Tối thiểu, đủ và quá nhiều chó

*Báo cáo nghiên cứu khoa học dự án HerdSim*  
*Đánh giá thực nghiệm qua 23 giao thức chiến dịch (164.740 lượt chạy mô phỏng) trên các kiến trúc chăn dắt đa tác tử, tiếp theo là 14 giao thức tiếp nối và ba lượt chạy tiếp (162.130 lượt): tổng cộng 37 giao thức và 326.870 lượt chạy, không có lỗi.*  
*(Lưu ý: Các phương trình động lực học vi mô, thuật toán điều khiển và định nghĩa hình học sân bãi đã được trình bày đầy đủ trong [README_vi.md](../../README_vi.md). Báo cáo này tập trung chuyên sâu vào ranh giới mở rộng thực nghiệm, câu trả lời thống kê cho các câu hỏi nghiên cứu, phân tích cơ chế thất bại vi mô và các hàm ý khoa học.)*

---

## Tóm tắt (Abstract)

Cần bao nhiêu tác tử chăn dắt tự hành ($D$) để gom một bầy $N$ con cừu và lùa bầy vào vùng đích một cách tin cậy trước thời hạn: tối thiểu là bao nhiêu, bao nhiêu thì đủ, và từ khi nào thêm chó lại làm hỏng việc? Chúng tôi khảo sát bài toán này thông qua môi trường mô phỏng trên 37 giao thức chiến dịch với tổng cộng 326.870 lượt chạy mà không phát sinh bất kỳ lỗi mô phỏng nào. Chúng tôi định nghĩa $D_{\min}$ là quy mô đội nhỏ nhất đạt độ tin cậy (tỷ lệ thành công được chứng minh $\ge 0{,}90$ dưới khoảng tin cậy nhị thức Clopper–Pearson hai phía ở mức ý nghĩa 99%). Sử dụng thuật toán phân bổ tuần tự thích ứng giúp tập trung tài nguyên tính toán vào các ô tham số ranh giới (tối đa 200 hạt giống mỗi ô), 23 giao thức đầu tiên (164.740 lượt) lập bản đồ $D_{\min}$ qua 5 quy mô bầy đàn ($N \in [25, 400]$), 4 bố cục không gian xuất phát (`compact`, `wide`, `split`, `outlier_rich`) và 3 mức thời hạn chuẩn hóa ($12\times$, $6\times$, và $3\times$ thời gian lùa tối thiểu) dưới cả hai tiêu chí: *chặn giữ nghiêm ngặt* (100% cừu trong đích) và *tiếp cận 99%* (tối thiểu $\lceil 0{,}99 N \rceil$ cừu trong đích). Các giao thức tiếp theo chỉ dùng tiêu chí 99% và bổ sung quy mô đội mà từ đó thêm chó không còn giúp ích (*D*<sub>sat</sub>), bốn quy mô bầy mới đến $N = 566$, các quy tắc đội, giữ đàn, giãn cách chó, độ gắn kết, tầm cảm nhận, và các bầy vượt giới hạn của mô hình đến $N = 3200$.

Các kết quả thực nghiệm chỉ ra:
1. **Tính bất biến của bầy co cụm**: Với bầy xuất phát co cụm (`compact`), $D_{\min} \equiv 1$ là một hằng số bất biến tuyệt đối trên mọi quy mô ($N = 25$ đến $400$) và mọi thời hạn. Bổ sung thêm chó không giúp rút ngắn thời gian lùa đàn.
2. **Quy luật tăng trưởng dưới tuyến tính trên bầy phân tán**: Với bầy phân tán, $D_{\min} = 1$ khi $N \le 50$, và chỉ cần 2 đến 3 chó ở $N = 400$ dưới thời hạn nới lỏng ($12\times$). Trong không gian log-log ($\log_2 D_{\min}$ theo $\log_2 N$), độ dốc tăng trưởng trên năm kích thước ban đầu dao động từ 0,20 đến 0,50 ở thời hạn $12\times$, và từ 0,30 đến 0,80 ở thời hạn $6\times$ (thu hẹp trên chín kích thước, mục 8).
3. **Áp lực thời hạn là yếu tố chi phối hàng đầu**: Rút ngắn thời hạn từ $12\times$ xuống $3\times$ làm tăng vọt $D_{\min}$ trên bố cục `wide` ở $N = 400$ từ 2 lên 5–6 chó—mức gia tăng này vượt qua cả tác động của việc mở rộng quy mô đàn cừu lên gấp bốn lần.
4. **Cơ chế cá thể lạc đàn (The Straggler Mechanism)**: Trong 95% số lượt thất bại nghiêm ngặt của các đội có từ 6 chó trở lên, đàn chó thực chất đã đưa được 99% số cừu vào đích từ rất sớm. Thất bại nghiêm ngặt xảy ra do đàn chó quay sang săn đuổi 1–2 cá thể rớt lại sau cùng, vượt quá đà và vô tình lùa ngược khối cừu chủ lực ra ngoài pasture. Việc giảm vận tốc chó ($v_{\mathrm{dog}} = 1{,}15$) loại bỏ được xung lực vượt đà này, giúp đưa $D_{\min}$ nghiêm ngặt từ thất bại hoàn toàn (`none`) xuống còn 6 chó ở bố cục `outlier_rich` ($N = 400$).
5. **Tính vững chắc của tiêu chí tiếp cận 99%**: Dưới tiêu chí 99%, giá trị $D_{\min}$ duy trì sự ổn định cao (dao động trong phạm vi $\pm 1$ chó so với mốc cơ sở) trước các thay đổi về quy ước mô phỏng (xuất phát từ cọc người chăn, xuất phát vòng tròn, cự ly xuất phát, và các tham số cừu thực địa GPS). Ngược lại, tiêu chí nghiêm ngặt phóng đại quá mức các sai số do quy ước hình học gây ra.
6. **Sự bắt buộc của tầng phối hợp đội**: Mô hình đối chứng không phối hợp (FAT) thiếu thuật toán gán nhiệm vụ và lực đẩy không gian đã thất bại hoàn toàn: các chú chó dồn cục thành bản sao trùng lặp (`dog_overlap` $> 0{,}80$), không đạt được bất kỳ giá trị $D_{\min}$ tin cậy nào ở $N \ge 200$.
7. **Đủ chó, và không có tác hại theo tiêu chí 99%** (phân tích tiếp theo, mục 3.7): vượt quá quy mô đội *D*<sub>sat</sub> mà tại đó việc lùa không còn nhanh hơn, chó thêm giữ thời gian hoàn thành ở mức 0,96 đến 1,01 lần thời gian tại *D*<sub>sat</sub>, trong khi thời gian chó tăng tỉ lệ với $D$, và thời gian mỗi con cừu chạy trốn không tăng. Theo tiêu chí 99%, không quy mô đội nào đến 24 làm nhiệm vụ thất bại trên năm kích thước ban đầu (một lần sụt trên lưới dày hơn); chó thêm chỉ làm bầy `split` chậm hơn, ở $N \ge 200$.
8. **Lưới dày hơn** (mục 3.8): trên chín kích thước bầy, $D_{\min}$ tăng với độ dốc 0,27–0,38 ở $12\times$ và 0,38–0,61 ở $6\times$, còn *D*<sub>sat</sub> tăng nhanh gấp khoảng hai lần (0,70–0,91 trên `wide`). Đến $N = 566$, một quy luật lũy thừa và một đường cong chững lại khớp dữ liệu tốt như nhau.
9. **Các phần của quy tắc đội** (mục 3.9): riêng công tắc gom/lùa của bài báo đã đưa một đội chó độc lập đến $N = 200$; tầng đội là điều làm cho $N = 400$ trở nên khả thi.
10. **Quá nhiều chó** (mục 3.10): với chó chiếm chỗ (cách nhau 2 m), `outlier_rich` $N = 400$ thất bại từ $D = 9$ (được quyết định không đạt độ tin cậy đến $D = 24$), trong khi chó dạng điểm không cho thấy tác hại được quyết định đến 24.
11. **Độ gắn kết và tầm cảm nhận** (mục 3.11, 3.12): gắn kết yếu hơn làm sự tăng dốc hơn về phía 0,5 của mục tiêu không gắn kết; tầm nhìn cục bộ tốn khoảng một con chó ở $N = 200$, và chia sẻ với cả đội mua lại được con chó đó.
12. **Một giới hạn của quy tắc lùa** (mục 3.13): trên $N \approx 1056$, điểm lùa của bài báo nằm ngoài cự ly phản ứng của cừu, và không đội nào, dù lớn đến đâu, lùa được bầy. Khi giới hạn điểm lùa trong tầm với, một bầy phân tán cần 3 chó ở $N = 800$, 5–9 ở 1131 và hơn 12 ở 1600.

---

## 1. Câu hỏi nghiên cứu và mục tiêu

Các nghiên cứu trước đây về chăn dắt đa tác tử chủ yếu khảo sát các quy mô đội cố định hoặc trên các mục tiêu không liên kết (Pierson và Schwager 2015; Kubo et al. 2022; Lama và di Bernardo 2024). Để xác lập quy luật mở rộng quy mô của đội chăn tối thiểu dưới ảnh hưởng của lực hút bầy đàn, áp lực thời hạn và sự phân tán không gian, nghiên cứu này giải quyết 7 Câu hỏi Nghiên cứu (RQs):

- **RQ1 (Quy luật mở rộng quy mô $N$)**: Quy mô đội tối thiểu $D_{\min}$ tăng trưởng thế nào theo kích thước bầy $N \in [25, 400]$ trên các bố cục không gian và thời hạn khác nhau? Lực hút bầy đàn có làm giảm độ dốc tăng trưởng so với bầy không liên kết ($\sqrt{N}$) hay không?
- **RQ2 (Bố cục hình học so với quy mô dân số $N$)**: Với cùng một thời hạn, yếu tố nào chi phối $D_{\min}$ mạnh mẽ hơn: bố cục xuất phát (co cụm hay phân tán) hay quy mô đàn cừu $N$?
- **RQ3 (Áp lực thời hạn hoàn thành)**: Áp lực thời gian ($12\times \to 6\times \to 3\times$ thời gian lùa) làm dịch chuyển $D_{\min}$ ra sao? Tác động này là tuyến tính hay phi tuyến?
- **RQ4 (Tiêu chí thành công và Hiệu ứng cá thể lạc đàn)**: Tiêu chí nghiêm ngặt 100% khác biệt thế nào so với tiêu chí 99% tiếp cận? Cơ chế vi mô nào gây ra sự sụp đổ thành công của các đội nhiều chó dưới tiêu chí nghiêm ngặt?
- **RQ5 (Tính vững chắc trước các quy ước mô phỏng)**: Các quy luật mở rộng có đứng vững trước những thay đổi về quy ước thiết lập (vị trí thả chó, cự ly xuất phát, bán kính đích, tham số thực địa, vận tốc chó) hay không?
- **RQ6 (Sự cần thiết của phối hợp đa tác tử)**: Một đàn chó hoạt động độc lập không phối hợp (FAT) có thể đạt được $D_{\min}$ hữu hạn ở đàn lớn hay không?
- **RQ7 (Vượt quá $D_{\min}$: đủ chó và quá nhiều chó)**: Từ quy mô đội *D*<sub>sat</sub> nào thì thêm một con chó không còn làm việc lùa nhanh hơn, mỗi con chó vượt quá nó tốn bao nhiêu, nó có thêm áp lực lên cừu không, và có quy mô đội nào làm nhiệm vụ tệ đi không? (Phân tích tiếp theo trên các lượt chạy 99% hiện có; không chạy chiến dịch mới.)

Các chiến dịch tiếp theo (tiêu chí 99% xuyên suốt) bổ sung sáu câu hỏi:

- **RQ8 (Lưới dày hơn và hình dạng đường cong)**: Với chín kích thước bầy đến ngưỡng của mô hình ($N = 566$), $D_{\min}$ và *D*<sub>sat</sub> tăng nhanh thế nào, và có phân biệt được tăng đều với một đường cong chững lại không?
- **RQ9 (Phần nào của quy tắc quan trọng)**: Công tắc gom/lùa và tầng đội mỗi phần đóng góp gì, và một mô hình mà thời gian hoàn thành giảm theo $D$ (Kubo) bão hòa ra sao?
- **RQ10 (Quá nhiều chó)**: Việc giữ bầy trong đích, hay chó chiếm chỗ, có làm cho chó thêm gây hại không?
- **RQ11 (Độ gắn kết)**: Sự tăng của $D_{\min}$ thay đổi thế nào theo độ mạnh của sự gắn kết giữa các con cừu?
- **RQ12 (Chó nhìn thấy gì)**: Tầm cảm nhận giới hạn tốn thêm bao nhiêu chó, và việc chia sẻ những gì các chó thấy có bù lại được không?
- **RQ13 (N lớn)**: Điều gì xảy ra trên kích thước mà bầy của mô hình còn có kích thước riêng?

---

## 2. Phương pháp luận thống kê và quy tắc quyết định

*(Chi tiết đầy đủ về vòng lặp thích ứng, khoảng tin cậy Clopper–Pearson và hệ thống hạt giống ngẫu nhiên chung CRN được trình bày tại [README_vi: Cơ chế thực thi thích ứng](../../README_vi.md#các-cơ-chế-thực-thi-thích-ứng).)*

### 2.1 Tiêu chí quyết định hình thức cho *D*<sub>min</sub>
Một **ô (cell)** được xác định bởi bộ tham số (phương pháp, bố cục, $N$, thời hạn, $D$). Mỗi lượt chạy mô phỏng là một phép thử Bernoulli độc lập cho ra kết quả thành công ($1$) hoặc thất bại ($0$). Với một mẫu gồm $n_{\mathrm{trials}}$ hạt giống được đánh giá và $k$ lần thành công quan sát được, khoảng tin cậy nhị thức Clopper–Pearson hai phía 99% $[L, U]$ cho xác suất thành công thực tế $p$ được tính toán như sau:

$$
L = B\left(\frac{\alpha}{2}, k, n_{\mathrm{trials}} - k + 1\right), \quad U = B\left(1 - \frac{\alpha}{2}, k + 1, n_{\mathrm{trials}} - k\right)
$$

trong đó:
- $n_{\mathrm{trials}} \in [10, 200]$: Tổng số lượt mô phỏng tích lũy đã chạy cho ô tham số đó.
- $k \in [0, n_{\mathrm{trials}}]$: Số lượt mô phỏng ghi nhận thành công.
- $\alpha = 0{,}01$: Mức ý nghĩa thống kê, tương ứng với độ tin cậy hai phía $1 - \alpha = 99\%$ (mỗi phía đuôi phân phối chiếm $\alpha/2 = 0{,}005$).
- $B(q, a, b)$: Hàm phân vị (hàm phân phối tích lũy nghịch đảo) của phân phối Beta với hai tham số hình dạng $a$ và $b$, tính tại xác suất tích lũy $q$.
- $L$: Cận dưới thống kê của tỷ lệ thành công thực tế với độ tin cậy 99%.
- $U$: Cận trên thống kê của tỷ lệ thành công thực tế với độ tin cậy 99%.

Với ngưỡng tin cậy mục tiêu quy định là $\theta = 0{,}90$:
- **Đạt độ tin cậy (Reliable)**: $L \ge 0{,}90$. Chúng ta có độ tin cậy toán học 99% rằng tỷ lệ thành công thực tế đạt ít nhất 90% (đòi hỏi tối thiểu 51 trận thắng liên tiếp không có trận thua nào, được làm tròn thành 60 lượt chạy với kích thước lô 10).
- **Không đạt tin cậy (Unreliable)**: $U < 0{,}90$. Chúng ta tin cậy 99% rằng ô này không thể đạt ngưỡng 90%, kích hoạt cơ chế dừng sớm để tiết kiệm thời gian (thường dừng sau 10–20 lượt).
- **Chưa quyết định (Undecided)**: $L < 0{,}90 \le U$. Khoảng tin cậy vẫn đang bao trùm ngưỡng 90%, ô sẽ tiếp tục nhận các lô 10 hạt giống tiếp theo cho đến trần tối đa 200 hạt giống.

Trên một đường cong kiểm thử theo số lượng chó $D \in \mathcal{D}$:

$$
D_{\min} = \min \{ D \in \mathcal{D} \mid \mathrm{Cell}(D) \text{ is Reliable} \}
$$

$$
D_{\min,\mathrm{low}} = \min \{ D \in \mathcal{D} \mid U(D) \ge \theta \}
$$

- **Giá trị quyết định**: Khi $D_{\min,\mathrm{low}} = D_{\min}$, mọi $D < D_{\min}$ đều chắc chắn không đạt tin cậy ($U < 0{,}90$).
- **Khoảng chặn ($[D_{\min,\mathrm{low}}, D_{\min}]$)**: Khi $D_{\min}$ đạt tin cậy nhưng vẫn còn một số $D$ nhỏ hơn ở trạng thái chưa quyết định tại mốc 200 hạt giống (ví dụ `3-8`).
- **Cận dưới ($[n]$)**: Chưa có $D$ nào đạt tin cậy nhưng tồn tại $D \ge n$ chưa quyết định.
- **Thất bại (`none`)**: Toàn bộ các giá trị $D$ trên lưới kiểm thử (đến $D = 24$ ở các lượt chạy chính) đều chắc chắn không đạt độ tin cậy ($U < 0{,}90$).

### 2.2 Tổng quan ma trận 23 giao thức thực nghiệm
Nghiên cứu đầu tiên bao gồm 23 giao thức (164.740 lượt chạy, 20 luồng worker, 0 lỗi):
- **Lưới chính (6 giao thức)**: Đánh giá đầy đủ 5 quy mô ($N \in [25, 400]$), 4 bố cục (`compact`, `wide`, `split`, `outlier_rich`), và 3 thời hạn ($12\times, 6\times, 3\times$ thời gian lùa) dưới cả hai tiêu chí Nghiêm ngặt 100% và Tiếp cận 99%.
- **Đối chứng không phối hợp (2 giao thức)**: `dmin_fat` và `dmin_f99_fat` ở thời hạn $6\times$.
- **Mô hình lực liên tục Kubo (1 giao thức)**: `dmin_kubo` trên bầy co cụm ($N \in [25, 100]$).
- **Bộ kiểm tra độ nhạy (14 giao thức)**: Đánh giá ở thời hạn $6\times$ qua 7 biến thể (cọc handler, vòng tròn ring, khoảng cách khởi đầu 15/30/60, bán kính đích $1{,}5 R_f$, tham số thực địa GPS, và tốc độ chó 1,15) dưới cả hai tiêu chí.

Phần tiếp theo bổ sung 14 giao thức và chạy tiếp ba lưới 99% (162.130 lượt, 0 lỗi, chỉ tiêu chí 99%), được liệt kê cùng RQ8–RQ13 và trong phụ lục.

---

## 3. Kết quả thực nghiệm và câu trả lời cho các câu hỏi nghiên cứu

### 3.1 RQ1: *D*<sub>min</sub> mở rộng thế nào theo kích thước bầy *N*?

**Câu trả lời trực tiếp cho RQ1**:
- **Bầy co cụm (`compact`)**: $D_{\min} \equiv 1$ là một hằng số bất biến tuyệt đối trên mọi quy mô ($N = 25$ đến $400$) và mọi thời hạn. Bổ sung thêm chó không làm thay đổi thời gian hoàn thành (trung vị thời gian hoàn thành giữ nguyên từ 1,44 đến 1,74 thời gian lùa cho mọi $D \in [1, 24]$).
- **Bầy phân tán (`wide`, `split`, `outlier_rich`)**: $D_{\min}$ tăng trưởng **dưới tuyến tính (sub-linear)** theo $N$. Ở thời hạn thoải mái ($12\times$), $D_{\min} = 1$ khi $N \le 50$, và chỉ cần 2 đến 3 chó ở $N = 400$.
- **Hệ số góc tăng trưởng log-log**: Trong không gian log-log ($\log_2 D_{\min}$ theo $\log_2 N$), độ dốc dao động từ **0,20 đến 0,50** ở thời hạn $12\times$, và từ **0,30 đến 0,80** ở thời hạn $6\times$. Đàn cừu có tính liên kết đòi hỏi số lượng chó bổ sung ít hơn rất nhiều so với mức tăng $\alpha = 0{,}50$ ($\sqrt{M}$) của các mục tiêu không liên kết.

Bảng 1 tổng hợp lưới ranh giới $D_{\min}$ thực nghiệm (Nghiêm ngặt 100% / Tiếp cận 99%):

| Thời hạn | Bố cục xuất phát | $N = 25$ | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ |
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

![D_min mở rộng theo quy mô N](../figures/fig20_dmin_vs_n.png)

**Hình 1:** Thực nghiệm mở rộng *D*<sub>min</sub> theo kích thước bầy *N* qua các thời hạn và bố cục. Vòng tròn/nét liền: nghiêm ngặt; vuông/nét đứt: tiếp cận 99%. Thanh đứng tô bóng là các khoảng chặn chưa quyết định.

![Thời gian hoàn thành trên bầy Compact](../figures/fig31_compact.png)

**Hình 2:** Thời gian hoàn thành theo số lượng chó *D* trên bầy compact. Trái: Cừu Strömbom với quy tắc đội (thời gian hoàn thành bất biến theo *D*). Phải: Mô hình lực liên tục Kubo (thời gian giảm từ 116 s xuống 30 s khi *D* tăng từ 1 lên 10).

Bảng 2 liệt kê độ dốc tăng trưởng trong không gian log-log:

| Tiêu chí | Thời hạn | Độ dốc `wide` | Độ dốc `split` | Độ dốc `outlier_rich` |
| :--- | :---: | :---: | :---: | :---: |
| **Nghiêm ngặt** | $12\times$ | 0,42 | 0,32 đến 0,42 | 0,42 |
| **Nghiêm ngặt** | $6\times$ | 0,48 ($N \le 200$) | Đi ngang ($N \le 100$) | 0,79 ($N \le 100$) |
| **Nghiêm ngặt** | $3\times$ | 0,79 ($N \le 100$) | Đi ngang ($N \le 100$) | 0,79 đến 1,50 ($N \le 100$) |
| **Tiếp cận 99%** | $12\times$ | 0,20 đến 0,30 | 0,20 | 0,30 |
| **Tiếp cận 99%** | $6\times$ | 0,30 đến 0,42 | Đi ngang ($N \le 100$) | 0,42 đến 0,48 |
| **Tiếp cận 99%** | $3\times$ | 0,62 đến 0,68 | Đi ngang ($N \le 100$) | 0,70 đến 1,10 ($N \le 200$) |

**Ý nghĩa vật lý và giải thích các số liệu trong Bảng 2:**
1. **Khái niệm độ dốc log-log ($\alpha$)**:
   Trong biểu đồ hai trục logarit ($\log_2 D_{\min}$ theo $\log_2 N$), mối quan hệ mở rộng được mô hình hóa dưới dạng hàm lũy thừa: $D_{\min} \propto N^\alpha$, với hệ số góc $\alpha = \frac{\Delta \log_2 D_{\min}}{\Delta \log_2 N}$. Hệ số này đo lường mức độ nhạy cảm của nhu cầu bổ sung chó khi đàn cừu tăng quy mô:
   - **&alpha; = 1,0 (Tuyến tính)**: Cứ tăng gấp đôi số cừu thì phải tăng gấp đôi số chó (tỉ lệ cừu/chó cố định, không có lợi thế quy mô).
   - **&alpha; < 1,0 (Dưới tuyến tính - Sub-linear)**: Bầy cừu càng lớn thì số lượng chó cần thêm càng ít đi (tính kinh tế theo quy mô). Ví dụ với $\alpha = 0{,}33$, khi quy mô bầy $N$ tăng gấp 8 lần ($2^3$), số lượng chó cần thiết chỉ tăng gấp đôi ($2^1 = 2$).
   - **&alpha; = 0 ("Đi ngang" - Flat)**: Nhu cầu chó không hề tăng theo $N$. Trên bố cục `split` ở quy mô $N \le 100$, một chú chó ($D_{\min} = 1$) vẫn hoàn thành tốt nhiệm vụ thu gom cả 3 phân cụm trong thời hạn cho phép.
2. **Lợi thế từ tính gắn kết bầy đàn sinh học (Cohesion)**:
   Trong các bài toán thu gom mục tiêu độc lập không có tính xã hội (chẳng hạn robot gom rác hay lùa các hạt rời rạc trên mặt phẳng), độ dốc lý thuyết tối thiểu là $\alpha = 0{,}50$ ($D \propto \sqrt{M}$). Ngược lại, đối với bầy cừu có tính bầy đàn tự nhiên, ở thời hạn thong thả ($12\times$), độ dốc thực nghiệm chỉ đạt từ **0,20 đến 0,42** (dưới tiêu chí 99% thậm chí chỉ từ **0,20 đến 0,30**). Điều này chứng minh rằng bản năng tự gắn kết bầy đàn của cừu đã san sẻ gánh nặng gom đàn cho bầy chó: khi số cừu tăng lên, lực hút về khối tâm tự nhiên giúp đàn cừu dễ tụ lại hơn, giúp hạn chế tối đa việc phải bổ sung thêm chó.
3. **Tại sao độ dốc lại tăng mạnh khi thời hạn siết chặt?**:
   Khi thời hạn bị rút ngắn từ $12\times$ xuống $3\times$, độ dốc tăng vọt lên **0,62 đến 1,50**. Lý do là khi thời gian quá gấp rút, cừu không còn đủ thời gian tự tìm về bầy, và một chú chó không thể chạy gom tuần tự từng con cừu lạc. Đàn chó bắt buộc phải phân công làm việc song song đồng thời, làm mất đi lợi thế gắn kết tự nhiên và đẩy hệ số mở rộng tiến gần (hoặc vượt qua) mức tăng trưởng tuyến tính.

---

### 3.2 RQ2: Bố cục phân tán so với Quy mô *N*: Yếu tố nào chi phối mạnh hơn?

**Đặt vấn đề thực tế**:
Khi cần triển khai một đội chó chăn cừu (hoặc hệ thống robot tự hành), người điều hành sẽ đối mặt với câu hỏi cốt lõi: *Để ước tính số lượng chó tối thiểu cần dùng, ta nên bận tâm nhiều hơn về việc đàn cừu đông bao nhiêu con (Quy mô $N$), hay về việc đàn cừu đang đứng tản mác thế nào trên bãi cỏ (Bố cục địa hình)?*

**Giải thích khái niệm "Độ biến động theo số lần nhân đôi" (Doublings) trong Bảng 3**:
Do quy mô bầy đàn là một biến số số học liên tục ($N \in [25, 400]$) trong khi bố cục là các hình thái không gian rời rạc (`compact`, `wide`, `split`, `outlier_rich`), để so sánh công bằng mức độ ảnh hưởng của hai yếu tố này trên cùng một thước đo, chúng tôi đo lường độ dao động của $D_{\min}$ theo thang logarit cơ số 2, được gọi là **số lần nhân đôi (doublings)**:

$$
\text{Spread} = \log_2 \left( \frac{D_{\min,\max}}{D_{\min,\min}} \right)
$$

- *Ví dụ trực quan*:
  - Nếu $D_{\min}$ dao động từ 1 chó lên 2 chó: $\log_2(2/1) = 1{,}0$ lần nhân đôi (tăng gấp $2^1 = 2$ lần).
  - Nếu $D_{\min}$ dao động từ 1 chó lên 3 chó: $\log_2(3/1) \approx 1{,}58$ lần nhân đôi (tăng gấp ~3 lần).
  - Nếu $D_{\min}$ giữ nguyên: $0$ lần nhân đôi (hoàn toàn không biến động).

Bảng 3 so sánh định lượng độ biến động theo số lần nhân đôi:

| Tiêu chí | Thời hạn | Biến động giữa các bố cục (Cố định $N$) | Biến động theo $N$ (Cố định bố cục) | Yếu tố chi phối chính |
| :--- | :---: | :---: | :---: | :--- |
| **Nghiêm ngặt** | $12\times$ | 0,68 lần nhân đôi | 1,19 lần nhân đôi | Quy mô đàn cừu $N$ |
| **Nghiêm ngặt** | $6\times$ | 1,67 lần nhân đôi | 1,69 lần nhân đôi | Tương đương / Quy mô $N$ |
| **Nghiêm ngặt** | $3\times$ | 0,76 lần nhân đôi | 0,97 lần nhân đôi | Quy mô đàn cừu $N$ |
| **Tiếp cận 99%** | $12\times$ | 0,50 lần nhân đôi | 0,75 lần nhân đôi | Quy mô đàn cừu $N$ |
| **Tiếp cận 99%** | $6\times$ | 0,92 lần nhân đôi | 1,30 lần nhân đôi | Quy mô đàn cừu $N$ |
| **Tiếp cận 99%** | $3\times$ | 1,25 lần nhân đôi | 1,28 lần nhân đôi | Tương đương / Quy mô $N$ |

**Ý nghĩa và phát hiện cốt lõi từ Bảng 3**:
1. **Quy mô đàn cừu $N$ là yếu tố chi phối bậc nhất**:
   Trong hầu hết các điều kiện khảo sát, cột "Biến động theo $N$" luôn lớn hơn cột "Biến động giữa các bố cục" (trung bình dao động từ 0,75 đến 1,69 lần nhân đôi so với 0,50 đến 1,67 lần nhân đôi). Điều này có nghĩa là: việc tăng kích thước bầy từ 25 lên 400 con cừu sẽ làm thay đổi số chó cần thiết nhiều hơn và ổn định hơn so với việc xáo trộn các kiểu địa hình.
2. **Hiệu ứng địa hình thực chất là một "công tắc nhị phân"**:
   Phần lớn sự biến động giữa các bố cục (cột "Biến động giữa các bố cục") chỉ xuất phát từ bước nhảy duy nhất: từ bố cục **đã gom sẵn (`compact`)** sang **ba bố cục phân tán**.
   - Trên bầy `compact`, cừu đã kết nối thành một khối nên $D_{\min} \equiv 1$ bất biến trên mọi quy mô và thời hạn.
   - Nhưng một khi đàn cừu đã bị tản mác, thì việc chúng tản mác theo kiểu rải đều (`wide`) hay có vài con cừu lạc xa (`outlier_rich`) hầu như **không làm thay đổi số lượng chó cần thiết** (sự chênh lệch giữa `wide` và `outlier_rich` hiếm khi vượt quá 1 chú chó).

---

### 3.3 RQ3: Áp lực thời hạn làm dịch chuyển *D*<sub>min</sub> ra sao?

**Câu trả lời trực tiếp cho RQ3**:
- Thời hạn là tham số chi phối bậc một. Khi siết chặt thời hạn, toàn bộ đường cong tin cậy bị tịnh tiến sang phía bên phải.
- Mức độ dịch chuyển mang tính **phi tuyến**: nới lỏng từ $6\times$ lên $12\times$ thời gian lùa chỉ thay đổi $D_{\min}$ tối đa 1 chó, nhưng siết chặt từ $6\times$ xuống $3\times$ tạo ra sự gia tăng bùng nổ (ví dụ trên `wide` $N = 400$ dưới tiêu chí 99%, $D_{\min}$ tăng vọt từ 2–3 lên 5–6 chó; trên `split` $N \ge 200$, thời hạn ngặt nghèo dẫn đến thất bại trên toàn bộ các cỡ đội khảo sát).
- **Cơ chế vật lý**: Tác tử có vận tốc tối đa hữu hạn ($v_{\mathrm{sheep}} = 1{,}0$, $v_{\mathrm{dog}} = 1{,}5$). Ở thời hạn $12\times$, một chú chó có thừa thời gian để thu gom tuần tự từng con cừu rải rác. Ở thời hạn $3\times$, gom tuần tự là bất khả thi về mặt động học; đàn chó bắt buộc phải phân công gom song song đồng thời tất cả các cá thể tản mác.

![Tác động của thời hạn lên đường cong thành công](../figures/fig29_deadline.png)

**Hình 3:** Tác động của thời hạn. Trái/Giữa: Đường cong thành công ở các thời hạn 12&times;, 6&times;, và 3&times;. Phải: Giá trị *D*<sub>min</sub> biểu diễn trực tiếp theo hệ số thời hạn *m*.

---

### 3.4 RQ4: Tiêu chí thành công và Hiệu ứng cá thể lạc đàn

**Câu trả lời trực tiếp cho RQ4**:
- Tiêu chí tiếp cận 99% đòi hỏi số chó bằng hoặc ít hơn đáng kể so với tiêu chí 100% nghiêm ngặt trên toàn bộ 34 ô phân tán khảo sát, giảm từ 1 đến 6 chó ở $N \ge 100$.
- Có 6 ô ở quy mô bầy lớn thất bại hoàn toàn dưới tiêu chí nghiêm ngặt nhưng đạt được $D_{\min}$ xác định dưới tiêu chí 99%.
- **Cơ chế cá thể lạc đàn (Straggler Mechanism)**: Trong 95% số lượt thất bại nghiêm ngặt của các đội có $D \ge 6$, đàn chó thực tế đã đưa được 99% số cừu vào đích từ rất sớm. Thất bại nghiêm ngặt xảy ra do đàn chó phá vỡ đội hình lùa để quay sang săn đuổi 1–2 con cừu lạc đàn còn lại bên ngoài. Khi áp sát, đàn chó vô tình đứng vào vị trí giữa bầy cừu và tâm đích, đẩy ngược toàn bộ khối cừu đã ổn định ra khỏi vòng tròn mục tiêu.
- Chó chạy chậm hơn ($v_{\mathrm{dog}} = 1{,}15$) loại bỏ được xung lực vượt đà này, giúp tỷ lệ thành công nghiêm ngặt tăng từ thất bại hoàn toàn (`none`) lên $D_{\min} = 6$ ở bố cục `outlier_rich` ($N = 400$).

![Tỷ lệ thành công Nghiêm ngặt so với Tiếp cận 99%](../figures/fig30_strict_vs_99.png)

**Hình 4:** So sánh tỷ lệ thành công giữa hai tiêu chí trên cùng hạt giống. Vùng tô bóng chứa các ô đạt độ tin cậy &ge; 90% dưới tiêu chí 99% nhưng thất bại dưới tiêu chí nghiêm ngặt.

![Phân tích vi mô hiệu ứng cá thể lạc đàn](../figures/fig22_straggler.png)

**Hình 5:** Phân tích vi mô hiệu ứng cá thể lạc đàn. Trái: Tỷ lệ các lượt chạy *D* &ge; 6 đưa được 99% cừu vào đích so với thành công nghiêm ngặt. Phải: Quỹ đạo chuỗi thời gian cho thấy chó nhanh (1,5 m/s) đẩy bật bầy cừu ra ngoài đích trong khi chó chậm (1,15 m/s) duy trì bầy ổn định trong đích.

---

### 3.5 RQ5: Những quy luật nào đứng vững trước các phân tích độ nhạy?

**Câu trả lời trực tiếp cho RQ5**:
- **Dưới tiêu chí 99%**: Các quy luật mở rộng có tính vững chắc vượt trội. Dù thay đổi hình học thả chó (`handler`, `ring`, `arcs`), cự ly xuất phát (15, 30, 60 m), vận tốc chó (1,15 so với 1,50), hay áp dụng bộ tham số thực địa GPS của cừu, giá trị $D_{\min}$ vẫn duy trì ổn định trong phạm vi **&plusmn;1 chó** so với mốc cơ sở trên mọi ô.
- **Dưới tiêu chí nghiêm ngặt**: Giá trị tuyệt đối biến động dữ dội gấp 3 lần trở lên, do các quy ước thiết lập làm thay đổi quỹ đạo nhạy cảm của con cừu cuối cùng khi vào đích.
- **Hình học đích**: Việc thu hẹp bán kính đích ($1{,}5 R_f$) là biến thể duy nhất làm tăng thực sự $D_{\min}$ dưới cả hai tiêu chí (nâng `wide` $N = 400$ từ 2–3 lên 5–6 chó).

![Biểu đồ nhiệt phân tích độ nhạy](../figures/fig24_sensitivity.png)

**Hình 6:** Phân tích độ nhạy trên các biến thể thực nghiệm ở thời hạn 6&times;. Tiêu chí nghiêm ngặt (trên) biến động mạnh; tiêu chí tiếp cận 99% (dưới) thể hiện tính ổn định cao.

---

### 3.6 RQ6: Mô hình đối chứng không phối hợp (FAT) có đạt được *D*<sub>min</sub> hữu hạn?

**Câu trả lời trực tiếp cho RQ6**:
- Hoàn toàn không. Một quy tắc không có tầng phối hợp phân công hay lực đẩy không gian sẽ thất bại hoàn toàn khi đàn cừu mở rộng quy mô.
- Mặc dù FAT thành công ở đàn nhỏ ($N \le 100$), mô hình này đạt **0 ô tin cậy** ở $N \ge 200$ trên mọi bố cục phân tán, và thất bại ngay cả trên bầy `compact` $N = 400$ nơi `strombom_multi` chỉ cần 1 chó.
- **Lý do vật lý**: Do toàn bộ chó có cùng góc nhìn toàn cục, mọi chú chó tính toán ra cùng một mục tiêu ($\arg\max_i \lVert \mathbf{x}_i - \mathbf{x}_{\text{goal}} \rVert$). Khi thiếu lực đẩy né tránh nhau, đàn chó dồn cục lại thành một khối duy nhất (`dog_overlap` $> 80\%$). Bổ sung thêm chó vào mô hình FAT không đem lại bất kỳ lợi ích song song hóa nào. Điều này chứng minh rằng việc $D_{\min}$ duy trì ở mức hữu hạn ở quy mô lớn là thuộc tính xuất hiện từ tầng phối hợp đội chứ không phải do số lượng cơ cấu chấp hành.

Bảng 5 so sánh $D_{\min}$ giữa FAT và `strombom_multi` ở thời hạn $6\times$:

| Bố cục xuất phát | $N = 25$ | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `compact` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / [12] (1 / 1) |
| `wide` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / none (3 / 2) | none / none ([9] / 2–3) |
| `split` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / none (none / [1]) | none / none (none / [5]) |
| `outlier_rich` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 2 / 2 (3 / 2) | none / none ([12] / 2–3) | none / none (none / 3) |

![So sánh FAT với Quy tắc đội strombom_multi](../figures/fig26_fat.png)

**Hình 7:** Tỷ lệ thành công theo số lượng chó *D* giữa strombom_multi (xanh lam) và FAT (cam). Đường cong của FAT đi ngang và hoàn toàn không cải thiện khi tăng số lượng chó.

---

### 3.7 RQ7: Vượt quá *D*<sub>min</sub>: Đủ chó (*D*<sub>sat</sub>), chi phí vận hành và áp lực lên đàn cừu

Khi đã xác định được quy mô đội tối thiểu $D_{\min}$, một câu hỏi thực tiễn quan trọng được đặt ra cho người chăn thả hoặc người vận hành robot tự hành:
*Nếu chúng ta đưa thêm chó vào bãi cỏ vượt quá $D_{\min}$, việc đó có giúp rút ngắn thời gian lùa cừu hay không? Chi phí vận hành tăng lên thế nào, đàn cừu có bị căng thẳng quá mức không, và liệu việc quá nhiều chó có gây chen chúc làm vỡ trận (thất bại nhiệm vụ) hay không?*

Để trả lời, chúng tôi phân tích tập dữ liệu 11 giao thức theo tiêu chí 99% (gồm các lưới chính, mô hình đối chứng FAT và 7 biến thể độ nhạy), kết hợp chạy lại chi tiết 164 lượt mô phỏng mẫu để đo lường các chỉ số vi mô từng nhịp tick. Mọi lượt chạy lại đều tái hiện hoàn hảo kết quả thành công và số nhịp tick đã lưu.

#### 1. Ngưỡng bão hòa tốc độ (*D*<sub>sat</sub>)
- **Định nghĩa**: *D*<sub>sat</sub> là số lượng chó nhỏ nhất đạt độ tin cậy mà từ đó trở đi, việc bổ sung thêm chó không còn mang lại sự cải thiện tốc độ có ý nghĩa thống kê (thời gian lùa bắt đầu đi ngang).
- **Kết quả thực nghiệm**:
  - *Trên bầy co cụm (`compact`) và quy mô nhỏ ($N \le 50$)*: *D*<sub>sat</sub> = 1 ngay từ đầu. Một chú chó đã đạt tốc độ tối đa; việc thêm chó không thể làm cừu di chuyển nhanh hơn vận tốc đi bộ tự nhiên ($1{,}0$ m/s).
  - *Trên bầy phân tán ở thời hạn trung bình ($6\times$)*: *D*<sub>sat</sub> dao động từ 2 đến 7 chú chó ở $N = 100$–400 (ví dụ: bầy `outlier_rich` $N = 100$ bão hòa ở *D*<sub>sat</sub> = 3; bầy `wide` $N = 400$ ở *D*<sub>sat</sub> = 5).
  - *Các ô tham số chưa ngã ngũ*: Trong các lượt chạy đầu, các phép so sánh thời gian hoàn thành chưa giải quyết dứt điểm trên 6 trong số 18 đường cong phân tán do tài nguyên được ưu tiên cho việc tìm $D_{\min}$ (`decide_finish_times: false`), nên *D*<sub>sat</sub> được ghi nhận dưới dạng khoảng chặn (ví dụ `wide` $N = 200$ là 3–24). Lượt bổ sung sau đó đã quyết định phần lớn (mục 3.8): trên `wide`, *D*<sub>sat</sub> giờ là 1, 1, 1, 2, 3, 3, 4, 5 từ $N = 25$ đến $400$. Ở $6\times$ nó vẫn là một khoảng trên 5 trong 23 đường cong phân tán (`outlier_rich` $N = 50$, 283, 400, 566; `wide` 566).

#### 2. Chi phí lãng phí khi vượt ngưỡng bão hòa (*D* > *D*<sub>sat</sub>)
- **Thêm chó không rút ngắn thời gian, nhưng chi phí tăng tỉ lệ thuận**:
  - Khi tăng số chó vượt qua *D*<sub>sat</sub>, thời gian đưa đàn cừu về đích gần như giữ nguyên: dao động trong khoảng **0,96 đến 1,01 lần** thời gian tại mốc *D*<sub>sat</sub> (189 ô đạt độ tin cậy trên một *D*<sub>sat</sub> đã quyết định, chín quy mô bầy). Tức là việc tăng thêm hàng chục con chó chỉ giúp về đích nhanh hơn tối đa 4%, và đôi khi chậm hơn khoảng 1%.
  - Tuy nhiên, **tổng thời gian làm việc của bầy chó** (tổng thời gian tích lũy $\mathrm{dog\_time} = D \times T$) và tổng quãng đường chạy của cả đội lại tăng tuyến tính tỉ lệ thuận với *D* / *D*<sub>sat</sub>.
  - *Minh họa thực tế*: Trên bầy compact, triển khai 24 chú chó tiêu tốn năng lượng gấp 24 lần so với 1 chú chó, nhưng đàn cừu vẫn mất cùng một khoảng thời gian (~140 giây) để về tới đích.

Bảng 6 tổng hợp chi phí vận hành ở mốc gấp đôi ngưỡng bão hòa (2 *D*<sub>sat</sub>) và ở đội hình tối đa ($D = 24$) so với mốc *D*<sub>sat</sub> (trên các bầy phân tán ở thời hạn $6\times$):

| Bố cục xuất phát, Quy mô *N* | Ngưỡng *D*<sub>sat</sub> | Tại 2 *D*<sub>sat</sub>: Thời gian lùa / Thời gian chó | Tại *D* = 24: Thời gian lùa / Thời gian chó |
| :--- | :---: | :---: | :---: |
| `wide`, $N = 200$ | 3 | 0,97 / 1,94 | 0,96 / 7,70 |
| `wide`, $N = 400$ | 5 | 0,97 / 2,32 (tại $D = 12$) | 0,96 / 4,61 |
| `outlier_rich`, $N = 100$ | 3 | 0,99 / 1,98 | 0,98 / 7,85 |
| `outlier_rich`, $N = 400$ | 6–24 | 0,96 / 1,91 | 0,94 / 3,74 |
| `split`, $N = 100$ | 4 | 0,99 / 1,98 | 0,99 / 5,91 |

*Ý nghĩa Bảng 6*: Tại $D = 24$, thời gian lùa cừu chỉ nhanh hơn từ 1% đến 6% ($0{,}94 - 0{,}99$), nhưng tổng công suất và năng lượng tiêu hao của bầy chó lại bị đội lên từ **3,7 đến 7,9 lần** ($3{,}74 - 7{,}85$). Giá trị sau lượt bổ sung thời gian hoàn thành (`uv run cli/dmin_tables.py effort dmin_f99_m6`).

#### 3. Áp lực tâm lý và mức độ hoảng sợ của đàn cừu (Flock Stress)
Nhiều người e ngại rằng một bầy chó đông đúc sẽ gây hoảng loạn và kiệt sức cho đàn cừu. Tuy nhiên, dữ liệu vi mô từng giây cho thấy bức tranh hoàn toàn khác:
- **Tổng thời gian hoảng sợ của mỗi con cừu thực chất giảm đi**: Một con cừu ở trạng thái tháo chạy khi có bất kỳ chú chó nào nằm trong cự ly đe dọa $r_s = 65$ m. Khi tăng số chó từ $D_{\min}$ lên *D*<sub>sat</sub>, do bầy chó thu gom cừu lạc nhanh hơn nên thời gian tháo chạy của mỗi con cừu giảm rõ rệt (trên `wide` $N = 400$, thời gian chạy trốn trung bình của mỗi cá thể giảm từ 485 giây ở $D = 3$ xuống còn 359 giây ở $D = 6$). Khi vượt quá *D*<sub>sat</sub>, con số này đi ngang (361 giây ở $D = 12$).
- **Tỉ lệ đàn chạy trốn tức thời tăng lên**: Tại một thời điểm bất kỳ, bầy chó đông hơn sẽ giăng thành vòng cung rộng hơn, khiến một tỉ lệ lớn hơn trong đàn cừu cùng chạy trốn một lúc (trung bình 68% số cừu chạy trốn ở $D = 3$, tăng lên 84% ở $D = 12$). Nhưng vì toàn bộ cuộc lùa kết thúc nhanh hơn, tổng lượng stress tích lũy không hề bị gia tăng.
- **Không xảy ra va chạm nguy hiểm**: Nhờ quy tắc dừng giữ khoảng cách ($3 r_a = 6$ m), thời gian chó áp sát cừu ở cự ly dưới 6 m luôn duy trì dưới 1,3 giây trên mỗi con cừu trong suốt hành trình và hoàn toàn không tăng lên khi có thêm chó.

#### 4. Khả năng chống vỡ trận: Không có ngưỡng quá tải (*D*<sub>overcrowd</sub>) dưới tiêu chí 99%
- Dưới tiêu chí tiếp cận 99%, trên toàn bộ 11 thư mục dữ liệu khảo sát (lưới chính, mô hình đối chứng FAT và 7 biến thể độ nhạy), **không xuất hiện bất kỳ ngưỡng quá tải $D_{\mathrm{overcrowd}}$ nào** lên tới $D = 24$ trên năm kích thước bầy ban đầu.
- Không có bất kỳ đường cong nào bị tụt giảm độ tin cậy sau khi đã đạt chuẩn: một khi quy mô đội đã thành công, việc bổ sung thêm chó không bao giờ làm nhiệm vụ bị thất bại. Hiện tượng đàn chó bị "đóng băng" vì quá đông trên bố cục `split` ở thời hạn gấp ($3\times$) dưới tiêu chí nghiêm ngặt đã hoàn toàn biến mất dưới tiêu chí 99%. *Đính chính từ lưới dày hơn (mục 3.8)*: ở kích thước được thêm `split` $N = 141$ ($6\times$), $D = 4$ thành công 0,80 số lượt trong khi các quy mô đội bên cạnh đạt độ tin cậy, một lần sụt giảm duy nhất, lại trên `split`.
- Thêm chó làm tốc độ hoàn thành chậm đi trên `split` và trên mô hình đối chứng FAT. Khi đã bổ sung các phép so sánh thời gian (mục 3.8), `split` ở $12\times$ chậm hơn khi có nhiều chó ở mọi $N$ từ 200 đến 566 (ví dụ $N = 400$: 950–1040 s với $D \ge 9$ so với 839 s ở $D = 5$), dù vẫn hoàn thành ổn định. `wide` và `outlier_rich` không bị chậm như vậy.

![Chi phí của chó vượt quá D_sat](../figures/fig33_effort.png)

**Hình 8:** Đánh giá chi phí khi vượt quá ngưỡng *D*<sub>sat</sub> ở thời hạn 6&times; (tiêu chí 99%). Trái: Thời gian hoàn thành so với mốc *D*<sub>sat</sub> giữ sát mức 1. Phải: Tổng thời gian làm việc của chó tăng tuyến tính theo tỉ số *D* / *D*<sub>sat</sub>.

![Áp lực lên bầy](../figures/fig34_pressure.png)

**Hình 9:** Đánh giá áp lực tâm lý lên đàn cừu (12 hạt giống mỗi ô, dữ liệu `dmin_f99_m6`). Trái: Số giây tháo chạy của mỗi con cừu giảm mạnh tới mốc *D*<sub>sat</sub> rồi đi ngang. Phải: Tỉ lệ phần trăm đàn cừu tháo chạy tức thời tăng theo số lượng chó *D*.

Kết quả về áp lực một phần xuất phát từ các đặc tính chuẩn mực của mô hình Strömbom: lực đẩy từ nhiều chú chó lên một con cừu được chuẩn hóa độ dài về 1 (cơ chế blending), nên sự hiện diện của chú chó thứ hai ở gần không làm tăng độ mạnh của lực đẩy; đồng thời tầm nhìn $r_s = 65$ m rộng gấp khoảng 7 lần bán kính bầy ở $N = 100$, nên chỉ vài chú chó đã đủ để toàn bầy cảm nhận được sự hiện diện của người chăn. Toàn bộ bảng số liệu chi tiết và câu lệnh phân tích được lưu trữ tại [`results_tables.md`](results_tables.md) (mục "D_sat, effort, zones and methods, 99 percent").

### 3.8 RQ8: Tăng trưởng theo *N* trên lưới dày hơn, *D*<sub>sat</sub> và hình dạng đường cong

Các lượt chạy chính theo tiêu chí 99% ở $12\times$ và $6\times$ được mở rộng thêm bốn kích thước bầy, $N = 71, 141, 283$ (các điểm giữa theo thang log của 50–400) và $566 = 400\sqrt{2}$, để mọi kích thước trên $N = 50$ đều cách nhau một bước $\sqrt{2}$ và có trọng số như nhau trong phép khớp. Mỗi kích thước thêm vào đều hiệu chuẩn suôn sẻ (sáu lượt hiệu chuẩn khớp nhau trong phạm vi 2%). Trên mức đó, mô hình không còn cho bầy một kích thước riêng: ở $N = 630$ một lượt xuất phát thưa vẫn lớn hơn 17%, ở 700 lượt xuất phát thưa giữ nguyên kích thước ban đầu, ở 800 phép kiểm tra hiệu chuẩn thất bại. Các phép so sánh thời gian hoàn thành được bổ sung trong cùng lần chạy tiếp (`decide_finish_times: true`). Việc hiệu chuẩn lại trả về mọi $R_f$ trước đó không đổi.

**Câu trả lời trực tiếp cho RQ8**:
- **Các độ dốc giờ đã hẹp.** Trên chín kích thước, độ dốc log-log của $D_{\min}$ theo $N$ là 0,27–0,38 (`wide`) và 0,28–0,38 (`outlier_rich`) ở $12\times$, và 0,38–0,61 và 0,40–0,58 ở $6\times$. Ở $12\times$ mức tăng vẫn nằm dưới quy luật căn bậc hai của các mục tiêu không liên kết (0,5); ở $6\times$ nó nằm vắt qua quy luật này.
- ***D*<sub>sat</sub> tăng nhanh gấp khoảng hai lần $D_{\min}$.** Trên `wide`, *D*<sub>sat</sub> là 1, 1, 1, 2, 3, 3, 4, 5 từ $N = 25$ đến $400$ và 7–24 ở $566$ (độ dốc 0,70–0,91), như nhau ở cả hai thời hạn. Khoảng cách giữa đội đạt độ tin cậy và đội nhanh nhất có thể nới rộng theo $N$.
- **Đến $N = 566$, dữ liệu chưa phân biệt được tăng trưởng đều với một đường cong chững lại.** Một hàm lũy thừa và một đường cong bão hòa, khớp bằng hợp lý cực đại cho dữ liệu kiểm duyệt khoảng (interval-censored), đều đi qua mọi khoảng chặn $D_{\min}$ ở cả hai thời hạn (tỉ số hợp lý 1). Mọi đường cong thuộc một trong hai dạng mà khớp được đều cho phép từ 1,5 đến 6,7 chó ở $N = 1600$ ($12\times$). Chỉ $N$ lớn hơn mới tách được hai dạng này (mục 3.13).

| $N$ | 25 | 50 | 71 | 100 | 141 | 200 | 283 | 400 | 566 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `wide`, $12\times$ | 1 | 1 | 1 | 1 | 2 | 1–2 | 2 | 2 | 2–3 |
| `outlier_rich`, $12\times$ | 1 | 1 | 1 | 1–2 | 2 | 2 | 2 | 2 | 2–3 |
| `wide`, $6\times$ | 1 | 1 | 1 | 1 | 2 | 2 | 2–3 | 2–3 | 3–7 |
| `outlier_rich`, $6\times$ | 1 | 1 | 1 | 2 | 2 | 2–3 | 2–3 | 3 | 3–6 |
| *D*<sub>sat</sub> `wide`, $6\times$ | 1 | 1 | 1 | 2 | 3 | 3 | 4 | 5 | 7–24 |

![D_min trên chín kích thước và phạm vi của hai dạng](../figures/fig35_growth_fits.png)

**Hình 10:** $D_{\min}$ theo $N$ trên chín kích thước (thanh: khoảng chặn). Sau $N = 566$: phạm vi mà mỗi dạng đã khớp cho phép. Hai phạm vi gần như trùng nhau hoàn toàn.

### 3.9 RQ9: Phần nào của quy tắc đội có tác dụng, và một mô hình có thời gian hoàn thành giảm theo *D*

FAT thiếu cả tầng đội (phân công cừu lạc, vị trí lùa) lẫn công tắc gom/lùa của người chăn trong bài báo gốc, nên không thể cho biết phần nào có tác dụng. Một đội gồm các người chăn độc lập theo bài báo, mỗi chó tự chạy quy tắc một chó (`dmin_f99_indep`, cùng nhiệm vụ với `dmin_f99_m6`), có công tắc nhưng không có tầng đội. Với một chó, nó chính xác là lượt chạy của bài báo (đã kiểm thử).

**Câu trả lời trực tiếp cho RQ9**:
- **Công tắc gom/lùa đưa một đội tới $N = 200$; tầng đội là thứ giúp đạt được $N = 400$.** Các người chăn độc lập theo bài báo đạt được một $D_{\min}$ trên mọi bố cục phân tán đến $N = 200$, nơi FAT không có, và không có ở $N = 400$, nơi quy tắc đội cần 2–3 chó.
- **Trên `split` $N = 200$, các chó độc lập làm tốt hơn quy tắc đội** (1–3 so với một cận dưới chưa đóng [1]), phù hợp với mục 4.1: quy tắc đội gửi các chó đi gom tới cùng một cụm.
- **Kubo, với $D$ đến 24**: $D_{\min} = 1$ ở $N = 25$–100 như trước; *D*<sub>sat</sub> nằm giữa 16 và 24. Ở $N = 100$, thời gian hoàn thành giảm từ 115 s với một chó xuống 29 s với mười chó và 25 s với 24 chó: phần lớn lợi ích đã có khi $D = 10$. Điều này ngược với bầy Strömbom, có thời gian hoàn thành trên bố cục compact không phụ thuộc vào $D$.

| `strombom_multi` / độc lập / FAT, 99%, $6\times$ | $N = 200$ | $N = 400$ |
| :--- | :---: | :---: |
| `wide` | 2 / 2–3 / none | 2–3 / none / none |
| `outlier_rich` | 2–3 / 3 / none | 3 / none / none |
| `split` | [1] / 1–3 / none | [5] / none / none |

### 3.10 RQ10: Quá nhiều chó: Giữ bầy, và chó chiếm chỗ

Tác hại của việc có thêm người chăn đã được đo trong bài toán giữ bầy (containment), chưa phải trong bài toán lùa trên đồng trống (Green et al. 2022). Ở đây có hai thay đổi để kiểm tra điều đó. **Nhiệm vụ giữ bầy** chỉ tính là đạt đích sau khi 99% số cừu đã ở yên bên trong trong một khoảng thời gian lùa; trong lúc đích đang đạt, các chó rút ra ngoài cự ly đe dọa của cừu để bầy gặm cỏ. Không có bước rút lui này, quy tắc đội hoàn toàn không giữ được bầy (0 trên 10 ở mọi ô đã kiểm tra: bầy bị lùa xuyên qua đích). **Chó chiếm chỗ** không thể bước tới gần nhau dưới 2 m (khoảng cách trùng (twin distance) của mô hình), nên vòng cung lùa chỉ chứa được một số chó giới hạn: theo hình học của vòng cung, khoảng $D_{\mathrm{cap}} = 7, 9, 10, 11, 12$ ở $N = 25$ đến $400$.

**Câu trả lời trực tiếp cho RQ10**:
- **Giữ bầy có tác dụng từ $N = 100$ và thất bại ở $N \le 50$ với mọi $D$.** Một chó đang rút lui vẫn ở trong phạm vi $r_s = 65$ m khoảng 40 s trong lúc đi ra xa, và bầy đang tháo chạy bị đẩy ra khỏi đích bán kính 12–14 m. Đây là khoảng cách tháo chạy của mô hình so với một đích nhỏ, không phải hiệu ứng của quy mô đội. Ở $N \ge 100$, $D_{\min}$ trùng với nhiệm vụ lùa (wide 1, 2, 3 ở $N = 100, 200, 400$).
- **Với chó dạng điểm, không có tác hại đã quyết định nào đến $D = 24$.** `outlier_rich` $N = 400$ trượt từ 0,96–0,97 ở $D = 4$–6 xuống 0,84–0,92 ở $D \ge 7$, chưa quyết định.
- **Với chó chiếm chỗ, nhiều chó hơn làm nhiệm vụ thất bại.** Trên `outlier_rich` $N = 400$, mọi đội từ $D = 9$ đến 24 đều được quyết định là không đạt độ tin cậy (cận trên dưới 0,90; tỉ lệ thành công 0,77 ở 9, 0,65 ở 11–12, 0,50 ở 16), trong khi $D = 3$–6 thành công ở mức 0,93–0,94. Điểm khởi phát ($D = 9$) đến trước ước tính theo vòng cung (12). Trên `wide` và `compact`, cùng quy tắc này không gây hại đến 24: các chó không tìm được vị trí thì đứng yên (một phần ba số chó ở $D = 24$) và thời gian hoàn thành không đổi.

![Giữ bầy với chó dạng điểm và với chó cách nhau 2 m](../figures/fig36_spacing.png)

**Hình 11:** Nhiệm vụ giữ bầy ở $N = 400$. Trái: `wide`, không có tác hại. Phải: `outlier_rich`, tỉ lệ thành công giảm từ $D = 9$ khi chó chiếm chỗ.

### 3.11 RQ11: Tính liên kết

Quy luật mở rộng duy nhất đã được công bố (căn bậc hai của số mục tiêu) dành cho các mục tiêu không có tính liên kết. Tính liên kết được thay đổi qua trọng số lực hút của cừu $c$ (1,05 trong bài báo) và số hàng xóm mà một con cừu bị hút về. Với loại cừu này, không thể tạo một bầy yếu hơn bầy của bài báo: ở $c = 0{,}8$–0,9 lực đẩy của một chó thắng lực hút và bầy không có kích thước ổn định, và khi số hàng xóm ít hơn một nửa bầy thì bầy tách rời. Mức yếu hơn duy nhất ổn định được là $n = 0{,}5N$ (từ $N = 50$).

**Câu trả lời trực tiếp cho RQ11**:
- **Tính liên kết mạnh hơn hầu như không làm thay đổi mức tăng**: trên $N = 50$–400 (`wide`), độ dốc 0,30 ở $c = 1{,}3$, 1,6, 2,0 so với 0,30–0,40 ở giá trị của bài báo; một bầy chặt hơn tiết kiệm nhiều nhất một chó.
- **Tính liên kết yếu hơn làm mức tăng dốc hơn**: ở $n = 0{,}5N$ độ dốc `wide` là 0,40–0,70, tiến tới và vượt mức 0,5 của quy luật không liên kết, và `split` trở nên khó hơn nhiều ($D_{\min}$ 3–4 ở $N = 200$, 4–5 ở 400). Kết luận này dựa trên mức yếu hơn duy nhất mà mô hình tạo được.

| `wide`, 99%, $12\times$ | $N = 50$ | 100 | 200 | 400 | độ dốc |
| :--- | :---: | :---: | :---: | :---: | :---: |
| $n = 0{,}5N$ (yếu hơn) | 1 | 1 | 2 | 2–4 | 0,40–0,70 |
| $c = 1{,}05$ (bài báo) | 1 | 1 | 1–2 | 2 | 0,30–0,40 |
| $c = 1{,}3$, 1,6, 2,0 | 1 | 1 | 1 | 2 | 0,30 |

### 3.12 RQ12: Những gì một chó nhìn thấy

Mọi robot hoặc drone chăn dắt đều cảm nhận cục bộ. Ở đây mỗi chó chỉ biết những con cừu trong tầm cảm nhận của nó; với `communication` nó còn biết những gì các chó khác thấy (không chó nào, các chó trong tầm, hoặc cả đội). Một chó không thấy con cừu nào sẽ đi về tâm bầy mà nó biết lần cuối. Một tầm lớn hơn bãi cỏ cho kết quả đúng như lượt chạy toàn cục (đã kiểm thử).

**Câu trả lời trực tiếp cho RQ12**:
- **Từ tầm 30 m, góc nhìn cục bộ tốn khoảng một chó ở $N = 200$ và không tốn gì ở $N \le 100$** (`wide` $N = 200$: 2 với góc nhìn toàn cục, 3 ở các tầm 30–65, 2–3 ở 100).
- **Ở 15 m, thêm chó không bù lại được**: `wide` $N = 50$ không có đội nào đạt độ tin cậy đến 16 chó, $N = 100$ cần ít nhất 6.
- **Chia sẻ với cả đội lấy lại được con chó bị mất** (`wide` $N = 200$ ở tầm 65: 3 khi không chia sẻ, 3 khi chia sẻ với các chó trong tầm, 2 khi chia sẻ với cả đội, bằng góc nhìn toàn cục).

![D_min theo tầm cảm nhận, và chia sẻ](../figures/fig37_view.png)

**Hình 12:** Trái: $D_{\min}$ theo tầm cảm nhận của mỗi chó (thanh: khoảng chặn; tam giác: cận dưới). Phải: tỉ lệ thành công theo $D$ ở tầm 65 khi có và không có chia sẻ.

### 3.13 RQ13: *N* lớn, và một giới hạn của quy tắc lùa

Trên mép hiệu chuẩn, bán kính bầy được áp đặt: giữ nguyên mật độ của bầy $N = 566$, $R_f(N) = R_f(566)\sqrt{N/566}$, cho $N = 800$ đến $3200$ ở $12\times$. Mọi kết quả trên 566 là kết quả ở mật độ áp đặt đó.

**Câu trả lời trực tiếp cho RQ13**:
- **Theo quy tắc của bài báo, không đội nào với bất kỳ quy mô nào lùa được một bầy trên $N \approx 1056$.** Bài báo đặt chó lùa phía sau tâm bầy một khoảng $r_a\sqrt{N}$; khoảng cách đó vượt cự ly đe dọa của cừu $r_s = 65$ m tại $N = (r_s/r_a)^2 = 1056$. Ở $N = 1131$, chó đứng cách con cừu gần nhất 59 m, chỉ 140–240 trong số 1131 con cừu cảm nhận được nó, phần còn lại của bầy giữ chúng lại, và tâm bầy di chuyển chưa tới 3 m trong 400 nhịp tick. Mọi chó thêm vào đều đứng trên cùng một vòng cung. Không $D$ nào đến 12 đạt độ tin cậy ở $N = 1131$–3200, kể cả compact, trong khi $N = 566$ và 800 hoạt động như dự kiến (compact 1; wide 2–3 và 3).
- **Mật độ áp đặt ảnh hưởng tới hai chó**: `wide` $N = 800$ cần 4–5 chó ở mật độ gấp đôi, 3 ở mật độ cơ sở và 3 ở mật độ một nửa.
- **Khi giới hạn điểm lùa trong tầm với ($r_s - r_a = 63$ m, một biến thể được ghi rõ của quy tắc trong bài báo), các bầy trên 1056 có thể được lùa, và bầy phân tán khi đó cần nhiều chó hơn hẳn**: `wide` cần 3 chó ở $N = 800$, 5–9 ở 1131 và hơn 12 ở 1600 (12 chó thành công 0,72), trong khi `compact` cần 1, 1 và 2. Ở $N = 3200$ (2 giờ chạy trước khi kích thước này bị bỏ vì chi phí), một con chó lùa được bầy compact trong mọi lượt (42 trên 42) và không đội nào từ 2 đến 12 chó lùa được bầy wide (0 trên 58). Mức tăng này dốc hơn những gì cả hai đường cong khớp dưới ngưỡng cho phép.
- **Mật độ áp đặt lỏng hơn bầy mà các chó thực sự lùa**: trên $N = 566$, bầy compact co lại còn 0,53–0,82 bán kính áp đặt, nên đích và quãng lùa được định cỡ cho một bầy lỏng hơn bầy được lùa. Cả giới hạn điểm lùa và bán kính áp đặt đều là lựa chọn; các con số trên $N = 1056$ là kết quả theo các lựa chọn đó, không phải của quy tắc trong bài báo.

| khoảng lùa có giới hạn, 99%, $12\times$ | $N = 800$ | 1131 | 1600 | 3200 (một phần) |
| :--- | :---: | :---: | :---: | :---: |
| `compact` | 1 | 1 | 2 | 1 trong 42 trên 42 lượt |
| `wide` | 3 | 5–9 | không có đến 12 | 0 trên 58 lượt ở $D = 2$–12 |

---

## 4. Phân tích vi mô chuyên sâu: Dị thường bố cục và Động lực học từng lượt chạy

### 4.1 Hiện tượng tắc nghẽn trên bố cục phân cụm (`split`)
Trên bố cục `split` ở $N \ge 200$, việc tăng số lượng chó $D$ không giúp cải thiện tỷ lệ thành công ở các thời hạn trung bình ($6\times$ và $3\times$), với tỷ lệ thành công bị kẹt ở mức 0,60 đến 0,90 cho mọi $D \ge 4$. Phân tích vi mô dữ liệu log từng nhịp chỉ ra 2 nguyên nhân:
1. **Dồn ứ vào một phân cụm khi thu gom ($D = 4$)**: Do nhiệm vụ thu gom được chọn thuần túy theo khoảng cách tới trọng tâm toàn cục, các con cừu xa nhất thường nằm tập trung trong cùng một phân cụm. Trong lượt chạy lại với 12 hạt giống, toàn bộ $D$ chú chó cùng lao vào một phân cụm duy nhất trong $82 - 91\%$ số nhịp thu gom ban đầu. Khi can thiệp bằng cách phân tán mục tiêu đều ra các cụm, thời gian hoàn thành trung vị ở $D = 4$ giảm từ 631 s xuống 318 s.
2. **Quy tắc dừng $3 r_a$ gây đóng băng đàn chó ($D \ge 8$)**: Quy tắc Strömbom bắt buộc chó đứng yên khi cách bất kỳ con cừu nào dưới $3 r_a = 6$ m. Trên đàn `split`, mật độ cục bộ dày đặc khiến **25% tổng số chó bị đóng băng đứng yên** trong suốt thời gian chạy (so với $< 1\%$ trên đàn `wide`). Trong lượt chạy thử nghiệm rút ngắn khoảng cách dừng xuống $r_a = 2$ m, tỷ lệ chó đứng yên giảm mạnh, rút ngắn 20–24% thời gian lùa và đạt 12/12 trận thắng ở $D = 16$.

**Chẩn đoán tiếp theo (RQ-B1)**: các lượt đã lưu của `split` $N = 100$ và $200$ ($D = 2, 4, 8, 16$; $6\times$ và $3\times$; 12 hạt giống) được chạy lại với khoảng cách dừng rút ngắn còn $r_a$, với các chó đi gom nhận những con lạc đàn cách nhau ít nhất $f(N)$, và với cả hai. Mọi lượt chạy lại không thay đổi đều tái hiện đúng lượt đã lưu. Ở $6\times$, $N = 200$: dàn trải phân công giảm một nửa thời gian ở $D = 4$ (631 s xuống 318 s), và khoảng cách dừng ngắn hơn giảm khoảng một phần năm ở $D \ge 8$ (679 s xuống 536 s, 724 s xuống 551 s). Với cả hai thay đổi, $D = 8$–16 vẫn mất 530–540 s so với 365 s ở $D = 2$, nên vẫn còn một nguyên nhân thứ ba. Ở $3\times$, tỉ lệ thành công giảm từ 0,67 ở $D = 2$ xuống 0,08 ở $D = 8$ và 16, và không thay đổi nào cứu được (dàn trải phân công nâng $D = 4$ lên 0,58 và $D = 8$ lên 0,25): ở thời hạn chặt, nguyên nhân chính vẫn còn mở. Ở $N = 100$ số chó không ảnh hưởng. Đây là chẩn đoán 12 hạt giống, cho một hướng chứ không phải một quyết định.

![Đường cong thành công trên bố cục Split](../figures/fig23_split_curves.png)

**Hình 13:** Tắc nghẽn hiệu năng trên bố cục split. Tăng số chó không giúp đạt độ tin cậy ở *N* &ge; 200, một phần do dồn ứ cụm và quy tắc dừng cự ly (nguyên nhân thứ ba vẫn chưa rõ).

### 4.2 Tương quan các chỉ số vi mô
Trên toàn bộ các lượt chạy, các phép đo từng nhịp khẳng định:
- **Độ tản của bầy so với Thành công**: Tương quan nghịch Spearman mạnh giữa độ tản trung bình của bầy (khoảng cách RMS tới trọng tâm) và tỷ lệ thành công của ô ($r = -0{,}56$ đến $-0{,}81$ ở thời hạn $6\times$ và $3\times$). Bầy càng co cụm chặt chẽ thì thời gian lùa càng nhanh.
- **Động lực học trùng lặp cặp đôi**: Trong `strombom_multi`, tỷ lệ trùng lặp giữa các chú chó duy trì ở mức rất thấp trong giai đoạn gom, và chỉ tăng lên khi đàn chó xếp hàng vào vòng cung lùa. Trong FAT, độ trùng lặp vượt quá 0,80 ngay từ nhịp 1, xác nhận sự sụp đổ không phối hợp.

![Tương quan chỉ số vi mô](../figures/fig27_metrics.png)

**Hình 14:** Tương quan chỉ số vi mô. (a) Tương quan nghịch mạnh giữa độ tản trung bình của bầy và tỷ lệ thành công. (b) Tỷ lệ chó đứng yên trên split so với wide. (c) Tỷ lệ trùng lặp cặp đôi giữa các chú chó.

---

## 5. Thảo luận khoa học (Discussion)

### 5.1 So sánh với các quy luật mở rộng lý thuyết
Độ dốc tăng trưởng dưới tuyến tính của chúng tôi ($\alpha = 0{,}20 - 0{,}50$ ở $12\times$ trên năm kích thước bầy; 0,27–0,38 trên chín kích thước, mục 3.8) khác hẳn với mức tăng $\sqrt{M}$ ($\alpha = 0{,}50$) được Lama và di Bernardo (2024) chứng minh cho các mục tiêu không liên kết. Sự khác biệt này dễ hiểu cả về sinh học lẫn cơ học: với các mục tiêu không liên kết, mỗi cá thể lạc phải được một tác tử điều khiển lùa riêng. Trong các bầy có tính liên kết, lực hút toàn cục ($n = N - 1$) cho phép một người chăn duy nhất gián tiếp tác động lên cả bầy khi các con lạc đàn đã được đưa vào phạm vi cảm nhận, làm giảm mạnh số tác tử cần cho các bầy lớn.

Các lượt chạy về tính liên kết (mục 3.11) kiểm tra trực tiếp cách giải thích này. Làm bầy liên kết mạnh hơn bầy của bài báo hầu như không thay đổi độ dốc (0,30 trên `wide`), trong khi bầy yếu hơn duy nhất mà mô hình tạo được (mỗi con cừu bị hút về một nửa bầy) làm độ dốc tăng lên 0,40–0,70, tiến tới và vượt mức 0,5 của trường hợp không liên kết. Thời hạn cũng có tác dụng như vậy: ở $6\times$ độ dốc là 0,38–0,61. Tính liên kết và áp lực thời gian cùng nhau quyết định một bầy nằm ở phía nào của quy luật căn bậc hai.

### 5.2 Tính hai giai đoạn của bài toán chăn dắt tập thể
Kết quả của chúng tôi cho thấy bài toán chăn dắt tập thể gồm hai giai đoạn vật lý khác nhau về bản chất:
1. **Giai đoạn di chuyển (Thu gom và lùa bầy)**: Mở rộng quy mô tốt, tăng dưới tuyến tính theo $N$, và được tiêu chí đến đích 99% phản ánh vững chắc.
2. **Giai đoạn chặn giữ tại đích (Bước xử lý cá thể lạc đàn)**: Rất nhạy, không mở rộng quy mô được, và dễ bị vượt đà dưới các tiêu chí nghiêm ngặt.

Trong thực tế ứng dụng robot và chăn thả nông nghiệp, một con cừu rớt lại phía sau không có nghĩa là nhiệm vụ thất bại. Chúng tôi kiến nghị các chuẩn đánh giá đa tác tử trong tương lai tách rõ chỉ số đến đích khỏi một giai đoạn chặn giữ chủ động sau cùng (ví dụ đóng chuồng hoặc tuần tra vòng ngoài với vận tốc thấp). Các lượt chạy giữ bầy (mục 3.10) cho thấy vì sao phải tách hai việc này: một quy tắc đội chỉ biết lùa thì hoàn toàn không giữ được bầy (0 trên 10 ở mọi ô đã kiểm tra), và việc giữ bầy chỉ có tác dụng khi các chó lùi ra ngoài cự ly phản ứng của cừu.

### 5.3 Đóng góp khoa học

1. **Một bản đồ đã quyết định về đội tối thiểu, có ghi rõ độ bất định.** $D_{\min}$ theo kích thước bầy, bố cục xuất phát, thời hạn và quy tắc thành công, mỗi giá trị được quyết định ở độ tin cậy 99% hoặc được báo cáo dưới dạng khoảng chặn hay cận dưới, không bao giờ là một ước lượng điểm từ một số lượt chạy cố định. Cơ chế phân bổ thích ứng đã quyết định 92% trong số 4.773 ô trong vòng 200 hạt giống.
2. **Quy tắc thành công là một kết quả, không phải một chi tiết.** Theo tiêu chí "mọi con cừu ở trong đích", con cừu cuối cùng quyết định phần lớn các ô bầy lớn, và các quy ước thiết lập làm $D_{\min}$ thay đổi gấp ba lần trở lên; theo tiêu chí đến đích 99%, chúng làm nó thay đổi nhiều nhất một chó (mục 3.4, 3.5).
3. **Đủ và tối thiểu là hai con số khác nhau.** Đội nhanh nhất có thể (*D*<sub>sat</sub>) tăng theo $N$ nhanh gấp khoảng hai lần đội chỉ vừa đạt độ tin cậy, và mọi chó vượt quá *D*<sub>sat</sub> chỉ là chi phí (mục 3.7, 3.8).
4. **Phần nào của quy tắc đội có tác dụng.** Công tắc gom/lùa của một chó đưa một đội gồm các chó độc lập tới $N = 200$; tầng đội (phân công cừu lạc, vị trí lùa) là thứ giúp đạt được $N = 400$; một quy tắc không có cả hai (FAT) không đạt được mức nào (mục 3.6, 3.9).
5. **Khi nào thêm chó gây hại.** Trong bài toán lùa trên đồng trống, thêm chó dạng điểm chưa bao giờ làm nhiệm vụ thất bại. Tác hại xuất hiện khi chó chiếm chỗ: với khoảng cách 2 m, một bầy phân tán 400 con thất bại từ 9 chó trở lên. Phần tổng quan tài liệu làm nền cho nghiên cứu này chỉ tìm thấy tác hại của việc thêm người chăn trong bài toán giữ bầy (Green et al. 2022) và với điều khiển tập trung hoặc không phối hợp; đây là một trường hợp đã quyết định cho một bầy có tính liên kết trong bài toán lùa trên đồng trống, với điều kiện là quy tắc giãn cách (mục 3.10).
6. **Tính liên kết nối các kết quả mở rộng của bầy liên kết và không liên kết** qua một tham số duy nhất, theo đúng hướng mà quy luật không liên kết dự đoán (mục 3.11).
7. **Một giới hạn cứng của quy tắc lùa Strömbom.** Điểm lùa $r_a\sqrt{N}$ vượt cự ly phản ứng của cừu tại $N = (r_s/r_a)^2 \approx 1056$, trên mức này không đội nào với bất kỳ quy mô nào lùa được bầy. Giới hạn này suy ra từ hai tham số của quy tắc và được xác nhận trong mô phỏng (mục 3.13).
8. **Cái giá của góc nhìn cục bộ, và cách lấy lại**: khoảng thêm một chó ở $N = 200$, lấy lại được bằng cách chia sẻ những gì cả đội nhìn thấy (mục 3.12).
9. **Một trình mô phỏng mở, đã được kiểm tra.** Mọi kết quả đều tái lập được từ tệp giao thức của nó, mọi thư mục đều mang mã băm vật lý của nó, và mọi chẩn đoán chạy lại đều được đối chiếu với lượt chạy đã lưu.

### 5.4 Khả năng ứng dụng thực tế

Ứng dụng trực tiếp là chăn dắt bằng robot và drone, nơi phải chọn quy mô đội trước một lượt thử nghiệm. Với người chăn cừu thực thụ, các con số chỉ mang tính gián tiếp: họ quyết định theo kinh nghiệm và tự điều khiển chó, và cừu trong mô hình khác với cừu thật (bầy lỏng hơn, một cự ly phản ứng cố định duy nhất).

Dưới đây, một *đơn vị* là một tác tử chăn trong đội: một con chó, một robot hoặc một drone. Số đơn vị chính là quy mô đội $D$ dùng trong toàn bộ báo cáo, nên "một đến ba đơn vị" nghĩa là $D = 1$ đến 3.

- **Định cỡ đội.** Ở thời hạn thong thả, một đến ba đơn vị xử lý được một bầy phân tán đến 400 con, và một bầy compact cần một đơn vị ở mọi kích thước. Thời hạn làm thay đổi câu trả lời gần bằng một bầy lớn gấp bốn lần, nên cần cố định thời gian có được trước khi chọn quy mô đội.
- **Tốc độ tốn kém hơn độ tin cậy.** Trên các bầy `wide` và `outlier_rich`, đội hoàn thành nhanh nhất lớn gấp một rưỡi đến hai lần rưỡi mức tối thiểu (nhiều hơn trên `split`), và các đơn vị vượt quá nó chỉ tốn thêm thời gian pin mà không đem lại gì (Bảng 6).
- **Kích thước vật lý giới hạn đội hữu ích.** Các đơn vị không thể đứng gần nhau dưới 2 m sẽ làm chật vòng cung lùa của một bầy phân tán từ khoảng 9 đơn vị ở $N = 400$; chiều dài vòng cung (13 đến 23 m ở đây) giới hạn đội hữu ích.
- **Chia sẻ bản đồ trước khi thêm đơn vị.** Góc nhìn cục bộ tốn khoảng một đơn vị ở $N = 200$, và gộp những gì mọi đơn vị nhìn thấy sẽ lấy lại được đơn vị đó.
- **Lùi ra để giữ bầy.** Các đơn vị phải đi ra ngoài cự ly tháo chạy của con vật để giữ bầy tại chỗ; các đơn vị chỉ dừng lại thì vẫn làm bầy tiếp tục di chuyển.
- **Bầy lớn cần điểm lùa gần hơn.** Một bộ điều khiển dùng quy tắc lùa Strömbom phải giới hạn khoảng đứng sau ở cự ly tháo chạy với các bầy trên khoảng một nghìn con.
- **Phúc lợi động vật.** Trong mô hình, thời gian mỗi con cừu tháo chạy không tăng khi có thêm đơn vị; đây là một giả thuyết để thử nghiệm ngoài thực địa theo tinh thần của Yaxley et al. (2021), không phải một phát hiện về động vật.

---

## 6. Hạn chế và các yếu tố ảnh hưởng độ tin cậy (Limitations)

1. **Đơn giản hóa động học 2D**: Cừu và chó được mô phỏng như các chất điểm 2D có khả năng đổi hướng tức thời và không bị suy giảm thể lực theo thời gian.
2. **Điều kiện biên mở hoàn toàn**: Đồng cỏ thực tế luôn có hàng rào bao quanh, đóng vai trò hỗ trợ đắc lực cho chó chăn dồn ép gia súc.
3. **Ranh giới khoảng chặn do rời rạc hóa**: Các ô có độ tin cậy thực tế xấp xỉ $\theta = 0{,}90$ sẽ không thể ngã ngũ ở mốc 200 hạt giống, đòi hỏi phải báo cáo dưới dạng khoảng chặn.
4. **Thông tin toàn cục trong các lượt chạy chính**: ngoài các lượt chạy về tầm cảm nhận ở mục 3.12, `strombom_multi` giả định chó biết vị trí của mọi con cừu. Mục 3.12 kiểm tra tầm cảm nhận giới hạn với vị trí đã biết trong tầm đó; cảm biến chỉ đo hướng (bearing-only) chưa được mô hình hóa.
5. **Các lựa chọn định hình kết quả tiếp nối**: bước giữ bầy (chó rút ra ngoài $r_s$), quy tắc giãn cách (không chó nào trong vòng 2 m của chó khác), quy tắc tầm nhìn cục bộ (chó không thấy gì đi về tâm bầy biết lần cuối), mật độ áp đặt trên $N = 566$, và điểm lùa có giới hạn là các lựa chọn của HerdSim, không có nguồn trong các bài báo. Mỗi kết quả trong mục 3.10 đến 3.13 đúng theo lựa chọn được nêu cùng nó.
6. **N lớn**: trên $N \approx 600$ bầy của mô hình không có kích thước riêng, và bán kính áp đặt lỏng hơn bầy mà các chó lùa (0,53–0,82 của nó). Trên $N = 1056$ chỉ biến thể có giới hạn mới lùa được bầy.
7. **Các chẩn đoán còn nhỏ**: các lượt chạy lại đo áp lực và chẩn đoán split dùng 12 hạt giống mỗi ô; chúng cho hướng, không cho giá trị đã quyết định.

---

## 7. Kết luận và định hướng tương lai (Conclusions & Future Work)

Thông qua 326.870 lượt chạy mô phỏng qua 37 giao thức chiến dịch, HerdSim lập bản đồ quy mô đội tối thiểu $D_{\min}$, quy mô đội mà vượt quá nó thì chó không còn giúp ích (*D*<sub>sat</sub>), và các điều kiện mà khi đó thêm chó gây hại. Bầy có tính liên kết cần một chó ở mọi kích thước đã kiểm tra; trên đồng cỏ phân tán, đội tối thiểu tăng dưới tuyến tính, với độ dốc 0,27–0,38 ở thời hạn thong thả và 0,38–0,61 ở thời hạn chặt hơn, trong khi đội nhanh nhất tăng nhanh gấp khoảng hai lần. Dưới tiêu chí chặn giữ nghiêm ngặt, con cừu cuối cùng quyết định; dưới tiêu chí đến đích 99%, các câu trả lời vững trước các quy ước thiết lập. Sự phối hợp có ý nghĩa ở các bầy lớn, chó thêm chỉ gây hại khi chúng chiếm chỗ, và bản thân quy tắc lùa của bài báo ngừng hoạt động trên khoảng một nghìn con cừu.

### Định hướng nghiên cứu tiếp theo
Mỗi hướng dưới đây xuất phát từ một khoảng trống trong kết quả hiện tại. Hai hướng đầu kiểm tra xem các phát hiện chính có còn đúng ngoài những lựa chọn đã dùng ở đây không, ba hướng tiếp theo trả lời các câu hỏi nghiên cứu này còn để mở, và hai hướng cuối đưa mô hình đến gần người chăn thật hơn.

- **Lực đẩy cộng dồn từ nhiều chó** (kiểm tra phát hiện 1 và 7). HerdSim giới hạn lực đẩy của nhiều chó bằng lực đẩy của một con. Lựa chọn này là một phần lý do khiến thêm chó không làm bầy compact đi nhanh hơn và không tăng áp lực lên mỗi con cừu, trong khi các bài báo về nhiều người chăn cộng dồn lực. Chạy lại các lưới 99% chính với lực cộng dồn sẽ cho biết các phát hiện đó thuộc về bài toán chăn dắt hay chỉ thuộc về cách mô hình hóa này. Đây là hướng rẻ nhất và bảo vệ kết quả hiện tại nhiều nhất.
- **Đầu không liên kết, đối chiếu với quy luật đã công bố** (kiểm tra RQ1 và RQ11). Kết luận rằng tính liên kết làm $D_{\min}$ tăng chậm hơn quy luật căn bậc hai đang so độ dốc từ trình mô phỏng này với một quy luật được chứng minh trong một trình mô phỏng khác (Lama và di Bernardo 2024), với mô hình, nhiệm vụ và quy tắc người chăn khác. Cừu Strömbom không thể làm lỏng hơn mức $n = 0.5N$ mà bầy không tan rã. Đưa vào HerdSim một mô hình mục tiêu không liên kết, một nhiệm vụ thu gom và quy tắc người chăn của Lama sẽ kiểm tra xem quy luật căn bậc hai có xuất hiện ở đây không. Nếu có, các độ dốc tạo thành một đường liên tục trong cùng một trình mô phỏng: 0,5 khi không liên kết, 0,4–0,7 ở $n = 0.5N$, 0,3–0,4 ở mức liên kết của bài báo.
- **Bầy lớn với một quy tắc lùa hợp lý** (trả lời RQ8, mở rộng RQ13). Mục 3.8 cho thấy đến $N = 566$, dữ liệu không phân biệt được $D_{\min}$ tiếp tục tăng hay chững lại; chỉ bầy lớn hơn mới phân biệt được. Trên $N \approx 1056$ quy tắc lùa của bài báo hỏng, và các con số ở N lớn hiện dựa vào một điểm lùa có giới hạn được thêm như một bản vá. So sánh các quy tắc lùa cho bầy lớn như một đối tượng nghiên cứu riêng, với bộ điều khiển chó được vector hóa để bầy hàng nghìn con chạy được trong thời gian hợp lý, sẽ xác định hình dạng của $D_{\min}(N)$: một bầy lớn hơn nhiều có cần thêm chó mãi hay không.
- **Nguyên nhân còn mở trên bầy split** (hoàn thiện RQ7 và mục 4.1). Với bầy chia ba cụm, thêm chó làm việc lùa chậm đi, và ở $3\times$ tỉ lệ thành công tụt từ 0,67 với 2 chó xuống 0,08 với 8 và 16 chó. Việc dàn trải phân công gom và rút ngắn khoảng dừng giải thích được một phần, nhưng không giải thích được sự sụp đổ này. Đây là trường hợp duy nhất mà kết luận "thêm chó dạng điểm không gây hại" chưa được giải thích trọn. Tìm nguyên nhân còn lại, và thử một quy tắc gom chọn mục tiêu trải đều các cụm như một quy tắc riêng trên mọi bố cục (lần chạy lại giữ các con cừu được chọn cách nhau ít nhất $f(N)$ đã giảm một nửa thời gian của bầy split ở $D = 4$), sẽ hoặc giải thích được điểm bất thường, hoặc cho ra một quy tắc đội tốt hơn. Vấn đề nằm ở việc chọn con cừu nào để gom, không ở cách ghép chúng với chó: phép ghép cặp đã tối ưu.
- **Giữ các bầy nhỏ** (hoàn thiện RQ10). Giữ bầy thất bại ở $N \le 50$ với mọi quy mô đội, vì con chó lùi ra vẫn ở trong cự ly phản ứng 65 m khoảng 40 giây và đẩy bầy ra khỏi một đích bán kính 12–14 m. Kết quả đó đến từ quy tắc giữ bầy, không phải từ số chó. Một chuồng có cổng, hoặc một quy tắc giữ không dựa vào việc lùi ra, sẽ cho phép câu hỏi khi nào thêm chó gây hại bao phủ mọi kích thước bầy.
- **Cảm nhận chỉ theo hướng** (mở rộng RQ12). Các lượt chạy tầm nhìn cục bộ cho mỗi con chó biết chính xác vị trí của cừu trong tầm; camera trên robot và drone chỉ cho hướng, không cho khoảng cách đáng tin cậy (Li et al. 2025). Vì vậy chi phí hiện tại của tầm nhìn cục bộ (khoảng một chó ở $N = 200$, lấy lại được khi chia sẻ) có thể quá lạc quan. Chạy lại các lưới tầm nhìn với cảm nhận chỉ theo hướng sẽ cho một con số dùng được để thiết kế đội robot.
- **Dữ liệu thực địa với nhiều chó hoặc drone** (kiểm tra mục 5.4). Mọi con số ở đây đều từ mô phỏng, và cừu trong mô hình khác cừu thật (bầy lỏng hơn, một cự ly phản ứng cố định). Chưa có nghiên cứu GPS nào với hai người chăn trở lên. Dù chỉ một nghiên cứu nhỏ, với một đến ba drone hoặc chó và vài kích thước bầy, cũng sẽ cho thấy các quy mô đội và hiệu ứng giãn cách có đúng với động vật thật hay không.

---

## Khả năng tái lập và dữ liệu (Data & Code Availability)

Toàn bộ tập dữ liệu, cấu hình giao thức và mã nguồn phân tích được công khai trong kho mã nguồn HerdSim:
- Công cụ dòng lệnh thực thi: `cli/campaign.py`
- Phân tích thống kê: `analysis/frontier.py` và `analysis/dmin_tables.py`
- Lệnh tái lập kết quả:
  ```bash
  make install && make check && make bench
  uv run cli/run_queue.py --workers 20
  uv run cli/dmin_tables.py record
  uv run cli/dmin_tables.py dmin dmin_m12 dmin_m6 dmin_m3 dmin_f99_m12 dmin_f99_m6 dmin_f99_m3
  ```

---

## Tài liệu tham khảo (References)

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

## Phụ lục: Bảng tổng kết các chiến dịch chạy mô phỏng

| Giao thức | Tổng số lượt chạy | Số ô kiểm thử | Số ô quyết định | Ô bỏ ngỏ ở mốc 200 | Số lỗi | Thời gian chạy |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `dmin_m12` | 17.220 | 183 | 179 | 4 | 0 | 1,24 h |
| `dmin_m6` | 13.470 | 191 | 170 | 21 | 0 | 0,41 h |
| `dmin_m3` | 9.530 | 183 | 178 | 5 | 0 | 0,17 h |
| `dmin_f99_m12` | 11.100 | 180 | 178 | 2 | 0 | 0,41 h |
| `dmin_f99_m6` | 14.240 | 191 | 174 | 17 | 0 | 0,49 h |
| `dmin_f99_m3` | 11.140 | 185 | 177 | 8 | 0 | 0,27 h |
| `dmin_fat` | 8.660 | 181 | 179 | 2 | 0 | 0,22 h |
| `dmin_f99_fat` | 8.670 | 184 | 183 | 1 | 0 | 0,23 h |
| `dmin_kubo` | 1.080 | 18 | 18 | 0 | 0 | 0,08 h |
| Các giao thức độ nhạy (14 lượt) | 69.630 | 805 | 734 | 71 | 0 | 3,50 h |
| **Tổng cộng** | **164.740** | **2.291** | **2.190** | **148** | **0** | **~7,0 h** |

Các lượt chạy tiếp nối (tiêu chí 99%; số giờ với 20 tiến trình, có lúc chạy song song với lượt khác):

| Giao thức | Lượt chạy | Ô | Còn mở ở giới hạn | Lỗi | Giờ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3` (chạy tiếp: hạt giống thời gian hoàn thành; thêm $N$ 71, 141, 283, 566 cho hai giao thức đầu) | +38.770 | | | 0 | 4,0 |
| `dmin_f99_indep` | 12.990 | 181 | 18 | 0 | 0,30 |
| `dmin_f99_kubo` | 3.260 | 38 | 6 | 0 | 0,18 |
| `dmin_f99_hold` | 14.280 | 280 | 18 | 0 | 0,74 |
| `dmin_f99_hold_spacing` (chạy lại với quy tắc giãn cách cứng) | 13.930 | 283 | 19 | 0 | 0,71 |
| `dmin_f99_c1.3`, `_c1.6`, `_c2.0` | 10.800 / 10.830 / 10.780 | 180 mỗi giao thức | 1 / 0 / 0 | 0 | 0,31 / 0,29 / 0,41 |
| `dmin_f99_k05` | 11.630 | 149 | 14 | 0 | 2,29 |
| `dmin_f99_view_range` | 21.040 | 293 | 27 | 0 | 0,53 |
| `dmin_f99_view_comm` | 6.890 | 102 | 3 | 0 | 0,20 |
| `dmin_f99_big` | 2.230 | 84 | 1 | 0 | 3,12 |
| `dmin_f99_big_dense`, `_loose` | 1.320 / 830 | 15 / 14 | 2 / 1 | 0 | 0,73 / 0,26 |
| `dmin_f99_big_cap` | 2.550 (+100 ở $N = 3200$) | 45 | 3 | 0 | 7,6 |

Các lượt chạy lại chẩn đoán (không phải chiến dịch): 164 lượt đo áp lực và 768 lượt chẩn đoán split, mọi lượt chạy lại không thay đổi đều giống hệt lượt đã lưu. Lưu trữ, không dùng: `dmin_f99_hold_spacing_soft` (một quy tắc giãn cách không giữ được các chó cách nhau).
