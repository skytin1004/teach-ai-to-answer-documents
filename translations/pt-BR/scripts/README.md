# Scripts

Esta pasta contém scripts de verificação do repositório.

## `verify_notebooks.py`

Valida links locais de Markdown, JSON de notebook, limpeza da saída do notebook e padrões de segredos de alto risco:

```powershell
python scripts\verify_notebooks.py
```

Executa todos os notebooks públicos locais e seguros:

```powershell
python scripts\verify_notebooks.py --execute
```

O fluxo de trabalho do GitHub Actions usa o mesmo script.

Material em rascunho dentro de `drafts/` é ignorado até estar pronto para o índice público.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido usando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, por favor, esteja ciente de que traduções automatizadas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->