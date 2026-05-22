# Zvezki

Ti zvezki podpirajo serijo člankov z izvajanimi primeri.

| Zvezek | Članek | Namen |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Serija 2](../articles/series-2-open-source-rag-end-to-end.md) | Odprtokodni RAG z FastEmbed, Qdrant lokalni način, iskanje, ponovno razvrščanje, opcijska Ollama generacija in sklici na vire |

## Zaženi lokalno

Namestite zahteve za zvezek, ki ga želite zagnati:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Ali namestite vse odvisnosti:

```powershell
python -m pip install -r requirements\all.txt
```

## Preveri

Iz korena repozitorija:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Serija 2 lahko prebere konfiguracijo Ollama iz datoteke `.env` v korenu repozitorija. Začnite z [../.env.example](../../../.env.example), ki je razvrščena po serijah.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Omejitev odgovornosti**:
Ta dokument je bil preveden z uporabo AI prevajalske storitve [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas prosimo, da upoštevate, da avtomatizirani prevodi lahko vsebujejo napake ali netočnosti. Izvirni dokument v njegovem izvirnem jeziku je treba obravnavati kot avtoritativni vir. Za kritične informacije je priporočljiv strokovni človeški prevod. Ne odgovarjamo za morebitna nesporazume ali napačne interpretacije, ki izhajajo iz uporabe tega prevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->