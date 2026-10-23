# Quy mô đội tối thiểu để lùa một bầy cừu mô phỏng: Quy luật mở rộng thực nghiệm, Động lực học ranh giới và Cơ chế thất bại

*Báo cáo nghiên cứu khoa học dự án HerdSim*  
*Đánh giá thực nghiệm qua 23 giao thức chiến dịch (164.740 lượt chạy mô phỏng) trên các kiến trúc chăn dắt đa tác tử.*  
*(Lưu ý: Các phương trình động lực học vi mô, thuật toán điều khiển và định nghĩa hình học sân bãi đã được trình bày đầy đủ trong [README_vi.md](../../README_vi.md). Báo cáo này tập trung chuyên sâu vào ranh giới mở rộng thực nghiệm, câu trả lời thống kê cho các câu hỏi nghiên cứu, phân tích cơ chế thất bại vi mô và các hàm ý khoa học.)*

---

## Tóm tắt (Abstract)

Cần bao nhiêu tác tử chăn dắt tự hành ($D$) để thu gom và lùa một bầy cừu gồm $N$ cá thể vào một khu vực đích trước một thời hạn xác định? Chúng tôi khảo sát bài toán này thông qua môi trường mô phỏng trên 23 giao thức chiến dịch với tổng cộng 164.740 lượt chạy mà không phát sinh bất kỳ lỗi mô phỏng nào. Chúng tôi định nghĩa $D_{\min}$ là quy mô đội nhỏ nhất đạt độ tin cậy (tỷ lệ thành công được chứng minh $\ge 0{,}90$ dưới khoảng tin cậy nhị thức Clopper–Pearson hai phía ở mức ý nghĩa 99%). Sử dụng thuật toán phân bổ tuần tự thích ứng giúp tập trung tài nguyên tính toán vào các ô tham số ranh giới (tối đa 200 hạt giống mỗi ô), chúng tôi lập bản đồ $D_{\min}$ qua 5 quy mô bầy đàn ($N \in [25, 400]$), 4 bố cục không gian xuất phát (`compact`, `wide`, `split`, `outlier_rich`) và 3 mức thời hạn chuẩn hóa ($12\times$, $6\times$, và $3\times$ thời gian lùa tối thiểu) dưới cả hai tiêu chí: *chặn giữ nghiêm ngặt* (100% cừu trong đích) và *tiếp cận 99%* (tối thiểu $\lceil 0{,}99 N \rceil$ cừu trong đích).

