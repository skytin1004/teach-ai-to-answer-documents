# Dạy AI Trả Lời Câu Hỏi Dựa Trên Tài Liệu Của Bạn

Kho lưu trữ này tập hợp một chuỗi bài viết năm 2026 về việc xây dựng các hệ thống AI dựa trên tài liệu với RAG, dịch vụ AI Azure, các lựa chọn mã nguồn mở và quy trình làm việc hướng đến đánh giá.

## Bối Cảnh

Năm 2023, tôi đã thực hiện một cặp hướng dẫn về việc dạy ChatGPT trả lời câu hỏi từ tài liệu PDF sử dụng Azure AI Search và Azure OpenAI. Ý tưởng "ChatGPT trên dữ liệu của bạn" khi đó vẫn còn mới, và mục tiêu là trình bày một quy trình thực tiễn: lưu trữ tài liệu, lập chỉ mục chúng, truy xuất nội dung liên quan và tạo câu trả lời từ ngữ cảnh được truy xuất đó.

Năm 2026, hệ sinh thái RAG đã lớn hơn rất nhiều. Azure AI Search hỗ trợ các mô hình truy xuất vector và lai hiện đại, Azure OpenAI là một phần của hệ sinh thái Microsoft Foundry Models rộng lớn hơn, và các công cụ mã nguồn mở như LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama và vLLM đã trở thành những lựa chọn thực tiễn cho các hệ thống thật.

Đó là lý do tôi muốn quay lại chủ đề này. Câu hỏi không còn chỉ là "Làm thế nào để xây dựng RAG?" nữa. Hiện nay có nhiều cách để xây dựng nó, và câu hỏi quan trọng hơn là "Kiến trúc nào nên được chọn cho tình huống của tôi?"

Chuỗi bài này bắt đầu từ lớp quyết định đó. Trước khi đi sâu vào triển khai, nó xem xét lý do dịch vụ AI cần truy xuất, khi nào các dịch vụ do Azure quản lý là hợp lý, khi nào các lựa chọn mã nguồn mở thích hợp hơn, và vị trí của tinh chỉnh mô hình.

## Các Bài Viết

1. [Chuỗi 1: RAG, Azure so với Lựa chọn Mã nguồn mở, và Khi Nào Tinh Chỉnh Có Ý Nghĩa](./series-1-rag-azure-open-source-fine-tuning.md)

## Hỗ Trợ Đa Ngôn Ngữ

### Hỗ Trợ Qua Co-op Translator (Tự Động và Luôn Cập Nhật)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Tiếng Ả Rập](../ar/README.md) | [Tiếng Bengal](../bn/README.md) | [Tiếng Bungary](../bg/README.md) | [Tiếng Myanmar (Miến Điện)](../my/README.md) | [Tiếng Trung (Giản Thể)](../zh-CN/README.md) | [Tiếng Trung (Phồn Thể, Hồng Kông)](../zh-HK/README.md) | [Tiếng Trung (Phồn Thể, Macau)](../zh-MO/README.md) | [Tiếng Trung (Phồn Thể, Đài Loan)](../zh-TW/README.md) | [Tiếng Croatia](../hr/README.md) | [Tiếng Séc](../cs/README.md) | [Tiếng Đan Mạch](../da/README.md) | [Tiếng Hà Lan](../nl/README.md) | [Tiếng Estonia](../et/README.md) | [Tiếng Phần Lan](../fi/README.md) | [Tiếng Pháp](../fr/README.md) | [Tiếng Đức](../de/README.md) | [Tiếng Hy Lạp](../el/README.md) | [Tiếng Hebrew](../he/README.md) | [Tiếng Hindi](../hi/README.md) | [Tiếng Hungary](../hu/README.md) | [Tiếng Indonesia](../id/README.md) | [Tiếng Ý](../it/README.md) | [Tiếng Nhật](../ja/README.md) | [Tiếng Kannada](../kn/README.md) | [Tiếng Khmer](../km/README.md) | [Tiếng Hàn](../ko/README.md) | [Tiếng Litva](../lt/README.md) | [Tiếng Mã Lai](../ms/README.md) | [Tiếng Malayalam](../ml/README.md) | [Tiếng Marathi](../mr/README.md) | [Tiếng Nepal](../ne/README.md) | [Tiếng Pidgin Nigeria](../pcm/README.md) | [Tiếng Na Uy](../no/README.md) | [Tiếng Ba Tư (Farsi)](../fa/README.md) | [Tiếng Ba Lan](../pl/README.md) | [Tiếng Bồ Đào Nha (Brazil)](../pt-BR/README.md) | [Tiếng Bồ Đào Nha (Bồ Đào Nha)](../pt-PT/README.md) | [Tiếng Punjabi (Gurmukhi)](../pa/README.md) | [Tiếng Rumani](../ro/README.md) | [Tiếng Nga](../ru/README.md) | [Tiếng Serbia (Chữ Cyrillic)](../sr/README.md) | [Tiếng Slovakia](../sk/README.md) | [Tiếng Slovenia](../sl/README.md) | [Tiếng Tây Ban Nha](../es/README.md) | [Tiếng Swahili](../sw/README.md) | [Tiếng Thụy Điển](../sv/README.md) | [Tiếng Tagalog (Filipino)](../tl/README.md) | [Tiếng Tamil](../ta/README.md) | [Tiếng Telugu](../te/README.md) | [Tiếng Thái](../th/README.md) | [Tiếng Thổ Nhĩ Kỳ](../tr/README.md) | [Tiếng Ukraina](../uk/README.md) | [Tiếng Urdu](../ur/README.md) | [Tiếng Việt](./README.md)

> **Ưu Tiên Clone Local?**
>
> Kho lưu trữ này bao gồm hơn 50 bản dịch ngôn ngữ, điều này làm tăng đáng kể kích thước tải xuống. Để clone mà không tải bản dịch, sử dụng sparse checkout:
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
> Điều này cung cấp cho bạn mọi thứ cần thiết để hoàn thành khóa học với tốc độ tải nhanh hơn nhiều.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Tuyên bố miễn trừ trách nhiệm**:
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng bản dịch tự động có thể chứa lỗi hoặc sai sót. Tài liệu gốc bằng ngôn ngữ gốc nên được coi là nguồn tin chính thức. Đối với thông tin quan trọng, nên sử dụng dịch vụ dịch thuật chuyên nghiệp bởi con người. Chúng tôi không chịu trách nhiệm về bất kỳ hiểu lầm hoặc giải thích sai nào phát sinh từ việc sử dụng bản dịch này.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->