import os, sys

from pymilvus import MilvusClient
from typing import Optional

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from vectorDB.milvus_manager.milvus_manager import get_milvus_client

client: Optional[MilvusClient] = None
client = get_milvus_client()
if client is None:
    raise Exception("Failed to initialize Milvus client")

def load_collection(collection_name:str)-> bool:
    print("loading collection...")
    client.load_collection(collection_name=collection_name,timeout=3600.0)

    return True