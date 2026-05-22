# Ensine a IA a Responder a Perguntas com Base nos Seus Documentos
## Série 2: Construir um Sistema Local RAG Open-Source de Ponta a Ponta

![Local open-source RAG tutorial pipeline](../../../assets/images/series-2-local-rag.svg)

> Este artigo transforma a discussão sobre a arquitetura da Série 1 num tutorial local RAG executável. O objetivo é construir primeiro todo o fluxo de trabalho com dados de exemplo, sem conta na cloud e sem segredos, para depois usar essa base funcional para tomar melhores decisões arquitetónicas.

O sistema que vamos construir é um pequeno assistente de política escolar. Uso dois documentos locais em Markdown como base de conhecimento e depois percorro todo o pipeline RAG: fragmentação, embeddings locais, armazenamento vetorial Qdrant, recuperação, reranking, composição da resposta com consciência da fonte e geração local opcional com Ollama e Phi-4-mini.

Navegação da série: [Página principal do repositório](../README.md) | Anterior: [Série 1 - RAG, Azure vs Alternativas Open-Source, e Quando o Fine-Tuning Faz Sentido](./series-1-rag-azure-open-source-fine-tuning.md)

Notebook: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Requisitos: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> Este é o melhor ponto de partida se quiser compreender o pipeline RAG antes de criar recursos na cloud. O caminho por defeito corre localmente com embeddings amigáveis à CPU e sem segredos.

## 1. O que Estamos a Construir

No tutorial de 2023, comecei pela Azure porque o objetivo era mostrar como o Azure AI Search e o Azure OpenAI poderiam responder a perguntas a partir de documentos PDF.

Para esta série de 2026, quero começar um nível abaixo.

Antes de usar serviços geridos, quero construir localmente um pequeno sistema RAG e tornar cada passo visível: carregar documentos, fragmentar texto, armazenar vetores, recuperar evidências, reranquear resultados e devolver uma resposta com consciência da fonte.

O cenário de exemplo é um assistente de política escolar. O utilizador pergunta:

```text
Can I use generative AI for my final assignment?
```

O sistema não deve responder a partir da memória geral do modelo. Deve recuperar a secção relevante da política e responder com base nessa evidência.

A versão completa executável encontra-se em [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). O código abaixo mostra os passos principais para que o artigo possa ser lido como um tutorial.

## 2. Instalar as Dependências Locais

Crie um ambiente virtual e instale os requisitos da Série 2:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

A primeira versão usa o modo local Qdrant e FastEmbed. O cliente Python do Qdrant suporta um modo local em memória com `QdrantClient(":memory:")`, útil para tutoriais locais e verificação estilo CI. O FastEmbed fornece um modelo de embedding local real sem precisar de chave de API na cloud.

O ficheiro de requisitos inclui também `python-dotenv` porque o notebook pode opcionalmente ler um nome de modelo Ollama do `.env`. Nenhuma chave API do Azure OpenAI ou OpenAI é necessária para este tutorial local.

## 3. Carregar os Documentos de Exemplo

O corpus de exemplo é intencionalmente pequeno:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

No notebook, carrego todos os ficheiros Markdown de `sample_data/`:

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

Quando executei o notebook, carregou 2 documentos. Isso é pequeno o suficiente para inspeção manual, o que é útil ao construir a primeira versão de um pipeline RAG.

## 4. Fragmentar por Títulos Markdown

O próximo passo é dividir os documentos em fragmentos.

Para este tutorial, uso títulos Markdown como sinal estrutural. O título do documento vem de `#` e cada fragmento de secção vem de `##`.

> [!NOTE]
> A fragmentação não é uma solução universal. Neste tutorial uso títulos Markdown porque os documentos de exemplo têm uma estrutura clara com `#` e `##`. Para PDFs, documentos Word, slides, tickets ou páginas web, uma estratégia melhor pode usar limites de página, informação de layout, secções semânticas, limites de tokens, tabelas ou metadados. O importante é escolher uma estratégia de fragmentação que preserve o significado e a rastreabilidade da fonte nos seus documentos.

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

Depois aplico a cada documento:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

Isto criou 8 fragmentos na minha execução local.

O que gostei neste passo foi que os metadados já são úteis. Cada fragmento conhece a sua `source`, `sectionHeading`, `documentVersion` e o marcador `permissions`. Mesmo num pequeno tutorial, isto facilita o raciocínio sobre citações e posterior recuperação consciente das permissões.

## 5. Criar Embeddings Locais

Para a primeira versão pública, uso `BAAI/bge-small-en-v1.5` através do FastEmbed.

Isto mantém o tutorial local e amigável à CPU, mas ainda utiliza um modelo real de embeddings em vez de uma função vetorial marcador. Na primeira execução, descarrega os pesos do modelo. Depois disso, o notebook pode reutilizar a cache local.

