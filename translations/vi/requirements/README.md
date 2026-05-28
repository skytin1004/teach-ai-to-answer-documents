# Yêu cầu

Mỗi bài viết triển khai có một tập tin yêu cầu tập trung.

| Tập tin | Được sử dụng bởi |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | Sổ tay RAG mã nguồn mở Series 2, bao gồm các trợ giúp tạo Ollama tùy chọn |
| [all.txt](../../../requirements/all.txt) | Xác minh cấp kho lưu trữ và CI |

Sử dụng tập tin tập trung khi chạy một sổ tay. Sử dụng `all.txt` khi xác thực toàn bộ kho lưu trữ.

`open-source-rag.txt` và `all.txt` bao gồm `fastembed` cho nhúng cục bộ và `python-dotenv` để Series 2 có thể tùy chọn bật tạo Ollama từ `.env` mà không thay đổi pipeline truy xuất.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Tuyên bố miễn trừ trách nhiệm**:
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng bản dịch tự động có thể chứa lỗi hoặc sai sót. Tài liệu gốc bằng ngôn ngữ gốc nên được coi là nguồn tin chính thức. Đối với thông tin quan trọng, nên sử dụng dịch vụ dịch thuật chuyên nghiệp bởi con người. Chúng tôi không chịu trách nhiệm về bất kỳ hiểu lầm hoặc giải thích sai nào phát sinh từ việc sử dụng bản dịch này.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->