# あなたのドキュメントに基づいてAIに質問応答を教える
## シリーズ2: ローカルオープンソースRAGシステムのエンドツーエンド構築

![ローカルオープンソースRAGチュートリアルパイプライン](../../../assets/images/series-2-local-rag.svg)

> この記事はシリーズ1のアーキテクチャ議論を実行可能なローカルRAGチュートリアルに変換します。目標は、サンプルデータでフルワークフローをまず構築し、クラウドアカウントやシークレットなしで動作するベースラインを作り、その後より良いアーキテクチャ判断に活用することです。

私たちが構築するシステムは小さな学校方針アシスタントです。私は2つのローカルMarkdownドキュメントを知識ベースとして使用し、その後フルRAGパイプラインを順に説明します：チャンク分割、ローカル埋め込み、Qdrantベクター格納、検索、再ランキング、ソース認識型回答合成、オプションでOllamaとPhi-4-miniによるローカル生成。

シリーズ案内: [リポジトリホーム](../README.md) | 前へ: [シリーズ1 - RAG、Azure対オープンソース代替、ファインチューニングが意味をなす時](./series-1-rag-azure-open-source-fine-tuning.md)

ノートブック: [series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb) | 要件: [open-source-rag.txt](../../../requirements/open-source-rag.txt)

> [!TIP]
> クラウドリソースを作成する前にRAGパイプラインを理解したい場合はここが最良の出発点です。デフォルトのパスはCPUに優しい埋め込みを使い、秘密情報なしでローカルに実行されます。

## 1. 何を構築するのか

2023年のチュートリアルでは、Azureを起点にしました。なぜならAzure AI SearchとAzure OpenAIでPDFドキュメントから質問に答える方法を示すのが目的だったからです。

この2026年シリーズでは、より下のレイヤーから始めたいと思います。

マネージドサービスを使う前に、小さなRAGシステムをローカルで構築し、各ステップを可視化したい：ドキュメントの読み込み、テキストのチャンク分割、ベクターの格納、根拠の検索、再ランキング、ソース認識型回答の返却。

サンプルシナリオは学校方針アシスタントで、ユーザーは以下のように質問します：

```text
Can I use generative AI for my final assignment?
```

システムは一般的なモデルの記憶から答えてはいけません。関連する方針のセクションを検索し、その証拠から回答すべきです。

フルで実行可能なバージョンは[series-2-open-source-rag.ipynb](../notebooks/series-2-open-source-rag.ipynb)にあります。以下のコードは主な手順を示しており、この記事をチュートリアルとして読むことができます。

## 2. ローカル依存関係のインストール

仮想環境を作成し、シリーズ2の要件をインストールします：

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

最初のバージョンではQdrantのローカルモードとFastEmbedを使います。QdrantのPythonクライアントは`QdrantClient(":memory:")`でメモリ内ローカルモードをサポートし、ローカルチュートリアルやCIスタイルの検証に便利です。FastEmbedはクラウドAPIキー不要で実際のローカル埋め込みモデルを提供します。

要件ファイルには`python-dotenv`も含まれており、ノートブックはオプションで`.env`からOllamaモデル名を読み込みます。このローカルチュートリアルにAzure OpenAIやOpenAI APIキーは不要です。

## 3. サンプルドキュメントの読み込み

サンプルコーパスは意図的に小さくしています：

- [school_ai_policy.md](../sample_data/school_ai_policy.md)
- [course_ai_guidance.md](../sample_data/course_ai_guidance.md)

ノートブックでは`sample_data/`からすべてのMarkdownファイルを読み込みます：

```python
from pathlib import Path

repo_root = Path.cwd()
if not (repo_root / "sample_data").exists():
    repo_root = Path.cwd().parent

sample_dir = repo_root / "sample_data"
sample_files = ["course_ai_guidance.md", "school_ai_policy.md"]
documents = []

for file_name in sample_files:
    path = sample_dir / file_name
    documents.append({
        "source": path.name,
        "text": path.read_text(encoding="utf-8"),
    })

print(f"Loaded {len(documents)} documents")
```

私が実行したときは2つのドキュメントが読み込まれました。これは手動で検査するのに十分小さく、RAGパイプライン初期版構築時に有用です。

## 4. Markdown見出しでチャンク分割

次はドキュメントをチャンクに分割するステップです。

このチュートリアルではMarkdown見出しを構造の手がかりとして使います。ドキュメントのタイトルは`#`から、各セクションチャンクは`##`から取ります。

