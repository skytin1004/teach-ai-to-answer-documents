# 문서 기반 질문에 답변하도록 AI 가르치기
## 시리즈 2: 로컬 오픈소스 RAG 시스템 종단 간 구축

![Local open-source RAG tutorial pipeline](../../../assets/images/series-2-local-rag.svg)

> 이 글은 시리즈 1의 아키텍처 논의를 실행 가능한 로컬 RAG 튜토리얼로 전환합니다. 목표는 먼저 샘플 데이터를 사용해 클라우드 계정과 비밀 없이 전체 워크플로우를 구축한 후, 그 작동하는 기본선을 바탕으로 더 나은 아키텍처 결정을 내리는 것입니다.

우리가 구축할 시스템은 작은 학교 정책 도우미입니다. 두 개의 로컬 마크다운 문서를 지식 베이스로 사용한 후, 전체 RAG 파이프라인: 청킹, 로컬 임베딩, Qdrant 벡터 저장, 검색, 재순위, 출처 인지 답변 구성, 그리고 선택적인 Ollama 및 Phi-4-mini로 로컬 생성까지 진행합니다.

시리즈 탐색: [저장소 홈](../README.md) | 이전: [시리즈 1 - RAG, Azure 대 오픈소스 대안, 그리고 파인튜닝이 의미 있는 경우](./series-1-rag-azure-open-source-fine-tuning.md)

노트북: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | 요구사항: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> 클라우드 리소스 생성 전에 RAG 파이프라인을 이해하고 싶을 때 가장 좋은 출발점입니다. 기본 경로는 CPU 친화적 임베딩과 비밀 없이 로컬에서 실행됩니다.

## 1. 우리가 만드는 것

2023년 튜토리얼에서는 Azure AI Search와 Azure OpenAI가 PDF 문서에서 질문에 답하는 방법을 보여주기 위해 Azure부터 시작했습니다.

2026년 이 시리즈에서는 한 단계 더 낮은 레벨에서 시작하려 합니다.

관리형 서비스를 사용하기 전에, 로컬에서 작은 RAG 시스템을 구축하고 모든 단계를 가시화하려 합니다: 문서 로드, 텍스트 청킹, 벡터 저장, 증거 검색, 결과 재순위, 출처 인지 답변 반환.

샘플 시나리오는 학교 정책 도우미입니다. 사용자가 묻습니다:

```text
Can I use generative AI for my final assignment?
```

시스템은 일반 모델 기억에서 답변해서는 안 됩니다. 관련 정책 섹션을 검색하여 그 증거에서 답변해야 합니다.

완전 실행 가능한 버전은 [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb)에 있습니다. 아래 코드는 주요 단계를 보여주므로 이 글을 튜토리얼로 읽을 수 있습니다.

## 2. 로컬 종속성 설치

가상 환경을 만들고 시리즈 2 요구사항을 설치합니다:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

첫 버전은 Qdrant 로컬 모드와 FastEmbed를 사용합니다. Qdrant의 파이썬 클라이언트는 `QdrantClient(":memory:")`와 함께 메모리 내 로컬 모드를 지원하며, 로컬 튜토리얼과 CI 스타일 검증에 유용합니다. FastEmbed는 클라우드 API 키 없이 진짜 로컬 임베딩 모델을 제공합니다.

요구사항 파일에는 `python-dotenv`도 포함되어 있는데, 노트북이 선택적으로 `.env`에서 Ollama 모델 이름을 읽을 수 있기 때문입니다. 이 로컬 튜토리얼에는 Azure OpenAI나 OpenAI API 키가 필요 없습니다.

## 3. 샘플 문서 로드

샘플 말뭉치는 의도적으로 작습니다:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

노트북에서는 `sample_data/`의 모든 마크다운 파일을 로드합니다:

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

노트북 실행 시 2개의 문서를 로드했습니다. 이 정도는 수동으로 검토하기에 충분히 작아 RAG 파이프라인 첫 버전 구축에 유용합니다.

## 4. 마크다운 헤딩별 청킹

다음 단계는 문서를 청크로 분할하는 것입니다.

이 튜토리얼에서는 마크다운 헤딩을 구조 신호로 사용합니다. 문서 제목은 `#`에서, 각 섹션 청크는 `##`에서 가져옵니다.

> [!NOTE]
> 청킹은 모두에 맞는 하나의 해법이 아닙니다. 여기서는 샘플 문서가 명확한 `#` 및 `##` 구조를 가지고 있어 마크다운 헤딩을 사용합니다. PDF, 워드 문서, 슬라이드, 티켓, 웹 페이지라면 페이지 경계, 레이아웃 정보, 의미 단락, 토큰 제한, 표, 메타데이터 등을 활용하는 더 나은 전략이 있을 수 있습니다. 중요한 점은 문서의 의미와 출처 추적 가능성을 보존하는 청킹 전략을 선택하는 것입니다.

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

