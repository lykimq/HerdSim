# Quy mô đội tối thiểu để lùa một bầy cừu mô phỏng: Sự phụ thuộc vào kích thước bầy, bố cục xuất phát, thời hạn và tiêu chí thành công

*Báo cáo nghiên cứu khoa học dự án HerdSim*  
*Đánh giá thực nghiệm qua 23 giao thức chiến dịch (164.740 lượt chạy mô phỏng) trên các kiến trúc chăn dắt đa tác tử.*

---

## Tóm tắt (Abstract)

Cần bao nhiêu tác tử chăn dắt tự hành ($D$) để thu gom và lùa một bầy cừu gồm $N$ cá thể vào một khu vực đích trước một thời hạn xác định? Chúng tôi khảo sát bài toán này thông qua môi trường mô phỏng vi mô, sử dụng mô hình hạt tự hành của Strömbom et al. (2014) và phát triển một kiến trúc phối hợp đa chó hoàn chỉnh (`strombom_multi`): phân công các chú chó thu gom từng cá thể cừu tản mác riêng biệt khi bầy bị phân tán, và dàn đội hình vòng cung phía sau bầy khi lùa đàn. Chúng tôi định nghĩa $D_{\min}$ là quy mô đội nhỏ nhất đạt độ tin cậy (tỷ lệ thành công được chứng minh $\ge 0{,}90$ thông qua khoảng tin cậy nhị thức Clopper–Pearson hai phía ở mức ý nghĩa 99%). Một thuật toán phân bổ tuần tự thích ứng sẽ tập trung tài nguyên tính toán vào các ô tham số chưa ngã ngũ (tối đa 200 hạt giống ngẫu nhiên mỗi ô) và báo cáo các biên chưa quyết định dưới dạng khoảng chặn (bracket).

Nghiên cứu lập bản đồ toàn diện $D_{\min}$ qua 5 quy mô bầy đàn ($N \in [25, 400]$), 4 bố cục hình học xuất phát (`compact`, `wide`, `split`, `outlier_rich`) và 3 mức thời hạn chuẩn hóa ($12\times$, $6\times$, và $3\times$ thời gian lùa tối thiểu), đồng thời đánh giá song song hai tiêu chí thành công: *chặn giữ nghiêm ngặt* (100% số cừu đồng thời ở trong đích) và *tiếp cận 99%* (tối thiểu $\lceil 0{,}99 N \rceil$ cừu vào đích). Qua 23 giao thức với 164.740 lượt chạy không xảy ra bất kỳ lỗi mô phỏng nào, nghiên cứu rút ra các kết luận then chốt:
1. **Tính bất biến của bầy co cụm**: Với bầy xuất phát co cụm (`compact`), một chú chó duy nhất ($D_{\min} = 1$) là đủ cho mọi quy mô ($N = 25$ đến $400$) và mọi thời hạn. Việc bổ sung thêm chó không giúp rút ngắn thời gian hoàn thành nhiệm vụ.
2. **Quy luật tăng trưởng dưới tuyến tính trên bầy phân tán**: Với bầy phân tán, $D_{\min} = 1$ khi $N \le 50$, và chỉ tăng chậm lên 2 hoặc 3 chó ở $N = 400$ dưới thời hạn nới lỏng ($12\times$). Trong không gian log-log ($\log_2 D_{\min}$ theo $\log_2 N$), hệ số góc $\alpha$ dao động từ 0,20 đến 0,50 ở thời hạn $12\times$, và từ 0,30 đến 0,80 ở thời hạn $6\times$.
3. **Áp lực thời hạn là yếu tố chi phối hàng đầu**: Rút ngắn thời hạn từ $12\times$ xuống $3\times$ làm tăng vọt $D_{\min}$ trên bố cục `wide` ở $N = 400$ từ 2 lên 5–6 chó—mức tăng này vượt qua cả tác động của việc tăng quy mô bầy cừu lên gấp bốn lần.
4. **Hiệu ứng cá thể lạc đàn (The Straggler Effect)**: Trong 95% số lượt thất bại dưới tiêu chí 100% nghiêm ngặt của các đội có từ 6 chó trở lên, đàn chó thực chất đã đưa được 99% số cừu vào trong đích từ rất sớm. Sự thất bại xảy ra do đàn chó cố săn đuổi 1–2 cá thể rớt lại sau cùng, vượt quá đà và vô tình lùa ngược khối cừu chủ lực ra ngoài pasture. Việc giảm vận tốc chó ($v_{\text{dog}} = 1{,}15$) loại bỏ được quán tính vượt đích này, giúp đưa $D_{\min}$ nghiêm ngặt từ thất bại hoàn toàn xuống còn 6 chó ở bố cục `outlier_rich` ($N = 400$).
5. **Tính vững chắc của tiêu chí tiếp cận 99%**: Dưới tiêu chí 99%, giá trị $D_{\min}$ duy trì sự ổn định cao (dao động trong phạm vi 1 chó so với mốc cơ sở) trước các thay đổi về quy ước mô phỏng (xuất phát từ cọc người chăn, xuất phát vòng tròn, cự ly xuất phát, và các tham số cừu đo đạc từ thực địa GPS). Ngược lại, tiêu chí nghiêm ngặt phóng đại quá mức các sai số do quy ước hình học gây ra.
6. **Sự bắt buộc của tầng phối hợp đội**: Mô hình đối chứng không phối hợp (FAT) sử dụng cơ chế nhắm cá thể xa nhất nhưng tước bỏ thuật toán gán cặp Hungarian và lực đẩy né tránh nhau đã thất bại hoàn toàn: các chú chó dồn cục thành bản sao trùng lặp (`dog_overlap` $> 0{,}80$), không đạt được bất kỳ giá trị $D_{\min}$ tin cậy nào ở $N \ge 200$.

---

## 1. Giới thiệu (Introduction)

Hoạt động chăn dắt bầy cừu bằng chó chăn là hình mẫu sinh học kinh điển cho bài toán điều khiển cơ cấu chấp hành thưa (sparse actuation): một số lượng rất nhỏ các tác tử điều khiển có thể định hướng và dẫn dắt hiệu quả một quần thể khổng lồ các thực thể tự hành không phối hợp. Bài toán này có sự tương đồng trực tiếp với các thách thức lớn trong điều khiển bầy robot (swarm robotics), hướng dẫn đám đông sơ tán, kiểm soát động vật xâm lấn, và lý thuyết điều khiển hệ thống đa tác tử quy mô lớn (Strömbom et al. 2014; di Bernardo 2026).