> [!NOTE]
> チャンク分割に万能策はありません。このチュートリアルではサンプルドキュメントが`#`と`##`で明確な構造を持つためMarkdown見出しを用います。PDF、Wordドキュメント、スライド、チケット、ウェブページでは、ページ区切り、レイアウト情報、意味的セクション、トークン制限、表、メタデータなどを活用したほうが良い場合もあります。大切なのは、意味とソースの追跡性を維持できるチャンク化戦略を選ぶことです。

```python
def chunk_markdown(document):
    title = None
    current_heading = None
    current_lines = []
    chunks = []

    def flush():
        if current_heading and current_lines:
            content = "\n".join(current_lines).strip()
            if content:
                chunks.append({
                    "id": f"{document['source']}::{len(chunks)}",
                    "source": document["source"],
                    "title": title or document["source"],
                    "sectionHeading": current_heading,
                    "content": content,
                    "documentVersion": "local-sample-v1",
                    "permissions": ["students", "instructors"],
                })

    for raw_line in document["text"].splitlines():
        line = raw_line.strip()
        if line.startswith("# "):
            title = line[2:].strip()
        elif line.startswith("## "):
            flush()
            current_heading = line[3:].strip()
            current_lines = []
        elif line:
            current_lines.append(line)

    flush()
    return chunks
```

次にこれを各ドキュメントに適用します：

```python
chunks = []
for document in documents:
    chunks.extend(chunk_markdown(document))

print(f"Created {len(chunks)} chunks")
```

私の実行では8チャンクが生成されました。

この手順の良い点はメタデータがすでに有用なことです。各チャンクは`source`、`sectionHeading`、`documentVersion`、プレースホルダ`permissions`を持ちます。小さなチュートリアルでも引用や後日の権限対応検索に役立ちます。

## 5. ローカル埋め込みの作成

最初の公開バージョンではFastEmbed経由で`BAAI/bge-small-en-v1.5`を使います。

これによりチュートリアルはローカルでCPUに優しく保たれますが、単なる疑似ベクター関数ではなく実際の埋め込みモデルを使います。初回実行でモデル重みをダウンロードし、それ以降はローカルキャッシュを再利用します。

> [!NOTE]
> `BAAI/bge-small-en-v1.5`はFastEmbedやQdrantでのローカルチュートリアル向けに適した軽量な英語埋め込みモデルです。384次元のベクトルを作り、高速で安価にローカル実行可能です。他に良い選択肢もあります。2023年は`text-embedding-ada-002`といったホスティング型がよく使われました。現在はOpenAIの`text-embedding-3-small`や`text-embedding-3-large`、オープンソースのBGEやE5、MiniLM、Nomic Embed、多言語の`BAAI/bge-m3`などがあり、用途に応じて適切なモデルを選べます。プロダクションでは自分のドキュメントに対する検索性能評価で適切な埋め込みモデルを選定します。

実用的な代替案：

| モデルファミリー | 検討する状況 |
| --- | --- |
| `text-embedding-ada-002` | 2023年頃の多くのチュートリアルで使われた古いホスティングベースライン。新しいチュートリアルのデフォルトにはおすすめしない。 |
| `text-embedding-3-small` | 強力なコスト/性能バランスを望み、ローカル専用埋め込みが不要な場合の現代的ホスティングデフォルト。 |
| `text-embedding-3-large` | ベクトルサイズや埋め込みコストよりも検索品質重視のホスティング選択肢。 |
| `BAAI/bge-small-en-v1.5` | チュートリアルやプロトタイプ、CPUに優しい実験向けの軽量ローカル英語ベースライン。 |
| `BAAI/bge-base-en-v1.5` / `BAAI/bge-large-en-v1.5` | より良い検索品質が必要でより多くの計算資源を使える場合の大規模ローカル英語モデル。 |
| `BAAI/bge-m3` | 多言語や長文コンテキスト対応検索、特に英語以外のドキュメントを含む場合。 |
| `sentence-transformers/all-MiniLM-L6-v2` | 非常に小型で高速な意味検索ベースライン。速度と単純さ重視の場合に有用。 |
| `nomic-embed-text-v1.5` | 長文コンテキストや移植性重視のセットアップ向けのオープンローカル埋め込み。 |

```python
import re
from fastembed import TextEmbedding

EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"
embedding_model = TextEmbedding(model_name=EMBEDDING_MODEL_NAME)

def tokenize(text):
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    expanded = []
    for token in tokens:
        expanded.append(token)
        if token.endswith("s") and len(token) > 3:
            expanded.append(token[:-1])
    return expanded
```