그 후 모든 문서에 적용합니다:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

로컬 실행에서 8개의 청크가 생성되었습니다.

이 단계에서 좋았던 점은 메타데이터가 이미 유용하다는 것입니다. 각 청크는 자신의 `source`, `sectionHeading`, `documentVersion`, 그리고 플레이스홀더 `permissions`을 알고 있습니다. 작은 튜토리얼이라도 인용과 나중에 권한 인지 검색을 더 쉽게 만듭니다.

## 5. 로컬 임베딩 생성

첫 공개 버전으로 FastEmbed를 통해 `BAAI/bge-small-en-v1.5`를 사용합니다.

이렇게 하면 튜토리얼이 로컬에서 CPU 친화적으로 유지되면서도, 단순 벡터 함수가 아닌 실제 임베딩 모델을 사용합니다. 첫 실행 시 모델 가중치를 다운로드하고 이후에는 노트북이 로컬 캐시를 재사용합니다.

> [!NOTE]
> `BAAI/bge-small-en-v1.5`를 사용하는 이유는 FastEmbed 및 Qdrant와 잘 어울리는 가벼운 영어 임베딩 모델이기 때문입니다. 384차원 벡터를 생성해 예제를 빠르고 저렴하게 로컬에서 실행할 수 있습니다. 이것이 유일한 좋은 선택은 아닙니다. 2023년에는 `text-embedding-ada-002` 같은 호스팅 임베딩 모델을 많이 사용했습니다. 현재는 OpenAI의 `text-embedding-3-small`, `text-embedding-3-large`, BGE, E5, MiniLM, Nomic Embed, 그리고 `BAAI/bge-m3` 같은 다중언어 모델 등 사용 목적과 작업량에 따라 적절한 선택지가 다양합니다. 프로덕션에서는 자체 문서로 검색 평가를 통해 적합한 임베딩 모델을 선정해야 합니다.

몇 가지 실용적인 대안:

| 모델 군 | 고려 시점 |
| --- | --- |
| `text-embedding-ada-002` | 2023년 다수 튜토리얼에서 사용된 오래된 호스팅 기본값. 오늘날 새 튜토리얼에서는 기본값으로 선택하지 않습니다. |
| `text-embedding-3-small` | 강력한 비용/성능 균형이 필요하고 로컬 전용 임베딩이 필요 없을 때 현대 호스팅 기본값. |
| `text-embedding-3-large` | 벡터 크기나 임베딩 비용보다 검색 품질이 더 중요한 경우의 호스팅 옵션. |
| `BAAI/bge-small-en-v1.5` | 튜토리얼, 프로토타입 및 CPU 친화적 실험용 경량 로컬 영어 베이스라인. |
| `BAAI/bge-base-en-v1.5` 또는 `BAAI/bge-large-en-v1.5` | 더 좋은 검색 품질을 원하고 더 많은 연산 자원이 허용될 때의 더 큰 로컬 영어 모델. |
| `BAAI/bge-m3` | 문서가 영어뿐만 아니라 다국어이거나 더 긴 컨텍스트 검색이 필요한 경우. |
| `sentence-transformers/all-MiniLM-L6-v2` | 매우 작고 빠른 의미 검색 기본값. 속도와 단순함이 가장 중요할 때 유용. |
| `nomic-embed-text-v1.5` | 더 긴 컨텍스트 또는 휴대성 중심 환경에 적합한 오픈 로컬 임베딩 옵션으로 테스트할 가치 있음. |

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

그 후 각 청크에 임베딩을 생성합니다:

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

## 6. Qdrant 로컬 모드에 벡터 저장

이제 메모리 내 Qdrant 컬렉션을 만들고 페이로드 메타데이터와 함께 청크를 삽입합니다.

> [!NOTE]
> 2023년 튜토리얼에서는 LangChain으로 로컬 벡터 유사도 검색을 시연하기 쉬운 FAISS를 사용했습니다. FAISS는 빠른 로컬 실험에 여전히 유용합니다. 이번 2026년 버전에서는 튜토리얼이 프로덕션 RAG 시스템에 더 가깝게 느껴지도록 Qdrant를 씁니다. Qdrant는 벡터뿐 아니라 원본 파일, 섹션 제목, 문서 버전, 권한 등 페이로드 메타데이터도 함께 저장할 수 있어 검색 검토가 더 쉬워지고 필터링, 인용, 후속 영속적 혹은 서버 기반 배포 준비에 적합합니다.

