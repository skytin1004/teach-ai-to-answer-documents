# 문서 기반으로 질문에 답하도록 AI 교육하기

이 저장소는 RAG, Azure AI 서비스, 오픈 소스 대안, 평가 중심 워크플로우를 사용하여 문서 기반 AI 시스템을 구축하는 2026년 블로그 시리즈를 모았습니다.

## 배경

2023년에 저는 Azure AI Search와 Azure OpenAI를 사용하여 PDF 문서에서 질문에 답하도록 ChatGPT를 가르치는 튜토리얼 두 편을 작업했습니다. 그때는 "내 데이터 위의 ChatGPT"라는 개념이 여전히 새롭게 느껴졌으며, 목표는 실용적인 워크플로우를 보여주는 것이었습니다: 문서를 저장하고, 인덱싱하며, 관련 콘텐츠를 검색하고, 그 검색된 컨텍스트에서 답변을 생성하는 것입니다.

2026년에는 RAG 생태계가 훨씬 커졌습니다. Azure AI Search는 최신 벡터 및 하이브리드 검색 패턴을 지원하고, Azure OpenAI는 더 넓은 Microsoft Foundry Models 생태계의 일부이며, LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, vLLM과 같은 오픈 소스 도구들도 실제 시스템에 사용 가능한 선택지가 되었습니다.

그래서 이 주제를 다시 다루고 싶었습니다. 이제 질문은 단순히 "RAG를 어떻게 구축하나요?"가 아닙니다. 구축하는 방법은 다양해졌고, 더 중요한 질문은 "내 상황에 맞는 아키텍처는 무엇인가?"입니다.

이 시리즈는 그 의사 결정 단계에서 시작합니다. 구현에 깊이 들어가기 전에 AI 서비스가 왜 검색이 필요한지, 언제 Azure 기반 관리형 서비스가 적합하며, 언제 오픈 소스 대안이 더 좋은지, 그리고 파인튜닝은 어디에 적합한지 살펴봅니다.

## 글 목록

1. [시리즈 1: RAG, Azure 대 오픈 소스 대안, 그리고 파인튜닝이 적합한 시점](./series-1-rag-azure-open-source-fine-tuning.md)

## 다국어 지원

### Co-op 번역기 통해 지원 (자동 및 항상 최신)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](./README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **로컬 복제를 선호하시나요?**
>
> 이 저장소에는 50개 이상의 언어 번역본이 포함되어 있어 다운로드 크기가 크게 증가합니다. 번역본 없이 복제하려면 sparse checkout을 사용하세요:
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
> 이 방법으로 훨씬 빠른 다운로드 속도로 코스 완료에 필요한 모든 것을 얻을 수 있습니다.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**면책 조항**:
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 기하기 위해 노력하고 있으나, 자동 번역은 오류나 부정확한 부분이 있을 수 있음을 유의하시기 바랍니다. 원본 문서의 원어본이 권위 있는 자료로 간주되어야 합니다. 중요한 정보의 경우, 전문가의 인간 번역을 권장합니다. 이 번역 사용으로 인해 발생하는 오해나 잘못된 해석에 대해 당사는 책임을 지지 않습니다.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->