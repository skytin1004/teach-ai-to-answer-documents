# Ensine a IA a Responder Perguntas com Base nos Seus Documentos

![Visão geral do sistema RAG com base em documentos grounded AI](../../assets/images/readme-hero.svg)

Este repositório reúne uma série de blogues de 2026 sobre a criação de sistemas de IA baseados em documentos com RAG, serviços Azure AI, alternativas open-source e fluxos de trabalho orientados para avaliação.

## Contexto

Em 2023, trabalhei num par de tutoriais sobre ensinar o ChatGPT a responder a perguntas de documentos PDF usando o Azure AI Search e Azure OpenAI. A ideia de "ChatGPT nos seus dados" ainda parecia nova nessa altura, e o objetivo era mostrar um fluxo de trabalho prático: armazenar documentos, indexá-los, recuperar conteúdos relevantes e gerar respostas a partir desse contexto recuperado.

Em 2026, o ecossistema RAG é muito maior. O Azure AI Search suporta padrões modernos de recuperação vetorial e híbrida, o Azure OpenAI faz parte do ecossistema mais amplo dos Microsoft Foundry Models, e ferramentas open-source como LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, e vLLM tornaram-se escolhas práticas para sistemas reais.

Por isso é que quis revisitar este tema. A questão já não é apenas "Como é que construo um RAG?" Há agora várias maneiras de o construir, e a questão mais importante é "Qual arquitetura devo escolher para a minha situação?"

Esta série começa por essa camada de tomada de decisão, depois transforma-a em tutoriais práticos. O primeiro caminho de implementação constrói um sistema RAG open-source local que qualquer pessoa pode correr com dados de exemplo, Qdrant, Ollama e Phi-4-mini.

## Artigos

Consulte [articles/README.md](./articles/README.md) para o índice de artigos.

