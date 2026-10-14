# Tình trạng nghiệm thu Day 26

**Cập nhật:** 15/10/2026. Nhóm nộp: `VuHieuThien`.

Bộ bài tấn công, cổng kiểm soát lệnh và 17 bộ phát hiện lỗi đều có mã trong repository. Ba hàm bảo vệ đầu ra trước đây còn để trống đã có xử lý thực tế. Sau lần duyệt mã gần nhất, bộ kiểm tra được mở rộng để nhận diện chỉ thị giả mạo, che giá trị bí mật ngắn và phát hiện những kết luận số liệu thiếu căn cứ.

Bộ kiểm tra hồi quy hiện có **35 trường hợp được khai báo**: 22 cho guardrails, tám cho Gateway và năm cho bộ công tố. Đây là số lượng trường hợp trong mã, **không phải số lượng đã chạy thành công**. Tôi chưa có nhật ký chạy Python 3.12 trên đúng commit mới nhất để xác nhận chúng đạt.

Kilo Code từng báo cáo 41 bài kiểm thử công tố đạt, 34 cáo buộc đúng trên 40 vết chạy có nhãn, không có cáo buộc sai, cùng điểm đấu tập 64–0, 92–0 và 54–8. Các con số này chưa có nhật ký độc lập để kiểm tra và được báo cáo trước những thay đổi mới.

Đã tạo `K4-DAY26-VuHieuThien/TEAMMATES.md` cho **Vũ Hiếu Thiên — 2A202602867**. Chưa có bundle. Tại thời điểm kiểm tra, GitHub Releases không có bản world để hoàn tất `make doctor`, `make validate` và `make submit` trong môi trường hiện có. Trên máy Kilo Code, phải dùng bản world chính thức nếu đã được cấp riêng.

**Việc còn lại:** chạy toàn bộ kiểm thử, phân tích bài kiểm thử cách ly mà Kilo Code từng báo thất bại, xác nhận `make validate` không có `FAIL`, bảo đảm không thay `kit/`, `bots/`, `fixtures/` và tạo bundle hợp lệ. Các hàm guardrails vẫn chưa được `kit.loop.agent.Agent` tự gọi trước khi phát `ANSWER`; không được mô tả chúng là lớp bảo vệ tích hợp nếu chưa chứng minh đường gọi đó.

**Kết luận:** Mã và danh sách thành viên đã được cập nhật; bài lab chưa có đủ bằng chứng nghiệm thu và chưa thể kết luận đã nộp thành công.

Đọc thêm `LAB_REPORT.md` và `SUBMISSION_GUIDE.md`.
