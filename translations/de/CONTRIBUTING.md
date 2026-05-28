# Beitrag

Dieses Repository ist als Blogserie plus ausführbare Notebook-Beispiele organisiert.

## Vor dem Öffnen eines Pull Requests

Führen Sie das lokale Validierungsskript aus:

```powershell
python scripts\verify_notebooks.py
```

Für Implementierungs- oder Notebook-Änderungen führen Sie die lokal-sichere Notebook-Ausführung aus:

```powershell
python scripts\verify_notebooks.py --execute
```

## Notebook-Richtlinien

- Halten Sie Notebooks lesbar und auf den zugehörigen Artikel fokussiert.
- Committen Sie keine gespeicherten Notebook-Ausgaben oder Ausführungszähler.
- Verwenden Sie kleine Beispieldaten aus `sample_data/`, es sei denn, der Artikel erfordert eine spezifische externe Ressource.
- Dokumentieren Sie Verifikationsergebnisse im zugehörigen Artikel, wenn sich das Verhalten ändert.

## Geheimnisse und Zugangsdaten

- Committen Sie keine API-Schlüssel, Tokens, Passwörter, private Endpunkte oder `.env`-Dateien.
- Verwenden Sie `.env.example` nur für Platzhalterwerte.
- Verwenden Sie Umgebungsvariablen für optionale lokale Ollama-Experimente.

## Dokumentation

- Halten Sie die Navigationslinks der Artikel aktuell.
- Aktualisieren Sie `README.md`, wenn Sie einen neuen Artikel, ein Notebook, eine Requirements-Datei oder eine Beispieldatendatei hinzufügen.
- Aktualisieren Sie `CHANGELOG.md` vor der Veröffentlichung eines sichtbaren Repository-Updates.

## Verifikation

Der GitHub Actions Workflow läuft:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Entwurfsmaterial unter `drafts/` wird von der Repository-Verifikation übersprungen, bis es bereit für die öffentliche Indexierung ist.

## Probleme

Verwenden Sie die Feedback-Vorlage für Artikelkorrekturen und die Notebook-Issue-Vorlage für Probleme bei der Notebook-Ausführung.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Haftungsausschluss**:
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, beachten Sie bitte, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner Ursprungssprache gilt als maßgebliche Quelle. Bei kritischen Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die aus der Verwendung dieser Übersetzung entstehen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->