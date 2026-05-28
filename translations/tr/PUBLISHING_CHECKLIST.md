# Yayınlama Kontrol Listesi

Genel güncellemeleri commit veya push yapmadan önce bu kontrol listesini kullanın.

## Güvenlik

- API anahtarlarının, tokenların, parolaların veya özel uç noktaların Markdown dosyalarına, defterlere, örnek verilere veya betiklere yazılmadığını doğrulayın.
- Kimlik bilgilerini ortam değişkenlerinde veya yönetilen kimlikte tutun, commit edilen dosyalarda değil.
- `.env` dosyalarını veya çalıştırılmış notebook çıktı dosyalarını commit etmeyin.
- `.env.example` sadece yer tutucu olarak kalmalıdır.

## Doğrulama

Depo doğrulama betiğini çalıştırın:

```powershell
python scripts\verify_notebooks.py
```

Uygulama değişikliklerini yayınlamadan önce tamamı yerel güvenli notebook yürütmesini çalıştırın:

```powershell
python scripts\verify_notebooks.py --execute
```

Beklenen kontroller:

- yerel Markdown bağlantıları geçer
- notebook JSON doğrulaması geçer
- notebooklar kayıtlı çıktı veya yürütme sayısı içermez
- yüksek riskli gizli desen taraması geçer
- genel notebooklar yerel olarak yürütülür
- `drafts/` altındaki taslak materyaller kasten atlanır

## İnceleme

- README makale bağlantılarının hedef dosyalara işaret ettiğini doğrulayın.
- Her makalenin depo gezinmesi ve ilgili notebook bağlantılarına sahip olduğunu doğrulayın.
- Taslakların kamu indekslerinden bağlantı verilmediğini, yalnızca yayınlanmaya hazır oldukları durumda bağlandığını doğrulayın.
- GitHub issue ve pull request şablonlarının depo iş akışıyla uyumlu olduğunu doğrulayın.
- Makaledeki doğrulama sonuçlarının en son notebook çıktısıyla eşleştiğini doğrulayın.
- GitHub Actions iş akışının push sonrası beklenen şekilde çalışacağını doğrulayın.
- `CHANGELOG.md` dosyasının yapılan güncellemeyi yansıttığını doğrulayın.
- `CONTRIBUTING.md` dosyasının depo iş akışıyla uyumlu olduğunu doğrulayın.

## Git

- `git status --short --branch` komut çıktısını inceleyin.
- `git diff --stat` komut çıktısını inceleyin.
- Sadece açıkça hazır olduğunda commit ve push yapın.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Feragatname**:
Bu belge, AI çeviri hizmeti [Co-op Translator](https://github.com/Azure/co-op-translator) kullanılarak çevrilmiştir. Doğruluk için çaba sarf etsek de, otomatik çevirilerin hata veya yanlışlık içerebileceğini lütfen unutmayınız. Orijinal belge, kendi dilinde yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilir. Bu çevirinin kullanımı sonucu ortaya çıkabilecek yanlış anlamalardan veya yanlış yorumlamalardan sorumlu değiliz.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->