from pymilvus import MilvusClient
from typing import Optional
_client: Optional[MilvusClient] = None



def init_milvus():
    global _client
    server_url = "http://localhost:19530"
    _client = MilvusClient(server_url,token='root:Milvus')


def get_schema_config():
    _client = get_milvus_client()

    schema = _client.create_schema(
        auto_id=True,
        enable_dynamic_field=False,
    )
    return schema

def get_milvus_client():
    if _client is None:
        init_milvus()
    return _client
