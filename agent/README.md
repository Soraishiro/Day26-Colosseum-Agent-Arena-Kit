# Bộ phận phòng thủ

Thư mục `agent/` chứa quy tắc xử lý lệnh công cụ và các phép kiểm tra câu trả lời. Hai nhiệm vụ này khác nhau. `Gateway.decide` xử lý lệnh `MCP`, `A2A` và `DISCOVER`; lệnh `ANSWER` đi qua đường xử lý riêng.

| Tệp | Chức năng thực tế | Giới hạn |
|---|---|---|
| `gateway.py` | Kiểm tra quyền người học, phạm vi ghi, header, mã thuê, đích A2A và chi phí ước tính; trả `Decision` | Không xem nội dung câu trả lời, không trực tiếp chạy công cụ |
| `strategy.py` | Các hàm hỗ trợ chọn công cụ, bản dữ liệu và ngân sách | Một số hàm chỉ được dùng khi nơi gọi kết nối chúng |
| `guardrails.py` | Kiểm tra mã nguồn được dẫn, phát hiện chỉ thị cài, che dữ liệu riêng tư và kiểm tra phép tính/số liệu | Không tự chạy trên `ANSWER`; cần bộ điều phối gọi |
| `telemetry.py` | Lưu sự kiện nội bộ để tìm nguyên nhân lỗi | Nhật ký riêng không thay thế sự kiện L1 của trọng tài |
| `prompt.md` | Hướng dẫn mô hình chọn công cụ và trình bày câu trả lời | Chỉ có hiệu lực khi được ghép vào thông điệp hệ thống |
| `test_gateway_regressions.py` | Kiểm tra quyền, mã thuê, A2A và chi phí | Bài kiểm thử đơn vị, không phải kết quả đấu |
| `test_guardrails_regressions.py` | Kiểm tra phát hiện chỉ thị, che dữ liệu và xử lý số liệu | Không chứng minh khả năng ngăn mọi kiểu tấn công |

## Giới hạn quyền truy cập

Quyền của lệnh ghi xuất phát từ `ctx.act`, tức người học mà hệ thống đại diện. Không suy quyền từ `ctx.sub`, tức danh tính của trợ lý. Lệnh ghi phải có quyền phù hợp và hai header `If-Match`, `Idempotency-Key`. Lệnh đọc trang cần mã thuê còn hiệu lực.

Công cụ chỉ được chuyển tiếp khi có căn cứ. Tuy nhiên, không từ chối hàng loạt lệnh đọc hợp lệ: ở lượt không có tấn công, việc từ chối nhầm cũng bị tính lỗi.

## Kiểm tra câu trả lời

`check_grounding(answer, retrieved_anchors)` kiểm tra cú pháp và sự hiện diện của nguồn đã được truy xuất. Nó không chứng minh mọi mệnh đề trong câu là đúng. `scan_for_injected_instructions(text)` chỉ báo dấu hiệu đáng ngờ, không phải lệnh từ chối tự động. `redact(text, private_values=...)` che các giá trị riêng tư được cung cấp từ nguồn đáng tin cậy; hàm không thể tự biết mọi trường bí mật khi chỉ nhận văn bản. `verify_arithmetic(text, source_text=...)` kiểm tra phép tính và sự hiện diện của số liệu trong nguồn. Nếu không có đủ dữ liệu để kiểm tra, hàm trả về trạng thái chưa xác minh.

`abstention_policy` cân nhắc nguồn được dẫn, trường bắt buộc, phép tính đã xác minh và mâu thuẫn chưa giải quyết. Khi từ chối, cần nêu rõ phần thiếu chứng cứ. Không coi một câu hỏi sạch là nguy hiểm chỉ vì nội dung có nhắc tới an toàn hoặc tấn công.

**Giới hạn tích hợp:** Bộ vòng lặp `kit/loop/agent.py` không tự gọi những hàm này khi phát `ANSWER`. Bộ kiểm thử tập trung chỉ chứng minh hành vi của hàm, không chứng minh hệ thống đấu đã áp dụng bước kiểm tra đầu ra. Muốn kiểm chứng việc sử dụng trong một phiên chạy thật, phải quan sát đường phát `ANSWER` hoặc kết quả của bộ điều phối có gắn kiểm tra đó.

## Lệnh kiểm tra

```bash
python3.12 -m unittest agent.test_gateway_regressions agent.test_guardrails_regressions -v
make test
make spar BOT=rookie AS=defender
make spar BOT=operator AS=defender
make spar BOT=adversary AS=defender
```

Mọi thay đổi ở `agent/` phải giữ quy định thư viện chuẩn, không gọi mạng và không đọc tệp trong `Gateway.decide`.
