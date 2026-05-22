# Contribuir

Este repositório está organizado como uma série de blog mais exemplos de cadernos executáveis.

## Antes de Abrir um Pull Request

Execute o script de validação local:

```powershell
python scripts\verify_notebooks.py
```

Para implementações ou alterações em cadernos, execute a execução segura local do caderno:

```powershell
python scripts\verify_notebooks.py --execute
```

## Diretrizes para Cadernos

- Mantenha os cadernos legíveis e focados no artigo relacionado.
- Não faça commit das saídas salvas do caderno nem dos contadores de execução.
- Use pequenos dados de exemplo de `sample_data/` a menos que o artigo exija um recurso externo específico.
- Registe os resultados da verificação no artigo relacionado quando houver alterações de comportamento.

## Segredos e Credenciais

- Não faça commit de chaves API, tokens, passwords, endpoints privados, ou ficheiros `.env`.
- Use `.env.example` apenas para valores de espaço reservado.
- Use variáveis de ambiente para experiências locais opcionais com Ollama.

## Documentação

- Mantenha os links de navegação do artigo atualizados.
- Atualize o `README.md` ao adicionar um novo artigo, caderno, ficheiro de requisitos, ou ficheiro de dados de exemplo.
- Atualize o `CHANGELOG.md` antes de publicar uma atualização visível do repositório.

## Verificação

O fluxo de trabalho GitHub Actions executa:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

Material em rascunho na pasta `drafts/` é ignorado pela verificação do repositório até estar pronto para indexação pública.

## Problemas

Use o modelo de feedback para artigos para correções nos artigos e o modelo de issues para problemas na execução dos cadernos.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas resultantes da utilização desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->