Strömbom et al. (2014) đã chứng minh rằng một cá thể chăn dắt đơn lẻ luân phiên giữa hai trạng thái hành vi suy nghiệm—**thu gom (collect)** khi có cừu cách tâm bầy xa hơn $f(N) = r_a N^{2/3}$ và **lùa bầy (drive)** từ phía sau khi bầy đã co cụm—đã tái hiện xuất sắc quỹ đạo lùa hình chữ S đặc trưng của chó chăn cừu thật, lùa thành công các đàn lên tới 150 con. Dữ liệu GPS thực nghiệm gần đây trên giống chó Border Collie lùa đàn 14 con cừu khẳng định rằng chó chăn luôn duy trì cự ly sát phía sau bầy và liên tục điều chỉnh tư thế theo hình học tập thể của đàn cừu (Jadhav et al. 2024).

Khi mở rộng lên nhiều tác tử chăn dắt, nhiều chiến lược điều khiển đã được đề xuất:
- Bộ điều khiển bao vây dựa trên trường thế năng đưa hệ thống về mô hình động học vi sai (Pierson và Schwager 2015).
- Mô hình lực liên tục trong đó chó đẩy cá thể xa mục tiêu nhất kết hợp lực đẩy né tránh nhau để phân tán quanh bầy (Kubo et al. 2022).
- Chiến lược chọn mục tiêu cho các thực thể chuyển động Brown không liên kết (Auletta et al. 2021).
- Chăn dắt bầy tự hành dựa thuần túy trên phép đo góc nhìn mà không cần định vị tuyệt đối (Li et al. 2025).
- Phương pháp điều khiển tối ưu giải tích cho các nhóm nhỏ tác tử (Brown et al. 2025).

Tuy nhiên, các công trình này chủ yếu so sánh hiệu năng giữa các quy mô đội cố định mà chưa trả lời câu hỏi cốt lõi: **Cần tối thiểu bao nhiêu tác tử chăn dắt ($D_{\min}$)?** Lama và di Bernardo (2024) đã khảo sát ranh giới này cho các mục tiêu không liên kết, chứng minh rằng số người chăn tối thiểu $N^*$ tỷ lệ với căn bậc hai số lượng mục tiêu ($\sqrt{M}$) theo lý thuyết thẩm thấu của đồ thị chăn dắt. Dẫu vậy, mô hình của họ cố định hình dạng xuất phát, giới hạn thời gian và giả định mục tiêu không có lực liên kết bầy đàn, để ngỏ câu hỏi quy luật này biến đổi ra sao khi bầy cừu có lực hút sinh học, khi thời hạn bị siết chặt và khi hình học xuất phát bị phân tán.

### Đóng góp chính của báo cáo
1. **Định nghĩa thống kê chặt chẽ về $D_{\min}$**: Thiết lập $D_{\min}$ thông qua bài toán kiểm định giả thuyết nhị thức tuần tự sử dụng khoảng tin cậy Clopper–Pearson 99% ($\theta = 0{,}90$), vận hành bởi thuật toán phân bổ thích ứng giúp tập trung tài nguyên vào các ô tham số ranh giới.
2. **Bản đồ hóa đa chiều toàn diện**: Xác định ranh giới $D_{\min}$ qua 5 quy mô bầy đàn ($N \in [25, 400]$), 4 bố cục không gian, và 3 mức thời hạn ($12\times$, $6\times$, $3\times$) dưới cả hai tiêu chí 100% nghiêm ngặt và 99% tiếp cận.
3. **Phát hiện cơ chế của hiệu ứng cá thể lạc đàn (Straggler Effect)**: Chỉ rõ nguyên nhân thất bại ở quy mô lớn dưới tiêu chí nghiêm ngặt là do quán tính vượt đích khi săn đuổi 1–2 con cừu rớt lại sau cùng.
4. **Kiểm tra độ nhạy và tính vững thực nghiệm**: Đánh giá toàn diện các quy ước mô phỏng (vị trí xuất phát dạng vòng cung, hình tròn, cọc handler; khoảng cách khởi đầu; tốc độ chó; và bộ tham số cừu thực địa). Phân tách rạch ròi quy luật vật lý khách quan khỏi các sai số do quy ước mô phỏng.
5. **Chứng minh vai trò của tầng phối hợp đội**: So sánh kiến trúc `strombom_multi` với mô hình triệt tiêu FAT, chứng minh sự hội tụ $D_{\min}$ hữu hạn ở quy mô lớn là thuộc tính của tầng phối hợp đội chứ không phải do việc tăng số lượng chó đơn thuần.

---

## 2. Câu hỏi nghiên cứu (Research Questions)

Báo cáo tập trung giải quyết 6 Câu hỏi Nghiên cứu (RQs):

- **RQ1 (Quy luật mở rộng quy mô $N$)**: Quy mô đội tối thiểu $D_{\min}$ tăng trưởng thế nào theo kích thước bầy $N \in [25, 400]$ trên các bố cục không gian và thời hạn khác nhau? Lực hút bầy đàn có làm giảm độ dốc tăng trưởng so với bầy không liên kết ($\sqrt{N}$) hay không?
- **RQ2 (Bố cục hình học so với quy mô dân số)**: Với cùng một thời hạn, yếu tố nào chi phối $D_{\min}$ mạnh mẽ hơn: bố cục xuất phát (co cụm hay phân tán) hay quy mô đàn cừu $N$?
- **RQ3 (Áp lực thời hạn hoàn thành)**: Áp lực thời gian ($12\times \to 6\times \to 3\times$ thời gian lùa) làm dịch chuyển $D_{\min}$ ra sao? Tác động này là tuyến tính hay phi tuyến?
- **RQ4 (Tiêu chí thành công và động lực học lùa đàn)**: Tiêu chí nghiêm ngặt 100% khác biệt thế nào so với tiêu chí 99% tiếp cận? Cơ chế vi mô nào gây ra sự sụp đổ thành công của các đội nhiều chó dưới tiêu chí nghiêm ngặt?
- **RQ5 (Tính vững chắc trước các quy ước mô phỏng)**: Các quy luật mở rộng có đứng vững trước những thay đổi về quy ước thiết lập (vị trí thả chó, cự ly xuất phát, bán kính đích, tham số thực địa, vận tốc chó) hay không?
- **RQ6 (Sự cần thiết của phối hợp đa tác tử)**: Một đàn chó hoạt động độc lập không phối hợp (FAT) có thể đạt được $D_{\min}$ hữu hạn ở đàn lớn hay không?

---

## 3. Cơ sở toán học và phương pháp luận thống kê

### 3.1 Định nghĩa $D_{\min}$ bằng khoảng tin cậy nhị thức Clopper–Pearson

