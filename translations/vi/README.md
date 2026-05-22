# Dạy AI Trả Lời Câu Hỏi Dựa Trên Tài Liệu Của Bạn

![Tổng quan hệ thống AI RAG dựa trên tài liệu](../../assets/images/readme-hero.svg)

Kho lưu trữ này tập hợp một chuỗi blog năm 2026 về xây dựng hệ thống AI dựa trên tài liệu với RAG, dịch vụ AI Azure, các lựa chọn thay thế mã nguồn mở và quy trình làm việc hướng đến đánh giá.

## Bối cảnh

Vào năm 2023, tôi đã làm việc trên một cặp hướng dẫn về cách dạy ChatGPT trả lời câu hỏi từ tài liệu PDF sử dụng Azure AI Search và Azure OpenAI. Ý tưởng "ChatGPT trên dữ liệu của bạn" vẫn còn mới vào thời điểm đó, và mục tiêu là để trình bày một quy trình thực tế: lưu trữ tài liệu, lập chỉ mục chúng, truy xuất nội dung liên quan, và tạo câu trả lời từ ngữ cảnh đã lấy được.

Vào năm 2026, hệ sinh thái RAG đã phát triển lớn hơn nhiều. Azure AI Search hỗ trợ các mẫu truy xuất vector hiện đại và lai, Azure OpenAI là một phần của hệ sinh thái Mô hình Foundry rộng lớn hơn của Microsoft, và các công cụ mã nguồn mở như LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, và vLLM đã trở thành các lựa chọn thực tiễn cho hệ thống thực tế.

Đó là lý do tôi muốn xem lại chủ đề này. Câu hỏi giờ đây không còn là "Làm thế nào để xây dựng RAG?" mà có rất nhiều cách để xây dựng nó, và câu hỏi quan trọng hơn là "Kiến trúc nào tôi nên chọn cho tình huống của mình?"

Chuỗi bài này bắt đầu từ lớp quyết định đó, rồi biến nó thành các hướng dẫn thực hành. Đường dẫn triển khai đầu tiên xây dựng một hệ thống RAG mã nguồn mở chạy cục bộ mà bất kỳ ai cũng có thể chạy với dữ liệu mẫu, Qdrant, Ollama và Phi-4-mini.

## Các bài viết

Xem [articles/README.md](./articles/README.md) để xem mục lục bài viết.

