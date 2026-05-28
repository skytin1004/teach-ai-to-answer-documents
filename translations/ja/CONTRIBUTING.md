# Contributing

このリポジトリはブログシリーズと実行可能なノートブックの例で構成されています。

## Pull Request を開く前に

ローカル検証スクリプトを実行してください:

```powershell
python scripts\verify_notebooks.py
```

実装やノートブックの変更については、ローカルで安全なノートブック実行を実行してください:

```powershell
python scripts\verify_notebooks.py --execute
```

## ノートブックのガイドライン

- ノートブックは読みやすく関連記事に集中したものにしてください。
- 保存されたノートブックの出力や実行カウントはコミットしないでください。
- 記事で特定の外部リソースを必要としない限り、`sample_data/` の小さなサンプルデータを使用してください。
- 動作が変わった場合は関連記事に検証結果を記録してください。

## シークレットと認証情報

- APIキー、トークン、パスワード、プライベートエンドポイント、`.env` ファイルをコミットしないでください。
- `.env.example` はプレースホルダー値のみの使用にしてください。
- オプションのローカル Ollama 実験には環境変数を使用してください。

## ドキュメンテーション

- 記事のナビゲーションリンクを最新の状態に保ってください。
- 新しい記事、ノートブック、requirementsファイル、サンプルデータファイルを追加する際は `README.md` を更新してください。
- リポジトリの変更を公開する前に `CHANGELOG.md` を更新してください。

## 検証

GitHub Actions ワークフローは以下を実行します:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

`drafts/` 以下のドラフト資料は、公開インデックス化の準備ができるまでリポジトリ検証から除外されます。

## Issues

記事の修正には記事フィードバックテンプレートを、ノートブックの実行問題にはノートブック用のIssueテンプレートを使用してください。

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責事項**：
本書類は AI 翻訳サービス [Co-op Translator](https://github.com/Azure/co-op-translator) を使用して翻訳されています。正確性を期していますが、自動翻訳には誤りや不正確な部分が含まれる可能性があることをご承知おきください。原文の原語版が正式な情報源とみなされるべきです。重要な情報については、専門の人間による翻訳を推奨します。本翻訳の利用により生じたいかなる誤解や解釈違いについても、当方は責任を負いかねます。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->