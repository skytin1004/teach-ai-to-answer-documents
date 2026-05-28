# 요구 사항

각 구현 문서에는 집중된 요구 사항 파일이 있습니다.

| 파일 | 사용처 |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | 선택적 Ollama 생성 도우미를 포함한 Series 2 오픈 소스 RAG 노트북 |
| [all.txt](../../../requirements/all.txt) | 리포지토리 수준 검증 및 CI |

하나의 노트북을 실행할 때는 집중된 파일을 사용하세요. 전체 리포지토리를 검증할 때는 `all.txt`를 사용하세요.

`open-source-rag.txt`와 `all.txt`에는 로컬 임베딩을 위한 `fastembed`와 Series 2가 검색 파이프라인을 변경하지 않고 `.env`에서 Ollama 생성을 선택적으로 활성화할 수 있도록 하는 `python-dotenv`가 포함되어 있습니다.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**면책 조항**:
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 기하기 위해 노력하고 있으나, 자동 번역은 오류나 부정확한 부분이 있을 수 있음을 유의하시기 바랍니다. 원본 문서의 원어본이 권위 있는 자료로 간주되어야 합니다. 중요한 정보의 경우, 전문가의 인간 번역을 권장합니다. 이 번역 사용으로 인해 발생하는 오해나 잘못된 해석에 대해 당사는 책임을 지지 않습니다.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->