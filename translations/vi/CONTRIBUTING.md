# Đóng góp

Kho lưu trữ này được tổ chức thành một chuỗi blog cùng với các ví dụ notebook có thể chạy được.

## Trước khi Mở Pull Request

Chạy script kiểm tra cục bộ:

```powershell
python scripts\verify_notebooks.py
```

Đối với các thay đổi về triển khai hoặc notebook, chạy thực thi notebook an toàn cục bộ:

```powershell
python scripts\verify_notebooks.py --execute
```

## Hướng dẫn về Notebook

- Giữ cho các notebook dễ đọc và tập trung vào bài viết liên quan.
- Không cam kết các đầu ra notebook đã lưu hoặc số lần thực thi.
- Sử dụng dữ liệu mẫu nhỏ từ `sample_data/` trừ khi bài viết yêu cầu tài nguyên bên ngoài cụ thể.
- Ghi lại kết quả xác minh trong bài viết liên quan khi có thay đổi hành vi.

## Bí mật và Thông tin đăng nhập

- Không cam kết các khóa API, token, mật khẩu, điểm cuối riêng tư, hoặc các file `.env`.
- Chỉ sử dụng `.env.example` cho các giá trị giữ chỗ.
- Sử dụng biến môi trường cho các thử nghiệm Ollama cục bộ tùy chọn.

## Tài liệu

- Giữ các liên kết điều hướng bài viết luôn cập nhật.
- Cập nhật `README.md` khi thêm bài viết mới, notebook, file yêu cầu hoặc file dữ liệu mẫu.
- Cập nhật `CHANGELOG.md` trước khi công bố cập nhật kho lưu trữ công khai.

## Xác minh

Quy trình làm việc GitHub Actions chạy:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Chất liệu nháp trong `drafts/` bị bỏ qua bởi xác minh kho lưu trữ cho đến khi nó sẵn sàng cho việc lập chỉ mục công khai.

## Vấn đề

Sử dụng mẫu phản hồi bài viết cho các chỉnh sửa bài viết và mẫu vấn đề notebook cho các sự cố thực thi notebook.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Tuyên bố miễn trừ trách nhiệm**:
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng bản dịch tự động có thể chứa lỗi hoặc sai sót. Tài liệu gốc bằng ngôn ngữ gốc nên được coi là nguồn tin chính thức. Đối với thông tin quan trọng, nên sử dụng dịch vụ dịch thuật chuyên nghiệp bởi con người. Chúng tôi không chịu trách nhiệm về bất kỳ hiểu lầm hoặc giải thích sai nào phát sinh từ việc sử dụng bản dịch này.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->