Các kết quả thực nghiệm chỉ ra:
1. **Tính bất biến của bầy co cụm**: Với bầy xuất phát co cụm (`compact`), $D_{\min} \equiv 1$ là một hằng số bất biến tuyệt đối trên mọi quy mô ($N = 25$ đến $400$) và mọi thời hạn. Bổ sung thêm chó không giúp rút ngắn thời gian lùa đàn.
2. **Quy luật tăng trưởng dưới tuyến tính trên bầy phân tán**: Với bầy phân tán, $D_{\min} = 1$ khi $N \le 50$, và chỉ cần 2 đến 3 chó ở $N = 400$ dưới thời hạn nới lỏng ($12\times$). Trong không gian log-log ($\log_2 D_{\min}$ theo $\log_2 N$), độ dốc tăng trưởng dao động từ 0,20 đến 0,50 ở thời hạn $12\times$, và từ 0,30 đến 0,80 ở thời hạn $6\times$.
3. **Áp lực thời hạn là yếu tố chi phối hàng đầu**: Rút ngắn thời hạn từ $12\times$ xuống $3\times$ làm tăng vọt $D_{\min}$ trên bố cục `wide` ở $N = 400$ từ 2 lên 5–6 chó—mức gia tăng này vượt qua cả tác động của việc mở rộng quy mô đàn cừu lên gấp bốn lần.
4. **Cơ chế cá thể lạc đàn (The Straggler Mechanism)**: Trong 95% số lượt thất bại nghiêm ngặt của các đội có từ 6 chó trở lên, đàn chó thực chất đã đưa được 99% số cừu vào đích từ rất sớm. Thất bại nghiêm ngặt xảy ra do đàn chó quay sang săn đuổi 1–2 cá thể rớt lại sau cùng, vượt quá đà và vô tình lùa ngược khối cừu chủ lực ra ngoài pasture. Việc giảm vận tốc chó ($v_{\mathrm{dog}} = 1{,}15$) loại bỏ được xung lực vượt đà này, giúp đưa $D_{\min}$ nghiêm ngặt từ thất bại hoàn toàn (`none`) xuống còn 6 chó ở bố cục `outlier_rich` ($N = 400$).
5. **Tính vững chắc của tiêu chí tiếp cận 99%**: Dưới tiêu chí 99%, giá trị $D_{\min}$ duy trì sự ổn định cao (dao động trong phạm vi $\pm 1$ chó so với mốc cơ sở) trước các thay đổi về quy ước mô phỏng (xuất phát từ cọc người chăn, xuất phát vòng tròn, cự ly xuất phát, và các tham số cừu thực địa GPS). Ngược lại, tiêu chí nghiêm ngặt phóng đại quá mức các sai số do quy ước hình học gây ra.
6. **Sự bắt buộc của tầng phối hợp đội**: Mô hình đối chứng không phối hợp (FAT) thiếu thuật toán gán nhiệm vụ và lực đẩy không gian đã thất bại hoàn toàn: các chú chó dồn cục thành bản sao trùng lặp (`dog_overlap` $> 0{,}80$), không đạt được bất kỳ giá trị $D_{\min}$ tin cậy nào ở $N \ge 200$.
7. **Đủ chó, và không có tác hại theo tiêu chí 99%** (phân tích tiếp theo, mục 3.7): vượt quá quy mô đội *D*<sub>sat</sub> mà tại đó việc lùa không còn nhanh hơn, chó thêm giữ thời gian hoàn thành ở mức 0,90 đến 1,02 lần thời gian tại *D*<sub>sat</sub>, trong khi thời gian chó tăng tỉ lệ với $D$, và thời gian mỗi con cừu chạy trốn không tăng. Theo tiêu chí 99%, không quy mô đội nào đến 24 làm nhiệm vụ thất bại; chó thêm chỉ làm bầy `split` ở $N = 200$ chậm hơn. Bản thân *D*<sub>sat</sub> vẫn còn là một khoảng trên một phần ba các đường cong phân tán.

---

## 1. Câu hỏi nghiên cứu và mục tiêu

Các nghiên cứu trước đây về chăn dắt đa tác tử chủ yếu khảo sát các quy mô đội cố định hoặc trên các mục tiêu không liên kết (Pierson và Schwager 2015; Kubo et al. 2022; Lama và di Bernardo 2024). Để xác lập quy luật mở rộng quy mô của đội chăn tối thiểu dưới ảnh hưởng của lực hút bầy đàn, áp lực thời hạn và sự phân tán không gian, nghiên cứu này giải quyết 6 Câu hỏi Nghiên cứu (RQs):

