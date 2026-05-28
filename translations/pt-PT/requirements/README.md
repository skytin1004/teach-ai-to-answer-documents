# Requisitos

Cada artigo de implementação tem um ficheiro de requisitos focado.

| Ficheiro | Utilizado por |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | Caderno RAG open-source da Série 2, incluindo auxiliares opcionais de geração Ollama |
| [all.txt](../../../requirements/all.txt) | Verificação e CI a nível do repositório |

Use o ficheiro focado ao executar um caderno. Use `all.txt` ao validar o repositório inteiro.

`open-source-rag.txt` e `all.txt` incluem `fastembed` para embeddings locais e `python-dotenv` para que a Série 2 possa opcionalmente ativar a geração Ollama a partir do `.env` sem alterar o pipeline de recuperação.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas resultantes da utilização desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->