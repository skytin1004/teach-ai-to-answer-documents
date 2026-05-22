# Scripts

Esta pasta contém scripts de verificação do repositório.

## `verify_notebooks.py`

Valida ligações locais em Markdown, JSON de notebooks, limpeza da saída dos notebooks e padrões de segredos de alto risco:

```powershell
python scripts\verify_notebooks.py
```

Executa todos os notebooks públicos seguros locais:

```powershell
python scripts\verify_notebooks.py --execute
```

O fluxo de trabalho do GitHub Actions utiliza o mesmo script.

Material rascunho em `drafts/` é ignorado até estar pronto para o índice público.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas resultantes da utilização desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->