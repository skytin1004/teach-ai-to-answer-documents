# Danh sách kiểm tra khi xuất bản

Sử dụng danh sách kiểm tra này trước khi cam kết hoặc đẩy các cập nhật công khai.

## An toàn

- Xác nhận không có khóa API, mã thông báo, mật khẩu hoặc điểm cuối riêng tư nào được ghi vào các tệp Markdown, sổ tay, dữ liệu mẫu hoặc kịch bản.
- Giữ thông tin đăng nhập trong biến môi trường hoặc nhận diện được quản lý, không giữ trong các tệp đã cam kết.
- Không cam kết các tệp `.env` hoặc các tệp đầu ra sổ tay thực thi.
- Giữ `.env.example` chỉ có chỗ giữ chỗ.

## Xác minh

Chạy kịch bản xác minh kho lưu trữ:

```powershell
python scripts\verify_notebooks.py
```

Chạy thực thi đầy đủ sổ tay an toàn cục bộ trước khi xuất bản các thay đổi triển khai:

```powershell
python scripts\verify_notebooks.py --execute
```

Các kiểm tra dự kiến:

- các liên kết Markdown cục bộ vượt qua
- xác thực JSON sổ tay vượt qua
- sổ tay không chứa đầu ra đã lưu hoặc số lần thực thi
- quét mẫu bí mật có rủi ro cao vượt qua
- sổ tay công khai thực thi cục bộ
- tài liệu thảo luận trong `drafts/` được bỏ qua có chủ ý

## Rà soát

- Xác nhận các liên kết bài viết README trỏ đến các tệp dự kiến.
- Xác nhận mỗi bài viết có điều hướng kho lưu trữ và liên kết sổ tay liên quan.
- Xác nhận các bản thảo không được liên kết từ các chỉ mục công khai trừ khi chúng đã sẵn sàng xuất bản.
- Xác nhận mẫu vấn đề và yêu cầu kéo GitHub vẫn phù hợp với quy trình làm việc kho lưu trữ.
- Xác nhận kết quả xác minh trong bài viết khớp với đầu ra sổ tay mới nhất.
- Xác nhận quy trình làm việc GitHub Actions dự kiến chạy sau khi đẩy.
- Xác nhận `CHANGELOG.md` phản ánh cập nhật được xuất bản.
- Xác nhận `CONTRIBUTING.md` vẫn phù hợp với quy trình làm việc kho lưu trữ.

## Git

- Xem xét `git status --short --branch`.
- Xem xét `git diff --stat`.
- Cam kết và đẩy chỉ khi rõ ràng đã sẵn sàng.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Tuyên bố miễn trừ trách nhiệm**:
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng bản dịch tự động có thể chứa lỗi hoặc sai sót. Tài liệu gốc bằng ngôn ngữ gốc nên được coi là nguồn tin chính thức. Đối với thông tin quan trọng, nên sử dụng dịch vụ dịch thuật chuyên nghiệp bởi con người. Chúng tôi không chịu trách nhiệm về bất kỳ hiểu lầm hoặc giải thích sai nào phát sinh từ việc sử dụng bản dịch này.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->