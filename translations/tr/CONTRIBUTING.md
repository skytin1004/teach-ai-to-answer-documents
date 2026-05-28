# Katkıda Bulunma

Bu depo, bir blog serisi artı çalıştırılabilir not defteri örnekleri olarak organize edilmiştir.

## Pull Request Açmadan Önce

Yerel doğrulama betiğini çalıştırın:

```powershell
python scripts\verify_notebooks.py
```

Uygulama veya not defteri değişiklikleri için, yerel-güvenli not defteri yürütmesini çalıştırın:

```powershell
python scripts\verify_notebooks.py --execute
```

## Not Defteri Kuralları

- Not defterlerini okunabilir ve ilgili makaleye odaklı tutun.
- Kaydedilmiş not defteri çıktılarını veya yürütme sayımlarını commit etmeyin.
- Makale belirli bir dış kaynağı gerektirmedikçe `sample_data/` içindeki küçük örnek verileri kullanın.
- Davranış değişikliklerinde doğrulama sonuçlarını ilgili makalede kaydedin.

## Gizli Bilgiler ve Kimlik Doğrulama Bilgileri

- API anahtarları, tokenlar, şifreler, özel uç noktalar veya `.env` dosyalarını commit etmeyin.
- Yer tutucu değerler için sadece `.env.example` kullanın.
- İsteğe bağlı yerel Ollama deneyleri için ortam değişkenlerini kullanın.

## Dokümantasyon

- Makale gezinti bağlantılarını güncel tutun.
- Yeni bir makale, not defteri, gereksinimler dosyası veya örnek veri dosyası eklerken `README.md` dosyasını güncelleyin.
- Görünür bir depo güncellemesi yayınlamadan önce `CHANGELOG.md` dosyasını güncelleyin.

## Doğrulama

GitHub Actions iş akışı şunları çalıştırır:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

`drafts/` altındaki taslak materyaller, genel dizine eklenmeye hazır olana kadar depo doğrulaması tarafından atlanır.

## Sorunlar

Makalelerdeki düzeltmeler için makale geri bildirim şablonunu, not defteri yürütme problemleri için not defteri sorun şablonunu kullanın.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Feragatname**:
Bu belge, AI çeviri hizmeti [Co-op Translator](https://github.com/Azure/co-op-translator) kullanılarak çevrilmiştir. Doğruluk için çaba sarf etsek de, otomatik çevirilerin hata veya yanlışlık içerebileceğini lütfen unutmayınız. Orijinal belge, kendi dilinde yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilir. Bu çevirinin kullanımı sonucu ortaya çıkabilecek yanlış anlamalardan veya yanlış yorumlamalardan sorumlu değiliz.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->