- **RQ1 (Quy luật mở rộng quy mô $N$)**: Quy mô đội tối thiểu $D_{\min}$ tăng trưởng thế nào theo kích thước bầy $N \in [25, 400]$ trên các bố cục không gian và thời hạn khác nhau? Lực hút bầy đàn có làm giảm độ dốc tăng trưởng so với bầy không liên kết ($\sqrt{N}$) hay không?
- **RQ2 (Bố cục hình học so với quy mô dân số $N$)**: Với cùng một thời hạn, yếu tố nào chi phối $D_{\min}$ mạnh mẽ hơn: bố cục xuất phát (co cụm hay phân tán) hay quy mô đàn cừu $N$?
- **RQ3 (Áp lực thời hạn hoàn thành)**: Áp lực thời gian ($12\times \to 6\times \to 3\times$ thời gian lùa) làm dịch chuyển $D_{\min}$ ra sao? Tác động này là tuyến tính hay phi tuyến?
- **RQ4 (Tiêu chí thành công và Hiệu ứng cá thể lạc đàn)**: Tiêu chí nghiêm ngặt 100% khác biệt thế nào so với tiêu chí 99% tiếp cận? Cơ chế vi mô nào gây ra sự sụp đổ thành công của các đội nhiều chó dưới tiêu chí nghiêm ngặt?
- **RQ5 (Tính vững chắc trước các quy ước mô phỏng)**: Các quy luật mở rộng có đứng vững trước những thay đổi về quy ước thiết lập (vị trí thả chó, cự ly xuất phát, bán kính đích, tham số thực địa, vận tốc chó) hay không?
- **RQ6 (Sự cần thiết của phối hợp đa tác tử)**: Một đàn chó hoạt động độc lập không phối hợp (FAT) có thể đạt được $D_{\min}$ hữu hạn ở đàn lớn hay không?
- **RQ7 (Vượt quá $D_{\min}$: đủ chó và quá nhiều chó)**: Từ quy mô đội *D*<sub>sat</sub> nào thì thêm một con chó không còn làm việc lùa nhanh hơn, mỗi con chó vượt quá nó tốn bao nhiêu, nó có thêm áp lực lên cừu không, và có quy mô đội nào làm nhiệm vụ tệ đi không? (Phân tích tiếp theo trên các lượt chạy 99% hiện có; không chạy chiến dịch mới.)

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
- **Thất bại (`none`)**: Toàn bộ các giá trị $D$ trên lưới kiểm thử đều chắc chắn không đạt độ tin cậy ($U < 0{,}90$).

### 2.2 Tổng quan ma trận 23 giao thức thực nghiệm
Tập dữ liệu nghiên cứu bao gồm 23 giao thức (164.740 lượt chạy, 20 luồng worker, 0 lỗi):
- **Lưới chính (12 giao thức)**: Đánh giá đầy đủ 5 quy mô ($N \in [25, 400]$), 4 bố cục (`compact`, `wide`, `split`, `outlier_rich`), và 3 thời hạn ($12\times, 6\times, 3\times$ thời gian lùa) dưới cả hai tiêu chí Nghiêm ngặt 100% và Tiếp cận 99%.
- **Đối chứng không phối hợp (2 giao thức)**: `dmin_fat` và `dmin_f99_fat` ở thời hạn $6\times$.
- **Mô hình lực liên tục Kubo (1 giao thức)**: `dmin_kubo` trên bầy co cụm ($N \in [25, 100]$).
- **Bộ kiểm tra độ nhạy (14 giao thức)**: Đánh giá ở thời hạn $6\times$ qua 7 biến thể (cọc handler, vòng tròn ring, khoảng cách khởi đầu 15/30/60, bán kính đích $1{,}5 R_f$, tham số thực địa GPS, và tốc độ chó 1,15) dưới cả hai tiêu chí.

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
| **$12\times$** | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| **$12\times$** | `wide` | 1 / 1 | 1 / 1 | 1 / 1 | 2 / 1–2 | 3 / 2 |
| **$12\times$** | `split` | 1 / 1 | 1 / 1 | 1 / 1 | 1–2 / 1 | 3 / 2 |
| **$12\times$** | `outlier_rich` | 1 / 1 | 1 / 1 | 1–3 / 1–2 | 2 / 2 | 3 / 2 |
| **$6\times$** | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| **$6\times$** | `wide` | 1 / 1 | 1 / 1 | 1 / 1 | 3 / 2 | [9] / 2–3 |
| **$6\times$** | `split` | 1 / 1 | 1 / 1 | 1 / 1 | none / [1] | none / [5] |
| **$6\times$** | `outlier_rich` | 1 / 1 | 1 / 1 | 3 / 2 | [12] / 2–3 | none / 3 |
| **$3\times$** | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| **$3\times$** | `wide` | 1 / 1 | 1 / 1 | 3 / 2 | none / 3 | none / 5–6 |
| **$3\times$** | `split` | 1 / 1 | 1 / 1 | 1 / 1 | none / none | none / none |
| **$3\times$** | `outlier_rich` | 1 / 1 | 1 / 1 | 3–8 / 2 | none / 4–10 | none / [6] |

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
   - **$\alpha = 1{,}0$ (Tuyến tính)**: Cứ tăng gấp đôi số cừu thì phải tăng gấp đôi số chó (tỉ lệ cừu/chó cố định, không có lợi thế quy mô).
   - **$\alpha < 1{,}0$ (Dưới tuyến tính - Sub-linear)**: Bầy cừu càng lớn thì số lượng chó cần thêm càng ít đi (tính kinh tế theo quy mô). Ví dụ với $\alpha = 0{,}33$, khi quy mô bầy $N$ tăng gấp 8 lần ($2^3$), số lượng chó cần thiết chỉ tăng gấp đôi ($2^1 = 2$).
   - **$\alpha = 0$ ("Đi ngang" - Flat)**: Nhu cầu chó không hề tăng theo $N$. Trên bố cục `split` ở quy mô $N \le 100$, một chú chó ($D_{\min} = 1$) vẫn hoàn thành tốt nhiệm vụ thu gom cả 3 phân cụm trong thời hạn cho phép.
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
- **Dưới tiêu chí 99%**: Các quy luật mở rộng có tính vững chắc vượt trội. Dù thay đổi hình học thả chó (`handler`, `ring`, `arcs`), cự ly xuất phát (15, 30, 60 m), vận tốc chó (1,15 so với 1,50), hay áp dụng bộ tham số thực địa GPS của cừu, giá trị $D_{\min}$ vẫn duy trì ổn định trong phạm vi **$\pm 1$ chó** so với mốc cơ sở trên mọi ô.
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
  - *Trên bầy phân tán ở thời hạn trung bình ($6\times$)*: *D*<sub>sat</sub> dao động từ 3 đến 6 chú chó (ví dụ: bầy `outlier_rich` $N = 100$ bão hòa ở *D*<sub>sat</sub> = 3; bầy `wide` $N = 400$ bão hòa ở *D*<sub>sat</sub> = 6).
  - *Các ô tham số chưa ngã ngũ*: Ở 6 trong số 18 đường cong phân tán, các phép so sánh thời gian hoàn thành giữa các đội hình đạt độ tin cậy chưa giải quyết dứt điểm do thuật toán ưu tiên tài nguyên cho việc tìm $D_{\min}$ (`decide_finish_times: false`). Tại đây, *D*<sub>sat</sub> được ghi nhận dưới dạng khoảng chặn (ví dụ `wide` $N = 200$ là 3–24).

