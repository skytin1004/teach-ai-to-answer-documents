# Dạy AI Trả Lời Câu Hỏi Dựa Trên Tài Liệu Của Bạn
## Phần 2: Xây dựng Hệ Thống RAG Mã Nguồn Mở Cục Bộ Từ Đầu Đến Cuối

![Local open-source RAG tutorial pipeline](../../../assets/images/series-2-local-rag.svg)

> Bài viết này biến thảo luận kiến trúc của Phần 1 thành một hướng dẫn chạy được về RAG cục bộ. Mục tiêu là xây dựng đầy đủ quy trình làm việc trước với dữ liệu mẫu, không cần tài khoản đám mây, không cần bí mật, rồi dùng cơ sở hoạt động đó để quyết định kiến trúc tốt hơn về sau.

Hệ thống chúng ta sẽ xây dựng là một trợ lý chính sách trường học nhỏ. Tôi dùng hai tài liệu Markdown cục bộ làm cơ sở tri thức, rồi đi qua toàn bộ đường ống RAG: chia đoạn, nhúng cục bộ, lưu vectơ Qdrant, truy xuất, sắp xếp lại, tạo câu trả lời có nguồn biết, và tùy chọn sinh câu trả lời cục bộ với Ollama và Phi-4-mini.

Điều hướng chuỗi bài: [Trang chủ kho lưu trữ](../README.md) | Trước: [Phần 1 - RAG, Azure vs Các lựa chọn Mã nguồn mở, và Khi nào Việc Tinh chỉnh Hợp lý](./series-1-rag-azure-open-source-fine-tuning.md)

Notebook: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Yêu cầu: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> Đây là điểm bắt đầu tốt nhất nếu bạn muốn hiểu quy trình RAG trước khi tạo tài nguyên đám mây. Đường dẫn mặc định chạy cục bộ với nhúng thân thiện CPU và không có bí mật.

## 1. Chúng Ta Đang Xây Dựng Gì

Trong hướng dẫn 2023, tôi bắt đầu từ Azure vì mục tiêu là cho thấy Azure AI Search và Azure OpenAI có thể trả lời câu hỏi từ tài liệu PDF như thế nào.

Với chuỗi 2026 này, tôi muốn bắt đầu từ một tầng thấp hơn.

Trước khi dùng dịch vụ quản lý, tôi muốn xây một hệ thống RAG nhỏ cục bộ và làm rõ từng bước: tải tài liệu, chia đoạn, lưu vectơ, truy xuất bằng chứng, sắp xếp lại kết quả, và trả lời có nguồn tham khảo.

Tình huống mẫu là trợ lý chính sách trường học. Người dùng hỏi:

```text
Can I use generative AI for my final assignment?
```

Hệ thống không nên trả lời từ bộ nhớ mô hình tổng quát. Nó nên truy xuất phần chính sách liên quan và trả lời từ bằng chứng đó.

Phiên bản chạy được đầy đủ có trong [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). Mã dưới đây trình bày các bước chính để bài viết có thể được đọc như một hướng dẫn.

## 2. Cài Đặt Các Phụ Thuộc Cục Bộ

Tạo môi trường ảo và cài đặt yêu cầu của Phần 2:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Phiên bản đầu tiên dùng chế độ cục bộ Qdrant và FastEmbed. Client Python của Qdrant hỗ trợ chế độ cục bộ trong bộ nhớ với `QdrantClient(":memory:")`, rất hữu ích cho các hướng dẫn cục bộ và kiểm thử kiểu CI. FastEmbed cung cấp mô hình nhúng thực sự cục bộ mà không cần khóa API đám mây.

File yêu cầu cũng bao gồm `python-dotenv` vì notebook có thể tùy chọn đọc tên mô hình Ollama từ `.env`. Hướng dẫn này không cần khóa Azure OpenAI hay OpenAI API.

## 3. Tải Tài Liệu Mẫu

Tập hợp tài liệu mẫu được thiết kế nhỏ:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

Trong notebook, tôi tải tất cả file Markdown từ `sample_data/`:

