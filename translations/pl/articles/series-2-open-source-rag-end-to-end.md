# Naucz AI odpowiadać na pytania na podstawie Twoich dokumentów
## Seria 2: Zbuduj lokalny, otwartoźródłowy system RAG od podstaw

![Lokalny, otwartoźródłowy samouczek RAG](../../../assets/images/series-2-local-rag.svg)

> Ten artykuł przekształca dyskusję o architekturze z serii 1 w działający lokalny samouczek RAG. Celem jest najpierw zbudowanie pełnego przepływu pracy na przykładowych danych, bez konta w chmurze i bez sekretów, a następnie wykorzystanie tego działającego punktu wyjścia do podejmowania lepszych decyzji architektonicznych.

System, który zbudujemy, to mały asystent polityki szkolnej. Korzystam z dwóch lokalnych dokumentów Markdown jako bazy wiedzy, a następnie przechodzę przez cały potok RAG: dzielenie na fragmenty, lokalne reprezentacje wektorowe, przechowywanie wektorów w Qdrant, wyszukiwanie, ponowne rankingowanie, komponowanie odpowiedzi z uwzględnieniem źródła oraz opcjonalną lokalną generację za pomocą Ollama i Phi-4-mini.

Nawigacja po serii: [Strona główna repozytorium](../README.md) | Poprzedni: [Seria 1 - RAG, Azure kontra otwartoźródłowe alternatywy i kiedy fine-tuning ma sens](./series-1-rag-azure-open-source-fine-tuning.md)

Notatnik: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Wymagania: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> To jest najlepszy punkt startowy, jeśli chcesz zrozumieć potok RAG zanim utworzysz zasoby w chmurze. Domyślna ścieżka działa lokalnie z reprezentacjami przyjaznymi dla CPU i bez sekretów.

## 1. Co Budujemy

W samouczku z 2023 roku zacząłem od Azure, ponieważ celem było pokazanie, jak Azure AI Search i Azure OpenAI mogą odpowiadać na pytania z dokumentów PDF.

W tej serii 2026 chcę zacząć o warstwę niżej.

Zanim użyję zarządzanych usług, chcę zbudować mały system RAG lokalnie i uczynić każdy krok widocznym: ładowanie dokumentów, dzielenie tekstu na fragmenty, przechowywanie wektorów, wyszukiwanie dowodów, ponowne rankingowanie wyników oraz zwracanie odpowiedzi ze świadomością źródła.

Przykładowy scenariusz to asystent polityki szkolnej. Użytkownik pyta:

```text
Can I use generative AI for my final assignment?
```

System nie powinien odpowiadać z ogólnej pamięci modelu. Powinien wyszukać odpowiednią sekcję polityki i odpowiedzieć na podstawie tego dowodu.

Pełna działająca wersja jest w [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). Kod poniżej pokazuje główne kroki, aby artykuł mógł być czytany jako samouczek.

## 2. Instalacja lokalnych zależności

Utwórz środowisko wirtualne i zainstaluj wymagania serii 2:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Pierwsza wersja korzysta z trybu lokalnego Qdrant i FastEmbed. Klient Python Qdrant obsługuje tryb lokalny in-memory z `QdrantClient(":memory:")`, co jest przydatne do lokalnych samouczków i weryfikacji w stylu CI. FastEmbed daje nam prawdziwy lokalny model osadzający bez konieczności posiadania klucza API do chmury.

Plik wymagań zawiera również `python-dotenv`, ponieważ notatnik może opcjonalnie odczytać nazwę modelu Ollama z `.env`. Do tego lokalnego samouczka nie potrzeba klucza API Azure OpenAI ani OpenAI.

## 3. Załaduj przykładowe dokumenty

Przykładowy korpus jest celowo mały:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

W notatniku ładuję wszystkie pliki Markdown z katalogu `sample_data/`:

