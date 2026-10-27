# Xác định cỡ đội chăn theo độ tin cậy: đội nhỏ nhất tăng ra sao theo cỡ bầy, thời hạn và quy tắc thành công

*Bản nháp cho tạp chí Swarm Intelligence (Springer), bản tiếng Việt của [draft_d_min_paper.md](draft_d_min_paper.md). Cấu trúc theo thể thức bài nghiên cứu của tạp chí: tóm tắt từ 150 đến 250 từ, 4 đến 6 từ khóa, các mục đánh số, một mục tuyên bố và tài liệu tham khảo theo tác giả–năm. Những chỗ ghi VIỆC CẦN LÀM phải xong trước khi nộp.*

[Tên tác giả và cơ quan — VIỆC CẦN LÀM]

---

## Tóm tắt

Cần bao nhiêu tác tử chăn để lùa một bầy vào đích? Các câu trả lời đã công bố dựa trên tỉ lệ thành công lấy trung bình qua một số lượt chạy cố định. Chúng tôi định nghĩa đội nhỏ nhất $D_{\min}$ là đội nhỏ nhất có tỉ lệ thành công ít nhất 0,90 với độ tin cậy 99%, theo khoảng Clopper–Pearson chính xác, và ước lượng nó bằng một bộ lấy mẫu thích nghi chỉ chạy thêm ở những ô còn chưa có câu trả lời. Với mô hình cừu của Strömbom và cộng sự (2014) và một bộ điều khiển nhiều chó có điều phối, chúng tôi lập bản đồ $D_{\min}$ theo cỡ bầy từ 25 đến 566, bốn bố cục xuất phát và ba thời hạn, qua 29 giao thức và 299.740 lượt mô phỏng. Bầy gọn chỉ cần một chó ở mọi cỡ. Trên bầy tản mát, $D_{\min}$ tăng chậm hơn tuyến tính, với hệ số góc log-log 0,27–0,38 ở thời hạn thong thả và 0,38–0,61 ở thời hạn chặt hơn, và rút thời hạn từ 6 xuống 3 lần thời gian lùa làm nó tăng nhiều hơn khi bầy lớn gấp bốn. Quy tắc thành công làm đổi câu trả lời: khi mọi con cừu phải vào đích, đội lớn thất bại vì con cuối cùng, và $D_{\min}$ phản ứng với những lựa chọn thiết lập hầu như không làm nó đổi khi chỉ cần 99% vào đích. Các thí nghiệm bỏ bớt thành phần cho thấy công tắc gom/lùa đưa một đội không điều phối tới bầy 200 con, và việc phân công con lạc là cần thiết ở 400 con. Chạy trong cùng bộ mô phỏng, các mục tiêu không gắn kết của Lama và di Bernardo (2024) theo đúng quy luật căn bậc hai của họ, nhưng gần ngưỡng cảm nhận, tiêu chí trung bình 0,99 chấp nhận một đội chỉ thành công 21 trong 30 lượt.

**Từ khóa:** chăn bầy · hệ đa tác tử · rô-bốt bầy đàn · cỡ đội · kiểm định tuần tự · quy luật tỉ lệ

---

## 1 Giới thiệu

Bài toán chăn bầy, trong đó một vài tác tử điều khiển một nhóm tác tử lớn hơn phản ứng với chúng, được nghiên cứu như mô hình công việc của chó chăn cừu và như một bài toán điều khiển cho bầy rô-bốt và thiết bị bay không người lái (Strömbom và cộng sự 2014; Long và cộng sự 2020). Người triển khai một đội như vậy phải chốt cỡ đội trước khi chạy. Quá ít tác tử thì nhiệm vụ thất bại; nhiều hơn mức cần thì tốn phần cứng, năng lượng, và với động vật thì gây căng thẳng.

Các công trình nhiều tác tử trước đây xét những cỡ đội cố định hoặc những mục tiêu không tụ bầy (Pierson và Schwager 2015; Kubo và cộng sự 2022; Lama và di Bernardo 2024). Lama và di Bernardo (2024) thấy rằng với mục tiêu không gắn kết, đội đủ nhỏ nhất tăng theo căn bậc hai của số mục tiêu. Tiêu chí của họ, như phần lớn trong lĩnh vực, là một giá trị trung bình: một đội được coi là đủ khi tỉ lệ mục tiêu được gom, lấy trung bình qua các lượt, đạt 0,99. Giá trị trung bình cho biết đội làm được bao nhiêu phần việc ở một lượt điển hình. Nó không cho biết đội thất bại thường xuyên đến đâu, mà đó lại là điều người thiết kế cần biết.

Bài báo này xác định cỡ đội theo độ tin cậy. Một đội là đủ khi tỉ lệ thành công của nó ít nhất $\theta = 0{,}90$ với độ tin cậy 99%. Chúng tôi gọi đội nhỏ nhất như vậy là $D_{\min}$, ước lượng nó bằng một bộ lấy mẫu tuần tự thích nghi, và báo cáo nó dưới dạng một giá trị, một khoảng, hoặc một cận dưới khi dữ liệu chưa quyết định được. Chúng tôi áp dụng quy tắc này cho đàn cừu gắn kết của Strömbom và cộng sự (2014) do một đội chó có điều phối lùa, và cho các mục tiêu không gắn kết của Lama và di Bernardo (2024) trong cùng bộ mô phỏng.

Các đóng góp gồm:

1. Một định nghĩa đội nhỏ nhất dựa trên độ tin cậy, cùng một bộ ước lượng thích nghi quyết định từng ô ở độ tin cậy 99% hoặc báo cáo ô đó là còn mở.
2. Một bản đồ $D_{\min}$ cho bầy gắn kết theo cỡ bầy, bố cục xuất phát và thời hạn, cho thấy mức tăng chậm hơn tuyến tính với hệ số góc phụ thuộc vào thời hạn nhiều hơn vào bầy.
3. Bằng chứng rằng quy tắc thành công làm đổi câu trả lời: dưới quy tắc nghiêm ngặt, con cừu cuối cùng quyết định lượt chạy và kết quả nhạy với những lựa chọn thiết lập tùy ý; dưới quy tắc 99% thì không.
4. Một phân tích bỏ bớt thành phần của bộ điều khiển đội, tách phần đóng góp của công tắc gom/lùa khỏi phần đóng góp của việc phân công con lạc.
5. Một lần tái hiện độc lập quy luật căn bậc hai của Lama và di Bernardo (2024), và một minh chứng rằng gần ngưỡng của họ, tiêu chí trung bình chấp nhận những đội thất bại 9 trong 30 lượt.

Mọi lượt chạy đều được lưu cùng cấu hình và hạt giống ngẫu nhiên, và có thể chạy lại chính xác; mã nguồn và dữ liệu được công khai (mục 9).

## 2 Các công trình liên quan