```python
from pathlib import Path

repo_root = Path.cwd()
if not (repo_root / "sample_data").exists():
    repo_root = Path.cwd().parent

sample_dir = repo_root / "sample_data"
sample_files = ["course_ai_guidance.md", "school_ai_policy.md"]
documents = []

for file_name in sample_files:
    path = sample_dir / file_name
    documents.append({
        "source": path.name,
        "text": path.read_text(encoding="utf-8"),
    })

print(f"Loaded {len(documents)} documents")
```

Khi chạy notebook, nó tải 2 tài liệu. Đủ nhỏ để kiểm tra thủ công, tiện khi xây dựng phiên bản đầu tiên của quy trình RAG.

## 4. Chia Đoạn Theo Tiêu Đề Markdown

Bước tiếp theo là chia tài liệu thành đoạn.

Trong hướng dẫn này, tôi dùng tiêu đề Markdown làm tín hiệu cấu trúc. Tiêu đề tài liệu lấy từ `#`, mỗi đoạn phần lấy từ `##`.

> [!NOTE]
> Việc chia đoạn không phải lúc nào cũng như nhau. Trong hướng dẫn này, tôi dùng tiêu đề Markdown vì tài liệu mẫu cấu trúc rõ với `#` và `##`. Với PDF, Word, slide, ticket hay trang web, chiến lược tốt hơn có thể dùng ranh giới trang, thông tin bố cục, phần mục nghĩa, giới hạn token, bảng biểu hay metadata. Quan trọng là chọn chiến lược chia đoạn bảo toàn ý nghĩa và có thể truy nguồn cho tài liệu của bạn.

```python
def chunk_markdown(document):
    title = None
    current_heading = None
    current_lines = []
    chunks = []

    def flush():
        if current_heading and current_lines:
            content = "\n".join(current_lines).strip()
            if content:
                chunks.append({
                    "id": f"{document['source']}::{len(chunks)}",
                    "source": document["source"],
                    "title": title or document["source"],
                    "sectionHeading": current_heading,
                    "content": content,
                    "documentVersion": "local-sample-v1",
                    "permissions": ["students", "instructors"],
                })

    for raw_line in document["text"].splitlines():
        line = raw_line.strip()
        if line.startswith("# "):
            title = line[2:].strip()
        elif line.startswith("## "):
            flush()
            current_heading = line[3:].strip()
            current_lines = []
        elif line:
            current_lines.append(line)

    flush()
    return chunks
```

Rồi áp dụng cho từng tài liệu:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

Chạy tại máy tôi tạo ra 8 đoạn.

Điểm tôi thích ở bước này là metadata đã có ích. Mỗi đoạn biết `source`, `sectionHeading`, `documentVersion` và placeholder `permissions`. Ngay cả với hướng dẫn nhỏ, điều này giúp việc tham khảo và lần lượt truy xuất có quyền dễ suy nghĩ hơn.

## 5. Tạo Nhúng Cục Bộ

Phiên bản công khai đầu dùng `BAAI/bge-small-en-v1.5` qua FastEmbed.

Điều này giữ hướng dẫn cục bộ và thân thiện với CPU, nhưng vẫn dùng mô hình nhúng thực thay vì hàm vectơ giả. Lần chạy đầu tải trọng số mô hình. Sau đó notebook có thể dùng lại bộ nhớ đệm cục bộ.

> [!NOTE]
> Tôi dùng `BAAI/bge-small-en-v1.5` vì nó là mô hình nhúng tiếng Anh nhẹ, phù hợp với FastEmbed và Qdrant cho hướng dẫn cục bộ. Nó tạo vectơ 384 chiều, giữ ví dụ chạy nhanh và kinh tế cục bộ. Đây không phải là lựa chọn duy nhất. Năm 2023 nhiều hướng dẫn dùng mô hình nhúng được lưu trữ như `text-embedding-ada-002`. Nay, các lựa chọn lưu trữ mới như OpenAI `text-embedding-3-small` và `text-embedding-3-large`, cùng các lựa chọn mã nguồn mở như BGE, E5, MiniLM, Nomic Embed, và mô hình đa ngôn ngữ như `BAAI/bge-m3` đều hợp lý tùy theo tải công việc. Trong sản xuất, mô hình nhúng phù hợp nên được chọn qua đánh giá truy xuất trên tài liệu riêng của bạn.