#### 2. Chi phí lãng phí khi vượt ngưỡng bão hòa (*D* > *D*<sub>sat</sub>)
- **Thêm chó không rút ngắn thời gian, nhưng chi phí tăng tỉ lệ thuận**:
  - Khi tăng số chó vượt qua *D*<sub>sat</sub>, thời gian đưa đàn cừu về đích gần như giữ nguyên: dao động trong khoảng **0,90 đến 1,02 lần** thời gian tại mốc *D*<sub>sat</sub> (khảo sát trên 128 ô tham số). Tức là việc tăng thêm hàng chục con chó chỉ giúp về đích nhanh hơn chưa đầy 5–10%, thậm chí đôi khi chậm hơn một chút do cản trở nhau.
  - Tuy nhiên, **tổng thời gian làm việc của bầy chó** (tổng thời gian tích lũy $\mathrm{dog\_time} = D \times T$) và tổng quãng đường chạy của cả đội lại tăng tuyến tính tỉ lệ thuận với *D* / *D*<sub>sat</sub>.
  - *Minh họa thực tế*: Trên bầy compact, triển khai 24 chú chó tiêu tốn năng lượng gấp 24 lần so với 1 chú chó, nhưng đàn cừu vẫn mất cùng một khoảng thời gian (~140 giây) để về tới đích.

Bảng 6 tổng hợp chi phí vận hành ở mốc gấp đôi ngưỡng bão hòa (2 *D*<sub>sat</sub>) và ở đội hình tối đa ($D = 24$) so với mốc *D*<sub>sat</sub> (trên các bầy phân tán ở thời hạn $6\times$):

