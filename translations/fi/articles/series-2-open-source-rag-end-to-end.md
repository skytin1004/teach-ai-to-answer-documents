# Opeta tekoäly vastaamaan kysymyksiin dokumenttiesi perusteella
## Sarja 2: Paikallisen avoimen lähdekoodin RAG-järjestelmän rakentaminen alusta loppuun

![Paikallinen avoimen lähdekoodin RAG-opastusputki](../../../assets/images/series-2-local-rag.svg)

> Tämä artikkeli muuttaa Sarja 1:n arkkitehtuurikeskustelun ajettavaksi paikalliseksi RAG-opastukseksi. Tavoitteena on rakentaa ensin koko työnkulku esimerkkidatalla, ilman pilvitiliä ja salaisuuksia, ja käyttää tätä toimivaa pohjaa myöhemmin parempiin arkkitehtuuriratkaisuihin.

Rakennettava järjestelmä on pieni koulun politiikka-avustaja. Käytän kahta paikallista Markdown-dokumenttia tietokantana, ja käyn läpi koko RAG-putken: tekstin pilkkominen osiin, paikalliset upotukset, Qdrantin vektorivarastoinnin, hakemisen, uudelleenjärjestämisen, lähdetietoisen vastausten koostamisen ja valinnaisen paikallisen generoinnin Ollamalla ja Phi-4-mini:llä.

Sarjan navigointi: [Repositorion etusivu](../README.md) | Edellinen: [Sarja 1 - RAG, Azure vs avoimen lähdekoodin vaihtoehdot ja milloin hienosäätö on järkevää](./series-1-rag-azure-open-source-fine-tuning.md)

Muistikirja: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Vaadittavat riippuvuudet: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> Tämä on paras aloituspiste, jos haluat ymmärtää RAG-putken ennen pilvipalveluiden resurssien luontia. Oletuspolku toimii paikallisesti CPU-ystävällisillä upotuksilla eikä vaadi salaisuuksia.

## 1. Mitä Rakennamme

Vuoden 2023 opastuksessa aloitin Azuresta, koska tavoitteena oli näyttää miten Azure AI Search ja Azure OpenAI pystyvät vastaamaan PDF-dokumenteista.

Tälle vuoden 2026 sarjalle haluan aloittaa yhden kerroksen alemmalta tasolta.

Ennen hallinnoitujen palveluiden käyttämistä haluan rakentaa pienen paikallisen RAG-järjestelmän ja tehdä jokaisesta vaiheesta näkyvän: dokumenttien latauksesta, tekstin pilkkomisesta, vektorien tallennuksesta, todistusaineiston hakemisesta, uudelleenjärjestämisestä ja lähdetietoisesta vastauksen palauttamisesta.

Esimerkkitilanne on koulun politiikka-avustaja. Käyttäjä kysyy:

```text
Can I use generative AI for my final assignment?
```

Järjestelmän ei tulisi vastata yleisen mallimuistin perusteella. Sen tulisi hakea asiaankuuluva politiikkaosio ja vastata siitä todistusaineistosta.

Täysi ajettava versio on [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). Alla oleva koodi näyttää päävaiheet, jotta artikkelin voi lukea opastuksena.

## 2. Asenna Paikalliset Riippuvuudet

Luo virtuaaliympäristö ja asenna Sarja 2:n vaatimukset:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Ensimmäinen versio käyttää Qdrantin paikallista tilaa ja FastEmbediä. Qdrantin Python-kirjasto tukee muistissa olevaa paikallista tilaa kutsulla `QdrantClient(":memory:")`, mikä on hyödyllistä paikallisissa oppaissa ja CI-tyylisissä tarkistuksissa. FastEmbed tarjoaa oikean paikallisen upotusmallin ilman tarvetta pilven API-avaimelle.

Vaadittavat riippuvuudet sisältävät myös `python-dotenv`-paketin, koska muistikirja voi valinnaisesti lukea Ollama-mallin nimeä `.env`-tiedostosta. Azure OpenAI:n tai OpenAI API-avainta ei tarvita tähän paikalliseen opastukseen.

## 3. Lataa Esimerkkidokumentit

Esimerkkikorpus on tarkoituksella pieni:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

