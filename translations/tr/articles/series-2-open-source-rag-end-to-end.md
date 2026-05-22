# Yapay Zekaya Belgeleriniz Temelli Soruları Yanıtlamayı Öğretin
## Seri 2: Yerel Açık Kaynak RAG Sistemi Baştan Sona Kurulumu

![Yerel açık kaynak RAG öğretici iş akışı](../../../assets/images/series-2-local-rag.svg)

> Bu makale, Seri 1 mimari tartışmasını çalıştırılabilir bir yerel RAG öğreticisine dönüştürüyor. Hedef, önce örnek verilerle, bulut hesabı ve gizli bilgi olmadan tam iş akışını kurmak, ardından çalışan bu temel üzerinden daha iyi mimari kararlar almaktır.

Oluşturacağımız sistem küçük bir okul politika asistanıdır. İki yerel Markdown belgesini bilgi tabanı olarak kullanıyorum, ardından tam RAG iş akışını adım adım gösteriyorum: parçalara bölme, yerel gömme, Qdrant vektör deposu, getirme, yeniden sıralama, kaynağı fark eden cevap oluşturma ve isteğe bağlı olarak Ollama ve Phi-4-mini ile yerel üretim.

Seri navigasyonu: [Depo ana sayfa](../README.md) | Önceki: [Seri 1 - RAG, Azure ve Açık Kaynak Alternatifleri, ve Ne Zaman İnce Ayar Yapmak Mantıklı](./series-1-rag-azure-open-source-fine-tuning.md)

Defter: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Gereksinimler: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> Bulut kaynakları oluşturmadan önce RAG iş akışını anlamak isteyenler için en iyi başlangıç noktası budur. Varsayılan yol CPU-dostu gömmelerle ve gizli bilgi olmadan yerel çalışır.

## 1. İnşa Ettiklerimiz

2023 öğreticisinde Azure’dan başladım çünkü hedef PDF belgelerden soru yanıtlamak için Azure AI Search ve Azure OpenAI’nın nasıl kullanılacağını göstermekti.

2026 serisi için bir katman daha altından başlamak istiyorum.

Yönetilen hizmetleri kullanmadan önce, küçük bir RAG sistemini yerel olarak inşa etmek ve her adımı görünür yapmak istiyorum: belgeleri yükleme, metni parçalara ayırma, vektörleri depolama, delilleri getirme, sonuçları yeniden sıralama ve kaynak odaklı yanıt döndürme.

Örnek senaryo küçük bir okul politika asistanıdır. Kullanıcı sorar:

```text
Can I use generative AI for my final assignment?
```

Sistem genel model hafızasından yanıt vermemelidir. İlgili politika bölümünü getirmeli ve yanıtı o delilden üretmelidir.

Tam çalıştırılabilir versiyon [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) dosyasında. Aşağıdaki kod ana adımları gösteriyor, böylece makale öğretici olarak okunabilir.

## 2. Yerel Bağımlılıkları Kurun

Bir sanal ortam oluşturun ve Seri 2 gereksinimlerini yükleyin:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

İlk versiyon Qdrant yerel modu ve FastEmbed kullanıyor. Qdrant Python istemcisi, `QdrantClient(":memory:")` ile bellek içi yerel modu destekler, bu yerel öğreticiler ve CI tarzı doğrulama için çok kullanışlıdır. FastEmbed bizim gerçek yerel bir gömme modeli kullanmamızı sağlar, bulut API anahtarı gerektirmez.

Gereksinimler dosyasında ayrıca `python-dotenv` bulunur çünkü defter isteğe bağlı olarak `.env` dosyasından bir Ollama model adı okuyabilir. Bu yerel öğretici için Azure OpenAI veya OpenAI API anahtarı gerekli değildir.

## 3. Örnek Belgeleri Yükleyin

Örnek metin kasıtlı olarak küçüktür:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

Defterde `sample_data/` içindeki tüm Markdown dosyalarını yüklüyorum:

