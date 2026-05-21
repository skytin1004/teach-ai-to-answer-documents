# Naucz SI, aby odpowiadało na pytania na podstawie Twoich dokumentów

To repozytorium zawiera serię blogową z 2026 roku dotyczącą budowania systemów SI opartych na dokumentach z wykorzystaniem RAG, usług Azure AI, alternatyw open-source oraz workflow nastawionych na ewaluację.

## Tło

W 2023 roku pracowałem nad serią dwóch samouczków na temat nauczania ChatGPT odpowiadania na pytania z dokumentów PDF z użyciem Azure AI Search i Azure OpenAI. Idea "ChatGPT na twoich danych" wciąż wydawała się wtedy nowa, a celem było pokazanie praktycznego workflow: przechowywanie dokumentów, indeksowanie ich, wyszukiwanie odpowiednich treści oraz generowanie odpowiedzi na podstawie wyszukanego kontekstu.

W 2026 ekosystem RAG jest znacznie większy. Azure AI Search wspiera nowoczesne wzorce wyszukiwania wektorowego i hybrydowego, Azure OpenAI jest częścią szerszego ekosystemu modeli Microsoft Foundry, a narzędzia open-source takie jak LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama i vLLM stały się praktycznym wyborem dla rzeczywistych systemów.

Dlatego chciałem wrócić do tego tematu. Pytanie nie brzmi już tylko "Jak zbudować RAG?" Obecnie istnieje wiele sposobów na jego budowę, a ważniejsze pytanie to "Którą architekturę wybrać dla mojej sytuacji?"

Ta seria zaczyna się od tej warstwy podejmowania decyzji. Zanim zagłębi się w implementację, omawia, dlaczego usługi AI potrzebują wyszukiwania, kiedy opłacają się zarządzane usługi oparte na Azure, kiedy lepsze są alternatywy open-source oraz gdzie pasuje dostrajanie.

## Artykuły

1. [Seria 1: RAG, Azure vs alternatywy open-source oraz kiedy sensowne jest dostrajanie](./series-1-rag-azure-open-source-fine-tuning.md)

## Wsparcie wielojęzyczne

### Wspierane przez Co-op Translator (Zautomatyzowane i zawsze aktualne)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabski](../ar/README.md) | [Bengalski](../bn/README.md) | [Bułgarski](../bg/README.md) | [Birmański (Myanmar)](../my/README.md) | [Chiński (uproszczony)](../zh-CN/README.md) | [Chiński (tradycyjny, Hongkong)](../zh-HK/README.md) | [Chiński (tradycyjny, Makau)](../zh-MO/README.md) | [Chiński (tradycyjny, Tajwan)](../zh-TW/README.md) | [Chorwacki](../hr/README.md) | [Czeski](../cs/README.md) | [Duński](../da/README.md) | [Niderlandzki](../nl/README.md) | [Estoński](../et/README.md) | [Fiński](../fi/README.md) | [Francuski](../fr/README.md) | [Niemiecki](../de/README.md) | [Grecki](../el/README.md) | [Hebrajski](../he/README.md) | [Hindi](../hi/README.md) | [Węgierski](../hu/README.md) | [Indonezyjski](../id/README.md) | [Włoski](../it/README.md) | [Japoński](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Koreański](../ko/README.md) | [Litewski](../lt/README.md) | [Malajski](../ms/README.md) | [Malajalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepalski](../ne/README.md) | [Nigeryjski Pidgin](../pcm/README.md) | [Norweski](../no/README.md) | [Perski (Farsi)](../fa/README.md) | [Polski](./README.md) | [Portugalski (Brazylia)](../pt-BR/README.md) | [Portugalski (Portugalia)](../pt-PT/README.md) | [Pendżabski (Gurmukhi)](../pa/README.md) | [Rumuński](../ro/README.md) | [Rosyjski](../ru/README.md) | [Serbski (cyrylica)](../sr/README.md) | [Słowacki](../sk/README.md) | [Słoweński](../sl/README.md) | [Hiszpański](../es/README.md) | [Suahili](../sw/README.md) | [Szwedzki](../sv/README.md) | [Tagalog (Filipiński)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Tajski](../th/README.md) | [Turecki](../tr/README.md) | [Ukraiński](../uk/README.md) | [Urdu](../ur/README.md) | [Wietnamski](../vi/README.md)

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
> Dzięki temu masz wszystko, co potrzebne do ukończenia kursu, przy znacznie szybszym pobieraniu.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:
Niniejszy dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Choć dążymy do dokładności, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub niedokładności. Oryginalny dokument w jego języku źródłowym należy uznawać za autorytatywne źródło. W przypadku informacji krytycznych zalecane jest skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z użycia tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->