```python
from pathlib import Path

repo_root = Path.cwd()
if not (repo_root / "sample_data").exists():
    repo_root = Path.cwd().parent

sample_dir = repo_root / "sample_data"
sample_files = ["course_ai_guidance.md", "school_ai_policy.md"]
documents = []

for file_name in sample_files:
    path = sample_dir / file_name
    documents.append({
        "source": path.name,
        "text": path.read_text(encoding="utf-8"),
    })

print(f"Loaded {len(documents)} documents")
```

Kiedy uruchomiłem notatnik, załadował 2 dokumenty. To wystarczająco mało, aby sprawdzić je ręcznie, co jest przydatne podczas tworzenia pierwszej wersji potoku RAG.

## 4. Dzielenie na fragmenty według nagłówków Markdown

Następnym krokiem jest podzielenie dokumentów na fragmenty.

W tym samouczku korzystam z nagłówków Markdown jako sygnału strukturalnego. Tytuł dokumentu pochodzi z `#`, a każdy fragment sekcji pochodzi z `##`.

> [!NOTE]
> Dzielenie nie jest uniwersalne. W tym samouczku używam nagłówków Markdown, ponieważ dokumenty przykładowe mają klarowną strukturę `#` i `##`. W przypadku dokumentów PDF, Word, slajdów, zgłoszeń lub stron internetowych lepsza strategia może używać granic stron, informacji o układzie, semantycznych sekcji, limitów tokenów, tabel lub metadanych. Ważne jest, aby wybrać strategię dzielenia, która zachowuje sens i możliwość śledzenia źródła dokumentów.

```python
def chunk_markdown(document):
    title = None
    current_heading = None
    current_lines = []
    chunks = []

    def flush():
        if current_heading and current_lines:
            content = "\n".join(current_lines).strip()
            if content:
                chunks.append({
                    "id": f"{document['source']}::{len(chunks)}",
                    "source": document["source"],
                    "title": title or document["source"],
                    "sectionHeading": current_heading,
                    "content": content,
                    "documentVersion": "local-sample-v1",
                    "permissions": ["students", "instructors"],
                })

    for raw_line in document["text"].splitlines():
        line = raw_line.strip()
        if line.startswith("# "):
            title = line[2:].strip()
        elif line.startswith("## "):
            flush()
            current_heading = line[3:].strip()
            current_lines = []
        elif line:
            current_lines.append(line)

    flush()
    return chunks
```

Następnie stosuję to do każdego dokumentu:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

W moim lokalnym uruchomieniu utworzono 8 fragmentów.

Podobało mi się w tej części, że metadane są już użyteczne. Każdy fragment zna swoje `source`, `sectionHeading`, `documentVersion` oraz symboliczne `permissions`. Nawet w małym samouczku ułatwia to rozumowanie na temat cytowań i późniejszego wyszukiwania uwzględniającego uprawnienia.

## 5. Tworzenie lokalnych reprezentacji wektorowych (embeddings)

Dla pierwszej publicznej wersji używam `BAAI/bge-small-en-v1.5` przez FastEmbed.

Dzięki temu samouczek pozostaje lokalny i przyjazny CPU, ale wciąż korzysta z prawdziwego modelu osadzającego, a nie funkcji zastępczej. Pierwsze uruchomienie pobiera wagi modelu. Później notatnik może ponownie wykorzystać lokalny cache.

> [!NOTE]
> Używam `BAAI/bge-small-en-v1.5`, ponieważ jest to lekki model osadzający w języku angielskim, który dobrze działa z FastEmbed i Qdrant w lokalnym samouczku. Tworzy wektory 384-wymiarowe, co sprawia, że przykład jest szybki i tani do uruchomienia lokalnie. To nie jest jedyna dobra opcja. W 2023 wiele samouczków używało hostowanych modeli osadzających, takich jak `text-embedding-ada-002`. Dzisiaj nowsze opcje hostowane, takie jak OpenAI `text-embedding-3-small` i `text-embedding-3-large`, oraz otwartoźródłowe opcje takie jak BGE, E5, MiniLM, Nomic Embed oraz modele wielojęzyczne jak `BAAI/bge-m3` są rozsądnymi wyborami zależnie od obciążenia. W produkcji właściwy model osadzający powinien być dobierany poprzez ocenę wyszukiwania na własnych dokumentach.

