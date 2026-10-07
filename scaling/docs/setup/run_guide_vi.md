# Hướng dẫn chạy

Chạy lệnh từ `/home/gwen/HerdSim`. Makefile đặt `PYTHONPATH` và gọi `scaling/scripts/campaign.py`.

## Kiểm tra và thử

```bash
make -C scaling help
uv run scaling/scripts/campaign.py help
make -C scaling scaling-test
```

Mục tiêu đúng đắn chạy:

```bash
uv run pytest tests/backend/correctness/test_scaling_stack.py -q
```

Số worker mặc định là 18 cho máy chủ được ghi trong `scaling/Makefile`. Trên máy nhỏ hơn, ghi đè ví dụ `WORKERS=4`.

## Giai đoạn 1: kích thước cơ sở

```bash
make -C scaling scaling-pilot
make -C scaling scaling-scout
make -C scaling scaling-claim-plan
make -C scaling scaling-claim-reseed
make -C scaling scaling-analyse PROTOCOL=phase1_claim PACKAGE=A
make -C scaling scaling-t1-plan
make -C scaling scaling-t1
```

Dùng đúng thứ tự này. Pilot là kiểm tra khói. Scout lập bản đồ toàn lưới. Lập kế hoạch claim ghi lựa chọn ô nhưng không chạy mô phỏng. Gieo lại claim thực thi các ô đó và tạo tập dữ liệu claim đã hợp nhất. Lập kế hoạch và thực thi T1 chỉ có điều kiện khi phát hiện quá tải.

Bản đồ cơ sở đã hoàn thành không có ô quá tải, nên T1 Giai đoạn 1 không được chạy. Không chạy T1 chỉ để lấp thư mục trừ khi bộ lập kế hoạch của giao thức chỉ ra các ô.

## Giai đoạn 2: cấu trúc ban đầu

```bash
make -C scaling scaling-pilot-state
make -C scaling scaling-phase2-scout
make -C scaling scaling-phase2-claim-plan
make -C scaling scaling-phase2-claim-reseed
make -C scaling scaling-analyse PROTOCOL=phase2_claim PACKAGE=B
```

Mỗi bố cục và N nhận cửa sổ biên riêng.

## Giai đoạn 4: bộ điều khiển chuyển giao

Chạy chiến dịch kích thước và cấu trúc riêng cho Kubo và FAT:

```bash
make -C scaling scaling-transfer-size-scout TRANSFER_METHOD=kubo
make -C scaling scaling-transfer-size-claim-plan TRANSFER_METHOD=kubo
make -C scaling scaling-transfer-size-claim-reseed TRANSFER_METHOD=kubo
make -C scaling scaling-transfer-structure-scout TRANSFER_METHOD=kubo
make -C scaling scaling-transfer-structure-claim-plan TRANSFER_METHOD=kubo
make -C scaling scaling-transfer-structure-claim-reseed TRANSFER_METHOD=kubo
```

Lặp lại với `TRANSFER_METHOD=fat`. Gói D được tổng hợp chung sau khi các bản đồ bắt buộc đã có.

## Giai đoạn 5: thang thông tin

Quan sát:

```bash
make -C scaling scaling-factor-sweep
make -C scaling scaling-phase5-obs-claim-plan
make -C scaling scaling-phase5-obs-claim-reseed
```

Tầm cảm biến:

```bash
make -C scaling scaling-phase5-range-scout
make -C scaling scaling-phase5-range-claim-plan
make -C scaling scaling-phase5-range-claim-reseed
```

Giao tiếp:

```bash
make -C scaling scaling-phase5-comm-scout
make -C scaling scaling-phase5-comm-claim-plan
make -C scaling scaling-phase5-comm-claim-reseed
```

Các thang này là chiến dịch riêng, không phải tích Descartes.

## Lệnh chiến dịch trực tiếp

Dạng chung:

```bash
uv run scaling/scripts/campaign.py VERB --protocol PROTOCOL_ID [OPTIONS]
```

Các động từ là `run`, `claim-plan`, `claim-reseed`, `t1-plan`, `t1`, và `analyse`. Định danh giao thức được resolve dưới `scaling/configs/protocols/`.

Ví dụ:

```bash
uv run scaling/scripts/campaign.py run --protocol phase1_scout --workers 8
uv run scaling/scripts/campaign.py claim-plan --protocol phase1_claim
uv run scaling/scripts/campaign.py claim-reseed --protocol phase1_claim --workers 8
uv run scaling/scripts/campaign.py analyse --protocol phase1_claim --package A
```

Các tùy chọn hữu ích gồm `--output`, `--workers`, `--upstream-trials`, `--no-analyse`, `--package`, `--trials`, `--methods`, `--layouts`, `--n`, `--d`, `--seeds`, `--max-ticks`, `--no-timeseries`, và `--no-resume`.

