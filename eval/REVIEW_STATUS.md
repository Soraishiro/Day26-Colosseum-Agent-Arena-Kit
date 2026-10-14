# Kiểm tra tích hợp Day 26 — 14/10/2026

## Phạm vi

Đối chiếu thay đổi từ `dea32c05b4718f1555088fbdeebe1c49cb9a2cb3` tới `2a60d3180ccf9a26045768746be64fe5fe4039d1`, tập trung vào `eval/prosecute.py` và hợp đồng chấm điểm trong `RULES.md`.

## Những gì đã xác minh từ GitHub

- `eval/prosecute.py` có đủ 16 hàm `_hook_*` và hàm `detect_enforcement_failure` cho lớp lỗi thứ 17. Phần gọi `ProsecutionBudget.try_add` đã được kết nối với các hàm phát hiện.
- Sáu tệp JSONL có nhãn trong `fixtures/prosecution/labelled/` chứa **40 trường hợp** (6 không lỗi; 34 trường hợp dương tính/đối chứng gần đúng cho 17 lớp).
- Các bài kiểm thử có sẵn được khai báo trong `tests/test_prosecute.py`; những tên kiểm thử không phải bằng chứng rằng quá trình chạy thành công.
- Bộ phát hiện sử dụng quy tắc và dấu hiệu ngôn ngữ, chưa thể chứng minh 100% độ chính xác/độ bao phủ ngoài 40 trường hợp có nhãn.
- Các kết quả `41 tests pass`, `perfect recall`, `64 damage / 0 damage` hiện chỉ là báo cáo từ tác nhân cục bộ; chưa có đầu ra lệnh chạy hoặc GitHub Actions xác nhận độc lập.

## Lỗi có thể tái hiện bằng phân tích mã

1. `_hook_stale_read` gọi `_load_drift()`, từ đó đọc `kit/world/df8c55dabb35/drift.json` mỗi khi chạy `prosecute()`, bất kể có trường hợp stale_read hay không. Điều này trái yêu cầu không I/O trong hàm chấm. Khi không có world export, lời gọi phát sinh `FileNotFoundError`.
2. `_hook_write_violation` trước đây có thể lập cáo buộc từ `command` dù Gateway đã `deny`, hoặc mặc định chấp nhận nếu chỉ có một trong hai header.
3. `_hook_authority_exceeded` dùng `exchange_start.defender` làm định danh người học, trong khi `spar.py` dùng trường đó làm **tên đội phòng thủ**.
4. `_hook_protocol_misuse` không nhận `lease_used=False` là thiếu lease, chỉ nhận `None` hoặc chuỗi rỗng.

## Biện pháp đã đưa vào mã

- Loại bỏ truy cập `drift.json` khỏi đường chạy `prosecute()`. Chỉ đưa ra cáo buộc stale khi lời đáp công khai chính nó báo `fresher=w`, `delta>0`, cặp anchor của cùng deck và bằng chứng trong `tool_result`. Đây là lựa chọn bảo thủ, có thể bỏ sót trường hợp thiếu metadata.
- Chỉ ghi nhận vi phạm ghi khi lời gọi **thực sự được thực thi thành công**; cả `If-Match` và `Idempotency-Key` đều bắt buộc. Không coi lặp an toàn cùng tham số là vi phạm.
- Xác định người học từ `act` / `learner` đáng tin cậy, hoặc `exchange_start.defender` chỉ nếu đó đúng là định danh `Learner:`; nếu thiếu bằng chứng thì không lập cáo buộc.
- Xem `lease_used=False` là thiếu lease.
- Tạo `eval/test_runtime_regressions.py` với 5 phép thử sử dụng `unittest`. Chạy bằng `python -m unittest eval.test_runtime_regressions -v`.

## Phần chưa đạt điều kiện nghiệm thu

- Chưa chạy được `make doctor`, `make test`, `make validate`, `make spar` trong môi trường kiểm tra: không có Python 3.12 / bản học liệu thực trên máy công cụ; GitHub Releases của repository hiện trả về danh sách rỗng.
- Chưa có kết quả chấm đối đầu chính thức. `spar.py` dùng `MockBroker` và không chấm đủ tám lớp lỗi ngữ nghĩa.
- Chưa kiểm định `precision/recall/F1` trên bộ giữ lại độc lập, chưa đo sai số qua nhiều seed, chưa so sánh với phiên bản trước trên cùng điều kiện.
- `agent/gateway.py` đã được bổ sung chính sách kiểm tra quyền theo `ctx.act`, xác thực A2A, lease, header ghi và ước tính chi phí; có tám kiểm tra hồi quy tại `agent/test_gateway_regressions.py`. Các kiểm tra này **chưa được chạy trên repository đầy đủ**, nên chưa xác nhận phòng thủ hoàn chỉnh.

## Lệnh kiểm tra cho máy đã có world

```bash
git pull --ff-only origin main
python3.12 -m unittest eval.test_runtime_regressions agent.test_gateway_regressions -v
make install
make doctor
make test
make validate
python3.12 run_score.py
make spar BOT=rookie AS=all
make spar BOT=operator AS=all
make spar BOT=adversary AS=all
make submit TEAM=<ten-doi>
```

Lưu stdout, stderr, exit code và mã SHA của từng lượt chạy. Không coi dữ liệu mô phỏng là điểm thi chính thức. Nếu mất world, không tự thêm `truth.json` hoặc thay `kit/` để vượt qua cổng kiểm tra.