```python
from pathlib import Path

repo_root = Path.cwd()
if not (repo_root / "sample_data").exists():
    repo_root = Path.cwd().parent

sample_dir = repo_root / "sample_data"
sample_files = ["course_ai_guidance.md", "school_ai_policy.md"]
documents = []

for file_name in sample_files:
    path = sample_dir / file_name
    documents.append({
        "source": path.name,
        "text": path.read_text(encoding="utf-8"),
    })

print(f"Loaded {len(documents)} documents")
```

Defteri çalıştırdığımda 2 belge yüklendi. Bu, elle incelemek için yeterince küçüktür ve RAG iş akışının ilk versiyonunu oluştururken faydalıdır.

## 4. Markdown Başlıklarına Göre Parçalara Ayırın

Sonraki adım belgeleri parçalara bölmektir.

Bu öğretici için yapısal sinyal olarak Markdown başlıklarını kullanıyorum. Belge başlığı `#` den gelir, her bölüm parçası `##` ile gelir.

> [!NOTE]
> Parçalama herkese uyan tek yöntem değildir. Bu öğreticide örnek belgelerde açık `#` ve `##` yapısı olduğu için Markdown başlıklarını kullanıyorum. PDF, Word belgeleri, slaytlar, destek talepleri veya web sayfaları için daha iyi strateji sayfa sınırları, düzen bilgisi, anlamsal bölümler, token sınırları, tablolar veya meta veriler kullanmak olabilir. Önemli olan belgenizin anlamını ve kaynak takibini koruyacak bir parçalama stratejisi seçmektir.

```python
def chunk_markdown(document):
    title = None
    current_heading = None
    current_lines = []
    chunks = []

    def flush():
        if current_heading and current_lines:
            content = "\n".join(current_lines).strip()
            if content:
                chunks.append({
                    "id": f"{document['source']}::{len(chunks)}",
                    "source": document["source"],
                    "title": title or document["source"],
                    "sectionHeading": current_heading,
                    "content": content,
                    "documentVersion": "local-sample-v1",
                    "permissions": ["students", "instructors"],
                })

    for raw_line in document["text"].splitlines():
        line = raw_line.strip()
        if line.startswith("# "):
            title = line[2:].strip()
        elif line.startswith("## "):
            flush()
            current_heading = line[3:].strip()
            current_lines = []
        elif line:
            current_lines.append(line)

    flush()
    return chunks
```

Sonra bunu her belgeye uygularım:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

Yerel çalıştırmamda 8 parça oluştu.

Bu adımda hoşuma giden şey, meta verilerin zaten faydalı olmasıydı. Her parça `source`, `sectionHeading`, `documentVersion` ve örnek `permissions` bilgisine sahiptir. Küçük bir öğreticide bile bu, alıntılar ve izin tabanlı getirmeyi düşünmeyi kolaylaştırır.

## 5. Yerel Gömme Oluşturma

İlk herkese açık versiyon için FastEmbed üzerinden `BAAI/bge-small-en-v1.5` modelini kullanıyorum.

Bu öğreticiyi yerel ve CPU dostu tutar, aynı zamanda gerçek bir gömme modeli kullanır placeholder vektör fonksiyonu değil. İlk çalıştırmada model ağırlıkları indirilir. Sonrasında defter yerel önbelleği kullanabilir.

> [!NOTE]
> `BAAI/bge-small-en-v1.5` kullanıyorum çünkü FastEmbed ve Qdrant ile iyi çalışan hafif bir İngilizce gömme modeli ve yerel öğretici için uygundur. 384 boyutlu vektörler oluşturur, örneği hızlı ve ekonomik çalıştırır. Bu tek iyi seçenek değil. 2023’te birçok öğretici `text-embedding-ada-002` gibi barındırılan gömme modellerini tercih etti. Günümüzde ise OpenAI `text-embedding-3-small` ve `text-embedding-3-large` gibi daha yeni barındırılan seçenekler ile BGE, E5, MiniLM, Nomic Embed gibi açık kaynak ve `BAAI/bge-m3` gibi çok dilli modeller iş yüküne göre makul tercihlerdir. Üretimde en uygun gömme modeli, kendi belgeleriniz üzerinde getirme değerlendirmesiyle seçilmelidir.

