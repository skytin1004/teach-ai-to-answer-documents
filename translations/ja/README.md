# ドキュメントに基づいてAIに質問への回答を教える

![ドキュメントに基づくAI RAGシステム概要](../../assets/images/readme-hero.svg)

このリポジトリは、RAG、Azure AIサービス、オープンソース代替、および評価指向ワークフローを使用したドキュメントに基づくAIシステム構築に関する2026年のブログシリーズをまとめたものです。

## 背景

2023年には、Azure AI SearchとAzure OpenAIを使ってPDFドキュメントから質問に答えるChatGPTの教育に関する一連のチュートリアルを制作しました。「データ上のChatGPT」という考え方はその当時まだ新鮮で、実用的なワークフロー：ドキュメントを保存し、インデックスを作成し、関連コンテンツを取り出し、その取り出したコンテキストから回答を生成する方法を示すことが目的でした。

2026年になると、RAGエコシステムは格段に大きくなりました。Azure AI Searchは最新のベクトルおよびハイブリッド検索パターンをサポートし、Azure OpenAIはより広範なMicrosoft Foundry Modelsエコシステムの一部となり、LangGraph、LlamaIndex、Haystack、Qdrant、Milvus、Weaviate、Chroma、Ollama、vLLMなどのオープンソースツールが実践的な選択肢として現実的になっています。

だからこそ、このテーマを再検討したいと考えました。もはや「RAGをどう作るか？」だけが問われるのではなく、多様な構築方法が存在し、「自分の状況に最適なアーキテクチャは何か？」というより重要な問いに変わっています。

このシリーズはその意思決定層から出発し、実践的なチュートリアルへと展開します。最初の実装パスは、サンプルデータ、Qdrant、Ollama、Phi-4-miniを使って誰でも実行できるローカルのオープンソースRAGシステムを構築します。

## 記事

記事のインデックスは[articles/README.md](./articles/README.md)を参照してください。

