# Leer AI vragen te beantwoorden op basis van uw documenten - Serienplan

Dit plan volgt de openbare uitgave van Serie 1 en Serie 2. Later worden Azure- en evaluatiewerkzaamheden als concepten bewaard totdat de voorbeelden volledig end-to-end en geverifieerd zijn.

Breng geen wijzigingen aan of push deze niet totdat dit uitdrukkelijk is toegestaan.

## Openbare reikwijdte

Huidige openbare uitgave:

- Serie 1 artikel: RAG architectuurbeslissingen, Azure versus open-source afwegingen, en waar fijninstelling past.
- Serie 2 artikel: lokale open-source RAG tutorial.
- Serie 2 notebook: uitvoerbaar lokaal RAG-lab met FastEmbed, Qdrant, Ollama, en Phi-4-mini.
- Voorbeeldgegevens: schoolbeleid en cursus AI-richtlijnen Markdown-bestanden.

Concepten maar nog niet in de openbare index:

- Azure AI Search en Azure OpenAI herbouw.
- RAG evaluatie en regressiecontroles.

## Tutorialscenario

Het gedeelde scenario is een assistent voor schoolbeleid.

De assistent beantwoordt deze vraag uit lokale documenten:

```text
Can I use generative AI for my final assignment?
```

Het verwachte gedrag is:

1. Laad lokale Markdown-documenten.
2. Parseer en deel ze op koppen.
3. Maak lokale embeddings en bewaar doorzoekbare representaties met metadata.
4. Haal de relevante beleidssectie op.
5. Herordenen indien nodig.
6. Genereer of stel een onderbouwd antwoord samen.
7. Geef citaties terug.
8. Leg verificatieresultaten vast.

## Huidige openbare structuur

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

Conceptmateriaal wordt opgeslagen onder `drafts/` en wordt overgeslagen door repository-verificatie totdat het klaar is voor publieke indexering.

## Serie 2 verificatie

Geverifieerd op Windows met Python 3.12.6.

- `requirements/open-source-rag.txt` succesvol geïnstalleerd.
- `notebooks/series-2-open-source-rag.ipynb` uitgevoerd met `nbclient`.
- Lokale verificatie geslaagd: 2 voorbeeld documenten geladen, 8 chunks aangemaakt, FastEmbed genereerde lokale embeddings van 384 dimensies, Qdrant in-memory collectie geïnitialiseerd, en 8 vectoren ingevoegd.
- Testvraag: "Kan ik generatieve AI gebruiken voor mijn eindopdracht?"
- Top opgevraagde bron na lichte herordening: `school_ai_policy.md`.
- Top opgevraagde sectie na lichte herordening: `Final Assignments`.
- Standaard antwoordroute: lokale transparante antwoordcomponist.
- Ollama geïnstalleerd via winget; `phi4-mini:3.8b` succesvol binnengehaald.
- Ollama antwoord-generatie route: voltooid met `phi4-mini:3.8b`.
- Bestandsgrootte Ollama-model: ongeveer 2,49GB op schijf.
- Gelezen modelgrootte Ollama: 3,3GB gerapporteerd door `ollama ps`.
- GPU offload: 100% GPU gerapporteerd door `ollama ps` op RTX 3060 Laptop GPU.
- GPU-geheugen na generatie geobserveerd: ongeveer 3,5GB van 6GB.
- Notebook-uitvoering met gecachte FastEmbed-model en ingeschakelde Ollama-generatie geslaagd in ongeveer 34 seconden via de verificatiescript.
- Observatie: een vroege document-laadronde nam per ongeluk `sample_data/README.md` mee; de notebook laadt nu expliciet alleen de twee bedoelde voorbeeld documenten.

## Repository verificatie

- `scripts/verify_notebooks.py` valideert lokale Markdown-links, notebook JSON, netheid van notebookoutput, en risicovolle geheime patronen.
- `scripts/verify_notebooks.py --execute` voert openbare notebooks uit vanuit de root van de repository.
- Conceptmateriaal onder `drafts/` wordt bewust overgeslagen.

## Volgend werk

- Hetzelfde scenario herbouwen met Azure AI Search en Azure OpenAI als toekomstig onderdeel van de serie.
- Ophalen en antwoordevaluatie toevoegen zodra zowel lokale als Azure-implementaties stabiel zijn.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dit document is vertaald met behulp van de AI vertaaldienst [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we streven naar nauwkeurigheid, dient u er rekening mee te houden dat geautomatiseerde vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet worden beschouwd als de gezaghebbende bron. Voor kritieke informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor eventuele misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->