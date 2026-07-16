from __future__ import annotations

from typing import Any

from pymilvus import MilvusClient
from sentence_transformers import SentenceTransformer


MILVUS_URI = "http://localhost:19530"
MILVUS_TOKEN = "root:Milvus"
DATABASE_NAME = "default"  # 這裡是你在 Milvus 中使用的資料庫名稱

COLLECTION_NAME = "python3_14"

# 必須和建立 Markdown embedding 時使用的模型相同
EMBEDDING_MODEL = "BAAI/bge-m3"

VECTOR_FIELD = "embedding"

# 依照你的 schema 調整
OUTPUT_FIELDS = [
    "source_file",
    "chunk_index",
    "text",
]


def create_client() -> MilvusClient:
    """建立 Milvus client。"""
    return MilvusClient(
        uri=MILVUS_URI,
        token=MILVUS_TOKEN,
        db_name=DATABASE_NAME,
    )


def load_embedding_model() -> SentenceTransformer:
    """載入與資料匯入時相同的 embedding model。"""
    print(f"Loading embedding model: {EMBEDDING_MODEL}")

    model = SentenceTransformer(
        EMBEDDING_MODEL,
        trust_remote_code=True,
    )

    print("Embedding model loaded.")
    return model


def verify_collection(
    client: MilvusClient,
    collection_name: str,
) -> bool:
    """檢查 collection 是否存在並顯示基本資訊。"""
    if not client.has_collection(collection_name=collection_name):
        print(f"Collection does not exist: {collection_name}")
        return False

    description = client.describe_collection(
        collection_name=collection_name,
    )

    stats = client.get_collection_stats(
        collection_name=collection_name,
    )

    print("\nCollection information")
    print("-" * 60)
    print(f"name      : {collection_name}")
    print(f"row count : {stats.get('row_count')}")
    print(f"loaded    : {client.get_load_state(collection_name)}")

    fields = description.get("fields", [])

    print("\nFields:")

    for field in fields:
        print(
            f"  - name={field.get('name')}, "
            f"type={field.get('type')}, "
            f"dimension={field.get('params', {}).get('dim')}"
        )

    return True


def encode_query(
    model: SentenceTransformer,
    query: str,
) -> list[float]:
    """
    將查詢文字轉換成 embedding。

    normalize_embeddings 的設定必須盡量與匯入資料時一致。
    """
    embedding = model.encode(
        query,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    return embedding.tolist()


def search_markdown(
    client: MilvusClient,
    model: SentenceTransformer,
    query: str,
    top_k: int = 5,
) -> list[dict[str, Any]]:
    """搜尋與問題最相近的 Markdown chunks。"""
    query_vector = encode_query(model, query)

    results = client.search(
        collection_name=COLLECTION_NAME,
        data=[query_vector],
        anns_field=VECTOR_FIELD,
        limit=top_k,
        output_fields=OUTPUT_FIELDS,
        search_params={
            # 必須與 index 使用的 metric 相容
            "metric_type": "L2",
            "params": {},
        },
    )

    if not results:
        return []

    return results[0]


def print_search_results(
    query: str,
    results: list[dict[str, Any]],
) -> None:
    """顯示搜尋結果。"""
    print("\n")
    print("=" * 80)
    print(f"Query: {query}")
    print("=" * 80)

    if not results:
        print("No results found.")
        return

    for rank, result in enumerate(results, start=1):
        entity = result.get("entity", {})

        source_file = entity.get("source_file", "<unknown>")
        chunk_index = entity.get("chunk_index", "<unknown>")
        text = entity.get("text", "")

        # 部分 PyMilvus 版本使用 distance，部分結果可能含 score
        score = result.get(
            "distance",
            result.get("score", "<unknown>"),
        )

        print(f"\n[{rank}] score/distance: {score}")
        print(f"source_file          : {source_file}")
        print(f"chunk_index          : {chunk_index}")
        print("-" * 80)
        print(text)
        print("-" * 80)


def inspect_raw_records(
    client: MilvusClient,
    limit: int = 5,
) -> None:
    """
    不進行向量搜尋，直接查看 Milvus 裡儲存的資料。

    用來確認 source_file、chunk_index、text 是否真的有寫進去。
    """
    records = client.query(
        collection_name=COLLECTION_NAME,
        filter="",
        output_fields=OUTPUT_FIELDS,
        limit=limit,
    )

    print("\nRaw records")
    print("=" * 80)

    for index, record in enumerate(records, start=1):
        print(f"\nRecord {index}")
        print(f"source_file : {record.get('source_file')}")
        print(f"chunk_index : {record.get('chunk_index')}")
        print(f"text        : {record.get('text', '')[:500]}")


def interactive_search(
    client: MilvusClient,
    model: SentenceTransformer,
) -> None:
    """互動式測試 Markdown 檢索。"""
    print("\nMilvus Markdown retrieval test")
    print("輸入問題進行搜尋，輸入 exit 離開。")

    while True:
        try:
            query = input("\nQuestion > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExit.")
            break

        if query.lower() in {"exit", "quit", "q"}:
            print("Exit.")
            break

        if not query:
            continue

        try:
            results = search_markdown(
                client=client,
                model=model,
                query=query,
                top_k=5,
            )

            print_search_results(query, results)

        except Exception as error:
            print(f"Search failed: {error}")


def main() -> None:
    client = create_client()

    try:
        if not verify_collection(
            client=client,
            collection_name=COLLECTION_NAME,
        ):
            return

        # 先確認原始欄位是否真的存在
        inspect_raw_records(
            client=client,
            limit=3,
        )

        model = load_embedding_model()

        interactive_search(
            client=client,
            model=model,
        )

    except Exception as error:
        print(f"Milvus verification failed: {error}")

    finally:
        client.close()


if __name__ == "__main__":
    main()