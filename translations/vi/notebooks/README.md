# Notebooks

Những sổ tay này hỗ trợ chuỗi bài viết với các ví dụ có thể chạy được.

| Notebook | Bài viết | Mục đích |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Series 2](../articles/series-2-open-source-rag-end-to-end.md) | RAG mã nguồn mở với FastEmbed, chế độ cục bộ Qdrant, truy xuất, sắp xếp lại, tạo tùy chọn Ollama và tham chiếu nguồn |

## Chạy trên máy cục bộ

Cài đặt các yêu cầu cho sổ tay bạn muốn chạy:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Hoặc cài đặt tất cả các phụ thuộc:

```powershell
python -m pip install -r requirements\all.txt
```

## Xác minh

Từ thư mục gốc của kho:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Series 2 có thể đọc cấu hình Ollama từ tệp `.env` ở thư mục gốc kho. Bắt đầu từ [../.env.example](../../../.env.example), được nhóm theo series.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Tuyên bố miễn trừ trách nhiệm**:
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng bản dịch tự động có thể chứa lỗi hoặc sai sót. Tài liệu gốc bằng ngôn ngữ gốc nên được coi là nguồn tin chính thức. Đối với thông tin quan trọng, nên sử dụng dịch vụ dịch thuật chuyên nghiệp bởi con người. Chúng tôi không chịu trách nhiệm về bất kỳ hiểu lầm hoặc giải thích sai nào phát sinh từ việc sử dụng bản dịch này.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->