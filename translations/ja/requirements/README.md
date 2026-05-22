# 要件

各実装記事には、特定の要件ファイルがあります。

| ファイル | 使用先 |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | シリーズ2のオープンソースRAGノートブック、オプションのOllama生成ヘルパーを含む |
| [all.txt](../../../requirements/all.txt) | リポジトリレベルの検証とCI |

1つのノートブックを実行する際は特化したファイルを使用してください。リポジトリ全体を検証する際は`all.txt`を使用してください。

`open-source-rag.txt`と`all.txt`には、ローカル埋め込み用の`fastembed`と、シリーズ2が取得パイプラインを変更せずに`.env`からOllama生成をオプションで有効にできるように`python-dotenv`が含まれています。

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責事項**：
本書類は AI 翻訳サービス [Co-op Translator](https://github.com/Azure/co-op-translator) を使用して翻訳されています。正確性を期していますが、自動翻訳には誤りや不正確な部分が含まれる可能性があることをご承知おきください。原文の原語版が正式な情報源とみなされるべきです。重要な情報については、専門の人間による翻訳を推奨します。本翻訳の利用により生じたいかなる誤解や解釈違いについても、当方は責任を負いかねます。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->