# Scripts

Thư mục này chứa các script kiểm tra kho lưu trữ.

## `verify_notebooks.py`

Xác thực các liên kết Markdown nội bộ, JSON sổ tay, độ sạch của đầu ra sổ tay, và các mẫu bí mật nguy cơ cao:

```powershell
python scripts\verify_notebooks.py
```

Thực thi tất cả các sổ tay an toàn nội bộ công khai:

```powershell
python scripts\verify_notebooks.py --execute
```

Quy trình làm việc GitHub Actions sử dụng cùng một script.

Tài liệu nháp trong `drafts/` sẽ bị bỏ qua cho đến khi sẵn sàng cho chỉ mục công khai.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Tuyên bố miễn trừ trách nhiệm**:
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng bản dịch tự động có thể chứa lỗi hoặc sai sót. Tài liệu gốc bằng ngôn ngữ gốc nên được coi là nguồn tin chính thức. Đối với thông tin quan trọng, nên sử dụng dịch vụ dịch thuật chuyên nghiệp bởi con người. Chúng tôi không chịu trách nhiệm về bất kỳ hiểu lầm hoặc giải thích sai nào phát sinh từ việc sử dụng bản dịch này.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->