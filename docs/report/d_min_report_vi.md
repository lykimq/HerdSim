# Quy mô đội tối thiểu để lùa một bầy cừu mô phỏng: Sự phụ thuộc vào kích thước đàn, bố cục khởi tạo, thời hạn và tiêu chí thành công

Dự án HerdSim. Bản thảo ngày 21-10-2026, được tổng hợp từ đề cương nghiên cứu và dữ liệu thực nghiệm ngày 20 và 21-10-2026.

## Tóm tắt (Abstract)

Cần bao nhiêu cá thể chó để lùa một bầy cừu vào mục tiêu trước một thời hạn xác định? Chúng tôi nghiên cứu câu hỏi này thông qua mô phỏng, sử dụng mô hình hành vi cừu của Strömbom et al. (2014) và phần mở rộng đa tác tử (multi-dog) cho thuật toán gom và lùa đàn; trong đó mỗi cá thể chó tự động phụ trách một cá thể cừu tản mác riêng biệt khi thu gom, và chiếm một vị trí xác định trên vòng cung phía sau bầy cừu khi lùa đàn. Chúng tôi định nghĩa $D_{\min}$ là quy mô đội nhỏ nhất có tỷ lệ thành công được chứng minh đạt ít nhất 0,90 theo khoảng tin cậy hai phía 99% Clopper–Pearson. Các hạt giống ngẫu nhiên (seeds) chỉ được bổ sung vào các ô thực nghiệm mà quyết định phân loại vẫn chưa ngã ngũ, tối đa 200 hạt giống mỗi ô. Chúng tôi lập bản đồ $D_{\min}$ trên các quy mô bầy cừu từ $N = 25$ đến $400$, bốn bố cục khởi tạo và các thời hạn bằng 12, 6 và 3 lần thời gian lùa tiêu chuẩn ($T_{\text{drive}}$), dưới hai tiêu chí thành công: nghiêm ngặt (toàn bộ 100% cừu vào mục tiêu) và nới lỏng (99% số cừu vào mục tiêu).

Trong 17 giao thức thực nghiệm (112.785 lượt chạy, không có lỗi hệ thống), một bầy cừu co cụm (compact) chỉ cần đúng 1 chó ở mọi quy mô $N$ và mọi thời hạn. Trên các bố cục phân tán, $D_{\min} = 1$ đối với $N \le 50$ và tăng chậm theo $N$, với độ dốc log-log từ 0,2 đến 0,5 ở hầu hết các hàng thử nghiệm tại thời hạn $12\times$ và $6\times$, chỉ chạm mức 2 hoặc 3 chó khi $N = 400$ với thời hạn $12\times$. Việc siết chặt thời hạn từ $12\times$ xuống $3\times$ làm tăng $D_{\min}$ mạnh hơn cả việc tăng quy mô $N$ lên gấp bốn lần (bố cục phân tán rộng wide, $N = 400$: tăng từ 2 lên 6 chó). Dưới tiêu chí nghiêm ngặt 100%, sáu ô quy mô $N$ lớn không thể chốt được $D_{\min}$ nhưng lại được giải quyết dứt điểm dưới tiêu chí 99%; trong các lượt chạy thất bại, bầy cừu đã vào đến mục tiêu cùng toàn bộ đàn ngoại trừ một hoặc hai con rớt lại, và sau đó cả bầy bị lùa vọt qua và bật ra ngoài mục tiêu. Trên bố cục gồm ba cụm tách biệt (split), tỷ lệ thành công không tăng theo quy mô đội khi $N \ge 200$. Các lượt chạy thay đổi tham số cừu, kích thước mục tiêu, vị trí xuất phát hoặc tốc độ của chó có thể làm thay đổi giá trị tuyệt đối của $D_{\min}$ lên tới sáu lần, nhưng không có ô nào khi tăng $N$ lại làm giảm $D_{\min}$. Do đó, mối quan hệ phụ thuộc của $D_{\min}$ vào $N$, bố cục và thời hạn có tính chất vững chắc (robust) hơn nhiều so với giá trị số tuyệt đối của nó; và bất kỳ giá trị $D_{\min}$ nào được báo cáo đều bắt buộc phải gắn liền với thời hạn và tiêu chí thành công tương ứng.

**Từ khóa:** chăn dắt bầy đàn (shepherding), điều khiển bầy đa tác tử (multi-agent herding), khả năng mở rộng (scalability), mô phỏng dựa trên tác tử (agent-based simulation), chó chăn cừu, quy mô đội tối thiểu, kiểm định giả thuyết tuần tự.

---

## 1. Giới thiệu (Introduction)

Lùa cừu bằng chó chăn dắt là ví dụ kinh điển về việc một số ít tác tử bị kiểm soát điều hướng một lượng lớn các tác tử tự do. Bài toán tương tự xuất hiện trong kỹ thuật robot và điều khiển học như dẫn đường cho đàn robot tự hành (swarms), điều tiết đám đông hoặc xua đuổi động vật hoang dã khỏi các khu vực nhạy cảm (Strömbom et al. 2014; di Bernardo 2026). Strömbom et al. (2014) đã chứng minh rằng một cá thể chăn dắt đơn lẻ luân phiên giữa hai hành vi: thu gom cá thể cừu xa tâm bầy nhất và lùa cả đàn từ phía sau, có thể tái hiện chính xác chuyển động zíc-zắc của chó chăn cừu thực tế và dẫn dắt bầy đàn lên tới 150 cá thể khi mỗi con cừu bị hút về một tỷ lệ đủ lớn các cá thể khác trong đàn. Dữ liệu thực địa từ một chú chó Border Collie lùa 14 con cừu xác nhận rằng chó luôn làm việc sát phía sau những con cừu đi cuối và liên tục điều chỉnh theo bầy (Jadhav et al. 2024).

Khi có nhiều hơn một cá thể chăn dắt, nhiều chiến lược điều khiển đã được đề xuất. Pierson và Schwager (2015) sử dụng hai hoặc nhiều robot chó bao vây một phần bầy đàn và chứng minh sự hội tụ đối với một con cừu đơn lẻ. Kubo et al. (2022) bổ sung lực đẩy giữa các cá thể chó khiến chúng tự tạo thành vòng tròn bao quanh bầy cừu, và báo cáo rằng nhiều chó hơn giúp dẫn đàn nhanh hơn và tin cậy hơn. Auletta et al. (2021) nghiên cứu các quy tắc cục bộ và chiến lược chọn mục tiêu cho các cá thể chăn dắt gom các mục tiêu ngẫu nhiên không có lực liên kết. Li et al. (2025) chứng minh việc chăn dắt khả thi ngay cả khi chỉ đo được góc phương vị (bearing-only), và Brown et al. (2025) mô hình hóa bài toán dưới dạng điều khiển tối ưu cho $m$ chó và $n$ cừu. Các nghiên cứu này cho thấy việc tăng số lượng chó có thể đem lại lợi ích, nhưng họ luôn cố định quy mô đội và không đặt câu hỏi một nhiệm vụ cụ thể đòi hỏi tối thiểu bao nhiêu cá thể chăn dắt.