1. [Série 1: RAG, Azure vs Alternativas Open-Source, e Quando Faz Sentido Ajustar o Modelo](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [Série 2: Construa um Sistema RAG Open-Source Local de Ponta a Ponta](./articles/series-2-open-source-rag-end-to-end.md)

A seguir:

- Reconstruir o mesmo sistema RAG com Azure AI Search e Azure OpenAI.
- Adicionar avaliação e verificações de regressão para além de uma resposta de demonstração.

## Notebooks

Os artigos de implementação usam notebooks para que as etapas de recuperação e avaliação possam ser inspecionadas diretamente. Veja [notebooks/README.md](./notebooks/README.md) para orientação ao nível da pasta.

> [!TIP]
> Comece pela Série 2 se quiser o caminho mais rápido. Corre localmente com dados de exemplo, embeddings amigáveis para CPU, modo local do Qdrant, e sem credenciais na cloud.

| Série | Notebook | Requisitos | Verificação local |
| --- | --- | --- | --- |
| Série 2 | [Notebook RAG open-source](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Modo local Qdrant, recuperação, reclassificação e ligação à fonte verificados |

Para correr um notebook localmente, crie um ambiente virtual e instale o ficheiro de requisitos correspondente. Por exemplo:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## Dados de Exemplo

Os notebooks usam um pequeno corpus local em [sample_data](../../sample_data) para que os exemplos possam ser executados sem documentos privados ou credenciais na cloud. Veja [sample_data/README.md](./sample_data/README.md) para detalhes.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## Resumo da Verificação Local

Os resultados da verificação são registados em cada artigo e no [SERIES_PLAN.md](./SERIES_PLAN.md).

| Área | Resultado |
| --- | --- |
| Caminho open-source da Série 2 | FastEmbed gerou embeddings locais de 384 dimensões, a coleção em memória do Qdrant inseriu 8 vetores, a reclassificação leve recuperou a secção esperada; a geração opcional Ollama completou com `phi4-mini:3.8b` |

O notebook local evita intencionalmente segredos codificados.

## Geração Local com Ollama

O notebook da Série 2 é seguro para uso local por defeito. Para ativar a geração local com Ollama, copie [.env.example](../../.env.example) para `.env` e preencha os valores da Série 2.

Para a geração Ollama da Série 2, descomente:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

O notebook da Série 2 carrega automaticamente `.env` a partir da raíz do repositório usando `python-dotenv`.

> [!IMPORTANT]
> Não cometa ficheiros `.env`, chaves API, endpoints privados, ou valores específicos do inquilino. O repositório mantém intencionalmente os segredos fora dos ficheiros Markdown e notebooks.

Os ficheiros de requisitos estão documentados em [requirements/README.md](./requirements/README.md).

Para validar links, estrutura do notebook, limpeza dos outputs e padrões de segredos de alto risco:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

Os scripts de verificação estão documentados em [scripts/README.md](./scripts/README.md).

Para executar todos os notebooks seguros para uso local no mesmo ambiente:

```powershell
python scripts\verify_notebooks.py --execute
```

O mesmo fluxo de verificação corre nas GitHub Actions em pushes, pull requests, e despachos manuais do workflow. Artigos e notebooks em rascunho são intencionalmente excluídos da verificação pública.

Antes de publicar atualizações, use [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md).

Veja [CHANGELOG.md](./CHANGELOG.md) para o resumo atual das alterações não publicadas.

Para diretrizes de contribuição e higiene dos notebooks, consulte [CONTRIBUTING.md](./CONTRIBUTING.md).

## Suporte Multilingue

### Suportado via Co-op Translator (Automatizado e Sempre Atualizado)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Árabe](../ar/README.md) | [Bengali](../bn/README.md) | [Búlgaro](../bg/README.md) | [Birmanês (Myanmar)](../my/README.md) | [Chinês (Simplificado)](../zh-CN/README.md) | [Chinês (Tradicional, Hong Kong)](../zh-HK/README.md) | [Chinês (Tradicional, Macau)](../zh-MO/README.md) | [Chinês (Tradicional, Taiwan)](../zh-TW/README.md) | [Croata](../hr/README.md) | [Checo](../cs/README.md) | [Dinamarquês](../da/README.md) | [Holandês](../nl/README.md) | [Estónio](../et/README.md) | [Finlandês](../fi/README.md) | [Francês](../fr/README.md) | [Alemão](../de/README.md) | [Grego](../el/README.md) | [Hebraico](../he/README.md) | [Hindi](../hi/README.md) | [Húngaro](../hu/README.md) | [Indonésio](../id/README.md) | [Italiano](../it/README.md) | [Japonês](../ja/README.md) | [Canarês](../kn/README.md) | [Cambojano](../km/README.md) | [Coreano](../ko/README.md) | [Lituano](../lt/README.md) | [Malaio](../ms/README.md) | [Malaiala](../ml/README.md) | [Marata](../mr/README.md) | [Nepalês](../ne/README.md) | [Pidgin Nigeriano](../pcm/README.md) | [Norueguês](../no/README.md) | [Persa (Farsi)](../fa/README.md) | [Polaco](../pl/README.md) | [Português (Brasil)](../pt-BR/README.md) | [Português (Portugal)](./README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romeno](../ro/README.md) | [Russo](../ru/README.md) | [Sérvio (Cirílico)](../sr/README.md) | [Eslovaco](../sk/README.md) | [Esloveno](../sl/README.md) | [Espanhol](../es/README.md) | [Suaíli](../sw/README.md) | [Sueco](../sv/README.md) | [Tagalo (Filipino)](../tl/README.md) | [Tâmil](../ta/README.md) | [Telugu](../te/README.md) | [Tailandês](../th/README.md) | [Turco](../tr/README.md) | [Ucraniano](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamita](../vi/README.md)

> **Prefere Clonar Localmente?**
>
> Este repositório inclui traduções para mais de 50 idiomas, o que aumenta significativamente o tamanho do download. Para clonar sem as traduções, use checkout esparso:
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
> Isto dá-lhe tudo o que precisa para completar o curso com um download muito mais rápido.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas resultantes da utilização desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->