*VIỆC CẦN LÀM: mở rộng mục này với tài liệu về chăn bầy và dẫn hướng bầy đàn (chăn bầy theo lý thuyết điều khiển, chăn bầy bằng học máy, chăn bầy bằng thiết bị bay). Không đưa công trình chưa công bố được bàn trong quá trình nghiên cứu vào phần trích dẫn.*

Strömbom và cộng sự (2014) đề xuất một quy tắc kinh nghiệm cho một chó, khớp với dữ liệu định vị vệ tinh của một chó chăn và một đàn cừu: chó gom con cừu xa tâm bầy nhất khi còn con nào nằm ngoài khoảng cách $f(N) = r_a N^{2/3}$, và nếu không thì lùa bầy từ một điểm phía sau nó. Mô hình của họ là nền tảng của nhiều công trình chăn bầy về sau, được Long và cộng sự (2020) tổng quan.

Nhiều tác giả đã mở rộng bài toán chăn bầy sang đội. Pierson và Schwager (2015) điều khiển nhiều rô-bốt chăn các tác tử không hợp tác. Kubo và cộng sự (2022) cho nhiều tác tử chó chăn lực đẩy lẫn nhau và xét các cỡ đội cố định. Auletta và cộng sự (2021) kết hợp quy tắc điều khiển cục bộ với việc chọn mục tiêu trực tuyến để chăn các tác tử ngẫu nhiên. Lama và di Bernardo (2024) nghiên cứu đội đủ nhỏ nhất thay đổi thế nào theo số mục tiêu không gắn kết, di chuyển ngẫu nhiên, và tìm ra quy luật căn bậc hai trên một ngưỡng mật độ khi người chăn chỉ cảm nhận cục bộ.

Các nghiên cứu thực địa đo cách cừu thật phản ứng với người chăn. Jadhav và cộng sự (2024) theo dõi một đàn cừu phản ứng với một chó chăn giống border collie; Yaxley và cộng sự (2021) đo ảnh hưởng của các thông số tiếp cận bằng thiết bị bay tới mức căng thẳng và chuyển động của cừu.

Công trình của chúng tôi khác những công trình trên ở đại lượng được đo. Chúng tôi không đề xuất bộ điều khiển mới. Với các mô hình và một bộ điều khiển cho trước, chúng tôi đo đội nhỏ nhất đáng tin cậy ở một mức tin cậy đã nêu, và câu trả lời đó phụ thuộc thế nào vào bầy, thời hạn và quy tắc thành công.

## 3 Mô hình

### 3.1 Cừu

Chúng tôi dùng mô hình cừu của Strömbom và cộng sự (2014) với các tham số đã công bố. Thời gian tiến theo bước 1 giây. Con cừu có chó trong phạm vi $r_s = 65$ m thì phản ứng: hướng mới của nó là tổng có trọng số của hướng trước đó ($h = 0{,}5$), hướng về tâm của $n$ con gần nhất ($c = 1{,}05$), hướng tránh xa các con gần hơn $r_a = 2$ m ($\rho_a = 2$), hướng tránh xa các chó ($\rho_s = 1$) và nhiễu ($e = 0{,}3$). Sau đó nó đi 1 m theo hướng ấy. Khi không có chó trong phạm vi $r_s$, nó gặm cỏ: đứng yên với xác suất 0,95, còn lại bước 1 m theo một hướng ngẫu nhiên. Trong trường hợp cơ sở $n = N - 1$, nên mọi con cừu bị hút về tâm của cả bầy.

Mô hình định nghĩa lực đẩy của một chó. Với nhiều chó, chúng tôi cộng các vectơ đơn vị hướng ra xa từng chó trong phạm vi $r_s$ rồi chuẩn hóa tổng về độ dài một. Nếu cộng mà không chuẩn hóa, hai chó cách nhau dưới 116° (nhìn từ con cừu) sẽ đẩy mạnh hơn lực hút của bầy $c = 1{,}05$, và các con cừu ở hai phía khác nhau của bầy sẽ bị đẩy tách ra ngay từ $D = 2$. Khi chuẩn hóa, đội lớn hơn chỉ đổi hướng đẩy con cừu, không bao giờ đổi độ mạnh. Trong cả hai cách, tốc độ của con cừu không phụ thuộc vào lực đẩy, vì con cừu đang phản ứng luôn đi đúng 1 m mỗi bước, bất kể cỡ đội.

### 3.2 Bộ điều khiển chó

Mọi chó di chuyển với tốc độ 1,5 m/s, giá trị của Strömbom và cộng sự (2014), với nhiễu góc của bài báo đó, và đứng yên khi có con cừu nào trong phạm vi $3 r_a = 6$ m. Chúng tôi so sánh ba bộ điều khiển.

Bộ điều khiển đội mở rộng quy tắc một chó cho $D$ chó (Hình 1). Khi còn con cừu nào nằm xa tâm bầy hơn $f(N) = r_a N^{2/3}$, các chó gom. $D$ con lạc xa nhất được phân công mỗi con cho một chó bằng thuật toán Hungary (Kuhn 1955), cực tiểu tổng khoảng cách từ các chó tới các điểm nằm sau mỗi con lạc một đoạn $r_a$; việc phân công được tính lại ở mỗi bước. Các chó còn thừa lùa phần lõi. Khi mọi con cừu đều trong phạm vi $f(N)$, các chó lùa: chúng dàn ra trên một cung quanh tâm bầy đi qua điểm lùa của Strömbom, cách tâm $r_a\sqrt{N}$ về phía ngược với đích, đủ rộng để che hai bên bầy, và giữ thứ tự góc để đường đi của chúng không cắt nhau.

Bộ điều khiển độc lập cho mỗi chó dùng quy tắc một chó của Strömbom mà không có tầng điều phối đội. Vì mọi chó nhìn cùng một bầy, chúng đều chọn giống nhau.

Bộ điều khiển nhắm con xa nhất (FAT) đưa mọi chó ra sau con cừu xa đích nhất. Nó không có công tắc gom/lùa và không có phân công.

![Bộ điều khiển đội](figures/fig3_team_rule.png)

**Hình 1.** Bộ điều khiển đội với $D = 1, 2, 4, 8$ chó ở $N = 200$. Trên: gom một bầy xuất phát tản mát; $D$ con lạc xa nhất được phân công mỗi con cho một chó (dấu chéo là các điểm gom). Dưới: lùa một bầy gọn; các chó dàn trên một cung phía sau bầy theo thứ tự góc.

### 3.3 Mục tiêu không gắn kết