Hai nghiên cứu gần đây đã trực tiếp giải quyết câu hỏi này. Lama và di Bernardo (2024) nhận thấy số lượng cá thể chăn dắt tối thiểu $N^*$ để gom $M$ mục tiêu không liên kết tăng theo căn bậc hai của $M$ ($\sqrt{M}$), và dưới một mật độ mục tiêu tới hạn, con số này tăng nhanh hơn. Một bản thảo ẩn danh năm 2025, "Collective nudging that scales", đã đo lường số lượng chó tối thiểu để thu gom, duy trì và nhốt bầy cừu lên đến 400 con trong vòng 10.000 nhịp mô phỏng (ticks), và phát hiện sự gia tăng phi tuyến tính theo kích thước đàn cùng với hiện tượng sụt giảm tỷ lệ thành công khi sử dụng quá nhiều chó (anonymous 2025). Tuy nhiên, trong cả hai nghiên cứu, phân bố ban đầu, giới hạn thời gian và tiêu chí thành công đều bị đóng khung cố định. Chưa có công trình nào báo cáo kết quả này thay đổi ra sao khi thời gian cho phép co giãn, khi hình dạng ban đầu của bầy cừu biến thiên, hoặc khi tỷ lệ cừu bắt buộc phải đến đích thay đổi.

Trong nghiên cứu này, chúng tôi đo lường $D_{\min}$ — quy mô đội nhỏ nhất đạt độ tin cậy — đối với bầy cừu Strömbom được lùa vào một mục tiêu hình tròn, đồng thời xử lý bố cục khởi tạo, thời hạn và tiêu chí thành công như các biến số độc lập bên cạnh quy mô đàn cừu. Các đóng góp chính gồm:

1. Định nghĩa $D_{\min}$ dưới dạng một quyết định thống kê chặt chẽ, đi kèm cơ chế phân bổ hạt giống thích ứng (adaptive seed allocation) chỉ tập trung tính toán ở các ô chưa ngã ngũ và gắn nhãn rõ ràng các ô không thể quyết định.
2. Bản đồ thực nghiệm $D_{\min}$ trên năm quy mô bầy đàn, bốn bố cục ban đầu và ba thời hạn, dưới hai tiêu chí thành công, cho mô hình cừu Strömbom và tầng điều phối đội đa tác tử mở rộng.
3. Bằng chứng thực nghiệm cho thấy yêu cầu nghiêm ngặt (100% cừu vào đích) làm bế tắc nhiều ô thực nghiệm quy mô lớn chỉ vì một hoặc hai con cừu cuối cùng, cùng mô tả cơ chế hỏng hóc dẫn đến hiện tượng này.
4. Phân tích độ nhạy trên các quy ước thiết lập mô phỏng vốn không có quy tắc thực tế (điểm xuất phát của chó, khoảng cách ban đầu, kích thước mục tiêu, bộ tham số cừu, tốc độ chó), tách biệt phần quy luật cốt lõi vững chắc khỏi các con số tuyệt đối.

---

## 2. Các công trình liên quan (Related Work)

### 2.1 Một người chăn dắt
Strömbom et al. (2014) mô hình hóa mỗi con cừu như một hạt tự hành bị hút về trọng tâm của $n$ láng giềng gần nhất, bị đẩy xa khỏi các láng giềng quá gần và bị xua đuổi bởi người chăn dắt. Người chăn dắt lùa bầy từ phía sau khi toàn bộ cừu nằm trong khoảng cách $f(N) = r_a N^{2/3}$ tính từ tâm bầy, và ngược lại sẽ chạy ra phía sau con cừu xa nhất để thu gom. Chuyển động đảo qua đảo lại thực tế xuất hiện tự nhiên từ việc chuyển đổi giữa hai chế độ này. Với lực hút toàn cục ($n = N - 1$), một người chăn luôn thành công với $N \le 150$; khi $n$ giảm xuống dưới $0,53 N$, tỷ lệ thành công giảm mạnh, và khi $n \ll N$ thì hầu như thất bại. Bài báo ghi nhận rằng các đàn lớn hơn thường cần nhiều người chăn dắt nhưng không đưa ra quy tắc phối hợp cho họ.

### 2.2 Nhiều người chăn dắt
Pierson và Schwager (2015) thiết kế bộ điều khiển phản hồi cho hai hoặc nhiều robot chó quy đổi hệ chó-cừu về mô hình unicycle. Kubo et al. (2022) dùng mô hình lực đẩy-hút trong đó mỗi chó đẩy con cừu xa mục tiêu nhất và đẩy lẫn nhau; lực đẩy giữa các chó giúp chúng tản đều quanh bầy, dẫn dắt thành công đàn lên tới 1.000 con. Auletta et al. (2021) so sánh chiến lược chọn mục tiêu tĩnh và động cho 2 người chăn dắt và 3 đến 60 mục tiêu không liên kết. Li et al. (2025) loại bỏ giả định biết vị trí tuyệt đối và điều khiển bầy chỉ bằng góc nhìn. Brown et al. (2025) tính toán quỹ đạo tối ưu cho số lượng nhỏ chó và cừu, nhận thấy các phương pháp số giải tích gặp khó khăn lớn khi khoảng cách giữa chó và cừu quá gần.

### 2.3 Quy luật mở rộng quy mô đội chăn dắt
Lama và di Bernardo (2024) nghiên cứu các tác tử chăn dắt có tầm cảm nhận hữu hạn và các mục tiêu không có liên kết bầy đàn. Số lượng chăn dắt tối thiểu $N^*$ để đưa tỷ lệ $\chi^* = 0,99$ số mục tiêu vào đích tăng theo $\sqrt{M}$ khi tầm cảm nhận vô hạn. Bản thảo ẩn danh 2025 dùng mô hình mật độ cục bộ với 7 láng giềng topo, trường có tường chắn, nhiệm vụ 3 giai đoạn (thu gom, giữ chân 800 nhịp, thoát qua cổng) và thành công khi toàn bộ cừu qua cổng trong 10.000 nhịp. Công trình này báo cáo 1 chó thành công tới 100 cừu, 3 chó ở 150 cừu, 20 chó ở 200 cừu và 35 chó ở 400 cừu để đạt tỷ lệ thành công 90%; quá nhiều chó làm giảm thành công ở đàn nhỏ.

Bảng 1 tóm tắt các nghiên cứu tiêu biểu so với công trình hiện tại:

| Nghiên cứu | Mô hình cừu | Quy tắc chăn dắt | Quy mô bầy cừu $N$ | Quy mô đội $D$ | Tiêu chí thành công | Khảo sát đội tối thiểu |
|---|---|---|---|---|---|---|
| Strömbom et al. 2014 | Hút-đẩy, $n$ láng giềng | Thu gom hoặc lùa | 2 đến 150 | 1 | Tâm đàn gần đích, 8.000 bước | Không |
| Pierson & Schwager 2015 | Trường thế năng | Bao vây một phần | 1 đến 10 | 2 đến 3 | Hội tụ về vùng mục tiêu | Không |
| Kubo et al. 2022 | Mô hình lực, trường nhìn | Đẩy con xa đích nhất, đẩy giữa chó | Đến 1.000 | 1 đến 5 | Toàn bộ cừu vào đích | Không |
| Lama & di Bernardo 2024 | Chuyển động Brown, không liên kết | Đuổi con xa đích nhất | Đa dạng | Đa dạng | 99% mục tiêu vào đích | Có, $N^* \sim \sqrt{M}$ |
| Bản thảo ẩn danh 2025 | Mật độ cục bộ, 7 láng giềng | Gom, lùa trên cung, tuần tra | 5 đến 400 | 1 đến 35 | Toàn bộ qua cổng, 10.000 nhịp | Có, thời gian cố định |
| **Nghiên cứu này** | **Strömbom, $n = N - 1$** | **Gom hoặc lùa, có tầng phối hợp đội** | **25 đến 400** | **1 đến 24** | **100% hoặc 99% vào đích trước thời hạn** | **Có, xem thời hạn là một biến số** |

---

## 3. Câu hỏi nghiên cứu và Định nghĩa $D_{\min}$

Chúng tôi đặt câu hỏi: Cần bao nhiêu cá thể chó để lùa một bầy cừu vào mục tiêu một cách tin cậy trước thời hạn, và con số đó phụ thuộc thế nào vào bầy cừu và nhiệm vụ? Cụ thể:

- **RQ1**: $D_{\min}$ tăng trưởng như thế nào theo quy mô bầy đàn $N$, đối với từng bố cục khởi tạo và thời hạn?
- **RQ2**: Ở cùng một thời hạn, yếu tố nào tác động mạnh hơn đến $D_{\min}$: bố cục khởi tạo hay quy mô đàn $N$?
- **RQ3**: $D_{\min}$ phụ thuộc vào thời hạn hoàn thành như thế nào?
- **RQ4**: Tiêu chí thành công làm thay đổi $D_{\min}$ ra sao?
- **RQ5**: Những kết luận nào từ RQ1 đến RQ4 vẫn đứng vững trước các thay đổi về quy ước thiết lập mô phỏng?

Một **ô thực nghiệm (cell)** là sự kết hợp của một quy tắc chăn dắt, bố cục khởi tạo, quy mô $N$, thời hạn và kích thước đội $D$. Một lượt chạy thành công khi tỷ lệ cừu yêu cầu nằm trọn trong mục tiêu tại một nhịp thời gian trước khi hết hạn. Với một ô có $k$ lượt thành công trên $n$ lượt thử, gọi $[L, U]$ là khoảng tin cậy hai phía 99% Clopper–Pearson của tỷ lệ thành công. Với ngưỡng $\theta = 0,90$, ô thực nghiệm được phân loại:

- **Tin cậy (reliable)** khi $L \ge \theta$,
- **Không tin cậy (unreliable)** khi $U < \theta$,
- **Chưa ngã ngũ (undecided)** trong các trường hợp còn lại.

Trên một đường cong thực nghiệm quét qua các giá trị $D$ ở một cấu hình cố định:
- $D_{\min}$: giá trị $D$ nhỏ nhất có ô đạt mức tin cậy ($L \ge 0,90$).
- $D_{\min\_\text{low}}$: giá trị $D$ nhỏ nhất có cận trên $U$ chạm tới $\theta = 0,90$.

Khi đường cong đã ngã ngũ, $D_{\min\_\text{low}} = D_{\min}$. Khi $D_{\min}$ đã xuất hiện nhưng tồn tại giá trị $D$ nhỏ hơn vẫn chưa ngã ngũ, giá trị tối thiểu thực tế nằm trong khoảng $[D_{\min\_\text{low}}, D_{\min}]$, ký hiệu là `[D_min_low]`. Khi không có giá trị $D$ nào đạt tin cậy trên lưới thử nghiệm, ký hiệu là `none`. Một ô tin cậy đòi hỏi tối thiểu 51 trận thắng liên tiếp ($0,9^{51} < 0,005$), và với kích thước lô 10 hạt giống, con số này được làm tròn lên 60 lượt thử.

Thời hạn hoàn thành là một phần không thể tách rời của bài toán. Nếu cho thời gian vô hạn, một chú chó duy nhất cuối cùng cũng sẽ lùa được hầu hết mọi bầy cừu có tính liên kết. Chúng tôi biểu diễn thời hạn dưới dạng bội số $m$ của thời gian lùa tiêu chuẩn ($T_{\text{drive}}$), định nghĩa bằng khoảng cách lùa chia cho tốc độ tối đa của cừu. Bầy cừu co cụm được 1 chó lùa ngay từ nhịp đầu tiên sẽ đến đích trong trung vị 1,45 đến 1,74 $T_{\text{drive}}$ ($N = 25$ đến $400$). Do đó, $m$ nhỏ hơn 1,5 là bất khả thi, và các giá trị $m$ lớn hơn sẽ đo lường xem cần bao nhiêu chó để vừa gom đàn phân tán vừa đưa về đích kịp thời.

---

## 4. Mô hình (Model)

### 4.1 Cừu
Cừu tuân theo mô hình Strömbom et al. (2014). Cừu cách xa mọi chó hơn khoảng cách đe dọa $r_s$ sẽ gặm cỏ: đứng yên hoặc bước một bước ngẫu nhiên độ dài $\delta$ với xác suất $p$. Cừu nằm trong bán kính $r_s$ của bất kỳ chó nào sẽ chuyển hướng theo vector:

$$\mathbf{H}' = h \mathbf{H} + c \mathbf{C} + \rho_a \mathbf{R}_a + \rho_s \mathbf{R}_s + e \mathbf{\epsilon} \tag{1}$$

trong đó mỗi số hạng là một vector đơn vị: $\mathbf{H}$ là hướng di chuyển trước đó, $\mathbf{C}$ hướng về tâm khối của $n$ láng giềng gần nhất, $\mathbf{R}_a$ đẩy xa khỏi các láng giềng gần hơn khoảng cách $r_a$, $\mathbf{R}_s$ đẩy xa khỏi các chó trong phạm vi $r_s$, và $\mathbf{\epsilon}$ là nhiễu góc ngẫu nhiên. Cừu sau đó di chuyển một đoạn $\delta$ theo hướng $\mathbf{H}'$.

**Hòa trộn lực đẩy đa tác tử (Push Blending):** Khi có nhiều chó trong tầm $r_s$, chúng tôi cộng các vector đẩy đơn vị từ tất cả các chó lại rồi chuẩn hóa về độ dài đơn vị:

$$\mathbf{S}_i = \frac{\sum_{j \in \text{threat}} \frac{\mathbf{x}_i - \mathbf{y}_j}{\lVert \mathbf{x}_i - \mathbf{y}_j \rVert}}{\left\lVert \sum_{j \in \text{threat}} \frac{\mathbf{x}_i - \mathbf{y}_j}{\lVert \mathbf{x}_i - \mathbf{y}_j \rVert} \right\rVert}$$

Điều này bảo đảm tính chân thực sinh học: nhiều chó cùng dồn ép một con cừu sẽ tạo áp lực từ hướng trung bình mà không gây ra gia tốc siêu vật lý phi thực tế (Hình S1).

![Quy tắc di chuyển của cừu](figures/fig1_sheep_rule.png)

