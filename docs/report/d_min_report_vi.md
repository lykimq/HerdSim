# Quy mô đội để lùa một bầy cừu mô phỏng: Tối thiểu, đủ và quá nhiều chó

*Báo cáo nghiên cứu khoa học dự án HerdSim*  
*Đánh giá thực nghiệm qua 23 giao thức chiến dịch (164.740 lượt chạy mô phỏng) trên các kiến trúc chăn dắt đa tác tử, tiếp theo là 14 giao thức tiếp nối và ba lượt chạy tiếp (162.130 lượt): và hai giao thức của mô hình không gắn kết của Lama và di Bernardo (2024) (40.280 lượt): tổng cộng 39 giao thức và 367.150 lượt chạy, không có lỗi.*  
*(Lưu ý: Các phương trình động lực học vi mô và thuật toán điều phối được trình bày tại [docs/methods/models_vi.md](../methods/models_vi.md). Hình học nhiệm vụ, tính bất biến quy mô và cơ chế lấy mẫu thích ứng được trình bày tại [docs/experiments/task_design_vi.md](../experiments/task_design_vi.md). Báo cáo này tập trung chuyên sâu vào các quy luật mở rộng thực nghiệm, câu trả lời thống kê cho các câu hỏi nghiên cứu, phân tích vi mô cơ chế thất bại và các hàm ý khoa học.)*

---

## Tóm tắt (Abstract)

Cần bao nhiêu tác tử chăn dắt tự hành ($D$) để gom một bầy $N$ con cừu và lùa bầy vào vùng đích một cách tin cậy trước thời hạn: tối thiểu là bao nhiêu ($D_{\min}$), bao nhiêu thì đủ ($D_{\mathrm{sat}}$), và từ khi nào thêm chó lại làm hỏng việc? Chúng tôi khảo sát bài toán này thông qua môi trường mô phỏng trên 39 giao thức chiến dịch với tổng cộng 367.150 lượt chạy mà không phát sinh bất kỳ lỗi mô phỏng nào. Chúng tôi định nghĩa $D_{\min}$ là quy mô đội nhỏ nhất đạt độ tin cậy (tỷ lệ thành công được chứng minh $\ge 0{,}90$ dưới khoảng tin cậy nhị thức Clopper–Pearson hai phía ở mức ý nghĩa 99%). Sử dụng thuật toán phân bổ tuần tự thích ứng giúp tập trung tài nguyên tính toán vào các ô tham số ranh giới (tối đa 200 hạt giống mỗi ô), 23 giao thức đầu tiên (164.740 lượt) lập bản đồ $D_{\min}$ qua 5 quy mô bầy đàn ($N \in [25, 400]$), 4 bố cục không gian xuất phát (`compact`, `wide`, `split`, `outlier_rich`) và 3 mức thời hạn chuẩn hóa ($12\times$, $6\times$, và $3\times$ thời gian lùa tối thiểu) dưới cả hai tiêu chí: *chặn giữ nghiêm ngặt* (100% cừu trong đích) và *tiếp cận 99%* (tối thiểu $\lceil 0{,}99 N \rceil$ cừu trong đích). Các giao thức tiếp theo chỉ dùng tiêu chí 99% và bổ sung quy mô đội mà từ đó thêm chó không còn giúp ích (*D*<sub>sat</sub>), bốn quy mô bầy mới đến $N = 566$, các quy tắc đội, giữ đàn, giãn cách chó, độ gắn kết, tầm cảm nhận, và các bầy vượt giới hạn của mô hình đến $N = 3200$. Hai giao thức cuối chạy mô hình mục tiêu không gắn kết và người chăn cảm nhận cục bộ của Lama và di Bernardo (2024) trên nhiệm vụ gom riêng của nó, để kiểm tra quy luật căn bậc hai của họ trong cùng một mô phỏng và cùng một lớp thống kê.

Các kết quả thực nghiệm chỉ ra:
1. **Tính bất biến của bầy co cụm**: Với bầy xuất phát co cụm (`compact`), $D_{\min} \equiv 1$ là một hằng số bất biến tuyệt đối trên mọi quy mô ($N = 25$ đến $400$) và mọi thời hạn. Bổ sung thêm chó không giúp rút ngắn thời gian lùa đàn.
2. **Quy luật tăng trưởng dưới tuyến tính trên bầy phân tán**: Với bầy phân tán, $D_{\min} = 1$ khi $N \le 50$, và chỉ cần 2 đến 3 chó ở $N = 400$ dưới thời hạn nới lỏng ($12\times$). Trong không gian log-log ($\log_2 D_{\min}$ theo $\log_2 N$), độ dốc tăng trưởng trên năm kích thước ban đầu dao động từ 0,20 đến 0,42 ở thời hạn $12\times$, và từ 0,30 đến 0,79 ở thời hạn $6\times$ (thu hẹp trên chín kích thước, mục 8).
3. **Áp lực thời hạn là yếu tố chi phối hàng đầu**: Rút ngắn thời hạn từ $12\times$ xuống $3\times$ làm tăng vọt $D_{\min}$ trên bố cục `wide` ở $N = 400$ từ 2 lên 5–6 chó—mức gia tăng này vượt qua cả tác động của việc mở rộng quy mô đàn cừu lên gấp bốn lần.
4. **Cơ chế cá thể lạc đàn (The Straggler Mechanism)**: Trong 97% số lượt thất bại nghiêm ngặt của các đội có từ 6 chó trở lên (lượt chạy cơ sở của bộ độ nhạy), đàn chó đã đưa được 99% số cừu vào đích từ trước thời hạn. Trong một lượt chạy mẫu, đàn chó khi đuổi theo những con cừu cuối cùng đã lùa ngược khối cừu chủ lực ra ngoài qua đích. Việc giảm vận tốc chó ($v_{\mathrm{dog}} = 1{,}15\text{ m/s}$) loại bỏ được xung lực vượt đà này, giúp đưa $D_{\min}$ nghiêm ngặt từ thất bại hoàn toàn (`none`) xuống còn 6 chó ở bố cục `outlier_rich` ($N = 400$).
5. **Tính vững chắc của tiêu chí tiếp cận 99%**: Dưới tiêu chí 99%, giá trị $D_{\min}$ duy trì sự ổn định cao (dao động trong phạm vi khoảng 1 chó so với mốc cơ sở) trước các thay đổi về quy ước mô phỏng (xuất phát từ cọc người chăn, xuất phát vòng tròn, cự ly xuất phát, và các tham số cừu thực địa GPS). Ngược lại, tiêu chí nghiêm ngặt phóng đại độ nhạy với quy ước lên gấp ba lần hoặc hơn.
6. **Quy tắc tham lam thất bại**: Mô hình đối chứng không phối hợp (FAT), trong đó mọi chú chó đuổi cùng một con cừu, không mở rộng được: không có quy mô đội tin cậy nào ở $N \ge 200$ trên mọi bố cục phân tán, và cả trên `compact` $N = 400$.
7. **Đủ chó, và không có tác hại theo tiêu chí 99%** (mục 3.7): vượt quá quy mô đội *D*<sub>sat</sub> mà tại đó việc lùa không còn nhanh hơn, chó thêm giữ thời gian hoàn thành ở mức 0,96 đến 1,01 lần thời gian tại *D*<sub>sat</sub>, trong khi thời gian chó tăng tỉ lệ với $D$, và thời gian mỗi con cừu chạy trốn không tăng. Theo tiêu chí 99%, không quy mô đội nào đến 24 làm nhiệm vụ thất bại trên năm kích thước ban đầu (một lần sụt trên lưới dày hơn); chó thêm chủ yếu làm bầy `split` chậm hơn ở $N \ge 200$ (và `outlier_rich` ở $N = 566$, $12\times$).
8. **Lưới dày hơn** (mục 3.8): trên chín kích thước bầy, $D_{\min}$ tăng với độ dốc 0,27–0,38 ở $12\times$ và 0,38–0,61 ở $6\times$, còn *D*<sub>sat</sub> tăng nhanh gấp khoảng hai lần (0,70–0,91 trên `wide`). Đến $N = 566$, một quy luật lũy thừa và một đường cong chững lại khớp dữ liệu tốt như nhau.
9. **Các phần của quy tắc đội** (mục 3.9): riêng công tắc gom/lùa của bài báo đã đưa một đội chó độc lập đến $N = 200$; tầng đội là điều làm cho $N = 400$ trở nên khả thi.
10. **Quá nhiều chó** (mục 3.10): với chó chiếm chỗ (cách nhau 2 m), `outlier_rich` $N = 400$ thất bại từ $D = 9$ (được quyết định không đạt độ tin cậy đến $D = 24$), trong khi chó dạng điểm không cho thấy tác hại được quyết định đến 24.
11. **Độ gắn kết và tầm cảm nhận** (mục 3.11, 3.12): gắn kết yếu hơn làm sự tăng dốc hơn về phía 0,5 của mục tiêu không gắn kết; tầm nhìn cục bộ tốn khoảng một con chó ở $N = 200$, và chia sẻ với cả đội mua lại được con chó đó.
12. **Một giới hạn của quy tắc lùa** (mục 3.13): trên $N \approx 1056$, điểm lùa của bài báo nằm ngoài cự ly phản ứng của cừu, và không đội nào đến 12 chó lùa được bầy. Khi giới hạn điểm lùa trong tầm với, một bầy phân tán cần 3 chó ở $N = 800$, 5–9 ở 1131 và hơn 12 ở 1600.
13. **Mục tiêu không gắn kết** (mục 3.14): mô hình của Lama và di Bernardo (2024), chạy trong HerdSim trên nhiệm vụ riêng của nó, tái lập Hình 2 của bài báo theo từng ô (sai khác trung vị về tỷ lệ mục tiêu được gom là 0,034 với bán kính cảm nhận 10 và 0,003 với cảm nhận vô hạn), khi người chăn và mục tiêu được tích phân từ cùng một trạng thái như trong bài báo. Với cảm nhận vô hạn, đội tối thiểu tăng theo căn bậc hai của số mục tiêu (số mũ 0,52–0,53 trên 100 đến 400 mục tiêu) theo cả thống kê của bài báo lẫn của HerdSim. Với bán kính cảm nhận 10, không đội nào tới 25 người chăn gom tin cậy được 81 mục tiêu trở xuống, và gần ngưỡng (100 đến 196 mục tiêu) hai thống kê tách nhau: tỷ lệ trung bình của bài báo đạt 0,99 với 11 người chăn ở 144 mục tiêu, trong khi 17 đến 25 người chăn vẫn mất một mục tiêu ở khoảng một lượt trong mười.

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

Các chiến dịch tiếp theo (tiêu chí 99% xuyên suốt) bổ sung bảy câu hỏi:

- **RQ8 (Lưới dày hơn và hình dạng đường cong)**: Với chín kích thước bầy đến ngưỡng của mô hình ($N = 566$), $D_{\min}$ và *D*<sub>sat</sub> tăng nhanh thế nào, và có phân biệt được tăng đều với một đường cong chững lại không?
- **RQ9 (Phần nào của quy tắc quan trọng)**: Công tắc gom/lùa và tầng đội mỗi phần đóng góp gì, và một mô hình mà thời gian hoàn thành giảm theo $D$ (Kubo) bão hòa ra sao?
- **RQ10 (Quá nhiều chó)**: Việc giữ bầy trong đích, hay chó chiếm chỗ, có làm cho chó thêm gây hại không?
- **RQ11 (Độ gắn kết)**: Sự tăng của $D_{\min}$ thay đổi thế nào theo độ mạnh của sự gắn kết giữa các con cừu?
- **RQ12 (Chó nhìn thấy gì)**: Tầm cảm nhận giới hạn tốn thêm bao nhiêu chó, và việc chia sẻ những gì các chó thấy có bù lại được không?
- **RQ13 (N lớn)**: Điều gì xảy ra trên kích thước mà bầy của mô hình còn có kích thước riêng?
- **RQ14 (Mục tiêu không gắn kết)**: HerdSim có tái lập được đội tối thiểu, ngưỡng mật độ và quy luật căn bậc hai của Lama và di Bernardo (2024) cho các mục tiêu không tụ bầy không, và quy luật đó có giữ dưới quy tắc tin cậy của HerdSim cũng như dưới thống kê của bài báo không?

---

## 2. Phương pháp luận thống kê và quy tắc quyết định