| Bố cục xuất phát, Quy mô *N* | Ngưỡng *D*<sub>sat</sub> | Tại 2 *D*<sub>sat</sub>: Thời gian lùa / Thời gian chó | Tại *D* = 24: Thời gian lùa / Thời gian chó |
| :--- | :---: | :---: | :---: |
| `wide`, $N = 200$ | 3–24 | 0,97 / 1,94 | 0,96 / 7,68 |
| `wide`, $N = 400$ | 6 | 0,99 / 1,98 | 0,98 / 3,93 |
| `outlier_rich`, $N = 100$ | 3 | 0,99 / 1,98 | 0,98 / 7,85 |
| `outlier_rich`, $N = 400$ | 6–24 | 0,97 / 1,93 | 0,95 / 3,78 |
| `split`, $N = 100$ | 2–24 | 0,95 / 1,89 | 0,93 / 11,19 |

*Ý nghĩa Bảng 6*: Tại $D = 24$, thời gian lùa cừu chỉ nhanh hơn từ 2% đến 7% ($0{,}93 - 0{,}98$), nhưng tổng công suất và năng lượng tiêu hao của bầy chó lại bị đội lên từ **3,8 đến 11,2 lần** ($3{,}78 - 11{,}19$).

#### 3. Áp lực tâm lý và mức độ hoảng sợ của đàn cừu (Flock Stress)
Nhiều người e ngại rằng một bầy chó đông đúc sẽ gây hoảng loạn và kiệt sức cho đàn cừu. Tuy nhiên, dữ liệu vi mô từng giây cho thấy bức tranh hoàn toàn khác:
- **Tổng thời gian hoảng sợ của mỗi con cừu thực chất giảm đi**: Một con cừu ở trạng thái tháo chạy khi có bất kỳ chú chó nào nằm trong cự ly đe dọa $r_s = 65$ m. Khi tăng số chó từ $D_{\min}$ lên *D*<sub>sat</sub>, do bầy chó thu gom cừu lạc nhanh hơn nên thời gian tháo chạy của mỗi con cừu giảm rõ rệt (trên `wide` $N = 400$, thời gian chạy trốn trung bình của mỗi cá thể giảm từ 485 giây ở $D = 3$ xuống còn 359 giây ở $D = 6$). Khi vượt quá *D*<sub>sat</sub>, con số này đi ngang (361 giây ở $D = 12$).
- **Tỉ lệ đàn chạy trốn tức thời tăng lên**: Tại một thời điểm bất kỳ, bầy chó đông hơn sẽ giăng thành vòng cung rộng hơn, khiến một tỉ lệ lớn hơn trong đàn cừu cùng chạy trốn một lúc (trung bình 68% số cừu chạy trốn ở $D = 3$, tăng lên 84% ở $D = 12$). Nhưng vì toàn bộ cuộc lùa kết thúc nhanh hơn, tổng lượng stress tích lũy không hề bị gia tăng.
- **Không xảy ra va chạm nguy hiểm**: Nhờ quy tắc dừng giữ khoảng cách ($3 r_a = 6$ m), thời gian chó áp sát cừu ở cự ly dưới 6 m luôn duy trì dưới 1,3 giây trên mỗi con cừu trong suốt hành trình và hoàn toàn không tăng lên khi có thêm chó.

#### 4. Khả năng chống vỡ trận: Không có ngưỡng quá tải (*D*<sub>overcrowd</sub>) dưới tiêu chí 99%
- Dưới tiêu chí tiếp cận 99%, trên toàn bộ 11 thư mục dữ liệu khảo sát (lưới chính, mô hình đối chứng FAT và 7 biến thể độ nhạy), **không xuất hiện bất kỳ ngưỡng quá tải $D_{\mathrm{overcrowd}}$ nào** lên tới $D = 24$.
- Không có bất kỳ đường cong nào bị tụt giảm độ tin cậy sau khi đã đạt chuẩn: một khi quy mô đội đã thành công, việc bổ sung thêm chó không bao giờ làm nhiệm vụ bị thất bại. Hiện tượng đàn chó bị "đóng băng" vì quá đông trên bố cục `split` ở thời hạn gấp ($3\times$) dưới tiêu chí nghiêm ngặt đã hoàn toàn biến mất dưới tiêu chí 99%.
- Thêm chó chỉ làm tốc độ hoàn thành chậm đi đôi chút ở hai tình huống cá biệt: trên bầy `split` $N = 200$ ở thời hạn $12\times$ (nơi $D \ge 8$ bị vướng chân nhau do mật độ cừu cục bộ quá đặc) và trên mô hình đối chứng FAT (do các chú chó thiếu thuật toán né tránh nên dồn cục vào nhau). Trong cả hai trường hợp, bầy chó vẫn đưa được đàn cừu về đích an toàn, chỉ tốn thêm thời gian.