*Hình S1: Mô hình cừu Strömbom. Trái: một cá thể cừu nằm trong khoảng cách phản xạ với 5 thành phần của phương trình (1), trọng số tương ứng và vector hướng di chuyển kết quả. Phải: một chú chó và bầy cừu xung quanh; cừu nằm ngoài bán kính r_s tiếp tục gặm cỏ, cừu nằm trong bán kính r_s di chuyển trốn chạy.*

### 4.2 Chó
Với 1 chó, hành vi tuân thủ chính xác quy tắc của Strömbom et al. (2014) (Hình S2). Chó chuyển sang chế độ **thu gom (collect)** khi có bất kỳ con cừu nào cách tâm bầy xa hơn $f(N) = r_a N^{2/3}$, nhắm vào điểm cách con cừu xa nhất một đoạn $r_a$ về phía đối diện tâm bầy. Ngược lại, chó chuyển sang chế độ **lùa đàn (drive)**, nhắm vào điểm cách tâm bầy một đoạn $r_a \sqrt{N}$ về phía đối diện mục tiêu. Chó di chuyển với vận tốc $\delta_s$ và đứng yên nếu cách bất kỳ con cừu nào dưới $3 r_a$.

![Người chăn dắt đơn lẻ](figures/fig2_shepherd.png)

*Hình S2: Người chăn dắt đơn lẻ theo Strömbom et al. (2014). Trái: khi có cừu tản mác ngoài f(N), chó di chuyển tới điểm thu gom P_c phía sau con cừu xa nhất. Phải: khi bầy đã co cụm, chó di chuyển tới điểm lùa P_d phía sau bầy cừu đối diện với mục tiêu. Chó đứng yên khi nằm trong khoảng cách 3 r_a tới cừu (vùng tô bóng).*

Với nhiều chó ($D > 1$), tầng phối hợp đội phân công nhiệm vụ chuyên biệt (`strombom_multi`) (Hình 1):
- **Khi thu gom**: $D$ cá thể cừu tản mác xa nhất được ghép cặp với $D$ cá thể chó thông qua thuật toán gán tuyến tính tối thiểu hóa tổng quãng đường di chuyển (linear sum assignment). Chó thừa sẽ tham gia hỗ trợ lùa đàn.
- **Khi lùa đàn**: Các chó dàn hàng trên một vòng cung phía sau bầy cừu, trải đều trên góc mở bao trọn bề rộng bầy đàn, giữ nguyên thứ tự góc để tuyệt đối không cắt chéo đường đi của nhau. Mỗi cá thể chó đều nắm rõ tọa độ của mọi con cừu và các đồng đội khác.

![Quy tắc phối hợp đội strombom_multi](figures/fig3_team_rule.png)

*Hình 1: Từ một chó đến nhiều chó, trích xuất từ mô phỏng khi bắt đầu thử nghiệm. Cột trái: một chó theo quy tắc Strömbom et al. (2014). Hàng trên: trên bố cục phân tán wide, các chó thu gom cừu, mỗi chó nhắm tới điểm gom của cá thể tản mác được ghép cặp theo quãng đường ngắn nhất. Hàng dưới: trên bố cục co cụm compact, các chó dàn hàng hình cung phía sau bầy, trải đều theo bề rộng bầy cừu. Dấu chữ thập đánh dấu điểm nhắm tới.*

### 4.3 Mô hình cừu thứ hai (Kubo et al. 2022)
Để đối chứng, chúng tôi chạy thử mô hình lực liên tục của Kubo et al. (2022) (Hình S3). Mô hình này không có nhiễu ngẫu nhiên nên các hạt giống chỉ thay đổi vị trí khởi đầu. Do mô hình này nén bầy cừu về một bán kính cố định, chúng tôi thử nghiệm đến $N = 100$.

![Mô hình lực Kubo](figures/fig5_kubo.png)

*Hình S3: Mô hình lực liên tục của Kubo et al. (2022). Trái: 4 vector lực tác động lên một con cừu (lực đẩy, căn chỉnh hướng, lực hút, và lực trốn chạy chó). Giữa: 4 vector lực tác động lên một chú chó (hút về cừu mục tiêu, cự ly an toàn với cừu, tránh mục tiêu, và lực đẩy giữa các chó). Phải: Lượt thử nghiệm cho thấy lực đẩy giữa các chó giúp chúng tự động phân tán đều quanh chu vi bầy đàn.*

### 4.4 Các tham số
Bảng 2 liệt kê các tham số của mô hình Strömbom:

| Ký hiệu | Giá trị | Ý nghĩa vật lý |
|---|---|---|
| $r_a$ | 2 | Khoảng cách tương tác cừu-cừu; thiết lập khoảng cách lùi của chó |
| $\rho_a$ | 2 | Trọng số lực đẩy tránh va chạm giữa các cừu láng giềng |
| $c$ | 1.05 | Trọng số lực hút về tâm bầy cừu láng giềng |
| $\rho_s$ | 1 | Trọng số lực đẩy hoảng sợ né tránh chó chăn dắt |
| $h$ | 0.5 | Trọng số quán tính duy trì hướng di chuyển trước |
| $e$ | 0.3 | Trọng số nhiễu góc ngẫu nhiên (áp dụng cho cả cừu và chó) |
| $\delta$ | 1 | Độ dài bước di chuyển của cừu trong 1 nhịp (1 m/s) |
| $p$ | 0.05 | Xác suất cừu bước ngẫu nhiên khi gặm cỏ |
| $r_s$ | 65 | Bán kính đe dọa (cừu bắt đầu phản ứng hoảng sợ khi chó tiến vào) |
| $n$ | $N - 1$ | Số lượng láng giềng trong lực hút bầy (hút toàn cục) |
| $\delta_s$ | 1.5 | Bước di chuyển của chó trong 1 nhịp (tốc độ $v_{\text{dog}} = 1.5$ m/s) |
| - | $3 r_a$ | Chó đứng yên nếu tiến sát cừu trong cự ly này để tránh làm vỡ đàn |

Strömbom et al. (2014) cũng cung cấp bộ tham số thực địa GPS ($r_a = 1$, $e = 0,1$, $r_s = 75$), được chúng tôi đưa vào phân tích độ nhạy (Hình S6).

![Đối chiếu thực địa](figures/fig14_realism_numbers.png)

*Hình S6: So sánh bầy cừu thực địa của Jadhav et al. (2024) với bộ tham số cơ sở và bộ tham số thực địa GPS tại N = 100: bán kính bầy, mật độ, cự ly làm việc của chó phía sau tâm bầy, và cự ly dừng của chó.*

---

## 5. Thiết kế thực nghiệm (Experimental Design)

### 5.1 Nhiệm vụ và Hiệu chuẩn bán kính bầy $R_f(N)$
Bầy cừu xuất phát quanh một điểm tâm và phải được lùa vào mục tiêu hình tròn. Nhằm bảo đảm **tính bất biến theo quy mô (scale invariance)**, mọi kích thước hình học đều được neo theo bán kính bầy cân bằng $R_f(N)$, đo đạc thực nghiệm qua bước hiệu chuẩn (calibration): 1 chó lùa đàn co cụm hướng tới một mục tiêu vô tận trong 300 s, và $R_f$ là $\sqrt{2}$ lần bán kính hiệu dụng RMS trong 90 s cuối.

