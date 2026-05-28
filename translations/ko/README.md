# 문서를 기반으로 AI에게 질문에 답하도록 가르치기

![문서 기반 AI RAG 시스템 개요](../../assets/images/readme-hero.svg)

이 저장소는 RAG, Azure AI 서비스, 오픈 소스 대안, 평가 지향 워크플로우로 문서 기반 AI 시스템을 구축하는 2026년 블로그 시리즈를 모은 것입니다.

## 배경

2023년에 저는 Azure AI 검색과 Azure OpenAI를 사용하여 PDF 문서에서 질문에 답하도록 ChatGPT를 가르치는 튜토리얼 두 편 작업을 했습니다. "데이터 기반 ChatGPT"라는 아이디어가 그때는 아직 새로웠으며, 목표는 실질적인 워크플로우를 보여주는 것이었습니다: 문서를 저장하고, 인덱싱하고, 관련 콘텐츠를 검색하고, 검색된 컨텍스트에서 답변을 생성하는 과정입니다.

2026년 현재 RAG 생태계는 훨씬 확장되었습니다. Azure AI Search는 최신 벡터 및 하이브리드 검색 패턴을 지원하고, Azure OpenAI는 더 넓은 Microsoft Foundry Models 생태계의 일부이며, LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, vLLM 같은 오픈 소스 도구들이 실제 시스템에 적합한 선택지가 되었습니다.

그래서 이 주제를 다시 다루고 싶었습니다. 이제 질문은 단순히 "RAG를 어떻게 구축합니까?"가 아니라, 구축 방법이 다양해졌기에 "내 상황에 맞는 아키텍처는 무엇인가?"가 더 중요한 질문이 되었습니다.

이 시리즈는 그런 의사결정 단계부터 시작해서 이를 실습 튜토리얼로 전환합니다. 첫 구현 경로는 누구나 샘플 데이터, Qdrant, Ollama, Phi-4-mini를 사용해 로컬에서 실행할 수 있는 오픈 소스 RAG 시스템을 구축하는 것입니다.

## 글 목록

글 목록은 [articles/README.md](./articles/README.md)를 참조하세요.

