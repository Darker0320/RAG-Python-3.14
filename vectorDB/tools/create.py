import os
from pymilvus import MilvusClient , DataType , CollectionSchema
from typing import Optional
import json

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
conf_path = os.path.join(project_root, 'conf')
conf = os.path.join(conf_path, 'schema.json')
if not os.path.exists(conf) or not conf.endswith('.json'):
    raise FileNotFoundError(f"Schema format file not found: {conf}")

type_mapping = {
    "INT64": DataType.INT64,
    "FLOAT_VECTOR": DataType.FLOAT_VECTOR,
    "VARCHAR": DataType.VARCHAR,
    "JSON": DataType.JSON,
}

from vectorDB.milvus_manager.milvus_manager import get_milvus_client

client: Optional[MilvusClient] = None
client = get_milvus_client()
if client is None:
    raise Exception("Failed to initialize Milvus client")

def gen_schema_format() -> CollectionSchema:
    with open(conf,'r',encoding='utf-8') as f:
        schema_format = json.load(f)
        for field in schema_format.get("fields", []):
            field_type = field.get("type")
            if field_type not in type_mapping:
                raise ValueError(f"Unsupported data type: {field_type}")
            field["type"] = type_mapping[field_type.upper()]

    return CollectionSchema.construct_from_dict(schema_format)

def create_collection(collection_name:str , schema:CollectionSchema):
    if client.has_collection(collection_name):
        print(f"Collection '{collection_name}' already exists.")
    else:
        client.create_collection(collection_name=collection_name, schema=schema)
        print(f"Collection '{collection_name}' created successfully.")

    if not client.list_indexes(collection_name=collection_name):
        create_index(collection_name)
        print(f"Index on 'embedding' created for '{collection_name}'.")

def create_index(collection_name:str) -> bool:
    index_params =  client.prepare_index_params()
    index_params.add_index(
        field_name="embedding",
        index_type="IVF_FLAT",
        metric_type="L2",
        params={"nlist": 128},
    )
    client.create_index(collection_name=collection_name, index_params=index_params)
    return True
