# Scripts

Tässä kansiossa on säilön tarkistusskriptejä.

## `verify_notebooks.py`

Vahvistaa paikalliset Markdown-linkit, muistikirjan JSON:n, muistikirjan tulosten puhtauden ja korkean riskin salaisuuksien mallit:

```powershell
python scripts\verify_notebooks.py
```

Suorittaa kaikki julkiset paikallisesti turvalliset muistikirjat:

```powershell
python scripts\verify_notebooks.py --execute
```

GitHub Actions -työnkulku käyttää samaa skriptiä.

Luonnosaineisto kansiossa `drafts/` ohitetaan, kunnes se on valmis julkiseen hakemistoon.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastuuvapauslauseke**:
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, otathan huomioon, että automaattiset käännökset saattavat sisältää virheitä tai epätarkkuuksia. Alkuperäinen asiakirja sen alkuperäiskielellä on virallinen lähde. Tärkeissä asioissa suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa tämän käännöksen käytöstä aiheutuvista väärinymmärryksistä tai tulkinnoista.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->