Biến Make ánh xạ tới các bộ lọc phổ biến:

```bash
make -C scaling scaling-scout WORKERS=4 SCALING_N=100 SCALING_D=1 SCALING_SEEDS=2
make -C scaling scaling-analyse PROTOCOL=phase1_claim PACKAGE=F \
  TRIALS=scaling/results/phase1/claim/merged_trials.csv
```

Bộ lọc và ghi đè seed hữu ích cho chẩn đoán. Một lần chạy đã lọc không phải chiến dịch đóng băng đầy đủ và không được trình bày như vậy.

## Tiếp tục

Tiếp tục được bật mặc định. Chạy lại cùng lệnh trên cùng thư mục đầu ra. Bộ chạy đọc `manifest.jsonl` và bỏ qua khóa lần thử có `status=ok`. Khóa lần thử gồm N, D, seed, bố cục, phương pháp, và mọi nhân tố quan sát, tầm, hoặc giao tiếp.

```bash
make -C scaling scaling-scout
```

Kiểm tra `status.json` trước và sau khi tiếp tục. Tệp ghi các trường đã lập kế hoạch, đã hoàn thành, đang chờ lúc bắt đầu, đang chạy, và dấu thời gian. Tránh `--no-resume` trừ khi cần thực thi mới có chủ đích, vì tùy chọn này tắt việc bỏ qua khóa đã xong.

## Phân tích lần thử có sẵn

```bash
make -C scaling scaling-analyse \
  PROTOCOL=phase1_claim \
  PACKAGE=A \
  TRIALS=scaling/results/phase1/claim/merged_trials.csv
```

`TRIALS` và `OUT` là biến Make tùy chọn. Với một giao thức, chọn đầu vào mặc định theo cách nối chiến dịch. Phân tích trực tiếp không có giao thức cần cả `--trials` và `--output`.

Các gói tương ứng kế hoạch:

- A: biên kích thước cơ sở và độ tin cậy.
- B: cấu trúc.
- C: cơ chế.
- D: chuyển giao.
- E: thay thế thông tin.
- F: khớp scaling.
- G: cảnh báo sớm.

Gói C, F, và G chủ yếu phân tích dữ liệu đã thu. G cần chuỗi thời gian đã lưu. Giao thức scout thường đặt `store_timeseries: false` để giảm I/O đĩa; giao thức claim đặt true cho quỹ đạo biên.

## Đầu ra

Thư mục đầu ra của một giao thức thường chứa:

| Artifact | Ý nghĩa |
|---|---|
| `protocol.yaml` | Công thức đã resolve được sao chép cho lần chạy |
| `provenance.json` | Dấu giao thức, danh sách seed, siêu dữ liệu mã và máy chủ, định danh chỉ số, và dấu thời gian |
| `manifest.jsonl` | Nhật ký tiếp tục; khóa lần thử thành công có `status=ok` |
| `status.json` | Số đã lập kế hoạch và đã hoàn thành kèm dấu thời gian chạy |
| `trials.csv` | Một dòng mỗi mô phỏng |
| `boundary_cells.csv` | Lựa chọn lập kế hoạch claim, khi áp dụng |
| `merged_trials.csv` | Dòng claim thay dòng scout tại ô gieo lại |
| `timeseries/*.parquet` | Quỹ đạo theo lần thử khi được bật |
| `packages/` | Bảng và hình đã xuất |
| `README.md` | Ghi chú chạy cho người và liên kết |

Vị trí điển hình:

```text
scaling/results/phase1/pilot/
scaling/results/phase1/scout/
scaling/results/phase1/claim/
scaling/results/phase1/t1/
scaling/results/phase2/{pilot_state,scout,claim}/
scaling/results/phase4/{kubo,fat}_{size,structure}/{scout,claim}/
scaling/results/phase5/
```

## Nguồn gốc và cách đọc

Trước khi trích một kết quả:

1. Xác nhận `status.json` báo hoàn thành.
2. Xác nhận `protocol.yaml` đã sao chép có đúng giao thức, cấp độ, nhân tố, và số seed kỳ vọng.
3. Giữ `provenance.json` và `manifest.jsonl`.
4. Dùng `merged_trials.csv` cho phân tích claim, không nối tay.
5. Xác nhận báo cáo ghi bằng chứng cấp CLAIM.
6. Coi D = 35 là trần lưới khi D_overcrowd trống.
7. Ghi rõ giai đoạn có điều kiện bị bỏ qua, gồm cả điều kiện kích hoạt.

Hình scout có thể hướng dẫn lập kế hoạch nhưng không nâng được một claim. Thư mục giao thức là đơn vị nguồn gốc: công thức đã resolve và bản ghi máy của nó ưu tiên hơn ví dụ tổng quát trong văn bản.
