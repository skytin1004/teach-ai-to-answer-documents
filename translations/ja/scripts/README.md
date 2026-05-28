# Scripts

このフォルダーにはリポジトリ検証スクリプトが含まれています。

## `verify_notebooks.py`

ローカルのMarkdownリンク、ノートブックJSON、ノートブックの出力のクリーンさ、および高リスクのシークレットパターンを検証します：

```powershell
python scripts\verify_notebooks.py
```

すべての公開ローカル安全ノートブックを実行します：

```powershell
python scripts\verify_notebooks.py --execute
```

GitHub Actionsのワークフローも同じスクリプトを使用しています。

`drafts/` 内の草稿資料は、公開インデックスの準備ができるまでスキップされます。

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責事項**：
本書類は AI 翻訳サービス [Co-op Translator](https://github.com/Azure/co-op-translator) を使用して翻訳されています。正確性を期していますが、自動翻訳には誤りや不正確な部分が含まれる可能性があることをご承知おきください。原文の原語版が正式な情報源とみなされるべきです。重要な情報については、専門の人間による翻訳を推奨します。本翻訳の利用により生じたいかなる誤解や解釈違いについても、当方は責任を負いかねます。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->