Một **ô (cell)** là một bộ tham số xác định gồm (phương pháp, bố cục, $N$, thời hạn, $D$). Mỗi lượt chạy mô phỏng là một phép thử Bernoulli độc lập cho ra kết quả thành công ($1$) hoặc thất bại ($0$). Với một ô chạy qua $n$ lượt với $k$ lần thành công, khoảng tin cậy hai phía 99% Clopper–Pearson $[L, U]$ cho xác suất thành công thực sự $p$ được tính chính xác qua hàm phân phối Beta:

$$
L = B\left(\frac{\alpha}{2};\, k,\, n - k + 1\right), \quad U = B\left(1 - \frac{\alpha}{2};\, k + 1,\, n - k\right)
$$

với $\alpha = 0{,}01$ (độ tin cậy 99%) và $B(q; a, b)$ là phân vị thứ $q$ của phân phối Beta. Với ngưỡng độ tin cậy $\theta = 0{,}90$:
- **Đạt độ tin cậy (Reliable)** nếu $L \ge 0{,}90$. (Về mặt toán học, cần tối thiểu 51 trận thắng liên tiếp không có trận thua nào để $L \ge 0{,}90$, tương ứng 60 lượt chạy với kích thước lô 10).
- **Không đạt tin cậy (Unreliable)** nếu $U < 0{,}90$.
- **Chưa quyết định (Undecided)** nếu $L < 0{,}90 \le U$.

Trên một đường cong kiểm thử theo số lượng chó $D \in \mathcal{D}$:

$$
D_{\min} = \min \{ D \in \mathcal{D} \mid \text{Cell}(D) \text{ đạt độ tin cậy} \}
$$

$$
D_{\min,\text{low}} = \min \{ D \in \mathcal{D} \mid U(D) \ge \theta \}
$$

- **Giá trị quyết định ($D_{\min}$)**: Khi $D_{\min,\text{low}} = D_{\min}$, mọi $D < D_{\min}$ đều chắc chắn không đạt tin cậy ($U < 0{,}90$).
- **Khoảng chặn ($[D_{\min,\text{low}}, D_{\min}]$)**: Khi $D_{\min}$ đạt tin cậy nhưng vẫn còn một số $D$ nhỏ hơn ở trạng thái chưa quyết định tại mốc 200 hạt giống, giá trị tối thiểu thực sự nằm trong khoảng $[D_{\min,\text{low}}, D_{\min}]$ (ví dụ `3-8`).
- **Cận dưới ($[n]$)**: Chưa có $D$ nào đạt tin cậy nhưng tồn tại $D \ge n$ chưa quyết định.
- **Thất bại (`none`)**: Toàn bộ các giá trị $D$ trên lưới kiểm thử đều chắc chắn không đạt độ tin cậy ($U < 0{,}90$).

### 3.2 Thuật toán phân bổ tuần tự thích ứng

HerdSim loại bỏ phương pháp quét lưới thô cố định tốn kém bằng cơ chế 4 tầng:
1. **Khởi tạo**: Mỗi ô bắt đầu với một lô cơ sở gồm 10 hạt giống (`master_seed + i`).
2. **Dừng sớm**: Các ô thất bại rõ rệt ($U < 0{,}90$) dừng lại sau 10–20 lượt; các ô thành công tuyệt đối dừng ngay khi $L \ge 0{,}90$.
3. **Làm mịn thích ứng**: Các ô chưa quyết định nhận tiếp các lô 10 hạt giống lên tới trần 200 hạt giống. Khi hai giá trị $D$ liền kề có sự dịch chuyển trạng thái, điểm chia đôi nguyên (midpoint) sẽ tự động được bổ sung vào vòng sau.
4. **Cắt tỉa bản sao trùng lặp**: Phía trên điểm bão hòa ($D_{\text{sat}}$), nếu số chó bổ sung chỉ hoạt động như bản sao của nhau (độ trùng lặp trung bình `dog_overlap` $\ge 0{,}90$) mà không giúp cải thiện thời gian hoàn thành, ô đó sẽ bị cắt tỉa (`pruned`) để tiết kiệm tài nguyên tính toán.

---

## 4. Mô hình động lực học và thiết lập thực nghiệm

### 4.1 Động lực học cừu Strömbom

Cừu được mô hình hóa theo Strömbom et al. (2014). Khi toàn bộ chó ở ngoài tầm đe dọa $r_s = 65$, cừu **gặm cỏ**: đứng yên hoặc bước một bước dài $\delta = 1$ m với xác suất $p = 0{,}05$ theo hướng ngẫu nhiên đều.

Khi có chó tiến vào bán kính đe dọa ($\min_j \lVert \mathbf{x}_i - \mathbf{y}_j \rVert < r_s$), cừu $i$ tính toán vector hướng di chuyển trốn chạy $\mathbf{H}_i'$:

$$
\mathbf{H}_i' = h\,\mathbf{H}_i + c\,\mathbf{C}_i + \rho_a\,\mathbf{R}_{a,i} + \rho_s\,\mathbf{R}_{s,i} + e\,\mathbf{\epsilon}_i \tag{1}
$$

Cừu tiến một bước có độ dài $\delta = 1$ m/s theo vector chuẩn hóa $\mathbf{H}_i' / \lVert \mathbf{H}_i' \rVert$.

![Mô hình cừu Strömbom](../figures/fig1_sheep_rule.png)

*Hình S1: Mô hình cừu Strömbom. Trái: Các vector lực thành phần trong phương trình (1). Phải: Ranh giới đe dọa ($r_s = 65$) phân tách trạng thái gặm cỏ và trốn chạy chủ động.*

### 4.2 Hòa trộn lực đẩy đa tác tử ($\mathbf{R}_{s,i}$)

Mô hình gốc của Strömbom et al. (2014) chỉ thiết kế cho một chú chó đơn lẻ ($D = 1$). Với đội hình nhiều chó ($D \ge 2$), việc cộng dồn lực đẩy độc lập sẽ nhân bội lực sợ hãi, xé nát bầy cừu. HerdSim hòa trộn lực đẩy từ tất cả các chú chó trong tầm đe dọa thành một vector đơn vị chuẩn hóa:

$$
\mathbf{R}_{s,i} = \frac{\sum_{j \in \text{threat}} \frac{\mathbf{x}_i - \mathbf{y}_j}{\lVert \mathbf{x}_i - \mathbf{y}_j \rVert}}{\left\lVert \sum_{j \in \text{threat}} \frac{\mathbf{x}_i - \mathbf{y}_j}{\lVert \mathbf{x}_i - \mathbf{y}_j \rVert} \right\rVert} \tag{2}
$$

Điều này đảm bảo cường độ lực đẩy luôn giữ đúng chuẩn mực sinh học, đồng thời các chú chó kẹp hai bên sẽ triệt tiêu lực đẩy ngang và gia tăng lực đẩy tiến về phía trước.

