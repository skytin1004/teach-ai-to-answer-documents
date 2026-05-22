# Notebooks

Diese Notebooks unterstützen die Artikelserie mit ausführbaren Beispielen.

| Notebook | Artikel | Zweck |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Serie 2](../articles/series-2-open-source-rag-end-to-end.md) | Open-Source RAG mit FastEmbed, Qdrant Lokalmodus, Retrieval, Reranking, optionaler Ollama-Generierung und Quellverweisen |

## Lokal ausführen

Installieren Sie die Anforderungen für das Notebook, das Sie ausführen möchten:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Oder installieren Sie alle Abhängigkeiten:

```powershell
python -m pip install -r requirements\all.txt
```

## Überprüfen

Vom Repository-Stammverzeichnis aus:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Serie 2 kann die Ollama-Konfiguration aus einer `.env`-Datei im Repository-Stamm lesen. Starten Sie von [../.env.example](../../../.env.example), welche nach Serien gruppiert ist.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Haftungsausschluss**:
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, beachten Sie bitte, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner Ursprungssprache gilt als maßgebliche Quelle. Bei kritischen Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die aus der Verwendung dieser Übersetzung entstehen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->