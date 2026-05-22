# Naucz SI odpowiadać na pytania na podstawie Twoich dokumentów

![Przegląd systemu RAG opartego na dokumentach](../../assets/images/readme-hero.svg)

To repozytorium gromadzi serię blogów z 2026 roku na temat budowania systemów SI opartych na dokumentach z wykorzystaniem RAG, usług Azure AI, otwartoźródłowych alternatyw oraz workflow zorientowanych na ewaluację.

## Tło

W 2023 roku pracowałem nad parą samouczków o tym, jak nauczyć ChatGPT odpowiadać na pytania z dokumentów PDF, korzystając z Azure AI Search i Azure OpenAI. Idea „ChatGPT na twoich danych” wciąż była wtedy nowa, a celem było pokazanie praktycznego workflow: przechowywać dokumenty, indeksować je, pobierać odpowiednie treści i generować odpowiedzi na podstawie pobranego kontekstu.

W 2026 roku ekosystem RAG jest znacznie większy. Azure AI Search wspiera nowoczesne wzorce pobierania wektorowego i hybrydowego, Azure OpenAI jest częścią szerszego ekosystemu Microsoft Foundry Models, a otwartoźródłowe narzędzia takie jak LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama i vLLM stały się praktycznymi wyborami dla rzeczywistych systemów.

Dlatego chciałem powrócić do tego tematu. Pytanie nie brzmi już tylko „Jak zbudować RAG?” Obecnie jest wiele sposobów, by go zbudować, a ważniejsze pytanie to „Którą architekturę wybrać w mojej sytuacji?”

Ta seria zaczyna się od warstwy decyzyjnej, a następnie zamienia ją w praktyczne samouczki. Pierwsza ścieżka implementacyjna buduje lokalny otwartoźródłowy system RAG, który każdy może uruchomić na przykładowych danych, z Qdrant, Ollama i Phi-4-mini.

## Artykuły

Zobacz [articles/README.md](./articles/README.md) dla indeksu artykułów.

