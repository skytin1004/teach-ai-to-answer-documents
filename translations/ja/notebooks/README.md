# ノートブック

これらのノートブックは、実行可能な例を含む記事シリーズをサポートしています。

| ノートブック | 記事 | 目的 |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [シリーズ2](../articles/series-2-open-source-rag-end-to-end.md) | FastEmbed、Qdrantローカルモード、検索、再ランキング、オプションのOllama生成、およびソース参照を備えたオープンソースRAG |

## ローカルでの実行

実行したいノートブックの要件をインストールしてください：

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

またはすべての依存関係をインストール：

```powershell
python -m pip install -r requirements\all.txt
```

## 検証

リポジトリのルートから：

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

シリーズ2はリポジトリルートの `.env` ファイルからOllama設定を読み取ることができます。シリーズ別にグループ化された [../.env.example](../../../.env.example) から開始してください。

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責事項**：
本書類は AI 翻訳サービス [Co-op Translator](https://github.com/Azure/co-op-translator) を使用して翻訳されています。正確性を期していますが、自動翻訳には誤りや不正確な部分が含まれる可能性があることをご承知おきください。原文の原語版が正式な情報源とみなされるべきです。重要な情報については、専門の人間による翻訳を推奨します。本翻訳の利用により生じたいかなる誤解や解釈違いについても、当方は責任を負いかねます。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->