FAISS는 벡터 유사도 검색 시연에 좋습니다. Qdrant는 작은 규모이지만 프로덕션 형태 RAG 검색 계층을 보여주기에 더 좋습니다.

몇 가지 실용적인 대안:

| 벡터 저장소 / 검색 계층 | 고려 시점 |
| --- | --- |
| Qdrant | 로컬 프로토타입, 메타데이터 필터링, 프로덕션 친화적 벡터 검색 및 간단한 파이썬 워크플로우. |
| Chroma | 간단함이 가장 중요한 빠른 로컬 RAG 실험 및 노트북. |
| FAISS | 유사도 검색만 필요하고 메타데이터를 별도로 관리할 수 있을 때 가벼운 로컬 벡터 검색. |
| Milvus | 팀이 전용 벡터 데이터베이스 운영 준비가 됐을 때 대규모 오픈소스 벡터 검색. |
| Weaviate | 스키마, 메타데이터, 하이브리드 검색, 관리형 또는 자체 호스팅 배포 옵션이 포함된 벡터 검색. |
| Azure AI Search | 키워드 검색, 벡터 검색, 하이브리드 검색, 의미론적 순위, 필터링, 보안, 관리형 운영을 통합한 엔터프라이즈 RAG(Azure). |
| PostgreSQL + pgvector | PostgreSQL을 이미 쓰고 있거나 벡터 검색을 애플리케이션 데이터 근처에서 원하는 팀. |

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

그 후 포인트를 삽입합니다:

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

내 실행에서는 컬렉션에 8개의 벡터가 삽입되었습니다.

여기서부터 RAG 시스템은 검토 가능해지기 시작합니다. 벡터 DB는 단순히 벡터를 저장하는 게 아니라 증거 텍스트와 인용에 필요한 메타데이터도 저장합니다.

## 7. 후보 청크 검색

이제 질문을 던지고 후보 청크를 검색합니다.

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

이 시점에서 생성 전 검색된 청크를 출력합니다. 이것이 중요합니다. 검색이 잘못되면 생성은 유창한 텍스트 뒤에 문제를 숨기기 때문입니다.

## 8. 경량 재순위기 추가

검색 경로를 처음 테스트할 때 벡터 유사도만으로 연관 정책 내용을 찾았으나 가장 정확한 섹션이 항상 최상단에 오지는 않았습니다.

그래서 작은 로컬 재순위기를 추가했습니다. 질문어가 섹션 헤딩 및 내용과 겹칠 때 추가 가중치를 줍니다.

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

재순위 후 최상위 결과는 다음과 같았습니다:

```text
school_ai_policy.md / Final Assignments
```

테스트 질문에 기대한 섹션이었습니다.

첫 구현에서 얻은 가장 유용한 교훈입니다. 아주 작은 로컬 예시에서도 벡터 유사도에 다른 신호를 결합하면 검색 품질이 개선됩니다.

## 9. 근거 기반 로컬 답변 구성

기본 경로에서는 LLM 대신 투명한 로컬 답변 작성기를 사용합니다.

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

최종 제품용 답변 생성기는 아닙니다. 디버깅 도구입니다. 모델 변동성을 추가하기 전에 검색, 메타데이터, 인용 연결이 작동함을 증명합니다.

## 10. Ollama 및 Phi-4-mini로 로컬 답변 생성

검색이 작동하면 노트북은 최종 답변 단계만 Ollama와 `phi4-mini:3.8b`로 교체할 수 있습니다.

> [!NOTE]
> Ollama는 최종 답변 생성 단계만 교체해야 합니다. 문서 로딩, 청킹, 벡터 저장, 검색, 재순위, 인용 연결은 동일하게 유지해야 합니다.

먼저 노트북은 검색된 청크로 증거 프롬프트를 만듭니다:

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

이 튜토리얼에서는 기본 로컬 생성 옵션으로 Ollama를 통한 Microsoft의 Phi-4-mini 패밀리를 권장합니다. 테스트한 모델 이름은:

```powershell
ollama pull phi4-mini:3.8b
```

모델이 사용 가능한지 빠르게 확인할 수 있습니다:

```powershell
ollama list
```

그 다음 이 변수들을 설정합니다:

```powershell
Copy-Item .env.example .env
```

`.env`를 열어 시리즈 2 Ollama 값을 주석 해제합니다:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

노트북은 저장소 루트에서 `python-dotenv`로 `.env`를 로드하고, 같은 증거 프롬프트를 Ollama 로컬 `/api/chat` 엔드포인트에 스트리밍 비활성화로 보냅니다. Ollama가 실행 중이지 않거나 `SERIES2_OLLAMA_MODEL`이 없으면 이 트랙은 건너뜁니다.

