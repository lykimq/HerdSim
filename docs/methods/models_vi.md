# Mô hình Tác tử và Thuật toán Phối hợp Đa Chó

Tài liệu này trình bày chi tiết công thức toán học, cơ sở sinh học và thuật toán điều khiển của các tác tử cừu và chó trong **HerdSim**.

HerdSim kết nối giữa nghiên cứu hành vi động vật thực nghiệm (qua dữ liệu vòng đeo GPS) với hệ thống đa tác tử tự hành (Autonomous Multi-Agent Systems). Phần mềm mô hình hóa các tập tính cá thể của cừu và phát triển các thuật toán mở rộng giúp đội chó chăn cừu phối hợp nhịp nhàng, chia sẻ mục tiêu và tránh va chạm.

---

## Mục lục

- [1. Mô hình Tập tính Bầy cừu](#1-mô-hình-tập-tính-bầy-cừu)
  - [Mô hình hành vi rời rạc Strömbom et al. (2014)](#mô-hình-hành-vi-rời-rạc-strömbom-et-al-2014)
  - [Chuẩn hóa tổng lực đẩy từ nhiều chó (Cải tiến của HerdSim)](#chuẩn-hóa-tổng-lực-đẩy-từ-nhiều-chó-cải-tiến-của-herdsim)
  - [Mô hình trường lực thế liên tục Kubo et al. (2022)](#mô-hình-trường-lực-thế-liên-tục-kubo-et-al-2022)
  - [Mô hình mục tiêu Brownian không liên kết Lama (2024)](#mô-hình-mục-tiêu-brownian-không-liên-kết-lama-2024)
- [2. Các Bộ điều khiển Chó chăn cừu](#2-các-bộ-điều-khiển-chó-chăn-cừu)
  - [Đội hình phối hợp tự hành: `strombom_multi`](#đội-hình-phối-hợp-tự-hành-strombom_multi)
  - [Mô hình đối chứng tham lam: `fat` (Farthest-Agent Targeting)](#mô-hình-đối-chứng-tham-lam-fat-farthest-agent-targeting)
  - [Mô hình chó độc lập: `independent`](#mô-hình-chó-độc-lập-independent)
  - [Mô hình lực liên tục: `kubo`](#mô-hình-lực-liên-tục-kubo)
- [Tài liệu tham khảo](#tài-liệu-tham-khảo)

---

## 1. Mô hình Tập tính Bầy cừu

### Mô hình hành vi rời rạc Strömbom et al. (2014)

Dựa trên dữ liệu định vị GPS tần số cao thu được từ các đàn cừu thực tế bị rượt đuổi bởi chó chăn cừu giống Border Collie ([Strömbom et al. 2014](https://doi.org/10.1098/rsif.2014.0719)), các nhà khoa học nhận thấy cừu không có một kế hoạch tổng thể phức tạp. Thay vào đó, mỗi cá thể cừu $i$ tự cân bằng **5 bản năng sinh học cạnh tranh nhau** tại mỗi bước thời gian rời rạc ($t \to t+1$, với 1 tick = 1 giây).

![Cơ chế phối hợp đa chó](../../docs/figures/fig3_team_rule.png)
*Hình 1: Tương tác giữa cừu và chó. Cừu chuyển đổi giữa trạng thái gặm cỏ bình yên và chạy trốn chủ động dựa trên khoảng cách tới chó. Khi chạy trốn, cừu tổng hợp các lực: tránh va chạm với bạn cùng bầy, lực hút bầy đàn, quán tính di chuyển, lực chạy trốn kẻ săn mồi và nhiễu ngẫu nhiên.*

#### Trạng thái chạy trốn chủ động (Khoảng cách tới chó $< r_s$)

Khi bất kỳ chú chó nào tiến vào cự ly đe dọa $r_s = 65\text{ m}$ (tầm nhìn phát hiện nguy hiểm tự nhiên của loài cừu), cừu $i$ phát hiện mối đe dọa và chuyển sang **trạng thái chạy trốn chủ động**. Hướng di chuyển mong muốn $\mathbf{H}_i'$ được tính bằng tổng có trọng số của 5 vector đơn vị:

$$\mathbf{H}_i' = h\,\mathbf{H}_i + c\,\mathbf{C}_i + \rho_a\,\mathbf{R}_{a,i} + \rho_s\,\mathbf{R}_{s,i} + e\,\mathbf{\epsilon}_i$$

1. **Quán tính di chuyển ($\mathbf{H}_i$, trọng số $h = 0.5$)**:
   - *Tại sao?* Động vật có khối lượng cơ thể nên không thể đổi hướng đột ngột ngay tức khắc.
   - Vector: Hướng chuyển động từ bước thời gian trước đó:
     $$\mathbf{H}_i = \frac{\mathbf{x}_i^t - \mathbf{x}_i^{t-1}}{\lVert \mathbf{x}_i^t - \mathbf{x}_i^{t-1} \rVert}$$

2. **Lực hút gắn kết xã hội ($\mathbf{C}_i$, trọng số $c = 1.05$)**:
   - *Tại sao?* An toàn nhờ số đông. Một con cừu đứng tách biệt luôn cảm thấy bất an và có xu hướng tự nhiên muốn lao về phía trung tâm đàn.
   - Vector: Hướng từ vị trí cừu $\mathbf{x}_i$ tới Trọng tâm Cục bộ ($\mathrm{LCM}_i$) của $n$ cá thể láng giềng gần nhất:
     $$\mathbf{C}_i = \frac{\mathrm{LCM}_i - \mathbf{x}_i}{\lVert \mathrm{LCM}_i - \mathbf{x}_i \rVert}, \quad \text{với } \mathrm{LCM}_i = \frac{1}{n} \sum_{k \in \mathcal{N}_n(i)} \mathbf{x}_k$$
   - Trong mô hình chuẩn, $n = N - 1$ (tương tác với toàn bộ thành viên trong đàn).

3. **Tránh va chạm ($\mathbf{R}_{a,i}$, trọng số $\rho_a = 2.0$)**:
   - *Tại sao?* Động vật ưu tiên việc không giẫm đạp hay húc vào nhau lên hàng đầu. Do đó, lực này mang trọng số cao nhất ($\rho_a = 2.0$).
   - Bất kỳ cá thể láng giềng $j$ nào ở cự ly gần hơn không gian cá nhân $r_a = 2\text{ m}$ sẽ tạo ra một lực đẩy né tránh:
     $$\mathbf{R}_{a,i} = \frac{\sum_{j \ne i, \lVert \mathbf{x}_i - \mathbf{x}_j \rVert < r_a} \frac{\mathbf{x}_i - \mathbf{x}_j}{\lVert \mathbf{x}_i - \mathbf{x}_j \rVert}}{\left\lVert \sum_{j \ne i, \lVert \mathbf{x}_i - \mathbf{x}_j \rVert < r_a} \frac{\mathbf{x}_i - \mathbf{x}_j}{\lVert \mathbf{x}_i - \mathbf{x}_j \rVert} \right\rVert}$$

4. **Trốn chạy kẻ săn mồi ($\mathbf{R}_{s,i}$, trọng số $\rho_s = 1.0$)**:
   - Lực đẩy trực tiếp tránh xa những chú chó đang nằm trong cự ly đe dọa $r_s = 65\text{ m}$. (Xem cơ chế gộp lực bên dưới).

5. **Nhiễu hành vi ngẫu nhiên ($\mathbf{\epsilon}_i$, trọng số $e = 0.3$)**:
   - Mô phỏng sự bất định và giác quan không hoàn hảo của cá thể. $\mathbf{\epsilon}_i$ là vector đơn vị có góc định hướng phân bố đều ngẫu nhiên trong $[0, 2\pi)$.

#### Cập nhật vị trí
Tại mỗi giây ($1\text{ tick}$), cừu $i$ tiến về phía trước một khoảng $\delta = 1\text{ m}$ theo hướng chuyển động chuẩn hóa:

$$\mathbf{x}_i^{t+1} = \mathbf{x}_i^t + \delta\,\frac{\mathbf{H}_i'}{\lVert \mathbf{H}_i' \rVert}$$

Quy tắc này giới hạn vận tốc tối đa của cừu ở mức $1.0\text{ m/s}$.

#### Trạng thái gặm cỏ (Khoảng cách tới chó $\ge r_s$)
Khi tất cả chó ở xa hơn $r_s = 65\text{ m}$, đàn cừu cảm thấy an toàn và chuyển sang **gặm cỏ**: 95% thời gian chúng đứng yên, và 5% thời gian ($p = 0.05$) chúng bước một bước ngẫu nhiên:

$$\mathbf{x}_i^{t+1} = \begin{cases} \mathbf{x}_i^t + \delta\,\mathbf{\epsilon}_{\mathrm{graze}}, & \text{với xác suất } 0.05 \\ \mathbf{x}_i^t, & \text{với xác suất } 0.95 \end{cases}$$

---

### Chuẩn hóa tổng lực đẩy từ nhiều chó (Cải tiến của HerdSim)

Mô hình gốc năm 2014 của Strömbom chỉ được thiết kế cho **duy nhất một chú chó**. Nếu chúng ta cộng dồn lực đẩy độc lập của $D = 4$ hay $8$ chú chó một cách ngây thơ, tổng lực sợ hãi sẽ bị nhân lên gấp 8 lần, hoàn toàn áp đảo lực gắn kết xã hội ($c = 1.05$) và xé toạc đàn cừu thành nhiều mảnh hỗn loạn.

HerdSim giải quyết triệt để vấn đề này bằng cách **cộng vector và chuẩn hóa về độ dài đơn vị**:

$$\mathbf{R}_{s,i} = \frac{\sum_{j \in \mathrm{threat}} \frac{\mathbf{x}_i - \mathbf{y}_j}{\lVert \mathbf{x}_i - \mathbf{y}_j \rVert}}{\left\lVert \sum_{j \in \mathrm{threat}} \frac{\mathbf{x}_i - \mathbf{y}_j}{\lVert \mathbf{x}_i - \mathbf{y}_j \rVert} \right\rVert}$$

với $\mathrm{threat} = \{j \mid \lVert \mathbf{x}_i - \mathbf{y}_j \rVert < r_s\}$.

#### Ví dụ trực quan về thế gọng kìm (Flanking)
Giả sử một con cừu ở tọa độ $(0, 5)$ đang bị kẹp giữa hai chú chó: Chó 1 ở $(-3, 0)$ (sau-trái) và Chó 2 ở $(3, 0)$ (sau-phải):
- Chó 1 đẩy cừu tiến lên phía trước và lệch sang phải $(+x, +y)$.
- Chó 2 đẩy cừu tiến lên phía trước và lệch sang trái $(-x, +y)$.
- Phép cộng vector triệt tiêu hai lực đẩy ngang sang hai bên, nhưng lại cộng dồn lực đẩy thẳng về phía trước.
- Phép chuẩn hóa đưa độ lớn lực sợ hãi trở lại đúng độ dài đơn vị tiêu chuẩn ($\lVert \mathbf{R}_{s,i} \rVert = 1.0$). Nhờ đó, cừu bị hướng thẳng về phía trước một cách tự nhiên mà không bị tăng áp lực sợ hãi phi lý.

---

### Mô hình trường lực thế liên tục Kubo et al. (2022)

Để kiểm chứng chéo trên một trường phái vật lý hoàn toàn khác, HerdSim tích hợp mô hình lực liên tục của [Kubo et al. (2022)](https://doi.org/10.1007/s10015-021-00726-7). Thay vì máy trạng thái rời rạc, các tác tử chuyển động dưới các trường thế nhân tạo trơn tru:

![Mô hình lực liên tục Kubo](../../docs/figures/fig5_kubo.png)
*Hình 2: Mô hình trường lực Kubo et al. (2022). Trái: Các lực tác dụng lên cừu (đẩy tránh va chạm, hút bầy, né chó, đồng bộ vận tốc). Giữa: Các lực tác dụng lên chó (hút về cừu xa nhất, né bờ chuồng, lực đẩy tương hỗ giữa các chó). Phải: Mô phỏng lực đẩy tương hỗ giúp các chú chó tự động tản đều tạo thành vòng cung lùa bầy.*

- **Lực tác dụng lên cừu Kubo**:
  1. Lực đẩy va chạm giữa cừu với nhau ($1/r^2$).
  2. Lực đồng bộ vận tốc với láng giềng.
  3. Lực hút xã hội về trọng tâm láng giềng ($-1/r$).
  4. Lực trốn chạy chó ($1/r^3$).
- **Điểm khác biệt chính so với Strömbom**:
  - Trong Kubo, việc thêm nhiều chó giúp đẩy nhanh thời gian lùa ngay cả trên đàn tập trung (từ $\sim 115\text{ s}$ với 1 chó xuống $29\text{ s}$ với 10 chó) do lực đẩy là hàm liên tục phụ thuộc phi tuyến vào khoảng cách.
  - Cừu Kubo chỉ tương tác trong bán kính cố định $20\text{ m}$, do đó bắt buộc phải xuất phát ở dạng tập trung (`compact`).

---

### Mô hình mục tiêu Brownian không liên kết Lama (2024)

HerdSim tích hợp mô hình từ bài báo của [Lama & di Bernardo (2024)](https://doi.org/10.1103/PhysRevResearch.6.L032012):
- **Mục tiêu (đóng vai trò "cừu")**: Các hạt chuyển động nhiệt Brownian ngẫu nhiên, **hoàn toàn không có lực gắn kết bầy đàn** và không đồng bộ vận tốc.
- **Tác dụng của người lùa**: Khi người lùa lại gần hơn cự ly $\lambda = 2.5$, mục tiêu bị đẩy ra xa với cường độ giảm tuyến tính về 0 ở khoảng cách $\lambda$.
- **Mục đích**: Cung cấp một hệ quy chiếu thực nghiệm để so sánh động lực học giữa các sinh vật có tính xã hội (bầy cừu) với các tập hợp hạt ngẫu nhiên rời rạc (kiểm chứng định luật tỷ lệ $D \propto \sqrt{N}$).

---

## 2. Các Bộ điều khiển Chó chăn cừu

HerdSim hiện thực 4 kiến trúc điều khiển chó chăn cừu:

```text
Các bộ điều khiển chó
├── strombom_multi   (Đội hình phối hợp tự hành: Hungarian matching + vòng cung lùa)
├── fat              (Đối chứng tham lam không phối hợp: Farthest-Agent Targeting)
├── independent      (Các cá thể độc lập: máy trạng thái nhưng không có tầng phối hợp đội)
└── kubo_forces      (Trường thế vật lý liên tục với lực đẩy tương hỗ giữa các chó)
```

---

### Đội hình phối hợp tự hành: `strombom_multi`

Mở rộng các quy tắc kinh nghiệm của Strömbom thành một đội đa tác tử tự hành, có ý thức tránh va chạm:

#### 1. Ngưỡng phát hiện cá thể lạc đàn ($f(N) = r_a N^{2/3}$)
- *Tại sao là $r_a N^{2/3}$?* Khi xếp chặt các hình tròn bán kính $r_a$ trong mặt phẳng 2D, bán kính cụm tăng theo $\sim N^{1/2}$. Trong không gian 3D, bán kính tăng theo $\sim N^{1/3}$. Trên đồng cỏ mở, cừu phân tán theo cụm dạng fractal tự nhiên, nên biên giới tự nhiên nơi một cá thể bị xem là "lạc đàn" tăng theo hàm $N^{2/3}$.
- Nếu có bất kỳ con cừu nào nằm xa hơn $f(N)$ tính từ Trọng tâm Toàn cục ($\mathrm{GCM} = \frac{1}{N} \sum_k \mathbf{x}_k$), bầy cừu được xem là bị phân tán, kích hoạt **Chế độ Gom cừu lạc (Outlier Collection Mode)**.

#### 2. Phân công mục tiêu gom bằng thuật toán Hungarian
- Đối với mỗi con cừu lạc $o$, điểm gom $P_c$ được đặt sau lưng con cừu $r_a = 2\text{ m}$ theo hướng chiếu từ trọng tâm bầy:
  $$P_c = \mathbf{x}_o + r_a \frac{\mathbf{x}_o - \mathrm{GCM}}{\lVert \mathbf{x}_o - \mathrm{GCM} \rVert}$$
- $D$ con cừu lạc xa nhất được phân công tương ứng 1-đối-1 cho $D$ chú chó sẵn sàng thông qua thuật toán Hungarian (`scipy.optimize.linear_sum_assignment`). Thuật toán này tối thiểu hóa tổng quãng đường chạy của toàn đội và ngăn ngừa tình trạng các chú chó chạy chéo đường cắt mặt nhau. Chó dư thừa sẽ tham gia đội hình lùa phía sau.

#### 3. Đội hình Vòng cung lùa đàn ($P_d$)
- Khi toàn bộ cừu đã nằm gọn trong phạm vi $f(N)$, bầy cừu đã gắn kết, các chú chó đồng loạt chuyển sang **Chế độ Lùa đàn (Drive Mode)**.
- Điểm lùa danh định $P_d$ được đặt sau lưng đàn cừu dọc theo trục thẳng hướng về đích:
  $$P_d = \mathrm{GCM} + r_a \sqrt{N} \frac{\mathrm{GCM} - \mathbf{x}_{\mathrm{goal}}}{\lVert \mathrm{GCM} - \mathbf{x}_{\mathrm{goal}} \rVert}$$
- *Tại sao khoảng cách lùa tỷ lệ với $r_a \sqrt{N}$?* Một đàn cừu gắn kết gồm $N$ con tạo thành một hình đĩa có bán kính tỷ lệ thuận với $r_a\sqrt{N}$. Khoảng cách này đảm bảo đàn chó đứng ngay sát phía sau rìa mép của bầy cừu.
- Các chú chó dàn đều trên một vòng cung bán kính $R$ ôm trọn góc mở của đàn cừu ($\pm \arcsin(R_{\mathrm{flock}} / R)$). Thứ tự góc cực của các chú chó quanh bầy được cố định, đảm bảo không chú chó nào chen lấn hay cắt ngang đường chạy của đồng đội.

#### 4. Vận tốc và Quy tắc Giữ khoảng cách an toàn (Standoff Rule)
- **Vận tốc**: $v_{\mathrm{dog}} = 1.5\text{ m/s}$ (nhanh gấp 1.5 lần cừu, đúng theo tỷ lệ thực tế giữa chó chăn cừu Border Collie và cừu).
- **Quy tắc Giữ khoảng cách an toàn**: Nếu một chú chó tiến gần hơn $3 r_a = 6\text{ m}$ tới bất kỳ con cừu nào, nó lập tức dừng bước ($\mathbf{v}_{\mathrm{dog}} = 0$) để tránh làm cừu hoảng loạn dẫn đến giẫm đạp lẫn nhau.

---

### Mô hình đối chứng tham lam: `fat` (Farthest-Agent Targeting)

Bộ điều khiển **FAT** được thiết kế để kiểm chứng xem khả năng phối hợp đồng đội có thực sự cần thiết hay không:
- **Quy tắc**: Mỗi chú chó tự động tìm con cừu nào đang xa đích nhất và lao thẳng tới vị trí cách sau lưng nó $r_a$.
- **Điểm khiếm khuyết**: Hoàn toàn không có thuật toán Hungarian, không có vòng cung lùa, không có giao tiếp và không tránh va chạm giữa các chú chó.

![FAT clumping](../../docs/figures/fig4_fat.png)
*Hình 3: Hiện tượng co cụm của thuật toán FAT. Vì không có cơ chế phân công nhiệm vụ, toàn bộ đàn chó đều chọn chung một con cừu xa nhất, dồn vào thành một đám đông hỗn loạn. Thêm nhiều chó không mang lại bất kỳ lợi ích mở rộng nào.*

---

### Mô hình chó độc lập: `independent`

Mỗi chú chó độc lập thực thi quy tắc một-chó nguyên bản của Strömbom (2014):
- Tự quyết định chuyển đổi giữa gom cừu và lùa bầy dựa trên toàn bộ đàn.
- Chạy tới các điểm đích với nhiễu bước đi và quy tắc dừng độc lập.
- Có máy trạng thái chuyển đổi nhưng **hoàn toàn thiếu tầng điều phối đa tác tử**.
- *Kết quả*: Hoạt động ổn định trên đàn nhỏ lên đến $N = 200$ cừu; nhưng thất bại hoàn toàn ở $N = 400$ nơi sự phối hợp phân tán là bắt buộc.

---

### Mô hình lực liên tục: `kubo`

Điều khiển đàn chó bằng các trường thế liên tục:
1. Lực hút về phía con cừu xa nhất.
2. Lực đẩy khi lại quá gần con cừu đó ($1/r^3$).
3. Lực đẩy tránh xa bờ chuồng đích.
4. **Lực đẩy tương hỗ giữa các chú chó**: Lực đẩy rất mạnh ($1/r^3$, trọng số $K_{f4} = 3000$) giữa các chú chó với nhau.
- Đàn chó hành xử tương tự như các hạt tích điện cùng dấu: chúng tự động tản đều dọc theo rìa sau của bầy cừu một cách tự nhiên mà không cần bất kỳ bộ điều phối trung tâm nào.

---

## Tài liệu tham khảo

1. **Strömbom, D., et al. (2014)**. *Solving the shepherding problem: heuristics for herding autonomous, interacting agents*. Journal of the Royal Society Interface, 11(100), 20140719. [DOI: 10.1098/rsif.2014.0719](https://doi.org/10.1098/rsif.2014.0719)
2. **Kubo, M., Tashiro, M., Sato, H., Yamaguchi, A. (2022)**. *Herd guidance by multiple sheepdog agents with repulsive force*. Artificial Life and Robotics, 27, 416–427. [DOI: 10.1007/s10015-021-00726-7](https://doi.org/10.1007/s10015-021-00726-7)
3. **Lama, A., & di Bernardo, M. (2024)**. *Universal scaling laws in multi-agent herding of non-cohesive targets*. Physical Review Research, 6(L032012). [DOI: 10.1103/PhysRevResearch.6.L032012](https://doi.org/10.1103/PhysRevResearch.6.L032012)
