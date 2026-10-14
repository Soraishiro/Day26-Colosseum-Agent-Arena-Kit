# Kiểm tra trước khi nộp Day 26

Hãy thực hiện các bước dưới đây trên máy đã có Python 3.12 và bộ world do giảng viên cấp. Không dùng `truth.json` và không thay đổi `kit/`, `bots/`, `fixtures/`.

## Kiểm tra mã và dữ liệu

```bash
git pull --ff-only origin main
git status -- kit bots fixtures
make install
make doctor
make test
python3.12 -m unittest \
  agent.test_gateway_regressions \
  agent.test_guardrails_regressions \
  eval.test_runtime_regressions -v
python3.12 run_score.py
make validate
```

Nếu có một bài kiểm thử thất bại, ghi tên bài kiểm thử, thông báo lỗi và mã SHA. Không ghi “tất cả đạt” khi vẫn có một bài thất bại. Nếu `make validate` báo `WARN`, đọc nguyên nhân và xem nhật ký đấu; `WARN` không thay thế `PASS` của từng luật cơ học.

## Kiểm tra đấu thử

```bash
make spar BOT=rookie AS=all
make spar BOT=operator AS=all
make spar BOT=adversary AS=all
```

Lưu kết quả, seed, mã SHA, số lần `mutation.applied`, cáo buộc `VERIFIED`, `FALSE`, `MISSED` và kết quả các lượt `blank`. Đối chiếu điểm từng vòng với tổng điểm ở cuối; không sử dụng riêng con số cuối trận để khẳng định hiệu quả.

## Tạo gói nộp

```bash
make submit TEAM=<ten-doi>
```

Lệnh tạo `submissions/<ten-doi>.bundle`. Sau đó, tạo thư mục `K4-DAY26-TenNhom/` và đặt bundle cùng `TEAMMATES.md` trong đó.

Nội dung `TEAMMATES.md` phải ghi họ tên đầy đủ và mã số sinh viên của từng người. Chỉ điền dữ liệu thật do các thành viên xác nhận. Giảng viên quyết định số thành viên và nơi nộp; hai thông tin này chưa được cung cấp trong repository.

## Sáu điều kiện kết thúc

- [ ] `make doctor` kết thúc bằng `ready to spar.`
- [ ] `make test` không có bài thất bại, hoặc giảng viên đã xác nhận ngoại lệ bằng văn bản
- [ ] `make validate` không có `FAIL` trên world chính thức
- [ ] `git status -- kit bots fixtures` không báo thay đổi trái phép
- [ ] Bundle được tạo thành công và kiểm tra được manifest
- [ ] Thư mục nộp có `TEAMMATES.md` đủ thông tin và đúng tên đội

Không đưa trace của đội đối thủ cho trợ lý AI khi thi. Chỉ được dùng trace của đội mình và bộ mẫu công khai để sửa lỗi.
