# Lista de Verificação para Publicação

Utilize esta lista de verificação antes de fazer commit ou push de atualizações públicas.

## Segurança

- Confirme que não existem chaves API, tokens, passwords ou endpoints privados escritos em ficheiros Markdown, notebooks, dados de exemplo ou scripts.
- Mantenha as credenciais em variáveis de ambiente ou identidade gerida, não em ficheiros com commit.
- Não faça commit de ficheiros `.env` nem ficheiros de output de notebooks executados.
- Mantenha `.env.example` apenas com placeholders.

## Verificação

Execute o script de verificação do repositório:

```powershell
python scripts\verify_notebooks.py
```

Execute a execução completa local segura do notebook antes de publicar alterações de implementação:

```powershell
python scripts\verify_notebooks.py --execute
```

Verificações esperadas:

- links locais em Markdown passam
- validação JSON dos notebooks passa
- notebooks não contêm outputs guardados nem contadores de execução
- scan de padrões de segredos de alto risco passa
- notebooks públicos executam localmente
- material em rascunho em `drafts/` é intencionalmente ignorado

## Revisão

- Confirme que os links nos artigos README apontam para os ficheiros pretendidos.
- Confirme que cada artigo tem navegação pelo repositório e links para notebooks relacionados.
- Confirme que rascunhos não estão ligados a partir de índices públicos, a menos que estejam prontos para publicar.
- Confirme que os templates de issues e pull requests do GitHub ainda correspondem ao fluxo de trabalho do repositório.
- Confirme que os resultados da verificação no artigo correspondem ao output mais recente do notebook.
- Confirme que o workflow do GitHub Actions está configurado para correr após o push.
- Confirme que o `CHANGELOG.md` reflete a atualização a ser publicada.
- Confirme que o `CONTRIBUTING.md` ainda corresponde ao fluxo de trabalho do repositório.

## Git

- Reveja o estado com `git status --short --branch`.
- Reveja as alterações com `git diff --stat`.
- Faça commit e push apenas quando estiver explicitamente pronto.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas resultantes da utilização desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->