# KI beibringen, Fragen basierend auf Ihren Dokumenten zu beantworten – Serienplan

Dieser Plan verfolgt die öffentliche Veröffentlichung von Serie 1 und Serie 2. Spätere Azure- und Evaluierungsarbeiten werden als Entwürfe geführt, bis die Beispiele vollständig durchgängig und verifiziert sind.

Änderungen dürfen erst nach ausdrücklicher Anweisung committet oder gepusht werden.

## Öffentlicher Umfang

Aktuelle öffentliche Veröffentlichung:

- Serie 1 Artikel: RAG-Architekturentscheidungen, Azure- vs. Open-Source-Abwägungen und wo Feinabstimmung passt.
- Serie 2 Artikel: Lokales Open-Source-RAG-Tutorial.
- Serie 2 Notebook: ausführbares lokales RAG-Labor mit FastEmbed, Qdrant, Ollama und Phi-4-mini.
- Beispieldaten: Schulrichtlinien- und Kurs-KI-Anleitungs-Markdown-Dateien.

Als Entwurf erfasst, aber noch nicht im öffentlichen Index:

- Azure AI Search und Azure OpenAI Wiederaufbau.
- RAG-Evaluierung und Regressionsprüfungen.

## Tutorial-Szenario

Das gemeinsame Szenario ist ein Schulrichtlinienassistent.

Der Assistent beantwortet diese Frage aus lokalen Dokumenten:

```text
Can I use generative AI for my final assignment?
```

Das erwartete Verhalten ist:

1. Lokale Markdown-Dokumente laden.
2. Diese nach Überschriften parsen und in Abschnitte unterteilen.
3. Lokale Einbettungen erstellen und durchsuchbare Repräsentationen mit Metadaten speichern.
4. Den relevanten Richtlinienabschnitt abrufen.
5. Bei Bedarf neu bewerten (Re-Ranking).
6. Eine fundierte Antwort generieren oder komponieren.
7. Quellenangaben zurückgeben.
8. Verifikationsergebnisse protokollieren.

## Aktuelle öffentliche Struktur

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

Entwurfsmaterial wird unter `drafts/` gespeichert und wird von der Repository-Verifikation übersprungen, bis es bereit zur öffentlichen Indizierung ist.

## Verifikation Serie 2

Verifiziert unter Windows mit Python 3.12.6.

- `requirements/open-source-rag.txt` erfolgreich installiert.
- `notebooks/series-2-open-source-rag.ipynb` mit `nbclient` ausgeführt.
- Lokale Verifikation bestanden: 2 Beispieldokumente geladen, 8 Abschnitte erstellt, FastEmbed erzeugte 384-dimensionale lokale Einbettungen, Qdrant In-Memory-Sammlung initialisiert und 8 Vektoren eingefügt.
- Testfrage: „Kann ich generative KI für meine Abschlussarbeit verwenden?“
- Nach leichtem Re-Ranking oberste gefundene Quelle: `school_ai_policy.md`.
- Nach leichtem Re-Ranking oberster Abschnitt: `Abschlussarbeiten`.
- Standard-Antwortpfad: lokaler transparenter Antwortkomponist.
- Ollama via winget installiert; `phi4-mini:3.8b` erfolgreich heruntergeladen.
- Ollama Antwortgenerierungspfad: mit `phi4-mini:3.8b` abgeschlossen.
- Ollama Modell-Dateigröße: ca. 2,49 GB auf der Festplatte.
- Ollama geladene Modellgröße: 3,3 GB laut `ollama ps`.
- GPU-Last: 100 % GPU, gemeldet von `ollama ps` auf RTX 3060 Laptop-GPU.
- GPU-Speichernutzung nach Generierung: ca. 3,5 GB von 6 GB.
- Notebook-Ausführung mit zwischengespeichertem FastEmbed-Modell und aktivierter Ollama-Generation bestand mit ca. 34 Sekunden Laufzeit im Verifikationsskript.
- Beobachtung: Ein früher Dokumentlade-Durchgang enthielt versehentlich `sample_data/README.md`; das Notebook lädt nun explizit nur die zwei vorgesehenen Beispieldokumente.

## Repository-Verifikation

- `scripts/verify_notebooks.py` prüft lokale Markdown-Links, Notebook-JSON, Sauberkeit der Notebook-Ausgaben und Hochrisiko-Geheimnismuster.
- `scripts/verify_notebooks.py --execute` führt öffentliche Notebooks vom Repository-Stammverzeichnis aus.
- Entwurfsmaterial unter `drafts/` wird absichtlich übersprungen.

## Nächste Arbeiten

- Dasselbe Szenario mit Azure AI Search und Azure OpenAI als Teil einer zukünftigen Serie neu aufbauen.
- Retrieval- und Antwort-Evaluierung hinzufügen, sobald die lokalen und Azure-Implementierungen stabil sind.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Haftungsausschluss**:
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, beachten Sie bitte, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner Ursprungssprache gilt als maßgebliche Quelle. Bei kritischen Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die aus der Verwendung dieser Übersetzung entstehen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->