### 4.3 Các kiến trúc điều khiển chó

#### Kiến trúc phối hợp đội: `strombom_multi`
- **Mức 1 chó ($D = 1$)**: Khi có cừu cách tâm bầy xa hơn $f(N) = r_a N^{2/3}$, chó chuyển sang chế độ gom, nhắm vào điểm $P_c$ cách con cừu xa nhất một khoảng $r_a$. Khi bầy co cụm, chó lùa đàn từ điểm $P_d$ cách tâm bầy $r_a \sqrt{N}$ đối diện mục tiêu. Chó đứng yên khi cách cừu dưới $3 r_a$.
- **Tầng phối hợp đội ($D \ge 2$)**:
  - *Thu gom cá thể tản mác*: Xác định $D$ con cừu xa nhất. Phân công 1-1 giữa $D$ chú chó với $D$ con cừu tản mác thông qua thuật toán gán tuyến tính (Hungarian algorithm) tối thiểu hóa tổng quãng đường di chuyển Euclidean. Chó dư thừa sẽ tham gia hỗ trợ lùa đàn.
  - *Đội hình vòng cung lùa đàn*: Khi bầy co cụm, đàn chó dàn thành một hàng vòng cung bán kính $r_d$ bao trọn bề rộng bầy cừu phía sau tâm bầy. Chó được sắp xếp theo vị trí góc tương đối, loại trừ hoàn toàn nguy cơ cắt chéo đường đi của nhau.

![Quy tắc phối hợp đội strombom_multi](../figures/fig3_team_rule.png)

*Hình 1: Cơ chế phối hợp đa chó strombom_multi. Hàng trên: Thu gom cá thể tản mác qua thuật toán gán tối ưu. Hàng dưới: Đội hình vòng cung lùa đàn song song.*

#### Mô hình đối chứng không phối hợp: `fat` (Farthest-Agent Targeting)
Được HerdSim đề xuất làm mô hình triệt tiêu đối chứng, FAT kiểm chứng sự cần thiết của tầng phối hợp. Mỗi chú chó độc lập đuổi theo con cừu xa mục tiêu nhất, tiếp cận vị trí cách con cừu $r_a$ bằng bước động học Strömbom. FAT không có thuật toán gán Hungarian, không có đội hình vòng cung và không có lực đẩy giãn cách giữa các chú chó. Vì toàn bộ chó có cùng góc nhìn toàn cục, chúng cùng săn đuổi chung một con cừu duy nhất và dồn cục lại phía sau nó.

![Mô hình đối chứng không phối hợp FAT](../figures/fig4_fat.png)

*Hình S2b: Mô hình đối chứng FAT. Trái: Hình học của hành vi lùa không phối hợp săn đuổi con cừu xa đích nhất. Phải: Đàn chó dồn cục phía sau cùng một cá thể tản mác do thiếu cơ chế phân công và giãn cách (độ trùng lặp dog_overlap cao).*

#### Kiến trúc trường lực liên tục: `kubo` (Kubo et al. 2022)
HerdSim tích hợp mô hình lực liên tục hoàn chỉnh của Kubo et al. (2022) nhằm đối chứng chéo, bao gồm 4 lực liên tục tác động lên cừu và 4 lực thế năng tác động lên chó, trong đó lực đẩy giữa các chú chó ($1/r^3$) giúp chúng tự động dạt đều quanh bầy cừu.

![Mô hình lực liên tục Kubo](../figures/fig5_kubo.png)

*Hình S3: Mô hình lực liên tục của Kubo et al. (2022). Trái: 4 lực trên cừu. Giữa: 4 lực trên chó. Phải: Ảnh chụp mô phỏng cho thấy lực đẩy giữa các chó giúp duy trì khoảng cách bao quanh bầy cừu.*

### 4.4 Hình học sân bãi bất biến quy mô và thời hạn

Để loại bỏ sai số do sự giam hãm không gian khi $N$ tăng từ 25 lên 400, toàn bộ kích thước sân bãi được neo theo **bán kính bầy cừu ổn định đã hiệu chuẩn $R_f(N)$**:

![Hình học nhiệm vụ](../figures/fig6_task_geometry.png)

*Hình 2: Kích thước nhiệm vụ vẽ theo đúng tỷ lệ. Khoảng cách lùa $l = \max(13 R_f, 80, \text{reach} + R_{\text{goal}} + R_f)$ và bán kính đích $R_{\text{goal}} = 1{,}9 R_f$. Biên mở hoàn toàn không có tường phản xạ.*

Thời hạn được chuẩn hóa theo thời gian lùa tối thiểu $T_{\text{drive}} = l / v_{\text{sheep,max}}$:
- Thời hạn $12\times$ $T_{\text{drive}}$: Thoải mái (cho phép thu gom tuần tự nhiều lần).
- Thời hạn $6\times$ $T_{\text{drive}}$: Trung bình.
- Thời hạn $3\times$ $T_{\text{drive}}$: Cấp bách (tiến sát giới hạn di chuyển vật lý 1,46–1,74 $T_{\text{drive}}$).

Bảng 1 tóm tắt thông số nghiên cứu so với các công trình trước:

| Công trình | Mô hình bầy đàn | Bộ điều khiển chó | Kích thước bầy ($N$) | Quy mô đội ($D$) | Tiêu chí thành công | Có tìm quy mô tối thiểu? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Strömbom et al. 2014 | Hút khoảng cách ($n=N-1$) | Suy nghiệm gom/lùa | 2 đến 150 | 1 | Tâm bầy gần đích, 8.000 bước | Không ($D=1$) |
| Pierson & Schwager 2015 | Trường thế năng | Bao vây một phần | 1 đến 10 | 2 đến 12 | Hội tụ về đích | Không |
| Kubo et al. 2022 | Lực thế năng liên tục | Con xa đích nhất + đẩy giữa chó | 100 đến 1.000 | 1 đến 80 | Tâm bầy vào đích trong 500 s | So sánh cỡ đội; không tìm min |
| Lama & di Bernardo 2024 | Chuyển động Brown không liên kết | Phân chia mục tiêu cục bộ | Đa dạng | Đa dạng | 99% mục tiêu vào đích | Có ($N^* \sim \sqrt{M}$) |
| **Nghiên cứu này (HerdSim)** | **Strömbom & Kubo forces** | **`strombom_multi` & `fat`** | **25 đến 400** | **1 đến 24** | **100% hoặc 99% vào trước thời hạn** | **Có ($D_{\min}$ cùng thời hạn & hình học)** |

---

## 5. Tổng quan 23 chiến dịch thực nghiệm

