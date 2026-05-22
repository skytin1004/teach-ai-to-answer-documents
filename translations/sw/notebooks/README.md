# Daftari za Kumbukumbu

Daftari hizi za kumbukumbu zinaunga mkono mfululizo wa makala na mifano inayoweza kuendesha.

| Daftari la Kumbukumbu | Makala | Kusudi |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Mfululizo 2](../articles/series-2-open-source-rag-end-to-end.md) | RAG ya chanzo huria na FastEmbed, hali ya eneo la Qdrant, utafutaji, upangaji upya, uzalishaji wa hiari wa Ollama, na marejeleo ya vyanzo |

## Endesha Kwenye Eneo la Mitaa

Sakinisha mahitaji kwa daftari la kumbukumbu unalotaka kuendesha:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Au sakinisha utegemezi wote:

```powershell
python -m pip install -r requirements\all.txt
```

## Thibitisha

Kutoka kwenye mizizi ya hazina:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Mfululizo wa 2 unaweza kusoma usanidi wa Ollama kutoka kwenye faili `.env` ya mizizi ya hazina. Anza kutoka [../.env.example](../../../.env.example), ambayo imeainishwa kwa mfululizo.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Kionyozo**:
Hati hii imetafsiriwa kwa kutumia huduma ya tafsiri ya AI [Co-op Translator](https://github.com/Azure/co-op-translator). Ingawa tunajitahidi kupata usahihi, tafadhali fahamu kwamba tafsiri za kiotomatiki zinaweza kuwa na makosa au upungufu wa usahihi. Hati ya asili katika lugha yake halisi inapaswa kuchukuliwa kama chanzo cha mamlaka. Kwa taarifa muhimu, tafsiri ya kitaalamu inayofanywa na binadamu inapendekezwa. Hatutojibu kwa kuelewa vibaya au tafsiri potofu zinazotokea kutokana na matumizi ya tafsiri hii.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->