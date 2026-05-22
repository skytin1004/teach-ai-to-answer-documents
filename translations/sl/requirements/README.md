# Zahteve

Vsak članek o implementaciji ima osredotočeno datoteko z zahtevami.

| Datoteka | Uporablja |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | Zvezek odprtokodnega RAG serije 2, vključno z izbirnimi pomočniki za generiranje Ollama |
| [all.txt](../../../requirements/all.txt) | Preverjanje na ravni repozitorija in CI |

Osredotočenno datoteko uporabite pri zaganjanju enega zvezka. `all.txt` uporabite pri preverjanju celotnega repozitorija.

`open-source-rag.txt` in `all.txt` vključujeta `fastembed` za lokalne vdelave in `python-dotenv`, da lahko Serija 2 opcijsko omogoči generiranje Ollama iz `.env` brez spremembe pridobitvenega postopka.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Omejitev odgovornosti**:
Ta dokument je bil preveden z uporabo AI prevajalske storitve [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas prosimo, da upoštevate, da avtomatizirani prevodi lahko vsebujejo napake ali netočnosti. Izvirni dokument v njegovem izvirnem jeziku je treba obravnavati kot avtoritativni vir. Za kritične informacije je priporočljiv strokovni človeški prevod. Ne odgovarjamo za morebitna nesporazume ali napačne interpretacije, ki izhajajo iz uporabe tega prevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->