# Julkaisun tarkistuslista

Käytä tätä tarkistuslista ennen julkisten päivitysten sitomista tai työntämistä.

## Turvallisuus

- Varmista, ettei API-avaimia, tunnuksia, salasanoja tai yksityisiä päätepisteitä ole kirjoitettu Markdown-tiedostoihin, muistikirjoihin, esimerkkidataan tai skripteihin.
- Säilytä tunnistetiedot ympäristömuuttujissa tai hallitussa identiteetissä, ei sitotuissa tiedostoissa.
- Älä sitoudu `.env`-tiedostoja tai ajettujen muistikirjojen tulostustiedostoja.
- Pidä `.env.example` pelkkänä paikkamerkkinä.

## Varmistus

Suorita arkiston varmistuskomentosarja:

```powershell
python scripts\verify_notebooks.py
```

Suorita täysi paikallinen turvallinen muistikirjan ajo ennen toteutuksen muutosten julkaisua:

```powershell
python scripts\verify_notebooks.py --execute
```

Odotetut tarkastukset:

- paikalliset Markdown-linkit läpäisevät
- muistikirjan JSON-validointi hyväksytään
- muistikirjat eivät sisällä tallennettuja tuloksia tai ajojen määriä
- korkean riskin salaisuuksien kuvioiden tarkistus hyväksytään
- julkiset muistikirjat suorittavat paikallisesti
- luonnosmateriaalit kansiossa `drafts/` jätetään tahallisesti huomioimatta

## Tarkistus

- Varmista, että README-artikkelin linkit osoittavat tarkoitettuihin tiedostoihin.
- Varmista, että jokaisessa artikkelissa on arkiston navigointi- ja siihen liittyvät muistikirjalinkit.
- Varmista, ettei luonnoksia ole linkitetty julkisista hakemistoista ellei ne ole valmiita julkaistavaksi.
- Varmista, että GitHub-ongelma- ja vetopyyntöpohjat vastaavat edelleen arkiston työnkulkua.
- Varmista, että varmistus tulokset artikkelissa vastaavat uusinta muistikirjan tulostetta.
- Varmista, että GitHub Actions -työnkulun odotetaan suorittuvan pushin jälkeen.
- Varmista, että `CHANGELOG.md` heijastaa julkaistavaa päivitystä.
- Varmista, että `CONTRIBUTING.md` vastaa edelleen arkiston työnkulkua.

## Git

- Tarkista `git status --short --branch`.
- Tarkista `git diff --stat`.
- Sitoudu ja työnnä vain, kun olet nimenomaisesti valmis.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastuuvapauslauseke**:
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, otathan huomioon, että automaattiset käännökset saattavat sisältää virheitä tai epätarkkuuksia. Alkuperäinen asiakirja sen alkuperäiskielellä on virallinen lähde. Tärkeissä asioissa suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa tämän käännöksen käytöstä aiheutuvista väärinymmärryksistä tai tulkinnoista.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->