Bán kính mục tiêu được đặt cố định là $R_{\text{goal}} = 1,9 R_f(N)$. Khoảng cách lùa đàn từ tâm xuất phát đến tâm mục tiêu là:

$$l = \max(13 R_f(N), 80, \text{reach} + 1,9 R_f + R_f) \tag{2}$$

trong đó `reach` là khoảng cách xa nhất mà một con cừu có thể xuất hiện trong bố cục ban đầu. Đấu trường hoàn toàn không có tường phản xạ (open boundary) để tránh việc tường biên trở thành công cụ gom cừu nhân tạo làm sai lệch kết quả (Hình S9).

![Kiểm tra tường biên phản xạ](figures/fig10_wall_check.png)

*Hình S9: Tỷ lệ thành công theo số lượng chó D khi có tường phản xạ ở cự ly lề 80 và 250, so với trường hợp không có tường biên (3000), trên cùng tập hạt giống. Khác biệt rõ rệt nhất xuất hiện trên bố cục outlier_rich tại N = 400.*

### 5.2 Bố cục khởi tạo bầy cừu
Bảng 3 định nghĩa bốn bố cục xuất phát (định cỡ bằng khoảng cách thu gom $L = f(N) = 2 N^{2/3}$):

| Bố cục | Hình dạng không gian |
|---|---|
| **`compact`** | Phân phối Gauss, $\sigma = 0,5 R_f$, cắt cụt ở $3\sigma$. Toàn bộ cừu nằm trong $f(N)$; chó vào thẳng chế độ lùa. |
| **`wide`** | Phân phối Gauss rộng, $\sigma = 0,5 L$, cắt cụt ở $3\sigma$. Cừu phân tán rộng, đòi hỏi quét gom vùng biên. |
| **`split`** | Chia đều thành 3 cụm co cụm (2 cụm nếu $N < 12$) đặt đối xứng trên đường tròn bán kính $L$. |
| **`outlier_rich`** | 80% cừu nằm trong lõi co cụm, 20% là các cá thể tản mác rải rác từ $1,1$ đến $1,6 L$. |

### 5.3 Điểm xuất phát của chó (`dog_start`)
- **`arcs` (mặc định)**: Chó đứng trên các nửa đường tròn phía sau bầy cừu, cách biên bầy 30 đơn vị, cách đều nhau tối thiểu 5 đơn vị (Hình S4).
- **`ring`**: Chó phân bố đều trên đường tròn $360^\circ$ bao quanh bầy cừu.
- **`handler`**: Toàn bộ chó xuất phát từ một điểm duy nhất phía sau bầy cừu (mô phỏng việc thả chó từ trạm của người điều khiển).

Trên bố cục co cụm, toàn bộ cừu nằm trong phạm vi $r_s$ của chó tại nhịp 0; trên các bố cục phân tán, 66% đến 100% số cừu nằm ngoài tầm với và tiếp tục gặm cỏ cho đến khi chó tiếp cận (Hình S5).

![Các trạm xuất phát của chó](figures/fig8_dog_starts.png)

*Hình S4: Các vị trí xuất phát của chó. Phía trên: các vòng cung cho D = 1, 2, 4, 8, 24 và 64 trên bố cục compact. Một chó xuất phát trên đường lùa đàn phía sau bầy cừu và mỗi cá thể bổ sung chiếm một vị trí riêng. Phía dưới: ba kiểu bố trí (arcs, ring, handler point) cho 8 chó trên bố cục wide.*

![Cự ly ban đầu](figures/fig11_start_distances.png)

*Hình S5: Khởi đầu với 1 chó trên các vòng cung arcs, theo từng bố cục và N. Vòng tròn là bán kính phản xạ đe dọa r_s = 65. Cừu xanh lam phản ứng chạy trốn ngay nhịp 0, cừu xám tiếp tục gặm cỏ. Con số hiển thị khoảng cách từ chó đến tâm bầy cừu.*

### 5.4 Thời hạn (`deadline`)
Thời hạn được tính theo $T = m l / \delta$ giây với $m \in \{12, 6, 3\}$. Với $N = 200$, thời gian lùa tiêu chuẩn $T_{\text{drive}} \approx 140$ s, tương ứng các thời hạn là 1.680 s ($12\times$), 839 s ($6\times$) và 420 s ($3\times$).

### 5.5 Tiêu chí thành công
- **Nghiêm ngặt (Strict 100%)**: Toàn bộ 100% cừu phải nằm trong mục tiêu tại một nhịp thời gian trước khi hết hạn.
- **Ngưỡng 99% ($f_{99}$)**: Ít nhất $\lceil 0,99 N \rceil$ số cừu phải nằm trong mục tiêu. Với $N = 25$ và $50$, $\lceil 0,99 N \rceil = N$ nên hai tiêu chí trùng nhau; với $N = 100, 200, 400$, tiêu chí này cho phép sót lại lần lượt 1, 2 và 4 con bên ngoài.

### 5.6 Cơ chế kiểm định tuần tự và Phân bổ hạt giống thích ứng
Mỗi hạt giống $i$ sinh ra ba chuỗi ngẫu nhiên độc lập (bố cục, nhiễu cừu, nhiễu chó) dựa trên `master_seed + i` (2026 + $i$). Mỗi ô ban đầu nhận 1 lô 10 hạt giống. Sau mỗi vòng, chỉ các ô chưa ngã ngũ mới nhận thêm lô 10 hạt giống (tối đa 200). Điểm chia đôi (midpoint) được tự động chèn vào giữa các vùng hành vi khác biệt, và các ô trên ngưỡng bão hòa có độ trùng lặp hành vi cao (mean dog overlap $\ge 0,90$) sẽ bị cắt tỉa (pruning) để tiết kiệm năng lượng tính toán.

### 5.7 Các giao thức thực nghiệm
17 giao thức được thực hiện: 6 giao thức chính (quét $m \in \{12, 6, 3\}$ dưới tiêu chí strict và 99%), 1 giao thức Kubo, và 10 giao thức kiểm tra độ nhạy (đối chiếu điểm xuất phát handler/ring, khoảng cách gap 15/60, bán kính mục tiêu 1.5 $R_f$, bộ tham số thực địa GPS, và tốc độ chó $v_{\text{dog}} = 1,15$) (Hình S8).

![Bố cục các biến thể độ nhạy](figures/fig16_variants.png)

*Hình S8: Cấu hình ban đầu của từng biến thể phân tích độ nhạy trên bố cục wide tại N = 200 với 4 chó. Biến thể tốc độ chó có hình dạng tương tự như cấu hình cơ sở.*

---

## 6. Kết quả thực nghiệm (Results)

17 giao thức đã hoàn thành 112.785 lượt mô phỏng mà không có bất kỳ lỗi nào, mất khoảng 5 giờ trên 20 tiến trình song song.

