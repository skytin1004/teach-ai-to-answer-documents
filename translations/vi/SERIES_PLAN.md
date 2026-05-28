# Teach AI to Answer Questions Based on Your Documents - Kế Hoạch Chuỗi

Kế hoạch này theo dõi các phát hành Công khai Chuỗi 1 và Chuỗi 2. Công việc Azure và đánh giá về sau được giữ dưới dạng bản nháp cho đến khi các ví dụ hoàn chỉnh từ đầu đến cuối và được xác minh.

Không được cam kết hoặc đẩy thay đổi cho đến khi được hướng dẫn rõ ràng.

## Phạm Vi Công Khai

Phát hành công khai hiện tại:

- Bài viết Chuỗi 1: các quyết định kiến trúc RAG, các đánh đổi giữa Azure và mã nguồn mở, và vị trí của fine-tuning.
- Bài viết Chuỗi 2: hướng dẫn RAG mã nguồn mở cục bộ.
- Sổ tay Chuỗi 2: phòng thí nghiệm RAG cục bộ có thể chạy với FastEmbed, Qdrant, Ollama, và Phi-4-mini.
- Dữ liệu mẫu: các tập tin Markdown chính sách trường học và hướng dẫn AI khóa học.

Đã soạn thảo nhưng chưa có trong chỉ mục công khai:

- Xây dựng lại Azure AI Search và Azure OpenAI.
- Đánh giá và kiểm tra hồi quy RAG.

## Kịch Bản Hướng Dẫn

Kịch bản chia sẻ là trợ lý chính sách trường học.

Trợ lý trả lời câu hỏi này từ các tài liệu cục bộ:

```text
Can I use generative AI for my final assignment?
```
  
Hành vi mong đợi là:

1. Tải các tài liệu Markdown cục bộ.  
2. Phân tích và chia nhỏ chúng theo tiêu đề.  
3. Tạo embeddings cục bộ và lưu trữ các biểu diễn có thể tìm kiếm với siêu dữ liệu.  
4. Truy xuất phần chính sách phù hợp.  
5. Xếp lại hạng khi cần thiết.  
6. Tạo hoặc tổng hợp câu trả lời dựa trên tài liệu.  
7. Trả về các trích dẫn.  
8. Ghi lại kết quả xác minh.

## Cấu Trúc Công Khai Hiện Tại

```text
.
├── README.md
├── SERIES_PLAN.md
├── articles/
│   ├── README.md
│   ├── series-1-rag-azure-open-source-fine-tuning.md
│   └── series-2-open-source-rag-end-to-end.md
├── notebooks/
│   ├── README.md
│   └── series-2-open-source-rag.ipynb
├── sample_data/
│   ├── README.md
│   ├── course_ai_guidance.md
│   └── school_ai_policy.md
├── requirements/
│   ├── README.md
│   ├── all.txt
│   └── open-source-rag.txt
└── scripts/
    ├── README.md
    └── verify_notebooks.py
```
  
Tài liệu nháp được lưu trong `drafts/` và bị bỏ qua bởi việc xác minh kho lưu trữ cho tới khi sẵn sàng đưa vào chỉ mục công khai.

## Xác Minh Chuỗi 2

Đã xác minh trên Windows với Python 3.12.6.

- Đã cài đặt thành công `requirements/open-source-rag.txt`.  
- Thực thi `notebooks/series-2-open-source-rag.ipynb` với `nbclient`.  
- Xác minh cục bộ thành công: 2 tài liệu mẫu được tải, 8 phân đoạn được tạo, FastEmbed tạo embeddings cục bộ 384 chiều, bộ sưu tập Qdrant trong bộ nhớ được khởi tạo, và 8 vector được chèn.  
- Câu hỏi kiểm tra: "Tôi có thể sử dụng AI tạo nội dung cho bài tập cuối khóa không?"  
- Nguồn được truy xuất hàng đầu sau khi xếp lại hạng nhẹ: `school_ai_policy.md`.  
- Phần được truy xuất hàng đầu sau khi xếp lại hạng nhẹ: `Final Assignments`.  
- Đường dẫn câu trả lời mặc định: bộ soạn câu trả lời minh bạch cục bộ.  
- Ollama được cài đặt qua winget; `phi4-mini:3.8b` được kéo về thành công.  
- Đường dẫn tạo câu trả lời Ollama: hoàn tất với `phi4-mini:3.8b`.  
- Kích thước file mô hình Ollama: khoảng 2.49GB trên đĩa.  
- Kích thước mô hình Ollama đang tải: 3.3GB được báo bởi `ollama ps`.  
- Tải GPU: 100% GPU được báo bởi `ollama ps` trên RTX 3060 Laptop GPU.  
- Bộ nhớ GPU quan sát được sau khi tạo: khoảng 3.5GB trên tổng 6GB.  
- Thực thi sổ tay với mô hình FastEmbed đã được lưu cache và bật tạo Ollama thành công trong khoảng 34 giây qua script xác minh.  
- Quan sát: lần tải tài liệu đầu tiên vô tình bao gồm `sample_data/README.md`; sổ tay bây giờ chỉ tải hai tài liệu mẫu dự kiến một cách rõ ràng.

## Xác Minh Kho Lưu Trữ

- `scripts/verify_notebooks.py` xác thực các liên kết Markdown cục bộ, JSON sổ tay, sự sạch sẽ của đầu ra sổ tay, và các mẫu bí mật rủi ro cao.  
- `scripts/verify_notebooks.py --execute` chạy các sổ tay công khai từ thư mục gốc kho lưu trữ.  
- Tài liệu nháp trong `drafts/` bị bỏ qua một cách có chủ ý.

## Công Việc Tiếp Theo

- Xây dựng lại cùng kịch bản với Azure AI Search và Azure OpenAI trong phần chuỗi tương lai.  
- Thêm truy xuất và đánh giá câu trả lời khi cả hai triển khai cục bộ và Azure đều ổn định.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Tuyên bố miễn trừ trách nhiệm**:
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng bản dịch tự động có thể chứa lỗi hoặc sai sót. Tài liệu gốc bằng ngôn ngữ gốc nên được coi là nguồn tin chính thức. Đối với thông tin quan trọng, nên sử dụng dịch vụ dịch thuật chuyên nghiệp bởi con người. Chúng tôi không chịu trách nhiệm về bất kỳ hiểu lầm hoặc giải thích sai nào phát sinh từ việc sử dụng bản dịch này.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->