Một số lựa chọn thực tế:

| Dòng mô hình | Khi tôi xem xét |
| --- | --- |
| `text-embedding-ada-002` | Cơ sở lưu trữ cũ từng xuất hiện nhiều trong hướng dẫn năm 2023. Tôi không chọn nó làm mặc định cho hướng dẫn mới hôm nay. |
| `text-embedding-3-small` | Mặc định lưu trữ hiện đại khi tôi muốn cân bằng chi phí/hiệu năng tốt và không cần nhúng chỉ cục bộ. |
| `text-embedding-3-large` | Lựa chọn lưu trữ khi chất lượng truy xuất quan trọng hơn kích thước vector hay chi phí nhúng. |
| `BAAI/bge-small-en-v1.5` | Mức cơ sở nhẹ cục bộ tiếng Anh cho hướng dẫn, nguyên mẫu, và thí nghiệm thân thiện CPU. |
| `BAAI/bge-base-en-v1.5` hoặc `BAAI/bge-large-en-v1.5` | Mô hình tiếng Anh cục bộ lớn hơn khi muốn chất lượng truy xuất tốt hơn và có thể chi trả nhiều tính toán hơn. |
| `BAAI/bge-m3` | Truy xuất đa ngôn ngữ hoặc ngữ cảnh dài, nhất là khi tài liệu không chỉ tiếng Anh. |
| `sentence-transformers/all-MiniLM-L6-v2` | Mức cơ sở rất nhỏ và nhanh cho tìm kiếm ngữ nghĩa. Hữu ích khi tốc độ và đơn giản quan trọng nhất. |
| `nomic-embed-text-v1.5` | Lựa chọn nhúng cục bộ mở đáng thử cho thiết lập đa ngữ cảnh hoặc tập trung di động. |

```python
import re
from fastembed import TextEmbedding

EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"
embedding_model = TextEmbedding(model_name=EMBEDDING_MODEL_NAME)

def tokenize(text):
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    expanded = []
    for token in tokens:
        expanded.append(token)
        if token.endswith("s") and len(token) > 3:
            expanded.append(token[:-1])
    return expanded
```

Rồi mỗi đoạn được nhúng:

```python
texts_to_embed = [
    f"{chunk['title']} {chunk['sectionHeading']} {chunk['content']}"
    for chunk in chunks
]
chunk_vectors = list(embedding_model.embed(texts_to_embed))
VECTOR_SIZE = len(chunk_vectors[0])

for chunk, vector in zip(chunks, chunk_vectors):
    chunk["vector"] = vector
```

## 6. Lưu Vectơ Trong Chế Độ Cục Bộ Qdrant

Bây giờ tạo bộ sưu tập Qdrant trong bộ nhớ và chèn các đoạn cùng metadata gắn kèm.

> [!NOTE]
> Trong hướng dẫn 2023, tôi dùng FAISS vì đây là cách đơn giản, phổ biến để minh họa tìm kiếm vectơ cục bộ với LangChain. FAISS vẫn hữu ích cho thí nghiệm cục bộ nhanh. Trong phiên bản 2026 này, tôi dùng Qdrant vì muốn hướng dẫn gần mô hình RAG sản xuất hơn. Qdrant cho phép lưu vectơ cùng metadata như file nguồn, tiêu đề phần, phiên bản tài liệu và quyền. Điều này giúp truy xuất dễ kiểm tra và chuẩn bị cho lọc, trích dẫn, và triển khai lâu dài hoặc máy chủ.

FAISS rất tốt cho minh họa tìm kiếm vectơ tương tự. Qdrant tốt hơn cho lớp truy xuất RAG nhỏ nhưng có hình dạng sản xuất.

Một số lựa chọn thực tế:

| Kho lưu vectơ / lớp tìm kiếm | Khi tôi xem xét |
| --- | --- |
| Qdrant | Nguyên mẫu cục bộ, lọc metadata, tìm kiếm vectơ thân thiện sản xuất, và quy trình Python đơn giản. |
| Chroma | Thí nghiệm RAG cục bộ nhanh và notebook khi đơn giản quan trọng nhất. |
| FAISS | Tìm vectơ cục bộ nhẹ khi chỉ cần tìm kiếm tương tự và có thể quản lý metadata riêng. |
| Milvus | Tìm kiếm vectơ mở quy mô lớn hơn khi nhóm sẵn sàng vận hành cơ sở dữ liệu vectơ chuyên dụng. |
| Weaviate | Tìm kiếm vectơ có schema, metadata, tìm kiếm lai, và tùy chọn triển khai quản lý hoặc tự host. |
| Azure AI Search | RAG doanh nghiệp trên Azure khi muốn tìm bằng từ khóa, tìm vectơ, truy xuất lai, xếp hạng ngữ nghĩa, lọc, bảo mật và vận hành quản lý trong một lớp tìm kiếm. |
| PostgreSQL + pgvector | Nhóm đã dùng PostgreSQL muốn tìm kiếm vectơ gần dữ liệu ứng dụng. |

```python
from qdrant_client import QdrantClient, models

collection_name = "school_policy_local"
client = QdrantClient(":memory:")

client.create_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(
        size=VECTOR_SIZE,
        distance=models.Distance.COSINE,
    ),
)
```

Rồi chèn các điểm:

```python
points = []

for idx, chunk in enumerate(chunks):
    payload = {
        key: chunk[key]
        for key in [
            "source",
            "title",
            "sectionHeading",
            "content",
            "documentVersion",
            "permissions",
        ]
    }
    points.append(
        models.PointStruct(
            id=idx,
            vector=chunk["vector"].tolist(),
            payload=payload,
        )
    )

client.upsert(collection_name=collection_name, points=points)
```

Chạy tại tôi, bộ sưu tập chèn 8 vectơ.

Đây là điểm hệ thống RAG bắt đầu có thể kiểm tra. Cơ sở dữ liệu vectơ không chỉ lưu vectơ; nó lưu cả văn bản bằng chứng và metadata cần cho trích dẫn.

## 7. Truy Xuất Đoạn Ứng Viên

Bây giờ hỏi câu hỏi và truy xuất đoạn ứng viên.

```python
question = "Can I use generative AI for my final assignment?"
query_vector = list(embedding_model.embed([question]))[0].tolist()

raw_results = client.query_points(
    collection_name=collection_name,
    query=query_vector,
    limit=5,
    with_payload=True,
).points
```

Tại bước này, tôi in các đoạn được truy xuất trước khi tạo câu trả lời. Điều này quan trọng. Nếu truy xuất sai, tạo văn bản chỉ che giấu vấn đề bằng từ ngữ mượt mà.

## 8. Thêm Bộ Sắp Xếp Lại Nhẹ

Khi thử truy xuất lần đầu, chỉ tương tự vectơ tìm nội dung chính sách liên quan, nhưng phần chính xác nhất không luôn đứng đầu.

Vậy tôi thêm bộ sắp xếp lại cục bộ nhỏ. Nó thêm trọng số khi thuật ngữ câu hỏi trùng với tiêu đề và nội dung đoạn.

```python
query_terms = set(tokenize(question))

def rerank_score(result):
    payload = result.payload
    heading_terms = set(tokenize(payload["sectionHeading"]))
    content_terms = set(tokenize(payload["content"]))
    heading_overlap = len(query_terms & heading_terms)
    content_overlap = len(query_terms & content_terms)
    return result.score + (0.12 * heading_overlap) + (0.02 * content_overlap)

results = sorted(raw_results, key=rerank_score, reverse=True)[:3]
```

Sau sắp xếp lại, kết quả đầu tiên là:

```text
school_ai_policy.md / Final Assignments
```

Đó là phần mong đợi với câu hỏi thử.

Bài học hữu ích nhất từ triển khai đầu là vậy. Ngay trong ví dụ cục bộ nhỏ, chất lượng truy xuất cải thiện khi tôi kết hợp tương tự vectơ với tín hiệu khác.

## 9. Tạo Câu Trả Lời Cục Bộ Có Nền Tảng

