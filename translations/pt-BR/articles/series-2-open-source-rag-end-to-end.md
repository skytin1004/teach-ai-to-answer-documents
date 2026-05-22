# Ensine a IA a Responder Perguntas com Base nos Seus Documentos
## Série 2: Construa um Sistema Local RAG de Código Aberto de Ponta a Ponta

![Pipeline tutorial RAG local de código aberto](../../../assets/images/series-2-local-rag.svg)

> Este artigo transforma a discussão da arquitetura da Série 1 em um tutorial RAG local executável. O objetivo é construir primeiro todo o fluxo de trabalho com dados de amostra, sem conta na nuvem e sem segredos, para depois usar essa base funcional para tomar decisões melhores de arquitetura.

O sistema que construiremos é um assistente de políticas escolares pequeno. Eu uso dois documentos Markdown locais como base de conhecimento e depois passo por todo o pipeline RAG: chunking, embeddings locais, armazenamento vetorial Qdrant, recuperação, reranking, composição de resposta consciente da fonte e geração local opcional com Ollama e Phi-4-mini.

Navegação da série: [Início do repositório](../README.md) | Anterior: [Série 1 - RAG, Azure vs Alternativas de Código Aberto, e Quando o Fine-Tuning Faz Sentido](./series-1-rag-azure-open-source-fine-tuning.md)

Notebook: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | Requisitos: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> Este é o melhor ponto de partida se você quiser entender o pipeline RAG antes de criar recursos na nuvem. O caminho padrão roda localmente com embeddings amigáveis à CPU e sem segredos.

## 1. O Que Estamos Construindo

No tutorial de 2023, comecei pelo Azure porque o objetivo era mostrar como Azure AI Search e Azure OpenAI podiam responder perguntas a partir de documentos PDF.

Para esta série de 2026, quero começar um nível mais abaixo.

Antes de usar serviços gerenciados, quero construir um pequeno sistema RAG localmente e tornar cada etapa visível: carregar documentos, dividir texto em chunks, armazenar vetores, recuperar evidências, reranquear resultados e retornar uma resposta consciente da fonte.

O cenário de amostra é um assistente de políticas escolares. O usuário pergunta:

```text
Can I use generative AI for my final assignment?
```

O sistema não deve responder a partir da memória geral do modelo. Deve recuperar a seção relevante da política e responder com base nessa evidência.

A versão completa executável está em [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb). O código abaixo mostra as principais etapas para que o artigo possa ser lido como um tutorial.

## 2. Instale as Dependências Locais

Crie um ambiente virtual e instale os requisitos da Série 2:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

A primeira versão usa o modo local do Qdrant e FastEmbed. O cliente Python do Qdrant suporta um modo local em memória com `QdrantClient(":memory:")`, útil para tutoriais locais e verificação estilo CI. FastEmbed nos dá um modelo de embedding local real sem precisar de chave API de nuvem.

O arquivo de requisitos também inclui `python-dotenv` porque o notebook pode ler opcionalmente um nome de modelo Ollama do `.env`. Nenhuma chave API do Azure OpenAI ou OpenAI é necessária para esse tutorial local.

## 3. Carregue os Documentos de Amostra

O corpus de amostra é intencionalmente pequeno:

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

No notebook, carrego todos os arquivos Markdown de `sample_data/`:

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

Quando executei o notebook, ele carregou 2 documentos. Isso é pequeno o suficiente para inspecionar manualmente, o que é útil ao construir a primeira versão de um pipeline RAG.

## 4. Divida pelo Cabeçalho Markdown

O próximo passo é dividir os documentos em chunks.

Para este tutorial, uso os cabeçalhos Markdown como sinal de estrutura. O título do documento vem de `#` e cada chunk de seção vem de `##`.

> [!NOTE]
> Dividir em chunks não é uma solução única para todos. Neste tutorial, uso os cabeçalhos Markdown porque os documentos de amostra têm estrutura clara `#` e `##`. Para PDFs, documentos Word, slides, tickets ou páginas web, uma estratégia melhor pode utilizar limites de página, informações de layout, seções semânticas, limites de tokens, tabelas ou metadados. O ponto importante é escolher uma estratégia de chunking que preserve significado e rastreabilidade da fonte para seus documentos.

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

Depois aplico a todos os documentos:

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

Isso criou 8 chunks na minha execução local.

O que gostei nesta etapa foi que os metadados já são úteis. Cada chunk sabe sua `source`, `sectionHeading`, `documentVersion` e o placeholder `permissions`. Mesmo em um tutorial pequeno, isso facilita o raciocínio sobre citações e recuperação consciente de permissões depois.

## 5. Crie Embeddings Locais

Para a primeira versão pública, uso `BAAI/bge-small-en-v1.5` via FastEmbed.

Isso mantém o tutorial local e amigável à CPU, mas ainda usa um modelo real de embedding em vez de uma função vetorial fictícia. A primeira execução baixa os pesos do modelo. Depois disso, o notebook pode reutilizar o cache local.