次に各チャンクに埋め込みを付与：

```python
texts_to_embed = [
    f"{chunk['title']} {chunk['sectionHeading']} {chunk['content']}"
    for chunk in chunks
]
chunk_vectors = list(embedding_model.embed(texts_to_embed))
VECTOR_SIZE = len(chunk_vectors[0])

for chunk, vector in zip(chunks, chunk_vectors):
    chunk["vector"] = vector
```

## 6. Qdrantローカルモードにベクトルを格納

今度はインメモリのQdrantコレクションを作り、チャンクをペイロードメタデータ付きで挿入します。

> [!NOTE]
> 2023年チュートリアルではLangChainでのローカルベクトル類似度検索のデモに単純で人気のあるFAISSを使いました。FAISSは依然として高速ローカル実験に有用です。2026年版では、チュートリアルをより実運用寄りなRAGシステムに近づけるためQdrantを使います。Qdrantはソースファイル、セクション見出し、ドキュメントバージョン、権限といったペイロードメタデータとベクトルを一緒に格納できるため、検索の検査が容易になり、フィルタリング、引用、将来の永続やサーバー展開に備えられます。

FAISSは類似度検索の説明に優れ、Qdrantはより小規模ながら実務向けのRAG検索層を示すのに適しています。

実用的な代替案：

| ベクトルストア / 検索層 | 検討する状況 |
| --- | --- |
| Qdrant | ローカルプロトタイプ、メタデータフィルタリング、実運用向けベクトル検索、Pythonワークフローの単純さ。 |
| Chroma | 単純さ重視のクイックローカルRAG実験やノートブック。 |
| FAISS | 類似度検索のみ必要でメタデータを別管理できる軽量ローカル検索。 |
| Milvus | チームが専用ベクトルDB運用準備ができている大規模オープンソース検索。 |
| Weaviate | スキーマ、メタデータ、ハイブリッド検索対応の管理型・セルフホスト型ベクトル検索。 |
| Azure AI Search | Azure上でキーワード検索、ベクトル検索、ハイブリッド検索、セマンティックランキング、フィルタリング、セキュリティ、管理運用を統合した企業向けRAG。 |
| PostgreSQL + pgvector | すでにPostgreSQLを使うチームがアプリケーションデータに近いベクトル検索を行いたい場合。 |

```python
from qdrant_client import QdrantClient, models

collection_name = "school_policy_local"
client = QdrantClient(":memory:")

client.create_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(
        size=VECTOR_SIZE,
        distance=models.Distance.COSINE,
    ),
)
```

続いてポイントを挿入：

```python
points = []

for idx, chunk in enumerate(chunks):
    payload = {
        key: chunk[key]
        for key in [
            "source",
            "title",
            "sectionHeading",
            "content",
            "documentVersion",
            "permissions",
        ]
    }
    points.append(
        models.PointStruct(
            id=idx,
            vector=chunk["vector"].tolist(),
            payload=payload,
        )
    )

client.upsert(collection_name=collection_name, points=points)
```

私の実行では8つのベクトルが挿入されました。

ここからRAGシステムの検査可能性が増します。ベクトルDBは単にベクトルを保存するだけでなく、根拠テキストや引用に必要なメタデータも格納しています。

## 7. 候補チャンクの検索

質問して候補チャンクを検索します。

```python
question = "Can I use generative AI for my final assignment?"
query_vector = list(embedding_model.embed([question]))[0].tolist()

raw_results = client.query_points(
    collection_name=collection_name,
    query=query_vector,
    limit=5,
    with_payload=True,
).points
```

この時点で、回答生成前に検索されたチャンクを表示します。これは重要です。検索が誤っている場合、生成は流暢なテキストで問題を覆い隠すだけになります。

## 8. 軽量な再ランキングの追加

検索経路を最初にテストしたとき、ベクトル類似度だけで関連方針内容は見つかりましたが、最も正確なセクションが常にトップになっていませんでした。

そこで小さなローカル再ランキング器を追加しました。質問の用語とセクション見出し・本文が重なる場合に重みづけするものです。

