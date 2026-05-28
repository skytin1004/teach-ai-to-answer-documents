# Бележници

Тези бележници поддържат поредицата от статии с изпълними примери.

| Бележник | Статия | Цел |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Поредица 2](../articles/series-2-open-source-rag-end-to-end.md) | Отворен RAG с FastEmbed, локален режим Qdrant, извличане, пренареждане, опционално генериране с Ollama и препратки към източници |

## Стартиране локално

Инсталирайте изискванията за бележника, който искате да стартирате:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Или инсталирайте всички зависимости:

```powershell
python -m pip install -r requirements\all.txt
```

## Проверка

От корена на хранилището:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Поредица 2 може да прочете конфигурацията на Ollama от `.env` файл в корена на хранилището. Започнете от [../.env.example](../../../.env.example), който е групиран по серии.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Отказ от отговорност**:
Този документ е преведен с помощта на AI преводачески услуга [Co-op Translator](https://github.com/Azure/co-op-translator). Въпреки че се стремим към точност, моля имайте предвид, че автоматизираните преводи могат да съдържат грешки или неточности. Оригиналният документ на неговия роден език трябва да се счита за авторитетен източник. За критична информация се препоръчва професионален човешки превод. Ние не носим отговорност за каквито и да е недоразумения или неправилни тълкувания, произтичащи от използването на този превод.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->