1. [시리즈 1: RAG, Azure vs 오픈 소스 대안, 파인튜닝이 의미 있을 때](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [시리즈 2: 로컬 오픈 소스 RAG 시스템 엔드 투 엔드 구축](./articles/series-2-open-source-rag-end-to-end.md)

곧 다룰 내용:

- Azure AI Search와 Azure OpenAI로 같은 RAG 시스템 재구축
- 데모 답변 이상으로 평가 및 회귀 검사 추가

## 노트북

구현 글들은 노트북을 사용하기 때문에 검색 및 평가 단계를 직접 검토할 수 있습니다. 폴더 단위 안내는 [notebooks/README.md](./notebooks/README.md)를 보세요.

> [!TIP]
> 가장 빠른 경로를 원하면 시리즈 2부터 시작하세요. 샘플 데이터, CPU에 친화적인 임베딩, Qdrant 로컬 모드, 클라우드 인증서 없이 로컬에서 실행됩니다.

| 시리즈 | 노트북 | 요구사항 | 로컬 검증 |
| --- | --- | --- | --- |
| 시리즈 2 | [오픈 소스 RAG 노트북](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Qdrant 로컬 모드, 검색, 재순위화 및 출처 연결 검증 완료 |

로컬에서 노트북을 실행하려면 가상 환경을 만들고 매칭되는 요구 사항 파일을 설치하세요. 예:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## 샘플 데이터

노트북은 [sample_data](../../sample_data)에 있는 작은 로컬 코퍼스를 사용하므로, 개인 문서나 클라우드 인증 없이 예제를 실행할 수 있습니다. 자세한 내용은 [sample_data/README.md](./sample_data/README.md)를 참고하세요.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## 로컬 검증 요약

검증 결과는 각 글과 [SERIES_PLAN.md](./SERIES_PLAN.md)에 기록되어 있습니다.

| 영역 | 결과 |
| --- | --- |
| 시리즈 2 오픈 소스 경로 | FastEmbed가 384차원 로컬 임베딩 생성, Qdrant 인메모리 컬렉션에 8개 벡터 삽입, 경량 재순위화가 예상 섹션 검색; 선택적 Ollama 생성은 `phi4-mini:3.8b`로 완료됨 |

로컬 노트북은 의도적으로 하드코딩된 비밀 정보를 포함하지 않습니다.

## 로컬 Ollama 생성

시리즈 2 노트북은 기본적으로 로컬 안전합니다. 로컬 Ollama 생성을 활성화하려면 [.env.example](../../.env.example)를 `.env`로 복사하고 시리즈 2 값을 작성하세요.

시리즈 2 Ollama 생성을 위해 다음을 주석 해제하세요:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

시리즈 2 노트북은 `python-dotenv`를 사용해 저장소 루트에서 자동으로 `.env`를 로드합니다.

> [!IMPORTANT]
> `.env` 파일, API 키, 개인 엔드포인트, 테넌트별 값은 커밋하지 마세요. 저장소는 의도적으로 비밀 정보를 Markdown 파일 및 노트북에서 분리하고 있습니다.

요구 사항 파일은 [requirements/README.md](./requirements/README.md)에 문서화되어 있습니다.

링크, 노트북 구조, 노트북 출력 청결, 고위험 비밀 패턴을 검증하려면:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

검증 스크립트는 [scripts/README.md](./scripts/README.md)에 문서화되어 있습니다.

같은 환경에서 로컬 안전한 모든 노트북을 실행하려면:

```powershell
python scripts\verify_notebooks.py --execute
```

동일한 검증 흐름이 GitHub Actions에서 푸시, 풀 리퀘스트, 수동 워크플로우 실행 시에도 작동합니다. 초안 글과 노트북은 공개 검증 경로에서 의도적으로 제외됩니다.

업데이트 게시 전에 [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md)를 사용하세요.

현재 미공개 변경 요약은 [CHANGELOG.md](./CHANGELOG.md)를 보세요.

기여 및 노트북 관리 지침은 [CONTRIBUTING.md](./CONTRIBUTING.md)를 확인하세요.

## 다국어 지원

### Co-op Translator를 통해 지원 (자동화 및 항상 최신)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[아랍어](../ar/README.md) | [벵골어](../bn/README.md) | [불가리아어](../bg/README.md) | [버마어 (미얀마)](../my/README.md) | [중국어 (간체)](../zh-CN/README.md) | [중국어 (번체, 홍콩)](../zh-HK/README.md) | [중국어 (번체, 마카오)](../zh-MO/README.md) | [중국어 (번체, 대만)](../zh-TW/README.md) | [크로아티아어](../hr/README.md) | [체코어](../cs/README.md) | [덴마크어](../da/README.md) | [네덜란드어](../nl/README.md) | [에스토니아어](../et/README.md) | [핀란드어](../fi/README.md) | [프랑스어](../fr/README.md) | [독일어](../de/README.md) | [그리스어](../el/README.md) | [히브리어](../he/README.md) | [힌디어](../hi/README.md) | [헝가리어](../hu/README.md) | [인도네시아어](../id/README.md) | [이탈리아어](../it/README.md) | [일본어](../ja/README.md) | [칸나다어](../kn/README.md) | [크메르어](../km/README.md) | [한국어](./README.md) | [리투아니아어](../lt/README.md) | [말레이어](../ms/README.md) | [말라얄람어](../ml/README.md) | [마라티어](../mr/README.md) | [네팔어](../ne/README.md) | [나이지리아 피진어](../pcm/README.md) | [노르웨이어](../no/README.md) | [페르시아어 (파르시)](../fa/README.md) | [폴란드어](../pl/README.md) | [포르투갈어 (브라질)](../pt-BR/README.md) | [포르투갈어 (포르투갈)](../pt-PT/README.md) | [펀자브어 (구르무키)](../pa/README.md) | [루마니아어](../ro/README.md) | [러시아어](../ru/README.md) | [세르비아어 (키릴 문자)](../sr/README.md) | [슬로바키아어](../sk/README.md) | [슬로베니아어](../sl/README.md) | [스페인어](../es/README.md) | [스와힐리어](../sw/README.md) | [스웨덴어](../sv/README.md) | [타갈로그어 (필리피노)](../tl/README.md) | [타밀어](../ta/README.md) | [텔루구어](../te/README.md) | [태국어](../th/README.md) | [터키어](../tr/README.md) | [우크라이나어](../uk/README.md) | [우르두어](../ur/README.md) | [베트남어](../vi/README.md)

> **로컬 클론을 선호하시나요?**
>
> 이 저장소는 50개 이상의 언어 번역을 포함하여 다운로드 크기를 크게 증가시킵니다. 번역 없이 클론하려면 sparse checkout을 사용하세요:
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
> 이렇게 하면 훨씬 빠른 다운로드로 코스를 완료하는 데 필요한 모든 것을 갖게 됩니다.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**면책 조항**:
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 기하기 위해 노력하고 있으나, 자동 번역은 오류나 부정확한 부분이 있을 수 있음을 유의하시기 바랍니다. 원본 문서의 원어본이 권위 있는 자료로 간주되어야 합니다. 중요한 정보의 경우, 전문가의 인간 번역을 권장합니다. 이 번역 사용으로 인해 발생하는 오해나 잘못된 해석에 대해 당사는 책임을 지지 않습니다.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->