> [!NOTE]
> Uso `BAAI/bge-small-en-v1.5` porque é um modelo leve de embedding para inglês que funciona bem com FastEmbed e Qdrant para um tutorial local. Cria vetores de 384 dimensões, mantendo o exemplo rápido e barato para correr localmente. Não é a única boa escolha. Em 2023, muitos tutoriais usavam modelos hospedados como `text-embedding-ada-002`. Hoje, opções hospedadas mais recentes como `text-embedding-3-small` e `text-embedding-3-large` da OpenAI, e opções open-source como BGE, E5, MiniLM, Nomic Embed e modelos multilíngues como `BAAI/bge-m3` são todas escolhas razoáveis conforme a carga de trabalho. Em produção, o modelo correto deve ser selecionado através de avaliação de recuperação nos seus próprios documentos.

Algumas alternativas práticas:

| Família do modelo | Quando consideraria |
| --- | --- |
| `text-embedding-ada-002` | Referência hospedada antiga encontrada em muitos tutoriais de 2023. Não a escolheria hoje como padrão para um tutorial novo. |
| `text-embedding-3-small` | Padrão hospedado moderno para equilíbrio forte de custo/desempenho e se não precisar de embeddings apenas locais. |
| `text-embedding-3-large` | Opção hospedada quando a qualidade da recuperação importa mais que tamanho do vetor ou custo do embedding. |
| `BAAI/bge-small-en-v1.5` | Referência local leve para inglês, ideal para tutoriais, protótipos e experiências CPU-friendly. |
| `BAAI/bge-base-en-v1.5` ou `BAAI/bge-large-en-v1.5` | Modelos locais maiores para inglês, para melhor qualidade de recuperação quando houver mais capacidade computacional. |
| `BAAI/bge-m3` | Recuperação multilíngue ou de contexto mais longo, especialmente quando os documentos não são apenas em inglês. |
| `sentence-transformers/all-MiniLM-L6-v2` | Referência de pesquisa semântica muito rápida e pequena. Útil quando a velocidade e simplicidade são essenciais. |
| `nomic-embed-text-v1.5` | Opção local open-source de embeddings que vale a pena testar para contextos mais longos ou setups focados em portabilidade. |

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

Depois cada fragmento obtém um embedding:

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

## 6. Armazenar Vetores no Modo Local Qdrant

Agora criamos uma coleção Qdrant em memória e inserimos os fragmentos com metadados no payload.

> [!NOTE]
> No tutorial de 2023 usei FAISS porque era uma forma simples e popular de demonstrar pesquisa vetorial local com LangChain. O FAISS é ainda útil para experiências rápidas locais. Nesta versão 2026 uso Qdrant porque quero que o tutorial se aproxime de um sistema RAG de produção. O Qdrant permite armazenar vetores juntamente com metadados como ficheiro fonte, título da secção, versão do documento e permissões. Isso torna a recuperação mais fácil de inspecionar e prepara o exemplo para filtragem, citações e futura implementação persistente ou baseada em servidor.

O FAISS é ótimo para mostrar pesquisa por similaridade vetorial. O Qdrant é melhor para mostrar uma camada extra de recuperação RAG pequena mas com formato de produção.

Algumas alternativas práticas:

| Armazenamento / camada de pesquisa vetorial | Quando consideraria |
| --- | --- |
| Qdrant | Protótipos locais, filtragem por metadados, pesquisa vetorial preparada para produção e fluxo de trabalho Python simples. |
| Chroma | Experiências rápidas locais RAG e notebooks onde a simplicidade é essencial. |
| FAISS | Pesquisa vetorial local leve quando só preciso de pesquisa por similaridade e posso gerir os metadados separadamente. |
| Milvus | Pesquisa vetorial open-source de maior escala quando a equipa estiver pronta para operar uma base de dados vetorial dedicada. |
| Weaviate | Pesquisa vetorial com esquema, metadados, pesquisa híbrida e opções de implementação gerida ou self-hosted. |
| Azure AI Search | RAG empresarial na Azure quando quiser pesquisa por palavras-chave, pesquisa vetorial, recuperação híbrida, ranqueamento semântico, filtragem, segurança e operações geridas numa camada de pesquisa única. |
| PostgreSQL + pgvector | Equipas que já usam PostgreSQL e querem pesquisa vetorial integrada perto dos dados da aplicação. |

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

Depois inserimos os pontos:

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

Na minha execução, a coleção inseriu 8 vetores.

Aqui o sistema RAG começa a ser inspecionável. A base vetorial não está só a armazenar vetores; está a armazenar o texto da evidência e os metadados necessários para citações.

## 7. Recuperar Fragmentos Candidatos

Agora fazemos a pergunta e recuperamos os fragmentos candidatos.

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

A esta altura, imprimo os fragmentos recuperados antes de gerar a resposta. Isto é importante. Se a recuperação falhar, a geração vai apenas esconder o problema com texto fluente.

## 8. Adicionar um Reranker Leve

Quando testei pela primeira vez o caminho de recuperação, a similaridade vetorial encontrou conteúdo de política relacionado, mas a secção mais precisa nem sempre estava no topo.

Por isso adicionei um pequeno reranker local. Dá peso extra quando termos da pergunta se sobrepõem ao título da secção e conteúdo.

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

