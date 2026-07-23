import os, sys
from pymilvus import MilvusClient, AnnSearchRequest, RRFRanker
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

    def hybrid_search(self, msg:str , hybrid_top_K:int=30, filter_expr:str = "") -> list[dict[str,Any]]:
        dense_embedding , sparse_embedding = do_embedding(msg)

        dense_request = AnnSearchRequest(
            data=[dense_embedding],
            anns_field="dense_embedding",
            param={"metric_type":"COSINE", "params": {}},
            limit=hybrid_top_K *3,
            expr=filter_expr or None,
        )

        sparse_request = AnnSearchRequest(
            data=[sparse_embedding],
            anns_field="sparse_embedding",
            param={"metric_type":"IP", "params": {}},
            limit=hybrid_top_K *3,
            expr=filter_expr or None,
        )

        result = sorted(self.client.hybrid_search(
            collection_name=self.collection_name,
            reqs=[dense_request, sparse_request],
            ranker=RRFRanker(),
            output_fields=[
                "text",
                "metadata",
                "source_file",
                "title",
                "chunk_index",
                "header_path",
            ],
        )[0], key=lambda x: float(x['distance']), reverse=True)[:hybrid_top_K]

        return result if result else []

    def cross_rerank(self, query:str, candidates:list[dict[str,Any]], top_k:int=5) -> list[dict[str,Any]]:
        if not candidates:
            return []

        candidate_texts = [candidate['entity']['text'] for candidate in candidates]
        scores = self.reranker.predict([(query, text) for text in candidate_texts])
        scored_candidates = [
            {**candidate, 'score': score}
            for candidate, score in zip(candidates, scores)
        ]
        scored_candidates.sort(key=lambda x: x['score'], reverse=True)
        return scored_candidates[:top_k]