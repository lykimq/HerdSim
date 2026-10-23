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
4. **Cơ chế cá thể lạc đàn (The Straggler Mechanism)**: Trong 95% số lượt thất bại nghiêm ngặt của các đội có từ 6 chó trở lên, đàn chó thực chất đã đưa được 99% số cừu vào đích từ rất sớm. Thất bại nghiêm ngặt xảy ra do đàn chó quay sang săn đuổi 1–2 cá thể rớt lại sau cùng, vượt quá đà và vô tình lùa ngược khối cừu chủ lực ra ngoài pasture. Việc giảm vận tốc chó ($v_{\text{dog}} = 1{,}15$) loại bỏ được xung lực vượt đà này, giúp đưa $D_{\min}$ nghiêm ngặt từ thất bại hoàn toàn (`none`) xuống còn 6 chó ở bố cục `outlier_rich` ($N = 400$).
5. **Tính vững chắc của tiêu chí tiếp cận 99%**: Dưới tiêu chí 99%, giá trị $D_{\min}$ duy trì sự ổn định cao (dao động trong phạm vi $\pm 1$ chó so với mốc cơ sở) trước các thay đổi về quy ước mô phỏng (xuất phát từ cọc người chăn, xuất phát vòng tròn, cự ly xuất phát, và các tham số cừu thực địa GPS). Ngược lại, tiêu chí nghiêm ngặt phóng đại quá mức các sai số do quy ước hình học gây ra.
6. **Sự bắt buộc của tầng phối hợp đội**: Mô hình đối chứng không phối hợp (FAT) thiếu thuật toán gán nhiệm vụ và lực đẩy không gian đã thất bại hoàn toàn: các chú chó dồn cục thành bản sao trùng lặp (`dog_overlap` $> 0{,}80$), không đạt được bất kỳ giá trị $D_{\min}$ tin cậy nào ở $N \ge 200$.
7. **Đủ chó, và không có tác hại theo tiêu chí 99%** (phân tích tiếp theo, mục 3.7): vượt quá quy mô đội $D_{\text{sat}}$ mà tại đó việc lùa không còn nhanh hơn, chó thêm giữ thời gian hoàn thành ở mức 0,90 đến 1,02 lần thời gian tại $D_{\text{sat}}$, trong khi thời gian chó tăng tỉ lệ với $D$, và thời gian mỗi con cừu chạy trốn không tăng. Theo tiêu chí 99%, không quy mô đội nào đến 24 làm nhiệm vụ thất bại; chó thêm chỉ làm bầy `split` ở $N = 200$ chậm hơn. Bản thân $D_{\text{sat}}$ vẫn còn là một khoảng trên một phần ba các đường cong phân tán.

---

## 1. Câu hỏi nghiên cứu và mục tiêu

Các nghiên cứu trước đây về chăn dắt đa tác tử chủ yếu khảo sát các quy mô đội cố định hoặc trên các mục tiêu không liên kết (Pierson và Schwager 2015; Kubo et al. 2022; Lama và di Bernardo 2024). Để xác lập quy luật mở rộng quy mô của đội chăn tối thiểu dưới ảnh hưởng của lực hút bầy đàn, áp lực thời hạn và sự phân tán không gian, nghiên cứu này giải quyết 6 Câu hỏi Nghiên cứu (RQs):