Để so sánh ở mục 5.6, chúng tôi cài đặt mô hình của Lama và di Bernardo (2024) theo văn bản bài báo, vì mã nguồn không được công bố. Mục tiêu di chuyển theo bước ngẫu nhiên và bị đẩy ra xa khi người chăn ở gần hơn $\lambda = 2{,}5$; chúng không hút nhau. Mỗi người chăn đuổi mục tiêu xa đích nhất trong số những mục tiêu nó cảm nhận được, trong bán kính cảm nhận 10 hoặc không giới hạn, bỏ qua mọi mục tiêu đang gần một người chăn khác mà nó cảm nhận được hơn. Mục tiêu và người chăn xuất phát phân bố đều trên một đĩa bán kính $R = 50$ quanh một đích bán kính $R/5$, và một lượt kéo dài tối đa 5000 giây, thời gian tối đa mà Hình S8 trong phần bổ sung của họ ghi cho $R = 50$ và bán kính cảm nhận 10. Ở những chỗ văn bản không nói rõ, chúng tôi đưa ra lựa chọn và nêu rõ: lực đẩy hướng ra xa người chăn; một lượt kết thúc khi mọi người chăn ở trong đích và không người chăn nào cảm nhận được mục tiêu ngoài đích; mục tiêu và người chăn được cập nhật từ cùng một trạng thái.

## 4 Phương pháp

### 4.1 Hình học nhiệm vụ

Nhiệm vụ là gom bầy và lùa nó vào một đích hình tròn trước thời hạn. Không có hàng rào. Mọi độ dài tỉ lệ với bán kính bầy đã hiệu chỉnh $R_f(N)$, bán kính mà bầy $N$ con ổn định khi một chó lùa nó ($\sqrt{2}$ lần khoảng cách căn trung bình bình phương tới tâm bầy trong 90 giây cuối của một lần lùa 300 giây, lấy trung vị qua 3 hạt giống và hai cỡ xuất phát). $R_f$ là 6,2 m ở $N = 25$ và 11,4 m ở $N = 400$. Bán kính đích là $1{,}9 R_f$. Quãng lùa $l$ từ tâm xuất phát của bầy tới tâm đích là giá trị lớn nhất trong ba giá trị: $13 R_f$, 80 m, và khoảng cách giữ đích tách khỏi mọi vị trí xuất phát. Trên khoảng 600 con, bầy xuất phát lỏng giữ lại một phần cỡ ban đầu, nên $R_f$ không còn xác định; chúng tôi dừng ở $N = 566$.

Thời hạn là bội số của thời gian lùa $T_{\mathrm{drive}} = l / (1\ \mathrm{m/s})$, thời gian một con cừu đi thẳng với tốc độ của nó cần để hết quãng lùa. Một bầy gọn do một chó lùa về đích trong khoảng 1,46 đến 1,74 $T_{\mathrm{drive}}$. Chúng tôi dùng các thời hạn 12, 6 và 3 $T_{\mathrm{drive}}$, tức khoảng tám, bốn và hai lần thời gian của một chó đó.

### 4.2 Bố cục xuất phát và vị trí xuất phát của chó

Bốn bố cục xuất phát (Hình 2) trải từ một bầy không cần gom tới một bầy cần gom nhiều. Các bố cục tản mát được định cỡ theo khoảng cách gom của Strömbom $L = f(N)$, để "xuất phát tản mát" có cùng nghĩa ở mọi $N$:

- `compact`: phân bố Gauss với $\sigma = 0{,}5 R_f$, cắt ở $3\sigma$;
- `wide`: phân bố Gauss với $\sigma = 0{,}5 L$, cắt ở $3\sigma$, nên khoảng 14% số cừu xuất phát ngoài $L$;
- `split`: ba cụm gọn có tâm nằm trên một đường tròn bán kính $L$;
- `outlier_rich`: 80% số cừu trong một lõi gọn và 20% trên một vành từ $1{,}1 L$ đến $1{,}6 L$.

Các chó xuất phát trên những nửa đường tròn phía sau bầy, về phía ngược với đích. Nửa đường tròn đầu tiên cách điểm xa nhất mà một con cừu có thể xuất phát 30 m; các chó trên một nửa đường tròn đứng cách nhau ít nhất 5 m, và các chó còn lại đứng trên nửa đường tròn xa hơn 5 m.

![Bố cục xuất phát](figures/fig7_layouts.png)

**Hình 2.** Bốn bố cục xuất phát ở $N = 200$ với $D = 4$ chó, cùng tỉ lệ. Đường tròn nét đứt là khoảng cách gom $f(N) = r_a N^{2/3}$.

### 4.3 Quy tắc thành công

Một lượt thành công khi, ở một bước nào đó trước thời hạn, có đủ số cừu cùng lúc ở trong đích. Dưới quy tắc nghiêm ngặt, mọi con cừu phải ở trong. Dưới quy tắc 99%, ít nhất $\lceil 0{,}99 N \rceil$ con phải ở trong, nên hai quy tắc trùng nhau khi $N$ dưới 100; cho phép một con lạc ở $N = 100$ và bốn con ở $N = 400$.

### 4.4 Độ tin cậy và đội nhỏ nhất

Một ô là một tổ hợp gồm mô hình, bộ điều khiển, bố cục, $N$, thời hạn, quy tắc thành công và cỡ đội $D$. Với $n$ lượt có $k$ lượt thành công, $[L, U]$ là khoảng Clopper–Pearson hai phía chính xác ở mức 99% (Clopper và Pearson 1934) của tỉ lệ thành công, với $\alpha = 0{,}01$. Với $\theta = 0{,}90$, một ô là đáng tin cậy khi $L \ge \theta$, không đáng tin cậy khi $U < \theta$, và chưa quyết định trong các trường hợp còn lại. Với một đường cong gồm các cỡ đội đã thử,

$$
D_{\min} = \min \lbrace D \mid \text{ô } D \text{ đáng tin cậy} \rbrace .
$$

Chúng tôi báo cáo $D_{\min}$ là một giá trị khi mọi $D$ nhỏ hơn đã thử đều không đáng tin cậy, là một khoảng (ví dụ 2–3) khi một $D$ nhỏ hơn vẫn chưa quyết định ở mức trần, là một cận dưới ([5]) khi chưa có $D$ nào đáng tin cậy, và là "không có" khi mọi $D$ đã thử tới 24 đều không đáng tin cậy.

Mỗi ô bắt đầu với 10 lượt. Sau mỗi đợt 10 lượt, khoảng được tính lại; ô đã quyết định không chạy thêm, còn ô chưa quyết định được thêm một đợt, tới tối đa 200 lượt. Một quyết định "đáng tin cậy" cần ít nhất 51 lượt thành công liên tiếp không có thất bại, nên sớm nhất là ở lượt thứ 60, trong khi các ô rõ ràng không đáng tin cậy thường dừng sau 10 đến 20 lượt. Khi hai cỡ đội kề nhau đã thử rơi vào hai vùng khác nhau và chênh nhau hơn một, vòng sau thêm cỡ đội ở giữa. Ở 200 lượt, một ô chỉ được quyết định nếu tỉ lệ thành công ít nhất 0,955 hoặc nhiều nhất 0,835.

