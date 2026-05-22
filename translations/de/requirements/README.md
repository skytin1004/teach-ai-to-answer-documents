# Anforderungen

Jeder Implementierungsartikel hat eine fokussierte Anforderungsdatei.

| Datei | Verwendet von |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | Series 2 Open-Source-RAG-Notebook, einschließlich optionaler Ollama-Generierungshilfen |
| [all.txt](../../../requirements/all.txt) | Repository-weite Verifikation und CI |

Verwenden Sie die fokussierte Datei, wenn Sie ein Notebook ausführen. Verwenden Sie `all.txt`, wenn das gesamte Repository validiert wird.

`open-source-rag.txt` und `all.txt` enthalten `fastembed` für lokale Einbettungen und `python-dotenv`, sodass Series 2 optional die Ollama-Generierung aus `.env` aktivieren kann, ohne die Retrieval-Pipeline zu ändern.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Haftungsausschluss**:
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, beachten Sie bitte, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner Ursprungssprache gilt als maßgebliche Quelle. Bei kritischen Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die aus der Verwendung dieser Übersetzung entstehen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->