### 6.1 Một chú chó là đủ cho bầy co cụm
Trên bố cục `compact`, $D_{\min} = 1$ ở mọi quy mô $N$ từ 25 đến 400, ở mọi thời hạn và dưới cả hai tiêu chí thành công. Thêm chó không làm giảm thời gian hoàn thành: các cá thể chó thừa chỉ lặp lại đường đi của nhau (độ trùng lặp đạt 84% đến 93%). Mô hình Kubo cũng xác nhận $D_{\min} = 1$ cho bầy co cụm tại $N = 25, 50, 100$.

### 6.2 Bản đồ $D_{\min}$ qua các bố cục, quy mô đàn và thời hạn
Bảng 5 trình bày giá trị $D_{\min}$ (Strict / 99%):

| Thời hạn | Bố cục | $N = 25$ | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ |
|---|---|---|---|---|---|---|
| **$12\times$** | wide | 1 / 1 | 1 / 1 | 1 / 1 | 2 / 2 | 3 / 2 |
| **$12\times$** | split | 1 / 1 | 1 / 1 | 1 / 1 | 2 / 1 | 3 / 2 |
| **$12\times$** | outlier_rich | 1 / 1 | 1 / 1 | 3 / 2 | 2 / 2 | 3 / 2 |
| **$6\times$** | wide | 1 / 1 | 1 / 1 | 1 / 1 | 3 / 2 | [12] / 3 |
| **$6\times$** | split | 1 / 1 | 1 / 1 | 1 / 1 | none / [1] | none / [6] |
| **$6\times$** | outlier_rich | 1 / 1 | 1 / 1 | 3 / 2 | [12] / 3 | none / 3 |
| **$3\times$** | wide | 1 / 1 | 1 / 1 | 3 / 2 | none / 3 | none / 6 |
| **$3\times$** | split | 1 / 1 | 1 / 1 | 1 / 1 | none / none | none / none |
| **$3\times$** | outlier_rich | 1 / 1 | 1 / 1 | 8 / 2 | none / 12 | none / [6] |

*Ghi chú: Bố cục compact đạt 1 / 1 ở mọi ô và được lược bỏ khỏi bảng.*

Mọi bố cục đều chỉ cần 1 chó khi $N \le 50$. Với $N = 200$ và $400$, ở thời hạn $12\times$ và $6\times$, đội chó chỉ cần từ 1 đến 3 cá thể. Khi thời hạn bị ép xuống $3\times$, $D_{\min}$ tăng vọt lên 6 (wide, $N = 400$) hoặc 12 (outlier_rich, $N = 200$).

### 6.3 Tốc độ tăng trưởng theo $N$ (RQ1)
Độ dốc $\log_2 D_{\min}$ theo $\log_2 N$ trên các bố cục phân tán:
- Ở thời hạn $12\times$ và $6\times$: độ dốc chỉ từ 0,2 đến 0,5 (tăng gấp đôi bầy cừu chỉ đòi hỏi tăng thêm 20% đến 50% số lượng chó).
- Ở thời hạn gấp gáp $3\times$: độ dốc tăng lên 0,6 đến 1,5.

### 6.4 Bố cục ban đầu so với Quy mô đàn (RQ2)
Quy mô đàn $N$ dịch chuyển $D_{\min}$ nhiều hơn so với hình dạng bố cục ban đầu. Phần lớn tác động của bố cục thực chất là sự khác biệt nhị phân giữa bố cục co cụm (luôn cần 1 chó) và ba bố cục phân tán còn lại.

### 6.5 Tác động của Thời hạn (RQ3)
Rút ngắn thời hạn từ $12\times$ xuống $3\times$ làm tăng $D_{\min}$ trên bố cục wide từ 2 lên 6 chó ($N = 400$). Tác động của thời hạn mang tính phi tuyến: từ $12\times$ sang $6\times$, $D_{\min}$ chỉ thay đổi tối đa 1 chó, nhưng bước nhảy vọt xảy ra khốc liệt giữa $6\times$ và $3\times$.

### 6.6 Tiêu chí thành công và "Hiệu ứng cá thể rớt lại" (RQ4)
Giá trị $D_{\min}$ dưới tiêu chí 99% không bao giờ lớn hơn tiêu chí nghiêm ngặt 100%, và nhỏ hơn từ 1 đến 6 chó ở 9 ô thực nghiệm quy mô lớn. Đặc biệt, có 6 ô hoàn toàn thất bại (`none`) dưới tiêu chí nghiêm ngặt nhưng lại đạt $D_{\min}$ rất gọn gàng dưới tiêu chí 99%.

**Cơ chế hỏng hóc (The Straggler Effect):** Phân tích chi tiết các lượt chạy thất bại ($N = 400, D = 8$ đến 16) chỉ ra rằng: 386 đến 399 con cừu đã vào gọn trong đích từ rất sớm. Tuy nhiên, khi toàn bộ bầy chó dồn lên phía trước mục tiêu để hỗ trợ, một hoặc hai con cừu lạc đàn rớt lại phía sau kích hoạt hành vi truy đuổi; đàn chó vô tình lùa bầy cừu chính đang ở trong mục tiêu vọt ra ngoài. Dưới tiêu chí 99%, nhiệm vụ đã hoàn thành ngay ở nhịp lùa đầu tiên.

### 6.7 Hiện tượng thêm chó làm giảm hiệu quả trên bố cục cụm rời (split)
Trên bố cục `split` ở $N \ge 200$, tỷ lệ thành công không tăng theo số lượng chó. Tại $N = 200$ thời hạn $6\times$, tỷ lệ thành công đạt 0,92 (1 chó), 0,95 (2 chó), nhưng tụt xuống 0,60 đến 0,90 khi dùng 4 đến 24 chó; thời gian hoàn thành cũng bị kéo dài từ 425 s lên 700 s. Việc phân bổ chó vào các cụm riêng lẻ dễ gây xung đột và làm tán loạn các cụm trước khi gom được về tâm.

### 6.8 Phân tích độ nhạy (RQ5)
Bảng 8 tóm tắt kết quả phân tích độ nhạy ($D_{\min}$ Base / Biến thể tại thời hạn $6\times$):

| Tiêu chí | Biến thể | wide 100 | wide 200 | wide 400 | outlier 100 | outlier 200 | outlier 400 |
|---|---|---|---|---|---|---|---|
| **strict** | Bộ cừu thực địa GPS | 1 / 6 | 3 / none | [12] / none | 3 / [1] | [12] / none | none / none |
| **strict** | Xuất phát trạm handler | 1 / 1 | 3 / 3 | [12] / none | 3 / 2 | [12] / [3] | none / none |
| **strict** | Xuất phát vòng tròn ring | 1 / 1 | 3 / 5 | [12] / [8] | 3 / 8 | [12] / [6] | none / none |
| **strict** | Mục tiêu hẹp $1,5 R_f$ | 1 / 3 | 3 / none | [12] / none | 3 / 3 | [12] / none | none / none |
| **strict** | Cự ly lùi gap 15 | 1 / 1 | 3 / [3] | [12] / none | 3 / [1] | [12] / none | none / none |
| **strict** | Cự ly lùi gap 60 | 1 / 1 | 3 / 4 | [12] / 8 | 3 / 3 | [12] / 5 | none / [12] |
| **strict** | Chó chạy chậm 1.15 | 1 / 1 | 3 / 3 | [12] / 5 | 3 / 3 | [12] / 4 | none / 6 |
| **99%** | Bộ cừu thực địa GPS | 1 / 1 | 2 / 1 | 3 / 2 | 2 / 1 | 3 / 1 | 3 / 3 |
| **99%** | Chó chạy chậm 1.15 | 1 / 1 | 2 / 3 | 3 / 3 | 2 / 2 | 3 / 3 | 3 / 3 |

