# Wymagania

Każdy artykuł implementacyjny ma skupiony plik wymagań.

| Plik | Używany przez |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | Notebook open-source RAG serii 2, w tym opcjonalne pomocniki generowania Ollama |
| [all.txt](../../../requirements/all.txt) | Weryfikacja na poziomie repozytorium i CI |

Używaj skupionego pliku podczas uruchamiania jednego notebooka. Używaj `all.txt` podczas weryfikacji całego repozytorium.

`open-source-rag.txt` i `all.txt` zawierają `fastembed` dla lokalnych embeddingów oraz `python-dotenv`, aby seria 2 mogła opcjonalnie włączyć generowanie Ollama z `.env` bez zmiany pipeline pobierania.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:
Niniejszy dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Choć dążymy do dokładności, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub niedokładności. Oryginalny dokument w jego języku źródłowym należy uznawać za autorytatywne źródło. W przypadku informacji krytycznych zalecane jest skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z użycia tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->