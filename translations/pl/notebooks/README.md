# Notatniki

Te notatniki wspierają serię artykułów przykładami do uruchomienia.

| Notatnik | Artykuł | Cel |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Seria 2](../articles/series-2-open-source-rag-end-to-end.md) | Open-source RAG z FastEmbed, trybem lokalnym Qdrant, wyszukiwaniem, ponownym rankingiem, opcjonalną generacją Ollama i odwołaniami do źródeł |

## Uruchom lokalnie

Zainstaluj wymagania dla notatnika, który chcesz uruchomić:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Lub zainstaluj wszystkie zależności:

```powershell
python -m pip install -r requirements\all.txt
```

## Weryfikacja

Z katalogu głównego repozytorium:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Seria 2 może odczytać konfigurację Ollama z pliku `.env` w katalogu głównym repozytorium. Zacznij od [../.env.example](../../../.env.example), który jest pogrupowany według serii.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:
Niniejszy dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Choć dążymy do dokładności, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub niedokładności. Oryginalny dokument w jego języku źródłowym należy uznawać za autorytatywne źródło. W przypadku informacji krytycznych zalecane jest skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z użycia tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->