> [!NOTE]
> Uso `BAAI/bge-small-en-v1.5` porque é um modelo leve de embedding em inglês que funciona bem com FastEmbed e Qdrant para um tutorial local. Ele cria vetores de 384 dimensões, o que mantém o exemplo rápido e barato para rodar localmente. Esta não é a única boa escolha. Em 2023, muitos tutoriais usavam modelos de embedding hospedados como `text-embedding-ada-002`. Hoje, opções hospedadas mais novas como OpenAI `text-embedding-3-small` e `text-embedding-3-large`, e opções open-source como BGE, E5, MiniLM, Nomic Embed e modelos multilíngues como `BAAI/bge-m3` são escolhas razoáveis dependendo da carga de trabalho. Em produção, o modelo de embedding certo deve ser selecionado por avaliação de recuperação no conjunto dos seus documentos.

Algumas alternativas práticas:

| Família de modelo | Quando eu consideraria |
| --- | --- |
| `text-embedding-ada-002` | Linha de base hospedada mais antiga que apareceu em muitos tutoriais da era 2023. Eu não escolheria como padrão para um tutorial novo hoje. |
| `text-embedding-3-small` | Padrão hospedado moderno quando quero bom equilíbrio custo/desempenho e não preciso de embeddings exclusivamente locais. |
| `text-embedding-3-large` | Opção hospedada quando a qualidade de recuperação importa mais que o tamanho do vetor ou custo do embedding. |
| `BAAI/bge-small-en-v1.5` | Linha de base local leve em inglês para tutoriais, protótipos e experimentos amigáveis à CPU. |
| `BAAI/bge-base-en-v1.5` ou `BAAI/bge-large-en-v1.5` | Modelos locais em inglês maiores quando quero melhor qualidade de recuperação e posso pagar mais computação. |
| `BAAI/bge-m3` | Recuperação multilíngue ou de contexto mais longo, especialmente quando os documentos não são somente em inglês. |
| `sentence-transformers/all-MiniLM-L6-v2` | Linha de base de busca semântica muito pequena e rápida. Útil quando velocidade e simplicidade importam mais. |
| `nomic-embed-text-v1.5` | Opção local aberta para embeddings que vale testar para contextos longos ou setups focados em portabilidade. |

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

Depois, cada chunk recebe um embedding:

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

## 6. Armazene Vetores no Modo Local Qdrant

Agora criamos uma coleção Qdrant em memória e inserimos os chunks com metadados no payload.

> [!NOTE]
> No tutorial de 2023, usei FAISS porque era uma forma simples e popular de demonstrar busca local por similaridade vetorial com LangChain. FAISS ainda é útil para experimentos locais rápidos. Nesta versão 2026, uso Qdrant porque quero que o tutorial se aproxime mais de um sistema RAG de produção. O Qdrant permite armazenar vetores junto com metadados do payload como arquivo fonte, título da seção, versão do documento e permissões. Isso facilita inspecionar a recuperação e prepara o exemplo para filtragem, citações e implantação futura persistente ou baseada em servidor.

FAISS é ótimo para mostrar busca por similaridade vetorial. Qdrant é melhor para mostrar uma camada RAG pequena, mas com padrão de produção.

Algumas alternativas práticas:

| Armazenamento vetorial / camada de busca | Quando eu consideraria |
| --- | --- |
| Qdrant | Protótipos locais, filtragem por metadados, busca vetorial amigável para produção e fluxo Python simples. |
| Chroma | Experimentos RAG locais rápidos e notebooks onde simplicidade importa mais. |
| FAISS | Busca vetorial local leve quando só preciso de similaridade vetorial e posso gerenciar metadados separadamente. |
| Milvus | Busca vetorial open-source de maior escala quando a equipe está pronta para operar um banco de dados vetorial dedicado. |
| Weaviate | Busca vetorial com esquema, metadados, busca híbrida e opções de implantação gerenciada ou auto-hospedada. |
| Azure AI Search | RAG empresarial no Azure quando quero busca por palavra-chave, busca vetorial, recuperação híbrida, ranqueamento semântico, filtragem, segurança e operações gerenciadas numa camada de busca única. |
| PostgreSQL + pgvector | Equipes já usando PostgreSQL que querem busca vetorial próxima aos dados da aplicação. |

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

Depois insira os pontos:

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

É aqui que o sistema RAG começa a ficar inspecionável. O banco de dados vetorial não está só armazenando vetores; está armazenando o texto da evidência e os metadados necessários para citações.

## 7. Recupere Chunks Candidatos

Agora fazemos a pergunta e recuperamos os chunks candidatos.

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

Neste ponto, imprimo os chunks recuperados antes de gerar uma resposta. Isso é importante. Se a recuperação estiver errada, a geração só esconderá o problema por trás de um texto fluente.

## 8. Adicione um Reranker Leve