Kilka praktycznych alternatyw:

| Rodzina modeli | Kiedy bym ją rozważył |
| --- | --- |
| `text-embedding-ada-002` | Starsza hostowana baza, pojawiająca się w wielu samouczkach z 2023. Dziś nie wybrałbym jej jako domyślnej dla nowego samouczka. |
| `text-embedding-3-small` | Nowoczesna domyślna hostowana opcja, gdy potrzebuję dobrego balansu koszt/wykonanie i nie potrzebuję embeddings wyłącznie lokalnych. |
| `text-embedding-3-large` | Opcja hostowana, gdy jakość wyszukiwania jest ważniejsza niż rozmiar wektora czy koszt osadzania. |
| `BAAI/bge-small-en-v1.5` | Lekka lokalna baza angielska do samouczków, prototypów i eksperymentów przyjaznych CPU. |
| `BAAI/bge-base-en-v1.5` lub `BAAI/bge-large-en-v1.5` | Większe lokalne modele angielskie, gdy chcę lepszą jakość wyszukiwania i mogę pozwolić sobie na większe zużycie zasobów. |
| `BAAI/bge-m3` | Wielojęzyczne lub wyszukiwanie w dłuższym kontekście, szczególnie gdy dokumenty nie są wyłącznie po angielsku. |
| `sentence-transformers/all-MiniLM-L6-v2` | Bardzo mała i szybka baza do wyszukiwania semantycznego. Przydatna, gdy szybkość i prostota są najważniejsze. |
| `nomic-embed-text-v1.5` | Otwarta lokalna opcja embeddingów warta testów w setupach wymagających dłuższego kontekstu lub przenośności. |

```python
import re
from fastembed import TextEmbedding

EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"
embedding_model = TextEmbedding(model_name=EMBEDDING_MODEL_NAME)

def tokenize(text):
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    expanded = []
    for token in tokens:
        expanded.append(token)
        if token.endswith("s") and len(token) > 3:
            expanded.append(token[:-1])
    return expanded
```

Następnie każdemu fragmentowi przypisuję embedding:

```python
texts_to_embed = [
    f"{chunk['title']} {chunk['sectionHeading']} {chunk['content']}"
    for chunk in chunks
]
chunk_vectors = list(embedding_model.embed(texts_to_embed))
VECTOR_SIZE = len(chunk_vectors[0])

for chunk, vector in zip(chunks, chunk_vectors):
    chunk["vector"] = vector
```

## 6. Przechowywanie wektorów w Qdrant w trybie lokalnym

Teraz tworzymy lokalną kolekcję Qdrant działającą w pamięci i wstawiamy fragmenty z metadanymi payload.

> [!NOTE]
> W samouczku z 2023 roku używałem FAISS, ponieważ był to prosty i popularny sposób na pokazanie lokalnego wyszukiwania podobieństwa wektorów z LangChain. FAISS nadal jest użyteczny do szybkich lokalnych eksperymentów. W tej wersji 2026 używam Qdrant, ponieważ chcę, aby samouczek był bliższy produkcyjnemu systemowi RAG. Qdrant pozwala przechowywać wektory razem z metadanymi payload, takimi jak plik źródłowy, nagłówek sekcji, wersja dokumentu i uprawnienia. To ułatwia inspekcję i przygotowuje przykład do filtrowania, cytowań i przyszłego utrwalenia lub wdrożenia na serwerze.

FAISS jest świetny do pokazania wyszukiwania podobieństwa wektorów. Qdrant jest lepszy do pokazania małej, ale produkcyjnie ukształtowanej warstwy wyszukiwania RAG.

Kilka praktycznych alternatyw:

| Magazyn wektorów / warstwa wyszukiwania | Kiedy bym ją rozważył |
| --- | --- |
| Qdrant | Lokalne prototypy, filtrowanie metadanych, wyszukiwanie produkcyjnie przyjazne oraz prosty przepływ pracy Python. |
| Chroma | Szybkie lokalne eksperymenty RAG oraz notatniki, gdzie liczy się prostota. |
| FAISS | Lekka lokalna wyszukiwarka wektorów, gdy potrzebuję tylko wyszukiwania podobieństwa i mogę zarządzać metadanymi oddzielnie. |
| Milvus | Wyszukiwanie wektorów na większą skalę open-source, gdy zespół jest gotowy do obsługi dedykowanej bazy danych wektorowych. |
| Weaviate | Wyszukiwanie wektorowe ze schematem, metadanymi, wyszukiwaniem hybrydowym oraz opcjami wdrożenia zarządzanego lub samodzielnego. |
| Azure AI Search | Korporacyjny RAG na Azure z wyszukiwaniem słów kluczowych, wyszukiwaniem wektorowym, wyszukiwaniem hybrydowym, rankingiem semantycznym, filtrowaniem, bezpieczeństwem i zarządzaniem w jednej warstwie wyszukiwania. |
| PostgreSQL + pgvector | Zespoły już korzystające z PostgreSQL chcące mieć wyszukiwanie wektorowe blisko danych aplikacji. |

```python
from qdrant_client import QdrantClient, models

collection_name = "school_policy_local"
client = QdrantClient(":memory:")

client.create_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(
        size=VECTOR_SIZE,
        distance=models.Distance.COSINE,
    ),
)
```

Następnie wstawiam punkty:

```python
points = []

for idx, chunk in enumerate(chunks):
    payload = {
        key: chunk[key]
        for key in [
            "source",
            "title",
            "sectionHeading",
            "content",
            "documentVersion",
            "permissions",
        ]
    }
    points.append(
        models.PointStruct(
            id=idx,
            vector=chunk["vector"].tolist(),
            payload=payload,
        )
    )

client.upsert(collection_name=collection_name, points=points)
```

W moim uruchomieniu kolekcja wstawiła 8 wektorów.

To tutaj system RAG zaczyna być możliwy do zbadania. Baza danych wektorów przechowuje nie tylko wektory, ale także tekst dowodów i metadane potrzebne do cytowania.

## 7. Pobierz kandydujące fragmenty

Teraz zadajemy pytanie i pobieramy kandydujące fragmenty.

```python
question = "Can I use generative AI for my final assignment?"
query_vector = list(embedding_model.embed([question]))[0].tolist()

raw_results = client.query_points(
    collection_name=collection_name,
    query=query_vector,
    limit=5,
    with_payload=True,
).points
```

W tym momencie wyświetlam pobrane fragmenty przed wygenerowaniem odpowiedzi. To ważne. Jeśli wyszukiwanie zawiedzie, generowanie ukryje problem za płynnym tekstem.

## 8. Dodaj lekki reranker

Gdy pierwszy raz testowałem ścieżkę wyszukiwania, samo podobieństwo wektorów znajdowało powiązane sekcje polityki, ale najbardziej precyzyjna sekcja nie zawsze była na szczycie.

Dlatego dodałem mały, lokalny reranker. Nadaje dodatkową wagę, gdy terminy z pytania pokrywają się z nagłówkiem sekcji i jej zawartością.

```python
query_terms = set(tokenize(question))

def rerank_score(result):
    payload = result.payload
    heading_terms = set(tokenize(payload["sectionHeading"]))
    content_terms = set(tokenize(payload["content"]))
    heading_overlap = len(query_terms & heading_terms)
    content_overlap = len(query_terms & content_terms)
    return result.score + (0.12 * heading_overlap) + (0.02 * content_overlap)

results = sorted(raw_results, key=rerank_score, reverse=True)[:3]
```

Po rerankingu najlepszy wynik był:

```text
school_ai_policy.md / Final Assignments
```

To była oczekiwana sekcja dla testowego pytania.

