# Ensine IA a Responder Perguntas com Base em Seus Documentos

![Visão geral do sistema AI RAG ancorado em documentos](../../assets/images/readme-hero.svg)

Este repositório reúne uma série de blogs de 2026 sobre a construção de sistemas de IA ancorados em documentos com RAG, serviços Azure AI, alternativas de código aberto e fluxos de trabalho orientados à avaliação.

## Contexto

Em 2023, trabalhei em um par de tutoriais sobre como ensinar o ChatGPT a responder perguntas a partir de documentos PDF usando Azure AI Search e Azure OpenAI. A ideia de "ChatGPT nos seus dados" ainda parecia nova naquela época, e o objetivo era mostrar um fluxo de trabalho prático: armazenar documentos, indexá-los, recuperar conteúdo relevante e gerar respostas a partir desse contexto recuperado.

Em 2026, o ecossistema RAG é muito maior. O Azure AI Search suporta padrões modernos de recuperação vetorial e híbrida, o Azure OpenAI faz parte do ecossistema mais amplo dos Microsoft Foundry Models, e ferramentas de código aberto como LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama e vLLM tornaram-se escolhas práticas para sistemas reais.

Por isso, quis revisitar esse tema. A pergunta não é mais apenas "Como construir RAG?" Agora existem muitas maneiras de construí-lo, e a questão mais importante é "Qual arquitetura devo escolher para minha situação?"

Esta série começa a partir dessa camada de decisão, e depois a torna em tutoriais práticos. O primeiro caminho de implementação constrói um sistema RAG local de código aberto que qualquer pessoa pode executar com dados de exemplo, Qdrant, Ollama e Phi-4-mini.

## Artigos

Veja [articles/README.md](./articles/README.md) para o índice dos artigos.

1. [Série 1: RAG, Azure vs Alternativas de Código Aberto e Quando Ajustar é Adequado](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [Série 2: Construir um Sistema RAG Local de Código Aberto de Ponta a Ponta](./articles/series-2-open-source-rag-end-to-end.md)

Próximos passos:

- Reconstruir o mesmo sistema RAG com Azure AI Search e Azure OpenAI.
- Adicionar avaliação e verificações de regressão além da resposta de demonstração.

## Notebooks

Os artigos de implementação usam notebooks para que as etapas de recuperação e avaliação possam ser inspecionadas diretamente. Veja [notebooks/README.md](./notebooks/README.md) para orientações em nível de pasta.

> [!TIP]
> Comece pela Série 2 se desejar o caminho mais rápido. Ela roda localmente com dados de exemplo, embeddings amigáveis com CPU, modo local do Qdrant e sem credenciais na nuvem.

| Série | Notebook | Requisitos | Verificação local |
| --- | --- | --- | --- |
| Série 2 | [Notebook do RAG de código aberto](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Verificados modo local do Qdrant, recuperação, reranking e conexão da fonte |

Para executar um notebook localmente, crie um ambiente virtual e instale o arquivo de requisitos correspondente. Por exemplo:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## Dados de Exemplo

Os notebooks usam um pequeno corpus local em [sample_data](../../sample_data) para que os exemplos possam rodar sem documentos privados ou credenciais de nuvem. Veja [sample_data/README.md](./sample_data/README.md) para detalhes.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## Resumo da Verificação Local

Os resultados da verificação são registrados em cada artigo e em [SERIES_PLAN.md](./SERIES_PLAN.md).

| Área | Resultado |
| --- | --- |
| Caminho open-source da Série 2 | FastEmbed gerou embeddings locais de 384 dimensões, a coleção na memória do Qdrant inseriu 8 vetores, reranking leve recuperou a seção esperada; geração opcional do Ollama completada com `phi4-mini:3.8b` |

O notebook local evita intencionalmente segredos codificados.

## Geração Local com Ollama

O notebook da Série 2 é seguro localmente por padrão. Para habilitar a geração local com Ollama, copie [.env.example](../../.env.example) para `.env` e preencha os valores da Série 2.

Para a geração com Ollama da Série 2, descomente:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

O notebook da Série 2 carrega automaticamente `.env` da raiz do repositório usando `python-dotenv`.

> [!IMPORTANT]
> Não faça commit de arquivos `.env`, chaves de API, endpoints privados ou valores específicos do tenant. O repositório intencionalmente mantém segredos fora dos arquivos Markdown e notebooks.

Os arquivos de requisitos estão documentados em [requirements/README.md](./requirements/README.md).

Para validar links, estrutura do notebook, limpeza da saída e padrões de segredos de alto risco:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

Os scripts de verificação estão documentados em [scripts/README.md](./scripts/README.md).

Para executar todos os notebooks seguros localmente no mesmo ambiente:

```powershell
python scripts\verify_notebooks.py --execute
```

O mesmo fluxo de verificação roda no GitHub Actions em pushes, pull requests e disparos manuais de workflow. Artigos e notebooks em rascunho são intencionalmente excluídos do caminho de verificação público.

Antes de publicar atualizações, utilize [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md).

Veja [CHANGELOG.md](./CHANGELOG.md) para o resumo atual das mudanças não publicadas.

Para diretrizes de contribuição e higiene de notebooks, veja [CONTRIBUTING.md](./CONTRIBUTING.md).

## Suporte a Múltiplos Idiomas

### Suportado via Co-op Translator (Automatizado e Sempre Atualizado)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Árabe](../ar/README.md) | [Bengali](../bn/README.md) | [Búlgaro](../bg/README.md) | [Birmanês (Myanmar)](../my/README.md) | [Chinês (Simplificado)](../zh-CN/README.md) | [Chinês (Tradicional, Hong Kong)](../zh-HK/README.md) | [Chinês (Tradicional, Macau)](../zh-MO/README.md) | [Chinês (Tradicional, Taiwan)](../zh-TW/README.md) | [Croata](../hr/README.md) | [Tcheco](../cs/README.md) | [Dinamarquês](../da/README.md) | [Holandês](../nl/README.md) | [Estoniano](../et/README.md) | [Finlandês](../fi/README.md) | [Francês](../fr/README.md) | [Alemão](../de/README.md) | [Grego](../el/README.md) | [Hebraico](../he/README.md) | [Hindi](../hi/README.md) | [Húngaro](../hu/README.md) | [Indonésio](../id/README.md) | [Italiano](../it/README.md) | [Japonês](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Coreano](../ko/README.md) | [Lituano](../lt/README.md) | [Malaio](../ms/README.md) | [Malaiala](../ml/README.md) | [Marata](../mr/README.md) | [Nepali](../ne/README.md) | [Pidgin Nigeriano](../pcm/README.md) | [Norueguês](../no/README.md) | [Persa (Farsi)](../fa/README.md) | [Polonês](../pl/README.md) | [Português (Brasil)](./README.md) | [Português (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romeno](../ro/README.md) | [Russo](../ru/README.md) | [Sérvio (Cirílico)](../sr/README.md) | [Eslovaco](../sk/README.md) | [Esloveno](../sl/README.md) | [Espanhol](../es/README.md) | [Suaíli](../sw/README.md) | [Sueco](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tâmil](../ta/README.md) | [Telugu](../te/README.md) | [Tailandês](../th/README.md) | [Turco](../tr/README.md) | [Ucraniano](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamita](../vi/README.md)

> **Prefere clonar localmente?**
>
> Este repositório inclui traduções em mais de 50 idiomas, o que aumenta significativamente o tamanho do download. Para clonar sem as traduções, use checkout esparso:
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
> Isso fornece tudo o que você precisa para concluir o curso com um download muito mais rápido.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido usando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, por favor, esteja ciente de que traduções automatizadas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->