- **RQ1 (Quy luật mở rộng quy mô $N$)**: Quy mô đội tối thiểu $D_{\min}$ tăng trưởng thế nào theo kích thước bầy $N \in [25, 400]$ trên các bố cục không gian và thời hạn khác nhau? Lực hút bầy đàn có làm giảm độ dốc tăng trưởng so với bầy không liên kết ($\sqrt{N}$) hay không?
- **RQ2 (Bố cục hình học so với quy mô dân số $N$)**: Với cùng một thời hạn, yếu tố nào chi phối $D_{\min}$ mạnh mẽ hơn: bố cục xuất phát (co cụm hay phân tán) hay quy mô đàn cừu $N$?
- **RQ3 (Áp lực thời hạn hoàn thành)**: Áp lực thời gian ($12\times \to 6\times \to 3\times$ thời gian lùa) làm dịch chuyển $D_{\min}$ ra sao? Tác động này là tuyến tính hay phi tuyến?
- **RQ4 (Tiêu chí thành công và Hiệu ứng cá thể lạc đàn)**: Tiêu chí nghiêm ngặt 100% khác biệt thế nào so với tiêu chí 99% tiếp cận? Cơ chế vi mô nào gây ra sự sụp đổ thành công của các đội nhiều chó dưới tiêu chí nghiêm ngặt?
- **RQ5 (Tính vững chắc trước các quy ước mô phỏng)**: Các quy luật mở rộng có đứng vững trước những thay đổi về quy ước thiết lập (vị trí thả chó, cự ly xuất phát, bán kính đích, tham số thực địa, vận tốc chó) hay không?
- **RQ6 (Sự cần thiết của phối hợp đa tác tử)**: Một đàn chó hoạt động độc lập không phối hợp (FAT) có thể đạt được $D_{\min}$ hữu hạn ở đàn lớn hay không?
- **RQ7 (Vượt quá $D_{\min}$: đủ chó và quá nhiều chó)**: Từ quy mô đội $D_{\text{sat}}$ nào thì thêm một con chó không còn làm việc lùa nhanh hơn, mỗi con chó vượt quá nó tốn bao nhiêu, nó có thêm áp lực lên cừu không, và có quy mô đội nào làm nhiệm vụ tệ đi không? (Phân tích tiếp theo trên các lượt chạy 99% hiện có; không chạy chiến dịch mới.)

---

## 2. Phương pháp luận thống kê và quy tắc quyết định