Đường dẫn mặc định tôi dùng trình tạo câu trả lời cục bộ minh bạch thay vì LLM.

```python
top = results[0].payload

answer = (
    "Based on the retrieved policy section, students may use generative AI for "
    "brainstorming, outlining, grammar feedback, and code explanation when the "
    "instructor allows it. They should not submit AI-generated work as their own, "
    "and they should include a disclosure when AI tools are used."
)

print("Answer:")
print(answer)
print("\nSource:")
print(f"{top['source']} / {top['sectionHeading']}")
```

Nó không phải trình tạo câu trả lời cuối cùng sản phẩm. Đây là công cụ gỡ lỗi. Nó chứng minh truy xuất, metadata, trích dẫn vận hành được trước khi thêm yếu tố biến thiên mô hình.

## 10. Sinh Câu Trả Lời Cục Bộ Với Ollama và Phi-4-mini

Khi truy xuất hoạt động, notebook có thể thay thế bước trả lời cuối cùng với Ollama và `phi4-mini:3.8b`.

> [!NOTE]
> Ollama chỉ nên thay bước sinh câu trả lời cuối cùng. Tải tài liệu, chia đoạn, lưu vectơ, truy xuất, sắp xếp lại, và dây nối trích dẫn giữ nguyên.

Trước hết, notebook xây prompt bằng chứng từ các đoạn tìm được:

```python
def build_evidence(retrieved_results):
    evidence_blocks = []
    for idx, result in enumerate(retrieved_results, start=1):
        payload = result.payload
        evidence_blocks.append(
            f"[{idx}] Source: {payload['source']} / {payload['sectionHeading']}\n"
            f"{payload['content']}"
        )
    return "\n\n".join(evidence_blocks)

evidence = build_evidence(results)
answer_prompt = (
    "Answer the question using only the evidence below. "
    "If the evidence is insufficient, say that the provided documents do not contain enough information. "
    "End with a Sources line that lists the source file and section.\n\n"
    f"Question: {question}\n\nEvidence:\n{evidence}"
)
```

Trong hướng dẫn này, tôi khuyên gia đình Phi-4-mini của Microsoft qua Ollama là lựa chọn sinh cục bộ mặc định. Trong Ollama, tên mô hình tôi thử là:

```powershell
ollama pull phi4-mini:3.8b
```

Bạn có thể kiểm tra nhanh mô hình có sẵn:

```powershell
ollama list
```

Rồi đặt các biến sau:

```powershell
Copy-Item .env.example .env
```

Mở `.env` và bỏ chú thích giá trị Ollama của Phần 2:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Notebook tải `.env` từ gốc kho với `python-dotenv`, rồi gửi prompt bằng chứng tương tự đến endpoint cục bộ `/api/chat` của Ollama với streaming tắt. Nếu Ollama không chạy hoặc `SERIES2_OLLAMA_MODEL` thiếu, lộ trình này bị bỏ qua.

> [!NOTE]
> Trên máy này, `phi4-mini:3.8b` tải xuống khoảng 2.49GB file mô hình. Khi suy diễn, Ollama báo kích thước mô hình đã tải là 3.3GB và dùng GPU RTX 3060 Laptop.

Điều này đưa hướng dẫn hai cấp độ:

1. Trình tạo câu trả lời xác định chỉ CPU.
2. Sinh câu trả lời cục bộ với Ollama và Phi-4-mini.

Quy trình truy xuất giữ nguyên cả hai.

## 11. Kết Quả Xác Minh

Tôi chạy notebook cục bộ trên Windows với Python 3.12.6.

Các gói cài đặt:

| Gói | Phiên bản |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Thực thi notebook:

- Notebook: `notebooks/series-2-open-source-rag.ipynb`
- Kết quả thực thi: thành công với `nbclient`
- Tài liệu tải: 2
- Đoạn tạo: 8
- Bộ sưu tập Qdrant: `school_policy_local`
- Vectơ chèn: 8
- Mô hình nhúng: `BAAI/bge-small-en-v1.5`
- Kích thước nhúng: 384
- Câu hỏi truy xuất: "Tôi có thể sử dụng AI tạo sinh cho bài tập cuối kỳ của mình không?"
- Đường dẫn sắp xếp lại: sắp xếp lại ngữ nghĩa nhẹ tại chỗ
- Nguồn truy xuất hàng đầu sau khi sắp xếp lại: `school_ai_policy.md`
- Phần truy xuất hàng đầu sau khi sắp xếp lại: `Final Assignments`
- Đường dẫn trả lời mặc định: trình tạo câu trả lời minh bạch tại chỗ
- Đường dẫn tạo Ollama: hoàn thành với `phi4-mini:3.8b`
- Kích thước tệp mô hình Ollama: 2.49GB trên đĩa
- Kích thước mô hình Ollama đã tải: 3.3GB báo cáo bởi `ollama ps`
- GPU offload: 100% GPU báo cáo bởi `ollama ps`
- Bộ nhớ GPU quan sát sau khi tạo: khoảng 3.5GB trên 6GB sử dụng trên RTX 3060 Laptop GPU
- Thực thi Notebook với mô hình FastEmbed được lưu cache và tạo Ollama được bật: vượt qua trong khoảng 34 giây thông qua kịch bản xác minh

Câu trả lời do Ollama tạo là:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

Tôi sẽ không gọi câu trả lời này là hoàn hảo. Nó trả lời dựa trên bằng chứng đúng, nhưng dòng nguồn cuối cùng kém chính xác hơn so với định dạng trích dẫn xác định. Điều đó hữu ích để thể hiện trong hướng dẫn vì nó làm rõ câu hỏi kỹ thuật tiếp theo: tạo câu trả lời cũng cần được đánh giá, không chỉ truy xuất.

Điều chính tôi học được trong khi xác minh điều này là chất lượng truy xuất cần được kiểm tra trước khi tạo câu trả lời. Kết quả nhúng đã hữu ích, và bộ sắp xếp lại ngữ nghĩa nhẹ làm phần chính sách dự kiến xuất hiện đầu tiên một cách đáng tin cậy. Đó chính là loại hành vi hệ thống nhỏ mà tôi muốn hướng dẫn tiết lộ thay vì che giấu.

## 12. Điều gì sẽ đến tiếp theo

Cải tiến tiếp theo là so sánh thiết lập tại chỗ này với phiên bản Azure được quản lý trong cùng kịch bản trợ lý chính sách trường học. Giữ nguyên kịch bản sẽ giúp dễ dàng thấy những đánh đổi: độ phức tạp thiết lập, kiểm soát truy xuất, tích hợp danh tính, quyền sở hữu vận hành, và chi phí.

## 13. Tài liệu tham khảo

- [Qdrant Python client quickstart](https://python-client.qdrant.tech/quickstart.html)
- [Qdrant client GitHub repository](https://github.com/qdrant/qdrant-client)
- [Các mô hình được hỗ trợ FastEmbed](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [Hướng dẫn embeddings OpenAI](https://platform.openai.com/docs/guides/embeddings)
- [Thẻ mô hình BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [Thẻ mô hình BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3)
- [Thẻ mô hình sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Trang mô hình Ollama phi4-mini](https://ollama.com/library/phi4-mini)
- [Tài liệu Ollama trên Windows](https://docs.ollama.com/windows)
- [Tài liệu streaming API Ollama](https://docs.ollama.com/api/streaming)
- [Thẻ mô hình Microsoft Phi-4-mini-instruct](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [Tổng quan LangGraph](https://docs.langchain.com/oss/python/langgraph)
- [Giới thiệu về RAG - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

Trước: [Series 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Tuyên bố miễn trừ trách nhiệm**:
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng bản dịch tự động có thể chứa lỗi hoặc sai sót. Tài liệu gốc bằng ngôn ngữ gốc nên được coi là nguồn tin chính thức. Đối với thông tin quan trọng, nên sử dụng dịch vụ dịch thuật chuyên nghiệp bởi con người. Chúng tôi không chịu trách nhiệm về bất kỳ hiểu lầm hoặc giải thích sai nào phát sinh từ việc sử dụng bản dịch này.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->