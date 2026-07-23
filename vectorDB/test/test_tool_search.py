import os, sys
file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if file_path not in sys.path:
    sys.path.append(file_path)

from tools.search import RAGRetriever

def test_tool_search():
    # Test the search functionality
    retriever = RAGRetriever(collection_name="python3_14")
    msg= "How about use dict in python3.14 version . "
    search_results = retriever.hybrid_search(msg=msg, hybrid_top_K=30, filter_expr="")
    reranked_results = retriever.cross_rerank(query=msg, candidates=search_results, top_k=5)
    assert reranked_results is not None

