# Lista de Verificação para Publicação

Use esta lista de verificação antes de commitar ou enviar atualizações públicas.

## Segurança

- Confirme que nenhuma chave de API, token, senha ou endpoint privado está escrito em arquivos Markdown, notebooks, dados de amostra ou scripts.
- Mantenha as credenciais em variáveis de ambiente ou identidade gerenciada, não em arquivos comitados.
- Não comite arquivos `.env` ou arquivos de saída de notebook executados.
- Mantenha `.env.example` apenas como espaço reservado.

## Verificação

Execute o script de verificação do repositório:

```powershell
python scripts\verify_notebooks.py
```

Execute a execução completa e localmente segura do notebook antes de publicar alterações de implementação:

```powershell
python scripts\verify_notebooks.py --execute
```

Checagens esperadas:

- links locais de Markdown passam
- validação JSON dos notebooks passa
- notebooks não contêm saídas salvas ou contagens de execução
- varredura de padrões de segredo de alto risco passa
- notebooks públicos executam localmente
- material de rascunho em `drafts/` é intencionalmente ignorado

## Revisão

- Confirme que links de artigos no README apontam para os arquivos pretendidos.
- Confirme que cada artigo tem navegação do repositório e links para notebooks relacionados.
- Confirme que rascunhos não estão linkados em índices públicos, a menos que estejam prontos para publicação.
- Confirme que os templates de issues e pull requests do GitHub ainda correspondem ao fluxo de trabalho do repositório.
- Confirme que os resultados da verificação no artigo correspondem à última saída do notebook.
- Confirme que o workflow do GitHub Actions será executado após o push.
- Confirme que o `CHANGELOG.md` reflete a atualização que está sendo publicada.
- Confirme que o `CONTRIBUTING.md` ainda corresponde ao fluxo de trabalho do repositório.

## Git

- Revise `git status --short --branch`.
- Revise `git diff --stat`.
- Commite e envie somente quando explicitamente pronto.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido usando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, por favor, esteja ciente de que traduções automatizadas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->