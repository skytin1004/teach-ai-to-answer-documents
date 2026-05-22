# Ноутбуки

Эти ноутбуки поддерживают серию статей с выполняемыми примерами.

| Ноутбук | Статья | Назначение |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Серия 2](../articles/series-2-open-source-rag-end-to-end.md) | Open-source RAG с FastEmbed, локальным режимом Qdrant, поиском, переранжированием, опциональной генерацией Ollama и ссылками на источники |

## Запуск локально

Установите зависимости для нужного ноутбука:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Или установите все зависимости:

```powershell
python -m pip install -r requirements\all.txt
```

## Проверка

Из корня репозитория:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Серия 2 может считывать конфигурацию Ollama из файла `.env` в корне репозитория. Начните с [../.env.example](../../../.env.example), который сгруппирован по сериям.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Отказ от ответственности**:
Этот документ был переведен с использованием сервиса машинного перевода [Co-op Translator](https://github.com/Azure/co-op-translator). Несмотря на наши усилия по обеспечению точности, имейте в виду, что автоматический перевод может содержать ошибки или неточности. Оригинальный документ на его исходном языке следует считать авторитетным источником. Для получения критически важной информации рекомендуется обратиться к профессиональному человеческому переводу. Мы не несем ответственности за любые недоразумения или неправильные толкования, возникшие в результате использования этого перевода.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->