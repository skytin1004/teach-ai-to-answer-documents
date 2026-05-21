# KI beibringen, Fragen basierend auf Ihren Dokumenten zu beantworten

Dieses Repository sammelt eine Blogserie aus dem Jahr 2026 über den Aufbau dokumentbasierter KI-Systeme mit RAG, Azure AI-Diensten, Open-Source-Alternativen und evaluationsorientierten Workflows.

## Hintergrund

Im Jahr 2023 habe ich an einem Paar Tutorials gearbeitet, in denen gezeigt wurde, wie man ChatGPT beibringt, Fragen aus PDF-Dokumenten mit Azure AI Search und Azure OpenAI zu beantworten. Die Idee von „ChatGPT auf Ihren Daten“ war damals noch neu, und das Ziel war es, einen praktischen Workflow zu zeigen: Dokumente speichern, indexieren, relevante Inhalte abrufen und Antworten aus dem abgerufenen Kontext generieren.

Im Jahr 2026 ist das RAG-Ökosystem viel größer. Azure AI Search unterstützt moderne Vektor- und hybride Abrufmuster, Azure OpenAI ist Teil des breiteren Microsoft Foundry Models-Ökosystems, und Open-Source-Tools wie LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama und vLLM sind zu praktischen Optionen für reale Systeme geworden.

Deshalb wollte ich dieses Thema erneut aufgreifen. Die Frage ist nicht mehr nur „Wie baue ich RAG auf?“ Es gibt jetzt viele Wege, es zu bauen, und die wichtigere Frage lautet: „Welche Architektur sollte ich für meine Situation wählen?“

Diese Serie beginnt mit dieser Entscheidungsschicht. Bevor tief in die Implementierung eingestiegen wird, wird betrachtet, warum KI-Dienste Abruf benötigen, wann Azure-basierte Managed Services sinnvoll sind, wann Open-Source-Alternativen besser passen und wo Fine-Tuning seinen Platz hat.

## Artikel

1. [Serie 1: RAG, Azure vs Open-Source-Alternativen und wann Fine-Tuning sinnvoll ist](./series-1-rag-azure-open-source-fine-tuning.md)

## Mehrsprachige Unterstützung

### Unterstützt durch Co-op Translator (Automatisiert und immer aktuell)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabisch](../ar/README.md) | [Bengalisch](../bn/README.md) | [Bulgarisch](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinesisch (vereinfacht)](../zh-CN/README.md) | [Chinesisch (traditionell, Hongkong)](../zh-HK/README.md) | [Chinesisch (traditionell, Macau)](../zh-MO/README.md) | [Chinesisch (traditionell, Taiwan)](../zh-TW/README.md) | [Kroatisch](../hr/README.md) | [Tschechisch](../cs/README.md) | [Dänisch](../da/README.md) | [Niederländisch](../nl/README.md) | [Estnisch](../et/README.md) | [Finnisch](../fi/README.md) | [Französisch](../fr/README.md) | [Deutsch](./README.md) | [Griechisch](../el/README.md) | [Hebräisch](../he/README.md) | [Hindi](../hi/README.md) | [Ungarisch](../hu/README.md) | [Indonesisch](../id/README.md) | [Italienisch](../it/README.md) | [Japanisch](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Koreanisch](../ko/README.md) | [Litauisch](../lt/README.md) | [Malaiisch](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerianisches Pidgin](../pcm/README.md) | [Norwegisch](../no/README.md) | [Persisch (Farsi)](../fa/README.md) | [Polnisch](../pl/README.md) | [Portugiesisch (Brasilien)](../pt-BR/README.md) | [Portugiesisch (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Rumänisch](../ro/README.md) | [Russisch](../ru/README.md) | [Serbisch (Kyrillisch)](../sr/README.md) | [Slowakisch](../sk/README.md) | [Slowenisch](../sl/README.md) | [Spanisch](../es/README.md) | [Suaheli](../sw/README.md) | [Schwedisch](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Türkisch](../tr/README.md) | [Ukrainisch](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamesisch](../vi/README.md)

> **Möchten Sie lieber lokal klonen?**
>
> Dieses Repository beinhaltet über 50 Sprachübersetzungen, was die Download-Größe erheblich erhöht. Um ohne Übersetzungen zu klonen, verwenden Sie Sparse Checkout:
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
> So erhalten Sie alles, was Sie brauchen, um den Kurs abzuschließen, mit einem viel schnelleren Download.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Haftungsausschluss**:
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, beachten Sie bitte, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner Ursprungssprache gilt als maßgebliche Quelle. Bei kritischen Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die aus der Verwendung dieser Übersetzung entstehen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->