Khoảng tin cậy trên là khoảng của một lần xem. Với tới 20 lần xem mỗi ô, xác suất quyết định sai cao hơn 1% một chút; khoảng Clopper–Pearson vốn thận trọng, nhưng chúng tôi không hiệu chỉnh cho việc xem lặp lại.

Hạt giống thứ $i$ của mọi ô là cùng một hạt giống gốc cộng $i$, và mỗi lượt lấy vị trí xuất phát, nhiễu của cừu và nhiễu của chó từ ba luồng ngẫu nhiên riêng. Vì vậy các ô chỉ khác nhau ở $D$ xuất phát từ cùng một bầy với cùng nhiễu của cừu, và thời gian hoàn thành của chúng có thể so sánh theo từng hạt giống. Chúng tôi dùng điều này để định nghĩa cỡ đội mà từ đó thêm chó không còn giúp ích. Hai ô đáng tin cậy được so sánh bằng phép lấy mẫu lại có ghép cặp trên hiệu thời gian hoàn thành theo từng hạt giống (ít nhất 5 hạt giống chung đều thành công, 4000 lần lấy mẫu lại, khoảng 99%). Một ô nhanh hơn hay chậm hơn khi toàn bộ khoảng của hiệu trung vị, tính tương đối theo trung vị của ô chậm hơn, nằm ngoài ±5%. $D_{\mathrm{sat}}$ là $D$ đáng tin cậy nhỏ nhất mà không $D$ đáng tin cậy nào lớn hơn nhanh hơn nó.

Mức tăng của $D_{\min}$ theo $N$ được tóm tắt bằng hệ số góc bình phương tối thiểu của $\log_2 D_{\min}$ theo $\log_2 N$. Khi một số $D_{\min}$ là khoảng, hệ số góc được báo cáo là khoảng các hệ số góc mà hai đầu của các khoảng đó cho phép.

### 4.5 Thiết kế thí nghiệm

Bảng 1 liệt kê 29 giao thức được dùng ở đây; tổng cộng chúng chạy 299.740 lượt, không có lỗi mô phỏng nào. Lưới cỡ đội là $D \in \{1, 2, 3, 4, 6, 8, 12, 16, 24\}$, khoảng hai giá trị cho mỗi lần gấp đôi, cộng các điểm giữa mà bộ lấy mẫu thêm vào; các giao thức Lama thử mọi $D$ từ 1 đến 25, đúng độ phân giải của nghiên cứu gốc.

**Bảng 1.** Các giao thức dùng trong bài.

| Nhóm | Số giao thức | Lưới | Số lượt |
| :--- | :---: | :--- | ---: |
| Lưới chính | 6 | $N = 25$–400, 4 bố cục, thời hạn 12, 6, 3 $T_{\mathrm{drive}}$, quy tắc nghiêm ngặt và 99%; các lưới 99% ở 12 và 6 $T_{\mathrm{drive}}$ được mở rộng tới $N = 71, 141, 283, 566$ | 115.470 |
| Bỏ bớt thành phần bộ điều khiển | 3 | Nhắm con xa nhất (nghiêm ngặt và 99%), độc lập (99%), ở 6 $T_{\mathrm{drive}}$ | 30.320 |
| Độ nhạy | 14 | Ở 6 $T_{\mathrm{drive}}$, một bản cơ sở và sáu biến thể (chó thả từ một điểm, chó trên một vòng tròn đủ, khoảng cách xuất phát 15 và 60 m, bán kính đích $1{,}5 R_f$, tham số cừu khớp thực địa, tốc độ chó 1,15 m/s), mỗi bản dưới cả hai quy tắc | 69.630 |
| Độ gắn kết | 4 | Trọng số hút $c = 1{,}3;\ 1{,}6;\ 2{,}0$; hút về nửa bầy ($n = 0{,}5N$); quy tắc 99%, 12 $T_{\mathrm{drive}}$ | 44.040 |
| Mục tiêu không gắn kết | 2 | Mô hình Lama và di Bernardo (2024), bán kính cảm nhận 10 và vô hạn, tới 400 mục tiêu | 40.280 |
| Tổng | 29 | | 299.740 |

## 5 Kết quả

### 5.1 Đội nhỏ nhất tăng chậm theo bầy

Bầy gọn cần một chó ở mọi cỡ bầy và mọi thời hạn (Bảng 2). Tới $N = 50$, một chó cũng đủ trên mọi bố cục tản mát, ở mọi thời hạn. Một lý do có thể là ở $N = 50$, con cừu xa nhất xuất phát cách tâm bầy nhiều nhất khoảng 45 m, nằm trong phạm vi 65 m mà cừu phản ứng, nên một chó làm gần như mọi con cừu chuyển động ngay từ đầu.

Trên bầy tản mát từ 100 con trở lên, $D_{\min}$ tăng, nhưng chậm. Ở 12 lần thời gian lùa với quy tắc 99%, nó chỉ đạt 2 chó ở $N = 400$ trên mọi bố cục tản mát. Trên chín cỡ bầy của các lưới mở rộng (Bảng 3, Hình 3), hệ số góc của $D_{\min}$ theo $N$ là 0,27–0,38 trên `wide` và 0,28–0,38 trên `outlier_rich` ở 12 lần thời gian lùa, và 0,38–0,61 trên `wide` và 0,40–0,58 trên `outlier_rich` ở 6 lần. Tới $N = 566$, một luật lũy thừa $D = c N^b$ và một đường cong chững lại $D = 1 + (D_\infty - 1) N / (N + K)$ khớp dữ liệu tốt như nhau, nên dữ liệu không phân biệt được tăng đều với bão hòa.

**Bảng 2.** $D_{\min}$ dưới quy tắc nghiêm ngặt / quy tắc 99%. Một khoảng nghĩa là một đội nhỏ hơn vẫn chưa quyết định ở 200 lượt; [k] là cận dưới; "không" nghĩa là không có đội đáng tin cậy tới 24.

| Thời hạn | Bố cục | $N = 25$ | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 12× | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| 12× | `wide` | 1 / 1 | 1 / 1 | 1 / 1 | 2 / 1–2 | 3 / 2 |
| 12× | `split` | 1 / 1 | 1 / 1 | 1 / 1 | 1–2 / 1 | 3 / 2 |
| 12× | `outlier_rich` | 1 / 1 | 1 / 1 | 1–3 / 1–2 | 2 / 2 | 3 / 2 |
| 6× | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| 6× | `wide` | 1 / 1 | 1 / 1 | 1 / 1 | 3 / 2 | [9] / 2–3 |
| 6× | `split` | 1 / 1 | 1 / 1 | 1 / 1 | không / [1] | không / [5] |
| 6× | `outlier_rich` | 1 / 1 | 1 / 1 | 3 / 2 | [12] / 2–3 | không / 3 |
| 3× | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| 3× | `wide` | 1 / 1 | 1 / 1 | 3 / 2 | không / 3 | không / 5–6 |
| 3× | `split` | 1 / 1 | 1 / 1 | 1 / 1 | không / không | không / không |
| 3× | `outlier_rich` | 1 / 1 | 1 / 1 | 3–8 / 2 | không / 4–10 | không / [6] |