Toàn bộ 23 giao thức chiến dịch (164.740 lượt chạy) được thực thi trên cụm 20 luồng worker không có lỗi phát sinh:

| Nhóm giao thức | Danh sách giao thức | Kích thước bầy ($N$) | Thời hạn | Tiêu chí | Mục tiêu khảo sát chính |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Lưới chính (Strict)** | `dmin_m12`, `dmin_m6`, `dmin_m3` | 25, 50, 100, 200, 400 | $12\times, 6\times, 3\times$ | 100% nghiêm ngặt | Lập bản đồ mở rộng quy mô trên 4 bố cục |
| **Lưới chính (99%)** | `dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3` | 25, 50, 100, 200, 400 | $12\times, 6\times, 3\times$ | Tiếp cận 99% | Đánh giá song song nhằm cô lập hiệu ứng cá thể lạc đàn |
| **Đối chứng FAT** | `dmin_fat`, `dmin_f99_fat` | 25, 50, 100, 200, 400 | $6\times$ | Cả hai | Kiểm chứng sự cần thiết của tầng phối hợp đội |
| **Mô hình Kubo** | `dmin_kubo` | 25, 50, 100 | 500 s | Nghiêm ngặt | Kiểm chứng chéo trên động lực học lực liên tục |
| **Độ nhạy (Strict)** | `dmin_s_base`, `_matched`, `_handler`, `_ring`, `_goal`, `_gap`, `_dogspeed` | 100, 200, 400 | $6\times$ | 100% nghiêm ngặt | Khảo sát quy ước: cách thả chó, tốc độ chó, cự ly, GPS thực địa |
| **Độ nhạy (99%)** | `dmin_f99_s_base`, `_matched`, `_handler`, `_ring`, `_goal`, `_gap`, `_dogspeed` | 100, 200, 400 | $6\times$ | Tiếp cận 99% | Kiểm tra xem độ nhạy có bắt nguồn từ cá thể lạc đàn hay không |

---

## 6. Kết quả thực nghiệm và câu trả lời cho các câu hỏi nghiên cứu

### 6.1 RQ1: $D_{\min}$ tăng trưởng thế nào theo kích thước bầy $N$?

**Câu trả lời trực tiếp cho RQ1**:
- Với bầy xuất phát co cụm (`compact`), $D_{\min} = 1$ là một hằng số bất biến tuyệt đối trên mọi quy mô ($N = 25$ đến $400$) và mọi thời hạn.
- Với các bầy phân tán (`wide`, `split`, `outlier_rich`), $D_{\min}$ tăng trưởng **dưới tuyến tính (sub-linear)** theo $N$. Ở thời hạn rộng rãi ($12\times$), $D_{\min} = 1$ cho $N \le 50$, và chỉ cần 2 đến 3 chó ở $N = 400$.
- Trong không gian log-log ($\log_2 D_{\min}$ theo $\log_2 N$), độ dốc tăng trưởng $\alpha$ dao động từ **0,20 đến 0,50** ở thời hạn $12\times$, và từ **0,30 đến 0,80** ở thời hạn $6\times$. Bầy cừu có tính liên kết đòi hỏi số lượng chó bổ sung ít hơn rất nhiều so với mức tăng $\alpha = 0{,}50$ ($\sqrt{M}$) của các mục tiêu không liên kết.

Bảng 2 tổng hợp ranh giới $D_{\min}$ (Nghiêm ngặt / Tiếp cận 99%):

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

*Hình 3: Thực nghiệm mở rộng $D_{\min}$ theo kích thước bầy $N$ qua các thời hạn và bố cục. Vòng tròn/nét liền: nghiêm ngặt; vuông/nét đứt: tiếp cận 99%. Thanh đứng tô bóng là các khoảng chặn chưa quyết định.*

![Thời gian hoàn thành trên bầy Compact](../figures/fig31_compact.png)

*Hình 4: Thời gian hoàn thành theo số lượng chó $D$ trên bầy compact. Trái: Cừu Strömbom với quy tắc đội (thời gian hoàn thành bất biến theo $D$). Phải: Mô hình lực liên tục Kubo (thời gian giảm từ 116 s xuống 30 s khi $D$ tăng từ 1 lên 10).*

Bảng 3 liệt kê độ dốc tăng trưởng trong không gian log-log:

| Tiêu chí | Thời hạn | Độ dốc `wide` | Độ dốc `split` | Độ dốc `outlier_rich` |
| :--- | :---: | :---: | :---: | :---: |
| **Nghiêm ngặt** | $12\times$ | 0,42 | 0,32 đến 0,42 | 0,42 |
| **Nghiêm ngặt** | $6\times$ | 0,48 ($N \le 200$) | Đi ngang ($N \le 100$) | 0,79 ($N \le 100$) |
| **Nghiêm ngặt** | $3\times$ | 0,79 ($N \le 100$) | Đi ngang ($N \le 100$) | 0,79 đến 1,50 ($N \le 100$) |
| **Tiếp cận 99%** | $12\times$ | 0,20 đến 0,30 | 0,20 | 0,30 |
| **Tiếp cận 99%** | $6\times$ | 0,30 đến 0,42 | Đi ngang ($N \le 100$) | 0,42 đến 0,48 |
| **Tiếp cận 99%** | $3\times$ | 0,62 đến 0,68 | Đi ngang ($N \le 100$) | 0,70 đến 1,10 ($N \le 200$) |

---

### 6.2 RQ2: Với cùng thời hạn, yếu tố nào chi phối $D_{\min}$ mạnh hơn: Bố cục hay $N$?

**Câu trả lời trực tiếp cho RQ2**:
- Quy mô đàn cừu $N$ tạo ra tác động định lượng tương đương hoặc lớn hơn so với bố cục hình học trên tất cả các điều kiện khảo sát.
- Phân tích độ biến động tính theo số lần nhân đôi (doublings - $\log_2$ của tỷ số giữa điểm giữa khoảng chặn lớn nhất và nhỏ nhất):
  - Biến thiên theo $N$ tạo ra độ phân tán trung bình từ **0,75 đến 1,69 lần nhân đôi**.
  - Biến thiên theo bố cục ở cùng quy mô $N$ tạo ra độ phân tán trung bình từ **0,50 đến 1,67 lần nhân đôi**.
- Tác động của bố cục chủ yếu đến từ bước nhảy giữa bầy `compact` ($D_{\min} \equiv 1$) và 3 bố cục phân tán. Giữa các bố cục phân tán với nhau (`wide` so với `outlier_rich`), sự chênh lệch hiếm khi vượt quá 1 chú chó.

Bảng 4 so sánh định lượng độ biến động theo số lần nhân đôi:

