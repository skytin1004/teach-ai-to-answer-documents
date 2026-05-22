# Ноутбуки

Ці ноутбуки підтримують серію статей із виконуваними прикладами.

| Ноутбук | Стаття | Мета |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Серія 2](../articles/series-2-open-source-rag-end-to-end.md) | Відкрите джерело RAG з FastEmbed, локальний режим Qdrant, пошук, повторне ранжування, необов’язкова генерація Ollama та посилання на джерела |

## Запуск локально

Встановіть вимоги для ноутбука, який ви хочете запустити:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Або встановіть усі залежності:

```powershell
python -m pip install -r requirements\all.txt
```

## Перевірка

З кореня репозиторію:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Серія 2 може зчитувати конфігурацію Ollama з файлу `.env` у корені репозиторію. Почніть з [../.env.example](../../../.env.example), який згрупований за серіями.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Відмова від відповідальності**:
Цей документ було перекладено за допомогою сервісу штучного інтелекту для перекладу [Co-op Translator](https://github.com/Azure/co-op-translator). Хоча ми прагнемо до точності, будь ласка, майте на увазі, що автоматичні переклади можуть містити помилки або неточності. Оригінальний документ рідною мовою слід вважати авторитетним джерелом. Для критично важливої інформації рекомендується професійний людський переклад. Ми не несемо відповідальності за будь-які непорозуміння або неправильні тлумачення, що виникли внаслідок використання цього перекладу.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->