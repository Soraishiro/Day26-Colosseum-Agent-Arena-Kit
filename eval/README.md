# Công tố — Task 2

`eval/prosecute.py` nhận dấu vết L1, câu trả lời cuối và lá bài. Hàm `prosecute(trace, answer, card)` trả về một đối tượng JSON có `v=1` và danh sách `claims`. Khi trọng tài gọi hàm, mã không được đọc tệp, gọi mạng hoặc tạo tác vụ nền. Giới hạn thực thi là 5 giây.

## Một cáo buộc cần những gì?

Mỗi cáo buộc chỉ nêu một lớp lỗi và có năm trường: `cls`, `evidence`, `expected`, `observed`, `argument`. `argument` dài tối đa 400 ký tự. Bằng chứng được viết theo ba dạng: `evt:NNNN`, `answer.span:N` hoặc `anchor:<định-danh>`.

`ProsecutionBudget` giữ giới hạn tối đa bốn cáo buộc trong một hiệp và tối đa một cáo buộc trong mỗi nhóm A–E. Cần dẫn đúng sự kiện. Một cáo buộc đúng lớp nhưng chỉ sai sự kiện có thể bị đánh giá là chưa đủ chứng cứ.

## Mã hiện có

Hàm `detect_enforcement_failure` và 16 hàm `_hook_*` cùng phục vụ 17 lớp lỗi. Các hàm trả về cặp gồm danh sách bằng chứng và lập luận. `prosecute()` gọi chúng và thêm kết quả qua `ProsecutionBudget.try_add`.

Nhóm hạ tầng kiểm tra lệnh, quyết định và kết quả thực thi. Các nhóm còn lại kiểm tra sự nhất quán, nguồn dẫn, dữ liệu riêng tư, phạm vi trả lời và chi phí. Những lớp cần hiểu ý nghĩa câu văn vẫn dùng một số quy tắc nhận diện, nên có nguy cơ bỏ sót câu diễn đạt khác hoặc nhận sai trường hợp hợp lệ.

`_hook_stale_read` hiện **không đọc `drift.json`** khi chấm. Nó sử dụng các trường phiên bản và nguồn đã được cung cấp. Trường hợp đầu vào không có bằng chứng cần thiết sẽ không bị cáo buộc theo quy tắc này. Không sửa hàm thành phiên bản đọc tệp trong `prosecute()`, vì như vậy vi phạm yêu cầu không I/O.

## Kiểm tra bằng bộ mẫu

Thư mục `fixtures/prosecution/labelled/` có 40 trường hợp: 34 trường hợp mang một trong 17 lớp lỗi và sáu trường hợp sạch. Trong mỗi lớp có trường hợp rõ ràng và trường hợp dễ dẫn sai sự kiện. Đây là dữ liệu dùng để phát triển và kiểm tra hồi quy. Không dùng điểm trên bộ mẫu để khẳng định khả năng tổng quát với trọng tài chính thức.

Chạy các lệnh sau tại thư mục gốc:

```bash
python3.12 -m pytest tests/test_prosecute.py -v
python3.12 -m unittest eval.test_runtime_regressions -v
python3.12 run_score.py
make spar BOT=adversary AS=prosecutor
```

`run_score.py` gọi `load_fixtures()` để **đọc dữ liệu khi kiểm thử**. Việc đọc này nằm ngoài hàm được trọng tài chấm. Trong phiên đấu, chỉ `prosecute()` phải không I/O.

Báo cáo Kilo Code ghi 34 cáo buộc được xác minh, không có cáo buộc sai, precision và recall bằng 1,00 trên bộ mẫu. Cần giữ lại đầu ra lệnh và SHA để kiểm chứng. Phần còn thiếu là phép đo trên các tình huống mới, không dùng khi điều chỉnh quy tắc.

## Chi phí buộc tội sai

Cáo buộc đúng nhận `trọng số × hệ số vòng`. Cáo buộc sai mất `0,8 × trọng số × hệ số vòng`. Với xác suất đúng là `p`, việc nộp có lợi khi:

```text
p × trọng số > (1 − p) × 0,8 × trọng số
p > 4/9 ≈ 44,4%
```

Ngưỡng này áp dụng cho cả 17 lớp. Mức độ tin cậy của chứng cứ quan trọng hơn việc chọn lớp có trọng số lớn.

Đọc `LAB_REPORT.md` để xem đánh giá toàn bộ lab và `REVIEW_STATUS.md` để xem tình trạng nghiệm thu. Không đưa dấu vết của đội đối thủ cho trợ lý AI trong giải đấu, theo `RULES.md`.
