# ドキュメントに基づいて質問に回答するAIを教える - シリーズ計画

この計画はパブリックなシリーズ1およびシリーズ2のリリースを追跡します。後のAzureおよび評価作業は、サンプルが完全にエンドツーエンドで検証されるまでドラフトとして保持されます。

明示的な指示があるまで変更をコミットやプッシュしないでください。

## 公開範囲

現在の公開リリース：

- シリーズ1記事：RAGのアーキテクチャの決定、Azure対オープンソースのトレードオフ、ファインチューニングの位置付け。
- シリーズ2記事：ローカルオープンソースRAGのチュートリアル。
- シリーズ2ノートブック：FastEmbed、Qdrant、Ollama、Phi-4-miniを用いた実行可能なローカルRAGラボ。
- サンプルデータ：学校方針およびコースAIガイダンスのMarkdownファイル。

ドラフトだがまだ公開インデックスにないもの：

- Azure AI SearchおよびAzure OpenAIの再構築。
- RAGの評価およびリグレッションチェック。

## チュートリアルシナリオ

共有されているシナリオは学校方針アシスタントです。

アシスタントは以下の質問にローカルドキュメントから回答します：

```text
Can I use generative AI for my final assignment?
```
  
期待される動作は以下の通りです：

1. ローカルのMarkdownドキュメントを読み込む。  
2. 見出しごとに解析してチャンク化する。  
3. ローカル埋め込みを作成し、メタデータ付きの検索可能な表現を保存する。  
4. 関連する方針セクションを取得する。  
5. 必要に応じてリランキングする。  
6. 根拠のある回答を生成または作成する。  
7. 引用を返す。  
8. 検証結果を記録する。

## 現在の公開構成

```text
.
├── README.md
├── SERIES_PLAN.md
├── articles/
│   ├── README.md
│   ├── series-1-rag-azure-open-source-fine-tuning.md
│   └── series-2-open-source-rag-end-to-end.md
├── notebooks/
│   ├── README.md
│   └── series-2-open-source-rag.ipynb
├── sample_data/
│   ├── README.md
│   ├── course_ai_guidance.md
│   └── school_ai_policy.md
├── requirements/
│   ├── README.md
│   ├── all.txt
│   └── open-source-rag.txt
└── scripts/
    ├── README.md
    └── verify_notebooks.py
```
  
ドラフト資料は `drafts/` 以下に保存されており、公開インデックス可能になるまではリポジトリ検証でスキップされます。

## シリーズ2検証

Windows上でPython 3.12.6を用いて検証済み。

- `requirements/open-source-rag.txt` を正常にインストール。  
- `notebooks/series-2-open-source-rag.ipynb` を `nbclient` で実行。  
- ローカル検証成功：2つのサンプルドキュメントが読み込まれ、8チャンクが作成され、FastEmbedが384次元のローカル埋め込みを生成、Qdrantのインメモリコレクションが初期化され、8ベクトルが挿入された。  
- テスト質問：「最終課題に生成的AIを使用できますか？」  
- 軽量リランキング後のトップ取得元：`school_ai_policy.md`。  
- 軽量リランキング後のトップ取得セクション：`Final Assignments`。  
- デフォルトの回答経路：ローカルの透過的回答コンポーザー。  
- Ollamaはwinget経由でインストール済み；`phi4-mini:3.8b`を正常に取得。  
- Ollamaでの回答生成経路：`phi4-mini:3.8b`で完了。  
- Ollamaモデルのファイルサイズ：約2.49GB（ディスク上）。  
- Ollama読み込み時のモデルサイズ：`ollama ps`によると3.3GB報告。  
- GPUオフロード：RTX 3060 Laptop GPU 上で `ollama ps` により100% GPU使用報告。  
- 生成後のGPUメモリ観測：約6GB中3.5GB程度。  
- FastEmbedモデルキャッシュおよびOllama生成を有効にしたままノートブックを実行し、検証スクリプトを約34秒で通過。  
- 観察：初期のドキュメント読み込みパスで誤って `sample_data/README.md` が含まれていたが、ノートブックは現在明示的に2つの意図したサンプルドキュメントのみを読み込む。

## リポジトリ検証

- `scripts/verify_notebooks.py` はローカルMarkdownリンク、ノートブックJSON、ノートブック出力のクリーンさ、および高リスクな秘密パターンを検証。  
- `scripts/verify_notebooks.py --execute` はリポジトリルートからパブリックノートブックを実行。  
- `drafts/` 以下のドラフト資料は意図的にスキップ。

## 次の作業

- 将来のシリーズとしてAzure AI SearchおよびAzure OpenAIで同じシナリオを再構築。  
- ローカルおよびAzureの両実装が安定したら、検索と回答評価を追加。

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責事項**：
本書類は AI 翻訳サービス [Co-op Translator](https://github.com/Azure/co-op-translator) を使用して翻訳されています。正確性を期していますが、自動翻訳には誤りや不正確な部分が含まれる可能性があることをご承知おきください。原文の原語版が正式な情報源とみなされるべきです。重要な情報については、専門の人間による翻訳を推奨します。本翻訳の利用により生じたいかなる誤解や解釈違いについても、当方は責任を負いかねます。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->