# Scripts

이 폴더에는 저장소 검증 스크립트가 포함되어 있습니다.

## `verify_notebooks.py`

로컬 마크다운 링크, 노트북 JSON, 노트북 출력 청결도 및 고위험 비밀 패턴을 검증합니다:

```powershell
python scripts\verify_notebooks.py
```

모든 공개 로컬 안전 노트북을 실행합니다:

```powershell
python scripts\verify_notebooks.py --execute
```

GitHub Actions 워크플로우에서도 동일한 스크립트를 사용합니다.

`drafts/` 아래의 초안 자료는 공개 인덱스 준비가 될 때까지 건너뜁니다.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**면책 조항**:
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 기하기 위해 노력하고 있으나, 자동 번역은 오류나 부정확한 부분이 있을 수 있음을 유의하시기 바랍니다. 원본 문서의 원어본이 권위 있는 자료로 간주되어야 합니다. 중요한 정보의 경우, 전문가의 인간 번역을 권장합니다. 이 번역 사용으로 인해 발생하는 오해나 잘못된 해석에 대해 당사는 책임을 지지 않습니다.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->