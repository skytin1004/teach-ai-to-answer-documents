# Gereksinimler

Her uygulama makalesinin odaklanmış bir gereksinimler dosyası vardır.

| Dosya | Kullanıldığı Yer |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | Serisi 2 açık kaynak RAG not defteri, isteğe bağlı Ollama oluşturma yardımcıları dahil |
| [all.txt](../../../requirements/all.txt) | Depo düzeyinde doğrulama ve CI |

Tek bir not defteri çalıştırırken odaklanmış dosyayı kullanın. Tüm depoyu doğrularken `all.txt` kullanın.

`open-source-rag.txt` ve `all.txt`, yerel embeddingler için `fastembed` ile Serisi 2'nin retrieval pipeline'ını değiştirmeden `.env` dosyasından isteğe bağlı olarak Ollama oluşturmayı etkinleştirebilmesi için `python-dotenv` içerir.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Feragatname**:
Bu belge, AI çeviri hizmeti [Co-op Translator](https://github.com/Azure/co-op-translator) kullanılarak çevrilmiştir. Doğruluk için çaba sarf etsek de, otomatik çevirilerin hata veya yanlışlık içerebileceğini lütfen unutmayınız. Orijinal belge, kendi dilinde yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilir. Bu çevirinin kullanımı sonucu ortaya çıkabilecek yanlış anlamalardan veya yanlış yorumlamalardan sorumlu değiliz.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->