Depois do reranking, o resultado principal passou a ser:

```text
school_ai_policy.md / Final Assignments
```

Essa foi a secção esperada para a pergunta de teste.

Esta foi a lição mais útil da primeira implementação. Mesmo num exemplo local pequeno, a qualidade da recuperação melhorou quando combinei similaridade vetorial com outro sinal.

## 9. Compor uma Resposta Local Fundamentada

Para o caminho por defeito, uso um compositor de respostas local transparente em vez de um LLM.

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

Isto não é para ser um gerador de respostas final. É uma ferramenta de debugging. Prova que a recuperação, metadados e ligação das citações funcionam antes de adicionar variabilidade do modelo.

## 10. Gerar uma Resposta Local com Ollama e Phi-4-mini

Quando a recuperação estiver a funcionar, o notebook pode substituir só o passo final da resposta por Ollama e `phi4-mini:3.8b`.

> [!NOTE]
> O Ollama deve substituir só o passo final de geração de resposta. Carregamento de documentos, fragmentação, armazenamento vetorial, recuperação, reranking e ligação das citações devem manter-se iguais.

Primeiro, o notebook constrói um prompt de evidência a partir dos fragmentos recuperados:

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

Para este tutorial, recomendo a família Phi-4-mini da Microsoft via Ollama como opção por defeito para geração local. No Ollama, o nome do modelo que testei é:

```powershell
ollama pull phi4-mini:3.8b
```

Pode rapidamente verificar que o modelo está disponível:

```powershell
ollama list
```

Depois defina estas variáveis:

```powershell
Copy-Item .env.example .env
```

Abra `.env` e descomente os valores Ollama da Série 2:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

O notebook carrega o `.env` da raiz do repositório com `python-dotenv` e envia o mesmo prompt de evidência para a endpoint local `/api/chat` do Ollama com streaming desativado. Se o Ollama não estiver a correr ou faltar `SERIES2_OLLAMA_MODEL`, esse caminho é ignorado.

> [!NOTE]
> Nesta máquina, `phi4-mini:3.8b` descarregou cerca de 2,49GB de ficheiros do modelo. Durante a inferência, o Ollama indicou um tamanho de modelo carregado de 3,3GB e usou a GPU RTX 3060 Laptop.

Isto cria dois níveis no tutorial:

1. Compositor de respostas determinístico apenas CPU.
2. Geração local de respostas com Ollama e Phi-4-mini.

O pipeline de recuperação mantém-se igual em ambos.

## 11. Resultado da Verificação

Executei o notebook localmente em Windows com Python 3.12.6.

Pacotes instalados:

| Pacote | Versão |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

Execução do notebook:

- Notebook: `notebooks/series-2-open-source-rag.ipynb`
- Resultado da execução: aprovado com `nbclient`
- Documentos carregados: 2
- Fragmentos criados: 8
- Coleção Qdrant: `school_policy_local`
- Vetores inseridos: 8
- Modelo de embedding: `BAAI/bge-small-en-v1.5`
- Tamanho do embedding: 384
```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

Eu não chamaria esta resposta de perfeita. Ela responde com base na evidência correta, mas a linha final da fonte é menos precisa do que o formato de citação determinístico. Isso é útil mostrar no tutorial porque torna óbvia a próxima questão de engenharia: a geração de respostas também precisa de avaliação, não apenas a recuperação.

O principal que aprendi ao verificar isto é que a qualidade da recuperação deve ser verificada antes da geração da resposta. O resultado do embedding já era útil, e o reranker leve fez com que a seção de política esperada aparecesse primeiro de forma fiável. Esse é exatamente o tipo de comportamento pequeno do sistema que quero que o tutorial exponha em vez de esconder.

## 12. O que Vem a Seguir

A próxima melhoria é comparar esta configuração local com uma versão gerida da Azure do mesmo cenário do assistente de política escolar. Manter o cenário fixo deve tornar as concessões mais fáceis de perceber: complexidade da configuração, controlos de recuperação, integração de identidade, propriedade operacional e custo.

## 13. Referências

- [Introdução rápida ao cliente Python Qdrant](https://python-client.qdrant.tech/quickstart.html)
- [Repositório GitHub do cliente Qdrant](https://github.com/qdrant/qdrant-client)
- [Modelos suportados pelo FastEmbed](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [Guia de embeddings OpenAI](https://platform.openai.com/docs/guides/embeddings)
- [Cartão do modelo BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [Cartão do modelo BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3)
- [Cartão do modelo sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Página do modelo Ollama phi4-mini](https://ollama.com/library/phi4-mini)
- [Documentação Ollama Windows](https://docs.ollama.com/windows)
- [Documentação API streaming Ollama](https://docs.ollama.com/api/streaming)
- [Cartão do modelo Microsoft Phi-4-mini-instruct](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [Visão geral LangGraph](https://docs.langchain.com/oss/python/langgraph)
- [Introdução ao RAG - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

Anterior: [Série 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas resultantes da utilização desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->