# Skrypty

Ten folder zawiera skrypty do weryfikacji repozytorium.

## `verify_notebooks.py`

Waliduje lokalne linki Markdown, JSON notatników, czystość wyjścia notatników oraz wzory wysokiego ryzyka sekretów:

```powershell
python scripts\verify_notebooks.py
```

Wykonuje wszystkie publiczne notatniki lokalnie bezpieczne:

```powershell
python scripts\verify_notebooks.py --execute
```

Workflow GitHub Actions używa tego samego skryptu.

Materiały robocze w `drafts/` są pomijane, dopóki nie będą gotowe do publicznego indeksu.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:
Niniejszy dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Choć dążymy do dokładności, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub niedokładności. Oryginalny dokument w jego języku źródłowym należy uznawać za autorytatywne źródło. W przypadku informacji krytycznych zalecane jest skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z użycia tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->