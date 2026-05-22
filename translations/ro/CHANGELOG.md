# Changelog

## Unreleased

Scopul lansării publice inițiale pentru **Teach AI to Answer Questions Based on Your Documents**.

### Added

- Articolul din Seria 1 despre deciziile arhitecturii RAG, compromisurile Azure vs open-source și locul unde se potrivește fine-tuning-ul.
- Articolul și caietul de lucru din Seria 2 pentru un flux de lucru RAG open-source local folosind modul local Qdrant, embeddings FastEmbed locale, reranking ușor, Ollama și Phi-4-mini.
- Format tutorial pas cu pas de la Seria 2 cu fragmente Python și note de verificare din caietul de lucru executat.
- Cale opțională de generare a răspunsurilor din Seria 2 cu Ollama și Phi-4-mini, păstrând recuperarea locală prietenoasă cu CPU ca cale implicită.
- Verificare locală Ollama pentru Seria 2 folosind `phi4-mini:3.8b` pe GPU Laptop RTX 3060.
- Date de exemplu pentru politica școlii și ghidarea AI a cursului.
- Fișiere de cerințe pentru caietul public și verificarea la nivel de depozit.
- Script de verificare a depozitului pentru linkuri Markdown locale și validarea/executarea caietului.
- Workflow GitHub Actions pentru verificarea caietului.
- `.env.example` pentru configurarea opțională locală a generării Ollama fără a comite configurația locală.
- Fișiere README la nivel de folder pentru articole, caiete, cerințe, date de exemplu și scripturi.
- Listă de verificare pentru publicare pentru siguranță și verificare publică.
- Workspace în schiță pentru viitoare conținuturi Azure și evaluare.

### Verified

- Validarea linkurilor Markdown locale trece cu succes.
- Caietul Seriei 2 validează cu succes.
- Caietul Seriei 2 se execută cu succes în mediul local de verificare.
- Fișierele caietelor sunt păstrate fără ieșiri salvate sau numere de execuție.
- Nu sunt comise secreți reale.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Declinare a responsabilității**:
Acest document a fost tradus folosind serviciul de traducere AI [Co-op Translator](https://github.com/Azure/co-op-translator). În timp ce ne străduim pentru acuratețe, vă rugăm să rețineți că traducerile automate pot conține erori sau inexactități. Documentul original în limba sa nativă trebuie considerat sursa autorizată. Pentru informații critice, se recomandă traducerea profesională realizată de un om. Nu ne asumăm responsabilitatea pentru eventualele neînțelegeri sau interpretări greșite care decurg din utilizarea acestei traduceri.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->