Bazı pratik alternatifler:

| Model ailesi | Ne zaman düşünürüm |
| --- | --- |
| `text-embedding-ada-002` | 2023 çağındaki öğreticilerde çok kullanılan eski barındırılan temel model. Bugün yeni öğreticilerde varsayılan yapmazdım. |
| `text-embedding-3-small` | Güçlü maliyet/performans dengesi istediğimde ve sadece yerel gömme gerekmiyorsa modern barındırılan varsayılan. |
| `text-embedding-3-large` | Vektör boyutu veya gömme maliyetinden ziyade getirme kalitesi önemliyse barındırılan seçenek. |
| `BAAI/bge-small-en-v1.5` | Öğreticiler, prototipler ve CPU dostu deneyler için hafif yerel İngilizce temel. |
| `BAAI/bge-base-en-v1.5` veya `BAAI/bge-large-en-v1.5` | Daha iyi getirme kalitesi istediğimde ve daha fazla işlem gücü ayırabileceğim yerel İngilizce modeller. |
| `BAAI/bge-m3` | Çok dilli veya uzun bağlamlı getirmede, özellikle belgeler sadece İngilizce olmadığında. |
| `sentence-transformers/all-MiniLM-L6-v2` | Çok küçük ve hızlı anlamsal arama temeli. Hız ve basitlik en önemli olduğunda kullanışlı. |
| `nomic-embed-text-v1.5` | Daha uzun bağlam veya taşınabilirlik odaklı kurulumlarda denenebilir açık yerel gömme seçeneği. |

```python
import re
from fastembed import TextEmbedding

EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"
embedding_model = TextEmbedding(model_name=EMBEDDING_MODEL_NAME)

def tokenize(text):
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    expanded = []
    for token in tokens:
        expanded.append(token)
        if token.endswith("s") and len(token) > 3:
            expanded.append(token[:-1])
    return expanded
```

Sonra her parçaya gömme atanır:

```python
texts_to_embed = [
    f"{chunk['title']} {chunk['sectionHeading']} {chunk['content']}"
    for chunk in chunks
]
chunk_vectors = list(embedding_model.embed(texts_to_embed))
VECTOR_SIZE = len(chunk_vectors[0])

for chunk, vector in zip(chunks, chunk_vectors):
    chunk["vector"] = vector
```

## 6. Vektörleri Qdrant Yerel Modunda Depolayın

Şimdi bellek içi Qdrant koleksiyonu oluşturup parçaları yükleyeceğiz, taşıyıcı meta verilerle birlikte.

> [!NOTE]
> 2023 öğreticisinde LangChain ile yerel vektör benzerliği araması göstermek için FAISS kullandım çünkü basit ve popülerdi. FAISS hızlı yerel deneyler için hala kullanışlı. Bu 2026 versiyonunda Qdrant kullanmamın sebebi, öğreticinin üretime daha yakın hissettirmesini istememdir. Qdrant, kaynak dosya, bölüm başlığı, belge versiyonu ve izinler gibi meta verilerle birlikte vektörleri depolamamı sağlar. Bu, getirmenin incelenmesini kolaylaştırır ve filtreleme, alıntılar ile ileriye dönük kalıcı veya sunucu tabanlı dağıtım için örneği hazırlar.

FAISS, vektör benzerliği aramasını göstermek için harikadır. Qdrant, küçük ama üretim şekilli bir RAG getirme katmanı göstermede daha iyidir.

Bazı pratik alternatifler:

| Vektör deposu / arama katmanı | Ne zaman düşünüyorum |
| --- | --- |
| Qdrant | Yerel prototipler, meta veri filtreleme, üretime uygun vektör araması ve basit Python iş akışı için. |
| Chroma | Basitlik en önemli olduğunda hızlı yerel RAG deneyleri ve defterler için. |
| FAISS | Yalnızca benzerlik araması gerektiğinde ve meta veriyi ayrı yönetebileceğim hafif yerel vektör araması için. |
| Milvus | Takım hazırsa büyük ölçekli açık kaynak vektör araması için. |
| Weaviate | Şema, meta veri, hibrit arama ve yönetilen veya kendi barındırdığı dağıtım seçenekleriyle vektör araması. |
| Azure AI Search | Anahtar kelime araması, vektör araması, hibrit getirme, anlamsal sıralama, filtreleme, güvenlik ve yönetilen operasyonları tek arama katmanında istediğimde Azure’da kurumsal RAG. |
| PostgreSQL + pgvector | PostgreSQL kullanan ekiplere, uygulama verisine yakın vektör araması için. |

```python
from qdrant_client import QdrantClient, models

collection_name = "school_policy_local"
client = QdrantClient(":memory:")

client.create_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(
        size=VECTOR_SIZE,
        distance=models.Distance.COSINE,
    ),
)
```

Sonra noktalar insert edilir:

```python
points = []

for idx, chunk in enumerate(chunks):
    payload = {
        key: chunk[key]
        for key in [
            "source",
            "title",
            "sectionHeading",
            "content",
            "documentVersion",
            "permissions",
        ]
    }
    points.append(
        models.PointStruct(
            id=idx,
            vector=chunk["vector"].tolist(),
            payload=payload,
        )
    )

client.upsert(collection_name=collection_name, points=points)
```

Benim çalıştırmamda koleksiyon 8 vektör yükledi.

Burada RAG sistemi denetlenebilir hale gelir. Vektör veri tabanı sadece vektör depolamaz; alıntılar için gereken delil metni ve meta veriyi de depolar.

## 7. Aday Parçaları Getirin

Şimdi soruyu sorar ve aday parçaları getiririz.

```python
question = "Can I use generative AI for my final assignment?"
query_vector = list(embedding_model.embed([question]))[0].tolist()

raw_results = client.query_points(
    collection_name=collection_name,
    query=query_vector,
    limit=5,
    with_payload=True,
).points
```

Bu noktada yanıt üretmeden önce getirilen parçaları yazdırıyorum. Bu önemli çünkü eğer getirme yanlışsa, üretim sadece sorunları akıcı metinle gizler.

## 8. Hafif Bir Yeniden Sıralayıcı Ekleyin

İlk testte, vektör benzerliği ilgili politika içeriğini buldu ama en doğru bölüm her zaman en üstte değildi.

Bu yüzden küçük yerel bir yeniden sıralayıcı ekledim. Bölüm başlığı ve içerikle soru terimleri örtüştüğünde ekstra ağırlık verir.

```python
query_terms = set(tokenize(question))

def rerank_score(result):
    payload = result.payload
    heading_terms = set(tokenize(payload["sectionHeading"]))
    content_terms = set(tokenize(payload["content"]))
    heading_overlap = len(query_terms & heading_terms)
    content_overlap = len(query_terms & content_terms)
    return result.score + (0.12 * heading_overlap) + (0.02 * content_overlap)

results = sorted(raw_results, key=rerank_score, reverse=True)[:3]
```

Yeniden sıralamadan sonra en üst sonuç:

```text
school_ai_policy.md / Final Assignments
```

Test sorusu için beklenen bölümdü.

Bu ilk uygulamadan en faydalı ders oldu. Çok küçük yerel örnekte bile, vektör benzerliğini başka bir sinyalle birleştirdiğimde getirme kalitesi iyileşti.

## 9. Dayanıklı Yerel Yanıt Oluşturma

Varsayılan yol için şeffaf bir yerel cevap oluşturucu kullanıyorum, LLM değil.