*(Chi tiết đầy đủ về vòng lặp thích ứng, khoảng tin cậy Clopper–Pearson và hệ thống hạt giống ngẫu nhiên chung CRN được trình bày tại [README_vi: Cơ chế thực thi thích ứng](../../README_vi.md#các-cơ-chế-thực-thi-thích-ứng).)*

### 2.1 Tiêu chí quyết định hình thức cho $D_{\min}$
Một **ô (cell)** được xác định bởi bộ tham số (phương pháp, bố cục, $N$, thời hạn, $D$). Mỗi lượt chạy mô phỏng là một phép thử Bernoulli độc lập cho ra kết quả thành công ($1$) hoặc thất bại ($0$). Với một mẫu gồm $n_{\text{trials}}$ hạt giống được đánh giá và $k$ lần thành công quan sát được, khoảng tin cậy nhị thức Clopper–Pearson hai phía 99% $[L, U]$ cho xác suất thành công thực tế $p$ được tính toán như sau:

$$
L = B\left(\frac{\alpha}{2}, k, n_{\text{trials}} - k + 1\right), \quad U = B\left(1 - \frac{\alpha}{2}, k + 1, n_{\text{trials}} - k\right)
$$

trong đó:
- $n_{\text{trials}} \in [10, 200]$: Tổng số lượt mô phỏng tích lũy đã chạy cho ô tham số đó.
- $k \in [0, n_{\text{trials}}]$: Số lượt mô phỏng ghi nhận thành công.
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
D_{\min} = \min \{ D \in \mathcal{D} \mid \text{Cell}(D) \text{ đạt độ tin cậy} \}
$$

$$
D_{\min,\text{low}} = \min \{ D \in \mathcal{D} \mid U(D) \ge \theta \}
$$

- **Giá trị quyết định**: Khi $D_{\min,\text{low}} = D_{\min}$, mọi $D < D_{\min}$ đều chắc chắn không đạt tin cậy ($U < 0{,}90$).
- **Khoảng chặn ($[D_{\min,\text{low}}, D_{\min}]$)**: Khi $D_{\min}$ đạt tin cậy nhưng vẫn còn một số $D$ nhỏ hơn ở trạng thái chưa quyết định tại mốc 200 hạt giống (ví dụ `3-8`).
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

### 3.1 RQ1: $D_{\min}$ mở rộng thế nào theo kích thước bầy $N$?

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

*Hình 1: Thực nghiệm mở rộng $D_{\min}$ theo kích thước bầy $N$ qua các thời hạn và bố cục. Vòng tròn/nét liền: nghiêm ngặt; vuông/nét đứt: tiếp cận 99%. Thanh đứng tô bóng là các khoảng chặn chưa quyết định.*

![Thời gian hoàn thành trên bầy Compact](../figures/fig31_compact.png)

*Hình 2: Thời gian hoàn thành theo số lượng chó $D$ trên bầy compact. Trái: Cừu Strömbom với quy tắc đội (thời gian hoàn thành bất biến theo $D$). Phải: Mô hình lực liên tục Kubo (thời gian giảm từ 116 s xuống 30 s khi $D$ tăng từ 1 lên 10).*

Bảng 2 liệt kê độ dốc tăng trưởng trong không gian log-log:

| Tiêu chí | Thời hạn | Độ dốc `wide` | Độ dốc `split` | Độ dốc `outlier_rich` |
| :--- | :---: | :---: | :---: | :---: |
| **Nghiêm ngặt** | $12\times$ | 0,42 | 0,32 đến 0,42 | 0,42 |
| **Nghiêm ngặt** | $6\times$ | 0,48 ($N \le 200$) | Đi ngang ($N \le 100$) | 0,79 ($N \le 100$) |
| **Nghiêm ngặt** | $3\times$ | 0,79 ($N \le 100$) | Đi ngang ($N \le 100$) | 0,79 đến 1,50 ($N \le 100$) |
| **Tiếp cận 99%** | $12\times$ | 0,20 đến 0,30 | 0,20 | 0,30 |
| **Tiếp cận 99%** | $6\times$ | 0,30 đến 0,42 | Đi ngang ($N \le 100$) | 0,42 đến 0,48 |
| **Tiếp cận 99%** | $3\times$ | 0,62 đến 0,68 | Đi ngang ($N \le 100$) | 0,70 đến 1,10 ($N \le 200$) |

---

### 3.2 RQ2: Bố cục phân tán so với Quy mô $N$: Yếu tố nào chi phối mạnh hơn?

**Câu trả lời trực tiếp cho RQ2**:
- Quy mô đàn cừu $N$ tạo ra tác động định lượng tương đương hoặc lớn hơn so với bố cục hình học trên tất cả các điều kiện khảo sát.
- Phân tích độ biến động tính theo số lần nhân đôi (doublings):
  - Biến thiên theo $N$ tạo ra độ phân tán trung bình từ **0,75 đến 1,69 lần nhân đôi**.
  - Biến thiên theo bố cục ở cùng quy mô $N$ tạo ra độ phân tán trung bình từ **0,50 đến 1,67 lần nhân đôi**.
- Tác động của bố cục chủ yếu đến từ bước nhảy giữa bầy `compact` ($D_{\min} \equiv 1$) và 3 bố cục phân tán. Giữa các bố cục phân tán với nhau (`wide` so với `outlier_rich`), sự chênh lệch hiếm khi vượt quá 1 chú chó.

Bảng 3 so sánh định lượng độ biến động theo số lần nhân đôi:

| Tiêu chí | Thời hạn | Biến động giữa các bố cục (Cố định $N$) | Biến động theo $N$ (Cố định bố cục) | Yếu tố chi phối chính |
| :--- | :---: | :---: | :---: | :--- |
| **Nghiêm ngặt** | $12\times$ | 0,68 lần nhân đôi | 1,19 lần nhân đôi | Quy mô đàn cừu $N$ |
| **Nghiêm ngặt** | $6\times$ | 1,67 lần nhân đôi | 1,69 lần nhân đôi | Tương đương / Quy mô $N$ |
| **Nghiêm ngặt** | $3\times$ | 0,76 lần nhân đôi | 0,97 lần nhân đôi | Quy mô đàn cừu $N$ |
| **Tiếp cận 99%** | $12\times$ | 0,50 lần nhân đôi | 0,75 lần nhân đôi | Quy mô đàn cừu $N$ |
| **Tiếp cận 99%** | $6\times$ | 0,92 lần nhân đôi | 1,30 lần nhân đôi | Quy mô đàn cừu $N$ |
| **Tiếp cận 99%** | $3\times$ | 1,25 lần nhân đôi | 1,28 lần nhân đôi | Tương đương / Quy mô $N$ |

---

### 3.3 RQ3: Áp lực thời hạn làm dịch chuyển $D_{\min}$ ra sao?

**Câu trả lời trực tiếp cho RQ3**:
- Thời hạn là tham số chi phối bậc một. Khi siết chặt thời hạn, toàn bộ đường cong tin cậy bị tịnh tiến sang phía bên phải.
- Mức độ dịch chuyển mang tính **phi tuyến**: nới lỏng từ $6\times$ lên $12\times$ thời gian lùa chỉ thay đổi $D_{\min}$ tối đa 1 chó, nhưng siết chặt từ $6\times$ xuống $3\times$ tạo ra sự gia tăng bùng nổ (ví dụ trên `wide` $N = 400$ dưới tiêu chí 99%, $D_{\min}$ tăng vọt từ 2–3 lên 5–6 chó; trên `split` $N \ge 200$, thời hạn ngặt nghèo dẫn đến thất bại trên toàn bộ các cỡ đội khảo sát).
- **Cơ chế vật lý**: Tác tử có vận tốc tối đa hữu hạn ($v_{\text{sheep}} = 1{,}0$, $v_{\text{dog}} = 1{,}5$). Ở thời hạn $12\times$, một chú chó có thừa thời gian để thu gom tuần tự từng con cừu rải rác. Ở thời hạn $3\times$, gom tuần tự là bất khả thi về mặt động học; đàn chó bắt buộc phải phân công gom song song đồng thời tất cả các cá thể tản mác.

![Tác động của thời hạn lên đường cong thành công](../figures/fig29_deadline.png)

*Hình 3: Tác động của thời hạn. Trái/Giữa: Đường cong thành công ở các thời hạn $12\times$, $6\times$, và $3\times$. Phải: Giá trị $D_{\min}$ biểu diễn trực tiếp theo hệ số thời hạn $m$.*

---

### 3.4 RQ4: Tiêu chí thành công và Hiệu ứng cá thể lạc đàn

**Câu trả lời trực tiếp cho RQ4**:
- Tiêu chí tiếp cận 99% đòi hỏi số chó bằng hoặc ít hơn đáng kể so với tiêu chí 100% nghiêm ngặt trên toàn bộ 34 ô phân tán khảo sát, giảm từ 1 đến 6 chó ở $N \ge 100$.
- Có 6 ô ở quy mô bầy lớn thất bại hoàn toàn dưới tiêu chí nghiêm ngặt nhưng đạt được $D_{\min}$ xác định dưới tiêu chí 99%.
- **Cơ chế cá thể lạc đàn (Straggler Mechanism)**: Trong 95% số lượt thất bại nghiêm ngặt của các đội có $D \ge 6$, đàn chó thực tế đã đưa được 99% số cừu vào đích từ rất sớm. Thất bại nghiêm ngặt xảy ra do đàn chó phá vỡ đội hình lùa để quay sang săn đuổi 1–2 con cừu lạc đàn còn lại bên ngoài. Khi áp sát, đàn chó vô tình đứng vào vị trí giữa bầy cừu và tâm đích, đẩy ngược toàn bộ khối cừu đã ổn định ra khỏi vòng tròn mục tiêu.
- Chó chạy chậm hơn ($v_{\text{dog}} = 1{,}15$) loại bỏ được xung lực vượt đà này, giúp tỷ lệ thành công nghiêm ngặt tăng từ thất bại hoàn toàn (`none`) lên $D_{\min} = 6$ ở bố cục `outlier_rich` ($N = 400$).

![Tỷ lệ thành công Nghiêm ngặt so với Tiếp cận 99%](../figures/fig30_strict_vs_99.png)

*Hình 4: So sánh tỷ lệ thành công giữa hai tiêu chí trên cùng hạt giống. Vùng tô bóng chứa các ô đạt độ tin cậy $\ge 90\%$ dưới tiêu chí 99% nhưng thất bại dưới tiêu chí nghiêm ngặt.*

![Phân tích vi mô hiệu ứng cá thể lạc đàn](../figures/fig22_straggler.png)

*Hình 5: Phân tích vi mô hiệu ứng cá thể lạc đàn. Trái: Tỷ lệ các lượt chạy $D \ge 6$ đưa được 99% cừu vào đích so với thành công nghiêm ngặt. Phải: Quỹ đạo chuỗi thời gian cho thấy chó nhanh ($1{,}5$) đẩy bật bầy cừu ra ngoài đích trong khi chó chậm ($1{,}15$) duy trì bầy ổn định trong đích.*

---

### 3.5 RQ5: Những quy luật nào đứng vững trước các phân tích độ nhạy?

**Câu trả lời trực tiếp cho RQ5**:
- **Dưới tiêu chí 99%**: Các quy luật mở rộng có tính vững chắc vượt trội. Dù thay đổi hình học thả chó (`handler`, `ring`, `arcs`), cự ly xuất phát (15, 30, 60 m), vận tốc chó (1,15 so với 1,50), hay áp dụng bộ tham số thực địa GPS của cừu, giá trị $D_{\min}$ vẫn duy trì ổn định trong phạm vi **$\pm 1$ chó** so với mốc cơ sở trên mọi ô.
- **Dưới tiêu chí nghiêm ngặt**: Giá trị tuyệt đối biến động dữ dội gấp 3 lần trở lên, do các quy ước thiết lập làm thay đổi quỹ đạo nhạy cảm của con cừu cuối cùng khi vào đích.
- **Hình học đích**: Việc thu hẹp bán kính đích ($1{,}5 R_f$) là biến thể duy nhất làm tăng thực sự $D_{\min}$ dưới cả hai tiêu chí (nâng `wide` $N = 400$ từ 2–3 lên 5–6 chó).

![Biểu đồ nhiệt phân tích độ nhạy](../figures/fig24_sensitivity.png)

*Hình 6: Phân tích độ nhạy trên các biến thể thực nghiệm ở thời hạn $6\times$. Tiêu chí nghiêm ngặt (trên) biến động mạnh; tiêu chí tiếp cận 99% (dưới) thể hiện tính ổn định cao.*

---

### 3.6 RQ6: Mô hình đối chứng không phối hợp (FAT) có đạt được $D_{\min}$ hữu hạn?

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

*Hình 7: Tỷ lệ thành công theo số lượng chó $D$ giữa strombom_multi (xanh lam) và FAT (cam). Đường cong của FAT đi ngang và hoàn toàn không cải thiện khi tăng số lượng chó.*

---

### 3.7 RQ7: Vượt quá $D_{\min}$: đủ chó, chi phí của chúng, và áp lực lên bầy

Mục này đọc lại các lượt chạy 99% hiện có (`dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3`, `dmin_f99_fat`, và `dmin_kubo` được gán nhãn lại theo tiêu chí đến nơi 99%) và chạy lại 164 lượt đã lưu. Không chạy chiến dịch mới nào, và mọi lượt chạy lại đều tái hiện đúng kết quả thành công và số tick đã lưu.

**Câu trả lời trực tiếp cho RQ7**:
- **$D_{\text{sat}}$ phần lớn vẫn còn mở.** Nó được quyết định bằng 1 trên mọi đường cong compact và ở $N \le 50$, và ở vài đường cong phân tán (`outlier_rich` $N = 100$: 3; `wide` $N = 400$: 6 ở $6\times$). Trên 6 trong 18 đường cong có $D_{\min}$ ở $6\times$ (8 trong 20 ở $12\times$), một $D$ đạt độ tin cậy lớn hơn vẫn chưa ngã ngũ khi so với nó, nên chỉ biết được một khoảng (ví dụ `outlier_rich` $N = 400$: 6 đến 24). Các lượt chạy này không dành hạt giống cho các phép so sánh thời gian hoàn thành (`decide_finish_times: false`), nên các phép so sánh quyết định $D_{\text{sat}}$ chưa bao giờ được giải quyết. Trả lời câu hỏi này cần bổ sung các phép so sánh đó.
- **Chó vượt quá $D_{\text{sat}}$ không mua được gì và tốn theo tỉ lệ.** Ở $6\times$, mọi $D$ đạt độ tin cậy trên $D_{\text{sat}}$ hoàn thành trong 0,90 đến 1,02 lần thời gian tại $D_{\text{sat}}$ (128 ô), trong khi thời gian chó tăng theo $D / D_{\text{sat}}$ (tỉ số 0,90 đến 1,02 so với đường đó). Trên bầy compact, 24 con chó tốn khoảng 24 lần thời gian chó của một con cho cùng một lần lùa.
- **Nhiều chó hơn không thêm áp lực lên mỗi con cừu.** Một con cừu ở trạng thái chạy trốn khi có chó gần hơn $r_s = 65$ m. Từ $D_{\min}$ đến $D_{\text{sat}}$, số giây chạy trốn của mỗi con cừu giảm (`wide` $N = 400$: 485 s ở $D = 3$, 359 s ở $D = 6$), và từ $D_{\text{sat}}$ đến $2 D_{\text{sat}}$ thì giữ nguyên (361 s ở $D = 12$). Tại mỗi thời điểm, nhiều chó hơn khiến phần lớn bầy chạy trốn hơn (tỉ lệ trung bình 0,68 ở $D = 3$, 0,84 ở $D = 12$), nhưng quãng lùa ngắn hơn. Thời gian ở trong khoảng cách dừng của chó (6 m) dưới 1,3 s mỗi con cừu và không tăng theo $D$.
- **Theo tiêu chí 99%, không quy mô đội nào làm nhiệm vụ thất bại.** Không đường cong nào trong mười một thư mục 99% (các lượt chính, FAT và bảy biến thể độ nhạy) có một $D$ không đạt độ tin cậy sau một $D$ đã đạt: không có sụt giảm, không có sụp đổ và không có $D_{\text{overcrowd}}$ trên lưới nào đến $D = 24$. Sự sụp đổ của `split` $N = 100$ theo tiêu chí strict ở $3\times$ ($D = 2$ đến 4) không xuất hiện theo tiêu chí 99%, nơi $D = 1, 2, 4$ đến 24 đều đạt độ tin cậy và $D = 3$ ở mức 0,935. Thêm chó chỉ làm nhiệm vụ chậm hơn ở hai chỗ: `split` $N = 200$ ở $12\times$, nơi $D \ge 8$ mất 695 đến 744 s so với 364,5 s ở $D = 2$, và FAT trên `split` $N = 100$, nơi $D \ge 4$ mất 219 đến 224 s so với 205 s ở $D = 1$.

Bảng 6 cho chi phí ở hai lần $D_{\text{sat}}$ và ở $D$ đạt độ tin cậy lớn nhất cho các đường cong phân tán ở $6\times$ (thời gian hoàn thành và thời gian chó so với ô $D_{\text{sat}}$; khi $D_{\text{sat}}$ là một khoảng thì lấy đầu dưới; tổng quãng đường của chó nằm trong `results_tables.md` và bám theo thời gian chó trong khoảng 0,01):

| Bố cục, $N$ | $D_{\text{sat}}$ | $2 D_{\text{sat}}$: thời gian / thời gian chó | $D = 24$: thời gian / thời gian chó |
| :--- | :---: | :---: | :---: |
| `wide`, 200 | 3–24 | 0,97 / 1,94 | 0,96 / 7,68 |
| `wide`, 400 | 6 | 0,99 / 1,98 | 0,98 / 3,93 |
| `outlier_rich`, 100 | 3 | 0,99 / 1,98 | 0,98 / 7,85 |
| `outlier_rich`, 400 | 6–24 | 0,97 / 1,93 | 0,95 / 3,78 |
| `split`, 100 | 2–24 | 0,95 / 1,89 | 0,93 / 11,19 |

![Chi phí của chó vượt quá D_sat](../figures/fig33_effort.png)

*Hình 8: Chó vượt quá $D_{\text{sat}}$ ở $6\times$ thời gian lùa (tiêu chí 99%). Trái: thời gian hoàn thành so với ô $D_{\text{sat}}$ giữ ở 0,90 đến 1,02. Phải: thời gian chó đi theo đường $D / D_{\text{sat}}$.*

![Áp lực lên bầy](../figures/fig34_pressure.png)

*Hình 9: Các lượt chạy lại (12 hạt giống mỗi ô, `dmin_f99_m6`). Trái: số giây mỗi con cừu chạy trốn, giảm đến $D_{\text{sat}}$ rồi giữ nguyên. Phải: tỉ lệ bầy đang chạy trốn tại một thời điểm, tăng theo $D$.*

Kết quả về áp lực một phần là tính chất của mô hình. Lực đẩy của nhiều chó lên một con cừu được chuẩn hóa về độ dài 1, nên con chó thứ hai ở gần không đẩy mạnh hơn, và $r_s = 65$ m gấp khoảng bảy lần bán kính bầy ở $N = 100$, nên chỉ vài con chó đã giữ phần lớn bầy ở trạng thái chạy trốn. Số đo này cho biết cừu chạy trốn bao lâu, không cho biết điều đó ảnh hưởng thế nào đến con vật. Bảng và lệnh nằm trong [`results_tables.md`](results_tables.md) (mục "Phase 1").

---

## 4. Phân tích vi mô chuyên sâu: Dị thường bố cục và Động lực học từng lượt chạy

### 4.1 Hiện tượng tắc nghẽn trên bố cục phân cụm (`split`)
Trên bố cục `split` ở $N \ge 200$, việc tăng số lượng chó $D$ không giúp cải thiện tỷ lệ thành công ở các thời hạn trung bình ($6\times$ và $3\times$), với tỷ lệ thành công bị kẹt ở mức 0,60 đến 0,90 cho mọi $D \ge 4$. Phân tích vi mô dữ liệu log từng nhịp chỉ ra 2 nguyên nhân:
1. **Dồn ứ vào một phân cụm khi thu gom ($D = 4$)**: Do nhiệm vụ thu gom được chọn thuần túy theo khoảng cách tới trọng tâm toàn cục, các con cừu xa nhất thường nằm tập trung trong cùng một phân cụm. Trong lượt chạy lại với 12 hạt giống, toàn bộ $D$ chú chó cùng lao vào một phân cụm duy nhất trong $82 - 91\%$ số nhịp thu gom ban đầu. Khi can thiệp bằng cách phân tán mục tiêu đều ra các cụm, thời gian hoàn thành trung vị ở $D = 4$ giảm từ 631 s xuống 318 s.
2. **Quy tắc dừng $3 r_a$ gây đóng băng đàn chó ($D \ge 8$)**: Quy tắc Strömbom bắt buộc chó đứng yên khi cách bất kỳ con cừu nào dưới $3 r_a = 6$ m. Trên đàn `split`, mật độ cục bộ dày đặc khiến **25% tổng số chó bị đóng băng đứng yên** trong suốt thời gian chạy (so với $< 1\%$ trên đàn `wide`). Trong lượt chạy thử nghiệm rút ngắn khoảng cách dừng xuống $r_a = 2$ m, tỷ lệ chó đứng yên giảm mạnh, rút ngắn 20–24% thời gian lùa và đạt 12/12 trận thắng ở $D = 16$.

![Đường cong thành công trên bố cục Split](../figures/fig23_split_curves.png)

*Hình 10: Tắc nghẽn hiệu năng trên bố cục split. Tăng số chó không giúp đạt độ tin cậy ở $N \ge 200$ do dồn ứ cụm và quy tắc dừng cự ly.*

### 4.2 Tương quan các chỉ số vi mô
Trên toàn bộ các lượt chạy, các phép đo từng nhịp khẳng định:
- **Độ tản của bầy so với Thành công**: Tương quan nghịch Spearman mạnh giữa độ tản trung bình của bầy (khoảng cách RMS tới trọng tâm) và tỷ lệ thành công của ô ($r = -0{,}56$ đến $-0{,}81$ ở thời hạn $6\times$ và $3\times$). Bầy càng co cụm chặt chẽ thì thời gian lùa càng nhanh.
- **Động lực học trùng lặp cặp đôi**: Trong `strombom_multi`, tỷ lệ trùng lặp giữa các chú chó duy trì ở mức rất thấp trong giai đoạn gom, và chỉ tăng lên khi đàn chó xếp hàng vào vòng cung lùa. Trong FAT, độ trùng lặp vượt quá 0,80 ngay từ nhịp 1, xác nhận sự sụp đổ không phối hợp.

![Tương quan chỉ số vi mô](../figures/fig27_metrics.png)

*Hình 11: Tương quan chỉ số vi mô. (a) Tương quan nghịch mạnh giữa độ tản trung bình của bầy và tỷ lệ thành công. (b) Tỷ lệ chó đứng yên trên split so với wide. (c) Tỷ lệ trùng lặp cặp đôi giữa các chú chó.*

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