1. [シリーズ1：RAG、Azure対オープンソース代替、ファインチューニングが有効な場合](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [シリーズ2：ローカルオープンソースRAGシステムをエンドツーエンドで構築](./articles/series-2-open-source-rag-end-to-end.md)

今後予定していること：

- 同じRAGシステムをAzure AI SearchとAzure OpenAIで再構築。
- デモ回答を超えた評価と回帰チェックを追加。

## ノートブック

実装記事は、検索および評価ステップを直接検査できるようノートブックを使用しています。[notebooks/README.md](./notebooks/README.md)でフォルダレベルの案内を確認してください。

> [!TIP]
> 最速のルートを望む場合はシリーズ2から始めてください。これはサンプルデータ、CPU対応の埋め込み、Qdrantローカルモード、クラウドクレデンシャル不要でローカル実行できます。

| シリーズ | ノートブック | 要件 | ローカル検証 |
| --- | --- | --- | --- |
| シリーズ2 | [オープンソースRAGノートブック](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Qdrantローカルモード、検索、再ランキング、ソース配線が検証済み |

ノートブックをローカルで実行するには、仮想環境を作成し該当の要件ファイルをインストールしてください。例：

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## サンプルデータ

ノートブックは、プライベートドキュメントやクラウド資格情報なしで実行できるよう、[sample_data](../../sample_data)内の小規模なローカルコーパスを使用します。[sample_data/README.md](./sample_data/README.md)を参照してください。

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## ローカル検証の概要

検証結果は各記事および[SERIES_PLAN.md](./SERIES_PLAN.md)に記録されています。

| 領域 | 結果 |
| --- | --- |
| シリーズ2オープンソースパス | FastEmbedが384次元のローカル埋め込みを生成、Qdrantのインメモリコレクションに8ベクトル挿入、軽量の再ランキングで期待されたセクションを検索、オプションのOllama生成は`phi4-mini:3.8b`で完了 |

ローカルノートブックは意図的にハードコードされたシークレットを避けています。

## ローカルOllama生成

シリーズ2ノートブックはデフォルトでローカル安全です。ローカルOllama生成を有効にするには、[.env.example](../../.env.example)を`.env`にコピーしシリーズ2用の値を入力してください。

シリーズ2のOllama生成を有効にするには、以下をコメント解除してください：

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

シリーズ2ノートブックは`python-dotenv`を使用してリポジトリルートから自動的に`.env`を読み込みます。

> [!IMPORTANT]
> `.env`ファイル、APIキー、プライベートエンドポイント、テナント固有の値はコミットしないでください。本リポジトリは意図的にMarkdownファイルやノートブックからシークレットを排除しています。

要件ファイルは[requirements/README.md](./requirements/README.md)で説明されています。

リンク検証、ノートブック構造、ノートブックの出力のクリーンさ、高リスクなシークレットパターンの検出には：

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

検証スクリプトは[scripts/README.md](./scripts/README.md)に記載されています。

同じ環境でローカル安全なノートブックをすべて実行するには：

```powershell
python scripts\verify_notebooks.py --execute
```

この検証フローはGitHub Actionsでもプッシュ、プルリクエスト、手動ワークフロードメインで実行されます。ドラフト記事やノートブックは公開検証パスから意図的に除外されています。

更新を公開する前には[PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md)を使用してください。

未公開の変更概要は[CHANGELOG.md](./CHANGELOG.md)でご覧いただけます。

貢献およびノートブック衛生ガイドラインは[CONTRIBUTING.md](./CONTRIBUTING.md)を参照してください。

## 多言語対応

### Co-op Translatorによるサポート（自動かつ常に最新）

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[アラビア語](../ar/README.md) | [ベンガル語](../bn/README.md) | [ブルガリア語](../bg/README.md) | [ビルマ語（ミャンマー）](../my/README.md) | [中国語（簡体字）](../zh-CN/README.md) | [中国語（繁体字・香港）](../zh-HK/README.md) | [中国語（繁体字・マカオ）](../zh-MO/README.md) | [中国語（繁体字・台湾）](../zh-TW/README.md) | [クロアチア語](../hr/README.md) | [チェコ語](../cs/README.md) | [デンマーク語](../da/README.md) | [オランダ語](../nl/README.md) | [エストニア語](../et/README.md) | [フィンランド語](../fi/README.md) | [フランス語](../fr/README.md) | [ドイツ語](../de/README.md) | [ギリシャ語](../el/README.md) | [ヘブライ語](../he/README.md) | [ヒンディー語](../hi/README.md) | [ハンガリー語](../hu/README.md) | [インドネシア語](../id/README.md) | [イタリア語](../it/README.md) | [日本語](./README.md) | [カンナダ語](../kn/README.md) | [クメール語](../km/README.md) | [韓国語](../ko/README.md) | [リトアニア語](../lt/README.md) | [マレー語](../ms/README.md) | [マラヤーラム語](../ml/README.md) | [マラーティー語](../mr/README.md) | [ネパール語](../ne/README.md) | [ナイジェリア・ピジン](../pcm/README.md) | [ノルウェー語](../no/README.md) | [ペルシア語（ファルシ）](../fa/README.md) | [ポーランド語](../pl/README.md) | [ポルトガル語（ブラジル）](../pt-BR/README.md) | [ポルトガル語（ポルトガル）](../pt-PT/README.md) | [パンジャブ語（グルムキー）](../pa/README.md) | [ルーマニア語](../ro/README.md) | [ロシア語](../ru/README.md) | [セルビア語（キリル）](../sr/README.md) | [スロバキア語](../sk/README.md) | [スロベニア語](../sl/README.md) | [スペイン語](../es/README.md) | [スワヒリ語](../sw/README.md) | [スウェーデン語](../sv/README.md) | [タガログ語（フィリピン）](../tl/README.md) | [タミル語](../ta/README.md) | [テルグ語](../te/README.md) | [タイ語](../th/README.md) | [トルコ語](../tr/README.md) | [ウクライナ語](../uk/README.md) | [ウルドゥー語](../ur/README.md) | [ベトナム語](../vi/README.md)

> **ローカルでクローンしたいですか？**
>
> 本リポジトリには50以上の言語翻訳が含まれており、ダウンロードサイズが大幅に増加します。翻訳なしでクローンするにはスパースチェックアウトを使用してください：
>
> **Bash / macOS / Linux:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD（Windows）:**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> これにより、コースを完了するために必要なすべてが含まれ、ずっと高速なダウンロードになります。
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責事項**：
本書類は AI 翻訳サービス [Co-op Translator](https://github.com/Azure/co-op-translator) を使用して翻訳されています。正確性を期していますが、自動翻訳には誤りや不正確な部分が含まれる可能性があることをご承知おきください。原文の原語版が正式な情報源とみなされるべきです。重要な情報については、専門の人間による翻訳を推奨します。本翻訳の利用により生じたいかなる誤解や解釈違いについても、当方は責任を負いかねます。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->