```python
query_terms = set(tokenize(question))

def rerank_score(result):
    payload = result.payload
    heading_terms = set(tokenize(payload["sectionHeading"]))
    content_terms = set(tokenize(payload["content"]))
    heading_overlap = len(query_terms & heading_terms)
    content_overlap = len(query_terms & content_terms)
    return result.score + (0.12 * heading_overlap) + (0.02 * content_overlap)

results = sorted(raw_results, key=rerank_score, reverse=True)[:3]
```

再ランキング後、トップ結果は：

```text
school_ai_policy.md / Final Assignments
```

テスト質問に対して期待通りのセクションでした。

これが最初の実装から得た最も有用な教訓でした。小規模ローカル例でもベクトル類似度に別の信号を加えると検索品質が向上しました。

## 9. 根拠を持ったローカル回答の合成

デフォルトパスではLLMではなく透過的なローカル回答合成器を使います。

```python
top = results[0].payload

answer = (
    "Based on the retrieved policy section, students may use generative AI for "
    "brainstorming, outlining, grammar feedback, and code explanation when the "
    "instructor allows it. They should not submit AI-generated work as their own, "
    "and they should include a disclosure when AI tools are used."
)

print("Answer:")
print(answer)
print("\nSource:")
print(f"{top['source']} / {top['sectionHeading']}")
```

これは最終製品の回答生成器ではありません。デバッグ用のツールです。検索、メタデータ、引用連携が正しく機能することを証明し、モデルの不確実性を加える前段階です。

## 10. OllamaとPhi-4-miniによるローカル回答生成

検索が機能したら、ノートブックは最後の回答ステップだけをOllamaと`phi4-mini:3.8b`に置き換えられます。

> [!NOTE]
> Ollamaは回答生成の最終ステップのみ置き換えるべきです。ドキュメント読み込み、チャンク分割、ベクトル格納、検索、再ランキング、引用連携はそのままです。

まず、検索チャンクから証拠プロンプトを作成：

```python
def build_evidence(retrieved_results):
    evidence_blocks = []
    for idx, result in enumerate(retrieved_results, start=1):
        payload = result.payload
        evidence_blocks.append(
            f"[{idx}] Source: {payload['source']} / {payload['sectionHeading']}\n"
            f"{payload['content']}"
        )
    return "\n\n".join(evidence_blocks)

evidence = build_evidence(results)
answer_prompt = (
    "Answer the question using only the evidence below. "
    "If the evidence is insufficient, say that the provided documents do not contain enough information. "
    "End with a Sources line that lists the source file and section.\n\n"
    f"Question: {question}\n\nEvidence:\n{evidence}"
)
```

このチュートリアルでは、ローカル生成のデフォルトとしてMicrosoftのPhi-4-miniシリーズをOllama経由で推奨します。私がテストしたモデル名は：

```powershell
ollama pull phi4-mini:3.8b
```

モデルの利用可能性を素早くチェック：

```powershell
ollama list
```

変数を設定：

```powershell
Copy-Item .env.example .env
```

`.env`を開き、シリーズ2用Ollamaの値をコメント解除：

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

ノートブックは`python-dotenv`でリポジトリルートの`.env`を読み込み、同じ証拠プロンプトをOllamaのローカル`/api/chat`エンドポイントにストリーミングなしで送信します。Ollamaが起動していないか`SERIES2_OLLAMA_MODEL`が無い場合、このトラックはスキップされます。

> [!NOTE]
> このマシンでは`phi4-mini:3.8b`は約2.49GBのモデルファイルをダウンロードしました。推論中は3.3GBのロード済モデルサイズを報告し、RTX 3060 Laptop GPUを使用しました。

このチュートリアルは2段階を提供します：

1. CPUのみの決定論的回答合成器。
2. OllamaとPhi-4-miniによるローカル回答生成。

検索パイプラインは両方とも同じです。

## 11. 検証結果

私はWindowsのPython 3.12.6でローカル実行しました。

インストール済みパッケージ：

| パッケージ | バージョン |
| --- | --- |
| `qdrant-client` | `1.18.0` |
| `fastembed` | `0.8.0` |
| `python-dotenv` | `1.2.2` |
| `nbclient` | `0.10.4` |
| `nbformat` | `5.10.4` |
| `ipykernel` | `7.2.0` |
| `numpy` | `2.4.6` |

ノートブック実行：

