# Ensine IA a Responder Perguntas Baseadas em Seus Documentos - Plano da Série

Este plano acompanha o lançamento público da Série 1 e Série 2. Trabalhos futuros com Azure e avaliação estão sendo mantidos como rascunhos até que os exemplos estejam totalmente completos e verificados.

Não cometa nem envie mudanças até que seja instruído explicitamente.

## Escopo Público

Lançamento público atual:

- Artigo da Série 1: decisões de arquitetura RAG, tradeoffs entre Azure e open-source, e onde o fine-tuning se encaixa.
- Artigo da Série 2: tutorial RAG open-source local.
- Notebook da Série 2: laboratório RAG local executável com FastEmbed, Qdrant, Ollama e Phi-4-mini.
- Dados de exemplo: arquivos Markdown de políticas escolares e orientação de IA para cursos.

Rascunhado, mas ainda não no índice público:

- Reconstrução Azure AI Search e Azure OpenAI.
- Avaliação RAG e verificações de regressão.

## Cenário do Tutorial

O cenário compartilhado é um assistente de política escolar.

O assistente responde a esta pergunta a partir de documentos locais:

```text
Can I use generative AI for my final assignment?
```

O comportamento esperado é:

1. Carregar documentos locais em Markdown.
2. Analisá-los e dividir em partes por títulos.
3. Criar embeddings locais e armazenar representações pesquisáveis com metadados.
4. Recuperar a seção relevante da política.
5. Realizar reranking quando necessário.
6. Gerar ou compor uma resposta fundamentada.
7. Retornar citações.
8. Registrar resultados da verificação.

## Estrutura Pública Atual

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

Material rascunhado está armazenado em `drafts/` e é ignorado pela verificação do repositório até estar pronto para indexação pública.

## Verificação da Série 2

Verificado no Windows com Python 3.12.6.

- Instalado com sucesso `requirements/open-source-rag.txt`.
- Executado `notebooks/series-2-open-source-rag.ipynb` com `nbclient`.
- Verificação local passou: 2 documentos de amostra carregados, 8 partes criadas, FastEmbed gerou embeddings locais de 384 dimensões, coleção em memória Qdrant inicializada, e 8 vetores inseridos.
- Pergunta de teste: "Posso usar IA generativa para meu trabalho final?"
- Fonte recuperada principal após reranking leve: `school_ai_policy.md`.
- Seção recuperada principal após reranking leve: `Final Assignments`.
- Caminho padrão para resposta: compositor de resposta transparente local.
- Ollama instalado via winget; `phi4-mini:3.8b` baixado com sucesso.
- Caminho de geração de resposta do Ollama: concluído com `phi4-mini:3.8b`.
- Tamanho do arquivo do modelo Ollama: cerca de 2,49GB no disco.
- Tamanho do modelo carregado pelo Ollama: 3,3GB reportados pelo `ollama ps`.
- Descarregamento para GPU: 100% de GPU reportado pelo `ollama ps` em RTX 3060 Laptop GPU.
- Memória da GPU observada após geração: cerca de 3,5GB de 6GB.
- Execução do notebook com modelo FastEmbed em cache e geração Ollama ativada passou em cerca de 34 segundos pelo script de verificação.
- Observação: uma passada precoce de carregamento de documentos incluiu acidentalmente `sample_data/README.md`; o notebook agora carrega apenas os dois documentos de amostra pretendidos explicitamente.

## Verificação do Repositório

- `scripts/verify_notebooks.py` valida links Markdown locais, JSON do notebook, limpeza de saída do notebook e padrões de segredos de alto risco.
- `scripts/verify_notebooks.py --execute` executa notebooks públicos a partir da raiz do repositório.
- Material rascunhado em `drafts/` é intencionalmente ignorado.

## Próximos Trabalhos

- Reconstruir o mesmo cenário com Azure AI Search e Azure OpenAI como parte futura da série.
- Adicionar avaliação de recuperação e resposta assim que as implementações locais e Azure estiverem estáveis.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido usando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, por favor, esteja ciente de que traduções automatizadas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->