| Tiêu chí | Thời hạn | Biến động giữa các bố cục (Cố định $N$) | Biến động theo $N$ (Cố định bố cục) | Yếu tố chi phối chính |
| :--- | :---: | :---: | :---: | :--- |
| **Nghiêm ngặt** | $12\times$ | 0,68 lần nhân đôi | 1,19 lần nhân đôi | Quy mô đàn cừu $N$ |
| **Nghiêm ngặt** | $6\times$ | 1,67 lần nhân đôi | 1,69 lần nhân đôi | Tương đương / Quy mô $N$ |
| **Nghiêm ngặt** | $3\times$ | 0,76 lần nhân đôi | 0,97 lần nhân đôi | Quy mô đàn cừu $N$ |
| **Tiếp cận 99%** | $12\times$ | 0,50 lần nhân đôi | 0,75 lần nhân đôi | Quy mô đàn cừu $N$ |
| **Tiếp cận 99%** | $6\times$ | 0,92 lần nhân đôi | 1,30 lần nhân đôi | Quy mô đàn cừu $N$ |
| **Tiếp cận 99%** | $3\times$ | 1,25 lần nhân đôi | 1,28 lần nhân đôi | Tương đương / Quy mô $N$ |

---

### 6.3 RQ3: Áp lực thời hạn làm dịch chuyển $D_{\min}$ ra sao?

**Câu trả lời trực tiếp cho RQ3**:
- Thời hạn là tham số chi phối bậc một. Khi siết chặt thời hạn, toàn bộ đường cong tin cậy bị tịnh tiến sang phía bên phải.
- Mức độ dịch chuyển mang tính **phi tuyến**: nới lỏng từ $6\times$ lên $12\times$ thời gian lùa chỉ thay đổi $D_{\min}$ tối đa 1 chó, nhưng siết chặt từ $6\times$ xuống $3\times$ tạo ra sự gia tăng bùng nổ (ví dụ trên `wide` $N = 400$ dưới tiêu chí 99%, $D_{\min}$ tăng vọt từ 2–3 lên 5–6 chó; trên `split` $N \ge 200$, thời hạn ngặt nghèo dẫn đến thất bại trên toàn bộ các cỡ đội khảo sát).
- Lý do vật lý: Vận tốc di chuyển của tác tử là hữu hạn ($v_{\text{sheep}} = 1{,}0$, $v_{\text{dog}} = 1{,}5$). Ở thời hạn $12\times$, một chú chó có thừa thời gian để thu gom tuần tự từng con cừu rải rác. Ở thời hạn $3\times$, việc gom tuần tự là bất khả thi về mặt động học; đàn chó bắt buộc phải phân công gom song song đồng thời tất cả các cá thể tản mác.

![Tác động của thời hạn lên đường cong thành công](../figures/fig29_deadline.png)

*Hình 5: Tác động của thời hạn. Trái/Giữa: Đường cong thành công ở các thời hạn $12\times$, $6\times$, và $3\times$. Phải: Giá trị $D_{\min}$ biểu diễn trực tiếp theo hệ số thời hạn $m$.*

---

### 6.4 RQ4: Tiêu chí thành công làm thay đổi $D_{\min}$ thế nào? (Hiệu ứng cá thể lạc đàn)

**Câu trả lời trực tiếp cho RQ4**:
- Tiêu chí tiếp cận 99% đòi hỏi số chó bằng hoặc ít hơn đáng kể so với tiêu chí 100% nghiêm ngặt trên toàn bộ 34 ô phân tán khảo sát, giảm từ 1 đến 6 chó ở $N \ge 100$.
- Có 6 ô ở quy mô bầy lớn thất bại hoàn toàn dưới tiêu chí nghiêm ngặt nhưng đạt được $D_{\min}$ xác định dưới tiêu chí 99%.
- **Cơ chế cá thể lạc đàn (Straggler Mechanism)**: Trong 95% số lượt thất bại nghiêm ngặt của các đội có $D \ge 6$, đàn chó thực tế đã đưa được 99% số cừu vào đích từ rất sớm. Thất bại nghiêm ngặt xảy ra do đàn chó phá vỡ đội hình lùa để quay sang săn đuổi 1–2 con cừu lạc đàn còn lại bên ngoài. Khi áp sát, đàn chó vô tình đứng vào vị trí giữa bầy cừu và tâm đích, đẩy ngược toàn bộ khối cừu đã ổn định ra khỏi vòng tròn mục tiêu.
- Chó chạy chậm hơn ($v_{\text{dog}} = 1{,}15$) loại bỏ được xung lực vượt đà này, giúp tỷ lệ thành công nghiêm ngặt tăng từ thất bại hoàn toàn (`none`) lên $D_{\min} = 6$ ở bố cục `outlier_rich` ($N = 400$).

![Tỷ lệ thành công Nghiêm ngặt so với Tiếp cận 99%](../figures/fig30_strict_vs_99.png)

*Hình 6: So sánh tỷ lệ thành công giữa hai tiêu chí trên cùng hạt giống. Vùng tô bóng chứa các ô đạt độ tin cậy $\ge 90\%$ dưới tiêu chí 99% nhưng thất bại dưới tiêu chí nghiêm ngặt.*

![Phân tích vi mô hiệu ứng cá thể lạc đàn](../figures/fig22_straggler.png)

*Hình 7: Phân tích vi mô hiệu ứng cá thể lạc đàn. Trái: Tỷ lệ các lượt chạy $D \ge 6$ đưa được 99% cừu vào đích so với thành công nghiêm ngặt. Phải: Quỹ đạo chuỗi thời gian cho thấy chó nhanh ($1{,}5$) đẩy bật bầy cừu ra ngoài đích trong khi chó chậm ($1{,}15$) duy trì bầy ổn định trong đích.*

---

### 6.5 RQ5: Những quy luật nào đứng vững trước các phân tích độ nhạy?

**Câu trả lời trực tiếp cho RQ5**:
- **Dưới tiêu chí 99%**: Các quy luật mở rộng có tính vững chắc vượt trội. Dù thay đổi hình học thả chó (`handler`, `ring`, `arcs`), cự ly xuất phát (15, 30, 60 m), vận tốc chó (1,15 so với 1,50), hay áp dụng bộ tham số thực địa GPS của cừu, giá trị $D_{\min}$ vẫn duy trì ổn định trong phạm vi **1 chó** so với mốc cơ sở trên mọi ô.
- **Dưới tiêu chí nghiêm ngặt**: Giá trị tuyệt đối biến động dữ dội gấp 3 lần trở lên, do các quy ước thiết lập làm thay đổi quỹ đạo nhạy cảm của con cừu cuối cùng khi vào đích.
- **Hình học đích**: Việc thu hẹp bán kính đích ($1{,}5 R_f$) là biến thể duy nhất làm tăng thực sự $D_{\min}$ dưới cả hai tiêu chí (nâng `wide` $N = 400$ từ 2–3 lên 5–6 chó).

