# Opeta tekoäly vastaamaan kysymyksiin asiakirjojesi perusteella - Sarjasuunnitelma

Tämä suunnitelma seuraa julkisia Sarja 1- ja Sarja 2 -julkaisuja. Myöhemmät Azure- ja arviointityöt pidetään luonnoksina, kunnes esimerkit ovat täysin loppuun asti testattuja ja varmennettuja.

Älä tee commit- tai push-muutoksia ennen kuin saat siihen selkeän ohjeen.

## Julkinen laajuus

Nykyinen julkinen julkaisu:

- Sarja 1 artikkeli: RAG-arkkitehtuuripäätökset, Azure vs avoimen lähdekoodin kompromissit ja missä hienosäätö sopii.
- Sarja 2 artikkeli: paikallinen avoimen lähdekoodin RAG-opas.
- Sarja 2 notebook: suoritettava paikallinen RAG-laboratorio FastEmbed-, Qdrant-, Ollama- ja Phi-4-mini -työkaluilla.
- Esimerkkidata: koulun politiikka- ja kurssin tekoälyohjeistuksen Markdown-tiedostot.

Luonnosteltu mutta ei vielä julkisessa hakemistossa:

- Azure AI Search ja Azure OpenAI uudelleenrakennus.
- RAG-arviointi ja regressiotarkastukset.

## Opastus-tilanne

Jaettu tilanne on koulun politiikka-avustaja.

Avustaja vastaa tähän kysymykseen paikallisista asiakirjoista:

```text
Can I use generative AI for my final assignment?
```

Odotettu toiminta on:

1. Ladata paikalliset Markdown-asiakirjat.
2. Jäsentää ja pilkkoa ne otsikoittain.
3. Luoda paikalliset upotukset ja tallentaa haettavat esitykset metatietoineen.
4. Hakea asiaankuuluva politiikkaosio.
5. Järjestää uudelleen tarvittaessa.
6. Luoda tai koostaa perusteltu vastaus.
7. Palauttaa lähdeviitteet.
8. Tallentaa varmennustulokset.

## Nykyinen julkinen rakenne

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

Luonnosmateriaali tallennetaan hakemistoon `drafts/` ja sitä ohitetaan varmentamisessa, kunnes se on valmis julkiseen indeksointiin.

## Sarja 2 varmennus

Varmennettu Windowsilla Python 3.12.6 -ympäristössä.

- Asennettiin onnistuneesti `requirements/open-source-rag.txt`.
- Suoritettiin `notebooks/series-2-open-source-rag.ipynb` `nbclient`-työkalulla.
- Paikallinen varmennus hyväksyttiin: 2 esimerkkiasiakirjaa ladattu, 8 pätkää luotu, FastEmbed loi 384-ulotteiset paikalliset upotukset, Qdrantin muistissa oleva kokoelma alustettu, ja 8 vektoria lisätty.
- Testikysymys: "Voinko käyttää generatiivista tekoälyä lopputyössäni?"
- Kevyen uudelleenjärjestämisen jälkeen korkeimmalle noussut lähde: `school_ai_policy.md`.
- Kevyen uudelleenjärjestämisen jälkeen korkeimmalle noussut osio: `Final Assignments`.
- Oletusvastauksiin käytetty reitti: paikallinen läpinäkyvä vastaajan koostaja.
- Ollama asennettu wingetillä; `phi4-mini:3.8b` vedettiin onnistuneesti.
- Ollaman vastausten tuottoreitti: suoritettu `phi4-mini:3.8b`-mallilla.
- Ollama-mallin tiedostokoko: noin 2,49 Gt levyllä.
- Ollaman ladatun mallin koko: 3,3 Gt, `ollama ps` raportoi.
- GPU-kuormitus: 100 % GPU käyttöönottolaitteella RTX 3060 Laptop GPU, raportoi `ollama ps`.
- GPU-muistin käyttö generoinnin jälkeen: noin 3,5 Gt 6 Gt:sta.
- Notebookin suoritus välimuistitetun FastEmbed-mallin ja Ollama-tuotannon kanssa hyväksyttiin noin 34 sekunnissa varmennusskriptillä.
- Huomio: alkuperäisessä asiakirjan latauskierroksessa vahingossa ladattiin `sample_data/README.md`; nyt notebook lataa eksplisiittisesti vain kaksi tarkoitettua esimerkkiasiakirjaa.

## Repositorion varmennus

- `scripts/verify_notebooks.py` validoi paikalliset Markdown-linkit, notebookin JSON-rakenteen, notebookin tulosten puhtauden ja korkean riskin salaisuuskäyttäytymismallit.
- `scripts/verify_notebooks.py --execute` suorittaa julkiset notebookit repositorion juuressa.
- Luonnosmateriaali hakemistossa `drafts/` ohitetaan tahallisesti.

## Seuraava työ

- Rakentaa sama tilanne uudelleen Azure AI Searchilla ja Azure OpenAI:lla tulevana sarjan osana.
- Lisätä haun ja vastausten arvioinnin, kun sekä paikalliset että Azure-toteutukset ovat vakaita.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastuuvapauslauseke**:
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, otathan huomioon, että automaattiset käännökset saattavat sisältää virheitä tai epätarkkuuksia. Alkuperäinen asiakirja sen alkuperäiskielellä on virallinen lähde. Tärkeissä asioissa suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa tämän käännöksen käytöstä aiheutuvista väärinymmärryksistä tai tulkinnoista.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->