Muistikirjassa lataan kaikki Markdown-tiedostot kansiosta `sample_data/`:

```python
from pathlib import Path

repo_root = Path.cwd()
if not (repo_root / "sample_data").exists():
    repo_root = Path.cwd().parent

sample_dir = repo_root / "sample_data"
sample_files = ["course_ai_guidance.md", "school_ai_policy.md"]
documents = []

for file_name in sample_files:
    path = sample_dir / file_name
    documents.append({
        "source": path.name,
        "text": path.read_text(encoding="utf-8"),
    })

print(f"Loaded {len(documents)} documents")
```

Kun ajoin muistikirjan, se latasi 2 dokumenttia. Se on tarpeeksi pieni, jotta voi tarkastella manuaalisesti, mikä on hyödyllistä kun rakennetaan ensimmäistä versiota RAG-putkesta.

## 4. Pilko Markdown-otsikoiden Mukaan

Seuraava vaihe on jakaa dokumentit osiin.

Tässä oppaassa käytän Markdown-otsikoita rakenteellisena merkkinä. Asiakirjan otsikko tulee `#`-merkistä ja jokainen osio pilkotaan kohdalla `##`.

> [!NOTE]
> Pilkkominen ei sovellu yhtä kokoaan kaikille. Tässä opastuksessa käytän Markdown-otsikoita, koska esimerkkidokumenteissa on selkeä `#` ja `##` rakenne. PDF-tiedostoissa, Word-dokumenteissa, dioissa, tiketeissä tai verkkosivuilla parempi strategia voi perustua sivurajoihin, asettelutietoihin, semanttisiin osioihin, token-rajoihin, taulukoihin tai metatietoihin. Tärkeää on valita pilkkomisstrategia, joka säilyttää dokumenttien merkityksen ja lähdeseurannan.

```python
def chunk_markdown(document):
    title = None
    current_heading = None
    current_lines = []
    chunks = []

    def flush():
        if current_heading and current_lines:
            content = "\n".join(current_lines).strip()
            if content:
                chunks.append({
                    "id": f"{document['source']}::{len(chunks)}",
                    "source": document["source"],
                    "title": title or document["source"],
                    "sectionHeading": current_heading,
                    "content": content,
                    "documentVersion": "local-sample-v1",
                    "permissions": ["students", "instructors"],
                })

    for raw_line in document["text"].splitlines():
        line = raw_line.strip()
        if line.startswith("# "):
            title = line[2:].strip()
        elif line.startswith("## "):
            flush()
            current_heading = line[3:].strip()
            current_lines = []
        elif line:
            current_lines.append(line)

    flush()
    return chunks
```

Sovellan sitä sitten jokaiseen dokumenttiin:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

Tämä loi paikallisessa ajossani 8 osaa.

Pidin tässä vaiheessa siitä, että metatiedot ovat jo hyödyllisiä. Jokainen osa tietää sen `source`-lähteen, `sectionHeading`-osiootsikon, `documentVersion`-asiakirjan version ja paikkamerkin `permissions`. Jo pienessäkin opastuksessa tämä helpottaa viittauksia ja myöhempää lupa-tietoista hakua.

## 5. Luo Paikalliset Upotukset

Ensimmäisessä julkisessa versiossa käytän `BAAI/bge-small-en-v1.5` FastEmbedin kautta.

Tämä pitää opastuksen paikallisena ja CPU-ystävällisenä, mutta käyttää silti oikeaa upotusmallia paikkamerkkivektorin sijaan. Ensimmäisellä kerralla malli ladataan painoineen. Sen jälkeen muistikirja voi käyttää paikallista välimuistia.

> [!NOTE]
> Käytän `BAAI/bge-small-en-v1.5` koska se on kevyt englanninkielinen upotusmalli, joka toimii hyvin FastEmbedin ja Qdrantin kanssa paikallisessa opastuksessa. Se luo 384-ulotteisia vektoreita, mikä pitää esimerkin nopeana ja edullisena paikalliseen käyttöön. Tämä ei ole ainoa hyvä vaihtoehto. Vuonna 2023 monet oppaat käyttivät isännöityjä upotusmalleja kuten `text-embedding-ada-002`. Nykyään uudemmat isännöidyt vaihtoehdot kuten OpenAI:n `text-embedding-3-small` ja `text-embedding-3-large` sekä avoimen lähdekoodin mallit kuten BGE, E5, MiniLM, Nomic Embed ja monikieliset mallit kuten `BAAI/bge-m3` ovat kaikki kohtuullisia valintoja kuormituksesta riippuen. Tuotannossa oikea upotusmalli valitaan oman dokumenttihakujen arvioinnin perusteella.