1. [Chuỗi 1: RAG, Azure so với các lựa chọn thay thế mã nguồn mở, và khi nào việc tinh chỉnh có ý nghĩa](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [Chuỗi 2: Xây dựng hệ thống RAG mã nguồn mở chạy cục bộ từ đầu đến cuối](./articles/series-2-open-source-rag-end-to-end.md)

Sắp tới:

- Xây dựng lại cùng hệ thống RAG với Azure AI Search và Azure OpenAI.
- Thêm bước đánh giá và kiểm tra hồi quy ngoài câu trả lời demo.

## Sổ tay (Notebooks)

Các bài viết triển khai sử dụng sổ tay để có thể trực tiếp kiểm tra các bước truy xuất và đánh giá. Xem hướng dẫn thư mục [notebooks/README.md](./notebooks/README.md).

> [!TIP]
> Bắt đầu với Chuỗi 2 nếu bạn muốn con đường nhanh nhất. Nó chạy cục bộ với dữ liệu mẫu, embedding thân thiện với CPU, chế độ local Qdrant và không cần thông tin đăng nhập đám mây.

| Chuỗi | Sổ tay | Yêu cầu | Xác minh cục bộ |
| --- | --- | --- | --- |
| Chuỗi 2 | [Sổ tay RAG mã nguồn mở](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Xác minh chế độ local Qdrant, truy xuất, sắp xếp lại và kết nối nguồn |

Để chạy sổ tay cục bộ, tạo một môi trường ảo và cài các gói yêu cầu tương ứng. Ví dụ:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## Dữ liệu mẫu

Các sổ tay sử dụng một tập hợp nhỏ dữ liệu cục bộ trong [sample_data](../../sample_data) để các ví dụ có thể chạy mà không cần tài liệu riêng tư hay thông tin đăng nhập đám mây. Xem chi tiết ở [sample_data/README.md](./sample_data/README.md).

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## Tóm tắt xác minh cục bộ

Kết quả xác minh được ghi trong mỗi bài viết và tại [SERIES_PLAN.md](./SERIES_PLAN.md).

| Khu vực | Kết quả |
| --- | --- |
| Đường dẫn mã nguồn mở Chuỗi 2 | FastEmbed sinh embedding cục bộ 384 chiều, bộ sưu tập Qdrant bộ nhớ trong chèn 8 vector, sắp xếp lại nhẹ lấy đúng phần mục tiêu; tạo Ollama tùy chọn hoàn thành với `phi4-mini:3.8b` |

Sổ tay chạy cục bộ tránh chứa bí mật cứng mã hóa.

## Tạo Ollama cục bộ

Sổ tay Chuỗi 2 an toàn chạy cục bộ theo mặc định. Để bật tạo Ollama cục bộ, sao chép [.env.example](../../.env.example) thành `.env` và điền các giá trị Chuỗi 2.

Để tạo Ollama Chuỗi 2, bỏ chú thích:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Sổ tay Chuỗi 2 tự động tải `.env` từ thư mục gốc kho lưu trữ bằng cách sử dụng `python-dotenv`.

> [!IMPORTANT]
> Không cam kết các file `.env`, khóa API, điểm cuối riêng tư, hoặc các giá trị đặc thù tenant. Kho lưu trữ cố ý giữ bí mật tránh xa các file Markdown và sổ tay.

Các file yêu cầu được ghi chú trong [requirements/README.md](./requirements/README.md).

Để kiểm tra các liên kết, cấu trúc sổ tay, sạch đầu ra sổ tay và các mẫu bí mật rủi ro cao:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

Các script kiểm tra được tài liệu trong [scripts/README.md](./scripts/README.md).

Để chạy tất cả các sổ tay an toàn cục bộ trong cùng môi trường:

```powershell
python scripts\verify_notebooks.py --execute
```

Quy trình xác minh tương tự cũng chạy trên GitHub Actions khi đẩy mã, yêu cầu kéo và kích hoạt thủ công workflow. Các bài viết và sổ tay bản nháp được loại trừ khỏi đường xác minh công khai.

Trước khi xuất bản cập nhật, hãy sử dụng [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md).

Xem [CHANGELOG.md](./CHANGELOG.md) để biết tóm tắt thay đổi chưa xuất bản hiện tại.

Để biết hướng dẫn đóng góp và vệ sinh sổ tay, xem [CONTRIBUTING.md](./CONTRIBUTING.md).

## Hỗ trợ đa ngôn ngữ

### Hỗ trợ qua Co-op Translator (Tự động và luôn cập nhật)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Tiếng Ả Rập](../ar/README.md) | [Tiếng Bengal](../bn/README.md) | [Tiếng Bungari](../bg/README.md) | [Tiếng Miến Điện (Myanmar)](../my/README.md) | [Tiếng Trung (Giản thể)](../zh-CN/README.md) | [Tiếng Trung (Phồn thể, Hồng Kông)](../zh-HK/README.md) | [Tiếng Trung (Phồn thể, Macau)](../zh-MO/README.md) | [Tiếng Trung (Phồn thể, Đài Loan)](../zh-TW/README.md) | [Tiếng Croatia](../hr/README.md) | [Tiếng Séc](../cs/README.md) | [Tiếng Đan Mạch](../da/README.md) | [Tiếng Hà Lan](../nl/README.md) | [Tiếng Estonia](../et/README.md) | [Tiếng Phần Lan](../fi/README.md) | [Tiếng Pháp](../fr/README.md) | [Tiếng Đức](../de/README.md) | [Tiếng Hy Lạp](../el/README.md) | [Tiếng Do Thái](../he/README.md) | [Tiếng Hindi](../hi/README.md) | [Tiếng Hungary](../hu/README.md) | [Tiếng Indonesia](../id/README.md) | [Tiếng Ý](../it/README.md) | [Tiếng Nhật](../ja/README.md) | [Tiếng Kannada](../kn/README.md) | [Tiếng Khmer](../km/README.md) | [Tiếng Hàn](../ko/README.md) | [Tiếng Litva](../lt/README.md) | [Tiếng Malay](../ms/README.md) | [Tiếng Malayalam](../ml/README.md) | [Tiếng Marathi](../mr/README.md) | [Tiếng Nepal](../ne/README.md) | [Tiếng Pidgin Nigeria](../pcm/README.md) | [Tiếng Na Uy](../no/README.md) | [Tiếng Ba Tư (Farsi)](../fa/README.md) | [Tiếng Ba Lan](../pl/README.md) | [Tiếng Bồ Đào Nha (Brazil)](../pt-BR/README.md) | [Tiếng Bồ Đào Nha (Bồ Đào Nha)](../pt-PT/README.md) | [Tiếng Punjabi (Gurmukhi)](../pa/README.md) | [Tiếng Romania](../ro/README.md) | [Tiếng Nga](../ru/README.md) | [Tiếng Serbia (Chữ Kirin)](../sr/README.md) | [Tiếng Slovakia](../sk/README.md) | [Tiếng Slovenia](../sl/README.md) | [Tiếng Tây Ban Nha](../es/README.md) | [Tiếng Swahili](../sw/README.md) | [Tiếng Thụy Điển](../sv/README.md) | [Tiếng Tagalog (Phi-líp-pin)](../tl/README.md) | [Tiếng Tamil](../ta/README.md) | [Tiếng Telugu](../te/README.md) | [Tiếng Thái](../th/README.md) | [Tiếng Thổ Nhĩ Kỳ](../tr/README.md) | [Tiếng Ukraina](../uk/README.md) | [Tiếng Urdu](../ur/README.md) | [Tiếng Việt](./README.md)

> **Thích sao chép về máy hơn?**
>
> Kho lưu trữ này bao gồm hơn 50 bản dịch ngôn ngữ làm tăng đáng kể kích thước tải xuống. Để sao chép kho không có bản dịch, hãy sử dụng sparse checkout:
>
> **Bash / macOS / Linux:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (Windows):**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> Điều này cung cấp cho bạn tất cả những gì cần thiết để hoàn thành khóa học với tốc độ tải xuống nhanh hơn nhiều.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Tuyên bố miễn trừ trách nhiệm**:
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng bản dịch tự động có thể chứa lỗi hoặc sai sót. Tài liệu gốc bằng ngôn ngữ gốc nên được coi là nguồn tin chính thức. Đối với thông tin quan trọng, nên sử dụng dịch vụ dịch thuật chuyên nghiệp bởi con người. Chúng tôi không chịu trách nhiệm về bất kỳ hiểu lầm hoặc giải thích sai nào phát sinh từ việc sử dụng bản dịch này.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->