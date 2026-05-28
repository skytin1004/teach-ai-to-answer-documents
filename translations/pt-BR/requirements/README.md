# Requisitos

Cada artigo de implementação possui um arquivo de requisitos focado.

| Arquivo | Usado por |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | Notebook RAG open-source da Série 2, incluindo ajudantes opcionais de geração Ollama |
| [all.txt](../../../requirements/all.txt) | Verificação e CI em nível de repositório |

Use o arquivo focado ao executar um notebook. Use `all.txt` ao validar todo o repositório.

`open-source-rag.txt` e `all.txt` incluem `fastembed` para embeddings locais e `python-dotenv` para que a Série 2 possa, opcionalmente, habilitar a geração Ollama a partir do `.env` sem alterar o pipeline de recuperação.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido usando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, por favor, esteja ciente de que traduções automatizadas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->