> [!NOTE]
> 이 머신에서 `phi4-mini:3.8b`는 약 2.49GB 모델 파일을 다운로드했습니다. 추론 중 Ollama가 3.3GB 로드된 모델 크기를 보고했고 RTX 3060 랩탑 GPU를 사용했습니다.

튜토리얼은 다음 두 수준을 제공합니다:

1. CPU 전용 결정론적 답변 작성기.
2. Ollama와 Phi-4-mini를 이용한 로컬 답변 생성.

두 경우 모두 검색 파이프라인은 동일합니다.

## 11. 검증 결과

Windows에서 Python 3.12.6으로 노트북을 로컬 실행했습니다.

설치된 패키지:

| 패키지 | 버전 |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

노트북 실행:

- 노트북: `notebooks/series-2-open-source-rag.ipynb`
- 실행 결과: `nbclient`로 성공
- 로드한 문서 수: 2개
- 생성한 청크 수: 8개
- Qdrant 컬렉션: `school_policy_local`
- 삽입된 벡터 수: 8개
- 임베딩 모델: `BAAI/bge-small-en-v1.5`
- 임베딩 크기: 384
- 검색 질문: "최종 과제에 생성 AI를 사용할 수 있나요?"
- 재순위 경로: 경량 로컬 어휘 재순위
- 재순위 후 최상위 검색 출처: `school_ai_policy.md`
- 재순위 후 최상위 검색 섹션: `Final Assignments`
- 기본 답변 경로: 로컬 투명 답변 컴포저
- Ollama 생성 경로: `phi4-mini:3.8b`로 완료
- Ollama 모델 파일 크기: 디스크에서 2.49GB
- Ollama 로드된 모델 크기: `ollama ps`에서 3.3GB 보고됨
- GPU 오프로딩: `ollama ps`에서 100% GPU 보고됨
- 생성 후 GPU 메모리 사용량: RTX 3060 노트북 GPU에서 6GB 중 약 3.5GB 사용됨
- 캐시된 FastEmbed 모델과 Ollama 생성을 활성화한 노트북 실행: 검증 스크립트를 통해 약 34초 만에 통과

Ollama가 생성한 답변은 다음과 같습니다:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

이 답변을 완벽하다고 부르지는 않겠습니다. 올바른 근거에서 답변하였지만, 최종 출처 줄이 결정적 인용 형식보다 덜 정확합니다. 이 점은 다음 엔지니어링 질문을 명확히 하기 때문에 튜토리얼에서 보여주는 것이 유용합니다: 답변 생성에도, 검색뿐 아니라 평가가 필요합니다.

검증하면서 배운 주요 내용은 답변 생성 전에 검색 품질을 먼저 확인해야 한다는 것입니다. 임베딩 결과는 이미 유용했고, 경량 재순위기는 예상한 정책 섹션이 신뢰성 있게 첫 번째로 나타나도록 만들었습니다. 이런 종류의 작은 시스템 동작을 튜토리얼에서 숨기지 않고 드러내고 싶습니다.

## 12. 다음 단계

다음 개선 사항은 동일한 학교 정책 보조 시나리오를 위한 관리형 Azure 버전과 이 로컬 설정을 비교하는 것입니다. 시나리오를 고정하면 타협점을 더 쉽게 볼 수 있습니다: 설정 복잡성, 검색 제어, 신원 통합, 운영 소유권, 비용 등.

## 13. 참고 문헌

- [Qdrant Python client quickstart](https://python-client.qdrant.tech/quickstart.html)
- [Qdrant client GitHub repository](https://github.com/qdrant/qdrant-client)
- [FastEmbed supported models](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [OpenAI embeddings guide](https://platform.openai.com/docs/guides/embeddings)
- [BAAI/bge-small-en-v1.5 model card](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [BAAI/bge-m3 model card](https://huggingface.co/BAAI/bge-m3)
- [sentence-transformers/all-MiniLM-L6-v2 model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Ollama phi4-mini model page](https://ollama.com/library/phi4-mini)
- [Ollama Windows documentation](https://docs.ollama.com/windows)
- [Ollama API streaming documentation](https://docs.ollama.com/api/streaming)
- [Microsoft Phi-4-mini-instruct model card](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph)
- [Introduction to RAG - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

이전: [Series 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**면책 조항**:
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 기하기 위해 노력하고 있으나, 자동 번역은 오류나 부정확한 부분이 있을 수 있음을 유의하시기 바랍니다. 원본 문서의 원어본이 권위 있는 자료로 간주되어야 합니다. 중요한 정보의 경우, 전문가의 인간 번역을 권장합니다. 이 번역 사용으로 인해 발생하는 오해나 잘못된 해석에 대해 당사는 책임을 지지 않습니다.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->