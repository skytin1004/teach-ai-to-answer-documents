# Muistikirjat

Nämä muistikirjat tukevat artikkelisarjaa suoritettavilla esimerkeillä.

| Muistikirja | Artikkeli | Tarkoitus |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Sarja 2](../articles/series-2-open-source-rag-end-to-end.md) | Avoimen lähdekoodin RAG FastEmbedin, Qdrantin paikallisen tilan, haun, uudelleenjärjestelyn, valinnaisen Ollama-luonnin ja lähdeviitteiden kanssa |

## Suorita paikallisesti

Asenna muistikirjan suorittamiseen tarvittavat vaatimukset:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Tai asenna kaikki riippuvuudet:

```powershell
python -m pip install -r requirements\all.txt
```

## Vahvista

Rekisteröitymän juuressa:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Sarja 2 voi lukea Ollama-konfiguraation rekisteröitymän juuren `.env`-tiedostosta. Aloita tiedostosta [../.env.example](../../../.env.example), joka on ryhmitelty sarjoittain.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastuuvapauslauseke**:
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, otathan huomioon, että automaattiset käännökset saattavat sisältää virheitä tai epätarkkuuksia. Alkuperäinen asiakirja sen alkuperäiskielellä on virallinen lähde. Tärkeissä asioissa suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa tämän käännöksen käytöstä aiheutuvista väärinymmärryksistä tai tulkinnoista.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->