# 笔记本

这些笔记本支持带有可运行示例的文章系列。

| 笔记本 | 文章 | 目的 |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [系列 2](../articles/series-2-open-source-rag-end-to-end.md) | 使用 FastEmbed、Qdrant 本地模式、检索、重排序、可选 Ollama 生成和来源引用的开源 RAG |

## 本地运行

安装您想运行的笔记本的依赖：

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

或者安装所有依赖：

```powershell
python -m pip install -r requirements\all.txt
```

## 验证

从仓库根目录：

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

系列 2 可以从仓库根目录的 `.env` 文件读取 Ollama 配置。请从 [../.env.example](../../../.env.example) 开始，该文件按系列分组。

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免责声明**：
本文件由 AI 翻译服务 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻译完成。尽管我们力求准确，但请注意，自动翻译可能包含错误或不准确之处。原始语言版文件应视为权威来源。对于重要信息，建议使用专业人工翻译。我们对因使用本翻译而产生的任何误解或误释不承担责任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->