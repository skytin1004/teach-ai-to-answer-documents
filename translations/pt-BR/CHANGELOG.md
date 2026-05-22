# Changelog

## Não lançado

Escopo de lançamento público inicial para **Ensinar IA a Responder Perguntas com Base em Seus Documentos**.

### Adicionado

- Artigo da Série 1 sobre decisões de arquitetura RAG, trade-offs Azure vs open-source, e onde o fine-tuning se encaixa.
- Artigo e notebook da Série 2 para um fluxo de trabalho RAG open-source local usando modo local do Qdrant, embeddings locais FastEmbed, reranking leve, Ollama e Phi-4-mini.
- Formato tutorial passo a passo de ponta a ponta da Série 2 com trechos de código Python e notas de verificação do notebook executado.
- Caminho opcional na Série 2 para geração de respostas com Ollama e Phi-4-mini mantendo a recuperação amigável ao CPU local como caminho padrão.
- Verificação local Ollama para a Série 2 usando `phi4-mini:3.8b` em GPU Laptop RTX 3060.
- Dados de exemplo para política escolar e orientação AI de curso.
- Arquivos de requisitos para o notebook público e verificação a nível de repositório.
- Script de verificação do repositório para links locais Markdown e validação/execução do notebook.
- Workflow GitHub Actions para verificação do notebook.
- `.env.example` para configuração opcional local de geração Ollama sem commitar configuração local.
- Arquivos README em nível de pasta para artigos, notebooks, requisitos, dados de exemplo e scripts.
- Lista de verificação para publicação focada em segurança e verificação pública.
- Workspace rascunho para conteúdo futuro de Azure e avaliação.

### Verificado

- Validação de links locais Markdown passou.
- Notebook da Série 2 validado com sucesso.
- Notebook da Série 2 executado com sucesso no ambiente local de verificação.
- Arquivos do notebook mantidos sem saídas salvas ou contagem de execução.
- Nenhum segredo real foi comitado.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido usando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, por favor, esteja ciente de que traduções automatizadas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->