Joihinkin käytännöllisiin vaihtoehtoihin kuuluvat:

| Malliperhe | Milloin harkitsisin |
| --- | --- |
| `text-embedding-ada-002` | Vanhempi isännöity perusta, joka esiintyi monissa vuoden 2023 opetusohjelmissa. En valitsisi sitä oletukseksi uuteen opastukseen tänään. |
| `text-embedding-3-small` | Nykyajan isännöity oletus, kun haluan hyvän kustannus-suorituskykytasapainon enkä tarvitse pelkästään paikallisia upotuksia. |
| `text-embedding-3-large` | Isännöity vaihtoehto, kun hakutarkkuus on tärkeämpää kuin vektorin koko tai upotuskustannus. |
| `BAAI/bge-small-en-v1.5` | Kevyt paikallinen englanninkielinen malli opetusohjelmiin, prototyyppeihin ja CPU-ystävällisiin kokeiluihin. |
| `BAAI/bge-base-en-v1.5` tai `BAAI/bge-large-en-v1.5` | Suuremmat paikalliset englanninkieliset mallit parempaan hakutarkkuuteen ja jos laskentatehoa on saatavilla. |
| `BAAI/bge-m3` | Monikielinen tai pidemmän kontekstin haku, erityisesti kun dokumentit eivät ole pelkästään englanniksi. |
| `sentence-transformers/all-MiniLM-L6-v2` | Erittäin pieni ja nopea semanttinen haku. Hyödyllinen, kun nopeus ja yksinkertaisuus ovat tärkeimmät. |
| `nomic-embed-text-v1.5` | Avoin paikallinen upotusvaihtoehto, joka kannattaa testata pidemmän kontekstin tai siirrettävyyteen painottuvissa asetuksissa. |

```python
import re
from fastembed import TextEmbedding

EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"
embedding_model = TextEmbedding(model_name=EMBEDDING_MODEL_NAME)

def tokenize(text):
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    expanded = []
    for token in tokens:
        expanded.append(token)
        if token.endswith("s") and len(token) > 3:
            expanded.append(token[:-1])
    return expanded
```

Sitten jokaiselle osalle luodaan upotus:

```python
texts_to_embed = [
    f"{chunk['title']} {chunk['sectionHeading']} {chunk['content']}"
    for chunk in chunks
]
chunk_vectors = list(embedding_model.embed(texts_to_embed))
VECTOR_SIZE = len(chunk_vectors[0])

for chunk, vector in zip(chunks, chunk_vectors):
    chunk["vector"] = vector
```

## 6. Tallenna Vektorit Qdrantin Paikallisessa Tilassa

Nyt luomme muistissa olevan Qdrant-kokoelman ja lisäämme osat payload-metatietoineen.

> [!NOTE]
> Vuoden 2023 oppaassa käytin FAISSia, koska se oli yksinkertainen ja suosittu tapa demonstroida paikallista vektoriläheisyyshakua LangChainilla. FAISS on edelleen hyödyllinen nopeita paikallisia kokeiluja varten. Tässä vuoden 2026 versiossa käytän Qdrantia, koska haluan oppaan tuntuvan lähempänä tuotannon RAG-järjestelmää. Qdrant antaa tallentaa vektorit yhdessä metadatan kanssa kuten lähdetiedosto, osiootsikko, dokumenttiversio ja käyttöoikeudet. Tämä helpottaa hakujen tarkastelua ja valmistelee esimerkin suodatukseen, viitteisiin ja tulevaan pysyvään tai palvelinperusteiseen käyttöönottoon.

FAISS on erinomainen osoittamaan vektoreihin perustuvaa samankaltaisuushaun toimintaa. Qdrant on parempi näyttämään pieni mutta tuotannon kaltainen RAG-hakukerros.