```python
top = results[0].payload

answer = (
    "Based on the retrieved policy section, students may use generative AI for "
    "brainstorming, outlining, grammar feedback, and code explanation when the "
    "instructor allows it. They should not submit AI-generated work as their own, "
    "and they should include a disclosure when AI tools are used."
)

print("Answer:")
print(answer)
print("\nSource:")
print(f"{top['source']} / {top['sectionHeading']}")
```

Bu nihai ürün yanıt üreticisi değil. Bir hata ayıklama aracıdır. Model değişkenliğinden önce getirme, meta veri ve alıntı bağlama işleyişini kanıtlar.

## 10. Ollama ve Phi-4-mini ile Yerel Yanıt Üretin

Getirme çalışınca defter yalnızca son yanıt aşamasını Ollama ve `phi4-mini:3.8b` ile değiştirebilir.

> [!NOTE]
> Ollama yalnızca son yanıt üretme aşamasını değiştirmelidir. Belge yükleme, parçalara ayırma, vektör depolama, getirme, yeniden sıralama ve alıntı bağlantıları aynı kalmalıdır.

Önce defter getirilen parçalardan bir delil istemi oluşturur:

```python
def build_evidence(retrieved_results):
    evidence_blocks = []
    for idx, result in enumerate(retrieved_results, start=1):
        payload = result.payload
        evidence_blocks.append(
            f"[{idx}] Source: {payload['source']} / {payload['sectionHeading']}\n"
            f"{payload['content']}"
        )
    return "\n\n".join(evidence_blocks)

evidence = build_evidence(results)
answer_prompt = (
    "Answer the question using only the evidence below. "
    "If the evidence is insufficient, say that the provided documents do not contain enough information. "
    "End with a Sources line that lists the source file and section.\n\n"
    f"Question: {question}\n\nEvidence:\n{evidence}"
)
```

Bu öğretici için varsayılan yerel üretim seçeneği olarak Microsoft’un Phi-4-mini ailesini Ollama üzerinden öneriyorum. Ollama’da denediğim model adı:

```powershell
ollama pull phi4-mini:3.8b
```

Modelin kullanılabilir olup olmadığını hızlıca kontrol edebilirsiniz:

```powershell
ollama list
```

Sonra bu değişkenleri ayarlayın:

```powershell
Copy-Item .env.example .env
```

`.env` dosyasını açın ve Seri 2 Ollama değerlerinin yorumlarını kaldırın:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

Defter, `python-dotenv` ile depo kökünden `.env` dosyasını yükler, sonra aynı delil istemini Ollama’nın yerel `/api/chat` uç noktasına akışsız olarak gönderir. Ollama çalışmıyorsa veya `SERIES2_OLLAMA_MODEL` eksikse bu aşama atlanır.

> [!NOTE]
> Bu bilgisayarda `phi4-mini:3.8b` yaklaşık 2.49GB model dosyası indirdi. Çıkarım sırasında Ollama 3.3GB yüklü model boyutunu bildirdi ve RTX 3060 Laptop GPU kullandı.

Bu öğreticiye iki seviye kazandırır:

1. Yalnızca CPU ile kararlı yanıt oluşturucu.
2. Ollama ve Phi-4-mini ile yerel yanıt üretimi.

Getirme boru hattı her iki durumda da aynıdır.

## 11. Doğrulama Sonucu

Defteri Windows’ta Python 3.12.6 ile yerelde çalıştırdım.

Yüklü paketler:

| Paket | Versiyon |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Defter çalıştırması:

- Defter: `notebooks/series-2-open-source-rag.ipynb`
- Çalıştırma sonucu: `nbclient` ile geçti
- Yüklenen belge: 2
- Oluşturulan parça: 8
- Qdrant koleksiyonu: `school_policy_local`
- Eklenen vektörler: 8
- Gömme modeli: `BAAI/bge-small-en-v1.5`
- Gömme boyutu: 384
- Getirme sorusu: "Son ödevim için üretken yapay zekayı kullanabilir miyim?"
- Yeniden sıralama yöntemi: hafif yerel leksikal yeniden sıralama
- Yeniden sıralamadan sonra en iyi getirilen kaynak: `school_ai_policy.md`
- Yeniden sıralamadan sonra en iyi getirilen bölüm: `Final Assignments`
- Varsayılan cevap yolu: yerel şeffaf cevap bileştirici
- Ollama üretim yolu: `phi4-mini:3.8b` ile tamamlandı
- Ollama model dosya boyutu: diskte 2.49GB
- Ollama yüklenen model boyutu: `ollama ps` ile bildirilen 3.3GB
- GPU devre dışı bırakma: `ollama ps` ile bildirilen %100 GPU
- Üretim sonrası gözlemlenen GPU belleği: RTX 3060 Laptop GPU'da 6GB'ın yaklaşık 3.5GB kullanıldı
- Önbellekli FastEmbed modeli ve Ollama üretimi etkinleştirilmiş dizüstü bilgisayar çalıştırması: doğrulama betiğiyle yaklaşık 34 saniyede geçti

Ollama tarafından oluşturulan cevap:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

Bu cevabı mükemmel olarak adlandırmazdım. Doğru kanıttan yanıt veriyor, ancak son kaynak satırı deterministik atıf formatından daha az kesin. Bu, cevabı oluşturma ile sadece getirmenin değil, değerlendirme ihtiyacını da ortaya koyduğundan eğitimde göstermek için faydalı.

Doğrulama sırasında öğrendiğim en önemli şey, cevap üretiminden önce getirme kalitesinin kontrol edilmesi gerektiğiydi. Gömülü sonuç zaten faydalıydı ve hafif yeniden sıralayıcı beklenen politika bölümünü güvenilir şekilde ilk sırada gösterdi. Tam da eğitimin ortaya çıkarmak istediği, küçük sistem davranışlarından biridir; gizlemek yerine.

## 12. Sırada Ne Var

Bir sonraki geliştirme, aynı okul politika asistanı senaryosunun yönetilen Azure versiyonuyla bu yerel kurulumu karşılaştırmaktır. Senaryoyu sabit tutmak, takasları daha kolay görmeyi sağlar: kurulum karmaşıklığı, getirme kontrolleri, kimlik entegrasyonu, operasyonel sahiplik ve maliyet.

## 13. Kaynaklar

- [Qdrant Python istemci hızlı başlangıç](https://python-client.qdrant.tech/quickstart.html)
- [Qdrant istemci GitHub deposu](https://github.com/qdrant/qdrant-client)
- [FastEmbed desteklenen modeller](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [OpenAI gömme rehberi](https://platform.openai.com/docs/guides/embeddings)
- [BAAI/bge-small-en-v1.5 model kartı](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [BAAI/bge-m3 model kartı](https://huggingface.co/BAAI/bge-m3)
- [sentence-transformers/all-MiniLM-L6-v2 model kartı](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Ollama phi4-mini model sayfası](https://ollama.com/library/phi4-mini)
- [Ollama Windows dokümantasyonu](https://docs.ollama.com/windows)
- [Ollama API yayını dokümantasyonu](https://docs.ollama.com/api/streaming)
- [Microsoft Phi-4-mini-instruct model kartı](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [LangGraph genel bakış](https://docs.langchain.com/oss/python/langgraph)
- [RAG’e Giriş - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

Önceki: [Seri 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Feragatname**:
Bu belge, AI çeviri hizmeti [Co-op Translator](https://github.com/Azure/co-op-translator) kullanılarak çevrilmiştir. Doğruluk için çaba sarf etsek de, otomatik çevirilerin hata veya yanlışlık içerebileceğini lütfen unutmayınız. Orijinal belge, kendi dilinde yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilir. Bu çevirinin kullanımı sonucu ortaya çıkabilecek yanlış anlamalardan veya yanlış yorumlamalardan sorumlu değiliz.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->