*(Chi tiết đầy đủ về vòng lặp thích ứng, khoảng tin cậy Clopper–Pearson và hệ thống hạt giống ngẫu nhiên chung CRN được trình bày tại [docs/experiments/task_design_vi.md: Động cơ Lấy mẫu Thích ứng Tuần tự](../experiments/task_design_vi.md#3-động-cơ-lấy-mẫu-thích-ứng-tuần-tự-adaptive-sequential-sampling).)*

### 2.1 Tiêu chí quyết định hình thức cho *D*<sub>min</sub>
Một **ô (cell)** được xác định bởi bộ tham số (phương pháp, bố cục, $N$, thời hạn, $D$). Mỗi lượt chạy mô phỏng là một phép thử Bernoulli độc lập cho ra kết quả thành công ($1$) hoặc thất bại ($0$). Với một mẫu gồm $n_{\mathrm{trials}}$ hạt giống được đánh giá và $k$ lần thành công quan sát được, khoảng tin cậy nhị thức Clopper–Pearson hai phía 99% $[L, U]$ cho xác suất thành công thực tế $p$ được tính toán như sau:

$$
L = B\left(\frac{\alpha}{2}, k, n_{\mathrm{trials}} - k + 1\right), \quad U = B\left(1 - \frac{\alpha}{2}, k + 1, n_{\mathrm{trials}} - k\right)
$$

trong đó:
- $n_{\mathrm{trials}} \in [10, 200]$: Tổng số lượt mô phỏng tích lũy đã chạy cho ô tham số đó.
- $k \in [0, n_{\mathrm{trials}}]$: Số lượt mô phỏng ghi nhận thành công.
- $\alpha = 0{,}01$: Mức ý nghĩa thống kê, tương ứng với độ tin cậy hai phía $1 - \alpha = 99$% (mỗi phía đuôi phân phối chiếm $\alpha/2 = 0{,}005$).
- $B(q, a, b)$: Hàm phân vị (hàm phân phối tích lũy nghịch đảo) của phân phối Beta với hai tham số hình dạng $a$ và $b$, tính tại xác suất tích lũy $q$.
- $L$: Cận dưới thống kê của tỷ lệ thành công thực tế với độ tin cậy 99%.
- $U$: Cận trên thống kê của tỷ lệ thành công thực tế với độ tin cậy 99%.

Với ngưỡng tin cậy mục tiêu quy định là $\theta = 0{,}90$:
- **Đạt độ tin cậy (Reliable)**: $L \ge 0{,}90$. Chúng ta có độ tin cậy toán học 99% rằng tỷ lệ thành công thực tế đạt ít nhất 90% (đòi hỏi tối thiểu 51 trận thắng liên tiếp không có trận thua nào, được làm tròn thành 60 lượt chạy với kích thước lô 10).
- **Không đạt tin cậy (Unreliable)**: $U \lt 0{,}90$. Chúng ta tin cậy 99% rằng ô này không thể đạt ngưỡng 90%, kích hoạt cơ chế dừng sớm để tiết kiệm thời gian (thường dừng sau 10–20 lượt).
- **Chưa quyết định (Undecided)**: $L \lt 0{,}90 \le U$. Khoảng tin cậy vẫn đang bao trùm ngưỡng 90%, ô sẽ tiếp tục nhận các lô 10 hạt giống tiếp theo cho đến trần tối đa 200 hạt giống.

Trên một đường cong kiểm thử theo số lượng chó $D \in \mathcal{D}$:

$$
D_{\min} = \min \lbrace D \in \mathcal{D} \mid \mathrm{Cell}(D) \text{ is Reliable} \rbrace
$$

$$
D_{\min,\mathrm{low}} = \min \lbrace D \in \mathcal{D} \mid U(D) \ge \theta \rbrace
$$

- **Giá trị quyết định**: Khi $D_{\min,\mathrm{low}} = D_{\min}$, mọi $D \lt D_{\min}$ đều chắc chắn không đạt tin cậy ($U \lt 0{,}90$).
- **Khoảng chặn ($[D_{\min,\mathrm{low}}, D_{\min}]$)**: Khi $D_{\min}$ đạt tin cậy nhưng vẫn còn một số $D$ nhỏ hơn ở trạng thái chưa quyết định tại mốc 200 hạt giống (ví dụ `3-8`).
- **Cận dưới ($[n]$)**: Chưa có $D$ nào đạt tin cậy nhưng tồn tại $D \ge n$ chưa quyết định.
- **Thất bại (`none`)**: Toàn bộ các giá trị $D$ trên lưới kiểm thử (đến $D = 24$ ở các lượt chạy chính) đều chắc chắn không đạt độ tin cậy ($U \lt 0{,}90$).

### 2.2 Tổng quan ma trận giao thức thực nghiệm
Nghiên cứu đầu tiên bao gồm 23 giao thức (164.740 lượt chạy, 20 luồng worker, 0 lỗi):
- **Lưới chính (6 giao thức)**: Đánh giá đầy đủ 5 quy mô ($N \in [25, 400]$), 4 bố cục (`compact`, `wide`, `split`, `outlier_rich`), và 3 thời hạn ($12\times, 6\times, 3\times$ thời gian lùa) dưới cả hai tiêu chí Nghiêm ngặt 100% và Tiếp cận 99%.
- **Đối chứng không phối hợp (2 giao thức)**: `dmin_fat` và `dmin_f99_fat` ở thời hạn $6\times$.
- **Mô hình lực liên tục Kubo (1 giao thức)**: `dmin_kubo` trên bầy co cụm ($N \in [25, 100]$).
- **Bộ kiểm tra độ nhạy (14 giao thức)**: Đánh giá ở thời hạn $6\times$, một mốc cơ sở và 6 biến thể (cọc handler, vòng tròn ring, khoảng cách khởi đầu 15/60 so với mốc 30, bán kính đích $1{,}5 R_f$, tham số thực địa GPS, và tốc độ chó 1,15) dưới cả hai tiêu chí.

Phần tiếp theo bổ sung 14 giao thức và chạy tiếp ba lưới 99% (162.130 lượt, 0 lỗi, chỉ tiêu chí 99%), được liệt kê cùng RQ8–RQ13 và trong phụ lục. Hai giao thức của mô hình Lama và di Bernardo trên nhiệm vụ gom (40.280 lượt, 0 lỗi) trả lời RQ14.

---

## 3. Kết quả thực nghiệm và Câu trả lời trực tiếp cho các Câu hỏi nghiên cứu

### 3.1 RQ1: Quy mô đội tối thiểu *D*<sub>min</sub> mở rộng thế nào theo số lượng cừu *N*?

**Câu trả lời trực tiếp cho RQ1**:
- **Bầy tập trung (`compact`)**: $D_{\min} \equiv 1$ là một hằng số bất biến tuyệt đối trên mọi quy mô bầy ($N = 25$ đến $400$) và mọi mức thời hạn. Bố trí thêm chó không hề làm giảm thời gian lùa đàn (trung vị thời gian hoàn thành luôn duy trì trong khoảng 1,44–1,74 lần thời gian lùa lý thuyết cho mọi $D \in [1, 24]$).
- **Bầy phân tán (`wide`, `split`, `outlier_rich`)**: $D_{\min}$ mở rộng **dưới tuyến tính (sub-linear)** theo $N$. Ở thời hạn thong thả ($12\times$), $D_{\min} = 1$ cho bầy $N \le 50$, và chỉ cần 2 hoặc 3 chó cho đàn lớn $N = 400$.
- **Hệ số góc trong không gian log-log**: Trong không gian log-log ($\log_2 D_{\min}$ so với $\log_2 N$), độ dốc dao động từ **0,20 đến 0,42** ở thời hạn $12\times$, và từ **0,30 đến 0,79** ở thời hạn $6\times$. Ở $12\times$, bầy cừu gắn kết đòi hỏi số tác tử tăng chậm hơn định luật căn bậc hai $\alpha = 0{,}50$ ($\sqrt{M}$) của mục tiêu không liên kết; ở $6\times$ và $3\times$, một số độ dốc vượt quá mức này.

Bảng 1 thể hiện ma trận thực nghiệm đầy đủ của $D_{\min}$ (Nghiêm ngặt 100% / Tiếp cận 99%):

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

Số liệu: [D_min by layout and N, strict success](results_tables.md#d_min-by-layout-and-n-strict-success) (`dmin_m12`, `dmin_m6`, `dmin_m3`) và [success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent) (`dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3`).

![Quy mô D_min theo số cừu N](../figures/fig20_dmin_vs_n.png)

**Hình 1: Quy luật mở rộng thực nghiệm của $D_{\min}$ theo quy mô bầy $N$ qua các thời hạn và bố cục xuất phát.**

Số liệu: cùng hai bảng với bảng phía trên, cùng [D_min, dmin_f99_m12](results_tables.md#d_min-dmin_f99_m12) và [D_min, dmin_f99_m6](results_tables.md#d_min-dmin_f99_m6) cho các kích thước bổ sung $N = 71, 141, 283, 566$.

*Cách đọc biểu đồ:*
- **Các khung**: Ba khung, mỗi khung một mức thời hạn ($12\times$, $6\times$, $3\times$). Màu sắc chỉ bố cục (`compact` xám, `wide` xanh dương, `split` cam, `outlier_rich` xanh ngọc).
- **Các trục**: Quy mô bầy $N$ theo $D_{\min}$, cả hai trục thang log. Các đường 99% ở $12\times$ và $6\times$ kéo dài tới $N = 566$.
- **Ký hiệu đường & Điểm**: Đường nét liền với vòng tròn biểu thị tiêu chí nghiêm ngặt 100%; đường nét đứt với hình vuông biểu thị tiêu chí tiếp cận 99%. Các dải bóng mờ dọc thể hiện khoảng chặn chưa ngã ngũ (ví dụ $[3, 8]$) tại mức trần 200 hạt giống. Tam giác rỗng là cận dưới ($[n]$), và dấu chéo cùng màu bố cục trên hàng "none" biểu thị không có $D$ tin cậy nào tới 24.
- **Ý nghĩa cốt lõi**: Bầy tập trung luôn phẳng lì ở $D_{\min} = 1$ trong mọi điều kiện. Trên bầy phân tán, đường cong tăng chậm ở thời hạn thong thả, nhưng thời hạn gấp gáp ($3\times$) đẩy đường cong uốn dốc lên rất mạnh và gây thất bại hoàn toàn ở các đàn lớn dưới tiêu chí 100% do hiệu ứng cá thể lạc đàn.

![Thời gian hoàn thành trên bầy Compact](../figures/fig31_compact.png)

**Hình 2: Thời gian hoàn thành theo số lượng chó $D$ trên bầy xuất phát tập trung compact.**

Số liệu: thời gian hoàn thành của các lượt compact thành công trong `results/dmin_m6` và `results/dmin_kubo` (không có bảng); $D_{\min}$ của Kubo nằm trong [Kubo (compact, strict)](results_tables.md#kubo-compact-strict).

*Cách đọc biểu đồ:*
- **Các khung hình**: Khung trái là mô hình Strömbom với quy tắc đội nhiều chó, $N = 25$ đến $400$; khung phải là mô hình trường thế của Kubo et al. (2022), $N = 25$, $50$ và $100$.
- **Các trục**: Số chó $D$ trên thang log. Trái: trung vị thời gian hoàn thành tính theo số lần thời gian lùa. Phải: trung vị thời gian hoàn thành tính bằng giây, so với giới hạn 500 s.
- **Ý nghĩa cốt lõi**: Trong mô hình Strömbom, thời gian hoàn thành không đổi theo số chó vì cừu đi ở tốc độ riêng của chúng ($1{,}0\text{ m/s}$) và thêm chó không làm chúng đi nhanh hơn. Trong mô hình Kubo, các lực cộng dồn lùa bầy nhanh hơn, từ $\approx 115\text{ s}$ với 1 chó xuống $29\text{ s}$ với 10 chó ở $N = 100$; 10 là mức cao nhất của lưới này, và với tới 24 chó (mục 3.9) thời gian còn tiếp tục giảm.

Bảng 2 trình bày các hệ số góc tăng trưởng log-log thực nghiệm:

| Tiêu chí | Thời hạn | Độ dốc `wide` | Độ dốc `split` | Độ dốc `outlier_rich` |
| :--- | :---: | :---: | :---: | :---: |
| **Nghiêm ngặt 100%** | $12\times$ | 0,42 | 0,32 đến 0,42 | 0,42 |
| **Nghiêm ngặt 100%** | $6\times$ | 0,48 ($N \le 200$) | Đi ngang ($N \le 100$) | 0,79 ($N \le 100$) |
| **Nghiêm ngặt 100%** | $3\times$ | 0,79 ($N \le 100$) | Đi ngang ($N \le 100$) | 0,79 đến 1,50 ($N \le 100$) |
| **Tiếp cận 99%** | $12\times$ | 0,20 đến 0,30 | 0,20 | 0,30 |
| **Tiếp cận 99%** | $6\times$ | 0,30 đến 0,42 | Đi ngang ($N \le 100$) | 0,42 đến 0,48 |
| **Tiếp cận 99%** | $3\times$ | 0,62 đến 0,68 | Đi ngang ($N \le 100$) | 0,70 đến 1,10 ($N \le 200$) |

Số liệu: [Growth with N, strict](results_tables.md#growth-with-n-strict) và [Growth with N, 99 percent](results_tables.md#growth-with-n-99-percent).

**Cơ sở vật lý và ý nghĩa của Bảng 2:**
1. **Khái niệm Hệ số góc Log-Log ($\alpha$)**:
   Trong tọa độ log-log ($\log_2 D_{\min}$ theo $\log_2 N$), quan hệ tỷ lệ tuân theo hàm lũy thừa: $D_{\min} \propto N^\alpha$, trong đó độ dốc $\alpha = \frac{\Delta \log_2 D_{\min}}{\Delta \log_2 N}$ trực tiếp đo lường **tính kinh tế theo quy mô (economies of scale)**:
   - **$\alpha = 1{,}0$ (Tăng trưởng tuyến tính)**: Gấp đôi số cừu bắt buộc phải gấp đôi số chó (tỷ lệ cố định cừu/chó, không có hiệu quả quy mô).
   - **$\alpha \lt 1{,}0$ (Tăng trưởng dưới tuyến tính)**: Đàn cừu càng lớn thì số lượng chó bổ sung trên mỗi con cừu càng giảm đi. Ví dụ, tại $\alpha \approx 0{,}33$, quy mô bầy tăng gấp 8 lần ($2^3$) chỉ đòi hỏi tăng gấp 2 lần số chó ($2^1 = 2$).
   - **$\alpha = 0$ (Đi ngang)**: Nhu cầu chó không hề tăng theo $N$. Trên bố cục `split` ở $N \le 100$, 1 chú chó duy nhất ($D_{\min} = 1$) gom thành công cả 3 cụm con trong thời hạn.
2. **Lợi thế của Lực gắn kết sinh học**:
   Trong bài toán thu gom các mục tiêu độc lập bằng robot (ví dụ: robot dọn rác trên mặt phẳng), cận dưới lý thuyết là $\alpha = 0{,}50$ ($D \propto \sqrt{M}$). Ngược lại, đối với bầy cừu gắn kết ở thời hạn thong thả ($12\times$), độ dốc thực nghiệm giảm mạnh xuống **0,20 đến 0,42** (và **0,20 đến 0,30** dưới tiêu chí 99%). Điều này chứng minh lực hút xã hội tự nhiên đã làm giúp một nửa khối lượng công việc: khi quy mô bầy tăng lên, cừu tự động hút nhau về trung tâm, giảm bớt nhu cầu bổ sung thêm chó.
3. **Vì sao Áp lực thời gian làm tăng độ dốc**:
   Rút ngắn thời hạn từ $12\times$ xuống $3\times$ đẩy độ dốc vọt lên **0,62 đến 1,50**. Khi thời gian cạn kiệt, cừu không còn thời gian tự tụ về bầy, và một chú chó đơn độc không thể đi gom tuần tự từng con. Đội chó bắt buộc phải can thiệp song song cùng lúc, lấn át cơ chế tự gắn kết tự nhiên và đẩy hệ số góc tiến về (hoặc vượt qua) mức tuyến tính.

---

### 3.2 RQ2: Sự phân tán không gian so với Quy mô bầy: Yếu tố nào chi phối mạnh hơn?

**Đo lường độ phân tán thông qua "Số lần tăng đôi" (Doublings) trong Bảng 3**:
Vì quy mô bầy là biến số liên tục ($N \in [25, 400]$) trong khi các bố cục là các hình thái rời rạc (`compact`, `wide`, `split`, `outlier_rich`), chúng tôi so sánh mức độ tác động của chúng trên cùng một thước đo: số lần tăng gấp đôi ($\log_2$ span của $D_{\min}$):

$$
\text{Độ phân tán (doublings)} = \log_2 \left( \frac{D_{\min,\max}}{D_{\min,\min}} \right)
$$

Độ phân tán được lấy qua các bố cục tại mỗi $N$ rồi lấy trung bình theo $N$ (và qua các $N$ tại mỗi bố cục rồi lấy trung bình theo bố cục), dùng trung điểm nhân của khoảng chặn; các đường cong không có $D$ tin cậy nào trên lưới bị loại ra.

Bảng 3 so sánh mức độ phân tán định lượng:

| Tiêu chí | Thời hạn | Biến thiên qua các Bố cục (Cố định $N$) | Biến thiên qua $N$ (Cố định Bố cục) | Yếu tố chi phối |
| :--- | :---: | :---: | :---: | :--- |
| **Nghiêm ngặt** | $12\times$ | 0,68 doublings | 1,19 doublings | Quy mô bầy $N$ |
| **Nghiêm ngặt** | $6\times$ | 1,67 doublings | 1,69 doublings | Ngang nhau / Quy mô $N$ |
| **Nghiêm ngặt** | $3\times$ | 0,76 doublings | 0,97 doublings | Quy mô bầy $N$ |
| **99%** | $12\times$ | 0,50 doublings | 0,75 doublings | Quy mô bầy $N$ |
| **99%** | $6\times$ | 0,92 doublings | 1,30 doublings | Quy mô bầy $N$ |
| **99%** | $3\times$ | 1,25 doublings | 1,28 doublings | Ngang nhau / Quy mô $N$ |

Số liệu: tính từ các bảng số lần gấp đôi trong [Growth with N, strict](results_tables.md#growth-with-n-strict) và [Growth with N, 99 percent](results_tables.md#growth-with-n-99-percent).

**Kết luận cốt lõi từ Bảng 3**:
1. **Quy mô bầy $N$ là yếu tố chi phối hàng đầu**: Trong hầu hết điều kiện, sự biến thiên do tăng số lượng cừu luôn vượt qua sự biến thiên do thay đổi bố cục (trung bình 0,75 đến 1,69 lần tăng đôi so với 0,50 đến 1,67 lần tăng đôi).
2. **Tác động của bố cục chỉ mang tính nhị phân**: Gần như toàn bộ sự khác biệt giữa các bố cục bắt nguồn từ một bước chuyển duy nhất: chuyển từ **bầy đã co cụm sẵn (`compact`)** sang **đồng cỏ phân tán**. Dưới tiêu chí 99% ở $12\times$, việc cừu phân bố đều (`wide`) hay có cá thể lạc xa (`outlier_rich`) hiếm khi làm nhu cầu chênh quá 1 chó. Dưới tiêu chí nghiêm ngặt ở $6\times$ hai bố cục chênh nhau nhiều (3 so với [12] ở $N = 200$), và `split` có thể thất bại hoàn toàn trong khi hai bố cục kia có $D_{\min}$ hữu hạn.

---

### 3.3 RQ3: Áp lực thời hạn làm dịch chuyển *D*<sub>min</sub> như thế nào?

**Câu trả lời trực tiếp cho RQ3**:
- Áp lực thời gian là một hệ số nhân cực mạnh. Rút ngắn thời hạn đẩy toàn bộ ranh giới tin cậy dịch chuyển sang bên phải.
- Tác động này mang tính **phi tuyến**: dưới tiêu chí 99% trên `wide` và `outlier_rich`, nới lỏng từ $6\times$ lên $12\times$ chỉ giúp tiết kiệm tối đa 1 chó (dưới tiêu chí nghiêm ngặt và trên `split` mức chênh lớn hơn), nhưng rút ngắn từ $6\times$ xuống $3\times$ làm bùng nổ nhu cầu chó (trên `wide` $N = 400$ dưới tiêu chí 99%, $D_{\min}$ nhảy từ 2–3 lên 5–6 chó; trên `split` $N \ge 200$, thời hạn gấp gáp gây thất bại hoàn toàn trên mọi số lượng chó).
- **Cơ chế vật lý**: Chó và cừu có tốc độ di chuyển hữu hạn ($v_{\mathrm{sheep}} = 1{,}0$, $v_{\mathrm{dog}} = 1{,}5\text{ m/s}$). Ở $12\times$, một chú chó có thừa thời gian gom cừu lạc tuần tự từng con. Ở $3\times$, gom tuần tự là điều bất khả thi về mặt vật lý; đàn chó bắt buộc phải tỏa ra gom đồng thời cùng lúc.

![Tác động của thời hạn](../figures/fig29_deadline.png)

**Hình 3: Tác động của áp lực thời hạn lên đường cong thành công và quy mô đội chăn dắt.**

Số liệu: tỷ lệ thành công từng ô trong `results/dmin_f99_m12`, `dmin_f99_m6` và `dmin_f99_m3` (không có bảng); $D_{\min}$ lấy từ [D_min by layout and N, success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent).

*Cách đọc biểu đồ:*
- **Khung trái & giữa**: Tỷ lệ thành công kèm khoảng tin cậy 99% theo số chó $D$ cho `wide` $N = 400$ (trái) và `outlier_rich` $N = 200$ (giữa), ở $12\times$ (xanh nhạt), $6\times$ (xanh vừa) và $3\times$ (xanh đậm). Đường chấm đánh dấu $\theta = 0{,}90$.
- **Khung phải**: $D_{\min}$ (trục log) theo thời hạn ($12\times$, $6\times$, $3\times$) cho `wide` và `outlier_rich` ở $N = 200$ (nét liền, tròn) và $N = 400$ (nét đứt, vuông); điểm rỗng là cận dưới.
- **Ý nghĩa cốt lõi**: Đường cong dịch chuyển phi tuyến sang phải khi thời hạn bị siết chặt. Trên các đường 99% này, nới lỏng quá $6\times$ chỉ tiết kiệm tối đa 1 chó, trong khi siết chặt từ $6\times$ xuống $3\times$ làm tăng vọt số chó cần thiết do đòi hỏi bắt buộc phải làm việc nhóm song song.

---

### 3.4 RQ4: Tiêu chí thành công và "Hiệu ứng cá thể lạc đàn" (Straggler Effect)

**Câu trả lời trực tiếp cho RQ4**:
- Tiêu chí 99% cừu vào đích đòi hỏi số chó bằng hoặc ít hơn tiêu chí tuyệt đối 100% trên toàn bộ 34 ô bầy phân tán mà cả hai tiêu chí đều có $D$ tin cậy. Ở những ô cả hai giá trị đều đã quyết định, mức tiết kiệm đúng bằng một chó (ví dụ 3 xuống 2); `outlier_rich` $N = 100$ ở $3\times$ đi từ khoảng chặn 3–8 xuống 2; một số ô ở $N \ge 100$ không đổi.
- Sáu ô bầy lớn không có $D$ tin cậy dưới tiêu chí nghiêm ngặt (bốn ô none trên lưới, hai ô còn mở) có $D$ tin cậy dưới tiêu chí 99% (hai ô đã quyết định, bốn ô dạng khoảng chặn).
- **Cơ chế vi mô của Hiệu ứng cá thể lạc đàn**: Trong 97% số lượt thất bại nghiêm ngặt của các đội có từ 6 chó trở lên ở lượt chạy cơ sở của bộ độ nhạy (`dmin_s_base`; 91% ở `dmin_m6`), 99% số cừu đã có lúc nằm trong đích trước thời hạn. Trong một lượt chạy mẫu (`wide` $N = 400$, 16 chó), đàn chó khi đuổi theo 1–2 con cừu cuối cùng đã đứng chắn giữa bầy và đích, lùa khối cừu chủ lực ngược ra ngoài.
- Cho chó chạy chậm hơn, điềm tĩnh hơn ($v_{\mathrm{dog}} = 1{,}15\text{ m/s}$) giúp triệt tiêu đà vượt qua cửa chuồng, đưa tỷ lệ thành công nghiêm ngặt trên `outlier_rich` $N = 400$ từ thất bại hoàn toàn (`none`) lên $D_{\min} = 6$.

![Strict so với 99%](../figures/fig30_strict_vs_99.png)

**Hình 4: So sánh từng ô tham số giữa tiêu chí nghiêm ngặt 100% và tiêu chí tiếp cận 99% trên cùng các hạt giống ngẫu nhiên.**

Số liệu: tỷ lệ thành công từng ô của các lượt chạy nghiêm ngặt đọc theo cả hai tiêu chí, từ `results/dmin_m12`, `dmin_m6` và `dmin_m3` (không có bảng); các giá trị $D_{\min}$ nằm trong [strict success](results_tables.md#d_min-by-layout-and-n-strict-success), [success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent) và [strict run read at 99 percent arrival](results_tables.md#strict-run-read-at-99-percent-arrival-for-comparison-with-the-99-percent-runs).

*Cách đọc biểu đồ:*
- **Các khung**: Mỗi khung một mức thời hạn ($12\times$, $6\times$, $3\times$), bố cục phân tán ở $N \ge 100$, các ô có ít nhất 20 hạt giống chung (80, 57 và 33 ô).
- **Các trục & Đường chéo**: Trục hoành là tỷ lệ thành công theo tiêu chí nghiêm ngặt; trục tung là tỷ lệ thành công theo tiêu chí 99%. Đường chéo là đường đồng nhất ($y = x$).
- **Vùng bóng mờ**: Các điểm nằm trong vùng bóng mờ phía trên bên trái đạt độ tin cậy $\ge 90$% dưới tiêu chí 99% nhưng lại trượt dưới tiêu chí tuyệt đối.
- **Ý nghĩa cốt lõi**: 40 ô (6, 21 và 13 theo từng mức thời hạn) nằm trong vùng bóng mờ, 31 ô trong số đó ở $N \ge 200$: ở đó chính con cừu cuối cùng, chứ không phải việc gom bầy, quyết định kết quả nghiêm ngặt.

![Cơ chế cá thể lạc đàn](../figures/fig22_straggler.png)

**Hình 5: Phân tích vi mô Hiệu ứng cá thể lạc đàn.**

Số liệu: tỷ lệ cừu trong đích của từng lượt chạy trong `results/dmin_s_base` và `results/dmin_s_dogspeed` (không có bảng); D_min của hai lượt chạy này nằm trong [Sensitivity, strict: base / variant](results_tables.md#sensitivity-strict-base--variant).

*Cách đọc biểu đồ:*
- **Khung trái**: Đánh giá các lượt chạy với từ 6 chó trở lên ($D \ge 6$). Các cột so sánh tỷ lệ đạt 99% cừu vào đích với tỷ lệ đạt 100% tuyệt đối. Chó chạy chậm ($v = 1{,}15\text{ m/s}$) xóa bỏ hoàn toàn khoảng cách chênh lệch này.
- **Các khung phải**: Một bầy (`wide` $N = 400$, 16 chó, hạt giống 2) từ cùng một điểm xuất phát; trên, khoảng cách từ tâm bầy tới đích; dưới, số cừu ngoài đích (thang symlog). Chó chạy nhanh ($1{,}50\text{ m/s}$, xanh dương) đưa được tất cả trừ một con vào đích, rồi lùa bầy ra ngoài qua đích và vào lại hai lần. Chó chạy chậm ($1{,}15\text{ m/s}$, cam) hoàn thành trong một lượt.
- **Ý nghĩa cốt lõi**: Thất bại nghiêm ngặt của các đội nhiều chó gắn với tốc độ của chó tại đích (biến mất ở $1{,}15\text{ m/s}$), chứ không phải do thiếu năng lực gom bầy.

---

### 3.5 RQ5: Những quy luật mở rộng nào đứng vững trước các biến thể kiểm tra độ nhạy?

**Câu trả lời trực tiếp cho RQ5**:
- **Dưới tiêu chí tiếp cận 99%**: Các quy luật mở rộng có tính bền vững đặc biệt cao. Trước các thay đổi về cách thả chó (`handler`, `ring`, `arcs`), cự ly xuất phát (15, 30, 60 m), tốc độ chó (1,15 so với 1,50), và bộ tham số cừu thực địa thu từ vòng đeo GPS, giá trị $D_{\min}$ chỉ dao động trong phạm vi khoảng **1 chó** so với mốc cơ sở (chênh nhiều nhất: bộ tham số matched, `outlier_rich` $N = 200$, 2–3 so với 1).
- **Dưới tiêu chí nghiêm ngặt 100%**: Giá trị biến động mạnh gấp 3 lần hoặc hơn, do những thay đổi nhỏ về hình học làm xáo trộn đường đi nhạy cảm của con cừu lạc cuối cùng.
- **Hình học chuồng đích**: Việc thu hẹp bán kính chuồng đích ($1{,}5 R_f$) là biến thể duy nhất làm tăng $D_{\min}$ dưới cả hai tiêu chí (dưới tiêu chí 99%, đẩy `wide` $N = 400$ từ 2–3 lên 5–6 chó). Riêng dưới tiêu chí nghiêm ngặt, bộ matched và gap 15 cũng đẩy một số ô lên none.

![Bản đồ nhiệt độ nhạy](../figures/fig24_sensitivity.png)

**Hình 6: Bản đồ nhiệt kiểm tra độ nhạy qua các biến thể thực nghiệm ở thời hạn $6\times$.**

Số liệu: [Sensitivity, strict: base / variant](results_tables.md#sensitivity-strict-base--variant) và [Sensitivity, 99 percent: base / variant](results_tables.md#sensitivity-99-percent-base--variant).

*Cách đọc biểu đồ:*
- **Đường phân cách ngang**: Tách biệt tiêu chí nghiêm ngặt 100% (nửa trên) và tiêu chí tiếp cận 99% (nửa dưới).
- **Các hàng & Cột**: Các hàng thử nghiệm các biến thể thả chó (`handler`, `ring`), cự ly (`gap 15`, `gap 60`), chuồng nhỏ (`goal 1.5 R_f`), chó điềm tĩnh (`dog speed 1.15`), và tham số thực địa GPS (`matched sheep set`). Các cột tương ứng với các tổ hợp bố cục (`wide`, `outlier_rich`) và quy mô bầy ($N \in \lbrace 100, 200, 400\rbrace$).
- **Màu sắc & Ô gạch chéo**: Màu càng đậm thể hiện $D_{\min}$ càng cao. Các ô gạch chéo ghi "none" thể hiện không có số chó nào đạt tin cậy.
- **Ý nghĩa cốt lõi**: Tiêu chí nghiêm ngặt (nửa trên) cực kỳ bất ổn và tràn ngập thất bại trên bầy lớn. Ngược lại, tiêu chí 99% (nửa dưới) duy trì sự nhất quán vững chắc: $D_{\min}$ chỉ lệch tối đa 1 chó so với chuẩn. Chỉ có việc thu hẹp chuồng đích mới thực sự làm tăng đòi hỏi số lượng chó.

---

### 3.6 RQ6: Đội chó không phối hợp (FAT) có đạt được quy mô *D*<sub>min</sub> hữu hạn không?

**Câu trả lời trực tiếp cho RQ6**:
- Hoàn toàn không. Một thuật toán tham lam thiếu cơ chế phân chia nhiệm vụ và tránh va chạm sẽ thất bại toàn diện trên các đàn cừu lớn.
- Mặc dù FAT thành công trên đàn nhỏ ($N \le 100$), nó ghi nhận **0 ô đạt độ tin cậy** khi bầy cừu tăng lên $N \ge 200$ trên các bố cục phân tán, và thất bại ngay cả trên bầy tập trung $N = 400$ nơi thuật toán phối hợp `strombom_multi` chỉ cần đúng 1 chú chó.
- **Nguyên nhân vật lý**: Vì tất cả các chú chó đều có cùng góc nhìn toàn cục, chúng cùng nhắm vào đúng một con cừu xa nhất ($\arg\max_i \lVert \mathbf{x}_ i - \mathbf{x}_ {\text{goal}} \rVert$) và dồn cục lại (trung vị tỷ lệ chó có một chó khác trong vòng 2 m: 0,86 trên compact và 0,79 trên split ở $N \ge 200$; 0,46 trên wide, 0,30 trên outlier_rich). Bổ sung thêm chó trong FAT không tạo ra việc làm song song. Đối chứng chó độc lập (mục 3.9), cũng không có tầng đội nhưng giữ công tắc gom/lùa, vẫn đạt $D_{\min}$ hữu hạn ở $N = 200$, nên thất bại của FAT không chỉ do thiếu phối hợp.

Bảng 5 so sánh $D_{\min}$ giữa FAT và `strombom_multi` ở thời hạn $6\times$:

| Bố cục | $N = 25$ | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `compact` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / [12] (1 / 1) |
| `wide` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / none (3 / 2) | none / none ([9] / 2–3) |
| `split` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / none (none / [1]) | none / none (none / [5]) |
| `outlier_rich` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 2 / 2 (3 / 2) | none / none ([12] / 2–3) | none / none (none / 3) |

Số liệu: [FAT dog rule, deadline 6](results_tables.md#fat-dog-rule-deadline-6-strict-then-99-percent) (`dmin_fat`, `dmin_f99_fat`); các giá trị `strombom_multi` trong ngoặc là `dmin_m6` và `dmin_f99_m6` trong [strict success](results_tables.md#d_min-by-layout-and-n-strict-success) và [success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent).

![FAT so với Team Rule](../figures/fig26_fat.png)

**Hình 7: Tỷ lệ thành công theo số lượng chó $D$ của thuật toán phối hợp `strombom_multi` (xanh dương) so với đối chứng không phối hợp FAT (cam) ở thời hạn $6\times$.**

Số liệu: tỷ lệ thành công từng ô trong `results/dmin_fat`, `dmin_f99_fat`, `dmin_m6` và `dmin_f99_m6` (không có bảng); $D_{\min}$ như trong Bảng 5.

*Cách đọc biểu đồ:*
- **Các khung**: Năm khung: `compact` $N = 400$, `wide` $N = 200$ và $400$, `outlier_rich` $N = 200$, `split` $N = 200$; đường nghiêm ngặt và 99% cho mỗi quy tắc. Điểm rỗng: ô có dưới 30 lượt chạy.
- **Các trục**: Số chó $D$ theo tỷ lệ thành công. Đường chấm đánh dấu $\theta = 0{,}90$.
- **Ý nghĩa cốt lõi**: Tỷ lệ thành công của FAT ở quanh hoặc dưới 0,5 tại mọi $D$ lớn hơn 2 (trên `wide` $N = 200$ nó tăng từ 0 tại $D = 1$ lên 0,30–0,55). `strombom_multi` đạt độ tin cậy trên `wide` và `outlier_rich`, nhưng không đạt trên `split` $N = 200$, nơi đường 99% giảm xuống 0,60 tại $D = 24$.

---

### 3.7 RQ7: Vượt quá *D*<sub>min</sub>: Bao nhiêu chó là đủ (*D*<sub>sat</sub>), Chi phí vận hành, và Áp lực lên bầy cừu

Sau khi đã tìm ra đội hình nhỏ nhất đạt độ tin cậy $D_{\min}$, một câu hỏi thực tế tối quan trọng được đặt ra cho các nhà quản lý nông trại và kỹ sư điều khiển robot:
*Nếu chúng ta đưa thêm chó vào làm việc vượt quá mức tối thiểu* $D_{\min}$*, liệu đàn cừu có được lùa về nhanh hơn không? Chi phí vận hành tăng nhanh thế nào, đàn cừu có bị hoảng loạn quá mức không, và sự đông đúc có làm tắc nghẽn gây sụp đổ nhiệm vụ không?*

Để trả lời, chúng tôi phân tích lại toàn bộ tập dữ liệu tiêu chí 99% trên 11 thư mục giao thức (các lưới chính, đối chứng FAT, và 7 giao thức độ nhạy: mốc cơ sở và 6 biến thể), đồng thời chạy replay chẩn đoán chi tiết trên 164 lượt mô phỏng đại diện để đo lường áp lực chạy trốn của từng cá thể cừu qua từng tích tắc. Mọi lượt replay đều tái tạo đúng kết quả và số tích tắc đã lưu.

#### 1. Ngưỡng bão hòa tốc độ (*D*<sub>sat</sub>)
- **Định nghĩa**: *D*<sub>sat</sub> là quy mô đội tin cậy nhỏ nhất mà từ đó trở đi, việc bổ sung thêm chó không mang lại sự rút ngắn thời gian hoàn thành có ý nghĩa thống kê (tốc độ đi ngang).
- **Phát hiện thực nghiệm**:
  - *Trên bầy tập trung ở mọi* $N$*, và ở* $N \le 50$ *trừ `outlier_rich`* $N = 50$ *(1–24)*: *D*<sub>sat</sub> = 1 ngay từ đầu. Một chú chó duy nhất đã lùa bầy cừu di chuyển ở vận tốc đi bộ tối đa ($1{,}0\text{ m/s}$); thêm chó không thể ép cừu đi nhanh hơn.
  - *Trên bầy phân tán ở thời hạn trung bình (*$6\times$): *D*<sub>sat</sub> dao động từ 2 đến 7 chó ở $N = 100$–400 (ví dụ `outlier_rich` $N = 100$ bão hòa tại *D*<sub>sat</sub> = 3; `wide` $N = 400$ tại *D*<sub>sat</sub> = 5).
  - *Các ô chưa phân định*: Trong các lượt chạy đầu, phép so sánh thời gian hoàn thành từng cặp còn chưa quyết định trên 6 trong 13 đường cong phân tán có giá trị, vì tài nguyên tính toán dồn cho ranh giới độ tin cậy (`decide_finish_times: false`), nên *D*<sub>sat</sub> được ghi dưới dạng khoảng chặn (ví dụ `wide` $N = 200$ là 3–24). Đợt chạy bổ sung đã phân định phần lớn (mục 3.8): trên `wide`, *D*<sub>sat</sub> giờ là 1, 1, 1, 2, 3, 3, 4, 5 từ $N = 25$ đến $400$. Ở $6\times$ vẫn còn là khoảng chặn trên 5 trong 23 đường cong phân tán (`outlier_rich` $N = 50$, 283, 400, 566; `wide` 566).

#### 2. Hiệu suất giảm dần và Chi phí vận hành (*D* > *D*<sub>sat</sub>)
- **Chó vượt quá bão hòa chỉ mang lại lợi ích tốc độ không đáng kể nhưng làm đội chi phí lên gấp bội**:
  - Trên toàn bộ 189 ô đạt tin cậy nằm trên một *D*<sub>sat</sub> đã quyết định ở thời hạn $6\times$ (chín quy mô bầy), thời gian hoàn thành luôn duy trì trong khoảng **0,96 đến 1,01 lần** thời gian tại mốc *D*<sub>sat</sub> (chỉ nhanh hơn tối đa 4%, đôi khi còn chậm đi 1%).
  - Trong khi đó, **tổng khối lượng công việc của đàn chó** (`dog_time` $= D \times T$) và tổng quãng đường chạy tăng tuyến tính theo đúng tỷ lệ $D / D_{\mathrm{sat}}$.
  - *Ví dụ thực tế*: Trên bầy cừu tập trung, việc thả 24 chú chó tiêu tốn năng lượng pin gấp 24 lần so với 1 chú chó, nhưng thời gian đưa đàn về đích là như nhau (ví dụ $N = 50$: 154 s với 1 chó, 154 s với 24 chó).

Bảng 6 tóm tắt chi phí vận hành tại mốc gấp đôi bão hòa (2 *D*<sub>sat</sub>) và tại mốc tối đa ($D = 24$) so với mốc chuẩn *D*<sub>sat</sub> trên các đường cong phân tán ở $6\times$:

| Bố cục, Quy mô bầy $N$ | Ngưỡng *D*<sub>sat</sub> | Tại 2 *D*<sub>sat</sub>: Thời gian / Công sức chó | Tại $D = 24$: Thời gian / Công sức chó |
| :--- | :---: | :---: | :---: |
| `wide`, $N = 200$ | 3 | 0,97 / 1,94 | 0,96 / 7,70 |
| `wide`, $N = 400$ | 5 | 0,97 / 2,32 (tại $D = 12$) | 0,96 / 4,61 |
| `outlier_rich`, $N = 100$ | 3 | 0,99 / 1,98 | 0,98 / 7,85 |
| `outlier_rich`, $N = 400$ | 6–24 | 0,96 / 1,91 | 0,94 / 3,74 |
| `split`, $N = 100$ | 4 | 0,99 / 1,98 | 0,99 / 5,91 |

*Ý nghĩa của Bảng 6*: Tại $D = 24$, thời gian lùa chỉ nhanh hơn từ 1% đến 6% ($0{,}94 - 0{,}99$), nhưng tổng tiêu hao pin và công sức của đàn chó tăng vọt từ **3,7 đến 7,9 lần** ($3{,}74 - 7{,}85$). Giá trị sau đợt chạy bổ sung thời gian hoàn thành (`uv run cli/dmin_tables.py effort dmin_f99_m6`).

Số liệu: [Effort, dmin_f99_m6](results_tables.md#effort-dmin_f99_m6-cost-of-dogs-beyond-d_sat-relative-to-the-d_sat-cell-1) và [D_sat, dmin_f99_m6](results_tables.md#d_sat-dmin_f99_m6-d_sat-1), sau đợt chạy bổ sung (giá trị của các lượt chạy đầu nằm trong [D_sat, effort, zones and methods, 99 percent](results_tables.md#d_sat-effort-zones-and-methods-99-percent)).

#### 3. Tâm lý hoảng loạn và Phúc lợi bầy cừu
Một mối lo ngại lớn trong robot nông nghiệp là liệu một đàn chó đông đúc có gây stress hoặc làm đàn cừu kiệt sức không. Dữ liệu đo đạc từng giây cho thấy điều ngược lại:
- **Tổng thời gian chạy trốn của mỗi con cừu thực chất giảm đi**: Một con cừu chỉ rơi vào trạng thái hoảng loạn bỏ chạy khi có chó tiến vào cự ly $65\text{ m}$. Khi tăng số chó từ $D_{\min}$ lên *D*<sub>sat</sub>, việc gom cừu lạc diễn ra song song nhanh hơn nhiều, rút ngắn tổng thời gian mỗi con cừu phải tháo chạy (trên `wide` $N = 400$, trung vị thời gian chạy trốn của mỗi con cừu giảm từ 485 s tại $D = 3$ xuống còn 359 s tại $D = 6$). Vượt quá *D*<sub>sat</sub>, thời gian chạy trốn duy trì đi ngang (361 s tại $D = 12$).
- **Tỷ lệ cừu chạy trốn tức thời tăng lên**: Tại một giây bất kỳ, đàn chó đông hơn sẽ giăng một vòng cung rộng hơn, khiến một tỷ lệ bầy cừu lớn hơn cùng chuyển động (trung vị tăng từ 68% bầy cừu chạy trốn tại $D = 3$ lên 84% tại $D = 12$). Tuy nhiên, do tổng thời gian hoàn thành ngắn hơn, tổng mức độ phơi nhiễm áp lực không hề bị đội lên.
- **Khoảng cách an toàn luôn được bảo toàn**: Dưới quy tắc giữ khoảng cách $3 r_a = 6\text{ m}$, thời gian một con cừu ở trong vòng 6 m của một chú chó luôn dưới 1,3 s mỗi con (trung vị) ở mọi $D$ đã thử, không có xu hướng đều theo $D$.

#### 4. Tính ổn định hệ thống: Không có hiện tượng quá tải sụp đổ dưới tiêu chí 99%
- Dưới tiêu chí 99%, trên toàn bộ 11 bộ thử nghiệm lên tới $D = 24$ chó, **chúng tôi không ghi nhận bất kỳ ngưỡng quá tải sụp đổ ($D_{\mathrm{overcrowd}}$) nào** trên năm quy mô bầy gốc.
- Trên các quy mô đó, không có đường cong nào bị rớt khỏi ngưỡng tin cậy sau khi đã đạt được nó. Sự sụp đổ từng thấy dưới tiêu chí 100% trên `split` $N = 100$ ở $3\times$ biến mất dưới tiêu chí 99%. *Hiệu chỉnh từ lưới dày (mục 3.8)*: ở quy mô bổ sung `split` $N = 141$ ($6\times$), $D = 4$ thành công trong 0,80 số lượt trong khi $D = 3$ và $D \ge 7$ đạt tin cậy ($D = 5$ và $6$ chưa quyết định), một lần sụt duy nhất, lại trên `split`.
- Thêm chó làm chậm đi trên `split` và với đối chứng FAT. Với các phép so sánh thời gian hoàn thành đã được bổ sung (mục 3.8), `split` ở $12\times$ chậm hơn khi thêm chó ở mọi $N$ từ 200 đến 566 (ví dụ $N = 400$: 950–1040 s với $D \ge 9$ so với 839 s tại $D = 5$), dù vẫn hoàn thành tin cậy. `wide` không chậm lại như vậy; `outlier_rich` chỉ chậm lại ở $N = 566$ ($D \ge 15$: khoảng 1130–1170 s so với 628 s tại $D = 10$).

![Chi phí chó vượt quá D_sat](../figures/fig33_effort.png)

**Hình 8: Chi phí vận hành và hiệu suất giảm dần vượt quá quy mô bão hòa $D_{\mathrm{sat}}$ (thời hạn $6\times$, tiêu chí 99%).**

Số liệu: [Effort, dmin_f99_m6](results_tables.md#effort-dmin_f99_m6-cost-of-dogs-beyond-d_sat-relative-to-the-d_sat-cell-1) (sau đợt chạy bổ sung hạt giống thời gian).

*Cách đọc biểu đồ:*
- **Khung trái**: Thời gian hoàn thành so với ô $D_{\mathrm{sat}}$ ($T / T_{\mathrm{sat}}$) theo $D / D_{\mathrm{sat}}$ (thang log), mỗi đường cong có $D_{\mathrm{sat}}$ đã quyết định là một đường, tô màu theo bố cục. Mọi giá trị nằm trong khoảng 0,96 đến 1,01.
- **Khung phải**: Tổng công sức của đàn chó (`dog_time` $= D \times T$) so với ô $D_{\mathrm{sat}}$, bám theo đường chéo $D / D_{\mathrm{sat}}$.
- **Ý nghĩa cốt lõi**: Bố trí thêm chó vượt quá $D_{\mathrm{sat}}$ chỉ rút ngắn thời gian dưới 4%, trong khi thời gian chó tăng tỷ lệ với quy mô đội.

![Áp lực lên bầy cừu](../figures/fig34_pressure.png)

**Hình 9: Động lực học chạy trốn vi mô của bầy cừu qua các quy mô đội chó (12 hạt giống mỗi ô, 10 tại $D = 1$, $N = 400$; `dmin_f99_m6`).**

Số liệu: [Pressure, dmin_f99_m6](results_tables.md#pressure-dmin_f99_m6-replay-of-12-stored-seeds-per-cell-every-replay-reproduced-its-stored-trial).

*Cách đọc biểu đồ:*
- **Các đường**: Mỗi bố cục và $N$ là một đường; tròn và nét chấm cho $N = 100$, vuông và nét liền cho $N = 400$. Cả hai khung là trung vị trên các hạt giống thành công.
- **Khung trái**: Số giây chạy trốn của mỗi con cừu (thời gian nằm trong cự ly đe dọa $65\text{ m}$ của chó).
- **Khung phải**: Tỷ lệ bầy cừu đang bỏ chạy tại một giây (0 đến 1).
- **Ý nghĩa cốt lõi**: Thêm nhiều chó không làm tăng tổng thời gian chịu áp lực của từng cá thể cừu: vượt quá $D_{\mathrm{sat}}$, thời gian chạy trốn chỉ lệch trong khoảng 2%. Tăng từ $D_{\min}$ lên $D_{\mathrm{sat}}$ giúp rút ngắn thời gian lùa bầy, từ đó giảm tổng thời gian cừu phải bỏ chạy (trái). Mặc dù tại mỗi thời điểm có tỷ lệ cừu tháo chạy cao hơn (phải), tổng thời gian chịu đe dọa lại ít hơn.

---

### 3.8 RQ8: Tăng trưởng theo *N* trên Lưới dày, *D*<sub>sat</sub>, và Hình dạng đường cong

Để xác định chính xác hình dạng hàm số của đường cong tăng trưởng $D_{\min}(N)$, chúng tôi mở rộng các lưới chạy 99% ($12\times$ và $6\times$) thêm 4 quy mô bầy trung gian: $N = 71, 141, 283$ (các trung điểm logarit giữa 50 và 400) và $N = 566 = 400\sqrt{2}$.

**Vì sao là các bước $\sqrt{2}$?** Việc chia tỷ lệ theo các bước nhân $\sqrt{2}$ đảm bảo mọi quy mô bầy đều có trọng số hình học ngang nhau khi khớp hồi quy log-log. Đồng thời, $N = 566$ là giới hạn vật lý của mô hình sinh học Strömbom: dưới 600 con, đàn cừu luôn ổn định về một bán kính dừng tự nhiên $R_f(N)$. Trên 600 con, bầy cừu xuất phát lỏng lẻo không còn khả năng tự co cụm về kích thước riêng (tại $N = 630$, bầy xuất phát rộng vẫn to hơn 17%; tại $N = 800$, quy trình hiệu chuẩn bán kính thất bại hoàn toàn).

**Câu trả lời trực tiếp cho RQ8**:
- **Hệ số góc được xác định chặt chẽ**: Trên lưới 9 quy mô bầy, hệ số góc log-log của $D_{\min}$ theo $N$ dao động từ **0,27 đến 0,38** (`wide`) và **0,28 đến 0,38** (`outlier_rich`) ở thời hạn thong thả ($12\times$), và từ **0,38 đến 0,61** ở thời hạn trung bình ($6\times$). Dưới điều kiện thong thả, tốc độ tăng trưởng luôn nằm dưới định luật căn bậc hai ($\alpha = 0{,}50$) của bầy không liên kết.
- ***D*<sub>sat</sub> tăng nhanh gấp đôi $D_{\min}$**: Trên bầy `wide`, *D*<sub>sat</sub> tăng đều đặn: $1, 1, 1, 2, 3, 3, 4, 5$ chó từ $N = 25$ đến $400$, và đạt $7\text{--}24$ ở $N = 566$ (độ dốc log-log **0,70 đến 0,91**). Khoảng cách giữa đội hình chỉ cần đạt độ tin cậy và đội hình đạt tốc độ tối đa ngày càng giãn rộng khi đàn cừu lớn dần.
- **Tăng đều hay chững lại**: Đến mốc $N = 566$, dữ liệu thực nghiệm khớp hoàn hảo với cả hàm lũy thừa không chặn ($D \propto N^\alpha$) lẫn hàm bão hòa đi ngang (tỷ số hợp lý $\approx 1$). Cả hai dạng đường cong đều đi qua toàn bộ các khoảng chặn $D_{\min}$. Khi ngoại suy lên $N = 1600$, cả hai hàm số cho phép giá trị dao động từ 1,5 đến 6,7 chó ở $12\times$ (3,1 đến 10,4 ở $6\times$); chỉ khi thử nghiệm các bầy cực lớn ($N \gt 1000$) mới có thể phân định được (mục 3.13).

Bảng 7 thể hiện bước tiến thực nghiệm qua 9 quy mô bầy (tiêu chí 99%):

| $N$ | 25 | 50 | 71 | 100 | 141 | 200 | 283 | 400 | 566 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `wide`, $12\times$ | 1 | 1 | 1 | 1 | 2 | 1–2 | 2 | 2 | 2–3 |
| `outlier_rich`, $12\times$ | 1 | 1 | 1 | 1–2 | 2 | 2 | 2 | 2 | 2–3 |
| `wide`, $6\times$ | 1 | 1 | 1 | 1 | 2 | 2 | 2–3 | 2–3 | 3–7 |
| `outlier_rich`, $6\times$ | 1 | 1 | 1 | 2 | 2 | 2–3 | 2–3 | 3 | 3–6 |
| *D*<sub>sat</sub> `wide`, $6\times$ | 1 | 1 | 1 | 2 | 3 | 3 | 4 | 5 | 7–24 |

Số liệu: [Finish-time top-up, densified N, independent shepherds, Kubo to D = 24, 99 percent](results_tables.md#finish-time-top-up-densified-n-independent-shepherds-kubo-to-d--24-99-percent).

![D_min trên chín kích thước bầy](../figures/fig35_growth_fits.png)

**Hình 10: Quy mô đội tối thiểu $D_{\min}$ qua chín kích thước bầy và các dải ngoại suy của hai mô hình tăng trưởng.**

Số liệu: [D_min, dmin_f99_m12](results_tables.md#d_min-dmin_f99_m12), [D_min, dmin_f99_m6](results_tables.md#d_min-dmin_f99_m6) và các phép khớp cho [dmin_f99_m12](results_tables.md#fits-dmin_f99_m12-d_minn-power-law-against-saturating-curve) và [dmin_f99_m6](results_tables.md#fits-dmin_f99_m6-d_minn-power-law-against-saturating-curve).

*Cách đọc biểu đồ:*
- **Các khung**: Trái $12\times$, phải $6\times$; `wide` tròn, `outlier_rich` vuông; cả hai trục thang log.
- **Các trục & Dữ liệu**: Quy mô bầy $N$ theo $D_{\min}$. Các thanh dọc là khoảng chặn $D_{\min}$. Một đường dọc đánh dấu giới hạn hiệu chuẩn ($N \approx 600$).
- **Dải ngoại suy (Bên phải $N = 566$)**: Vùng tô bóng là phạm vi $D$ mà mọi luật lũy thừa ($D \propto N^\alpha$, cạnh trên nét đứt) hoặc mọi đường cong bão hòa (cạnh trên nét chấm) đi qua tất cả các khoảng chặn cho phép.
- **Ý nghĩa cốt lõi**: Trên chín quy mô, hai dạng khớp tốt như nhau (log-odds 0,0). Cả hai đều khẳng định việc chăn hàng trăm con cừu chỉ cần một số lượng chó rất nhỏ, nhưng để biết đường cong có thực sự đi ngang hay không đòi hỏi phải khảo sát vượt qua ngưỡng hiệu chuẩn sinh học của mô hình.

---

### 3.9 RQ9: Phần nào của Quy tắc Đội đóng vai trò quyết định, và Mô hình lực liên tục

Trong Mục 3.6, mô hình không phối hợp FAT đã thất bại ở $N \ge 200$ trên các bố cục phân tán. Tuy nhiên, FAT thiếu cả *hai* thành phần: (1) máy trạng thái hành vi Strömbom (chuyển đổi giữa gom cừu lạc và lùa đàn), và (2) tầng phối hợp đa tác tử (phân công Hungarian và dàn vòng cung lùa).

Để tách bạch hai thành phần này, chúng tôi thử nghiệm đội **chó độc lập (`dmin_f99_indep`)**: mỗi chú chó chạy máy trạng thái một-chó gốc của Strömbom (2014) hoàn toàn độc lập, không hề giao tiếp hay phân chia nhiệm vụ.

**Câu trả lời trực tiếp cho RQ9**:
- **Công tắc chuyển trạng thái gánh vác đội hình đến $N = 200$; tầng phối hợp đội là chìa khóa mở cánh cửa $N = 400$**:
  - Đội chó độc lập đạt độ tin cậy trên mọi bố cục phân tán lên đến $N = 200$, nơi FAT thất bại 100%. Điều này gợi ý rằng riêng cơ chế chuyển đổi giữa gom cừu lạc và lùa bầy đã đủ ở quy mô vừa và nhỏ.
  - Tuy nhiên, tại $N = 400$, đội chó độc lập thất bại hoàn toàn, trong khi thuật toán phối hợp `strombom_multi` thành công với 2–3 chó trên `wide` và `outlier_rich` (trên `split` nó cũng không có đội tin cậy). Sự phối hợp phân công tối ưu là bắt buộc trên đàn lớn.
- **Động lực học của Mô hình lực liên tục (Kubo đến 24 chó)**:
  - Trên bầy tập trung, $D_{\min} = 1$ trên mọi $N \in [25, 100]$, tái khẳng định phát hiện cốt lõi của chúng tôi.
  - Khác với cừu Strömbom (thời gian hoàn thành không đổi theo $D$ khi vượt quá *D*<sub>sat</sub>), cừu Kubo chịu các lực trường thế liên tục cộng dồn. Ở $N = 100$, thời gian lùa giảm mạnh từ $115\text{ s}$ với 1 chó xuống $29\text{ s}$ với 10 chó, và đạt $25\text{ s}$ với 24 chó. Phần lớn mức cải thiện đạt được trước mốc $D = 10$, xác nhận quy luật hiệu suất giảm dần trên cả hai trường phái vật lý.

Bảng 8 so sánh chó độc lập với thuật toán phối hợp và FAT ở thời hạn $6\times$:

| So sánh phương pháp (`strombom_multi` / `independent` / `fat`), 99%, $6\times$ | $N = 200$ | $N = 400$ |
| :--- | :---: | :---: |
| `wide` | 2 / 2–3 / none | 2–3 / none / none |
| `outlier_rich` | 2–3 / 3 / none | 3 / none / none |
| `split` | [1] / 1–3 / none | [5] / none / none |

Số liệu: [Methods at 99 percent, 6 drive times](results_tables.md#methods-at-99-percent-6-drive-times-team-rule-independent-paper-shepherds-fat) và [Kubo, compact, D to 24](results_tables.md#kubo-compact-d-to-24-99-percent); thời gian hoàn thành của Kubo lấy từ `results/dmin_f99_kubo` (không có bảng).

---

### 3.10 RQ10: Quá nhiều chó: Bài toán Giữ đàn và Chó chiếm chỗ không gian

Trong bài toán lùa đàn mở, thêm chó vượt quá mức bão hòa không làm hỏng nhiệm vụ dưới tiêu chí 99%. Tuy nhiên, các tài liệu robot bầy đàn cho rằng sự quá tải gây hại chủ yếu ở giai đoạn chặn giữ (Green et al. 2022). Chúng tôi đánh giá hai thay đổi:

1. **Nhiệm vụ Giữ đàn (Holding Task)**: Nhiệm vụ chỉ thành công sau khi 99% cừu ở yên trong đích trọn vẹn một khoảng thời gian lùa ($T_{\mathrm{drive}}$). Khi cừu đã vào chuồng, đàn chó chủ động lùi xa ngoài cự ly đe dọa ($65 + 2\text{ m}$) để cừu gặm cỏ bình yên.
2. **Chó chiếm chỗ vật lý (Dog Spacing)**: Chó có kích thước cơ thể thực tế: không chú chó nào được bước vào phạm vi $2\text{ m}$ của đồng đội (`dog_spacing = 2.0`). Do vòng cung lùa có chu vi giới hạn, nó chỉ có thể chứa tối đa một số lượng chó nhất định: $D_{\mathrm{cap}} \approx 7, 9, 10, 11, 12$ tương ứng với $N = 25$ đến $400$.

**Câu trả lời trực tiếp cho RQ10**:
- **Nhiệm vụ Giữ đàn thành công từ $N = 100$, nhưng thất bại ở bầy nhỏ ($N \le 50$) do hình học chuồng đích**:
  - Khi giữ đàn, chó phải lùi ra ngoài $65\text{ m}$, và chuồng đích của bầy nhỏ chỉ rộng $12\text{--}14\text{ m}$; các lượt giữ đàn thất bại ở $N \le 50$ thường kết thúc do kẹt hoặc hết giờ hơn là do bầy thoát ra. Trên `wide` (và `compact`) ở $N \ge 100$, việc giữ đàn thành công tin cậy và $D_{\min}$ trùng khớp với bài toán lùa mở (1, 2, và 3 chó tại $N = 100, 200, 400$). Trên `split`, giữ đàn không có đội tin cậy ở $N = 200$ và $400$, còn `outlier_rich` cần 3 chó ở $N = 100$ so với 2 khi lùa mở.
- **Kích thước cơ thể chó gây ra hiện tượng sụp đổ do quá tải ($D_{\mathrm{overcrowd}}$)**:
  - Trên bố cục `outlier_rich` ở $N = 400$, đội từ $3\text{--}6$ chó thành công trong 92,5–94% lượt chạy (chưa quyết định; không có đội tin cậy). Khi quy mô đội đạt $D \ge 9$, **toàn bộ các đội đến 24 chó đều bị xác nhận không đạt độ tin cậy** (tỷ lệ thành công sụt xuống 0,77 tại $D = 9$, 0,65 tại $D = 12$, và 0,50 tại $D = 16$). Tình trạng ùn ứ trên vòng cung lùa khiến đàn chó mất khả năng xoay xở, phá hỏng hoàn toàn nhiệm vụ.
  - Trên bố cục `wide` và `compact`, các chú chó không tìm được vị trí trên vòng cung sẽ tự động đứng yên phía sau, duy trì độ tin cậy đến 24 chó. Tác hại của sự quá tải phụ thuộc mật thiết vào bố cục không gian và thể tích vật lý của tác tử.

![Giữ đàn với chó chiếm chỗ](../figures/fig36_spacing.png)

**Hình 11: Độ tin cậy của nhiệm vụ Giữ đàn tại $N = 400$ so sánh giữa chó dạng điểm và chó có kích thước vật lý (giãn cách $2\text{ m}$).**

Số liệu: [D_min, dmin_f99_hold](results_tables.md#d_min-dmin_f99_hold) và [D_min, dmin_f99_hold_spacing](results_tables.md#d_min-dmin_f99_hold_spacing).

*Cách đọc biểu đồ:*
- **Các khung hình**: Khung trái đánh giá bố cục `wide`; khung phải đánh giá bố cục `outlier_rich`.
- **Các trục & Đường nét**: Số chó $D$ (thang log) theo tỷ lệ thành công của nhiệm vụ giữ đàn. Xám nét chấm: chó dạng điểm; xanh dương nét liền: chó cách nhau $2\text{ m}$; dải cam: sức chứa của vòng cung lùa ($D = 10$–12); nét đứt: $\theta = 0{,}90$; điểm rỗng: ô có dưới 30 lượt chạy.
- **Ý nghĩa cốt lõi**: Trên bố cục `wide`, chó chiếm chỗ không gây hại vì chó thừa đứng lùi lại phía sau. Nhưng trên `outlier_rich`, chó chiếm chỗ gây ra hiện tượng sụp đổ do quá tải nghiêm trọng: tỷ lệ thành công lao dốc từ $D = 9$ trở lên do vòng cung lùa bị kẹt cứng, triệt tiêu khả năng điều phối tập thể.

---

### 3.11 RQ11: Độ gắn kết xã hội làm thay đổi quy luật mở rộng ra sao?

Định luật tỷ lệ căn bậc hai $\alpha = 0{,}50$ ($\sqrt{M}$) của Lama và di Bernardo (2024) được chứng minh trên các mục tiêu hoàn toàn không có lực gắn kết bầy đàn. Để bắc cầu giữa các hạt vật lý rời rạc với bầy cừu sinh học, chúng tôi thay đổi hai tham số gắn kết: (1) trọng số hút xã hội $c$ (từ $1{,}05$ lên $2{,}0$), và (2) tỷ lệ láng giềng tương tác $n / N$ (thử nghiệm $n = 0{,}5N$).

**Câu trả lời trực tiếp cho RQ11**:
- **Gắn kết mạnh hơn chỉ mang lại lợi ích rất nhỏ**: Tăng trọng số hút từ $c = 1{,}05$ lên $1{,}3, 1{,}6$, hoặc $2{,}0$ cho hệ số góc như nhau ($\alpha = 0{,}20$ trên `wide`), chỉ tiết kiệm tối đa 1 chó trên toàn bộ các quy mô bầy. Lực hút tự nhiên vốn có của cừu đã đủ mạnh để việc kéo chặt hơn không giúp ích thêm nhiều.
- **Gắn kết yếu hơn làm độ dốc dựng đứng tiệm cận định luật căn bậc hai**: Giảm số lượng láng giềng tương tác xuống $n = 0{,}5N$ làm độ dốc tăng lên **0,40 đến 0,70**, một khoảng chứa mốc $\alpha = 0{,}50$ của mục tiêu không liên kết. Bố cục `split` trở nên khó hơn rất nhiều ($D_{\min}$ tăng từ 1 lên 3–4 ở $N = 200$, và từ 2 lên 4–5 ở $N = 400$). Bầy cừu có độ gắn kết yếu hơn $n = 0{,}5N$ sẽ vỡ vụn hoàn toàn dưới áp lực lùa của 1 chú chó.

Bảng 9 tóm tắt độ dốc mở rộng qua các mức độ gắn kết (`wide`, tiếp cận 99%, $12\times$):

| Mức độ gắn kết (`wide`, 99%, $12\times$) | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ | Hệ số góc log-log $\alpha$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Gắn kết yếu ($n = 0{,}5N$)** | 1 | 1 | 2 | 2–4 | **0,40 đến 0,70** |
| **Mốc chuẩn sinh học ($c = 1{,}05$)** | 1 | 1 | 1–2 | 2 | **0,20 đến 0,30** |
| **Gắn kết rất mạnh ($c = 1{,}3, 1{,}6, 2{,}0$)** | 1 | 1 | 1 | 2 | **0,20** |

Số liệu: hàng mốc chuẩn lấy từ [dmin_f99_m12](results_tables.md#dmin_f99_m12) và [Growth with N, 99 percent](results_tables.md#growth-with-n-99-percent); [D_min, dmin_f99_c1.3](results_tables.md#d_min-dmin_f99_c13), [dmin_f99_c1.6](results_tables.md#d_min-dmin_f99_c16), [dmin_f99_c2.0](results_tables.md#d_min-dmin_f99_c20) và [D_min, dmin_f99_k05](results_tables.md#d_min-dmin_f99_k05). Độ dốc của các lượt chạy độ gắn kết: [dmin_f99_c1.3](results_tables.md#dmin_f99_c13), [c1.6](results_tables.md#dmin_f99_c16), [c2.0](results_tables.md#dmin_f99_c20) và [k05](results_tables.md#dmin_f99_k05) trong khối growth.

---

### 3.12 RQ12: Giới hạn Tầm nhìn và Mạng lưới Giao tiếp giữa các Chú chó

Trong thực tế, robot hoặc thiết bị bay không người lái (drone) không thể có tầm nhìn toàn cục bao quát toàn bộ cánh đồng. Chúng tôi đánh giá các kịch bản trong đó mỗi chú chó chỉ nhìn thấy cừu trong một bán kính cảm nhận hữu hạn ($15, 30, 45, 65, 100\text{ m}$), kết hợp với ba cấu hình giao tiếp: `none` (tự quan sát độc lập), `neighbour` (chia sẻ với các chó ở gần), và `shared` (mạng lưới toàn đội).

**Câu trả lời trực tiếp cho RQ12**:
- **Tầm nhìn 30–65 m làm tốn thêm khoảng 1 chú chó ở $N = 200$**: Trên bầy `wide`, đội có tầm nhìn toàn cục cần $D_{\min} = 2$. Giới hạn tầm nhìn xuống $30\text{--}65\text{ m}$ đẩy nhu cầu lên $D_{\min} = 3$ (3–4 ở 45 m). Ở $N \le 100$, tầm nhìn cục bộ không gây thiệt hại nào vì cả đàn cừu nằm gọn trong phạm vi $65\text{ m}$.
- **Tầm nhìn dưới 30 m gây sụp đổ trên `wide`**: Tại bán kính $15\text{ m}$ (trên `split`, $D_{\min}$ vẫn là 1 ở $N = 50$ và 100): ở $N = 50$, không đội nào đến 16 chó đạt độ tin cậy; ở $N = 100$, cần ít nhất 6 chó. Các chú chó mất dấu cừu lạc và đi lang thang mất phương hướng.
- **Giao tiếp mạng lưới mua lại chú chó bị mất**: Tại tầm nhìn $65\text{ m}$ ($N = 200$), chó độc lập cần 3 con. Việc chia sẻ thông tin vị trí cừu cho toàn đội giúp đưa $D_{\min}$ trở lại mức 2 chó, ngang bằng với tầm nhìn toàn cục mà không cần nâng cấp cảm biến phần cứng. Chỉ chia sẻ với chó trong tầm không làm giảm $D_{\min}$ (vẫn 3). Trên `split` $N = 200$, chia sẻ không đưa về được giá trị toàn cục (3 so với [1]).

![D_min theo tầm nhìn và giao tiếp](../figures/fig37_view.png)

**Hình 12: Tác động của tầm cảm nhận cá thể và mạng lưới giao tiếp đa tác tử lên quy mô đội $D_{\min}$.**

Số liệu: [Views: sensing range](results_tables.md#views-sensing-range-no-sharing-base-row--range-0-global) và [Views: sharing at range 65](results_tables.md#views-sharing-at-range-65-beside-the-no-sharing-rows-of-dmin_f99_view_range).

*Cách đọc biểu đồ:*
- **Khung trái**: $D_{\min}$ theo bán kính cảm nhận (m) cho `wide` (tròn) và `split` (vuông) ở $N = 100$ (mờ) và $N = 200$; các điểm được dịch ngang, và một đường nét đứt đánh dấu $r_s = 65$. Các thanh dọc là khoảng chặn; tam giác rỗng là cận dưới.
- **Khung phải**: Tỷ lệ thành công theo số chó trên `wide` $N = 200$ ở tầm $65\text{ m}$: không chia sẻ (nét chấm), chia sẻ với chó trong tầm (nét đứt), chia sẻ toàn đội (nét liền), đều màu xanh dương, và tầm nhìn toàn cục (đen).
- **Ý nghĩa cốt lõi**: Giới hạn tầm nhìn ở mức $30\text{--}65\text{ m}$ tốn thêm 1 chó trên `wide` ở $N = 200$, trong khi tầm nhìn dưới $30\text{ m}$ gây thất bại nặng nề ở đó. Chia sẻ với cả đội lấy lại được con chó đó trên `wide`.

---

### 3.13 RQ13: Đàn cừu quy mô cực lớn và Giới hạn Toán học của Quy tắc Lùa đàn

Để khảo sát giới hạn mở rộng tận cùng của bài toán chăn dắt, chúng tôi thử nghiệm các đàn cừu khổng lồ từ $N = 800$ đến $3200$ con ở thời hạn thong thả ($12\times$). Phía trên ngưỡng hiệu chuẩn ($N = 566$), bán kính đàn cừu được áp đặt bằng cách giữ nguyên mật độ: $R_f(N) = R_f(566)\sqrt{N/566}$.

**Câu trả lời trực tiếp cho RQ13**:
- **Quy tắc lùa của Strömbom gặp điểm kỳ dị toán học tại $N \approx 1056$**:
  - Quy tắc Strömbom nguyên bản đặt vị trí lùa đàn ở khoảng cách $r_a\sqrt{N}$ phía sau trọng tâm bầy cừu.
  - Tại $N = (r_s / r_a)^2 = (65 / 2)^2 = 1056$ cừu, cự ly này bằng đúng tầm nhìn phát hiện đe dọa của cừu ($65\text{ m}$).
  - Vượt quá $N = 1056$, các chú chó đứng quá xa đến mức **phần lớn bầy cừu không cảm nhận được chó** và vẫn ở trạng thái gặm cỏ. Tại $N = 1131$, không đội chó nào đến $D = 12$ thành công (0 trên 10 lượt ở mọi $D$).
- **Giới hạn cự ly lùa giải cứu bài toán đàn cừu khổng lồ**:
  - Bằng cách đặt trần cự ly lùa tối đa ($r_s - r_a = 63\text{ m}$), đàn chó luôn duy trì tiếp xúc giác quan với rìa sau của bầy, lùa thành công các đàn cừu khổng lồ.
  - Trên bầy tập trung (`compact`), 1 chú chó duy nhất ($D_{\min} = 1$) lùa nhẹ nhàng đàn $N = 800$ và $1131$ con, và 2 chó lùa đàn $N = 1600$. Tại $N = 3200$, các đội từ 3 đến 12 chó thành công trong cả 42 lượt chạy trước khi quy mô này bị bỏ ($D = 1$ và 2 chưa được chạy).
  - Trên bầy phân tán (`wide`), nhu cầu chó tăng vọt: 3 chó ở $N = 800$, 5–9 chó ở $N = 1131$, và vượt quá 12 chó ở $N = 1600$. Sự gia tăng dốc đứng này chứng minh rằng việc bao quát chu vi của một bầy phân tán khổng lồ đòi hỏi một đội ngũ tác tử lớn hơn nhiều để khóa các cánh.

Bảng 10 tóm tắt kết quả với quy tắc lùa có giới hạn trần cự ly (tiêu chí 99%, $12\times$):

| Giới hạn cự ly lùa ($63\text{ m}$ cap), 99%, $12\times$ | $N = 800$ | $N = 1131$ | $N = 1600$ | $N = 3200$ (Kiểm thử một phần) |
| :--- | :---: | :---: | :---: | :---: |
| `compact` | 1 | 1 | 2 | 42 / 42 thành công ở $D = 3$–12 ($D = 1, 2$ chưa chạy) |
| `wide` | 3 | 5–9 | none đến 12 | **none** (0 / 58 ở $D = 2\text{--}12$) |

Số liệu: [dmin_f99_big_cap](results_tables.md#dmin_f99_big_cap) cho các lượt chạy có giới hạn trần; cột $N = 3200$ lấy từ `results/dmin_f99_big_cap` (100 lượt, bị bỏ trước khi lượt chạy kết thúc và không được tính vào tổng). Các lượt chạy không giới hạn nằm trong [D_min, dmin_f99_big](results_tables.md#d_min-dmin_f99_big), [dmin_f99_big_dense](results_tables.md#d_min-dmin_f99_big_dense), [dmin_f99_big_loose](results_tables.md#d_min-dmin_f99_big_loose) và [Large N: flock size against the imposed R_f](results_tables.md#large-n-flock-size-against-the-imposed-r_f-compact).

### 3.14 RQ14: Mục tiêu không gắn kết: Quy luật căn bậc hai của Lama và di Bernardo (2024) trong HerdSim

Mục 5.1 so sánh độ dốc của HerdSim với quy luật căn bậc hai mà Lama và di Bernardo (2024) tìm thấy cho các mục tiêu không gắn kết. Quy luật đó được đo trong một mô phỏng khác, với nhiệm vụ và quy tắc người chăn khác, nên phép so sánh dựa trên ba khác biệt cùng lúc. Ở đây mô hình của bài báo chạy ngay trong HerdSim dưới tên phương pháp `lama`, trên nhiệm vụ riêng `gather` ([mô hình](../methods/models_vi.md#mô-hình-mục-tiêu-brownian-không-liên-kết-lama-2024), [nhiệm vụ](../experiments/task_design_vi.md#6-nhiệm-vụ-gom-lama-và-di-bernardo-2024)): mục tiêu chuyển động Brown bị người chăn trong bán kính $\lambda = 2{,}5$ đẩy ra xa theo hàm tuyến tính, người chăn đuổi mục tiêu xa đích nhất trong tầm, mọi tác nhân xuất phát đều trong một đĩa bán kính $R = 50$ quanh đích bán kính $R/5$, thành công khi 99% mục tiêu vào đích, và giới hạn 5000 s của bài báo. Bài báo viết $N$ cho người chăn và $M$ cho mục tiêu; ở đây, như mọi nơi trong báo cáo này, $D$ là số người chăn và $N$ là số mục tiêu.

Hai thống kê được đọc từ cùng các lượt chạy. Thống kê của bài báo là tỷ lệ trung bình mục tiêu trong đích lúc kết thúc một lượt; một cỡ đội được xem là đạt khi trung bình đó ít nhất bằng 0,99. Thống kê của HerdSim là quy tắc của mọi mục khác: tỷ lệ thành công (số lượt kết thúc với 99% trong đích) phải nằm tại hoặc trên 0,90 với độ tin cậy 99%. Hai giao thức `lama_r50` (bán kính cảm nhận 10, Hình 2b của bài báo) và `lama_r50_inf` (cảm nhận vô hạn, Hình 2a) phủ lưới của bài báo: $\sqrt{N} = 1$ đến 20 và $D = 1$ đến 25.

**Kiểm chứng trước các chiến dịch.** Bài báo không công bố mã, nên Hình 2 của nó được đọc từng ô từ ảnh raster qua chính thang màu của hình. Pilot đầu tiên (5.700 lượt) cần ít hơn bài báo tới hai người chăn ở biên nơi người chăn bị áp đảo về số lượng (16 so với 18 ở 400 mục tiêu). Nguyên nhân là thứ tự cập nhật: engine của HerdSim di chuyển mục tiêu trước, và người chăn khi đó thấy vị trí mục tiêu đã di chuyển, một lợi thế khoảng 0,2 mỗi bước so với $\lambda = 2{,}5$; bài báo tích phân cả hai phía từ trạng thái đầu bước. Với thứ tự của bài báo (người chăn nay đọc vị trí mục tiêu ở đầu bước), pilot thứ hai nằm trong phạm vi một người chăn so với bài báo ở mọi cỡ đã thử, đúng tiêu chí đặt ra trước khi chạy pilot.

**Trả lời trực tiếp RQ14:**

1. **Bản đồ của bài báo được tái lập.** Trên toàn lưới, tỷ lệ trung bình được gom khác Hình 2 của bài báo với trung vị 0,034 ở bán kính cảm nhận 10 (448 ô) và 0,003 với cảm nhận vô hạn (451 ô). Các khác biệt lớn hơn chỉ nằm trên các hàng biên, nơi bước chuyển từ thất bại sang thành công của HerdSim sắc hơn một người chăn. Theo thống kê của bài báo, đội nhỏ nhất của HerdSim bằng của bài báo hoặc nhỏ hơn một người chăn ở mọi cỡ từ $\sqrt{N} = 12$ với bán kính cảm nhận 10 (Hình 13).
2. **Với cảm nhận vô hạn, quy luật căn bậc hai giữ dưới cả hai thống kê.** Đội tối thiểu theo thống kê của bài báo và của HerdSim bằng nhau ở mọi cỡ trừ một (289 mục tiêu: 15 so với khoảng 14–15): 8 người chăn cho 100 mục tiêu, 13 cho 225, 17 cho 400, tức $\sqrt{N} - 2$ từ 100 đến 256 mục tiêu và $\sqrt{N} - 3$ từ 324. Số mũ luật lũy thừa khớp trên 100 đến 400 mục tiêu là 0,52 (thống kê của bài báo) và 0,53 (của HerdSim).
3. **Với bán kính cảm nhận 10 có một ngưỡng mật độ.** Không đội nào tới 25 người chăn đạt tỷ lệ trung bình 0,99 với 81 mục tiêu trở xuống; tốt nhất là 0,81–0,97, và mọi thất bại ở đó để lại mục tiêu ngoài tầm nhìn của mọi người chăn (`targets_lost`). Ngay cả một mục tiêu duy nhất cũng bị mất ở khoảng một lượt trong năm (tỷ lệ trung bình 0,82 với 25 người chăn), vì mục tiêu xuất phát cách mọi người chăn hơn 10 thì không bao giờ được nhìn thấy. Bài báo đặt ngưỡng tại $\sqrt{N} = 11$ (Bảng I); trong HerdSim tỷ lệ trung bình lần đầu đạt 0,99 tại $\sqrt{N} = 10$ với 19 người chăn, và đường căn bậc hai được nhập lại tại $\sqrt{N} = 12$ (11 người chăn cho 144 mục tiêu).
4. **Gần ngưỡng, hai thống kê tách nhau.** Với 144 đến 196 mục tiêu, tỷ lệ trung bình của bài báo vượt 0,99 với một đội gần đường căn bậc hai, nhưng tỷ lệ thành công mỗi lượt vẫn ở mức 0,70–0,94 với nhiều người chăn hơn hẳn, vì một lượt mất hai trên 144 mục tiêu vẫn cho trung bình trên 0,99 cùng các lượt khác. Ở 144 mục tiêu, 11 người chăn cho tỷ lệ trung bình 0,992 và tỷ lệ thành công 0,70; với 17 đến 25 người chăn tỷ lệ thành công là 0,88–0,96 và $D_{\min}$ của HerdSim là khoảng 17–25. Theo quy tắc của HerdSim, vùng áp dụng quy luật căn bậc hai bắt đầu ở khoảng 196–225 mục tiêu chứ không phải 144.
5. **Trên ngưỡng, quy luật giữ dưới cả hai thống kê.** Từ 225 đến 400 mục tiêu, đội tối thiểu là 13, 14, 15, 15, 16, 17 (HerdSim) so với 14, 15, 16, 17, 17, 18 đọc từ bài báo; số mũ khớp trên sáu cỡ này là 0,41 (HerdSim) và 0,42 (thống kê của bài báo trên các lượt của HerdSim). Phép khớp trên sáu điểm từ $\sqrt{N} = 15$ đến 20 còn ngắn; các đội theo $D \approx 0{,}8\sqrt{N} + 1$, mà độ dốc log-log cục bộ nhỏ hơn 0,5 vì có hằng số cộng.

![Mô hình Lama và di Bernardo trong HerdSim](../figures/fig38_lama.png)
*Hình 13: Đội nhỏ nhất theo số mục tiêu, nhiệm vụ gom,* $R = 50$*. Hình vuông: Hình 2 của bài báo (tỷ lệ trung bình ít nhất 0,99), đọc từ ảnh raster. Hình tròn: thống kê của bài báo trên các lượt của HerdSim. Hình thoi và thanh:* $D_{\min}$ *của HerdSim theo quy tắc 0,90 / 99%, với khoảng; dấu chéo là không có đội tin cậy nào tới 25 và tam giác rỗng là cận dưới còn mở. Trái: bán kính cảm nhận 10, vùng ngưỡng tô xám. Phải: cảm nhận vô hạn.*

Số liệu: [Lama and di Bernardo (2024): gather task](results_tables.md#lama-and-di-bernardo-2024-gather-task) (cả hai thống kê theo từng cỡ, thống kê của bài báo ở 0,90, 0,95 và 0,99, và các số mũ).

Điều này thay đổi gì ở mục 5.1: trong cùng một mô phỏng, mục tiêu không gắn kết cần một đội tăng với số mũ khoảng 0,5 (cảm nhận vô hạn) hoặc 0,41–0,42 trên ngưỡng (cảm nhận 10), so với 0,27–0,38 của bầy Strömbom ở 12 lần thời gian lùa (mục 3.8). Hai nhiệm vụ vẫn khác nhau (gom từ một đĩa trong 5000 s cố định so với lùa theo hạn chót tính bằng thời gian lùa), và quy tắc người chăn cũng khác, nên khoảng cách này chưa phải là thước đo riêng của độ gắn kết; các lượt chạy ghép chéo hai mô hình trên cùng một nhiệm vụ là bước tiếp theo (mục 7).

---

## 4. Phân tích vi mô: Dị thường Bố cục và Đo đạc Từng tích tắc

### 4.1 Dị thường Bố cục `split` (Bầy phân cụm)
Trên bố cục `split` ở $N \ge 200$, việc tăng thêm số lượng chó không cải thiện tỷ lệ thành công: ở $6\times$ dưới tiêu chí 99%, tỷ lệ thành công ở mức 0,60–0,90 với mọi $D \ge 4$ (0,10–0,76 dưới tiêu chí nghiêm ngặt), còn ở $3\times$ gần như bằng 0 với mọi $D$. Replay các lượt chạy đã lưu chỉ ra hai nguyên nhân:
1. **Dồn cục bộ khi gom cừu ($D = 4$)**: Do cừu lạc được chọn thuần túy theo khoảng cách tới trọng tâm toàn cục, $D$ con cừu xa nhất thường cùng thuộc về một cụm con. Bắt các chó đi gom chọn cừu lạc cách nhau ít nhất $f(N)$ giúp giảm trung vị thời gian hoàn thành từ 631 s xuống 318 s tại $D = 4$ ($N = 200$, $6\times$).
2. **Hiện tượng Chó đứng yên do Quy tắc Giữ khoảng cách $3 r_a$ (từ $D = 4$)**: Quy tắc của Strömbom bắt chó phải dừng bước khi cách bất kỳ con cừu nào dưới $3 r_a = 6\text{ m}$. Trên bố cục `split`, trung bình khoảng một phần tư số chó đang đứng yên (1 đến 7% trên `wide` và `outlier_rich`). Trong replay rút ngắn khoảng cách dừng xuống $r_a = 2\text{ m}$, thời gian lùa giảm 21–24% tại $D = 8$ và 16, với 12/12 lượt thành công tại $D = 16$ ($N = 200$, $6\times$).

**Replay chẩn đoán**: Các lượt chạy đã lưu của `split` $N = 100$ và $200$ ($D = 2, 4, 8, 16$; $6\times$ và $3\times$; 12 hạt giống) được replay với khoảng cách dừng rút ngắn còn $r_a$, với các chó đi gom chọn cừu lạc cách nhau ít nhất $f(N)$, và với cả hai thay đổi cùng lúc. Ở $6\times$ ($N = 200$), chia đều việc gom giảm một nửa thời gian hoàn thành tại $D = 4$ ($631\text{ s} \to 318\text{ s}$), và rút ngắn khoảng cách dừng giảm thời gian hoàn thành khoảng 20% tại $D \ge 8$; ngay cả với cả hai thay đổi, $D = 8\text{--}16$ chó vẫn chậm hơn $D = 2$ chó, một điểm kém hiệu quả còn bỏ ngỏ khi vòng cung nhiều chó gặp bầy nhiều cụm. Ở $3\times$ các thay đổi không giúp ích: với khoảng cách dừng ngắn hơn, $D = 8$ chậm hơn và $D = 16$ thành công 0 trên 12 lượt.

Số liệu: [RQ-B1 split diagnostic](results_tables.md#rq-b1-split-diagnostic-2026-10-24); tỷ lệ thành công từ `results/dmin_m6`, `dmin_f99_m6`, `dmin_m3` và `dmin_f99_m3`, và tỷ lệ chó đứng yên từ các lượt chạy `dmin_f99_m6` (không có bảng).

![Đường cong Split](../figures/fig23_split_curves.png)

**Hình 14: Hiện tượng chững hiệu suất trên bố cục bầy phân cụm `split` ($N \ge 200$).**

Số liệu: tỷ lệ thành công và khoảng tin cậy 99% của từng ô trong `results/dmin_m6` và `results/dmin_f99_m6` (thời hạn $6\times$); D_min của các hàng này nằm trong [dmin_m6](results_tables.md#dmin_m6) và [dmin_f99_m6](results_tables.md#dmin_f99_m6).

*Cách đọc biểu đồ:*
- **Các khung**: `split` tại $N = 100$, $200$ và $400$, và `wide` tại $N = 400$ để đối chiếu, tất cả ở thời hạn $6\times$.
- **Các trục**: Tỷ lệ thành công kèm khoảng tin cậy 99% theo số chó $D$ (thang log). Chấm tròn xanh: tiêu chí nghiêm ngặt 100%; ô vuông cam: tiêu chí 99%. Đường chấm: $\theta = 0{,}90$.
- **Ý nghĩa cốt lõi**: Trên `wide` tại $N = 400$, đường 99% tăng lên 1 khi thêm chó. Trên `split` tại $N = 200$ và $400$, tỷ lệ thành công không tăng theo $D$, và khoảng tin cậy rộng ở các ô chỉ có 10 đến 70 hạt giống. Dữ liệu replay chỉ ra nguyên nhân là đàn chó dồn vào một cụm tại $D = 4$ và đứng yên theo quy tắc $6\text{ m}$ từ $D = 4$.

### 4.2 Tương quan Đo đạc Từng tích tắc
Mỗi lượt chạy lưu giá trị trung bình, nhỏ nhất và lớn nhất của từng đại lượng đo theo tích tắc. Từ đó:
- **Độ tản bầy so với Thành công**: Hệ số tương quan Spearman giữa độ tản trung bình của bầy trong một ô (bán kính RMS) và tỷ lệ thành công của ô đó là $-0{,}71$ đến $-0{,}76$ ở $6\times$ ($-0{,}57$ đến $-0{,}68$ ở $3\times$), trên các ô có ít nhất 20 hạt giống. Các ô có bầy gọn hơn thành công thường xuyên hơn.
- **Trùng lặp chó**: Trong `strombom_multi`, tỷ lệ chó có một chó khác trong vòng 2 m tăng theo $D$ (0 cho tới $D = 6$ trên `wide`, 0,45–0,59 tại $D = 16$ trên cả ba bố cục phân tán). Các đội FAT có trung bình 0,56–0,82 từ $D = 2$.

![Đo đạc từng tích tắc](../figures/fig27_metrics.png)

**Hình 15: Tương quan đo đạc vi mô và chẩn đoán đo đạc từng tích tắc.**

Số liệu: đo đạc từng lượt chạy trong `results/dmin_m6` và `results/dmin_f99_m6` (không có bảng); các giá trị FAT trong phần chữ lấy từ `results/dmin_fat` và `dmin_f99_fat`.

*Cách đọc biểu đồ:*
- **Khung (a)**: Tỷ lệ thành công của từng ô theo độ tản bầy trung bình của ô (bán kính RMS, mét) ở $6\times$, các lượt nghiêm ngặt và 99% ($r = -0{,}71$ đến $-0{,}76$).
- **Khung (b)**: Trung vị tỷ lệ chó đứng yên theo $D$ ở $N = 200$ (tiêu chí 99%) cho `wide`, `split` và `outlier_rich`; khoảng một phần tư số chó trên `split`.
- **Khung (c)**: Trung vị tỷ lệ chó có một chó khác trong vòng 2 m theo $D$, cùng các ô. Mức chen chúc không tách `split` khỏi các bố cục khác. Hình này không có đường FAT.

---

## 5. Thảo luận và Hàm ý Khoa học

### 5.1 So sánh với các Định luật Mở rộng Lý thuyết
Hệ số góc tăng trưởng dưới tuyến tính của chúng tôi ($\alpha = 0{,}20 - 0{,}42$ ở $12\times$ trên 5 kích thước; 0,27–0,38 trên 9 kích thước, mục 3.8) tương phản sâu sắc với định luật tỷ lệ $\sqrt{M}$ ($\alpha = 0{,}50$) được chứng minh bởi Lama và di Bernardo (2024) trên các mục tiêu không gắn kết. Sự khác biệt này bắt nguồn từ bản chất sinh học: với các hạt rời rạc, mỗi hạt lạc phải được tiếp cận trực tiếp bởi một tác tử chăn dắt. Với bầy cừu có tính xã hội, lực hút toàn cục ($n = N - 1$) giúp một chú chó có thể gián tiếp tác động lên cả bầy ngay khi đưa được các con lạc vào tầm giao tiếp thị giác, giảm mạnh số lượng tác tử cần thiết.

Các lượt chạy độ gắn kết (mục 3.11) kiểm tra trực tiếp cách giải thích này. Làm bầy gắn kết hơn mức của bài báo hầu như không đổi độ dốc (0,20 trên `wide`, so với 0,20–0,30 của bầy gốc), còn bầy yếu hơn duy nhất mà mô hình tạo được (mỗi con cừu bị hút về một nửa bầy) làm độ dốc tăng lên 0,40–0,70, một khoảng chứa mốc 0,5 của mục tiêu không gắn kết. Thời hạn cũng có tác dụng tương tự: ở $6\times$ độ dốc là 0,38–0,61. Độ gắn kết và áp lực thời gian cùng quyết định một bầy nằm ở phía nào của quy luật căn bậc hai.

Mục 3.14 nay cho phía không gắn kết ngay trong HerdSim. Mô hình của bài báo, chạy ở đây, tái lập chính quy luật của nó: số mũ 0,52–0,53 với cảm nhận vô hạn và 0,41–0,42 trên ngưỡng mật độ với bán kính cảm nhận 10, theo cả thống kê của bài báo lẫn của HerdSim. Cả hai đều lớn hơn 0,27–0,38 của bầy Strömbom ở 12 lần thời gian lùa, đúng như cách giải thích ở trên dự đoán. Hai loạt chạy vẫn khác nhau cả về nhiệm vụ và quy tắc người chăn chứ không chỉ về độ gắn kết, nên phần khoảng cách thuộc về độ gắn kết vẫn chưa được đo.

### 5.2 Bản chất Hai giai đoạn của Bài toán Chăn dắt Tập thể
Kết quả của chúng tôi chỉ ra rằng bài toán chăn dắt tập thể bao gồm hai giai đoạn vật lý hoàn toàn khác biệt:
1. **Giai đoạn Di chuyển (Gom bầy và Lùa đàn)**: Khả năng mở rộng quy mô rất cao, dưới tuyến tính theo $N$, và được phản ánh chính xác bởi tiêu chí 99%.
2. **Giai đoạn Đóng chuồng (Xử lý cá thể lạc cuối cùng)**: Rất nhạy cảm, khó mở rộng quy mô, và dễ thất bại do quán tính chạy lố dưới tiêu chí nghiêm ngặt 100%.

Trong thực tế chăn thả cũng như điều khiển robot, một cá thể chậm chạp không đồng nghĩa với việc nhiệm vụ đã thất bại. Chúng tôi khuyến nghị các nghiên cứu đa tác tử tương lai nên tách bạch tiêu chí đưa đàn đến nơi khỏi giai đoạn chặn giữ cuối cùng (ví dụ: đóng cổng chuồng hoặc cử chó đi tuần vận tốc chậm). Các lượt chạy giữ đàn (mục 3.10) cho thấy vì sao phải tách hai giai đoạn: giữ đàn chỉ thành công khi chó lùi ra ngoài cự ly phản ứng của cừu, một bước mà quy tắc được thiết kế để lùa không làm.

### 5.3 Chín Đóng góp Khoa học Chính

1. **Bản đồ Ranh giới Thực nghiệm Hoàn chỉnh**: Thiết lập bản đồ ranh giới $D_{\min}$ và $D_{\mathrm{sat}}$ có độ tin cậy toán học 99% đầu tiên qua các quy mô đàn ($N \le 566$, mở rộng đến 3200), bố cục và thời hạn.
2. **Tiêu chí Thành công Định hình Vật lý**: Chứng minh tiêu chí tuyệt đối 100% tạo ra nút thắt cổ chai nhân tạo (Hiệu ứng cá thể lạc đàn), trong khi tiêu chí 99% phản ánh đúng năng lực phối hợp tập thể.
3. **Tách bạch Độ tin cậy khỏi Tốc độ**: Chứng minh quy mô đội để đạt tốc độ tối đa ($D_{\mathrm{sat}}$) tăng nhanh gấp đôi quy mô đội chỉ để đạt độ tin cậy ($D_{\min}$). Chó bổ sung vượt quá $D_{\mathrm{sat}}$ chỉ làm tăng chi phí mà không mang lại tốc độ.
4. **Giải phẫu Tầng Phối hợp Đa Tác tử**: Chứng minh việc chuyển trạng thái gom/lùa đưa đội chó độc lập tới $N = 200$, nhưng tầng phân công tối ưu Hungarian là bắt buộc ở $N \ge 400$.
5. **Hiện tượng Quá tải do Kích thước Vật lý**: Chứng minh tác hại của sự đông đúc không xuất hiện ở chó dạng điểm, nhưng bộc lộ rõ rệt khi chó có thể tích chiếm chỗ ($2\text{ m}$), gây nghẽn vòng cung lùa.
6. **Mục tiêu Gắn kết và Không Gắn kết**: Liên hệ độ mạnh của lực gắn kết với số mũ tăng trưởng: bầy của bài báo tăng chậm hơn quy luật $\sqrt{N}$ ở thời hạn thong thả, và làm yếu độ gắn kết đưa số mũ về phía 0,5.
7. **Ranh giới Giải tích của Quy tắc Lùa Strömbom**: Phát hiện giới hạn toán học tại $N = 1056$ nơi khoảng cách lùa vượt quá tầm cảm nhận của cừu, chỉ ra sự cần thiết phải đặt trần cự ly cho các đàn khổng lồ.
8. **Đánh đổi giữa Cảm biến và Giao tiếp**: Đo cái giá của tầm nhìn cục bộ ($30\text{--}65\text{ m}$, khoảng một chó ở $N = 200$) và cho thấy, ở tầm 65 m, chia sẻ với cả đội đưa $D_{\min}$ về giá trị toàn cục trên `wide` $N = 200$ (không đạt trên `split`).
9. **Hệ thống Mô phỏng Mã nguồn mở Minh bạch**: Cung cấp bộ công cụ mô phỏng tất định, an toàn trước sự cố, có thể tái lập chính xác qua 367.150 lượt chạy.

### 5.4 Gợi ý Ứng dụng Thực tế (Robot & Drone)

- **Định cỡ Đội hình**: Ở thời hạn thong thả, 1 đến 3 robot có thể kiểm soát đàn cừu tản mác lên tới 400 con, và một đàn tập trung cần 1 robot tới $N = 1131$ (2 ở 1600). Áp lực thời hạn làm dịch chuyển nhu cầu tương đương với việc tăng đàn cừu lên gấp 4 lần, do đó cần xác định quỹ thời gian trước khi chốt số lượng robot.
- **Tốc độ tốn kém hơn Độ tin cậy**: Trên bầy `wide` và `outlier_rich`, đội hình chạy nhanh nhất đòi hỏi số lượng robot gấp 1,5 đến 2,5 lần đội hình tối thiểu (nhiều hơn trên `split`); robot vượt quá ngưỡng này chỉ làm hao pin vô ích (Bảng 6).
- **Kích thước vật lý giới hạn quy mô đội**: Robot không thể đứng gần nhau dưới 2 m sẽ gây nghẽn vòng cung lùa của bầy `outlier_rich` từ khoảng 9 thiết bị tại $N = 400$.
- **Chia sẻ bản đồ trước khi mua thêm robot**: Tầm nhìn cục bộ tốn thêm khoảng 1 robot ở $N = 200$; chia sẻ dữ liệu giữa mọi robot lấy lại được robot đó trên `wide` (không đạt trên `split`).
- **Lùi xa để Giữ đàn**: Robot bắt buộc phải rút lui ra ngoài tầm phản ứng của động vật để giữ chúng trong chuồng; robot đứng lại ở cửa chuồng chỉ làm đàn vật nuôi tiếp tục bỏ chạy.

---

## 6. Hạn chế và Đe dọa Tính Đúng đắn

1. **Giản lược Động học 2D**: Cừu và chó được mô hình hóa dưới dạng chất điểm chuyển hướng tức thì và không bị mệt mỏi thể lực.
2. **Điều kiện Biên Mở**: Đồng cỏ mô phỏng không có hàng rào; đồng cỏ thực tế có hàng rào giúp chó dồn những con cừu lạc.
3. **Các Khoảng chặn Ranh giới**: Các ô tham số mấp mé ngưỡng $\theta = 0{,}90$ vẫn chưa ngã ngũ tại mốc trần 200 hạt giống, đòi hỏi phải báo cáo dưới dạng khoảng chặn.
4. **Tầm nhìn Toàn cục trong Lưới chính**: Ngoại trừ các thử nghiệm ở mục 3.12, mô hình giả định chó biết vị trí của mọi con cừu. Mục 3.12 thử tầm nhìn giới hạn với vị trí đã biết trong tầm đó; cảm nhận chỉ theo góc hướng (bearing-only) chưa được mô hình hóa.
5. **Các Thiết lập Kỹ thuật Bổ sung**: Quy tắc rút lui giữ đàn, giãn cách chó $2\text{ m}$, và trần cự ly lùa là các giải pháp kỹ thuật do HerdSim đưa ra chứ không có nguồn gốc từ tài liệu sinh học.
6. **Mức trần Hiệu chuẩn Bầy**: Vượt quá $N \approx 600$, bầy cừu Strömbom không còn tự co cụm về kích thước riêng; các nghiên cứu trên 600 con dựa trên mật độ đàn được áp đặt.
7. **Cỡ mẫu Replay Chẩn đoán**: Các phép thử replay áp lực và dị thường split sử dụng 12 hạt giống mỗi ô, mang tính chỉ báo cơ chế chứ không phải phân tích giới hạn toàn diện.
8. **Cơ chế Chuẩn hóa Tổng Lực đe dọa từ Nhiều Chó**:
   - Mô hình gốc của Strömbom chỉ áp dụng cho một chú chó. HerdSim chuẩn hóa tổng vector lực đẩy từ các chú chó trong phạm vi $65\text{ m}$ về độ dài đơn vị tiêu chuẩn.
   - *Vì sao không dùng phép cộng lực*: Lực gắn kết xã hội của cừu là $c = 1{,}05$. Nếu cộng dồn lực đẩy độc lập từ hai chú chó ở góc $\theta$, độ lớn tổng lực là $2\cos(\theta/2)$, luôn lớn hơn $1{,}05$ trừ khi hai chú chó đứng đối diện nhau ở góc $\gt 116^\circ$. Do đó, phép cộng lực sẽ khiến 2 chú chó đi cạnh nhau xé toạc đàn cừu ngay từ $D = 2$.   - *Hàm ý*: Mặc dù phép chuẩn hóa phản ánh đúng hiện tượng bão hòa sợ hãi sinh học, việc cừu thực tế có hoảng loạn hơn trước nhiều kẻ săn mồi hay không vẫn là câu hỏi mở cho các nhà sinh học thực địa.
9. **Mô hình Lama và di Bernardo là bản tái lập từ văn bản bài báo**: bài báo không công bố mã. Ở những chỗ văn bản không nói rõ, HerdSim đưa ra các lựa chọn có ghi lại (lực đẩy hướng ra xa người chăn; một lượt kết thúc khi mọi người chăn ở trong đích và không ai thấy mục tiêu bên ngoài; mục tiêu và người chăn được tích phân từ cùng một trạng thái). Giá trị của bài báo được đọc từ hình với độ phân giải một người chăn và 50 lượt mỗi ô. Đội của HerdSim vẫn nhỏ hơn đội của bài báo tối đa một người chăn ở biên thiếu người chăn; nguyên nhân của người chăn cuối cùng đó chưa được tìm ra.

---

## 7. Kết luận và Hướng Nghiên cứu Tương lai

Thông qua 367.150 lượt mô phỏng trên 39 giao thức, HerdSim đã lập bản đồ toàn diện về quy mô đội tối thiểu $D_{\min}$, quy mô bão hòa $D_{\mathrm{sat}}$, và các điều kiện khiến việc tăng thêm chó gây hại. Đàn cừu tập trung chỉ cần 1 chú chó tới $N = 1131$; trên đồng cỏ phân tán, số chó cần thiết tăng trưởng dưới tuyến tính với độ dốc 0,27–0,38 ở $12\times$ và 0,38–0,61 ở $6\times$, trong khi đội nhanh nhất tăng nhanh gấp khoảng hai lần. Dưới tiêu chí nghiêm ngặt, con cừu lạc cuối cùng chi phối cuộc chơi; dưới tiêu chí 99%, kết quả có tính bền vững cao trước các quy ước mô phỏng. Sự phối hợp đội ngũ quan trọng ở các đàn lớn; chó dạng điểm thêm vào không bao giờ làm mất độ tin cậy trên `wide` hay `outlier_rich` nhưng làm `split` chậm đi, và chó chiếm chỗ vật lý gây thất bại; và quy tắc lùa kinh nghiệm của Strömbom bộc lộ giới hạn giải tích ở đàn trên một ngàn con. Chạy trong cùng mô phỏng, các mục tiêu không gắn kết của Lama và di Bernardo tái lập quy luật căn bậc hai của họ, và quy luật này cũng giữ dưới quy tắc tin cậy của HerdSim, trừ gần ngưỡng mật độ, nơi tỷ lệ trung bình 0,99 che đi những lượt mất một mục tiêu.

### Hướng Nghiên cứu Tiếp theo

1. **Phân bổ Nhiệm vụ Nhận thức Cụm trên Bố cục Phân cụm**: Giải quyết hiện tượng tắc nghẽn trên bố cục `split` bằng cách thiết kế thuật toán phân công chó tỏa đều ra các cụm cấu trúc topo khác nhau thay vì chọn theo khoảng cách trọng tâm toàn cục.
2. **Nhiệm vụ Giữ đàn có Hàng rào Cổng**: Đánh giá giai đoạn giữ đàn bằng cổng rào vật lý thay vì rút lui ra đồng cỏ mở, kiểm tra xem nút thắt giữ đàn có còn tồn tại khi lối thoát bị chặn.
3. **Cảm nhận Góc nhìn Thuần túy (Bearing-Only)**: Mở rộng mô hình tầm nhìn cục bộ sang cảm nhận chỉ có góc hướng mà không có cự ly chính xác, mô phỏng chân thực camera trên các thiết bị drone.
4. **Ghép chéo hai mô hình trên cùng một nhiệm vụ**: Chạy quy tắc đội Strömbom trên mục tiêu Lama trong nhiệm vụ gom, và người chăn Lama trên cừu Strömbom, để tách khoảng cách giữa các số mũ ở mục 3.14 thành phần do độ gắn kết và phần do quy tắc người chăn và nhiệm vụ. Mỗi quy tắc đọc những đại lượng mà phía kia không có (quy tắc đội đọc khoảng cách gom vô nghĩa khi không có gắn kết, người chăn đọc khoảng cách tới một đích mà trong nhiệm vụ lùa nằm xa bầy), nên mỗi phép ghép cần thiết kế riêng trước.
5. **Thu thập Dữ liệu Thực địa Đa Chó / Drone với Vòng đeo GPS**: Hợp tác với các nhà nghiên cứu động vật thực địa để đo đạc phản ứng của đàn cừu khi bị rượt đuổi bởi từ 2 chú chó trở lên, kiểm tra xem cừu thật cảm nhận nỗi sợ theo kiểu cộng dồn hay chuẩn hóa.

---

## Tính Sẵn sàng của Dữ liệu và Mã nguồn

Mọi lượt chạy và quyết định của từng ô được lưu trong `results/<protocol>/`. Các bảng chứa số liệu của báo cáo này nằm trong [results_tables.md](results_tables.md); mỗi khối ghi rõ script đã tạo ra nó. Cách chạy lại toàn bộ nghiên cứu và tạo lại các bảng: xem [cli/README.md](../../cli/README.md) và [tài liệu tham chiếu CLI](../guides/cli_reference.md).

---

## Tài liệu Tham khảo

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

## Phụ lục: Nhật ký Các Giao thức Thực nghiệm

| Giao thức | Tổng lượt chạy | Số ô khảo sát | Số ô quyết định | Ô mở tại trần (200) | Lỗi | Thời gian chạy |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `dmin_m12` | 17.220 | 183 | 179 | 4 | 0 | 1,24 h |
| `dmin_m6` | 13.470 | 191 | 170 | 21 | 0 | 0,28 h |
| `dmin_m3` | 9.530 | 183 | 178 | 5 | 0 | 0,17 h |
| `dmin_f99_m12` | 11.100 | 180 | 178 | 2 | 0 | 0,41 h |
| `dmin_f99_m6` | 14.240 | 191 | 174 | 17 | 0 | 0,49 h |
| `dmin_f99_m3` | 11.140 | 185 | 177 | 8 | 0 | 0,27 h |
| `dmin_fat` | 8.660 | 181 | 179 | 2 | 0 | 0,22 h |
| `dmin_f99_fat` | 8.670 | 184 | 183 | 1 | 0 | 0,23 h |
| `dmin_kubo` | 1.080 | 18 | 18 | 0 | 0 | 0,08 h |
| Các giao thức độ nhạy (14 runs) | 69.630 | 921 | 800 | 121 | 0 | 3,27 h |
| **Tổng cộng** | **164.740** | **2.417** | **2.236** | **181** | **0** | **~6,7 h** |

Các lượt chạy tiếp nối (tiêu chí 99%; thời gian ở 20 workers):

| Giao thức | Lượt chạy | Số ô | Ô mở tại trần | Lỗi | Số giờ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3` (chạy tiếp: hạt giống thời gian; thêm $N$ 71, 141, 283, 566 cho hai lưới đầu) | +38.770 | | | 0 | 4,0 |
| `dmin_f99_indep` | 12.990 | 181 | 18 | 0 | 0,30 |
| `dmin_f99_kubo` | 3.260 | 38 | 6 | 0 | 0,18 |
| `dmin_f99_hold` | 14.280 | 280 | 18 | 0 | 0,74 |
| `dmin_f99_hold_spacing` (chạy lại với quy tắc khoảng cách cứng) | 13.930 | 283 | 19 | 0 | 0,70 |
| `dmin_f99_c1.3`, `_c1.6`, `_c2.0` | 10.800 / 10.830 / 10.780 | 180 mỗi protocol | 1 / 0 / 0 | 0 | 0,31 / 0,29 / 0,41 |
| `dmin_f99_k05` | 11.630 | 149 | 14 | 0 | 2,29 |
| `dmin_f99_view_range` | 21.040 | 293 | 27 | 0 | 0,53 |
| `dmin_f99_view_comm` | 6.890 | 102 | 3 | 0 | 0,20 |
| `dmin_f99_big` | 2.230 | 84 | 1 | 0 | 3,12 |
| `dmin_f99_big_dense`, `_loose` | 1.320 / 830 | 15 / 14 | 2 / 1 | 0 | 0,73 / 0,26 |
| `dmin_f99_big_cap` | 2.550 (+100 ở $N = 3200$, không tính) | 45 | 3 | 0 | 5,5 (7,6 tính cả $N = 3200$) |
| `lama_r50` (nhiệm vụ gom, bán kính cảm nhận 10) | 17.660 | 500 | 23 | 0 | 6,53 |
| `lama_r50_inf` (nhiệm vụ gom, cảm nhận vô hạn) | 22.620 | 500 | 1 | 0 | 6,47 |

Replay chẩn đoán: 164 lượt replay áp lực và 768 lượt replay split, mọi lượt replay không đổi đều cho kết quả bit-identical với lượt chạy đã lưu. Các pilot kiểm chứng mô hình Lama (8.200 lượt trong hai lần, thư mục tạm không giữ lại) được mô tả ở mục 3.14.
