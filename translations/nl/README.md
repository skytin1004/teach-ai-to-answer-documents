# Leer AI om Vragen te Beantwoorden op Basis van Uw Documenten

Deze repository verzamelt een blogserie uit 2026 over het bouwen van document-ondersteunde AI-systemen met RAG, Azure AI-diensten, open-source alternatieven en evaluatiegerichte workflows.

## Achtergrond

In 2023 werkte ik aan een paar tutorials over het aanleren van ChatGPT om vragen te beantwoorden uit PDF-documenten met behulp van Azure AI Search en Azure OpenAI. Het idee van "ChatGPT op je eigen data" voelde toen nog nieuw aan, en het doel was om een praktische workflow te laten zien: documenten opslaan, indexeren, relevante inhoud ophalen en antwoorden genereren uit die opgehaalde context.

In 2026 is het RAG-ecosysteem veel groter. Azure AI Search ondersteunt moderne vector- en hybride retrievelpatronen, Azure OpenAI maakt deel uit van het bredere Microsoft Foundry Models-ecosysteem, en open-source tools zoals LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama en vLLM zijn praktische keuzes geworden voor echte systemen.

Daarom wilde ik dit onderwerp opnieuw behandelen. De vraag is niet langer alleen "Hoe bouw ik RAG?" Er zijn nu vele manieren om het te bouwen, en de belangrijkere vraag is "Welke architectuur moet ik kiezen voor mijn situatie?"

Deze serie begint bij die beslissingslaag. Voordat er diepgaand op de implementatie wordt ingegaan, kijkt het naar waarom AI-diensten retrieval nodig hebben, wanneer Azure-gebaseerde beheerde diensten zinvol zijn, wanneer open-source alternatieven beter passen, en waar fine-tuning staat.

## Artikelen

1. [Serie 1: RAG, Azure vs Open-Source Alternatieven, en Wanneer Fine-Tuning Zinvol Is](./series-1-rag-azure-open-source-fine-tuning.md)

## Meertalige Ondersteuning

### Ondersteund via Co-op Translator (Geautomatiseerd en Altijd Up-to-Date)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabisch](../ar/README.md) | [Bengaals](../bn/README.md) | [Bulgaars](../bg/README.md) | [Birmaans (Myanmar)](../my/README.md) | [Chinees (Vereenvoudigd)](../zh-CN/README.md) | [Chinees (Traditioneel, Hong Kong)](../zh-HK/README.md) | [Chinees (Traditioneel, Macau)](../zh-MO/README.md) | [Chinees (Traditioneel, Taiwan)](../zh-TW/README.md) | [Kroatisch](../hr/README.md) | [Tsjechisch](../cs/README.md) | [Deens](../da/README.md) | [Nederlands](./README.md) | [Ests](../et/README.md) | [Fins](../fi/README.md) | [Frans](../fr/README.md) | [Duits](../de/README.md) | [Grieks](../el/README.md) | [Hebreeuws](../he/README.md) | [Hindi](../hi/README.md) | [Hongaars](../hu/README.md) | [Indonesisch](../id/README.md) | [Italiaans](../it/README.md) | [Japans](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Koreaans](../ko/README.md) | [Litouws](../lt/README.md) | [Maleis](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepalees](../ne/README.md) | [Nigeriaans Pidgin](../pcm/README.md) | [Noors](../no/README.md) | [Perzisch (Farsi)](../fa/README.md) | [Pools](../pl/README.md) | [Portugees (Brazilië)](../pt-BR/README.md) | [Portugees (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Roemeens](../ro/README.md) | [Russisch](../ru/README.md) | [Servisch (Cyrillisch)](../sr/README.md) | [Slowaaks](../sk/README.md) | [Sloveens](../sl/README.md) | [Spaans](../es/README.md) | [Swahili](../sw/README.md) | [Zweeds](../sv/README.md) | [Tagalog (Filipijns)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turks](../tr/README.md) | [Oekraïens](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamees](../vi/README.md)

> **Wilt u liever lokaal klonen?**
>
> Deze repository bevat 50+ taalvertalingen wat de downloadgrootte aanzienlijk vergroot. Om zonder vertalingen te klonen, gebruik sparse checkout:
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
> Dit geeft u alles wat u nodig heeft om de cursus te voltooien met een veel snellere download.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dit document is vertaald met behulp van de AI vertaaldienst [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we streven naar nauwkeurigheid, dient u er rekening mee te houden dat geautomatiseerde vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet worden beschouwd als de gezaghebbende bron. Voor kritieke informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor eventuele misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->