# 노트북

이 노트북들은 실행 가능한 예제로 기사 시리즈를 지원합니다.

| 노트북 | 기사 | 목적 |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [시리즈 2](../articles/series-2-open-source-rag-end-to-end.md) | FastEmbed, Qdrant 로컬 모드, 검색, 재순위 지정, 선택적 Ollama 생성 및 출처 참조를 포함한 오픈 소스 RAG |

## 로컬 실행

실행하려는 노트북에 필요한 요구 사항을 설치하세요:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

또는 모든 종속성을 설치하세요:

```powershell
python -m pip install -r requirements\all.txt
```

## 검증

레포지토리 루트에서:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

시리즈 2는 레포지토리 루트의 `.env` 파일에서 Ollama 구성을 읽을 수 있습니다. 시리즈별로 그룹화된 [../.env.example](../../../.env.example)에서 시작하세요.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**면책 조항**:
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 기하기 위해 노력하고 있으나, 자동 번역은 오류나 부정확한 부분이 있을 수 있음을 유의하시기 바랍니다. 원본 문서의 원어본이 권위 있는 자료로 간주되어야 합니다. 중요한 정보의 경우, 전문가의 인간 번역을 권장합니다. 이 번역 사용으로 인해 발생하는 오해나 잘못된 해석에 대해 당사는 책임을 지지 않습니다.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->