Joihinkin käytännöllisiin vaihtoehtoihin kuuluvat:

| Vektorivarasto / hakukerros | Milloin harkitsisin |
| --- | --- |
| Qdrant | Paikalliset prototyypit, metatietojen suodatus, tuotantoon soveltuva vektorihaku ja yksinkertainen Python-työnkulku. |
| Chroma | Nopeat paikalliset RAG-kokeilut ja muistikirjat, joissa yksinkertaisuus on tärkeintä. |
| FAISS | Kevyt paikallinen vektorihaku, kun tarvitsen vain samankaltaisuushakua ja voin hallita metatietoja erillään. |
| Milvus | Suuremmat avoimen lähdekoodin vektorihakuratkaisut, kun tiimi on valmis päivittämään dedikoidun vektoritietokannan. |
| Weaviate | Vektorihaku skeemalla, metatiedoilla, hybridihaulla sekä hallinnoidut tai itse isännöidyt käyttöönotot. |
| Azure AI Search | Yritystason RAG Azurella, kun haluan avainsanahaun, vektorihaku, hybridihakemiston, semanttisen lajittelun, suodattamisen, tietoturvan ja hallinnoidut toiminnot yhdellä hakukerroksella. |
| PostgreSQL + pgvector | Tiimit, jotka käyttävät jo PostgreSQL:ää ja haluavat vektorihakua lähellä sovellusdataa. |

```python
from qdrant_client import QdrantClient, models

collection_name = "school_policy_local"
client = QdrantClient(":memory:")

client.create_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(
        size=VECTOR_SIZE,
        distance=models.Distance.COSINE,
    ),
)
```

Lisää sitten pisteet:

```python
points = []

for idx, chunk in enumerate(chunks):
    payload = {
        key: chunk[key]
        for key in [
            "source",
            "title",
            "sectionHeading",
            "content",
            "documentVersion",
            "permissions",
        ]
    }
    points.append(
        models.PointStruct(
            id=idx,
            vector=chunk["vector"].tolist(),
            payload=payload,
        )
    )

client.upsert(collection_name=collection_name, points=points)
```

Omassa ajossani kokoelmaan lisättiin 8 vektoria.

Tässä vaiheessa RAG-järjestelmästä alkaa tulla tutkittavissa oleva. Vektorivarasto ei tallenna pelkkiä vektoreita, vaan myös todistustekstiä ja viitteisiin tarvittavaa metadataa.

## 7. Hae Hakuehdokkaat

Nyt kysymme kysymyksen ja haemme ehdokkaat osat.

```python
question = "Can I use generative AI for my final assignment?"
query_vector = list(embedding_model.embed([question]))[0].tolist()

raw_results = client.query_points(
    collection_name=collection_name,
    query=query_vector,
    limit=5,
    with_payload=True,
).points
```

Tässä vaiheessa tulostan haetut osat ennen vastauksen generointia. Tämä on tärkeää. Jos haku on väärin, generointi vain piilottaa ongelman sujuvan tekstin taakse.

## 8. Lisää Kevyt Uudelleenjärjestäjä

Kun testasin aluksi hakupolkua, vektoriläheisyys löysi aiheeseen liittyvän politiikkasisällön, mutta täsmällisin osio ei aina ollut ylimpänä.

Lisäsin siis pienen paikallisen uudelleenjärjestäjän. Se antaa lisäpainoa, kun kysymyksen termit menevät päällekkäin osion otsikon ja sisällön kanssa.

```python
query_terms = set(tokenize(question))

def rerank_score(result):
    payload = result.payload
    heading_terms = set(tokenize(payload["sectionHeading"]))
    content_terms = set(tokenize(payload["content"]))
    heading_overlap = len(query_terms & heading_terms)
    content_overlap = len(query_terms & content_terms)
    return result.score + (0.12 * heading_overlap) + (0.02 * content_overlap)

results = sorted(raw_results, key=rerank_score, reverse=True)[:3]
```

Uudelleenjärjestämisen jälkeen kärkitulos oli:

```text
school_ai_policy.md / Final Assignments
```

