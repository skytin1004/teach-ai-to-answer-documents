# Kuchangia

Hifadhi hii imepangwa kama mfululizo wa blogi pamoja na mifano ya daftari inayoweza kuendeshwa.

## Kabla ya Kufungua Ombi la Kuvuta

Endesha script ya uhakiki ya ndani:

```powershell
python scripts\verify_notebooks.py
```

Kwa utekelezaji au mabadiliko ya daftari, endesha utekelezaji wa daftari salama wa ndani:

```powershell
python scripts\verify_notebooks.py --execute
```

## Miongozo ya Daftari

- Weka daftari zisiwe ngumu kusomeka na zizingatie makala husika.
- Usihifadhi matokeo ya daftari yaliyohifadhiwa au idadi ya utekelezaji.
- Tumia data ndogo ya mfano kutoka `sample_data/` isipokuwa makala inahitaji rasilimali maalum ya nje.
- Rekodi matokeo ya uhakiki katika makala husika wakati tabia zinabadilika.

## Siri na Vibali

- Usihifadhi funguo za API, tokeni, nywila, viambatanisho vya binafsi, au faili za `.env`.
- Tumia `.env.example` kwa thamani za kielezi tu.
- Tumia vigezo vya mazingira kwa majaribio ya eneo la Ollama ya hiari.

## Nyaraka

- Sasisha viungo vya urambazaji wa makala.
- Sasisha `README.md` unapoongeza makala mpya, daftari, faili za mahitaji, au faili za data za mfano.
- Sasisha `CHANGELOG.md` kabla ya kuchapisha sasisho la hifadhi linaloonekana.

## Uhifadhi

Mchakato wa GitHub Actions unafanya kazi:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Vifungu vya rasimu chini ya `drafts/` havizingatiwi na uhakiki wa hifadhi hadi viwe tayari kwa uteuzi wa umma.

## Masuala

Tumia kiolezo cha maoni ya makala kwa marekebisho ya makala na kiolezo cha masuala ya daftari kwa matatizo ya utekelezaji wa daftari.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Kionyozo**:
Hati hii imetafsiriwa kwa kutumia huduma ya tafsiri ya AI [Co-op Translator](https://github.com/Azure/co-op-translator). Ingawa tunajitahidi kupata usahihi, tafadhali fahamu kwamba tafsiri za kiotomatiki zinaweza kuwa na makosa au upungufu wa usahihi. Hati ya asili katika lugha yake halisi inapaswa kuchukuliwa kama chanzo cha mamlaka. Kwa taarifa muhimu, tafsiri ya kitaalamu inayofanywa na binadamu inapendekezwa. Hatutojibu kwa kuelewa vibaya au tafsiri potofu zinazotokea kutokana na matumizi ya tafsiri hii.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->