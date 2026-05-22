# Komut Dosyaları

Bu klasör depo doğrulama komut dosyalarını içerir.

## `verify_notebooks.py`

Yerel Markdown bağlantılarını, defter JSON'unu, defter çıktı temizliğini ve yüksek riskli gizli desenleri doğrular:

```powershell
python scripts\verify_notebooks.py
```

Tüm genel yerel-güvenli defterleri çalıştırır:

```powershell
python scripts\verify_notebooks.py --execute
```

GitHub Actions iş akışı aynı komut dosyasını kullanır.

`drafts/` altındaki taslak materyal, genel dizin için hazır olana kadar atlanır.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Feragatname**:
Bu belge, AI çeviri hizmeti [Co-op Translator](https://github.com/Azure/co-op-translator) kullanılarak çevrilmiştir. Doğruluk için çaba sarf etsek de, otomatik çevirilerin hata veya yanlışlık içerebileceğini lütfen unutmayınız. Orijinal belge, kendi dilinde yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilir. Bu çevirinin kullanımı sonucu ortaya çıkabilecek yanlış anlamalardan veya yanlış yorumlamalardan sorumlu değiliz.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->