Bảng 5 tổng hợp lưới phân tích độ nhạy ở thời hạn $6\times$ ($D_{\min}$ Cơ sở / Biến thể):

| Tiêu chí | Biến thể kiểm tra độ nhạy | `wide` 100 | `wide` 200 | `wide` 400 | `outlier` 100 | `outlier` 200 | `outlier` 400 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Nghiêm ngặt** | Bộ tham số GPS thực địa | 1 / 1–6 | 3 / none | [9] / none | 3 / [1] | [12] / none | none / none |
| **Nghiêm ngặt** | Xuất phát từ cọc Handler | 1 / 1 | 3 / 3 | [9] / none | 3 / 2 | [12] / [3] | none / none |
| **Nghiêm ngặt** | Xuất phát vòng tròn Ring | 1 / 1 | 3 / 3–5 | [9] / [8] | 3 / 2–7 | [12] / [5] | none / none |
| **Nghiêm ngặt** | Thu hẹp bán kính đích ($1{,}5 R_f$) | 1 / 1–3 | 3 / none | [9] / none | 3 / 3 | [12] / none | none / none |
| **Nghiêm ngặt** | Thu hẹp cự ly xuất phát ($15$) | 1 / 1 | 3 / [3] | [9] / none | 3 / [1] | [12] / none | none / none |
| **Nghiêm ngặt** | Mở rộng cự ly xuất phát ($60$) | 1 / 1 | 3 / 3–4 | [9] / 6–7 | 3 / 3 | [12] / 5 | none / [12] |
| **Nghiêm ngặt** | Giảm vận tốc chó ($1{,}15$) | 1 / 1 | 3 / 3 | [9] / 5 | 3 / 2–3 | [12] / 4 | none / 6 |
| **99%** | Bộ tham số GPS thực địa | 1 / 1 | 2 / 1 | 2–3 / 2 | 2 / 1 | 2–3 / 1 | 3 / 2–3 |
| **99%** | Xuất phát từ cọc Handler | 1 / 1 | 2 / 2–3 | 2–3 / 2–3 | 2 / 2 | 2–3 / 2–3 | 3 / 3 |
| **99%** | Xuất phát vòng tròn Ring | 1 / 1 | 2 / 2–3 | 2–3 / 3 | 2 / 2 | 2–3 / 2 | 3 / 3 |
| **99%** | Thu hẹp bán kính đích ($1{,}5 R_f$) | 1 / 1 | 2 / 2 | 2–3 / 5–6 | 2 / 2 | 2–3 / 2–3 | 3 / none |
| **99%** | Thu hẹp cự ly xuất phát ($15$) | 1 / 1 | 2 / 2 | 2–3 / 2–3 | 2 / 1–2 | 2–3 / 2 | 3 / 3 |
| **99%** | Mở rộng cự ly xuất phát ($60$) | 1 / 1 | 2 / 2–3 | 2–3 / 2–3 | 2 / 2 | 2–3 / 2–3 | 3 / 3 |
| **99%** | Giảm vận tốc chó ($1{,}15$) | 1 / 1 | 2 / 2–3 | 2–3 / 2–3 | 2 / 2 | 2–3 / 2–3 | 3 / 3 |

![Biểu đồ nhiệt phân tích độ nhạy](../figures/fig24_sensitivity.png)

*Hình 8: Phân tích độ nhạy trên các biến thể thực nghiệm ở thời hạn $6\times$. Tiêu chí nghiêm ngặt (trên) biến động mạnh; tiêu chí tiếp cận 99% (dưới) thể hiện tính ổn định cao.*

---

### 6.6 RQ6: Mô hình đối chứng không phối hợp (FAT) có đạt được $D_{\min}$ hữu hạn?

**Câu trả lời trực tiếp cho RQ6**:
- Hoàn toàn không. Một quy tắc không có tầng phối hợp phân công hay lực đẩy không gian sẽ thất bại hoàn toàn khi đàn cừu mở rộng quy mô.
- Mặc dù FAT thành công ở đàn nhỏ ($N \le 100$), mô hình này đạt **0 ô tin cậy** ở $N \ge 200$ trên mọi bố cục phân tán, và thất bại ngay cả trên bầy `compact` $N = 400$ nơi `strombom_multi` chỉ cần 1 chó.
- Lý do toán học: Do toàn bộ chó có cùng góc nhìn toàn cục, mọi chú chó tính toán ra cùng một mục tiêu ($\arg\max_i \lVert \mathbf{x}_i - \mathbf{x}_{\text{goal}} \rVert$). Khi thiếu lực đẩy né tránh nhau, đàn chó dồn cục lại thành một khối duy nhất (`dog_overlap` $> 80\%$). Bổ sung thêm chó vào mô hình FAT không đem lại bất kỳ lợi ích song song hóa nào. Điều này chứng minh rằng việc $D_{\min}$ duy trì ở mức hữu hạn ở quy mô lớn là thuộc tính xuất hiện từ tầng phối hợp đội chứ không phải do số lượng cơ cấu chấp hành.

Bảng 6 so sánh $D_{\min}$ giữa FAT và `strombom_multi` ở thời hạn $6\times$:

| Bố cục xuất phát | $N = 25$ | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `compact` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / [12] (1 / 1) |
| `wide` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / none (3 / 2) | none / none ([9] / 2–3) |
| `split` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / none (none / [1]) | none / none (none / [5]) |
| `outlier_rich` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 2 / 2 (3 / 2) | none / none ([12] / 2–3) | none / none (none / 3) |

![So sánh FAT với Quy tắc đội strombom_multi](../figures/fig26_fat.png)

*Hình 9: Tỷ lệ thành công theo số lượng chó $D$ giữa strombom_multi (xanh lam) và FAT (cam). Đường cong của FAT đi ngang và hoàn toàn không cải thiện khi tăng số lượng chó.*

---

### 6.7 Phân tích vi mô hiện tượng tắc nghẽn trên bố cục phân cụm (`split`)

