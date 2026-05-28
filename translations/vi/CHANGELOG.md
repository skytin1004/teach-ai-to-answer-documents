# Changelog

## Chưa phát hành

Phạm vi phát hành công khai ban đầu cho **Dạy AI Trả Lời Câu Hỏi Dựa Trên Tài Liệu Của Bạn**.

### Đã thêm

- Bài viết Chuỗi 1 về các quyết định kiến trúc RAG, sự đánh đổi giữa Azure và mã nguồn mở, và vị trí của việc tinh chỉnh.
- Bài viết và sổ tay Chuỗi 2 cho quy trình RAG mã nguồn mở cục bộ sử dụng chế độ cục bộ Qdrant, nhúng cục bộ FastEmbed, tái xếp hạng nhẹ, Ollama và Phi-4-mini.
- Định dạng hướng dẫn từng bước đầu cuối Chuỗi 2 với đoạn mã Python và ghi chú xác minh từ sổ tay đã thực thi.
- Đường đi tạo câu trả lời tùy chọn Chuỗi 2 với Ollama và Phi-4-mini trong khi giữ truy xuất thân thiện với CPU cục bộ làm đường mặc định.
- Xác minh Ollama cục bộ cho Chuỗi 2 sử dụng `phi4-mini:3.8b` trên GPU Laptop RTX 3060.
- Dữ liệu mẫu cho chính sách trường học và hướng dẫn AI khóa học.
- Các file yêu cầu cho sổ tay công khai và xác minh ở cấp độ kho.
- Script xác minh kho cho các liên kết Markdown cục bộ và xác thực/thi hành sổ tay.
- Quy trình làm việc GitHub Actions cho xác minh sổ tay.
- `.env.example` cho thiết lập tạo Ollama cục bộ tùy chọn mà không cam kết cấu hình cục bộ.
- File README cấp thư mục cho bài viết, sổ tay, yêu cầu, dữ liệu mẫu và các script.
- Danh sách kiểm tra xuất bản cho an toàn công khai và xác minh.
- Không gian làm việc bản thảo cho nội dung Azure và đánh giá trong tương lai.

### Đã xác minh

- Xác thực liên kết Markdown cục bộ thành công.
- Sổ tay Chuỗi 2 được xác thực thành công.
- Sổ tay Chuỗi 2 được thi hành thành công trong môi trường xác minh cục bộ.
- Các file sổ tay được giữ không có đầu ra đã lưu hay số lần thực thi.
- Không có bí mật thực sự nào bị cam kết.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Tuyên bố miễn trừ trách nhiệm**:
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng bản dịch tự động có thể chứa lỗi hoặc sai sót. Tài liệu gốc bằng ngôn ngữ gốc nên được coi là nguồn tin chính thức. Đối với thông tin quan trọng, nên sử dụng dịch vụ dịch thuật chuyên nghiệp bởi con người. Chúng tôi không chịu trách nhiệm về bất kỳ hiểu lầm hoặc giải thích sai nào phát sinh từ việc sử dụng bản dịch này.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->