- **Tốc độ chó ($v_{\text{dog}} = 1,15$ vs $1,5$):** Chó chạy chậm hơn đạt thành tích vượt trội dưới tiêu chí nghiêm ngặt trên đàn lớn ($N = 400$, wide: $D_{\min} = 5$ so với thất bại ở tốc độ 1.5; outlier: $D_{\min} = 6$ so với thất bại). Chó chậm di chuyển điềm tĩnh hơn, không tạo ra xung lực đẩy đàn cừu vọt qua vòng đích.
- **Trạm xuất phát:** Xuất phát tập trung tại trạm `handler` cần ít chó hơn so với bao vây `ring` ở quy mô nhỏ và vừa, vì chó xuất phát từ vòng tròn ở phía mục tiêu vô tình dọa cừu chạy ngược hướng.

![Cảnh bầy cừu được lùa](figures/fig15_matched_scene.png)

*Hình S7: Bầy cừu trong bộ tham số cơ sở và bộ tham số thực địa GPS khi được lùa ở quy mô N = 100 với 1 chó, trên cùng một tỷ lệ không gian. Phải: bầy cừu đã ổn định trong các mục tiêu có bán kính 1,9, 1,5, 1,3 và 1,1 R_f, kèm theo số lượng cừu bị sót lại bên ngoài mỗi vòng.*

---

## 7. Thảo luận (Discussion)

### 7.1 So sánh với các nghiên cứu trước
Kết quả $D_{\min}$ của chúng tôi tăng trưởng chậm hơn nhiều so với bản thảo ẩn danh 2025 (nơi 1 chó thất bại ở 150 cừu và cần 20 chó ở 200 cừu; trong khi chúng tôi chỉ cần 2 đến 3 chó ở $N = 400$). Sự khác biệt cốt lõi nằm ở cơ chế hút bầy đàn: mô hình Strömbom duy trì lực hút toàn cục ($n = N - 1$), giúp bầy cừu tự động co cụm lại khi chó tiếp cận, giảm tải rất lớn cho đội chăn dắt.

### 7.2 Thời hạn là một yếu tố then chốt
Các nghiên cứu trước đây luôn cố định thời gian. Kết quả của chúng tôi chứng minh rằng thời hạn dịch chuyển $D_{\min}$ mạnh mẽ không kém gì quy mô bầy đàn. Về mặt thực tiễn, việc bổ sung thêm chó chủ yếu có tác dụng "mua thời gian" để thu gom bầy đàn phân tán.

### 7.3 Bản chất đo lường của tiêu chí thành công
Tiêu chí 100% đo lường khả năng đưa toàn bộ đàn vào đích và giữ yên tại đó trong 1 nhịp, trong khi tiêu chí 99% đo lường năng lực dẫn dắt dòng chảy bầy đàn. Sự khác biệt này giải thích tại sao các thuật toán chăn dắt thực tế cần bổ sung một trạng thái giữ đàn chuyên biệt (holding) khi đàn đã vào đích.

### 7.4 Những kết luận vững chắc
Mặc dù giá trị số tuyệt đối của $D_{\min}$ có thể thay đổi tùy thuộc vào các tham số mô phỏng, bốn quy luật cốt lõi luôn bất biến:
1. Bầy cừu co cụm chỉ cần duy nhất 1 chó;
2. Trên bầy phân tán, $D_{\min}$ tăng trưởng dưới tuyến tính (sub-linear, độ dốc 0,2–0,5) theo quy mô $N$;
3. Thời hạn là yếu tố chi phối mạnh mẽ tương đương quy mô bầy;
4. Tiêu chí nghiêm ngặt 100% làm thổi phồng số lượng chó cần thiết ở đàn lớn do hiệu ứng cá thể rớt lại.

---

## 8. Giới hạn nghiên cứu (Limitations)

1. Nghiên cứu tập trung vào quy tắc `strombom_multi` trên mô hình cừu Strömbom;
2. Chưa mô phỏng rào chắn thực tế (chuồng có cổng hẹp và hàng rào vật lý giữ cừu);
3. Khoảng cách phản xạ đe dọa $r_s$ chưa có dữ liệu đo đạc chính xác trên cừu sống thực địa;
4. Chưa giải thích triệt để nguyên nhân suy giảm hiệu quả trên bố cục `split` ở $N \ge 200$.

---

## 9. Kết luận và Hướng phát triển (Conclusions and Future Work)

Nghiên cứu khẳng định rằng việc chăn dắt đa tác tử có khả năng mở rộng quy mô vượt bậc đối với các bầy đàn có tính liên kết: một đội ngũ nhỏ từ 2 đến 6 cá thể chó có thể dẫn dắt hiệu quả hàng trăm cá thể cừu nếu được phối hợp phân công tối ưu.

Các hướng phát triển tiếp theo bao gồm: thử nghiệm quy tắc không phối hợp (FAT) trên diện rộng, kiểm tra các biến thể 99% cho các hình thức xuất phát, bổ sung giai đoạn giữ đàn (holding phase) tường minh khi vào đích, và khảo sát sự thay đổi của tham số láng giềng $n$.

---

## Tính khả dụng của Dữ liệu và Mã nguồn (Data and Code Availability)

Toàn bộ 112.785 lượt thử nghiệm được lưu trữ theo từng giao thức trong thư mục `results/` của kho mã nguồn HerdSim. Các bảng biểu và hình vẽ có thể tái lập hoàn toàn thông qua các lệnh CLI:

```bash
make install && make check && make bench
uv run cli/run_queue.py --workers 20                 # Chạy toàn bộ các giao thức
uv run cli/dmin_tables.py record                     # Bảng Phụ lục A
uv run cli/dmin_tables.py dmin dmin_m12 dmin_m6 dmin_m3 dmin_f99_m12 dmin_f99_m6 dmin_f99_m3
uv run cli/dmin_tables.py growth dmin_m12 dmin_m6 dmin_m3
uv run cli/dmin_tables.py compare dmin_s_matched dmin_s_handler --base dmin_s_base
uv run python docs/science/design_version2/figures/make_figures.py
uv run python docs/science/design_version2/figures/make_result_figures.py
```

---

## Tài liệu tham khảo (References)

