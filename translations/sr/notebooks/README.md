# Бележнице

Ове бележнице подржавају серију чланака са извршним примерима.

| Бележница | Чланак | Сврха |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Серија 2](../articles/series-2-open-source-rag-end-to-end.md) | Отворени RAG са FastEmbed, Qdrant локални режим, проналажење, поновно рангирање, опционална Ollama генерација и референце извора |

## Покрени локално

Инсталирајте захтеве за бележницу коју желите да покренете:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Или инсталирајте све зависности:

```powershell
python -m pip install -r requirements\all.txt
```

## Верификуј

Из корена репозиторијума:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Серија 2 може читати Ollama конфигурацију из `.env` фајла у корену репозиторијума. Почните од [../.env.example](../../../.env.example), који је груписан по серијама.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Изјава о одрицању одговорности**:
Овај документ је преведен коришћењем услуге за аутоматски превод [Co-op Translator](https://github.com/Azure/co-op-translator). Иако тежимо тачности, имајте у виду да аутоматски преводи могу садржати грешке или нетачности. Оригинални документ на његовом изворном језику треба сматрати ауторитативним извором. За критичне информације препоручује се професионални људски превод. Нисмо одговорни за било каква неспоразума или погрешна тумачења која произилазе из коришћења овог превода.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->