![Chi phí của chó vượt quá D_sat](../figures/fig33_effort.png)

**Hình 8:** Đánh giá chi phí khi vượt quá ngưỡng *D*<sub>sat</sub> ở thời hạn 6&times; (tiêu chí 99%). Trái: Thời gian hoàn thành so với mốc *D*<sub>sat</sub> đi ngang ở mức 0,90 đến 1,02. Phải: Tổng thời gian làm việc của chó tăng tuyến tính theo tỉ số *D* / *D*<sub>sat</sub>.

![Áp lực lên bầy](../figures/fig34_pressure.png)

**Hình 9:** Đánh giá áp lực tâm lý lên đàn cừu (12 hạt giống mỗi ô, dữ liệu `dmin_f99_m6`). Trái: Số giây tháo chạy của mỗi con cừu giảm mạnh tới mốc *D*<sub>sat</sub> rồi đi ngang. Phải: Tỉ lệ phần trăm đàn cừu tháo chạy tức thời tăng theo số lượng chó *D*.

Kết quả về áp lực một phần xuất phát từ các đặc tính chuẩn mực của mô hình Strömbom: lực đẩy từ nhiều chú chó lên một con cừu được chuẩn hóa độ dài về 1 (cơ chế blending), nên sự hiện diện của chú chó thứ hai ở gần không làm tăng độ mạnh của lực đẩy; đồng thời tầm nhìn $r_s = 65$ m rộng gấp khoảng 7 lần bán kính bầy ở $N = 100$, nên chỉ vài chú chó đã đủ để toàn bầy cảm nhận được sự hiện diện của người chăn. Toàn bộ bảng số liệu chi tiết và câu lệnh phân tích được lưu trữ tại [`results_tables.md`](results_tables.md) (mục "Phase 1").

---

## 4. Phân tích vi mô chuyên sâu: Dị thường bố cục và Động lực học từng lượt chạy

### 4.1 Hiện tượng tắc nghẽn trên bố cục phân cụm (`split`)
Trên bố cục `split` ở $N \ge 200$, việc tăng số lượng chó $D$ không giúp cải thiện tỷ lệ thành công ở các thời hạn trung bình ($6\times$ và $3\times$), với tỷ lệ thành công bị kẹt ở mức 0,60 đến 0,90 cho mọi $D \ge 4$. Phân tích vi mô dữ liệu log từng nhịp chỉ ra 2 nguyên nhân:
1. **Dồn ứ vào một phân cụm khi thu gom ($D = 4$)**: Do nhiệm vụ thu gom được chọn thuần túy theo khoảng cách tới trọng tâm toàn cục, các con cừu xa nhất thường nằm tập trung trong cùng một phân cụm. Trong lượt chạy lại với 12 hạt giống, toàn bộ $D$ chú chó cùng lao vào một phân cụm duy nhất trong $82 - 91\%$ số nhịp thu gom ban đầu. Khi can thiệp bằng cách phân tán mục tiêu đều ra các cụm, thời gian hoàn thành trung vị ở $D = 4$ giảm từ 631 s xuống 318 s.
2. **Quy tắc dừng $3 r_a$ gây đóng băng đàn chó ($D \ge 8$)**: Quy tắc Strömbom bắt buộc chó đứng yên khi cách bất kỳ con cừu nào dưới $3 r_a = 6$ m. Trên đàn `split`, mật độ cục bộ dày đặc khiến **25% tổng số chó bị đóng băng đứng yên** trong suốt thời gian chạy (so với $< 1\%$ trên đàn `wide`). Trong lượt chạy thử nghiệm rút ngắn khoảng cách dừng xuống $r_a = 2$ m, tỷ lệ chó đứng yên giảm mạnh, rút ngắn 20–24% thời gian lùa và đạt 12/12 trận thắng ở $D = 16$.

