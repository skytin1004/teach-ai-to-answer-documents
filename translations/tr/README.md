# Belgelerinize Dayalı Sorulara Cevap Vermeyi Yapay Zekaya Öğretin

Bu depo, RAG, Azure AI servisleri, açık kaynak alternatifleri ve değerlendirmeye yönelik iş akışları ile belge tabanlı yapay zeka sistemleri kurmaya dair 2026 blog dizisini toplar.

## Arka Plan

2023 yılında, Azure AI Search ve Azure OpenAI kullanarak PDF belgelerinden sorulara cevap vermeyi ChatGPT'ye öğretmeye yönelik iki eğitim üzerinde çalıştım. "Verilerinizde ChatGPT" fikri o zamanlar hâlâ yeniydi ve amaç pratik bir iş akışını göstermekti: belgeleri depolamak, dizinlemek, ilgili içeriği getirmek ve getirilen bağlamdan cevaplar üretmek.

2026 yılında RAG ekosistemi çok daha büyük. Azure AI Search, modern vektör ve hibrit getirme modellerini destekliyor, Azure OpenAI Microsoft Foundry Modelleri ekosisteminin bir parçası ve LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama ve vLLM gibi açık kaynak araçlar gerçek sistemler için pratik seçenekler haline geldi.

Bu yüzden bu konuya tekrar dönmek istedim. Artık soru sadece "RAG nasıl kurarım?" değil. RAG kurmanın birçok yolu var ve daha önemli soru "Durumuma hangi mimari uygun?" oldu.

Bu seri, o karar verme katmanından başlıyor. Uygulamaya derinlemesine girmeden önce yapay zeka servislerinin neden getirmeye ihtiyaç duyduğunu, Azure tabanlı yönetilen servislerin ne zaman mantıklı olduğunu, açık kaynak alternatiflerinin ne zaman daha uygun olduğunu ve ince ayarın nereye uyduğunu inceliyor.

## Makaleler

1. [Seri 1: RAG, Azure ve Açık Kaynak Alternatifleri ile İnce Ayarın Anlamı](./series-1-rag-azure-open-source-fine-tuning.md)

## Çok Dilli Destek

### Co-op Translator ile Desteklenmektedir (Otomatik ve Her Zaman Güncel)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](./README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **Yerel Olarak Klonlamayı mı Tercih Ediyorsunuz?**
>
> Bu depo 50+ dil çevirisi içerir ve bu da indirme boyutunu önemli ölçüde artırır. Çeviriler olmadan klonlamak için seyrek kontrol (sparse checkout) kullanabilirsiniz:
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
> Bu, kursu tamamlamak için ihtiyacınız olan her şeyi çok daha hızlı indirmenizi sağlar.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Feragatname**:
Bu belge, AI çeviri hizmeti [Co-op Translator](https://github.com/Azure/co-op-translator) kullanılarak çevrilmiştir. Doğruluk için çaba sarf etsek de, otomatik çevirilerin hata veya yanlışlık içerebileceğini lütfen unutmayınız. Orijinal belge, kendi dilinde yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilir. Bu çevirinin kullanımı sonucu ortaya çıkabilecek yanlış anlamalardan veya yanlış yorumlamalardan sorumlu değiliz.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->