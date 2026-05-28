# Bringen Sie KI bei, Fragen basierend auf Ihren Dokumenten zu beantworten

![Übersicht des dokumentengestützten AI RAG-Systems](../../assets/images/readme-hero.svg)

Dieses Repository sammelt eine Blogserie aus dem Jahr 2026 über den Aufbau dokumentengestützter AI-Systeme mit RAG, Azure AI-Diensten, Open-Source-Alternativen und evaluationsorientierten Workflows.

## Hintergrund

Im Jahr 2023 arbeitete ich an einem Paar von Tutorials darüber, wie man ChatGPT beibringt, Fragen aus PDF-Dokumenten mit Azure AI Search und Azure OpenAI zu beantworten. Die Idee von „ChatGPT auf Ihren Daten“ fühlte sich damals noch neu an, und das Ziel war es, einen praktischen Workflow zu zeigen: Dokumente speichern, sie indexieren, relevante Inhalte abrufen und Antworten aus dem abgerufenen Kontext generieren.

Im Jahr 2026 ist das RAG-Ökosystem viel größer. Azure AI Search unterstützt moderne Vektor- und hybride Abrufmuster, Azure OpenAI ist Teil des größeren Microsoft Foundry Models Ökosystems, und Open-Source-Tools wie LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama und vLLM sind zu praktischen Optionen für reale Systeme geworden.

Deshalb wollte ich dieses Thema noch einmal aufgreifen. Die Frage lautet nicht mehr nur „Wie baue ich RAG?“ Es gibt jetzt viele Möglichkeiten, es zu bauen, und die wichtigere Frage ist „Welche Architektur soll ich für meine Situation wählen?“

Diese Serie beginnt bei dieser Entscheidungsebene und wandelt sie dann in praktische Tutorials um. Der erste Implementierungspfad baut ein lokales Open-Source-RAG-System auf, das jeder mit Beispieldaten, Qdrant, Ollama und Phi-4-mini ausführen kann.

## Artikel

Siehe [articles/README.md](./articles/README.md) für das Inhaltsverzeichnis der Artikel.