**Bảng 3.** $D_{\min}$ trên chín cỡ bầy (quy tắc 99%), và $D_{\mathrm{sat}}$ trên `wide` ở 6 lần thời gian lùa.

| $N$ | 25 | 50 | 71 | 100 | 141 | 200 | 283 | 400 | 566 | Hệ số góc |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `wide`, 12× | 1 | 1 | 1 | 1 | 2 | 1–2 | 2 | 2 | 2–3 | 0,27–0,38 |
| `outlier_rich`, 12× | 1 | 1 | 1 | 1–2 | 2 | 2 | 2 | 2 | 2–3 | 0,28–0,38 |
| `wide`, 6× | 1 | 1 | 1 | 1 | 2 | 2 | 2–3 | 2–3 | 3–7 | 0,38–0,61 |
| `outlier_rich`, 6× | 1 | 1 | 1 | 2 | 2 | 2–3 | 2–3 | 3 | 3–6 | 0,40–0,58 |
| $D_{\mathrm{sat}}$ `wide`, 6× | 1 | 1 | 1 | 2 | 3 | 3 | 4 | 5 | 7–24 | 0,70–0,91 |

![D_min theo N](figures/fig20_dmin_vs_n.png)

**Hình 3.** $D_{\min}$ theo cỡ bầy trên trục log-log, mỗi ô hình một thời hạn (12, 6 và 3 lần thời gian lùa). Đường liền có chấm tròn: quy tắc nghiêm ngặt; đường nét đứt có ô vuông: quy tắc 99%. Thanh tô mờ là khoảng, tam giác rỗng là cận dưới, dấu chéo là không có đội đáng tin cậy tới 24.

### 5.2 Thời hạn làm đổi đội nhỏ nhất nhiều hơn cỡ bầy

Dưới quy tắc 99% trên `wide` và `outlier_rich`, nới thời hạn từ 6 lên 12 lần thời gian lùa tiết kiệm nhiều nhất một chó. Rút từ 6 xuống 3 thì tốn hơn: trên `wide` ở $N = 400$, $D_{\min}$ tăng từ 2–3 lên 5–6, trong khi ở 6 lần thời gian lùa, bầy lớn gấp bốn từ 100 lên 400 chỉ đưa nó từ 1 lên 2–3. Ở 3 lần thời gian lùa, hệ số góc của $D_{\min}$ theo $N$ tăng lên 0,62–0,68 trên `wide` và 0,70–1,10 trên `outlier_rich` (với $N \le 200$, nơi nó đã quyết định). Cừu đi 1 m/s còn chó chạy 1,5 m/s. Với 12 lần thời gian lùa, một chó có đủ thời gian đưa từng con lạc về trước khi lùa bầy; với 3 lần thì trình tự đó không còn vừa, và nhiều chó phải làm việc cùng lúc ở các phía khác nhau của bầy.

Bố cục `split` hành xử khác. Ở 6 lần thời gian lùa và $N \ge 200$, tỉ lệ thành công dưới quy tắc 99% nằm giữa 0,60 và 0,92 với mọi $D \ge 4$, và ở 3 lần thời gian lùa không đội nào tới 24 là đáng tin cậy. Chạy lại các lượt đã lưu chỉ ra hai nguyên nhân: việc phân công, vốn cực tiểu tổng khoảng cách, có thể đưa mọi chó đang gom tới một cụm trong khi cụm khác trôi đi, và khoảng một phần tư số chó bị quy tắc dừng giữ đứng yên cạnh một cụm trên đường tới cụm khác.

### 5.3 Quy tắc thành công làm đổi câu trả lời

Trong cả 34 đường cong tản mát mà cả hai quy tắc đều cho một đội đáng tin cậy, quy tắc 99% cần bằng hoặc ít chó hơn (Bảng 2, Hình 4). Ở những chỗ cả hai đã quyết định và khác nhau, chênh lệch là một chó. Sáu đường cong bầy lớn không có đội đáng tin cậy dưới quy tắc nghiêm ngặt lại có một đội dưới quy tắc 99% (hai đã quyết định, bốn là khoảng).

Các thất bại nghiêm ngặt của đội lớn xảy ra ở đích. Trong 97% các thất bại nghiêm ngặt với 6 chó trở lên ở lần chạy cơ sở của nhóm độ nhạy, 99% bầy đã từng ở trong đích trước thời hạn (Hình 5). Trong một lượt điển hình, các chó đuổi con lạc cuối cùng rốt cuộc đứng giữa bầy và đích, và lùa bầy ra ngoài trở lại. Với chó chậm hơn (1,15 m/s, gần tỉ lệ tốc độ chó so với cừu mà Jadhav và cộng sự 2024 đo được), hiện tượng này phần lớn biến mất: $D_{\min}$ nghiêm ngặt trên `outlier_rich` $N = 400$ giảm từ "không có" xuống 6, và trên `wide` $N = 400$ từ [9] xuống 5.

Hai quy tắc cũng khác nhau ở độ nhạy với những lựa chọn không có giá trị thực tế (Hình 6). Dưới quy tắc 99%, việc thả chó từ một điểm hoặc từ một vòng tròn đủ, đổi khoảng cách xuất phát thành 15 hoặc 60 m, làm chó chậm lại hay dùng tham số cừu khớp thực địa chỉ làm $D_{\min}$ xê dịch nhiều nhất khoảng một chó. Dưới quy tắc nghiêm ngặt, cùng những thay đổi đó thường biến một $D_{\min}$ hữu hạn thành "không có": trên `wide` $N = 200$, từ 3 thành "không có" với tham số cừu khớp thực địa. Lựa chọn duy nhất quan trọng dưới cả hai quy tắc là bán kính đích: với $1{,}5 R_f$ thay vì $1{,}9 R_f$, $D_{\min}$ theo quy tắc 99% trên `wide` $N = 400$ tăng từ 2–3 lên 5–6, vì một bầy đã ổn định chỉ vừa khít trong đích.

![Thành công nghiêm ngặt so với 99 phần trăm](figures/fig30_strict_vs_99.png)

**Hình 4.** Tỉ lệ thành công nghiêm ngặt so với 99%, từng ô trên cùng các hạt giống, cho các bố cục tản mát ở $N \ge 100$, mỗi ô hình một thời hạn. Vùng tô mờ phía trên bên trái chứa 40 ô có tỉ lệ 99% ít nhất 0,90 trong khi tỉ lệ nghiêm ngặt dưới mức đó.

![Con cừu cuối cùng](figures/fig22_straggler.png)

