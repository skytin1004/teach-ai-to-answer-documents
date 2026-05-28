# Changelog

## Unreleased

Zakres początkowego publicznego wydania dla **Teach AI to Answer Questions Based on Your Documents**.

### Dodano

- Artykuł z serii 1 o decyzjach dotyczących architektury RAG, kompromisach między Azure a open-source oraz roli fine-tuningu.
- Artykuł i notatnik z serii 2 dla lokalnego open-source'owego workflow RAG wykorzystującego lokalny tryb Qdrant, lokalne osadzanie FastEmbed, lekkie reranking, Ollama i Phi-4-mini.
- Format samouczka krok po kroku z serii 2 w trybie end-to-end z fragmentami Pythona i notatkami weryfikacyjnymi z wykonywanego notatnika.
- Opcjonalna ścieżka generowania odpowiedzi z serii 2 z Ollama i Phi-4-mini, przy zachowaniu lokalnego, przyjaznego CPU sposobu pobierania jako domyślnej ścieżki.
- Lokalna weryfikacja Ollama dla serii 2 z użyciem `phi4-mini:3.8b` na RTX 3060 Laptop GPU.
- Przykładowe dane dotyczące polityki szkolnej i wsparcia AI dla kursów.
- Pliki wymagań dla publicznego notatnika i weryfikacji na poziomie repozytorium.
- Skrypt weryfikujący repozytorium dla lokalnych linków Markdown oraz walidacji/uruchamiania notatnika.
- Workflow GitHub Actions do weryfikacji notatnika.
- `.env.example` dla opcjonalnej lokalnej konfiguracji generowania Ollama bez konieczności commitowania lokalnej konfiguracji.
- Pliki README na poziomie folderów dla artykułów, notatników, wymagań, przykładowych danych i skryptów.
- Lista kontrolna publikacji dla bezpieczeństwa publicznego i weryfikacji.
- Wersja robocza workspace dla przyszłych treści związanych z Azure i ewaluacją.

### Zweryfikowano

- Lokalna walidacja linków Markdown zakończona pomyślnie.
- Notatnik z serii 2 zweryfikowany pomyślnie.
- Notatnik z serii 2 pomyślnie wykonany w lokalnym środowisku weryfikacyjnym.
- Pliki notatników są przechowywane bez zapisanych wyników ani liczników wykonania.
- Nie wprowadzono żadnych prawdziwych sekretów.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:
Niniejszy dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Choć dążymy do dokładności, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub niedokładności. Oryginalny dokument w jego języku źródłowym należy uznawać za autorytatywne źródło. W przypadku informacji krytycznych zalecane jest skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z użycia tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->