To była najważniejsza lekcja z pierwszej implementacji. Nawet w maleńkim, lokalnym przykładzie jakość wyszukiwania poprawiła się, gdy połączyłem podobieństwo wektorów z innym sygnałem.

## 9. Komponuj ugruntowaną lokalną odpowiedź

Dla domyślnej ścieżki używam przezroczystego lokalnego kompozytora odpowiedzi zamiast LLM.

```python
top = results[0].payload

answer = (
    "Based on the retrieved policy section, students may use generative AI for "
    "brainstorming, outlining, grammar feedback, and code explanation when the "
    "instructor allows it. They should not submit AI-generated work as their own, "
    "and they should include a disclosure when AI tools are used."
)

print("Answer:")
print(answer)
print("\nSource:")
print(f"{top['source']} / {top['sectionHeading']}")
```

To nie ma być końcowy produkt generujący odpowiedzi. To narzędzie do debugowania. Udowadnia, że wyszukiwanie, metadane i powiązania cytacji działają zanim dodamy wariancję modelu.

## 10. Generuj lokalną odpowiedź z Ollama i Phi-4-mini

Gdy wyszukiwanie działa, notatnik może zastąpić tylko ostatni krok generowania odpowiedzi z użyciem Ollama i `phi4-mini:3.8b`.

> [!NOTE]
> Ollama powinno zastąpić tylko końcowy krok generowania odpowiedzi. Ładowanie dokumentów, dzielenie na fragmenty, przechowywanie wektorów, wyszukiwanie, reranking i powiązania cytacji powinny pozostać bez zmian.

Najpierw notatnik tworzy prompt z dowodami z pobranych fragmentów:

```python
def build_evidence(retrieved_results):
    evidence_blocks = []
    for idx, result in enumerate(retrieved_results, start=1):
        payload = result.payload
        evidence_blocks.append(
            f"[{idx}] Source: {payload['source']} / {payload['sectionHeading']}\n"
            f"{payload['content']}"
        )
    return "\n\n".join(evidence_blocks)

evidence = build_evidence(results)
answer_prompt = (
    "Answer the question using only the evidence below. "
    "If the evidence is insufficient, say that the provided documents do not contain enough information. "
    "End with a Sources line that lists the source file and section.\n\n"
    f"Question: {question}\n\nEvidence:\n{evidence}"
)
```

Dla tego samouczka polecam rodzinę Phi-4-mini Microsoftu przez Ollama jako domyślną lokalną opcję generacji. Nazwa modelu, którą testowałem w Ollama, to:

```powershell
ollama pull phi4-mini:3.8b
```

Możesz szybko sprawdzić, czy model jest dostępny:

```powershell
ollama list
```

Następnie ustaw te zmienne:

```powershell
Copy-Item .env.example .env
```

Otwórz `.env` i odkomentuj wartości Ollama serii 2:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Notatnik ładuje `.env` z katalogu głównego repozytorium za pomocą `python-dotenv`, a następnie wysyła ten sam prompt z dowodami do lokalnego punktu końcowego Ollama `/api/chat` z wyłączonym streamingiem. Jeśli Ollama nie działa lub brakuje `SERIES2_OLLAMA_MODEL`, ten wariant jest pomijany.

> [!NOTE]
> Na tym komputerze `phi4-mini:3.8b` pobrał około 2,49 GB plików modelu. Podczas inferencji Ollama zgłosiło 3,3 GB załadowanego modelu i korzystało z GPU RTX 3060 Laptop.

To daje samouczkowi dwa poziomy:

1. Kompozytor odpowiedzi deterministyczny, wyłącznie CPU.
2. Lokalna generacja odpowiedzi z Ollama i Phi-4-mini.

Potok wyszukiwania jest taki sam w obu.

## 11. Wynik weryfikacji

Uruchomiłem notatnik lokalnie na Windows z Python 3.12.6.

Zainstalowane pakiety:

| Pakiet | Wersja |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Uruchomienie notatnika:

- Notatnik: `notebooks/series-2-open-source-rag.ipynb`
- Wynik wykonania: pomyślny z `nbclient`
- Załadowane dokumenty: 2
- Utworzone fragmenty: 8
- Kolekcja Qdrant: `school_policy_local`
- Wstawione wektory: 8
- Model embeddingu: `BAAI/bge-small-en-v1.5`
- Rozmiar embeddingu: 384
- Pytanie wyszukiwania: "Czy mogę użyć generatywnej AI do mojego końcowego zadania?"
- Ścieżka ponownego rankingu: lekki lokalny leksykalny reranking
- Najlepsze źródło po ponownym rankingu: `school_ai_policy.md`
- Najlepsza sekcja po ponownym rankingu: `Final Assignments`
- Domyślna ścieżka odpowiedzi: lokalny przezroczysty kompozytor odpowiedzi
- Ścieżka generacji Ollama: ukończona modelem `phi4-mini:3.8b`
- Rozmiar pliku modelu Ollama: 2,49 GB na dysku
- Załadowany rozmiar modelu Ollama: 3,3 GB raportowane przez `ollama ps`
- Odciążenie GPU: 100% GPU raportowane przez `ollama ps`
- Obserwowana pamięć GPU po generacji: około 3,5 GB z 6 GB używane na RTX 3060 Laptop GPU
- Wykonanie notebooka z pamięcią podręczną modelu FastEmbed i włączoną generacją Ollama: zakończone w około 34 sekundy wg skryptu weryfikacyjnego

Odpowiedź wygenerowana przez Ollama była:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

Nie nazwałbym tej odpowiedzi idealną. Odpowiada na podstawie właściwych dowodów, ale końcowa linia źródła jest mniej precyzyjna niż deterministyczny format cytowania. To jest przydatne do pokazania w samouczku, ponieważ wyraźnie wskazuje na kolejny problem inżynieryjny: generowanie odpowiedzi również wymaga oceny, nie tylko wyszukiwanie.

Główna rzecz, której się nauczyłem podczas weryfikacji, to to, że jakość wyszukiwania powinna być sprawdzana przed generowaniem odpowiedzi. Wynik osadzenia był już użyteczny, a lekki reranker sprawił, że oczekiwana sekcja polityki pojawiła się jako pierwsza niezawodnie. To właśnie taki drobny aspekt działania systemu chcę, aby samouczek ujawniał, a nie ukrywał.

## 12. Co Dalej

Kolejną poprawą jest porównanie tej lokalnej konfiguracji z zarządzaną wersją Azure tego samego scenariusza asystenta polityki szkolnej. Zachowanie scenariusza stałego powinno ułatwić dostrzeżenie kompromisów: złożoność konfiguracji, kontrola wyszukiwania, integracja tożsamości, zarządzanie operacyjne i koszty.

## 13. Bibliografia

- [Szybki start klienta Qdrant Python](https://python-client.qdrant.tech/quickstart.html)
- [Repozytorium klienta Qdrant na GitHub](https://github.com/qdrant/qdrant-client)
- [Modele wspierane przez FastEmbed](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [Przewodnik po osadzeniach OpenAI](https://platform.openai.com/docs/guides/embeddings)
- [Karta modelu BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [Karta modelu BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3)
- [Karta modelu sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Strona modelu Ollama phi4-mini](https://ollama.com/library/phi4-mini)
- [Dokumentacja Ollama dla Windows](https://docs.ollama.com/windows)
- [Dokumentacja strumieniowania API Ollama](https://docs.ollama.com/api/streaming)
- [Karta modelu Microsoft Phi-4-mini-instruct](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [Przegląd LangGraph](https://docs.langchain.com/oss/python/langgraph)
- [Wprowadzenie do RAG - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

Poprzedni: [Seria 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:
Niniejszy dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Choć dążymy do dokładności, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub niedokładności. Oryginalny dokument w jego języku źródłowym należy uznawać za autorytatywne źródło. W przypadku informacji krytycznych zalecane jest skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z użycia tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->