- ノートブック: `notebooks/series-2-open-source-rag.ipynb`
- 実行結果: `nbclient`で合格
- 読み込んだドキュメント数: 2
- 作成したチャンク数: 8
- Qdrantコレクション名: `school_policy_local`
- 挿入済みベクトル数: 8
- 埋め込みモデル: `BAAI/bge-small-en-v1.5`
- 埋め込みサイズ: 384
- 検索クエリ: 「最終課題に生成AIを使ってもいいですか？」
- 再ランキング手法: 軽量ローカル語彙再ランキング
- 再ランキング後の最上位取得ソース: `school_ai_policy.md`
- 再ランキング後の最上位セクション: `Final Assignments`
- デフォルト回答生成手法: ローカル透明回答コンポーザー
- Ollama生成手法: `phi4-mini:3.8b` による完了
- Ollamaモデルファイルサイズ: ディスク上で2.49GB
- Ollamaロード済みモデルサイズ: `ollama ps`による3.3GB報告
- GPUオフロード: `ollama ps`で100% GPU使用報告
- 生成後のGPUメモリ使用状況: RTX 3060 Laptop GPU上で約6GB中3.5GB使用
- キャッシュ済みFastEmbedモデルおよびOllama生成有効のノートブック実行: 検証スクリプトで約34秒で通過

Ollama生成の回答は以下の通りでした:

```text
Based on the provided documents [1], you can indeed utilize generative AI tools as part of your final assignment if explicitly permitted by an instructor in a specified guide (such as brainstorming assistance), but it must not be submitted as entirely generated work without proper disclosure regarding its usage.

For comparison, reviewing drafts for readability improvement or practicing explanation techniques may also fall under the allowed uses [2].

Additionally, generative AI can assist with summarizing background materials and generating search keywords in research projects. However, you are responsible to verify sources manually while citing original references as noted in document 3 ([school_ai_policy.md / Research Projects]).

SOURCES: school_ai_policy.md; course_ai_guidance.md; [specific sections mentioned for each relevant guideline].
```

この回答を完璧とは言えません。正しい証拠から答えていますが、最終的なソース行が決定論的な引用形式ほど正確ではありません。これはチュートリアルで示すのに役立ちます。なぜなら、次の工学的な課題が明白になるからです：回答生成も評価が必要であり、検索だけではないということです。

検証中に学んだ主なことは、回答生成の前に検索品質を確認するべきだということです。埋め込み結果はすでに有用であり、軽量再ランキングは期待されるポリシーのセクションを確実に最初に表示しました。これこそ、チュートリアルで隠すのではなく公開したい小さなシステムの挙動です。

## 12. 次に来るもの

次の改善点は、このローカル設定を同じ学校ポリシーアシスタントシナリオの管理されたAzureバージョンと比較することです。シナリオを固定することで、設定の複雑さ、検索制御、ID統合、運用所有権、コストなどのトレードオフが見えやすくなります。

## 13. 参考文献

- [Qdrant Pythonクライアント クイックスタート](https://python-client.qdrant.tech/quickstart.html)
- [Qdrantクライアント GitHubリポジトリ](https://github.com/qdrant/qdrant-client)
- [FastEmbed対応モデル](https://qdrant.github.io/fastembed/examples/Supported_Models/)
- [OpenAI埋め込みガイド](https://platform.openai.com/docs/guides/embeddings)
- [BAAI/bge-small-en-v1.5 モデルカード](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [BAAI/bge-m3 モデルカード](https://huggingface.co/BAAI/bge-m3)
- [sentence-transformers/all-MiniLM-L6-v2 モデルカード](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Ollama phi4-mini モデルページ](https://ollama.com/library/phi4-mini)
- [Ollama Windows ドキュメント](https://docs.ollama.com/windows)
- [Ollama API ストリーミングドキュメント](https://docs.ollama.com/api/streaming)
- [Microsoft Phi-4-mini-instruct モデルカード](https://huggingface.co/microsoft/Phi-4-mini-instruct)
- [LangGraph 概要](https://docs.langchain.com/oss/python/langgraph)
- [RAG入門 - LlamaIndex](https://docs.llamaindex.ai/en/stable/understanding/rag/)

前へ: [シリーズ1](./series-1-rag-azure-open-source-fine-tuning.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責事項**：
本書類は AI 翻訳サービス [Co-op Translator](https://github.com/Azure/co-op-translator) を使用して翻訳されています。正確性を期していますが、自動翻訳には誤りや不正確な部分が含まれる可能性があることをご承知おきください。原文の原語版が正式な情報源とみなされるべきです。重要な情報については、専門の人間による翻訳を推奨します。本翻訳の利用により生じたいかなる誤解や解釈違いについても、当方は責任を負いかねます。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->