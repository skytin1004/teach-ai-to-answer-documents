# Változásnapló

## Kiadatlan

Az **Teach AI to Answer Questions Based on Your Documents** kezdeti nyilvános kiadási körének ismertetése.

### Hozzáadva

- 1. sorozat cikk a RAG architektúra döntéseiről, Azure és nyílt forráskódú megoldások közötti kompromisszumokról, valamint a finomhangolás helyéről.
- 2. sorozat cikk és jegyzetfüzet helyi nyílt forráskódú RAG munkafolyamathoz Qdrant helyi móddal, FastEmbed helyi beágyazásokkal, könnyű újrarangsorolással, Ollamával és Phi-4-minivel.
- 2. sorozat lépésről lépésre, végponttól végpontig tartó oktatóformátum Python részletekkel és a futtatott jegyzetfüzetből származó ellenőrzési jegyzetekkel.
- Opcionális 2. sorozat válaszgenerálási út Ollamával és Phi-4-minivel, miközben a helyi CPU-barát lekérés marad az alapértelmezett.
- Helyi Ollama ellenőrzés a 2. sorozathoz `phi4-mini:3.8b` használatával RTX 3060 Laptop GPU-n.
- Mintaadatok iskolai irányelvekhez és tanfolyam AI irányításhoz.
- Követelményfájlok a nyilvános jegyzetfüzethez és a tárházi szintű ellenőrzéshez.
- Tárházi ellenőrző script helyi Markdown linkekhez és jegyzetfüzet validáláshoz/futtatáshoz.
- GitHub Actions munkafolyamat a jegyzetfüzet ellenőrzéséhez.
- `.env.example` opcionális helyi Ollama generálási beállításhoz helyi konfiguráció elkötelezése nélkül.
- Mappaszintű README fájlok cikkekhez, jegyzetfüzetekhez, követelményekhez, mintaadatokhoz és scriptekhez.
- Kiadási ellenőrzőlista a nyilvános biztonság és hitelesítés érdekében.
- Vázlat munkaterület a jövőbeli Azure és értékelési tartalomhoz.

### Ellenőrizve

- A helyi Markdown linkek érvényesítése sikeres.
- A 2. sorozat jegyzetfüzete sikeresen validált.
- A 2. sorozat jegyzetfüzete sikeresen fut a helyi ellenőrzési környezetben.
- A jegyzetfüzet fájlok mentett kimenetek vagy végrehajtási számok nélkül vannak megőrizve.
- Nincs valódi titok elkötelezve.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Jogi nyilatkozat**:
Ez a dokumentum az AI fordítási szolgáltatás, a [Co-op Translator](https://github.com/Azure/co-op-translator) segítségével készült. Bár az pontosságra törekszünk, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum az anyanyelvén tekintendő hiteles forrásnak. Fontos információk esetén professzionális emberi fordítást javasolunk. Nem vállalunk felelősséget semmilyen félreértésért vagy téves értelmezésért, amely ebből a fordításból ered.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->