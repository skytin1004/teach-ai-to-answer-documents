# Contributing

이 저장소는 블로그 시리즈와 실행 가능한 노트북 예제로 구성되어 있습니다.

## Pull Request를 열기 전

로컬 검증 스크립트를 실행하세요:

```powershell
python scripts\verify_notebooks.py
```

구현이나 노트북 변경 사항의 경우, 로컬 안전 노트북 실행을 실행하세요:

```powershell
python scripts\verify_notebooks.py --execute
```

## 노트북 지침

- 노트북을 읽기 쉽고 관련 기사에 집중되도록 유지하세요.
- 저장된 노트북 출력이나 실행 횟수를 커밋하지 마세요.
- 기사가 특정 외부 리소스를 요구하지 않는 한 `sample_data/`의 작은 샘플 데이터를 사용하세요.
- 동작이 변경될 경우 관련 기사에 검증 결과를 기록하세요.

## 비밀 및 자격 증명

- API 키, 토큰, 비밀번호, 비공개 엔드포인트, `.env` 파일을 커밋하지 마세요.
- `.env.example`은 플레이스홀더 값 용도로만 사용하세요.
- 선택적 로컬 Ollama 실험에는 환경 변수를 사용하세요.

## 문서화

- 기사 내비게이션 링크를 최신 상태로 유지하세요.
- 새 기사, 노트북, 요구 사항 파일 또는 샘플 데이터 파일을 추가할 때 `README.md`를 업데이트하세요.
- 공개 저장소 업데이트를 게시하기 전에 `CHANGELOG.md`를 업데이트하세요.

## 검증

GitHub Actions 워크플로우가 실행됩니다:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

`drafts/`에 있는 초안 자료는 공개 인덱싱 준비가 될 때까지 저장소 검증에서 건너뜁니다.

## 이슈

기사 수정은 기사 피드백 템플릿을, 노트북 실행 문제는 노트북 이슈 템플릿을 사용하세요.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**면책 조항**:
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 기하기 위해 노력하고 있으나, 자동 번역은 오류나 부정확한 부분이 있을 수 있음을 유의하시기 바랍니다. 원본 문서의 원어본이 권위 있는 자료로 간주되어야 합니다. 중요한 정보의 경우, 전문가의 인간 번역을 권장합니다. 이 번역 사용으로 인해 발생하는 오해나 잘못된 해석에 대해 당사는 책임을 지지 않습니다.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->