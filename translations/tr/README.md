# Belgeleriniz Bazında Soruları Yanıtlamayı Öğreten Yapay Zeka

![Belge-tabancı AI RAG sistemi genel bakışı](../../assets/images/readme-hero.svg)

Bu depo, RAG, Azure AI hizmetleri, açık kaynak alternatifleri ve değerlendirme odaklı iş akışları ile belge-tabancı yapay zeka sistemleri oluşturma hakkında 2026 blog serisini toplar.

## Arka Plan

2023 yılında, Azure AI Search ve Azure OpenAI kullanarak PDF belgelerinden soruları yanıtlamayı ChatGPT'ye öğretme üzerine bir çift eğitim üzerinde çalıştım. "Verilerinizde ChatGPT" fikri o zamanlar hâlâ yeniydi ve amaç pratik bir iş akışını göstermekti: belgeleri saklamak, dizinlemek, ilgili içeriği almak ve alınan bağlamdan yanıtlar üretmek.

2026'da RAG ekosistemi çok daha büyük. Azure AI Search modern vektör ve hibrit alma desenlerini destekliyor, Azure OpenAI Microsoft Foundry Models ekosisteminin bir parçası ve LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama ve vLLM gibi açık kaynak araçlar gerçek sistemler için pratik seçenekler haline geldi.

Bu yüzden bu konuyu tekrar ele almak istedim. Soru artık sadece "RAG nasıl kurarım?" değil. Artık birçok şekilde inşa etmek mümkün ve daha önemli soru "Durumuma en uygun mimari hangisi?"

Bu seri o karar alma katmanından başlıyor, sonra bunu uygulamalı eğitimlere dönüştürüyor. İlk uygulama yolu, herkesin örnek verilerle, Qdrant, Ollama ve Phi-4-mini kullanarak çalıştırabileceği yerel bir açık kaynak RAG sistemi inşa etmeyi içeriyor.

## Makaleler

Makale dizini için [articles/README.md](./articles/README.md)'ye bakın.

