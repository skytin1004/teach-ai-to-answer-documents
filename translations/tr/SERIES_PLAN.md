# Yapay Zekayı Belgeleriniz Üzerinden Soru Cevaplamaya Öğretme - Seri Planı

Bu plan, genel Seri 1 ve Seri 2 yayını takip eder. Daha sonra Azure ve değerlendirme çalışmaları, örnekler tam uçtan uca ve doğrulanana kadar taslak olarak tutuluyor.

Açıkça talimat verilinceye kadar değişiklikleri commit veya push etmeyin.

## Genel Kapsam

Mevcut genel yayın:

- Seri 1 makalesi: RAG mimari kararları, Azure ve açık kaynak karşılaştırmaları, ince ayarın nerede yer aldığı.
- Seri 2 makalesi: yerel açık kaynak RAG eğitimi.
- Seri 2 defteri: FastEmbed, Qdrant, Ollama ve Phi-4-mini ile çalıştırılabilir yerel RAG laboratuvarı.
- Örnek veri: okul politikası ve kurs yapay zeka rehberi Markdown dosyaları.

Taslak halinde olup henüz genel indeks içinde olmayanlar:

- Azure AI Search ve Azure OpenAI'nin yeniden yapımı.
- RAG değerlendirmesi ve regresyon kontrolleri.

## Eğitim Senaryosu

Paylaşılan senaryo bir okul politika asistanıdır.

Asistan, yerel belgelerden şu soruyu yanıtlar:

```text
Can I use generative AI for my final assignment?
```

Beklenen davranış şudur:

1. Yerel Markdown belgeleri yükle.
2. Başlıklara göre ayrıştır ve parçala.
3. Yerel gömüler oluştur ve metadata ile aranabilir temsiller yap.
4. İlgili politika bölümünü al.
5. Gerekirse yeniden sıralama yap.
6. Temellendirilmiş bir cevap üret veya oluştur.
7. Kaynakları geri döndür.
8. Doğrulama sonuçlarını kaydet.

## Mevcut Genel Yapı

```text
.
├── README.md
├── SERIES_PLAN.md
├── articles/
│   ├── README.md
│   ├── series-1-rag-azure-open-source-fine-tuning.md
│   └── series-2-open-source-rag-end-to-end.md
├── notebooks/
│   ├── README.md
│   └── series-2-open-source-rag.ipynb
├── sample_data/
│   ├── README.md
│   ├── course_ai_guidance.md
│   └── school_ai_policy.md
├── requirements/
│   ├── README.md
│   ├── all.txt
│   └── open-source-rag.txt
└── scripts/
    ├── README.md
    └── verify_notebooks.py
```

Taslak materyal `drafts/` altında saklanır ve genel indekslemeye hazır olana kadar depo doğrulamasında atlanır.

## Seri 2 Doğrulama

Windows üzerinde Python 3.12.6 ile doğrulanmıştır.

- `requirements/open-source-rag.txt` başarıyla yüklendi.
- `notebooks/series-2-open-source-rag.ipynb` `nbclient` ile çalıştırıldı.
- Yerel doğrulama geçti: 2 örnek doküman yüklendi, 8 parça oluşturuldu, FastEmbed 384 boyutlu yerel gömüler üretti, Qdrant bellekte koleksiyon başlattı ve 8 vektör eklendi.
- Test sorusu: "Son ödevimde üretken yapay zekayı kullanabilir miyim?"
- Hafif yeniden sıralamadan sonra en üst bulunan kaynak: `school_ai_policy.md`.
- Hafif yeniden sıralamadan sonra en üst bulunan bölüm: `Final Assignments`.
- Varsayılan cevap yolu: yerel şeffaf cevap oluşturucu.
- Ollama winget ile yüklendi; `phi4-mini:3.8b` başarıyla çekildi.
- Ollama cevap üretim yolu: `phi4-mini:3.8b` ile tamamlandı.
- Ollama model dosya boyutu: disk üzerinde yaklaşık 2.49GB.
- Ollama yüklü model boyutu: `ollama ps` tarafından bildirilen 3.3GB.
- GPU offload: RTX 3060 Laptop GPU’da `ollama ps` tarafından %100 GPU olarak raporlandı.
- Üretim sonrası gözlemlenen GPU belleği: 6GB’dan yaklaşık 3.5GB.
- Önbelleğe alınmış FastEmbed modeli ve Ollama üretimi etkin olarak defterin çalıştırılması doğrulama betiğiyle yaklaşık 34 saniyede geçti.
- Gözlem: erken belge yükleme geçişinde yanlışlıkla `sample_data/README.md` dahil edilmiş; defter artık sadece iki hedeflenen örnek belgeyi açıkça yüklüyor.

## Depo Doğrulaması

- `scripts/verify_notebooks.py` yerel Markdown bağlantılarını, defter JSON’unu, defter çıktı temizliğini ve yüksek riskli gizli desenleri doğrular.
- `scripts/verify_notebooks.py --execute` depo kökünden genel defterleri çalıştırır.
- `drafts/` altındaki taslak materyal kasti şekilde atlanır.

## Sonraki Çalışmalar

- Aynı senaryonun Azure AI Search ve Azure OpenAI ile yeniden kurulması, gelecekteki bir seri olarak.
- Yerel ve Azure uygulamaları kararlı hale geldikçe alma ve cevap değerlendirmesi eklenmesi.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Feragatname**:
Bu belge, AI çeviri hizmeti [Co-op Translator](https://github.com/Azure/co-op-translator) kullanılarak çevrilmiştir. Doğruluk için çaba sarf etsek de, otomatik çevirilerin hata veya yanlışlık içerebileceğini lütfen unutmayınız. Orijinal belge, kendi dilinde yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilir. Bu çevirinin kullanımı sonucu ortaya çıkabilecek yanlış anlamalardan veya yanlış yorumlamalardan sorumlu değiliz.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->