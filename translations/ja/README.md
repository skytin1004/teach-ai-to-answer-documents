# ドキュメントに基づいて質問に答えるAIを教える

このリポジトリは、2026年のブログシリーズを収集しており、RAG、Azure AIサービス、オープンソース代替、評価指向のワークフローを用いたドキュメントに基づくAIシステムの構築について取り扱っています。

## 背景

2023年に、Azure AI Search と Azure OpenAI を使ってPDFドキュメントからの質問にChatGPTが答える方法を教えるチュートリアルを2本作成しました。その当時は「データ上のChatGPT」という考え方はまだ新しかったように感じられ、実践的なワークフローを示すことが目的でした。すなわち、ドキュメントを保存し、インデックス化し、関連コンテンツを検索し、その取得された文脈から回答を生成するという流れです。

2026年には、RAGのエコシステムははるかに大きくなっています。Azure AI Searchは最新のベクトル検索とハイブリッド検索パターンをサポートし、Azure OpenAIはより広範なMicrosoft Foundry Modelsエコシステムの一部となり、LangGraph、LlamaIndex、Haystack、Qdrant、Milvus、Weaviate、Chroma、Ollama、vLLMといったオープンソースツールは実際のシステムに使える選択肢となっています。

このため、このテーマを改めて取り上げたいと思いました。もはや「RAGをどう作るか」だけが問題ではなく、多様な作り方の中で「自分の状況にどのアーキテクチャを選ぶべきか」がより重要な問いとなっています。

このシリーズはその意思決定の層から始まります。実装に深く入る前に、なぜAIサービスが検索を必要とするのか、Azureベースのマネージドサービスが有効な場合はいつか、オープンソース代替はどんな場合に適しているか、ファインチューニングはどこに位置づけられるのかを考察します。

## 記事一覧

1. [シリーズ1: RAG、Azureとオープンソース代替、ファインチューニングが有効な場合](./series-1-rag-azure-open-source-fine-tuning.md)

## 多言語サポート

### Co-op Translatorを利用して対応（自動かつ常に最新）

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[アラビア語](../ar/README.md) | [ベンガル語](../bn/README.md) | [ブルガリア語](../bg/README.md) | [ビルマ語（ミャンマー）](../my/README.md) | [中国語（簡体字）](../zh-CN/README.md) | [中国語（繁体字、香港）](../zh-HK/README.md) | [中国語（繁体字、マカオ）](../zh-MO/README.md) | [中国語（繁体字、台湾）](../zh-TW/README.md) | [クロアチア語](../hr/README.md) | [チェコ語](../cs/README.md) | [デンマーク語](../da/README.md) | [オランダ語](../nl/README.md) | [エストニア語](../et/README.md) | [フィンランド語](../fi/README.md) | [フランス語](../fr/README.md) | [ドイツ語](../de/README.md) | [ギリシャ語](../el/README.md) | [ヘブライ語](../he/README.md) | [ヒンディー語](../hi/README.md) | [ハンガリー語](../hu/README.md) | [インドネシア語](../id/README.md) | [イタリア語](../it/README.md) | [日本語](./README.md) | [カンナダ語](../kn/README.md) | [クメール語](../km/README.md) | [韓国語](../ko/README.md) | [リトアニア語](../lt/README.md) | [マレー語](../ms/README.md) | [マラヤーラム語](../ml/README.md) | [マラーティー語](../mr/README.md) | [ネパール語](../ne/README.md) | [ナイジェリア・ピジン](../pcm/README.md) | [ノルウェー語](../no/README.md) | [ペルシア語（ファルシ）](../fa/README.md) | [ポーランド語](../pl/README.md) | [ポルトガル語（ブラジル）](../pt-BR/README.md) | [ポルトガル語（ポルトガル）](../pt-PT/README.md) | [パンジャブ語（グルムキー）](../pa/README.md) | [ルーマニア語](../ro/README.md) | [ロシア語](../ru/README.md) | [セルビア語（キリル文字）](../sr/README.md) | [スロバキア語](../sk/README.md) | [スロベニア語](../sl/README.md) | [スペイン語](../es/README.md) | [スワヒリ語](../sw/README.md) | [スウェーデン語](../sv/README.md) | [タガログ語（フィリピン）](../tl/README.md) | [タミル語](../ta/README.md) | [テルグ語](../te/README.md) | [タイ語](../th/README.md) | [トルコ語](../tr/README.md) | [ウクライナ語](../uk/README.md) | [ウルドゥー語](../ur/README.md) | [ベトナム語](../vi/README.md)

> **ローカルでクローンしたいですか？**
>
> このリポジトリには50以上の言語の翻訳が含まれており、ダウンロードサイズが大きくなります。翻訳なしでクローンするにはスパースチェックアウトを利用してください：
>
> **Bash / macOS / Linux:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (Windows):**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> こうすると、コースを完了するために必要なものがすべて得られ、ダウンロードがはるかに高速になります。
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責事項**：
本書類は AI 翻訳サービス [Co-op Translator](https://github.com/Azure/co-op-translator) を使用して翻訳されています。正確性を期していますが、自動翻訳には誤りや不正確な部分が含まれる可能性があることをご承知おきください。原文の原語版が正式な情報源とみなされるべきです。重要な情報については、専門の人間による翻訳を推奨します。本翻訳の利用により生じたいかなる誤解や解釈違いについても、当方は責任を負いかねます。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->