1. [Serie 1: RAG, Azure vs Open-Source-Alternativen und wann Fine-Tuning Sinn macht](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [Serie 2: Bau eines lokalen Open-Source-RAG-Systems von Anfang bis Ende](./articles/series-2-open-source-rag-end-to-end.md)

Als nächstes:

- Dasselbe RAG-System mit Azure AI Search und Azure OpenAI neu aufbauen.
- Evaluation und Regressionstests über eine Demo-Antwort hinaus hinzufügen.

## Notebooks

Die Implementierungsartikel verwenden Notebooks, damit die Abruf- und Evaluierungsschritte direkt inspiziert werden können. Siehe [notebooks/README.md](./notebooks/README.md) für Ordner-Level-Anleitungen.

> [!TIP]
> Beginnen Sie mit Serie 2, wenn Sie den schnellsten Weg wollen. Es läuft lokal mit Beispieldaten, CPU-freundlichen Embeddings, Qdrant im lokalen Modus und ohne Cloud-Anmeldeinformationen.

| Serie | Notebook | Anforderungen | Lokale Verifikation |
| --- | --- | --- | --- |
| Serie 2 | [Open-Source-RAG-Notebook](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Qdrant lokaler Modus, Abruf, Nachrangierung und Quellenverkettung verifiziert |

Um ein Notebook lokal auszuführen, erstellen Sie eine virtuelle Umgebung und installieren die passende Anforderungsdatei. Zum Beispiel:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## Beispieldaten

Die Notebooks verwenden einen kleinen lokalen Korpus in [sample_data](../../sample_data), sodass die Beispiele ohne private Dokumente oder Cloud-Zugangsdaten ausgeführt werden können. Siehe [sample_data/README.md](./sample_data/README.md) für Details.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## Zusammenfassung der lokalen Verifikation

Verifikationsergebnisse werden in jedem Artikel sowie in [SERIES_PLAN.md](./SERIES_PLAN.md) dokumentiert.

| Bereich | Ergebnis |
| --- | --- |
| Serie 2 Open-Source-Pfad | FastEmbed generierte lokale 384-dimensionale Embeddings, Qdrant im Arbeitsspeicher sammelte 8 Vektoren ein, leichte Nachrangierung holte den erwarteten Abschnitt ab; optionale Ollama-Generierung wurde mit `phi4-mini:3.8b` abgeschlossen |

Das lokale Notebook vermeidet absichtlich hartkodierte Geheimnisse.

## Lokale Ollama-Generierung

Das Serie 2 Notebook ist standardmäßig lokal sicher. Um lokale Ollama-Generierung zu aktivieren, kopieren Sie [.env.example](../../.env.example) nach `.env` und füllen die Werte für Serie 2 aus.

Für die Ollama-Generierung in Serie 2 heben Sie die Kommentierung von

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

auf. Das Serie 2 Notebook lädt `.env` automatisch aus dem Repository-Stamm mit `python-dotenv`.

> [!IMPORTANT]
> Committen Sie keine `.env`-Dateien, API-Schlüssel, private Endpunkte oder mandantenspezifische Werte. Das Repository hält absichtlich Geheimnisse aus Markdown-Dateien und Notebooks heraus.

Anforderungsdateien sind in [requirements/README.md](./requirements/README.md) dokumentiert.

Um Links, Notebook-Struktur, Sauberkeit der Notebook-Ausgabe und risikoreiche Geheimnismuster zu validieren:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

Verifikationsskripte sind in [scripts/README.md](./scripts/README.md) dokumentiert.

Um alle lokal-sicheren Notebooks in derselben Umgebung auszuführen:

```powershell
python scripts\verify_notebooks.py --execute
```

Der gleiche Verifikationsablauf läuft in GitHub Actions bei Pushes, Pull Requests und manuellen Workflow-Ausführungen. Entwurfsartikel und Notebooks sind absichtlich vom öffentlichen Verifikationspfad ausgenommen.

Vor dem Veröffentlichen von Updates verwenden Sie [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md).

Siehe [CHANGELOG.md](./CHANGELOG.md) für die aktuelle, unveröffentlichte Änderungsübersicht.

Für Beiträge und Richtlinien zur Pflege von Notebooks siehe [CONTRIBUTING.md](./CONTRIBUTING.md).

## Mehrsprachige Unterstützung

### Unterstützt durch Co-op Translator (Automatisiert und stets aktuell)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabisch](../ar/README.md) | [Bengalisch](../bn/README.md) | [Bulgarisch](../bg/README.md) | [Birmanisch (Myanmar)](../my/README.md) | [Chinesisch (Vereinfacht)](../zh-CN/README.md) | [Chinesisch (Traditionell, Hongkong)](../zh-HK/README.md) | [Chinesisch (Traditionell, Macau)](../zh-MO/README.md) | [Chinesisch (Traditionell, Taiwan)](../zh-TW/README.md) | [Kroatisch](../hr/README.md) | [Tschechisch](../cs/README.md) | [Dänisch](../da/README.md) | [Niederländisch](../nl/README.md) | [Estnisch](../et/README.md) | [Finnisch](../fi/README.md) | [Französisch](../fr/README.md) | [Deutsch](./README.md) | [Griechisch](../el/README.md) | [Hebräisch](../he/README.md) | [Hindi](../hi/README.md) | [Ungarisch](../hu/README.md) | [Indonesisch](../id/README.md) | [Italienisch](../it/README.md) | [Japanisch](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Koreanisch](../ko/README.md) | [Litauisch](../lt/README.md) | [Malaiisch](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepalesisch](../ne/README.md) | [Nigerianisches Pidgin](../pcm/README.md) | [Norwegisch](../no/README.md) | [Persisch (Farsi)](../fa/README.md) | [Polnisch](../pl/README.md) | [Portugiesisch (Brasilien)](../pt-BR/README.md) | [Portugiesisch (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Rumänisch](../ro/README.md) | [Russisch](../ru/README.md) | [Serbisch (Kyrillisch)](../sr/README.md) | [Slowakisch](../sk/README.md) | [Slowenisch](../sl/README.md) | [Spanisch](../es/README.md) | [Suaheli](../sw/README.md) | [Schwedisch](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thailändisch](../th/README.md) | [Türkisch](../tr/README.md) | [Ukrainisch](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamesisch](../vi/README.md)

> **Bevorzugen Sie das lokale Klonen?**
>
> Dieses Repository enthält über 50 Sprachübersetzungen, was die Downloadgröße deutlich erhöht. Um ohne Übersetzungen zu klonen, verwenden Sie Sparse Checkout:
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
> So erhalten Sie alles, was Sie brauchen, um den Kurs abzuschließen, mit einem deutlich schnelleren Download.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Haftungsausschluss**:
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, beachten Sie bitte, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner Ursprungssprache gilt als maßgebliche Quelle. Bei kritischen Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die aus der Verwendung dieser Übersetzung entstehen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->