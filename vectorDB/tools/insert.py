import os ,sys
from pymilvus import MilvusClient
from typing import Optional, Any

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from vectorDB.milvus_manager.milvus_manager import get_milvus_client

client: Optional[MilvusClient] = None
client = get_milvus_client()
if client is None:
    raise Exception("Failed to initialize Milvus client")

def insert_to_collection(collection_name:str , datas:list[dict[str,Any]] , batch_size:int = 1000)-> bool:
    insert_count=0
    total = len(datas)
    print("datas type:", type(datas))
    print(f"datas count:{total}")

    for start in range(0, total, batch_size):
        end = min(start + batch_size, total)
        batch = datas[start:end]
        result = client.insert(collection_name=collection_name, data=batch)
        insert_count += len(batch)

        print(
            f"Inserted batch: {start} ~ {end - 1}, "
            f"progress: {insert_count}/{total}, "
            f"result: {result}"
        )

    print("all inserted successfully\n Flush the data to ensure it's written to disk.")
    client.flush(collection_name=collection_name)
    print("Flush completed successfully.")
    return True

