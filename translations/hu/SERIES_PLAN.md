# Tanítsd meg az AI-nak, hogy dokumentumaid alapján válaszoljon kérdésekre – Sorozatterv

Ez a terv nyomon követi az 1. és 2. sorozat nyilvános kiadását. Később az Azure és értékelési munkák tervezett állapotban maradnak, amíg a példák teljesen átfogóak és ellenőrzöttek nem lesznek.

Ne kövess el vagy tolj be változtatásokat, amíg erre kifejezetten nem utasítanak.

## Nyilvános hatókör

Jelenlegi nyilvános kiadás:

- 1. sorozat cikke: RAG architektúra döntések, Azure és nyílt forráskódú kompromisszumok, valamint a finomhangolás helye.
- 2. sorozat cikke: helyi nyílt forráskódú RAG útmutató.
- 2. sorozat jegyzetfüzete: futtatható helyi RAG labor FastEmbed-del, Qdrant-tal, Ollama-val és Phi-4-mini-vel.
- Mintaadatok: iskolai szabályzat és kurzus AI iránymutatás Markdown fájlokban.

Tervezett, de még nem szerepel a nyilvános indexben:

- Azure AI Search és Azure OpenAI újjáépítés.
- RAG értékelés és visszaesés ellenőrzések.

## Oktató forgatókönyv

A megosztott forgatókönyv egy iskolai szabályzat asszisztens.

Az asszisztens ezt a kérdést válaszolja meg helyi dokumentumok alapján:

```text
Can I use generative AI for my final assignment?
```
  
A várt működés a következő:

1. Helyi Markdown dokumentumok betöltése.  
2. Elemzés és darabolás címsorok szerint.  
3. Helyi beágyazások létrehozása, és kereshető reprezentációk tárolása metaadatokkal.  
4. A releváns szabályzati szakasz lekérése.  
5. Szükség esetén újbóli rangsorolás.  
6. Alapozott válasz generálása vagy összeállítása.  
7. Hivatkozások visszaadása.  
8. Ellenőrzési eredmények rögzítése.

## Jelenlegi nyilvános felépítés

```text
.
├── README.md
├── SERIES_PLAN.md
├── articles/
│   ├── README.md
│   ├── series-1-rag-azure-open-source-fine-tuning.md
│   └── series-2-open-source-rag-end-to-end.md
├── notebooks/
│   ├── README.md
│   └── series-2-open-source-rag.ipynb
├── sample_data/
│   ├── README.md
│   ├── course_ai_guidance.md
│   └── school_ai_policy.md
├── requirements/
│   ├── README.md
│   ├── all.txt
│   └── open-source-rag.txt
└── scripts/
    ├── README.md
    └── verify_notebooks.py
```
  
A tervezett anyag a `drafts/` mappában van tárolva, és a tároló ellenőrzés során kihagyásra kerül, amíg nyilvános indexelésre nem kész.

## 2. sorozat ellenőrzése

Windows rendszeren ellenőrizve Python 3.12.6-tal.

- A `requirements/open-source-rag.txt` sikeresen telepítve.  
- A `notebooks/series-2-open-source-rag.ipynb` futtatva `nbclient`-tel.  
- Helyi ellenőrzés sikeres: 2 minta dokumentum betöltve, 8 darab létrehozva, FastEmbed 384 dimenziós helyi beágyazásokat generált, Qdrant memóriagyűjtemény inicializálva, és 8 vektor beszúrva.  
- Teszt kérdés: „Használhatok generatív AI-t a záró dolgozatomhoz?”  
- Legjobb lekért forrás könnyű újbóli rangsorolás után: `school_ai_policy.md`.  
- Legjobb lekért szakasz könnyű újbóli rangsorolás után: `Záró dolgozatok` (Final Assignments).  
- Alapértelmezett válaszút: helyi átlátható válaszkészítő.  
- Ollama winget-en keresztül telepítve; a `phi4-mini:3.8b` sikeresen letöltve.  
- Ollama válaszgenerálási folyamat: befejezve a `phi4-mini:3.8b`-vel.  
- Ollama modell fájlmérete: körülbelül 2,49 GB lemezen.  
- Ollama betöltött modellméret: 3,3 GB a `ollama ps` szerint.  
- GPU terhelés: 100% GPU-t jelent a `ollama ps` az RTX 3060 Laptop GPU-n.  
- GPU memória a generálás után: körülbelül 3,5 GB a 6 GB-ból.  
- A jegyzetfüzet végrehajtása a gyorsított FastEmbed modellel és engedélyezett Ollama generálással körülbelül 34 másodperc alatt sikeresen ment át a validációs szkripten.  
- Megfigyelés: egy korai dokumentumbetöltési kör véletlenül tartalmazta a `sample_data/README.md` fájlt; a jegyzetfüzet most már csak a két szándékosan megadott minta dokumentumot tölti be kifejezetten.

## Tároló ellenőrzése

- A `scripts/verify_notebooks.py` ellenőrzi a helyi Markdown hivatkozásokat, a jegyzetfüzet JSON-t, a jegyzetfüzet kimeneti tisztaságát és magas kockázatú titkos mintákat.  
- A `scripts/verify_notebooks.py --execute` lefuttatja a nyilvános jegyzetfüzeteket a tároló gyökérből.  
- A `drafts/` alatti tervezett anyagot szándékosan kihagyják.

## Következő munkák

- Ugyanennek a forgatókönyvnek az újjáépítése Azure AI Search és Azure OpenAI használatával a jövőbeni sorozatrész részeként.  
- Lekérdezés és válaszértékelés hozzáadása, ha a helyi és Azure megvalósítások egyaránt stabilak.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Jogi nyilatkozat**:
Ez a dokumentum az AI fordítási szolgáltatás, a [Co-op Translator](https://github.com/Azure/co-op-translator) segítségével készült. Bár az pontosságra törekszünk, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum az anyanyelvén tekintendő hiteles forrásnak. Fontos információk esetén professzionális emberi fordítást javasolunk. Nem vállalunk felelősséget semmilyen félreértésért vagy téves értelmezésért, amely ebből a fordításból ered.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->