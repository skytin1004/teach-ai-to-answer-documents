# Contribuindo

Este repositório está organizado como uma série de blogs mais exemplos executáveis em notebooks.

## Antes de Abrir um Pull Request

Execute o script de validação local:

```powershell
python scripts\verify_notebooks.py
```

Para alterações de implementação ou notebook, execute a execução segura local do notebook:

```powershell
python scripts\verify_notebooks.py --execute
```

## Diretrizes para Notebooks

- Mantenha os notebooks legíveis e focados no artigo relacionado.
- Não envie saídas salvas dos notebooks ou contagens de execução.
- Use pequenos dados de amostra de `sample_data/`, a menos que o artigo exija um recurso externo específico.
- Registre os resultados de verificação no artigo relacionado quando o comportamento mudar.

## Segredos e Credenciais

- Não envie chaves de API, tokens, senhas, endpoints privados ou arquivos `.env`.
- Use `.env.example` apenas para valores de espaço reservado.
- Use variáveis de ambiente para experimentos locais opcionais com Ollama.

## Documentação

- Mantenha os links de navegação dos artigos atualizados.
- Atualize `README.md` ao adicionar um novo artigo, notebook, arquivo de requisitos ou arquivo de dados de amostra.
- Atualize `CHANGELOG.md` antes de publicar uma atualização visível no repositório.

## Verificação

O fluxo de trabalho do GitHub Actions executa:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Material de rascunho em `drafts/` é ignorado pela verificação do repositório até estar pronto para indexação pública.

## Problemas

Use o modelo de feedback para artigos para correções de artigos e o modelo de problemas para notebooks para problemas de execução.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido usando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, por favor, esteja ciente de que traduções automatizadas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->