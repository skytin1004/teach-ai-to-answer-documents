# Cadernos

Estes cadernos suportam a série de artigos com exemplos executáveis.

| Caderno | Artigo | Propósito |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Série 2](../articles/series-2-open-source-rag-end-to-end.md) | RAG open-source com FastEmbed, modo local Qdrant, recuperação, reranqueamento, geração opcional Ollama e referências à fonte |

## Executar Localmente

Instale os requisitos para o caderno que deseja executar:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

Ou instale todas as dependências:

```powershell
python -m pip install -r requirements\all.txt
```

## Verificar

A partir da raiz do repositório:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

A Série 2 pode ler a configuração Ollama a partir de um ficheiro `.env` na raiz do repositório. Comece por [../.env.example](../../../.env.example), que está agrupado por séries.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas resultantes da utilização desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->