1. [Seri 1: RAG, Azure vs Açık Kaynak Alternatifleri ve İnce Ayarın Anlamlı Olduğu Zaman](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [Seri 2: Yerel Açık Kaynak RAG Sistemini Baştan Sona İnşa Et](./articles/series-2-open-source-rag-end-to-end.md)

Sırada geliyor:

- Aynı RAG sistemini Azure AI Search ve Azure OpenAI ile yeniden inşa et.
- Demo yanıtın ötesinde değerlendirme ve regresyon kontrolleri ekle.

## Defterler

Uygulama makaleleri, alma ve değerlendirme adımlarının doğrudan incelenebilmesi için defterler (notebook) kullanır. Klasör düzeyinde kılavuz için [notebooks/README.md](./notebooks/README.md)'ye bakın.

> [!TIP]
> En hızlı yol isterseniz Seri 2 ile başlayın. Örnek veriler, CPU dostu gömme (embedding), Qdrant yerel modu ve bulut kimlik bilgisi olmadan yerel çalışır.

| Seri | Defter | Gereksinimler | Yerel doğrulama |
| --- | --- | --- | --- |
| Seri 2 | [Açık kaynak RAG defteri](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Qdrant yerel modu, alma, yeniden sıralama ve kaynak bağlantısı doğrulandı |

Bir defteri yerel çalıştırmak için bir sanal ortam oluşturup eşleşen gereksinimler dosyasını yükleyin. Örneğin:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## Örnek Veri

Defterler, örneklerin özel belgeler veya bulut kimlik bilgisi olmadan çalışabilmesi için [sample_data](../../sample_data) içinde küçük yerel bir korpus kullanır. Detaylar için [sample_data/README.md](./sample_data/README.md)'ye bakın.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## Yerel Doğrulama Özeti

Doğrulama sonuçları her makalede ve [SERIES_PLAN.md](./SERIES_PLAN.md)'de kaydedilmiştir.

| Alan | Sonuç |
| --- | --- |
| Seri 2 açık kaynak yolu | FastEmbed 384 boyutlu yerel gömme oluşturdu, Qdrant bellekte koleksiyona 8 vektör ekledi, hafif yeniden sıralama beklenen bölümü getirdi; isteğe bağlı Ollama üretimi `phi4-mini:3.8b` ile tamamlandı |

Yerel defter bilerek gizli bilgileri sert kodlamadan kaçınır.

## Yerel Ollama Üretimi

Seri 2 defteri varsayılan olarak yerel güvenlidir. Yerel Ollama üretimini etkinleştirmek için [.env.example](../../.env.example) dosyasını `.env` olarak kopyalayın ve Seri 2 değerlerini doldurun.

Seri 2 Ollama üretimi için yorum satırını kaldırın:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Seri 2 defteri `python-dotenv` kullanarak `.env` dosyasını depo kökünden otomatik yükler.

> [!IMPORTANT]
> `.env` dosyalarını, API anahtarlarını, özel uç noktaları veya kiracıya özel değerleri asla göndermeyin. Depo gizli bilgileri Markdown dosyalarından ve defterlerden bilinçli olarak dışarıda tutar.

Gereksinim dosyaları [requirements/README.md](./requirements/README.md)'de belgelenmiştir.

Bağlantıları, defter yapısını, defter çıktı temizliğini ve yüksek riskli gizli desenleri doğrulamak için:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

Doğrulama betikleri [scripts/README.md](./scripts/README.md)'de belgelenmiştir.

Tüm yerel güvenli defterleri aynı ortamda çalıştırmak için:

```powershell
python scripts\verify_notebooks.py --execute
```

Aynı doğrulama akışı GitHub Actions'ta push, çekme istekleri ve manuel iş akışı dispatch'larında çalışır. Taslak makaleler ve defterler bilinçli olarak herkese açık doğrulama yolundan hariç tutulmuştur.

Güncellemeleri yayımlamadan önce [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md)'i kullanın.

Mevcut yayımlanmamış değişiklik özeti için [CHANGELOG.md](./CHANGELOG.md)'ye bakın.

Katkı ve defter hijyeni yönergeleri için [CONTRIBUTING.md](./CONTRIBUTING.md)'ye bakın.

## Çok Dilli Destek

### Co-op Çevirmeni ile Desteklenir (Otomatik ve Her Zaman Güncel)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arapça](../ar/README.md) | [Bengalce](../bn/README.md) | [Bulgarca](../bg/README.md) | [Burma (Myanmar)](../my/README.md) | [Çince (Basitleştirilmiş)](../zh-CN/README.md) | [Çince (Geleneksel, Hong Kong)](../zh-HK/README.md) | [Çince (Geleneksel, Macau)](../zh-MO/README.md) | [Çince (Geleneksel, Tayvan)](../zh-TW/README.md) | [Hırvatça](../hr/README.md) | [Çekçe](../cs/README.md) | [Danca](../da/README.md) | [Flemenkçe](../nl/README.md) | [Estonca](../et/README.md) | [Fince](../fi/README.md) | [Fransızca](../fr/README.md) | [Almanca](../de/README.md) | [Yunanca](../el/README.md) | [İbranice](../he/README.md) | [Hintçe](../hi/README.md) | [Macarca](../hu/README.md) | [Endonezce](../id/README.md) | [İtalyanca](../it/README.md) | [Japonca](../ja/README.md) | [Kannada](../kn/README.md) | [Kmerce](../km/README.md) | [Korece](../ko/README.md) | [Litvanca](../lt/README.md) | [Malayca](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepalce](../ne/README.md) | [Nijerya Pidgin](../pcm/README.md) | [Norveççe](../no/README.md) | [Farsça (Persian)](../fa/README.md) | [Lehçe](../pl/README.md) | [Portekizce (Brezilya)](../pt-BR/README.md) | [Portekizce (Portekiz)](../pt-PT/README.md) | [Pencapça (Gurmukhi)](../pa/README.md) | [Romence](../ro/README.md) | [Rusça](../ru/README.md) | [Sırpça (Kiril)](../sr/README.md) | [Slovakça](../sk/README.md) | [Slovence](../sl/README.md) | [İspanyolca](../es/README.md) | [Svahili](../sw/README.md) | [İsveççe](../sv/README.md) | [Tagalog (Filipince)](../tl/README.md) | [Tamilce](../ta/README.md) | [Telugu](../te/README.md) | [Tayca](../th/README.md) | [Türkçe](./README.md) | [Ukraynaca](../uk/README.md) | [Urduca](../ur/README.md) | [Vietnamca](../vi/README.md)

> **Yerel Klonlamayı mı Tercih Ediyorsunuz?**
>
> Bu depo 50’den fazla dil çevirisi içermektedir ve bu indirmenin boyutunu önemli ölçüde artırır. Çeviriler olmadan klonlamak için seyrek kontrol kullanın:
>
> **Bash / macOS / Linux:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (Windows):**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> Bu, kursu tamamlamak için ihtiyacınız olan her şeyi çok daha hızlı indirme ile sağlar.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Feragatname**:
Bu belge, AI çeviri hizmeti [Co-op Translator](https://github.com/Azure/co-op-translator) kullanılarak çevrilmiştir. Doğruluk için çaba sarf etsek de, otomatik çevirilerin hata veya yanlışlık içerebileceğini lütfen unutmayınız. Orijinal belge, kendi dilinde yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilir. Bu çevirinin kullanımı sonucu ortaya çıkabilecek yanlış anlamalardan veya yanlış yorumlamalardan sorumlu değiliz.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->