**Hình 5.** Trái: tỉ lệ lượt với 6 chó trở lên mà mọi con cừu vào đích, mà 99% đã ở trong đích ở một bước nào đó, và mà mọi con cừu vào đích khi chó chạy 1,15 m/s. Phải: một lượt (`wide`, $N = 400$, 16 chó) trong đó các chó đưa 399 con vào rồi hai lần lùa bầy ra ngoài khi đuổi con cuối cùng; chó chậm hơn xong trong một lần.

![Độ nhạy](figures/fig24_sensitivity.png)

**Hình 6.** $D_{\min}$ cho từng thay đổi thiết lập ở 6 lần thời gian lùa; nửa trên là quy tắc nghiêm ngặt, nửa dưới là quy tắc 99%. Dưới quy tắc 99%, phần lớn các hàng khớp bản cơ sở trong phạm vi một chó.

### 5.4 Phần nào của bộ điều khiển quan trọng

Bộ điều khiển nhắm con xa nhất đáng tin cậy với bầy tới 100 con nhưng không có đội đáng tin cậy ở $N \ge 200$ trên bất kỳ bố cục tản mát nào, và trên bầy gọn 400 con, nó không có đội nào dưới quy tắc nghiêm ngặt và chỉ có cận dưới 12 dưới quy tắc 99%, nơi bộ điều khiển đội chỉ cần một chó (Bảng 4, Hình 7). Mọi chó của nó đuổi cùng một con cừu: ở $N \ge 200$, tỉ lệ trung vị số chó có một chó khác trong phạm vi 2 m là 0,86 trên `compact` và 0,79 trên `split`. Một đội nhắm con xa nhất lớn hơn chỉ là một đám đông hơn sau lưng một con cừu.

Bộ điều khiển độc lập giữ công tắc gom/lùa nhưng không có phân công. Nó đáng tin cậy trên mọi bố cục tản mát tới $N = 200$ (2–3 chó trên `wide`, 3 trên `outlier_rich`), nơi bộ điều khiển nhắm con xa nhất thất bại. Ở $N = 400$, nó không có đội đáng tin cậy nào tới 24, trong khi bộ điều khiển đội cần 2–3 chó trên `wide` và 3 trên `outlier_rich`. Công tắc đủ để giữ một bầy 200 con lại với nhau; việc phân công các con lạc khác nhau cho các chó khác nhau trở nên cần thiết ở khoảng giữa 200 và 400.

**Bảng 4.** $D_{\min}$ của ba bộ điều khiển ở 6 lần thời gian lùa, quy tắc 99% (đội / độc lập / nhắm con xa nhất).

| Bố cục | $N = 200$ | $N = 400$ |
| :--- | :---: | :---: |
| `wide` | 2 / 2–3 / không | 2–3 / không / không |
| `outlier_rich` | 2–3 / 3 / không | 3 / không / không |
| `split` | [1] / 1–3 / không | [5] / không / không |

![Nhắm con xa nhất so với bộ điều khiển đội](figures/fig26_fat.png)

**Hình 7.** Tỉ lệ thành công theo cỡ đội của bộ điều khiển đội (xanh lam) và bộ điều khiển nhắm con xa nhất (cam, ký hiệu FAT trên hình) ở 6 lần thời gian lùa. Nét liền: quy tắc nghiêm ngặt; nét đứt: quy tắc 99%; nét chấm: $\theta = 0{,}90$.

### 5.5 Đội đáng tin cậy và đội nhanh nhất

$D_{\mathrm{sat}}$ tăng theo $N$ nhanh hơn $D_{\min}$. Trên `wide` ở 6 lần thời gian lùa, nó là 1, 1, 1, 2, 3, 3, 4, 5 chó từ $N = 25$ tới 400 (hệ số góc 0,70–0,91, Bảng 3), bằng 1,15 tới 2,4 lần hệ số góc của $D_{\min}$ trên `wide` (0,38–0,61) theo hai đầu khoảng, và khoảng 1,6 lần theo điểm giữa. Vượt quá $D_{\mathrm{sat}}$, thêm chó chỉ thêm chi phí mà không nhanh hơn: trong cả 189 ô đáng tin cậy nằm trên một $D_{\mathrm{sat}}$ đã quyết định ở 6 lần thời gian lùa, thời gian hoàn thành bằng 0,96 tới 1,01 lần thời gian của ô $D_{\mathrm{sat}}$, trong khi tổng thời gian làm việc của chó tăng tỉ lệ với $D$.

Dưới quy tắc 99%, không đường cong nào trên năm cỡ bầy ban đầu trở lại không đáng tin cậy sau khi đã đáng tin cậy, tới 24 chó; trên lưới chín cỡ có một chỗ trũng (`split` $N = 141$, $D = 4$, tỉ lệ thành công 0,80). Với chó là chất điểm, thêm chó làm chậm một số bầy (trên `split` $N = 400$ ở 12 lần thời gian lùa, thời gian hoàn thành trung vị là 950–1040 giây với $D \ge 9$, so với 839 giây ở $D = 5$) nhưng không làm nhiệm vụ thất bại.

Thời gian hoàn thành không đổi khi vượt $D_{\mathrm{sat}}$ là hệ quả của mô hình cừu: con cừu đang phản ứng luôn đi 1 m/s, và lực đẩy đã chuẩn hóa của nhiều chó có độ mạnh bằng của một chó (mục 3.1). Trong mô hình của Kubo và cộng sự (2022), nơi cừu tăng tốc dưới lực đẩy mạnh hơn, thời gian hoàn thành tiếp tục giảm theo $D$, từ 115 giây với một chó xuống 29 giây với mười chó ở $N = 100$ trên một bầy gọn.

### 5.6 Mục tiêu không gắn kết: lấy trung bình so với đếm số lượt

Chạy trong bộ mô phỏng của chúng tôi, mô hình của Lama và di Bernardo (2024) tái hiện các con số mà bài báo nêu cho thiết lập này. Với $R = 50$ và bán kính cảm nhận 10, Bảng I trong phần bổ sung của họ cho cỡ mà từ đó đội nhỏ nhất theo quy luật căn bậc hai là $\sqrt{N} = 8$, 9 và 11 ở các mức 90%, 95% và 99%. Đọc bảng đội nhỏ nhất theo từng cỡ của chúng tôi theo cùng cách, tức $\sqrt{N}$ đầu tiên mà từ đó đội ấy rơi vào dải tăng theo $\sqrt{N}$, chúng tôi thu được 8, 9 và 12. Các hàng khác của bảng đó, với bán kính đĩa và bán kính cảm nhận khác, chưa được chạy. Các kết quả khác của họ là bản đồ màu; bản đồ của chúng tôi có cùng hình dạng khi so bằng mắt, với không đội nào tới 25 thành công khi có ít mục tiêu, một ngưỡng sắc nét, và trên ngưỡng là một dải đội tăng theo $\sqrt{N}$. *VIỆC CẦN LÀM: quyết định hình so sánh cạnh nhau với Hình 2 của bài báo (giấy phép CC BY 4.0) đặt trong bài chính hay trong phần bổ sung.*

