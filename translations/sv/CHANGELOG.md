# Ändringslogg

## Ej utgiven

Initial offentlig releaseomfattning för **Lär AI att svara på frågor baserat på dina dokument**.

### Tillagt

- Serie 1-artikel om RAG-arkitekturval, Azure vs open source-avvägningar och var finjustering passar in.
- Serie 2-artikel och anteckningsbok för ett lokalt open source RAG-arbetsflöde med Qdrant lokalt läge, FastEmbed lokala embeddingar, lättviktig omrankning, Ollama och Phi-4-mini.
- Serie 2 steg-för-steg slut-till-slut handledningsformat med Python-snippets och verifieringsnoteringar från den körda anteckningsboken.
- Valbar Serie 2 svarsgenereringsväg med Ollama och Phi-4-mini samtidigt som lokal CPU-vänlig hämtning behålls som standardväg.
- Lokal Ollama-verifiering för Serie 2 med `phi4-mini:3.8b` på RTX 3060 Laptop GPU.
- Exempeldata för skolpolicy och AI-vägledning för kurser.
- Kravfiler för den offentliga anteckningsboken och verifiering på biblioteknivå.
- Repository-verifieringsskript för lokala Markdown-länkar och anteckningsboksvalidering/utförande.
- GitHub Actions-arbetsflöde för anteckningsboksverifiering.
- `.env.example` för valfri lokal Ollama-genereringssättning utan att begå lokal konfiguration.
- Mappnivå README-filer för artiklar, anteckningsböcker, krav, exempeldata och skript.
- Publiceringschecklista för offentlig säkerhet och verifiering.
- Utkast arbetsyta för framtida Azure- och utvärderingsinnehåll.

### Verifierat

- Lokal Markdown-länkvalidering passerar.
- Serie 2 anteckningsbok valideras framgångsrikt.
- Serie 2 anteckningsbok körs framgångsrikt i den lokala verifieringsmiljön.
- Anteckningsboksfiler hålls utan sparade utdata eller körningsräkningar.
- Inga verkliga hemligheter är incheckade.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfriskrivning**:
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, var vänlig notera att automatiska översättningar kan innehålla fel eller brister. Det ursprungliga dokumentet på dess modersmål bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för några missförstånd eller feltolkningar som uppstår till följd av användningen av denna översättning.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->