Se oli odotettu osio testikysymykselle.

Tämä oli hyödyllisin oppi ensimmäisestä toteutuksesta. Jo pienessä paikallisessa esimerkissä hakutarkkuus parani, kun yhdistin vektoriläheisyyden toiseen signaaliin.

## 9. Koosta Perusteltu Paikallinen Vastaus

Oletuspolulla käytän läpinäkyvää paikallista vastausten koostajaa LLM:n sijaan.

```python
top = results[0].payload

answer = (
    "Based on the retrieved policy section, students may use generative AI for "
    "brainstorming, outlining, grammar feedback, and code explanation when the "
    "instructor allows it. They should not submit AI-generated work as their own, "
    "and they should include a disclosure when AI tools are used."
)

print("Answer:")
print(answer)
print("\nSource:")
print(f"{top['source']} / {top['sectionHeading']}")
```

Tätä ei ole tarkoitettu lopulliseksi tuotantovastauksen generaattoriksi. Se on debug-työkalu. Se osoittaa, että haku, metadata ja viittaukset toimivat ennen mallivariaatioiden lisäämistä.

## 10. Generoi Paikallinen Vastaus Ollamalla ja Phi-4-minillä

Kun haku toimii, muistikirja voi korvata pelkän lopullisen vastausvaiheen Ollamalla ja `phi4-mini:3.8b`:llä.

> [!NOTE]
> Ollama tulisi korvata vain lopullinen vastausgenerointivaihe. Dokumenttien lataus, pilkkominen, vektorivarastointi, haku, uudelleenjärjestäminen ja viittausten yhdistely säilyvät ennallaan.

Ensiksi muistikirja rakentaa todistuskappalepromptin haetuista osista:

```python
def build_evidence(retrieved_results):
    evidence_blocks = []
    for idx, result in enumerate(retrieved_results, start=1):
        payload = result.payload
        evidence_blocks.append(
            f"[{idx}] Source: {payload['source']} / {payload['sectionHeading']}\n"
            f"{payload['content']}"
        )
    return "\n\n".join(evidence_blocks)

evidence = build_evidence(results)
answer_prompt = (
    "Answer the question using only the evidence below. "
    "If the evidence is insufficient, say that the provided documents do not contain enough information. "
    "End with a Sources line that lists the source file and section.\n\n"
    f"Question: {question}\n\nEvidence:\n{evidence}"
)
```

Tässä oppaassa suosittelen Microsoftin Phi-4-miniperhettä Ollaman kautta oletuksena paikalliseen generointiin. Ollamassa testaamani mallin nimi on:

```powershell
ollama pull phi4-mini:3.8b
```

Voit nopeasti varmistaa mallin saatavuuden:

```powershell
ollama list
```

Aseta sitten nämä muuttujat:

```powershell
Copy-Item .env.example .env
```

Avaa `.env` ja poista kommentointi Sarja 2:n Ollama-arvoista:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Muistikirja lataa `.env`-tiedoston repositorion juuresta `python-dotenv`-kirjastolla ja lähettää saman todistuspohjaisen promtin Ollaman paikalliseen `/api/chat`-päätepisteeseen ilman striimausta. Jos Ollama ei ole käynnissä tai `SERIES2_OLLAMA_MODEL` puuttuu, tämä polku ohitetaan.

> [!NOTE]
> Tällä koneella `phi4-mini:3.8b` latasi noin 2.49 Gt mallin tiedostoja. Inferenssin aikana Ollama raportoi 3.3 Gt ladatun mallin koon ja käytti RTX 3060 Laptop GPU:ta.

Tämä antaa opastukselle kaksi tasoa:

1. Pelkkään CPU:hun perustuva deterministinen vastausten koostaja.
2. Paikallinen vastausgenerointi Ollamalla ja Phi-4-minillä.

Hakuprosessi pysyy samana molemmissa.

## 11. Tarkistustulos

Ajoin muistikirjan paikallisesti Windowsilla Python 3.12.6 -ympäristössä.

Asennetut paketit:

| Paketti | Versio |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Muistikirjan suoritus:

- Muistikirja: `notebooks/series-2-open-source-rag.ipynb`
- Suoritustulos: onnistui `nbclient`-kirjastolla
- Latautuneet dokumentit: 2
- Luodut osat: 8
- Qdrant-kokoelma: `school_policy_local`
- Lisätyt vektorit: 8
- Upotusmalli: `BAAI/bge-small-en-v1.5`
- Upotusvektorin koko: 384
- Haku kysymys: "Voinko käyttää generatiivista tekoälyä lopputyössäni?"
- Uudelleenjärjestely polku: kevyt paikallinen leksikaalinen uudelleenjärjestely
- Paras haettu lähde uudelleenjärjestelyn jälkeen: `school_ai_policy.md`
- Paras haettu osio uudelleenjärjestelyn jälkeen: `Final Assignments`
- Oletus vastauspolku: paikallinen läpinäkyvä vastauskomponisti
- Ollama generointipolku: valmistui `phi4-mini:3.8b` avulla
- Ollama mallin tiedostokoko: 2.49GB levyllä
- Ollama ladatun mallin koko: 3.3GB raportoituna komennolla `ollama ps`
- GPU:n kuormitus: 100% GPU raportoituna komennolla `ollama ps`
- GPU muistin käyttö generoinnin jälkeen: noin 3.5GB käytössä 6GB:stä RTX 3060 Laptop GPU:lla
- Muistikirjan suoritus välimuistitetulla FastEmbed-mallilla ja Ollama generoinnilla: suoritettu noin 34 sekunnissa vahvistusskriptin läpi

Ollaman generoima vastaus oli:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

En kutsuisi tätä vastausta täydelliseksi. Se vastaa oikeasta todisteesta, mutta lopullinen lähderivi on vähemmän tarkka kuin deterministinen viittausmuoto. Tämä on hyödyllistä näyttää tutoriaalissa, koska se tekee seuraavasta insinöörikysymyksestä ilmeisen: vastausten generointia täytyy myös arvioida, ei pelkästään hakua.

Pääasia, jonka opin tätä varmistaessani, on että haun laatua tulee tarkistaa ennen vastausten generointia. Upotus tulos oli jo hyödyllinen, ja kevyt uudelleenjärjestäjä sai odotetun politiikkaosion näkyviin luotettavasti ensimmäisenä. Tämä on juuri sellainen pieni järjestelmän käyttäytyminen, joka haluan, että tutoriaali paljastaa sen sijaan, että piilottaa.

## 12. Mitä seuraavaksi

Seuraava parannus on verrata tätä paikallista asetusta Azure-palveluna tarjottuun samaan koulun politiikkavastaaja-skenaarioon. Skenaarion pitäminen samana helpottaa kompromissien näkemistä: asennuksen monimutkaisuus, haun hallinta, identiteetin integrointi, operatiivinen vastuu ja kustannukset.

## 13. Viitteet

- [Qdrant Python client quickstart](https://python-client.qdrant.tech/quickstart.html)
- [Qdrant client GitHub -varasto](https://github.com/qdrant/qdrant-client)
- [FastEmbed tuetut mallit](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [OpenAI upotukset opas](https://platform.openai.com/docs/guides/embeddings)
- [BAAI/bge-small-en-v1.5 mallikortti](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [BAAI/bge-m3 mallikortti](https://huggingface.co/BAAI/bge-m3)
- [sentence-transformers/all-MiniLM-L6-v2 mallikortti](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Ollama phi4-mini mallisivu](https://ollama.com/library/phi4-mini)
- [Ollama Windows dokumentaatio](https://docs.ollama.com/windows)
- [Ollama API suoratoistodokumentaatio](https://docs.ollama.com/api/streaming)
- [Microsoft Phi-4-mini-instruct mallikortti](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [LangGraph yleiskatsaus](https://docs.langchain.com/oss/python/langgraph)
- [Johdanto RAG:iin - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

Edellinen: [Sarja 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastuuvapauslauseke**:
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, otathan huomioon, että automaattiset käännökset saattavat sisältää virheitä tai epätarkkuuksia. Alkuperäinen asiakirja sen alkuperäiskielellä on virallinen lähde. Tärkeissä asioissa suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa tämän käännöksen käytöstä aiheutuvista väärinymmärryksistä tai tulkinnoista.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->