Chúng tôi đọc cùng các lượt chạy với hai tiêu chí: tiêu chí trung bình của bài báo (một đội là đủ khi tỉ lệ mục tiêu được gom, lấy trung bình qua các lượt, ít nhất 0,99) và quy tắc độ tin cậy của chúng tôi (ít nhất 90% số lượt kết thúc với 99% số mục tiêu ở trong đích, ở độ tin cậy 99%). Với cảm nhận vô hạn, hai tiêu chí trùng nhau ở hầu hết mọi cỡ (8 người chăn cho 100 mục tiêu, 13 cho 225, 17 cho 400), với số mũ khớp được là 0,52 và 0,53 trên 100 mục tiêu (0,52 và 0,51 trên 121). Với bán kính cảm nhận 10, số mũ khớp được trên 225 mục tiêu là 0,42 và 0,41.

Với bán kính cảm nhận 10, chúng tách nhau từ 100 mục tiêu trở lên, ở ngưỡng và ngay trên ngưỡng (Hình 8). Ở 100 mục tiêu, tiêu chí trung bình chấp nhận 19 người chăn, trong khi không đội nào tới 25 là đáng tin cậy. Ở 144 mục tiêu, 11 người chăn gom trung bình 99,2% số mục tiêu, nên tiêu chí trung bình chấp nhận họ. Chỉ 21 trong 30 lượt của họ kết thúc với 99% số mục tiêu ở trong đích (khoảng 99% của tỉ lệ thành công là 0,45–0,89). Chín lượt thất bại mất từ hai tới bốn trong 144 mục tiêu, và những lượt mất một hoặc không mất con nào kéo trung bình lên trên 0,99. Quy tắc của chúng tôi không chấp nhận 11 người chăn; $D_{\min}$ của nó là khoảng 17–25. Gần ngưỡng, hai câu trả lời chênh nhau 6 tới 14 người chăn ở 144 mục tiêu, và ít hơn ở các cỡ lớn hơn. Với 81 mục tiêu trở xuống, hai tiêu chí cùng cho rằng không đội nào tới 25 là đủ.

![Mô hình Lama](figures/fig38_lama.png)

**Hình 8.** Đội nhỏ nhất cho mỗi số mục tiêu trong mô hình của Lama và di Bernardo (2024). Trái: bán kính cảm nhận 10, vùng ngưỡng được tô mờ; phải: cảm nhận vô hạn. Chấm tròn áp dụng tiêu chí trung bình, hình thoi là $D_{\min}$ (thanh là khoảng, tam giác là cận dưới, dấu chéo là không có đội đủ tới 25).

## 6 Thảo luận

### 6.1 Độ gắn kết và quy luật căn bậc hai

Ở thời hạn thong thả, đội nhỏ nhất cho bầy gắn kết tăng với hệ số góc 0,27–0,38, dưới mức 0,5 của quy luật căn bậc hai cho mục tiêu không gắn kết, mà các lượt chạy mô hình Lama của chúng tôi xác nhận dưới cả hai tiêu chí khi cảm nhận vô hạn (số mũ 0,52 và 0,53; với bán kính cảm nhận 10 là 0,42 và 0,41 trên 225 mục tiêu). Một cách hiểu hợp lý là bầy gắn kết tự làm một phần việc của người chăn. Mỗi con cừu Strömbom bị hút về tâm của cả bầy, nên con lạc mà chó lùa quay lại sẽ tự nhập bầy, và không chó nào phải đi đón từng mục tiêu.

Các giao thức độ gắn kết kiểm tra cách hiểu này. Làm bầy gắn kết hơn mô hình gốc ($c = 1{,}3$; 1,6; 2,0) hầu như không đổi hệ số góc trên `wide` (0,20, so với 0,20–0,30 khi $c = 1{,}05$ trên cùng các cỡ, $N = 50$–400). Làm yếu đi, để mỗi con cừu bị hút về tâm của nửa bầy gần nó nhất, nâng hệ số góc lên 0,40–0,70, một khoảng chứa 0,5; trên `split`, bầy yếu hơn tách ra dưới tay một chó, và $D_{\min}$ ở $N = 200$ đi từ 1 lên 3–4. Thời hạn chặt có tác dụng tương tự (0,38–0,61 ở 6 lần thời gian lùa). Độ gắn kết và áp lực thời gian cùng nhau đặt một bầy dưới hoặc gần quy luật căn bậc hai.

Phép so sánh này có giới hạn. Các lượt chạy Lama và các lượt chạy cừu khác nhau cùng lúc ở mục tiêu, quy tắc người chăn và nhiệm vụ, nên phần chênh lệch số mũ do riêng độ gắn kết gây ra chưa được đo. Chạy mỗi bộ điều khiển trên mục tiêu của mô hình kia sẽ tách được các yếu tố, nhưng mỗi bộ điều khiển đọc những đại lượng mà mô hình kia không có (một khoảng cách gom vô nghĩa khi không có gắn kết, một đích nằm xa bầy trong nhiệm vụ lùa), nên mỗi phép ghép chéo cần một thiết kế riêng.

### 6.2 Điều mà tiêu chí thành công che đi

Hai kết quả của chúng tôi liên quan đến tiêu chí nhiều hơn đến bầy. Dưới quy tắc nghiêm ngặt, đội nhỏ nhất cho một bầy lớn phụ thuộc vào việc một hai con cừu cuối cùng có vào được hay không, và điều đó phụ thuộc vào những chi tiết như tốc độ chó hay vị trí chó xuất phát. Người thiết kế đọc kết quả như vậy thành đội mà bầy cần sẽ ước lượng quá cao, hoặc không tìm được đội nào. Dưới tiêu chí trung bình, một đội mất vài mục tiêu ở 9 trong 30 lượt vẫn qua, vì những lượt nó thua được bù trung bình bởi những lượt nó thắng.

Cả hai hiệu ứng lớn nhất đúng ở chỗ câu trả lời quan trọng nhất, gần cỡ mà một đội bắt đầu không còn đủ. Vì vậy chúng tôi đề nghị các nghiên cứu về cỡ đội báo cáo tỉ lệ thành công theo lượt, kèm khoảng tin cậy, bên cạnh mọi giá trị trung bình, và nêu rõ được phép bỏ sót bao nhiêu tác tử. Bộ lấy mẫu thích nghi làm việc này có chi phí chấp nhận được: các ô rõ ràng dừng sau 10 tới 60 lượt, và chỉ các ô gần ngưỡng mới chạy tới gần 200.

### 6.3 Điều phụ thuộc vào mô hình

