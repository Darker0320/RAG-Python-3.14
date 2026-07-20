import os, sys
file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if file_path not in sys.path:
    sys.path.append(file_path)

from tools.search import RAGRetriever

def test_tool_search():
    # Test the search functionality
    retriever = RAGRetriever(collection_name="python3_14")
    search_results = retriever.search(msg="How about use dict in python. ", limit=10, filter_expr="")
    assert search_results is not None