![Đường cong thành công trên bố cục Split](../figures/fig23_split_curves.png)

**Hình 10:** Tắc nghẽn hiệu năng trên bố cục split. Tăng số chó không giúp đạt độ tin cậy ở *N* &ge; 200 do dồn ứ cụm và quy tắc dừng cự ly.

### 4.2 Tương quan các chỉ số vi mô
Trên toàn bộ các lượt chạy, các phép đo từng nhịp khẳng định:
- **Độ tản của bầy so với Thành công**: Tương quan nghịch Spearman mạnh giữa độ tản trung bình của bầy (khoảng cách RMS tới trọng tâm) và tỷ lệ thành công của ô ($r = -0{,}56$ đến $-0{,}81$ ở thời hạn $6\times$ và $3\times$). Bầy càng co cụm chặt chẽ thì thời gian lùa càng nhanh.
- **Động lực học trùng lặp cặp đôi**: Trong `strombom_multi`, tỷ lệ trùng lặp giữa các chú chó duy trì ở mức rất thấp trong giai đoạn gom, và chỉ tăng lên khi đàn chó xếp hàng vào vòng cung lùa. Trong FAT, độ trùng lặp vượt quá 0,80 ngay từ nhịp 1, xác nhận sự sụp đổ không phối hợp.

![Tương quan chỉ số vi mô](../figures/fig27_metrics.png)

**Hình 11:** Tương quan chỉ số vi mô. (a) Tương quan nghịch mạnh giữa độ tản trung bình của bầy và tỷ lệ thành công. (b) Tỷ lệ chó đứng yên trên split so với wide. (c) Tỷ lệ trùng lặp cặp đôi giữa các chú chó.

---

## 5. Thảo luận khoa học (Discussion)

### 5.1 So sánh với các quy luật mở rộng lý thuyết
Độ dốc tăng trưởng dưới tuyến tính của chúng tôi ($\alpha = 0{,}20 - 0{,}50$ ở $12\times$) thấp hơn đáng kể so với mức tăng trưởng $\sqrt{M}$ ($\alpha = 0{,}50$) được chứng minh bởi Lama và di Bernardo (2024) cho các mục tiêu không liên kết. Sự khác biệt này hoàn toàn phù hợp với cơ chế sinh học: với các mục tiêu rời rạc không liên kết, mỗi cá thể phải được lùa độc lập bởi một tác tử điều khiển. Ngược lại, lực hút bầy đàn toàn cục ($n = N - 1$) trong mô hình Strömbom tạo ra khả năng tự co cụm: chỉ cần chó đưa các cá thể tản mác tiếp cận phạm vi tương tác của bầy, lực hút nội tại sẽ tự động kéo chúng hòa nhập vào khối chính, giúp giảm tải rất lớn cho đội ngũ chăn dắt ở quy mô lớn.

### 5.2 Tính hai giai đoạn của bài toán chăn dắt tập thể
Kết quả của chúng tôi chứng minh rằng bài toán chăn dắt tập thể bao gồm hai giai đoạn vật lý hoàn toàn tách biệt:
1. **Giai đoạn di chuyển (Thu gom và lùa bầy)**: Có khả năng mở rộng quy mô cao, tăng trưởng dưới tuyến tính theo $N$, và được phản ánh vững chắc thông qua tiêu chí tiếp cận 99%.
2. **Giai đoạn chặn giữ tại đích (Xử lý cá thể lạc đàn)**: Có tính nhạy cảm cực cao, không mở rộng quy mô tốt, và dễ bị hiện tượng vượt đà xé đàn dưới tiêu chí nghiêm ngặt.

Trong thực tế ứng dụng robot và nông nghiệp, một cá thể cừu rớt lại phía sau không đồng nghĩa với nhiệm vụ thất bại. Chúng tôi kiến nghị các chuẩn đánh giá hệ thống đa tác tử trong tương lai nên tách bạch rõ ràng giữa chỉ số tiếp cận đích và một giai đoạn chặn giữ chủ động sau cùng (như đóng cổng chuồng hoặc thiết lập vòng tuần tra vận tốc chậm).

