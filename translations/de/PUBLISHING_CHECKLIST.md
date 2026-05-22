# Veröffentlichungs-Checkliste

Verwenden Sie diese Checkliste vor dem Committen oder Pushen öffentlicher Updates.

## Sicherheit

- Bestätigen Sie, dass keine API-Schlüssel, Tokens, Passwörter oder private Endpunkte in Markdown-Dateien, Notebooks, Beispieldaten oder Skripten geschrieben sind.
- Bewahren Sie Zugangsdaten in Umgebungsvariablen oder verwalteter Identität auf, nicht in festgeschriebenen Dateien.
- Committen Sie keine `.env`-Dateien oder ausgeführte Notebook-Ausgabedateien.
- Halten Sie `.env.example` nur als Platzhalter.

## Überprüfung

Führen Sie das Repository-Überprüfungsskript aus:

```powershell
python scripts\verify_notebooks.py
```

Führen Sie die vollständige lokal sichere Notebook-Ausführung vor der Veröffentlichung von Implementierungsänderungen aus:

```powershell
python scripts\verify_notebooks.py --execute
```

Erwartete Prüfungen:

- Lokale Markdown-Links funktionieren
- Notebook-JSON-Validierung besteht
- Notebooks enthalten keine gespeicherten Ausgaben oder Ausführungszählungen
- Hochrisikosekretmusterprüfung besteht
- Öffentliche Notebooks laufen lokal aus
- Entwurfsinhalte unter `drafts/` werden absichtlich übersprungen

## Überprüfung

- Bestätigen Sie, dass die README-Artikel-Links auf die vorgesehenen Dateien verweisen.
- Bestätigen Sie, dass jeder Artikel Navigations- und zugehörige Notebook-Links des Repositories enthält.
- Bestätigen Sie, dass Entwürfe nicht von öffentlichen Indexen verlinkt sind, es sei denn, sie sind veröffentlichungsbereit.
- Bestätigen Sie, dass GitHub-Issue- und Pull-Request-Vorlagen noch dem Repository-Workflow entsprechen.
- Bestätigen Sie, dass die Verifizierungsergebnisse im Artikel mit der neuesten Notebook-Ausgabe übereinstimmen.
- Bestätigen Sie, dass der GitHub Actions-Workflow nach dem Push erwartungsgemäß ausgeführt wird.
- Bestätigen Sie, dass `CHANGELOG.md` die zu veröffentlichende Änderung widerspiegelt.
- Bestätigen Sie, dass `CONTRIBUTING.md` noch dem Repository-Workflow entspricht.

## Git

- Überprüfen Sie `git status --short --branch`.
- Überprüfen Sie `git diff --stat`.
- Committen und pushen Sie nur, wenn Sie ausdrücklich bereit sind.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Haftungsausschluss**:
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, beachten Sie bitte, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner Ursprungssprache gilt als maßgebliche Quelle. Bei kritischen Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die aus der Verwendung dieser Übersetzung entstehen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->