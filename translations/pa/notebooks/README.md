# ਨੋਟਬੁੱਕਸ

ਇਹ ਨੋਟਬੁੱਕਸ ਦੌੜਾਏ ਜਾ ਸਕਦੇ ਉਦਾਹਰਣਾਂ ਨਾਲ ਲੇਖ ਸਿਰੀਜ਼ ਦਾ ਸਹਾਰਾ ਦਿੰਦੇ ਹਨ।

| ਨੋਟਬੁੱਕ | ਲੇਖ | ਉਦੇਸ਼ |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [ਸਿਰੀਜ਼ 2](../articles/series-2-open-source-rag-end-to-end.md) | ਫਾਸਟਐਮਬੇਡ, Qdrant ਲੋਕਲ ਮੋਡ, ਰੀਟਰੀਵਲ, ਰੀਰੈਂਕਿੰਗ, ਵਿਕਲਪੀ ਓਲਾਮਾ ਜਨਰੇਸ਼ਨ ਅਤੇ ਸਰੋਤ ਸੰਦਰਭਾਂ ਨਾਲ ਖੁੱਲ੍ਹਾ ਸਰੋਤ RAG |

## ਸਥਾਨਕ ਤੌਰ 'ਤੇ ਚਲਾਓ

ਜੋ ਨੋਟਬੁੱਕ ਤੁਸੀਂ ਚਲਾਉਣਾ ਚਾਹੁੰਦੇ ਹੋ ਉਸ ਲਈ ਲੋੜੀਂਦੇ ਪੈਕੇਜ ਇੰਸਟਾਲ ਕਰੋ:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

ਜਾਂ ਸਾਰੇ ਨਿਰਭਰਤਾ ਇੰਸਟਾਲ ਕਰੋ:

```powershell
python -m pip install -r requirements\all.txt
```

## ਵੈਰੀਫਾਈ ਕਰੋ

ਰਿਪੋਜ਼ਿਟਰੀ ਰੂਟ ਤੋਂ:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

ਸਿਰੀਜ਼ 2 ਰਿਪੋਜ਼ਿਟਰੀ-ਰੂਟ `.env` ਫਾਈਲ ਤੋਂ ਓਲਾਮਾ ਕਾਂਫਿਗਰੇਸ਼ਨ ਪੜ੍ਹ ਸਕਦਾ ਹੈ। [../.env.example](../../../.env.example) ਤੋਂ ਸ਼ੁਰੂ ਕਰੋ, ਜੋ ਕਿ ਸਿਰੀਜ਼ ਅਨੁਸਾਰ ਸਮੂਹਬੱਧ ਹੈ।

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ਅਸਵੀਕਾਰੋਪਣ**:
ਇਸ ਦਸਤਾਵੇਜ਼ ਦਾ ਅਨੁਵਾਦ ਏਆਈ ਅਨੁਵਾਦ ਸੇਵਾ [Co-op Translator](https://github.com/Azure/co-op-translator) ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਕੀਤਾ ਗਿਆ ਹੈ। ਜਦੋਂ ਕਿ ਅਸੀਂ ਸਹੀਤਾਵਾਂ ਲਈ ਯਤਨਸ਼ੀਲ ਹਾਂ, ਕਿਰਪਾ ਕਰਕੇ ਧਿਆਨ ਰੱਖੋ ਕਿ ਸਵੈਚਾਲਿਤ ਅਨੁਵਾਦਾਂ ਵਿੱਚ ਗਲਤੀਆਂ ਜਾਂ ਅਸਮੱਤਿਆਵਾਂ ਹੋ ਸਕਦੀਆਂ ਹਨ। ਮੂਲ ਦਸਤਾਵੇਜ਼ ਆਪਣੀ ਮੂਲ ਭਾਸ਼ਾ ਵਿੱਚ ਅਧਿਕਾਰਕ ਸਰੋਤ ਮੰਨਿਆ ਜਾਣਾ ਚਾਹੀਦਾ ਹੈ। ਜਰੂਰੀ ਜਾਣਕਾਰੀ ਲਈ, ਪੇਸ਼ੇਵਰ ਮਨੁੱਖੀ ਅਨੁਵਾਦ ਦੀ ਸਿਫ਼ਾਰਸ਼ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। ਅਸੀਂ ਇਸ ਅਨੁਵਾਦ ਦੇ ਉਪਯੋਗ ਤੋਂ ਪੈਦਾ ਹੋਣ ਵਾਲੀਆਂ ਕਿਸੇ ਵੀ ਗਲਤਫਹਿਮੀਆਂ ਜਾਂ ਗਲਤ ਵਿਆਖਿਆਵਾਂ ਲਈ ਜਵਾਬਦੇਹ ਨਹੀਂ ਹਾਂ।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->