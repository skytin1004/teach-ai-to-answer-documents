# Naucz AI odpowiadać na pytania na podstawie Twoich dokumentów - Plan serii

Ten plan śledzi publiczne wydania Serii 1 i Serii 2. Późniejsze prace nad Azure i ewaluacją są utrzymywane jako szkice, dopóki przykłady nie będą w pełni end-to-end i zweryfikowane.

Nie wprowadzaj ani nie wysyłaj zmian, dopóki nie zostanie to wyraźnie zalecane.

## Zakres publiczny

Aktualne publiczne wydanie:

- Artykuł Serii 1: decyzje dotyczące architektury RAG, kompromisy Azure vs open source oraz miejsce fine-tuningu.
- Artykuł Serii 2: lokalny tutorial RAG open source.
- Notatnik Serii 2: działające lokalne laboratorium RAG z FastEmbed, Qdrant, Ollama i Phi-4-mini.
- Przykładowe dane: pliki Markdown z polityką szkoły i wytycznymi AI do kursów.

Szkice, które jeszcze nie są w publicznym indeksie:

- Przebudowa Azure AI Search i Azure OpenAI.
- Ewaluacja RAG i kontrole regresji.

## Scenariusz tutorialu

Udostępniony scenariusz to asystent polityki szkolnej.

Asystent odpowiada na to pytanie na podstawie lokalnych dokumentów:

```text
Can I use generative AI for my final assignment?
```

Oczekiwane zachowanie to:

1. Załaduj lokalne dokumenty Markdown.
2. Przeanalizuj i podziel je na fragmenty według nagłówków.
3. Utwórz lokalne osadzenia i przechowuj przeszukiwalne reprezentacje z metadanymi.
4. Pobierz odpowiednią sekcję polityki.
5. W razie potrzeby przeprowadź ponowne sortowanie (reranking).
6. Wygeneruj lub zbuduj uargumentowaną odpowiedź.
7. Zwróć cytowania.
8. Zapisz wyniki weryfikacji.

## Aktualna publiczna struktura

```text
.
├── README.md
├── SERIES_PLAN.md
├── articles/
│   ├── README.md
│   ├── series-1-rag-azure-open-source-fine-tuning.md
│   └── series-2-open-source-rag-end-to-end.md
├── notebooks/
│   ├── README.md
│   └── series-2-open-source-rag.ipynb
├── sample_data/
│   ├── README.md
│   ├── course_ai_guidance.md
│   └── school_ai_policy.md
├── requirements/
│   ├── README.md
│   ├── all.txt
│   └── open-source-rag.txt
└── scripts/
    ├── README.md
    └── verify_notebooks.py
```

Materiał w szkicach jest przechowywany w folderze `drafts/` i jest pomijany podczas weryfikacji repozytorium, dopóki nie będzie gotowy do publicznego indeksowania.

## Weryfikacja Serii 2

Zweryfikowano na Windows z Python 3.12.6.

- Pomyślnie zainstalowano `requirements/open-source-rag.txt`.
- Uruchomiono `notebooks/series-2-open-source-rag.ipynb` za pomocą `nbclient`.
- Lokalna weryfikacja zakończona powodzeniem: załadowano 2 próbne dokumenty, utworzono 8 fragmentów, FastEmbed wygenerował lokalne osadzenia o wymiarze 384, zainicjowano kolekcję Qdrant w pamięci, wstawiono 8 wektorów.
- Testowe pytanie: "Czy mogę użyć generatywnej AI do mojego zadania końcowego?"
- Najlepiej dopasowane źródło po lekkim rerankingu: `school_ai_policy.md`.
- Najlepiej dopasowana sekcja po lekkim rerankingu: `Final Assignments`.
- Domyślna ścieżka odpowiedzi: lokalny transparentny kompozytor odpowiedzi.
- Ollama zainstalowana przez winget; `phi4-mini:3.8b` pobrany pomyślnie.
- Ścieżka generowania odpowiedzi Ollama: zakończona z `phi4-mini:3.8b`.
- Rozmiar pliku modelu Ollama: około 2,49GB na dysku.
- Ładowany rozmiar modelu Ollama: 3,3GB zgłoszone przez `ollama ps`.
- Odciążenie GPU: 100% GPU zgłoszone przez `ollama ps` na RTX 3060 Laptop GPU.
- Obserwowany użytek pamięci GPU po generowaniu: około 3,5GB z 6GB.
- Wykonanie notatnika z cache’owanym modelem FastEmbed i włączonym generowaniem Ollama zakończyło się powodzeniem w około 34 sekundy przez skrypt weryfikujący.
- Obserwacja: wczesny etap ładowania dokumentów przypadkowo uwzględnił `sample_data/README.md`; notatnik teraz ładuje tylko dwa przeznaczone dokumenty próbne w sposób jawny.

## Weryfikacja repozytorium

- `scripts/verify_notebooks.py` waliduje lokalne linki w Markdown, JSON notatników, czystość wyjść notatnika oraz wzorce wysokiego ryzyka sekretów.
- `scripts/verify_notebooks.py --execute` uruchamia publiczne notatniki z katalogu głównego repozytorium.
- Materiały szkicowe w `drafts/` są celowo pomijane.

## Kolejne prace

- Przebuduj ten sam scenariusz z Azure AI Search i Azure OpenAI jako przyszły element serii.
- Dodaj ewaluację wyszukiwania i odpowiedzi, gdy lokalne i Azure implementacje będą stabilne.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:
Niniejszy dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Choć dążymy do dokładności, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub niedokładności. Oryginalny dokument w jego języku źródłowym należy uznawać za autorytatywne źródło. W przypadku informacji krytycznych zalecane jest skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z użycia tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->