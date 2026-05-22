# Orodha ya Kuchapisha

Tumia orodha hii kabla ya kutuma au kusukuma masasisho ya umma.

## Usalama

- Thibitisha hakuna funguo za API, tokeni, nywila, au sehemu binafsi zilizomo ndani ya faili za Markdown, daftari, data ya mfano, au skripti.
- Weka nyaraka za kuingia kwenye vigezo vya mazingira au utambulisho ulioendeshwa, sio katika faili zilizotumwa.
- Usitume faili za `.env` au faili za matokeo ya daftari zilizotekwa.
- Weka `.env.example` kuwa tu nafasi ya mfano.

## Uhakiki

Endesha skripti ya uhakiki ya hazina:

```powershell
python scripts\verify_notebooks.py
```

Endesha utekelezaji kamili wa daftari salama kwa ndani kabla ya kuchapisha mabadiliko ya utekelezaji:

```powershell
python scripts\verify_notebooks.py --execute
```

Ukaguzi unaotarajiwa:

- viungo vya Markdown vya ndani vipite
- uthibitishaji wa JSON wa daftari upite
- daftari hazina matokeo yaliyohifadhiwa au hesabu za utekelezaji
- mtihani wa mifumo ya siri yenye hatari kubwa upite
- daftari za umma zote zinaendeshwa kwa ndani
- vifaa vya rasimu chini ya `drafts/` vimetengwa kwa makusudi

## Mapitio

- Thibitisha viungo vya makala za README vinaelekeza kwenye faili sahihi.
- Thibitisha kila makala ina urambazaji wa hazina na viungo vya daftari vinavyohusiana.
- Thibitisha rasimu hazijiunganishwi katika faharasa za umma isipokuwa ziko tayari kuchapishwa.
- Thibitisha templeti za masuala na madai za GitHub bado zinaendana na utaratibu wa hazina.
- Thibitisha matokeo ya uhakiki katika makala yanalingana na matokeo ya hivi karibuni ya daftari.
- Thibitisha mchakato wa GitHub Actions unatarajiwa kuendeshwa baada ya kusukuma.
- Thibitisha `CHANGELOG.md` inaonyesha sasisho linalochapishwa.
- Thibitisha `CONTRIBUTING.md` bado inaendana na utaratibu wa hazina.

## Git

- Pitia `git status --short --branch`.
- Pitia `git diff --stat`.
- Tuma na sukuma tu wakati uko tayari wazi.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Kionyozo**:
Hati hii imetafsiriwa kwa kutumia huduma ya tafsiri ya AI [Co-op Translator](https://github.com/Azure/co-op-translator). Ingawa tunajitahidi kupata usahihi, tafadhali fahamu kwamba tafsiri za kiotomatiki zinaweza kuwa na makosa au upungufu wa usahihi. Hati ya asili katika lugha yake halisi inapaswa kuchukuliwa kama chanzo cha mamlaka. Kwa taarifa muhimu, tafsiri ya kitaalamu inayofanywa na binadamu inapendekezwa. Hatutojibu kwa kuelewa vibaya au tafsiri potofu zinazotokea kutokana na matumizi ya tafsiri hii.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->