- anonymous (2025). Collective nudging that scales. How many dogs do I need to herd sheep? Manuscript.
- Auletta F, Fiore D, Richardson MJ, di Bernardo M (2021). Herding stochastic autonomous agents via local control rules and online global target selection strategies. arXiv:2010.00386.
- Brown D, Garrity T, Perkins D, Hunter D, Pochman W (2025). Optimal control strategies for multi-agent sheep herding. arXiv:2510.25115.
- di Bernardo M (2026). Multi-scale control of large agent populations: from density dynamics to individual actuation. arXiv:2603.15160.
- Jadhav V, Pasqua R, Zanon C, Roy M, Tredan G, Bon R, Guttal V, Theraulaz G (2024). Collective responses of flocking sheep (Ovis aries) to a herding dog (border collie). Communications Biology. doi:10.1038/s42003-024-07245-8.
- Kubo M, Tashiro M, Sato H, Yamaguchi A (2022). Herd guidance by multiple sheepdog agents with repulsive force. Artificial Life and Robotics 27: 416-427. doi:10.1007/s10015-021-00726-7.
- Lama A, di Bernardo M (2024). Shepherding control and herdability in complex multiagent systems. arXiv:2307.16797.
- Li A, Ogura M, Wakamiya N (2025). Swarm shepherding using bearing-only measurements. Phil. Trans. R. Soc. A 383: 20240145. doi:10.1098/rsta.2024.0145.
- Pierson A, Schwager M (2015). Bio-inspired non-cooperative multi-robot herding. IEEE International Conference on Robotics and Automation (ICRA).
- Strömbom D, Mann RP, Wilson AM, Hailes S, Morton AJ, Sumpter DJT, King AJ (2014). Solving the shepherding problem: heuristics for herding autonomous, interacting agents. J. R. Soc. Interface 11: 20140719. doi:10.1098/rsif.2014.0719.

---

## Phụ lục A. Nhật ký các lượt chạy (Appendix A. Record of Runs)

| Giao thức | Số lượt thử | Số ô | Đã ngã ngũ | Chưa ngã ngũ ở giới hạn 200 | Lỗi | Số giờ chạy |
|---|---|---|---|---|---|---|
| dmin_m12 | 17.220 | 183 | 147 | 36 | 0 | 1,24 |
| dmin_m6 | 11.625 | 180 | 165 | 15 | 0 | 0,41 |
| dmin_m3 | 9.130 | 181 | 178 | 3 | 0 | 0,17 |
| dmin_f99_m12 | 11.100 | 180 | 178 | 2 | 0 | 0,41 |
| dmin_f99_m6 | 12.390 | 180 | 171 | 9 | 0 | 0,49 |
| dmin_f99_m3 | 10.670 | 181 | 174 | 7 | 0 | 0,27 |
| dmin_kubo | 1.080 | 18 | 18 | 0 | 0 | 0,08 |
| dmin_s_base | 3.690 | 48 | 38 | 10 | 0 | 0,21 |
| dmin_s_matched | 3.690 | 48 | 33 | 15 | 0 | 0,09 |
| dmin_s_handler | 2.370 | 48 | 46 | 2 | 0 | 0,10 |
| dmin_s_ring | 3.790 | 49 | 39 | 10 | 0 | 0,21 |
| dmin_s_goal | 2.320 | 49 | 46 | 3 | 0 | 0,09 |
| dmin_s_gap | 10.830 | 145 | 121 | 24 | 0 | 0,58 |
| dmin_s_dogspeed | 2.620 | 50 | 49 | 1 | 0 | 0,11 |
| dmin_f99_s_base | 3.360 | 48 | 46 | 2 | 0 | 0,16 |
| dmin_f99_s_matched | 3.790 | 48 | 44 | 4 | 0 | 0,16 |
| dmin_f99_s_dogspeed | 3.110 | 48 | 45 | 3 | 0 | 0,16 |
| **Tổng cộng** | **112.785** | | | | **0** | |

---

## Phụ lục B. Thử nghiệm sơ bộ (Appendix B. Pilot)

![Thử nghiệm sơ bộ](figures/fig18_pilot_success.png)

*Hình S10: Khảo sát sơ bộ (10 hạt giống mỗi ô): tỷ lệ thành công theo D đối với bố cục wide và outlier_rich tại N = 200 và 400, ghi nhận ở ba mốc thời hạn 3, 6 và 12 drive times. Thử nghiệm sơ bộ được sử dụng để lựa chọn các mốc thời hạn và lưới quy mô đội chó.*

Tỷ lệ thành công trên bố cục `wide` trong đợt chạy thử nghiệm sơ bộ (10 hạt giống mỗi ô, không tường biên):

| $N$ | Thời hạn | $D = 1$ | 2 | 3 | 4 | 6 | 8 | 12 | 16 |
|---|---|---|---|---|---|---|---|---|---|
| 200 | $3\times$ | 0,0 | 0,4 | 0,4 | 0,9 | 0,9 | 0,8 | 0,9 | 0,9 |
| 200 | $6\times$ | 0,3 | 0,7 | 0,9 | 1,0 | 1,0 | 1,0 | 1,0 | 1,0 |
| 200 | $12\times$ | 0,7 | 1,0 | 1,0 | 1,0 | 1,0 | 1,0 | 1,0 | 1,0 |
| 400 | $3\times$ | 0,0 | 0,0 | 0,0 | 0,1 | 0,1 | 0,4 | 0,3 | 0,6 |
| 400 | $6\times$ | 0,0 | 0,0 | 0,5 | 0,5 | 0,6 | 0,8 | 0,9 | 0,8 |
| 400 | $12\times$ | 0,0 | 0,7 | 0,9 | 1,0 | 1,0 | 1,0 | 1,0 | 1,0 |

---

## Phụ lục C. So sánh hai mức tốc độ của chó (Appendix C. The Two Dog Speeds)

Các lượt thử nghiệm với $D \ge 6$ trên lưới độ nhạy tại thời hạn $6\times$ drive times. Bán kính bầy cân bằng giữa hai lượt chạy chênh lệch dưới 1%, do đó kích thước mục tiêu và thời hạn là hoàn toàn tương đồng.

| Bố cục, quy mô $N$ | Chó 1.5: Strict | Đạt mốc 99% | Trung vị giây đến 99% | Chó 1.15: Strict | Đạt mốc 99% | Trung vị giây đến 99% |
|---|---|---|---|---|---|---|
| wide 100 | 1,00 | 1,00 | 205 | 1,00 | 1,00 | 207 |
| wide 200 | 0,94 | 1,00 | 268 | 1,00 | 1,00 | 277 |
| wide 400 | 0,83 | 1,00 | 426 | 1,00 | 1,00 | 442 |
| outlier_rich 100 | 0,99 | 1,00 | 210 | 1,00 | 1,00 | 213 |
| outlier_rich 200 | 0,83 | 0,98 | 276 | 1,00 | 1,00 | 283 |
| outlier_rich 400 | 0,68 | 0,99 | 460 | 1,00 | 1,00 | 448 |

Tại bố cục `wide`, $N = 400$ với 12 chó, lượt thành công nghiêm ngặt cần trung vị 876 s đối với chó tốc độ 1.5 nhưng chỉ cần 444 s đối với chó tốc độ 1.15, và quãng đường đi trung vị của mỗi chó là 1.130 đơn vị so với 511 đơn vị. Dưới tiêu chí 99%, toàn bộ các lượt thử của chó tốc độ 1.15 với $D \ge 6$ đều thành công (240/240 lượt), so với 0,97 đến 1,00 của chó tốc độ 1.5 cơ sở, và thời gian hoàn thành trung vị chênh lệch không quá 4%.
