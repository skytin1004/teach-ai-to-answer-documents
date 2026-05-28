# Changelog

## Ikke udgivet

Første offentlige udgivelsesomfang for **Teach AI to Answer Questions Based on Your Documents**.

### Tilføjet

- Serie 1 artikel om RAG-arkitekturvalg, Azure vs open source afvejninger, og hvor finjustering passer ind.
- Serie 2 artikel og notesbog til en lokal open-source RAG arbejdsgang med Qdrant lokal tilstand, FastEmbed lokale embeddings, letvægts genrangering, Ollama og Phi-4-mini.
- Serie 2 trin-for-trin end-to-end tutorial format med Python snippets og verifikationsnoter fra den udførte notesbog.
- Valgfri Serie 2 svar-genereringssti med Ollama og Phi-4-mini mens lokal CPU-venlig opslag forbliver standardstien.
- Lokal Ollama verifikation for Serie 2 med `phi4-mini:3.8b` på RTX 3060 Laptop GPU.
- Eksempeldatasæt for skolepolitik og kursus AI-vejledning.
- Requirements-filer til den offentlige notesbog og repository-niveau verifikation.
- Repository verifikationsscript til lokale Markdown-links og notesbogsvalidering/eksekvering.
- GitHub Actions arbejdsgang til notesbogsverifikation.
- `.env.example` til valgfri lokal Ollama genereringsopsætning uden at committed lokal konfiguration.
- Mappeniveau README-filer til artikler, notesbøger, requirements, eksempeldatasæt og scripts.
- Udgivelsestjekliste for offentlig sikkerhed og verifikation.
- Udkast til arbejdsområde til fremtidigt Azure og evalueringsindhold.

### Verificeret

- Lokal Markdown link validering bestået.
- Serie 2 notesbog valideres succesfuldt.
- Serie 2 notesbog eksekveres succesfuldt i det lokale verifikationsmiljø.
- Notesbogsfiler opbevares uden gemte output eller eksekveringstællere.
- Ingen rigtige hemmeligheder er committet.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os intet ansvar for misforståelser eller fejltolkninger, der opstår som følge af brugen af denne oversættelse.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->