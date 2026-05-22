# Not Defterleri

Bu not defterleri, çalıştırılabilir örneklerle makale serisini destekler.

| Not Defteri | Makale | Amaç |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Seri 2](../articles/series-2-open-source-rag-end-to-end.md) | FastEmbed, Qdrant yerel mod, alma, yeniden sıralama, isteğe bağlı Ollama üretimi ve kaynak referansları ile açık kaynak RAG |

## Yerelde Çalıştır

Çalıştırmak istediğiniz not defteri için gereksinimleri yükleyin:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Ya da tüm bağımlılıkları yükleyin:

```powershell
python -m pip install -r requirements\all.txt
```

## Doğrula

Depo kökünden:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Seri 2, bir depo kökü `.env` dosyasından Ollama yapılandırmasını okuyabilir. Seriye göre gruplanmış [../.env.example](../../../.env.example) dosyasından başlayın.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Feragatname**:
Bu belge, AI çeviri hizmeti [Co-op Translator](https://github.com/Azure/co-op-translator) kullanılarak çevrilmiştir. Doğruluk için çaba sarf etsek de, otomatik çevirilerin hata veya yanlışlık içerebileceğini lütfen unutmayınız. Orijinal belge, kendi dilinde yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilir. Bu çevirinin kullanımı sonucu ortaya çıkabilecek yanlış anlamalardan veya yanlış yorumlamalardan sorumlu değiliz.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->