1. [Seria 1: RAG, Azure vs Otwartoźródłowe Alternatywy oraz Kiedy Fine-Tuning Ma Sens](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [Seria 2: Budowa lokalnego otwartoźródłowego systemu RAG krok po kroku](./articles/series-2-open-source-rag-end-to-end.md)

Wkrótce pojawi się:

- Odbudowa tego samego systemu RAG z użyciem Azure AI Search i Azure OpenAI.
- Dodanie ewaluacji i testów regresji wykraczających poza demonstracyjne odpowiedzi.

## Notatniki

Artykuły dotyczące implementacji korzystają z notatników, aby kroki pobierania i ewaluacji mogły być bezpośrednio zbadane. Zobacz [notebooks/README.md](./notebooks/README.md) dla wskazówek dotyczących folderu.

> [!TIP]
> Zacznij od Serii 2, jeśli chcesz najszybszą ścieżkę. Działa lokalnie z przykładowymi danymi, osadzaniami przyjaznymi CPU, lokalnym trybem Qdrant i bez danych uwierzytelniających w chmurze.

| Seria | Notatnik | Wymagania | Weryfikacja lokalna |
| --- | --- | --- | --- |
| Seria 2 | [Notatnik otwartoźródłowego RAG](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Tryb lokalny Qdrant, pobieranie, reranking i podłączenie źródeł zweryfikowane |

Aby uruchomić notatnik lokalnie, utwórz środowisko wirtualne i zainstaluj pasujący plik wymagań. Na przykład:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## Przykładowe dane

Notatniki korzystają z małego lokalnego korpusu w [sample_data](../../sample_data), dzięki czemu przykłady mogą działać bez prywatnych dokumentów czy danych uwierzytelniających w chmurze. Szczegóły znajdziesz w [sample_data/README.md](./sample_data/README.md).

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## Podsumowanie weryfikacji lokalnej

Wyniki weryfikacji są zapisywane w każdym artykule oraz w [SERIES_PLAN.md](./SERIES_PLAN.md).

| Obszar | Wynik |
| --- | --- |
| Seria 2 ścieżka otwartoźródłowa | FastEmbed wygenerował lokalne osadzenia o wymiarze 384, kolekcja Qdrant in-memory wstawiła 8 wektorów, lekki reranking pobrał oczekiwany fragment; opcjonalna generacja Ollama zakończona z `phi4-mini:3.8b` |

Notatnik lokalny celowo unika twardo zakodowanych sekretów.

## Lokalna generacja Ollama

Notatnik Serii 2 jest domyślnie bezpieczny lokalnie. Aby włączyć lokalną generację Ollama, skopiuj [.env.example](../../.env.example) do `.env` i wypełnij wartości Serii 2.

Dla generacji Ollama z Serii 2 odkomentuj:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Notatnik Serii 2 automatycznie ładuje `.env` z katalogu głównego repozytorium przy pomocy `python-dotenv`.

> [!IMPORTANT]
> Nie zatwierdzaj plików `.env`, kluczy API, prywatnych punktów końcowych ani wartości specyficznych dla tenantów. Repozytorium celowo nie umieszcza sekretów w plikach Markdown ani notatnikach.

Pliki wymagań są udokumentowane w [requirements/README.md](./requirements/README.md).

Aby zweryfikować linki, strukturę notatników, czystość wyników oraz wzorce sekretów wysokiego ryzyka:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

Skrypty weryfikacyjne udokumentowane są w [scripts/README.md](./scripts/README.md).

Aby wykonać wszystkie lokalnie bezpieczne notatniki w jednym środowisku:

```powershell
python scripts\verify_notebooks.py --execute
```

Ten sam proces weryfikacji działa w GitHub Actions przy pushach, pull requestach i ręcznych uruchomieniach workflow. Wstępne artykuły i notatniki są celowo wyłączone z publicznej ścieżki weryfikacji.

Przed publikacją aktualizacji użyj [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md).

Zobacz [CHANGELOG.md](./CHANGELOG.md) dla aktualnego podsumowania nieopublikowanych zmian.

Zasady dotyczące wkładu i higieny notatników znajdują się w [CONTRIBUTING.md](./CONTRIBUTING.md).

## Obsługa wielu języków

### Wspierane przez Co-op Translator (Automatyczne i Zawsze Aktualne)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabski](../ar/README.md) | [Bengalski](../bn/README.md) | [Bułgarski](../bg/README.md) | [Birmański (Myanmar)](../my/README.md) | [Chiński (uproszczony)](../zh-CN/README.md) | [Chiński (tradycyjny, Hongkong)](../zh-HK/README.md) | [Chiński (tradycyjny, Makau)](../zh-MO/README.md) | [Chiński (tradycyjny, Tajwan)](../zh-TW/README.md) | [Chorwacki](../hr/README.md) | [Czeski](../cs/README.md) | [Duński](../da/README.md) | [Niderlandzki](../nl/README.md) | [Estoński](../et/README.md) | [Fiński](../fi/README.md) | [Francuski](../fr/README.md) | [Niemiecki](../de/README.md) | [Grecki](../el/README.md) | [Hebrajski](../he/README.md) | [Hindi](../hi/README.md) | [Węgierski](../hu/README.md) | [Indonezyjski](../id/README.md) | [Włoski](../it/README.md) | [Japoński](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Koreański](../ko/README.md) | [Litewski](../lt/README.md) | [Malajski](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepalski](../ne/README.md) | [Pidgin Nigeryjski](../pcm/README.md) | [Norweski](../no/README.md) | [Perski (Farsi)](../fa/README.md) | [Polski](./README.md) | [Portugalski (Brazylia)](../pt-BR/README.md) | [Portugalski (Portugalia)](../pt-PT/README.md) | [Pendżabski (Gurmukhi)](../pa/README.md) | [Rumuński](../ro/README.md) | [Rosyjski](../ru/README.md) | [Serbski (cyrylica)](../sr/README.md) | [Słowacki](../sk/README.md) | [Słoweński](../sl/README.md) | [Hiszpański](../es/README.md) | [Suahili](../sw/README.md) | [Szwedzki](../sv/README.md) | [Tagalog (Filipiński)](../tl/README.md) | [Tamilski](../ta/README.md) | [Telugu](../te/README.md) | [Tajski](../th/README.md) | [Turecki](../tr/README.md) | [Ukraiński](../uk/README.md) | [Urdu](../ur/README.md) | [Wietnamski](../vi/README.md)

> **Wolisz sklonować lokalnie?**
>
> To repozytorium zawiera ponad 50 tłumaczeń językowych, co znacznie zwiększa rozmiar pobierania. Aby sklonować bez tłumaczeń, użyj sparse checkout:
>
> **Bash / macOS / Linux:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (Windows):**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> To daje wszystko, co potrzebne, aby ukończyć kurs z dużo szybszym pobraniem.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:
Niniejszy dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Choć dążymy do dokładności, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub niedokładności. Oryginalny dokument w jego języku źródłowym należy uznawać za autorytatywne źródło. W przypadku informacji krytycznych zalecane jest skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z użycia tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->