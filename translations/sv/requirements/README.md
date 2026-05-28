# Krav

Varje implementeringsartikel har en fokuserad kravfil.

| Fil | Används av |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | Serie 2 open-source RAG-anteckningsbok, inklusive valfria Ollama-genereringshjälpmedel |
| [all.txt](../../../requirements/all.txt) | Verifiering på förrådsnivå och CI |

Använd den fokuserade filen när du kör en anteckningsbok. Använd `all.txt` när du validerar hela förrådet.

`open-source-rag.txt` och `all.txt` inkluderar `fastembed` för lokala inbäddningar och `python-dotenv` så Serie 2 kan valfritt aktivera Ollama-generering från `.env` utan att ändra hämtpipelinjen.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfriskrivning**:
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, var vänlig notera att automatiska översättningar kan innehålla fel eller brister. Det ursprungliga dokumentet på dess modersmål bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för några missförstånd eller feltolkningar som uppstår till följd av användningen av denna översättning.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->