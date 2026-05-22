# Követelmények

Minden implementációs cikkhez tartozik egy fókuszált követelményfájl.

| Fájl | Használja |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | Series 2 nyílt forráskódú RAG jegyzetfüzet, beleértve az opcionális Ollama-generáló segédleteket |
| [all.txt](../../../requirements/all.txt) | Tárolószintű ellenőrzés és CI |

Egy jegyzetfüzet futtatásakor használd a fókuszált fájlt. Az egész tároló érvényesítésekor használd az `all.txt`-t.

Az `open-source-rag.txt` és az `all.txt` tartalmazza a `fastembed`-et helyi beágyazásokhoz és a `python-dotenv`-et, hogy a Series 2 opcionálisan engedélyezhesse az Ollama-generálást `.env` fájlból anélkül, hogy megváltoztatná a lekérdezési csővezetéket.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Jogi nyilatkozat**:
Ez a dokumentum az AI fordítási szolgáltatás, a [Co-op Translator](https://github.com/Azure/co-op-translator) segítségével készült. Bár az pontosságra törekszünk, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum az anyanyelvén tekintendő hiteles forrásnak. Fontos információk esetén professzionális emberi fordítást javasolunk. Nem vállalunk felelősséget semmilyen félreértésért vagy téves értelmezésért, amely ebből a fordításból ered.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->