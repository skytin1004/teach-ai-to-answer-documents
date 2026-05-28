# ನೋಟ್ಬುಕ್ಸ್

ಈ ನೋಟ್ಬುಕ್ಸ್ ರನ ಮಾಡಬಹುದಾದ ಉದಾಹರಣೆಗಳೊಂದಿಗೆ ಲೇಖನ ಸರಣಿಯನ್ನು ಬೆಂಬಲಿಸುತ್ತವೆ.

| ನೋಟ್ಬುಕ್ | ಲೇಖನ | ಉದ್ದೇಶ |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Series 2](../articles/series-2-open-source-rag-end-to-end.md) | ಫಾಸ್ಟ್‌ಎಂಬೆಡ್, Qdrant ಸ್ಥಳೀಯ ಮೋಡ್, ರಿಟ್ರೀವಲ್, ರೀ-ರ್ಯಾಂಕಿಂಗ್, ಐಚ್ಛಿಕ ಒಳ್ಳಾಮಾ ಉತ್ಪಾದನೆ ಮತ್ತು ಮೂಲ ಉಲ್ಲೇಖಗಳೊಂದಿಗೆ ಓಪನ್‌ಸೋರ್ಸ್ RAG |

## ಸ್ಥಳೀಯವಾಗಿ ರನ್ ಮಾಡಿ

ನೀವು ರನ್ ಮಾಡಲು ಇಚ್ಛಿಸುವ ನೋಟ್ಬುಕ್‌ಗಾಗಿ ಅವಶ್ಯಕತೆಗಳನ್ನು ಇನ್‌ಸ್ಟಾಲ್ ಮಾಡಿ:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

ಅಥವಾ ಎಲ್ಲಾ ಅವಲಂಬನೆಯನ್ನು ಇನ್‌ಸ್ಟಾಲ್ ಮಾಡಿ:

```powershell
python -m pip install -r requirements\all.txt
```

## ಪರಿಶೀಲಿಸಿ

ಗ್ರಂಥಾಲಯ ಮೂಲದಿಂದ:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

ಸಿರೀಸ್ 2 ಒಳ್ಳಾಮಾ ಕಾನ್ಫಿಗರೇಶನ್ ಅನ್ನು ಗ್ರಂಥಾಲಯ-ಮೂಲ `.env` ಫೈಲ್ ನಿಂದ ಓದುತ್ತದೆ. [../.env.example](../../../.env.example) ನಿಂದ ಪ್ರಾರಂಭಿಸಿ, ಇದು ಸರಣಿಯಿಂದ ಗುಂಪುಗೊಳಿಸಲಾಗಿದೆ.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ಅಸ್ವೀಕಾರ**:
ಈ ದಸ್ತಾವೇಜು AI ಅನುವಾದ ಸೇವೆ [Co-op Translator](https://github.com/Azure/co-op-translator) ಬಳಸಿ ಅನುವಾದಿಸಲಾಗಿದೆ. ನಾವು ನಿಖರತೆಯನ್ನು ಸಾಧಿಸಲು ಪ್ರಯತ್ನಿಸುತ್ತಿದ್ದರೂ, ದಯವಿಟ್ಟು ಗಮನಿಸಿ, ಸ್ವಯಂಚಾಲಿತ ಅನುವಾದಗಳಲ್ಲಿ ದೋಷಗಳು ಅಥವಾ ಅಸಡ್ಡೆಗಳು ಇರಬಹುದು. ಮೂಲ ಭಾಷೆಯಲ್ಲಿರುವ ಮೂಲ ದಸ್ತಾವೇಜು ಪ್ರಾಮಾಣಿಕ ಮೂಲವೆಂದು ಪರಿಗಣಿಸಬೇಕು. ಪ್ರಮುಖ ಮಾಹಿತಿಗಾಗಿ, ವೃತ್ತಿಪರ ಮಾನವ ಅನುವಾದವನ್ನು ಶಿಫಾರಸು ಮಾಡಲಾಗುತ್ತದೆ. ಈ ಅನುವಾದವನ್ನು ಬಳಸುವ ಮೂಲಕ ಉಂಟಾಗುವ ಯಾವುದೇ ತಪ್ಪು ಅರ್ಥಗಳ ಅಥವಾ ತಪ್ಪು ವ್ಯಾಖ್ಯಾನಗಳ ಬಗ್ಗೆ ನಾವು ಹೊಣೆಗಾರರಲ್ಲ.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->