Một số kết quả là hệ quả của mô hình và nên được đọc như vậy. Thời gian hoàn thành không đổi khi vượt $D_{\mathrm{sat}}$ là hệ quả của tốc độ đi không đổi của con cừu đang phản ứng và của việc chuẩn hóa lực đẩy của nhiều chó; cừu thật có chạy mạnh hơn khi có nhiều chó hay không vẫn là câu hỏi mở, và phép so sánh với Kubo cho thấy câu trả lời thay đổi khi cừu tăng tốc dưới áp lực. Bộ điều khiển đội là phần mở rộng của chúng tôi từ một quy tắc một chó, và $D_{\min}$ là tính chất của mô hình cừu, bộ điều khiển và nhiệm vụ gộp lại. Phân tích bỏ bớt thành phần (mục 5.4) cho thấy câu trả lời xê dịch bao nhiêu giữa ba bộ điều khiển cùng họ, nhưng một bộ điều khiển thiết kế khác có thể làm nó đổi thêm.

### 6.4 Hạn chế

Cừu và chó là chất điểm, quay tức thời và không mệt, và cánh đồng không có hàng rào. Chó biết vị trí của mọi con cừu. Các ô có tỉ lệ thành công thật gần 0,90 vẫn chưa quyết định ở 200 lượt và được báo cáo dưới dạng khoảng. Độ tin cậy của một quyết định chỉ là gần đúng, vì độ tin cậy được kiểm tra sau mỗi đợt mà không hiệu chỉnh cho việc xem lặp lại. Trên khoảng 600 con, bầy của mô hình không có cỡ ổn định, điều này giới hạn lưới; nghiên cứu đầy đủ của chúng tôi cũng thấy rằng trên $N \approx 1056$, điểm lùa của Strömbom nằm ngoài khoảng cách phản ứng của cừu ($r_a\sqrt{N} > r_s$), nên chính quy tắc lùa cần thay đổi cho bầy lớn hơn. Mô hình Lama được tái hiện từ văn bản bài báo, và các kết quả ngoài Bảng I được so với hình đã công bố bằng mắt. Các lượt chạy lại chính xác trên cùng máy với các thư viện phụ thuộc đã khóa phiên bản; trên phần cứng khác, vài bit dấu phẩy động cuối cùng có thể khác, điều này có thể làm đổi những lượt hiếm kết thúc đúng ở thời hạn.

## 7 Kết luận

Chúng tôi xác định cỡ đội chăn theo độ tin cậy: đội nhỏ nhất có tỉ lệ thành công ít nhất 0,90 ở độ tin cậy 99%, được ước lượng thích nghi và báo cáo kèm độ bất định. Với bầy gắn kết của Strömbom và cộng sự (2014) do một đội có điều phối lùa, một chó là đủ cho bầy gọn ở mọi cỡ đã xét, và trên bầy tản mát, đội nhỏ nhất tăng chậm hơn tuyến tính, tăng nhiều hơn khi thời hạn chặt hơn so với khi bầy lớn hơn. Điều phối quan trọng ở bầy lớn: công tắc gom/lùa đưa một đội không điều phối tới 200 con, và việc phân công con lạc là cần thiết ở 400 con. Tiêu chí thành công làm đổi câu trả lời. Đòi hỏi mọi con cừu khiến đội nhỏ nhất phụ thuộc vào con cuối cùng và vào những lựa chọn thiết lập tùy ý, còn lấy trung bình qua các lượt thì chấp nhận những đội thường xuyên thất bại gần ngưỡng. Báo cáo tỉ lệ thành công theo lượt kèm khoảng tin cậy tránh được cả hai.

Hướng tiếp theo: một cách phân công có tính đến các cụm, điều mà bố cục `split` đòi hỏi; một con cừu ước lượng tâm bầy từ các con lân cận, để kiểm tra mức tăng chậm đến từ lực hút toàn bầy bao nhiêu; và dữ liệu thực địa với nhiều chó hoặc thiết bị bay, để kiểm tra nhiều người chăn hơn có đẩy bầy mạnh hơn hay không.

---

## 8 Tuyên bố

**Tài trợ.** VIỆC CẦN LÀM.

**Xung đột lợi ích.** Các tác giả không có xung đột lợi ích nào cần khai báo. VIỆC CẦN LÀM: xác nhận.

**Dữ liệu.** Mọi bản ghi lượt chạy, quyết định ô và bảng có tại VIỆC CẦN LÀM (đường dẫn kho mã và mã DOI trên Zenodo).

**Mã nguồn.** Bộ mô phỏng, các giao thức và các tập lệnh phân tích có tại VIỆC CẦN LÀM (đường dẫn kho mã). Mọi lượt chạy đều có thể chạy lại từ cấu hình và hạt giống đã lưu.

**Đóng góp của tác giả.** VIỆC CẦN LÀM.

## 9 Mã nguồn và dữ liệu

Mỗi giao thức là một tệp YAML; mỗi lần chạy lưu mọi lượt và mọi quyết định ô. Các bảng trong bài được sinh ra từ các lần chạy đã lưu. *VIỆC CẦN LÀM: ghi đường dẫn kho mã và lưu trữ phiên bản dùng cho bài báo trên Zenodo.*

---

## Tài liệu tham khảo

Auletta F, Fiore D, Richardson MJ, di Bernardo M (2021) Herding stochastic autonomous agents via local control rules and online global target selection strategies. arXiv:2010.00386

Clopper CJ, Pearson ES (1934) The use of confidence or fiducial limits illustrated in the case of the binomial. Biometrika 26(4):404–413

Jadhav V, Pasqua R, Zanon C, Roy M, Tredan G, Bon R, Guttal V, Theraulaz G (2024) Collective responses of flocking sheep (*Ovis aries*) to a herding dog (border collie). Communications Biology 7:1543

Kubo M, Tashiro M, Sato H, Yamaguchi A (2022) Herd guidance by multiple sheepdog agents with repulsive force. Artificial Life and Robotics 27:416–427

Kuhn HW (1955) The Hungarian method for the assignment problem. Naval Research Logistics Quarterly 2(1–2):83–97

Lama A, di Bernardo M (2024) Shepherding control and herdability in complex multiagent systems. Physical Review Research 6:L032012

Long NK, Sammut K, Sgarioto D, Garratt M, Abbass HA (2020) A comprehensive review of shepherding as a bio-inspired swarm-robotics guidance approach. IEEE Transactions on Emerging Topics in Computational Intelligence 4(4):523–537. VIỆC CẦN LÀM: kiểm tra thông tin.

Pierson A, Schwager M (2015) Bio-inspired non-cooperative multi-robot herding. In: IEEE International Conference on Robotics and Automation (ICRA)

Strömbom D, Mann RP, Wilson AM, Hailes S, Morton AJ, Sumpter DJT, King AJ (2014) Solving the shepherding problem: heuristics for herding autonomous, interacting agents. Journal of the Royal Society Interface 11(100):20140719

Yaxley KJ, Joiner KF, Abbass H (2021) Drone approach parameters leading to lower stress sheep flocking and movement: sky shepherding. Scientific Reports 11:7803
