# Ensinar a IA a Responder a Perguntas com Base nos Seus Documentos - Plano da Série

Este plano acompanha o lançamento público da Série 1 e Série 2. O trabalho posterior com Azure e avaliação está a ser mantido como rascunho até que os exemplos estejam completamente integrados e verificados.

Não faça commit nem push das alterações até receber instruções explícitas.

## Âmbito Público

Lançamento público atual:

- Artigo da Série 1: decisões sobre a arquitetura RAG, trade-offs entre Azure e open-source, e onde o fine-tuning se enquadra.
- Artigo da Série 2: tutorial local open-source RAG.
- Caderno da Série 2: laboratório local RAG executável com FastEmbed, Qdrant, Ollama e Phi-4-mini.
- Dados de exemplo: ficheiros Markdown de política escolar e orientações de IA para cursos.

Rascunhado mas ainda não no índice público:

- Reconstrução do Azure AI Search e Azure OpenAI.
- Avaliação e verificações de regressão do RAG.

## Cenário do Tutorial

O cenário partilhado é um assistente de política escolar.

O assistente responde a esta pergunta com base em documentos locais:

```text
Can I use generative AI for my final assignment?
```

O comportamento esperado é:

1. Carregar documentos locais em Markdown.
2. Fazer parsing e dividir por secções.
3. Criar embeddings locais e armazenar representações pesquisáveis com metadados.
4. Recuperar a secção relevante da política.
5. Reordenar quando necessário.
6. Gerar ou compor uma resposta fundamentada.
7. Retornar citações.
8. Registar resultados de verificação.

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

O material em rascunho está armazenado na pasta `drafts/` e é ignorado pela verificação do repositório até estar pronto para indexação pública.

## Verificação da Série 2

Verificado no Windows com Python 3.12.6.

- Instalado com sucesso o `requirements/open-source-rag.txt`.
- Executado o `notebooks/series-2-open-source-rag.ipynb` com `nbclient`.
- Verificação local passou: 2 documentos de exemplo carregados, 8 fragmentos criados, FastEmbed gerou embeddings locais de 384 dimensões, coleção Qdrant em memória inicializada, e 8 vetores inseridos.
- Pergunta de teste: "Posso usar IA generativa para o meu trabalho final?"
- Fonte principal recuperada após reordenação leve: `school_ai_policy.md`.
- Secção principal recuperada após reordenação leve: `Final Assignments`.
- Caminho de resposta padrão: compositor de respostas transparente local.
- Ollama instalado via winget; `phi4-mini:3.8b` transferido com sucesso.
- Caminho de geração de resposta do Ollama: concluído com `phi4-mini:3.8b`.
- Tamanho do ficheiro do modelo Ollama: cerca de 2,49GB em disco.
- Tamanho do modelo Ollama carregado: 3,3GB reportado pelo `ollama ps`.
- Descarga para GPU: 100% GPU reportado pelo `ollama ps` numa RTX 3060 Laptop GPU.
- Memória GPU observada após geração: cerca de 3,5GB de 6GB.
- Execução do caderno com modelo FastEmbed em cache e geração Ollama ativada passou em cerca de 34 segundos pelo script de verificação.
- Observação: uma passagem inicial de carregamento de documentos incluiu acidentalmente `sample_data/README.md`; o caderno agora carrega explicitamente apenas os dois documentos de amostra pretendidos.

## Verificação do Repositório

- `scripts/verify_notebooks.py` valida links Markdown locais, JSON do caderno, limpeza da saída do caderno e padrões de segredos de alto risco.
- `scripts/verify_notebooks.py --execute` executa os cadernos públicos desde a raiz do repositório.
- Material em rascunho na pasta `drafts/` é intencionalmente desconsiderado.

## Próximo Trabalho

- Reconstruir o mesmo cenário com Azure AI Search e Azure OpenAI numa futura parte da série.
- Adicionar avaliação da recuperação e da resposta quando as implementações locais e Azure estiverem ambas estáveis.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas resultantes da utilização desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->