Quando testei o caminho de recuperação pela primeira vez, a similaridade vetorial sozinha encontrava conteúdo de política relacionado, mas a seção mais precisa nem sempre ficava no topo.

Então adicionei um pequeno reranker local. Ele dá peso extra quando os termos da pergunta se sobrepõem ao título da seção e ao conteúdo.

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

Depois do reranking, o resultado principal virou:

```text
school_ai_policy.md / Final Assignments
```

Essa foi a seção esperada para a pergunta de teste.

Essa foi a lição mais útil da primeira implementação. Mesmo em um exemplo local minúsculo, a qualidade da recuperação melhorou quando combinei similaridade vetorial com outro sinal.

## 9. Componha uma Resposta Local Fundamentada

Para o caminho padrão, uso um compositor transparente de resposta local ao invés de um LLM.

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

Isso não se destina a ser um gerador de resposta final. É uma ferramenta de depuração. Prova que a recuperação, os metadados e o encadeamento de citações funcionam antes de adicionar variabilidade do modelo.

## 10. Gere uma Resposta Local com Ollama e Phi-4-mini

Quando a recuperação está funcionando, o notebook pode substituir só a etapa final de resposta pelo Ollama e `phi4-mini:3.8b`.

> [!NOTE]
> Ollama deve substituir apenas a etapa final de geração de resposta. Carregamento de documento, chunking, armazenamento vetorial, recuperação, reranking e encadeamento de citações devem permanecer os mesmos.

Primeiro, o notebook monta um prompt de evidência a partir dos chunks recuperados:

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

Para este tutorial, recomendo a família Phi-4-mini da Microsoft via Ollama como opção padrão de geração local. Em Ollama, o nome do modelo que testei é:

```powershell
ollama pull phi4-mini:3.8b
```

Você pode rapidamente checar se o modelo está disponível:

```powershell
ollama list
```

Depois, defina essas variáveis:

```powershell
Copy-Item .env.example .env
```

Abra `.env` e descomente os valores Ollama da Série 2:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

O notebook carrega o `.env` da raiz do repositório com `python-dotenv`, então envia o mesmo prompt de evidência para o endpoint local `/api/chat` do Ollama com streaming desativado. Se o Ollama não estiver rodando ou `SERIES2_OLLAMA_MODEL` estiver faltando, essa trilha é pulada.

> [!NOTE]
> Nesta máquina, `phi4-mini:3.8b` baixou cerca de 2,49GB de arquivos do modelo. Durante a inferência, o Ollama reportou um tamanho carregado do modelo de 3,3GB e usou a GPU RTX 3060 Laptop.

Isso dá ao tutorial dois níveis:

1. Compositor de respostas determinístico apenas CPU.
2. Geração local de resposta com Ollama e Phi-4-mini.

O pipeline de recuperação fica o mesmo em ambos.

## 11. Resultado da Verificação

Executei o notebook localmente no Windows com Python 3.12.6.

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
- Chunks criados: 8
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

Eu não chamaria esta resposta de perfeita. Ela responde com base na evidência correta, mas a linha da fonte final é menos precisa do que o formato determinístico de citação. Isso é útil para mostrar no tutorial porque torna a próxima questão de engenharia óbvia: a geração de respostas também precisa de avaliação, não apenas a recuperação.

O principal que aprendi ao verificar isso é que a qualidade da recuperação deve ser verificada antes da geração da resposta. O resultado do embedding já era útil, e o reranker leve fez a seção de política esperada aparecer confiavelmente em primeiro lugar. Esse é exatamente o tipo de comportamento pequeno do sistema que quero que o tutorial exponha em vez de esconder.

## 12. O Que Vem a Seguir

A próxima melhoria é comparar essa configuração local com uma versão gerenciada da Azure do mesmo cenário do assistente de política escolar. Manter o cenário fixo deve facilitar a visualização dos trade-offs: complexidade da configuração, controles de recuperação, integração de identidade, propriedade operacional e custo.

## 13. Referências

- [Qdrant Python client quickstart](https://python-client.qdrant.tech/quickstart.html)
- [Repositório GitHub do cliente Qdrant](https://github.com/qdrant/qdrant-client)
- [Modelos suportados pelo FastEmbed](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [Guia de embeddings da OpenAI](https://platform.openai.com/docs/guides/embeddings)
- [Card do modelo BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [Card do modelo BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3)
- [Card do modelo sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Página do modelo Ollama phi4-mini](https://ollama.com/library/phi4-mini)
- [Documentação do Ollama para Windows](https://docs.ollama.com/windows)
- [Documentação da API de streaming do Ollama](https://docs.ollama.com/api/streaming)
- [Card do modelo Microsoft Phi-4-mini-instruct](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [Visão geral do LangGraph](https://docs.langchain.com/oss/python/langgraph)
- [Introdução ao RAG - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

Anterior: [Série 1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido usando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, por favor, esteja ciente de que traduções automatizadas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->