Trên bố cục `split` ở $N \ge 200$, việc tăng số lượng chó $D$ không giúp cải thiện tỷ lệ thành công ở các thời hạn trung bình ($6\times$ và $3\times$), với tỷ lệ thành công bị kẹt ở mức 0,60 đến 0,90 cho mọi $D \ge 4$. Phân tích vi mô dữ liệu log từng nhịp chỉ ra 2 nguyên nhân:
1. **Dồn ứ vào một phân cụm khi thu gom ($D = 4$)**: Do nhiệm vụ thu gom được chọn thuần túy theo khoảng cách tới trọng tâm toàn cục, các con cừu xa nhất thường nằm tập trung trong cùng một phân cụm. Trong lượt chạy lại với 12 hạt giống, toàn bộ $D$ chú chó cùng lao vào một phân cụm duy nhất trong $82 - 91\%$ số nhịp thu gom ban đầu. Khi can thiệp bằng cách phân tán mục tiêu đều ra các cụm, thời gian hoàn thành trung vị ở $D = 4$ giảm từ 631 s xuống 318 s.
2. **Quy tắc dừng $3 r_a$ gây đóng băng đàn chó ($D \ge 8$)**: Quy tắc Strömbom bắt buộc chó đứng yên khi cách bất kỳ con cừu nào dưới $3 r_a = 6$ m. Trên đàn `split`, mật độ cục bộ dày đặc khiến **25% tổng số chó bị đóng băng đứng yên** trong suốt thời gian chạy (so với $< 1\%$ trên đàn `wide`). Trong lượt chạy thử nghiệm rút ngắn khoảng cách dừng xuống $r_a = 2$ m, tỷ lệ chó đứng yên giảm mạnh, rút ngắn 20–24% thời gian lùa và đạt 12/12 trận thắng ở $D = 16$.

![Đường cong thành công trên bố cục Split](../figures/fig23_split_curves.png)

*Hình 10: Tắc nghẽn hiệu năng trên bố cục split. Tăng số chó không giúp đạt độ tin cậy ở $N \ge 200$ do dồn ứ cụm và quy tắc dừng cự ly.*

![Tương quan các chỉ số vi mô](../figures/fig27_metrics.png)

*Hình 11: Tương quan chỉ số vi mô. (a) Tương quan nghịch mạnh giữa độ tản trung bình của bầy và tỷ lệ thành công (Spearman $r = -0{,}56$ đến $-0{,}81$). (b) Tỷ lệ chó đứng yên trên split so với wide. (c) Tỷ lệ trùng lặp cặp đôi giữa các chú chó.*

---

## 7. Thảo luận khoa học (Discussion)

### 7.1 So sánh với các quy luật mở rộng đã công bố
Độ dốc tăng trưởng dưới tuyến tính của chúng tôi ($\alpha = 0{,}20 - 0{,}50$ ở $12\times$) thấp hơn đáng kể so với mức tăng trưởng $\sqrt{M}$ ($\alpha = 0{,}50$) được chứng minh bởi Lama và di Bernardo (2024) cho các mục tiêu không liên kết. Sự khác biệt này hoàn toàn phù hợp với cơ chế sinh học: với các mục tiêu rời rạc không liên kết, mỗi cá thể phải được lùa độc lập bởi một tác tử điều khiển. Ngược lại, lực hút bầy đàn toàn cục ($n = N - 1$) trong mô hình Strömbom tạo ra khả năng tự co cụm: chỉ cần chó đưa các cá thể tản mác tiếp cận phạm vi tương tác của bầy, lực hút nội tại sẽ tự động kéo chúng hòa nhập vào khối chính, giúp giảm tải rất lớn cho đội ngũ chăn dắt ở quy mô lớn.

### 7.2 Tính hai giai đoạn của bài toán chăn dắt tập thể
Kết quả của chúng tôi chứng minh rằng bài toán chăn dắt tập thể bao gồm hai giai đoạn vật lý hoàn toàn tách biệt:
1. **Giai đoạn di chuyển (Thu gom và lùa bầy)**: Có khả năng mở rộng quy mô cao, tăng trưởng dưới tuyến tính theo $N$, và được phản ánh vững chắc thông qua tiêu chí tiếp cận 99%.
2. **Giai đoạn chặn giữ tại đích (Xử lý cá thể lạc đàn)**: Có tính nhạy cảm cực cao, không mở rộng quy mô tốt, và dễ bị hiện tượng vượt đà xé đàn dưới tiêu chí nghiêm ngặt.

Trong thực tế ứng dụng robot và nông nghiệp, một cá thể cừu rớt lại phía sau không đồng nghĩa với nhiệm vụ thất bại. Chúng tôi kiến nghị các chuẩn đánh giá hệ thống đa tác tử trong tương lai nên tách bạch rõ ràng giữa chỉ số tiếp cận đích và một giai đoạn chặn giữ chủ động sau cùng (như đóng cổng chuồng hoặc thiết lập vòng tuần tra vận tốc chậm).

---

## 8. Hạn chế và các yếu tố ảnh hưởng độ tin cậy (Limitations)

1. **Đơn giản hóa động học 2D**: Cừu và chó được mô phỏng như các chất điểm 2D có khả năng đổi hướng tức thời và không bị suy giảm thể lực theo thời gian.
2. **Điều kiện biên mở hoàn toàn**: Đồng cỏ thực tế luôn có hàng rào bao quanh, đóng vai trò hỗ trợ đắc lực cho chó chăn dồn ép gia súc.
3. **Ranh giới khoảng chặn do rời rạc hóa**: Các ô có độ tin cậy thực tế xấp xỉ $\theta = 0{,}90$ sẽ không thể ngã ngũ ở mốc 200 hạt giống, đòi hỏi phải báo cáo dưới dạng khoảng chặn.
4. **Giả định thông tin toàn cục**: Kiến trúc `strombom_multi` giả định đàn chó nắm rõ tọa độ chính xác của mọi cá thể, trong khi robot thực địa phải dựa trên thông tin cục bộ, cảm biến góc nhìn hoặc truyền thông giới hạn.

---

## 9. Kết luận và định hướng tương lai (Conclusions & Future Work)

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
| `dmin_m6` | 13.470 | 191 | 170 | 21 | 0 | 0.41 h |
| `dmin_m3` | 9.530 | 183 | 178 | 5 | 0 | 0,17 h |
| `dmin_f99_m12` | 11.100 | 180 | 178 | 2 | 0 | 0,41 h |
| `dmin_f99_m6` | 14.240 | 191 | 174 | 17 | 0 | 0,49 h |
| `dmin_f99_m3` | 11.140 | 185 | 177 | 8 | 0 | 0,27 h |
| `dmin_fat` | 8.660 | 181 | 179 | 2 | 0 | 0,22 h |
| `dmin_f99_fat` | 8.670 | 184 | 183 | 1 | 0 | 0,23 h |
| `dmin_kubo` | 1.080 | 18 | 18 | 0 | 0 | 0,08 h |
| Các giao thức độ nhạy (14 lượt) | 69.630 | 805 | 734 | 71 | 0 | 3,50 h |
| **Tổng cộng** | **164.740** | **2.291** | **2.190** | **148** | **0** | **~7,0 h** |
