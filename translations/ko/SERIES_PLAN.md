# 문서를 기반으로 질문에 답변하도록 AI 교육 - 시리즈 계획

이 계획은 공개된 시리즈 1 및 시리즈 2 릴리스를 추적합니다. 이후 Azure 및 평가 작업은 예제가 완전한 엔드투엔드로 검증될 때까지 초안으로 유지됩니다.

명시적으로 지시받기 전까지 변경 사항을 커밋하거나 푸시하지 마십시오.

## 공개 범위

현재 공개 릴리스:

- 시리즈 1 기사: RAG 아키텍처 결정, Azure vs 오픈 소스 트레이드오프, 그리고 파인튜닝의 위치.
- 시리즈 2 기사: 로컬 오픈 소스 RAG 튜토리얼.
- 시리즈 2 노트북: FastEmbed, Qdrant, Ollama, Phi-4-mini를 이용한 실행 가능한 로컬 RAG 실습.
- 샘플 데이터: 학교 정책 및 과정 AI 가이드 Markdown 파일.

초안 작성 되었으나 아직 공개 인덱스에 포함되지 않음:

- Azure AI Search 및 Azure OpenAI 재구성.
- RAG 평가 및 회귀 검사.

## 튜토리얼 시나리오

공유된 시나리오는 학교 정책 조력자입니다.

조력자는 로컬 문서에서 다음 질문에 답변합니다:

```text
Can I use generative AI for my final assignment?
```
  
예상 동작은 다음과 같습니다:

1. 로컬 Markdown 문서를 불러온다.  
2. 문서들을 제목별로 구문 분석하고 청크로 분할한다.  
3. 로컬 임베딩을 생성하고 메타데이터와 함께 검색 가능한 표현을 저장한다.  
4. 관련 정책 구역을 검색한다.  
5. 필요시 재순위를 수행한다.  
6. 근거 있는 답변을 생성하거나 구성한다.  
7. 인용을 반환한다.  
8. 검증 결과를 기록한다.

## 현재 공개 구조

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
  
초안 자료는 `drafts/` 아래에 저장되며 공개 인덱싱 준비가 될 때까지 저장소 검증에서 건너뛰어집니다.

## 시리즈 2 검증

Windows에서 Python 3.12.6으로 검증됨.

- `requirements/open-source-rag.txt` 성공적으로 설치.  
- `notebooks/series-2-open-source-rag.ipynb`를 `nbclient`로 실행함.  
- 로컬 검증 통과: 2개의 샘플 문서가 로드되고, 8개의 청크 생성, FastEmbed가 384 차원 로컬 임베딩 생성, Qdrant 인메모리 컬렉션 초기화, 8개의 벡터 삽입.  
- 테스트 질문: "최종 과제에 생성형 AI를 사용할 수 있나요?"  
- 가벼운 재순위 후 최상위 검색 소스: `school_ai_policy.md`.  
- 가벼운 재순위 후 최상위 검색 구역: `Final Assignments`.  
- 기본 답변 경로: 로컬 투명 답변 작성기.  
- Ollama는 winget을 통해 설치됨; `phi4-mini:3.8b`를 성공적으로 불러옴.  
- Ollama 답변 생성 경로: `phi4-mini:3.8b`로 완료됨.  
- Ollama 모델 파일 크기: 디스크상 약 2.49GB.  
- Ollama 로드된 모델 크기: `ollama ps`에 의해 3.3GB 보고됨.  
- GPU 오프로드: RTX 3060 Laptop GPU에서 `ollama ps`가 100% GPU 사용 보고.  
- 생성 후 관찰된 GPU 메모리: 6GB 중 약 3.5GB 사용.  
- 캐시된 FastEmbed 모델과 Ollama 생성 사용하여 노트북 실행이 약 34초 만에 검증 스크립트를 통과함.  
- 관찰 사항: 초기 문서 로드 시 `sample_data/README.md`가 실수로 포함됨; 노트북은 이제 명시적으로 두 개의 의도된 샘플 문서만 로드함.

## 저장소 검증

- `scripts/verify_notebooks.py`는 로컬 Markdown 링크, 노트북 JSON, 노트북 출력 청결도, 고위험 비밀 패턴을 검증함.  
- `scripts/verify_notebooks.py --execute`는 저장소 루트에서 공개 노트북을 실행함.  
- `drafts/` 아래 초안 자료는 의도적으로 건너뜀.

## 앞으로 작업

- 동일한 시나리오를 Azure AI Search 및 Azure OpenAI로 재구성하여 향후 시리즈 일부로 진행.  
- 로컬 및 Azure 구현이 모두 안정되면 검색 및 답변 평가 추가.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**면책 조항**:
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 기하기 위해 노력하고 있으나, 자동 번역은 오류나 부정확한 부분이 있을 수 있음을 유의하시기 바랍니다. 원본 문서의 원어본이 권위 있는 자료로 간주되어야 합니다. 중요한 정보의 경우, 전문가의 인간 번역을 권장합니다. 이 번역 사용으로 인해 발생하는 오해나 잘못된 해석에 대해 당사는 책임을 지지 않습니다.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->