---

## 6. Hạn chế và các yếu tố ảnh hưởng độ tin cậy (Limitations)

1. **Đơn giản hóa động học 2D**: Cừu và chó được mô phỏng như các chất điểm 2D có khả năng đổi hướng tức thời và không bị suy giảm thể lực theo thời gian.
2. **Điều kiện biên mở hoàn toàn**: Đồng cỏ thực tế luôn có hàng rào bao quanh, đóng vai trò hỗ trợ đắc lực cho chó chăn dồn ép gia súc.
3. **Ranh giới khoảng chặn do rời rạc hóa**: Các ô có độ tin cậy thực tế xấp xỉ $\theta = 0{,}90$ sẽ không thể ngã ngũ ở mốc 200 hạt giống, đòi hỏi phải báo cáo dưới dạng khoảng chặn.
4. **Giả định thông tin toàn cục**: Kiến trúc `strombom_multi` giả định đàn chó nắm rõ tọa độ chính xác của mọi cá thể, trong khi robot thực địa phải dựa trên thông tin cục bộ, cảm biến góc nhìn hoặc truyền thông giới hạn.

---

## 7. Kết luận và định hướng tương lai (Conclusions & Future Work)

Thông qua 164.740 lượt chạy mô phỏng qua 23 giao thức chiến dịch, HerdSim đã thiết lập bản đồ thực nghiệm có hệ thống đầu tiên về quy mô đội chăn dắt tối thiểu ($D_{\min}$). Chúng tôi chứng minh rằng bầy cừu co cụm có yêu cầu bất biến theo quy mô ($D_{\min} = 1$ trên bầy compact) và tăng trưởng dưới tuyến tính rõ rệt trên bầy phân tán. Nghiên cứu chỉ ra Hiệu ứng cá thể lạc đàn là nguyên nhân chính gây sụp đổ thành công của các đội nhiều chó dưới tiêu chí nghiêm ngặt, khẳng định tính vững chắc của tiêu chí tiếp cận 99%, và chứng minh rằng việc thiếu tầng phối hợp đa tác tử sẽ khiến hệ thống không thể mở rộng quy mô.

### Định hướng nghiên cứu tiếp theo
- **Phối hợp dựa trên cảm biến cục bộ phân tán**: Thay thế thuật toán gán Hungarian toàn cục bằng cơ chế đồng thuận góc nhìn cục bộ.
- **Bộ điều khiển chặn giữ chuyên biệt tại đích**: Thiết kế hành vi tuần tra chu vi chủ động với vận tốc thấp ngay khi đàn cừu chạm đích.
- **Mở rộng tương tác topo**: Khảo sát sự thay đổi khi số lượng láng giềng tương tác giảm xuống quy mô cục bộ ($n \ll N$).

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
- Jadhav V, Pasqua R, Zanon C, Roy M, Tredan G, Bon R, Guttal V, Theraulaz G (2024). Collective responses of flocking sheep (*Ovis aries*) to a herding dog (border collie). *Communications Biology* 7: 1543.
- Kubo M, Tashiro M, Sato H, Yamaguchi A (2022). Herd guidance by multiple sheepdog agents with repulsive force. *Artificial Life and Robotics* 27: 416–427.
- Lama A, di Bernardo M (2024). Shepherding control and herdability in complex multiagent systems. *Physical Review Research* 6: L032012.
- Li A, Ogura M, Wakamiya N (2025). Swarm shepherding using bearing-only measurements. *Philosophical Transactions of the Royal Society A* 383: 20240145.
- Pierson A, Schwager M (2015). Bio-inspired non-cooperative multi-robot herding. *IEEE International Conference on Robotics and Automation (ICRA)*.
- Strömbom D, Mann RP, Wilson AM, Hailes S, Morton AJ, Sumpter DJT, King AJ (2014). Solving the shepherding problem: heuristics for herding autonomous, interacting agents. *Journal of the Royal Society Interface* 11(100): 20140719.

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
