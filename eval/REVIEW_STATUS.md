# Tình trạng kiểm tra Day 26

**Cập nhật:** 15/10/2026.

Bộ bài tấn công, chính sách Gateway và 17 bộ phát hiện lỗi hiện có mã trong repository. Ba hàm bảo vệ đầu ra trước đây để trống đã được bổ sung logic kiểm tra; `agent/prompt.md` được viết lại bằng tiếng Việt.

**Điều đã xem xét qua mã:** số lá trong bộ bài, quy tắc cấp quyền theo `ctx.act`, giới hạn công tố, các hàm phát hiện và phạm vi tệp được phép sửa. Đã bổ sung 14 trường hợp kiểm tra mới cho `agent/guardrails.py`, bên cạnh tám trường hợp Gateway và năm trường hợp công tố đã có.

**Điều Kilo Code báo cáo:** 41/41 bài kiểm thử công tố đạt; 13/13 kiểm tra hồi quy cũ đạt; tính điểm trên 40 trường hợp có nhãn đạt 34 cáo buộc đúng, không có cáo buộc sai; đấu với Rookie 64–0, Operator 92–0, Adversary 54–8. Đây là số liệu do tác nhân cục bộ cung cấp. Chưa có nhật ký đầy đủ để xác minh độc lập và các số liệu này có trước thay đổi guardrails mới.

**Chưa nghiệm thu:** bộ kiểm thử tổng thể còn một bài thất bại (Kilo Code báo cáo 4.608 đạt, một thất bại, bảy bỏ qua); 14 kiểm tra mới chưa có đầu ra; chưa chứng minh guardrails được gọi trước `ANSWER`; chưa có nhật ký `make validate` trên world chính thức, bundle và danh sách thành viên. Trong bộ công cụ mẫu, tên `defense_event` và `enforced.verdict_applied` còn khác nhau.

Xem `LAB_REPORT.md` để biết nguyên nhân, rủi ro và lệnh nghiệm thu. Trạng thái: **đã triển khai, chưa hoàn tất nghiệm thu**.
