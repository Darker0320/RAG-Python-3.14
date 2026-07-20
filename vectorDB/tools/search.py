import os, sys
import numpy as np
from pymilvus import MilvusClient
from typing import Optional, Any
import torch
from sentence_transformers import CrossEncoder

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from vectorDB.milvus_manager.milvus_manager import get_milvus_client
from clean_doc.embedding.embedding import do_embedding

RERANKER_MODEL_NAME = "BAAI/bge-reranker-v2-m3"
reranker = CrossEncoder(model_name_or_path=RERANKER_MODEL_NAME , device='cuda')


client: Optional[MilvusClient] = None


class RAGRetriever:
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.reranker = CrossEncoder(
            model_name_or_path=RERANKER_MODEL_NAME,
            device='cuda',
            model_kwargs={"torch_dtype": torch.bfloat16,}
        )
        self.client = get_milvus_client()
        if self.client is None:
            raise Exception("Failed to initialize Milvus client")

    def search(self, msg:str , limit:int=10, filter_expr:str = "") -> list[dict[str,Any]]:
        query_embedding = do_embedding(msg)
        search_kwargs = {
            "collection_name": self.collection_name,
            "data": [query_embedding],
            "limit": limit,
            "output_fields": [
                "text",
                "metadata",
                "source_file",
                "title",
                "chunk_index",
                "header_path",
            ],
        }
        if filter_expr:
            search_kwargs["filter"] = filter_expr
        results = self.client.search(**search_kwargs)
        return  results if results else []

    def rerank(self, msg:str , candidates:list[dict[str, Any]] , top_k:int = 5 , min_score:float = 0.15) -> list[dict[str, Any]]:
        prepared: list[tuple[str, str]] = [
            (msg , candidate["text"]) for candidate in candidates[0]
        ]
        scores = self.reranker.predict(prepared,batch_size=top_k,show_progress_bar=False,convert_to_numpy=True)
        scores = np.asarray(scores).reshape(-1)
        reranked: list[dict[str, Any]] = []

        for candidate, score in zip(candidates[0], scores):
            item = candidate.copy()
            item["rerank_score"] = float(score)
            if score >= min_score:
                reranked.append(item)

        reranked = sorted(
            reranked,
            key=lambda item: item["rerank_score"],
            reverse=True,
        )[:top_k]
        return reranked