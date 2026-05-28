# Cerințe

Fiecare articol de implementare are un fișier de cerințe focusat.

| Fișier | Folosit de |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | Caietul open-source RAG Seria 2, inclusiv ajutoare opționale de generare Ollama |
| [all.txt](../../../requirements/all.txt) | Verificare la nivel de depozit și CI |

Folosește fișierul focusat când rulezi un singur caiet. Folosește `all.txt` când validezi întregul depozit.

`open-source-rag.txt` și `all.txt` includ `fastembed` pentru embedding-uri locale și `python-dotenv` astfel încât Seria 2 să poată activa opțional generarea Ollama din `.env` fără a schimba fluxul de recuperare.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Declinare a responsabilității**:
Acest document a fost tradus folosind serviciul de traducere AI [Co-op Translator](https://github.com/Azure/co-op-translator). În timp ce ne străduim pentru acuratețe, vă rugăm să rețineți că traducerile automate pot conține erori sau inexactități. Documentul original în limba sa nativă trebuie considerat sursa autorizată. Pentru informații critice, se recomandă traducerea profesională realizată de un om. Nu ne asumăm responsabilitatea pentru eventualele neînțelegeri sau interpretări greșite care decurg din utilizarea acestei traduceri.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->