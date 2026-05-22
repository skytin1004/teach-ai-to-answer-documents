# Contributing

Tämä repositorio on järjestetty blogisarjana sekä suoritettavina muistikirjaesimerkkeinä.

## Before Opening a Pull Request

Suorita paikallinen validointiskripti:

```powershell
python scripts\verify_notebooks.py
```

Implmentointi- tai muistikirjamuutosten kohdalla suorita paikallinen turvallinen muistikirjan suoritus:

```powershell
python scripts\verify_notebooks.py --execute
```

## Notebook Guidelines

- Pidä muistikirjat luettavina ja aiheeseen liittyvänä.
- Älä tallenna muistikirjan tuloksia tai suorituskertoja versionhallintaan.
- Käytä pieniä esimerkkidatoja kansiosta `sample_data/`, ellei artikkeli vaadi tiettyä ulkoista resurssia.
- Tallenna varmennustulokset asiaankuuluvaan artikkeliin, kun käyttäytyminen muuttuu.

## Secrets and Credentials

- Älä tallenna API-avaimia, tokeneita, salasanoja, yksityisiä päätepisteitä tai `.env`-tiedostoja.
- Käytä `.env.example` vain paikkamerkkien arvoihin.
- Käytä ympäristömuuttujia valinnaisiin paikallisiin Ollama-kokeiluihin.

## Documentation

- Pidä artikkelien navigointilinkit ajan tasalla.
- Päivitä `README.md` lisätessäsi uuden artikkelin, muistikirjan, vaatimustiedoston tai esimerkkidatoksen.
- Päivitä `CHANGELOG.md` ennen näkyvän repositoriopäivityksen julkaisua.

## Verification

GitHub Actions -työnkulku suorittaa:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Luonnosmateriaali kansiossa `drafts/` ohitetaan repositorion varmennuksessa, kunnes se on valmis julkiseen indeksointiin.

## Issues

Käytä artikkeleiden palautepohjaa artikkelien korjauksiin ja muistikirjan ongelmapohjaa muistikirjan suorituksen ongelmiin.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastuuvapauslauseke**:
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, otathan huomioon, että automaattiset käännökset saattavat sisältää virheitä tai epätarkkuuksia. Alkuperäinen asiakirja sen alkuperäiskielellä on virallinen lähde. Tärkeissä asioissa suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa tämän käännöksen käytöstä aiheutuvista väärinymmärryksistä tai tulkinnoista.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->